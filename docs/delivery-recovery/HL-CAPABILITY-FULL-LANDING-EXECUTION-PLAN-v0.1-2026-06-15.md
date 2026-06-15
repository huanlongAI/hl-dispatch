# HL Capability Full Landing Execution Plan v0.1

Status: DRAFT_PLAN_PR
Date: 2026-06-15
Scope: full landing execution planning for capability operating rules
Boundary: docs-only planning in `hl-dispatch/docs/delivery-recovery/`

## 1. Executive summary

This plan defines the remaining full landing path for the capability operating
rules after BF-03 Gateway / Can / Audit landed. It is a planning artifact only.
It does not execute BF-04, BF-05, BF-06, BF-07, portfolio readback, contract
changes, platform changes, runtime work, release work, or live business
operation.

Full landing in this plan means every active, pilot, or PM-led capability item
reaches an explicit planning terminal state: closed, ready for Founder / Gate
decision, blocked with owner and evidence, deferred with reason, or prepared for
a separate contract / platform decision packet.

## 2. Boundary and non-authorization statement

Allowed write scope for this planning PR:

- `hl-dispatch/docs/delivery-recovery/`

Forbidden scope:

- `hl-contracts/**`
- `hl-platform/**`
- runtime code
- schema, registry, manifest, config
- OpenAPI, events, facts, reasoncodes
- live booking operation
- live payment, refund, settlement, billing
- entitlement or quota mutation
- customer identity or privacy mutation
- formal business object mutation

This plan does not authorize production, release, MVP, active contract,
runtime authorization, live business operation, or cross-repo implementation.
Any future work that needs `hl-contracts` or `hl-platform` must be routed as a
decision packet first.

## 3. Current verified anchor

Fresh verification in the clean worktree established:

- PR #269 is merged.
- PR #269 merge commit is `f923c99cddcd68ae955d13f4d3648aebe718d9a3`.
- `origin/main` contains the BF-03 Gateway / Can / Audit merge history.
- `CAPABILITY-READINESS-LEDGER-v0.1.yaml` records `due:
  BF-04-OVERRIDE-RETRY_PR` for `biz.booking.fulfillment`.
- Required operating files exist:
  - `HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md`
  - `CAPABILITY-READINESS-LEDGER-v0.1.yaml`
  - `EVIDENCE-BUNDLE-TEMPLATE-v0.1.yaml`
  - `LEARNING-PATCH-TEMPLATE-v0.1.yaml`
  - `HL-CAPABILITY-OPERATING-RULES-GOAL-MODE-TASK-LEDGER-v0.1-2026-06-14.yaml`

## 4. Definition of full landing

Full landing means the operating loop has no ambiguous active, pilot, or PM-led
capability item. Each item must end this planning run with one explicit target:

1. closed for the current evidence scope;
2. ready for Founder / Gate decision;
3. blocked with owner and evidence;
4. deferred with reason;
5. prepared for a separate contract decision packet;
6. prepared for a separate platform decision packet.

Full landing does not mean production authorization.

## 5. Current completed baseline

The current baseline is dispatch-side evidence only:

| Area | Verified current state |
|---|---|
| Operating rules | Rules v0.2 landed. |
| Readiness Ledger | Ledger landed and continuously updated. |
| Templates | Evidence Bundle and Learning Patch templates landed. |
| Remaining task closure | Remaining task closure plan landed. |
| Cycle 1 scorecard | Scorecard landed. |
| BF-01 Human End | Docs-only patch, Evidence Bundle, and Learning Patch landed. |
| Tenant Entitlement check-only | Check-only slice, Evidence Bundle, and Learning Patch landed. |
| BF-02 Agent End | Docs-only patch, Evidence Bundle, and Learning Patch landed. |
| BF-03 Gateway / Can / Audit | Docs-only patch, Evidence Bundle, and Learning Patch landed in PR #269. |

None of the above authorizes runtime, contract, production, release, MVP,
active contract, or live business operation.

## 6. Remaining backlog

Minimum remaining backlog:

