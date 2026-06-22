#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from validate_task_assignment import load_structured_file, validate_assignment


TEAM_CONTEXT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = TEAM_CONTEXT / "RESPONSIBILITY-REGRESSION-CASES-v1.yaml"
DEFAULT_REGISTRY = TEAM_CONTEXT / "ROLE-REGISTRY-v1.yaml"
DEFAULT_OWNERS = TEAM_CONTEXT / "ROLE-OWNERS-v1.yaml"


def run_cases(cases_path, registry_path, owners_path):
    case_data = load_structured_file(cases_path)
    results = []
    failed = 0
    for case in case_data.get("cases", []):
        actual = validate_assignment(
            case["payload"],
            registry_path=registry_path,
            owners_path=owners_path,
        )
        passed = actual["decision"] == case["expected_decision"]
        if not passed:
            failed += 1
        results.append(
            {
                "id": case["id"],
                "expected_decision": case["expected_decision"],
                "actual_decision": actual["decision"],
                "passed": passed,
                "reason_codes": actual["reason_codes"],
            }
        )
    total = len(results)
    return {
        "schema": "responsibility-regression-result:v1",
        "status": "passed" if failed == 0 else "failed",
        "counts": {
            "total": total,
            "passed": total - failed,
            "failed": failed,
        },
        "results": results,
    }


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Run hl-dispatch responsibility regression cases.")
    parser.add_argument("--cases", default=str(DEFAULT_CASES), help="Regression case file.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="ROLE-REGISTRY path.")
    parser.add_argument("--owners", default=str(DEFAULT_OWNERS), help="ROLE-OWNERS path.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    result = run_cases(args.cases, args.registry, args.owners)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
