# Delivery Recovery Mode v0.1 / 交付恢复模式 v0.1

## 1. 定位

Delivery Recovery Mode v0.1 是 14–30 天的交付恢复模式，不是永久唯一流程。

目标不是继续完善治理，而是把组织从 GitHub 评论流、AI 回填流、总账流、飞书通知流拉回到 PR、test、demo、acceptance。

核心原则：
- 治理只服务交付，不再替代交付。
- 没有交付切片的治理，默认降级、冻结、归档或转为风险债。
- GitHub 是证据源；Bitable / Project / Feishu 是动作投影，不是事实源。
- 不先建完整 task 平台。
- 不全量清洗历史 issue。
- 不继续让总账 issue 承载日常流水评论。

## 2. 主流程

Mission Package
→ Delivery Slice / Risk-Retirement Slice
→ Work Unit
→ Context Pack
→ AI / Human Execution
→ PR / Test / Review
→ Evidence Resolver
→ Task Snapshot
→ Action Projection
→ Acceptance
→ Close / Iterate / Archive

## 3. 主规则

- No Package, No Planned Work
  计划内工作必须有 Mission Package；P0 incident / trivial fix / CI failure fix / security urgent fix 走 Exception Lane。

- No Slice, No Delivery Plan
  没有 Delivery Slice 或 Risk-Retirement Slice，不进入 1–2 周交付计划。

- No Context, No AI Guess
  缺任务包、快照、证据、授权时，AI 只能输出 gap_report，不能猜测或继续推进。

- No Evidence, No Done
  没有 PR / test / demo / acceptance / decision record，不得写“已完成、已确认、已授权、已阻塞、已通过、可关闭”。

- No Action, No Notification
  没有明确动作项，不推飞书，不刷公共状态评论。

- One Slice, Few Work Units
  一个 Delivery Slice 最多 3–5 个 Work Unit。

- One DRI
  每个 Work Unit 只能有一个直接负责人。

- Risk-Based Governance
  Green 快速，Yellow 正常，Red 强治理。

- GitHub Is Evidence
  GitHub 记录 PR、commit、CI、review、decision、acceptance 等事实，不作为非开发主 UI。

- Bitable Is Action Projection
  Bitable / Project 只展示 action、blocker、decision、acceptance，不承载事实裁决。

## 4. Mission Package

Mission Package 是战略入口，由 Founder / Sponsor 下发。

Founder 负责：
- 目标
- 范围
- 优先级
- 成功标准
- 授权边界
- 重大裁决

Founder 不负责：
- 派发每个子 issue
- 维护总账
- 解释每条 GitHub 评论
- 审核每条 AI 回填

Mission Package 必填：
- package_id
- 目标
- 背景
- 范围：必做 / 不做 / 可调研但不阻塞
- 已知上下文：只放关键链接
- 已确认事实：每条必须带证据
- 成功标准
- 授权边界
- 风险级别
- Package Owner
- 升级条件

重要：
- Mission Package 是 Delivery Slice 的上游。
- mission_package.yml 不应强制 slice_id。

## 5. Package Owner

Package Owner 不是文档 owner，而是交付 owner。

Package Owner 负责：
- 把 Mission Package 拆成 1–3 个 Delivery Slice 或 Risk-Retirement Slice
- 控制 active Work Unit 数量
- 维护 Task Snapshot
- 保证证据链
- 组织验收
- 只向 Founder 升级目标、范围、Red Path 授权、重大取舍

无 Package Owner 的 Mission Package 不进入交付计划。

## 6. Delivery Slice

Delivery Slice 是计划入口。

定义：
Delivery Slice = 一个 3–7 天内可以被运行、测试、演示、验收的纵向业务或工程闭环。

必填 7 字段：
- slice_id
- 业务 / 工程目标
- 可运行路径：API / UI / CLI / workflow / smoke test 至少一种
- 完成定义：PR + test + demo/evidence + acceptance
- 验收人
- 风险级别：Green / Yellow / Red
- 不做事项

时间盒：
- Green: 3–5 天
- Yellow: 5–10 天
- Red: 不固定，但必须有 unblock condition 和 decision deadline

