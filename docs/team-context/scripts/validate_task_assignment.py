#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


TEAM_CONTEXT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = TEAM_CONTEXT / "ROLE-REGISTRY-v1.yaml"
DEFAULT_OWNERS = TEAM_CONTEXT / "ROLE-OWNERS-v1.yaml"


def load_structured_file(path):
    source_path = Path(path)
    text = source_path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError as json_error:
        try:
            import yaml  # type: ignore
        except ImportError as import_error:
            raise ValueError(
                f"{source_path} must be JSON-compatible YAML when PyYAML is unavailable"
            ) from import_error
        try:
            return yaml.safe_load(text)
        except Exception as yaml_error:
            raise ValueError(f"failed to parse {source_path}: {json_error}") from yaml_error


def _load_registry(registry_path=None, registry_data=None):
    if registry_data is not None:
        return registry_data
    return load_structured_file(registry_path or DEFAULT_REGISTRY)


def _load_owners(owners_path=None, owners_data=None):
    if owners_data is not None:
        return owners_data
    return load_structured_file(owners_path or DEFAULT_OWNERS)


def _normalise_role(role, owners):
    if role is None:
        return ""
    role_text = str(role).strip()
    aliases = owners.get("role_aliases", {})
    return aliases.get(role_text, role_text)


def _has_authorization_ref(payload):
    refs = payload.get("authorization_refs", [])
    return isinstance(refs, list) and any(str(ref).strip() for ref in refs)


def _result(payload, registry, task_type, owner_role, decision, reason_codes, messages):
    allowed_decisions = set(registry.get("allowed_decisions", []))
    if decision not in allowed_decisions:
        raise ValueError(f"unsupported decision: {decision}")
    return {
        "schema": "task-assignment-validation:v1",
        "case_id": payload.get("task_id", "unknown"),
        "decision": decision,
        "reason_codes": reason_codes,
        "messages": messages,
        "task_type": task_type,
        "owner_role": owner_role,
        "registry_version": registry.get("version"),
    }


def validate_assignment(
    payload,
    registry_path=None,
    owners_path=None,
    registry_data=None,
    owners_data=None,
):
    registry = _load_registry(registry_path, registry_data)
    owners = _load_owners(owners_path, owners_data)
    tasks = registry.get("task_types", {})
    owner_role = _normalise_role(payload.get("assignee_role"), owners)
    task_type = str(payload.get("task_type", "")).strip()
    payload_registry_version = str(payload.get("registry_version", "")).strip()

    if payload_registry_version != registry.get("version"):
        return _result(
            payload,
            registry,
            task_type,
            owner_role,
            "REJECT",
            ["stale_responsibility_source"],
            ["assignment registry_version does not match current ROLE-REGISTRY version"],
        )

    assignment_entrypoint = payload.get("assignment_entrypoint")
    if assignment_entrypoint in registry.get("forbidden_entrypoints", []):
        return _result(
            payload,
            registry,
            task_type,
            owner_role,
            "REJECT",
            ["formal_publisher_bypass"],
            ["assignment attempts to bypass the formal publisher or GitHub/repo SSOT path"],
        )

    if assignment_entrypoint not in registry.get("formal_entrypoints", []):
        return _result(
            payload,
            registry,
            task_type,
            owner_role,
            "REJECT",
            ["unknown_assignment_entrypoint"],
            ["assignment_entrypoint is not listed as a formal GitHub/repo SSOT path"],
        )

    task_rule = tasks.get(task_type)
    if not task_rule:
        reason_codes = ["unknown_task_type"]
        if payload.get("auto_dispatch"):
            reason_codes.append("auto_dispatch_blocked")
        return _result(
            payload,
            registry,
            task_type,
            owner_role,
            "REVIEW_REQUIRED",
            reason_codes,
            ["unknown task_type cannot be automatically assigned"],
        )

    if task_rule.get("requires_authorization_ref") and not _has_authorization_ref(payload):
        return _result(
            payload,
            registry,
            task_type,
            owner_role,
            "REJECT",
            ["missing_authorization_ref"],
            ["task requires an explicit authorization reference before assignment"],
        )

    if task_rule.get("risk_status") == "unresolved_high_risk":
        return _result(
            payload,
            registry,
            task_type,
            owner_role,
            "REVIEW_REQUIRED",
            ["unresolved_high_risk_responsibility"],
            ["high-risk responsibility is unresolved and requires review before formal dispatch"],
        )

    roles = owners.get("roles", {})
    if owner_role not in roles:
        return _result(
            payload,
            registry,
            task_type,
            owner_role,
            "REJECT",
            ["unknown_assignee_role"],
            ["assignee_role is not present in ROLE-OWNERS-v1"],
        )

    if owner_role in task_rule.get("disallowed_roles", []):
        return _result(
            payload,
            registry,
            task_type,
            owner_role,
            "REJECT",
            ["owner_explicitly_disallowed"],
            ["assignee_role is explicitly outside this task responsibility boundary"],
        )

    allowed_roles = task_rule.get("allowed_roles", [])
    if owner_role in allowed_roles:
        return _result(
            payload,
            registry,
            task_type,
            owner_role,
            "ACCEPT",
            ["owner_allowed"],
            ["assignee_role matches an allowed responsibility owner"],
        )

    return _result(
        payload,
        registry,
        task_type,
        owner_role,
        task_rule.get("default_decision", "REVIEW_REQUIRED"),
        ["owner_not_in_allowed_roles"],
        ["assignee_role is not listed as an allowed owner for this task type"],
    )


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Validate one hl-dispatch task assignment.")
    parser.add_argument("--input", required=True, help="JSON file containing one assignment payload.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="ROLE-REGISTRY path.")
    parser.add_argument("--owners", default=str(DEFAULT_OWNERS), help="ROLE-OWNERS path.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    payload = load_structured_file(args.input)
    result = validate_assignment(
        payload,
        registry_path=args.registry,
        owners_path=args.owners,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["decision"] == "ACCEPT":
        return 0
    if result["decision"] == "REVIEW_REQUIRED":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
