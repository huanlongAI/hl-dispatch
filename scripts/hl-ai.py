#!/usr/bin/env python3
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AI_ADMISSION_GATE = ROOT / "scripts/ai-admission-gate.py"
SESSION_SCHEMA = "hl-ai-session-package:v0.1"
CANDIDATE_SCHEMA = "hl-ai-output-candidate:v0.1"
SUBMIT_RESULT_SCHEMA = "hl-ai-submit-result:v0.1"
ADMISSION_REQUEST_SCHEMA = "ai-admission-request:v0.1"
EXECUTE_RESULT_SCHEMA = "hl-ai-execute-result:v1"
LANDING_INTAKE_SCHEMA = "hl-landing-intake:v1"
READBACK_RESULT_SCHEMA = "hl-ai-readback-result:v1"
CLOSE_RESULT_SCHEMA = "hl-ai-close-result:v1"
ALLOWED_CANDIDATE_ACTIONS = {
    "dry_run",
    "draft",
    "prepare_candidate",
    "submit_to_ai_admission_gate",
}
REQUIRED_CONTEXT_ARTIFACTS = [
    {
        "id": "team_ai_context_plan",
        "path": "docs/team-ai-context/PLAN-v0.3.md",
        "required": True,
        "purpose": "Load the current team AI context plan, status boundaries, and enforcement state.",
    },
    {
        "id": "team_ai_context_core_identities",
        "path": "docs/team-ai-context/CORE-IDENTITIES.md",
        "required": True,
        "purpose": "Resolve foundational AI route identities, especially xinzhehui -> NODE-D.",
    },
]
IDENTITY_RESOLUTION_RULES = {
    "xinzhehui": {
        "identity": "新者辉",
        "route": "xinzhehui -> NODE-D",
        "node": "NODE-D",
        "role": "Design",
        "owner_kind": "agent_route_not_human_account",
        "dispatch_contract": "Air Task Contract",
        "dispatch_mode": "product-experience",
        "blocked_status": "NODE-D_DISPATCH_BLOCKED",
        "source": "docs/team-ai-context/CORE-IDENTITIES.md",
    }
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical_hash(payload):
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def no_github_write(reason):
    return {
        "enabled": False,
        "operation": "none",
        "reason": reason,
    }


def load_ai_admission_gate():
    spec = importlib.util.spec_from_file_location("ai_admission_gate", AI_ADMISSION_GATE)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load AI admission gate: {AI_ADMISSION_GATE}")
    spec.loader.exec_module(module)
    return module


def build_session_package(task_id, goal, actor, repo):
    required_context_artifacts = [dict(item) for item in REQUIRED_CONTEXT_ARTIFACTS]
    identity_resolution_rules = json.loads(json.dumps(IDENTITY_RESOLUTION_RULES, ensure_ascii=False))
    base_input = {
        "task_id": task_id,
        "repo": repo,
        "goal": goal,
        "mode": "dry_run",
        "write_boundary": "hl-dispatch local files only; no GitHub, Feishu, Yunxiao, Context Atlas, or production writes.",
        "next_allowed_action": "submit_candidate_to_ai_admission_gate",
        "required_context_artifacts": required_context_artifacts,
        "identity_resolution_rules": identity_resolution_rules,
    }
    return {
        "schema": SESSION_SCHEMA,
        "mode": "dry_run",
        "task_id": task_id,
        "repo": repo,
        "goal": goal,
        "next_allowed_action": "submit_candidate_to_ai_admission_gate",
        "required_context_artifacts": required_context_artifacts,
        "identity_resolution_rules": identity_resolution_rules,
        "candidate_output_contract": {
            "schema": CANDIDATE_SCHEMA,
            "allowed_candidate_actions": sorted(ALLOWED_CANDIDATE_ACTIONS),
            "required_output_fields": ["type", "target_surface", "source_hash"],
            "required_gate": "AI_ADMISSION_GATE",
        },
        "adapter_input_packages": [
            {
                "id": "codex",
                "actor": actor,
                "input": dict(base_input),
            },
            {
                "id": "claude",
                "actor": "claude",
                "input": dict(base_input),
            },
            {
                "id": "browser-ai",
                "actor": "browser-ai",
                "status": "contract_only",
                "input": dict(base_input),
            },
        ],
        "github_write": no_github_write(
            "hl-ai start only builds a local session package; external writes require a later Founder decision."
        ),
        "external_writes": [],
    }


def base_submit_result(task_id, status, reason_codes=None):
    return {
        "schema": SUBMIT_RESULT_SCHEMA,
        "mode": "dry_run",
        "task_id": task_id,
        "status": status,
        "reason_codes": reason_codes or [],
        "github_write": no_github_write(
            "hl-ai submit is local dry-run only; it can only prepare or evaluate AI_ADMISSION_GATE input."
        ),
        "external_writes": [],
    }


def fail_closed(task_id, reason_codes):
    return base_submit_result(task_id, "failed_closed", reason_codes=reason_codes)


def safe_ref(value):
    raw = str(value or "unknown")
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in raw).strip("-") or "unknown"


