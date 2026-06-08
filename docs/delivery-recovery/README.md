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
