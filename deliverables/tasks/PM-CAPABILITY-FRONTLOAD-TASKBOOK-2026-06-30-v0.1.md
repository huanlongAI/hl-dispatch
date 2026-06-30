# 唤龙 PM 能力包前置总控任务书 v0.1

> 日期：2026-06-30  
> 状态：PMO frontload baseline / local repo artifact  
> 机器矩阵：`deliverables/tasks/PM-CAPABILITY-FRONTLOAD-MATRIX-2026-06-30-v0.1.yaml`  
> SDD 任务书草案：`deliverables/tasks/PM-CAPABILITY-SDD-TASKBOOK-DRAFTS-2026-06-30-v0.1.md`  
> 真源：GitHub Issue / PR 与 `hl-contracts`。飞书 / Bitable 只做投影。  

## 0. 执行结论

采用 **全量盘点 + 分级深写**。

PM 可以前置，但前置对象是 **SDD 产品任务书 / PRD**，不是工程开工池，也不是轻量“准备包”。当前 `hl-dispatch` snapshot 为 Yellow，`current=4` 已满、`queued=11`，因此 PM 前置线不得增加工程 WIP，也不得把 SDD 产品任务书、PM understanding pass、CI green、飞书认可或 Bitable 状态解释成 runtime / deploy / release 授权。

能力包任务书的定义：一份可供人类和 AI 同时消费的完整产品文档，必须覆盖产品目标、用户/场景、用户流程、功能需求、业务规则、数据与契约上下文、验收场景、非目标、缺口和 Founder/Gate 裁决问题。

本任务书只授权本地文档化 PM 基线，不授权：

- GitHub Issue / PR 写入。
- 飞书通知或群发。
- Bitable / Obsidian / team-memory 写入。
- `hl-contracts` active registry / runtime route 修改。
- 任何实现、迁移、部署、真实用户数据、真实支付、provider、生产或发布动作。

## 1. 状态矩阵

| 能力包 | lifecycle | PM owner | 工件状态 | 优先级 | gated | 唯一下一步 |
|---|---:|---|---|---|---|---|
| `biz.service.order` | candidate-only | `zoucong121` | Cap-Spec / Acceptance / Reason-Codes / Contract Gap 已有 | P0 深写 | 是 | 提交 SDD 产品任务书，命名首个受限服务单切片 |
| `biz.booking.fulfillment` | active | `zoucong121` | Cap-Spec / Acceptance / Reason-Codes / Contract Gap 已有 | P0 深写 | 是 | 补 SDD 任务书增量，明确与 ServiceOrder / CustomerProfile 的依赖切分 |
| `biz.store.resource` | active | `zhuyang1204` | Cap-Spec / Acceptance / Reason-Codes / Contract Gap 已有 | P0 深写 | 否 | 对齐 STORE-P0，产出首个安全工程切片 |
| `biz.customer.asset` | active | `zhuyang1204` | Cap-Spec / Acceptance / Reason-Codes / Contract Gap 已有 | P0 深写 | 是 | 产出不触碰真实资产变更的 SDD 产品任务书 |
| `biz.sales.order` | candidate-only | `cuitiantian0704` | Cap-Spec / Acceptance / Reason-Codes / Contract Gap 已有 | P0 深写 | 否 | 提交 SDD 产品任务书，并澄清与 legacy `biz.flow.sales` 的关系 |
| `biz.customer.profile` | draft_candidate | `cuitiantian0704` | 多个 CP candidate / gap 已有，需汇总 | P1 深写 | 是 | 汇总为 Founder-readable SDD 产品任务书，不升级 lifecycle |
| `biz.offer.catalog` | active | `zhuyang1204` | Cap-Spec / Acceptance / Reason-Codes / Contract Gap 已有 | P1 深写 | 否 | 在 StoreResource 之后补 SDD 任务书增量 |
| `biz.payment.checkout` | draft_candidate | `zoucong121` | Cap-Spec / Acceptance / Reason-Codes / Contract Gap 已有 | GATED | 是 | 只写 provider-free 候选问题，不触发支付实现 |
| `biz.product` | active | `PMO_TBD` | prd/biz 下未见完整 v0.1 工件 | P1 深写 | 否 | PMO 请求 owner 确认后补 SDD 产品任务书 |
| `biz.supply.warehouse` | active | `PMO_TBD` | 仅见 supply reason-code carrier | P2 轻量卡 | 否 | 做边界卡和 owner 建议 |
| `biz.marketing.promotion` | active | `PMO_TBD` | 未见独立工件 | P2 轻量卡 | 是 | 在 CustomerAsset 稳定后做边界卡 |
| `biz.analytics.dashboard` | active | `PMO_TBD` | 未见独立工件；蓝图 key_action=0 | P3 backlog | 是 | 只记录数据边界卡 |
| `biz.hardware.pos` | active | `PMO_TBD` | 未见独立工件 | P3 backlog | 是 | 等 payment/provider/hardware owner 明确 |
| `biz.aftersales.service` | active | `PMO_TBD` | 未见独立工件 | P3 backlog | 否 | 等订单和资产上游稳定 |
| `biz.infra.bpm` | active | `PMO_TBD` | 未见独立工件 | P3 backlog | 是 | Founder 决定是否转架构治理线 |

