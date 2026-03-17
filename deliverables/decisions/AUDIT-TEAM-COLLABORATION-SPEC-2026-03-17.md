# 团队协作规范审计报告

## AUDIT-TEAM-COLLABORATION-SPEC — 已有规范盘点 × 冲突识别 × 模糊地带

---

**审计编号**：AUDIT-TEAM-COLLAB-2026-03-17
**版本**：v1.0
**日期**：2026-03-17
**审计范围**：7 个仓库全量扫描（hl-contracts / hl-dispatch / hl-platform / hl-framework / hl-factory / hl-console-native / _workspace-legacy）
**审计方法**：文档交叉比对，以 LOCKED 裁决为权威真源

---

## 一、已明确的协作规范（绿灯区）

以下规范在多份文档中一致、无矛盾，可直接沿用。

### 1.1 治理铁律（H3 三步链路）

**真源**：SAAC-HL-001 v1.1 + SAAC-HL-EP-001 v1.1 P0-5 + HK-NAMING-SPEC-KOTLIN-v1

所有 key_action 必须 Can → Action → Audit 三步完整执行，附 5 必过测试。命名规范（`Can{Action}{Entity}Service` / `{Action}{Entity}Service` / `{Action}{Entity}Facts` / `{Action}{Entity}Result`）在 HK-NAMING-SPEC、DEVPACK-biz.TEMPLATE、PM-BRANCH-LAUNCH-TEMPLATE 三处一致。

**状态**：✅ 完全明确，零冲突。

### 1.2 契约优先工作流（H4）

**真源**：SAAC-HL-001 v1.1 H4 + SAAC-HL-EP-001 P0-3 + DEVPACK-biz.TEMPLATE §0-§2

跨域通信必须先在 hl-contracts 注册（reason_codes.csv → OpenAPI YAML → capabilities.yaml），再写代码。reason_code 零硬编码（P0-4），CI 门禁自动校验。

**状态**：✅ 完全明确，DEVPACK-biz.TEMPLATE §1.2 的开工检查清单与 PM-BRANCH-LAUNCH-TEMPLATE §7.2 一致。

### 1.3 代码分层约束（P0-0 / P0-1 / P0-2）

**真源**：SAAC-HL-EP-001 v1.1 + TECH-STACK-SPEC v3 §10

domain/ 零 Spring、零 JPA import；adapter/ 允许 Spring；模块只依赖 `:contract`。8 道 CI 门禁脚本名称和对应约束在 TECH-STACK-SPEC v3 与 PM-BRANCH-LAUNCH-TEMPLATE §6 完全一致。

**状态**：✅ 完全明确，零冲突。

### 1.4 Gate H / Gate R 双门禁验收

**真源**：ROLE-RESPONSIBILITIES-PHASE1.md §1.3 + R-053 里程碑表 + hl-dispatch README

Gate H（许久明）= 代码健康 + 架构合规 + 测试覆盖；Gate R（曾正龙）= 可构建 + 可观测 + 可回滚。创始人代码不可自验，必须过 Gate H。里程碑 M0-M4 验收人分配在 R-053 中明确。

**状态**：✅ 验收人和职责在三份文档中一致。

### 1.5 hl-dispatch 异步协作三模式

**真源**：hl-dispatch README

模式 A（文档审查 = Issue）、模式 B（任务派发 = Issue + Checklist）、模式 C（代码/契约变更 = PR）。标签体系（doc-review / task-assign / decision-request / architect / ops / pm / priority-p0/p1）已定义。Issue 模板（doc-review.yml / task-assign.yml / decision-request.yml）已落地。

**状态**：✅ 完全明确，已有工程落地。

### 1.6 R-044 AI 驱动型任务主导权

**真源**：R-044 LOCKED

CI 门禁脚本、GitHub Actions、Skill、Prompt 模板等 AI 驱动型任务由创始人主导编写。团队做 review + 运维兜底 + 执行部署。不纳入 WS-C 工时。

