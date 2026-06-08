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

## 16. 当前优先切片

DS-0 Booking Readiness Check
- 24h 内判断 booking 是否可作为第一交付切片
- pass → DS-1A Booking Runtime Pilot
- fail → DS-1B Runtime Smoke Path

DS-1A Booking Runtime Pilot
- 仅 DS-0 pass 后启动
- 跑通 booking.submit → booking.confirm → booking.arrival.complete
- 输出 PR + integration/smoke test + demo evidence + acceptance report
- 不生产、不真实用户、不扩完整履约

DS-1B Runtime Smoke Path
- DS-0 fail 后启动
- 跑通 runtime 最小冒烟路径
- 不扩业务语义

DS-2 Tenant Entitlement Quota Check-only
- 低风险工程薄切片
- input: tenant_id, capability_id, requested_units
- output: allowed, remaining_quota, reason_code, trace_id
- mock / seed 数据
- 3 个 case：有额度、无额度、unknown tenant
- 不生产、不真实扣减、不接真实计费、不替代 PM 主线

DS-3 Formal Object Chain Snapshot
- 收稳 Sales / CustomerAsset / Service / Payment 当前成熟度与下一步
- 不派售后、优惠、业绩

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
