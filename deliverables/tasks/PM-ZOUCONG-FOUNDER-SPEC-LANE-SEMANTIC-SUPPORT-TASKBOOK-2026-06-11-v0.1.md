# PM 邹骢 Founder Spec Lane 语义支持任务书 v0.1

日期：2026-06-11

状态：DISPATCH_READY

Owner：邹骢 / `zoucong121`

任务类型：PM semantic support / gap response

GitHub SSOT：

- HK mainline parent: https://github.com/huanlongAI/hl-dispatch/issues/194
- Founder Spec Lane docs PR: https://github.com/huanlongAI/hl-dispatch/pull/232
- HK engineering taskbook PR: https://github.com/huanlongAI/hl-platform/pull/132
- ServiceOrder PM issue: https://github.com/huanlongAI/hl-dispatch/issues/192
- ServiceOrder candidate baseline: https://github.com/huanlongAI/hl-contracts/pull/111
- PaymentCheckout PM issue: https://github.com/huanlongAI/hl-dispatch/issues/198
- PaymentCheckout candidate baseline: https://github.com/huanlongAI/hl-contracts/pull/112
- Founder Spec Lane rule source: `docs/delivery-recovery/FOUNDER_SPEC_LANE_v0.1.md`
- Founder dispatch confirmation: 2026-06-11 当前 GitHub 发布线程确认批准

## 1. 任务定位

这不是工程实现任务，不是 Cap-Spec 新四件套任务，也不是 HPRD 前置阻断任务。

本任务用于把 PM 邹骢的工作流调整到 Founder Spec Lane 后的新位置：邹骢负责 booking / service / payment 相关业务语义口径、semantic gap 响应和 follow-up 建议；不作为许久明本轮 HK bounded engineering implementation 的开工前置门禁。

许久明本轮工程切片仍按 `hl-platform#132` 执行：

- capability: `biz.booking.fulfillment`
- path: staging / sandbox / capability-package
- output: PR first; structured `gap_report` if blocked
- timebox: 24h plan, 48h PR or `gap_report`, 3-5 days acceptable PR or final `gap_report`

邹骢只在出现 booking / service / payment 语义相关 gap 时介入，并且只在 GitHub 上回复。

## 2. 当前事实

截至 2026-06-11：

- `biz.booking.fulfillment` Cap-Spec baseline 已通过 `hl-contracts#30` 合入，但不等于 active contract、runtime、production 或工程开工授权。
- `biz.service.order` candidate-only Cap-Spec 已通过 `hl-contracts#111` 合入，但仍不是 active registry、HPRD、design.md、runtime 或生产授权。
- `biz.payment.checkout` candidate-only Cap-Spec 已通过 `hl-contracts#112` 合入，但仍不是真实 provider、真实计费、退款、结算、runtime 或生产授权。
- `hl-dispatch#192` 与 `hl-dispatch#198` 仍 open，应从旧 ETA / preflight 阻塞口径调整为 candidate baseline readback + bounded semantic support。
- PM Draft、HPRD 草稿、飞书认可、CI green、Gate readback 都只是证据或投影，不是生产授权。
- Founder Spec Lane 已允许许久明在 `hl-platform#132` 范围内做受控 HK 工程实现。

## 3. Scope In

邹骢允许做：

- 阅读 `hl-platform#132`、`hl-dispatch#194`、`hl-dispatch#192`、`hl-dispatch#198` 和 `hl-dispatch#232` 中的 Founder Spec Lane 规则。
- 当许久明 PR 或 `gap_report` 明确提出 booking / service / payment 语义问题时，在对应 GitHub PR / Issue 中回复。
- 对 semantic gap 给出最小可裁决业务口径。
- 标注该口径属于：
  - existing_baseline_clarification
  - needs_founder_gate_decision
  - out_of_scope_follow_up
  - conflicts_with_current_taskbook
- 提醒 Founder / Gate 是否需要把语义输入升级为 taskbook `v1.1+`、follow-up 或 reject。

## 4. Scope Out

邹骢禁止做：

- 阻断许久明按 `hl-platform#132` 提交 24h plan、PR 或 `gap_report`。
- 把 `hl-dispatch#192` / `hl-dispatch#198` 的旧 ETA、PM preflight、候选 Cap-Spec 或合并状态解释为 engineering start authorization。
- 直接授权 production runtime、active contract、active registry、真实用户数据、provider、支付、计费、退款、结算、secrets、deploy 或 release。
- 直接要求许久明修改 `hl-contracts`。
- 通过飞书口头确认替代 GitHub semantic gap 回复。
- 把 service / payment 语义扩展写成本轮 `biz.booking.fulfillment` 工程切片的新 scope。

## 5. 触发条件

邹骢只在以下条件之一满足时行动：

1. `hl-platform#132` 或许久明后续 PR / `gap_report` 明确 @ `zoucong121` 请求 booking / service / payment 语义口径。
2. Gate A / Gate B / Human Cross Audit 指出本轮工程切片受 booking / service / payment 语义影响，需要 PM 输入。
3. Founder / Gate 在 GitHub 明确要求邹骢回复一个 bounded semantic question。

如果没有 GitHub action item，不发飞书，不要求邹骢主动补台账。

## 6. 输出格式

邹骢在 GitHub 回复时使用以下结构：

```yaml
pm_semantic_response:
  owner: zoucong121
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

只有在 Founder 确认本 PM 任务书 dispatch-ready 后，才允许飞书提醒邹骢。

飞书正文必须包含：

```text
GitHub taskbook / issue 是唯一事实源，飞书只做提醒投影，不是授权源。
```

发送后必须回写 GitHub projection event。
