# Capability Review Issue Body 2026-06-07

Use this file to create a new independent GitHub Review Issue. Do not post this long body into `#173`.

## Issue Metadata

Title:

`[Mission Package Review] Capability package integration baseline 2026-06-07`

Labels:

- `type:review`
- `state:snapshot`
- `package:capability-integration`
- `no-feishu-broadcast`
- `no-daily-ledger`

## Body

### Review Objective

This issue reviews the capability package integration baseline for Delivery Recovery Mode v0.1.

The goal is not to start another governance ledger. The goal is to put current capability packages into the recovery flow:

Mission Package -> Delivery Slice / Risk-Retirement Slice -> Work Unit -> Context Pack -> PR / Test / Review -> Evidence -> Task Snapshot -> Action Projection -> Acceptance.

### Recovery Boundary

- Delivery Recovery Mode v0.1 is a 14-30 day recovery mode, not a permanent unique process.
- GitHub is the evidence source.
- Bitable / Project / Feishu are projections.
- No full task platform is authorized.
- No legacy long ledger comment stream is authorized.
- No action item means no Feishu broadcast and no public status refresh.

### Main Value Stream

Natural interaction intent
-> `intent_candidate`
-> AI draft
-> human confirmation / signature
-> formal booking / sales / service object
-> payment / asset / fulfillment linkage
-> audit evidence

### Global Red Lines

- Use `手艺人` and `服务人员`.
- Do not write back `美疗师` or `美容师`.
- Do not assume one room, one bed, one person.
- AI can draft, suggest, execute, audit, compress context, and report gaps.
- AI cannot confirm, sign, reject, approve, create formal business objects, or replace human acceptance.
- GitHub Issue / PR / comment is the task and decision evidence chain.
- Feishu is projection only.

### Current Capability Snapshot

| Package | Lane | Current Status | Required Next Action | Evidence Exit |
| --- | --- | --- | --- | --- |
| P0.5-A `biz.intent.capture` | waiting_hprd_draft | candidate only | Draft HPRD candidate and confirmation boundary | HPRD draft / gap report |
| P0.5-B `biz.ai.draft.confirmation` | waiting_hprd_draft | candidate only | Define AI draft -> human confirmation contract | HPRD draft / decision record |
| P0.5-C 横切依赖 / cross-cutting dependencies | waiting_owner_action | dependency map needed | Map only dependencies needed by active slices | dependency map / blocker list |
| `biz.customer.asset` | P1 formal object chain | adjacent boundary unresolved | Contract Gap decision | decision record |
| `biz.sales.order` | P1 formal object chain | terminology red line pending | Replace forbidden service-role terms with `手艺人` / `服务人员` | Draft PR update / review evidence |
| `biz.service.order` | P1 formal object chain | Draft PR / blocker expected | Produce Draft PR, blocker, or ETA revision | PR / blocker / ETA update |
| `biz.payment.checkout` | P1 formal object chain | preflight pending | PM preflight or blocker | preflight report / blocker |
| `biz.tenant.entitlement` | P2 thin engineering slice | check-only candidate | DS-2 quota check-only, mock / seed data, 3 cases | PR + tests + demo response |
| Booking staging pilot | P0 closeout | staging evidence accepted, closeout unresolved | Close out `hl-platform#106`: merge, split, or close superseded | PR / integration test / acceptance report |
| Supply / Resource | dependency / risk-retirement | blocker mapping needed | Identify only blockers for booking / service / asset | blocker closeout / decision record |
| CustomerProfile | dependency candidate | boundary unclear | Clarify with customer asset and identity | HPRD draft / decision record |
| HK 横切契约 / cross-cutting contracts | platform dependency | drift-sensitive | Keep registry / reason code / event taxonomy aligned | gate output / contract drift report |

### Waiting Queues

`waiting_owner_action`:
- Booking closeout / readiness decision.
- `biz.customer.asset` adjacent boundary and Contract Gap decision.
- `biz.sales.order` terminology red line fix.
- P0.5-C dependency mapping.
- Supply / Resource blocker mapping.
- HK cross-cutting contract drift handling.

`waiting_pm_eta`:
- `biz.service.order` Draft PR / blocker / ETA revision.
- `biz.payment.checkout` preflight / blocker.

`waiting_hprd_draft`:
- P0.5-A `biz.intent.capture`.
- P0.5-B `biz.ai.draft.confirmation`.
- CustomerProfile boundary.

### Candidate Queue

`candidate_queue`:

Candidate only, not active delivery:

- `biz.aftersale.case`
- `biz.promotion.discount`
- `biz.performance.commission`

Deferred:

- `biz.invoice.tax`
- `biz.payment.channel.settlement`

### Maturity Model

| Level | Name | Meaning |
| --- | --- | --- |
| M0 | observation_candidate | Observed candidate |
| M1 | session_candidate_locked | Session candidate locked |
| M2 | draft_candidate_baseline | Draft candidate baseline |
| M3 | hprd_understanding_confirmed | HPRD understanding confirmed |
| M4 | contract_draft_pr | Contract Draft PR |
| M5 | active_contract_baseline | Contract merged baseline |
| M6 | runtime_candidate | Runtime candidate |
| M7 | staging_evidence_accepted | Staging evidence accepted |
| M8 | internal_mvp_accepted | Internal MVP accepted |
| M9 | production_authorized | Production authorized |

### Forbidden Misreads

- Checks SUCCESS is not ready.
- Draft PR is not active contract.
- HPRD draft is not runtime authorization.
- Staging accepted is not PR merged or production.
- Feishu done is not GitHub done.
- AI draft is not a formal business object.
- Founder dispatch accepted is not engineering start allowed.
- Booking staging pilot is not MVP / production / merged.
- Tenant entitlement check-only is not production runtime.

### Review Questions

1. Is the current active set limited to Booking closeout, formal object chain stabilization, and Tenant entitlement check-only?
2. Are aftersale, promotion, and performance kept out of active delivery?
3. Is each active package attached to a Mission Package, Delivery Slice / Risk-Retirement Slice, or Work Unit?
4. Are all completion claims backed by GitHub PR / test / decision / acceptance evidence?

### Decision Requested

Approve this baseline as the current capability integration snapshot for Delivery Recovery Mode v0.1, or return one concrete correction.

### #173 Pointer

If a pointer is needed in `#173`, post only:

`当前能力包整合快照见 <新 Review Issue 链接>。`
