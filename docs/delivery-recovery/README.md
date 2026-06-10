# Delivery Recovery Docs

Delivery Recovery Mode v0.1 is a 14-30 day recovery mode. It is not the permanent unique delivery process.

The unique implementation contract is `DELIVERY_RECOVERY_IMPLEMENTATION_CONTRACT_v0.1.md`. Other files in this directory and the GitHub templates are execution projections of that contract.

## Main Flow

Mission Package -> Delivery Slice / Risk-Retirement Slice -> Work Unit -> Context Pack -> AI / Human Execution -> PR / Test / Review -> Evidence Resolver -> Task Snapshot -> Action Projection -> Acceptance -> Close / Iterate / Archive.

Use Delivery Slice for planned delivery. Use Risk-Retirement Slice for Red Path risk removal, architecture spikes, provider blockers, secret blockers, or other unblock work.

## Source Of Truth

- GitHub Issues, PRs, and repository files are the evidence source.
- Bitable, Project, Feishu, dashboards, and chat summaries are projections.
- Do not build a full task platform before recovery work starts.
- No action item means no Feishu notification and no public status comment refresh.

## Required Files

- `DELIVERY_RECOVERY_IMPLEMENTATION_CONTRACT_v0.1.md`: canonical implementation contract.
- `DELIVERY_RECOVERY_MODE_v0.1.md`: recovery mode scope, gates, flow, and exceptions.
- `AI_OUTPUT_CONTRACT_v1.md`: `ai-output:v1` output contract.
- `TASK_SNAPSHOT_v1.md`: `task-snapshot:v1` current-card contract.
- `RISK_PATH_GREEN_YELLOW_RED.md`: Green / Yellow / Red risk path and governance budget.

## Recovery Artifacts

- `DS-3_FORMAL_OBJECT_CHAIN_SNAPSHOT_2026-06-08.md`: Formal object chain evidence snapshot for Sales, CustomerAsset, ServiceOrder, and PaymentCheckout.
- `DS-3_FORMAL_OBJECT_CHAIN_SNAPSHOT_REFRESH_2026-06-10.md`: Current DS-3 post-merge readback. SalesOrder, CustomerAsset, ServiceOrder, and PaymentCheckout are merged only as `hl-contracts` candidate-only draft materials; DS-2 Tenant Entitlement is completed only as a check-only pilot. This does not authorize active contract, HPRD, design.md, runtime, real payment provider, real billing, real refund, real settlement, or production.
- `DS-4_FORMAL_OBJECT_CHAIN_READ_PATH_2026-06-10.md`: Current DS-4 read path evidence and acceptance report. Candidate A was selected and completed as a sandbox / embedded CLI evidence resolver via `hl-contracts#113` and `hl-platform#131`. This does not authorize active contract, HPRD, design.md, formal runtime, real payment provider, real billing, real refund, real settlement, customer asset deduction, service fulfillment, business object creation, workflow change, or production.
- `DS-5_FORMAL_OBJECT_CHAIN_NEXT_DECISION_REQUEST_2026-06-10.md`: Current DS-5 decision request after DS-4. Default recommendation is to accept DS-4 as check-only evidence only; any active registry, HPRD, design.md, formal runtime, provider, payment, billing, refund, settlement, asset deduction, service fulfillment, production, deploy, release, secrets, workflow, or real user data expansion requires a separate Founder / Gate GitHub SSOT decision.
- `DS-6_FORMAL_OBJECT_CHAIN_DECISION_INTAKE_2026-06-10.md`: Current DS-6 decision intake / acceptance readback. No separate Founder / Gate GitHub SSOT selecting DS-5 Option B, Option C, or a prereq-satisfied Option D was found, so DS-4 remains accepted only as check-only evidence and DS-5 remains the next-track decision request.
- `DS-7_FORMAL_OBJECT_CHAIN_OPTION_B_DECISION_2026-06-10.md`: Founder / Gate GitHub SSOT decision selecting DS-5 Option B for DS-7 `hl-contracts` docs-only activation readiness planning. This does not authorize active registry write, HPRD, design.md, formal runtime, provider, payment, billing, refund, settlement, asset deduction, service fulfillment, production, deploy/release, workflow, secrets, or real user data.
- `DS-7_FORMAL_OBJECT_CHAIN_ACTIVATION_READINESS_2026-06-10.md`: Current DS-7 acceptance readback. `hl-contracts#114` completed docs-only activation readiness planning with deterministic tests after `hl-dispatch#211` selected Option B. This does not authorize active registry write, HPRD, design.md, formal runtime, provider, payment, billing, refund, settlement, asset deduction, service fulfillment, production, deploy/release, workflow, secrets, or real user data.

## Public Updates

Public backfill comments must use one of these classes:

- `status_update`
- `gap_report`
- `decision_request`
- `acceptance_report`

No Structured Update, No Public Status Comment. Exceptions are PR review, CI failure, security incident, P0 incident, and blocker unblock.

## Recovery Rules

- No Package, No Planned Work.
- No Slice, No Delivery Plan.
- No Evidence, No Done.
- No Context, No AI Guess.
