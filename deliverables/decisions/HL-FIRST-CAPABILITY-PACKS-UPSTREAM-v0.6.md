# 唤龙平台首批能力包上游任务书 v0.6

## HL-FIRST-CAPABILITY-PACKS-UPSTREAM

---

**文档编号**：HL-FIRST-CAPABILITY-PACKS-UPSTREAM-001
**版本**：v0.6
**日期**：2026-04-28
**状态**：LOCKED（Founder Signed，2026-04-28）
**派生链**：Judgment Harness 实战 1 → Founder boundary / grill / baseline 签字 → PM 工作台通知
**适用对象**：Founder、PM-1 朱阳、PM-2 邹骢、技术验收官、后续工程师团队
**适用阶段**：首批能力包 Cap-Spec 设计接入
**发布规则**：GitHub PR 为正式留痕；飞书只做通知与协同，不作为决策真源

---

## 0. 定位

本文档是唤龙平台首批 4 个能力包的上游任务书，用于把 Founder 已签字的能力包边界、分工、强约束和首切片链路交给 PM。

本文档允许 PM 开始编写 Cap-Spec（能力包规格），但不允许工程师直接开工实现。工程开工必须等待 PM 的 Cap-Spec、契约缺口清单、关键动作注册提案、验收场景和对应 PR 完成审查。

本文档不替代 `hl-contracts`。`hl-contracts` 仍是唤龙契约、治理规则、OpenAPI、reason_code、capability registry、facts/rules 的 Tier 1 SSOT（一级事实真源）。

---

## 1. 全局硬约束

| 编号 | 约束 | 说明 |
|---|---|---|
| G-1 | 必须符合唤龙契约 | PM 的 Cap-Spec 必须引用和服从 `hl-contracts`，不得改写契约真相。 |
| G-2 | 必须接入 HK Kernel（唤龙治理内核） | 能力包必须以 HK 为基础，接入 HK.Policy / HK.Audit / HK.ID / HK.Consent 等治理能力。 |
| G-3 | 必须经过 Gateway / Protocol Gate（统一入口与协议门） | 能力包不得绕过统一入口、协议门和治理校验。 |
| G-4 | Founder 是全局契约语义 SSOT | PM 是所负责能力包的业务语义 SSOT，但不得越出 Founder 给定的契约包络。 |
| G-5 | PM 写 Cap-Spec，不写传统 PRD | PM 产出能力规格、验收场景、业务码提案、契约缺口清单，不复制 Tier 1 SSOT。 |
| G-6 | AI/NUI 只生成候选和草稿 | AI/NUI（自然交互界面）可以生成候选、建议、暂占请求，不得替用户确认正式业务事实。 |
| G-7 | GUI 是确认、主动操作、降级、治理与审计界面 | GUI（图形界面）作为自然交互不可用时的降级操作模式，也允许用户主动进入 GUI 操作。 |
| G-8 | key_action（关键治理动作）必须走 Can → Action → Audit | 改变业务事实、治理事实、审计事实或资源占用的动作，必须列为 key_action。 |
| G-9 | fail-secure（默认安全失败） | 未注册、未启用、契约不合规的动作默认失败，不得默默放行。 |
| G-10 | 未确认草稿不得成为真源 | 未经 Founder 确认的草稿、过程文件、AI 输出和飞书讨论，不得被当作决定或真源。 |
| G-11 | 旧系统只作业务覆盖参考 | 本次没有旧系统代码包袱；旧系统只用于覆盖业务场景，不作为分包边界真源。 |

---

## 2. 首批能力包与 PM 分工

| 能力包 ID | 中文名称 | PM | 责任域 |
|---|---|---|---|
| `biz.offer.catalog` | 供给目录 | PM-1 朱阳 | 定义商户提供什么服务、服务需要什么资源、服务规则是什么。 |
| `biz.store.resource` | 门店与资源（供给资源配置） | PM-1 朱阳 | 定义实际有什么供给资源、资源如何配置、资源是否可预约。 |
| `biz.customer.profile` | 客户档案 | PM-2 邹骢 | 定义客户主体识别、基础档案、预约关联。 |
| `biz.booking.fulfillment` | 预约与履约 | PM-2 邹骢 | 定义自然交互预约、AI 草稿、资源暂占、人工确认、正式预约、到店和履约闭环。 |

### 2.1 PM-1 朱阳：供给侧语义

朱阳负责 `biz.offer.catalog` 和 `biz.store.resource` 两个能力包。

核心职责：把“商户提供什么服务、服务需要什么资源、实际有什么资源”定义清楚。服务项目、手艺人能力、服务位类型、整房规则、可预约性必须保持一致。

