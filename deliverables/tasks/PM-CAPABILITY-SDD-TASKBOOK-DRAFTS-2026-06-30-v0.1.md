# PM 能力包 SDD 产品任务书草案合集 v0.1

> 日期：2026-06-30  
> 上游任务书：`deliverables/tasks/PM-CAPABILITY-FRONTLOAD-TASKBOOK-2026-06-30-v0.1.md`  
> 上游矩阵：`deliverables/tasks/PM-CAPABILITY-FRONTLOAD-MATRIX-2026-06-30-v0.1.yaml`  
> 状态：PMO draft index for owner completion，owner 尚未回包确认。  
> Founder 裁决：2026-06-30 选择 B；本草案索引按 E 双审意见修正 owner / Gate / STORE-P0 反链口径。

## 中文摘要

本文件是 PM 能力包 SDD 产品任务书草案索引，用于指导各 owner 回填完整产品设计、需求规格、用户流程、验收场景、契约依据和 AI 消费上下文。它只定义任务书格式、owner 草案索引和回包要求，不代表 PM 最终确认，也不授权实现、runtime、部署、生产或发布。

## 术语说明

- SDD 产品任务书：能力包级产品设计 / 需求规格 / PRD，供 Founder、PM、工程 owner、QA 和 AI 实现线程共同消费。
- Owner 回包：PM owner 基于本草案提交自己的最终产品任务书或边界卡。
- 边界卡：P2 / P3 能力包本轮只记录范围、依赖、风险、非目标和复审触发条件，不深写实现规格。
- GATED 边界：支付、真实用户数据、客户资产变更、provider、runtime、生产和发布等必须等待 Founder / Gate 裁决的范围。
- Adjacent 观察项：与本轮 15 个能力包有关但不计入本轮 PM 前置任务的相邻 registry 项。

## 0. 使用边界

本文件是 SDD 产品任务书草案索引，不是轻量准备包，不是 PM 本人最终回包，不是 Founder / Gate 裁决，不是工程 owner 理解确认，也不是 implementation / runtime / deployment / production / release 授权。

每个 PM 最终提交的能力包任务书必须是供人类和 AI 同时消费的完整产品文档，覆盖产品设计、需求规格、用户流程、验收场景、契约上下文和缺口。飞书、Bitable 或本地文件均不能改变 GitHub / `hl-contracts` 的 SSOT 状态。

Founder B 已裁决但仍不授权实现：AfterSales=GATED；Analytics=P2/GATED_READONLY；Product=朱阳 DRI / 邹骢 review；Supply=P2 边界卡；Hardware=PMO+Gate 风险卡；InfraBPM=架构治理；StoreResource / OfferCatalog 必须补 STORE-P0 反链与字段映射。`lifecycle: active` 只表示蓝图 / registry 状态，不等于 runtime、route、生产或发布授权。

## 1. 统一 SDD 任务书骨架

