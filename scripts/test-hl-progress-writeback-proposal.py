#!/usr/bin/env python3
import unittest
from pathlib import Path


DOC = Path(__file__).resolve().parents[1] / "docs" / "delivery-recovery" / "HL_PROGRESS_GITHUB_WRITEBACK_PROPOSAL_v0.1.md"


def read_doc():
    if not DOC.exists():
        raise AssertionError("expected HL_PROGRESS_GITHUB_WRITEBACK_PROPOSAL_v0.1.md to exist")
    return DOC.read_text(encoding="utf-8")


class HLProgressWritebackProposalTests(unittest.TestCase):
    def test_proposal_contains_required_gate_and_boundary_sections(self):
        text = read_doc()

        for phrase in [
            "Status: P3_PROPOSAL_ONLY",
            "Separate Founder / Gate SSOT Required",
            "Allowed Minimum Command Set",
            "Permission Boundary",
            "Rollback Plan",
            "Audit Log",
            "Rejected Actions",
            "Feishu / Dashboard Reverse Pollution Prevention",
        ]:
            self.assertIn(phrase, text)

    def test_proposal_names_allowed_commands_and_forbidden_surfaces(self):
        text = read_doc()

        for command in [
            "gh issue comment",
            "gh issue edit --add-label",
            "gh issue edit --remove-label",
            "gh issue create",
            "gh pr comment",
            "gh pr edit --add-label",
        ]:
            self.assertIn(command, text)

        for forbidden in [
            "git push origin main",
            "branch protection",
            "route / mode / permission",
            "production",
            "secrets",
            "Feishu-originated state must not mutate GitHub",
        ]:
            self.assertIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
