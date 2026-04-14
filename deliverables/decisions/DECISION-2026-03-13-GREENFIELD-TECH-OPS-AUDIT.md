# 唤龙平台全新构建 — 技术选型清单 & 运维就绪检查

> **文档编号**：DECISION-2026-03-13-GREENFIELD-TECH-OPS-AUDIT
> **版本**：v1.1（2026-03-17）
> **裁决人**：L0-Founder（创始人）
> **审计人**：Gate-H（架构）、Gate-R（运维）、Infra-A（后端基础设施）
> **性质**：全新系统建设规划，不受旧工程影响
> **v1.1 变更**：全面对齐 SAAC-HL-001 v1.1 + TECH-STACK-SPEC v3 + 2026-03-13～03-17 全部裁决变更。纳入 D1 Kotlin 裁决、DD-CACHE/DD-AUTH 推导、R-027 SUPERSEDED、R-015 SUPERSEDED、R-042 SUPERSEDED、R-054 Q1/Q3 状态变更。新增 T-31～T-36。

---

## 〇、前置声明

本清单基于 R-045（全新构建路线 LOCKED）和 **SAAC-HL-001 v1.1** 架构宪法。选型权威推导链：

```
SAAC-HL-001 v1.1（公理层）
    ↓
BRIDGE-DERIVATION v1（D1-D10 桥梁层推导）
    ↓
DD-ORM / DD-AUTH / DD-CACHE（补充推导）
    ↓
EP-001 v1.1（P0-0~P0-6 执行约束）
    ↓
TECH-STACK-SPEC v3（版本锁定 + 理由速查）
    ↓
本文件（选型清单 + 运维就绪检查）
```

所有选型遵循六大原则：

| 原则 | 编号 | 一句话 |
|------|------|--------|
| 治理深度 | HL-P1 | HK Kernel 是不可替换的结构性优势 |
| 桥梁递减 | HL-P2 | 基础设施只作为桥梁，能不引入就不引入 |
| 契约驱动 | HL-P3 | hl-contracts 是 SSOT，代码必须服从契约 |
| 退出准备 | HL-P4 | 任何桥梁组件必须可替换 |
| 审计主权 | HL-P5 | 所有 key_action 必经 Can→Action→Audit |
| 自由检验 | HL-P6 | 替换全部 S-L5 ≤ 10 人天 |

**旧系统完全无关**：本清单不含 MySQL、MyBatis、Canal、Seata、Java 17/25 双轨、SkyWalking 等已废弃选项。**Phase 0 不预置**：外部 MQ（RocketMQ/Kafka）、Nacos（R-027 SUPERSEDED）、Keycloak（DD-AUTH：Phase 0 内建 JWT）、缓存框架（DD-CACHE：Phase 0 无可测量瓶颈）。

---

## 一、技术选型清单（附根本原因）

### 1.1 语言与构建

| 序号 | 选型 | 版本 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-01 | **Kotlin** | 2.1.10 / JVM 21 LTS | sealed class 编译时穷举治理决策分支（A8 公理）+ 默认不可变 val + null safety（B2 公理）+ value class 零开销类型安全 | D1, R-030 修订 |
| T-02 | **Spring Boot** | 3.5.11 | **仅作 adapter/runtime 容器**（P0-0）：HTTP 服务器 + 连接池 + 配置加载。治理逻辑全部在纯 Kotlin domain 层，domain/ 零 Spring import（P0-1） | D2, R-040 |
| T-03 | **Gradle + Kotlin DSL** | 8.12 | 4 kernel 模块 + gateway + contract + app 各自独立 build.gradle.kts，编译器天然隔离越权依赖（P0-2） | D3, H-006 |
| T-04 | **容器镜像** | temurin:21-jre-alpine | Alpine 最小攻击面 + Temurin 社区免费 + 与 JVM 21 版本对齐 | — |

### 1.2 框架与模块治理

