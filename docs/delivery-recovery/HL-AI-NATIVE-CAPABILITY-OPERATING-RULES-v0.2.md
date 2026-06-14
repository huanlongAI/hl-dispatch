# HL AI-Native Capability Operating Rules v0.2

> Status: OPERATING_RULES_DRAFT_FOR_LANDING
> Date: 2026-06-14
> Owner: Founder / hl-dispatch operating layer
> Scope: capability dispatch, readiness tracking, evidence discipline, and execution-state governance
> Boundary: This document does not authorize runtime, production release, schema changes, registry changes, HPRD start, or live business-data integration.
> Review-first / Founder decision required: any move from dispatch docs into contracts, runtime, schema, registry, manifest, config, release, or live business operation is not authorized here and requires a separate Founder / Gate decision.

## 1. Purpose

This rule set defines how Huanlong capability packages move from planning language to reviewable execution without confusing drafts, staging evidence, pilot manifests, or PM readiness with runtime or release authorization.

The operating goal is not to add heavy governance. The operating goal is to raise judgment capacity by:

1. letting a Capability DRI advance low-risk work by default;
2. forcing GATED work to surface missing Gateway, Human End, Agent End, evidence, and audit paths early;
3. preventing AI-generated work from self-certifying;
4. capturing every useful lesson back into rules, templates, agent prompts, gates, or defer decisions.

## 2. Source-of-Truth Boundaries

| Layer | Repository | Authority | This document may do |
|---|---|---|---|
| Contract SSOT | `hl-contracts` | capability registry, rules, reason_code, OpenAPI, events, facts, PM capability specs | reference only |
| Dispatch / recovery | `hl-dispatch` | taskbooks, recovery snapshots, operating rules, readiness ledger, decision logs | create and update docs |
| Runtime | `hl-platform` | runtime implementation, module manifests, readiness gate, handlers, fixtures | reference only |

No file in `hl-dispatch` may become a new SSOT for `hl-contracts` or `hl-platform`.

## 3. Non-Authorization Boundary

The following do not authorize runtime or release:

1. DRAFT Cap-Spec.
2. PM readiness pack.
3. checks success.
4. staging evidence.
5. pilot manifest.
6. runtime candidate manifest.
7. Ledger entry.
8. Evidence Bundle index.
9. Founder discussion in chat.
10. AI audit report.

Runtime, release, schema, registry, taxonomy, payment, billing, entitlement, customer identity, privacy, contract, and production data changes require their own explicit Gate / Founder authorization through the appropriate repository evidence chain.

## 4. Core Terms

| Term | Definition |
|---|---|
| Capability DRI | Directly responsible individual for moving one capability item through Card, Evidence, Ledger, and next-state proposal. DRI does not own runtime authorization. |
| DRI Pull Model | Default execution model where DRI advances the item and pulls PM/Gate/Founder only when a trigger is met. |
| Readiness Ledger | Single dispatch-side YAML table that records execution state, risk class, blockers, missing evidence, and next action. It references SSOT; it does not copy SSOT. |
| Evidence Bundle | Index of evidence proving readiness or blockage. For GATED progression it must include independent verification and a failure path. |
| Learning Patch | Required patch after state progression that updates rules, templates, agent prompts, gates, taxonomy proposals, or defer rationale. |

## 5. DRI Pull Model

### 5.1 Default Rule

A Capability DRI owns forward movement of the capability item through:

1. Capability Execution Card.
2. Evidence Bundle.
3. Readiness Ledger update.
4. next-action proposal.
5. Learning Patch.

### 5.2 What DRI Does Not Own

DRI does not own:

1. runtime authorization;
2. production release authorization;
3. `hl-contracts` schema or registry modification;
4. `hl-platform` runtime or manifest modification;
5. Gate H or Founder approval;
6. financial, identity, privacy, contract, or live entitlement decisions.

### 5.3 Pull Triggers

DRI must pull PM, Gate Owner, Engineering Owner, or Founder when any of the following occurs:

