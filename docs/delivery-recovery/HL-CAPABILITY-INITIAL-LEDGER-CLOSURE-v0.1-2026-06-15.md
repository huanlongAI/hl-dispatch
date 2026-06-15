# HL Capability Initial Ledger Closure v0.1

Status: LONGRUN_DOCS_ONLY_LEDGER_CLOSURE_PREPARED
Date: 2026-06-15

## 中文摘要

本文把初始 8 个 Ledger 条目转换为明确计划终态，并说明哪些条目可以关闭、
哪些进入裁决包、哪些保持带 owner/evidence gap 的阻塞。它不把 Ledger 变成
contract 或 runtime registry。

## 术语说明

- Ledger closure：Ledger 闭环，指状态面消除歧义，不等于业务交付完成。
- CONTRACT_DECISION_PACKET_READY：可以准备 contract 裁决包，不等于 contract 已改。
- BLOCKED_WITH_OWNER_AND_EVIDENCE：阻塞原因和所需 owner/evidence 已明确。

## Closure table

| capability_id | terminal_planning_state | Ledger delta supported |
|---|---|---|
| booking_staging_pilot_closeout | CLOSED_FOR_CURRENT_SCOPE | yes, staging-only closeout |
| biz.booking.fulfillment | READY_FOR_FOUNDER_GATE_DECISION | yes, BF-07 due |
| biz.sales.order | CONTRACT_DECISION_PACKET_READY | yes, PM readiness prepared |
| biz.customer.asset | CONTRACT_DECISION_PACKET_READY | yes, PM readiness prepared |
| biz.offer.catalog | CONTRACT_DECISION_PACKET_READY | yes, gap pack prepared |
| biz.store.resource | CONTRACT_DECISION_PACKET_READY | yes, gap pack prepared |
| biz.tenant.entitlement | BLOCKED_WITH_OWNER_AND_EVIDENCE | yes, independent verifier gap |
| biz.payment.checkout | BLOCKED_WITH_OWNER_AND_EVIDENCE | yes, financial Gate gap |

## Not Authorized

Not Authorized: contract implementation, platform implementation, runtime,
schema, registry, manifest, config, OpenAPI, events, facts, reasoncodes,
production, release, MVP, active contract, live payment, live billing,
entitlement or quota mutation, identity/privacy mutation, or formal business
object mutation.
