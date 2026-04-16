# 规格驱动模式下 PRD 重定义规格

## PRD-REDEFINITION-SPEC v3.0

---

**文档编号**：PRD-REDEF-001
**版本**：v3.0
**日期**：2026-04-11
**状态**：DRAFT（待创始人裁决 R-5~R-7）
**替代文档**：PRD-REDEFINITION-SPEC v2.0 RULED（2026-03-30）
**派生链**：R-057 + 创始人 2026-03-30 纠正（PM = 产线责任人）→ v2.0 → TEAM-COLLAB-SPEC v2.1（四权分离 + AI-first）→ 本文档
**前置关系**：本文档是 PM-AI-COLLABORATION-ONBOARDING-SPEC 的先决依赖

> **v3.0 重大变更说明**：TEAM-COLLAB-SPEC v2.1 将组织从"创始人+AI=100%代码"扩展为"21 人全组织 AI 驱动"。PM 不再直接驱动 AI 编码——编码职责由工程师承担（AI-first）。PM 定位从"产线全闭环驱动者"收敛为"产线业务语义 SSOT owner"：编写 Cap-Spec、审批 HPRD、执行产品验收。

---

## 0. 问题陈述

创始人提出核心问题：

> "在规格驱动模式下，还需要 PRD 吗？PM 需要完成的 PRD 已经不是传统的那种文档了，必须符合新的工作流与产出规范，这是先决条件。"

并在后续讨论中明确了 PM 的正确定位：

> "PM 在负责的领域，某一个能力包业务或产品线，是整个产线的责任人。基于已有的唤龙运行态治理与契约（创始人给定的上游）接入开始，进行规格驱动开发，测试用例、AI 编码、验收，交技术验收官把关审计。"
> "规格驱动的工具，不作强制限定。使用的 AI 平台也不作强制规定。"

---

## 1. 现状审计：PRD 的实际地位

### 1.1 PRD 在 hl-contracts 中的层级

```
Tier 1 — LOCKED（contracts 一级目录）
  decisions/ facts/ rules/ reasoncodes/ apis/ events/ glossary/ auth/
  → 机器可读、CI 门禁强制、SSOT
  → 创始人主导定义与裁决

Tier 2 — ITERABLE（prd/ 目录）
  prd/core/ prd/biz/ prd/console/ prd/data/
  → CLAUDE.md 标注"参考性质"（非 SSOT）
  → 人工可读、无 CI 门禁、依赖 Tier 1

Tier 3 — RUNTIME（hl-platform / hl-console-native 代码）
  → 必须从 Tier 1 推导，不得自行定义
```

PRD 在 CLAUDE.md 中被标注为"参考性质"，从未被纳入 CI 强制校验链路。

> **v3.0 目录纠偏说明**：`prd/core/` 保留给 HK / Gateway / Engine 等平台内核 PRD；PM owner 的 `biz.*` Cap-Spec-1/2 当前操作路径为 `prd/biz/`。

### 1.2 PRD 6 卫星文档冗余分析

以 HK.Policy 能力包为样本：

