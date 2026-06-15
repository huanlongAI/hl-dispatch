# Biz Customer Asset PM Readiness Packet v0.1

Status: LONGRUN_DOCS_ONLY_PM_READINESS_PREPARED
Date: 2026-06-15
Capability: `biz.customer.asset`

## 中文摘要

本文为 `biz.customer.asset` 准备 PM readiness 和 Contract Gap 裁决面。它只
整理资产状态、CustomerProfile 依赖、identity / privacy 边界，不授权 live
customer asset mutation。

## 术语说明

- customer asset：客户资产能力项，当前仍为 SPEC_ONLY / GATED。
- identity/privacy boundary：身份和隐私状态边界，任何 live mutation 都需单独裁决。
- Contract Gap list：未来 contract packet 的输入清单。

## Readiness scope

| Area | Readiness output |
|---|---|
| asset state | state model gaps and transition questions |
| dependency | CustomerProfile dependency and identity boundary |
| privacy | no privacy state mutation without future decision |
| Contract Gap | lifecycle, reason, fact/event, OpenAPI decision list |

## Terminal planning state

`biz.customer.asset`: `CONTRACT_DECISION_PACKET_READY`.

## Not Authorized

Not Authorized: active contract claim, live customer asset mutation, identity
merge, privacy state mutation, runtime, production, release, MVP, `hl-contracts`
implementation, or `hl-platform` implementation.
