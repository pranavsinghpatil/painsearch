"""Validate and safely mutate the versioned PainSearch registry.

Usage:
  python src/registry.py validate
  python src/registry.py list
  python src/registry.py show P0002
  python src/registry.py transition P0002 --to validated --actor alice --reason "Evidence reproduced"
  python src/registry.py export --status investigating
"""
import argparse
import copy
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - exercised in environments without dependencies
    raise SystemExit("Missing dependency: install requirements.txt before using the registry CLI") from exc


FORMAT_CHECKER = FormatChecker()


@FORMAT_CHECKER.checks("date-time", raises=(TypeError, ValueError))
def is_rfc3339_datetime(value):
    """jsonschema does not register date-time in every installation."""
    if not isinstance(value, str) or "T" not in value:
        return False
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.tzinfo is not None


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry" / "registry.json"
SCHEMA = ROOT / "registry" / "schema" / "problem-registry-v1.json"
STATUSES = {"candidate", "investigating", "validated", "rejected", "unresolved"}
TRANSITIONS = {
    "candidate": {"investigating", "validated", "rejected", "unresolved"},
    "investigating": {"validated", "rejected", "unresolved"},
    "unresolved": {"investigating", "validated", "rejected"},
    "validated": {"investigating", "rejected"},
    "rejected": {"investigating"},
}


class RegistryValidationError(ValueError):
    """Raised when the registry fails schema or semantic validation."""


def load_json(path):
    try:
        with Path(path).open(encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise RegistryValidationError(f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    except OSError as exc:
        raise RegistryValidationError(f"{path}: {exc}") from exc


def schema_errors(data):
    schema = load_json(SCHEMA)
    validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.append(f"{path}: {error.message}")
    return errors


def semantic_errors(data):
    """Validate relationships JSON Schema cannot express by itself."""
    errors = []
    problem_ids = set()
    evidence_ids = set()
    investigation_ids = set()
    for problem in data.get("problems", []) if isinstance(data, dict) else []:
        pid = problem.get("id") if isinstance(problem, dict) else None
        if pid in problem_ids:
            errors.append(f"duplicate problem id: {pid}")
        problem_ids.add(pid)
        for evidence in problem.get("evidence", []) if isinstance(problem, dict) else []:
            eid = evidence.get("id")
            if eid in evidence_ids:
                errors.append(f"duplicate evidence id: {eid}")
            evidence_ids.add(eid)
        for investigation in problem.get("investigations", []) if isinstance(problem, dict) else []:
            iid = investigation.get("id")
            if iid in investigation_ids:
                errors.append(f"duplicate investigation id: {iid}")
            investigation_ids.add(iid)
        history = problem.get("history", []) if isinstance(problem, dict) else []
        if history and history[-1].get("to_status") != problem.get("status"):
            errors.append(f"{pid}.history last to_status must equal current status")
        previous = history[0].get("to_status") if history else None
        for index, event in enumerate(history[1:], start=1):
            if event.get("from_status") != previous:
                errors.append(f"{pid}.history[{index}].from_status does not follow prior status")
            previous = event.get("to_status")
    return errors


def validate(data):
    """Return human-readable schema and relationship errors; never throw on bad shapes."""
    try:
        errors = schema_errors(data)
    except (RegistryValidationError, TypeError, AttributeError) as exc:
        return [str(exc)]
    if errors:
        return errors
    return semantic_errors(data)


def load_valid_registry(path=REGISTRY):
    data = load_json(path)
    errors = validate(data)
    if errors:
        raise RegistryValidationError("\n".join(errors))
    return data


def apply_transition(data, problem_id, target, actor, reason, at=None):
    if target not in STATUSES:
        raise ValueError(f"invalid target status: {target}")
    actor = actor.strip()
    reason = reason.strip()
    if not actor or not reason:
        raise ValueError("actor and reason are required")
    problem = next((item for item in data["problems"] if item["id"] == problem_id), None)
    if problem is None:
        raise ValueError(f"unknown problem id: {problem_id}")
    current = problem["status"]
    if target == current:
        raise ValueError(f"{problem_id} is already {target}")
    if target not in TRANSITIONS[current]:
        raise ValueError(f"transition {current} -> {target} is not allowed")
    timestamp = at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    event = {
        "at": timestamp,
        "actor": actor,
        "event": "status_changed",
        "from_status": current,
        "to_status": target,
        "reason": reason,
    }
    updated = copy.deepcopy(data)
    target_problem = next(item for item in updated["problems"] if item["id"] == problem_id)
    target_problem["status"] = target
    target_problem["history"].append(event)
    updated["updated_at"] = timestamp[:10]
    errors = validate(updated)
    if errors:
        raise RegistryValidationError("transition would make registry invalid:\n" + "\n".join(errors))
    return updated


def atomic_write(data, path=REGISTRY):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as output:
            json.dump(data, output, indent=2, ensure_ascii=False)
            output.write("\n")
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def command_data(args):
    data = load_valid_registry()
    if args.command == "validate":
        print(f"valid: {len(data['problems'])} problems, registry v{data['registry_version']}")
    elif args.command == "list":
        for problem in data["problems"]:
            print(f"{problem['id']}\t{problem['status']}\t{problem['title']}")
    elif args.command == "show":
        match = next((item for item in data["problems"] if item["id"] == args.problem_id), None)
        if match is None:
            raise ValueError(f"unknown problem id: {args.problem_id}")
        print(json.dumps(match, indent=2, ensure_ascii=False))
    elif args.command == "export":
        selected = data if not args.status else dict(data, problems=[p for p in data["problems"] if p["status"] == args.status])
        print(json.dumps(selected, indent=2, ensure_ascii=False))
    elif args.command == "transition":
        updated = apply_transition(data, args.problem_id, args.to, args.actor, args.reason, args.at)
        atomic_write(updated)
        print(f"{args.problem_id}: {args.to} (history appended by {args.actor})")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("list")
    show = sub.add_parser("show")
    show.add_argument("problem_id")
    export = sub.add_parser("export")
    export.add_argument("--status", choices=sorted(STATUSES))
    transition = sub.add_parser("transition")
    transition.add_argument("problem_id")
    transition.add_argument("--to", required=True, choices=sorted(STATUSES))
    transition.add_argument("--actor", required=True)
    transition.add_argument("--reason", required=True)
    transition.add_argument("--at", help="ISO-8601 timestamp; defaults to current UTC time")
    args = parser.parse_args()
    try:
        command_data(args)
    except (RegistryValidationError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
