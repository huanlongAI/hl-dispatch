# PM 朱阳 Founder Spec Lane 语义支持任务书 v0.1

日期：2026-06-11

状态：DRAFT_FOR_FOUNDER_REVIEW

Owner：朱阳 / `zhuyang1204`

任务类型：PM semantic support / gap response

GitHub SSOT：

- HK mainline parent: https://github.com/huanlongAI/hl-dispatch/issues/194
- Founder Spec Lane docs PR: https://github.com/huanlongAI/hl-dispatch/pull/232
- HK engineering taskbook PR: https://github.com/huanlongAI/hl-platform/pull/132
- Dispatch-ready pointer: https://github.com/huanlongAI/hl-dispatch/issues/194#issuecomment-4678138374
- PM workflow adjustment source: `docs/delivery-recovery/FOUNDER_SPEC_LANE_v0.1.md`

## 1. 任务定位

这不是工程实现任务，不是 Cap-Spec 新四件套任务，也不是 HPRD 前置阻断任务。

本任务用于把 PM 朱阳的工作流调整到 Founder Spec Lane 后的新位置：朱阳负责客户与支付线相关的业务语义口径、semantic gap 响应和 follow-up 建议；不作为许久明本轮 HK bounded engineering implementation 的开工前置门禁。

许久明本轮工程切片仍按 `hl-platform#132` 执行：

- capability: `biz.booking.fulfillment`
- path: staging / sandbox / capability-package
- output: PR first; structured `gap_report` if blocked
- timebox: 24h plan, 48h PR or `gap_report`, 3-5 days acceptable PR or final `gap_report`

朱阳只在出现客户 / 支付 / 资产语义相关 gap 时介入，并且只在 GitHub 上回复。

## 2. 当前事实

截至 2026-06-11：

- `biz.customer.asset` candidate-only Cap-Spec 已合入 `hl-contracts`，但仍不是 active contract、active registry、runtime、production 或工程开工授权。
- PM Draft、HPRD 草稿、飞书认可、CI green、Gate readback 都只是证据或投影，不是生产授权。
- Founder Spec Lane 已允许许久明在 `hl-platform#132` 范围内做受控 HK 工程实现。
- PM 工作流需要从“开工前置审批链”调整为“业务语义基线与 gap 输入链”。

## 3. Scope In

朱阳允许做：

- 阅读 `hl-platform#132`、`hl-dispatch#194` 指针和 `hl-dispatch#232` 中的 Founder Spec Lane 规则。
- 当许久明 PR 或 `gap_report` 明确提出客户 / 支付 / 资产语义问题时，在对应 GitHub PR / Issue 中回复。
- 对 semantic gap 给出最小可裁决业务口径。
- 标注该口径属于：
  - existing_baseline_clarification
  - needs_founder_gate_decision
  - out_of_scope_follow_up
  - conflicts_with_current_taskbook
- 提醒 Founder / Gate 是否需要把语义输入升级为 taskbook `v1.1+`、follow-up 或 reject。

## 4. Scope Out

朱阳禁止做：

- 阻断许久明按 `hl-platform#132` 提交 24h plan、PR 或 `gap_report`。
- 把 PM Draft、HPRD 草稿、飞书消息或 PM 工作台状态解释为 engineering start authorization。
- 直接授权 production runtime、active contract、active registry、真实用户数据、provider、支付、计费、退款、结算、secrets、deploy 或 release。
- 直接要求许久明修改 `hl-contracts`。
- 通过飞书口头确认替代 GitHub semantic gap 回复。
- 把客户 / 支付 / 资产语义扩展写成本轮 `biz.booking.fulfillment` 工程切片的新 scope。

## 5. 触发条件

朱阳只在以下条件之一满足时行动：

1. `hl-platform#132` 或许久明后续 PR / `gap_report` 明确 @ `zhuyang1204` 请求客户 / 支付 / 资产语义口径。
2. Gate A / Gate B / Human Cross Audit 指出本轮工程切片受客户 / 支付 / 资产语义影响，需要 PM 输入。
3. Founder / Gate 在 GitHub 明确要求朱阳回复一个 bounded semantic question。

如果没有 GitHub action item，不发飞书，不要求朱阳主动补台账。

## 6. 输出格式

朱阳在 GitHub 回复时使用以下结构：

```yaml
pm_semantic_response:
  owner: zhuyang1204
  related_taskbook: https://github.com/huanlongAI/hl-platform/pull/132
  related_gap_or_pr: "<GitHub PR / issue / comment URL>"
  question: "<one bounded semantic question>"
  answer_type: existing_baseline_clarification | needs_founder_gate_decision | out_of_scope_follow_up | conflicts_with_current_taskbook
  answer: "<short business semantic answer>"
  evidence:
    - "<GitHub issue / PR / repo file URL>"
  not_authorized:
    - production_runtime
    - active_contract
    - active_registry
    - real_user_data
    - provider_payment_billing_refund_settlement
    - secrets
    - deploy_or_release
  recommended_next_step: "<taskbook v1.1 / follow-up / no change / Founder-Gate decision>"
```

## 7. 验收标准

合格输出必须满足：

- 回复在 GitHub，不在飞书。
- 只回答一个 bounded semantic question。
- 明确区分“现有基线澄清”和“需要 Founder / Gate 裁决”。
- 不把 PM 口径写成 production、active contract、runtime 或 registry 授权。
- 能被 Gate A / Gate B / Human Cross Audit 直接消费。

## 8. 飞书投影

只有在 Founder 确认本 PM 任务书 dispatch-ready 后，才允许飞书提醒朱阳。

飞书正文必须包含：

```text
GitHub taskbook / issue / PR 是唯一事实源；飞书只是提醒投影，不是授权、验收或完成证明。
```

本任务当前仍为 `DRAFT_FOR_FOUNDER_REVIEW`，不得发送飞书。
