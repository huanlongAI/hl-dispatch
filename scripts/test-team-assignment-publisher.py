#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEAM_CONTEXT = ROOT / "docs/team-context"
PUBLISHER = TEAM_CONTEXT / "scripts/build_assignment_publish_plan.py"
REGISTRY = TEAM_CONTEXT / "ROLE-REGISTRY-v1.yaml"
OWNERS = TEAM_CONTEXT / "ROLE-OWNERS-v1.yaml"
CURRENT_REGISTRY_VERSION = "ROLE-REGISTRY-v1"


def load_publisher():
    if not PUBLISHER.exists():
        raise AssertionError(f"missing publisher: {PUBLISHER}")
    spec = importlib.util.spec_from_file_location("team_assignment_publisher", PUBLISHER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assignment(task_type, assignee_role, **overrides):
    payload = {
        "task_id": f"case-{task_type}",
        "title": f"[任务] {task_type}",
        "task_type": task_type,
        "assignee_role": assignee_role,
        "registry_version": CURRENT_REGISTRY_VERSION,
        "assignment_entrypoint": "github_issue",
        "formal_assignment": True,
        "authorization_refs": ["founder-decision-2026-06-22"],
        "body": "本任务由 P1 dry-run 发布计划器预检，不直接写入 GitHub。",
    }
    payload.update(overrides)
    return payload


class TeamAssignmentPublisherTests(unittest.TestCase):
    def test_accept_builds_dry_run_plan_without_external_write(self):
        publisher = load_publisher()

        plan = publisher.build_publish_plan(
            assignment("server_deployment", "ops"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )

        self.assertEqual(plan["schema"], "assignment-publish-plan:v1")
        self.assertEqual(plan["mode"], "dry_run")
        self.assertEqual(plan["publication_decision"], "ACCEPT")
        self.assertEqual(plan["validation"]["decision"], "ACCEPT")
        self.assertFalse(plan["blocked"])
        self.assertEqual(plan["external_writes"], [])
        self.assertFalse(plan["github_write"]["enabled"])
        self.assertEqual(plan["github_write"]["operation"], "none")
        self.assertEqual(plan["publish_plan"]["target_entrypoint"], "github_issue")
        self.assertEqual(plan["publish_plan"]["action"], "prepare_assignment_payload")

    def test_accept_builds_formal_github_issue_payload_for_later_publisher(self):
        publisher = load_publisher()

        plan = publisher.build_publish_plan(
            assignment("server_deployment", "ops", priority="P1"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )

        payload = plan["formal_publisher_payload"]
        issue = payload["github_issue"]
        self.assertEqual(payload["schema"], "hl-dispatch-formal-publisher-payload:v1")
        self.assertEqual(payload["target_entrypoint"], "github_issue")
        self.assertEqual(payload["responsibility_gate"]["decision"], "ACCEPT")
        self.assertEqual(payload["responsibility_gate"]["registry_version"], CURRENT_REGISTRY_VERSION)
        self.assertEqual(issue["title"], "[任务] server_deployment")
        self.assertEqual(issue["assignees"], ["ZDragonMeta"])
        self.assertEqual(issue["labels"], ["task-assign", "ops", "priority-p1"])
        self.assertIn("task_type: server_deployment", issue["body"])
        self.assertIn("assignee_role: ops", issue["body"])
        self.assertIn("responsibility_gate_decision: ACCEPT", issue["body"])
        self.assertFalse(plan["github_write"]["enabled"])
        self.assertEqual(plan["external_writes"], [])

    def test_reject_fails_closed_without_decision_packet(self):
        publisher = load_publisher()

        plan = publisher.build_publish_plan(
            assignment("server_deployment", "ops", registry_version="ROLE-REGISTRY-v0"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )

        self.assertEqual(plan["publication_decision"], "REJECT")
        self.assertTrue(plan["blocked"])
        self.assertTrue(plan["fail_closed"])
        self.assertIsNone(plan["decision_packet"])
        self.assertIsNone(plan["formal_publisher_payload"])
        self.assertEqual(plan["external_writes"], [])
        self.assertIn("stale_responsibility_source", plan["validation"]["reason_codes"])

    def test_review_required_generates_decision_packet_only(self):
        publisher = load_publisher()

        plan = publisher.build_publish_plan(
            assignment("merchant_private_key", "product-customer-payment"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )

        self.assertEqual(plan["publication_decision"], "REVIEW_REQUIRED")
        self.assertTrue(plan["blocked"])
        self.assertFalse(plan["fail_closed"])
        self.assertEqual(plan["external_writes"], [])
        self.assertFalse(plan["github_write"]["enabled"])
        self.assertIsNotNone(plan["decision_packet"])
        self.assertTrue(plan["decision_packet"]["required"])
        self.assertEqual(plan["decision_packet"]["risk_level"], "high")
        self.assertIn("裁决", plan["decision_packet"]["minimum_reply_format"])

    def test_cli_accept_outputs_json_and_exits_zero(self):
        result = self.run_cli(assignment("server_deployment", "ops"))

        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["publication_decision"], "ACCEPT")

    def test_cli_reject_exits_one(self):
        result = self.run_cli(
            assignment("server_deployment", "ops", registry_version="ROLE-REGISTRY-v0")
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["publication_decision"], "REJECT")
        self.assertTrue(plan["fail_closed"])

    def test_cli_review_required_exits_three(self):
        result = self.run_cli(assignment("merchant_private_key", "product-customer-payment"))

        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["publication_decision"], "REVIEW_REQUIRED")
        self.assertTrue(plan["decision_packet"]["required"])

    def run_cli(self, payload):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "assignment.json"
            input_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(PUBLISHER),
                    "--input",
                    str(input_path),
                    "--registry",
                    str(REGISTRY),
                    "--owners",
                    str(OWNERS),
                ],
                capture_output=True,
                text=True,
            )


if __name__ == "__main__":
    unittest.main()