| Backlog item | Current planning role |
|---|---|
| BF-04 Override / Retry | Close owner matrix, approval_ref, retry classes, duplicate handling, and idempotency replay policy. |
| BF-05 Dependency Exit | Close StoreResource, CustomerProfile, OfferCatalog, QRH, and legacy mapping exit paths. |
| BF-06 Readiness Rollup | Roll up BF-01 through BF-05 evidence and decide whether `biz.booking.fulfillment` can become decision-packet ready. |
| BF-07 Founder / Gate Decision Packet | Conditional packet if BF-06 shows enough evidence for a next Gate decision. |
| Portfolio Readback | Reconcile the initial 8 Ledger items into explicit terminal planning states. |
| Contract Decision Packet | Conditional dispatch-side packet only. No `hl-contracts` implementation. |
| Platform Decision Packet | Conditional dispatch-side packet only. No `hl-platform` implementation. |
| Weekly Review | Establish evidence and learning review cadence. |
| Metrics 30/60/90 | Track mechanism integrity and trend metrics. |
| Rule thinning | Remove fields or rituals that do not affect decisions. |
| Risk-class evolution | Revisit whether REVERSIBLE / GATED is too coarse. |
| Discovery / value judgment loop | Restore upstream product value judgment before delivery pressure expands scope. |

## 7. Initial 8-item portfolio closure

| Item | Current state | Required next evidence | Allowed terminal state for this wave | Forbidden claims | Owner slot | Contract packet? | Platform packet? |
|---|---|---|---|---|---|---|---|
| `booking_staging_pilot_closeout` / `hl-platform#106` | THIN_SLICE / GATED; closed for staging evidence only. | Live issue / PR evidence if broader claim is requested. | Closed for staging evidence only, or ready for Founder / Gate packet. | release, production, merged-delivery without evidence. | Gate-H / Xu Jiuming | possible if active contract is requested | possible if runtime expansion is requested |
| `biz.booking.fulfillment` | THIN_SLICE / GATED; BF-01..BF-03 prepared; BF-04 next. | BF-04, BF-05, BF-06 bundles with independent verification and failure paths. | Ready for Founder / Gate decision packet, or blocked with evidence. | live booking operation, runtime authorization, active contract. | PM-A / Zou Cong + Gate-H / Xu Jiuming | possible | possible |
| `biz.sales.order` | SPEC_ONLY / GATED; PM readiness only. | PM readiness pack, terminology redlines, Contract Gap list. | PM readiness prepared, blocked, or deferred. | provider, payment, billing, live sales object mutation. | PM-A / Zou Cong | likely | possible later |
| `biz.customer.asset` | SPEC_ONLY / GATED; PM readiness only. | PM readiness pack, asset state gap list, identity / privacy boundary. | PM readiness prepared, blocked, or deferred. | live customer asset mutation, identity merge, privacy mutation. | PM-B / Zhu Yang | likely | possible later |
| `biz.offer.catalog` | SPEC_ONLY / GATED; PM dual-end review blocked. | Gateway, OpenAPI, idempotency, Agent / Human split, approval matrix gap pack. | Gap pack prepared or blocked with owner evidence. | PRD-direct engineering start, live catalog mutation, approval bypass. | PM-B / Zhu Yang | likely | possible later |
| `biz.store.resource` | SPEC_ONLY / GATED; PM dual-end review blocked. | Gateway, normalized state machine, QRH retry / idempotency, Human End confirmation gap pack. | Gap pack prepared or blocked with owner evidence. | live resource occupancy mutation, Gateway bypass, idempotency bypass. | PM-B / Zhu Yang | likely | possible later |
| `biz.tenant.entitlement` | THIN_SLICE / REVERSIBLE; check-only slice prepared for review. | Independent verifier readback for mock / seed / demo and failure cases. | Check-only closure, blocked for independent evidence, or decision packet if mutation appears. | live billing, entitlement deduction, quota mutation, commercial tenant mutation. | Gate-H / Xu Jiuming | possible if full capability requested | possible if runtime requested |
| `biz.payment.checkout` | SPEC_ONLY / GATED; preflight only. | Provider sovereignty, idempotency, financial audit, blocker map. | Preflight blocker map prepared or deferred. | provider integration, refund, settlement, financial ledger mutation, live money movement. | PM-B / Zhu Yang | likely | likely |

## 8. Wave execution model

This planning PR creates the wave model only. Wave execution requires separate
Founder authorization after this PR is reviewed.

### Wave 1: Booking Fulfillment closeout cluster

