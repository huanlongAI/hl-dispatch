# AI Admission Gate v0.1

Date: 2026-06-23

Status: STAGE_B_LOCAL_DRY_RUN_FORMAL_PUBLISHER_PRECHECK

## 中文摘要

`AI_ADMISSION_GATE` 是唤龙团队 AI 正式输出的本地 dry-run 准入总闸。它消费 `engineering-command-snapshot:v0.2`、职责门禁结果、Context Atlas 导航元数据和授权回执，输出 `ACCEPT | REJECT | REVIEW_REQUIRED` 与绑定 receipt。Stage B-B 已把它接入 `hl-dispatch` 正式发布器 dry-run 预检；仍不启用 GitHub required check，不写 GitHub / 飞书 / 多维表格 / 云效 / team-memory。

本文件的目标是把“AI 可以生成什么”和“AI 什么时候可以发布”拆开处理：脚本只判断本地候选输出是否满足准入条件，不代表生产授权、发布授权或外部写入授权。任何真实 GitHub 写入、云效参数、飞书通知、多维表格更新、team-memory 认可知识写入、运行时动作、生产动作、支付或供应商相关动作，都必须另有 Founder / Gate 的 GitHub 真源回执。

## 术语说明

- 准入总闸：统一判断正式 AI 输出能否进入下一步的本地门禁。
- 正式 AI 输出：会进入 GitHub、云效、团队任务、代码、配置、契约、发布候选、运行时、生产、支付、供应商、真实数据或动态真源的 AI 产物。
- 回执：门禁对某一次候选输出生成的可追溯记录，绑定任务、仓库、输出类型、输出哈希、快照哈希、语境版本、职责版本和授权引用。
- 防重放：禁止把旧回执拿去授权新的任务、新的输出内容、新的快照或新的职责版本。
- 导航语境：Context Atlas 只帮助找到应读材料，不是事实源，也不能替代 GitHub 真源和 Founder / Gate 回执。
- 本地 dry-run：只在本仓脚本中计算结果，不创建 Issue、不发评论、不写飞书、不写云效、不写多维表格、不改分支保护。

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

## Formal Publisher Dry-Run Hook

Stage B-B adds an optional local hook in `docs/team-context/scripts/preflight_formal_assignment_publisher.py`.

When the caller passes `--require-ai-admission-gate`, the formal publisher preflight builds an `ai-admission-request:v0.1` from the accepted GitHub Issue payload and the supplied `engineering-command-snapshot:v0.2`, then evaluates `scripts/ai-admission-gate.py` locally.

The hook is fail-closed:

- missing snapshot returns `ai_admission_snapshot_absent`;
- any gate result other than `ACCEPT` returns `ai_admission_gate_not_accept`;
- `ACCEPT` carries the local admission receipt into the preflight result;
- `github_write.enabled` remains `false`;
- `external_writes` remains `[]`.

This is only a local precheck for the formal publisher. It is not a GitHub required check, branch protection rule, production gate, external write authorization, or release approval.

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

Run the formal publisher dry-run with the admission gate:

```bash
python3 docs/team-context/scripts/preflight_formal_assignment_publisher.py \
  --input <assignment-publish-plan.json> \
  --publish \
  --require-ai-admission-gate \
  --admission-snapshot <engineering-command-snapshot.json> \
  --repo huanlongAI/hl-dispatch
```

Verification:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-ai-admission-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-team-assignment-publisher.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-exporter.py
```
