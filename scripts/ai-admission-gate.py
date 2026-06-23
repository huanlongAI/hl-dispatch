#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


RESULT_SCHEMA = "ai-admission-gate-result:v0.1"
RECEIPT_SCHEMA = "ai-admission-gate-receipt:v0.1"
REQUEST_SCHEMA = "ai-admission-request:v0.1"
SNAPSHOT_SCHEMA = "engineering-command-snapshot:v0.2"
GATE_NAME = "AI_ADMISSION_GATE"
POLICY = {
    "snapshot_ttl_minutes": 30,
    "wip_limit": 4,
    "formal_output_scope_version": "huanlong-team-ai-context-v0.3-section-4.1",
    "github_minimum_gate_mode": "dry_run",
}

GITHUB_OUTPUT_TYPES = {
    "github_issue",
    "github_pr",
    "github_comment",
    "governance_record",
    "team_task",
    "code",
    "config",
    "contract",
    "migration",
    "release_candidate",
}
FORMAL_OUTPUT_TYPES = GITHUB_OUTPUT_TYPES | {
    "yunxiao_work_item",
    "yunxiao_pipeline_param",
    "yunxiao_release_input",
    "deploy",
    "runtime",
    "production",
    "release",
    "production_release",
    "payment",
    "provider",
    "real_data",
    "team_memory_approved_knowledge",
    "dynamic_truth_write",
}
SENSITIVE_OUTPUT_TYPES = {
    "deploy",
    "runtime",
    "production",
    "release",
    "production_release",
    "payment",
    "provider",
    "real_data",
    "team_memory_approved_knowledge",
    "dynamic_truth_write",
}


def parse_utc(value):
    text = str(value or "").strip()
    if not text:
        raise ValueError("empty timestamp")
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_hash(payload):
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _truthy_text(value):
    return bool(str(value or "").strip())


def _authorization_refs_hash(authorization):
    refs = authorization.get("authorization_refs")
    if not isinstance(refs, list):
        refs = []
    return canonical_hash([str(ref).strip() for ref in refs if str(ref).strip()])


def _bound_to(request):
    output = request.get("output") or {}
    snapshot = request.get("snapshot") or {}
    context = request.get("context") or {}
    responsibility_gate = request.get("responsibility_gate") or {}
    authorization = request.get("authorization") or {}
    return {
        "task_id": request.get("task_id", "unknown"),
        "repo": request.get("repo") or snapshot.get("repo") or "unknown",
        "output_type": output.get("type", "unknown"),
        "output_source_hash": output.get("source_hash", ""),
        "target_surface": output.get("target_surface", ""),
        "snapshot_hash": snapshot.get("snapshot_hash", ""),
        "context_id": context.get("context_id", ""),
        "context_version": context.get("context_version", ""),
        "responsibility_registry_version": responsibility_gate.get("registry_version", ""),
        "authorization_refs_hash": _authorization_refs_hash(authorization),
    }


def _receipt(bound_to, issued_at, expires_at):
    receipt_payload = {
        "schema": RECEIPT_SCHEMA,
        "gate": GATE_NAME,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "bound_to": bound_to,
    }
    receipt_hash = canonical_hash(receipt_payload)
    receipt_payload["receipt_id"] = f"aiag-{receipt_hash[:24]}"
    return receipt_payload


def _base_result(request, now, decision, reason_codes, receipt=None):
    return {
        "schema": RESULT_SCHEMA,
        "gate": GATE_NAME,
        "mode": request.get("mode", "dry_run"),
        "task_id": request.get("task_id", "unknown"),
        "repo": request.get("repo") or (request.get("snapshot") or {}).get("repo") or "unknown",
        "decision": decision,
        "reason_codes": reason_codes,
        "evaluated_at": now,
        "policy": POLICY,
        "receipt": receipt,
        "github_write": {
            "enabled": False,
            "operation": "none",
            "reason": "AI_ADMISSION_GATE is dry-run in Stage B; required GitHub checks need a separate Founder decision.",
        },
        "external_writes": [],
    }