**状态**：✅ 原则明确（但与 ROLE-RESP 存在联动冲突，见第二节）。

---

## 二、冲突区域（红灯区）

以下问题是两份或以上文档对同一事项的描述存在实质性矛盾。

### 🔴 C-1：团队编制——R-034（SUPERSEDED）vs R-053（LOCKED）vs ROLE-RESP vs hl-dispatch README

| 维度 | R-034（已废弃） | R-053（现行） | ROLE-RESP | hl-dispatch README |
|------|---------------|-------------|-----------|-------------------|
| 核心团队 | 4 人 | **6 人**（旧 4 + 2 待定） | 4 人 | 7 人（含邹骢、李旭阳） |
| WS-C 编制 | 13 人固定 | **待独立裁决** | 13 人（刘建成项目 + 4 Java + 3 前端 + 4 QA） | 未提及 WS-C |
| Sprint 数 | 6 个（S0-S5） | **5 个（S0-S4）** | 6 个（S0-S5） | 未提及 |
| 里程碑 | M0-M5 | **M0-M4** | M0-M5 | 未提及 |

**冲突本质**：ROLE-RESPONSIBILITIES-PHASE1.md 标题即为「旧系统改造岗位职责说明」，整个前提（旧系统改造）已被 R-045 全新构建裁决推翻，但文档仍在 _workspace-legacy/outputs/ 中存在且未标注失效。hl-dispatch README 的角色表则超出了 R-053 的 6 人核心组定义（多了邹骢和李旭阳），但 R-053 未明确否定他们的存在。

**影响**：新成员阅读到 ROLE-RESP 会获得错误的团队结构认知（13 人 WS-C、6 Sprint、Canal 对账等任务）。

**建议**：ROLE-RESP 需要标注 SUPERSEDED 或归档；hl-dispatch README 需要与 R-053 对齐核心组定义；WS-C 团队编制需要尽快独立裁决。

---

### 🔴 C-2：魏鹏职责——Nacos / Keycloak / MQ 全部发生变化

| 原职责（ROLE-RESP + hl-dispatch README） | 现状（LOCKED 裁决） |
|----------------------------------------|-------------------|
| Keycloak 集成（S1 端到端联调） | DD-AUTH：Phase 0 Spring Security 内建 JWT，Keycloak 延后到 Phase 1+ |
| Nacos 集成（服务注册 + 健康检查） | R-027 SUPERSEDED（2026-03-17）：全阶段不引入 Nacos |
| RocketMQ starter-mq（S2 交付） | R-054 Q1：外部 MQ Phase 0 不预置 |
| starter-cache（S2 与许久明协作交付） | DD-CACHE / R-054 Q3 SUPERSEDED：Phase 0 无缓存框架 |

**冲突本质**：魏鹏在 ROLE-RESP 中定义为 WS-D「认证集成与性能」负责人，核心交付物几乎全部基于 Nacos + Keycloak + MQ + Cache。这四项在当前 LOCKED 裁决下全部被延后或取消。他在 Phase 0 的职责变成了空集。

**影响**：如果不重新定义魏鹏的 Phase 0 职责，出现以下风险：人力闲置 / 职责真空 / 其他成员对他的工作预期与实际不符。

**建议**：需要创始人裁决魏鹏在全新构建路径下的新职责（可能方向：starter-security JWT 实现、starter-observability、HK Client SDK、性能基线测试）。

---

### 🔴 C-3：曾正龙职责——基础设施大幅缩减

| 原职责（ROLE-RESP WS-E） | 现状 |
|--------------------------|------|
| PG + Nacos 3 副本 + SkyWalking + OTel + Redis + RocketMQ 部署 | Phase 0 仅 PG18 + App 容器（TECH-STACK-SPEC v3 §11 O-02） |
| Canal 对账脚本 + 首日运行报告 | R-031 SUPERSEDED：Canal 不再使用 |
| 灰度切流执行（S5） | R-053 无 S5（灰度策略与业务节奏绑定，按需单独规划） |

