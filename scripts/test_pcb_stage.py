"""Behavioral checks for missing coverage and stale evidence; no EDA needed."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from check_pcb_stage import FINAL_CHECKS, LAYOUT_CHECKS, digest, validate


class StageReviewTests(unittest.TestCase):
    def test_incomplete_or_stale_review_is_blocked(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            pcb = root / "current.epcb"
            pcb.write_text("test-only PCB snapshot", encoding="utf-8")
            inv = root / "inventory.json"
            inv.write_text(json.dumps({"components": ["U1", "C1"], "power_pins": ["U1.4"]}), encoding="utf-8")
            evidence = root / "review.txt"
            evidence.write_text("synthetic review fixture, not a real board approval", encoding="utf-8")
            passed = {"status": "pass", "evidence": ["review"], "rationale": "Synthetic test record"}
            report = {
                "schema_version": 1, "project": "test", "revision": "test", "stage": "final",
                "artifacts": {k: {"path": p.name, "sha256": digest(p)} for k, p in {"pcb": pcb, "inventory": inv, "review": evidence}.items()},
                "checks": {k: copy.deepcopy(passed) for k in FINAL_CHECKS},
                "components": {k: copy.deepcopy(passed) for k in ["U1", "C1"]},
                "power_pins": {"U1.4": copy.deepcopy(passed)},
            }
            target = root / "stage.json"

            def check(value, allowed=False):
                target.write_text(json.dumps(value), encoding="utf-8")
                self.assertEqual(not validate(target, pcb), allowed)

            check(report, True)
            self.assertTrue(validate(target, pcb, "layout"))
            layout = copy.deepcopy(report)
            layout["stage"] = "layout"
            layout["checks"] = {k: layout["checks"][k] for k in LAYOUT_CHECKS}
            check(layout, True)
            self.assertTrue(validate(target, pcb, "final"))
            missing_pin = copy.deepcopy(report)
            missing_pin["power_pins"].clear()
            check(missing_pin)
            missing_component = copy.deepcopy(report)
            del missing_component["components"]["C1"]
            check(missing_component)
            failed = copy.deepcopy(report)
            failed["checks"]["PCB-V04"]["status"] = "fail"
            check(failed)
            unchecked = copy.deepcopy(report)
            del unchecked["checks"]["PCB-L01/L17/L20"]
            check(unchecked)
            undocumented_na = copy.deepcopy(report)
            undocumented_na["power_pins"]["U1.4"] = {"status": "not_applicable", "evidence": [], "rationale": ""}
            check(undocumented_na)
            no_review = copy.deepcopy(report)
            no_review["checks"]["PCB-V04"]["evidence"] = ["pcb"]
            check(no_review)
            missing_file = copy.deepcopy(report)
            missing_file["artifacts"]["review"]["path"] = "missing.txt"
            check(missing_file)
            other_pcb = root / "other.epcb"
            other_pcb.write_bytes(pcb.read_bytes())
            wrong_source = copy.deepcopy(report)
            wrong_source["artifacts"]["pcb"]["path"] = other_pcb.name
            check(wrong_source)
            pcb.write_text("changed PCB", encoding="utf-8")
            check(report)
            pcb.write_text("test-only PCB snapshot", encoding="utf-8")
            evidence.write_text("changed evidence", encoding="utf-8")
            check(report)
            target.write_text("[]", encoding="utf-8")
            self.assertTrue(validate(target, pcb))


if __name__ == "__main__":
    unittest.main()
