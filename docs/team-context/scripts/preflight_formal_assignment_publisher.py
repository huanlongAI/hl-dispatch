#!/usr/bin/env python3
import argparse
import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LANGUAGE_GATE = REPO_ROOT / "scripts/check-github-language-gate.py"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_language_gate():
    spec = importlib.util.spec_from_file_location("github_language_gate", LANGUAGE_GATE)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load language gate: {LANGUAGE_GATE}")
    spec.loader.exec_module(module)
    return module


def base_result(plan):
    return {
        "schema": "hl-dispatch-formal-publisher-preflight:v1",
        "mode": "dry_run",
        "task_id": plan.get("task_id", "unknown"),
        "status": "failed",
        "ready_to_create_github_issue": False,
        "reason_codes": [],
        "github_write": {
            "enabled": False,
            "operation": "none",
            "reason": "formal publisher preflight is dry-run only; external writes require an explicit later execute step.",
        },
        "external_writes": [],
    }


def language_gate_result(issue):
    language_gate = load_language_gate()
    return language_gate.validate_event(
        {
            "action": "opened",
            "issue": {
                "title": issue.get("title", ""),
                "body": issue.get("body", ""),
                "html_url": "https://github.com/huanlongAI/hl-dispatch/issues/local-preflight",
            },
        }
    )


def build_preflight(plan):
    result = base_result(plan)
    if plan.get("publication_decision") != "ACCEPT":
        result["reason_codes"].append("publication_decision_not_accept")
        return result

    formal_payload = plan.get("formal_publisher_payload")
    if not isinstance(formal_payload, dict):
        result["reason_codes"].append("formal_publisher_payload_absent")
        return result

    gate = formal_payload.get("responsibility_gate") or {}
    if gate.get("decision") != "ACCEPT":
        result["reason_codes"].append("responsibility_gate_not_accept")
        return result

    if formal_payload.get("target_entrypoint") != "github_issue":
        result["reason_codes"].append("unsupported_target_entrypoint")
        return result

    issue = formal_payload.get("github_issue")
    if not isinstance(issue, dict):
        result["reason_codes"].append("github_issue_payload_absent")
        return result

    language_result = language_gate_result(issue)
    result["language_gate"] = language_result
    if language_result.get("errors"):
        result["reason_codes"].append("github_language_gate_failed")
        return result

    result["status"] = "passed"
    result["ready_to_create_github_issue"] = True
    result["github_issue"] = {
        "title": issue.get("title", ""),
        "body": issue.get("body", ""),
        "labels": issue.get("labels", []),
        "assignees": issue.get("assignees", []),
    }
    return result


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Dry-run preflight for hl-dispatch formal assignment publisher.")
    parser.add_argument("--input", required=True, help="assignment-publish-plan JSON file")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    result = build_preflight(load_json(args.input))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