| task_id | Goal | Branch | Output files | Evidence requirement | Learning Patch | Ledger delta | Validation command | Stop condition | Next Founder decision |
|---|---|---|---|---|---|---|---|---|---|
| BF-04-OVERRIDE-RETRY | Close override owner matrix, approval_ref, retry classes, duplicate handling, and idempotency replay policy. | `codex/cap-cycle2-bf04-override-retry-20260615` | BF-04 patch, Evidence Bundle, Learning Patch, optional Ledger delta. | Independent verification plus failure path for retry, duplicate, replay, and override ambiguity. | required | required | YAML parse, diff scope, boundary keyword scan. | Any active override or runtime path is implied. | GO_WAVE_1 or revise. |
| BF-05-DEPENDENCY-EXIT | Close StoreResource, CustomerProfile, OfferCatalog, QRH, and legacy mapping exit paths. | `codex/cap-cycle2-bf05-dependency-exit-20260615` | BF-05 patch, Evidence Bundle, Learning Patch, optional Ledger delta. | Dependency failure path evidence and cross-capability stop rules. | required | required | YAML parse, diff scope, boundary keyword scan. | Any dependency mutation is implied. | Continue Wave 1 or pause. |
| BF-06-READINESS-ROLLUP | Roll up BF-01..BF-05 and propose readiness state. | `codex/cap-cycle2-bf06-readiness-rollup-20260615` | BF-06 rollup, Evidence Bundle, Learning Patch, Ledger delta proposal. | Independent evidence summary across BF-01..BF-05 and failure path summary. | required | required | YAML parse, diff scope, Ledger consistency check. | Evidence remains generated-only or failure paths missing. | BF-07 required if decision-packet ready. |
| BF-07-FOUNDER-GATE-DECISION-PACKET | Conditional Founder / Gate packet after BF-06. | `codex/cap-cycle2-bf07-founder-gate-packet-20260615` | BF-07 decision packet only. | BF-06 evidence references and explicit non-authorization boundary. | false | false | diff scope and boundary keyword scan. | Packet would implement contract or runtime. | Founder / Gate decision. |

### Wave 2: Portfolio Readback and eight-item Ledger closure

| task_id | Goal | Branch | Output files | Evidence requirement | Learning Patch | Ledger delta | Validation command | Stop condition | Next Founder decision |
|---|---|---|---|---|---|---|---|---|---|
| PORTFOLIO-01-READBACK | Read back all 8 initial Ledger rows and reconcile terminal planning states. | `codex/full-landing-portfolio-readback-20260615` | Portfolio readback packet, optional Ledger delta proposal. | Current Ledger, PR refs, owner readback, blocker evidence. | required | required | YAML parse, diff scope, no forbidden path. | Any row needs factual Ledger change beyond evidence. | Founder / Gate on terminal states. |
| PORTFOLIO-02-LEDGER-CLOSURE | Close or block the initial 8 items with explicit reasons. | `codex/full-landing-ledger-closure-20260615` | Ledger closure proposal and Evidence Bundle. | Evidence for closed, blocked, deferred, or decision-packet states. | required | required | Ledger YAML parse and boundary scan. | Ledger would imply runtime or release. | Approve closure states or revise. |

### Wave 3: PM readiness and supply-side gap packs

| task_id | Goal | Branch | Output files | Evidence requirement | Learning Patch | Ledger delta | Validation command | Stop condition | Next Founder decision |
|---|---|---|---|---|---|---|---|---|---|
| SO-01-PM-READINESS | Prepare `biz.sales.order` PM readiness and Contract Gap list. | `codex/full-landing-sales-order-pm-readiness-20260615` | Sales Order PM readiness packet, Evidence Bundle, Learning Patch. | PM pack index, terminology redlines, provider/payment/billing boundary. | required | required | diff scope, evidence keyword scan. | Any provider/payment/billing integration is implied. | Contract packet if gap requires it. |
| CA-01-PM-READINESS | Prepare `biz.customer.asset` PM readiness and Contract Gap list. | `codex/full-landing-customer-asset-pm-readiness-20260615` | Customer Asset PM readiness packet, Evidence Bundle, Learning Patch. | Asset state gaps and identity/privacy boundary evidence. | required | required | diff scope, evidence keyword scan. | Any live asset or identity/privacy mutation is implied. | Contract packet if gap requires it. |
| OC-01-GAP-PACK | Prepare `biz.offer.catalog` Gateway/OpenAPI/idempotency/approval gap pack. | `codex/full-landing-offer-catalog-gap-pack-20260615` | Offer Catalog gap pack, Evidence Bundle, Learning Patch. | Gateway, OpenAPI, idempotency, approval matrix, Agent/Human split gaps. | required | required | diff scope, evidence keyword scan. | Engineering start from PRD is implied. | Contract or platform packet if needed. |
| SR-01-GAP-PACK | Prepare `biz.store.resource` Gateway/state machine/QRH retry/idempotency gap pack. | `codex/full-landing-store-resource-gap-pack-20260615` | Store Resource gap pack, Evidence Bundle, Learning Patch. | State machine, QRH retry, occupancy risk, Human End gap evidence. | required | required | diff scope, evidence keyword scan. | Live occupancy mutation is implied. | Contract or platform packet if needed. |

