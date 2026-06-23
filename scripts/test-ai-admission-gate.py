#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "ai-admission-gate.py"


def load_gate():
    if not SCRIPT.exists():
        raise AssertionError("expected scripts/ai-admission-gate.py to exist")
    spec = importlib.util.spec_from_file_location("ai_admission_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fresh_snapshot(**overrides):
    payload = {
        "schema": "engineering-command-snapshot:v0.2",
        "repo": "huanlongAI/hl-dispatch",
        "generated_at": "2026-06-23T00:00:00Z",
        "expires_at": "2026-06-23T00:30:00Z",
        "snapshot_ttl_minutes": 30,
        "wip_limit": 4,
        "snapshot_hash": "a" * 64,
        "receipt": {
            "schema": "engineering-command-snapshot-receipt:v0.1",
            "snapshot_hash": "a" * 64,
            "generated_at": "2026-06-23T00:00:00Z",
            "expires_at": "2026-06-23T00:30:00Z",
        },
        "external_writes": [],
        "source_coverage": {
            "github": {
                "repo": "huanlongAI/hl-dispatch",
                "issues": 1,
                "pull_requests": 0,
                "repo_files": 0,
            }
        },
        "snapshot_completeness": {
            "status": "complete",
            "missing": [],
        },
    }
    payload.update(overrides)
    return payload


def candidate(output_type="github_issue", **overrides):
    payload = {
        "schema": "ai-admission-request:v0.1",
        "mode": "dry_run",
        "task_id": "HL-AI-GATE-P1",
        "repo": "huanlongAI/hl-dispatch",
        "output": {
            "type": output_type,
            "target_surface": "github",
            "summary": "Create a dry-run GitHub issue payload.",
            "source_hash": "b" * 64,
        },
        "snapshot": fresh_snapshot(),
        "responsibility_gate": {
            "decision": "ACCEPT",
            "registry_version": "ROLE-REGISTRY-v1",
        },
        "context": {
            "context_id": "huanlong_platform",
            "context_status": "draft",
            "context_version": "2026-06-23",
            "source_truth_from_context_view": False,
        },
        "authorization": {
            "founder_gate_receipt_url": "https://github.com/huanlongAI/hl-dispatch/issues/400#issuecomment-1",
            "authorization_refs": ["founder-decision-2026-06-23"],
        },
    }
    payload.update(overrides)
    return payload


class AIAdmissionGateTests(unittest.TestCase):
    def test_accepts_fresh_github_formal_output_and_mints_bound_receipt_without_writes(self):
        gate = load_gate()

        result = gate.evaluate(candidate(), now="2026-06-23T00:10:00Z")

        self.assertEqual(result["schema"], "ai-admission-gate-result:v0.1")
        self.assertEqual(result["gate"], "AI_ADMISSION_GATE")
        self.assertEqual(result["decision"], "ACCEPT")
        self.assertEqual(result["reason_codes"], ["admission_gate_accept"])
        self.assertEqual(result["mode"], "dry_run")
        self.assertEqual(result["external_writes"], [])
        self.assertFalse(result["github_write"]["enabled"])
        self.assertEqual(result["policy"]["snapshot_ttl_minutes"], 30)
        self.assertEqual(result["policy"]["wip_limit"], 4)
        receipt = result["receipt"]
        self.assertEqual(receipt["schema"], "ai-admission-gate-receipt:v0.1")
        self.assertRegex(receipt["receipt_id"], r"^aiag-[0-9a-f]{24}$")
        self.assertEqual(receipt["bound_to"]["task_id"], "HL-AI-GATE-P1")
        self.assertEqual(receipt["bound_to"]["output_type"], "github_issue")
        self.assertEqual(receipt["bound_to"]["snapshot_hash"], "a" * 64)
        self.assertEqual(receipt["bound_to"]["responsibility_registry_version"], "ROLE-REGISTRY-v1")

    def test_rejects_expired_snapshot(self):
        gate = load_gate()

        result = gate.evaluate(candidate(), now="2026-06-23T00:31:00Z")

        self.assertEqual(result["decision"], "REJECT")
        self.assertIn("snapshot_expired", result["reason_codes"])
        self.assertEqual(result["external_writes"], [])
        self.assertIsNone(result["receipt"])

    def test_rejects_replayed_receipt_bound_to_different_output(self):
        gate = load_gate()
        accepted = gate.evaluate(candidate(), now="2026-06-23T00:10:00Z")
        replay = candidate(
            output={
                "type": "github_issue",
                "target_surface": "github",
                "summary": "Changed output payload.",
                "source_hash": "c" * 64,
            },
            prior_receipt=accepted["receipt"],
        )

        result = gate.evaluate(replay, now="2026-06-23T00:11:00Z")

        self.assertEqual(result["decision"], "REJECT")
        self.assertIn("receipt_binding_mismatch", result["reason_codes"])
        self.assertIsNone(result["receipt"])

    def test_requires_review_for_yunxiao_surface_until_adapter_is_approved(self):
        gate = load_gate()

        result = gate.evaluate(candidate(output_type="yunxiao_work_item"), now="2026-06-23T00:10:00Z")

        self.assertEqual(result["decision"], "REVIEW_REQUIRED")
        self.assertIn("unsupported_formal_surface", result["reason_codes"])
        self.assertEqual(result["external_writes"], [])

    def test_rejects_sensitive_formal_output_without_founder_gate_receipt(self):
        gate = load_gate()

        result = gate.evaluate(
            candidate(
                output_type="production_release",
                authorization={"authorization_refs": []},
            ),
            now="2026-06-23T00:10:00Z",
        )

        self.assertEqual(result["decision"], "REJECT")
        self.assertIn("missing_sensitive_authorization_receipt", result["reason_codes"])
        self.assertIsNone(result["receipt"])

    def test_cli_outputs_json_and_exit_codes_for_gate_decisions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            accept_path = Path(tmpdir) / "accept.json"
            review_path = Path(tmpdir) / "review.json"
            reject_path = Path(tmpdir) / "reject.json"
            accept_path.write_text(json.dumps(candidate(), ensure_ascii=False), encoding="utf-8")
            review_path.write_text(json.dumps(candidate(output_type="yunxiao_work_item"), ensure_ascii=False), encoding="utf-8")
            reject_path.write_text(json.dumps(candidate(), ensure_ascii=False), encoding="utf-8")

            accept = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(accept_path), "--now", "2026-06-23T00:10:00Z"],
                capture_output=True,
                text=True,
            )
            review = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(review_path), "--now", "2026-06-23T00:10:00Z"],
                capture_output=True,
                text=True,
            )
            reject = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(reject_path), "--now", "2026-06-23T00:31:00Z"],
                capture_output=True,
                text=True,
            )

        self.assertEqual(accept.returncode, 0, accept.stdout + accept.stderr)
        self.assertEqual(json.loads(accept.stdout)["decision"], "ACCEPT")
        self.assertEqual(review.returncode, 3, review.stdout + review.stderr)
        self.assertEqual(json.loads(review.stdout)["decision"], "REVIEW_REQUIRED")
        self.assertEqual(reject.returncode, 1, reject.stdout + reject.stderr)
        self.assertEqual(json.loads(reject.stdout)["decision"], "REJECT")


if __name__ == "__main__":
    unittest.main()
