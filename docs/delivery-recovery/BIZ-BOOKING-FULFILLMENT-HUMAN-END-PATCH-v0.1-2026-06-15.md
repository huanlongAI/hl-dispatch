# Biz Booking Fulfillment Human End Patch v0.1

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-15

## 中文摘要

本文是 `biz.booking.fulfillment` 的 BF-01 Human End docs-only patch。它把
人端确认、复核、例外处理、override、审计查看和失败路径写成可审查的任务包，
用于关闭 PM dual-end review 中的 Human End 缺口。

本文不授权 runtime、contract、schema、registry、manifest、config、OpenAPI、
events、facts、reasoncodes、生产、发布、MVP、active contract、live booking
operation、真实客户数据或正式业务对象变更。

## 术语说明

- Human End：人端可见、可确认、可复核、可审计的操作面，不等于 chat-only。
- Gateway / HK Kernel / Can -> Action -> Audit：网关、可做判定、动作执行、审计链路。
- BF-01-HUMAN-END：goal-mode task ledger 中 `biz.booking.fulfillment` 的第一个未完成任务。
- GATED：高风险执行类别，必须有独立证据、失败路径和 Gate / Founder 可审查边界。

## Scope

```yaml
capability_id: biz.booking.fulfillment
task_id: BF-01-HUMAN-END
dri: PM-A / 邹骢
pm_owner: PM-A / 邹骢
gate_owner: Gate-H / 许久明
maturity: M6_M7
execution_state: THIN_SLICE
risk_class: GATED
ledger_ref: docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml#biz.booking.fulfillment
goal_mode_task_ref: docs/delivery-recovery/HL-CAPABILITY-OPERATING-RULES-GOAL-MODE-TASK-LEDGER-v0.1-2026-06-14.yaml#BF-01-HUMAN-END
```

This file is a dispatch-layer Human End patch package. It references
`hl-contracts` and `hl-platform` evidence, but it does not copy or replace their
SSOT content.

## Boundary

Boundary: this patch may define docs-only Human End expectations, review
surfaces, acceptance criteria, failure paths, and next pull triggers. It is not a
runtime design, contract registry, schema, OpenAPI, events, facts, reasoncodes,
manifest, app resource, config, release approval, production approval, MVP pass,
active contract, or live booking operation approval.

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

## Source Evidence

| Evidence | Use in this patch |
|---|---|
| `hl-contracts/docs/pm/capabilities/biz.booking.fulfillment/DUAL-END-PM-REVIEW.md` | Human End is `PATCH_REQUIRED`; required surfaces are NUI intent entry, GUI state anchor, confirmation, review, audit, exception handling, and deterministic controls. |
| `hl-dispatch/docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-READINESS-PATCH-PACKAGE-v0.1-2026-06-14.md` | Current readiness result is patch package ready, not runtime expansion. |
| `hl-dispatch/docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-DOCS-PATCH-PLANNING-v0.1-2026-06-14.md` | Human End patch is the first planned follow-up lane. |
| `hl-contracts/apis/biz.booking.fulfillment.internal.openapi.v1.yaml` | References Can / Action route and action_id names only; no OpenAPI mutation. |
| `hl-contracts/events/biz-booking-fulfillment-state-audit.v0.1.yaml` | References existing event and audit semantics only. |
| `hl-contracts/reasoncodes/biz-booking-fulfillment-reasoncodes.v0.1.yaml` | References existing reason-code trace domains only. |
| `hl-platform/biz/booking-fulfillment/capability-manifest.yaml` | Pilot/staging evidence only; not production or MVP authorization. |

## Human Touchpoint Matrix

| Human touchpoint | Required human surface | Gateway / Can assumption | Audit / review output |
|---|---|---|---|
| booking intent entry | NUI intent may start draft capture; GUI must show booking detail anchor before final action. | Human intent does not bypass Can. | intent evidence ref, trace_id, actor, draft state. |
| `booking.submit` | Human confirmation is required before customer-visible submission. | Can precheck and Action recheck Can. | event_id on success; reason_code on reject; audit_ref. |
| `booking.confirm` | Store-side confirmation surface with booking state, resource hold, service, customer refs, and blocked reasons. | Confirmation cannot be implied by Agent text. | event_id, previous_state, booking_state, trace_id. |
| `booking.cancel` | Cancellation confirmation surface must show cancel actor, reason domain, resource-release effect, and dispute risk. | Cancellation Action must recheck Can and preserve idempotency_key. | cancellation evidence ref, reason_code, audit_ref. |
| `booking.reschedule` | Reschedule confirmation must show previous slot, target slot, resource / artisan dependency, and customer-visible effect. | No hidden resource occupancy mutation from docs-only patch. | reschedule event ref, reason_code if blocked. |
| `booking.artisan.reassign` | Reassign review surface must show candidate artisan, assignment status, approval_ref if required, and conflict result. | Owner / approver matrix remains separate BF-04 work. | assignment evidence ref, trace_id, audit_ref. |
| `booking.assignment_overdue.resolve` | Review surface must force explicit resolution path: manual assignment, governed resubmit, or fail-secure. | Automatic cancellation is not authorized by this patch. | resolution evidence, reason_code, audit_ref. |
| `booking.resource_release_failure.resolve` | Exception surface must show release failure ref, upstream StoreResource evidence, human approver, and retry/exit path. | Cross-capability effects require separate owner/Gate record. | resource_release_ref, approval_ref if required. |
| `booking.no_show.mark` | No-show marking must require confirmation, evidence ref, dispute path, and resource-release visibility. | Agent cannot hold final no-show decision authority. | no_show event, reason_code, audit_ref. |

