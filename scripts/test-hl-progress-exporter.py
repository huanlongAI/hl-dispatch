#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "export-hl-progress.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "hl-progress-input.json"


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


if __name__ == "__main__":
    unittest.main()
