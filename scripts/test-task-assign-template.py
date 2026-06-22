#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / ".github/ISSUE_TEMPLATE/task-assign.yml"
REGISTRY = ROOT / "docs/team-context/ROLE-REGISTRY-v1.yaml"
OWNERS = ROOT / "docs/team-context/ROLE-OWNERS-v1.yaml"
CURRENT_REGISTRY_VERSION = "ROLE-REGISTRY-v1"


def read_template():
    return TEMPLATE.read_text(encoding="utf-8")


def body_item_block(template_text, field_id):
    for block in re.findall(r"(?ms)^  - type: .*?(?=^  - type: |\Z)", template_text):
        if re.search(rf"(?m)^    id: {re.escape(field_id)}$", block):
            return block
    raise AssertionError(f"missing issue form field id: {field_id}")


def dropdown_options(field_block):
    return [
        line.split("- ", 1)[1].strip()
        for line in field_block.splitlines()
        if re.match(r"^        - ", line)
    ]


def assert_required(test_case, field_block):
    test_case.assertRegex(field_block, r"(?m)^    validations:$")
    test_case.assertRegex(field_block, r"(?m)^      required: true$")


class TaskAssignTemplateTests(unittest.TestCase):
    def test_template_collects_required_validator_payload_fields(self):
        template = read_template()
        expected_fields = {
            "task-type": "task_type",
            "registry-version": "registry_version",
            "assignee-role": "assignee_role",
        }

        for field_id, payload_key in expected_fields.items():
            with self.subTest(field_id=field_id):
                block = body_item_block(template, field_id)
                assert_required(self, block)
                self.assertIn(payload_key, block)

    def test_task_type_options_cover_registry_contract_and_unknown_review_fallback(self):
        template = read_template()
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        block = body_item_block(template, "task-type")

        for task_type in registry["task_types"].keys():
            with self.subTest(task_type=task_type):
                self.assertRegex(block, rf"(?m)^        - {re.escape(task_type)}\b")

        self.assertRegex(block, r"(?m)^        - unknown_task_type\b")
        self.assertIn("REVIEW_REQUIRED", block)

    def test_registry_version_is_pinned_to_current_responsibility_source(self):
        template = read_template()
        block = body_item_block(template, "registry-version")
        assert_required(self, block)

        options = dropdown_options(block)
        self.assertEqual(options, [CURRENT_REGISTRY_VERSION])

    def test_assignee_role_options_use_owner_role_ids(self):
        template = read_template()
        owners = json.loads(OWNERS.read_text(encoding="utf-8"))
        block = body_item_block(template, "assignee-role")
        assert_required(self, block)

        for role_id in owners["roles"].keys():
            with self.subTest(role_id=role_id):
                self.assertRegex(block, rf"(?m)^        - {re.escape(role_id)}\b")

    def test_template_states_collection_only_boundary(self):
        template = read_template()

        self.assertIn("只采集结构化字段", template)
        self.assertIn("不自动写入 GitHub", template)
        self.assertIn("不写入飞书", template)
        self.assertIn("不授权真实支付流量", template)
        self.assertIn("不接触商户私钥", template)
        self.assertIn("REVIEW_REQUIRED", template)


if __name__ == "__main__":
    unittest.main()
