#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
LATIN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
URL_RE = re.compile(r"https?://\S+")
FENCED_CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
MIN_BODY_CJK_CHARS = 6
MIN_BODY_CJK_RATIO = 0.2
LATIN_HEAVY_WORDS = 12
OWNER_CONFIRMATION_ROOTS = (
    "owner_confirmation_response_v1:",
    "frontend_owner_confirmation:",
)
ISSUE_URL_RE = re.compile(r"/issues/(\d+)(?:#|$)")


def has_chinese(text):
    return bool(CJK_RE.search(text or ""))


def chinese_signal_too_weak(text):
    normalized = URL_RE.sub(" ", text or "")
    cjk_count = len(CJK_RE.findall(normalized))
    if cjk_count == 0:
        return False

    prose_for_latin_count = FENCED_CODE_BLOCK_RE.sub(" ", normalized)
    latin_word_count = len(LATIN_WORD_RE.findall(prose_for_latin_count))
    if latin_word_count < LATIN_HEAVY_WORDS:
        return False

    cjk_ratio = cjk_count / (cjk_count + latin_word_count)
    return cjk_count < MIN_BODY_CJK_CHARS or cjk_ratio < MIN_BODY_CJK_RATIO


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
    elif body.strip() and chinese_signal_too_weak(body):
        errors.append("body_chinese_ratio_too_low")

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
    elif not structured_yaml_allowed and chinese_signal_too_weak(body):
        errors.append("comment_chinese_ratio_too_low")

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
    result["target_issue_number"] = target_issue_number(event, result["target_url"])
    return result


def target_issue_number(event, target_url):
    issue = event.get("issue") or {}
    number = issue.get("number")
    if number is not None:
        return str(number)

    match = ISSUE_URL_RE.search(target_url or "")
    if match:
        return match.group(1)

    return ""


def write_github_output(output_path, result):
    values = {
        "status": result["status"],
        "target_issue_number": result["target_issue_number"],
        "target_url": result["target_url"],
        "errors": ",".join(result["errors"]),
    }
    with Path(output_path).open("a", encoding="utf-8") as output:
        for key, value in values.items():
            output.write(f"{key}={value}\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check GitHub issue/comment language gate")
    parser.add_argument("--event-path", required=True)
    parser.add_argument("--github-output")
    args = parser.parse_args(argv)

    event = json.loads(Path(args.event_path).read_text(encoding="utf-8"))
    result = validate_event(event)
    if args.github_output:
        write_github_output(args.github_output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
