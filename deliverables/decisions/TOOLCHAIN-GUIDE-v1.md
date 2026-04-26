# 唤龙平台工具链指南

## TOOLCHAIN-GUIDE v1 — 工具链选型与流程映射

---

**文档编号**：TOOLCHAIN-GUIDE-001
**版本**：v1.0
**日期**：2026-04-11
**状态**：DRAFT（待创始人审批）
**文档性质**：TEAM-COLLABORATION-SPEC v2.1 附属文件（R-TEAM-006）
**派生链**：SAAC-HL-001 §A3 → BRIDGE-DERIVATION v1 → DD-TEST v1.2 → TEAM-COLLAB-SPEC v2.1 R-TEAM-006 → 本文档

---

## 1. 定位声明

### 1.1 本文档做什么

将治理文件（DD-TEST v1.2、verification-gates、TEAM-COLLAB-SPEC v2.1）中的抽象要求映射到具体工具和实践，为团队提供可操作的工具链参考。

### 1.2 本文档不做什么

**不锁死具体产品**。本文档列出的工具是当前推荐方案（Recommended），不是治理强制（Mandated）。团队可以在满足治理约束的前提下选择替代工具。

> **SAAC A3 原则**：工具是桥梁层组件，先问"需要吗"再选型；不预置不需要的工具。
>
> **PRD-REDEFINITION-SPEC v2.0**：规格驱动工具不作强制限定；AI 平台不作强制规定。

### 1.3 约束力层级

| 层级 | 来源 | 约束力 | 示例 |
|------|------|--------|------|
| **治理锁定** | TECH-STACK-SPEC v3 / DD-TEST v1.2 | 变更需创始人审批 | JUnit 5.10.2、Kotlin 2.1.10 |
| **治理要求** | verification-gates / TEAM-COLLAB-SPEC v2.1 | 必须满足（工具可换） | qa-verdict required status check |
| **推荐方案** | 本文档 | 默认使用，可替换 | SonarQube Community |
| **团队自选** | 无 | 无约束 | IDE、AI 平台、设计工具 |

---

## 2. 三舱映射：规格 / 执行 / 审计

将唤龙交付流分为三个舱位（Spec → Execution → Audit），每个舱位对应不同的工具职责。

```
┌─────────────────────────────────────────────────────────┐
│                    Spec 舱（规格定义）                    │
│  Cap-Spec (hl-contracts/prd/biz/**)                     │
│  acceptance-manifest.yaml                                │
│  HPRD (hl-platform/docs/hprd/**)                        │
│  design.md (hl-platform/docs/design/**)                  │
│                                                          │
│  工具：Markdown 编辑器（团队自选）                         │
│        AI 辅助编写（平台自选）                              │
│        飞书文档（上游讨论，非 SSOT）                        │
├─────────────────────────────────────────────────────────┤
│                  Execution 舱（代码实现）                  │
│  hl-platform 源代码                                      │
│  hl-console-native SwiftUI 治理控制台                     │
│  hl-scene-app Flutter 场景前端                            │
│                                                          │
│  工具：见 §3 开发工具栈                                    │
├─────────────────────────────────────────────────────────┤
│                    Audit 舱（验证审计）                    │
│  CI 门禁 L1-L4                                           │
│  qa-verdict / pm-acceptance status checks                │
│  L4 双模型交叉审计                                        │
│                                                          │
│  工具：见 §4 测试工具栈、§5 CI/Gate 工具                   │
└─────────────────────────────────────────────────────────┘
```

**舱位隔离原则**：Execution 舱的工程师不拥有 Audit 舱的放行权（四权分离）。

---

## 3. 开发工具栈

### 3.1 治理锁定（变更需创始人审批）

| 工具 | 版本 | 锁定来源 | 用途 |
|------|------|---------|------|
| Kotlin | 2.1.10 | TECH-STACK-SPEC v3 | 主开发语言 |
| Spring Boot | 3.5.11 | TECH-STACK-SPEC v3 | 应用框架 |
| Spring Modulith | 1.3.4 | TECH-STACK-SPEC v3 | 模块边界验证 |
| PostgreSQL | 18.x | TECH-STACK-SPEC v3 | 数据库 |
| Gradle | 8.12 | TECH-STACK-SPEC v3 | 构建工具 |
| SwiftUI / GHKit | (见 hl-console-native) | R-016 / R-052 | 治理/运营/审计客户端 |
| Flutter / Dart | Flutter 3.41 / Dart 3.x | R-FE-CLIENT-001 / DD-FE-CLIENT-v1 | 场景前端 App（hl-scene-app） |