### Wave 4: Payment and entitlement boundary closure

| task_id | Goal | Branch | Output files | Evidence requirement | Learning Patch | Ledger delta | Validation command | Stop condition | Next Founder decision |
|---|---|---|---|---|---|---|---|---|---|
| TE-02-CHECK-ONLY-CLOSURE | Close or block Tenant Entitlement check-only after independent verification. | `codex/full-landing-tenant-entitlement-check-only-closure-20260615` | Check-only closure packet, Evidence Bundle, Learning Patch, Ledger delta proposal. | Positive, negative, unknown-context, live-mode hard-stop evidence. | required | required | YAML parse, diff scope, boundary scan. | Mutation behavior appears. | Founder / Gate if upgrading to GATED. |
| PC-01-PREFLIGHT | Prepare Payment Checkout preflight and blocker map. | `codex/full-landing-payment-checkout-preflight-20260615` | Payment preflight packet, Evidence Bundle, Learning Patch. | Provider sovereignty, idempotency, financial audit, refund/settlement blockers. | required | required | diff scope, evidence keyword scan. | Any live money movement is implied. | Founder / Gate before any next step. |

### Wave 5: Cross-repo decision packets only

| task_id | Goal | Branch | Output files | Evidence requirement | Learning Patch | Ledger delta | Validation command | Stop condition | Next Founder decision |
|---|---|---|---|---|---|---|---|---|---|
| CONTRACT-DP-01 | Prepare contract decision packet if Wave 2-4 evidence requires `hl-contracts`. | `codex/full-landing-contract-decision-packet-20260615` | `CONTRACT-DECISION-PACKET-*` in dispatch only. | Exact target files, diff intent, compatibility check, rollback / defer option. | false | false | diff scope confirms dispatch-only. | Any `hl-contracts` edit is attempted. | Founder / Gate contract decision. |
| PLATFORM-DP-01 | Prepare platform decision packet if Wave 2-4 evidence requires `hl-platform`. | `codex/full-landing-platform-decision-packet-20260615` | `PLATFORM-DECISION-PACKET-*` in dispatch only. | Exact target files, fixture plan, gate plan, rollback / defer option. | false | false | diff scope confirms dispatch-only. | Any `hl-platform` edit is attempted. | Founder / Gate platform decision. |
| RELEASE-GATE-DP-01 | Prepare release gate packet only if a release-like claim appears. | `codex/full-landing-release-gate-packet-20260615` | Release Gate decision packet in dispatch only. | Claim source, evidence gap, explicit no-release state until decision. | false | false | forbidden claim scan and diff scope. | Packet implies release approval. | Founder release decision, if requested. |

### Wave 6: Operating mechanism closure

