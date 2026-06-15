# Biz Booking Fulfillment Gateway Can Audit Patch v0.1

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-15

## 中文摘要

本文是 `biz.booking.fulfillment` 的 BF-03 Gateway / Can / Action / Audit
docs-only patch。它把网关入口、Can 可做判定、Action 动作执行和 Audit 审计证据之间的
最小可审查链路写成任务包，用于关闭 PM dual-end review 中的 Gateway / Can / Audit
trace 缺口。

本文只做 `hl-dispatch/docs/delivery-recovery/` 文档落库，不授权 runtime、contract、
schema、registry、manifest、config、OpenAPI、events、facts、reasoncodes、生产、发布、
MVP、active contract、live booking operation、真实客户数据或正式业务对象变更。

## 术语说明

- Gateway：网关入口。这里指所有能力动作必须经过 HK Kernel / Gateway 的受控入口。
- Can：可做判定接口。只读，不改变状态，不写审计事件。
- Action：动作执行接口。执行前必须内部复验 Can，成功 key_action 必须返回 `event_id`。
- Audit：审计记录。需要保留 `event_id`、`trace_id`、`audit_ref`、`reason_code` 和必要事实。
- fail-secure：失败时保守停止，不做隐藏状态变更，也不制造成功证据。
- BF-03-GATEWAY-CAN-AUDIT：goal-mode task ledger 中 `biz.booking.fulfillment` 的 Gateway / Can / Audit 任务。
- GATED：高风险执行类别，必须有独立证据、失败路径和 Gate / Founder 可审查边界。

## Scope

```yaml
capability_id: biz.booking.fulfillment
task_id: BF-03-GATEWAY-CAN-AUDIT
dri: Gate-H / 许久明
pm_owner: PM-A / 邹骢
gate_owner: Gate-H / 许久明
maturity: M6_M7
execution_state: THIN_SLICE
risk_class: GATED
ledger_ref: docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml#biz.booking.fulfillment
goal_mode_task_ref: docs/delivery-recovery/HL-CAPABILITY-OPERATING-RULES-GOAL-MODE-TASK-LEDGER-v0.1-2026-06-14.yaml#BF-03-GATEWAY-CAN-AUDIT
```

This file is a dispatch-layer review packet. It references `hl-contracts` and
`hl-platform` evidence, but it does not copy or replace their SSOT content.

## Boundary

Boundary: this patch may define docs-only Gateway / Can / Action / Audit
expectations, trace-preservation rules, denied-Can no-mutation rules, failure
paths, acceptance criteria, and next pull triggers. It is not a runtime design,
contract registry, schema, OpenAPI, events, facts, reasoncodes, manifest, app
resource, config, release approval, production approval, MVP pass, active
contract, or live booking operation approval.

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
9. Agent or human bypass of Gateway / HK Kernel / Can -> Action -> Audit.
10. synthetic `event_id`, synthetic `audit_ref`, or generated-only GATED evidence.

## Source Evidence

| Evidence | Use in this patch |
|---|---|
| `hl-contracts/docs/pm/capabilities/biz.booking.fulfillment/DUAL-END-PM-REVIEW.md` | Gateway Path requires Can from OpenAPI, Action endpoints from OpenAPI, `x-hl-action-contracts`, fail-secure behavior, and no hidden mutation on denied Can. |
| `hl-contracts/apis/biz.booking.fulfillment.internal.openapi.v1.yaml` | References existing Can / Action route pairs, `trace_id`, `event_id`, `idempotency_key`, `reason_code`, and response rules only. |
| `hl-contracts/events/biz-booking-fulfillment-state-audit.v0.1.yaml` | References existing `action_id` to `event_type` and required audit facts only. |
| `hl-contracts/reasoncodes/biz-booking-fulfillment-reasoncodes.v0.1.yaml` | References registered non-success reason-code domains; success arrival classification remains outcome, not `reason_code`. |
| `hl-dispatch/docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-HUMAN-END-PATCH-v0.1-2026-06-15.md` | Human End confirmation and review surfaces that Gateway / Can / Audit must not bypass. |
| `hl-dispatch/docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-AGENT-END-PATCH-v0.1-2026-06-15.md` | Agent End requires Can before Action, Action rechecks Can, schema preservation, and no final booking decision authority. |
| `hl-platform/biz/booking-fulfillment/capability-manifest.yaml` | Pilot/staging implementation evidence only; not production, MVP, release, or active runtime authorization. |

## Gateway / HK Kernel / Can -> Action -> Audit Rules

