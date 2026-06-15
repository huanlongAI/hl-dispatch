# HL Capability Rule Thinning Proposal v0.1

Status: LONGRUN_DOCS_ONLY_PROPOSAL
Date: 2026-06-15

## 中文摘要

本文定义 rule thinning 的触发条件和裁决点。当前不删除任何规则，只要求在两次
weekly review 后用证据判断哪些字段或仪式没有影响决策。

## 术语说明

- rule thinning：规则瘦身，删除或合并无效规则。
- decision impact：规则是否改变过真实裁决。
- reporting-over-action：只增加汇报、不推动行动的流程。

## Thinning criteria

| Candidate | Evidence required | Decision |
|---|---|---|
| unused Ledger field | no decision impact in two reviews | remove or defer |
| duplicated SSOT copy | duplicates contract/platform truth | replace with reference |
| ritual causing DRI wait | wait time evidence | simplify |
| generated report without action | no owner or decision output | remove |

## Not Authorized

This proposal does not change `hl-contracts`, `hl-platform`, runtime, production,
release, MVP, active contract, or live business operation.