| 序号 | 选型 | 版本 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-16 | **Spring Modulith** | 1.3.4 | ApplicationModules.verify() 语义层验证 + Outbox 支持（spring-modulith-events）+ 与 Gradle multi-module 互补双层边界 | D2+D3, TECH-STACK-SPEC v3 §3.2 |
| T-17 | **5 Starters + BOM** | — | boot / web / security / data-jpa / observability，每个对应一个横切关注点。Phase 0 骨架（kotlin-stdlib），Phase 1 填充实际依赖 | R-037 修订, TECH-STACK-SPEC v3 §9 |
| T-18 | ~~starter-data-mybatis~~ **已砍** | — | 全新构建无旧项目，JPA 唯一 ORM | R-037 修订 |
| T-18b | ~~starter-cache / starter-mq~~ **已砍** | — | DD-CACHE：Phase 0 不预置缓存；EP-001 §2.2：Phase 0 不预置外部 MQ | R-037 修订, TECH-STACK-SPEC v3 §9 |

### 1.3 数据与存储

| 序号 | 选型 | 版本 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-05 | **PostgreSQL** | 18.x latest | RLS 行级安全（tenant_id 隔离）+ JSONB（EvaluationFacts / 审计 payload）+ ACID 事务（governedAction 语义），三个能力无替代 | D5, R-017, R-035 |
| T-06 | **两区数据模型** | — | S-L6 事务区（OLTP）+ D 域分析区（OLAP），Outbox→CDC 单向流 | R-035 修订 |
| T-05b | **Spring Data JPA + Hibernate** | Spring Boot 管理 | JPA 注解仅限 adapter/persistence 层，domain Entity 与 JpaEntity 分离（P0-1）。kotlin-jpa 2.1.10 自动 no-arg 构造 | DD-ORM |
| T-07 | ~~RocketMQ~~ **Phase 0 不预置** | — | EP-001 §2.2 优先：单 JVM 域内事件用 Spring Events + Modulith Outbox。R-054 Q1 降级为 Phase 1 参考 | R-054 Q1 冲突裁决, D6/D10 |
| T-08 | ~~Caffeine~~ **Phase 0 不预置** | — | DD-CACHE 推导：Phase 0 规模无可测量性能瓶颈，不预置任何缓存框架（含 Caffeine）。R-054 Q3 已 SUPERSEDED | DD-CACHE, R-054 Q3→SUPERSEDED |
| T-09 | ~~Nacos~~ **全阶段不引入** | — | HL-P2 桥梁递减：单 JVM 无服务发现需求，配置由 PG 策略表 + yml + env 覆盖。**R-027 SUPERSEDED（2026-03-17）** | R-054 Q2, R-027→SUPERSEDED, D10 |
| T-10 | ~~Redis~~ **Phase 0 不引入** | — | DD-CACHE：Phase 0 不预置。Phase 1 多实例后按需引入（缓存 L2 + pub/sub） | DD-CACHE |

### 1.4 认证与安全

| 序号 | 选型 | 版本 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-11 | **Phase 0: Spring Security 内建 JWT** | Spring Boot 管理 | DD-AUTH 推导：单 JVM 内自签发 JWT 满足 Phase 0，无需外部认证服务器。ProtocolGate 验证 JWT 提取 IdentityId | DD-AUTH |
| T-11b | **Phase 1+: Keycloak** | 26.x | 联邦登录需求出现时引入。开源 IdP 事实标准，仅负责 token 签发，业务授权由 HK.Policy 管辖 | R-024, DD-AUTH 退出条件 |
| T-12 | **HK.Policy + Gateway** | — | fail-secure 架构：路径解析失败→BLOCK；Feature Toggle 未启用→501。治理裁决不可绕过。R-042 已 SUPERSEDED（F-1~F-5 全部失效，新 Kotlin 代码从零满足契约） | R-008, R-009, R-013, R-042→SUPERSEDED |
| T-13 | **Secrets 管理** | 分阶段 | Phase 0: 环境变量注入（ECS .env + CI Secret）；Phase 1+: 阿里云 KMS + ack-secret-manager | B-2 |

### 1.5 可观测性

| 序号 | 选型 | 版本 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-14 | **OpenTelemetry** | Java Agent 最新稳定 | 厂商中立（HL-P4 退出准备），一套埋点对接任何后端 | R-021, R-039 |
| T-15 | **Grafana 生态** | — | Prometheus（指标）+ Loki（日志）+ Tempo（链路）+ Alertmanager（告警） | R-021 |
| T-15b | **Phase 0: Actuator + Logback + Micrometer** | Spring Boot 管理 | starter-observability 骨架，Phase 0 轻量可观测 | TECH-STACK-SPEC v3 §9 |

### 1.6 测试

