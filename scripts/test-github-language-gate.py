#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "check-github-language-gate.py"
WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/github-language-gate.yml"


def run_gate(event, github_output_path=None):
    with tempfile.TemporaryDirectory() as tmp:
        event_path = Path(tmp) / "event.json"
        event_path.write_text(json.dumps(event, ensure_ascii=False), encoding="utf-8")
        cmd = [sys.executable, str(SCRIPT), "--event-path", str(event_path)]
        if github_output_path:
            cmd.extend(["--github-output", str(github_output_path)])
        return subprocess.run(
            cmd,
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

    def test_rejects_english_body_with_incidental_chinese_terms(self):
        result = run_gate(
            {
                "action": "opened",
                "issue": {
                    "title": "[通知台账测试] Feishu delivery ledger summary",
                    "body": (
                        "Purpose: verify Feishu delivery ledger summary after 02bbf19.\n\n"
                        "Expected:\n"
                        "- Issue opened goes to AI native工程通知 and writes a delivery ledger summary.\n"
                        "- Assigned goes DM-only to tongzhenghui and writes a delivery ledger summary.\n\n"
                        "This issue will be closed after verification."
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/179",
                },
            }
        )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "failed")
        self.assertIn("body_chinese_ratio_too_low", payload["errors"])

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

    def test_failed_comment_reports_target_issue_number(self):
        result = run_gate(
            {
                "action": "created",
                "issue": {
                    "number": 164,
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/164",
                },
                "comment": {
                    "body": "Status: blocked pending runtime owner evidence.",
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/164#issuecomment-1",
                },
            }
        )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["target_issue_number"], "164")
        self.assertEqual(
            payload["target_url"],
            "https://github.com/huanlongAI/hl-dispatch/issues/164#issuecomment-1",
        )

    def test_writes_github_output_for_failed_comment(self):
        with tempfile.TemporaryDirectory() as tmp:
            github_output_path = Path(tmp) / "github-output.txt"
            result = run_gate(
                {
                    "action": "created",
                    "issue": {
                        "number": 164,
                        "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/164",
                    },
                    "comment": {
                        "body": "Status: blocked pending runtime owner evidence.",
                        "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/164#issuecomment-1",
                    },
                },
                github_output_path=github_output_path,
            )

            self.assertEqual(result.returncode, 1)
            github_output = github_output_path.read_text(encoding="utf-8")
            self.assertIn("status=failed", github_output)
            self.assertIn("target_issue_number=164", github_output)
            self.assertIn("errors=comment_missing_chinese", github_output)
            self.assertIn(
                "target_url=https://github.com/huanlongAI/hl-dispatch/issues/164#issuecomment-1",
                github_output,
            )

    def test_workflow_reports_issue_comment_gate_violations(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("issues: write", workflow)
        self.assertIn("continue-on-error: true", workflow)
        self.assertIn("--github-output \"$GITHUB_OUTPUT\"", workflow)
        self.assertIn("Report GitHub issue/comment gate violation", workflow)
        self.assertIn("ai-output:v1", workflow)
        self.assertIn("gh issue comment", workflow)
        self.assertIn("Fail GitHub issue/comment gate", workflow)

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

    def test_accepts_valid_ai_output_contract_comment(self):
        result = run_gate(
            {
                "action": "created",
                "comment": {
                    "body": (
                        "<!-- ai-output:v1 -->\n"
                        "【类型】status_update\n"
                        "【结论】DS-1A sandbox pilot evidence accepted，未声明 production ready。\n"
                        "【依据】PR #110；CI sentinel success；integration test evidence 已记录。\n"
                        "【当前状态】accepted\n"
                        "【下一步唯一动作】Package Owner 更新 Task Snapshot。\n"
                        "【需要人处理】Package Owner\n"
                        "【不确定项】无\n"
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/200#issuecomment-1",
                },
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "passed")

    def test_rejects_ai_output_missing_required_field(self):
        result = run_gate(
            {
                "action": "created",
                "comment": {
                    "body": (
                        "<!-- ai-output:v1 -->\n"
                        "【类型】status_update\n"
                        "【结论】已完成。\n"
                        "【依据】PR #110\n"
                        "【当前状态】accepted\n"
                        "【下一步唯一动作】关闭。\n"
                        "【需要人处理】Package Owner\n"
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/200#issuecomment-1",
                },
            }
        )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertIn("ai_output_missing_不确定项", payload["errors"])

    def test_rejects_ai_output_invalid_type(self):
        result = run_gate(
            {
                "action": "created",
                "comment": {
                    "body": (
                        "<!-- ai-output:v1 -->\n"
                        "【类型】普通同步\n"
                        "【结论】继续推进整体治理。\n"
                        "【依据】PR #110\n"
                        "【当前状态】doing\n"
                        "【下一步唯一动作】继续推进。\n"
                        "【需要人处理】无\n"
                        "【不确定项】无\n"
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/200#issuecomment-1",
                },
            }
        )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertIn("ai_output_invalid_type", payload["errors"])

    def test_rejects_needs_context_without_gap_report(self):
        result = run_gate(
            {
                "action": "created",
                "comment": {
                    "body": (
                        "<!-- ai-output:v1 -->\n"
                        "【类型】status_update\n"
                        "【结论】NEEDS_CONTEXT：缺少 Task Snapshot。\n"
                        "【依据】未找到 task-snapshot:v1\n"
                        "【当前状态】blocked\n"
                        "【下一步唯一动作】补 Task Snapshot。\n"
                        "【需要人处理】Package Owner\n"
                        "【不确定项】当前 DRI\n"
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/200#issuecomment-1",
                },
            }
        )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertIn("ai_output_needs_context_requires_gap_report", payload["errors"])

    def test_rejects_done_claim_without_evidence(self):
        result = run_gate(
            {
                "action": "created",
                "comment": {
                    "body": (
                        "<!-- ai-output:v1 -->\n"
                        "【类型】status_update\n"
                        "【结论】已完成，可以关闭。\n"
                        "【依据】无\n"
                        "【当前状态】done\n"
                        "【下一步唯一动作】关闭 Issue。\n"
                        "【需要人处理】无\n"
                        "【不确定项】无\n"
                    ),
                    "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/200#issuecomment-1",
                },
            }
        )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertIn("ai_output_evidence_required", payload["errors"])


if __name__ == "__main__":
    unittest.main()
