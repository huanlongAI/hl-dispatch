# Biz Offer Catalog Gap Pack v0.1

Status: LONGRUN_DOCS_ONLY_GAP_PACK_PREPARED
Date: 2026-06-15
Capability: `biz.offer.catalog`

## 中文摘要

本文为 `biz.offer.catalog` 准备 Gateway、OpenAPI、idempotency、Agent /
Human split、approval matrix 和 IAM boundary 的 gap pack。它不授权 PRD 直接
工程开工或 live catalog mutation。

## 术语说明

- gap pack：缺口包，列出进入契约或平台前必须裁决的缺口。
- approval matrix：审批矩阵，定义 owner、approver、approval_ref 和原因域。
- IAM boundary：身份权限边界，避免审批或可见性绕过。

## Gap matrix

| Gap | Required next evidence | Routing |
|---|---|---|
| Gateway path | Can / Action / Audit expectation | contract or platform packet |
| OpenAPI | route and schema intent | contract packet |
| idempotency | duplicate and replay behavior | contract packet |
| Agent / Human split | deterministic human approval surface | platform packet if UI/runtime needed |
| approval matrix | owner/approver/approval_ref | Founder / Gate decision |
| IAM boundary | visibility and approval permission | contract/platform packet |

## Terminal planning state

`biz.offer.catalog`: `CONTRACT_DECISION_PACKET_READY`.

## Not Authorized

Not Authorized: engineering start from PRD only, live catalog mutation, approval
bypass, Gateway bypass, runtime, production, release, MVP, active contract,
`hl-contracts` implementation, or `hl-platform` implementation.
