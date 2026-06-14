# HL Capability Operating Rules Remaining Task Closure v0.1

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-14

## Scope

This file defines the remaining task set for the capability operating rules
loop after PR #260 merged the `biz.booking.fulfillment` Founder / Gate readback
and docs-only patch planning.

It is a dispatch-side execution closure plan. It does not replace
`CAPABILITY-READINESS-LEDGER-v0.1.yaml`, `hl-contracts`, `hl-platform`, GitHub
Issues, PRs, or owner decisions.

The machine-readable task ledger for this plan is
`HL-CAPABILITY-OPERATING-RULES-GOAL-MODE-TASK-LEDGER-v0.1-2026-06-14.yaml`.
The Markdown plan is the human-readable execution brief; the YAML ledger is the
tracking surface for task IDs, dependencies, output files, validation, and
completion criteria.

## Boundary

Boundary: this file may create an execution queue and Definition of Done for
docs-only dispatch work. It is not a contract registry, runtime registry,
capability manifest, schema, OpenAPI, events, facts, reasoncodes, production
approval, release approval, MVP pass, active contract, or live business
operation approval.

Review-first: every task below must land through GitHub PR with explicit scope,
evidence, validation, and non-authorization wording before it can be counted as
done.

Founder decision required: any task that leaves `hl-dispatch/docs/delivery-recovery/`
or requests contract, runtime, schema, registry, manifest, config, OpenAPI,
events, facts, reasoncodes, release, production, active contract, MVP, live
data, payment, billing, entitlement, identity/privacy, or formal business object
mutation must stop and return for a separate Founder / Gate GitHub SSOT.

## Not Authorized

Not Authorized:

1. `hl-contracts` changes.
2. `hl-platform` changes.
3. runtime implementation.
4. schema, registry, manifest, app resource, or config mutation.
5. OpenAPI, events, facts, or reasoncodes mutation.
6. production, release, MVP, active contract, or live business operation.
7. live booking, payment, refund, settlement, billing, entitlement, customer
   identity/privacy, sales order, customer asset, provider, service order, or
   formal business object mutation.
8. generated-only evidence certifying GATED progression.
9. bypassing Gateway / HK Kernel / Can -> Action -> Audit.

## Goal Mode Contract

```yaml
goal_id: hl_capability_operating_rules_remaining_task_closure
objective: close the remaining capability operating-rule tasks as a sequence of bounded docs-only PRs
owner_model: DRI Pull Model
current_authorization: hl-dispatch docs-only
default_branch: origin/main
execution_unit: one PR per bounded task or tightly coupled task pair
confirmation_required:
  - push
  - draft_pr_create
  - merge
  - any scope expansion
stop_if:
  - target branch is unsafe, gone, dirty, or diverged
  - diff leaves hl-dispatch/docs/delivery-recovery/
  - task implies runtime, contract, production, MVP, release, active contract, live data, or live business operation
  - GATED item lacks independent evidence and failure path
done_when:
  - task file or Ledger/readback lands on origin/main
  - GitHub checks pass
  - validation commands are recorded
  - Ledger remains conservative unless separately authorized
  - Learning Patch exists after any state progression
```

## Current State Readback

| Area | Current status | Evidence |
|---|---|---|
| Operating rules | Landed | `HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md` |
| Ledger | Landed and current for 8 initial items | `CAPABILITY-READINESS-LEDGER-v0.1.yaml` |
| Booking staging closeout | Closed for staging evidence only | `BOOKING-STAGING-PILOT-CLOSEOUT-PACKAGE-v0.1-2026-06-14.md` |
| `biz.booking.fulfillment` readiness package | Prepared and accepted as decision basis only | `BIZ-BOOKING-FULFILLMENT-READINESS-PATCH-PACKAGE-v0.1-2026-06-14.md` |
| `biz.booking.fulfillment` Founder / Gate readback | Recorded | `BIZ-BOOKING-FULFILLMENT-FOUNDER-GATE-DECISION-READBACK-v0.1-2026-06-14.md` |
| `biz.booking.fulfillment` docs patch planning | Planned | `BIZ-BOOKING-FULFILLMENT-DOCS-PATCH-PLANNING-v0.1-2026-06-14.md` |
| Open dispatch PRs | none found when this file was prepared | `gh pr list --repo huanlongAI/hl-dispatch --state open` |

## Remaining Phase Tasks

Authoritative machine-readable task list:
`HL-CAPABILITY-OPERATING-RULES-GOAL-MODE-TASK-LEDGER-v0.1-2026-06-14.yaml`

