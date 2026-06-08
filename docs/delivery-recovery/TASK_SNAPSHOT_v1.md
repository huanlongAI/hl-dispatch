# Task Snapshot v1

Identifier: `task-snapshot:v1`
Purpose: capture the current card for a Mission Package, Delivery Slice, or Work Unit.

Use a Task Snapshot when context changes, a handoff happens, a risk path changes, or the next action changes. Task Snapshot is the current position, not a human signature.

No Structured Update, No Public Status Comment: a public status comment must be backed by a structured update class: `status_update`, `gap_report`, `decision_request`, or `acceptance_report`.

## Template

```yaml
<!-- task-snapshot:v1 -->
task-snapshot:v1
package_id: "<MP-...>"
slice_id: "<DS-... | n/a>"
risk_id: "<RISK-... | n/a>"
work_unit_id: "<WU-... | n/a>"
current_card: "<short title>"
maturity: "<M0 | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9>"
type: "<mission_package | delivery_slice | risk_retirement_slice | work_unit>"
state: "<open | in_progress | evidence_pending | blocked | ready_for_review | closed>"
dri: "<GitHub handle or role>"
risk_path: "<green | yellow | red>"
current_status: "<current position>"
confirmed_facts:
  - fact: "<fact>"
    evidence: "<issue | PR | file | command output | artifact>"
next_action: "<one concrete next action>"
blocked_by:
  - "<none | blocker>"
unblock_condition: "<condition or n/a>"
authorization: "<boundary or n/a>"
evidence:
  existing:
    - "<issue | PR | file | command output | artifact>"
  required_next:
    - "<test | demo | acceptance | reviewer confirmation>"
evidence_links:
  - "<issue | PR | artifact>"
close_condition: "<condition>"
context_validity:
  last_context_read:
    - "<file-or-issue-or-pr>"
  known_gaps:
    - "<none | concrete gap>"
non_goals:
  - "<what this card must not do>"
public_update_class: "<status_update | gap_report | decision_request | acceptance_report | n/a>"
last_material_change: "<YYYY-MM-DD>"
```

## Required Fields

- `package_id`
- `slice_id` or `risk_id`
- `maturity`
- `type`
- `state`
- `dri`
- `risk_path`
- `current_status`
- `confirmed_facts` with evidence
- `next_action`
- `blocked_by`
- `unblock_condition`
- `authorization`
- `evidence_links`
- `close_condition`
- `last_material_change`

## Rules

- GitHub Issue, PR, and repo files remain SSOT.
- Feishu and Bitable may reference a snapshot, but do not become the fact source.
- A stale snapshot must not be used as completion evidence.
- If the next action is unclear, state `NEEDS_CONTEXT` in the paired `ai-output:v1`.