### 3.2 团队自选（无约束）

| 类别 | 说明 |
|------|------|
| IDE | IntelliJ IDEA / VS Code / 其他，团队成员自选 |
| AI 编码平台 | Claude / GPT / Codex / Kiro / 其他，不作强制规定 |
| AI 辅助工具 | Cursor / Copilot / 其他，不作强制规定 |
| UI 设计工具 | Figma / Sketch / 其他，不作强制限定（TEAM-COLLAB-SPEC v2.1 §4.2） |
| API 调试 | Postman / Insomnia / httpie / 其他 |

> **AI-first 原则**（DD-TEST v1.2 B2）：默认由 AI 生成代码，工程师可在必要时手动补充。所有 diff 统一经过 CI 门禁，不区分人写还是 AI 写。AI 平台选择不影响门禁标准。

---

## 4. 测试工具栈

所有测试工具选型均由 DD-TEST v1.2 从 SAAC 公理推导得出。以下是推导结论的操作指南。

### 4.1 主测试框架

| 工具 | 版本 | 约束层级 | 用途 | 推导来源 |
|------|------|---------|------|---------|
| JUnit 5 | 5.10.2 | **治理锁定** | 唯一主测试框架 + 推荐运行器 | DD-TEST-1 / P0-6 + B2 |
| junit-jupiter-params | (同 JUnit 5) | **治理锁定** | 参数化测试 / 验收测试 | DD-TEST-4 |

**为什么是 JUnit 5**：AI 训练数据中 JUnit 5 样本最多，AI 生成准确率最高。在 AI-first 编码环境下，选 AI 不熟悉的框架 = 每天和 AI 生成的错误测试做斗争（DD-TEST v1.2 §1 选型理由）。

### 4.2 属性测试

| 工具 | 版本 | 约束层级 | 用途 | 推导来源 |
|------|------|---------|------|---------|
| Kotest Property | 5.9.1 | **治理锁定** | 属性测试 / 边界覆盖 | DD-TEST-1 |

**使用规范**：
- 在 JUnit 5 runner 中执行（在 `@Test` 方法内调用 `checkAll`/`forAll`）
- **不得**新增 `FunSpec`/`StringSpec` 等 Kotest Spec 风格测试
- 现有 `EdgePropertyTest` 的 `FunSpec` 用法需迁移到 JUnit 5 风格

### 4.3 集成测试

| 工具 | 版本 | 约束层级 | 用途 | 推导来源 |
|------|------|---------|------|---------|
| Testcontainers | 1.20.4 | **治理锁定** | 真实 PostgreSQL Docker 容器 | DD-TEST-3 |

**规范**：集成测试使用真实 PostgreSQL Docker 容器，**不使用 H2 模拟**。使用 Spring Boot `@ServiceConnection` 自动配置。

### 4.4 验收测试

| 方式 | 适用 AcceptanceMode | 工具 | 进入 PR 门禁？ |
|------|-------------------|------|--------------|
| JUnit 5 参数化测试 | API_EXEC | JUnit 5 + junit-jupiter-params | 是（G-023） |
| 审计脚本 | AUDIT_EXEC | 确定性脚本 / Gradle task | 是（G-023） |
| UI 自动化 | UI_AUTO | 待定（Phase 1 评估） | 是（G-023） |
| 人工验收 | UI_MANUAL | PM 里程碑验收 | 否 |

**为什么不用 Cucumber**：AI 生成 JUnit 5 `@ParameterizedTest` 质量远高于 Cucumber step definition（DD-TEST-4）。

### 4.5 Phase 1+ 工具（当前不引入）

| 工具 | 引入时机 | 用途 | 推导来源 |
|------|---------|------|---------|
| PIT (pitest) | 能力包测试用例达 50+ 时 | 变异测试 | DD-TEST-5 |
| SonarQube Community | Phase 1 | 圈复杂度/重复/安全扫描 | DD-TEST-6 |