| Rule | Required behavior | Failure behavior |
|---|---|---|
| Gateway entry | Human End and Agent End must use Gateway / HK Kernel / Can -> Action -> Audit. | Any direct state mutation path is blocked. |
| Can is read-only | `.can` checks do not mutate booking state and do not write audit events. | Denied Can preserves registered `reason_code` and `trace_id`; no Action is called. |
| Action rechecks Can | Action must internally recheck Can even if a previous Can succeeded. | Recheck denial stops the Action and must not emit success `event_id`. |
| Success audit | Successful key_action returns `event_id` and maps to the registered `event_type`. | Missing `event_id` blocks readiness progression. |
| Trace preservation | Preserve `trace_id`, `event_id`, `audit_ref`, `reason_code`, `idempotency_key`, current state, previous state, and resource refs when present. | Missing trace fields are evidence gaps; generated-only evidence cannot advance GATED progression. |
| Reason-code discipline | Use registered non-success booking reason codes for rejection, failure, exception, cancellation, timeout, no-show, and release failure. | Unknown `reason_code` stops and pulls PM / Gate. |
| Outcome discipline | Success arrival classification remains outcome / arrival classification, not `reason_code`. | If success outcome is written as `reason_code`, stop and treat as trace contract violation. |

## Can / Action / Audit Trace Matrix

This matrix is a review surface over existing SSOT files. It is not a new
registry and does not allocate new actions, routes, events, facts, or reason
codes.

| Action family | `action_id` | Can -> Action expectation | Audit event | Required trace rule |
|---|---|---|---|---|
| Draft | `booking.draft.persist` | `.can` must be read-only; Action rechecks Can before persisting draft. | `booking.draft.persisted` | Preserve `event_id`, `trace_id`, `audit_ref`, booking id/status, and no synthetic success evidence. |
| Submission | `booking.submit` | Can before Action; denied Can has no booking mutation. | `booking.submitted` | Preserve `event_id`, `trace_id`, `reason_code` on denial, schedule/resource refs, and audit facts. |
| Store confirmation | `booking.confirm` | Store-side Action rechecks Can before confirmation. | `booking.confirmed` | Preserve previous/current state, QRH ref, `event_id`, `trace_id`, and audit ref. |
| Store return | `booking.return_for_resubmit` | Return Action rechecks Can; no hidden resource release mutation on denied Can. | `booking.returned_for_resubmit` | Preserve previous/current state, resource release ref, registered reason, and audit ref. |
| Timeout | `booking.submission.expire` | Expire Action rechecks Can and must be fail-secure. | `booking.submission.expired` | Preserve hold expiry, release ref, `event_id`, `trace_id`, and registered timeout reason. |
| Resubmission | `booking.resubmit` | Can before Action; stale booking state blocks resubmit. | `booking.resubmitted` | Preserve source booking ref, new state, QRH ref, and audit trace. |
| Cancellation | `booking.cancel` | Can before Action; cancellation reason must be registered. | `booking.cancelled` | Preserve previous/current state, resource release ref, cancellation reason, and audit ref. |
| Reschedule | `booking.reschedule` | Can before Action; resource availability must not be inferred. | `booking.rescheduled` | Preserve schedule refs, QRH ref, `event_id`, `trace_id`, and audit facts. |
| Project change | `booking.project.change` | Can before Action; project / asset refs must remain visible. | `booking.project.changed` | Preserve project ref, asset ref, last action id, and audit trace. |
| Assignment | `booking.artisan.assign` | Can before Action; assignment candidate truth cannot be fabricated. | `booking.artisan.assigned` | Preserve artisan id, assignment status, `event_id`, `trace_id`, and audit ref. |
| Reassignment | `booking.artisan.reassign` | Can before Action; reassignment reason / customer confirmation stays visible. | `booking.artisan.reassigned` | Preserve artisan id, assignment status, customer confirm ref, and audit trace. |
| Reassignment confirmation | `booking.artisan.reassignment.confirm` | Can before Action; confirmation cannot be implied by Agent summary. | `booking.artisan.reassignment_confirmed` | Preserve artisan id, customer confirm ref, `event_id`, and audit ref. |
| Assignment overdue resolution | `booking.assignment_overdue.resolve` | Can before Action; denial has no status mutation. | `booking.assignment_overdue.resolved` | Preserve previous/current state, assignment status, registered reason, and audit ref. |
| Resource release failure | `booking.resource_release_failure.resolve` | Can before Action; StoreResource / QRH truth must be externally visible. | `booking.resource_release_failure.resolved` | Preserve resource release ref, last action id, reason_code, and trace. |
| Arrival complete | `booking.arrival.complete` | Can before Action; arrival outcome is not `reason_code`. | `booking.arrival.completed` | Preserve previous/current state, arrival time, service flow ref, outcome, and audit ref. |
| Arrival overdue | `booking.arrival.mark_overdue` | Can before Action; overdue reason must be registered when non-success. | `booking.arrival.marked_overdue` | Preserve scheduled start, previous/current state, `event_id`, `trace_id`, and audit ref. |
| Assignment overdue mark | `booking.assignment.mark_overdue` | Can before Action; no silent assignment status mutation. | `booking.assignment.marked_overdue` | Preserve deadline, previous/current state, reason_code, and audit ref. |
| No-show | `booking.no_show.mark` | Can before Action; no-show reason must be registered. | `booking.no_show.marked` | Preserve previous/current state, resource release ref, no-show reason, and trace. |
| Fast rebook | `booking.fast_rebook` | Can before Action; no stale booking-state reuse. | `booking.fast_rebooked` | Preserve source booking ref, new state, QRH ref, idempotency key, and audit trace. |

