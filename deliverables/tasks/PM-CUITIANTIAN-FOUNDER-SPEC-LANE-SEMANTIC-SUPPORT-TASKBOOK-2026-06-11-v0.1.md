# PM 崔田恬 Founder Spec Lane 语义支持任务书 v0.1

日期：2026-06-11

状态：DISPATCH_READY

Owner：崔田恬 / `cuitiantian0704`

任务类型：PM semantic support / gap response

GitHub SSOT：

- HK mainline parent: https://github.com/huanlongAI/hl-dispatch/issues/194
- Founder Spec Lane docs PR: https://github.com/huanlongAI/hl-dispatch/pull/232
- HK engineering taskbook PR: https://github.com/huanlongAI/hl-platform/pull/132
- SalesOrder PM issue: https://github.com/huanlongAI/hl-dispatch/issues/184
- SalesOrder candidate baseline: https://github.com/huanlongAI/hl-contracts/pull/99
- CustomerProfile owner confirmation: https://github.com/huanlongAI/hl-dispatch/issues/109
- CustomerProfile taskbook source: `deliverables/tasks/PM-CUITIANTIAN-CUSTOMER-PROFILE-CAPABILITY-TASKBOOK-2026-05-15-v0.1.md`
- Founder Spec Lane rule source: `docs/delivery-recovery/FOUNDER_SPEC_LANE_v0.1.md`
- Founder dispatch confirmation: 2026-06-11 当前 GitHub 发布线程确认批准

## 1. 任务定位

这不是工程实现任务，不是 Cap-Spec 新四件套任务，也不是 HPRD 前置阻断任务。

本任务用于把 PM 崔田恬的工作流调整到 Founder Spec Lane 后的新位置：崔田恬负责 sales / customer profile 相关业务语义口径、semantic gap 响应和 follow-up 建议；不作为许久明本轮 HK bounded engineering implementation 的开工前置门禁。

许久明本轮工程切片仍按 `hl-platform#132` 执行：

- capability: `biz.booking.fulfillment`
- path: staging / sandbox / capability-package
- output: PR first; structured `gap_report` if blocked
- timebox: 24h plan, 48h PR or `gap_report`, 3-5 days acceptable PR or final `gap_report`

崔田恬只在出现 sales / customer profile 语义相关 gap 时介入，并且只在 GitHub 上回复。

注意：这只描述当前 HK `biz.booking.fulfillment` 工程任务中的 PM 支持位置，不取消崔田恬对 sales / customer profile 能力包的 PM 主流程。若 Founder / Gate 派发对应能力包任务，崔田恬应按 PM capability lane 完成完整 Cap-Spec / requirements design，交给工程师产出 HPRD / technical implementation plan，PM 审 HPRD 通过后工程师立即进入受控开发。

## 2. 当前事实

截至 2026-06-11：

- `biz.sales.order` candidate-only Cap-Spec 已通过 `hl-contracts#99` 合入，但单独看仍不是 active registry、HPRD、design.md、runtime 或生产授权；它可以作为后续 PM capability lane 的输入。
- `hl-dispatch#184` 仍 open，应从旧 Draft correction / Gate prep 阻塞口径调整为 candidate baseline readback + bounded semantic support。
- `biz.customer.profile` 仍保留为 regular PM capability lane 的候选任务，不作为当前 HK booking staging pilot 的开工阻塞项。
- `hl-dispatch#109` 仍 open，当前只能作为 CustomerProfile owner confirmation / taskbook evidence，不授权 HK runtime 或 production。
- PM Draft、HPRD 草稿、飞书认可、CI green、Gate readback 都只是证据或投影，不是生产授权。
- Founder Spec Lane 已允许许久明在 `hl-platform#132` 范围内做受控 HK 工程实现。

## 3. Scope In

崔田恬允许做：

- 阅读 `hl-platform#132`、`hl-dispatch#194`、`hl-dispatch#184`、`hl-dispatch#109` 和 `hl-dispatch#232` 中的 Founder Spec Lane 规则。
- 当许久明 PR 或 `gap_report` 明确提出 sales / customer profile 语义问题时，在对应 GitHub PR / Issue 中回复。
- 对 semantic gap 给出最小可裁决业务口径。
- 标注该口径属于：
  - existing_baseline_clarification
  - needs_founder_gate_decision
  - out_of_scope_follow_up
  - conflicts_with_current_taskbook
- 提醒 Founder / Gate 是否需要把语义输入升级为 taskbook `v1.1+`、follow-up 或 reject。

## 4. Scope Out

崔田恬禁止做：

- 阻断许久明按 `hl-platform#132` 提交 24h plan、PR 或 `gap_report`。
- 把 `hl-dispatch#184`、`hl-dispatch#109`、PM preflight、候选 Cap-Spec 或合并状态解释为脱离签字 taskbook / PM HPRD pass 的工程开工授权。
- 直接授权 production runtime、active contract、active registry、真实用户数据、provider、支付、计费、退款、结算、secrets、deploy 或 release。
- 直接要求许久明修改 `hl-contracts`。
- 通过飞书口头确认替代 GitHub semantic gap 回复。
- 把 sales / customer profile 语义扩展写成本轮 `biz.booking.fulfillment` 工程切片的新 scope。

## 5. 触发条件

崔田恬只在以下条件之一满足时行动：

1. `hl-platform#132` 或许久明后续 PR / `gap_report` 明确 @ `cuitiantian0704` 请求 sales / customer profile 语义口径。
2. Gate A / Gate B / Human Cross Audit 指出本轮工程切片受 sales / customer profile 语义影响，需要 PM 输入。
3. Founder / Gate 在 GitHub 明确要求崔田恬回复一个 bounded semantic question。

如果没有 GitHub action item，不发飞书，不要求崔田恬主动补台账。

## 6. 输出格式

崔田恬在 GitHub 回复时使用以下结构：

```yaml
pm_semantic_response:
  owner: cuitiantian0704
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

## 7.1 PM Capability Lane Trigger

当 Founder / Gate 派发崔田恬负责的能力包任务时，流程改为：

```text
Founder / AI capability taskbook
-> 崔田恬完成 Cap-Spec / requirements design
-> 工程师提交 HPRD / technical implementation plan
-> 崔田恬审 HPRD 是否满足 Cap-Spec
-> PM HPRD pass 后工程师立即开发
-> PR / demo / test evidence
-> PM acceptance
-> Gate A / Gate B
-> Human Cross Audit
-> Founder Acceptance / merge decision
```

PM HPRD pass 只授权该能力包任务书范围内的受控开发；不授权 production runtime、active contract、真实用户、真实 provider、真实支付 / 计费 / 退款 / 结算、secrets、deploy 或 release。

## 8. 飞书投影

只有在 Founder 确认本 PM 任务书 dispatch-ready 后，才允许飞书提醒崔田恬。

飞书正文必须包含：

```text
GitHub taskbook / issue 是唯一事实源，飞书只做提醒投影，不是授权源。
```

发送后必须回写 GitHub projection event。
