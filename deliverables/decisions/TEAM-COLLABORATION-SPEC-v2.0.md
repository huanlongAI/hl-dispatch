# 唤龙平台团队协作规格

## TEAM-COLLABORATION-SPEC v2.0 — 全组织 AI 驱动协作模型

---

**文档编号**：TEAM-COLLAB-SPEC-001
**版本**：v2.0
**日期**：2026-04-11
**状态**：DRAFT（待创始人审计裁决）
**替代文档**：TEAM-COLLABORATION-SPEC v1.2（SUPERSEDED——v1.2 基于 7 人核心组 + 创始人写全部代码前提，已不适用）
**派生链**：SAAC-HL-001 v1.1 §1.3 → BRIDGE-DERIVATION v1 → PRD-REDEFINITION-SPEC v2.0 → DD-TEST v1.1 → 创始人 2026-04-11 组织裁决 → 本文档

> 说明：v2.0 为 v2.1 之前的历史基线。涉及 `biz.*` 能力包 Cap-Spec 存放位置时，以当前纠偏后的 `hl-contracts/prd/biz/` 为执行口径，不再沿用文中早期的 `prd/core/{capability}` 中间写法。

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
| I-6 | DD-TEST v1.1 | 测试工程推导（JUnit 5 / Kotest Property / Testcontainers / acceptance-manifest.yaml） |
| I-7 | 创始人 2026-04-11 裁决 | 全组织 21 人 AI 驱动，不再分批过渡 |
| I-8 | 创始人 2026-04-11 裁决 | path-based CODEOWNERS + CI 门禁自动放行，创始人退出能力包 feature PR 人工审批 |
| I-9 | 创始人 2026-04-11 裁决 | HPRD（Human-readable Product Design）替代 Impl-Semantics 术语 |
| I-10 | GPT Pro 独立评审 2026-04-11 | 四权分离建议（语义主权 / 技术实现 / 独立质量 / 组织治理）；创始人采纳方向，拒绝具体工具锁定 |

### 0.3 推导逻辑

```
I-1（AI 驱动）+ I-7（全组织 21 人）
  → v1.2 的"创始人 + AI = 100% 代码"前提失效
  → 组织级项目中，工程师承担 AI 编码职责
  → 创始人定位为治理 owner

I-5（PM = 产线责任人）+ I-9（HPRD）
  → PM 拥有业务语义 SSOT（Cap-Spec）
  → 工程师产出 HPRD（Cap-Spec 的派生解读），PM 审批业务理解正确性
  → PM 不审 design.md，不进技术审批链

I-6（DD-TEST）+ I-10（四权分离）
  → 测试团队独立于工程师，拥有验收放行权
  → 执行（工程师）与审计（QA + AI）分家

I-8（path-based gate）
  → 创始人通过规则本身（CODEOWNERS / rulesets / gates）行使治理权
  → 能力包 PR 由工程师互审 + QA 验收 + CI 门禁放行
  → 创始人只在 founder-owned paths 和高风险发布强制介入
```

### 0.4 与 v1.2 的关键变更

| 维度 | v1.2 | v2.0 | 变更原因 |
|------|------|------|---------|
| 团队规模 | 7 人核心组 | 21 人全组织 | 创始人裁决：不再分批过渡 |
| 代码产出 | 创始人 + AI = 100% | 工程师做能力包 AI 编码 | 组织级项目，工程师承担实现职责 |
| PR 审批 | 创始人审所有 PR | path-based CODEOWNERS + CI 门禁 | 创始人裁决：避免成为系统瓶颈 |
| 组织结构 | 三环模型（守护者/业务/基础设施） | 四角色模型（治理/能力/方案/质量） | 从"守护什么"改为"拥有什么" |
| 测试团队 | 未定义 | QA/Acceptance Owner × 4 人 | DD-TEST v1.1 推导 + 创始人确认 |
| PM 职责 | PM 驱动 AI 编码 | PM 驱动 Cap-Spec + 产品验收；AI 编码交工程师 | 创始人 2026-04-11 裁决 |
| PRD 术语 | Cap-Spec 替代 PRD | 新增 HPRD（工程师→PM 的产品设计解读） | 创始人裁决：名称需团队易懂 |