相邻观察项不计入 15 个 PM 前置能力包：

- `biz.flow.sales`：legacy broad workflow，由 `biz.sales.order` + `biz.booking.fulfillment` 承接 PM 前置；仅保留 action mapping 观察。
- `biz.tenant.entitlement`：当前保持 check-only / quota GATED 治理项；除非 Founder 后续裁决为独立 PM-led capability，否则不进入本轮 15 包。

## 2. SDD 产品任务书统一格式

P0 / P1 深写只允许输出 SDD 产品任务书，不允许输出实现任务。每份任务书必须包含：

```yaml
pm_sdd_product_taskbook_v1:
  capability_id: "<biz.*>"
  owner: "<github>"
  status: "draft | submitted | accepted | needs_decision"
  document_purpose:
    human_consumers: ["Founder", "PM", "engineering_owner", "QA"]
    ai_consumers: ["Codex", "Claude Code", "future implementation agents"]
    expected_use: "product design / requirements spec / PRD / SDD input"
  source_artifacts:
    cap_spec: []
    acceptance: []
    reason_codes: []
    contract_gap: []
  product_goal:
    problem: ""
    target_outcome: ""
    success_metrics: []
  users_and_scenarios:
    users: []
    primary_scenarios: []
    negative_scenarios: []
  user_flows:
    happy_path: []
    exception_paths: []
    cross_capability_dependencies: []
  business_boundary:
    in_scope: []
    out_of_scope: []
  product_rules:
    functional_requirements: []
    business_rules: []
    permission_and_role_rules: []
    data_visibility_rules: []
  data_and_contract_context:
    canonical_objects: []
    fields: []
    events_or_actions: []
    reason_codes: []
    contract_references: []
  ai_consumption_context:
    terms_and_aliases: []
    do_not_infer: []
    evidence_required_before_implementation: []
  first_bounded_engineering_slice:
    description: ""
    allowed: []
    not_allowed: []
  acceptance_scenarios:
    must_pass: []
    must_reject: []
    evidence_required: []
  contract_gaps: []
  founder_or_gate_questions: []
  authorization_boundary:
    implementation_authorized: false
    runtime_authorized: false
    deployment_authorized: false
    production_authorized: false
    release_authorized: false
```

PM understanding pass 只表示工程 owner 读懂业务语义，并且只能在已签定任务书边界内进入受限实现；它不授权 runtime、active registry、真实用户数据、支付、provider、secrets、deploy 或 release。

## 3. P0 SDD 产品任务书指令

### 3.1 `biz.service.order` / 邹骢

目标：把已合并候选四件套转成服务单 SDD 产品任务书。

首个受限工程切片建议：只做服务单生命周期事实读取 / 状态归一的最小闭环，不触碰真实客户资产锁定、扣减、支付、退款、结算、生产数据或运行态注册。

PM 验收必须回答：

- 正式服务单、草稿服务单、已签字服务单的边界。
- 与 BookingFulfillment 的归属边界。
- 哪些 lifecycle facts 只做 observation，不触发业务写入。
- 首个切片的输入、输出、拒绝条件和可审计 evidence。

当前唯一下一步：`zoucong121` 在现有 ServiceOrder SSOT 入口下提交 SDD 产品任务书。

### 3.2 `biz.booking.fulfillment` / 邹骢

目标：补齐 booking 主线与 M4/M5 runtime evidence 相关的 PM delta，但不重新生成整套 Cap-Spec。

首个受限工程切片建议：只围绕预约提交 / 到店承接中一个可验收动作形成 PM acceptance，不扩张到客户资产、支付或生产流量。

PM 验收必须回答：

- `booking.submit`、`booking.confirm`、`booking.arrival.complete` 哪个进入首个切片。
- 依赖 `customer.profile` 的内容是否可用候选证据替代。
- 哪些失败路径只做 Contract Gap，不阻塞本轮 SDD 产品任务书。

当前唯一下一步：`zoucong121` 提交 booking SDD 任务书增量。

### 3.3 `biz.store.resource` / 朱阳

目标：把 StoreResource 规格与 STORE-P0 门店客户端父任务书连接，保证 UI / 用户流程 / 后端切片不各搞一套。

首个受限工程切片建议：只做门店资源读模型或资源选择前置校验，不包含真实排班变更、支付、生产门店数据或发布。

PM 验收必须回答：

- 门店 App 首页工作台需要哪些 store resource 字段。
- 哪些字段来自契约，哪些只是客户端展示候选。
- 第一个后端 slice 如何被 STORE-P0 client flow 验收。

当前唯一下一步：`zhuyang1204` 输出 STORE-P0 对齐 SDD 产品任务书。

### 3.4 `biz.customer.asset` / 朱阳

目标：保留客户资产能力的 PM 前置，但不触碰真实资产变更。

首个受限工程切片建议：只做资产摘要只读 / 资产状态解释 / 验收场景分类，不做储值、扣减、退款、权益发放或结算。

