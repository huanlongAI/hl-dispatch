# 唤龙平台能力包规则、规划逻辑与进展评审材料

> Status: REVIEW_MATERIAL_DRAFT
> Date: 2026-06-13
> Prepared by: Codex Desktop / NODE-M
> Scope: capability package rules, planned list, planning logic, current progress
> Boundary: 本文是评审、复盘、研究材料；不替代 `hl-contracts`、GitHub Issue / PR、Founder / Gate 裁决，也不授权 runtime、HPRD、工程开工、生产发布或真实业务数据接入。

## 中文摘要

本文整理唤龙平台能力包的规则、规划逻辑和当前推进状态，用于交付恢复与治理复盘。核心结论是：能力包不是传统模块清单，而是围绕业务价值流、契约真源、PM 规格、双端交互、Gateway / HK Kernel 接入和 runtime readiness 的分层机制。本文仅作为 review material draft 保存，不改变 `hl-contracts`、GitHub Issue / PR、Founder / Gate 裁决或 runtime 授权边界。

## 术语说明

| 术语 | 说明 |
|---|---|
| 能力包 / Capability Package | 围绕业务价值流闭环定义的可审查业务能力边界，不等于代码模块名或一次性 PRD。 |
| Cap-Spec | PM 产出的能力规格工件，通常包含能力规格、验收场景、reason_code 提案和 Contract Gap。 |
| Human End | 人类确认、审查、兜底、审计和确定性操作界面，高风险动作必须保留人类确认面。 |
| Agent End | Agent 可调用的工具、schema、权限、上下文预算、重试、去重和证据路径，不得绕过 Gateway / HK Kernel。 |
| Runtime capability | `hl-platform` 中可被 Gateway / runtime registry 识别和调度的运行态能力；staging evidence 不等于生产授权。 |

## 0. 结论摘要

唤龙平台“能力包”当前不是传统模块清单，而是一套从业务价值流、契约治理、PM 规格、双端交互、Gateway / HK Kernel 接入到 runtime readiness 的分层机制。

当前可确认的规划事实：

1. Founder Signed 首批能力包为 4 个：`biz.offer.catalog`、`biz.store.resource`、`biz.customer.profile`、`biz.booking.fulfillment`。
2. `hl-contracts/rules/biz-capabilities-blueprint.yaml` 当前规划 15 个 `biz.*` 能力包，合计 128 个 `key_action`、6 个 `ordinary_action`。
3. 2026-06-07 PM 双端评审覆盖 15 个能力包：13 个 `BLOCKED`、1 个 `PATCH_REQUIRED`、1 个 `PASS_WITH_WAIVER`。这些结论均不等于 runtime 授权。
4. `hl-platform` 目前只看到 3 个 `biz/*` pilot manifest：`biz.booking.fulfillment`、`biz.tenant.entitlement`、`biz.demo`。其中 `biz.demo` 是样板，不是业务包；`biz.tenant.entitlement` 是 check-only；`biz.booking.fulfillment` 是 pilot/staging 证据链，不能误读为 MVP、生产或已合并交付。
5. 当前真正的瓶颈不是“还没列清功能”，而是每个能力包从 PM 语义到工程入口之间缺少可审查闭环：Human End、Agent End、Gateway / Can path、reason_code trace、OpenAPI / events / facts、idempotency、审计证据、外部依赖退出路径、Gate H 人审记录。

## 1. 证据来源与优先级

### 1.1 本次读取的主要证据