```yaml
pm_sdd_product_taskbook_v1:
  capability_id: "<biz.*>"
  owner: "<github>"
  status: "draft_for_owner_completion | submitted | needs_decision | accepted"
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

## 2. Owner 草案索引

| owner | 能力包 | 深度 | 必须补齐的产品上下文 | GATED 边界 |
|---|---|---|---|---|
| `zoucong121` | `biz.service.order` | P0 SDD 深写 | 服务单对象、状态流、草稿/正式/签字边界、与履约和客户资产的关系 | 不触碰真实资产、支付、履约生产流量、active runtime |
| `zoucong121` | `biz.booking.fulfillment` | P0 SDD 深写 | 预约提交、门店确认、到店承接、异常取消、与 ServiceOrder / CustomerProfile 的依赖 | 不接真实预约流量，不声明 runtime pass |
| `zoucong121` | `biz.payment.checkout` | GATED 规格候选 | 支付业务问题、provider-free 流程、退款/结算/对账缺口 | 不接 provider、真实计费、secrets、staging、production |
| `zhuyang1204` | `biz.store.resource` | P0 SDD 深写 | 门店 App UI 字段、门店资源选择流程、STORE-P0 source anchors、UI flow / fixture field / contract field / acceptance evidence 映射 | 不写生产门店数据，不发布客户端 |
| `zhuyang1204` | `biz.customer.asset` | P0 SDD 深写 | 资产摘要、资产状态解释、只读展示、资产变更非目标 | 不做余额/权益变更、扣减、退款、结算 |
| `zhuyang1204` | `biz.offer.catalog` | P1 SDD 深写 | 服务目录、门店引用、同服务关系、STORE-P0 客户端目录展示和字段映射 | 不上架真实服务，不声明门店 App runtime ready |
| `cuitiantian0704` | `biz.sales.order` | P0 SDD 深写 | 销售单草稿/创建前校验、legacy `biz.flow.sales` 映射、订单依赖 | 不触发库存、支付、履约或资产变化 |
| `cuitiantian0704` | `biz.customer.profile` | P1 SDD 合并 | CP-S2 到 CP-S13 候选合并、客户档案字段、敏感数据边界 | 不升级 lifecycle，不测真实客户数据，不开 active route |
| `zhuyang1204` / review `zoucong121` | `biz.product` | P1 SDD 深写 | 商品中心产品目标、对象、目录关系、legacy `/products` -> `/hk` rewrite、价格 / 上下架商业影响边界 | 不派工程；价格 / 状态 / rewrite 风险需 Gate/架构复核 |
| `PMO_TBD` | `biz.supply.warehouse` | P2 边界卡 | 采购、仓储、供应 reason-code carrier 和依赖 | 暂不深写实现规格，不派工程 |
| `PMO_TBD` | `biz.marketing.promotion` | P2 边界卡 | 优惠、核销、权益影响、CustomerAsset / Payment 依赖 | 触及真实客户价值时 GATED |
| `PMO_TBD` | `biz.analytics.dashboard` | P2 / GATED_READONLY | 只读指标、数据源、可见性、脱敏边界、metric owner、export/share/cross-tenant 禁止项 | 只读 waiver；真实经营数据、导出、分享、跨租户、指标定义变更均 GATED |
| `PMO + Gate` | `biz.hardware.pos` | 风险卡 | POS 终端、provider、支付邻接、硬件 owner 风险 | 硬件集成和支付邻接 GATED |
| `PMO_TBD` | `biz.aftersales.service` | GATED 边界卡 | 售后入口、订单/服务单/资产依赖、退款审批、转卡、补偿风险 | 退款 / 转卡 / 资产影响 GATED |
| `PMO / architecture-governance` | `biz.infra.bpm` | 架构治理线 | 工作流平台属性、跨能力执行路由、部署 / 暂停授权风险 | 不作为普通 PM 能力包派发 |

## 2.1 STORE-P0 反链要求

StoreResource / OfferCatalog 的 owner 回包必须引用以下 source anchors，并提交映射表：

- `huanlongAI/hl-scene-app#56`：STORE-P0 门店客户端父任务 / 客户端入口。
- `hl-scene-app/apps/store-app/README.md`：fixture-only 门店首页工作台范围。
- `hl-scene-app/docs/evidence/issue-56/README.md`：fixture 状态和截图证据。
- 门店 App Figma：`HZxav4vhN8k9OpILNdbR3K`。

映射表最小字段：`UI surface`、`user flow`、`client fixture field`、`contract field`、`acceptance evidence`、`not_allowed`。未提交映射表前，不得进入工程理解确认。

## 3. Adjacent 观察项

- `biz.flow.sales`：legacy broad workflow，只作为 SalesOrder / BookingFulfillment 的动作映射上下文，不单独派工程。
- `biz.tenant.entitlement`：保持 check-only / quota GATED。除非 Founder 明确裁决为 PM-led capability，否则不进入本轮 15 包。

## 4. Owner 回包要求

每个 owner 回包时只允许提交 SDD 产品任务书或边界卡，不得把任务书转成实现派发。回包必须明确：

1. 做什么：产品目标、用户、场景、流程、功能规则。
2. 不做什么：非目标、禁止推断、GATED 范围。
3. 契约依据：Cap-Spec、Acceptance、Reason-Codes、Contract Gap、字段和事件。
4. AI 上下文：术语、别名、禁止推断项、实现前必须补的 evidence。
5. PM 验收：must_pass、must_reject、evidence_required。
6. 首个受限工程切片：仅作为后续工程理解确认的输入，不构成实现授权。

## 5. 授权边界

本草案索引不授权：

- GitHub Issue / PR 写入。
- 飞书通知或群发。
- Bitable / Obsidian / team-memory 写入。
- `hl-contracts` active registry / runtime route 修改。
- 任何实现、迁移、部署、真实用户数据、真实支付、provider、生产或发布动作。
