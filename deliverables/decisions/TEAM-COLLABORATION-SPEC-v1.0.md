# 唤龙平台团队协作规格

## TEAM-COLLABORATION-SPEC v1.0 — 全新构建协作模型

---

**文档编号**：TEAM-COLLAB-SPEC-001
**版本**：v1.1
**日期**：2026-03-17
**状态**：LOCKED（D-1~D-5 全部裁决完毕，R-056~R-060）
**派生链**：SAAC-HL-001 v1.1 §1.3 → R-044 → R-045 → R-053 → 本文档
**替代文档**：`_workspace-legacy/outputs/ROLE-RESPONSIBILITIES-PHASE1.md`（SUPERSEDED，旧系统改造前提不再成立）

---

## 0. 推导声明

本文档从 SAAC-HL-001 v1.1 第一性原理重新推导，不沿用旧工程 WS-A/B/C/D/E 分工体系。

**推导输入**：

| 编号 | 输入 | 关键约束 |
|------|------|---------|
| I-1 | SAAC-HL §1.3 | AI 驱动基本运行前提：创始人主导小团队，AI 生成 100% 代码，人类负责意图/验证/裁决 |
| I-2 | R-044 LOCKED | AI 驱动型任务（CI/Skill/Prompt）由创始人主导编写，团队 review + 运维兜底 |
| I-3 | R-045 LOCKED | 全新构建，无旧系统适配。「适配」「改造」「Canal 对账」等概念全部消失 |
| I-4 | R-053 LOCKED | Phase 0→1 执行计划：5 Sprint / 核心组 6 人 / 能力包从零构建 |
| I-5 | HL-P3 | 契约法典是脊柱——跨域变更必须契约先行 |
| I-6 | HL-P8 | 治理正确性显式可验证——CI 门禁 > 人工巡检 |
| I-7 | R-055 LOCKED | Phase 0-2 单 JVM Modulith，HK 不独立部署 |
| I-8 | TECH-STACK-SPEC v3 | Kotlin 2.1.10 / 5 Starters + BOM / 8 CI Gates / Phase 0 不预置 MQ/Cache/Nacos/Keycloak |

**推导逻辑**：

```
I-1（AI 驱动）+ I-3（全新构建）
  → 没有「适配层」→ 没有 WS-C「适配团队」→ 旧 Workstream 分类全部失效
  → 团队角色从「工作流分类」改为「能力域分类」

I-1（小团队 + AI 100% 代码）+ I-2（AI 任务创始人主导）
  → 代码产出的主力是「创始人 + AI」，而非传统开发团队
  → 其他成员的核心价值 = 验证 + 守护 + 运维 + 业务定义
  → 角色设计应围绕「守护什么」而非「写什么代码」

I-5（契约先行）+ I-6（CI 自动化）
  → 协作流的核心节点是「契约评审 → 门禁通过 → 验收签字」
  → 减少人工流转环节，增加自动化校验环节
```

---

## 1. 组织模型

### 1.1 基本架构

```
                    ┌─────────────┐
                    │  创始人裁决层  │  意图定义 / 架构裁决 / 最终签字
                    │   童正辉      │  + AI 协同（Cowork / Claude Code）
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼────┐ ┌────▼─────┐
        │ 守护者环    │ │ 业务环  │ │ 基础设施环 │
        │ Guardians  │ │ Domain │ │  Infra   │
        └─────┬─────┘ └───┬────┘ └────┬─────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │   CI 自动化层  │  8 门禁 + 契约校验 + 编译测试
                    └─────────────┘
```

**三环模型**取代旧 WS-A~E。每环围绕「守护什么」定义，而非「写什么代码」：

| 环 | 守护对象 | 核心价值 |
|----|---------|---------|
| **守护者环 Guardians** | 架构合规性 + 发布安全性 | 确保 AI + 创始人产出符合 SAAC 治理规范 |
| **业务环 Domain** | 用户价值 + 业务语义 | 定义能力包边界、需求、验收标准 |
| **基础设施环 Infra** | 运行稳定性 + 数据安全 | 保障 PG / 部署 / 监控 / 环境可靠 |

### 1.2 角色定义

#### 创始人裁决层

| 角色 | 人员 | 职责 |
|------|------|------|
| **创始人 / 架构师** | 童正辉 | 产品决策、架构裁决、HK Kernel + Gateway 开发（AI 协同）、里程碑签字、RULINGS.md 写入 |