| Phase | Task ID | Objective | Output | Owner | Completion evidence |
|---|---|---|---|---|---|
| Phase 3 / 4 | `BF-01-HUMAN-END` | Close `biz.booking.fulfillment` Human End docs gap. | `BIZ-BOOKING-FULFILLMENT-HUMAN-END-PATCH-PACKET-v0.1-2026-06-14.md` | PM-A / 邹骢, Gate-H / 许久明 | PR merged; file has Boundary, Not Authorized, Review-first, Founder decision required, surfaces, failure path, validation. |
| Phase 3 / 4 | `BF-02-AGENT-END` | Close Agent End readiness criteria gap. | `BIZ-BOOKING-FULFILLMENT-AGENT-END-PATCH-PACKET-v0.1-2026-06-14.md` | Gate-H / 许久明, PM-A / 邹骢 | PR merged; file names tool pruning, context budget, pagination, evidence summarization, Can-before-Action, Action rechecks Can. |
| Phase 3 / 4 | `BF-03-GATEWAY-CAN-AUDIT` | Close Gateway / Can / Action / Audit trace gap. | `BIZ-BOOKING-FULFILLMENT-GATEWAY-CAN-AUDIT-PATCH-PACKET-v0.1-2026-06-14.md` | Gate-H / 许久明 | PR merged; denied Can no-mutation, fail-secure behavior, event_id, trace_id, reason_code, audit_ref are specified. |
| Phase 3 / 4 | `BF-04-OVERRIDE-RETRY` | Close override owner matrix, approval_ref, retry, duplicate, and idempotency policy gaps. | `BIZ-BOOKING-FULFILLMENT-OVERRIDE-RETRY-PATCH-PACKET-v0.1-2026-06-14.md` | Gate-H / 许久明, PM-A / 邹骢 | PR merged; owner / approver / approval_ref matrix and retry classes are specified without activating override path. |
| Phase 3 / 4 | `BF-05-DEPENDENCY-EXIT` | Close StoreResource, CustomerProfile, OfferCatalog, and legacy mapping exit-path gaps. | `BIZ-BOOKING-FULFILLMENT-DEPENDENCY-EXIT-PATH-PACKET-v0.1-2026-06-14.md` | PM-A / 邹骢, Gate-H / 许久明 | PR merged; each dependency has fail-secure or governed resubmit path and cross-capability stop rule. |
| Phase 4 | `BF-06-READINESS-ROLLUP` | Roll up BF-01..BF-05 and decide whether Ledger blocker can move from patch planning to decision packet ready. | Booking fulfillment readiness rollup and Ledger update, if evidence supports it. | PM-A / 邹骢, Gate-H / 许久明 | PR merged; independent evidence and failure paths present; no runtime or contract authorization. |
| Phase 4 | `SO-01-PM-READINESS` | Prepare `biz.sales.order` PM readiness pack. | `BIZ-SALES-ORDER-PM-READINESS-PACKET-v0.1-2026-06-14.md` | PM-A / 邹骢, Gate-H / 许久明 | PR merged; terminology redlines, Contract Gap decision list, no provider/payment/billing/runtime authorization. |
| Phase 4 | `CA-01-PM-READINESS` | Prepare `biz.customer.asset` PM readiness pack. | `BIZ-CUSTOMER-ASSET-PM-READINESS-PACKET-v0.1-2026-06-14.md` | PM-B / 朱阳, Gate-H / 许久明 | PR merged; asset state gaps, identity/customer-profile boundary, Contract Gap decision list, no live asset mutation. |
| Phase 4 | `OC-01-GAP-PATCH` | Prepare `biz.offer.catalog` gap patch. | `BIZ-OFFER-CATALOG-GAP-PATCH-PACKET-v0.1-2026-06-14.md` | PM-B / 朱阳, Gate-H / 许久明 | PR merged; Gateway, OpenAPI, idempotency, Agent/Human split, approval matrix gaps named. |
| Phase 4 | `SR-01-GAP-PATCH` | Prepare `biz.store.resource` gap patch. | `BIZ-STORE-RESOURCE-GAP-PATCH-PACKET-v0.1-2026-06-14.md` | PM-B / 朱阳, Gate-H / 许久明 | PR merged; resource state machine, QRH retry/idempotency, occupancy mutation risk, Human End confirmation surface named. |
| Phase 4 | `TE-01-CHECK-ONLY` | Prepare `biz.tenant.entitlement` check-only evidence packet. | `BIZ-TENANT-ENTITLEMENT-CHECK-ONLY-EVIDENCE-PACKET-v0.1-2026-06-14.md` | Gate-H / 许久明, PM-B / 朱阳 | PR merged; mock/seed/demo boundary, failure path, no live billing/entitlement/quota mutation. |
| Phase 4 | `PC-01-PREFLIGHT` | Prepare `biz.payment.checkout` preflight/blocker packet. | `BIZ-PAYMENT-CHECKOUT-PREFLIGHT-BLOCKER-PACKET-v0.1-2026-06-14.md` | PM-B / 朱阳, Gate-H / 许久明 | PR merged; payment/refund/settlement blocker map, provider sovereignty, idempotency, financial audit, no live money movement. |
| Phase 4 | `LEDGER-01-PORTFOLIO-READBACK` | Update Ledger after all Phase 4 docs-only packets land. | Ledger update and portfolio readback. | Dispatch / Codex | PR merged; every row has current `ssot_refs`, blockers, `not_authorized`, evidence mode, and next action. |
| Phase 5 | `CONTRACT-DP-01` | Prepare future contract decision packet only if a Phase 4 packet proves a contract change is needed. | Capability-specific contract decision packet. | Owning PM + Gate-H | PR merged in dispatch; exact `hl-contracts` files, diff intent, tests, rollback, and non-authorization boundary named. |
| Phase 6 | `PLATFORM-DP-01` | Prepare future platform decision packet only if Founder / Gate wants runtime exploration after Phase 4/5 evidence. | Capability-specific platform decision packet. | Gate-H + Engineering Owner | PR merged in dispatch; exact `hl-platform` files, fixture plan, readiness gate, rollback, and no-production boundary named. |
| Phase 7 | `WEEKLY-01` | Establish weekly Evidence / Learning Patch review. | Weekly review packet or runbook update. | Dispatch / Gate-H | PR merged; changed state, GATED evidence, failure paths, blockers, and Learning Patches reviewed. |
| Phase 8 | `METRICS-30` | Prepare Day-30 mechanism integrity review. | 30-day metrics readback. | Dispatch / Founder / Gate | PR merged; Ledger coverage, GATED bypass count, status misread count, Learning Patch rate, generated-only acceptance count. |
| Phase 8 | `METRICS-60-90` | Prepare Day-60/90 trend review and simplification recommendations. | 60/90-day metrics and simplification packet. | Dispatch / Founder / Gate | PR merged; lead time, blocker wait, rework, independent evidence, failure path coverage, process overhead trend. |