---

## 1. 组织模型

### 1.1 四角色架构

```
                    ┌──────────────────────┐
                    │   创始人 / 治理 Owner   │
                    │   Governance Owner    │
                    │   拥有：规则本身        │
                    └──────────┬───────────┘
                               │ 通过 CODEOWNERS / rulesets / gates 行使治理权
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
    │ PM           │     │ 工程师        │     │ QA           │
    │ 能力 Owner   │     │ 方案 Owner   │     │ 质量 Owner   │
    │ Cap-Spec    │     │ Design+Code │     │ Acceptance  │
    │ + 产品验收   │     │ + HPRD      │     │ + Verdict   │
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
                    └──────────────────────┘
```

### 1.2 四权分离原则

| 权 | Owner | 含义 | 不可与谁重合 |
|----|-------|------|------------|
| **语义主权** | PM | 业务语义的 SSOT（Cap-Spec） | 不可由工程师定义业务需求 |
| **技术实现** | 工程师 | 技术方案 + AI 编码 + 实现 | 不可由 PM 审技术设计 |
| **独立质量** | QA | 验收测试 + 质量放行 | 不可由工程师自己放行自己的代码 |
| **组织治理** | 创始人 | 规则、门禁、契约、内核 | 不可由执行者修改自己要遵守的规则 |

**铁律**：同一条变更的四种 owner 不得完全重合。这是 SAAC A4（审计主权不可外包）和 A5（Can→Action→Audit）在组织层面的投射。

### 1.3 未来演进

当前阶段四权分离是必要的——组织刚进入 AI 驱动工作模式，需要明确的职责边界和独立审计。

未来唤龙超级工厂成熟后，可以让岗位折叠——每个人负责一条产线闭环，没有职位区别。但即使在那个阶段，同一条变更的四种 owner 仍然不能由同一个人担任——可以通过 AI 审计来替代部分人类 owner，但"执行"和"审计"始终分家。

---

## 2. 角色详细定义

### 2.1 创始人 / Governance Owner

**组织治理职责**：
- 唤龙契约（hl-contracts）的定义与裁决权
- 组织级 Gate/CI / Sentinel / 技术合伙人智能体 的策略制定
- SAAC 推导链文件的维护
- 风险分级与路径级 code ownership 规则
- CODEOWNERS + GitHub 组织级 rulesets 的制定与维护

**审批范围**：
- founder-owned paths 变更（kernel/、gateway/、framework/、.github/、hl-contracts/）
- 高风险发布
- 战略能力包可选产品验收

**不再承担**：
- ~~所有 feature PR 的人工审批~~（改为 path-based CODEOWNERS + CI 门禁）
- ~~能力包的具体实现~~（交工程师 AI 编码）

**治理权行使方式**：
```
创始人 → 定义规则 → 规则自动执行 → 创始人只在规则覆盖不到时介入
        │
        ├── CODEOWNERS（谁审什么路径）
        ├── GitHub rulesets（required checks / reviews / merge queue）
        ├── verification-gates（L1-L3 自动门禁）
        ├── satisfaction-metrics（质量度量）
        └── sentinel（异常检测与告警）
```

### 2.2 PM / Capability Owner

**拥有**：
- 所负责能力包的业务语义、范围、目标/非目标
- 验收场景定义
- 产品验收权

**产出**：
- Cap-Spec-1（能力包规格书）：能力边界、目标/非目标、业务规则意图
- Cap-Spec-2（验收场景集）：Case-{ID} + input/expected/验收方式
- Cap-Spec-3（业务码提案）：reason_code 新增/变更建议

**审批**：
- HPRD（审批工程师对 Cap-Spec 的业务语义理解是否正确）
- 产品验收（可交互演示版本）

**不承担**：
- ~~design.md 审计~~（技术语言过多，PM 看不懂不如不审）
- ~~AI 编码~~（交工程师）
- ~~代码审查~~（交工程师互审 + AI 审计 + CI 门禁）
- ~~技术方案评审~~（交工程师 + AI reviewer）

### 2.3 工程师 / Solution Owner

