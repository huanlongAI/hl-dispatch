#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote


EXPORT_SCHEMA = "hl-progress-export:v0.1"
ITEM_SCHEMA = "hl-progress-work-item:v0.1"
SNAPSHOT_SCHEMA = "engineering-command-snapshot:v0.2"
SOURCE_SYSTEM = "github"
ISSUE_JSON_FIELDS = "number,title,url,state,labels,assignees,updatedAt,body"
PR_JSON_FIELDS = "number,title,url,state,labels,assignees,updatedAt,body,isDraft,reviewDecision,author,mergedAt"
HEADING_RE = re.compile(r"^#{2,6}\s+(.+?)\s*$")

EMPTY_VALUES = {
    "",
    "-",
    "n/a",
    "na",
    "none",
    "null",
    "unknown",
    "tbd",
    "无",
    "待补",
}

STATUS_VALUES = {
    "design",
    "decision_required",
    "bounded_implementation",
    "pr_evidence",
    "merged_pending_readback",
    "accepted",
    "closed",
    "queued",
    "history",
    "intake",
    "planned",
    "ready",
    "in_progress",
    "blocked",
    "review",
    "gate_a",
    "gate_b",
    "human_cross_audit",
    "founder_acceptance",
    "done",
    "rejected",
    "archived",
}

EVIDENCE_VALUES = {"none", "claimed", "linked", "verified", "accepted"}
RISK_VALUES = {"green", "yellow", "red"}
OWNER_ROLES = {"founder", "dahuizi", "pm", "engineer", "gate", "qa", "ops", "unknown"}
LANE_NAMES = ("current", "waiting_decision", "waiting_readback", "queued", "history")
CURRENT_COMMAND_STATES = {"design", "bounded_implementation", "pr_evidence"}
WAITING_DECISION_STATES = {"decision_required", "blocked"}
WAITING_READBACK_STATES = {"merged_pending_readback"}
QUEUED_STATES = {"queued"}
HISTORY_STATES = {"accepted", "closed", "history", "done", "rejected", "archived"}
AUTHORIZATION_BOOL_FIELDS = (
    "pm_readiness",
    "engineering_scope_confirmed",
    "implementation_authorized",
    "runtime_authorized",
    "deployment_authorized",
    "production_authorized",
    "release_authorized",
)
TRUE_VALUES = {"true", "yes", "y", "1", "ready", "pass", "passed", "approved", "authorized", "granted"}
FALSE_VALUES = {"false", "no", "n", "0", "blocked", "denied", "gated", "not_authorized", "not authorized"}
SENSITIVE_SCOPE_TERMS = {
    "payment",
    "provider",
    "production",
    "real-user-data",
    "real user data",
    "real_user_data",
    "secrets",
    "secret",
    "billing",
    "refund",
    "settlement",
    "deploy",
    "deployment",
    "release",
    "支付",
    "生产",
    "真实用户",
    "供应商",
    "凭据",
}


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value):
    normalized = (value or "").strip()
    if not normalized:
        raise ValueError("empty timestamp")
    return datetime.fromisoformat(normalized.replace("Z", "+00:00"))


