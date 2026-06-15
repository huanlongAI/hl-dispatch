# Biz Booking Fulfillment Agent End Patch v0.1

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-15

## 中文摘要

本文是 `biz.booking.fulfillment` 的 BF-02 Agent End docs-only patch。它把
Agent 可发现工具、工具裁剪、上下文预算、分页、证据摘要、schema 保真、
Can before Action、Action rechecks Can 和 Agent 权限边界写成可审查任务包，
用于关闭 PM dual-end review 中的 Agent End 缺口。

本文不授权 runtime、contract、schema、registry、manifest、config、OpenAPI、
events、facts、reasoncodes、生产、发布、MVP、active contract、live booking
operation、真实客户数据或正式业务对象变更。

## 术语说明

- Agent End：Agent 调用工具、读取上下文、汇总证据、触发 Can / Action 的机器端边界。
- Tool pruning：工具裁剪，只暴露当前状态和权限允许的最小工具集。
- Context budget：上下文预算，限定 Agent 可携带和摘要的输入、历史、证据范围。
- Gateway / HK Kernel / Can -> Action -> Audit：网关、可做判定、动作执行、审计链路。
- BF-02-AGENT-END：goal-mode task ledger 中 `biz.booking.fulfillment` 的 Agent End 任务。
- GATED：高风险执行类别，必须有独立证据、失败路径和 Gate / Founder 可审查边界。

## Scope

```yaml
capability_id: biz.booking.fulfillment
task_id: BF-02-AGENT-END
dri: Gate-H / 许久明
pm_owner: PM-A / 邹骢
gate_owner: Gate-H / 许久明
maturity: M6_M7
execution_state: THIN_SLICE
risk_class: GATED
ledger_ref: docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml#biz.booking.fulfillment
goal_mode_task_ref: docs/delivery-recovery/HL-CAPABILITY-OPERATING-RULES-GOAL-MODE-TASK-LEDGER-v0.1-2026-06-14.yaml#BF-02-AGENT-END
```

This file is a dispatch-layer Agent End patch package. It references
`hl-contracts` and `hl-platform` evidence, but it does not copy or replace their
SSOT content.

## Boundary

Boundary: this patch may define docs-only Agent End expectations, tool
discovery rules, tool pruning profile, context budget, pagination,
evidence-summary expectations, schema preservation rules, acceptance criteria,
failure paths, and next pull triggers. It is not a runtime design, contract
registry, schema, OpenAPI, events, facts, reasoncodes, manifest, app resource,
config, release approval, production approval, MVP pass, active contract, or
live booking operation approval.

Review-first: this patch must be reviewed as evidence before any contract or
runtime work is requested.

Founder decision required: any work outside `hl-dispatch/docs/delivery-recovery/`
or any request for contract, runtime, schema, registry, manifest, config,
OpenAPI, events, facts, reasoncodes, release, production, active contract, MVP,
live booking operation, customer data, payment, billing, entitlement, identity,
privacy, customer asset, sales order, provider, service order, or formal business
object mutation must stop and return for separate Founder / Gate GitHub SSOT.

## Not Authorized

Not Authorized:

1. `hl-contracts` changes.
2. `hl-platform` changes.
3. runtime implementation.
4. schema, registry, manifest, app resource, or config mutation.
5. OpenAPI, events, facts, or reasoncodes mutation.
6. production, release, MVP, active contract, or live booking operation.
7. live customer data mutation or formal booking object mutation.
8. payment, refund, settlement, billing, entitlement, identity/privacy, sales
   order, customer asset, provider, service order, or cross-capability state
   mutation.
9. Agent bypass of Gateway / HK Kernel / Can -> Action -> Audit.
10. Agent holding final booking decision authority.

## Source Evidence

| Evidence | Use in this patch |
|---|---|
| `hl-contracts/docs/pm/capabilities/biz.booking.fulfillment/DUAL-END-PM-REVIEW.md` | Agent End is `PATCH_REQUIRED`; missing areas are retry / duplicate prevention, discovery metadata, tool pruning, context budget, pagination, and evidence summarization. |
| `hl-contracts/apis/biz.booking.fulfillment.internal.openapi.v1.yaml` | References existing Can / Action route pairs, `x-hl-action-contracts`, request schema, `idempotency_key`, `trace_id`, `event_id`, and `reason_code` only. |
| `hl-contracts/events/biz-booking-fulfillment-state-audit.v0.1.yaml` | References existing action_id to event_type and audit fact expectations only. |
| `hl-contracts/reasoncodes/biz-booking-fulfillment-reasoncodes.v0.1.yaml` | References existing non-success reason-code domains only. |
| `hl-platform/biz/booking-fulfillment/capability-manifest.yaml` | Pilot/staging implementation evidence only; not production or MVP authorization. |
| `hl-dispatch/docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-HUMAN-END-PATCH-v0.1-2026-06-15.md` | BF-01 Human End already names human confirmation and review surfaces that Agent End must not bypass. |