delivery_slice.yml 必须强制：
- package_id
- slice_id
- DRI
- risk_path
- 可运行路径
- 完成定义
- 验收人
- 不做事项

## 7. Risk-Retirement Slice

Risk-Retirement Slice 用于不能直接 demo 的风险消除任务。

适用：
- Red Path 风险解除
- 架构 spike
- provider path
- secret-store
- endpoint
- production blocker
- security / compliance blocker

必填：
- risk_id
- 要消除的风险
- 解除条件
- decision deadline
- 输出：PR / spike report / decision record / blocker closeout
- 禁止变成长调研或长评论

## 8. Work Unit

Work Unit 是执行入口。

规则：
- 一个 Work Unit 只有一个交付物
- 一个 Work Unit 只有一个 DRI
- 一个 Work Unit 只有一个 next_action
- 一个 Work Unit 必须关联 package_id 和 slice_id 或 risk_id
- 一个 Work Unit 必须有 evidence_exit / expected_evidence
- Work Unit 创建时不应强制 actual evidence
- actual evidence 在验收或关闭时强制

work_unit.yml 必须强制：
- package_id
- slice_id 或 risk_id
- work_unit_id
- DRI
- next_action
- risk_path
- expected_evidence 或 evidence_exit

## 9. Context Pack

AI 处理任何 Work Unit 前，必须有 Context Pack。

Context Pack 包含：
- Mission Package
- Delivery Slice / Risk-Retirement Slice
- Task Snapshot
- Evidence List
- Allowed Action
- Authorization Boundary

缺任何一项，AI 只能输出 gap_report。

## 10. AI Output Contract

公共 GitHub 回填只允许四类：

1. status_update
   用于状态、owner、证据、阻塞发生实质变化。

2. gap_report
   用于缺任务包、缺快照、缺证据、缺授权、缺 owner。

3. decision_request
   用于必须人类裁决。一次只能问一个问题。

4. acceptance_report
   用于待验收、关闭、条件通过或不通过。

所有 AI 公共回填必须包含：
<!-- ai-output:v1 -->
【类型】
【结论】
【依据】
【当前状态】
【下一步唯一动作】
【需要人处理】
【不确定项】

禁止：
- “收到 / 已知 / 继续推进”
- AI 思考过程
- 普通同步
- 无证据判断
- 黑话式治理表达

判断词证据规则：
出现以下词必须带证据：
- 已完成
- 已确认
- 已授权
- 已阻塞
- 已通过
- 可关闭
- runtime ready
- production ready

黑话拦截：
- 继续推进整体治理
- 需要进一步确认
- 当前上下文显示
- 可能已经处理过
- runtime 那个
- HPRD 已确认但无证据

## 11. Task Snapshot

Task Snapshot 是当前口径，不是人肉签字。

必须包含：
- package_id
- slice_id 或 risk_id
- maturity
- type
- state
- risk_path
- DRI
- current_status
- confirmed_facts，每条必须有 evidence
- next_action
- blocked_by
- unblock_condition
- authorization
- evidence_links
- close_condition
- last_material_change

必须支持：
<!-- task-snapshot:v1 -->

## 12. No Structured Update, No Public Status Comment

没有结构化状态变化，不允许公共状态评论。

例外：
- PR review
- CI failure
- security incident
- P0 incident
- blocker unblock

这些例外仍必须带证据。

## 13. Exception Lane

以下情况可不等完整 Mission Package 先行动：
- P0 incident
- trivial fix
- CI failure fix
- security urgent fix
- blocker unblock

但必须事后补：
- evidence
- incident / fix report
- close reason
- next prevention if applicable

## 13.1 Founder Spec Lane / 创始人规格直达通道

Founder Spec Lane 是 Delivery Recovery Mode v0.1 恢复期内的正式通道之一，不是 Founder 特权通道，也不是永久唯一流程。

适用条件：
- Founder 提供完整任务书，或明确批准基于 GitHub 当前事实起草的任务书。
- 目标是受控 HK 工程实现、closeout、audit、fill-in、test、acceptance packaging 或受控交付恢复步骤。
- 契约方向、禁止事项、验收方式足够清楚，一个 DRI 可以执行。
- 输出可以是 PR、确定性测试 / demo evidence，或 `gap_report`。