def _snapshot_reason_codes(snapshot, now):
    reasons = []
    if snapshot.get("schema") != SNAPSHOT_SCHEMA:
        reasons.append("snapshot_schema_mismatch")
    if snapshot.get("snapshot_ttl_minutes") != POLICY["snapshot_ttl_minutes"]:
        reasons.append("snapshot_ttl_policy_mismatch")
    if snapshot.get("wip_limit") != POLICY["wip_limit"]:
        reasons.append("wip_limit_policy_mismatch")
    if snapshot.get("external_writes") != []:
        reasons.append("snapshot_contains_external_writes")
    if not _truthy_text(snapshot.get("snapshot_hash")):
        reasons.append("snapshot_hash_missing")
    receipt = snapshot.get("receipt") or {}
    if receipt.get("snapshot_hash") != snapshot.get("snapshot_hash"):
        reasons.append("snapshot_receipt_hash_mismatch")
    try:
        if parse_utc(now) > parse_utc(snapshot.get("expires_at")):
            reasons.append("snapshot_expired")
    except ValueError:
        reasons.append("snapshot_expiry_invalid")
    completeness = snapshot.get("snapshot_completeness") or {}
    if completeness.get("status") != "complete":
        reasons.append("snapshot_incomplete")
    return reasons


def _review_reason_codes(request):
    output = request.get("output") or {}
    output_type = output.get("type")
    target_surface = output.get("target_surface")
    reasons = []
    if output_type not in FORMAL_OUTPUT_TYPES:
        reasons.append("unknown_formal_output_type")
    if output_type not in GITHUB_OUTPUT_TYPES or target_surface != "github":
        reasons.append("unsupported_formal_surface")
    responsibility_gate = request.get("responsibility_gate") or {}
    if responsibility_gate.get("decision") == "REVIEW_REQUIRED":
        reasons.append("responsibility_gate_review_required")
    context = request.get("context") or {}
    if context.get("source_truth_from_context_view"):
        reasons.append("context_view_used_as_source_truth")
    return reasons


def _reject_reason_codes(request, now):
    output = request.get("output") or {}
    output_type = output.get("type")
    authorization = request.get("authorization") or {}
    responsibility_gate = request.get("responsibility_gate") or {}
    reasons = []
    if request.get("schema") != REQUEST_SCHEMA:
        reasons.append("request_schema_mismatch")
    reasons.extend(_snapshot_reason_codes(request.get("snapshot") or {}, now))
    if responsibility_gate.get("decision") == "REJECT":
        reasons.append("responsibility_gate_reject")
    if output_type in SENSITIVE_OUTPUT_TYPES and not _truthy_text(authorization.get("founder_gate_receipt_url")):
        reasons.append("missing_sensitive_authorization_receipt")
    prior_receipt = request.get("prior_receipt")
    if prior_receipt:
        prior_bound = prior_receipt.get("bound_to")
        if prior_bound != _bound_to(request):
            reasons.append("receipt_binding_mismatch")
    return sorted(set(reasons))


def evaluate(request, now=None):
    now = now or now_utc()
    reject_reasons = _reject_reason_codes(request, now)
    if reject_reasons:
        return _base_result(request, now, "REJECT", reject_reasons)

    review_reasons = sorted(set(_review_reason_codes(request)))
    if review_reasons:
        return _base_result(request, now, "REVIEW_REQUIRED", review_reasons)

    bound_to = _bound_to(request)
    receipt = _receipt(bound_to, now, (request.get("snapshot") or {}).get("expires_at", ""))
    return _base_result(request, now, "ACCEPT", ["admission_gate_accept"], receipt=receipt)


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Dry-run AI_ADMISSION_GATE for formal AI outputs.")
    parser.add_argument("--input", required=True, help="ai-admission-request:v0.1 JSON file.")
    parser.add_argument("--now", help="Override evaluated_at timestamp for deterministic tests.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    result = evaluate(load_json(args.input), now=args.now)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result["decision"] == "ACCEPT":
        return 0
    if result["decision"] == "REVIEW_REQUIRED":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
