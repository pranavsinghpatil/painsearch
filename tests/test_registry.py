import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import registry


class RegistryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = registry.load_valid_registry()

    def test_real_registry_is_valid(self):
        self.assertEqual(registry.validate(self.data), [])

    def test_malformed_nested_value_returns_error(self):
        bad = copy.deepcopy(self.data)
        bad["problems"][0]["statement"] = "not an object"
        errors = registry.validate(bad)
        self.assertTrue(any("statement" in error for error in errors))

    def test_unknown_nested_field_is_rejected(self):
        bad = copy.deepcopy(self.data)
        bad["problems"][0]["evidence"][0]["unexpected"] = True
        errors = registry.validate(bad)
        self.assertTrue(any("unexpected" in error for error in errors))

    def test_bad_timestamp_is_rejected(self):
        bad = copy.deepcopy(self.data)
        bad["problems"][0]["evidence"][0]["provenance"]["collected_at"] = "yesterday"
        errors = registry.validate(bad)
        self.assertTrue(any("collected_at" in error for error in errors))

    def test_consumers_refuse_invalid_registry(self):
        bad = copy.deepcopy(self.data)
        bad["problems"][0]["statement"] = "not an object"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaises(registry.RegistryValidationError):
                registry.load_valid_registry(path)

    def test_history_must_match_current_status(self):
        bad = copy.deepcopy(self.data)
        bad["problems"][0]["history"][-1]["to_status"] = "candidate"
        errors = registry.validate(bad)
        self.assertTrue(any("last to_status" in error for error in errors))

    def test_transition_requires_reason_and_appends_history(self):
        updated = registry.apply_transition(
            copy.deepcopy(self.data), "P0002", "unresolved", "test-user",
            "Baseline still missing", "2026-09-17T08:00:00+00:00"
        )
        problem = next(item for item in updated["problems"] if item["id"] == "P0002")
        self.assertEqual(problem["status"], "unresolved")
        self.assertEqual(problem["history"][-1]["actor"], "test-user")
        self.assertEqual(problem["history"][-1]["from_status"], "investigating")
        self.assertEqual(registry.validate(updated), [])

    def test_invalid_transition_is_rejected(self):
        with self.assertRaises(ValueError):
            registry.apply_transition(copy.deepcopy(self.data), "P0001", "validated", "test-user", "bad idea")


if __name__ == "__main__":
    unittest.main()