| 层级 | 文件 | 作用 |
|---|---|---|
| Founder 上游 | `hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md` | 首批 4 个能力包、PM 分工、首切片链路、工程开工门槛。 |
| PM 启动 | `hl-dispatch/deliverables/decisions/PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS-v0.1.md` | PM 产出 Cap-Spec 的工作法和禁区。 |
| 能力注册蓝图 | `hl-contracts/rules/biz-capabilities-blueprint.yaml` | 15 个 `biz.*` 能力包、生命周期、key_action / ordinary_action 设计态清单。 |
| Schema | `hl-contracts/rules/schemas/capabilities.schema.yaml` | `capabilities.yaml` 的结构、lifecycle、key_action / ordinary_action 语义。 |
| PM 双端评审 | `hl-contracts/docs/pm/capabilities/*/DUAL-END-PM-REVIEW.md` | 15 个能力包的人端 / Agent 端 readiness 评审。 |
| Cap-Spec 工件 | `hl-contracts/prd/biz/` | PM 能力规格、验收场景、reason_code 提案、Contract Gap。 |
| Runtime 设计 | `hl-platform/docs/design/HK-BIZ-CAPABILITY-MODULE-DESIGN.md` | `biz/*` module 落点、AutoConfiguration、manifest、runtime 触点。 |
| Runtime gate | `hl-platform/docs/design/HK-CAPABILITY-INTEGRATION-GATE-v1.md` | capability readiness gate、READY / PARTIAL / BLOCKED 语义。 |
| Recovery 快照 | `hl-dispatch/docs/delivery-recovery/CAPABILITY_INTEGRATION_BASELINE_2026-06-07.md` | Delivery Recovery Mode 下的能力包成熟度和当前队列。 |
| PM lane taskbook | `hl-dispatch/deliverables/tasks/*CAPABILITY-LANE-TASKBOOK-2026-06-12-v1.0.md` | `biz.sales.order`、`biz.customer.asset` 的 PM-led capability lane。 |

### 1.2 权威边界

| 问题 | 权威来源 | 本文处理方式 |
|---|---|---|
| 契约、reason_code、OpenAPI、events、facts、capability registry | `hl-contracts` | 只引用，不复制为新真源。 |
| 任务、反馈、裁决、review 留痕 | GitHub Issue / PR / repo file | 飞书、Project、Base 只作为 projection。 |
| runtime 实现与模块落点 | `hl-platform` | 只描述现状，不授权新增 runtime。 |
| 团队调度与 PM taskbook | `hl-dispatch` | 本文放在 `hl-dispatch` 作为研究材料。 |
| 人类签字与高风险授权 | Founder / Gate / Human Gate H | DRAFT、checks success、staging evidence 均不能替代。 |

## 2. 概念定义

| 概念 | 含义 | 常见误读 |
|---|---|---|
| 能力包 Capability Package | 围绕一个业务价值流闭环定义的可审查业务能力边界，包含目标、非目标、key_action、验收、reason_code 提案、Contract Gap。 | 不是传统大 PRD，也不是代码模块名称。 |
| Cap-Spec | PM 产出的能力规格工件。通常至少包括 Cap-Spec-1 能力规格、Cap-Spec-2 验收场景、Cap-Spec-3 reason_code 提案、Contract Gap。 | DRAFT Cap-Spec 不等于 active contract。 |
| `key_action` | 改变业务事实、治理事实、审计事实或资源占用的关键动作，必须触发 Can -> Action -> Audit。 | 不能把普通读取、AI 草稿、推荐候选都升级为 key_action。 |
| `ordinary_action` | 普通审计动作候选，只用于建立 OpenAPI / reason_code / event 引用闭环，不触发完整治理机制。 | 不授权 runtime 路由、HPRD 或工程开工。 |
| Human End | 人类确认、审查、兜底、审计和确定性操作界面。 | GUI 不是 NUI 失败后的低级补丁；高风险动作必须有人类确认面。 |
| Agent End | Agent 可调用的工具、schema、权限、上下文预算、重试、去重和证据路径。 | Agent 不得绕过 Gateway / HK Kernel，也不得替人确认正式业务事实。 |
| Runtime capability | `hl-platform` 中可被 Gateway / runtime registry 识别和调度的运行态能力。 | module manifest / staging evidence 不等于生产授权。 |

## 3. 能力包全局规则

### 3.1 真源规则

1. `hl-contracts` 是 capability registry、rules、reason_code、OpenAPI、events、facts 的契约 SSOT。
2. `hl-dispatch` 承载任务书、PM lane、交付恢复快照和调度材料。
3. `hl-platform` 承载运行态实现和 runtime gate。
4. GitHub PR / Issue / repo file 是正式证据链；飞书、Project、Base、聊天记录均为 projection。
5. 未经 Founder / Gate 确认的 AI 草稿、PM 过程文档、飞书讨论、DRAFT PR 不得当作决定。

### 3.2 设计规则

能力包必须服务主价值流：

```text
Natural interaction intent
-> intent_candidate
-> AI draft
-> human confirmation / signature
-> formal booking / sales / service object
-> payment / asset / fulfillment linkage
-> audit evidence
```

首批 Founder Signed 链路更具体：

