# AI Output Contract v1

Identifier: `ai-output:v1`
Purpose: make AI delivery output auditable without long SOP text.

Use this contract in PR summaries, issue comments, blocker reports, and completion reports when AI produced or reviewed delivery work. For public GitHub backfill, the HTML marker template below is required.

AI may draft, suggest, execute, and audit. AI must not replace human confirmation, signature, rejection, approval, or acceptance.

## Status Rules

- `DONE`: fresh evidence is attached.
- `DONE_WITH_CONCERNS`: fresh evidence is attached and residual risk is listed.
- `NEEDS_CONTEXT`: context is missing or stale.
- `BLOCKED`: the next action cannot proceed without an external dependency.

No Evidence, No Done. A statement without evidence cannot be `DONE`.

## Template

Public GitHub backfill template:

```text
<!-- ai-output:v1 -->
【类型】
【结论】
【依据】
【当前状态】
【下一步唯一动作】
【需要人处理】
【不确定项】
```

Allowed public backfill types:

- `status_update`
- `gap_report`
- `decision_request`
- `acceptance_report`

Structured YAML variant for PR summaries or internal handoff:

```yaml
ai-output:v1
package_id: "<MP-...>"
slice_id: "<DS-...>"
work_unit_id: "<WU-... | n/a>"
actor: "<human-or-ai-actor>"
status: "<DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED>"
risk_path: "<green | yellow | red>"
context_validity:
  sources_read:
    - "<file-or-issue-or-pr>"
  stale_or_missing_context:
    - "<none | concrete gap>"
context_usage_summary:
  context_id: ""
  context_route: ""
  files_read: []
  missing_or_stale_context: []
  full_repo_scan_detected: false
  context_not_authorization: true
changes:
  summary:
    - "<what changed>"
  non_goals:
    - "<what was intentionally not changed>"
public_update:
  class: "<status_update | gap_report | decision_request | acceptance_report | n/a>"
test_evidence:
  commands:
    - command: "<exact command>"
      result: "<pass | fail | not_run>"
      output_summary: "<short evidence summary>"
acceptance_evidence:
  demo_or_review: "<link | screenshot | reviewer note | n/a>"
  artifact_refs:
    - "<path-or-url>"
next_action: "<next concrete action or none>"
```

## Minimum Evidence

At least one of these must be present for `DONE`:

- test command and result;
- CI run link or local command output summary;
- acceptance screenshot, recording, or reviewer comment;
- artifact path with enough context for review.

## AI Guess Boundary

If the AI cannot confirm package, slice, owner, risk path, or evidence, it must use `NEEDS_CONTEXT` and name the missing field. Do not infer facts from Feishu, Bitable, memory, or chat-only history.

Do not write "已完成", "已确认", "已授权", "已阻塞", "已通过", "可关闭", "runtime ready", or "production ready" without evidence and the required human role where applicable.

Do not write filler or black-box governance phrases: "收到 / 已知 / 继续推进", "继续推进整体治理", "需要进一步确认", "当前上下文显示", "可能已经处理过", "runtime 那个", or "HPRD 已确认但无证据".

The live GitHub language gate rejects `ai-output:v1` comments that contain the canonical black-box phrases above only after the shared `sentinel-shared` gate update is merged into the reusable workflow consumed by this repository. `sentinel-shared` is the canonical source for live GitHub enforcement; this repository's local checker is a mirror for local tests and must stay aligned with it. If the work needs more context, use `gap_report` and name the missing context, evidence, authorization, or owner.