禁止用于：
- 开放式 discovery；
- 多方语义谈判；
- production runtime 实现或生产发布；
- 真实用户数据；
- 真实支付、计费、退款、结算或 provider 集成；
- secrets / secret-store 变更；
- 没有测试、demo 或证据入口的任务。

固定流程：

```text
Founder Taskbook
-> Engineer 24h Implementation Plan
-> PR or gap_report
-> Gate A: Dahuizi contract / business / redline review
-> Gate B: Xiaofeifei code / test / security / regression review
-> Human Cross Audit
-> Founder Acceptance
-> merge / conditional pass / follow-up / reject
```

硬规则：
- `gap_report` 是合格交付形态，不是失败。
- Founder 任务书可以授权受控 HK 工程实现，但不能被解释为生产 runtime、active contract、真实数据、真实 provider、真实支付 / 计费 / 退款 / 结算、secrets、部署或发布授权。
- Gate A / Gate B 必须反相关：职责不同、检查独立、分别给出 P0 / P1 / P2。
- 任一 P0 阻断 Founder Acceptance，除非 Founder / Gate 重新裁决 scope。
- Human Cross Audit 有 veto，最少独立读取 3 个核心文件或证据、运行或验证 1 个命令 / artifact、写出至少 1 条 AI 未提及观察。
- 任务书 `v1.0` 冻结 scope；`v1.1+` 只能通过编辑文件澄清。新范围和新验收标准必须走 follow-up，不能只写在评论里。
- 飞书只能投影 GitHub SSOT action，不承载授权、验收、owner confirmation 或完成事实。

### 13.2 PM Workflow Adjustment Under Founder Spec Lane

PM 流程在恢复期采用双轨：

1. 常规 PM Cap-Spec / HPRD lane
   - 适用于新能力、开放语义、多方业务协商、尚无 Founder 完整任务书的能力包。
   - PM 继续负责 Cap-Spec、HPRD 业务理解确认、semantic questions 和 PM acceptance。
   - PM Draft、HPRD 草稿、PM 飞书认可仍不授权 engineering start、runtime、active contract、OpenAPI、facts、events、reasoncodes 或 registry。

2. Founder Spec Lane PM support lane
   - 适用于 Founder 已签字的 bounded engineering taskbook。
   - PM 不作为工程师 24h plan、PR 或 `gap_report` 的开工前置阻塞。
   - PM 只在 taskbook 指名或工程 PR / `gap_report` 暴露 semantic gap 时介入。
   - PM 输出必须落 GitHub，只能提供业务语义口径、gap classification 或 follow-up 建议。
   - PM 输出不能扩大 scope，不能授权 production、active contract、真实用户数据、provider、支付、计费、退款、结算、secrets、deploy 或 release。
   - Founder / Gate 决定 PM 输入是否进入 taskbook `v1.1+`、follow-up 或 reject。

当前 HK recovery taskbook 的 PM support lane 采用 named semantic support taskbook：

- 朱阳 / `zhuyang1204`：customer / payment / asset semantic gaps。
- 邹骢 / `zoucong121`：booking / service / payment semantic gaps。
- 崔田恬 / `cuitiantian0704`：sales / customer profile semantic gaps。

这些 PM support taskbook 不是常驻待办池。没有 GitHub PR、`gap_report`、Gate 或 Founder / Gate comment 提出的 bounded semantic question，就没有 PM action item，也不发送飞书提醒。

禁止把两条轨混用成“PM / HPRD 前置阻断 Founder-signed engineering taskbook”。如果 Founder Spec Lane taskbook 已签字且 scope 明确，工程师应按 taskbook 开工；PM 语义缺口通过 PR / `gap_report` 回到 GitHub 裁决链。

## 14. Risk Path / Governance Budget

Green:
- sandbox / mock / docs / check-only / 无真实数据 / 无 secret / 无生产
- 1 个 Mission Package
- 1 个 Delivery Slice
- 最多 3–5 个 Work Unit
- 不允许新建 ledger issue
- AI review + owner self-check