**PIT 范围限定**：首批试点 = 能力包 domain/ 层。kernel/ 暂不纳入（Kotlin sealed class 变异算子不完善），非永久豁免。

**SonarQube 输出范围限定**：仅输出圈复杂度、重复代码率、安全扫描。模块边界清晰度的权威数据源是 Gradle 物理边界 + source-checks 脚本 + Spring Modulith `ApplicationModules.verify()`，**不是** SonarQube。

---

## 5. CI/Gate 工具

### 5.1 门禁执行平台

| 组件 | 推荐方案 | 约束层级 |
|------|---------|---------|
| CI 平台 | GitHub Actions | **推荐**（可替换为其他 CI） |
| 门禁脚本位置 | hl-factory/gates/ | **治理要求**（路径在 CODEOWNERS 中锁定） |
| 门禁规格 | hl-factory/specs/verification-gates.md | **治理锁定** |

### 5.2 四层门禁工具映射

#### L1 — 确定性门禁（BLOCKING）

| Gate ID | 检查项 | 工具/命令 |
|---------|--------|----------|
| G-001 | Java/Kotlin 编译 | `./gradlew compileJava compileKotlin` |
| G-002 | 测试编译 | `./gradlew compileTestJava compileTestKotlin` |
| G-003 | 代码格式 | `./gradlew spotlessCheck` |
| G-004 | 静态分析 | `./gradlew checkstyleMain`（如已配置） |

#### L2 — 规则性门禁（BLOCKING）

| Gate ID | 检查项 | 工具/命令 |
|---------|--------|----------|
| G-010 | deny 三参数调用检查 | `gate-deny-check.sh` |
| G-011 | 循环依赖 | `gate-circular-dep.sh` |
| G-012 | API 路径规范 | 正则/AST 检查 |
| G-013 | ReasonCode 对齐 | 对比代码常量 vs `reasoncodes.csv` |
| G-014 | @JsonProperty 覆盖 | DTO 字段检查脚本 |
| G-015 | HK 模块边界 | `package-info.java` + Modulith verify |
| G-016 | Spec 漂移检测 | `gate-spec-drift.sh` |
| G-026 | acceptance-manifest 覆盖率 | YAML 解析脚本（声明性，不解析源码） |

> G-026 在 DD-TEST v1.2 中定义为 L2（确定性 YAML 解析），不是 L3。

#### L3 — 行为性门禁（BLOCKING）

| Gate ID | 检查项 | 工具/命令 |
|---------|--------|----------|
| G-020 | 单元测试 | `./gradlew test` |
| G-021 | 集成测试 | `./gradlew integrationTest` (Testcontainers) |
| G-022 | DoD 静态验证 | `verify.sh run_XXXX` |
| G-023 | 验收场景回放 | JUnit 5 参数化测试（AcceptanceMode ≠ UI_MANUAL） |
| G-024 | 回归集 | `evals/` 历史回归测试 |

#### L4 — 语义性审计（ADVISORY）

| Gate ID | 检查项 | 工具 |
|---------|--------|------|
| A-001 | 交叉审计 | 双模型（GPT 初审 + Claude 仲裁） |
| A-002 | 意图一致性 | 模型对比 Spec vs 代码 |
| A-003 | 代码可读性 | 模型评估 |
| A-004 | 安全审计 | 模型扫描（P0 安全问题升级为 BLOCK） |

### 5.3 Required Status Checks 实现

TEAM-COLLAB-SPEC v2.1 要求 `pm-hprd-pass`、`qa-verdict` 和 `pm-acceptance` 作为 GitHub required status checks（R-TEAM-009 + R-TEAM-012）。以下是推荐实现方案：

**pm-hprd-pass**（PM 确认 HPRD 理解正确 — Draft PR 前置 gate）：

```yaml
# .github/workflows/pm-hprd-pass.yml（示意，非最终版）
name: pm-hprd-pass
on:
  pull_request_review:
    types: [submitted]
jobs:
  check:
    if: >
      github.event.review.state == 'approved' &&
      contains(fromJSON('["pm-team-member-list"]'), github.event.review.user.login)
    runs-on: ubuntu-latest
    steps:
      - run: echo "PM HPRD pass"
```