| 序号 | 选型 | 版本 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-19b | **JUnit 5** | 5.10.2 | Kotlin backtick 中文场景命名（测试即文档）+ 参数化测试（策略规则矩阵覆盖） | P0-6, TECH-STACK-SPEC v3 §5 |

### 1.7 CI/CD 与治理门禁

| 序号 | 选型 | 说明 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-19 | **GitHub Actions** | CI/CD 平台 | huanlongAI 组织已在 GitHub | R-025 |
| T-20 | **8 道 CI Gate** | check-domain-isolation / check-no-implicit-spring / check-jpa-isolation / check-reason-codes / gate-circular-dep / gate-deny-check / gate-spring-isolation / validate-contracts | 自动化守护 P0-0～P0-6 执行约束 | TECH-STACK-SPEC v3 §10 |
| T-21 | **main 分支保护** | PR + 1 Review + CI 全过 | 禁止直接 push main | R-025 |

### 1.8 客户端

| 序号 | 选型 | 说明 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-22 | **Apple 原生 (SwiftUI)** | C 域控制台 | 治理控制台面向管理员，原生体验 + 光合设计系统深度集成 | R-052, R-036 |
| T-23 | **Flutter** | S 域消费者端 | 消费者端跨平台覆盖（iOS/Android/Web），Phase 1 启动 | R-052 |

### 1.9 部署拓扑

| 序号 | 阶段 | 拓扑 | 规格 | 根本原因 | 裁决/推导源 |
|------|------|------|------|----------|------------|
| T-24 | Phase 0-1 | **单 JVM Modulith** | ECS 4C8G | 6 人团队 + 单产品，Modulith 足够 | D9, B-1 |
| T-25 | Phase 2 | **按需拆分** | ACS/ACK Pro | 多团队独立发布需求出现时 | D9 退出条件 |
| T-26 | Phase 3 | **微服务（生态开放）** | ACK Pro 多节点 | 生态开放需求 + R-055 条件满足后 | D9 退出条件 |

### 1.10 数据流转（CDC/Outbox）

| 序号 | 选型 | 阶段 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-31 | **Outbox 模式** | Phase 0: Spring Modulith Event Publication Log（内置 Outbox 表） | SAAC-HL §7.2："S-L6 事务事件必须通过 Outbox 模式发布"。Phase 0 单实例使用 Modulith 内置能力，零额外组件 | D6, TECH-STACK-SPEC v3 §3.2 |
| T-32 | **CDC 工具** | Phase 1+: Debezium 或阿里云 DTS（S2 选型评估） | S-L6 事务区→D 域分析区单向数据流 | 待 S2 裁决 |

### 1.11 智能态（Phase 1+ 范畴）

| 序号 | 选型 | 状态 | 说明 | 裁决/推导源 |
|------|------|------|------|------------|
| T-33 | **LLM 网关** | OPEN | LiteLLM Gateway（Sidecar 部署）已评估，Phase 1 首批能力包验证后触发 LOCK | R-014 修订 |

### 1.12 数据态（Phase 2 范畴）

| 序号 | 选型 | 状态 | 说明 | 裁决/推导源 |
|------|------|------|------|------------|
| T-34 | **D 域 OLAP 引擎** | 未裁决 | Phase 2 范畴。候选：ClickHouse / StarRocks / 阿里云 AnalyticDB | — |
| T-35 | **数据湖/仓库** | 未裁决 | Phase 2 范畴。候选：Hudi / Iceberg / 阿里云 MaxCompute | — |
| T-36 | **数据目录与血缘** | 未裁决 | Phase 2 范畴。候选：DataHub / Apache Atlas | — |

### 1.13 架构治理

| 序号 | 选型 | 说明 | 根本原因 | 裁决/推导源 |
|------|------|------|----------|------------|
| T-27 | **HK Kernel 4 模块** | Identity / OrgLink / Policy / Audit（Kotlin domain 纯实现） | SAAC-HL 核心资产，恒定层 H1。Phase 0 四模块，Consent / ReasonDict 按需后续纳入 | SAAC-HL §2.2, TECH-STACK-SPEC v3 |
| T-28 | **HK 内部消费模式** | Phase 0-2 SDK 内嵌，Phase 3 创始人裁决后方可开放 external API | 先内聚后外放，避免过早分布式化 | R-055 |
| T-29 | **Spring Modulith** | 模块化单体 | 先把模块边界做硬（CI gate 强制），再决定是否拆分 | SAAC-HL §2.2 |
| T-30 | **hl-contracts SSOT** | 契约法典驱动 | 所有 API、事件、术语、reason_code 以契约为准，代码服从契约 | HL-P3 |

