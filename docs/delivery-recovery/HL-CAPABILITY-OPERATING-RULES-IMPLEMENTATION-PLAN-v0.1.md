# HL Capability Operating Rules Implementation Plan v0.1

> Status: FULL_LANDING_PLAN_DRAFT
> Date: 2026-06-14
> Scope: complete landing plan for operating rules, Ledger, first capability cycle, future contract/runtime decision packets, and review cadence
> Boundary: Current implementation is docs-only in `hl-dispatch`. Future `hl-contracts` or `hl-platform` work requires separate Founder decision.
> Review-first / Founder decision required: this plan may prepare future decision packets, but any contract, runtime, schema, registry, manifest, config, release, or live business operation remains not authorized until separately approved.

## 1. Objective

Land the full capability operating plan so the team can move from scattered capability evidence to a controlled operating loop:

1. DRI owns forward movement.
2. Risk triggers pull PM/Gate/Founder only when needed.
3. Ledger prevents status misreads.
4. Evidence Bundle prevents AI self-certification.
5. Learning Patch compounds process knowledge.
6. Future contract/runtime work is routed through explicit decision packets.

## 2. Phase Overview

| Phase | Window | Objective | Current authorization |
|---|---:|---|---|
| Phase 0 | immediate | freshness, branch, forbidden-path guard | authorized |
| Phase 1 | day 0-1 | land docs, Ledger, decision log, templates | authorized |
| Phase 2 | day 1-2 | owner and status normalization | dispatch docs authorized |
| Phase 3 | day 2-7 | first operating cycle for 8 items | dispatch docs authorized |
| Phase 4 | day 7-14 | capability-specific readiness closure | dispatch docs authorized; contracts/platform no |
| Phase 5 | day 14-30 | prepare contract decision packets | prepare only |
| Phase 6 | day 14-45 | prepare platform decision packets | prepare only |
| Phase 7 | weekly | Evidence and Learning Patch cadence | authorized for dispatch docs |
| Phase 8 | day 30/60/90 | metrics and simplification review | authorized for reporting |

## 3. Phase 0 — Preflight and Branch Hygiene

### Actions

1. Fetch and prune `hl-dispatch`.
2. Check current branch and working tree.
3. Avoid landing on unsafe ahead/gone branch.
4. Prefer new branch from up-to-date `origin/main`:
   `codex/capability-operating-rules-v0.2-20260614`
5. Confirm `hl-contracts` and `hl-platform` remain untouched.

### Stop Conditions

| Stop condition | Required status |
|---|---|
| Dirty working tree before changes | `TARGET_BRANCH_DECISION_REQUIRED` |
| Current branch unsafe and no safe branch can be created | `TARGET_BRANCH_DECISION_REQUIRED` |
| Any needed change outside dispatch docs | record future decision packet; do not implement |

## 4. Phase 1 — Docs and Ledger Landing

### Files

| File | Action |
|---|---|
| `HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md` | create |
| `CAPABILITY-READINESS-LEDGER-v0.1.yaml` | create |
| `HL-CAPABILITY-OPERATING-RULES-IMPLEMENTATION-PLAN-v0.1.md` | create |
| `FOUNDER-DECISION-LOG-CAPABILITY-OPERATING-RULES-v0.1.md` | create |
| `EVIDENCE-BUNDLE-TEMPLATE-v0.1.yaml` | create |
| `LEARNING-PATCH-TEMPLATE-v0.1.yaml` | create |

### Validation

1. YAML parses.
2. Diff only touches approved dispatch docs path.
3. Ledger has exactly the approved initial items.
4. No Ledger entry claims release or live operation.
5. `hl-contracts` and `hl-platform` status remain unchanged.

## 5. Phase 2 — Owner and Status Normalization Within 48 Hours

### Objective

Convert `TBD_FOUNDER_DECISION` owner fields into named owners or explicit blockers.

### Owner Table

| Owner field | Required decision |
|---|---|
| DRI | one directly responsible person per Ledger item |
| PM owner | one owner or `not_required` |
| Gate owner | one owner or `not_required` only if REVERSIBLE and no gate touch |

### Required Output

1. Updated Ledger owner fields.
2. Any remaining `TBD_FOUNDER_DECISION` listed as blocker.
3. First weekly review agenda.

## 6. Phase 3 — First Operating Cycle for 8 Items

| Item | Allowed next action | Required evidence | Escalation trigger | Prohibited interpretation |
|---|---|---|---|---|
| Booking staging pilot closeout | closeout decision package | local evidence + live issue/PR evidence if available | live state unknown | release/production/merged claim |
| `biz.booking.fulfillment` | patch readiness gaps | Human End, Agent manifest, owner matrix, retry policy | Gateway/Human/Agent gaps remain | release claim |
| `biz.sales.order` | PM readiness pack | Cap-Spec readiness, terminology correction, Contract Gap | provider/payment/billing appears | runtime start |
| `biz.customer.asset` | PM readiness pack | state machine and Contract Gap decision | active contract or identity risk appears | runtime start |
| `biz.offer.catalog` | gap patch plan | Gateway/OpenAPI/idempotency/approval matrix | engineering start pressure | implementation start |
| `biz.store.resource` | gap patch plan | Gateway/state machine/retry/idempotency | resource occupancy mutation | implementation start |
| `biz.tenant.entitlement` | check-only evidence | mock/seed/demo evidence + failure path | live entitlement or billing appears | live entitlement mutation |
| `biz.payment.checkout` | preflight/blocker | provider sovereignty and financial audit gap list | live money flow appears | payment integration |

