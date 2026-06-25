#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/hl-ai.py"
TEAM_AI_CONTEXT = ROOT / "docs/team-ai-context"
STAGE_C_ENTRY_DOC = TEAM_AI_CONTEXT / "TEAM_AI_CONTEXT_STAGE_C_ENTRY_v0.1.md"
LONG_LOOP_DOC = TEAM_AI_CONTEXT / "TEAM_AI_CONTEXT_LONG_LOOP_v0.1.md"
STAGE_C_STATUS_DOC = TEAM_AI_CONTEXT / "TEAM_AI_CONTEXT_STAGE_C_STATUS_v0.1.md"
STAGE_C_FIXTURES = TEAM_AI_CONTEXT / "fixtures/stage-c"


def fresh_snapshot(**overrides):
    payload = {
        "schema": "engineering-command-snapshot:v0.2",
        "repo": "huanlongAI/hl-dispatch",
        "generated_at": "2026-06-25T00:00:00Z",
        "expires_at": "2026-06-25T00:30:00Z",
        "snapshot_ttl_minutes": 30,
        "wip_limit": 4,
        "snapshot_hash": "a" * 64,
        "receipt": {
            "schema": "engineering-command-snapshot-receipt:v0.1",
            "snapshot_hash": "a" * 64,
            "generated_at": "2026-06-25T00:00:00Z",
            "expires_at": "2026-06-25T00:30:00Z",
        },
        "external_writes": [],
        "source_coverage": {
            "github": {
                "repo": "huanlongAI/hl-dispatch",
                "issues": 1,
                "pull_requests": 0,
                "repo_files": 1,
            }
        },
        "snapshot_completeness": {
            "status": "complete",
            "missing": [],
        },
    }
    payload.update(overrides)
    return payload


def candidate(**overrides):
    payload = {
        "schema": "hl-ai-output-candidate:v0.1",
        "task_id": "HL-AI-C1",
        "candidate_action": "dry_run",
        "output": {
            "type": "github_issue",
            "target_surface": "github",
            "summary": "Create a local dry-run GitHub issue candidate.",
            "source_hash": "b" * 64,
        },
        "responsibility_gate": {
            "decision": "ACCEPT",
            "registry_version": "ROLE-REGISTRY-v1",
        },
        "context": {
            "context_id": "huanlong_platform",
            "context_status": "draft",
            "context_version": "TEAM_AI_CONTEXT_STAGE_C_ENTRY_v0.1",
            "source_truth_from_context_view": False,
        },
        "authorization": {
            "founder_gate_receipt_url": "https://github.com/huanlongAI/hl-dispatch/pull/407",
            "authorization_refs": ["stage-c-local-dry-run"],
        },
    }
    payload.update(overrides)
    return payload