| 卫星文档 | 与 Tier 1 重叠 | 重叠目标 | 独特价值 |
|---------|:-------------:|---------|----------|
| **MVP.v1.0.md**（主文档） | 部分 | decisions/ + rules/ | **高**——能力边界、目标/非目标、业务意图 |
| **Facts.v1.0.md** | **高度** | facts/facts-catalog.md | 低——SSOT 派生副本 |
| **Reason-Codes.v1.0.md** | **高度** | reasoncodes/reasoncodes.csv | 低——SSOT 派生副本 |
| **Decision-Trace.v1.0.md** | **高度** | decisions/ | 无——SSOT 派生副本 |
| **API-Return-Codes.v1.0.md** | **高度** | apis/*.openapi.yaml | 无——SSOT 派生副本 |
| **Core-Acceptance-Cases.v1.0.md** | **无** | — | **极高**——唯一的业务验收场景定义 |

6 个卫星中 4 个是 SSOT 派生副本，制造维护负担和一致性风险。

### 1.3 根本变化：AI-first 编码

传统 PRD 的消费者是人类开发者。在 AI-first 编码模式下（DD-TEST v1.2 B2），代码默认由 AI 生成、工程师可在必要时手动补充，统一经过 CI 门禁。AI 直接消费 contracts 的机器可读格式（OpenAPI / Rules YAML / reasoncodes CSV），不需要人类可读的需求叙述作为中间媒介。PRD 的传统角色已经失效。

> **v3.0 新增**：但工程师需要理解 PM 的业务意图才能正确驱动 AI 编码。HPRD（Human-readable Product Design）作为工程师产出的"理解确认件"解决这一问题——它证明"工程师理解正确了"，而非第二份 PRD。详见 §3.7。

---

## 2. PM 角色重定义

### 2.1 核心定位：产线责任人

**PM 不是"规格整理者"，而是所负责能力包/产品线的完整责任人。**

PM 的工作起点是创始人已定义的上游——唤龙运行态治理体系与契约法典（hl-contracts）。在此上游约束之下，PM 对自己负责的能力包拥有业务语义主权（TEAM-COLLAB-SPEC v2.1 R-TEAM-008）：

```
创始人给定上游（唤龙契约 + 运行态架构 + 治理裁决）
    ↓
PM 接入上游，成为该能力包/产品线的业务语义 SSOT owner
    ↓
PM 编写 Cap-Spec（规格定义 + 验收场景 + 业务码提案）
    ↓
工程师产出 HPRD → PM 审批（pm-hprd-pass）
    ↓
工程师 AI-first 编码实现 + QA 编写验收测试
    ↓
CI 门禁 + QA 验收（qa-verdict） + PM 产品验收（pm-acceptance）
    ↓
创始人通过 path-based CODEOWNERS 行使治理权
```

> **v3.0 关键变更**：PM 不再直接驱动 AI 编码。编码由工程师（AI-first）承担，PM 聚焦业务语义定义（Cap-Spec）和验收（pm-hprd-pass + pm-acceptance）。

### 2.2 PM 权责边界

| 维度 | PM 的权利 | 约束 |
|------|----------|------|
| **业务语义主权** | 在负责的能力包范围内，PM 拥有 Cap-Spec 业务语义 SSOT（R-TEAM-008） | 能力包语义不得越出契约包络（创始人持有全局契约语义 SSOT） |
| **Cap-Spec 编写权** | PM 编写 Cap-Spec-1/2/3 | 必须基于创始人给定的上游（contracts + governance） |
| **HPRD 审批权** | PM 审批工程师产出的 HPRD（pm-hprd-pass）| HPRD 是理解确认件，PM 审批业务理解正确性，不审技术设计 |
| **工具自主权** | 规格驱动工具不作强制限定 | — |
| **AI 平台自主权** | 使用的 AI 平台不作强制规定 | — |
| **产品验收权** | PM 对自己负责的能力包进行产品验收（pm-acceptance） | QA 独立拥有质量 verdict（qa-verdict） |

| 维度 | PM 不可做 | 原因 |
|------|----------|------|
| **修改上游契约** | 不可直接修改 hl-contracts 的 Tier 1 SSOT（rules / facts / apis 等） | 创始人主导定义 |
| **绕过技术验收** | 不可跳过技术验收官直接上线 | 执行者与审计者必须不同源 |
| **自定义治理规则** | 不可在能力包内发明不在 contracts 中的治理规则 | hl-contracts 是 SSOT |
| **跨产线干预** | 不可修改其他 PM 负责的能力包 | 产线责任边界 |

### 2.3 与创始人的分界

| 层面 | 创始人（上游） | PM（下游产线责任人） |
|------|-------------|-------------------|
| 唤龙契约（hl-contracts） | **主导定义与裁决** | 消费与引用 |
| 运行态架构 | **主导设计与决策** | 在架构内实现 |
| 能力包立项 | **裁决** | 推荐、建议 |
| 能力包规格（Cap-Spec） | 审批（契约包络检查） | **编写与驱动** |
| HPRD | — | **审批**（pm-hprd-pass）；工程师编写 |
| AI-first 编码 | 通过 CODEOWNERS/gates 治理 | ~~PM 驱动~~ → **工程师驱动**（v3.0 变更） |
| 验收测试 | — | **审批验收场景**；QA 编写测试代码 |
| 产品验收 | 里程碑签收 | **PM 执行验收**（pm-acceptance） |
| 技术验收 | — | 工程师互审 + CI 门禁 + QA verdict |

---

## 3. PRD 重定义

### 3.1 为什么废弃"PRD"术语

1. "Product Requirements Document"暗示其目标是传递需求给开发者——但规格驱动模式下 PM 自己驱动 AI 编码，不存在"传递"环节
2. 6 卫星结构中 4 个是 SSOT 派生副本，制造了维护负担
3. PRD 的名称暗示静态文档交付物，而 PM 作为产线责任人的产出是**完整的规格驱动闭环**，不是一摞文档

### 3.2 新定义：能力包规格（Capability Spec）

PM 的核心产出重命名为 **Capability Spec（能力包规格，简称 Cap-Spec）**。

> Cap-Spec 是 PM 作为产线责任人，为所负责的能力包编写的**规格驱动工件集**——定义能力边界、业务规则意图、验收标准，并以此驱动 AI 编码与验收的全过程。

与旧 PRD 的本质区别：PRD 是"交给别人的文档"，Cap-Spec 是"PM 自己驱动闭环的规格"。

### 3.3 Cap-Spec 工件集

每个能力包，PM 产出以下工件：

#### Cap-Spec-1：能力规格书（Capability Specification）

替代原 MVP.v1.0.md，剥离与 Tier 1 SSOT 重叠内容。

**必含章节**：

| 章节 | 内容 | 硬约束 |
|------|------|--------|
| §0 一句话定义 | 此能力是什么、解决什么问题 | 中文为主，≤ 50 字 |
| §1 业务背景与目标 | 为什么做、解决谁的什么痛点 | 必须有用户场景 |
| §2 能力边界 | 做什么 + **不做什么** | "非目标"至少 3 条 |
| §3 业务规则概述 | 关键业务规则（自然语言） | **只描述意图，不复制 rules YAML** |
| §4 上游引用索引 | 指向 contracts 中的相关定义 | **只列路径，不复制内容** |
| §5 依赖与时序 | 上游能力依赖、并行关系 | 对齐 LAUNCH-{MODULE}.md |

**禁止包含**：Tier 1 SSOT 的派生副本（API 映射表、Facts 详表、裁决追踪链等）。

**文件命名**：`Cap-Spec-{Domain}.{Module}.v{X.Y}.md`
**示例**：`Cap-Spec-Biz.Product.v1.0.md`
**文件位置**：`hl-contracts/prd/biz/`

#### Cap-Spec-2：验收场景集（Acceptance Scenarios）

PM 最高价值的独特产出，也是 PM 执行业务验收和驱动 AI 编码的核心依据。

**必含格式**：

```
### Case-{ID}：{场景名称}

输入：
  {结构化输入字段}

预期：
  {结构化输出字段，含 reason_code}

验收方式：
  □ API 调用验证 / □ UI 人工验证 / □ 审计日志验证
```

**文件命名**：`Cap-Spec-{Domain}.{Module}.Acceptance.v{X.Y}.md`
**文件位置**：`hl-contracts/prd/biz/`

#### Cap-Spec-3：业务码提案（Reason Code Proposal）

PM 对所负责能力包的 reason_code 提出业务侧定义，以 PR 形式直接提交到 `reasoncodes/reasoncodes.csv`。

**PM 在 PR 中提供**：code / domain / 中文描述 / 触发场景
**不提供**：HTTP mapping、OpenAPI 响应体结构、技术实现细节
**文件形态**：reasoncodes.csv PR + PR description 中的业务说明

### 3.4 能力包交付协作产出（v3.0 修订）

> **v3.0 变更**：v2.0 中 PM 直接驱动 AI 编码。v3.0 中编码由工程师（AI-first）承担，PM 产出聚焦于规格和验收。

| 产出 | 谁编写 | 谁审批 | 说明 |
|------|--------|--------|------|
| **Cap-Spec-1/2/3** | PM | 创始人（契约包络检查） | PM 业务语义 SSOT |
| **HPRD** | 工程师 | PM（pm-hprd-pass） | 理解确认件，非第二份 PRD |
| **代码实现** | 工程师（AI-first） | CI 门禁 + 工程师互审 | ~~PM 驱动~~ → 工程师驱动 |
| **验收测试** | QA | PM（场景审批） | 基于 Cap-Spec-2 + acceptance-manifest.yaml |
| **design.md** | 工程师 | 工程师互审 | PM 不审 design.md（R-TEAM-004） |

### 3.5 被废止的 PM 文档类型

| 原文档 | 废止原因 | 新归属 |
|--------|---------|--------|
| Facts.v1.0.md | facts-catalog.md 是 SSOT | 创始人直接维护 facts/ |
| Decision-Trace.v1.0.md | decisions/ 是 SSOT | 创始人裁决时沉淀 |
| API-Return-Codes.v1.0.md | apis/*.openapi.yaml 是 SSOT | AI 自动派生 |
| Dev-Checklist | PM 自己驱动 AI 编码，不需要转交清单 | 废止 |

### 3.6 存量迁移策略（R-2 裁决：逐步迁移）

| 优先级 | 对象 | 处理方式 |
|:-----:|------|----------|
| **立即** | 未来新建的能力包 | 按 Cap-Spec 工件集规范创建，不再使用旧 PRD 6 卫星结构 |
| **立即** | prd/README.md + prd/biz/README.md | 追加 "Cap-Spec 规范（2026-03 起适用）" 与 biz 目录说明 |
| **逐步** | 已定稿的 HK.* 系列 PRD | 当能力包进入下一版本迭代时，顺带迁移为 Cap-Spec 格式；不主动为迁移而迁移 |
| **逐步** | PRD 6 卫星中的 SSOT 派生副本 | 标注 DEPRECATED，引导读者直接查阅 Tier 1 SSOT（R-3 裁决） |

### 3.7 HPRD — 人类可读产品设计（v3.0 新增）

**HPRD（Human-readable Product Design）** 是工程师阅读 Cap-Spec 后产出的理解确认件，证明"工程师理解正确了"。

**HPRD 不是**：
- 第二份 PRD（Cap-Spec 才是业务语义 SSOT）
- 技术设计文档（design.md 是技术设计）
- AI 生成的需求转述

**HPRD 最小模板**（TEAM-COLLAB-SPEC v2.1 §2.2 / DD-TEST v1.2 §9.3）：

| 章节 | 内容 |
|------|------|
| 能力 ID | 对应 Cap-Spec 编号 |
| 用户可见变化 | 此能力上线后，用户在界面/API 上看到什么不同 |
| 不变行为 | 哪些现有行为保持不变（防止工程师误改） |
| 不在范围 | 明确排除的内容（防范围蔓延） |
| 验收走查 | 工程师描述自己如何验证每个 Cap-Spec-2 场景 |
| 语义疑问 | 阅读 Cap-Spec 时产生的疑问，PM 必须在 freeze 前答复 |

**术语演变**：v1.0 "人读版 PRD" → v1.1 "Impl-Semantics" → v1.2/v3.0 **HPRD**

**文件位置**：`hl-platform/docs/hprd/`（CODEOWNERS → @hl-pm-team 审批）

---

## 4. 能力包协作模型

### 4.1 四角色模型（v3.0 修订，对齐 TEAM-COLLAB-SPEC v2.1）

| 角色 | 定位 | 边界 |
|------|------|------|
| **创始人（治理 Owner）** | 全局契约语义 SSOT + 组织治理 | 通过 CODEOWNERS/rulesets/gates 行使治理权，不进入能力包 feature PR 人工审批 |
| **PM（业务语义 Owner）** | 能力包业务语义 SSOT | Cap-Spec 编写 + HPRD 审批 + 产品验收；不审 design.md，不驱动 AI 编码 |
| **工程师（技术实现 Owner）** | AI-first 编码 + 技术设计 | 产出 HPRD + design.md + 代码实现；互审技术质量 |
| **QA（独立质量 Owner）** | 验收自动化 + 质量判定 | qa-verdict required status check；独立于工程师 |

> v2.0 三角色 → v3.0 四角色：PM 退出 AI 编码，工程师从"技术验收官"升级为"AI-first 编码实现 + 技术设计 owner"，QA 从隐含角色升级为独立质量 owner。

### 4.2 完整流程（v3.0 修订：四权分离）

```
┌─────────────────────────────────────────────┐
│  创始人上游（唤龙契约 + 运行态架构 + 裁决）      │
│  hl-contracts SSOT · CODEOWNERS · rulesets   │
└─────────────────┬───────────────────────────┘
                  │ PM 接入上游
                  ▼
┌─────────────────────────────────────────────┐
│  PM 业务语义 SSOT Owner                      │
│  Cap-Spec-1 → Cap-Spec-2 → Cap-Spec-3       │
└─────────────────┬───────────────────────────┘
                  │ 工程师接入 Cap-Spec
                  ▼
┌─────────────────────────────────────────────┐
│  工程师 AI-first 编码                         │
│  HPRD → PM 审批（pm-hprd-pass）              │
│  design.md → 工程师互审                       │
│  AI-first 编码 → CI 门禁 L1-L3               │
└─────────────────┬───────────────────────────┘
                  │ 并行审计
                  ▼
┌─────────────────────────────────────────────┐
│  QA 独立质量 Owner                            │
│  验收测试 → qa-verdict status check           │
├─────────────────────────────────────────────┤
│  PM 产品验收                                  │
│  pm-acceptance status check                  │
└─────────────────┬───────────────────────────┘
                  │ path-based CODEOWNERS merge
                  ▼
         创始人通过 gates 行使治理权
```

### 4.3 工具与平台原则

| 维度 | 原则 |
|------|------|
| **规格驱动工具** | **不作强制限定**——PM 可自主选择适合的 spec 编写与管理工具 |
| **AI 编码平台** | **不作强制规定**——PM 可使用任何 AI 平台驱动编码 |
| **协作通道** | 以 GitHub（Issue + PR）为最终交付接口，过程工具自主 |
| **唯一硬约束** | 最终产出必须能合入 hl-contracts / hl-platform 等仓库，通过 CI 门禁 |

---

## 5. 风险与缓解

| 风险 | 后果 | 缓解措施 |
|------|------|----------|
| PM 在产线内偏离上游契约 | 能力包实现与 contracts 不一致 | 技术验收官架构评审 + CI 门禁 |
| PM 使用的 AI 产出质量不稳定 | 代码质量参差 | 技术验收官代码审计是最后防线 |
| PM 自定义治理规则绕过 contracts | 破坏 SSOT 唯一性 | contracts merge 权在创始人，PM 无法绕过 |
| 存量 PRD 与新 Cap-Spec 命名混乱 | 文档索引混乱 | prd/README.md 追加新旧共存规则 |

---

## 6. 待创始人裁决

| # | 事项 | 裁决结果 | 裁决日期 |
|---|------|---------|----------|
| R-1 | 废弃"PRD"术语，改用新术语（Cap-Spec） | **✅ 采纳** | 2026-03-30 |
| R-2 | 存量 HK.* PRD 迁移策略 | **✅ B) 逐步迁移** | 2026-03-30 |
| R-3 | PM 不再维护 SSOT 派生副本文档 | **✅ A) 不再维护** | 2026-03-30 |
| R-4 | v2.0 中间口径：Cap-Spec 暂沿用 prd/core/ | **✅ A) prd/core/**（后续 `biz.*` 路径纠偏为 `prd/biz/`） | 2026-03-30 |
| R-5 | PM 退出 AI 编码，编码由工程师（AI-first）承担 | 待裁决 | — |
| R-6 | 新增 HPRD 作为工程师理解确认件（§3.7），PM 审批 pm-hprd-pass | 待裁决 | — |
| R-7 | 四角色模型（创始人/PM/工程师/QA）替代三角色（创始人/PM/工程师） | 待裁决 | — |

---

## 7. 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-30 | v1.0 | DRAFT — 初版，PM 定位为规格整理者，CIS 三件套 |
| 2026-03-30 | v2.0 | **重大修订** — 创始人纠正 PM 定位为产线责任人；废弃 CIS 改用 Cap-Spec；明确 PM 驱动 AI 编码的完整闭环；工具与 AI 平台不作强制限定 |
| 2026-03-30 | v2.0 RULED | 创始人裁决 R-1~R-4：废弃 PRD 术语✅、存量逐步迁移✅、不维护 SSOT 派生副本✅、Cap-Spec 暂沿用 prd/core/✅（后续 `biz.*` 目录纠偏为 `prd/biz/`） |
| 2026-04-11 | v3.0 | **重大修订** — 对齐 TEAM-COLLAB-SPEC v2.1 四权分离：PM 退出 AI 编码，改由工程师（AI-first）承担；新增 HPRD 定义（§3.7）；四角色模型替代三角色（§4.1）；PM 权责边界从"产线全闭环驱动者"收敛为"业务语义 SSOT owner"；新增 R-5~R-7 待裁决 |
