# 唤龙平台团队协作规格

## TEAM-COLLABORATION-SPEC v2.1 — 全组织 AI 驱动协作模型

---

**文档编号**：TEAM-COLLAB-SPEC-001
**版本**：v2.1
**日期**：2026-04-11
**状态**：DRAFT / Pilot-Locked for Capability Flow（创始人 2026-04-11 裁决：按试运行基线执行能力包流，缺陷修复/技术改动/治理流另见 WORKFLOW-GUIDE）
**替代文档**：TEAM-COLLABORATION-SPEC v1.2（SUPERSEDED）；v2.0（SUPERSEDED by v2.1 审计修正）
**派生链**：SAAC-HL-001 v1.1 §1.3 → BRIDGE-DERIVATION v1 → PRD-REDEFINITION-SPEC v2.0 → DD-TEST v1.1 → 创始人 2026-04-11 组织裁决 → v2.0 → 双独立审计仲裁 → 创始人 2026-04-11 Pilot-Lock 裁决 → 本文档

---

## 0. 推导声明

### 0.1 推导规则

与 BRIDGE-DERIVATION v1 相同——只有 SAAC-HL 哲学层和恒定层定义是公理；桥梁层具体选型（包括 v1.2 中的组织模型）全部清零，重新推导。

### 0.2 推导输入

| 编号 | 输入 | 关键约束 |
|------|------|---------|
| I-1 | SAAC-HL §1.3 | AI 驱动基本运行前提 |
| I-2 | R-045 LOCKED | 全新构建，无旧系统适配 |
| I-3 | R-055 LOCKED | Phase 0-2 单 JVM Modulith |
| I-4 | TECH-STACK-SPEC v3 | Kotlin 2.1.10 / Spring Boot 3.5.11 / Spring Modulith 1.3.4 |
| I-5 | PRD-REDEFINITION-SPEC v2.0 | PM = 产线责任人，Cap-Spec 替代 PRD |
| I-6 | DD-TEST v1.1 | 测试工程推导（JUnit 5 / Kotest Property / Testcontainers / acceptance-manifest.yaml）；G-026 = L2 manifest-based 覆盖率；G-023 = L3 验收场景回放 |
| I-7 | 创始人 2026-04-11 裁决 | 全组织 21 人 AI 驱动，不再分批过渡 |
| I-8 | 创始人 2026-04-11 裁决 | path-based CODEOWNERS + CI 门禁自动放行，创始人退出能力包 feature PR 人工审批 |
| I-9 | 创始人 2026-04-11 裁决 | HPRD（Human-readable Product Design）替代 Impl-Semantics 术语 |
| I-10 | GPT Pro 独立评审 2026-04-11 | 四权分离建议；创始人采纳方向，拒绝具体工具锁定 |
| I-11 | v2.0 双独立审计 2026-04-11 | 7 + 6 条审计项仲裁；10 项纳入 v2.1，4 项记为后续候选 |

### 0.3 推导逻辑

```
I-1（AI 驱动）+ I-7（全组织 21 人）
  → v1.2 的"创始人 + AI = 100% 代码"前提失效
  → 组织级项目中，工程师承担 AI 编码职责
  → 创始人定位为治理 owner

I-5（PM = 产线责任人）+ I-9（HPRD）
  → PM 拥有能力包业务语义 SSOT（Cap-Spec）
  → 创始人拥有全局契约语义 SSOT（hl-contracts 核心）
  → 能力包语义不得越出契约包络
  → 工程师产出 HPRD（Cap-Spec 的派生解读），PM 审批业务理解正确性
  → PM 不审 design.md，不进技术审批链

I-6（DD-TEST）+ I-10（四权分离）
  → 测试团队独立于工程师，拥有验收放行权
  → 执行（工程师）与审计（QA + AI）分家

I-8（path-based gate）+ I-11（审计修正：机读化）
  → 创始人通过规则本身（CODEOWNERS / rulesets / gates）行使治理权
  → 能力包 PR 由工程师互审 + QA 验收 + CI 门禁放行
  → QA verdict / PM acceptance 必须是 required status checks，不是口头放行
```

### 0.4 v2.1 vs v2.0 修正追溯

| # | 修正 | 审计来源 |
|---|------|---------|
| F-1 | 拆分 hl-contracts/CODEOWNERS：prd/biz/ → PM team；契约核心路径 → 创始人 | 审计 A#1 + B#2 |
| F-2 | Cap-Spec-3 加治理前置门：涉及 reason_code 变更须创始人先批再 freeze | 审计 A#2 |
| F-3 | 重排 hl-platform/CODEOWNERS 顺序 + 补 docs/hprd/ docs/design/ 路径 | 审计 A#3 |
| F-4 | QA verdict / PM acceptance 做成 required status checks | 审计 A#4 + B#3 |
| F-5 | Cap-Spec-2 owner 统一为 PM，QA = collaborator/reviewer | 审计 A#5 |
| F-6 | Step 4 门禁分层对齐 DD-TEST：G-026→L2，G-023→L3 | 审计 A#6 |
| F-7 | 语义主权分层：PM = 能力包语义 SSOT；创始人 = 全局契约语义 SSOT | 审计 B#1 |
| F-8 | HPRD 缩薄为理解确认件 + 最小模板 | 审计 B#2 |
| F-9 | "AI 生成 100% 代码"→"AI-first，人工可补，统一过 gate" | 审计 B#6 |
| F-10 | §5 加流程分类声明：缺陷修复/技术改动/治理流另见 WORKFLOW-GUIDE | 审计 B#5 |