## Execution Order

Use this order unless a Founder / Gate decision changes priority:

1. `BF-01-HUMAN-END`
2. `BF-02-AGENT-END`
3. `BF-03-GATEWAY-CAN-AUDIT`
4. `BF-04-OVERRIDE-RETRY`
5. `BF-05-DEPENDENCY-EXIT`
6. `BF-06-READINESS-ROLLUP`
7. `SO-01-PM-READINESS`
8. `CA-01-PM-READINESS`
9. `OC-01-GAP-PATCH`
10. `SR-01-GAP-PATCH`
11. `TE-01-CHECK-ONLY`
12. `PC-01-PREFLIGHT`
13. `LEDGER-01-PORTFOLIO-READBACK`
14. `CONTRACT-DP-01`, only when needed and separately authorized for decision preparation
15. `PLATFORM-DP-01`, only when needed and separately authorized for decision preparation
16. `WEEKLY-01`
17. `METRICS-30`
18. `METRICS-60-90`

## Per-Task Execution Loop

Every task uses this loop:

```yaml
loop:
  - sync origin/main
  - create task branch from origin/main
  - inspect current Ledger and task-specific SSOT refs
  - create or update exactly the authorized docs-only file set
  - run local validation
  - commit locally
  - request Founder push confirmation
  - push branch only after confirmation
  - request Draft PR confirmation
  - create Draft PR
  - wait for checks
  - request merge confirmation
  - merge only after confirmation and passing checks
  - verify origin/main contains the result
  - update next task state
```

## Per-Task Minimum Validation

```bash
git fetch --prune origin
git status --short --branch
git diff --check
git diff --name-only origin/main...HEAD
python3 - <<'PY'
import yaml
from pathlib import Path
yaml.safe_load(Path('docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml').read_text())
print('LEDGER_YAML_OK')
PY
rg -n "Boundary|Not Authorized|Review-first|Founder decision required|Gateway / HK Kernel / Can -> Action -> Audit" docs/delivery-recovery
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-github-language-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-action-projection-exporter.py
```

## Completion Definition

The remaining task closure is complete only when:

1. all Phase 4 docs-only packets are merged or explicitly deferred with Founder / Gate reason;
2. every GATED item has independent evidence or remains blocked;
3. no GATED item advances on generated-only evidence;
4. every Ledger row has current owner, blocker, `next_action`, `not_authorized`, and `ssot_refs`;
5. every state progression has an Evidence Bundle and Learning Patch;
6. every future contract or runtime request is represented as a decision packet, not silently implemented;
7. there are zero open claims of production, release, MVP, active contract, live business operation, or Gateway bypass without explicit authorization.

## Immediate Next Action

Start with `BF-01-HUMAN-END` as the first task because it is the first blocker
named in the approved `biz.booking.fulfillment` docs-only patch planning file.

Do not start `BF-02` until `BF-01` is either merged or explicitly deferred.

## No Evidence, No Done

No Evidence, No Done remains active. This closure plan is not complete until it
lands through GitHub PR with passing checks and path-scope verification.