## Confirmation, Review, and Exception Rules

| Class | Required human judgment | Acceptance rule |
|---|---|---|
| Customer-visible state change | Human must see current state, intended transition, blocked reason if any, and post-action audit result. | No final state-changing Action can be represented as chat-only acceptance. |
| Store/resource-impacting action | Human must see StoreResource / QRH dependency status or an explicit evidence-missing warning. | If upstream evidence is missing, fail secure or route to governed resubmit. |
| Override / breakglass | Human must see owner_role, approver_role, approval_ref, allowed reason-code domain, and evidence_refs. | Owner / approver activation remains pending BF-04; this patch only names the required surface. |
| Exception handling | Human must see duplicate, retry, hold expiry, release failure, manual cancellation, no-show dispute, and evidence-missing cases. | Every exception path must produce trace_id and audit_ref or remain blocked. |

## Gateway / Can Path Assumptions and Gaps

Assumptions:

1. Can endpoints are read-only and do not change booking state.
2. Action endpoints must recheck Can.
3. Successful key actions return event_id.
4. Denied or failed paths must use registered booking reason-code domains.
5. Human End surfaces must preserve trace_id, audit_ref, reason_code, idempotency_key, booking_state, previous_state, and evidence_refs when those fields are present in the source contract.

Known gaps that this patch does not close:

1. Agent End discovery, tool pruning, context budget, pagination, and evidence summarization remain BF-02.
2. Gateway / Can / Action / Audit trace rollup remains BF-03.
3. Override owner matrix, approval_ref, retry, duplicate, and idempotency replay semantics remain BF-04.
4. StoreResource, CustomerProfile, OfferCatalog, and legacy mapping exit paths remain BF-05.

## Failure Path

| Failure case | Required Human End behavior | Result |
|---|---|---|
| duplicate submission | Show duplicate warning, existing evidence ref if known, and block hidden resubmission. | Do not mutate state without governed retry policy. |
| retry after internal error | Show uncertain outcome and require evidence lookup or fail-secure retry class from BF-04. | No blind retry. |
| hold expiry | Show hold expiry status and require StoreResource / QRH evidence or fail-secure exit. | No stale hold confirmation. |
| manual cancellation | Show actor, reason domain, customer-visible effect, and resource release impact. | Audit is required. |
| override request | Show owner/approver fields as required but mark activation pending BF-04. | No active override path from this patch. |
| evidence missing | Show missing evidence type and block progression or route to PM/Gate pull trigger. | Generated-only evidence cannot advance GATED progression. |

## Acceptance Criteria

This BF-01 patch is acceptable only if:

1. Human End surfaces are named for NUI intent entry, GUI state anchor,
   confirmation, review, audit, exception handling, and deterministic controls.
2. High-risk booking actions have explicit human confirmation or review
   expectations.
3. Failure paths include duplicate, retry, hold expiry, manual cancellation,
   override, and evidence-missing cases.
4. Gateway / HK Kernel / Can -> Action -> Audit bypass is explicitly blocked.
5. The companion Evidence Bundle is not generated-only and includes independent
   partial verification.
6. The companion Learning Patch identifies a future rule, template, gate, or
   agent instruction candidate.
7. Ledger keeps `risk_class: GATED` and `execution_state: THIN_SLICE`.

## Remaining Blockers

| Blocker | Next task |
|---|---|
| Agent tool pruning and authority boundary are not explicit enough. | `BF-02-AGENT-END` |
| Gateway / Can / Audit trace still needs per-action rollup. | `BF-03-GATEWAY-CAN-AUDIT` |
| Override owner matrix and approval_ref are still pending. | `BF-04-OVERRIDE-RETRY` |
| Retry / duplicate replay semantics are still pending. | `BF-04-OVERRIDE-RETRY` |
| StoreResource, CustomerProfile, OfferCatalog, and legacy mapping exits are still pending. | `BF-05-DEPENDENCY-EXIT` |

## Next Pull Triggers

Pull PM-A / 邹骢 and Gate-H / 许久明 when:

1. a confirmation threshold changes;
2. owner_role / approver_role / approval_ref must become active;
3. any Human End path would imply a contract, runtime, schema, registry,
   manifest, config, OpenAPI, events, facts, reasoncodes, production, release,
   MVP, active contract, live booking operation, or cross-capability state
   mutation;
4. independent evidence is unavailable for GATED progression;
5. a human concern needs conversion into `not_authorized`, acceptance criterion,
   or risk trigger.

## Validation Commands

```bash
git status --short --branch
git diff --check
git diff --name-only origin/main...HEAD
ruby -e 'require "yaml"; ARGV.each{|f| YAML.load_file(f); puts "YAML_OK: #{f}" }' docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-HUMAN-END-EVIDENCE-BUNDLE-v0.1-2026-06-15.yaml docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-HUMAN-END-LEARNING-PATCH-v0.1-2026-06-15.yaml docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml
rg -n "Boundary|Not Authorized|Review-first|Founder decision required|Gateway / HK Kernel / Can -> Action -> Audit|BF-01-HUMAN-END|Human End" docs/delivery-recovery
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-github-language-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-action-projection-exporter.py
```