### 2.2 PM-2 邹骢：客户与预约履约

邹骢负责 `biz.customer.profile` 和 `biz.booking.fulfillment` 两个能力包。

核心职责：把“谁来预约、如何生成预约、如何确认、如何履约”定义清楚。客户主体、AI Draft（AI 候选草稿）、Appointment Intent Hold（预约意向保留）、Qualified Resource Hold（合格资源暂占）、Confirmed Booking（正式预约）必须形成闭环。

---

## 3. 统一业务背景

唤龙平台服务的首要范畴是人本服务业 / 生活消费服务业，即以手艺人为核心供应链、由人为人提供服务的行业。能力包设计应优先服务这类场景，而不是按传统商品电商、纯到店核销或纯 SaaS 后台来切分。

本次首切片优先覆盖“自然交互预约 → 人工确认 → 正式预约 → 履约 → 审计”的最小闭环。GUI 不是主入口，而是确认、兜底、治理和可审计操作界面。

自然交互中的语音包含两类模式：

1. 咨询室一对一：交谈语音被收录、转写、识别意图，生成销售单或服务单候选。
2. 用户主动语音：用户主动表达预约或服务意图，生成销售单或服务单候选。

自然交互常规下只产生 AI Draft（AI 候选草稿）。当意图被识别后，系统弹出 GUI 草稿，由用户确认相关选项和内容。一旦用户确认，才进入正式单据，并留下可审计证据。

---

## 4. 首切片链路

首切片必须围绕以下链路设计，不得跳步：

```text
自然交互意图
  → AI Draft（AI 候选草稿）
  → Appointment Intent Hold（预约意向保留）
  → Qualified Resource Hold（合格资源暂占）
  → GUI Confirm（图形界面人工确认）
  → Confirmed Booking（正式预约）
  → Fulfillment（到店与履约）
  → Audit Evidence（审计证据）
```

| 状态 / 动作 | 中文解释 | 治理要求 |
|---|---|---|
| 自然交互意图 | 用户通过语音、LUI（语言用户界面）或咨询室交谈表达的业务意图。 | 识别到客户主体、时间、门店即可形成最小意图字段。 |
| AI Draft（AI 候选草稿） | AI 根据意图生成的候选业务单据，尚未生效。 | 普通审计，不占用资源，不是 key_action。 |
| Appointment Intent Hold（预约意向保留） | 对“客户 + 门店 + 时间窗口”的短时意向保留。 | key_action；TTL（有效期）统一 15 分钟，可刷新但最长 30 分钟；不锁具体资源。 |
| Qualified Resource Hold（合格资源暂占） | 对“服务项目 + 手艺人 + 服务位 / 整房 / 服务资源 + 时间段”的短时暂占。 | key_action；TTL 15 分钟；仅人工可刷新一次，最长 30 分钟。 |
| GUI Confirm（图形界面人工确认） | 用户在 GUI 中确认关键字段、影响范围、资源状态和风险提示。 | 确认前必须展示正式生效影响，不得由 AI 替用户确认。 |
| Confirmed Booking（正式预约） | 用户确认后形成的正式预约。 | 进入正式业务事实；确认前必须重新校验资源、客户、门店、服务项目与 hold 状态。 |
| Fulfillment（到店与履约） | 到店、服务执行、履约确认。 | 关键状态变化必须审计。 |
| Audit Evidence（审计证据） | 对草稿、保留、暂占、确认、过期、取消、释放、履约的证据记录。 | 必须能追溯谁、何时、基于什么输入、确认了什么。 |

---

## 5. 资源与时效规则

### 5.1 资源模型

不得默认“一房一床一人”。房间可以有多张床、多个服务位，甚至包含不同资源类型。实际模型必须支持：

- 门店（store）
- 房间（room）
- 服务位（service unit），例如床位、椅位、仪器位、操作台
- 整房资源（whole room），适用于必须独占整房的服务
- 手艺人（artisan）
- 手艺人能力 / 资质 / 角色
- 服务项目与资源需求关系

“美疗师”统一改称“手艺人”，用于覆盖更广的人本服务业。

### 5.2 Hold 时效

| Hold 类型 | TTL | 刷新规则 | 过期处理 |
|---|---|---|---|
| Appointment Intent Hold（预约意向保留） | 15 分钟 | 有效补充信息可刷新，最长 30 分钟 | 自动释放，写入审计。 |
| Qualified Resource Hold（合格资源暂占） | 15 分钟 | 仅人工可刷新一次，最长 30 分钟 | 自动释放，写入审计。 |

