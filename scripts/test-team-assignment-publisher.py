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
PUBLISHER_PREFLIGHT = TEAM_CONTEXT / "scripts/preflight_formal_assignment_publisher.py"
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


def load_publisher_preflight():
    if not PUBLISHER_PREFLIGHT.exists():
        raise AssertionError(f"missing publisher preflight: {PUBLISHER_PREFLIGHT}")
    spec = importlib.util.spec_from_file_location("team_assignment_publisher_preflight", PUBLISHER_PREFLIGHT)
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

    def test_formal_publisher_preflight_accepts_github_issue_payload_without_external_write(self):
        publisher = load_publisher()
        plan = publisher.build_publish_plan(
            assignment("server_deployment", "ops", priority="P1"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )

        result = self.run_publisher_preflight(plan)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        preflight = json.loads(result.stdout)
        self.assertEqual(preflight["schema"], "hl-dispatch-formal-publisher-preflight:v1")
        self.assertEqual(preflight["status"], "passed")
        self.assertTrue(preflight["ready_to_create_github_issue"])
        self.assertEqual(preflight["reason_codes"], [])
        self.assertEqual(preflight["language_gate"]["status"], "passed")
        self.assertFalse(preflight["github_write"]["enabled"])
        self.assertEqual(preflight["github_write"]["operation"], "none")
        self.assertEqual(preflight["github_issue"]["assignees"], ["ZDragonMeta"])
        self.assertEqual(preflight["github_issue"]["labels"], ["task-assign", "ops", "priority-p1"])

    def test_formal_publisher_preflight_rejects_review_required_plan(self):
        publisher = load_publisher()
        plan = publisher.build_publish_plan(
            assignment("merchant_private_key", "product-customer-payment"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )

        result = self.run_publisher_preflight(plan)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        preflight = json.loads(result.stdout)
        self.assertEqual(preflight["status"], "failed")
        self.assertFalse(preflight["ready_to_create_github_issue"])
        self.assertIn("publication_decision_not_accept", preflight["reason_codes"])
        self.assertNotIn("github_issue", preflight)
        self.assertFalse(preflight["github_write"]["enabled"])

    def test_formal_publisher_dry_run_outputs_issue_create_command_without_write(self):
        publisher = load_publisher()
        plan = publisher.build_publish_plan(
            assignment("server_deployment", "ops", priority="P1"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )

        result = self.run_publisher_preflight(
            plan,
            "--publish",
            "--repo",
            "huanlongAI/hl-dispatch",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        publish = json.loads(result.stdout)
        self.assertEqual(publish["schema"], "hl-dispatch-formal-assignment-publisher:v1")
        self.assertEqual(publish["status"], "dry_run_ready")
        self.assertEqual(publish["mode"], "dry_run")
        self.assertEqual(publish["preflight"]["status"], "passed")
        self.assertFalse(publish["github_write"]["enabled"])
        self.assertEqual(publish["github_write"]["operation"], "gh issue create")
        self.assertEqual(publish["github_write"]["repo"], "huanlongAI/hl-dispatch")
        self.assertEqual(publish["external_writes"], [])
        self.assertEqual(publish["github_issue"]["labels"], ["task-assign", "ops", "priority-p1"])
        self.assertIn("--repo", publish["command_preview"])
        self.assertIn("huanlongAI/hl-dispatch", publish["command_preview"])
        self.assertIn("--title", publish["command_preview"])
        self.assertIn("[任务] server_deployment", publish["command_preview"])
        self.assertIn("--label", publish["command_preview"])
        self.assertIn("--assignee", publish["command_preview"])
        self.assertIn("ZDragonMeta", publish["command_preview"])

    def test_formal_publisher_parse_args_exposes_execute_confirmation_flag(self):
        publisher_preflight = load_publisher_preflight()

        default_args = publisher_preflight.parse_args(["--input", "/tmp/plan.json", "--publish"])
        confirmed_args = publisher_preflight.parse_args(
            [
                "--input",
                "/tmp/plan.json",
                "--publish",
                "--execute",
                "--confirm-github-issue-create",
            ]
        )

        self.assertFalse(default_args.confirm_github_issue_create)
        self.assertTrue(confirmed_args.confirm_github_issue_create)

    def test_formal_publisher_execute_requires_create_confirmation_before_any_write(self):
        publisher = load_publisher()
        publisher_preflight = load_publisher_preflight()
        plan = publisher.build_publish_plan(
            assignment("server_deployment", "ops", priority="P1"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )
        preflight = publisher_preflight.build_preflight(plan)
        calls = []

        def fake_write_preflight_runner(args):
            calls.append(("write_preflight", args))
            return subprocess.CompletedProcess(args, 0, stdout='{"status":"passed"}\n', stderr="")

        def fake_gh_runner(args):
            calls.append(("gh", args))
            return subprocess.CompletedProcess(
                args,
                0,
                stdout="https://github.com/huanlongAI/hl-dispatch/issues/999\n",
                stderr="",
            )

        result = publisher_preflight.publish_preflight_result(
            preflight,
            repo="huanlongAI/hl-dispatch",
            execute=True,
            runner=fake_gh_runner,
            write_preflight_runner=fake_write_preflight_runner,
        )

        self.assertEqual(result["status"], "failed")
        self.assertFalse(result["github_write"]["enabled"])
        self.assertIn("missing_execute_confirmation", result["reason_codes"])
        self.assertEqual(result["external_writes"], [])
        self.assertEqual(calls, [])

    def test_formal_publisher_execute_uses_gh_issue_create_after_passed_preflight(self):
        publisher = load_publisher()
        publisher_preflight = load_publisher_preflight()
        plan = publisher.build_publish_plan(
            assignment("server_deployment", "ops", priority="P1"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )
        preflight = publisher_preflight.build_preflight(plan)
        calls = []

        def fake_write_preflight_runner(args):
            calls.append(("write_preflight", args))
            return subprocess.CompletedProcess(args, 0, stdout='{"status":"passed"}\n', stderr="")

        def fake_gh_runner(args):
            calls.append(("gh", args))
            return subprocess.CompletedProcess(
                args,
                0,
                stdout="https://github.com/huanlongAI/hl-dispatch/issues/999\n",
                stderr="",
            )

        result = publisher_preflight.publish_preflight_result(
            preflight,
            repo="huanlongAI/hl-dispatch",
            execute=True,
            confirm_create=True,
            runner=fake_gh_runner,
            write_preflight_runner=fake_write_preflight_runner,
        )

        self.assertEqual(result["status"], "created")
        self.assertTrue(result["github_write"]["enabled"])
        self.assertEqual(result["github_write"]["operation"], "gh issue create")
        self.assertEqual(result["github_issue_url"], "https://github.com/huanlongAI/hl-dispatch/issues/999")
        self.assertEqual(
            result["external_writes"],
            [
                {
                    "system": "github",
                    "operation": "issue_create",
                    "url": "https://github.com/huanlongAI/hl-dispatch/issues/999",
                }
            ],
        )
        self.assertEqual([kind for kind, _args in calls], ["write_preflight", "gh"])
        self.assertIn("preflight-github-language-write.py", calls[0][1][1])
        self.assertIn("--kind", calls[0][1])
        self.assertIn("--title", calls[0][1])
        self.assertEqual(calls[1][1][:5], ["gh", "issue", "create", "--repo", "huanlongAI/hl-dispatch"])
        self.assertIn("--label", calls[1][1])
        self.assertIn("--assignee", calls[1][1])

    def test_formal_publisher_execute_stops_when_write_preflight_fails(self):
        publisher = load_publisher()
        publisher_preflight = load_publisher_preflight()
        plan = publisher.build_publish_plan(
            assignment("server_deployment", "ops", priority="P1"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )
        preflight = publisher_preflight.build_preflight(plan)
        gh_calls = []

        def fake_write_preflight_runner(args):
            return subprocess.CompletedProcess(
                args,
                1,
                stdout='{"status":"failed","errors":["title/body language gate failed"]}\n',
                stderr="",
            )

        def fake_gh_runner(args):
            gh_calls.append(args)
            return subprocess.CompletedProcess(
                args,
                0,
                stdout="https://github.com/huanlongAI/hl-dispatch/issues/999\n",
                stderr="",
            )

        result = publisher_preflight.publish_preflight_result(
            preflight,
            repo="huanlongAI/hl-dispatch",
            execute=True,
            confirm_create=True,
            runner=fake_gh_runner,
            write_preflight_runner=fake_write_preflight_runner,
        )

        self.assertEqual(result["status"], "failed")
        self.assertFalse(result["github_write"]["enabled"])
        self.assertIn("github_language_write_preflight_failed", result["reason_codes"])
        self.assertEqual(result["external_writes"], [])
        self.assertEqual(gh_calls, [])

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

    def run_publisher_preflight(self, plan, *extra_args):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "plan.json"
            input_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(PUBLISHER_PREFLIGHT),
                    "--input",
                    str(input_path),
                    *extra_args,
                ],
                capture_output=True,
                text=True,
            )


if __name__ == "__main__":
    unittest.main()