| Trigger | Required escalation |
|---|---|
| Formal fact mutation | Gate Owner |
| Resource occupancy mutation | Gate Owner |
| Payment, refund, billing, settlement, entitlement, customer identity, privacy, contract, or live data touch | Gate Owner + Founder if necessary |
| Gateway / Can path missing | Gate Owner |
| Human End missing | PM + Gate Owner |
| Agent manifest missing | Gate Owner |
| idempotency / retry unclear | Gate Owner |
| reason trace / event / fact / audit evidence unclear | PM + Gate Owner |
| DRI confidence low | relevant owner |
| owner conflict unresolved within SLA | fail-secure or defer |

## 6. Risk Class

Only two execution-layer risk classes are used in v0.2.

| risk_class | Definition | Default path |
|---|---|---|
| REVERSIBLE | Does not create or mutate formal business facts, live resource occupancy, money, billing, entitlement, customer identity, privacy, contract, or production data; can be rolled back or discarded. | DRI may advance with evidence. |
| GATED | Mutates or may mutate formal facts, live resource occupancy, money, billing, entitlement, identity, privacy, contract, production data, or bypass-sensitive runtime paths; or is hard to reverse. | Must surface Gate / Human / Founder / independent evidence before advancement. |

If unclear, classify as GATED.

This field does not replace `risk_level` in `hl-contracts`. It is an execution escalation layer only.

## 7. Execution State

| execution_state | Meaning | Allowed work | Not allowed |
|---|---|---|---|
| SPEC_ONLY | Planning, PM spec, gap analysis, readiness clarification only. | Cap-Spec review, Contract Gap, reason proposal, scope definition. | runtime implementation, live object mutation, release claim. |
| THIN_SLICE | Controlled mock/seed/demo/staging/check-only slice. | fixtures, manifest review, check-only evidence, Gateway path exploration. | live business operation or release claim. |
| RELEASE_CANDIDATE | Evidence approaches release review completeness. | release/security/product evidence assembly, rollback plan, Gate H review. | release without explicit authorization. |

Execution state does not replace M0-M9 maturity. Ledger must record both.

## 8. Capability Execution Card

Each active Ledger item must be representable as a Card with:

- `capability_id`
- `dri`
- `lane`
- `maturity`
- `execution_state`
- `risk_class`
- `scope_in`
- `scope_out`
- `not_authorized`
- `contract_gap_p0p1`
- `gateway_can_path`
- `human_end`
- `agent_manifest`
- `idempotency_retry`
- `reason_trace`
- `events_facts_audit`
- `evidence_mode`
- `next_action`
- `learning_patch_required`

## 9. Readiness Ledger Rules

1. Ledger is a status surface, not a registry.
2. Ledger references SSOT paths; it does not copy full contracts, key_action definitions, reason_code definitions, OpenAPI, events, or facts.
3. Every active, PM-led, or pilot closeout item must have a Ledger row.
4. Unknown owner fields must use `TBD_FOUNDER_DECISION`, not invented names.
5. Any Ledger item without `not_authorized` is invalid.
6. Any GATED item without Gateway / Can path evidence is blocked or partial.
7. Any GATED item with generated-only evidence cannot advance.

## 10. Evidence Bundle Standard

Evidence Bundle is an evidence index. It does not replace acceptance manifest, readiness gate, release evidence, or Gate H.

For any GATED advancement, Evidence Bundle must include:

1. independent verifier;
2. verification method;
3. happy path evidence;
4. failure path evidence;
5. open risk list;
6. rollback or exit path;
7. gate decision state;
8. linked SSOT / repo / issue / PR evidence.

Generated-only evidence may be accepted as draft input but cannot certify GATED progression.

## 11. Learning Patch Rule

After any state progression, DRI must produce a Learning Patch.

| patch_type | Default repository | Separate Founder decision needed? |
|---|---|---|
| RULE_PATCH | `hl-dispatch` | no, if dispatch-only |
| TEMPLATE_PATCH | `hl-dispatch` | no, if dispatch-only |
| AGENT_PROMPT_PATCH | depends on prompt location | yes if outside dispatch |
| GATE_PATCH | `hl-platform` | yes |
| TAXONOMY_PATCH | `hl-contracts` | yes |
| DEFER_PATCH | `hl-dispatch` | no, if dispatch-only |

