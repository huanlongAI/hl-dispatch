#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


EXPORT_SCHEMA = "hl-progress-export:v0.1"
ITEM_SCHEMA = "hl-progress-work-item:v0.1"
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


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
    args = parser.parse_args(argv)

    try:
        if args.input:
            raw_source = load_json_file(args.input)
        else:
            raw_source = load_live_source(args.state, args.limit, args.label, args.file_ref, repo=args.repo, ref=args.source_ref)
        projection = build_export(raw_source, generated_at=args.generated_at, repo=args.repo)
        if args.format == "json":
            payload = json.dumps(projection, ensure_ascii=False, indent=2) + "\n"
        else:
            payload = render_founder_packet(projection)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"hl-progress export failed: {exc}", file=sys.stderr)
        return 1

    write_output(payload, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
