# HL Capability Metrics 30 v0.1

Status: LONGRUN_DOCS_ONLY_METRICS_PREPARED
Date: 2026-06-15

## 中文摘要

本文定义 Day-30 机制完整性指标，用来判断 Ledger、not_authorized、GATED
证据、Learning Patch 和 generated-only evidence 是否进入稳定运行。

## 术语说明

- Day-30 metrics：30 天机制健康指标。
- generated-only evidence：仅由生成内容构成的证据，不能完成 GATED progression。
- mechanism integrity：机制是否阻止误读和越权。

## Metrics

| Metric | Target | Owner |
|---|---|---|
| Ledger coverage for active / PM-led / pilot items | 100 percent | Dispatch |
| `not_authorized` coverage | 100 percent | Dispatch |
| GATED bypass count | 0 | Gate-H |
| draft/staging/manifest/readiness misread | 0 | Founder / Gate |
| Learning Patch after progression | 100 percent | Dispatch |
| generated-only evidence accepted for GATED | 0 | Gate-H |

## Not Authorized

Metrics do not authorize production, release, MVP, active contract, runtime, or
live business operation.