def _candidate_action_reason(candidate):
    action = str(candidate.get("candidate_action", "dry_run") or "").strip()
    if action in ALLOWED_CANDIDATE_ACTIONS:
        return None
    return "candidate_action_requires_external_write_decision"


def _receipt_from_candidate(candidate):
    return candidate.get("prior_receipt") or candidate.get("admission_receipt")


def build_admission_request(session, candidate, snapshot):
    output = dict(candidate.get("output") or {})
    if not output.get("source_hash"):
        output["source_hash"] = canonical_hash(output)
    return {
        "schema": ADMISSION_REQUEST_SCHEMA,
        "mode": "dry_run",
        "task_id": candidate.get("task_id") or session.get("task_id", "unknown"),
        "repo": candidate.get("repo") or session.get("repo") or snapshot.get("repo") or "huanlongAI/hl-dispatch",
        "output": output,
        "snapshot": snapshot,
        "responsibility_gate": candidate.get("responsibility_gate") or {},
        "context": candidate.get("context")
        or {
            "context_id": "huanlong_platform",
            "context_status": "draft",
            "context_version": "TEAM_AI_CONTEXT_STAGE_C_ENTRY_v0.1",
            "source_truth_from_context_view": False,
        },
        "authorization": candidate.get("authorization") or {},
    }


def submit_candidate(session, candidate, snapshot, now=None, require_admission_receipt=False):
    task_id = candidate.get("task_id") or session.get("task_id", "unknown")
    if candidate.get("schema") != CANDIDATE_SCHEMA:
        return fail_closed(task_id, ["candidate_schema_mismatch"])
    if session.get("schema") != SESSION_SCHEMA:
        return fail_closed(task_id, ["session_schema_mismatch"])
    if session.get("task_id") and candidate.get("task_id") and session.get("task_id") != candidate.get("task_id"):
        return fail_closed(task_id, ["session_candidate_task_id_mismatch"])
    action_reason = _candidate_action_reason(candidate)
    if action_reason:
        return fail_closed(task_id, [action_reason])
    if require_admission_receipt and not _receipt_from_candidate(candidate):
        return fail_closed(task_id, ["admission_receipt_missing"])

    request = build_admission_request(session, candidate, snapshot)
    prior_receipt = _receipt_from_candidate(candidate)
    if prior_receipt:
        request["prior_receipt"] = prior_receipt
    admission_result = load_ai_admission_gate().evaluate(request, now=now)
    decision = admission_result.get("decision")
    status_by_decision = {
        "ACCEPT": "admission_accepted",
        "REJECT": "admission_rejected",
        "REVIEW_REQUIRED": "admission_review_required",
    }
    result = base_submit_result(task_id, status_by_decision.get(decision, "admission_unknown"))
    result["admission_request"] = request
    result["admission_gate"] = admission_result
    return result


def build_landing_intake(bundle):
    task_id = bundle.get("task_id", "unknown")
    return {
        "schema": LANDING_INTAKE_SCHEMA,
        "solution_id": "HL-AI-AUTHORIZED-EXECUTION-LANDING",
        "solution_version": "v1.0",
        "task_id": task_id,
        "repository": bundle.get("repository", "unknown"),
        "base_sha": bundle.get("base_sha", ""),
        "change_bundle_hash": canonical_hash(bundle),
        "change_bundle": bundle,
        "source": {
            "source_dispatch_id": bundle.get("source_dispatch_id", ""),
            "source_node": bundle.get("source_node", ""),
            "source_role": bundle.get("source_role", ""),
        },
        "client_boundary": {
            "github_write_enabled": False,
            "direct_push_enabled": False,
            "merge_enabled": False,
            "activation_enabled": False,
        },
    }


