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
ROLE_LABELS = {
    "architect": "architect",
    "ops": "ops",
    "product": "pm",
    "product-customer-payment": "pm",
    "product-capability-pack": "pm",
}
PRIORITY_LABELS = {
    "P0": "priority-p0",
    "P1": "priority-p1",
    "P2": "priority-p2",
}
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


def _priority_label(payload):
    raw_priority = str(payload.get("priority", "") or "").strip().upper()
    if not raw_priority:
        return ""
    priority_key = raw_priority.split(maxsplit=1)[0]
    return PRIORITY_LABELS.get(priority_key, "")


def _github_issue_body(payload, validation):
    reason_codes = ", ".join(validation.get("reason_codes", [])) or "none"
    messages = "\n".join(f"- {message}" for message in validation.get("messages", [])) or "- none"
    return "\n".join(
        [
            "## 任务派发",
            "",
            "本 Issue payload 由 hl-dispatch 职责门禁 dry-run 发布计划器生成；后续正式发布器只能在门禁 ACCEPT 后消费该 payload。",
            "",
            "```yaml",
            f"task_id: {payload.get('task_id', 'unknown')}",
            f"task_type: {payload.get('task_type', '')}",
            f"assignee_role: {validation.get('owner_role', payload.get('assignee_role', ''))}",
            f"registry_version: {validation.get('registry_version', payload.get('registry_version', ''))}",
            f"assignment_entrypoint: {payload.get('assignment_entrypoint', '')}",
            f"responsibility_gate_decision: {validation.get('decision', '')}",
            f"responsibility_reason_codes: [{reason_codes}]",
            "```",
            "",
            "## 职责门禁消息",
            messages,
            "",
            "## 任务正文",
            str(payload.get("body", "") or "").strip() or "（未提供正文）",
        ]
    )


def _formal_publisher_payload(payload, validation, owners):
    if validation["decision"] != "ACCEPT":
        return None
    owner_role = validation.get("owner_role") or payload.get("assignee_role") or ""
    owner = owners.get("roles", {}).get(owner_role, {})
    labels = ["task-assign"]
    role_label = ROLE_LABELS.get(owner_role)
    if role_label:
        labels.append(role_label)
    priority_label = _priority_label(payload)
    if priority_label:
        labels.append(priority_label)
    assignees = [owner["github"]] if str(owner.get("github", "") or "").strip() else []
    return {
        "schema": "hl-dispatch-formal-publisher-payload:v1",
        "target_entrypoint": payload.get("assignment_entrypoint") or "github_issue",
        "task_id": payload.get("task_id", "unknown"),
        "responsibility_gate": validation,
        "github_issue": {
            "title": payload.get("title") or f"[任务] {payload.get('task_type', 'unknown')}",
            "body": _github_issue_body(payload, validation),
            "labels": labels,
            "assignees": assignees,
        },
    }


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
    owners = load_structured_file(owners_path or DEFAULT_OWNERS)
    validation = validate_assignment(
        payload,
        registry_path=registry_path or DEFAULT_REGISTRY,
        owners_data=owners,
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
        "formal_publisher_payload": _formal_publisher_payload(payload, validation, owners),
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