```text
自然交互意图
-> AI Draft
-> Appointment Intent Hold
-> Qualified Resource Hold
-> GUI Confirm
-> Confirmed Booking
-> Fulfillment
-> Audit Evidence
```

硬约束：

1. AI / NUI 可以生成候选、建议、草稿、审计和缺口报告；不能确认、签字、拒绝、批准、创建正式业务对象或替代人工验收。
2. GUI 是确认、主动操作、降级、治理和审计界面，不是可删除的附属物。
3. 改变状态、资源占用、资金、客户身份、隐私、合同或正式对象的动作必须走 Can -> Action -> Audit。
4. 未注册、未启用、契约不合规、权限不明、证据缺失时必须 fail-secure。
5. 高风险能力必须定义 idempotency、重试 / 去重、审计证据、失败 reason_code 和人工确认。

### 3.3 PM 交付规则

每个能力包至少应有：

| 交付物 | 作用 |
|---|---|
| Cap-Spec-1 | 能力规格：边界、目标、非目标、业务规则意图、上游引用。 |
| Cap-Spec-2 | 验收场景：输入、预期、验收方式、审计要求。 |
| Cap-Spec-3 | reason_code 提案：触发场景、业务含义、命名候选。 |
| Contract Gap | 需要 Founder / Gate / 工程补齐的契约缺口。 |
| 首切片验收说明 | 说明如何从意图走到正式对象和审计证据。 |
| 跨包依赖表 | 写清依赖谁、读取什么、输出什么、不得重定义什么。 |

### 3.4 工程开工门槛

工程开工至少需要同时满足：

1. Cap-Spec 四件套已进入可审查状态。
2. P0/P1 Contract Gap 已解决、豁免或明确作为 blocker。
3. `capability_id`、`key_action`、reason_code、OpenAPI / event / facts 落点明确。
4. Gateway / Protocol Gate 路由和 Can check 明确。
5. HK.Policy / HK.Audit / HK.ID / HK.Consent 触发点明确。
6. Human Gate H 语义审查记录明确。
7. `hl-platform` capability readiness gate 不处于 `BLOCKED`。

`PARTIAL` 只能表示证据路径存在，不表示 engineering start。

### 3.5 Runtime 接入规则

`hl-platform/docs/design/HK-BIZ-CAPABILITY-MODULE-DESIGN.md` 定义的正式 `biz/*` runtime 入口：

1. 每个 capability 一个独立 Gradle module：`biz/<module>/`。
2. runtime 装配走 `Spring Boot AutoConfiguration + CapabilityHandler`。
3. 新 capability 优先改模块和注册表，不改 shared runtime 核心。
4. `app/src/main/resources/*.yaml` 只保留 HK base 与全局 fallback；`biz/*` 不应为注册自己回改 app 资源。
5. 正式模块必须有 `capability-manifest.yaml`、`runtime-compatibility.yaml`、`acceptance-manifest.yaml` 和基础 fixture。
6. 对已实现 action，至少有 happy / failure 两类 fixture，并让 `failure_samples` 与 acceptance manifest 对齐。
7. 对应 `hl-contracts/rules/biz-capabilities-blueprint.yaml` 必须登记，不能靠本地例外绕过 gate。

## 4. 规划逻辑与原理

### 4.1 从价值流切能力，而不是从菜单切模块

能力包不是“客户管理、商品管理、订单管理”的传统菜单拆分。它首先回答：

1. 用户或操作员要完成哪条价值流？
2. 哪些业务事实会被正式改变？
3. 哪些动作需要人工确认、治理裁决、审计证据？
4. 哪些上游能力只被引用，不能在本包重定义？
5. 哪些内容现在只能成为 Contract Gap？

这也是 `biz.customer.profile` taskbook 反复强调的原则：能力包是“用户价值流闭环的可审查规格切片”，不是传统大 PRD。

### 4.2 能力包的三层结构

```text
PM 语义层
  - Cap-Spec / Acceptance / Reason-Codes proposal / Contract Gap

契约治理层
  - capability registry / key_action / reason_code / OpenAPI / events / facts / rules

运行态接入层
  - Gateway route / HK Policy / HK Audit / handler / manifest / readiness gate / CI
```

任何一层缺失，都不能把能力包宣称为可工程开工或可生产。

### 4.3 Human End 与 Agent End 同构