两个 Hold 都是动态业务状态，不是正式预约。正式预约确认前必须重新校验资源可用性。不同草稿、暂占和正式订单在时间上冲突时，系统必须按状态优先级与资源锁定规则处理，不得让过期草稿继续占用资源。

---

## 6. 四个能力包任务书

### 6.1 `biz.offer.catalog`：供给目录

**一句话定义**：定义服务业商户“提供什么服务”以及每项服务需要什么资源。

**PM 需要定义**：

- 服务项目唯一命名、展示名、基础说明。
- 基础服务时长、准备时间、清洁 / 整理缓冲时间。
- 服务是否可预约、是否需要手艺人、是否需要特定能力或资质。
- 服务需要的服务位类型，例如床位、椅位、仪器位、操作台。
- 服务是否要求整房。
- 服务与最小服务能力词典的引用关系。

**不得定义**：

- 门店实际有哪些资源。
- 某个手艺人当天是否可服务。
- 客户档案。
- 预约生命周期和资源暂占状态。

**输出要求**：

- Cap-Spec-1：能力规格书。
- Cap-Spec-2：验收场景集。
- Cap-Spec-3：reason_code（业务码）提案。
- Contract Gap（契约缺口）清单。

### 6.2 `biz.store.resource`：门店与资源（供给资源配置）

**一句话定义**：定义门店实际拥有哪些供给资源，以及这些资源如何支持预约。

**PM 需要定义**：

- 门店、营业状态、可预约配置。
- 房间、整房规则、服务位清单。
- 服务位类型：床位、椅位、仪器位、操作台等。
- 手艺人、手艺人能力 / 资质 / 角色。
- 手艺人与服务项目的可服务关系。
- 资源启停、维护、不可预约状态。
- 资源可预约性对预约链路的影响。

**不得定义**：

- 服务项目语义本身。
- 动态预约 Hold 的生命周期。
- 客户资产。
- 支付和结算。

**输出要求**：

- Cap-Spec-1：能力规格书。
- Cap-Spec-2：验收场景集。
- Cap-Spec-3：reason_code 提案。
- Contract Gap 清单。

### 6.3 `biz.customer.profile`：客户档案

**一句话定义**：定义客户主体识别、基础档案和预约关联。

**首版只做**：

- 客户主体识别。
- 客户创建。
- 基础档案字段。
- 客户与预约、草稿、正式单据的关联。

**首版不做**：

- 储值。
- 次卡。
- 权益。
- 会员等级。
- 复杂客户资产。

**输出要求**：

- Cap-Spec-1：能力规格书。
- Cap-Spec-2：验收场景集。
- Cap-Spec-3：reason_code 提案。
- Contract Gap 清单。

### 6.4 `biz.booking.fulfillment`：预约与履约

**一句话定义**：承载自然交互预约、AI 草稿、资源暂占、人工确认、正式预约、到店和履约闭环。

**PM 需要定义**：

- 接收自然交互预约意图的最小字段：客户主体、时间、门店。
- 生成 AI Draft（AI 候选草稿）。
- 创建、更新、释放 Appointment Intent Hold（预约意向保留）。
- 读取供给目录与门店资源配置。
- 创建、刷新、释放 Qualified Resource Hold（合格资源暂占）。
- GUI Confirm（图形界面人工确认）。
- 确认前二次校验。
- Confirmed Booking（正式预约）。
- 到店、履约、取消、过期释放和审计。

**不得定义**：

- 服务项目规则。
- 长期资源主数据。
- 支付。
- 客户资产扣减。

**输出要求**：

- Cap-Spec-1：能力规格书。
- Cap-Spec-2：验收场景集。
- Cap-Spec-3：reason_code 提案。
- Contract Gap 清单。

---

## 7. 初始 key_action（关键治理动作）建议

以下仅是 PM 提案起点，正式注册必须进入 `hl-contracts` 对应 registry 和 reason_code PR。

| 能力包 | key_action 候选 |
|---|---|
| `biz.offer.catalog` | `offer.service.create`、`offer.service.update`、`offer.service.publish`、`offer.service.disable` |
| `biz.store.resource` | `store.create`、`resource.service_unit.create`、`resource.service_unit.disable`、`artisan.create`、`artisan.skill.assign`、`artisan.disable` |
| `biz.customer.profile` | `customer.create`、`customer.update`、`customer.merge`、`customer.disable` |
| `biz.booking.fulfillment` | `booking.intent_hold.create`、`booking.intent_hold.update`、`booking.intent_hold.release`、`booking.resource_hold.create`、`booking.resource_hold.extend`、`booking.resource_hold.release`、`booking.confirm`、`booking.cancel`、`booking.checkin`、`booking.fulfill` |