**AI 驱动说明**（I-1 + I-2）：创始人通过 Cowork / Claude Code 完成 100% 代码编写（包括 HK Kernel、CI 门禁、能力包骨架）。这不是「创始人一个人写所有代码」，而是「创始人 + AI 组成的生产单元承担代码产出主力」。团队的价值不在于分担代码量，而在于守护代码质量和业务正确性。

#### 守护者环 Guardians

| 角色 | 人员 | 守护对象 | 核心职责 |
|------|------|---------|---------|
| **Gate H 守护者** | 许久明 | 架构合规 + 代码健康 | 所有 PR 的 Gate H 签字（含创始人代码）；hl-framework 5 Starters + BOM 维护；契约变更评审；术语 SSOT 守护 |
| **Gate R 守护者** | 曾正龙 | 发布安全 + 运行稳定 | 所有发布的 Gate R 签字；PG18 运维；Docker Compose 开发环境；Flyway 流水线；Grafana 监控面板；上线 SOP |

**守护者不写业务代码，但对所有代码有否决权。** 这是 SAAC-HL §1.3 的直接推论：AI 生产 100% 代码→人类的价值在于验证和否决，而非分担产量。

#### 业务环 Domain

| 角色 | 人员 | 守护对象 | 核心职责 |
|------|------|---------|---------|
| **PM（产品经理）** | 邹骢 | 用户价值 + 业务语义 | 能力包 MVP 规格、Facts 定义、reason_codes 初稿、验收用例、UAT 签收 |
| **业务开发者** | S0 招聘 2 人（R-056），S1 onboard | 能力包实现 | 基于 DEVPACK 模板开发能力包；domain 层 + adapter 层 Kotlin 实现；五必过测试编写 |

**业务开发者定位说明**：在 AI 驱动模型下，业务开发者的主要工作模式是：

1. 从创始人 + AI 产出的骨架代码开始
2. 按 DEVPACK 模板补充业务逻辑
3. 编写五必过测试（P0-5）
4. 确保 8 道 CI 门禁全部通过
5. 提交 PR → Gate H 审查

这与传统「从零设计并实现」不同——骨架（contract 层接口 + domain 层模式 + adapter 层配置）由创始人 + AI 生成，业务开发者聚焦于业务逻辑填充和测试覆盖。

#### 基础设施环 Infra

| 角色 | 人员 | 守护对象 | 核心职责 |
|------|------|---------|---------|
| **后端基础设施** | 魏鹏 | SDK + 安全 + 性能 | starter-security JWT 实现（DD-AUTH）；starter-observability；HK Client SDK 维护；性能基线测试 |

**魏鹏 Phase 0 职责重新推导**（I-3 + I-8）：

旧职责（Nacos 集成 / Keycloak 集成 / starter-mq / starter-cache）全部因 R-027 SUPERSEDED + DD-AUTH + DD-CACHE + R-054 Q1 而消失。从 TECH-STACK-SPEC v3 锁定的 Phase 0 技术栈重新推导：

| Phase 0 交付物 | 推导来源 | Sprint |
|---------------|---------|--------|
| starter-security（Spring Security 内建 JWT） | DD-AUTH：Phase 0 无 Keycloak，JWT 签发验签需要 Starter 封装 | S1 |
| starter-observability（Actuator + Logback + Micrometer + OTel Agent 配置） | TECH-STACK-SPEC v3 §9：5 Starters 之一 | S1 |
| HK Client SDK（Kotlin 版，消费 HK 治理能力的开发者友好封装） | R-053 S2 交付物 | S2 |
| 性能基线测试框架 | R-053 M4 验收标准（P99 < 200ms） | S3-S4 |
| Phase 1+ Keycloak 预研 | DD-AUTH 退出条件：联邦登录需求出现时引入 | S4（预研，非交付） |

#### 技术验收官（纳入核心组，R-059）

| 角色 | 人员 | 守护对象 | 核心职责 |
|------|------|---------|---------|
| **技术验收官** | 李旭阳 | 端到端业务正确性 | Gate 3（业务合规）签字；能力包集成测试执行；端到端链路验证；回归测试维护 |