**未纳入 v2.1 的候选项（记录备查）**：

| 候选 | 说明 | 计划 |
|------|------|------|
| capability-packet.yaml | 机读能力包包络 | T1 试运行后评估，v2.2 候选 |
| 完整状态机 | 流程状态机 + 异常回退 | 基于试运行数据设计，v2.2 候选 |
| 4 类流程详细定义 | 能力包/缺陷修复/技术改动/治理流 | WORKFLOW-GUIDE 附属文件 |
| post-release writeback | 发布后回写机制 | WORKFLOW-GUIDE 附属文件 |

### 0.5.1 R-TEAM-007 scope erratum（2026-04-25）

`R-TEAM-007` 原全域措辞按 2026-04-23 `R-FE-CLIENT-001 amend-001` 澄清为：**场景前端线转 Flutter**，覆盖 C 端消费者、B 端客户、门店员工等非治理后台业务前端；不覆盖治理/运营/审计人员客户端。

`hl-console-native` 仍属于 C 域治理客户端，技术方向为 SwiftUI / GHKit。

场景前端 App 为 `huanlongAI/hl-scene-app`，技术方向为 Flutter 3.41 / Dart 3.x。组织协作上的“前端转型”不得反向解释为 C 域客户端技术栈切换。

### 0.5 与 v1.2 的关键变更

| 维度 | v1.2 | v2.1 | 变更原因 |
|------|------|------|---------|
| 团队规模 | 7 人核心组 | 21 人全组织 | 创始人裁决：不再分批过渡 |
| 代码产出 | 创始人 + AI = 100% | 工程师 AI-first 编码（人工可补，统一过 gate） | 组织级项目，工程师承担实现职责 |
| PR 审批 | 创始人审所有 PR | path-based CODEOWNERS + CI 门禁 + required status checks | 创始人裁决 + 审计修正 |
| 组织结构 | 三环模型 | 四角色模型（治理/能力/方案/质量） | 从"守护什么"改为"拥有什么" |
| 语义主权 | 未明确分层 | 双层：全局契约（创始人）+ 能力包（PM） | 审计修正 F-7 |
| 测试团队 | 未定义 | QA/Acceptance Owner × 4 人 | DD-TEST v1.1 + 创始人确认 |
| PM 职责 | PM 驱动 AI 编码 | PM 驱动 Cap-Spec + 产品验收 | 创始人裁决 |
| 门禁机读化 | 无 | QA/PM verdict 为 required status checks | 审计修正 F-4 |

---

## 1. 组织模型

### 1.1 四角色架构

```
                    ┌──────────────────────┐
                    │   创始人 / 治理 Owner   │
                    │   Governance Owner    │
                    │   拥有：规则本身        │
                    │   + 全局契约语义 SSOT  │
                    └──────────┬───────────┘
                               │ 通过 CODEOWNERS / rulesets / gates 行使治理权
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
    │ PM           │     │ 工程师        │     │ QA           │
    │ 能力 Owner   │     │ 方案 Owner   │     │ 质量 Owner   │
    │ 能力包语义   │     │ Design+Code │     │ Acceptance  │
    │ SSOT        │     │ + HPRD      │     │ + Verdict   │
    │ + 产品验收   │     │ (AI-first)  │     │             │
    └─────┬──────┘     └──────┬──────┘     └──────┬──────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ┌──────────▼───────────┐
                    │   AI 执行/审计舰队     │
                    │   （机制层，不是角色）   │
                    │   NODE-C 执行         │
                    │   NODE-D 审计         │
                    └──────────────────────┘
                               │
                    ┌──────────▼───────────┐
                    │   CI 门禁自动化层      │
                    │   L1-L3 BLOCKING      │
                    │   L4 ADVISORY         │
                    │   + required status   │
                    │     checks 机读化     │
                    └──────────────────────┘
```

### 1.2 四权分离原则

| 权 | Owner | 含义 | 不可与谁重合 |
|----|-------|------|------------|
| **语义主权** | 创始人（全局契约）+ PM（能力包） | 业务语义的 SSOT——分层持有 | 不可由工程师定义业务需求 |
| **技术实现** | 工程师 | 技术方案 + AI-first 编码 + 实现 | 不可由 PM 审技术设计 |
| **独立质量** | QA | 验收测试 + 质量放行 | 不可由工程师自己放行自己的代码 |
| **组织治理** | 创始人 | 规则、门禁、契约核心、内核 | 不可由执行者修改自己要遵守的规则 |

**语义主权分层规则**（v2.1 新增，F-7）：

- **全局契约语义 SSOT** = 创始人。包括：hl-contracts 核心路径（rules/、facts/、reasoncodes/、apis/、events/、decisions/、governance/）、iron rules、reason_code 体系、跨域接口规范。
- **能力包业务语义 SSOT** = PM。包括：Cap-Spec-1（能力包规格书）、Cap-Spec-2（验收场景集）。
- **包络约束**：能力包语义不得越出契约包络。PM 的 Cap-Spec 必须在创始人定义的契约框架内；如果 Cap-Spec 需要变更契约（新增 reason_code、修改 API 规范等），必须先走契约变更流程获得创始人批准。

**铁律**：同一条变更的四种 owner 不得完全重合。这是 SAAC A4（审计主权不可外包）和 A5（Can→Action→Audit）在组织层面的投射。

### 1.3 未来演进

当前阶段四权分离是必要的——组织刚进入 AI 驱动工作模式，需要明确的职责边界和独立审计。

