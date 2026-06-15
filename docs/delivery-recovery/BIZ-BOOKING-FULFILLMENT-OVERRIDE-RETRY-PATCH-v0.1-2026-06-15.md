# Biz Booking Fulfillment Override Retry Patch v0.1

Status: LONGRUN_DOCS_ONLY_PREPARED_FOR_REVIEW
Date: 2026-06-15
Capability: `biz.booking.fulfillment`
Task: `BF-04-OVERRIDE-RETRY`

## 中文摘要

本文关闭 `biz.booking.fulfillment` 的 override / retry / duplicate /
idempotency replay 计划缺口。它只形成 dispatch 侧 docs-only 证据，不激活
override，不执行 retry，不变更 runtime 或 contract。

## 术语说明

- override：受控例外路径，必须有 owner、approver 和 `approval_ref`。
- retry class：重试分类，区分可重试、不可重试和未知结果。
- idempotency replay：同一个 idempotency key 再次提交时必须返回可审计的重放结果。
- fail-secure：结果未知时保守停止，不制造成功证据。

## Boundary

This patch is limited to `hl-dispatch/docs/delivery-recovery/`. It does not
change `hl-contracts`, `hl-platform`, runtime code, schemas, registries,
manifests, configs, OpenAPI, events, facts, reasoncodes, production, release,
MVP, active contract, or live booking operation.

## Override owner matrix

| Case | owner_role | approver_role | approval_ref policy | Result |
|---|---|---|---|---|
| manual assignment exception | Gate-H | Founder or Founder-delegated Gate | Required before action is active | Planned only |
| resource release failure | Gate-H | PM-A + Gate-H | Required before retry/exit | Planned only |
| duplicate booking dispute | PM-A | Gate-H | Required for dispute resolution | Planned only |
| no-show correction | PM-A | Gate-H | Required for correction path | Planned only |
| unknown result after timeout | Gate-H | Founder / Gate if customer-visible | Required before replay | Planned only |

## Retry and duplicate policy

| Class | Rule | Failure path |
|---|---|---|
| retryable transient read failure | Retry only after evidence lookup confirms no state mutation. | Stop if event/audit result is unknown. |
| non-retryable validation denial | Do not retry; preserve reason_code and trace_id. | Pull PM / Gate if reason domain is unclear. |
| ambiguous action result | Do not blind retry; require event_id / audit_ref lookup. | Mark blocked until evidence exists. |
| duplicate submission | Return existing evidence ref where known; no hidden resubmission. | Block if existing ref cannot be proven. |
| idempotency replay | Replay must preserve original outcome and trace. | Stop if replay would synthesize success. |

## Human End / Agent End boundary

Human End must display current state, proposed exception, owner, approver,
`approval_ref`, reason domain, idempotency key, trace fields, and audit result.
Agent End may prepare evidence and call read-only checks, but it cannot hold
final booking exception authority or bypass Gateway / HK Kernel / Can -> Action
-> Audit.

## Audit expectations

Every override or replay proposal must preserve `event_id` when success already
exists, `trace_id`, `audit_ref`, reason domain, idempotency key, actor, current
state, previous state, and evidence refs. Generated-only evidence cannot complete
GATED progression.

## Terminal planning state

`BF-04-OVERRIDE-RETRY` terminal planning state:
`READY_FOR_FOUNDER_GATE_DECISION` for docs-only review of the patch packet.

## Not Authorized

Not Authorized: active override, live retry, live booking operation,
`hl-contracts` changes, `hl-platform` changes, runtime authorization,
production, release, MVP, active contract, schema, registry, manifest, config,
OpenAPI, events, facts, reasoncodes, payment, billing, entitlement, quota,
identity, privacy, or formal business object mutation.