| task_id | Goal | Branch | Output files | Evidence requirement | Learning Patch | Ledger delta | Validation command | Stop condition | Next Founder decision |
|---|---|---|---|---|---|---|---|---|---|
| WEEKLY-01 | Establish weekly evidence and Learning Patch review. | `codex/full-landing-weekly-review-20260615` | Weekly review packet. | Changed states, GATED evidence gaps, failure path gaps, blockers, Learning Patch list. | required | false | diff scope, keyword scan. | Review creates busywork without decisions. | Confirm cadence or revise. |
| METRICS-30 | Prepare Day-30 mechanism integrity metrics. | `codex/full-landing-metrics-30-20260615` | Metrics 30 packet. | Ledger coverage, `not_authorized` coverage, GATED bypass, Learning Patch rate, generated-only ratio. | required | false | diff scope, metric field scan. | Metrics cannot be evidenced. | Founder metrics review. |
| METRICS-60-90 | Prepare Day-60/90 trend metrics. | `codex/full-landing-metrics-60-90-20260615` | Metrics 60/90 packet. | Lead time, blocker wait, rework, independent evidence, failure path coverage, overhead. | required | false | diff scope, metric field scan. | Trend inputs missing. | Founder metrics review. |
| RULE-THINNING-01 | Remove or defer rules that do not affect decisions. | `codex/full-landing-rule-thinning-20260615` | Rule thinning proposal. | Two-review inactivity, duplication, reporting-over-action, DRI wait evidence. | required | false | diff scope, rule change routing check. | Rule change touches contracts/platform. | Founder / Gate if rule changes leave dispatch. |
| RISK-CLASS-01 | Revisit whether REVERSIBLE / GATED is too coarse. | `codex/full-landing-risk-class-evolution-20260615` | Risk-class evolution proposal. | Evidence that two-level model caused ambiguity or over-ritual. | required | false | diff scope, rule keyword scan. | New class lacks evidence. | Founder / Gate rule decision. |
| DISCOVERY-01 | Run product discovery and value judgment loop. | `codex/full-landing-discovery-loop-20260615` | Discovery / value readback packet. | DRI slot value, observable user/system value, defer/candidate rationale. | required | false | diff scope, decision boundary scan. | Delivery pressure substitutes for value judgment. | Founder discovery decision. |

## 9. Evidence Bundle and Learning Patch requirement

Every executable task in Waves 1 through 4 and Wave 6 requires:

1. Evidence Bundle.
2. Learning Patch.
3. Ledger delta proposal when a Ledger row changes.
4. Independent verification for GATED progression.
5. Failure path for GATED progression.
6. Explicit `not_authorized` boundary.

Evidence Bundle is a judgment accelerator, not a compliance checklist. It should
make the next decision faster by preserving source refs, verification method,
failure path, open risks, and rollback or exit path.

Learning Patch must convert repeated human judgment into a future rule,
template, gate, agent instruction, defer rationale, or decision-packet routing.

## 10. Ledger update requirement

Ledger changes are not part of this planning PR. Future Ledger deltas must:

1. be scoped to the task branch;
2. parse as YAML;
3. keep every row non-authorizing;
4. preserve `not_authorized`;
5. keep SSOT references as references, not copied contracts;
6. never imply production, release, MVP, active contract, runtime, or live
   business authorization.

## 11. Cross-repo decision packet routing

No `hl-contracts` or `hl-platform` implementation is authorized by this plan.

Allowed future dispatch outputs:

- `CONTRACT-DECISION-PACKET-*`
- `PLATFORM-DECISION-PACKET-*`
- `RELEASE-GATE-DECISION-PACKET-*`, only if a release-like claim appears

Each decision packet must include target files, intent, compatibility impact,
rollback or defer option, evidence refs, owner, and the specific Founder / Gate
decision requested. A decision packet is not an implementation.

## 12. Discovery / value judgment loop

Full landing must include upstream product judgment:

| Question | Output |
|---|---|
| Which capability deserves a DRI slot? | DRI slot proposal with evidence and reason. |
| What user or system value is observable? | Value readback with measurable evidence or reason for deferral. |
| Which candidate or deferred items stay out of active delivery? | Defer list with reason and re-entry trigger. |
| Where is the Founder decision boundary? | Discovery decision boundary, distinct from downstream risk acceptance. |

The discovery loop prevents the operating model from becoming risk-control only.
If value is unclear, the item should return to SPEC_ONLY, defer, or request a
Founder product decision rather than expanding delivery ritual.

## 13. Weekly operating review cadence

Weekly review should cover:

1. Ledger rows changed since the prior review.
2. GATED items still relying on generated-only evidence.
3. Items missing failure path evidence.
4. Blockers requiring Founder / Gate decision.
5. Evidence Bundle quality.
6. Learning Patch outcomes.
7. Rule-thinning candidates.
8. Discovery / value decisions still open.

WIP limit:

- no more than 2 active execution PRs;
- no more than 1 review / readback PR;
- no more than 1 conditional decision-packet PR unless Founder confirms.

GATED items require independent evidence, but they should not require repeated
Founder handholding once the decision boundary and failure path are clear.
REVERSIBLE or check-only items should not inherit full GATED ritual unless they
touch formal facts, live state, money, entitlement, identity, privacy, contract,
or production data.

