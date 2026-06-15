# PM 能力包任务书：biz.service.order v1.0

状态：DISPATCH_READY_FOR_PM_READINESS
日期：2026-06-15
Owner：邹骢 / `zoucong121`
能力：`biz.service.order`
工作线：PM-led capability package lane
HK 总任务入口：https://github.com/huanlongAI/hl-dispatch/issues/253
PM 历史入口：https://github.com/huanlongAI/hl-dispatch/issues/192
Founder 派发裁决：2026-06-15 Codex 线程选择 `A 启动 ServiceOrder`

## 中文摘要

本任务书把 `biz.service.order`（服务单）从“按需语义支持”推进为独立的 PM-led 能力包工作线。邹骢需要先提交 PM readiness pack（产品经理准备包），说明服务单的业务边界、首个受限工程切片、PM 验收标准和仍需裁决的 Contract Gap（契约缺口）。

本任务书不启动产品代码实现，不授权 HPRD pass（工程理解通过）、production runtime（生产运行态）、active contract（生效契约）、active registry（生效注册）、真实用户数据、真实客户资产变更、真实服务履约、支付 / 退款 / 结算、secrets、deploy 或 release。

## 术语说明

- `PM readiness pack`：产品经理准备包。用于说明能力边界、首个受限切片、验收标准和未决问题。
- `HPRD`：Human-readable Product Design，人类可读产品设计。这里指工程师对 PM 能力规格的业务理解确认件，不是第二份 PRD，也不是技术设计。
- `PM HPRD pass`：PM 确认工程师 HPRD 忠于能力规格。它只允许在本任务书范围内进入受限工程实现，不等于生产授权。
- `bounded engineering implementation`：受限工程实现。只能在明确切片、测试证据和禁止边界内推进。
- `runtime authorization`：运行态授权。只有 Founder / Gate 明确授权时才成立，本任务书不授予。
- `active contract / active registry`：生效契约 / 生效注册。候选契约合并不等于生效登记。
- `Feishu projection`：飞书投影。飞书只提醒，不是状态真源；正式状态以 GitHub Issue / PR / comment 为准。

## 1. 任务目的

本任务书承接 `hl-contracts#111` 已合并的 `biz.service.order` 候选四件套，把服务单能力从候选材料推进到可交接 PM readiness 阶段。

目标是建立一条清晰交接链路：PM 先确认业务语义和首个受限切片；Founder / Gate 再命名 HPRD 工程师；工程师提交 HPRD；PM 审 HPRD 通过后，才可在本任务书边界内进入受限实现。

本任务书不会扩张当前 HK mainline 的 `hl-platform#139`，也不会把 ServiceOrder 塞进许久明当前 PR。

## 2. 当前 GitHub 事实

```yaml
capability: biz.service.order
pm_owner: zoucong121
source_issue: https://github.com/huanlongAI/hl-dispatch/issues/192
candidate_cap_spec_pr: https://github.com/huanlongAI/hl-contracts/pull/111
candidate_pr_state: MERGED
candidate_merge_commit: f5a12a3f242b011eaa9d9e626969a4016d139c5a
current_maturity: merged_draft_candidate
active_contract_authorized: false
runtime_authorized: false
engineering_start_authorized_by_candidate_merge: false
```

以上候选材料可以作为 PM readiness 的输入。它不是 active contract，不是 frozen implementation baseline（冻结实现基线），也不是 production authorization（生产授权）。

## 3. 工作流

```text
Founder / AI 能力包任务书确认
-> 邹骢提交 PM readiness pack
-> Founder / Gate 命名 HPRD 工程师和首个受限切片
-> 工程师提交 HPRD / technical implementation plan
-> 邹骢按 Cap-Spec 审 HPRD
-> PM HPRD pass 后进入本任务书内的受限工程实现
-> PR / demo / test evidence
-> PM acceptance
-> Gate A / Gate B
-> Human Cross Audit
-> Founder Acceptance
-> merge / conditional pass / follow-up / reject
```

PM HPRD pass 只表示工程师读懂了业务语义，并可在本任务书签定范围内做受限实现。它不授权生产运行态、生效契约注册、真实用户数据、支付 / 计费 / 退款 / 结算、secrets、deploy 或 release。