def execute_bundle(bundle, outbox):
    task_id = bundle.get("task_id", "unknown")
    intake = build_landing_intake(bundle)
    outbox_dir = Path(outbox)
    outbox_dir.mkdir(parents=True, exist_ok=True)
    outbox_ref = outbox_dir / f"{safe_ref(task_id)}-{intake['change_bundle_hash'][:12]}.json"
    outbox_ref.write_text(json.dumps(intake, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema": EXECUTE_RESULT_SCHEMA,
        "mode": "landing_client",
        "task_id": task_id,
        "status": "accepted_local_outbox",
        "intake": intake,
        "outbox_ref": str(outbox_ref),
        "next_allowed_action": "trusted_landing_control_plane_readback",
        "github_write": no_github_write("hl-ai execute only writes a local intake envelope; trusted Landing Control Plane owns GitHub writes."),
        "external_writes": [],
    }


def readback_receipt(receipt):
    return {
        "schema": READBACK_RESULT_SCHEMA,
        "task_id": receipt.get("task_id", "unknown"),
        "landing_state": receipt.get("landing_state", "LANDING_NOT_DONE"),
        "value_slice_state": receipt.get("value_slice_state", "VALUE_SLICE_NOT_CLOSED"),
        "activation_state": receipt.get("activation_state", "INACTIVE"),
        "machine_receipt": receipt,
        "github_write": no_github_write("hl-ai readback only reads a trusted machine receipt."),
        "external_writes": [],
    }


def close_from_receipt(receipt, closure_policy):
    reason_codes = []
    if receipt.get("schema") != "hl-landing-receipt:v1":
        reason_codes.append("receipt_schema_mismatch")
    if receipt.get("landing_state") != "LANDING_DONE":
        reason_codes.append("landing_not_done")
    if receipt.get("value_slice_state") != "VALUE_SLICE_CLOSED":
        reason_codes.append("value_slice_not_closed")
    if receipt.get("activation_state") != "INACTIVE":
        reason_codes.append("unexpected_activation_state")

    return {
        "schema": CLOSE_RESULT_SCHEMA,
        "task_id": receipt.get("task_id", "unknown"),
        "closure_policy": closure_policy,
        "status": "blocked" if reason_codes else "policy_closed",
        "reason_codes": reason_codes,
        "landing_state": receipt.get("landing_state", "LANDING_NOT_DONE"),
        "value_slice_state": receipt.get("value_slice_state", "VALUE_SLICE_NOT_CLOSED"),
        "activation_state": receipt.get("activation_state", "INACTIVE"),
        "github_write": no_github_write("hl-ai close does not write GitHub; closure requires trusted receipt and policy state."),
        "external_writes": [],
    }


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Local dry-run team AI entrypoint for hl-dispatch.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="Build a local hl-ai session package from a natural language goal.")
    start.add_argument("--task-id", required=True)
    start.add_argument("--goal", required=True)
    start.add_argument("--actor", default="codex")
    start.add_argument("--repo", default="huanlongAI/hl-dispatch")

    submit = subparsers.add_parser("submit", help="Submit a local output candidate to AI_ADMISSION_GATE.")
    submit.add_argument("--session", required=True)
    submit.add_argument("--candidate", required=True)
    submit.add_argument("--snapshot", required=True)
    submit.add_argument("--now")
    submit.add_argument("--require-admission-receipt", action="store_true")

    execute = subparsers.add_parser("execute", help="Create a local hl-landing-intake:v1 envelope for trusted Landing.")
    execute.add_argument("--bundle", required=True)
    execute.add_argument("--outbox", required=True)

    readback = subparsers.add_parser("readback", help="Read a trusted hl-landing-receipt:v1 machine receipt.")
    readback.add_argument("--receipt", required=True)

    close = subparsers.add_parser("close", help="Close only when machine receipt satisfies closure policy.")
    close.add_argument("--receipt", required=True)
    close.add_argument("--closure-policy", required=True, choices=["POLICY_CLOSE", "DOMAIN_CLOSE", "FOUNDER_CLOSE"])
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if args.command == "start":
        result = build_session_package(args.task_id, args.goal, args.actor, args.repo)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.command == "execute":
        result = execute_bundle(load_json(args.bundle), args.outbox)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.command == "readback":
        result = readback_receipt(load_json(args.receipt))
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.command == "close":
        result = close_from_receipt(load_json(args.receipt), args.closure_policy)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["status"] == "policy_closed" else 1

    result = submit_candidate(
        load_json(args.session),
        load_json(args.candidate),
        load_json(args.snapshot),
        now=args.now,
        require_admission_receipt=args.require_admission_receipt,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result["status"] == "admission_accepted":
        return 0
    if result["status"] == "admission_review_required":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
