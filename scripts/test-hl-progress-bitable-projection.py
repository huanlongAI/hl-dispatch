#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "project-hl-progress-bitable.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "hl-progress-export.json"


def load_projector():
    if not SCRIPT.exists():
        raise AssertionError("expected scripts/project-hl-progress-bitable.py to exist")
    spec = importlib.util.spec_from_file_location("project_hl_progress_bitable", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HLProgressBitableProjectionTests(unittest.TestCase):
    def test_field_mapping_covers_required_hl_progress_fields(self):
        projector = load_projector()

        mapping = projector.bitable_field_mapping()
        sources = {entry["source_field"] for entry in mapping}

        self.assertEqual(
            {
                "task_id",
                "repo",
                "owner",
                "status",
                "risk_path",
                "evidence_state",
                "next_gate",
                "next_action",
                "blocker",
                "founder_decision_required",
                "github_link",
                "last_synced",
                "warnings",
            },
            sources,
        )
        self.assertTrue(all(entry["write_semantics"] == "projection_only" for entry in mapping))

    def test_projects_rows_and_ledger_without_external_write(self):
        projector = load_projector()
        export = json.loads(FIXTURE.read_text(encoding="utf-8"))

        projection = projector.build_projection(export, generated_at="2026-06-12T01:00:00Z")

        self.assertEqual(projection["schema"], "hl-progress-bitable-projection:v0.1")
        self.assertEqual(projection["mode"], "dry_run")
        self.assertEqual(projection["target"], "feishu_bitable")
        self.assertEqual(projection["counts"], {"input_items": 2, "rows": 2, "warnings": 5})
        self.assertIn("GitHub remains SSOT", projection["projection_notice"])
        row = projection["rows"][0]
        self.assertEqual(row["Task ID"], "HLPROG-P1-WU1")
        self.assertEqual(row["Repo"], "huanlongAI/hl-dispatch")
        self.assertEqual(row["Owner"], "@dahuizi")
        self.assertEqual(row["Status"], "in_progress")
        self.assertEqual(row["Risk Path"], "green")
        self.assertEqual(row["Evidence State"], "linked")
        self.assertEqual(row["Next Gate"], "offline deterministic tests")
        self.assertEqual(row["Next Action"], "Run hl-progress exporter deterministic tests.")
        self.assertEqual(row["Blocker"], "n/a")
        self.assertEqual(row["Founder Decision Required"], False)
        self.assertEqual(row["GitHub Link"], "https://github.com/huanlongAI/hl-dispatch/issues/301")
        self.assertEqual(row["Last Synced"], "2026-06-12T01:00:00Z")
        self.assertEqual(row["Warnings"], "")
        ledger_entry = projection["ledger"][0]
        self.assertEqual(ledger_entry["operation"], "dry_run_upsert_preview")
        self.assertFalse(ledger_entry["external_write"])
        self.assertEqual(ledger_entry["result"], "skipped_external_write")

    def test_rows_without_github_link_carry_warning(self):
        projector = load_projector()
        export = json.loads(FIXTURE.read_text(encoding="utf-8"))
        export["items"][0]["source"] = {
            "system": "github",
            "repo": "huanlongAI/hl-dispatch",
            "issue_url": "",
            "pr_urls": [],
            "file_refs": [],
        }

        projection = projector.build_projection(export, generated_at="2026-06-12T01:00:00Z")

        self.assertEqual(projection["rows"][0]["GitHub Link"], "unknown")
        self.assertIn("missing_github_link_for_projection", projection["ledger"][0]["warnings"])

    def test_cli_outputs_json_and_markdown_dry_run_ledger(self):
        json_result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(FIXTURE),
                "--generated-at",
                "2026-06-12T01:00:00Z",
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
                "2026-06-12T01:00:00Z",
                "--format",
                "markdown",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["counts"]["rows"], 2)
        self.assertEqual(markdown_result.returncode, 0, markdown_result.stderr)
        self.assertIn("# HL Progress Bitable Dry-Run Projection", markdown_result.stdout)
        self.assertIn("Projection only", markdown_result.stdout)
        self.assertIn("dry_run_upsert_preview", markdown_result.stdout)


if __name__ == "__main__":
    unittest.main()