未来唤龙超级工厂成熟后，可以让岗位折叠——每个人负责一条产线闭环，没有职位区别。但即使在那个阶段，同一条变更的四种 owner 仍然不能由同一个人担任——可以通过 AI 审计来替代部分人类 owner，但"执行"和"审计"始终分家。

---

## 2. 角色详细定义

### 2.1 创始人 / Governance Owner

**组织治理职责**：
- 全局契约语义 SSOT（hl-contracts 核心路径）的定义与裁决权
- 组织级 Gate/CI / Sentinel / 技术合伙人智能体 的策略制定
- SAAC 推导链文件的维护
- 风险分级与路径级 code ownership 规则
- CODEOWNERS + GitHub 组织级 rulesets 的制定与维护

**审批范围**：
- founder-owned paths 变更（kernel/、gateway/、framework/、.github/、hl-contracts 核心路径）
- reason_code 新增/变更（Cap-Spec-3 治理前置门）
- 高风险发布
- 战略能力包可选产品验收

**不再承担**：
- ~~所有 feature PR 的人工审批~~（改为 path-based CODEOWNERS + CI 门禁）
- ~~能力包的具体实现~~（交工程师 AI 编码）
- ~~Cap-Spec 的日常 merge~~（prd/biz/ 路径交 PM team 持有）

**治理权行使方式**：
```
创始人 → 定义规则 → 规则自动执行 → 创始人只在规则覆盖不到时介入
        │
        ├── CODEOWNERS（谁审什么路径）
        ├── GitHub rulesets（required checks / reviews / merge queue）
        ├── verification-gates（L1-L3 自动门禁）
        ├── required status checks（qa-verdict / pm-acceptance 机读化）
        ├── satisfaction-metrics（质量度量）
        └── sentinel（异常检测与告警）
```

### 2.2 PM / Capability Owner

**拥有**：
- 所负责能力包的业务语义 SSOT（在契约包络内）
- 验收场景定义
- 产品验收权

**产出**：
- Cap-Spec-1（能力包规格书）：能力边界、目标/非目标、业务规则意图
- Cap-Spec-2（验收场景集）：Case-{ID} + input/expected/验收方式。**owner = PM；QA = collaborator/reviewer**（v2.1 修正 F-5）
- Cap-Spec-3（业务码提案）：reason_code 新增/变更建议

**审批**：
- HPRD（审批工程师对 Cap-Spec 的业务语义理解是否正确——仅此一项，不审技术方案）
- 产品验收（可交互演示版本）→ 通过 `pm-acceptance` required status check 机读化

**不承担**：
- ~~design.md 审计~~（技术语言过多，PM 看不懂不如不审）
- ~~AI 编码~~（交工程师）
- ~~代码审查~~（交工程师互审 + AI 审计 + CI 门禁）
- ~~技术方案评审~~（交工程师 + AI reviewer）

### 2.3 工程师 / Solution Owner

**拥有**：
- 技术方案设计
- AI-first 编码实现（默认由 AI 生成，工程师可在必要时手动补充，但所有 diff 统一经过 CI 门禁）（v2.1 修正 F-9）
- 单元测试、集成测试
- HPRD（Cap-Spec 的理解确认件）

**产出**：
- design.md（技术设计文档）
- HPRD（理解确认件，交 PM 审批）
- 代码 + 单元测试 + 集成测试
- 可运行 demo（交 PM 产品验收）
- Evidence draft（测试证据初稿）

**审批**：
- design.md（工程师互审 + AI reviewer；核心路径加创始人）

**不承担**：
- ~~业务需求定义~~（Cap-Spec 是 PM 的 SSOT）
- ~~最终质量放行~~（交 QA 独立验收）
- ~~修改治理规则~~（交创始人）

#### 2.3.1 HPRD 规格（v2.1 修正 F-8：缩薄为理解确认件）

**全称**：Human-readable Product Design（人类可读产品设计）

**定位**：工程理解确认件——证明"工程师理解对了没有"，不是"工程师重新定义了产品"。

**最小模板**：

| 字段 | 必填 | 说明 |
|------|------|------|
| Capability ID | 是 | 对应哪个能力包的 Cap-Spec |
| User-visible Changes | 是 | 用户会看到什么变化 |
| Unchanged Behavior | 是 | 哪些行为必须保持不变 |
| Out of Scope | 是 | 这次明确不做什么 |
| Acceptance Walkthrough | 是 | PM 将如何验收（对应 Cap-Spec-2 中的哪些 Case-ID） |
| Semantic Questions | 否 | 工程师理解中仍未决的问题 |

**约束**：
- HPRD 不是上游规格——上游 SSOT 始终是 PM 的 Cap-Spec
- 如果 HPRD 和 Cap-Spec 冲突，以 Cap-Spec 为准，由工程师修正 HPRD
- PM 审批 HPRD 的内容是"业务语义有没有理解错"，不是追加需求，不是审批技术方案
- HPRD 不包含技术实现细节（数据库设计、API 内部结构、类层次等）
- HPRD 不单独驱动开发，必须附着 Cap-Spec ID

**与其他产物的关系**：
```
Cap-Spec（PM 能力包语义 SSOT）
    ↓ 工程师解读
HPRD（PM 审批：理解是否忠于 Cap-Spec）
    ↓ 工程师技术设计
design.md（工程师互审 + AI reviewer）
    ↓ AI-first 编码
代码 + 测试
    ↓ CI 门禁 + QA 验收 + PM 产品验收（全部机读化）
merge
```

### 2.4 QA / Acceptance Owner