## 14. 30/60/90 metrics

Day 30 mechanism metrics:

| Metric | Target |
|---|---|
| Ledger coverage for active / PM-led / pilot items | 100 percent |
| DRI present or `TBD_FOUNDER_DECISION` | 100 percent |
| `not_authorized` present | 100 percent |
| Draft / staging / manifest / readiness misread | 0 |
| GATED item bypassing Gateway / Can path | 0 |
| State progression with Learning Patch | 100 percent |
| Generated-only evidence completing GATED progression | 0 |

Day 60/90 trend metrics:

| Metric | Desired direction |
|---|---|
| lead time | down |
| blocker wait time | down |
| generated-only evidence ratio | down |
| independent evidence coverage | up |
| failure path coverage | up |
| reversible autonomous movement | up |
| process overhead | down or justified |

## 15. Risk and controls

| Risk | Control |
|---|---|
| Dispatch docs are misread as runtime or release authorization. | Repeat non-authorization boundary in every task and PR body. |
| Founder becomes validation bottleneck. | Use DRI pull model, WIP limit, Evidence Bundle, and Learning Patch. |
| GATED work advances on generated-only evidence. | Require independent verification and failure path before progression. |
| Cross-repo implementation leaks into planning. | Route as decision packet only; diff scope check blocks `hl-contracts` and `hl-platform`. |
| REVERSIBLE / GATED is too coarse. | Track ambiguity and revisit in Wave 6 only with evidence. |
| Discovery is skipped under delivery pressure. | Wave 6 discovery loop must identify value, DRI slot, defer list, and Founder boundary. |

## 16. Founder decisions required before Wave 1 execution

Wave 1 execution is not authorized by this PR. Founder must separately decide:

1. approve or revise this full landing plan;
2. authorize `GO_WAVE_1_BF_CLOSEOUT_CREATE_PRS_ONLY`;
3. confirm one task / one branch / one PR policy;
4. decide whether BF-04, BF-05, and BF-06 may run sequentially without returning
   for separate approval after each PR, or whether each requires separate
   Founder approval;
5. confirm no `hl-contracts` or `hl-platform` implementation yet;
6. confirm Wave 1 and Wave 2 owner assignment policy;
7. confirm discovery / value loop owner;
8. confirm metrics owner;
9. confirm whether REVERSIBLE / GATED remains the only risk class until metrics review.

## 17. Validation commands

Planning PR validation:

```bash
git status --short --branch
git diff --stat
git diff -- docs/delivery-recovery/HL-CAPABILITY-FULL-LANDING-EXECUTION-PLAN-v0.1-2026-06-15.md
git diff -- docs/delivery-recovery/HL-CAPABILITY-FULL-LANDING-TASK-LEDGER-v0.1-2026-06-15.yaml
git diff -- docs/delivery-recovery/HL-CAPABILITY-FULL-LANDING-FOUNDER-DECISION-PACKET-v0.1-2026-06-15.md
ruby -e 'require "yaml"; YAML.load_file("docs/delivery-recovery/HL-CAPABILITY-FULL-LANDING-TASK-LEDGER-v0.1-2026-06-15.yaml"); puts "YAML_OK"'
rg -n "production_authorized|MVP|release authorized|runtime authorization|live payment|live billing|live entitlement deduction|active contract" docs/delivery-recovery/HL-CAPABILITY-FULL-LANDING-EXECUTION-PLAN-v0.1-2026-06-15.md docs/delivery-recovery/HL-CAPABILITY-FULL-LANDING-TASK-LEDGER-v0.1-2026-06-15.yaml docs/delivery-recovery/HL-CAPABILITY-FULL-LANDING-FOUNDER-DECISION-PACKET-v0.1-2026-06-15.md || true
git diff --name-only | grep -E '^(../)?(hl-contracts|hl-platform)/' && exit 1 || true
git diff --name-only | grep -v '^docs/delivery-recovery/' && exit 1 || true
```

## 18. Final stop and next action

This PR must stop after creating the planning PR. Do not merge it.

Next required action after PR review:

- Founder approves `GO_WAVE_1_BF_CLOSEOUT_CREATE_PRS_ONLY`; or
- Founder requests plan revision; or
- Founder changes wave order, WIP limit, owner assignment, discovery loop, or
  risk-class policy.