## Failure Paths

| Failure case | Required behavior | Result |
|---|---|---|
| Can denied | Stop; preserve registered `reason_code` and `trace_id`. | No Action call and no mutation. |
| Action recheck denied | Stop; do not emit success `event_id`. | No hidden mutation and no fake audit success. |
| Action returns unknown outcome | Preserve uncertainty and trace fields. | Pull BF-04 retry / duplicate policy if replay is needed. |
| Missing `event_id` on success | Treat as audit evidence gap. | Cannot advance GATED readiness. |
| Missing `trace_id` / `audit_ref` | Treat as trace evidence gap. | Cannot claim independent verification. |
| Unknown `reason_code` | Stop and pull PM / Gate. | No Action or Ledger readiness progression. |
| Success outcome used as `reason_code` | Stop and mark trace contract violation. | Fix rule / template before progression. |
| Upstream dependency evidence missing | Fail secure or pull BF-05 owner decision. | No cross-capability mutation. |
| Generated-only evidence | Cannot advance GATED progression. | Require independent verification and failure path evidence. |

## Acceptance Criteria

This BF-03 patch is acceptable only if:

1. Every listed booking key action has a visible Can -> Action -> Audit trace requirement.
2. Denied Can is explicitly read-only and cannot mutate booking state.
3. Action rechecks Can internally before execution.
4. Successful key_action must preserve `event_id` and registered `event_type`.
5. Failure and denial paths preserve registered `reason_code`, `trace_id`, and no-mutation semantics.
6. `audit_ref`, `idempotency_key`, current state, previous state, and resource refs remain visible when present.
7. Success arrival classification is kept out of `reason_code`.
8. Missing or generated-only evidence cannot advance GATED progression.
9. Evidence Bundle includes independent verification and failure paths.
10. Ledger keeps `risk_class: GATED` and `execution_state: THIN_SLICE`.

## Remaining Blockers

| Blocker | Next task |
|---|---|
| Override owner matrix and approval_ref are still pending. | `BF-04-OVERRIDE-RETRY` |
| Retry / duplicate replay semantics are still pending. | `BF-04-OVERRIDE-RETRY` |
| StoreResource, CustomerProfile, OfferCatalog, and legacy mapping exits are still pending. | `BF-05-DEPENDENCY-EXIT` |
| Readiness rollup still needs BF-01 through BF-05 merged evidence. | `BF-06-READINESS-ROLLUP` |

## Next Pull Triggers

Pull PM-A / 邹骢 and Gate-H / 许久明 when:

1. any Action lacks a matching Can, event mapping, trace field, reason-code
   domain, or audit facts evidence;
2. denied Can would still mutate booking state or write a success audit event;
3. Action success cannot preserve `event_id`, `trace_id`, `audit_ref`, or
   required facts;
4. retry, duplicate, replay, override, or approval_ref semantics must become
   active;
5. dependency truth from StoreResource, CustomerProfile, OfferCatalog, QRH,
   service flow, payment, asset, provider, or service order is missing;
6. any path would imply contract, runtime, schema, registry, manifest, config,
   OpenAPI, events, facts, reasoncodes, production, release, MVP, active
   contract, live booking operation, or cross-capability state mutation.

## Validation Commands

```bash
git status --short --branch
git diff --check
git diff --name-only -- ':!docs/delivery-recovery/**'
ruby -e 'require "yaml"; ARGV.each{|f| YAML.load_file(f); puts "YAML_OK: #{f}" }' docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-GATEWAY-CAN-AUDIT-EVIDENCE-BUNDLE-v0.1-2026-06-15.yaml docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-GATEWAY-CAN-AUDIT-LEARNING-PATCH-v0.1-2026-06-15.yaml docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml
rg -n "Boundary|Not Authorized|Review-first|Founder decision required|Gateway / HK Kernel / Can -> Action -> Audit|BF-03-GATEWAY-CAN-AUDIT|Can -> Action -> Audit" docs/delivery-recovery
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-github-language-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-action-projection-exporter.py
```