**冲突本质**：ROLE-RESP 定义曾正龙 S0 交付物为「PG18 + Nacos 3 副本 + SkyWalking + OTel receiver 联调」，但现在 Nacos 不引入、SkyWalking 未在 TECH-STACK-SPEC v3 中锁定。Canal 相关任务全部消失。

**影响**：与 C-2 类似，Phase 0 实际基础设施需求大幅缩减。

**建议**：重新定义 WS-E Phase 0 交付清单，可能聚焦于：PG18 部署 + RLS 验证 + Flyway 流水线 + Docker Compose 开发环境 + Outbox 事件表监控 + Grafana 面板。

---

### 🔴 C-4：许久明 Starter 交付——数量和内容冲突

| 文档 | Starter 数量 | 内容 |
|------|-------------|------|
| ROLE-RESP S1 交付 | 多个分批 | starter-logging + starter-exception（S1）→ starter-mq + starter-cache（S2） |
| R-037 修订 + TECH-STACK-SPEC v3 §9 | **5 + BOM** | boot / web / security / data-jpa / observability（无 mq / cache / mybatis） |
| hl-framework settings.gradle.kts | 8 个模块 | 包含 starter-mq / starter-cache / starter-api（多余） |
| hl-framework CLAUDE.md | 7 Starters | 未具体列举 |

**冲突本质**：四处文档给出了四个不同的 Starter 数量和组成。权威真源（TECH-STACK-SPEC v3 §9 LOCKED）为 5 + BOM，但 ROLE-RESP 还在要求许久明交付 starter-mq 和 starter-cache，hl-framework 代码里也还有多余模块。

**影响**：许久明可能仍在按旧交付清单工作（准备 starter-mq / starter-cache），浪费精力。

**建议**：hl-framework settings.gradle.kts 清理多余模块；ROLE-RESP 交付清单对齐 5 Starters；hl-framework CLAUDE.md 修正为 5 + BOM。

---

### 🔴 C-5：DEVPACK-biz.TEMPLATE capabilities.yaml 路由方式与架构冲突

| 文档 | route_to 值 | 架构假设 |
|------|------------|---------|
| DEVPACK-biz.TEMPLATE.v1.0.md §2.1 | `http://biz-{module}-service:8080` | 能力包是独立部署的微服务 |
| R-055 LOCKED + TECH-STACK-SPEC v3 §11 | `internal`（进程内调用） | Phase 0-2 单 JVM Modulith，HK 不独立部署 |
| PM-BRANCH-LAUNCH-TEMPLATE §3.3 | `internal` | 与 R-055 一致 |

**冲突本质**：DEVPACK-biz.TEMPLATE 是开发者的「唯一入口」文档，但它仍假设能力包是独立微服务（`route_to: http://biz-xxx:8080`）。这与 R-055（Phase 0-2 内部治理内核）和 TECH-STACK-SPEC v3 §7（Phase 0 不拆微服务）直接矛盾。开发者照此操作会配出错误的路由。

**影响**：高优先级——直接影响所有能力包的 Gateway 注册方式。

**建议**：DEVPACK-biz.TEMPLATE.v1.0.md §2.1 需要修订 `route_to` 为 `internal`，并标注 Phase 3 才可能使用 HTTP 路由。

---

### 🔴 C-6：ROLE-RESP 代码规范——Java 范式 vs Kotlin 现实

| 条目 | ROLE-RESP 规定 | 现行裁决 |
|------|--------------|---------|
| DTO 字段 | `@JsonProperty` 显式标注 snake_case | D1 裁决 Kotlin：data class + `@JsonNaming(SnakeCaseStrategy)` 或 kotlinx.serialization |
| 模块声明 | `package-info.java` 声明 `@ApplicationModule` | Kotlin 无 package-info.java，改用 `package-info.kt` 或 Modulith 注解 |
| 响应包裹 | `HlResponse.deny(code, msg, data)` Java 静态方法 | Kotlin sealed class / companion object 方式 |
| 代码注释 | AI 生成代码必须附充分注释 | Kotlin 惯例更偏向自文档化（命名表达意图），注释策略需修订 |