**拥有**：
- 技术方案设计
- AI 编码实现（全部代码通过 AI 生成，工程师负责意图/验证/裁决）
- 单元测试、集成测试
- HPRD（Cap-Spec 的人类可读产品设计解读）

**产出**：
- design.md（技术设计文档）
- HPRD（Human-readable Product Design，交 PM 审批）
- 代码（通过 AI 编码工具生成）
- 单元测试 + 集成测试
- 可运行 demo（交 PM 产品验收）
- Evidence draft（测试证据初稿）

**审批**：
- design.md（工程师互审 + AI reviewer；核心路径加创始人）

**不承担**：
- ~~业务需求定义~~（Cap-Spec 是 PM 的 SSOT）
- ~~最终质量放行~~（交 QA 独立验收）
- ~~修改治理规则~~（交创始人）

#### 2.3.1 HPRD 规格

**全称**：Human-readable Product Design（人类可读产品设计）

**定义**：工程师基于 PM 的 Cap-Spec，用非技术语言重新表述的产品设计解读——说明"这个能力包我打算做什么、用户会看到什么变化、边界在哪里、不做什么"。

**约束**：
- HPRD 不是上游规格——上游 SSOT 始终是 PM 的 Cap-Spec
- 如果 HPRD 和 Cap-Spec 冲突，以 Cap-Spec 为准，由工程师修正 HPRD
- PM 审批 HPRD 的内容是"业务语义有没有理解错"，不是审批技术方案
- HPRD 不包含技术实现细节（数据库设计、API 内部结构、类层次等）

**与其他产物的关系**：
```
Cap-Spec（PM SSOT）
    ↓ 工程师解读
HPRD（PM 审批业务理解）
    ↓ 工程师技术设计
design.md（工程师互审）
    ↓ AI 编码
代码 + 测试
    ↓ CI 门禁 + QA 验收 + PM 产品验收
merge
```

### 2.4 QA / Acceptance Owner

**拥有**：
- 独立质量验证权
- 验收自动化
- 回归基线
- 测试证据
- 发布质量建议

**产出**：
- acceptance-manifest.yaml（验收映射清单，每个能力包一份）
- Executable acceptance suite（可执行验收测试套件）
- Regression baseline（回归基线）
- Quality verdict（质量判定：PASS / FAIL / CONDITIONAL）

**审批**：
- staging/prod 质量放行（QA verdict 是 merge 前必要条件之一）

**不承担**：
- ~~功能代码实现~~
- ~~业务需求定义~~
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
- 前端 5 人统一使用 Flutter 技术栈（hl-console-native），web 前端全部计划转 Flutter

### 3.3 QA 团队内部分工

| 角色 | 人数 | 职责 |
|------|------|------|
| QA 架构师 | 1 | acceptance-manifest 标准制定、测试基础设施搭建、验收框架设计、质量度量体系 |
| QA 工程师 | 3 | 验收测试编写与执行、回归测试维护、测试证据收集、质量 verdict 出具 |

---

## 4. 产物矩阵

| 产物 | Owner | 审批人 | 性质 | 存放位置 |
|------|-------|--------|------|---------|
| Cap-Spec-1（能力包规格书） | PM | PM freeze；创始人可选审批 | 业务语义 SSOT | hl-contracts/prd/biz/ |
| Cap-Spec-2（验收场景集） | PM + QA | PM | 验收标准 | hl-contracts/prd/biz/ |
| Cap-Spec-3（业务码提案） | PM | 创始人 | reason_code 变更 | hl-contracts/reasoncodes/ （合入后） |
| HPRD（人类可读产品设计） | 工程师 | PM | Cap-Spec 派生解读 | hl-platform/docs/hprd/{capability}/ |
| design.md（技术设计） | 工程师 | 工程师互审 + AI reviewer | 技术方案 | hl-platform/docs/design/{capability}/ |
| 代码 | 工程师（AI 编码） | CI 门禁 + 工程师互审 | 实现 | hl-platform/app/biz-*/ |
| 单元/集成测试 | 工程师 | CI 门禁 | 实现验证 | hl-platform/app/biz-*/src/test/ |
| acceptance-manifest.yaml | QA | QA | 验收映射 | hl-platform/app/biz-*/acceptance/ |
| 验收测试套件 | QA | QA | 独立质量验证 | hl-platform/app/biz-*/acceptance/ |
| Quality Verdict | QA | — | 发布质量判定 | PR comment / release record |
| Evidence Pack | 工程师 + QA | QA + PM | 合并前验收包 | PR 附件 |
| UI 设计规格 | UI 设计师 | PM | 视觉/交互标准 | 设计工具（不作强制限定） |