No Learning Patch means the progression is incomplete.

## 12. Conflict Resolution

| Conflict | Rule |
|---|---|
| PM says ready, Gate says Gateway / Can path unclear | Gate may veto; record Contract Gap. |
| DRI says REVERSIBLE, Gate says GATED | Treat as GATED until evidence proves reversibility. |
| Founder concern about detail | Convert to rule, `not_authorized`, acceptance criterion, or risk trigger. |
| Owners cannot agree within SLA | fail-secure or defer. |
| Business value unclear but implementation pressure exists | return to SPEC_ONLY or cancel. |

## 13. Founder Behavior Discipline

Founder must not become the default validation bottleneck.

Founder participates in:

1. product doctrine;
2. priority and scope cuts;
3. irreversible or high-impact risk acceptance;
4. final rule changes;
5. explicit Gate escalation.

Founder concerns about REVERSIBLE details must be converted into:

1. Product Doctrine;
2. `not_authorized`;
3. acceptance criteria;
4. risk trigger;
5. Gate rule;
6. defer rationale.

Founder should not take over DRI work for ordinary reversible details.

## 14. Initial Portfolio Policy

| Item | v0.2 policy |
|---|---|
| Booking staging pilot / `hl-platform#106` | closeout only; no release claim without live evidence. |
| `biz.booking.fulfillment` | THIN_SLICE / GATED; patch Human End, Agent manifest, owner matrix, retry policy. |
| `biz.sales.order` | SPEC_ONLY / GATED; PM readiness only. |
| `biz.customer.asset` | SPEC_ONLY / GATED; PM readiness and Contract Gap decision only. |
| `biz.offer.catalog` | SPEC_ONLY / GATED; patch Gateway/OpenAPI/idempotency/approval matrix before engineering. |
| `biz.store.resource` | SPEC_ONLY / GATED; patch Gateway/state machine/retry/idempotency before engineering. |
| `biz.tenant.entitlement` | THIN_SLICE; check-only mock/seed/demo unless later authorized. |
| `biz.payment.checkout` | SPEC_ONLY / GATED; preflight/blocker only. |
| `biz.customer.profile` | dependency candidate / Founder-Gate contract phase only; not active runtime workstream in this cycle. |

## 15. Do-Not-Do List

Do not:

1. treat DRAFT as active contract;
2. treat checks success as readiness;
3. treat staging evidence as release;
4. treat pilot manifest as production authorization;
5. let Agent bypass Gateway / HK Kernel / Can -> Action -> Audit;
6. start runtime from PM readiness alone;
7. connect live payment, billing, entitlement, identity, privacy, contract, or production data without explicit authorization;
8. copy `hl-contracts` SSOT into Ledger;
9. use generated-only evidence to advance GATED work;
10. expand candidate/deferred packages into active delivery without Founder decision.

## 16. Metrics

### 16.1 First 30 Days: Mechanism Metrics

| Metric | Target |
|---|---|
| Ledger coverage for active / PM-led / pilot items | 100% |
| DRI field present or explicitly `TBD_FOUNDER_DECISION` | 100% |
| `not_authorized` present | 100% |
| draft/staging/manifest/readiness misread | 0 |
| GATED item bypassing Gateway / Can path | 0 |
| state progression with Learning Patch | 100% |

### 16.2 Day 60-90: Trend Metrics

| Metric | Desired direction |
|---|---|
| lead time | down |
| blocker wait time | down |
| generated-only evidence ratio | down |
| independent evidence coverage | up |
| failure fixture coverage | up |
| reversible autonomous movement | up |
| unauthorized runtime claim | 0 |

## 17. Revision Rule

v0.2 must remain thin. Any new field, role, or gate must earn its place by fixing a repeated failure or risk that cannot be handled by existing fields.