**冲突本质**：ROLE-RESP 全文基于 Java 编码规范，但 D1 裁决（2026-03-13）已将实现语言改为 Kotlin 2.1.10。Java 特有的模式（package-info.java、@JsonProperty、静态方法）在 Kotlin 中不适用或有更好的替代。

**影响**：中等——新开发者按 ROLE-RESP 写 Java 风格 Kotlin 代码。

**建议**：需要产出 Kotlin 版编码规范替代 ROLE-RESP §1.3 代码规范纪律，与 HK-NAMING-SPEC-KOTLIN-v1 对齐。

---

## 三、模糊地带（黄灯区）

以下事项在现有文档中未被清晰定义，但对 PM 分支业务启动有实质影响。

### ⚠️ A-1：WS-C 团队编制——从「适配」到「开发」，但无人员名单

R-053 明确说「WS-C 定位从适配转为开发」「编制和职责作为独立裁决，S3 验证通过后决定」，但：

- 原 WS-C 13 人（4 Java + 3 前端 + 4 QA + 刘建成 + 许久明技术）是否沿用？
- 全新构建不再需要「适配层」经验，团队技能匹配度是否足够？
- S4 需要 3-5 个能力包从零构建，人力估算完全缺失
- 李旭阳（Java 验收）、邹骢（PM）在 hl-dispatch README 中出现但在 R-053 核心组 6 人中未列入

**需裁决**：WS-C Phase 1 编制表（人数 / 角色 / 技能要求 / 与核心组的汇报关系）。

---

### ⚠️ A-2：PM 分支业务启动中 PM 角色的具体权限边界

PM-BRANCH-LAUNCH-TEMPLATE 定义了 PM 的交付物（MVP 规格 / Facts / reason_codes / 验收用例 / UAT），但未定义：

- PM 是否有权发起裁决请求（decision-request）？还是必须通过创始人？
- PM 定义的 reason_code 能否直接提 PR，还是必须先经过创始人审批？
- PM 与后端 Owner 在「能力包边界」上有分歧时，谁有最终决策权？
- LAUNCH-PRODUCT-CENTER 中的 PM（邹骢）在 hl-dispatch 中标注为「后续另行分工」，权限未正式授予

**需裁决**：PM 在能力包启动流程中的权限矩阵（可直接行动 / 需审批 / 需裁决）。

---

### ⚠️ A-3：前端协作接口——hl-console-native 与消费者端的交付规范缺失

PM-BRANCH-LAUNCH-TEMPLATE §5.3 定义了前端交付物（线框 / API 对接 / 审计回放 / 端到端联调），但：

- hl-console-native（Swift）与消费者端（Flutter）是两个完全不同的技术栈，合并为「前端」角色是否合理？
- 消费者端在 R-053 S3 止步于「stub 级别」，那 S4 呢？前端完整 UI 在哪个 Sprint 交付？
- 前端与后端的 API 契约对齐方式未定义：是前端消费 OpenAPI YAML 自动生成 client？还是手工对接？
- ROLE-RESP 中前端规范（Can→Confirm→Action 三步、ConfirmDialog / EventIdCopy / ReasonCodeTag 复用组件）全部基于旧系统 Web 端，在 Swift/Flutter 原生端是否适用？

**需裁决**：前端交付规范需要独立产出，区分 hl-console-native（Swift）和消费者端（Flutter）两条线。

---

### ⚠️ A-4：QA 角色完全未定义

PM-BRANCH-LAUNCH-TEMPLATE §5.4 给 QA 分配了交付物（测试计划 / 自动化测试 / 性能基线 / 缺陷报告），但全仓库无 QA 相关的具体规范：

