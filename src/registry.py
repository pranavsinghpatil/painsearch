"""Validate and inspect the versioned PainSearch registry.

Usage:
  python src/registry.py validate
  python src/registry.py list
  python src/registry.py show P0002
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry" / "registry.json"
ALLOWED_STATUS = {"candidate", "investigating", "validated", "rejected", "unresolved"}
REQUIRED_PROBLEM = {"id", "title", "status", "statement", "evidence", "investigations", "history"}
REQUIRED_STATEMENT = {"user", "task", "failure", "consequence"}
REQUIRED_EVIDENCE = {"id", "kind", "source_url", "observed_at", "quote", "supports"}
REQUIRED_INVESTIGATION = {"id", "question", "status", "next_action"}
REQUIRED_HISTORY = {"at", "event", "note"}


def load_registry():
    with REGISTRY.open(encoding="utf-8") as f:
        return json.load(f)


def validate(data):
    errors = []
    if data.get("registry_version") != "1.0":
        errors.append("registry_version must be 1.0")
    problems = data.get("problems")
    if not isinstance(problems, list):
        return ["problems must be a list"]
    problem_ids = set()
    for i, problem in enumerate(problems):
        prefix = f"problems[{i}]"
        missing = REQUIRED_PROBLEM - problem.keys()
        errors.extend(f"{prefix} missing {key}" for key in sorted(missing))
        pid = problem.get("id")
        if not isinstance(pid, str) or not re.fullmatch(r"P\d{4}", pid or ""):
            errors.append(f"{prefix}.id must match P0000")
        elif pid in problem_ids:
            errors.append(f"duplicate problem id: {pid}")
        problem_ids.add(pid)
        if problem.get("status") not in ALLOWED_STATUS:
            errors.append(f"{prefix}.status is invalid")
        statement = problem.get("statement", {})
        errors.extend(f"{prefix}.statement missing {key}" for key in sorted(REQUIRED_STATEMENT - statement.keys()))
        evidence_ids = set()
        for j, evidence in enumerate(problem.get("evidence", [])):
            ep = f"{prefix}.evidence[{j}]"
            errors.extend(f"{ep} missing {key}" for key in sorted(REQUIRED_EVIDENCE - evidence.keys()))
            eid = evidence.get("id")
            if eid in evidence_ids:
                errors.append(f"duplicate evidence id in {pid}: {eid}")
            evidence_ids.add(eid)
            if evidence.get("kind") not in {"report", "workaround", "consequence", "counter_report", "solution"}:
                errors.append(f"{ep}.kind is invalid")
            if not str(evidence.get("source_url", "")).startswith(("http://", "https://")):
                errors.append(f"{ep}.source_url must be http(s)")
        for j, investigation in enumerate(problem.get("investigations", [])):
            ip = f"{prefix}.investigations[{j}]"
            errors.extend(f"{ip} missing {key}" for key in sorted(REQUIRED_INVESTIGATION - investigation.keys()))
            if investigation.get("status") not in {"open", "answered", "blocked"}:
                errors.append(f"{ip}.status is invalid")
        for j, history in enumerate(problem.get("history", [])):
            hp = f"{prefix}.history[{j}]"
            errors.extend(f"{hp} missing {key}" for key in sorted(REQUIRED_HISTORY - history.keys()))
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate", "list", "show"])
    parser.add_argument("problem_id", nargs="?")
    args = parser.parse_args()
    data = load_registry()
    errors = validate(data)
    if args.command == "validate":
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            raise SystemExit(1)
        print(f"valid: {len(data['problems'])} problems, registry v{data['registry_version']}")
    elif args.command == "list":
        for problem in data["problems"]:
            print(f"{problem['id']}\t{problem['status']}\t{problem['title']}")
    else:
        match = next((p for p in data["problems"] if p["id"] == args.problem_id), None)
        if match is None:
            raise SystemExit(f"unknown problem id: {args.problem_id}")
        print(json.dumps(match, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