唤龙能力包规划的核心不是“AI 代替人”，而是把同一套业务真相同时投射给：

1. 人：GUI / NUI / 审查 / 确认 / 审计 / 异常处理。
2. Agent：工具 schema / permission / context budget / retry / idempotency / evidence。

两端必须共享同一套 state、reason_code、event_id、audit_ref、trace_id 和 Gateway / HK path。

### 4.4 风险驱动的 key_action 设计

`key_action` 的判断标准不是动作是否“常用”，而是是否改变正式事实或高风险状态。例如：

1. AI Draft 生成草稿通常不是 key_action。
2. Hold 创建 / 续期 / 释放、正式确认、取消、退款、资产扣减、客户合并、敏感可见性等必须进入 key_action 或至少进入强审计候选。
3. `ordinary_action` 可以建立普通审计引用，但不得冒充完整治理动作。

### 4.5 成熟度不等于完成度

Delivery Recovery 快照定义 M0-M9：

| Level | Name | 含义 | 禁止误读 |
|---|---|---|---|
| M0 | observation_candidate | 观察到的候选 | 不派发、不工程开工。 |
| M1 | session_candidate_locked | 会话候选锁定 | 不是正式任务。 |
| M2 | draft_candidate_baseline | 草稿候选基线 | 不是 active contract。 |
| M3 | hprd_understanding_confirmed | HPRD 理解确认 | 不是 runtime 授权。 |
| M4 | contract_draft_pr | 契约 Draft PR | checks success 不是 ready。 |
| M5 | active_contract_baseline | 已合并契约基线 | 受控拆解，不是生产 ready。 |
| M6 | runtime_candidate | runtime 候选 | sandbox / staging，不是 MVP。 |
| M7 | staging_evidence_accepted | staging 证据接受 | 不是 PR merged 或 production。 |
| M8 | internal_mvp_accepted | 内部 MVP 接受 | 不是生产发布。 |
| M9 | production_authorized | 生产授权 | 需要 release / security / product 证据。 |

## 5. 全部已规划清单

### 5.1 Founder Signed 首批能力包

| capability_id | 中文名 | 原 PM 分工 | 核心边界 |
|---|---|---|---|
| `biz.offer.catalog` | 供给目录 | PM-1 朱阳 | 商户提供什么服务、服务需要什么资源、服务规则。 |
| `biz.store.resource` | 门店与资源 | PM-1 朱阳 | 门店、房间、服务位、整房规则、手艺人、可预约资源。 |
| `biz.customer.profile` | 客户档案 | PM-2 邹骢，后续 taskbook 显示崔田恬承接 | 客户主体识别、基础档案、预约关联。 |
| `biz.booking.fulfillment` | 预约与履约 | PM-2 邹骢 | 自然交互预约、AI 草稿、资源暂占、人工确认、正式预约、到店履约。 |

### 5.2 `hl-contracts` blueprint 规划 15 包

本表来自 `hl-contracts/rules/biz-capabilities-blueprint.yaml`，属于设计态规划，不等于 runtime 已启用。

