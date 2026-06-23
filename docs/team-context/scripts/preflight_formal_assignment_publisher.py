#!/usr/bin/env python3
import argparse
import importlib.util
import json
import subprocess
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


def build_gh_issue_create_args(issue, repo):
    args = [
        "gh",
        "issue",
        "create",
        "--repo",
        repo,
        "--title",
        issue.get("title", ""),
        "--body",
        issue.get("body", ""),
    ]
    for label in issue.get("labels", []):
        args.extend(["--label", label])
    for assignee in issue.get("assignees", []):
        args.extend(["--assignee", assignee])
    return args


def _default_runner(args):
    return subprocess.run(args, capture_output=True, text=True)


def _base_publish_result(preflight, repo, execute):
    return {
        "schema": "hl-dispatch-formal-assignment-publisher:v1",
        "mode": "execute" if execute else "dry_run",
        "task_id": preflight.get("task_id", "unknown"),
        "status": "failed",
        "ready_to_create_github_issue": False,
        "preflight": preflight,
        "reason_codes": [],
        "github_write": {
            "enabled": False,
            "operation": "gh issue create",
            "repo": repo,
            "reason": "dry-run by default; --execute performs the GitHub write only after explicit approval.",
        },
        "external_writes": [],
    }


def publish_preflight_result(preflight, repo, execute=False, runner=None):
    result = _base_publish_result(preflight, repo, execute)
    issue = preflight.get("github_issue")
    if (
        preflight.get("status") != "passed"
        or not preflight.get("ready_to_create_github_issue")
        or not isinstance(issue, dict)
    ):
        result["reason_codes"] = list(preflight.get("reason_codes", [])) + ["preflight_not_ready"]
        return result

    language_gate = preflight.get("language_gate") or {}
    if language_gate.get("status") != "passed":
        result["reason_codes"] = list(preflight.get("reason_codes", [])) + ["github_language_gate_not_passed"]
        return result

    gh_args = build_gh_issue_create_args(issue, repo)
    result["ready_to_create_github_issue"] = True
    result["github_issue"] = issue
    result["command_preview"] = gh_args

    if not execute:
        result["status"] = "dry_run_ready"
        return result

    completed = (runner or _default_runner)(gh_args)
    if completed.returncode != 0:
        result["reason_codes"].append("gh_issue_create_failed")
        result["stderr"] = completed.stderr
        result["stdout"] = completed.stdout
        return result

    issue_url = completed.stdout.strip()
    result["status"] = "created"
    result["github_write"]["enabled"] = True
    result["github_issue_url"] = issue_url
    result["external_writes"] = [
        {
            "system": "github",
            "operation": "issue_create",
            "url": issue_url,
        }
    ]
    return result


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Dry-run preflight for hl-dispatch formal assignment publisher.")
    parser.add_argument("--input", required=True, help="assignment-publish-plan JSON file")
    parser.add_argument("--publish", action="store_true", help="Emit or execute the formal GitHub Issue publisher step.")
    parser.add_argument("--execute", action="store_true", help="Create the GitHub Issue after preflight passes.")
    parser.add_argument("--repo", default="huanlongAI/hl-dispatch", help="GitHub repository for issue creation.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if args.execute and not args.publish:
        raise SystemExit("--execute requires --publish")

    preflight = build_preflight(load_json(args.input))
    if args.publish:
        result = publish_preflight_result(preflight, repo=args.repo, execute=args.execute)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["status"] in {"dry_run_ready", "created"} else 1

    result = preflight
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