**李旭阳定位说明**（R-059）：从「职能支持」升级为正式技术验收官，纳入 R-053 核心组（6→8 人，含 R-056 扩编 2 名业务开发者 + R-059 李旭阳）。在 D-3 不设独立 QA 的裁决下，李旭阳承担集成测试和端到端验证的全部责任，是 Gate 3 的唯一签字人。

#### 旧工程协调（不纳入核心组）

| 角色 | 人员 | 职责 |
|------|------|------|
| **旧工程交付** | 刘建成 | 旧工程（非唤龙平台）的交付管理；旧工程与唤龙平台数据态打通的协调对接（详设后续定义） |

**刘建成定位说明**（R-059）：不纳入唤龙核心组。旧工程不接入唤龙平台，仅做数据态打通。刘建成继续负责旧工程交付，并在数据打通环节与唤龙团队对接。唤龙平台的 Sprint 看板和 Issue 流转由核心组成员自管理（GitHub Project Board）。

---

## 2. 协作流程

### 2.1 能力包启动流（对齐 PM-BRANCH-LAUNCH-TEMPLATE）

```
Phase                 负责人        产出物                          门禁
─────────────────────────────────────────────────────────────────────
① 裁决立项            创始人        RULINGS.md 能力包确认            创始人签字
                                   （biz.{module} ID + 优先级）
                      │
② 契约注册            PM + 创始人   reason_codes.csv PR             Gate H
                                   OpenAPI YAML
                                   capabilities.yaml
                                   PRD 文档集
                      │
③ 骨架生成            创始人 + AI   contract/ 层接口                 CI 8 门禁
                                   kernel/biz-{module}/ 骨架
                                   DDL + RLS
                      │
④ 业务填充            业务开发者    domain 层逻辑 + adapter 层        CI 8 门禁
                                   五必过测试（P0-5）
                      │
⑤ 集成验证            技术验证      端到端链路测试                    Gate 3
                      Gate H       代码健康 + 架构合规               Gate H 签字
                      Gate R       可构建 + 可观测 + 可回滚           Gate R 签字
                      │
⑥ UAT 验收            PM           全部验收用例人工验证               PM 签字
                      创始人        里程碑签收                       创始人签字
```

### 2.2 契约变更流（跨仓库协同协议）

**核心原则**：hl-contracts 变更必须先于 hl-platform 变更（HL-P3 契约先行）。

**三步提交协议**：

| 步骤 | 仓库 | 内容 | 先决条件 |
|------|------|------|---------|
| Step 1 | hl-contracts | reason_codes.csv + OpenAPI YAML + capabilities.yaml + PRD 文档 | PM 初稿 + 创始人审批 |
| Step 2 | hl-platform | contract/ 层 Kotlin 接口（Pure Kotlin，零依赖） | Step 1 PR 已 merge |
| Step 3 | hl-platform | kernel/biz-{module}/ 实现 + 测试 + DDL | Step 2 PR 已 merge |

**版本锁定机制**：

- hl-contracts PR 合并后，contract/ 层接口必须引用该版本的 reason_code constants
- 如果 hl-contracts PR 被打回修改，已基于旧版本的 hl-platform 代码必须暂停，等待新版本
- 禁止 hl-platform 代码引用尚未 merge 的 hl-contracts 定义

**Reviewer 指派规则**：

| 仓库 | Reviewer | 审查重点 |
|------|----------|---------|
| hl-contracts | 创始人 + Gate H（许久明） | 契约完整性、reason_code 命名、OpenAPI 格式 |
| hl-platform contract/ | Gate H（许久明） | Pure Kotlin 合规、命名规范（HK-NAMING-SPEC） |
| hl-platform kernel/ | Gate H（许久明） | P0-0~P0-6 合规、五必过测试、CI 全绿 |

### 2.3 日常协作模式（沿用 hl-dispatch 三模式）

| 模式 | 触发场景 | GitHub 载体 | 标签 |
|------|---------|------------|------|
| A 文档审查 | 规格评审、审计报告 | Issue（doc-review 模板） | `doc-review` + 角色标签 |
| B 任务派发 | OPS 清单、环境搭建、配置确认 | Issue（task-assign 模板） | `task-assign` + 角色标签 |
| C 代码/契约变更 | PR 评审 | Pull Request | 仓库对应 reviewer |

### 2.4 Sprint 节奏

沿用 R-053 Sprint 结构（5 个 Sprint），但重新定义各角色在每个 Sprint 的交付物：