- QA 在哪个仓库提交测试代码？hl-platform 的 test/ 目录？独立测试仓库？
- QA 测试与后端 P0-5 五必过测试的关系是什么？是后端自测后 QA 复验？还是 QA 独立编写？
- QA 使用什么测试框架？JUnit 5（与后端一致）？还是独立工具（Postman / K6）？
- E2E 测试覆盖范围：仅后端 API？还是包含 Gateway → HK → biz 全链路？
- ROLE-RESP 中原有 4 名 QA（属 WS-C），但 WS-C 编制待独立裁决

**需裁决**：QA 工作规范（工具链 / 测试分层 / 仓库归属 / 与后端测试的分工边界）。

---

### ⚠️ A-5：R-044 AI 主导权 vs Gate H 审查——CI 门禁的审批死循环

R-044 规定 CI 门禁脚本由创始人主导编写。ROLE-RESP §2.1 规定创始人的代码交付必须通过许久明 Gate H 审查（不可自验）。

当创始人修改 `gate-deny-check.sh`（CI 门禁脚本）时：

1. R-044 → 创始人主导编写 ✓
2. ROLE-RESP → 创始人代码必须过 Gate H ✓
3. 但 Gate H 的审查标准本身由 CI 门禁定义 → 循环依赖

如果许久明对 CI 门禁脚本的技术理解不足（R-044 的前提就是「团队尚未完成 AI-native 转型」），Gate H 审查可能流于形式。

**需澄清**：R-044 范围内的 AI 驱动型任务是否豁免 Gate H？还是走简化审查流程（逻辑正确性 review，不要求架构深审）？

---

### ⚠️ A-6：能力包清单讨论时机——S2 中期 vs Phase 0 结束

R-053 有两处关于能力包清单的时间表述：

- 「S2 中期即启动能力包清单讨论，S2 结束时裁决首批 3-5 个核心包」
- 「Phase 0 期间不锁定能力包清单」

S2 是 Phase 0 的一部分，所以这两条不矛盾——S2 结束 = Phase 0 结束。但如果 S2 提前完成或延期，讨论窗口在哪里？

- 如果 S2 提前完成 → 能力包讨论是否提前启动？
- 如果 S2 延期 → S3 demo 包选型何时确定？是否允许 S2 和 S3 重叠？
- PM 是否需要在 S1 就开始能力包调研准备？

**需澄清**：能力包清单讨论的触发条件是时间节点（S2 中期）还是交付节点（治理层投产后）。

---

### ⚠️ A-7：跨仓库变更的协同流程

能力包启动涉及同时修改多个仓库：

1. hl-contracts：reason_codes.csv + OpenAPI YAML + capabilities.yaml + PRD 文档集
2. hl-platform：contract/ 层接口 + kernel/biz-{module}/ 模块 + DDL
3. hl-dispatch：LAUNCH-{MODULE}.md 启动规格

但现有文档未定义：

- 三个仓库的 PR 提交顺序（contracts 先 → platform 后？还是同时？）
- 跨仓库 PR 的 reviewer 指派规则
- 契约变更与代码变更的版本锁定机制（contracts v1 → platform 引用 v1，如何保证不漂移？）
- 如果 contracts PR 被打回，platform 已经基于旧版本开发了怎么办？

**需定义**：跨仓库变更的提交协议和版本锁定机制。

---

### ⚠️ A-8：DEVPACK-biz.TEMPLATE 中的旧系统残留引用

DEVPACK-biz.TEMPLATE.v1.0.md §1.2 开工检查清单引用：

- `biz-capabilities-blueprint.yaml`（PM-A01 LOCKED / PM-A02 LOCKED / PM-A03 LOCKED）
- 但 R-015 已 SUPERSEDED（2026-03-17）：「PM-A01/A02/A03 的 key_action/reason_code/risk_level 降级为参考输入，不作为约束」

DEVPACK 还引用了 `HlResponseWrapFilter`（旧系统适配层概念），在全新构建路径下不再需要 Filter 包装——能力包直接在 Controller 层返回统一格式。

**需修订**：DEVPACK-biz.TEMPLATE.v1.0.md 需要对齐全新构建路径，清除旧系统适配层引用。

---

## 四、汇总矩阵