---

## 二、运维就绪检查清单

> **本节需Gate-R逐项确认**：成本估算是否准确、相关运维经验是否具备、是否需要额外学习/外部支持。

### 2.1 Phase 0 运维清单（ECS 单机 / 单 JVM Modulith）

| 序号 | 检查项 | 具体要求 | 估算成本（年） | 经验要求 | Gate-R确认 |
|------|--------|----------|---------------|----------|-----------|
| O-01 | ECS 实例 | 阿里云 4C8G，CentOS/Alinux 3 | ~1500-2500 元 | ECS 基础运维 | ☐ 成本确认 ☐ 经验具备 |
| O-02 | Docker Compose 部署 | Java App + PG18 两容器编排（v1.1：**无 Nacos/RocketMQ/Keycloak 容器**，Phase 0 单 JVM 最小化） | 含在 ECS 内 | Docker Compose 编排 | ☐ 经验具备 |
| O-03 | PostgreSQL 18 RDS | 阿里云 RDS 4C8G HA，复用已有实例 | 已有实例，增量 ~0 | PG 基础运维 + Flyway 迁移 | ☐ 成本确认 ☐ 经验具备 |
| O-06 | OTel Java Agent | 应用启动参数注入，数据发往 Grafana 后端 | Agent 免费 | OTel 配置 | ☐ 经验具备 ☐ 需要学习 |
| O-07 | Grafana 全家桶 | Grafana + Prometheus + Loki + Tempo | 自部署：含在 ECS 或单独小实例 ~500 元/年 | Grafana 运维 | ☐ 成本确认 ☐ 经验具备 ☐ 需要学习 |
| O-08 | SSL 证书 + 域名 | 阿里云免费证书 / Let's Encrypt + 已有域名 | ~0（免费证书） | Nginx/证书配置 | ☐ 经验具备 |
| O-09 | GitHub Actions CI | huanlongAI 组织，免费额度 2000 min/月 | 免费额度内 | GitHub Actions 配置 | ☐ 经验具备 |
| O-10 | Secrets 管理 | .env 文件 + CI Secret 注入 + 敏感扫描 CI | ~0 | 环境变量管理 | ☐ 经验具备 |
| O-11 | 备份策略 | PG RDS 自动备份 + 应用日志保留 30 天 | 含在 RDS 内 | 备份/恢复演练 | ☐ 经验具备 |
| O-18 | Outbox 事件表 | Spring Modulith Event Publication Log 内置 Outbox 表，PG 内自动管理，需监控 event_publication 表大小与清理策略 | 含在 RDS 内 | Spring Modulith 事件机制 | ☐ 经验具备 ☐ 需要学习 |

**Phase 0 总成本估算**：~2000-3500 元/年（ECS + RDS 增量 + Grafana）—— v1.1 注：因去除 RocketMQ serverless、Keycloak 容器，Phase 0 成本低于 v1.0 估算。

### 2.2 Phase 1 新增运维项（ACS/ACK 集群）

| 序号 | 检查项 | 具体要求 | 估算成本增量 | 经验要求 | Gate-R确认 |
|------|--------|----------|-------------|----------|-----------|
| O-04 | RocketMQ serverless | 阿里云 serverless 共享版（Phase 1 引入，R-054 Q1 降级） | 预计 <100 元/月 | RocketMQ 基础配置 | ☐ 成本确认 ☐ 经验具备 |
| O-05 | Keycloak 26.x | Phase 1+ 联邦登录需求触发时引入 | 含在集群内 | Keycloak Realm/Client 配置 | ☐ 经验具备 ☐ 需要学习 |
| O-12 | ACS/ACK Pro 集群 | 阿里云容器服务，按节点数计费 | ~5000-15000 元/年 | K8s 集群运维 | ☐ 成本确认 ☐ 经验具备 ☐ 需要学习 |
| O-13 | Redis 7.x | 阿里云 Redis 或自建，L2 分布式缓存 + pub/sub | ~1000-3000 元/年 | Redis 运维 | ☐ 成本确认 ☐ 经验具备 |
| O-14 | KMS + ack-secret-manager | 阿里云 KMS 托管密钥 | ~500 元/年 | KMS 配置 | ☐ 经验具备 ☐ 需要学习 |
| O-15 | HPA + PDB | K8s 水平扩缩 + Pod 中断预算 | 含在集群内 | K8s 高级调度 | ☐ 经验具备 ☐ 需要学习 |
| O-16 | Alertmanager | 生产告警 5 条 P0 规则 + runbook | 含在 Grafana 生态 | 告警规则配置 | ☐ 经验具备 |
| O-17 | CDC 工具 | Debezium 或阿里云 DTS（S2 选型） | DTS 按量 ~100-500 元/月 | CDC 管道运维 | ☐ 经验具备 ☐ 需要学习 |