**拥有**：
- 独立质量验证权
- 验收自动化
- 回归基线
- 测试证据
- 发布质量 verdict

**产出**：
- acceptance-manifest.yaml（验收映射清单，每个能力包一份）
- Executable acceptance suite（可执行验收测试套件）
- Regression baseline（回归基线）
- Quality verdict（PASS / FAIL）→ 通过 `qa-verdict` required status check 机读化

**审批**：
- staging/prod 质量放行（qa-verdict 是 merge 前 required status check）

**不承担**：
- ~~功能代码实现~~
- ~~业务需求定义~~（Cap-Spec-2 的 owner 是 PM，QA 是 collaborator/reviewer）
- ~~技术方案设计~~

**与工程师的测试分工**：
| 测试类型 | Owner | 说明 |
|---------|-------|------|
| 单元测试 | 工程师 | governedAction 五条必过测试 + domain 逻辑 |
| 集成测试 | 工程师 | Testcontainers 端到端 |
| 验收测试 | QA | 基于 Cap-Spec-2 验收场景集 |
| 回归测试 | QA | 基于回归基线 |
| 属性测试 | 工程师 + QA | 工程师写 kernel 属性测试，QA 写能力包边界属性测试 |

### 2.5 UI 设计师

**定位**：产品能力的视觉/交互维度 owner，归属于 PM 能力环。

**产出**：
- 设计规格（设计稿 / 交互原型 / 设计标注）
- 设计系统组件（Design Token / 组件规范）

**协作模式**：
- UI 设计师的产出是 Cap-Spec 的视觉维度补充——PM 定义"做什么"，UI 设计师定义"长什么样"
- 前端工程师消费 UI 设计规格，通过 AI 编码实现 Flutter 界面
- UI 设计师参与产品验收（视觉/交互验收维度）

**不承担**：
- 代码实现（交前端工程师 AI 编码）
- 技术选型（交工程师）

### 2.6 运维工程师 / Release & Infra Owner

**拥有**：
- 发布流水线（CI/CD pipeline 运维）
- 环境管理（dev / staging / prod）
- 基础设施运维（数据库、服务器、监控）
- 发布执行与回滚

**产出**：
- 环境配置与部署脚本
- 发布记录（release record）
- 监控告警配置
- 基础设施变更记录

**协作模式**：
- 创始人定义发布策略和环境保护规则（GitHub environments + deployment protection）
- 工程师 PR merge 后，运维执行发布流水线
- QA 在 staging 环境验收通过后，运维推 prod
- 运维不做代码审查、不做业务定义、不做技术方案设计

**在 AI 驱动模型中的定位**：
- CI/CD pipeline 的日常运维和故障排查
- 基础设施即代码（IaC）的维护——AI 可辅助生成，运维负责审核和执行
- 发布窗口协调（与 QA 验收、PM 产品验收的时序对齐）

### 2.7 AI 执行/审计舰队（机制层）

**定位**：AI 不是角色，是基础设施。

| 节点 | 职能 | 约束 |
|------|------|------|
| NODE-C（执行/调度） | 代码草稿、测试草稿、规格 formalize、首轮 review | 不做最终 owner |
| NODE-D（独立审计） | 异源模型审计、交叉验证、审计摘要 | 不替代人类审批 |
| sentinel | 异常检测、治理偏移告警 | 只告警，不阻断 |

**铁律**：AI 输出是草稿和证据，不是裁决。所有最终裁决（merge / reject / release）必须由人类 owner 做出。

---

## 3. 人员编制

### 3.1 当前编制（21 人）

| 角色 | 人数 | 人员来源 | 对应角色 |
|------|------|---------|-----------|
| PM | 3 | 现有产品经理 | PM / Capability Owner |
| UI 设计师 | 2 | 现有 UI 设计师 | UI 设计师（归属 PM 能力环） |
| 后端工程师 | 6 | 现有 Java 工程师 | 工程师 / Solution Owner（后端） |
| 前端工程师 | 5 | 4 web + 1 Flutter（全部转 Flutter） | 工程师 / Solution Owner（前端） |
| 测试工程师 | 4 | 现有测试人员 | QA / Acceptance Owner |
| 运维工程师 | 1 | 现有运维 | Release & Infra Owner |

**创始人**在 21 人之外，作为 Governance Owner。

### 3.2 能力包分配

基于 biz-C6-能力包边界预分析稿 的 10 个能力包三级分层：

| 能力包 | 分级 | PM | 后端工程师 | 前端工程师 | QA |
|--------|------|-----|-----------|-----------|-----|
| biz.flow.sales（销售流程） | T1 | PM-A | 2 | 1-2 | QA 横向覆盖 |
| biz.customer.asset（客户资产） | T1 | PM-A | 2 | 1 | QA 横向覆盖 |
| biz.payment.checkout（支付结账） | T1 | PM-B | 2 | 1 | QA 横向覆盖 |
| biz.marketing.promotion（营销） | T2 | PM-B | — | — | — |
| biz.product.center（商品中心） | T2 | PM-B | — | — | — |
| biz.supply.warehouse（供应仓储） | T2 | PM-C | — | — | — |
| biz.analytics.dashboard（数据看板） | T2 | PM-C | — | — | — |
| biz.hardware.pos（硬件POS） | T3 | PM-C | — | — | — |
| biz.aftersales.service（售后服务） | T3 | PM-A | — | — | — |
| biz.infra.bpm（流程引擎） | T3 | PM-C | — | — | — |

**说明**：

