# HL Capability Weekly Operating Review v0.1

Status: LONGRUN_DOCS_ONLY_OPERATING_MECHANISM_PREPARED
Date: 2026-06-15

## 中文摘要

本文定义 full landing 后的 weekly operating review。它用于回看 Ledger
变化、GATED 证据、failure path、Learning Patch 和 open decisions，不创建新
runtime 或生产授权。

## 术语说明

- weekly review：每周证据和学习补丁复盘。
- changed state：Ledger 或 terminal planning state 的变化。
- WIP limit：同时推进的 PR 数量上限。

## Cadence

| Review item | Owner | Output |
|---|---|---|
| changed Ledger rows | Dispatch / Gate-H | changed-state list |
| GATED evidence gaps | Gate-H | evidence gap list |
| failure paths | Gate-H | missing failure path list |
| Learning Patches | Dispatch | accepted/deferred patch list |
| Founder / Gate blockers | Founder / Gate | decision queue |
| discovery decisions | TBD_FOUNDER_DECISION | value queue |

WIP limit remains: two execution PRs, one review/readback PR, and one decision
packet PR unless Founder changes it.

## Not Authorized

Not Authorized: runtime, production, release, MVP, active contract, live
business operation, cross-repo implementation, or formal business object
mutation.