`booking.draft.create` 不是 key_action，只做普通审计，因为它只生成 AI Draft（AI 候选草稿），不改变正式业务事实，也不占用资源。

---

## 8. 契约缺口清单

PM 进入 Cap-Spec 后，必须显式列出以下缺口，不得假设已经存在：

| 缺口 | 说明 |
|---|---|
| capability_id 最终确认 | 4 个能力包 ID 需进入正式 registry。 |
| `capabilities.yaml` 注册 | 每个能力包的路由、开关、依赖 HK 模块需登记。 |
| key_actions 注册 | 所有关键治理动作需正式注册。 |
| reason_code 提案 | PM 需提出业务码，进入 `reasoncodes.csv`。 |
| OpenAPI / event contracts | 正式接口和事件契约需由工程侧根据 Cap-Spec 与治理规则生成。 |
| HK.Policy / HK.Audit / HK.ID / HK.Consent 触发点 | 必须标清每个动作何时鉴权、何时审计、何时需要身份与授权。 |
| 最小服务能力词典 | 当前可设计最小版，满足首切片；未来对齐 Founder 主导的开源“统一服务定义库”。 |
| 咨询室录音 / 转写 / 同意 / 证据链 | 首切片可作为 P1 合规任务，不在本轮展开。 |

---

## 9. PM 交付清单

每个 PM 对自己负责的能力包至少提交以下产出：

| 产出 | 要求 |
|---|---|
| Cap-Spec-1（能力规格书） | 定义能力边界、目标、非目标、业务规则意图、上游引用。 |
| Cap-Spec-2（验收场景集） | 提供结构化输入、预期、验收方式、审计要求。 |
| Cap-Spec-3（业务码提案） | 提出 reason_code，说明触发场景和业务含义。 |
| Contract Gap（契约缺口）清单 | 标明需要 Founder / Gate / 工程补齐的契约项。 |
| 首切片验收说明 | 说明如何验证自然交互意图到正式预约和审计证据的闭环。 |
| 跨包依赖表 | 写清依赖谁、读取什么、输出什么、不得重定义什么。 |

PM 的 Cap-Spec 必须体现“只引用不复制”的原则：引用 `hl-contracts` 真源路径，不在 PM 文档中复制 Tier 1 SSOT 内容。

---

## 10. 工程开工门槛

PM 接入不等于工程开工。工程启动前至少满足：

1. 对应能力包 Cap-Spec-1 / 2 / 3 已提交 PR。
2. 契约缺口清单已列出，并完成 Founder 或 Gate 裁决。
3. capability_id、key_actions、reason_code、OpenAPI / event 的落点已明确。
4. HK Kernel（唤龙治理内核）和 Gateway / Protocol Gate（统一入口与协议门）接入点已明确。
5. GUI Confirm（图形界面人工确认）前后的业务事实、资源状态和审计证据已定义。
6. 跨包依赖不再互相重定义。

---

## 11. 发布与通知口径

本文件应通过 GitHub PR 发布并审查。PR 合并后，飞书 PM 工作台只发布摘要和链接。

飞书通知口径：

```text
首批能力包上游任务书 v0.6 已 Founder Signed。

PM-1 朱阳负责：
- biz.offer.catalog｜供给目录
- biz.store.resource｜门店与资源（供给资源配置）

PM-2 邹骢负责：
- biz.customer.profile｜客户档案
- biz.booking.fulfillment｜预约与履约

PM 当前任务：开始编写 Cap-Spec，不直接启动工程实现。
正式真源：GitHub PR / 合并后的决策文件。
禁区：未经 Founder 确认的草稿、AI 输出、过程文件和飞书讨论，不得当作决定或真源。
```

---

## 12. Founder 签字

Founder 已确认以下 baseline：

- 首批 4 个能力包：`biz.offer.catalog`、`biz.store.resource`、`biz.customer.profile`、`biz.booking.fulfillment`。
- PM 分工：朱阳负责供给侧语义，邹骢负责客户与预约履约。
- 首切片链路：自然交互意图 → AI Draft（AI 候选草稿） → Appointment Intent Hold（预约意向保留） → Qualified Resource Hold（合格资源暂占） → GUI Confirm（图形界面人工确认） → Confirmed Booking（正式预约） → Fulfillment（到店与履约） → Audit Evidence（审计证据）。
- Hold TTL 统一 15 分钟，最长 30 分钟。
- 房间不得默认一房一床一人。
- “美疗师”统一改称“手艺人”。
- PM 设计规范必须符合唤龙契约。
- 能力包构建必须接入 HK Kernel（唤龙治理内核）。
- 未经 Founder 确认的草稿和过程文件不得作为真源或决定。

*v0.6 · 2026-04-28 · Founder Signed*