## 7. Phase 4 — Capability-Specific Readiness Closure

### 7.1 Booking closeout

Goal: close status ambiguity.

Required outputs:

1. local repo evidence summary;
2. live Issue/PR evidence if accessible;
3. recommendation: merge follow-up, split follow-up, close superseded, or keep blocked;
4. explicit non-release wording.

### 7.2 `biz.booking.fulfillment` PATCH

Required outputs:

1. Human End surface;
2. Agent manifest requirements;
3. override owner matrix;
4. retry / duplicate policy;
5. failure fixture requirement;
6. Gate H requirement.

### 7.3 `biz.sales.order` PM readiness

Required outputs:

1. PM readiness pack index;
2. terminology redline;
3. no provider/payment/billing authorization statement;
4. Contract Gap decision list.

### 7.4 `biz.customer.asset` PM readiness

Required outputs:

1. PM readiness pack index;
2. asset state model gaps;
3. identity/customer profile dependency boundary;
4. Contract Gap decision list.

### 7.5 `biz.offer.catalog` gap patch

Required outputs:

1. Gateway path gap;
2. OpenAPI gap;
3. idempotency rule;
4. approval matrix;
5. Agent/Human End split.

### 7.6 `biz.store.resource` gap patch

Required outputs:

1. resource state machine gap;
2. QRH retry/idempotency rules;
3. Gateway path gap;
4. occupancy mutation risk notes;
5. Human End confirmation surface.

### 7.7 `biz.tenant.entitlement` check-only

Required outputs:

1. check-only evidence index;
2. mock/seed/demo boundary;
3. failure path;
4. explicit no live entitlement mutation statement.

### 7.8 `biz.payment.checkout` preflight

Required outputs:

1. payment/refund/settlement blocker map;
2. provider sovereignty risk;
3. idempotency and financial audit requirements;
4. explicit no live money movement statement.

## 8. Phase 5 — Future Contract Decision Packets

No contract changes are authorized now.

Prepare decision packets for future Founder review when necessary:

| Target | Trigger | Packet must include |
|---|---|---|
| `hl-contracts` capability blueprint | key_action, reason_code, lifecycle, or risk_level change needed | exact file, diff intent, compatibility check, rollback |
| `hl-contracts/prd/biz/**` | Cap-Spec or Contract Gap must be updated | source evidence, scope, review owner |
| OpenAPI/events/facts | new or changed formal surface needed | schema impact, consumer impact, audit impact |
| taxonomy/reason_code | new reason_code proposed | naming, semantics, deprecation risk |

Required status after preparation:

`CONTRACT_DECISION_PACKET_READY_AWAITING_FOUNDER`

## 9. Phase 6 — Future Platform Decision Packets

No platform changes are authorized now.

Prepare decision packets for future Founder review when necessary:

| Target | Trigger | Packet must include |
|---|---|---|
| `hl-platform/biz/**` module | runtime thin slice needed | capability scope, manifest impact, fixture plan, gate plan |
| readiness gate | new gate or fixture needed | risk, test evidence, failure mode |
| app resources | should normally be avoided | reason why module-local path is insufficient |
| runtime handler | action execution needed | Gateway path, Can check, audit, idempotency, rollback |

Required status after preparation:

`PLATFORM_DECISION_PACKET_READY_AWAITING_FOUNDER`

## 10. Phase 7 — Evidence and Learning Patch Cadence

### Weekly Review Agenda

1. Which Ledger items changed state?
2. Which GATED items still have generated-only evidence?
3. Which items lack failure path evidence?
4. Which blockers require Founder/Gate decision?
5. Which Learning Patches were created?
6. Which rules/templates/prompts/gates should be simplified?

### Learning Patch Routing

| Patch type | Default action |
|---|---|
| RULE_PATCH | update dispatch operating rules |
| TEMPLATE_PATCH | update dispatch template |
| AGENT_PROMPT_PATCH | prepare target-specific decision if prompt lives outside dispatch |
| GATE_PATCH | prepare platform decision packet |
| TAXONOMY_PATCH | prepare contracts decision packet |
| DEFER_PATCH | update implementation plan / Ledger defer reason |

## 11. Phase 8 — 30/60/90-Day Metrics

### Day 30: Mechanism Integrity

| Metric | Target |
|---|---|
| Ledger coverage | 100% for active/PM-led/pilot items |
| `not_authorized` coverage | 100% |
| GATED bypass | 0 |
| status misread | 0 |
| Learning Patch after progression | 100% |
| generated-only evidence accepted for GATED | 0 |

### Day 60-90: Operational Trend

| Metric | Desired direction |
|---|---|
| lead time | down |
| blocker wait | down |
| rework rate | down |
| independent evidence | up |
| failure path coverage | up |
| reversible autonomous movement | up |
| process overhead | down or justified |

## 12. Simplification Trigger

If the operating rules add overhead without reducing misread, blocker, or rework, simplify.

A field or ritual should be removed when:

1. it has not affected a decision in two consecutive weekly reviews;
2. it duplicates SSOT;
3. it encourages reporting rather than action;
4. it causes DRI to wait for default approvals.

## 13. Final Definition of Done

The complete landing plan is done when:

1. the six dispatch docs are landed;
2. Ledger covers the initial scope;
3. owner gaps are either assigned or explicit blockers;
4. the first weekly review is scheduled;
5. every future contracts/platform action is represented as a decision packet, not silently implemented;
6. no runtime/contract/release authority is implied by dispatch docs.