---

## 5. 工作流

### 5.1 能力包交付流程（五步）

```
Step 1: Cap-Spec Freeze
  PM 编写 Cap-Spec（规格书 + 验收场景集 + 业务码提案）
  UI 设计师补充视觉/交互设计
  → PM 宣布 Cap-Spec freeze

Step 2: Design + HPRD
  工程师阅读 Cap-Spec，产出：
    ├── HPRD（人类可读产品设计）→ 交 PM 审批业务理解
    └── design.md（技术设计）→ 工程师互审 + AI review
  QA 同步开始编写 acceptance-manifest.yaml
  → PM 审批 HPRD + design.md 工程师互审通过

Step 3: Implementation + Tests
  工程师通过 AI 编码工具实现：
    ├── 功能代码
    ├── 单元测试（governedAction 五条必过 + domain 逻辑）
    ├── 集成测试（Testcontainers）
    └── 可运行 demo
  QA 同步编写验收测试套件
  → 工程师提交 Draft PR

Step 4: 门禁 + 验收（并行）
  ┌── CI 门禁（L1-L3 自动，BLOCKING）
  │     L1: 编译、类型检查、格式
  │     L2: 契约一致性、模块边界、ReasonCode 对齐
  │     L3: 单元测试、集成测试、验收覆盖率（G-026）
  ├── AI 审计（L4，ADVISORY）
  │     NODE-D 异源模型交叉审计
  ├── QA 验收
  │     执行验收测试套件 → 出具 Quality Verdict
  └── 工程师互审（code review）
  → Draft PR 转 Ready for Review（触发 path-based CODEOWNERS review）
  → L1-L3 全绿 + QA PASS + code review approved

Step 5: PM 产品验收 + Merge
  PM 在可交互演示版本上执行产品验收
  → PM PASS
  → Merge（进入 merge queue）
  → 如涉及 founder-owned paths → 创始人额外审批

Post-Merge: 发布
  运维工程师按发布策略执行部署
    ├── staging 环境部署 → QA 回归验证
    └── prod 环境部署 → 运维监控 + 回滚预案
```

---

## 6. Path-Based 门禁模型

### 6.1 hl-contracts CODEOWNERS（现有，保持不变）

```
# hl-contracts/CODEOWNERS — 创始人强制审批全部
*                           @founder
```

### 6.2 hl-platform CODEOWNERS（新建）

```
# hl-platform/CODEOWNERS
# 规则：最后匹配优先
# 原则：founder-owned paths 强制创始人审批；能力包由工程师互审 + QA 验收

# —— 默认：工程师互审 ——
*                                         @hl-engineers

# —— Kernel：创始人强制 ——
/kernel/**                                @founder

# —— Gateway：创始人强制 ——
/gateway/**                               @founder

# —— Framework：创始人强制 ——
/framework/**                             @founder

# —— CI / 构建 / 治理：创始人强制 ——
/.github/**                               @founder
/governance/**                            @founder
/scripts/**                               @founder
build.gradle.kts                          @founder
settings.gradle.kts                       @founder

# —— 能力包验收测试：QA 团队 ——
/app/**/acceptance/**                     @hl-qa-team
/app/**/acceptance-manifest*              @hl-qa-team

# —— 能力包业务代码：工程师互审 ——
/app/biz-*/**                             @hl-engineers

# —— Contract 引用同步：创始人 + 工程师 ——
/contract/**                              @founder @hl-engineers
```

### 6.3 hl-factory CODEOWNERS（新建）

```
# hl-factory/CODEOWNERS — 创始人强制审批
*                                         @founder
```

### 6.4 hl-console-native CODEOWNERS（新建）

```
# hl-console-native/CODEOWNERS
*                                         @hl-frontend-engineers
/.github/**                               @founder
```

### 6.5 GitHub 组织级 Rulesets（建议配置）

