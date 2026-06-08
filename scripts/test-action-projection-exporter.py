#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "export-action-projection.py"


def load_exporter():
    spec = importlib.util.spec_from_file_location("export_action_projection", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def label(name):
    return {"name": name}


class ActionProjectionExporterTests(unittest.TestCase):
    def test_exports_structured_work_unit_action(self):
        exporter = load_exporter()
        issues = [
            {
                "number": 200,
                "title": "[WU] DS-2 tenant entitlement quota check",
                "url": "https://github.com/huanlongAI/hl-dispatch/issues/200",
                "state": "OPEN",
                "labels": [label("task-assign")],
                "assignees": [{"login": "engineer-a"}],
                "updatedAt": "2026-06-08T01:02:03Z",
                "body": (
                    "### package_id\n"
                    "MP-DELIVERY-RECOVERY\n\n"
                    "### slice_id 或 risk_id\n"
                    "DS-2\n\n"
                    "### work_unit_id\n"
                    "WU-DS2-001\n\n"
                    "### DRI\n"
                    "@engineer-a\n\n"
                    "### risk_path\n"
                    "green\n\n"
                    "### next_action\n"
                    "Run quota_check three-case test and attach evidence.\n\n"
                    "### expected_evidence / evidence_exit\n"
                    "PR + 3 case test output\n"
                ),
            }
        ]

        projection = exporter.build_projection(
            issues,
            generated_at="2026-06-08T00:00:00Z",
        )

        self.assertEqual(projection["schema"], "action-projection:v0.1")
        self.assertEqual(projection["counts"]["total_input"], 1)
        self.assertEqual(projection["counts"]["exported"], 1)
        self.assertEqual(projection["counts"]["omitted_no_action"], 0)
        item = projection["items"][0]
        self.assertEqual(item["projection_class"], "action")
        self.assertEqual(item["package_id"], "MP-DELIVERY-RECOVERY")
        self.assertEqual(item["slice_id"], "DS-2")
        self.assertEqual(item["risk_id"], "n/a")
        self.assertEqual(item["work_unit_id"], "WU-DS2-001")
        self.assertEqual(item["dri"], "@engineer-a")
        self.assertEqual(item["risk_path"], "green")
        self.assertEqual(
            item["next_action"],
            "Run quota_check three-case test and attach evidence.",
        )
        self.assertEqual(item["expected_evidence"], "PR + 3 case test output")
        self.assertEqual(item["fact_source"], "github")
        self.assertEqual(item["warnings"], [])

    def test_exports_decision_signal_without_inventing_structured_ids(self):
        exporter = load_exporter()
        issues = [
            {
                "number": 201,
                "title": "[Decision] Select DS-1A or DS-1B",
                "url": "https://github.com/huanlongAI/hl-dispatch/issues/201",
                "state": "OPEN",
                "labels": [label("decision-request")],
                "assignees": [],
                "updatedAt": "2026-06-08T01:02:03Z",
                "body": "## 背景\n需要 Founder 裁决 DS-1A / DS-1B。",
            }
        ]

        projection = exporter.build_projection(
            issues,
            generated_at="2026-06-08T00:00:00Z",
        )

        self.assertEqual(projection["counts"]["exported"], 1)
        item = projection["items"][0]
        self.assertEqual(item["projection_class"], "decision")
        self.assertEqual(item["package_id"], "unknown")
        self.assertEqual(item["slice_id"], "unknown")
        self.assertEqual(
            item["next_action"],
            "Review GitHub issue for decision action.",
        )
        self.assertIn("missing_package_id", item["warnings"])
        self.assertIn("generated_next_action_from_projection_signal", item["warnings"])

    def test_omits_legacy_issue_without_action_signal(self):
        exporter = load_exporter()
        issues = [
            {
                "number": 202,
                "title": "[Legacy] old ledger note",
                "url": "https://github.com/huanlongAI/hl-dispatch/issues/202",
                "state": "OPEN",
                "labels": [label("governance")],
                "assignees": [],
                "updatedAt": "2026-06-08T01:02:03Z",
                "body": "历史总账说明，没有明确下一步动作。",
            }
        ]

        projection = exporter.build_projection(
            issues,
            generated_at="2026-06-08T00:00:00Z",
        )

        self.assertEqual(projection["counts"]["total_input"], 1)
        self.assertEqual(projection["counts"]["exported"], 0)
        self.assertEqual(projection["counts"]["omitted_no_action"], 1)
        self.assertEqual(projection["items"], [])

    def test_omits_generic_blocker_word_without_blocker_signal(self):
        exporter = load_exporter()
        issues = [
            {
                "number": 204,
                "title": "[PM Cap-Spec] payment checkout preflight",
                "url": "https://github.com/huanlongAI/hl-dispatch/issues/204",
                "state": "OPEN",
                "labels": [label("task-assign")],
                "assignees": [],
                "updatedAt": "2026-06-08T01:02:03Z",
                "body": "If unable to submit, reply with ETA or blocker.",
            }
        ]

        projection = exporter.build_projection(
            issues,
            generated_at="2026-06-08T00:00:00Z",
        )

        self.assertEqual(projection["counts"]["exported"], 0)
        self.assertEqual(projection["counts"]["omitted_no_action"], 1)

    def test_cli_reads_input_json_and_writes_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "issues.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "number": 203,
                            "title": "[WU] action",
                            "url": "https://github.com/huanlongAI/hl-dispatch/issues/203",
                            "state": "OPEN",
                            "labels": [],
                            "assignees": [],
                            "updatedAt": "2026-06-08T01:02:03Z",
                            "body": "### next_action\nRun local export smoke test.",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(input_path),
                    "--generated-at",
                    "2026-06-08T00:00:00Z",
                ],
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["counts"]["exported"], 1)
        self.assertEqual(payload["items"][0]["issue_number"], 203)

    def test_cli_writes_output_only_when_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "issues.json"
            output_path = Path(tmp) / "projection.json"
            input_path.write_text("[]", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                    "--generated-at",
                    "2026-06-08T00:00:00Z",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["counts"]["total_input"], 0)


if __name__ == "__main__":
    unittest.main()
