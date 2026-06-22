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
VALIDATOR = TEAM_CONTEXT / "scripts/validate_task_assignment.py"
RUNNER = TEAM_CONTEXT / "scripts/run_regression.py"
REGISTRY = TEAM_CONTEXT / "ROLE-REGISTRY-v1.yaml"
OWNERS = TEAM_CONTEXT / "ROLE-OWNERS-v1.yaml"
SCHEMA = TEAM_CONTEXT / "TASK-ASSIGNMENT-SCHEMA-v1.json"
CASES = TEAM_CONTEXT / "RESPONSIBILITY-REGRESSION-CASES-v1.yaml"

ALLOWED_DECISIONS = {"ACCEPT", "REJECT", "REVIEW_REQUIRED"}
CURRENT_REGISTRY_VERSION = "ROLE-REGISTRY-v1"


def load_validator():
    if not VALIDATOR.exists():
        raise AssertionError(f"missing validator: {VALIDATOR}")
    spec = importlib.util.spec_from_file_location("team_responsibility_gate", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assignment(task_type, assignee_role, **overrides):
    payload = {
        "task_id": f"case-{task_type}",
        "task_type": task_type,
        "assignee_role": assignee_role,
        "registry_version": CURRENT_REGISTRY_VERSION,
        "assignment_entrypoint": "github_issue",
        "formal_assignment": True,
        "authorization_refs": ["founder-decision-2026-06-22"],
    }
    payload.update(overrides)
    return payload


REQUIRED_REGRESSION_CASES = [
    (
        "reject_payment_provider_test_readiness_assigned_to_ops",
        assignment("payment_provider_test_business_readiness", "ops"),
        "REJECT",
    ),
    (
        "reject_payment_code_traffic_switch_assigned_to_ops",
        assignment("payment_code_traffic_switch", "ops"),
        "REJECT",
    ),
    (
        "reject_reconciliation_business_validation_assigned_to_ops",
        assignment("reconciliation_business_validation", "ops"),
        "REJECT",
    ),
    (
        "accept_server_deployment_assigned_to_ops",
        assignment("server_deployment", "ops"),
        "ACCEPT",
    ),
    (
        "reject_github_codeup_sync_topology_design_assigned_to_ops",
        assignment("github_codeup_sync_topology_design", "ops"),
        "REJECT",
    ),
    (
        "reject_technical_selection_assigned_to_business_operations",
        assignment("technical_selection", "business-operations"),
        "REJECT",
    ),
    (
        "review_required_merchant_private_key_assigned_to_product",
        assignment("merchant_private_key", "product-customer-payment"),
        "REVIEW_REQUIRED",
    ),
    (
        "reject_payment_release_declared_as_deployment_only",
        assignment("payment_release_declared_deployment_only", "ops"),
        "REJECT",
    ),
    (
        "reject_runtime_secret_injection_without_authorization_ref",
        assignment("runtime_secret_injection", "ops", authorization_refs=[]),
        "REJECT",
    ),
    (
        "reject_stale_responsibility_source",
        assignment("server_deployment", "ops", registry_version="ROLE-REGISTRY-v0"),
        "REJECT",
    ),
    (
        "review_required_unknown_task_type_auto_assignment",
        assignment("unknown_task_type", "ops", auto_dispatch=True),
        "REVIEW_REQUIRED",
    ),
    (
        "review_required_unresolved_high_risk_formal_assignment",
        assignment("real_payment_traffic_release", "ops"),
        "REVIEW_REQUIRED",
    ),
    (
        "accept_role_person_mapping_change_without_contract_change",
        assignment("server_deployment", "ops", assignee_github="replacement-gate-r"),
        "ACCEPT",
    ),
    (
        "reject_bypassing_formal_publisher",
        assignment("server_deployment", "ops", assignment_entrypoint="direct_release_bypass"),
        "REJECT",
    ),
]


class TeamResponsibilityGateTests(unittest.TestCase):
    def test_required_files_exist(self):
        for path in [VALIDATOR, RUNNER, REGISTRY, OWNERS, SCHEMA, CASES]:
            self.assertTrue(path.exists(), f"missing required team-context artifact: {path}")

    def test_required_regression_cases_match_expected_decisions(self):
        validator = load_validator()

        for case_id, payload, expected_decision in REQUIRED_REGRESSION_CASES:
            with self.subTest(case_id=case_id):
                result = validator.validate_assignment(
                    payload,
                    registry_path=REGISTRY,
                    owners_path=OWNERS,
                )
                self.assertIn(result["decision"], ALLOWED_DECISIONS)
                self.assertEqual(result["decision"], expected_decision)
                self.assertEqual(result["case_id"], payload["task_id"])

    def test_role_owner_mapping_can_change_without_contract_rewrite(self):
        validator = load_validator()
        owners_data = validator.load_structured_file(OWNERS)
        owners_data["roles"]["ops"]["github"] = "new-gate-r-handle"

        result = validator.validate_assignment(
            assignment("server_deployment", "ops"),
            registry_path=REGISTRY,
            owners_data=owners_data,
        )

        self.assertEqual(result["decision"], "ACCEPT")
        self.assertEqual(result["owner_role"], "ops")

    def test_runtime_secret_injection_with_authorization_still_requires_review(self):
        validator = load_validator()

        result = validator.validate_assignment(
            assignment(
                "runtime_secret_injection",
                "ops",
                authorization_refs=["runtime-secret-injection-approval"],
            ),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )

        self.assertEqual(result["decision"], "REVIEW_REQUIRED")
        self.assertIn("owner_not_in_allowed_roles", result["reason_codes"])

    def test_unknown_assignment_entrypoint_is_rejected(self):
        validator = load_validator()

        result = validator.validate_assignment(
            assignment("server_deployment", "ops", assignment_entrypoint="chat_backchannel"),
            registry_path=REGISTRY,
            owners_path=OWNERS,
        )

        self.assertEqual(result["decision"], "REJECT")
        self.assertIn("unknown_assignment_entrypoint", result["reason_codes"])

    def test_regression_case_file_covers_required_case_ids(self):
        validator = load_validator()
        case_data = validator.load_structured_file(CASES)
        actual = {case["id"]: case["expected_decision"] for case in case_data["cases"]}
        expected = {
            case_id: expected_decision
            for case_id, _payload, expected_decision in REQUIRED_REGRESSION_CASES
        }

        self.assertEqual(actual, expected)

    def test_schema_limits_decision_surface_to_three_states(self):
        self.assertTrue(SCHEMA.exists(), f"missing schema: {SCHEMA}")
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

        self.assertEqual(
            schema["properties"]["expected_decision"]["enum"],
            ["ACCEPT", "REJECT", "REVIEW_REQUIRED"],
        )

    def test_cli_validates_one_assignment_from_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "assignment.json"
            input_path.write_text(
                json.dumps(assignment("server_deployment", "ops")),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
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

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "ACCEPT")

    def test_regression_runner_passes_case_file(self):
        result = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--cases",
                str(CASES),
                "--registry",
                str(REGISTRY),
                "--owners",
                str(OWNERS),
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["counts"]["failed"], 0)
        self.assertEqual(
            payload["counts"]["total"],
            len(REQUIRED_REGRESSION_CASES),
        )


if __name__ == "__main__":
    unittest.main()