### 2.3 运维技能缺口自评

> 请Gate-R根据以下清单自评，标注需要补齐的技能和预计学习时间。

| 技能领域 | 具体技能 | 自评（熟练/了解/不会） | 预计补齐时间 |
|----------|----------|----------------------|-------------|
| 容器 | Docker Compose 编排 | ☐ | |
| 容器 | K8s 基础运维（Deployment/Service/ConfigMap） | ☐ | |
| 容器 | K8s 高级（HPA/PDB/滚动升级） | ☐ | |
| 数据库 | PostgreSQL RDS 运维 + Flyway | ☐ | |
| 数据库 | Redis 运维 | ☐ | |
| 认证 | Spring Security JWT（Phase 0）+ Keycloak 26.x（Phase 1+） | ☐ | |
| 消息 | RocketMQ 5.x 配置 + 监控（Phase 1+） | ☐ | |
| 可观测 | OTel Agent 配置 | ☐ | |
| 可观测 | Grafana + Prometheus + Loki + Tempo | ☐ | |
| 安全 | 阿里云 KMS + ack-secret-manager | ☐ | |
| CI/CD | GitHub Actions workflow 编写 | ☐ | |
| CDC | Debezium 或阿里云 DTS | ☐ | |
| 事件 | Spring Modulith Event Publication（Outbox） | ☐ | |

---

## 三、审计要求

> **v1.1 更新**：2026-03-17 SAAC 污染审计已完成（见附件审计报告），全面对齐 TECH-STACK-SPEC v3。以下审计要求保留供后续审计轮次使用。

### Gate-H（架构审计）

请逐项审查第一节「技术选型清单」：
1. 每个选型的根本原因是否成立？是否有遗漏的 trade-off？
2. T-27~T-30 架构治理部分是否与 SAAC-HL-001 v1.1 完全一致？
3. 是否存在选型之间的冲突或隐患？
4. HL-P6 自由检验（替换全部 S-L5 ≤ 10 人天）在当前选型下是否仍然成立？
5. **v1.1 新增**：T-31～T-36 新增条目的 SAAC 对齐性审查
6. **v1.1 新增**：D1 Kotlin 裁决 + DD-CACHE/DD-AUTH 推导对选型的连锁影响是否完整反映

### Gate-R（运维审计）

请逐项确认第二节「运维就绪检查清单」：
1. 每个 ☐ 打勾或标注问题
2. 成本估算是否与阿里云实际价格匹配？给出你的修正值
3. 技能缺口自评表全部填写
4. 如需外部培训或支持，列出具体需求和时间
5. **v1.1 新增**：Phase 0 容器编排简化（仅 App + PG）的运维影响确认
6. **v1.1 新增**：O-18 Outbox 事件表监控策略确认

### Infra-A（后端基础设施审计）

请审查以下实施可行性：
1. T-05 PostgreSQL 18 + Flyway：Schema 管理方案是否有坑？
2. T-01 Kotlin 2.1.10 + Spring Boot 3.5.11：kotlin-spring / kotlin-jpa 插件兼容性是否已验证？
3. T-11 Phase 0 Spring Security 内建 JWT：ProtocolGate 集成路径是否清晰？
4. T-17 五个 Starters 的依赖关系：是否存在循环依赖或版本冲突风险？
5. T-14 OTel Java Agent + Spring Boot 3.5.x：是否有兼容性问题？
6. **v1.1 新增**：T-31 Spring Modulith Event Publication Log 与 PG Outbox 表实现路径确认
7. **v1.1 新增**：8 道 CI Gate 脚本（T-20）是否全部就绪可执行？

---

## 四、时间线

