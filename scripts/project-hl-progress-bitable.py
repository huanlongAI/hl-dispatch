#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "hl-progress-bitable-projection:v0.1"
TARGET = "feishu_bitable"
MODE = "dry_run"
PROJECTION_NOTICE = (
    "Projection only. GitHub remains SSOT. Bitable edits are notes until captured in GitHub. "
    "External Bitable write requires a separate projection gate."
)


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def bitable_field_mapping():
    return [
        {
            "bitable_field": "Task ID",
            "source_field": "task_id",
            "field_type": "text",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Repo",
            "source_field": "repo",
            "field_type": "text",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Owner",
            "source_field": "owner",
            "field_type": "text",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Status",
            "source_field": "status",
            "field_type": "single_select",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Risk Path",
            "source_field": "risk_path",
            "field_type": "single_select",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Evidence State",
            "source_field": "evidence_state",
            "field_type": "single_select",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Next Gate",
            "source_field": "next_gate",
            "field_type": "text",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Next Action",
            "source_field": "next_action",
            "field_type": "text",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Blocker",
            "source_field": "blocker",
            "field_type": "text",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Founder Decision Required",
            "source_field": "founder_decision_required",
            "field_type": "checkbox",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "GitHub Link",
            "source_field": "github_link",
            "field_type": "url",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Last Synced",
            "source_field": "last_synced",
            "field_type": "datetime",
            "write_semantics": "projection_only",
        },
        {
            "bitable_field": "Warnings",
            "source_field": "warnings",
            "field_type": "text",
            "write_semantics": "projection_only",
        },
    ]


def load_export(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("input JSON must be an hl-progress export object")
    if payload.get("schema") != "hl-progress-export:v0.1":
        raise ValueError("input JSON schema must be hl-progress-export:v0.1")
    if not isinstance(payload.get("items"), list):
        raise ValueError("input JSON must include an items array")
    return payload


def primary_link(item):
    source = item.get("source") or {}
    issue_url = source.get("issue_url") or ""
    if issue_url:
        return issue_url
    pr_urls = source.get("pr_urls") or []
    if pr_urls:
        return pr_urls[0]
    file_refs = source.get("file_refs") or []
    if file_refs:
        return file_refs[0]
    return "unknown"


def blocker_text(item):
    blocker = item.get("blocker") or {}
    state = blocker.get("state") or "none"
    summary = blocker.get("summary") or "n/a"
    if state == "none":
        return "n/a"
    return f"{state}: {summary}"


def row_for_item(item, generated_at):
    warnings = list(item.get("warnings") or [])
    link = primary_link(item)
    if link == "unknown":
        warnings.append("missing_github_link_for_projection")
    source = item.get("source") or {}
    owner = item.get("owner") or {}
    return {
        "Task ID": item.get("task_id") or "unknown",
        "Repo": source.get("repo") or "unknown",
        "Owner": owner.get("github") or "unknown",
        "Status": item.get("status") or "unknown",
        "Risk Path": item.get("risk_path") or "unknown",
        "Evidence State": item.get("evidence_state") or "unknown",
        "Next Gate": item.get("next_gate") or "n/a",
        "Next Action": item.get("next_action") or "n/a",
        "Blocker": blocker_text(item),
        "Founder Decision Required": bool(item.get("founder_decision_required")),
        "GitHub Link": link,
        "Last Synced": generated_at,
        "Warnings": ", ".join(warnings),
    }, warnings


def ledger_for_row(row, warnings):
    return {
        "task_id": row["Task ID"],
        "github_link": row["GitHub Link"],
        "operation": "dry_run_upsert_preview",
        "external_write": False,
        "result": "skipped_external_write",
        "warnings": warnings,
    }


def build_projection(export, generated_at=None):
    generated_at = generated_at or now_utc()
    rows = []
    ledger = []
    warning_count = 0
    for item in export["items"]:
        row, warnings = row_for_item(item, generated_at)
        rows.append(row)
        ledger.append(ledger_for_row(row, warnings))
        warning_count += len(warnings)
    return {
        "schema": SCHEMA,
        "mode": MODE,
        "target": TARGET,
        "source_schema": export.get("schema"),
        "source_repo": export.get("repo") or "unknown",
        "generated_at": generated_at,
        "projection_notice": PROJECTION_NOTICE,
        "field_mapping": bitable_field_mapping(),
        "counts": {
            "input_items": len(export["items"]),
            "rows": len(rows),
            "warnings": warning_count,
        },
        "rows": rows,
        "ledger": ledger,
    }


def render_mapping(mapping):
    lines = ["## Field Mapping", "| Bitable Field | Source Field | Type | Semantics |", "|---|---|---|---|"]
    for entry in mapping:
        lines.append(
            f"| {entry['bitable_field']} | `{entry['source_field']}` | {entry['field_type']} | {entry['write_semantics']} |"
        )
    return "\n".join(lines)


def render_rows(rows):
    lines = ["## Row Preview", "| Task ID | Status | Risk | Owner | GitHub Link | Warnings |", "|---|---|---|---|---|---|"]
    if not rows:
        lines.append("| n/a | n/a | n/a | n/a | n/a | n/a |")
    for row in rows:
        warnings = row["Warnings"] or "none"
        lines.append(
            f"| `{row['Task ID']}` | `{row['Status']}` | `{row['Risk Path']}` | {row['Owner']} | {row['GitHub Link']} | {warnings} |"
        )
    return "\n".join(lines)


def render_ledger(ledger):
    lines = ["## Dry-Run Ledger", "| Task ID | Operation | External Write | Result | Warnings |", "|---|---|---|---|---|"]
    if not ledger:
        lines.append("| n/a | n/a | false | n/a | n/a |")
    for entry in ledger:
        warnings = ", ".join(entry["warnings"]) if entry["warnings"] else "none"
        lines.append(
            f"| `{entry['task_id']}` | `{entry['operation']}` | {str(entry['external_write']).lower()} | {entry['result']} | {warnings} |"
        )
    return "\n".join(lines)


def render_markdown(projection):
    return "\n".join(
        [
            "# HL Progress Bitable Dry-Run Projection",
            "",
            f"- Schema: `{projection['schema']}`",
            f"- Mode: `{projection['mode']}`",
            f"- Target: `{projection['target']}`",
            f"- Source Repo: `{projection['source_repo']}`",
            f"- Generated At: `{projection['generated_at']}`",
            f"- Rows: {projection['counts']['rows']}",
            f"- Warnings: {projection['counts']['warnings']}",
            f"- Projection only: {projection['projection_notice']}",
            "",
            render_mapping(projection["field_mapping"]),
            "",
            render_rows(projection["rows"]),
            "",
            render_ledger(projection["ledger"]),
            "",
        ]
    )


def write_output(payload, output_path):
    if output_path:
        Path(output_path).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build a dry-run Feishu Bitable projection ledger from hl-progress export JSON."
    )
    parser.add_argument("--input", required=True, help="hl-progress-export:v0.1 JSON path.")
    parser.add_argument("--output", help="Optional output path. Defaults to stdout.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--generated-at", help="Override generated_at for deterministic tests.")
    args = parser.parse_args(argv)

    try:
        export = load_export(args.input)
        projection = build_projection(export, generated_at=args.generated_at)
        if args.format == "json":
            payload = json.dumps(projection, ensure_ascii=False, indent=2) + "\n"
        else:
            payload = render_markdown(projection)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"hl-progress bitable dry-run projection failed: {exc}", file=sys.stderr)
        return 1

    write_output(payload, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