| 序 | capability_id | 中文名 | lifecycle | key_action 数 | ordinary_action 数 | 当前理解 |
|---:|---|---|---|---:|---:|---|
| 1 | `biz.flow.sales` | 销售服务工作流 | active | 6 | 0 | legacy / 待决定 retire、migrate 或 rewrite。 |
| 2 | `biz.booking.fulfillment` | 预约与到店承接 | active | 19 | 0 | 有 OpenAPI / events / reasoncodes / runtime pilot manifest；仍有 PM 双端 PATCH。 |
| 3 | `biz.customer.profile` | 客户档案 | draft_candidate | 9 | 6 | Cap-Spec baseline frozen，但 HPRD / runtime blocked。 |
| 4 | `biz.tenant.entitlement` | 租户权益与 AI 用量 | draft_candidate | 1 | 0 | DS-2 check-only pilot；不是真实计费或生产扣减。 |
| 5 | `biz.offer.catalog` | 服务目录 | active | 11 | 0 | 首批 4 包之一；PM / Gate 证据存在，Gateway / OpenAPI 等未闭环。 |
| 6 | `biz.store.resource` | 门店资源 | active | 46 | 0 | 首批 4 包之一；QRH / 资源侧最重，Gateway / 状态机仍未闭环。 |
| 7 | `biz.customer.asset` | 客户与资产管理 | active | 7 | 0 | 已进入 PM-led lane，但只授权 PM readiness，不授权 runtime。 |
| 8 | `biz.payment.checkout` | 收银与支付结算 | active | 5 | 0 | 资金高风险，PM preflight / candidate-only，不授权真实支付。 |
| 9 | `biz.marketing.promotion` | 营销促销 | active | 8 | 0 | candidate / blocked，不在当前 recovery active delivery。 |
| 10 | `biz.product` | 商品中心 | active | 3 | 0 | legacy PRD，需要按当前 `/hk` Gateway path 重写。 |
| 11 | `biz.supply.warehouse` | 采购与仓库 | active | 5 | 0 | dependency / risk-retirement，只识别 blocker，不授权广义 runtime。 |
| 12 | `biz.analytics.dashboard` | 数据分析仪表盘 | active | 0 | 0 | read-only，PM 双端 `PASS_WITH_WAIVER`，仍需 endpoint/schema/metric owner。 |
| 13 | `biz.hardware.pos` | POS 终端 | active | 2 | 0 | blocked，需要设备生命周期、供应商退出、security approval。 |
| 14 | `biz.aftersales.service` | 售后处理 | active | 4 | 0 | candidate only，当前 recovery 明确不进入 active delivery。 |
| 15 | `biz.infra.bpm` | 工作流引擎 | active | 2 | 0 | blocked，尤其需要防止 workflow / Agent 绕过 Gateway。 |

合计：15 个能力包、128 个 `key_action`、6 个 `ordinary_action`。

### 5.3 Recovery / PM lane 当前清单

来自 2026-06-07 recovery baseline 和 2026-06-12 PM lane taskbook。

| 包 / 队列项 | 当前 lane | 当前成熟度 / 状态 | 下一步 | 禁止误读 |
|---|---|---|---|---|
| P0.5-A `biz.intent.capture` | waiting_hprd_draft | M0-M1 | Draft HPRD candidate 和确认边界 | 不授权 runtime / formal object creation。 |
| P0.5-B `biz.ai.draft.confirmation` | waiting_hprd_draft | M0-M1 | 定义 AI draft -> human confirmation contract | AI 不得确认 / 签字。 |
| P0.5-C cross-cutting dependencies | waiting_owner_action | M1-M2 | 映射 booking / sales / service / payment / asset 依赖 | 不做 broad platform build。 |
| `biz.customer.asset` | P1 formal object chain | M2-M3 / PM lane ready | PM readiness pack，Contract Gap decision | 候选 merge 不授权 active contract 或 runtime。 |
| `biz.sales.order` | P1 formal object chain | merged_draft_candidate / PM lane ready | PM readiness pack，术语红线修复 | 不授权 provider / payment / billing / runtime。 |
| `biz.service.order` | P1 formal object chain | M2-M4 | Draft PR / blocker / ETA revision | 默认不授权 service runtime。 |
| `biz.payment.checkout` | P1 formal object chain | M2-M3 | PM preflight 或 blocker | 不接真实支付 / 退款 / 结算。 |
| `biz.tenant.entitlement` | P2 engineering thin slice | M5/M6 check-only | DS-2 quota check-only，mock / seed data，3 cases | check-only 不是生产权益扣减。 |
| Booking staging pilot | P0 closeout / DS-0 | M7 evidence accepted, closeout open | 关闭 `hl-platform#106`：merge / split / close superseded | staging accepted 不是 MVP / production / merged。 |
| Supply / Resource | dependency / risk-retirement | M1-M3 | 只识别 booking / service / asset blocker | 不授权 broad supply runtime。 |
| CustomerProfile | dependency candidate | M1-M2 | 明确 customer asset / identity 边界 | 不独立 active delivery。 |
| HK cross-cutting contracts | platform dependency | M5-M6 | 对齐 registry / reason_code / event taxonomy | 不允许 hidden contract changes。 |
| `biz.aftersale.case` | candidate_queue | candidate only | 观察 / 分类 | 不进入当前 active delivery。 |
| `biz.promotion.discount` | candidate_queue | candidate only | 观察 / 分类 | 不进入当前 active delivery。 |
| `biz.performance.commission` | candidate_queue | candidate only | 观察 / 分类 | 不进入当前 active delivery。 |
| `biz.invoice.tax` | deferred | deferred | 后续决策 | 当前不规划 active delivery。 |
| `biz.payment.channel.settlement` | deferred | deferred | 后续决策 | 当前不规划 active delivery。 |