- T1 先行：6 后端 + 5 前端集中到 T1 三个包；T2/T3 在 T1 完成后滚动开发
- PM 全覆盖：3 PM 各负责 3-4 个包，T1 阶段 PM-A/PM-B 压力最大
- QA 横向覆盖：4 QA 不按能力包分配，按测试类型分工（1 架构师 + 3 工程师）
- UI 设计师 2 人横向支持所有有 UI 界面的能力包
- 前端 5 人按场景前端线统一转向 Flutter / Dart（`huanlongAI/hl-scene-app`）
- `hl-console-native` 不在本转型范围内，继续按 SwiftUI / GHKit 治理客户端口径执行

### 3.3 QA 团队内部分工

| 角色 | 人数 | 职责 |
|------|------|------|
| QA 架构师 | 1 | acceptance-manifest 标准制定、测试基础设施搭建、验收框架设计、质量度量体系 |
| QA 工程师 | 3 | 验收测试编写与执行、回归测试维护、测试证据收集、quality verdict 出具 |

---

## 4. 产物矩阵

| 产物 | Owner | 审批人 | 性质 | 存放位置 |
|------|-------|--------|------|---------|
| Cap-Spec-1（能力包规格书） | PM | PM freeze；创始人可选审批 | 能力包业务语义 SSOT | hl-contracts/prd/biz/ |
| Cap-Spec-2（验收场景集） | PM | PM（QA 为 collaborator/reviewer） | 验收标准 | hl-contracts/prd/biz/ |
| Cap-Spec-3（业务码提案） | PM | **创始人必须先批**（治理前置门） | reason_code 变更 | hl-contracts/reasoncodes/ （合入后） |
| HPRD（理解确认件） | 工程师 | PM（仅审业务理解正确性） | Cap-Spec 派生解读 | hl-platform/docs/hprd/{capability}/ |
| design.md（技术设计） | 工程师 | 工程师互审 + AI reviewer | 技术方案 | hl-platform/docs/design/{capability}/ |
| 代码 | 工程师（AI-first） | CI 门禁 + 工程师互审 | 实现 | hl-platform/app/biz-*/ |
| 单元/集成测试 | 工程师 | CI 门禁 | 实现验证 | hl-platform/app/biz-*/src/test/ |
| acceptance-manifest.yaml | QA | QA | 验收映射 | hl-platform/app/biz-*/acceptance/ |
| 验收测试套件 | QA | QA | 独立质量验证 | hl-platform/app/biz-*/acceptance/ |
| Quality Verdict | QA | — | required status check `qa-verdict` | PR status check |
| PM Acceptance | PM | — | required status check `pm-acceptance` | PR status check |
| Evidence Pack | 工程师 + QA | QA + PM | 合并前验收包 | PR 附件 |
| UI 设计规格 | UI 设计师 | PM | 视觉/交互标准 | 设计工具（不作强制限定） |

---

## 5. 工作流

### 5.1 流程分类（v2.1 新增，F-10）

本文档定义**能力包交付主流程**。其他流程类型另见附属文件：

| 流程类型 | 适用场景 | 定义文档 |
|---------|---------|---------|
| **能力包流** | 新功能、用户可见能力变化 | 本文档 §5.2 |
| 缺陷修复流 | 缺陷修复、回归修复 | WORKFLOW-GUIDE v1 |
| 技术改动流 | 重构、性能、可观测性、工程性改动 | WORKFLOW-GUIDE v1 |
| 治理/内核流 | HK、contracts、gates、framework | WORKFLOW-GUIDE v1 |

### 5.2 能力包交付流程（五步）

```
Step 1: Cap-Spec Freeze
  PM 编写 Cap-Spec（规格书 + 验收场景集 + 业务码提案）
  UI 设计师补充视觉/交互设计
  ┌── 分支（v2.1 修正 F-2）：
  │   若 Cap-Spec-3 涉及新增/变更 reason_code：
  │     → 创始人先批准 reason_code 变更（治理前置门）
  │     → 批准后 PM 方可宣布 freeze
  └── 若 Cap-Spec-3 无契约变更：
      → PM 直接宣布 Cap-Spec freeze

Step 2: Design + HPRD
  工程师阅读 Cap-Spec，产出：
    ├── HPRD（理解确认件）→ 交 PM 审批业务理解
    │   （PM 仅审 HPRD，不审 design.md）
    └── design.md（技术设计）→ 工程师互审 + AI reviewer
  QA 同步开始编写 acceptance-manifest.yaml
  → PM 审批 HPRD 通过（pm-hprd-pass required status check — BLOCKING）
  → design.md 工程师互审通过
  ⛔ pm-hprd-pass 未通过前，工程师不得开始 Step 3 实现（防止"先做后补审"回退）

Step 3: Implementation + Tests
  工程师通过 AI-first 编码实现：
    ├── 功能代码（AI 生成为主，人工可补，统一过 gate）
    ├── 单元测试（governedAction 五条必过 + domain 逻辑）
    ├── 集成测试（Testcontainers）
    └── 可运行 demo
  QA 同步编写验收测试套件
  → 工程师提交 Draft PR

Step 4: 门禁 + 验收（并行）（v2.1 修正 F-6：对齐 DD-TEST）
  ┌── CI 门禁（自动，BLOCKING）
  │     L1: 编译、类型检查、格式
  │     L2: 契约一致性、模块边界、ReasonCode 对齐、G-026 验收覆盖率（manifest-based）
  │     L3: 单元测试、集成测试、G-023 验收场景回放
  ├── AI 审计（L4，ADVISORY）
  │     NODE-D 异源模型交叉审计
  ├── QA 验收
  │     执行验收测试套件 → 出具 Quality Verdict → qa-verdict status check
  └── 工程师互审（code review）
  → Draft PR 转 Ready for Review（触发 path-based CODEOWNERS review）
  → required status checks 全部通过：
      ✅ L1-L3 全绿
      ✅ qa-verdict = PASS
      ✅ code owner approved

Step 5: PM 产品验收 + Merge
  PM 在可交互演示版本上执行产品验收
  → pm-acceptance status check = PASS
  → Merge（进入 merge queue）
  → 如涉及 founder-owned paths → 创始人额外审批

Post-Merge: 发布
  运维工程师按发布策略执行部署
    ├── staging 环境部署 → QA 回归验证
    └── prod 环境部署 → 运维监控 + 回滚预案
```