**S0 就绪检查（~1 周）**

| 角色 | 交付物 |
|------|--------|
| 创始人 | 就绪报告全部 ✅ + 签字 |
| Gate H（许久明） | hl-framework 5 Starters + BOM 初始发布验证；术语 SSOT 建立 |
| Gate R（曾正龙） | PG18 开发实例 + Docker Compose 开发环境 |
| Infra（魏鹏） | starter-security JWT 方案设计（DD-AUTH 对齐） |
| 技术验收官（李旭阳） | Gate 3 流程文档化 + 验收检查项模板建立 |

**S1 地基（~2-3 周）**

| 角色 | 交付物 |
|------|--------|
| 创始人 + AI | HK Kernel Flyway V1 + Gateway ProtocolGate + CI 8 门禁脚本 |
| Gate H（许久明） | starter-boot + starter-web + starter-data-jpa 交付；Gate H 审查创始人代码 |
| Gate R（曾正龙） | PG18 生产级部署 + Flyway 流水线 + OTel Agent 配置 |
| Infra（魏鹏） | starter-security（JWT）+ starter-observability 交付 |

**S2 治理层投产（~2-3 周）**

| 角色 | 交付物 |
|------|--------|
| 创始人 + AI | HK 6 模块 PG 集成 + 审计链路端到端 + Gateway 投产 |
| Gate H（许久明） | Gate H 验收治理层全量代码；hl-framework BOM 版本锁定 |
| Gate R（曾正龙） | Grafana 监控面板 + Outbox 事件表监控 + 上线 SOP |
| Infra（魏鹏） | HK Client SDK 首版发布 |
| PM（邹骢） | S2 中期启动能力包清单讨论；首批 3-5 包推荐（用户价值链推导） |
| 技术验收官（李旭阳） | Gate 3 验收标准对齐能力包清单；验收环境就绪确认 |

**S3 开发框架验证（~2-3 周）**

| 角色 | 交付物 |
|------|--------|
| 创始人 + AI | 1 个 demo biz.* 骨架生成（contract + kernel + DDL） |
| 业务开发者 | demo 包业务逻辑填充 + 五必过测试 |
| PM（邹骢） | demo 包 MVP 规格 + Facts + 验收用例 |
| Gate H（许久明） | Gate H 验收 demo 包 |
| Gate R（曾正龙） | demo 包部署验证 + 性能基线初测 |
| 技术验收官（李旭阳） | demo 包端到端链路验证 + Gate 3 签字 |

**S4 首批能力包（~4-6 周）**

**人力模型（R-057）**：1 人 1 包，按序滚动。2 名业务开发者同时各负责 1 个能力包，完成后滚动接下一包。最多 2 包并行，质量优先于速度。创始人 + AI 批量生成 3-5 包骨架，业务开发者按优先级依次填充。

| 角色 | 交付物 |
|------|--------|
| 创始人 + AI | 3-5 个核心 biz.* 骨架生成（contract + kernel + DDL） |
| 业务开发者（2 人） | 1 人 1 包滚动填充 + 五必过测试；最多 2 包并行 |
| PM（邹骢） | 每个能力包的 LAUNCH-{MODULE}.md + PRD 文档集 |
| Gate H（许久明） | 逐包 Gate H 验收 |
| Gate R（曾正龙） | 逐包发布验证 + 性能基线（P99 < 200ms） |
| Infra（魏鹏） | 性能基线测试执行 + Phase 1+ Keycloak 预研 |
| 技术验收官（李旭阳） | 全部能力包端到端验证 + Gate 3 签字 |

### 2.5 前端交付规划（R-060）

**裁决**：Swift（hl-console-native 运营后台）与 Flutter（消费者端）并行推进。

| 端 | 技术栈 | 仓库 | Phase 0 目标 | 负责人 |
|----|--------|------|-------------|--------|
| 运营后台 | Swift（macOS / iOS） | hl-console-native | 与后端 API 联调，核心管理界面可用 | 待定（R-052 已锁定 Apple 原生） |
| 消费者端 | Flutter（跨平台） | 待建 | MVP 核心流程可用 | 待定 |

**前端与后端协作接口**：前端消费 hl-contracts 中 OpenAPI YAML 生成的类型定义，遵循契约先行（HL-P3）。前端 PR 不经过后端 8 道 CI 门禁，但需通过 Gate H 的 API 契约一致性审查。