### 5.4 PM 双端评审结果

来自 `hl-contracts/docs/pm/capabilities/*/DUAL-END-PM-REVIEW.md`。

| capability_id | current_stage | result | 主要缺口 |
|---|---|---|---|
| `biz.aftersales.service` | unknown | BLOCKED | state machine、GUI 高风险确认、reason_code、Gateway、idempotency、证据、外部依赖退出。 |
| `biz.analytics.dashboard` | unknown | PASS_WITH_WAIVER | read-only 边界保留；仍需 endpoint/schema、reason_code binding、data source inventory、metric owner。 |
| `biz.booking.fulfillment` | PRD | PATCH_REQUIRED | Human End、Agent manifest、override owner matrix、retry / duplicate policy。 |
| `biz.customer.asset` | unknown | BLOCKED | Cap-Spec 去留、state machine、reason_code trace、Human End、Agent manifest、Gateway、idempotency、证据。 |
| `biz.customer.profile` | PM-ready | BLOCKED | Founder / Gate 授权、Gateway route、can_check、idempotency、Agent manifest、Human End、privacy context budget。 |
| `biz.flow.sales` | unknown | BLOCKED | retire / migrate / rewrite 决策、当前 PM Cap-Spec、state machine、reason_code trace。 |
| `biz.hardware.pos` | unknown | BLOCKED | device lifecycle、vendor exit path、reason_code、security approval。 |
| `biz.infra.bpm` | unknown | BLOCKED | workflow state machine、side-effect model、Agent no-bypass controls。 |
| `biz.marketing.promotion` | unknown | BLOCKED | Cap-Spec 或 retire、targeting/evidence、reason_code、Gateway。 |
| `biz.offer.catalog` | PRD | BLOCKED | OpenAPI / Gateway path、idempotency、Human End、Agent manifest、IAM matrix。 |
| `biz.payment.checkout` | unknown | BLOCKED | payment/refund state machine、provider sovereignty、idempotency、financial audit。 |
| `biz.product` | PRD | BLOCKED | 按当前 `/hk` Gateway 重写、reason_code trace、events/facts audit。 |
| `biz.store.resource` | PRD | BLOCKED | OpenAPI / Gateway、normalized state machine、QRH retry/idempotency。 |
| `biz.supply.warehouse` | unknown | BLOCKED | procurement / inventory state machine、reason_code、Gateway、外部退出。 |
| `biz.tenant.entitlement` | PRD | BLOCKED | formal registry、OpenAPI/schema、facts/events、Gateway、Tool/API、IAM。 |

### 5.5 `hl-contracts/prd/biz` 已落库的主要 Cap-Spec 包

这些文件存在于仓库中，但大多数标题或正文明确是 `DRAFT`、`candidate-only`、`proposal only` 或 `草案`。存在文件不等于 active contract。

| 能力包 / 子包 | 已见工件 |
|---|---|
| `biz.booking.fulfillment / booking` | Cap-Spec-1、Acceptance、Reason-Codes、Contract Gap。 |
| `biz.booking.fulfillment / fulfillment` | Cap-Spec-1、Acceptance、Reason-Codes、Contract Gap。 |
| `biz.customer.profile` | CP-S2 至 CP-S13 多个候选、Contract Gap、freeze readiness、active registration plan。 |
| `biz.offer.catalog` | Cap-Spec-1、Acceptance、Reason-Codes、Contract Gap。 |
| `biz.store.resource` | Cap-Spec-1、Acceptance、Reason-Codes、Contract Gap。 |
| `biz.customer.asset` | Cap-Spec-1、Acceptance、Reason-Codes、Contract Gap。 |
| `biz.sales.order` | Cap-Spec-1、Acceptance、Reason-Codes、Contract Gap。 |
| `biz.service.order` | Cap-Spec-1、Acceptance、Reason-Codes、Contract Gap，以及 Formal Object Chain DS 系列 gap。 |
| `biz.payment.checkout` | Cap-Spec-1、Acceptance、Reason-Codes、Contract Gap。 |
| `biz.tenant.entitlement` | Cap-Spec-1、Acceptance、Reason-Codes、Contract Gap；另有 RRS-TE-0 check-only gap。 |
| `biz.intent.capture` P0.5-A | Cap-Spec、Acceptance、Reason-Codes，但已收窄为业务理解 / gap / 待裁决材料。 |
| `biz.ai.draft.confirmation` P0.5-B | AI 草稿与人工确认候选。 |