def plus_hours_utc(value, hours):
    return (parse_utc(value) + timedelta(hours=hours)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def plus_minutes_utc(value, minutes):
    return (parse_utc(value) + timedelta(minutes=minutes)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_label(label):
    value = (label or "").strip().strip(":")
    value = value.replace("`", "")
    value = value.replace("_", " ")
    value = re.sub(r"\s+", " ", value)
    return value.lower()


def normalize_key(label):
    return normalize_label(label).replace(" ", "_")


def normalize_value(value):
    return (value or "").strip().strip()


def parse_bool(value):
    normalized = normalize_key(value)
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return False


def is_concrete(value):
    normalized = normalize_value(value).lower().strip(":：。.")
    return normalized not in EMPTY_VALUES


def labels_from(record):
    labels = []
    for label in record.get("labels") or []:
        if isinstance(label, dict):
            name = label.get("name")
        else:
            name = str(label)
        if name:
            labels.append(name)
    return labels


def assignees_from(record):
    assignees = []
    for assignee in record.get("assignees") or []:
        if isinstance(assignee, dict):
            login = assignee.get("login") or assignee.get("name")
        else:
            login = str(assignee)
        if login:
            assignees.append(login)
    return assignees


def parse_sections(body):
    sections = {}
    current_label = None
    current_lines = []

    def flush():
        if not current_label:
            return
        sections[current_label] = "\n".join(current_lines).strip()

    for line in (body or "").splitlines():
        match = HEADING_RE.match(line)
        if match:
            flush()
            current_label = normalize_key(match.group(1))
            current_lines = []
            continue
        if current_label:
            current_lines.append(line)

    flush()
    return sections


def section_value(sections, *aliases):
    for alias in aliases:
        key = normalize_key(alias)
        if key in sections:
            return normalize_value(sections[key])
    return ""


def canonical_hash(payload):
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def handle_for(login):
    if not is_concrete(login):
        return "unknown"
    value = normalize_value(login)
    return value if value.startswith("@") else f"@{value}"


def lower_labels(record):
    return {label.lower() for label in labels_from(record)}


def has_decision_signal(record, sections):
    labels = lower_labels(record)
    title = (record.get("title") or "").lower()
    body = (record.get("body") or record.get("content") or "").lower()
    explicit = section_value(sections, "founder_decision_required", "decision_required")
    return (
        "decision-request" in labels
        or "action:decision_required" in labels
        or "[decision]" in title
        or explicit.lower() in {"true", "yes", "required"}
        or "founder decision required" in body
    )


def has_blocker_signal(record, sections):
    labels = lower_labels(record)
    title = (record.get("title") or "").lower()
    blocker = section_value(sections, "blocker", "current_blocker", "blocked_by")
    return (
        "blocked" in labels
        or "blocker" in labels
        or "action:blocker" in labels
        or re.search(r"\[[^\]]*blocker[^\]]*\]", title)
        or (is_concrete(blocker) and blocker.lower() != "none")
    )


def normalize_status(raw):
    value = normalize_key(raw)
    aliases = {
        "open": "intake",
        "ready_for_review": "review",
        "evidence_pending": "review",
        "closed": "archived",
    }
    value = aliases.get(value, value)
    return value if value in STATUS_VALUES else ""


def derive_status(kind, record, sections):
    explicit = normalize_status(section_value(sections, "status", "current_status", "state"))
    if explicit:
        return explicit
    if has_decision_signal(record, sections):
        return "founder_acceptance"
    if has_blocker_signal(record, sections):
        return "blocked"
    if kind == "pull_request":
        if record.get("isDraft"):
            return "in_progress"
        if (record.get("state") or "").upper() == "OPEN":
            return "review"
        return "archived"
    if kind == "issue" and (record.get("state") or "").upper() == "OPEN":
        return "intake"
    return "unknown"


def derive_risk_path(record, sections, warnings):
    explicit = section_value(sections, "risk_path", "risk")
    risk = normalize_key(explicit)
    if risk in RISK_VALUES:
        return risk
    for label in lower_labels(record):
        if label.startswith("risk:"):
            risk = label.split(":", 1)[1].strip().lower()
            if risk in RISK_VALUES:
                return risk
    warnings.append("missing_risk_path")
    return "unknown"


def derive_evidence_state(sections, warnings):
    evidence_state = normalize_key(section_value(sections, "evidence_state"))
    if evidence_state in EVIDENCE_VALUES:
        return evidence_state
    warnings.append("missing_evidence_state")
    return "unknown"


def derive_owner(kind, record, sections, warnings):
    owner = section_value(sections, "owner_github", "github_owner", "dri", "package_owner")
    assignees = assignees_from(record)
    if not is_concrete(owner) and assignees:
        owner = assignees[0]
    if not is_concrete(owner) and kind == "pull_request":
        author = record.get("author") or {}
        if isinstance(author, dict):
            owner = author.get("login") or author.get("name")
    github = handle_for(owner)
    if github == "unknown":
        warnings.append("missing_owner")

    role = normalize_key(section_value(sections, "owner_role", "role"))
    if role not in OWNER_ROLES:
        role = "unknown"
    return {"github": github, "role": role}


def derive_task_id(kind, record, sections, warnings):
    task_id = section_value(sections, "task_id", "work_unit_id", "work_unit")
    if is_concrete(task_id):
        return task_id
    number = record.get("number")
    if number:
        return f"{'pr' if kind == 'pull_request' else 'issue'}-{number}"
    path = record.get("path")
    if is_concrete(path):
        return f"file:{path}"
    warnings.append("missing_task_id")
    return "unknown"


def derive_next_gate(kind, record, sections, status):
    explicit = section_value(sections, "next_gate", "gate")
    if is_concrete(explicit):
        return explicit
    if status == "founder_acceptance":
        return "Founder"
    if kind == "pull_request" and status == "review":
        return "PR review"
    return "n/a"


def derive_next_action(sections, warnings):
    next_action = section_value(sections, "next_action")
    if is_concrete(next_action):
        return next_action
    warnings.append("missing_next_action")
    return "n/a"


def derive_blocker(record, sections):
    blocker = section_value(sections, "blocker", "current_blocker", "blocked_by")
    if has_blocker_signal(record, sections):
        summary = blocker if is_concrete(blocker) and blocker.lower() != "none" else "active blocker signal in GitHub source"
        owner = section_value(sections, "blocker_owner")
        return {
            "state": "active",
            "summary": summary,
            "owner": handle_for(owner) if is_concrete(owner) else "n/a",
        }
    return {"state": "none", "summary": "n/a", "owner": "n/a"}


def source_for(kind, repo, record, warnings):
    if kind == "issue":
        issue_url = record.get("url") or record.get("html_url") or ""
        pr_urls = []
        file_refs = []
    elif kind == "pull_request":
        issue_url = ""
        pr_url = record.get("url") or record.get("html_url") or ""
        pr_urls = [pr_url] if pr_url else []
        file_refs = []
    else:
        issue_url = ""
        pr_urls = []
        ref = record.get("url") or record.get("path") or ""
        file_refs = [ref] if ref else []

    if not issue_url and not pr_urls and not file_refs:
        warnings.append("missing_github_source_link")

    return {
        "system": SOURCE_SYSTEM,
        "repo": repo or "unknown",
        "issue_url": issue_url,
        "pr_urls": pr_urls,
        "file_refs": file_refs,
    }


def build_item(kind, repo, record, generated_at):
    content = record.get("body") if kind != "repo_file" else record.get("content")
    sections = parse_sections(content or "")
    warnings = []
    task_id = derive_task_id(kind, record, sections, warnings)
    owner = derive_owner(kind, record, sections, warnings)
    status = derive_status(kind, record, sections)
    risk_path = derive_risk_path(record, sections, warnings)
    evidence_state = derive_evidence_state(sections, warnings)
    if status == "done" and evidence_state != "accepted":
        warnings.append("done_requires_accepted_evidence")
        status = "unknown"
    next_gate = derive_next_gate(kind, record, sections, status)
    next_action = derive_next_action(sections, warnings)
    blocker = derive_blocker(record, sections)
    founder_decision_required = has_decision_signal(record, sections)
    source = source_for(kind, repo, record, warnings)

    if status == "unknown":
        warnings.append("missing_status")
    if status == "blocked" and blocker["state"] == "none":
        warnings.append("blocked_requires_blocker_state")

    return {
        "schema": ITEM_SCHEMA,
        "task_id": task_id,
        "source": source,
        "owner": owner,
        "status": status,
        "risk_path": risk_path,
        "evidence_state": evidence_state,
        "next_gate": next_gate,
        "next_action": next_action,
        "blocker": blocker,
        "founder_decision_required": founder_decision_required,
        "projection": {
            "target": "json",
            "generated_at": generated_at,
            "source_hash": canonical_hash({"kind": kind, "repo": repo, "record": record}),
        },
        "warnings": sorted(set(warnings)),
    }


def normalize_input(raw):
    if isinstance(raw, list):
        return {"repo": "unknown", "issues": raw, "pull_requests": [], "files": []}
    if not isinstance(raw, dict):
        raise ValueError("input JSON must be an object or a list of GitHub issues")
    return {
        "repo": raw.get("repo") or raw.get("repository") or "unknown",
        "issues": raw.get("issues") or [],
        "pull_requests": raw.get("pull_requests") or raw.get("prs") or [],
        "files": raw.get("files") or raw.get("repo_files") or [],
    }


def build_export(raw_source, generated_at=None, repo=None):
    normalized = normalize_input(raw_source)
    generated_at = generated_at or now_utc()
    repo = repo or normalized["repo"]

    items = []
    for issue in normalized["issues"]:
        items.append(build_item("issue", repo, issue, generated_at))
    for pull_request in normalized["pull_requests"]:
        items.append(build_item("pull_request", repo, pull_request, generated_at))
    for repo_file in normalized["files"]:
        items.append(build_item("repo_file", repo, repo_file, generated_at))

    warning_count = sum(len(item["warnings"]) for item in items)
    return {
        "schema": EXPORT_SCHEMA,
        "source": SOURCE_SYSTEM,
        "repo": repo,
        "generated_at": generated_at,
        "counts": {
            "issues": len(normalized["issues"]),
            "pull_requests": len(normalized["pull_requests"]),
            "repo_files": len(normalized["files"]),
            "items": len(items),
            "warnings": warning_count,
        },
        "items": items,
    }


def record_sequence(normalized):
    records = []
    for issue in normalized["issues"]:
        records.append(("issue", issue))
    for pull_request in normalized["pull_requests"]:
        records.append(("pull_request", pull_request))
    for repo_file in normalized["files"]:
        records.append(("repo_file", repo_file))
    return records


def source_query_summary(normalized, repo):
    return [
        {
            "system": SOURCE_SYSTEM,
            "repo": repo,
            "mode": "read_only_projection",
            "issues": len(normalized["issues"]),
            "pull_requests": len(normalized["pull_requests"]),
            "repo_files": len(normalized["files"]),
        }
    ]


def source_coverage(normalized, repo):
    return {
        SOURCE_SYSTEM: {
            "repo": repo,
            "issues": len(normalized["issues"]),
            "pull_requests": len(normalized["pull_requests"]),
            "repo_files": len(normalized["files"]),
        }
    }


def snapshot_completeness(normalized):
    missing = []
    if not normalized["issues"] and not normalized["pull_requests"] and not normalized["files"]:
        missing.append("github_sources")
    return {
        "status": "complete" if not missing else "incomplete",
        "missing": missing,
    }


def open_issue_index(normalized):
    index = {}
    for issue in normalized["issues"]:
        number = issue.get("number")
        if number is None:
            continue
        if (issue.get("state") or "").upper() == "OPEN":
            index[int(number)] = {
                "number": int(number),
                "url": issue.get("url") or issue.get("html_url") or "",
                "title": issue.get("title") or "",
            }
    return index


def referenced_issue_numbers(record):
    text = "\n".join([record.get("title") or "", record.get("body") or record.get("content") or ""])
    return sorted({int(match) for match in re.findall(r"(?<![\w/-])#(\d+)\b", text)})


def merged_open_issue_refs(kind, record, open_issues):
    if kind != "pull_request" or not is_concrete(record.get("mergedAt")):
        return []
    refs = []
    for number in referenced_issue_numbers(record):
        if number in open_issues:
            refs.append(open_issues[number])
    return refs


def detect_sensitive_scope(record):
    labels = " ".join(labels_from(record)).lower()
    text = "\n".join([record.get("title") or "", record.get("body") or record.get("content") or "", labels]).lower()
    return any(term in text for term in SENSITIVE_SCOPE_TERMS)


def derive_authorization(record, warnings):
    sections = parse_sections(record.get("body") or record.get("content") or "")
    authorization = {}
    for field in AUTHORIZATION_BOOL_FIELDS:
        authorization[field] = parse_bool(section_value(sections, field))
    receipt = section_value(sections, "founder_gate_receipt_url", "founder_gate_receipt", "gate_receipt")
    authorization["founder_gate_receipt_url"] = receipt if is_concrete(receipt) else ""

    if detect_sensitive_scope(record) and not authorization["founder_gate_receipt_url"]:
        for field in ("runtime_authorized", "deployment_authorized", "production_authorized", "release_authorized"):
            authorization[field] = False
        warnings.append("sensitive_scope_gated_without_founder_gate_receipt")

    return authorization


def command_state_for(kind, record, item, open_issues):
    if merged_open_issue_refs(kind, record, open_issues):
        return "merged_pending_readback"

    status = item["status"]
    if status in {
        "design",
        "decision_required",
        "bounded_implementation",
        "pr_evidence",
        "accepted",
        "closed",
        "queued",
        "history",
        "blocked",
    }:
        return status
    if item["founder_decision_required"] or status == "founder_acceptance":
        return "decision_required"
    if status in {"planned", "ready"}:
        return "design"
    if status in {"intake", "in_progress"}:
        return "bounded_implementation"
    if status in {"review", "gate_a", "gate_b", "human_cross_audit"}:
        return "pr_evidence"
    if status == "done":
        return "accepted"
    if status in {"rejected", "archived"}:
        return "history"
    if (record.get("state") or "").upper() == "CLOSED":
        return "closed"
    return "design"


def lane_for_command_state(command_state):
    if command_state in CURRENT_COMMAND_STATES:
        return "current"
    if command_state in WAITING_DECISION_STATES:
        return "waiting_decision"
    if command_state in WAITING_READBACK_STATES:
        return "waiting_readback"
    if command_state in QUEUED_STATES:
        return "queued"
    if command_state in HISTORY_STATES:
        return "history"
    return "current"


def compact_snapshot_item(kind, record, item, command_state, lane, linked_open_issues=None):
    warnings = list(item["warnings"])
    authorization = derive_authorization(record, warnings)
    return {
        "schema": ITEM_SCHEMA,
        "task_id": item["task_id"],
        "source_kind": kind,
        "source_number": record.get("number"),
        "source": item["source"],
        "owner": item["owner"],
        "status": item["status"],
        "command_state": command_state,
        "lane": lane,
        "risk_path": item["risk_path"],
        "evidence_state": item["evidence_state"],
        "next_gate": item["next_gate"],
        "next_action": item["next_action"],
        "founder_decision_required": item["founder_decision_required"],
        "authorization": authorization,
        "linked_open_issues": linked_open_issues or [],
        "warnings": sorted(set(warnings)),
    }


def action_for_decision(item):
    return {
        "type": "decision_request_candidate",
        "task_id": item["task_id"],
        "source": primary_link(item),
        "reason": "GitHub source carries a Founder/Gate decision signal.",
        "recommendation_only": True,
        "required_gate": "AI_ADMISSION_GATE",
        "external_write": False,
    }


def action_for_readback(item, linked_open_issues):
    return {
        "type": "merge_readback_candidate",
        "task_id": item["task_id"],
        "source": primary_link(item),
        "target_issue_urls": [issue["url"] for issue in linked_open_issues if issue.get("url")],
        "reason": "Merged PR references an open GitHub issue; readback is required before closing or accepting.",
        "recommendation_only": True,
        "required_gate": "AI_ADMISSION_GATE",
        "external_write": False,
    }


def action_for_hygiene(incident):
    return {
        "type": "hygiene_incident",
        "task_id": incident.get("repo_path") or incident.get("path") or "local-hygiene",
        "source": incident.get("repo_path") or incident.get("path") or "local",
        "reason": incident.get("detail") or incident.get("type") or "local hygiene warning",
        "recommendation_only": True,
        "required_gate": "AI_ADMISSION_GATE",
        "external_write": False,
    }


def snapshot_health(warnings, hygiene, candidate_actions):
    if any(item.get("severity") == "red" for item in hygiene):
        return "red"
    if warnings or hygiene or candidate_actions:
        return "yellow"
    return "green"


def build_engineering_command_snapshot(
    raw_source,
    generated_at=None,
    repo=None,
    wip_limit=4,
    ttl_minutes=30,
    ttl_hours=None,
    hygiene=None,
):
    if ttl_hours is not None:
        ttl_minutes = ttl_hours * 60
    normalized = normalize_input(raw_source)
    generated_at = generated_at or now_utc()
    repo = repo or normalized["repo"]
    export = build_export(normalized, generated_at=generated_at, repo=repo)
    open_issues = open_issue_index(normalized)
    lane_items = {name: [] for name in LANE_NAMES}
    current_items = []
    candidate_actions = []
    warnings = []

    for item, (kind, record) in zip(export["items"], record_sequence(normalized)):
        linked_open_issues = merged_open_issue_refs(kind, record, open_issues)
        command_state = command_state_for(kind, record, item, open_issues)
        lane = lane_for_command_state(command_state)
        snapshot_item = compact_snapshot_item(kind, record, item, command_state, lane, linked_open_issues)

        if lane == "current":
            current_items.append(snapshot_item)
        else:
            lane_items[lane].append(snapshot_item)

        if item["founder_decision_required"] or command_state == "decision_required":
            candidate_actions.append(action_for_decision(item))
        if linked_open_issues:
            candidate_actions.append(action_for_readback(item, linked_open_issues))

    if len(current_items) > wip_limit:
        warnings.append("wip_limit_exceeded")
        lane_items["current"].extend(current_items[:wip_limit])
        for item in current_items[wip_limit:]:
            item["lane"] = "queued"
            item["warnings"] = sorted(set(item["warnings"] + ["queued_due_to_wip_limit"]))
            lane_items["queued"].append(item)
    else:
        lane_items["current"].extend(current_items)

    hygiene = list(hygiene or [])
    for incident in hygiene:
        candidate_actions.append(action_for_hygiene(incident))

    lanes = [{"name": name, "items": lane_items[name]} for name in LANE_NAMES]
    snapshot = {
        "schema": SNAPSHOT_SCHEMA,
        "source": SOURCE_SYSTEM,
        "repo": repo,
        "generated_at": generated_at,
        "expires_at": plus_minutes_utc(generated_at, ttl_minutes),
        "snapshot_ttl_minutes": ttl_minutes,
        "source_queries": source_query_summary(normalized, repo),
        "source_coverage": source_coverage(normalized, repo),
        "snapshot_completeness": snapshot_completeness(normalized),
        "wip_limit": wip_limit,
        "health": snapshot_health(warnings, hygiene, candidate_actions),
        "lanes": lanes,
        "candidate_actions": candidate_actions,
        "hygiene": hygiene,
        "warnings": sorted(set(warnings)),
        "counts": {
            "items": export["counts"]["items"],
            "current": len(lane_items["current"]),
            "waiting_decision": len(lane_items["waiting_decision"]),
            "waiting_readback": len(lane_items["waiting_readback"]),
            "queued": len(lane_items["queued"]),
            "history": len(lane_items["history"]),
            "candidate_actions": len(candidate_actions),
            "hygiene": len(hygiene),
            "warnings": len(set(warnings)),
        },
        "work_items": export["items"],
        "external_writes": [],
    }
    snapshot_hash = canonical_hash(snapshot)
    snapshot["snapshot_hash"] = snapshot_hash
    snapshot["receipt"] = {
        "schema": "engineering-command-snapshot-receipt:v0.1",
        "snapshot_hash": snapshot_hash,
        "repo": repo,
        "generated_at": generated_at,
        "expires_at": snapshot["expires_at"],
        "snapshot_ttl_minutes": ttl_minutes,
        "wip_limit": wip_limit,
    }
    return snapshot


def primary_link(item):
    source = item["source"]
    if source["issue_url"]:
        return source["issue_url"]
    if source["pr_urls"]:
        return source["pr_urls"][0]
    if source["file_refs"]:
        return source["file_refs"][0]
    return "n/a"


def packet_line(item):
    warnings = ", ".join(item["warnings"]) if item["warnings"] else "none"
    return (
        f"- `{item['task_id']}` | `{item['status']}` | `{item['risk_path']}` | "
        f"{item['owner']['github']} | {primary_link(item)} | next: {item['next_action']} | warnings: {warnings}"
    )


def render_section(title, items):
    lines = [f"## {title}"]
    if not items:
        lines.append("- n/a")
    else:
        lines.extend(packet_line(item) for item in items)
    return "\n".join(lines)


def render_founder_packet(projection):
    items = projection["items"]
    decision_items = [item for item in items if item["founder_decision_required"]]
    blocked_items = [item for item in items if item["status"] == "blocked" or item["blocker"]["state"] != "none"]
    review_items = [
        item
        for item in items
        if item["status"] in {"review", "gate_a", "gate_b", "human_cross_audit", "founder_acceptance"}
    ]
    accepted_items = [item for item in items if item["evidence_state"] == "accepted"]
    active_items = [item for item in items if item["status"] not in {"done", "rejected", "archived"}]
    warning_items = [item for item in items if item["warnings"]]

    lines = [
        "# HL Progress Founder Packet",
        "",
        f"- Schema: `{projection['schema']}`",
        f"- Repo: `{projection['repo']}`",
        f"- Generated At: `{projection['generated_at']}`",
        f"- Items: {projection['counts']['items']}",
        f"- Warnings: {projection['counts']['warnings']}",
        "",
        render_section("Decision Required", decision_items),
        "",
        render_section("Blocked", blocked_items),
        "",
        render_section("Review Waiting", review_items),
        "",
        render_section("Accepted Evidence", accepted_items),
        "",
        render_section("Active Work", active_items),
        "",
        render_section("Warnings", warning_items),
        "",
    ]
    return "\n".join(lines)


def render_engineering_command_snapshot(snapshot):
    lines = [
        "# Engineering Command Snapshot",
        "",
        f"- Schema: `{snapshot['schema']}`",
        f"- Repo: `{snapshot['repo']}`",
        f"- Generated At: `{snapshot['generated_at']}`",
        f"- Expires At: `{snapshot['expires_at']}`",
        f"- Snapshot TTL Minutes: {snapshot.get('snapshot_ttl_minutes', 'n/a')}",
        f"- Health: `{snapshot['health']}`",
        f"- WIP Limit: {snapshot['wip_limit']}",
        f"- External Writes: {len(snapshot['external_writes'])}",
        "",
    ]
    for lane in snapshot["lanes"]:
        lines.append(f"## {lane['name']}")
        if not lane["items"]:
            lines.append("- n/a")
        else:
            for item in lane["items"]:
                warnings = ", ".join(item["warnings"]) if item["warnings"] else "none"
                lines.append(
                    f"- `{item['task_id']}` | `{item['command_state']}` | `{item['risk_path']}` | "
                    f"{item['owner']['github']} | {primary_link(item)} | next: {item['next_action']} | warnings: {warnings}"
                )
        lines.append("")

    lines.append("## Candidate Actions")
    if not snapshot["candidate_actions"]:
        lines.append("- n/a")
    else:
        for action in snapshot["candidate_actions"]:
            lines.append(
                f"- `{action['type']}` | `{action['task_id']}` | external_write: `{action['external_write']}` | "
                f"recommendation_only: `{action.get('recommendation_only', False)}` | required_gate: `{action.get('required_gate', 'n/a')}` | {action['reason']}"
            )
    lines.append("")
    lines.append("## Hygiene")
    if not snapshot["hygiene"]:
        lines.append("- n/a")
    else:
        for incident in snapshot["hygiene"]:
            source = incident.get("repo_path") or incident.get("path") or "local"
            lines.append(f"- `{incident['type']}` | `{incident['severity']}` | {source} | {incident.get('detail', 'n/a')}")
    lines.append("")
    return "\n".join(lines)


def git_status_hygiene(repo_path, now=None, stale_days=30):
    repo_path = str(repo_path)
    result = subprocess.run(
        ["git", "-C", repo_path, "status", "--porcelain=v2", "--branch"],
        check=True,
        capture_output=True,
        text=True,
    )
    dirty_count = 0
    ahead = 0
    behind = 0
    branch = "unknown"
    for line in result.stdout.splitlines():
        if line.startswith("# branch.head "):
            branch = line.split("# branch.head ", 1)[1].strip()
        elif line.startswith("# branch.ab "):
            match = re.search(r"\+(\d+)\s+-(\d+)", line)
            if match:
                ahead = int(match.group(1))
                behind = int(match.group(2))
        elif line and not line.startswith("#"):
            dirty_count += 1

    incidents = []
    if dirty_count:
        incidents.append(
            {
                "type": "dirty_worktree",
                "severity": "yellow",
                "repo_path": repo_path,
                "branch": branch,
                "detail": f"{dirty_count} dirty status entries",
            }
        )
    if ahead:
        incidents.append(
            {
                "type": "ahead_worktree",
                "severity": "yellow",
                "repo_path": repo_path,
                "branch": branch,
                "detail": f"local branch is ahead by {ahead} commit(s)",
            }
        )
    if behind:
        incidents.append(
            {
                "type": "behind_worktree",
                "severity": "yellow",
                "repo_path": repo_path,
                "branch": branch,
                "detail": f"local branch is behind by {behind} commit(s)",
            }
        )
    if now:
        try:
            last_commit = subprocess.run(
                ["git", "-C", repo_path, "log", "-1", "--format=%cI"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            if last_commit:
                age_days = (parse_utc(now) - parse_utc(last_commit)).days
                if age_days > stale_days:
                    incidents.append(
                        {
                            "type": "stale_worktree",
                            "severity": "yellow",
                            "repo_path": repo_path,
                            "branch": branch,
                            "last_commit_at": last_commit,
                            "age_days": age_days,
                            "detail": f"last commit is {age_days} day(s) old",
                        }
                    )
        except (OSError, subprocess.CalledProcessError, ValueError):
            pass
    return incidents


def progress_record_from_file(progress_file):
    if isinstance(progress_file, dict):
        return progress_file
    path = Path(progress_file)
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        "path": str(path),
        "updated_at": (
            payload.get("updated_at")
            or payload.get("updatedAt")
            or payload.get("last_updated")
            or payload.get("lastUpdated")
        ),
    }


def progress_hygiene(progress_file, now, stale_days):
    record = progress_record_from_file(progress_file)
    path = record.get("path") or str(progress_file)
    updated_at = record.get("updated_at") or record.get("last_updated")
    if not is_concrete(updated_at):
        return [
            {
                "type": "stale_progress",
                "severity": "yellow",
                "path": path,
                "detail": "PROGRESS.json has no updated_at or last_updated timestamp",
            }
        ]
    age_days = (parse_utc(now) - parse_utc(updated_at)).days
    if age_days > stale_days:
        return [
            {
                "type": "stale_progress",
                "severity": "yellow",
                "path": path,
                "updated_at": updated_at,
                "age_days": age_days,
                "detail": f"PROGRESS.json is {age_days} day(s) old",
            }
        ]
    return []


def collect_hygiene(repo_paths=None, progress_files=None, now=None, stale_days=30):
    now = now or now_utc()
    incidents = []
    for repo_path in repo_paths or []:
        try:
            incidents.extend(git_status_hygiene(repo_path, now=now, stale_days=stale_days))
        except (OSError, subprocess.CalledProcessError) as exc:
            incidents.append(
                {
                    "type": "hygiene_scan_failed",
                    "severity": "yellow",
                    "repo_path": str(repo_path),
                    "detail": str(exc),
                }
            )
    for progress_file in progress_files or []:
        try:
            incidents.extend(progress_hygiene(progress_file, now, stale_days))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            incidents.append(
                {
                    "type": "progress_scan_failed",
                    "severity": "yellow",
                    "path": progress_file.get("path") if isinstance(progress_file, dict) else str(progress_file),
                    "detail": str(exc),
                }
            )
    return incidents


def load_json_file(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_gh_json(args):
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    payload = json.loads(result.stdout)
    if not isinstance(payload, list):
        raise ValueError(f"{args[:3]} returned non-list JSON")
    return payload


def resolve_repo():
    result = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
        check=True,
        capture_output=True,
        text=True,
    )
    repo = result.stdout.strip()
    if not repo:
        raise ValueError("gh repo view returned empty nameWithOwner")
    return repo


def github_blob_url(repo, ref, path):
    return f"https://github.com/{repo}/blob/{quote(ref, safe='')}/{quote(path, safe='/')}"


def load_file_refs(repo, ref, file_refs):
    records = []
    for file_ref in file_refs:
        path = Path(file_ref)
        records.append(
            {
                "path": file_ref,
                "url": github_blob_url(repo, ref, file_ref),
                "content": path.read_text(encoding="utf-8"),
            }
        )
    return records


def load_live_source(state, limit, labels, file_refs, repo=None, ref="main"):
    repo = repo or resolve_repo()
    issue_cmd = [
        "gh",
        "issue",
        "list",
        "--state",
        state,
        "--limit",
        str(limit),
        "--json",
        ISSUE_JSON_FIELDS,
    ]
    pr_cmd = [
        "gh",
        "pr",
        "list",
        "--state",
        state,
        "--limit",
        str(limit),
        "--json",
        PR_JSON_FIELDS,
    ]
    for label in labels:
        issue_cmd.extend(["--label", label])
        pr_cmd.extend(["--label", label])
    return {
        "repo": repo,
        "issues": run_gh_json(issue_cmd),
        "pull_requests": run_gh_json(pr_cmd),
        "files": load_file_refs(repo, ref, file_refs),
    }


def write_output(payload, output_path):
    if output_path:
        Path(output_path).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Export read-only hl-progress work items from GitHub Issues, PRs, and repo files."
    )
    parser.add_argument("--input", help="Offline JSON containing repo, issues, pull_requests, and files.")
    parser.add_argument("--output", help="Optional output path. Defaults to stdout.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--repo", help="Repository nameWithOwner for live or offline input.")
    parser.add_argument("--state", default="open", choices=["open", "closed", "all"])
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--file-ref", action="append", default=[], help="Local repo file path to include as GitHub file evidence.")
    parser.add_argument("--source-ref", default="main", help="Git ref used to form GitHub blob URLs for --file-ref.")
    parser.add_argument("--generated-at", help="Override generated_at for deterministic tests.")
    parser.add_argument("--snapshot", action="store_true", help="Emit engineering-command-snapshot:v0.2 instead of raw hl-progress export.")
    parser.add_argument("--wip-limit", type=int, default=4, help="Maximum current lane items in --snapshot mode.")
    parser.add_argument("--snapshot-ttl-minutes", type=int, help="Snapshot expiry window in minutes. Defaults to 30.")
    parser.add_argument("--snapshot-ttl-hours", type=int, help="Deprecated: snapshot expiry window in hours.")
    parser.add_argument("--no-hygiene", action="store_true", help="Disable local Git / PROGRESS.json hygiene collection in --snapshot mode.")
    parser.add_argument("--hygiene-repo", action="append", default=[], help="Local Git repo path to inspect read-only for snapshot hygiene.")
    parser.add_argument("--progress-file", action="append", default=[], help="PROGRESS.json path to inspect read-only for staleness.")
    parser.add_argument("--stale-progress-days", type=int, default=30, help="Age threshold for stale PROGRESS.json hygiene warnings.")
    args = parser.parse_args(argv)

    try:
        if args.input:
            raw_source = load_json_file(args.input)
        else:
            raw_source = load_live_source(args.state, args.limit, args.label, args.file_ref, repo=args.repo, ref=args.source_ref)
        generated_at = args.generated_at or now_utc()
        if args.snapshot:
            ttl_minutes = args.snapshot_ttl_minutes
            if ttl_minutes is None and args.snapshot_ttl_hours is not None:
                ttl_minutes = args.snapshot_ttl_hours * 60
            if ttl_minutes is None:
                ttl_minutes = 30
            hygiene = []
            if not args.no_hygiene:
                hygiene = collect_hygiene(
                    repo_paths=args.hygiene_repo or [Path.cwd()],
                    progress_files=args.progress_file,
                    now=generated_at,
                    stale_days=args.stale_progress_days,
                )
            projection = build_engineering_command_snapshot(
                raw_source,
                generated_at=generated_at,
                repo=args.repo,
                wip_limit=args.wip_limit,
                ttl_minutes=ttl_minutes,
                hygiene=hygiene,
            )
        else:
            projection = build_export(raw_source, generated_at=generated_at, repo=args.repo)
        if args.format == "json":
            payload = json.dumps(projection, ensure_ascii=False, indent=2) + "\n"
        elif args.snapshot:
            payload = render_engineering_command_snapshot(projection)
        else:
            payload = render_founder_packet(projection)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"hl-progress export failed: {exc}", file=sys.stderr)
        return 1

    write_output(payload, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