### 5.2 能力包流最小状态机（Pilot-Lock 裁决新增）

| 状态 | Owner | 进入条件 | 退出条件 | 可回退至 |
|------|-------|---------|---------|---------|
| Proposed | PM | 能力包立项 | change_class 明确 + contract_touch 判定完成 | Cancelled |
| Contract Envelope Locked | 创始人/PM | 已确认是否触碰契约包络 | 若触碰 → 创始人审批通过；若未触碰 → 直接通过 | Proposed |
| Cap-Spec Frozen | PM | Cap-Spec-1/2/3 全部冻结 | PM 确认冻结 | Contract Envelope Locked |
| HPRD Passed | PM | 工程师提交 HPRD | pm-hprd-pass = PASS | Cap-Spec Frozen |
| Design Approved | 工程师 | 工程师完成 design.md | 工程师互审通过 | HPRD Passed |
| Draft PR Open | 工程师 | 实现 + 测试初版就绪 | Draft PR 已创建 | Design Approved |
| Gates Passed | CI | CI 门禁执行 | L1-L3 全绿 | Draft PR Open |
| QA Passed | QA | QA 执行验收 | qa-verdict = PASS | Draft PR Open |
| PM Accepted | PM | PM 产品验收 | pm-acceptance = PASS | Draft PR Open / QA Passed |
| Merged | System | 所有 required checks PASS | merge queue 完成 | 上游任一失败态 |
| Released | 运维 | staging 验证通过 | prod 部署完成 | Rollback |
| Writeback Pending | 多 owner | 发布后 | 回写完成（v2.2 定义） | — |

**状态机使用说明**：
- 本状态机仅覆盖**能力包流**（Capability Flow）。缺陷修复、技术改动、治理/内核流的状态机另见 WORKFLOW-GUIDE。
- 回退时必须清理下游产物（如从 HPRD Passed 回退到 Cap-Spec Frozen，已有的 HPRD 标记为 INVALIDATED）。
- Contract Envelope Locked 阶段使用 PR 分类模板（§5.3）判定。

### 5.3 PR 分类与契约包络检测（Pilot-Lock 裁决新增）

每个能力包 PR 提交时必须填写以下分类字段（在 PR template 或 PR body 中声明）：

```yaml
# PR Classification（必填）
change_class: capability    # capability | defect-fix | tech-improvement | governance
contract_touch: false       # true | false — 是否触碰 hl-contracts 核心路径
founder_required: false     # true | false — 是否需要创始人审批

# Contract Touch Checklist（当 contract_touch = true 时必填）
contract_touch_detail:
  reason_code_change: false    # 是否新增/修改 reason_code
  iron_rule_impact: false      # 是否涉及五条铁律
  api_contract_change: false   # 是否变更 /apis/ 下的契约定义
  event_schema_change: false   # 是否变更 /events/ 下的事件 schema
  cross_tenant_impact: false   # 是否涉及跨租户行为（IR-3）
```

**分类规则**：
- `contract_touch = true` → 自动触发 `founder_required = true`
- `change_class = governance` → 自动触发 `founder_required = true`
- `change_class = capability` 且 `contract_touch = false` → `founder_required = false`（path-based gate 自动放行）
- `change_class ≠ capability` → 不走本文档 §5.1 能力包流，走 WORKFLOW-GUIDE 对应流程

---

## 6. Path-Based 门禁模型

### 6.1 hl-contracts CODEOWNERS（v2.1 修正 F-1：拆分路径）

```
# hl-contracts/CODEOWNERS
# v2.1：拆分契约核心路径（创始人强制）与 Cap-Spec 路径（PM 持有）

# —— 默认：创始人 ——
*                           @founder

# —— 契约核心：创始人强制审批 ——
/decisions/                 @founder
/facts/                     @founder
/rules/                     @founder
/reasoncodes/               @founder
/apis/                      @founder
/events/                    @founder
/governance/                @founder
/auth/                      @founder
/.github/                   @founder
CLAUDE.md                   @founder
RULINGS.md                  @founder

# —— PRD：默认创始人；biz Cap-Spec 单独下放给 PM team ——
/prd/                       @founder
/prd/biz/**                 @hl-pm-team

# —— 说明：/prd/biz/** 最后匹配，覆盖 /prd/ 默认规则 ——
# PM team 持有 biz Cap-Spec；core/console/data 仍由创始人默认审查
```

### 6.2 hl-platform CODEOWNERS（v2.1 修正 F-3：重排顺序 + 补路径）

