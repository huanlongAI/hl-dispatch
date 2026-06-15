# Biz Booking Fulfillment Contract Change Plan Only v0.1

Status: CONTRACT_CHANGE_PLAN_ONLY_READY_FOR_REVIEW
Date: 2026-06-15
Capability: `biz.booking.fulfillment`
Target repo: `hl-contracts`

## 中文摘要

本文是 `biz.booking.fulfillment` 的 contract change plan only。它把
BF-01 到 BF-06 的 docs-only closeout 证据转换成未来可能进入
`hl-contracts` 的候选变更计划：目标文件、变更意图、兼容性影响、验证底线和
停止条件。本文不修改 contract SSOT，不新增 OpenAPI、events、facts、
reasoncodes，也不授权 runtime 或生产。

## 术语说明

- contract change plan only：契约变更计划，仅说明未来可能改什么和为什么。
- exact file subset：精确文件子集，未来若进入 `hl-contracts` PR 必须再次裁决。
- additive metadata：附加说明或元数据，不删除既有接口语义。
- compatibility impact：兼容性影响；本计划阶段只做预评估。

## Decision Anchor

Founder / Gate readback:

- `ACCEPT_DOCS_ONLY_CLOSEOUT`
- `PREPARE_CONTRACT_CHANGE_PLAN_ONLY: biz.booking.fulfillment`

Readback file:

- `docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-FOUNDER-GATE-DECISION-READBACK-v0.2-2026-06-15.md`

## Source SSOT Read

Fresh source files reviewed for this plan:

| Source | Current signal |
|---|---|
| `hl-contracts/docs/pm/capabilities/biz.booking.fulfillment/DUAL-END-PM-REVIEW.md` | PM result remains `PATCH_REQUIRED`; Human End, Agent End, override owner matrix, retry and duplicate policy need contract-side decision before engineering entry. |
| `hl-contracts/apis/biz.booking.fulfillment.internal.openapi.v1.yaml` | Can / Action pairs exist; Action must re-check Can; key actions return `event_id`; current file states engineering start is not authorized. |
| `hl-contracts/events/biz-booking-fulfillment-state-audit.v0.1.yaml` | State audit is active; booking-owned audit facts and state transitions exist; resource facts remain StoreResource-owned. |
| `hl-contracts/reasoncodes/biz-booking-fulfillment-reasoncodes.v0.1.yaml` | Non-success reason_code trace map is active; success arrival classification remains outside reason_code. |
| `docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-READINESS-ROLLUP-v0.1-2026-06-15.md` | BF-01 through BF-05 evidence is ready for Founder / Gate review; runtime and contract changes remain not authorized. |

## Candidate Exact File Subset

Future `hl-contracts` work, if separately authorized, should be narrowed to this
candidate subset first:

| Candidate file | Plan intent | Change type |
|---|---|---|
| `docs/pm/capabilities/biz.booking.fulfillment/DUAL-END-PM-REVIEW.md` | Convert accepted BF docs-only closeout into a PM-review delta section with Human End, Agent End, override/retry, dependency exit, and remaining blockers. | review delta only |
| `apis/biz.booking.fulfillment.internal.openapi.v1.yaml` | Decide whether idempotency replay, approval_ref, trace preservation, and duplicate behavior require additive schema or `x-hl-*` metadata. | exact future decision required |
| `events/biz-booking-fulfillment-state-audit.v0.1.yaml` | Decide whether override/retry and dependency exit audit facts are already covered or need additive trace notes. | likely additive notes only |
| `reasoncodes/biz-booking-fulfillment-reasoncodes.v0.1.yaml` | Confirm no success outcome becomes reason_code; add no new reason_code unless a specific missing non-success domain is proven. | hold by default |
| `events/biz-booking-fulfillment-outcome-classification.v0.1.yaml` | Confirm arrival outcome classification remains separate from reason_code. | read/confirm first |

## Diff Intent

The safe contract work order, if later authorized, should be split into small
PRs:

1. PM review delta PR: record accepted docs-only closeout and remaining contract blockers.
2. OpenAPI metadata decision PR: only if approval_ref, idempotency replay, or duplicate behavior needs machine-readable contract metadata.
3. Audit trace note PR: only if state audit needs additive facts or trace language.
4. Reasoncode no-change readback: explicitly preserve success outcome separation unless a missing failure domain is proven.

## Compatibility Impact

Expected compatibility posture:

- default path is additive documentation or metadata;
- no endpoint deletion;
- no state deletion;
- no reason_code reuse for success outcomes;
- no active contract registration by this plan;
- no runtime caller may treat this plan as implementation permission.

Any future OpenAPI or registry mutation must include exact before/after diff,
consumer impact, validation command, rollback/defer option, and Founder / Gate
authorization.

## Validation Floor For Future Contract PR

Future `hl-contracts` PR validation should include at minimum:

1. YAML parse for changed YAML files.
2. PRD / capability gate command required by `hl-contracts` for changed file family.
3. grep check that runtime, production, release, MVP, active contract, and live booking are not authorized by wording.
4. cross-check that every action_id mentioned exists in OpenAPI and state audit.
5. cross-check that every reason_code mentioned is registered or explicitly proposed as missing.

## Stop Conditions

Stop before opening a future `hl-contracts` PR if any of these appear:

1. exact file subset is broader than this plan;
2. runtime or platform implementation is implied;
3. payment, billing, entitlement, identity, privacy, or StoreResource mutation is pulled into booking without separate packet;
4. generated-only evidence is used for GATED progression;
5. success outcome classification is converted into reason_code;
6. owner / approver / approval_ref policy is still ambiguous for customer-visible override.

## Recommended Next Decision

Recommended next Founder / Gate reply, only if contract work should proceed:

```text
AUTHORIZE_CONTRACT_CHANGE_PR_ONLY: biz.booking.fulfillment
FILES:
- docs/pm/capabilities/biz.booking.fulfillment/DUAL-END-PM-REVIEW.md
SCOPE:
- add PM review delta for accepted docs-only closeout
- no OpenAPI/events/facts/reasoncodes mutation
```

Alternative:

```text
HOLD_CONTRACT_CHANGE_BLOCKED: <owner/evidence gap>
```

## Not Authorized

Not Authorized: editing `hl-contracts`, editing `hl-platform`, active registry
write, schema mutation, OpenAPI mutation, event/fact/reasoncode mutation,
runtime, production, release, MVP, active contract, live booking operation,
payment, billing, entitlement, quota, identity/privacy mutation, or formal
business object mutation.