### 5.6 `hl-platform` runtime / pilot 现状

| capability_id | module | manifest status | action 数 | 当前判断 |
|---|---|---|---:|---|
| `biz.demo` | `hl-platform/biz/demo` | pilot | 2 | runtime 样板，不是业务能力包规划结果。 |
| `biz.booking.fulfillment` | `hl-platform/biz/booking-fulfillment` | pilot | 19 | 有 module-local registry、route bindings、runtime policy baseline、acceptance/runtime compatibility；仍不能误读为生产或 MVP。 |
| `biz.tenant.entitlement` | `hl-platform/biz/tenant-entitlement` | pilot | 1 | DS-2 quota check-only，mock / seed / demo 边界，不接真实计费。 |

`hl-platform/app/src/main/resources/capabilities.yaml` 当前只保留 HK base：

| capability_id | lifecycle | key_action 数 |
|---|---|---:|
| `hk.id` | active | 2 |
| `hk.orglink` | active | 0 |
| `hk.policy` | active | 0 |
| `hk.consent` | active | 2 |
| `hk.audit` | active | 0 |
| `hk.reasondict` | active | 1 |
| `hk.worldgraph` | disabled | 7 |

这与 runtime 设计一致：`biz/*` 新 capability 不应为了注册自己回改 app 三份资源，而应使用 module-local `META-INF/hl-platform/*`。

## 6. 当前进展判断

### 6.1 已完成 / 已形成的东西

1. Founder Signed 首批 4 能力包上游任务书已锁定。
2. PM Codex 启动手册已形成，明确 PM 只做 Cap-Spec，不直接工程开工。
3. `hl-contracts` 已有 15 包 blueprint，覆盖关键动作、风险等级和部分 draft_candidate。
4. `hl-contracts/docs/pm/capabilities` 已有 15 个 PM 双端评审。
5. `hl-contracts/prd/biz` 已沉淀多个 DRAFT / candidate-only 能力包工件。
6. `hl-platform` 已有 runtime capability module design 和 readiness gate 设计。
7. `hl-platform` 已有 `biz.booking.fulfillment` 与 `biz.tenant.entitlement` pilot module manifest。
8. Delivery Recovery Mode 已把能力包纳入 M0-M9 成熟度模型和 waiting / candidate / deferred 队列。
9. 2026-06-12 已为 `biz.sales.order`、`biz.customer.asset` 建立 PM-led capability lane taskbook。

### 6.2 尚未完成 / 不能宣称完成的东西

1. 大多数能力包没有 formal Gateway / Can path。
2. 多数能力包没有完整 Human End surface。
3. 多数能力包没有 Agent manifest、tool pruning、context budget。
4. 多数能力包缺少 idempotency、retry / duplicate prevention。
5. 多数能力包缺少正式 reason_code trace、OpenAPI、events、facts 和 audit evidence 闭环。
6. 多数能力包没有 Gate H 人审记录。
7. `hl-platform/PROGRESS.json` 滞后到 2026-03-26，不能作为当前真实进展的唯一依据。
8. `hl-scene-app` 本地工作区 dirty 且远端分支 gone，本次未作为能力包进展依据。
9. 当前没有证据支持“能力包体系已经 production_authorized”。

### 6.3 关键风险

| 风险 | 表现 | 后果 |
|---|---|---|
| DRAFT 误读为 active contract | 文件已合并或 checks success 就当可开工 | 工程基于未审语义开工，后续重做。 |
| staging 误读为 MVP | Booking staging evidence accepted 被叫成 MVP / production | 发布、验收、责任边界混乱。 |
| runtime manifest 误读为生产授权 | module 有 `runtime_registry.lifecycle: active` 就当生产 active | 绕过 Gate / Founder / release。 |
| Agent 绕过 Gateway | 直接让 Agent 调业务动作 | 破坏 Can -> Action -> Audit。 |
| 模块思维吞噬能力包 | 把资产、会员、营销、支付都塞进 customer/profile | 边界失控，Contract Gap 被伪装成答案。 |
| 术语回退 | 写回 `美疗师` / `美容师` 或一房一床一人 | 违反全局红线和服务业世界模型。 |

