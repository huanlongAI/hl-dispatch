# Biz Sales Order PM Readiness Packet v0.1

Status: LONGRUN_DOCS_ONLY_PM_READINESS_PREPARED
Date: 2026-06-15
Capability: `biz.sales.order`

## 中文摘要

本文为 `biz.sales.order` 准备 PM readiness 和 Contract Gap 裁决面。它不授权
provider、payment、billing、runtime 或 live sales object mutation。

## 术语说明

- PM readiness：PM 语义、范围和边界准备完成，可供后续工程/契约裁决。
- Contract Gap：需要 `hl-contracts` 未来裁决的问题清单。
- provider/payment/billing boundary：供应商、支付和计费边界，当前全部不授权。

## Readiness scope

| Area | Readiness output |
|---|---|
| terminology | sales order, provider dependency, payment dependency, billing dependency redlines |
| PM scope | SPEC_ONLY planning surface |
| Contract Gap | lifecycle, key action, reason, event/fact, OpenAPI decision list |
| Boundary | no provider/payment/billing/runtime/live mutation |

## Terminal planning state

`biz.sales.order`: `CONTRACT_DECISION_PACKET_READY`.

## Not Authorized

Not Authorized: provider integration, payment integration, billing flow, live
sales object mutation, `hl-contracts` implementation, `hl-platform`
implementation, runtime, production, release, MVP, active contract, or formal
business object mutation.
