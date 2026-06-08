#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "action-projection:v0.1"
SOURCE = "github"
ISSUE_JSON_FIELDS = "number,title,url,state,labels,assignees,updatedAt,body"
HEADING_RE = re.compile(r"^#{2,6}\s+(.+?)\s*$")

EMPTY_VALUES = {
    "",
    "-",
    "n/a",
    "na",
    "none",
    "null",
    "unknown",
    "todo",
    "tbd",
    "无",
    "待补",
}


def normalize_label(label):
    value = (label or "").strip().strip(":")
    value = value.replace("`", "")
    value = re.sub(r"\s+", " ", value)
    return value.lower()


def normalize_value(value):
    return (value or "").strip().strip()


def is_concrete(value):
    normalized = normalize_value(value).lower().strip(":：。.")
    return normalized not in EMPTY_VALUES


def issue_labels(issue):
    labels = []
    for label in issue.get("labels") or []:
        if isinstance(label, dict):
            name = label.get("name")
        else:
            name = str(label)
        if name:
            labels.append(name)
    return labels


def issue_assignees(issue):
    assignees = []
    for assignee in issue.get("assignees") or []:
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
        value = "\n".join(current_lines).strip()
        sections[current_label] = value

    for line in (body or "").splitlines():
        match = HEADING_RE.match(line)
        if match:
            flush()
            current_label = normalize_label(match.group(1))
            current_lines = []
            continue
        if current_label:
            current_lines.append(line)

    flush()
    return sections


def section_value(sections, *aliases):
    for alias in aliases:
        normalized = normalize_label(alias)
        if normalized in sections:
            return normalize_value(sections[normalized])
    return ""


def projection_class(issue, sections, next_action):
    labels = {label.lower() for label in issue_labels(issue)}
    title = (issue.get("title") or "").lower()
    body = (issue.get("body") or "").lower()
    combined = " ".join([title, body, " ".join(labels)])

    if (
        "action:acceptance_ready" in labels
        or "acceptance_ready" in combined
        or "acceptance ready" in combined
    ):
        return "acceptance"
    if (
        "action:decision_required" in labels
        or "decision-request" in labels
        or "decision_request" in combined
        or "[decision]" in title
    ):
        return "decision"
    if (
        "action:blocker" in labels
        or "blocked" in labels
        or "blocker" in labels
        or re.search(r"\[[^\]]*blocker[^\]]*\]", title)
        or is_concrete(section_value(sections, "blocked_by", "current_blocker"))
    ):
        return "blocker"
    if is_concrete(next_action):
        return "action"
    return ""


def generated_next_action(projection_kind):
    return f"Review GitHub issue for {projection_kind} action."


def slice_and_risk_ids(sections):
    slice_id = section_value(sections, "slice_id")
    risk_id = section_value(sections, "risk_id")
    slice_or_risk = section_value(sections, "slice_id 或 risk_id", "slice_id_or_risk_id")

    if not is_concrete(slice_id) and is_concrete(slice_or_risk):
        if slice_or_risk.upper().startswith(("RISK-", "RRS-")):
            risk_id = slice_or_risk
        else:
            slice_id = slice_or_risk

    return (
        slice_id if is_concrete(slice_id) else "unknown",
        risk_id if is_concrete(risk_id) else "n/a",
    )


def build_item(issue):
    sections = parse_sections(issue.get("body") or "")
    labels = issue_labels(issue)
    assignees = issue_assignees(issue)
    next_action = section_value(sections, "next_action")
    kind = projection_class(issue, sections, next_action)
    warnings = []

    if not kind:
        return None

    if not is_concrete(next_action):
        next_action = generated_next_action(kind)
        warnings.append("generated_next_action_from_projection_signal")

    package_id = section_value(sections, "package_id")
    if not is_concrete(package_id):
        package_id = "unknown"
        warnings.append("missing_package_id")

    slice_id, risk_id = slice_and_risk_ids(sections)
    if slice_id == "unknown" and risk_id == "n/a":
        warnings.append("missing_slice_or_risk_id")

    work_unit_id = section_value(sections, "work_unit_id")
    if not is_concrete(work_unit_id):
        work_unit_id = "n/a"

    dri = section_value(sections, "DRI", "Package Owner", "package_owner")
    if not is_concrete(dri):
        dri = f"@{assignees[0]}" if assignees else "unknown"
        if dri == "unknown":
            warnings.append("missing_dri")

    risk_path = section_value(sections, "risk_path")
    if risk_path.lower() not in {"green", "yellow", "red"}:
        risk_path = "unknown"
        warnings.append("missing_risk_path")

    expected_evidence = section_value(
        sections,
        "expected_evidence / evidence_exit",
        "expected_evidence",
        "evidence",
    )

    if not is_concrete(expected_evidence):
        expected_evidence = "unknown"
        warnings.append("missing_expected_evidence")

    return {
        "issue_number": issue.get("number"),
        "issue_title": issue.get("title") or "",
        "issue_url": issue.get("url") or issue.get("html_url") or "",
        "projection_class": kind,
        "package_id": package_id,
        "slice_id": slice_id,
        "risk_id": risk_id,
        "work_unit_id": work_unit_id,
        "dri": dri,
        "risk_path": risk_path,
        "next_action": next_action,
        "expected_evidence": expected_evidence,
        "state": issue.get("state") or "",
        "labels": labels,
        "assignees": assignees,
        "updated_at": issue.get("updatedAt") or issue.get("updated_at") or "",
        "fact_source": SOURCE,
        "warnings": warnings,
    }


def build_projection(issues, generated_at=None):
    items = []
    omitted_no_action = 0

    for issue in issues:
        item = build_item(issue)
        if item:
            items.append(item)
        else:
            omitted_no_action += 1

    return {
        "schema": SCHEMA,
        "source": SOURCE,
        "generated_at": generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "counts": {
            "total_input": len(issues),
            "exported": len(items),
            "omitted_no_action": omitted_no_action,
        },
        "items": items,
    }


def load_issues_from_file(path):
    issues = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(issues, list):
        raise ValueError("input JSON must be a list of GitHub issue objects")
    return issues


def load_issues_from_github(state, limit, labels):
    cmd = [
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
    for label in labels:
        cmd.extend(["--label", label])

    result = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
    )
    issues = json.loads(result.stdout)
    if not isinstance(issues, list):
        raise ValueError("gh issue list returned non-list JSON")
    return issues


def write_projection(projection, output_path):
    payload = json.dumps(projection, ensure_ascii=False, indent=2) + "\n"
    if output_path:
        Path(output_path).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Export a read-only GitHub action projection for Delivery Recovery Mode."
    )
    parser.add_argument("--input", help="Offline JSON from gh issue list.")
    parser.add_argument("--output", help="Optional output JSON path. Defaults to stdout.")
    parser.add_argument("--state", default="open", choices=["open", "closed", "all"])
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--generated-at", help="Override generated_at for deterministic tests.")
    args = parser.parse_args(argv)

    try:
        if args.input:
            issues = load_issues_from_file(args.input)
        else:
            issues = load_issues_from_github(args.state, args.limit, args.label)
        projection = build_projection(issues, generated_at=args.generated_at)
        write_projection(projection, args.output)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"action projection export failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