**人力说明**：前端开发者尚未纳入 R-053 核心组，需在 S1 期间确定人选和 onboard 计划。

---

## 3. 门禁体系

### 3.1 自动化门禁（CI 层，R-044 创始人主导编写）

| # | 脚本 | 检查内容 | 约束来源 | 阻断级别 |
|---|------|---------|---------|---------|
| 1 | `check-domain-isolation.sh` | domain/ 零 Spring import | P0-1 | CI 阻断 |
| 2 | `check-no-implicit-spring.sh` | 无隐式 Spring 注解 | P0-0 | CI 阻断 |
| 3 | `check-jpa-isolation.sh` | domain/ 零 JPA import | DD-ORM | CI 阻断 |
| 4 | `check-reason-codes.sh` | reason_code 零硬编码 | P0-4 | CI 阻断 |
| 5 | `gate-circular-dep.sh` | 无循环依赖 | P0-2 | CI 阻断 |
| 6 | `gate-deny-check.sh` | deny 路径审计覆盖 | P0-5 | CI 阻断 |
| 7 | `gate-spring-isolation.sh` | Spring 隔离综合检查 | P0-0 | CI 阻断 |
| 8 | `validate-contracts.sh` | 契约一致性 | P0-3 | CI 阻断 |

**R-044 适用说明**：这 8 道门禁由创始人 + AI 编写和维护。团队成员（主要是许久明）做逻辑正确性 review + 运维部署。Gate H 对 CI 脚本的审查级别为「逻辑正确性 review」而非「架构深审」——因为 R-044 的前提是团队尚未完成 AI-native 转型，CI 脚本的设计意图由创始人把握。

### 3.2 人工门禁

| 门禁 | 签字人 | 审查内容 | 触发时机 |
|------|--------|---------|---------|
| **Gate H** | 许久明 | 代码质量 + 架构合规 + 测试覆盖 + 命名规范（HK-NAMING-SPEC） | 每个 PR merge 前 |
| **Gate R** | 曾正龙 | 可构建 + 可观测 + 可回滚 + Staging 健康 | 里程碑发布前 |
| **Gate 3** | 李旭阳（技术验收官） | 端到端业务合规 + 异常安全 + 回归测试 | 能力包集成验证 |
| **创始人签字** | 童正辉 | 裁决确认 + 里程碑签收 + 灰度决策 | M0-M4 里程碑 |
| **PM 签字** | 邹骢 | UAT 验收用例全部通过 | 能力包 UAT 阶段 |

### 3.3 测试分工（R-058：不设独立 QA）

**裁决**：唤龙平台不设独立 QA 角色。测试责任按层级分配：

| 测试层级 | 负责人 | 工具/框架 | 触发时机 |
|---------|--------|---------|---------|
| 单元测试（P0-5 五必过） | 业务开发者 | JUnit 5 + Kotlin | 每次 PR 提交，CI 自动执行 |
| 契约一致性测试 | CI 自动化（validate-contracts.sh） | Shell + JSON Schema | 每次 PR 提交 |
| 集成测试 | 技术验收官（李旭阳） | TestContainers + PG18 | 能力包 ④→⑤ 阶段 |
| 端到端链路验证 | 技术验收官（李旭阳） | Gate 3 检查项 | 能力包 ⑤ 集成验证阶段 |
| 回归测试 | 技术验收官（李旭阳） | 累积测试套件 | 里程碑发布前 |
| UAT 验收 | PM（邹骢） | 人工验收用例 | 能力包 ⑥ UAT 阶段 |

**推导逻辑**：AI 驱动模型下（I-1），代码量由创始人 + AI 产出，测试的核心价值在于「验证 AI 产出是否符合业务意图」——这恰好是技术验收官和 PM 的守护对象，无需额外 QA 层。P0-5 五必过确保基础质量由开发者自保证。

---

## 4. 编码规范（Kotlin 版，替代旧 Java 规范）

### 4.1 语言与风格

