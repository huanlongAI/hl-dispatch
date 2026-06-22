#!/usr/bin/env python3
import argparse
import importlib.util
import json
import sys
from pathlib import Path


CHECK_SCRIPT = Path(__file__).resolve().with_name("check-github-language-gate.py")


def load_language_gate():
    spec = importlib.util.spec_from_file_location("github_language_gate", CHECK_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_body(args):
    if args.body_file:
        return Path(args.body_file).read_text(encoding="utf-8")
    return args.body or ""


def target_url(args):
    if args.target_url:
        return args.target_url
    if args.kind == "issue_comment":
        return f"https://github.com/huanlongAI/hl-dispatch/issues/{args.issue_number}#local-preflight"
    return "https://github.com/huanlongAI/hl-dispatch/issues/local-preflight"


def build_event(args):
    body = read_body(args)
    url = target_url(args)

    if args.kind == "issue_comment":
        event = {
            "action": "created",
            "issue": {
                "number": args.issue_number,
                "html_url": f"https://github.com/huanlongAI/hl-dispatch/issues/{args.issue_number}",
            },
            "comment": {
                "body": body,
                "html_url": url,
            },
        }
    else:
        event = {
            "action": "opened",
            "issue": {
                "title": args.title or "",
                "body": body,
                "html_url": url,
            },
        }
    return event


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Local preflight for GitHub issue/comment Chinese language gate."
    )
    parser.add_argument("--kind", required=True, choices=["issue", "issue_comment"])
    parser.add_argument("--issue-number", type=int)
    parser.add_argument("--title")
    parser.add_argument("--body")
    parser.add_argument("--body-file")
    parser.add_argument("--target-url")
    args = parser.parse_args(argv)

    if args.kind == "issue_comment" and args.issue_number is None:
        parser.error("--issue-number is required for issue_comment")
    if args.kind == "issue" and not args.title:
        parser.error("--title is required for issue")
    if bool(args.body) == bool(args.body_file):
        parser.error("provide exactly one of --body or --body-file")
    return args


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    language_gate = load_language_gate()
    result = language_gate.validate_event(build_event(args))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