| Ruleset | 适用仓库 | 规则 |
|---------|---------|------|
| require-pr | 全部 | 禁止直推 main/develop，必须通过 PR |
| require-status-checks | 全部 | L1-L3 门禁全绿才能 merge |
| require-code-owner-review | 全部 | path-based code owner 必须 approve |
| merge-queue | hl-platform, hl-console-native | 启用 merge queue，避免合并冲突 |
| no-bypass | 全部 | 无人可绕过规则（包括 admin） |
| founder-paths-protection | hl-platform | kernel/ gateway/ framework/ .github/ 路径 → 必须创始人 approve |

---

## 7. 技术适配要求

### 7.1 Java 工程师 → Kotlin AI 编码

当前 6 名后端工程师是 Java 背景，技术栈为 Kotlin 2.1.10。在 AI 驱动模式下：

- 工程师**不需要**手写 Kotlin 代码——AI 生成 100% 代码
- 工程师**需要**能读懂 Kotlin 代码（review AI 产出）
- 工程师**需要**能定义 Kotlin 的类型和接口（意图定义）
- 工程师**需要**理解 Kotlin 特性（sealed class / value class / coroutines）以做验证和裁决

**适配措施**：不做 Java→Kotlin 培训班。通过实际能力包开发，在 AI 编码过程中自然习得。Java 工程师对 JVM 生态的理解（Spring Boot / JPA / Gradle）可以直接复用。

### 7.2 Web 前端 → Flutter 转型

4 名 web 前端 + 1 名 Flutter = 5 人，全部转 Flutter。在 AI 驱动模式下：

- 同 7.1 逻辑——AI 生成 Flutter 代码，工程师负责意图/验证/裁决
- Web 前端工程师需要理解 Flutter widget 体系、Dart 语言特性
- 现有 Flutter 工程师（1 人）作为前端技术 lead，辅助其他 4 人适配

### 7.3 测试团队适配

4 名测试工程师转型为 QA / Acceptance Owner：

- 从"手动测试执行者"转为"验收自动化 owner + 质量判定者"
- 需要掌握：JUnit 5 验收测试编写、acceptance-manifest.yaml 管理、CI 报告解读
- QA 架构师（1 人）额外需要：测试基础设施搭建、验收框架设计

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
| R-TEAM-007 | 前端全线转 Flutter，web 前端 4 人 + Flutter 1 人统一技术栈 | 2026-04-11 | 创始人 |

---

## 9. 退出条件

本文档适用于 Phase 0-1（基座就绪 + 能力包开发启动）。以下条件触发修订：

| 触发条件 | 修订方向 |
|---------|---------|
| 团队规模变化 | 更新能力包分配，调整人员矩阵 |
| T1 能力包全部交付 | 滚动分配 T2 工程师，更新能力包分配表 |
| 唤龙超级工厂成熟 | 开始评估"每人一条产线闭环"的岗位折叠 |
| 微服务拆分（R-055 退出） | 更新 CODEOWNERS 适配多仓库/多服务架构 |
| AI 审计能力成熟到可替代部分人类 owner | 评估哪些审批环节可以由 AI 独立完成 |

---

## 附录 A：与 v1.2 的完整变更追溯

| v1.2 条款 | v2.0 状态 | 说明 |
|-----------|----------|------|
| D-1 三环模型 | SUPERSEDED | 改为四角色模型 |
| D-2 不设业务开发者 | SUPERSEDED | 新增工程师 / Solution Owner，承担 AI 编码 |
| D-3 能力包启动流程 | EVOLVED | 保留 Cap-Spec 先行原则，更新为五步流程 |
| D-4 契约变更流程 | PRESERVED | 保持不变 |
| D-5 核心组 7 人 | SUPERSEDED | 改为全组织 21 人 |
| R-056 不设业务开发者岗位 | SUPERSEDED | 设工程师岗位 |
| R-057 创始人 + AI 全覆盖 | EVOLVED | 创始人覆盖 kernel/gate；工程师覆盖能力包 |
| R-058 核心组 7 人 | SUPERSEDED | 21 人全组织 |

---

*本文档为 DRAFT，待创始人审计裁决后转为 LOCKED。*