PM 验收必须回答：

- 哪些字段是展示 / 观察，哪些字段会影响客户资产。
- 首个切片如何证明 `data_mutated=false`。
- 哪些资产动作必须进入 Founder / Gate 再裁决。

当前唯一下一步：`zhuyang1204` 在现有 customer asset taskbook 下提交 SDD 产品任务书。

### 3.5 `biz.sales.order` / 崔田恬

目标：把 SalesOrder 候选四件套推进成可交给工程 owner 的 SDD 产品任务书。

首个受限工程切片建议：只做销售单创建前校验或订单草稿语义，不触发库存扣减、支付、履约或真实客户资产变化。

PM 验收必须回答：

- `biz.sales.order` 与 legacy `biz.flow.sales` 的动作映射。
- 与 BookingFulfillment、ServiceOrder、PaymentCheckout 的依赖边界。
- 首个切片的 acceptance cases 和 negative cases。

当前唯一下一步：`cuitiantian0704` 提交 SalesOrder SDD 产品任务书，并维护 SDD 模板质量。

## 4. P1 / GATED 指令

### 4.1 `biz.customer.profile` / 崔田恬

只做候选汇总，不升级 `draft_candidate`。输出应把 CP-S2 到 CP-S13 的候选片段折叠成一份 Founder-readable SDD 产品任务书摘要，明确哪些可以作为 PM 输入、哪些仍是 Contract Gap。

不得输出 active registry、runtime route、真实客户数据测试、声纹真实授权或生产可用结论。

### 4.2 `biz.offer.catalog` / 朱阳

StoreResource P0 SDD 产品任务书之后再补 SDD 任务书增量。重点回答服务项、门店引用、同服务关系与客户端展示的关系。

不得把服务目录 ready 解释为门店 App 或后端 runtime ready。

### 4.3 `biz.payment.checkout` / 邹骢

只允许 provider-free 候选总结。可列支付业务问题、provider gap、风控 gap、退款 / 结算 gap，但不得进入真实 provider、真实计费、退款、结算、secrets、staging、production 或 release。

任何后续动作都需要 Founder / Gate receipt。

### 4.4 `biz.product` / PMO 待分配

蓝图是 active，但 `prd/biz` main 未见完整 v0.1 四件套。PMO 先做 owner confirmation 候选，不直接派工程。

建议最小下一步：Founder 确认由谁承接 `biz.product` SDD 产品任务书；确认前只做缺口记录。

## 5. P2 / P3 轻量卡

P2 / P3 本轮不深写 SDD 产品任务书，只写边界卡。边界卡字段：

```yaml
pm_boundary_card_v1:
  capability_id: "<biz.*>"
  current_blueprint_status: ""
  why_not_deep_write_now: ""
  likely_owner: "PMO_TBD | <github>"
  dependencies: []
  risks: []
  next_review_trigger: ""
```

轻量卡对象：

- `biz.supply.warehouse`：有 supply reason-code carrier，但缺 PM 四件套。
- `biz.marketing.promotion`：依赖 customer asset 与 payment 边界。
- `biz.analytics.dashboard`：蓝图 key_action=0，先做数据访问边界。
- `biz.hardware.pos`：硬件和支付相邻，暂缓。
- `biz.aftersales.service`：等订单与资产上游稳定。
- `biz.infra.bpm`：可能应进入架构治理线，而不是普通 PM 能力包。

相邻观察卡：

- `biz.flow.sales`：legacy broad workflow，需要映射到 SalesOrder / BookingFulfillment。
- `biz.tenant.entitlement`：保持 check-only / quota GATED；未裁决前不写 reserve / confirm / refund / real billing SDD taskbook。

## 6. PMO 监测口径

PMO 每周只读复核一次：

1. `hl-dispatch/scripts/export-hl-progress.py --snapshot` 的 Green / Yellow / Red 状态。
2. 工程 `current` 是否仍为 4 条以内。
3. 本任务书矩阵中 15 个能力包是否都有 owner / status / gap / next_action。
4. P0 / P1 SDD 产品任务书 是否仍未被误读为实现授权。
5. GATED 项是否出现 provider、真实用户数据、生产、deploy、release 或权限扩大迹象。

若出现 PM 产物被误读为 runtime / deploy / release 授权，PMO 必须标记 `status_reconcile_candidate`，不自动写 GitHub，不自动关闭 Issue，不自动通知飞书。

## 7. 验收标准

- 15 个 PM 前置能力包全部出现在矩阵中，`biz.flow.sales` 与 `biz.tenant.entitlement` 只作为 adjacent registry item 观察。
- P0 / P1 / GATED / P2 / P3 分类明确。
- 每个能力包都有唯一下一步。
- 每个已分配能力包都有 GitHub handle owner。
- `PMO_TBD` 只用于待 Founder 分配的 backlog，不得派工程。
- 所有 GATED 项均明确 `runtime_authorized=false`、`deployment_authorized=false`、`production_authorized=false`、`release_authorized=false`。
- 本任务书不产生外部写入、飞书通知、GitHub comment、Bitable 更新或运行态授权。
