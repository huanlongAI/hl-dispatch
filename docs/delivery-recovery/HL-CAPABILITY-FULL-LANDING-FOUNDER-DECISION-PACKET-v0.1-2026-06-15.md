# HL Capability Full Landing Founder Decision Packet v0.1

Status: DRAFT_FOR_FOUNDER_REVIEW
Date: 2026-06-15
Scope: decisions required after the full landing execution plan PR is reviewed

## Decision brief

This packet asks Founder to review the full landing execution plan and decide
whether Wave 1 may start after the plan PR is merged. The plan PR itself does
not authorize BF-04, BF-05, BF-06, BF-07, `hl-contracts`, `hl-platform`,
runtime, production, release, MVP, active contract, live booking, live payment,
live billing, entitlement mutation, quota mutation, identity mutation, privacy
mutation, or formal business object mutation.

## Current anchor

- PR #269 is merged.
- Merge commit: `f923c99cddcd68ae955d13f4d3648aebe718d9a3`.
- Current Ledger next due for `biz.booking.fulfillment`: `BF-04-OVERRIDE-RETRY_PR`.
- This packet is prepared from a clean `hl-dispatch` worktree based on `origin/main`.

## Options

### Option A: GO_WAVE_1_BF_CLOSEOUT_CREATE_PRS_ONLY

Approve the full landing plan PR and authorize Wave 1 after merge:

1. BF-04 Override / Retry.
2. BF-05 Dependency Exit.
3. BF-06 Readiness Rollup.
4. BF-07 Founder / Gate Decision Packet only if BF-06 evidence supports it.

Boundary: create PRs only. No merge without later approval. No runtime or
cross-repo implementation.

### Option B: DO_NOT_EXECUTE_REVISE_PLAN

Do not start Wave 1. Revise the plan PR first.

Use this if the wave model, owner policy, WIP limit, discovery loop, or
decision-packet boundary is wrong.

### Option C: CHANGE_WAVE_ORDER

Approve the plan concept but change the order before execution.

Common alternatives:

- Run Portfolio Readback before BF-04.
- Run Tenant Entitlement check-only closure before Payment preflight.
- Run discovery/value loop before any more closeout PRs.

### Option D: CONFIRM_OR_CHANGE_WIP_LIMIT

Current recommended WIP limit:

- no more than 2 active execution PRs;
- no more than 1 review / readback PR;
- no more than 1 conditional decision-packet PR unless Founder confirms.

Founder may confirm or change this.

### Option E: CONFIRM_OR_CHANGE_OWNER_ASSIGNMENT_POLICY

Current owner policy:

- Wave 1: PM-A / Zou Cong + Gate-H / Xu Jiuming.
- Wave 2: Dispatch / Codex prepares readback; Founder / Gate reviews.
- Wave 3: PM-A owns `biz.sales.order`; PM-B / Zhu Yang owns `biz.customer.asset`,
  `biz.offer.catalog`, and `biz.store.resource`.
- Wave 4: Gate-H owns Tenant Entitlement check-only closure; PM-B owns Payment
  Checkout preflight.
- Wave 5: owning PM + Gate-H prepare contract packet; Gate-H + Engineering
  owner prepare platform packet.
- Wave 6: owner slots remain `TBD_FOUNDER_DECISION` where not yet assigned.

Founder may confirm, replace owners, or require owner readback first.

### Option F: CONFIRM_OR_CHANGE_DISCOVERY_LOOP_POLICY

Current discovery policy:

- Discovery is separate from downstream risk acceptance.
- A capability deserves a DRI slot only when value is observable or Founder
  explicitly chooses the bet.
- Candidate or deferred items remain out of active delivery until re-entry
  criteria are met.
- Founder decision at discovery selects product value and priority, not runtime
  risk acceptance.

Founder may confirm this loop, assign an owner, or move it before Wave 1.

### Option G: CONFIRM_OR_CHANGE_RISK_CLASS_POLICY

Current policy keeps two execution risk classes until metrics review:

- REVERSIBLE.
- GATED.

Founder may keep the two-level model until Day-30 metrics, or request a
separate risk-class evolution packet before Wave 1.

## Recommended option

Recommended: approve Option A with Options D, E, F, and G confirmed as written.

Reason: BF-04 is already the current Ledger next due, BF-01 through BF-03 are
landed, and Wave 1 is the smallest coherent closeout cluster for
`biz.booking.fulfillment`. The plan still blocks runtime, contracts, production,
release, and live operation.

## Minimum Founder reply format

Use one of:

```text
APPROVE_PLAN_AND_GO_WAVE_1_CREATE_PRS_ONLY
```

```text
REVISE_PLAN: <specific required changes>
```

```text
CHANGE_WAVE_ORDER: <new order>
```

```text
CHANGE_WIP_LIMIT: <new limit>
```

```text
CHANGE_OWNER_POLICY: <owner changes>
```

```text
CHANGE_DISCOVERY_LOOP: <policy or owner changes>
```

```text
CHANGE_RISK_CLASS_POLICY: <policy changes>
```

## Explicit non-authorization

Approving this packet may authorize planning or create-PR-only execution
depending on the option selected. It does not authorize:

1. `hl-contracts` implementation.
2. `hl-platform` implementation.
3. Runtime code.
4. Schema, registry, manifest, config, OpenAPI, events, facts, or reasoncodes
   mutation.
5. Production, release, MVP, active contract, or runtime authorization.
6. Live booking operation.
7. Live payment, refund, settlement, or billing.
8. Entitlement deduction or quota mutation.
9. Customer identity or privacy mutation.
10. Formal business object mutation.

