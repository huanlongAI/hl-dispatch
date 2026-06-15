# HL Contract Decision Packet Capability Full Landing v0.1

Status: READY_FOR_FOUNDER_GATE_REVIEW
Date: 2026-06-15
Target repo: `hl-contracts`

## 中文摘要

本文是 full landing 后续可能需要的 `hl-contracts` 裁决包。它只在
`hl-dispatch` 中准备待裁决事项，不修改 contract SSOT，不新增 schema、
OpenAPI、events、facts 或 reasoncodes。

## 术语说明

- contract decision packet：契约裁决包，用来请求是否允许未来改
  `hl-contracts`。
- exact target files：未来可能修改的文件路径，当前只作为裁决输入。
- compatibility impact：兼容性影响评估，当前只做计划说明。

## Candidate contract decisions

| Capability | Candidate target | Intent | Evidence refs | Owner |
|---|---|---|---|---|
| `biz.booking.fulfillment` | capability PM review / OpenAPI / reason trace refs | decide whether docs-only closeout should become contract work | BF-01..BF-07 packets | PM-A + Gate-H |
| `biz.sales.order` | `hl-contracts/prd/biz/**` and future capability surfaces | resolve PM readiness Contract Gap | Sales Order PM readiness packet | PM-A |
| `biz.customer.asset` | `hl-contracts/prd/biz/**` and identity/privacy-related surfaces | resolve asset state and identity/privacy contract gaps | Customer Asset PM readiness packet | PM-B |
| `biz.offer.catalog` | OpenAPI / approval / idempotency / IAM surfaces | resolve offer catalog gap pack | Offer Catalog gap pack | PM-B + Gate-H |
| `biz.store.resource` | state machine / QRH / idempotency surfaces | resolve store resource gap pack | Store Resource gap pack | PM-B + Gate-H |
| `biz.payment.checkout` | payment/refund/settlement audit surfaces | decide whether financial contract work may start | Payment preflight packet | PM-B + Founder/Gate |

## Requested Founder / Gate decision

Choose one:

```text
PREPARE_CONTRACT_CHANGE_PLAN_ONLY: <capability scope>
```

```text
HOLD_CONTRACT_WORK_BLOCKED: <owner/evidence gap>
```

```text
DEFER_CONTRACT_WORK: <reason>
```

## Rollback or defer option

If future contract work is not approved, keep all capability rows in their
current terminal planning states and preserve dispatch-side docs-only evidence.

## Not Authorized

Not Authorized: editing `hl-contracts`, active registry write, schema mutation,
OpenAPI mutation, event/fact/reasoncode mutation, runtime, production, release,
MVP, active contract, live booking, live payment, live billing, entitlement
deduction, quota mutation, identity/privacy mutation, or formal business object
mutation.