```
# hl-platform/CODEOWNERS
# v2.1：先广后窄，最后匹配优先
# 顺序：默认 → founder 路径 → 能力包广规则 → QA 窄规则 → docs 路径

# —— 默认：工程师互审 ——
*                                         @hl-engineers

# —— Kernel / Gateway / Framework / CI：创始人强制 ——
/kernel/**                                @founder
/gateway/**                               @founder
/framework/**                             @founder
/.github/**                               @founder
/governance/**                            @founder
/scripts/**                               @founder
build.gradle.kts                          @founder
settings.gradle.kts                       @founder

# —— Contract 引用同步：创始人 + 工程师 ——
/contract/**                              @founder @hl-engineers

# —— 能力包业务代码：工程师互审（广规则）——
/app/biz-*/**                             @hl-engineers

# —— 能力包验收测试：QA 团队（窄规则，覆盖上面的广规则）——
/app/**/acceptance/**                     @hl-qa-team
/app/**/acceptance-manifest*              @hl-qa-team

# —— HPRD 文档：PM 团队 ——
/docs/hprd/**                             @hl-pm-team

# —— 技术设计文档：工程师互审 ——
/docs/design/**                           @hl-engineers
```

### 6.3 hl-factory CODEOWNERS

```
# hl-factory/CODEOWNERS — 创始人强制审批
*                                         @founder
```

### 6.4 hl-console-native CODEOWNERS

```
# hl-console-native/CODEOWNERS
*                                         @hl-frontend-engineers
/.github/**                               @founder
```

### 6.5 GitHub 组织级 Rulesets（v2.1 修正 F-4：补 required status checks）

| Ruleset | 适用仓库 | 规则 |
|---------|---------|------|
| require-pr | 全部 | 禁止直推 main/develop，必须通过 PR |
| require-status-checks | 全部 | L1-L3 门禁全绿才能 merge |
| require-code-owner-review | 全部 | path-based code owner 必须 approve |
| **require-pm-hprd-pass** | hl-platform | `pm-hprd-pass` status check = PASS（Draft PR 前置 gate：工程师开始实现前，PM 必须确认 HPRD 理解正确）|
| **require-qa-verdict** | hl-platform, hl-console-native | `qa-verdict` status check = PASS（能力包 PR 必须）|
| **require-pm-acceptance** | hl-platform, hl-console-native | `pm-acceptance` status check = PASS（能力包 PR 必须）|
| merge-queue | hl-platform, hl-console-native | 启用 merge queue，避免合并冲突 |
| no-bypass | 全部 | 无人可绕过规则（包括 admin） |
| founder-paths-protection | hl-platform | kernel/ gateway/ framework/ .github/ 路径 → 必须创始人 approve |

**机读化说明**（v2.1 新增）：

`qa-verdict` 和 `pm-acceptance` 是 GitHub Actions workflow 中的 required status checks。具体实现方式（如 PR label、review approval、外部系统回调）在 TOOLCHAIN-GUIDE 中定义。治理文件只锁"必须有这个 check 且为 PASS"，不锁实现方式。

---

## 7. 技术适配要求

### 7.1 后端工程师：Java 背景 + Kotlin 技术栈

当前 6 名后端工程师是 Java 背景，技术栈为 Kotlin 2.1.10。在 AI-first 模式下：

- AI 生成代码为主，工程师可在必要时手动补充，所有 diff 统一经过 CI 门禁
- 工程师需要能读懂 Kotlin 代码（review AI 产出）、定义类型和接口（意图定义）、理解 Kotlin 特性（sealed class / value class / coroutines）以做验证和裁决
- 适配措施：通过实际能力包开发在 AI 编码过程中自然习得。Java 工程师对 JVM 生态的理解（Spring Boot / JPA / Gradle）可以直接复用

### 7.2 前端工程师：Web → Flutter 转型

4 名 web 前端 + 1 名 Flutter = 5 人，全部转 Flutter。同 7.1 逻辑——AI 生成 Flutter 代码，工程师负责意图/验证/裁决。现有 Flutter 工程师（1 人）作为前端技术 lead。

### 7.3 测试团队适配

4 名测试工程师转型为 QA / Acceptance Owner：从"手动测试执行者"转为"验收自动化 owner + 质量判定者"。需要掌握 JUnit 5 验收测试编写、acceptance-manifest.yaml 管理、CI 报告解读。QA 架构师额外需要测试基础设施搭建和验收框架设计。

---

## 8. 裁决记录

| 编号 | 裁决 | 日期 | 来源 |
|------|------|------|------|
| R-TEAM-001 | 全组织 21 人同步进入 AI 驱动模式，不再分批过渡 | 2026-04-11 | 创始人 |
| R-TEAM-002 | 创始人退出能力包 feature PR 人工审批，改为 path-based CODEOWNERS + CI 门禁自动放行 | 2026-04-11 | 创始人 |
| R-TEAM-003 | 工程师产出 HPRD（Human-readable Product Design），PM 审批业务理解正确性 | 2026-04-11 | 创始人 |
| R-TEAM-004 | PM 不审 design.md | 2026-04-11 | 创始人 |
| R-TEAM-005 | 测试团队 4 人定位为 QA / Acceptance Owner（1 架构师 + 3 工程师） | 2026-04-11 | 创始人 |
| R-TEAM-006 | 工具链选型作为附属文件（TOOLCHAIN-GUIDE），不在治理文件中锁死具体产品 | 2026-04-11 | 创始人 |
| R-TEAM-007 | 场景前端线转 Flutter；web 前端 4 人 + Flutter 1 人统一到 `hl-scene-app` / Flutter / Dart。scope erratum 2026-04-25：不覆盖 C 域治理客户端，治理客户端仍为 SwiftUI / GHKit。 | 2026-04-11 | 创始人 |
| R-TEAM-008 | 语义主权分层：PM = 能力包 SSOT；创始人 = 全局契约 SSOT | 2026-04-11 | 审计仲裁 |
| R-TEAM-009 | QA verdict / PM acceptance 必须为 required status checks，不接受口头放行 | 2026-04-11 | 审计仲裁 |
| R-TEAM-010 | AI-first 编码：默认 AI 生成，人工可补，统一过 gate | 2026-04-11 | 审计仲裁 |
| R-TEAM-011 | v2.1 保持 DRAFT，按 Pilot-Locked for Capability Flow 执行；能力包流可执行，非能力包流待 WORKFLOW-GUIDE 补齐 | 2026-04-11 | 创始人 |
| R-TEAM-012 | pm-hprd-pass 升级为 required status check（Draft PR 前置 gate），工程师不得在 HPRD 通过前开始实现 | 2026-04-11 | 创始人 |
| R-TEAM-013 | 每个能力包 PR 必须填写 PR 分类（change_class / contract_touch / founder_required），契约触碰自动升级创始人审批 | 2026-04-11 | 创始人 |
| R-TEAM-014 | 最小状态机立即生效（§5.2），为退回/挂起/冲突提供统一语言；完整状态机在 v2.2 中基于试运行数据校准 | 2026-04-11 | 创始人 |