| 条目 | 规范 | 推导来源 |
|------|------|---------|
| 实现语言 | **Kotlin 2.1.10** / JVM 21 LTS | D1 裁决 + TECH-STACK-SPEC v3 §2 |
| 序列化 | `@JsonNaming(SnakeCaseStrategy::class)` on data class，或 kotlinx.serialization | 替代旧 `@JsonProperty` 逐字段标注 |
| 模块声明 | Modulith `@ApplicationModule` 注解（Kotlin 文件），无 `package-info.java` | D1 → Kotlin 无 package-info.java |
| 空安全 | 充分利用 Kotlin non-null 类型；禁止 `!!` 操作符（代码审查强制） | Kotlin 惯例 |
| sealed class | 用于 Result / Event / Error 类型建模 | HK-NAMING-SPEC-KOTLIN-v1 |
| data class | 用于 Facts / DTO | HK-NAMING-SPEC-KOTLIN-v1 |
| companion object | 替代 Java 静态方法（如 HlResponse 构建） | Kotlin 惯例 |
| 显式事务 | `TransactionTemplate`，禁止 `@Transactional` | P0-0 |
| 显式依赖 | `@Configuration + @Bean`，禁止 `@ComponentScan` | P0-0 |
| 显式事件 | `DomainEventPublisher`，禁止 `@EventListener` | P0-0 |

### 4.2 命名规范

沿用 HK-NAMING-SPEC-KOTLIN-v1 全部规则，核心摘要：

| 类别 | 命名模式 | 示例 |
|------|---------|------|
| Can 服务 | `Can{Action}{Entity}Service` | `CanCreateProductService` |
| Action 服务 | `{Action}{Entity}Service` | `CreateProductService` |
| 输入 | `{Action}{Entity}Facts` | `CreateProductFacts` |
| 输出 | `{Action}{Entity}Result` | `CreateProductResult` (sealed class) |
| Port 接口 | `{Action}{Entity}Port` | `CreateProductPort` |
| API 路径 | `/biz/{module}/{action}` / `.can` | `/biz/product/create` |
| reason_code | `biz.{module}.{action}.{outcome}` | `biz.product.create.denied.no_permission` |

### 4.3 统一响应格式

```kotlin
data class HlResponse<T>(
    val code: String,
    val msg: String,
    val data: T? = null,
    val traceId: String,
    val eventId: String? = null   // 仅 key_action 成功时填充
) {
    companion object {
        fun <T> ok(data: T, traceId: String, eventId: String? = null) = // ...
        fun deny(code: String, msg: String, data: Any?, traceId: String) = // ...
    }
}
```

**三参数 deny 铁律不变**：`deny(code, msg, data)` — 禁止省略任何参数。

---

## 5. 权限矩阵

### 5.1 决策权限

| 决策类型 | 可发起 | 可审批 | 最终裁决 |
|---------|--------|--------|---------|
| 架构裁决（新增/修改 RULINGS） | 任何人 | Gate H 评审 | 创始人 |
| 能力包立项（biz.{module} 确认） | PM 推荐 | Gate H 技术可行性 | 创始人 |
| 能力包边界争议 | PM + 后端讨论 | Gate H 仲裁 | 创始人（如 Gate H 无法解决） |
| reason_code 新增 | PM 初稿 → 后端补充 | Gate H | 自动（PR merge 即生效） |
| 技术选型变更 | 任何人提议 | Gate H + 创始人评估 | 创始人 |
| 灰度发布决策 | Gate R 提议 | Gate H 确认 | 创始人 |

### 5.2 操作权限

| 操作 | PM | 业务开发者 | Gate H | Gate R | Infra | 验收官 | 创始人 |
|------|-----|-----------|--------|--------|-------|--------|--------|
| 提交 hl-contracts PR | ✅ | ✅ | ✅ | — | — | — | ✅ |
| 审批 hl-contracts PR | — | — | ✅ | — | — | — | ✅ |
| 提交 hl-platform PR | — | ✅ | ✅ | — | ✅ | — | ✅ |
| Gate H 签字 | — | — | ✅ | — | — | — | — |
| Gate R 签字 | — | — | — | ✅ | — | — | — |
| Gate 3 签字 | — | — | — | — | — | ✅ | — |
| 创建 hl-dispatch Issue | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 合并 PR | — | — | — | — | — | — | ✅ |
| RULINGS.md 写入 | — | — | — | — | — | — | ✅ |
| Flyway 迁移脚本执行（生产） | — | — | — | ✅ | — | — | ✅ |
| 灰度开关变更（生产） | — | — | — | ✅ | — | — | ✅ |

---

## 6. Phase 0 不适用概念清单

以下旧工程概念在本文档中**不再出现**，任何引用均视为文档污染：