class HLAICLITests(unittest.TestCase):
    def test_start_builds_session_package_from_natural_language_goal_without_writes(self):
        result = self.run_cli(
            "start",
            "--task-id",
            "HL-AI-C1",
            "--goal",
            "派发 server_deployment 给 ops，并先走本地 dry-run。",
            "--actor",
            "codex",
            "--repo",
            "huanlongAI/hl-dispatch",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        package = json.loads(result.stdout)
        self.assertEqual(package["schema"], "hl-ai-session-package:v0.1")
        self.assertEqual(package["mode"], "dry_run")
        self.assertEqual(package["task_id"], "HL-AI-C1")
        self.assertEqual(package["goal"], "派发 server_deployment 给 ops，并先走本地 dry-run。")
        self.assertEqual(package["repo"], "huanlongAI/hl-dispatch")
        self.assertEqual(package["next_allowed_action"], "submit_candidate_to_ai_admission_gate")
        self.assertEqual(package["external_writes"], [])
        self.assertFalse(package["github_write"]["enabled"])
        adapter_ids = [adapter["id"] for adapter in package["adapter_input_packages"]]
        self.assertEqual(adapter_ids, ["codex", "claude", "browser-ai"])
        self.assertEqual(package["adapter_input_packages"][0]["actor"], "codex")

    def test_submit_builds_ai_admission_request_and_accepts_fresh_github_issue_candidate(self):
        result = self.run_submit(candidate(), fresh_snapshot(), now="2026-06-25T00:10:00Z")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        submit = json.loads(result.stdout)
        self.assertEqual(submit["schema"], "hl-ai-submit-result:v0.1")
        self.assertEqual(submit["status"], "admission_accepted")
        self.assertEqual(submit["external_writes"], [])
        self.assertFalse(submit["github_write"]["enabled"])
        self.assertEqual(submit["admission_request"]["schema"], "ai-admission-request:v0.1")
        self.assertEqual(submit["admission_request"]["task_id"], "HL-AI-C1")
        self.assertEqual(submit["admission_request"]["output"]["type"], "github_issue")
        self.assertEqual(submit["admission_gate"]["decision"], "ACCEPT")
        self.assertIsNotNone(submit["admission_gate"]["receipt"])

    def test_submit_fails_closed_when_snapshot_is_expired(self):
        result = self.run_submit(candidate(), fresh_snapshot(), now="2026-06-25T00:31:00Z")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        submit = json.loads(result.stdout)
        self.assertEqual(submit["status"], "admission_rejected")
        self.assertEqual(submit["admission_gate"]["decision"], "REJECT")
        self.assertIn("snapshot_expired", submit["admission_gate"]["reason_codes"])
        self.assertEqual(submit["external_writes"], [])
        self.assertFalse(submit["github_write"]["enabled"])

    def test_submit_blocks_candidate_action_that_attempts_external_publish(self):
        result = self.run_submit(
            candidate(candidate_action="publish_github_issue"),
            fresh_snapshot(),
            now="2026-06-25T00:10:00Z",
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        submit = json.loads(result.stdout)
        self.assertEqual(submit["status"], "failed_closed")
        self.assertIn("candidate_action_requires_external_write_decision", submit["reason_codes"])
        self.assertNotIn("admission_gate", submit)
        self.assertEqual(submit["external_writes"], [])
        self.assertFalse(submit["github_write"]["enabled"])

    def test_submit_can_require_existing_admission_receipt_for_downstream_preflight(self):
        result = self.run_submit(
            candidate(),
            fresh_snapshot(),
            "--require-admission-receipt",
            now="2026-06-25T00:10:00Z",
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        submit = json.loads(result.stdout)
        self.assertEqual(submit["status"], "failed_closed")
        self.assertIn("admission_receipt_missing", submit["reason_codes"])
        self.assertEqual(submit["external_writes"], [])
        self.assertFalse(submit["github_write"]["enabled"])

    def test_stage_c_docs_and_fixtures_match_cli_contract(self):
        for path in [
            STAGE_C_ENTRY_DOC,
            LONG_LOOP_DOC,
            STAGE_C_FIXTURES / "session-package.json",
            STAGE_C_FIXTURES / "github-issue-candidate.json",
            STAGE_C_FIXTURES / "fresh-snapshot.json",
        ]:
            self.assertTrue(path.exists(), f"missing Stage C artifact: {path}")

        entry_doc = STAGE_C_ENTRY_DOC.read_text(encoding="utf-8")
        long_loop_doc = LONG_LOOP_DOC.read_text(encoding="utf-8")
        for doc in [entry_doc, long_loop_doc]:
            self.assertIn("## 术语说明", doc)
        self.assertIn("scripts/hl-ai.py start", entry_doc)
        self.assertIn("scripts/hl-ai.py submit", entry_doc)
        self.assertIn("TEAM-CONTEXT-ENFORCED", long_loop_doc)
        self.assertIn("future_condition_triggered_decision", long_loop_doc)

        result = self.run_cli(
            "submit",
            "--session",
            str(STAGE_C_FIXTURES / "session-package.json"),
            "--candidate",
            str(STAGE_C_FIXTURES / "github-issue-candidate.json"),
            "--snapshot",
            str(STAGE_C_FIXTURES / "fresh-snapshot.json"),
            "--now",
            "2026-06-25T00:10:00Z",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        submit = json.loads(result.stdout)
        self.assertEqual(submit["status"], "admission_accepted")
        self.assertEqual(submit["admission_gate"]["decision"], "ACCEPT")

    def test_stage_c_status_doc_keeps_enforcement_and_future_decisions_explicit(self):
        self.assertTrue(STAGE_C_STATUS_DOC.exists(), f"missing Stage C status: {STAGE_C_STATUS_DOC}")
        status_doc = STAGE_C_STATUS_DOC.read_text(encoding="utf-8")

        self.assertIn("Status: STAGE_C_LOCAL_TEAM_ENTRY_DRY_RUN_ACTIVE", status_doc)
        self.assertIn("## 术语说明", status_doc)
        self.assertIn("team_context_enforced: false", status_doc)
        self.assertIn("github_required_check_enabled: false", status_doc)
        self.assertIn("external_writes_enabled: false", status_doc)
        self.assertIn("Context Atlas", status_doc)
        self.assertIn("ai_loop_control", status_doc)
        self.assertIn("future_condition_triggered_decision", status_doc)

    def run_submit(self, candidate_payload, snapshot_payload, *extra_args, now):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            session_path = tmp_path / "session.json"
            candidate_path = tmp_path / "candidate.json"
            snapshot_path = tmp_path / "snapshot.json"
            session_path.write_text(
                json.dumps(
                    {
                        "schema": "hl-ai-session-package:v0.1",
                        "mode": "dry_run",
                        "task_id": "HL-AI-C1",
                        "repo": "huanlongAI/hl-dispatch",
                        "goal": "派发 server_deployment 给 ops，并先走本地 dry-run。",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            candidate_path.write_text(json.dumps(candidate_payload, ensure_ascii=False), encoding="utf-8")
            snapshot_path.write_text(json.dumps(snapshot_payload, ensure_ascii=False), encoding="utf-8")
            return self.run_cli(
                "submit",
                "--session",
                str(session_path),
                "--candidate",
                str(candidate_path),
                "--snapshot",
                str(snapshot_path),
                "--now",
                now,
                *extra_args,
            )

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
