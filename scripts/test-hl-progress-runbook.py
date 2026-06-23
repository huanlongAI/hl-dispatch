#!/usr/bin/env python3
import unittest
from pathlib import Path


DOC = Path(__file__).resolve().parents[1] / "docs" / "delivery-recovery" / "HL_PROGRESS_OPERATION_RUNBOOK_v0.1.md"


def read_doc():
    if not DOC.exists():
        raise AssertionError("expected HL_PROGRESS_OPERATION_RUNBOOK_v0.1.md to exist")
    return DOC.read_text(encoding="utf-8")


class HLProgressOperationRunbookTests(unittest.TestCase):
    def test_runbook_contains_daily_weekly_and_gate_stop_sections(self):
        text = read_doc()
        for phrase in [
            "Status: GREEN_READ_ONLY_OPERATION",
            "Daily Read-Only Scan",
            "Weekly Founder Packet",
            "Engineering Command Snapshot",
            "Bitable Dry-Run Projection",
            "Gate Stop Rules",
            "Verification Commands",
            "No External Writes",
        ]:
            self.assertIn(phrase, text)

    def test_runbook_names_safe_commands_and_forbidden_actions(self):
        text = read_doc()
        for command in [
            "python3 scripts/export-hl-progress.py --repo huanlongAI/hl-dispatch --state open --limit 100 --format json",
            "python3 scripts/export-hl-progress.py --repo huanlongAI/hl-dispatch --state open --limit 100 --format markdown",
            "python3 scripts/export-hl-progress.py --repo huanlongAI/hl-dispatch --state all --limit 100 --format json --snapshot",
            "python3 scripts/project-hl-progress-bitable.py --input <hl-progress-export.json> --format json",
            "PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-exporter.py",
            "PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-bitable-projection.py",
            "PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-writeback-proposal.py",
        ]:
            self.assertIn(command, text)

        for forbidden in [
            "do not write Feishu",
            "do not write Bitable",
            "do not write GitHub",
            "do not change route / mode / permission",
            "do not treat projection as evidence",
            "Founder / Gate SSOT",
        ]:
            self.assertIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