| 编号 | 类型 | 主题 | 影响域 | 优先级 | 处理方式 |
|------|------|------|--------|--------|---------|
| C-1 | 🔴 冲突 | 团队编制 R-034 vs R-053 vs ROLE-RESP vs dispatch README | 全团队 | P0 | ROLE-RESP 标注 SUPERSEDED；dispatch README 对齐 R-053 |
| C-2 | 🔴 冲突 | 魏鹏职责全部被延后/取消 | WS-D | P0 | 创始人裁决新 Phase 0 职责 |
| C-3 | 🔴 冲突 | 曾正龙基础设施大幅缩减 | WS-E | P0 | 重新定义 Phase 0 交付清单 |
| C-4 | 🔴 冲突 | Starter 数量四处不一致 | WS-B / hl-framework | P1 | 统一对齐 TECH-STACK-SPEC v3（5 + BOM） |
| C-5 | 🔴 冲突 | DEVPACK route_to 微服务 vs 单 JVM | 全开发者 | P0 | 修订 DEVPACK §2.1 route_to → internal |
| C-6 | 🔴 冲突 | ROLE-RESP Java 规范 vs Kotlin 现实 | 全后端 | P1 | 产出 Kotlin 编码规范替代 |
| A-1 | ⚠️ 模糊 | WS-C 编制从适配到开发，无名单 | S4 人力 | P0 | 独立裁决（R-053 已标注） |
| A-2 | ⚠️ 模糊 | PM 权限边界未定义 | PM 启动效率 | P1 | 在 PM-BRANCH-LAUNCH-TEMPLATE 补充权限矩阵 |
| A-3 | ⚠️ 模糊 | 前端交付规范缺失 | hl-console-native / 消费者端 | P1 | 分别产出 Swift / Flutter 前端交付规范 |
| A-4 | ⚠️ 模糊 | QA 角色完全未定义 | 测试质量 | P1 | 产出 QA 工作规范 |
| A-5 | ⚠️ 模糊 | R-044 AI 主导 vs Gate H 审查死循环 | CI 基础设施 | P2 | 澄清 AI 驱动型任务的 Gate H 审查级别 |
| A-6 | ⚠️ 模糊 | 能力包清单讨论触发条件 | S3/S4 规划 | P2 | 明确触发条件（时间 vs 交付节点） |
| A-7 | ⚠️ 模糊 | 跨仓库变更协同流程 | 全能力包启动 | P1 | 定义跨仓库提交协议 |
| A-8 | ⚠️ 模糊 | DEVPACK 旧系统残留引用 | 开发者体验 | P1 | 修订 DEVPACK-biz.TEMPLATE |

---

## 五、下一步行动建议

**立即处理（P0，Phase 0 启动前）**：

1. ROLE-RESPONSIBILITIES-PHASE1.md 头部追加 SUPERSEDED 标注 + 指向 R-053
2. hl-dispatch README 角色表对齐 R-053 核心组 6 人 + 明确扩展角色定位
3. 创始人裁决：魏鹏 / 曾正龙 Phase 0 新职责（可合并为一条裁决）
4. DEVPACK-biz.TEMPLATE.v1.0.md §2.1 修订 route_to → internal

**Sprint 内处理（P1，S2 前完成）**：

5. 产出 Kotlin 编码规范（替代 ROLE-RESP §1.3 Java 规范）
6. hl-framework settings.gradle.kts 清理多余 Starter 模块
7. 定义跨仓库变更提交协议
8. DEVPACK-biz.TEMPLATE 清除旧系统残留引用（PM-A01/A02/A03、HlResponseWrapFilter）
9. PM 权限矩阵补充到 PM-BRANCH-LAUNCH-TEMPLATE
10. 前端交付规范（Swift / Flutter 分别定义）
11. QA 工作规范

**可延后处理（P2）**：

12. R-044 × Gate H 审查级别澄清
13. 能力包清单讨论触发条件澄清

---

## 六、版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-17 | v1.0 | 初始审计：6 个红灯冲突 + 8 个黄灯模糊 |
