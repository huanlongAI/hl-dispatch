#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
OWNER_CONFIRMATION_ROOTS = (
    "owner_confirmation_response_v1:",
    "frontend_owner_confirmation:",
)


def has_chinese(text):
    return bool(CJK_RE.search(text or ""))


def is_structured_owner_yaml(text):
    stripped = (text or "").lstrip()
    return any(stripped.startswith(root) for root in OWNER_CONFIRMATION_ROOTS)


def validate_issue(issue):
    errors = []
    title = issue.get("title") or ""
    body = issue.get("body") or ""

    if not has_chinese(title):
        errors.append("title_missing_chinese")
    if body.strip() and not has_chinese(body):
        errors.append("body_missing_chinese")

    return {
        "kind": "issue",
        "target_url": issue.get("html_url") or "",
        "structured_yaml_allowed": False,
        "errors": errors,
    }


def validate_comment(comment):
    body = comment.get("body") or ""
    structured_yaml_allowed = is_structured_owner_yaml(body)
    errors = []

    if not structured_yaml_allowed and not has_chinese(body):
        errors.append("comment_missing_chinese")

    return {
        "kind": "issue_comment",
        "target_url": comment.get("html_url") or "",
        "structured_yaml_allowed": structured_yaml_allowed,
        "errors": errors,
    }


def validate_event(event):
    if "comment" in event:
        result = validate_comment(event.get("comment") or {})
    elif "issue" in event:
        result = validate_issue(event.get("issue") or {})
    else:
        result = {
            "kind": "unsupported",
            "target_url": "",
            "structured_yaml_allowed": False,
            "errors": ["unsupported_event_payload"],
        }

    result["status"] = "failed" if result["errors"] else "passed"
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check GitHub issue/comment language gate")
    parser.add_argument("--event-path", required=True)
    args = parser.parse_args(argv)

    event = json.loads(Path(args.event_path).read_text(encoding="utf-8"))
    result = validate_event(event)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
