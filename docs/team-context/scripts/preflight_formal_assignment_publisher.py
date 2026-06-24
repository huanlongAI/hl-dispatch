#!/usr/bin/env python3
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LANGUAGE_GATE = REPO_ROOT / "scripts/check-github-language-gate.py"
LANGUAGE_WRITE_PREFLIGHT = REPO_ROOT / "scripts/preflight-github-language-write.py"
AI_ADMISSION_GATE = REPO_ROOT / "scripts/ai-admission-gate.py"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical_hash(payload):
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_language_gate():
    spec = importlib.util.spec_from_file_location("github_language_gate", LANGUAGE_GATE)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load language gate: {LANGUAGE_GATE}")
    spec.loader.exec_module(module)
    return module


def load_ai_admission_gate():
    spec = importlib.util.spec_from_file_location("ai_admission_gate", AI_ADMISSION_GATE)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load AI admission gate: {AI_ADMISSION_GATE}")
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


def build_ai_admission_request(plan, snapshot):
    formal_payload = plan.get("formal_publisher_payload") or {}
    issue = formal_payload.get("github_issue") or {}
    responsibility_gate = formal_payload.get("responsibility_gate") or {}
    output_source_hash = canonical_hash(issue)
    return {
        "schema": "ai-admission-request:v0.1",
        "mode": "dry_run",
        "task_id": formal_payload.get("task_id") or plan.get("task_id", "unknown"),
        "repo": snapshot.get("repo") or "huanlongAI/hl-dispatch",
        "output": {
            "type": "github_issue",
            "target_surface": "github",
            "summary": issue.get("title", ""),
            "source_hash": output_source_hash,
        },
        "snapshot": snapshot,
        "responsibility_gate": responsibility_gate,
        "context": {
            "context_id": "huanlong_platform",
            "context_status": "draft",
            "context_version": "AI_ADMISSION_GATE_v0.1",
            "source_truth_from_context_view": False,
        },
        "authorization": {
            "founder_gate_receipt_url": plan.get("founder_gate_receipt_url", ""),
            "authorization_refs": plan.get("authorization_refs", []),
        },
    }


def ai_admission_gate_result(plan, snapshot, now=None):
    gate = load_ai_admission_gate()
    return gate.evaluate(build_ai_admission_request(plan, snapshot), now=now)


def build_preflight(plan, admission_snapshot=None, require_ai_admission_gate=False, now=None):
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

    if require_ai_admission_gate:
        if not isinstance(admission_snapshot, dict):
            result["reason_codes"].append("ai_admission_snapshot_absent")
            return result
        admission_result = ai_admission_gate_result(plan, admission_snapshot, now=now)
        result["admission_gate"] = admission_result
        if admission_result.get("decision") != "ACCEPT":
            result["reason_codes"].append("ai_admission_gate_not_accept")
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


def build_language_write_preflight_args(issue, repo):
    return [
        sys.executable,
        str(LANGUAGE_WRITE_PREFLIGHT),
        "--kind",
        "issue",
        "--title",
        issue.get("title", ""),
        "--body",
        issue.get("body", ""),
        "--target-url",
        f"https://github.com/{repo}/issues/local-preflight",
    ]


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
        "required_execute_confirmation": "--confirm-github-issue-create",
        "github_write": {
            "enabled": False,
            "operation": "gh issue create",
            "repo": repo,
            "reason": "dry-run by default; --execute requires --confirm-github-issue-create before performing the GitHub write.",
        },
        "external_writes": [],
    }


def publish_preflight_result(
    preflight,
    repo,
    execute=False,
    confirm_create=False,
    runner=None,
    write_preflight_runner=None,
):
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

    write_preflight_args = build_language_write_preflight_args(issue, repo)
    gh_args = build_gh_issue_create_args(issue, repo)
    result["ready_to_create_github_issue"] = True
    result["github_issue"] = issue
    result["write_preflight_command_preview"] = write_preflight_args
    result["command_preview"] = gh_args

    if not execute:
        result["status"] = "dry_run_ready"
        return result

    if not confirm_create:
        result["reason_codes"].append("missing_execute_confirmation")
        return result

    write_preflight = (write_preflight_runner or _default_runner)(write_preflight_args)
    result["write_preflight"] = {
        "returncode": write_preflight.returncode,
        "stdout": write_preflight.stdout,
        "stderr": write_preflight.stderr,
    }
    if write_preflight.returncode != 0:
        result["reason_codes"].append("github_language_write_preflight_failed")
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
    parser.add_argument(
        "--require-ai-admission-gate",
        action="store_true",
        help="Require local AI_ADMISSION_GATE dry-run ACCEPT before the formal publisher is ready.",
    )
    parser.add_argument("--admission-snapshot", help="engineering-command-snapshot:v0.2 JSON file for AI_ADMISSION_GATE.")
    parser.add_argument("--now", help="Override AI_ADMISSION_GATE evaluated_at timestamp for deterministic tests.")
    parser.add_argument(
        "--confirm-github-issue-create",
        action="store_true",
        help="Required with --execute to confirm the external GitHub Issue write.",
    )
    parser.add_argument("--repo", default="huanlongAI/hl-dispatch", help="GitHub repository for issue creation.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if args.execute and not args.publish:
        raise SystemExit("--execute requires --publish")

    admission_snapshot = load_json(args.admission_snapshot) if args.admission_snapshot else None
    preflight = build_preflight(
        load_json(args.input),
        admission_snapshot=admission_snapshot,
        require_ai_admission_gate=args.require_ai_admission_gate,
        now=args.now,
    )
    if args.publish:
        result = publish_preflight_result(
            preflight,
            repo=args.repo,
            execute=args.execute,
            confirm_create=args.confirm_github_issue_create,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["status"] in {"dry_run_ready", "created"} else 1

    result = preflight
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