> **时序要求**（R-TEAM-012）：pm-hprd-pass 必须在 Step 2 完成，工程师不得在此 check 通过前开始 Step 3 实现。

**qa-verdict**（QA 验收判定）：

```yaml
# .github/workflows/qa-verdict.yml（示意，非最终版）
name: qa-verdict
on:
  pull_request_review:
    types: [submitted]
jobs:
  check:
    if: >
      github.event.review.state == 'approved' &&
      contains(fromJSON('["qa-team-member-list"]'), github.event.review.user.login)
    runs-on: ubuntu-latest
    steps:
      - run: echo "QA verdict PASS"
```

**pm-acceptance**（PM 产品验收）：

```yaml
# .github/workflows/pm-acceptance.yml（示意，非最终版）
name: pm-acceptance
on:
  pull_request_review:
    types: [submitted]
jobs:
  check:
    if: >
      github.event.review.state == 'approved' &&
      contains(fromJSON('["pm-team-member-list"]'), github.event.review.user.login)
    runs-on: ubuntu-latest
    steps:
      - run: echo "PM acceptance PASS"
```

**替代实现方式**（均满足治理要求）：
- PR label 触发（`qa-pass` / `pm-accepted` label → status check）
- 外部系统回调（飞书审批 → GitHub commit status API）
- GitHub App bot（自动解析 review comment 中的结构化判定）

治理只锁"必须有这两个 required status check 且为 PASS"，不锁实现方式。

---

## 6. 团队工具自由度矩阵

| 工具类别 | 自由度 | 说明 |
|---------|--------|------|
| 编程语言 / 框架 / 数据库 | 🔒 锁定 | TECH-STACK-SPEC v3 管辖，变更需创始人审批 |
| 测试框架（JUnit 5 / Kotest Property / Testcontainers） | 🔒 锁定 | DD-TEST v1.2 推导，变更需创始人审批 |
| 门禁规格（L1-L4 检查项） | 🔒 锁定 | verification-gates 管辖 |
| CI 平台 | 🟡 推荐 | GitHub Actions 推荐，可在满足门禁要求前提下替换 |
| Status Check 实现方式 | 🟡 推荐 | 本文档 §5.3 推荐方案，可选替代实现 |
| Phase 1 工具（PIT / SonarQube） | 🟡 推荐 | DD-TEST 推导，可在满足同等指标前提下替换 |
| IDE | 🟢 自选 | 团队成员自行决定 |
| AI 编码/辅助平台 | 🟢 自选 | 不作强制规定 |
| UI 设计工具 | 🟢 自选 | 不作强制限定 |
| API 调试工具 | 🟢 自选 | 不作限定 |
| 沟通协作平台 | 🟢 自选 | 飞书为主（已有），不作排他限定 |

---

## 7. 退出条件与迭代

### 7.1 工具替换评审标准

当团队提议替换本文档中的推荐工具时，需满足：

1. **同等治理约束**：替代工具必须满足治理文件中的同等要求（如 required status check 必须存在且可靠）
2. **SAAC A3 合规**：不引入不必要的额外工具
3. **AI-first 兼容**：AI 对替代工具的生成质量不低于当前工具（DD-TEST v1.2 B2 标准）
4. **T1 试点验证**：替代工具需在至少一个 T1 能力包中完成端到端试点

### 7.2 版本演进

| 触发条件 | 动作 |
|---------|------|
| DD-TEST 版本更新 | 同步更新 §4 测试工具栈 |
| verification-gates 新增/变更 Gate | 同步更新 §5.2 门禁映射 |
| T1 试点发现工具不适配 | 评估替换方案，更新推荐 |
| Phase 1 工具引入 | 从 §4.5 移入对应的正式章节 |

---

## 变更日志

| 日期 | 版本 | 变更内容 |
|------|------|---------|
| 2026-04-11 | v1.0 | 初始版本——从 DD-TEST v1.2 + verification-gates + TEAM-COLLAB-SPEC v2.1 汇总的工具链操作指南。覆盖三舱映射、开发工具栈、测试工具栈、CI/Gate 工具映射、required status checks 实现方案、团队工具自由度矩阵。 |