Yellow:
- runtime / contract read path / 外部 sandbox API / 多仓库变更
- 允许 1 名 human reviewer
- 允许 contract review
- 最多 1 个 blocker issue
- 必须有 test evidence

Red:
- production / real user data / provider secret /真实计费 / 客户可见影响
- 允许强 gate
- 必须有 unblock condition
- 必须有 decision deadline
- 需要 security / product / release approval

## 15. 能力成熟度 M0–M9

M0 observation_candidate
M1 session_candidate_locked
M2 draft_candidate_baseline
M3 hprd_understanding_confirmed
M4 contract_draft_pr
M5 active_contract_baseline
M6 runtime_candidate
M7 staging_evidence_accepted
M8 internal_mvp_accepted
M9 production_authorized

禁止误读：
- checks SUCCESS ≠ ready
- Draft PR ≠ active contract
- HPRD 草稿 ≠ runtime 授权
- staging accepted ≠ PR merged / production
- Feishu done ≠ GitHub done
- AI draft ≠ 正式对象
- Founder dispatch accepted ≠ engineering start allowed

## 16. 当前切片状态

As of 2026-06-11:

Completed / accepted as evidence only:

- DS-0 Booking Readiness Check / booking staging pilot：`hl-dispatch#195` 已验收关闭，`hl-platform#106` 已合并为 staging / sandbox evidence，`hl-platform#109` 承载 DS-0 readback。
- DS-2 Tenant Entitlement Quota Check-only：`hl-dispatch#177`、`hl-contracts#103`、`hl-platform#113` 已完成 check-only evidence；`hl-dispatch#196` 已作为 DS-2 check-only superseded entry 关闭。
- Formal Object Chain DS-3 到 DS-16 已按各自 readback / decision request / closeout 文档收束；DS-15 只接受 `service_order.lifecycle.observed_state` 单个 descriptive facts catalog row，DS-16 Option A closeout 不授权继续扩展。

Current active staging work order:

- none

Next action:

- none unless Founder / Gate opens a new GitHub SSOT decision or dispatch-ready Founder Spec Lane taskbook.

禁止误读：
- booking staging pilot accepted ≠ production runtime authorization
- `hl-platform#106` merged ≠ MVP pass
- DS-2 check-only completed ≠ full entitlement runtime
- HPRD / PM Draft / Draft PR / CI green / Feishu done / Gate readback ≠ engineering start allowed
- Founder Spec Lane taskbook ≠ production authorization

## 17. 当前能力包处理原则

P0:
- Booking #106 closeout / readiness check

P1:
- biz.sales.order 术语红线修复，统一“手艺人 / 服务人员”
- biz.customer.asset 相邻边界与 Contract Gap 裁决
- biz.service.order Draft PR / blocker
- biz.payment.checkout preflight / blocker

P2:
- biz.tenant.entitlement check-only 工程薄切片

Freeze:
- biz.aftersale.case
- biz.promotion.discount
- biz.performance.commission

Deferred:
- biz.invoice.tax
- biz.payment.channel.settlement

## 18. AI 产品边界

AI 可以：
- 生成 draft
- 生成建议
- 执行代码任务
- 审计
- 压缩上下文
- 报缺口

AI 不得：
- 确认
- 签字
- 拒绝
- 审批
- 创建正式业务对象
- 替代人工验收

正式对象必须经过人工确认 / 签字。

## 19. 唤龙业务红线

- 统一使用“手艺人”
- 不得写回“美疗师 / 美容师”
- 不假设一房一床一人
- GitHub Issue / PR / comment 是任务和裁决证据链
- 飞书只是投影
- GUI 是确认、签字、兜底编辑和人工操作界面，不是主路径

## 20. 当前 PR 不做事项

当前 Delivery Recovery docs/forms PR 不做：
- 不改 workflow
- 不改 Feishu notification
- 不改业务代码
- 不改 runtime
- 不创建新总账 issue
- 不做完整 task platform
- 不全量清理历史 issue

后续独立 PR：
- Feishu issue_comment notification throttle
- Booking readiness check in hl-platform
- Capability integration baseline review issue
- ai-output lint / context validity gate
- action projection exporter