## 7. 研究性结论

### 7.1 能力包体系的本质

唤龙能力包体系是一种“业务语义可审查化 + 治理动作显式化 + runtime 接入门禁化”的机制。它的目标不是快速生成模块，而是让每个业务能力在进入工程前，先回答：

1. 业务事实是什么？
2. 谁可以确认？
3. 哪些动作改变正式事实？
4. 失败如何安全退出？
5. 人和 Agent 是否看到同一套真相？
6. 每个动作能否被审计、回放、追责？

### 7.2 当前规划的主脉络

当前规划已从“首批预约闭环 4 包”扩展为三条主脉络：

1. P0 / Booking closeout：围绕自然交互预约、AI draft、人类确认、正式预约、履约、审计。
2. P1 / Formal Object Chain：围绕 SalesOrder、ServiceOrder、CustomerAsset、PaymentCheckout 等正式对象链。
3. P2 / Engineering thin slice：围绕 Tenant Entitlement check-only 等低风险工程薄切片。

扩展包如 aftersales、promotion、performance、invoice、settlement 当前应保持 candidate / deferred，不应抢占 active delivery。

### 7.3 下一步最小有效动作

优先级建议：

1. 先关闭 Booking staging pilot 的状态误读：明确 `hl-platform#106` 是 merge、split follow-up 还是 close superseded。
2. 对 `biz.sales.order` 和 `biz.customer.asset` 收 PM readiness pack，不能直接派工程实现。
3. 为 `biz.booking.fulfillment` 补 PM 双端评审要求的 PATCH：Human End、Agent manifest、override matrix、retry / duplicate policy。
4. 对 `biz.customer.profile` 只推进 Founder / Gate 授权的下一 contract phase，不直接开 runtime。
5. 为 `biz.offer.catalog` / `biz.store.resource` 补 Gateway / OpenAPI / idempotency / approval matrix，否则首批供给侧仍无法工程化。
6. 建立一张 capability readiness dashboard，字段至少包括：capability_id、maturity、Cap-Spec 状态、Contract Gap 状态、Gateway path、reason_code trace、Human End、Agent End、runtime manifest、Gate H、not_authorized。

## 8. 复盘检查清单

评审任何能力包时，按下面顺序问：

1. 这个包是否有明确价值流，不是菜单模块？
2. 是否写清 scope in / scope out？
3. 是否有 Cap-Spec-1 / 2 / 3 / Contract Gap？
4. 是否只引用 `hl-contracts` 真源，没有复制 Tier 1 SSOT？
5. 是否列出 key_action，且每个 key_action 都有 risk_level？
6. 是否区分 key_action 与 ordinary_action？
7. 是否有 Human End 确认 / 审查 / 审计 / 异常处理面？
8. 是否有 Agent End tool schema / permission / context budget / retry / idempotency？
9. 是否有 Gateway / Can path？
10. 是否有 HK.Policy / HK.Audit / HK.ID / HK.Consent 触发点？
11. 是否有 reason_code trace、OpenAPI、events、facts？
12. 是否有 failure fixture / acceptance manifest / readiness gate？
13. 是否有 Gate H 人审记录？
14. 是否明确 `not_authorized`？
15. 是否避免把 DRAFT、checks success、staging evidence、Feishu done 误读为完成？

## 9. 本次调研验证记录

本次只读预检和证据提取记录：

1. 唤龙正式仓库已执行 `git status --short --branch` 与 `git fetch --prune origin`。
2. 除 `hl-scene-app` 外，主要唤龙仓库均为 `main...origin/main` 且干净。
3. `hl-scene-app` 位于已 gone 的本地分支，并有未跟踪 `android/`、`ios/`，本次未作为能力包进展依据。
4. 使用 Ruby 解析 `hl-contracts/rules/biz-capabilities-blueprint.yaml`：15 包、128 key_action、6 ordinary_action。
5. 使用 Ruby 解析 `hl-platform/biz/*/capability-manifest.yaml`：3 个 pilot manifest，分别为 `biz.booking.fulfillment`、`biz.tenant.entitlement`、`biz.demo`。
6. 本文新增在 `hl-dispatch/docs/delivery-recovery/`，不修改 `hl-contracts`、`hl-platform` 或 runtime 代码。
