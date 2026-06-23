# AI Admission Gate v0.1

Date: 2026-06-23

Status: STAGE_B_LOCAL_DRY_RUN

## 中文摘要

`AI_ADMISSION_GATE` 是唤龙团队 AI 正式输出的本地 dry-run 准入总闸。它消费 `engineering-command-snapshot:v0.2`、职责门禁结果、Context Atlas 导航元数据和授权回执，输出 `ACCEPT | REJECT | REVIEW_REQUIRED` 与绑定 receipt。Stage B 只在 `hl-dispatch` 内落地本地脚本和测试，不启用 GitHub required check，不写 GitHub / 飞书 / 多维表格 / 云效 / team-memory。

Implementation:

- `scripts/ai-admission-gate.py`
- `scripts/test-ai-admission-gate.py`
- `scripts/export-hl-progress.py` snapshot mode

## Founder Decisions Applied

- Stage B write scope is limited to `hl-dispatch`.
- Formal AI output scope follows the uploaded v0.3 plan section 4.1.
- Current operating policy is `snapshot_ttl_minutes: 30` and `wip_limit: 4`.
- GitHub minimum hard gate is dry-run only; required check enforcement needs a separate Founder decision.
- Context Atlas may only use the existing `huanlong_platform` view; no new Context View is authorized here.
- `ai_loop_control` implementation is deferred; this document defines only an interface / evidence contract.
- Local implementation is allowed; push is not authorized.

## Formal AI Output Scope

The gate treats these as formal AI outputs:

- GitHub Issues, PRs, comments, and governance records.
- Yunxiao work items, pipeline parameters, and release inputs.
- Formal team tasks.
- Code, config, contracts, migrations, and release candidates.
- Deploy, runtime, production, and release actions.
- Payment, provider, and real data surfaces.
- Team-memory approved knowledge.
- Writes to dynamic truth surfaces.

Stage B only supports GitHub-surface dry-run decisions. Yunxiao, Feishu, Bitable, team-memory approved knowledge, dynamic truth writes, runtime, deploy, production, release, payment, provider, and real data surfaces are blocked or escalated until their adapters and authorization paths are separately approved.

## Snapshot Contract

`engineering-command-snapshot:v0.2` keeps the read-only command projection from `hl-progress` and adds the Stage B hardening fields:

```yaml
schema: engineering-command-snapshot:v0.2
generated_at: "<ISO-8601>"
expires_at: "<generated_at + 30 minutes by default>"
snapshot_ttl_minutes: 30
wip_limit: 4
source_coverage:
  github:
    repo: "huanlongAI/hl-dispatch"
    issues: 0
    pull_requests: 0
    repo_files: 0
snapshot_completeness:
  status: "complete | incomplete"
  missing: []
snapshot_hash: "<sha256>"
receipt:
  schema: engineering-command-snapshot-receipt:v0.1
  snapshot_hash: "<same hash>"
candidate_actions:
  - recommendation_only: true
    required_gate: AI_ADMISSION_GATE
    external_write: false
external_writes: []
```

The snapshot is not authorization. It is a bounded, expiring read model for gate input.

## Gate Request

```yaml
schema: ai-admission-request:v0.1
mode: dry_run
task_id: "<stable task id>"
repo: "huanlongAI/hl-dispatch"
output:
  type: "github_issue | github_pr | github_comment | governance_record | ..."
  target_surface: "github"
  source_hash: "<sha256 over the output payload>"
snapshot: "<engineering-command-snapshot:v0.2 object>"
responsibility_gate:
  decision: "ACCEPT | REJECT | REVIEW_REQUIRED"
  registry_version: "ROLE-REGISTRY-v1"
context:
  context_id: "huanlong_platform"
  context_status: "draft"
  context_version: "<date or registry version>"
  source_truth_from_context_view: false
authorization:
  founder_gate_receipt_url: "<GitHub URL when sensitive output requires it>"
  authorization_refs: []
prior_receipt: "<optional ai-admission-gate-receipt:v0.1>"
```

## Gate Result

```yaml
schema: ai-admission-gate-result:v0.1
gate: AI_ADMISSION_GATE
mode: dry_run
decision: "ACCEPT | REJECT | REVIEW_REQUIRED"
reason_codes: []
receipt:
  schema: ai-admission-gate-receipt:v0.1
  receipt_id: "aiag-..."
  bound_to:
    task_id: "<task id>"
    repo: "<repo>"
    output_type: "<formal output type>"
    output_source_hash: "<payload hash>"
    target_surface: "<surface>"
    snapshot_hash: "<snapshot hash>"
    context_id: "<context id>"
    context_version: "<context version>"
    responsibility_registry_version: "<registry version>"
github_write:
  enabled: false
external_writes: []
```

The receipt is bound to task, repo, output type, output payload hash, target surface, snapshot hash, context version, responsibility registry version, and authorization refs hash. Reusing a receipt for a changed output is rejected with `receipt_binding_mismatch`.

## Decision Rules

`REJECT` is returned when:

- request schema is not `ai-admission-request:v0.1`;
- snapshot schema, TTL, WIP policy, receipt, hash, expiry, completeness, or `external_writes` violates policy;
- responsibility gate returned `REJECT`;
- sensitive output lacks a concrete Founder / Gate receipt URL;
- a supplied prior receipt is replayed against a different bound payload.

`REVIEW_REQUIRED` is returned when:

- the formal output type is unknown;
- the target surface is unsupported in Stage B;
- the responsibility gate returned `REVIEW_REQUIRED`;
- Context Atlas is being used as source truth rather than navigation.

`ACCEPT` is returned only when all required inputs are fresh, bound, policy-aligned, and GitHub dry-run supported.

## Context Atlas Slice Contract

No Context Atlas file is written in this Stage B implementation. If separately authorized later, the only allowed projection is a slice under the existing `huanlong_platform` Context View:

```yaml
slice_id: engineering_command_context
context_id: huanlong_platform
source_repo: huanlongAI/hl-dispatch
source_doc: docs/team-ai-context/AI_ADMISSION_GATE_v0.1.md
source_truth: false
navigation_only: true
allowed_gate: AI_ADMISSION_GATE
forbidden:
  - new_context_view
  - source_truth_from_context_view
  - runtime_expansion
  - write_capable_tooling
```

## `ai_loop_control` Interface Contract

No `ai_loop_control` implementation is present or authorized here. A future implementation may consume the gate result only through this evidence envelope:

```yaml
schema: ai-loop-control-evidence:v0.1
task_id: "<task id>"
state: "DRAFT | CONTEXT_RESOLVING | ADMISSION_REVIEW | EXECUTING | READBACK | COMPLETED | BLOCKED"
admission_gate:
  decision: "ACCEPT | REJECT | REVIEW_REQUIRED"
  receipt_id: "<aiag receipt id or empty>"
  reason_codes: []
snapshot_hash: "<engineering command snapshot hash>"
external_writes: []
```

The interface does not authorize a loop runner, queue, executor, runtime change, production action, or external write.

## Commands

Generate a fresh local snapshot:

```bash
python3 scripts/export-hl-progress.py \
  --input scripts/fixtures/engineering-command-snapshot-input.json \
  --generated-at 2026-06-23T00:00:00Z \
  --format json \
  --snapshot \
  --snapshot-ttl-minutes 30 \
  --no-hygiene
```

Evaluate a gate request:

```bash
python3 scripts/ai-admission-gate.py --input <ai-admission-request.json>
```

Verification:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-ai-admission-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-exporter.py
```