| 截止时间 | 动作 | 状态 |
|----------|------|------|
| 2026-03-13 | v1.0 发出，三人审计启动 | ✅ 完成 |
| 2026-03-13 | TECH-STACK-SPEC v3 发布，D1 Kotlin + DD-CACHE/DD-AUTH 推导完成 | ✅ 完成 |
| 2026-03-17 | SAAC 污染审计 + 全面对齐，v1.1 发布 | ✅ 完成 |
| v1.1 发出后 3 天内 | 三人根据 v1.1 更新项逐项复审 | ⏳ 待执行 |
| 复审完成后 | 纳入 R-053 执行计划，启动 S0 就绪检查 | ⏳ 待执行 |

---

## 五、关联裁决索引

**SAAC 推导链**：SAAC-HL-001 v1.1, BRIDGE-DERIVATION D1-D10, DD-ORM, DD-AUTH, DD-CACHE, EP-001 v1.1, TECH-STACK-SPEC v3

**LOCKED 裁决**：R-008, R-009, R-013, R-014, R-017, R-021, R-022, R-023, R-024, R-025, R-030, R-033, R-035, R-036, R-037, R-039, R-040, R-043, R-044, R-045, R-050, R-051, R-052, R-053, R-054, R-055

**SUPERSEDED 裁决**（本清单相关）：R-004, R-015, R-027, R-031, R-034, R-042, R-054 Q3

**桥梁组件**：B-1（Spring Boot）, B-2（Secrets 管理）

**v1.1 新增引用**：D1, D6, D9, D10, DD-ORM, DD-AUTH, DD-CACHE, P0-0～P0-6, M-2

---

## 六、裁决状态速查表

> 汇总 v1.0→v1.1 期间涉及的裁决状态变更。

| 裁决编号 | 原状态 | 新状态 | 变更日期 | 变更原因 | 影响选型项 |
|----------|--------|--------|----------|----------|-----------|
| R-027 | LOCKED | **SUPERSEDED** | 2026-03-17 | HL-P2 桥梁递减：B4 退出条件已满足，R-054 Q2 + TECH-STACK-SPEC v3 §7 确认 | T-09 Nacos 全阶段不引入 |
| R-015 | LOCKED（待修订） | **SUPERSEDED** | 2026-03-17 | 全新构建路径下旧系统适配方案不适用，PM-A01/A02/A03 降级 | — |
| R-042 | LOCKED（待修订） | **SUPERSEDED** | 2026-03-13 | D1 Kotlin 裁决：旧 Java 代码不复存在，F-1~F-5 失去前提 | T-12 HK.Policy |
| R-054 Q1 | LOCKED | **降级** | 2026-03-13 | EP-001 §2.2 优先，外部 MQ Phase 0 暂缓 | T-07 RocketMQ Phase 0 不预置 |
| R-054 Q3 | LOCKED | **SUPERSEDED** | 2026-03-13 | DD-CACHE 推导推翻 Caffeine/Redis 分层方案 | T-08 缓存 Phase 0 不预置 |
| R-035.A | LOCKED | LOCKED（**措辞修订**） | 2026-03-17 | 清除旧系统语言残留 | T-05 PG 租户模型 |

---

## 七、Phase 0 不预置清单（v1.0→v1.1 新增章节）

> 源自 TECH-STACK-SPEC v3 §7（D10 桥梁层递减），明确 Phase 0 的「不做清单」。

| 组件 | 不预置理由 | 引入条件 | 推导源 |
|------|-----------|---------|--------|
| gRPC | 域内函数调用足够 | 能力包独立部署 | D10 |
| 外部 MQ（RocketMQ/Kafka） | 单 JVM 用 Spring Events + Modulith Outbox | 跨进程异步需求 | D6/D10 |
| Nacos | 单 JVM 无服务发现/配置中心需求 | ~~多服务部署~~ 全阶段不引入（R-027 SUPERSEDED） | D10, R-027 |
| Keycloak | Spring Security 内建 JWT 满足 Phase 0 | 联邦登录需求 | DD-AUTH |
| 缓存框架（Caffeine/Redis） | Phase 0 规模无可测量性能瓶颈 | 出现性能瓶颈 | DD-CACHE |
| 微服务拆分 | 6 人团队 + 单产品 + 单 JVM 足够 | 多团队独立发布 | D9 |

---

*本文档由创始人发起，v1.0（2026-03-13）初版，v1.1（2026-03-17）全面对齐 SAAC-HL-001 v1.1 + TECH-STACK-SPEC v3 推导链。*
