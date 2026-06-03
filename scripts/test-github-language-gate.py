#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "check-github-language-gate.py"


def run_gate(event):
    with tempfile.TemporaryDirectory() as tmp:
        event_path = Path(tmp) / "event.json"
        event_path.write_text(json.dumps(event, ensure_ascii=False), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--event-path", str(event_path)],
            capture_output=True,
            text=True,
        )


class GitHubLanguageGateTests(unittest.TestCase):
    def test_rejects_pure_english_issue_title_and_body(self):
        result = run_gate(
            {
                "action": "opened",
                "issue": {
                    "title": "[ledger test] Feishu delivery ledger summary",
                    "body": (
                        "Purpose: verify Feishu delivery ledger summary.\n\n"
                        "Expected:\n"
                        "- Issue opened writes a delivery ledger summary.\n"
                        "- Assigned writes a delivery ledger summary."
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/179",
                },
            }
        )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "failed")
        self.assertIn("title_missing_chinese", payload["errors"])
        self.assertIn("body_missing_chinese", payload["errors"])

    def test_accepts_chinese_issue_with_english_terms(self):
        result = run_gate(
            {
                "action": "opened",
                "issue": {
                    "title": "[通知台账测试] Feishu delivery ledger summary",
                    "body": (
                        "目的：验证 Feishu delivery ledger summary。\n\n"
                        "预期：Issue opened 写入 delivery ledger summary。"
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/180",
                },
            }
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "passed")

    def test_rejects_pure_english_issue_comment(self):
        result = run_gate(
            {
                "action": "created",
                "comment": {
                    "body": "Status: ready. Next: close after verification.",
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/179#issuecomment-1",
                },
            }
        )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "failed")
        self.assertIn("comment_missing_chinese", payload["errors"])

    def test_accepts_chinese_inside_markdown_code_block(self):
        result = run_gate(
            {
                "action": "created",
                "comment": {
                    "body": (
                        "@owner\n\n"
                        "```yaml\n"
                        "runtime_main_chain_data_callback:\n"
                        "  status: blocked\n"
                        "  note: \"需要 Runtime Owner 追加结构化 ready 回执。\"\n"
                        "  requested_action:\n"
                        "    - \"请补齐 negative test evidence_ref。\"\n"
                        "```"
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/164#issuecomment-1",
                },
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "passed")

    def test_allows_owner_confirmation_yaml_without_chinese(self):
        result = run_gate(
            {
                "action": "created",
                "comment": {
                    "body": (
                        "owner_confirmation_response_v1:\n"
                        "  dispatch_id: FE-OC-001\n"
                        "  decision: confirmed\n"
                        "  confirmed_scope:\n"
                        "    - ledger_check\n"
                        "  blockers: []\n"
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/101#issuecomment-1",
                },
            }
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "passed")
        self.assertTrue(payload["structured_yaml_allowed"])


if __name__ == "__main__":
    unittest.main()
