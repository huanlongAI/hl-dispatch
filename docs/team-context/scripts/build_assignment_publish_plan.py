#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_task_assignment import load_structured_file, validate_assignment


TEAM_CONTEXT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = TEAM_CONTEXT / "ROLE-REGISTRY-v1.yaml"
DEFAULT_OWNERS = TEAM_CONTEXT / "ROLE-OWNERS-v1.yaml"
HIGH_RISK_TASK_TYPES = {
    "merchant_private_key",
    "real_payment_traffic_release",
    "reconciliation_evidence",
}
HIGH_RISK_REASON_CODES = {"unresolved_high_risk_responsibility"}


def _risk_level(payload, validation):
    if payload.get("task_type") in HIGH_RISK_TASK_TYPES:
        return "high"
    if HIGH_RISK_REASON_CODES.intersection(validation.get("reason_codes", [])):
        return "high"
    return "medium"


def _decision_packet(payload, validation):
    if validation["decision"] != "REVIEW_REQUIRED":
        return None
    task_type = payload.get("task_type") or validation.get("task_type") or "unknown"
    owner_role = validation.get("owner_role") or payload.get("assignee_role") or "unknown"
    return {
        "required": True,
        "risk_level": _risk_level(payload, validation),
        "decision_item": "是否允许该任务进入正式派发。",
        "background": "P1-A dry-run 发布计划器只生成裁决包，不写入 GitHub、飞书或外部系统。",
        "task_type": task_type,
        "owner_role": owner_role,
        "reason_codes": validation.get("reason_codes", []),
        "recommended_action": "补充 Founder / Gate 裁决后重新运行发布预检。",
        "minimum_reply_format": f"裁决：允许 / 拒绝 / 继续 REVIEW_REQUIRED；task_type={task_type}; owner_role={owner_role}",
    }


def _publish_plan(payload, validation):
    decision = validation["decision"]
    target_entrypoint = payload.get("assignment_entrypoint") or "unknown"
    if decision == "ACCEPT":
        return {
            "target_entrypoint": target_entrypoint,
            "action": "prepare_assignment_payload",
            "ready_for_formal_publisher": True,
            "manual_or_later_publisher_required": True,
        }
    if decision == "REJECT":
        return {
            "target_entrypoint": target_entrypoint,
            "action": "fail_closed_no_publish",
            "ready_for_formal_publisher": False,
            "manual_or_later_publisher_required": False,
        }
    return {
        "target_entrypoint": target_entrypoint,
        "action": "decision_packet_only",
        "ready_for_formal_publisher": False,
        "manual_or_later_publisher_required": False,
    }


def build_publish_plan(payload, registry_path=None, owners_path=None):
    validation = validate_assignment(
        payload,
        registry_path=registry_path or DEFAULT_REGISTRY,
        owners_path=owners_path or DEFAULT_OWNERS,
    )
    decision = validation["decision"]
    return {
        "schema": "assignment-publish-plan:v1",
        "mode": "dry_run",
        "source": "hl-dispatch/docs/team-context",
        "task_id": payload.get("task_id", "unknown"),
        "title": payload.get("title", ""),
        "publication_decision": decision,
        "blocked": decision != "ACCEPT",
        "fail_closed": decision == "REJECT",
        "validation": validation,
        "publish_plan": _publish_plan(payload, validation),
        "decision_packet": _decision_packet(payload, validation),
        "github_write": {
            "enabled": False,
            "operation": "none",
            "reason": "P1-A is dry-run/preflight only; external writes require a later formal publisher.",
        },
        "external_writes": [],
    }


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Build a dry-run assignment publish plan.")
    parser.add_argument("--input", required=True, help="JSON file containing one assignment payload.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="ROLE-REGISTRY path.")
    parser.add_argument("--owners", default=str(DEFAULT_OWNERS), help="ROLE-OWNERS path.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    payload = load_structured_file(args.input)
    plan = build_publish_plan(
        payload,
        registry_path=args.registry,
        owners_path=args.owners,
    )
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    if plan["publication_decision"] == "ACCEPT":
        return 0
    if plan["publication_decision"] == "REVIEW_REQUIRED":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
