# Biz Booking Fulfillment Dependency Exit Patch v0.1

Status: LONGRUN_DOCS_ONLY_PREPARED_FOR_REVIEW
Date: 2026-06-15
Capability: `biz.booking.fulfillment`
Task: `BF-05-DEPENDENCY-EXIT`

## 中文摘要

本文关闭 `biz.booking.fulfillment` 对 StoreResource、CustomerProfile、
OfferCatalog、QRH 和 legacy mapping 的依赖退出路径计划缺口。它只定义失败
时的保守退出、owner pull 和 decision routing，不实现跨能力 mutation。

## 术语说明

- dependency exit：依赖不可用或证据不足时的停止、回退、重提或裁决路径。
- QRH：Qualified Resource Hold，资源占用/锁定相关依赖证据。
- cross-capability stop rule：跨能力依赖不满足时必须停止，不能隐式推进。

## Boundary

This is a dispatch-side docs-only packet. It does not change contracts,
runtime, schema, registry, manifest, config, OpenAPI, events, facts,
reasoncodes, production, release, MVP, active contract, live booking, live
resource occupancy, or customer data.

## Dependency exit matrix

| Dependency | Required evidence | Exit path | Owner pull |
|---|---|---|---|
| StoreResource | resource availability / release evidence ref | fail secure or governed resubmit | Gate-H |
| QRH | hold state, expiry, release, conflict evidence | stop if stale or missing | Gate-H |
| CustomerProfile | customer/profile precheck evidence | block if identity/privacy boundary unclear | PM-A + Gate-H |
| OfferCatalog | offer/service requirement evidence | return for catalog gap decision | PM-A + PM-B |
| legacy reservation mapping | mapping source, confidence, audit ref | block if mapping cannot be proven | Gate-H |

## Fallback behavior

If dependency evidence is missing, stale, generated-only, or contradictory, the
booking flow remains blocked for planning purposes. The packet may recommend a
governed resubmit or decision packet, but it must not implement a dependency
mutation or infer truth from another capability.

## Terminal planning state

`BF-05-DEPENDENCY-EXIT` terminal planning state:
`READY_FOR_FOUNDER_GATE_DECISION` for docs-only dependency exit review.

## Not Authorized

Not Authorized: StoreResource mutation, QRH mutation, CustomerProfile mutation,
OfferCatalog mutation, legacy mapping rewrite, live booking, runtime,
`hl-contracts`, `hl-platform`, schema, registry, manifest, config, OpenAPI,
events, facts, reasoncodes, production, release, MVP, active contract, payment,
billing, entitlement, quota, identity, privacy, or formal business object
mutation.
