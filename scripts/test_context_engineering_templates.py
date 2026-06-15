#!/usr/bin/env python3
"""Contract checks for Context Engineering fields in dispatch templates."""

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def assert_existing_file(test_case: unittest.TestCase, path: str) -> str:
    target = REPO_ROOT / path
    test_case.assertTrue(target.exists(), f"Expected file to exist: {path}")
    return target.read_text(encoding="utf-8")


class ContextEngineeringTemplateTests(unittest.TestCase):
    def test_work_unit_ai_output_requires_context_usage_summary(self) -> None:
        template = read(".github/ISSUE_TEMPLATE/work_unit.yml")

        for required in (
            "context_usage_summary:",
            'context_id: ""',
            'context_route: ""',
            "files_read: []",
            "missing_or_stale_context: []",
            "full_repo_scan_detected: false",
            "context_not_authorization: true",
        ):
            with self.subTest(required=required):
                self.assertIn(required, template)

    def test_package_and_slice_snapshots_expose_context_usage_summary(self) -> None:
        for path in (
            ".github/ISSUE_TEMPLATE/mission_package.yml",
            ".github/ISSUE_TEMPLATE/delivery_slice.yml",
            "docs/delivery-recovery/TASK_SNAPSHOT_v1.md",
        ):
            template = read(path)
            with self.subTest(path=path):
                self.assertIn("context_usage_summary:", template)
                self.assertIn('context_id: ""', template)
                self.assertIn('context_route: ""', template)
                self.assertIn("full_repo_scan_detected: false", template)
                self.assertIn("context_not_authorization: true", template)

    def test_ai_output_contract_exposes_context_usage_summary(self) -> None:
        doc = read("docs/delivery-recovery/AI_OUTPUT_CONTRACT_v1.md")

        for required in (
            "context_usage_summary:",
            'context_id: ""',
            'context_route: ""',
            "files_read: []",
            "missing_or_stale_context: []",
            "full_repo_scan_detected: false",
            "context_not_authorization: true",
        ):
            with self.subTest(required=required):
                self.assertIn(required, doc)

    def test_pull_request_template_requires_context_usage_summary(self) -> None:
        template = read(".github/pull_request_template.md")

        for required in (
            "Context Usage Summary",
            "context_usage_summary:",
            "context_not_authorization: true",
        ):
            with self.subTest(required=required):
                self.assertIn(required, template)

    def test_ci_runs_context_engineering_template_gate(self) -> None:
        workflow = assert_existing_file(
            self,
            ".github/workflows/context-engineering-template-gate.yml",
        )

        for required in (
            "pull_request:",
            "workflow_dispatch:",
            "push:",
            "schedule:",
            "30 2 * * 1-5",
            "AGENTS.md",
            "CLAUDE.md",
            "scripts/check-agent-governance-d10.sh",
            "python3 -B scripts/test_context_engineering_templates.py",
            "git diff --check",
        ):
            with self.subTest(required=required):
                self.assertIn(required, workflow)

        self.assertNotIn("repository: huanlongAI/sentinel-shared", workflow)
        self.assertNotIn("path: .sentinel-shared", workflow)

    def test_consistency_sentinel_governs_d10(self) -> None:
        workflow = read(".github/workflows/consistency-sentinel.yml")

        self.assertIn("pull_request:", workflow)
        self.assertIn("huanlongAI/sentinel-shared/.github/workflows/consistency-sentinel.yml@main", workflow)
        self.assertIn("D-10", workflow)

    def test_runbook_lists_context_engineering_template_gate(self) -> None:
        runbook = read("docs/delivery-recovery/HL_PROGRESS_OPERATION_RUNBOOK_v0.1.md")

        self.assertIn("PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_context_engineering_templates.py", runbook)

    def test_local_d10_agent_governance_entrypoint_exists(self) -> None:
        script = assert_existing_file(self, "scripts/check-agent-governance-d10.sh")
        runbook = read("docs/delivery-recovery/HL_PROGRESS_OPERATION_RUNBOOK_v0.1.md")

        for required in (
            "sentinel-shared/scripts/precheck-agent-governance.sh",
            ".sentinel-shared/scripts/precheck-agent-governance.sh",
            "D-10",
            "Agent governance projection drift",
        ):
            with self.subTest(required=required):
                self.assertIn(required, script)

        self.assertIn("bash scripts/check-agent-governance-d10.sh", runbook)

    def test_local_sentinel_results_are_ignored(self) -> None:
        gitignore = read(".gitignore")

        self.assertIn(".sentinel/results/", gitignore)

    def test_founder_spec_lane_makes_context_usage_mandatory_without_runtime_authority(self) -> None:
        doc = read("docs/delivery-recovery/FOUNDER_SPEC_LANE_v0.1.md")

        self.assertIn("Every PR, implementation plan, `gap_report`, or acceptance pack must include", doc)
        self.assertIn("Team assignees do not need to read Context Atlas directly.", doc)
        self.assertIn("context_not_authorization: true", doc)

    def test_delivery_recovery_contract_blocks_ai_guessing_without_context_pack_summary(self) -> None:
        doc = read("docs/delivery-recovery/DELIVERY_RECOVERY_IMPLEMENTATION_CONTRACT_v0.1.md")

        self.assertIn("AI 处理任何 Work Unit 前，必须有 Context Pack", doc)
        self.assertIn("context_usage_summary", doc)
        self.assertIn("full_repo_scan_detected", doc)
        self.assertIn("context_not_authorization: true", doc)


if __name__ == "__main__":
    unittest.main()
