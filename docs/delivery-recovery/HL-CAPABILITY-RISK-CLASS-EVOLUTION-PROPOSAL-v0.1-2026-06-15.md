# HL Capability Risk Class Evolution Proposal v0.1

Status: LONGRUN_DOCS_ONLY_PROPOSAL
Date: 2026-06-15

## 中文摘要

本文定义 REVERSIBLE / GATED 是否需要演化的评审点。当前不新增风险类别；
只有当 Day-30 或 weekly review 证明两级模型造成误判或过度仪式时，才准备
Founder / Gate 规则裁决。

## 术语说明

- REVERSIBLE：当前证据范围内可回退。
- GATED：触碰正式事实、资源、资金、权益、身份、隐私、合同或生产数据。
- over-ritual：风险较低但被高风险流程拖慢。

## Evaluation matrix

| Signal | Meaning | Action |
|---|---|---|
| REVERSIBLE item repeatedly needs Gate | two-level model may be too coarse | propose intermediate class |
| GATED item lacks failure path | process is under-specified | keep GATED and fix evidence |
| check-only leaks mutation | classification trigger works | upgrade to GATED |
| reversible movement blocked by ritual | process overhead | rule thinning review |

## Not Authorized

This proposal does not change active rules outside dispatch docs and does not
authorize runtime, production, release, MVP, active contract, or live operation.