## Agent Authority Rules

| Rule | Required behavior | Acceptance rule |
|---|---|---|
| No final booking authority | Agent may prepare, summarize, validate, and call allowed tools only under explicit state and permission boundaries. | Agent cannot make final customer-visible booking decisions without the Human End surface named in BF-01. |
| No Gateway bypass | Agent must use Gateway / HK Kernel / Can -> Action -> Audit. | Any direct state mutation, hidden action, or non-Gateway action path is blocked. |
| Can before Action | Agent must call the matching `.can` endpoint before any Action endpoint. | A denied Can result must stop progression and preserve registered reason_code. |
| Action rechecks Can | Action must recheck Can internally; Agent cannot treat a previous Can result as permanent permission. | Action success must preserve `event_id`; failure or denial must not emit fake success evidence. |
| Schema preservation | Agent must preserve `idempotency_key`, `trace_id`, `event_id`, `reason_code`, booking state, resource refs, and evidence refs when present. | Agent summary cannot omit fields needed for audit or replay review. |
| Resource truth boundary | Agent must not fabricate availability, QRH, customer, offer, payment, asset, service order, or provider state. | Missing upstream evidence triggers fail-secure or separate owner/Gate pull, not inference. |

## Tool Discovery And Pruning Profile

Tool candidates must be discovered from existing SSOT references only:

1. OpenAPI path pairs under `/hk/biz/booking-fulfillment/**.can` and matching
   Action endpoints.
2. `x-hl-action-contracts` mapping to action_id, event_type, required facts, and
   allowed reason-code domains.
3. Existing pilot/staging manifest as read-only evidence of action surface, not
   as production or active runtime authorization.

| Tool class | Examples from SSOT | Pruning rule |
|---|---|---|
| Draft / intake | `booking.draft.persist` | Can be considered only for draft persistence; cannot submit, confirm, cancel, or mutate final state. |
| Customer-visible submission | `booking.submit`, `booking.resubmit` | Requires Human End confirmation and current state evidence before Action. |
| Store confirmation / return | `booking.confirm`, `booking.return_for_resubmit` | Requires store-side review surface and Can result; Agent cannot imply confirmation from chat. |
| Cancellation / reschedule | `booking.cancel`, `booking.reschedule` | Requires actor, reason domain, idempotency_key, and resource effect visibility. |
| Assignment | `booking.artisan.assign`, `booking.artisan.reassign`, `booking.artisan.reassignment.confirm`, `booking.assignment.mark_overdue`, `booking.assignment_overdue.resolve` | Requires assignment status, candidate evidence, and owner / approver pull if override is implied. |
| Resource exception | `booking.resource_release_failure.resolve` | Requires StoreResource / QRH evidence; cross-capability mutation is not authorized. |
| Arrival / no-show | `booking.arrival.complete`, `booking.arrival.mark_overdue`, `booking.no_show.mark` | Requires human confirmation or review for customer-visible and terminal effects. |
| Fast rebook | `booking.fast_rebook` | Treat as new chain candidate only; cannot reuse stale booking state or hidden service flow. |

The tool list above is not a new registry. It is a review matrix over existing
SSOT files.

## Context Budget, Pagination, And Evidence Summary

| Context item | Required Agent handling | Failure behavior |
|---|---|---|
| Current booking state | Include current state, previous state if available, and allowed transition assumption. | If state is missing or stale, call Can or stop; do not infer. |
| Actor and authority | Include actor, role, owner / approver if relevant, and Human End confirmation ref if available. | Missing authority blocks Action. |
| Idempotency and trace | Preserve `idempotency_key`, `trace_id`, and prior event / audit refs. | Missing idempotency for Action blocks Action until BF-04 clarifies retry / duplicate policy. |
| Evidence refs | Summarize source evidence refs, not raw unrelated history. | Generated-only evidence cannot advance GATED progression. |
| Resource / QRH refs | Include hold, release, resource, artisan, room, and schedule refs when relevant. | Missing upstream truth fails secure or pulls BF-05 owner decision. |
| Reason and outcome | Preserve registered non-success `reason_code`; keep success outcome classification out of reason_code. | If reason domain is unknown, stop and pull PM / Gate. |

Pagination rule: Agent must request or summarize only the minimal evidence page
needed for the current action review. Long histories must be summarized with
stable refs and must not drop `event_id`, `trace_id`, `audit_ref`,
`idempotency_key`, `reason_code`, current state, previous state, or resource refs
when those fields exist in SSOT evidence.