| 旧概念 | 替代 / 处置 |
|--------|-----------|
| WS-A / WS-B / WS-C / WS-D / WS-E | 三环模型（守护者 / 业务 / 基础设施） |
| 13 人适配团队 | 业务开发者（按需扩编，从零构建） |
| Canal 对账 / binlog 同步 | R-031 SUPERSEDED，不再使用 |
| Nacos 集成 / 服务注册 | R-027 SUPERSEDED，全阶段不引入 |
| Keycloak Phase 0 集成 | DD-AUTH：Phase 0 Spring Security JWT |
| starter-mq / starter-cache / starter-mybatis | TECH-STACK-SPEC v3：Phase 0 不预置 |
| RocketMQ 事务消息 | Phase 0 Spring Events + Modulith Outbox |
| 旧系统改造 / 旧 SaaS 适配 | R-045：全新构建，旧系统冻结 |
| 6 Sprint（S0-S5）/ M0-M5 | R-053：5 Sprint（S0-S4）/ M0-M4 |
| `route_to: http://biz-xxx:8080` | R-055：Phase 0-2 `route_to: internal` |
| `HlResponseWrapFilter` / `ReasonCodeMapper` | 全新构建无适配层，Controller 直接返回 HlResponse |
| `PM-A01 / PM-A02 / PM-A03` LOCKED | R-015 SUPERSEDED：降级为参考输入 |
| `package-info.java` | D1 Kotlin：使用 Kotlin 注解 |
| `@JsonProperty` 逐字段 | `@JsonNaming(SnakeCaseStrategy::class)` |
| `biz-capabilities-blueprint.yaml` | capabilities.yaml + reason_codes.csv（hl-contracts SSOT） |
| 10 个 biz.* 旧能力包清单 | R-053：S2 结束时从用户价值链重新推导 |

---

## 7. 裁决记录（原待裁决事项，2026-03-17 全部裁决完毕）

| 编号 | 事项 | 裁决结果 | Ruling |
|------|------|---------|--------|
| D-1 | 业务开发者扩编 | ✅ S0 招聘 2 名 Kotlin 业务开发者，S1 onboard | R-056 |
| D-2 | S4 能力包并行人力模型 | ✅ 1 人 1 包按序滚动，最多 2 包并行，质量优先，不扩编 | R-057 |
| D-3 | QA 角色定义 | ✅ 不设独立 QA；P0-5 开发者自测 / 集成+E2E 李旭阳 / UAT 邹骢 | R-058 |
| D-4 | 前端交付规范 | ✅ Swift + Flutter 并行，人力 S1 期间确定 | R-060 |
| D-5 | 刘建成/李旭阳角色定位 | ✅ 李旭阳升级技术验收官纳入核心组；刘建成不纳入（旧工程交付 + 数据打通） | R-059 |

---

## 8. 关联文档修订清单

本文档生效后，以下文档需要同步修订：

| 文档 | 修订内容 | 优先级 |
|------|---------|--------|
| `_workspace-legacy/outputs/ROLE-RESPONSIBILITIES-PHASE1.md` | 头部追加 SUPERSEDED 标注，指向本文档 | P0 |
| `hl-dispatch/README.md` | 角色表对齐三环模型；魏鹏职责从 Nacos/MQ 改为 JWT/Observability/SDK | P0 |
| `hl-contracts/prd/devpack/DEVPACK-biz.TEMPLATE.v1.0.md` | §2.1 `route_to` → `internal`；清除 HlResponseWrapFilter / PM-A01~A03 / blueprint 引用 | P0 |
| `hl-framework/CLAUDE.md` | Starter 数量从 7 改为 5 + BOM | P1 |
| `hl-contracts/governance/CLAUDE.md` | 已在 2026-03-17 SAAC 审计中更新，确认无残留 | ✅ 已完成 |

---

## 9. 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-17 | v1.0 | DRAFT — 从 SAAC-HL v1.1 第一性原理推导全新协作模型，替代旧工程 ROLE-RESP |
| 2026-03-17 | v1.1 | LOCKED — D-1~D-5 全部裁决：R-056 扩编 / R-057 滚动人力 / R-058 无QA / R-059 角色定位 / R-060 前端并行。李旭阳升级技术验收官纳入核心组；刘建成分离至旧工程；新增 §2.5 前端规划 + §3.3 测试分工 |