## 4. PM 范围内

邹骢需要基于已合并的候选基线，提交 Founder 可读的 PM readiness pack：

- 用普通语言确认 `biz.service.order` 的业务边界。
- 列出 `hl-contracts#111` 中应作为 PM 输入的四份候选文件。
- 判断哪些内容已经可以交给工程师写 HPRD。
- 标出未解决的 Contract Gap，尤其是正式服务单创建、已签字服务单草稿、服务来源类型、拆分 / 合并 / 部分履约、取消、补录、催办、客户资产锁定 / 扣减，以及 BookingFulfillment owner 边界。
- 定义 PM HPRD pass 后可进入的第一个受限工程切片。
- 定义 PM 对第一个切片的验收标准。

## 5. PM 范围外

邹骢不得：

- 授权 active contract registration（生效契约注册）。
- 授权 runtime、production、deploy、release、secrets 或真实用户数据。
- 授权 provider / payment / billing / refund / settlement 工作。
- 在没有单独 Founder / Gate 裁决时，要求工程师修改 `hl-contracts`。
- 把飞书、CI green、PM Draft、候选契约合并或语义支持解释成工程授权。
- 把 SalesOrder、CustomerAsset、BookingFulfillment、PaymentCheckout、CustomerProfile、售后、发票、税务、促销或佣金能力吸收到 ServiceOrder。

## 6. PM 必交输出

邹骢在 GitHub 回复：

```yaml
pm_capability_readiness_pack:
  owner: zoucong121
  capability: biz.service.order
  source_candidate_pr: https://github.com/huanlongAI/hl-contracts/pull/111
  conclusion: ready_for_engineer_hprd | needs_founder_gate_decision | blocked
  business_boundary_summary: "<3-8 句普通人能读懂的服务单边界说明>"
  source_files:
    - "<hl-contracts 仓库内的相对路径>"
  first_bounded_engineering_slice:
    name: "<一个小的受限工程切片>"
    user_value: "<门店员工 / 经营侧用户能看到或完成什么>"
    not_in_scope:
      - "<明确不做什么>"
  contract_gaps:
    - id: "<gap id>"
      question: "<一个有边界的问题>"
      required_decision_owner: Founder | Gate | PM | Engineering
  pm_acceptance_checks:
    - check: "<PM 要看什么>"
      pass_condition: "<什么算通过>"
      fail_condition: "<什么算失败>"
  hprd_review_standard:
    - "<工程师 HPRD 必须解释正确的业务语义>"
  not_authorized:
    - production_runtime
    - active_contract
    - active_registry
    - real_user_data
    - provider_payment_billing_refund_settlement
    - secrets
    - deploy_or_release
```

如果 PM 不能完成 readiness pack，只能回复最小 `gap_report`，并写清缺少哪个 Founder / Gate 裁决。

## 7. HPRD 启动条件

工程师 HPRD 只能在以下条件同时满足后启动：

- 本任务书已作为 GitHub SSOT 发布。
- 邹骢已提交 `ready_for_engineer_hprd`。
- Founder / Gate 已命名 HPRD 工程师和第一个受限工程切片。

工程师 HPRD 必须说明：

- 服务单在本能力中是什么意思。
- 已读取哪些候选契约文件。
- 首个受限切片实现什么。
- 哪些内容仍然不在范围内。
- 这个切片如何测试。
- 什么情况必须回复 `gap_report`，不能进入实现。

## 8. 人类可读门禁

每个 PM 回复、HPRD、PR、`gap_report`、Gate 报告和验收包都必须让 Founder、PM 和工程师能直接读懂：

- 一句话结论。
- 证据链接。
- 当前状态。
- 唯一下一步动作和 owner。
- 未解决的不确定项。
- 必要术语的普通语言解释。

禁止黑盒短语，例如“继续推进整体治理”、“需要进一步确认”、“当前上下文显示”或“runtime 那个”。

## 9. 飞书投影

Founder 已确认本任务书只用于 PM readiness 派发。

飞书消息必须包含背景、GitHub 入口、唯一下一步动作、GitHub 回复位置和授权边界。GitHub 仍是唯一事实源，飞书只做提醒投影。
