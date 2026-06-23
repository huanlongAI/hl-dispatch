#!/usr/bin/env python3
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "export-hl-progress.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "hl-progress-input.json"
SNAPSHOT_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "engineering-command-snapshot-input.json"


def load_exporter():
    if not SCRIPT.exists():
        raise AssertionError("expected scripts/export-hl-progress.py to exist")
    spec = importlib.util.spec_from_file_location("export_hl_progress", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def label(name):
    return {"name": name}


def assignee(login):
    return {"login": login}


class HLProgressExporterTests(unittest.TestCase):
    def test_builds_work_item_from_structured_issue_without_guessing(self):
        exporter = load_exporter()
        source = {
            "repo": "huanlongAI/hl-dispatch",
            "issues": [
                {
                    "number": 301,
                    "title": "[HLPROG] P1 exporter",
                    "url": "https://github.com/huanlongAI/hl-dispatch/issues/301",
                    "state": "OPEN",
                    "labels": [label("task-assign")],
                    "assignees": [assignee("dahuizi")],
                    "updatedAt": "2026-06-12T01:02:03Z",
                    "body": (
                        "### task_id\n"
                        "HLPROG-P1-WU1\n\n"
                        "### owner_role\n"
                        "dahuizi\n\n"
                        "### status\n"
                        "in_progress\n\n"
                        "### risk_path\n"
                        "green\n\n"
                        "### evidence_state\n"
                        "linked\n\n"
                        "### next_gate\n"
                        "offline deterministic tests\n\n"
                        "### next_action\n"
                        "Run hl-progress exporter deterministic tests.\n\n"
                        "### blocker\n"
                        "none\n"
                    ),
                }
            ],
            "pull_requests": [],
            "files": [],
        }

        projection = exporter.build_export(source, generated_at="2026-06-12T00:00:00Z")

        self.assertEqual(projection["schema"], "hl-progress-export:v0.1")
        self.assertEqual(projection["counts"]["issues"], 1)
        self.assertEqual(projection["counts"]["pull_requests"], 0)
        self.assertEqual(projection["counts"]["repo_files"], 0)
        self.assertEqual(projection["counts"]["items"], 1)
        item = projection["items"][0]
        self.assertEqual(item["schema"], "hl-progress-work-item:v0.1")
        self.assertEqual(item["task_id"], "HLPROG-P1-WU1")
        self.assertEqual(
            item["source"],
            {
                "system": "github",
                "repo": "huanlongAI/hl-dispatch",
                "issue_url": "https://github.com/huanlongAI/hl-dispatch/issues/301",
                "pr_urls": [],
                "file_refs": [],
            },
        )
        self.assertEqual(item["owner"], {"github": "@dahuizi", "role": "dahuizi"})
        self.assertEqual(item["status"], "in_progress")
        self.assertEqual(item["risk_path"], "green")
        self.assertEqual(item["evidence_state"], "linked")
        self.assertEqual(item["next_gate"], "offline deterministic tests")
        self.assertEqual(item["next_action"], "Run hl-progress exporter deterministic tests.")
        self.assertEqual(
            item["blocker"],
            {"state": "none", "summary": "n/a", "owner": "n/a"},
        )
        self.assertFalse(item["founder_decision_required"])
        self.assertEqual(item["projection"]["target"], "json")
        self.assertEqual(item["projection"]["generated_at"], "2026-06-12T00:00:00Z")
        self.assertRegex(item["projection"]["source_hash"], r"^[0-9a-f]{64}$")
        self.assertEqual(item["warnings"], [])

    def test_decision_issue_uses_unknown_and_warnings_for_missing_fields(self):
        exporter = load_exporter()
        source = {
            "repo": "huanlongAI/hl-dispatch",
            "issues": [
                {
                    "number": 302,
                    "title": "[Decision] P2 projection gate",
                    "url": "https://github.com/huanlongAI/hl-dispatch/issues/302",
                    "state": "OPEN",
                    "labels": [label("decision-request")],
                    "assignees": [],
                    "updatedAt": "2026-06-12T01:02:03Z",
                    "body": "Founder decision is required before writing Bitable.",
                }
            ],
        }

        item = exporter.build_export(source, generated_at="2026-06-12T00:00:00Z")["items"][0]

        self.assertEqual(item["task_id"], "issue-302")
        self.assertEqual(item["owner"], {"github": "unknown", "role": "unknown"})
        self.assertEqual(item["status"], "founder_acceptance")
        self.assertEqual(item["risk_path"], "unknown")
        self.assertEqual(item["evidence_state"], "unknown")
        self.assertEqual(item["next_gate"], "Founder")
        self.assertEqual(item["next_action"], "n/a")
        self.assertTrue(item["founder_decision_required"])
        self.assertIn("missing_owner", item["warnings"])
        self.assertIn("missing_risk_path", item["warnings"])
        self.assertIn("missing_evidence_state", item["warnings"])
        self.assertIn("missing_next_action", item["warnings"])

    def test_builds_review_item_from_pull_request(self):
        exporter = load_exporter()
        source = {
            "repo": "huanlongAI/hl-dispatch",
            "pull_requests": [
                {
                    "number": 303,
                    "title": "[HLPROG] P1 exporter PR",
                    "url": "https://github.com/huanlongAI/hl-dispatch/pull/303",
                    "state": "OPEN",
                    "labels": [label("priority-p1")],
                    "assignees": [],
                    "author": {"login": "engineer-a"},
                    "isDraft": False,
                    "reviewDecision": "REVIEW_REQUIRED",
                    "updatedAt": "2026-06-12T01:02:03Z",
                    "body": (
                        "### task_id\n"
                        "HLPROG-P1-PR\n\n"
                        "### risk_path\n"
                        "green\n\n"
                        "### evidence_state\n"
                        "linked\n\n"
                        "### next_action\n"
                        "Review the read-only exporter PR.\n"
                    ),
                }
            ],
        }

        item = exporter.build_export(source, generated_at="2026-06-12T00:00:00Z")["items"][0]

        self.assertEqual(item["task_id"], "HLPROG-P1-PR")
        self.assertEqual(item["source"]["issue_url"], "")
        self.assertEqual(
            item["source"]["pr_urls"],
            ["https://github.com/huanlongAI/hl-dispatch/pull/303"],
        )
        self.assertEqual(item["owner"], {"github": "@engineer-a", "role": "unknown"})
        self.assertEqual(item["status"], "review")
        self.assertEqual(item["next_gate"], "PR review")
        self.assertEqual(item["next_action"], "Review the read-only exporter PR.")

    def test_builds_item_from_repo_file_reference(self):
        exporter = load_exporter()
        source = {
            "repo": "huanlongAI/hl-dispatch",
            "files": [
                {
                    "path": "deliverables/tasks/HL-PROGRESS-GOVERNANCE-LOOP-TASKBOOK-2026-06-12-v0.1.md",
                    "url": "https://github.com/huanlongAI/hl-dispatch/blob/main/deliverables/tasks/HL-PROGRESS-GOVERNANCE-LOOP-TASKBOOK-2026-06-12-v0.1.md",
                    "content": (
                        "# Taskbook\n\n"
                        "### task_id\n"
                        "HLPROG-P1-WU2\n\n"
                        "### owner_role\n"
                        "dahuizi\n\n"
                        "### status\n"
                        "planned\n\n"
                        "### risk_path\n"
                        "green\n\n"
                        "### evidence_state\n"
                        "none\n\n"
                        "### next_gate\n"
                        "deterministic fixture\n\n"
                        "### next_action\n"
                        "Create Founder packet fixture.\n"
                    ),
                }
            ],
        }

        item = exporter.build_export(source, generated_at="2026-06-12T00:00:00Z")["items"][0]

        self.assertEqual(item["task_id"], "HLPROG-P1-WU2")
        self.assertEqual(item["source"]["issue_url"], "")
        self.assertEqual(item["source"]["pr_urls"], [])
        self.assertEqual(
            item["source"]["file_refs"],
            [
                "https://github.com/huanlongAI/hl-dispatch/blob/main/deliverables/tasks/HL-PROGRESS-GOVERNANCE-LOOP-TASKBOOK-2026-06-12-v0.1.md"
            ],
        )
        self.assertEqual(item["status"], "planned")
        self.assertIn("missing_owner", item["warnings"])

    def test_source_hash_changes_when_source_facts_change(self):
        exporter = load_exporter()
        source = {
            "repo": "huanlongAI/hl-dispatch",
            "issues": [
                {
                    "number": 304,
                    "title": "[HLPROG] hash",
                    "url": "https://github.com/huanlongAI/hl-dispatch/issues/304",
                    "state": "OPEN",
                    "labels": [],
                    "assignees": [assignee("engineer-a")],
                    "updatedAt": "2026-06-12T01:02:03Z",
                    "body": "### next_action\nFirst action.\n",
                }
            ],
        }
        changed = json.loads(json.dumps(source))
        changed["issues"][0]["body"] = "### next_action\nSecond action.\n"

        first = exporter.build_export(source, generated_at="2026-06-12T00:00:00Z")
        second = exporter.build_export(changed, generated_at="2026-06-12T00:00:00Z")

        self.assertNotEqual(
            first["items"][0]["projection"]["source_hash"],
            second["items"][0]["projection"]["source_hash"],
        )

    def test_cli_outputs_json_and_markdown_founder_packet(self):
        json_result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(FIXTURE),
                "--generated-at",
                "2026-06-12T00:00:00Z",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )
        markdown_result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(FIXTURE),
                "--generated-at",
                "2026-06-12T00:00:00Z",
                "--format",
                "markdown",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["counts"]["items"], 1)
        self.assertEqual(markdown_result.returncode, 0, markdown_result.stderr)
        self.assertIn("# HL Progress Founder Packet", markdown_result.stdout)
        self.assertIn("Decision Required", markdown_result.stdout)
        self.assertIn("https://github.com/huanlongAI/hl-dispatch/issues/305", markdown_result.stdout)

    def test_builds_engineering_command_snapshot_with_readback_and_gated_authorization(self):
        exporter = load_exporter()
        source = json.loads(SNAPSHOT_FIXTURE.read_text(encoding="utf-8"))

        snapshot = exporter.build_engineering_command_snapshot(
            source,
            generated_at="2026-06-23T00:00:00Z",
            hygiene=[
                {
                    "type": "dirty_worktree",
                    "severity": "yellow",
                    "repo_path": "/workspace/hl-platform",
                    "detail": "1 modified file",
                }
            ],
        )

        self.assertEqual(snapshot["schema"], "engineering-command-snapshot:v0.2")
        self.assertEqual(snapshot["generated_at"], "2026-06-23T00:00:00Z")
        self.assertEqual(snapshot["expires_at"], "2026-06-23T00:30:00Z")
        self.assertEqual(snapshot["snapshot_ttl_minutes"], 30)
        self.assertEqual(snapshot["wip_limit"], 4)
        self.assertEqual(snapshot["source_coverage"]["github"]["issues"], 7)
        self.assertEqual(snapshot["source_coverage"]["github"]["pull_requests"], 1)
        self.assertEqual(snapshot["snapshot_completeness"], {"status": "complete", "missing": []})
        self.assertRegex(snapshot["snapshot_hash"], r"^[0-9a-f]{64}$")
        self.assertEqual(snapshot["receipt"]["schema"], "engineering-command-snapshot-receipt:v0.1")
        self.assertEqual(snapshot["receipt"]["snapshot_hash"], snapshot["snapshot_hash"])
        self.assertEqual(snapshot["receipt"]["expires_at"], snapshot["expires_at"])
        self.assertTrue(snapshot["source_queries"])
        self.assertEqual({lane["name"] for lane in snapshot["lanes"]}, {"current", "waiting_decision", "waiting_readback", "queued", "history"})

        lanes = {lane["name"]: lane["items"] for lane in snapshot["lanes"]}
        self.assertEqual([item["source_number"] for item in lanes["current"]], [39, 245, 281, 142])
        self.assertIn(267, [item["source_number"] for item in lanes["queued"]])
        self.assertEqual(lanes["waiting_decision"][0]["source_number"], 242)
        self.assertEqual(lanes["waiting_readback"][0]["source_number"], 393)

        payment_item = next(item for item in lanes["current"] if item["source_number"] == 245)
        self.assertEqual(payment_item["authorization"]["pm_readiness"], True)
        self.assertEqual(payment_item["authorization"]["runtime_authorized"], False)
        self.assertEqual(payment_item["authorization"]["production_authorized"], False)
        self.assertEqual(payment_item["authorization"]["release_authorized"], False)
        self.assertEqual(payment_item["authorization"]["founder_gate_receipt_url"], "")
        self.assertIn("sensitive_scope_gated_without_founder_gate_receipt", payment_item["warnings"])

        self.assertTrue(any(action["type"] == "merge_readback_candidate" for action in snapshot["candidate_actions"]))
        self.assertTrue(any(action["type"] == "decision_request_candidate" for action in snapshot["candidate_actions"]))
        self.assertTrue(any(action["type"] == "hygiene_incident" for action in snapshot["candidate_actions"]))
        self.assertTrue(all(action["external_write"] is False for action in snapshot["candidate_actions"]))
        self.assertTrue(all(action["recommendation_only"] is True for action in snapshot["candidate_actions"]))
        self.assertTrue(all(action["required_gate"] == "AI_ADMISSION_GATE" for action in snapshot["candidate_actions"]))
        self.assertIn("wip_limit_exceeded", snapshot["warnings"])
        self.assertEqual(snapshot["hygiene"][0]["type"], "dirty_worktree")

    def test_snapshot_does_not_infer_runtime_authorization_from_pm_ci_feishu_or_assignee(self):
        exporter = load_exporter()
        source = {
            "repo": "huanlongAI/hl-dispatch",
            "issues": [
                {
                    "number": 501,
                    "title": "[PM Ready][CI green][Feishu reminded] Booking checkout",
                    "url": "https://github.com/huanlongAI/hl-dispatch/issues/501",
                    "state": "OPEN",
                    "labels": [label("approved"), label("ci:green"), label("feishu:reminded")],
                    "assignees": [assignee("engineer-a")],
                    "updatedAt": "2026-06-23T01:02:03Z",
                    "body": (
                        "### status\n"
                        "bounded_implementation\n\n"
                        "### pm_readiness\n"
                        "true\n\n"
                        "### evidence_state\n"
                        "linked\n\n"
                        "### risk_path\n"
                        "green\n\n"
                        "### next_action\n"
                        "Continue bounded implementation.\n"
                    ),
                }
            ],
        }

        snapshot = exporter.build_engineering_command_snapshot(source, generated_at="2026-06-23T00:00:00Z")
        item = snapshot["lanes"][0]["items"][0]

        self.assertEqual(item["authorization"]["pm_readiness"], True)
        self.assertEqual(item["authorization"]["implementation_authorized"], False)
        self.assertEqual(item["authorization"]["runtime_authorized"], False)
        self.assertEqual(item["authorization"]["deployment_authorized"], False)
        self.assertEqual(item["authorization"]["production_authorized"], False)
        self.assertEqual(item["authorization"]["release_authorized"], False)

    def test_collects_git_and_progress_hygiene_without_writing(self):
        exporter = load_exporter()
        hygiene = exporter.collect_hygiene(
            repo_paths=[],
            progress_files=[
                {
                    "path": "/workspace/hl-platform/PROGRESS.json",
                    "updated_at": "2026-03-26T00:00:00Z",
                }
            ],
            now="2026-06-23T00:00:00Z",
            stale_days=30,
        )

        self.assertEqual(hygiene[0]["type"], "stale_progress")
        self.assertEqual(hygiene[0]["severity"], "yellow")
        self.assertIn("PROGRESS.json", hygiene[0]["path"])

    def test_collects_dirty_and_stale_worktree_hygiene(self):
        exporter = load_exporter()
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
            (repo / "README.md").write_text("baseline\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
            env = {
                **os.environ,
                "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+0000",
                "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+0000",
            }
            subprocess.run(["git", "commit", "-m", "baseline"], cwd=repo, check=True, env=env, capture_output=True, text=True)
            (repo / "README.md").write_text("dirty\n", encoding="utf-8")

            hygiene = exporter.collect_hygiene(
                repo_paths=[str(repo)],
                progress_files=[],
                now="2026-06-23T00:00:00Z",
                stale_days=30,
            )

        self.assertIn("dirty_worktree", {item["type"] for item in hygiene})
        self.assertIn("stale_worktree", {item["type"] for item in hygiene})

    def test_cli_outputs_snapshot_json_without_external_writes(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(SNAPSHOT_FIXTURE),
                "--generated-at",
                "2026-06-23T00:00:00Z",
                "--format",
                "json",
                "--snapshot",
                "--no-hygiene",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema"], "engineering-command-snapshot:v0.2")
        self.assertEqual(payload["snapshot_ttl_minutes"], 30)
        self.assertEqual(payload["expires_at"], "2026-06-23T00:30:00Z")
        self.assertEqual(payload["external_writes"], [])
        self.assertTrue(payload["candidate_actions"])

    def test_snapshot_cli_accepts_explicit_ttl_minutes(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(SNAPSHOT_FIXTURE),
                "--generated-at",
                "2026-06-23T00:00:00Z",
                "--format",
                "json",
                "--snapshot",
                "--snapshot-ttl-minutes",
                "45",
                "--no-hygiene",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["snapshot_ttl_minutes"], 45)
        self.assertEqual(payload["expires_at"], "2026-06-23T00:45:00Z")


if __name__ == "__main__":
    unittest.main()
