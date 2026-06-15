# HL Capability Metrics 60 90 v0.1

Status: LONGRUN_DOCS_ONLY_METRICS_PREPARED
Date: 2026-06-15

## 中文摘要

本文定义 Day-60 / Day-90 趋势指标，用来判断 full landing 机制是否降低等待、
减少返工、提升独立证据和 failure path 覆盖。

## 术语说明

- trend metrics：趋势指标，用于看方向，不替代单次裁决。
- blocker wait：阻塞等待时间。
- process overhead：流程开销，必须被证据证明有价值。

## Metrics

| Metric | Desired direction | Owner |
|---|---|---|
| lead time | down | Dispatch |
| blocker wait time | down | Founder / Gate |
| rework rate | down | Dispatch |
| independent evidence coverage | up | Gate-H |
| failure path coverage | up | Gate-H |
| reversible autonomous movement | up | Dispatch |
| process overhead | down or justified | Founder / Gate |

## Not Authorized

Metrics do not authorize runtime, production, release, MVP, active contract, or
live business operation.