## Can / Action / Audit Requirements

| Requirement | Agent End rule | Next owner if gap remains |
|---|---|---|
| Can endpoint | Always call matching `.can` before Action. | BF-03 if Can / Action / Audit trace is unclear. |
| Action endpoint | Action must recheck Can internally. | BF-03 for trace rollup; runtime remains not authorized. |
| Audit result | Successful key Action must preserve `event_id`; failure must preserve reason_code / trace. | BF-03 for event_id / trace_id / audit_ref rollup. |
| Retry / duplicate | Agent cannot blind retry or hide duplicate detection. | BF-04 for retry classes, replay result, duplicate submission result. |
| Override | Agent cannot activate breakglass or owner override from this patch. | BF-04 for owner_role, approver_role, approval_ref. |

## Failure Path

| Failure case | Required Agent End behavior | Result |
|---|---|---|
| tool not discoverable from SSOT | Do not invent tool name, route, or schema. | Stop and mark evidence gap. |
| tool pruned by current state | Do not call Action; explain required state / Can evidence. | No mutation. |
| Can denied | Stop; preserve reason_code and trace. | No Action call. |
| Action fails or returns unknown outcome | Preserve trace and uncertainty; do not synthesize event_id. | Pull BF-04 retry / duplicate policy if needed. |
| context exceeds budget | Summarize with stable evidence refs and required audit fields. | No hidden omission of audit-critical fields. |
| generated-only evidence | Cannot advance GATED progression. | Require independent verification. |
| Human End missing | Do not proceed to final customer-visible or terminal Action. | Pull BF-01 / PM / Gate review. |

## Acceptance Criteria

This BF-02 patch is acceptable only if:

1. Agent authority boundary explicitly blocks final booking decision authority.
2. Gateway / HK Kernel / Can -> Action -> Audit bypass is explicitly blocked.
3. Tool discovery is tied to OpenAPI / `x-hl-action-contracts` / manifest
   evidence and not copied into a new registry.
4. Tool pruning rules distinguish draft, submit, confirm, cancel, reschedule,
   assignment, resource exception, arrival, no-show, and fast rebook surfaces.
5. Context budget preserves audit-critical fields and prevents stale or missing
   evidence from being hidden by summaries.
6. Can before Action and Action rechecks Can are both explicit.
7. Evidence Bundle includes independent verification and failure paths.
8. Learning Patch identifies future rule, template, gate, or agent instruction
   candidates.
9. Ledger keeps `risk_class: GATED` and `execution_state: THIN_SLICE`.

## Remaining Blockers

| Blocker | Next task |
|---|---|
| Gateway / Can / Action / Audit trace still needs per-action rollup. | `BF-03-GATEWAY-CAN-AUDIT` |
| Override owner matrix and approval_ref are still pending. | `BF-04-OVERRIDE-RETRY` |
| Retry / duplicate replay semantics are still pending. | `BF-04-OVERRIDE-RETRY` |
| StoreResource, CustomerProfile, OfferCatalog, and legacy mapping exits are still pending. | `BF-05-DEPENDENCY-EXIT` |

## Next Pull Triggers

Pull PM-A / 邹骢 and Gate-H / 许久明 when:

1. Agent tool discovery needs a new route, schema, OpenAPI field, event, fact, or
   reason_code;
2. tool pruning would expose an Action without Human End confirmation or Can
   result;
3. context budget would omit `event_id`, `trace_id`, `audit_ref`,
   `idempotency_key`, `reason_code`, state, or resource refs;
4. retry, duplicate, replay, override, or approval_ref semantics must become
   active;
5. any Agent End path would imply a contract, runtime, schema, registry,
   manifest, config, OpenAPI, events, facts, reasoncodes, production, release,
   MVP, active contract, live booking operation, or cross-capability state
   mutation;
6. independent evidence is unavailable for GATED progression.

## Validation Commands

```bash
git status --short --branch
git diff --check
git diff --name-only origin/main...HEAD
ruby -e 'require "yaml"; ARGV.each{|f| YAML.load_file(f); puts "YAML_OK: #{f}" }' docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-AGENT-END-EVIDENCE-BUNDLE-v0.1-2026-06-15.yaml docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-AGENT-END-LEARNING-PATCH-v0.1-2026-06-15.yaml docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml
rg -n "Boundary|Not Authorized|Review-first|Founder decision required|Gateway / HK Kernel / Can -> Action -> Audit|BF-02-AGENT-END|Agent End" docs/delivery-recovery
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-github-language-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-action-projection-exporter.py
```