---

## 9. 退出条件与验证指标

### 9.1 Pilot-Lock → LOCKED 升级条件（R-TEAM-011）

本文档从 Pilot-Locked 升级到 LOCKED，需满足以下**全部 4 个通过门槛**：

| # | 通过门槛 | 验证方法 |
|---|---------|---------|
| 1 | 至少 1 个不触碰契约的 T1 slice 全链路通过 | 从 Proposed → Released 完整走通 |
| 2 | 至少 1 个触碰 reason_code 的 T1 slice 全链路通过 | Contract Envelope Locked 阶段创始人审批 → Released |
| 3 | qa-verdict、pm-acceptance、pm-hprd-pass 全部机读落地 | GitHub Actions 中 3 个 required status checks 真实运行 |
| 4 | 没有出现"能力包流误套到技术改动流"的严重混乱 | PR 分类（§5.3）有效分流 |

### 9.2 核心验证指标

| 指标 | 看什么 | 采集来源 |
|------|--------|---------|
| HPRD Rejection Rate | 工程师对业务语义理解偏差率 | pm-hprd-pass 打回次数 / 总 HPRD 提交次数 |
| Contract Envelope Miss Count | 已 freeze 后才发现触碰契约的次数 | PR 分类回溯 |
| QA Lead Time | QA 是否成为主瓶颈 | qa-verdict 从 PR 开始到 PASS 的时间 |
| PM Acceptance Rework Rate | PM 产品验收打回轮数 | pm-acceptance 打回次数 / 总提交次数 |
| Founder Queue Load | 创始人是否真的退出 feature PR 队列 | 创始人 review 的能力包 PR 数 |
| Non-Capability Misroute Count | 缺陷修复/技术改动是否被迫走能力包流 | change_class 字段回溯 |
| Gate Bypass Count | 有没有绕过 rulesets/checks 的情况 | GitHub audit log |
| Escape Defect Rate | QA/PM 通过后仍逃逸的问题比例 | 发布后缺陷追溯 |

### 9.3 版本演进触发条件

| 触发条件 | 修订方向 |
|---------|---------|
| T1 试运行通过 4 个门槛 | 升级为 LOCKED；评估 v2.2 候选项 |
| 团队规模变化 | 更新能力包分配，调整人员矩阵 |
| T1 能力包全部交付 | 滚动分配 T2 工程师，更新能力包分配表 |
| 唤龙超级工厂成熟 | 开始评估"每人一条产线闭环"的岗位折叠 |
| 微服务拆分（R-055 退出） | 更新 CODEOWNERS 适配多仓库/多服务架构 |
| AI 审计能力成熟到可替代部分人类 owner | 评估哪些审批环节可以由 AI 独立完成 |

---

## 附录 A：与 v1.2 的完整变更追溯

| v1.2 条款 | v2.1 状态 | 说明 |
|-----------|----------|------|
| D-1 三环模型 | SUPERSEDED | 改为四角色模型 |
| D-2 不设业务开发者 | SUPERSEDED | 新增工程师 / Solution Owner，承担 AI-first 编码 |
| D-3 能力包启动流程 | EVOLVED | 保留 Cap-Spec 先行原则，更新为五步流程 + 治理前置门 |
| D-4 契约变更流程 | PRESERVED | 保持不变（另见 WORKFLOW-GUIDE） |
| D-5 核心组 7 人 | SUPERSEDED | 改为全组织 21 人 |
| R-056 不设业务开发者岗位 | SUPERSEDED | 设工程师岗位 |
| R-057 创始人 + AI 全覆盖 | EVOLVED | 工程师覆盖能力包（AI-first） |
| R-058 核心组 7 人 | SUPERSEDED | 21 人全组织 |

---

*本文档为 DRAFT / Pilot-Locked for Capability Flow（创始人 2026-04-11 裁决）。*
*锁版前置条件：1. Cap-Spec owner 冲突已消除 ✅（F-1）；2. QA/PM/Founder 门禁机读化 ✅（F-4）；3. pm-hprd-pass 纳入 required check ✅（R-TEAM-012）；4. 最小状态机落地 ✅（R-TEAM-014）；5. §9.1 全部 4 个通过门槛满足（待 T1 试运行验证）。*
