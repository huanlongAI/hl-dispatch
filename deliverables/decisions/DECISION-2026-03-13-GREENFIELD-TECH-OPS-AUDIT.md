# 唤龙平台全新构建 — 技术选型清单 & 运维就绪检查

> **文档编号**：DECISION-2026-03-13-GREENFIELD-TECH-OPS-AUDIT
> **版本**：v1.0（2026-03-13）
> **裁决人**：童正辉（创始人）
> **审计人**：许久明（架构）、曾正龙（运维）、魏鹏（后端基础设施）
> **性质**：全新系统建设规划，不受旧工程影响

---

## 〇、前置声明

本清单基于 R-045（全新构建路线 LOCKED）和 SAAC-HL-001 v1.0 架构宪法。所有选型遵循六大原则：

| 原则 | 编号 | 一句话 |
|------|------|--------|
| 治理深度 | HL-P1 | HK Kernel 是不可替换的结构性优势 |
| 桥梁递减 | HL-P2 | 基础设施只作为桥梁，能不引入就不引入 |
| 契约驱动 | HL-P3 | hl-contracts 是 SSOT，代码必须服从契约 |
| 退出准备 | HL-P4 | 任何桥梁组件必须可替换 |
| 审计主权 | HL-P5 | 所有 key_action 必经 Can→Action→Audit |
| 自由检验 | HL-P6 | 替换全部 S-L5 ≤ 10 人天 |

**旧系统完全无关**：本清单不含 MySQL、MyBatis、Canal、Seata、Java 17/25 双轨、SkyWalking、Nacos（Phase 0）等已废弃选项。

---

## 一、技术选型清单（附根本原因）

### 1.1 计算与运行时

| 序号 | 选型 | 版本 | 根本原因 | 裁决 |
|------|------|------|----------|------|
| T-01 | **Java 21 LTS** | 21 | 全平台统一基线，Virtual Threads 为 Phase 1 高并发预留能力，LTS 保证 8 年支持周期 | R-030 |
| T-02 | **Spring Boot** | 3.5.11 | Modulith 唯一成熟选择，Spring Modulith 模块化单体架构直接支持 SAAC-HL 的"先内聚后外放"策略 | R-040, B-1 |
| T-03 | **Gradle + Kotlin DSL** | 8.12 | 类型安全构建脚本 + 多模块依赖管理能力优于 Maven | H-006 |
| T-04 | **容器镜像** | temurin:21-jre-alpine | Alpine 最小攻击面 + Temurin 社区免费 + 与 Java 21 版本对齐 | — |

### 1.2 数据与存储

| 序号 | 选型 | 版本 | 根本原因 | 裁决 |
|------|------|------|----------|------|
| T-05 | **PostgreSQL** | 18 | RLS 行级安全（tenant_id 天然隔离）+ 递归 CTE（OrgLink 树查询）+ JSONB（策略规则灵活存储），三个能力无替代 | R-017, R-035 |
| T-06 | **两区数据模型** | — | S-L6 事务区（OLTP）+ D 域分析区（OLAP），Outbox→CDC 单向流，职责清晰不互污染 | R-035 修订 |
| T-07 | **RocketMQ** | 5.x serverless | 阿里云 serverless 共享版零运维 + 按量计费，Phase 0 验证成本极低；30s 窗口/3 次退避/event_id 幂等语义已锁定 | R-043, R-023 |
| T-08 | **Caffeine 本地缓存** | — | Phase 0 单实例不需要分布式缓存，L1 足够；Phase 1 再叠加 Redis L2 | R-054 Q3 |
| T-09 | ~~Nacos~~ **不引入** | — | HL-P2 桥梁递减：Modulith 单实例无服务发现需求，配置由 PG 策略表 + application.yml 覆盖 | R-054 Q2 |
| T-10 | ~~Redis~~ **Phase 0 不引入** | — | HL-P2 桥梁递减：单实例 Caffeine L1 TTL 足够；Phase 1 多实例后按需引入 | R-054 Q3 |

### 1.3 认证与安全

| 序号 | 选型 | 版本 | 根本原因 | 裁决 |
|------|------|------|----------|------|
| T-11 | **Keycloak** | 26.x | 开源 IdP 事实标准，仅负责 token 签发（认证），业务授权由 HK.Policy 管辖——职责分离 | R-024 |
| T-12 | **HK.Policy + Gateway** | — | fail-secure 架构：路径解析失败→BLOCK；Feature Toggle 未启用→501。治理裁决不可绕过 | R-008, R-009, R-013 |
| T-13 | **Secrets 管理** | 分阶段 | Phase 0: 环境变量注入（ECS .env + CI Secret）；Phase 1+: 阿里云 KMS + ack-secret-manager | B-2 |

### 1.4 可观测性

| 序号 | 选型 | 版本 | 根本原因 | 裁决 |
|------|------|------|----------|------|
| T-14 | **OpenTelemetry** | Java Agent 最新稳定 | 厂商中立（HL-P4 退出准备），一套埋点对接任何后端；跳过 SkyWalking 过渡，直接投产 | R-021, R-039 |
| T-15 | **Grafana 生态** | — | Prometheus（指标）+ Loki（日志）+ Tempo（链路）+ Alertmanager（告警），统一 Dashboard | R-021 |

### 1.5 开发框架（hl-framework）

| 序号 | 选型 | 说明 | 根本原因 | 裁决 |
|------|------|------|----------|------|
| T-16 | **hl-framework-bom** | 统一版本管理 | 子模块不单独声明版本，BOM 一处锁定全平台依赖 | R-037 |
| T-17 | **7 Starters** | boot/web/security/data-jpa/cache/mq/observability | 每个 Starter 对应一个横切关注点，按需引入不强制全装 | R-037 |
| T-18 | ~~starter-data-mybatis~~ **已砍** | — | 全新构建无旧项目，JPA 唯一 ORM，不做双轨 | R-037 修订 |

### 1.6 CI/CD 与治理门禁

| 序号 | 选型 | 说明 | 根本原因 | 裁决 |
|------|------|------|----------|------|
| T-19 | **GitHub Actions** | CI/CD 平台 | huanlongAI 组织已在 GitHub，迁移成本为零 | R-025 |
| T-20 | **4 道 CI Gate** | deny-check / circular-dep / terminology / spring-isolation | 自动化守护 SAAC-HL §7.1 禁令，不依赖人工 review 发现违规 | R-033, R-054 Q4 |
| T-21 | **main 分支保护** | PR + 1 Review + CI 全过 | 禁止直接 push main，所有变更可追溯 | R-025 |

### 1.7 客户端

| 序号 | 选型 | 说明 | 根本原因 | 裁决 |
|------|------|------|----------|------|
| T-22 | **Apple 原生 (SwiftUI)** | C 域控制台 | 治理控制台面向管理员，原生体验 + 光合设计系统深度集成 | R-052, R-036 |
| T-23 | **Flutter** | S 域消费者端 | 消费者端跨平台覆盖（iOS/Android/Web），Phase 1 启动 | R-052 |

### 1.8 部署拓扑

| 序号 | 阶段 | 拓扑 | 规格 | 根本原因 | 裁决 |
|------|------|------|------|----------|------|
| T-24 | Phase 0 | ECS 单机 Docker Compose | 4C8G | 300 租户 Modulith 单实例足够，成本最低 | B-1 |
| T-25 | Phase 1 | ACS/ACK Pro 托管 | 按量弹性 | 多实例高可用需求出现时切换 | B-1 |
| T-26 | 10K 租户 | ACK Pro 多节点 | HPA + PDB | 水平扩缩 + 滚动升级零停机 | B-1 |

### 1.9 架构治理

| 序号 | 选型 | 说明 | 根本原因 | 裁决 |
|------|------|------|----------|------|
| T-27 | **HK Kernel 6 模块** | ID/OrgLink/Policy/Consent/Audit/ReasonDict | SAAC-HL 核心资产，恒定层 H1，不可替换 | SAAC-HL §2.2 |
| T-28 | **HK 内部消费模式** | Phase 0-2 SDK 内嵌，Phase 3 创始人裁决后方可开放 external API | 先内聚后外放，避免过早分布式化 | R-055 |
| T-29 | **Spring Modulith** | 模块化单体 | 先把模块边界做硬（CI gate 强制），再决定是否拆分 | SAAC-HL §2.2 |
| T-30 | **hl-contracts SSOT** | 契约法典驱动 | 所有 API、事件、术语、reason_code 以契约为准，代码服从契约 | HL-P3 |

---

## 二、运维就绪检查清单

> **本节需曾正龙逐项确认**：成本估算是否准确、相关运维经验是否具备、是否需要额外学习/外部支持。

### 2.1 Phase 0 运维清单（ECS 单机）

| 序号 | 检查项 | 具体要求 | 估算成本（年） | 经验要求 | 曾正龙确认 |
|------|--------|----------|---------------|----------|-----------|
| O-01 | ECS 实例 | 阿里云 4C8G，CentOS/Alinux 3 | ~1500-2500 元 | ECS 基础运维 | ☐ 成本确认 ☐ 经验具备 |
| O-02 | Docker Compose 部署 | Java App + PG18 + Keycloak + RocketMQ 四容器编排 | 含在 ECS 内 | Docker Compose 编排 | ☐ 经验具备 |
| O-03 | PostgreSQL 18 RDS | 阿里云 RDS 4C8G HA，复用已有实例 | 已有实例，增量 ~0 | PG 基础运维 + Flyway 迁移 | ☐ 成本确认 ☐ 经验具备 |
| O-04 | RocketMQ serverless | 阿里云 serverless 共享版，按累积消息量计费 | Phase 0 消息量极低，预计 <100 元/月 | RocketMQ 基础配置 | ☐ 成本确认 ☐ 经验具备 |
| O-05 | Keycloak 26.x | Docker 容器部署，连接 PG 作为后端存储 | 含在 ECS 内 | Keycloak Realm/Client 配置 | ☐ 经验具备 ☐ 需要学习 |
| O-06 | OTel Java Agent | 应用启动参数注入，数据发往 Grafana 后端 | Agent 免费 | OTel 配置 | ☐ 经验具备 ☐ 需要学习 |
| O-07 | Grafana 全家桶 | Grafana + Prometheus + Loki + Tempo | 自部署：含在 ECS 或单独小实例 ~500 元/年；云版按用量 | Grafana 运维 | ☐ 成本确认 ☐ 经验具备 ☐ 需要学习 |
| O-08 | SSL 证书 + 域名 | 阿里云免费证书 / Let's Encrypt + 已有域名 | ~0（免费证书） | Nginx/证书配置 | ☐ 经验具备 |
| O-09 | GitHub Actions CI | huanlongAI 组织，免费额度 2000 min/月 | 免费额度内（预计够用） | GitHub Actions 配置 | ☐ 经验具备 |
| O-10 | Secrets 管理 | .env 文件 + CI Secret 注入 + 敏感扫描 CI | ~0 | 环境变量管理 | ☐ 经验具备 |
| O-11 | 备份策略 | PG RDS 自动备份 + 应用日志保留 30 天 | 含在 RDS 内 | 备份/恢复演练 | ☐ 经验具备 |

**Phase 0 总成本估算**：~2000-4000 元/年（ECS + RDS 增量 + RocketMQ 按量 + Grafana）

### 2.2 Phase 1 新增运维项（ACS/ACK 集群）

| 序号 | 检查项 | 具体要求 | 估算成本增量 | 经验要求 | 曾正龙确认 |
|------|--------|----------|-------------|----------|-----------|
| O-12 | ACS/ACK Pro 集群 | 阿里云容器服务，按节点数计费 | 视节点规模，~5000-15000 元/年 | K8s 集群运维 | ☐ 成本确认 ☐ 经验具备 ☐ 需要学习 |
| O-13 | Redis 7.x | 阿里云 Redis 或自建，L2 分布式缓存 | ~1000-3000 元/年 | Redis 运维 | ☐ 成本确认 ☐ 经验具备 |
| O-14 | KMS + ack-secret-manager | 阿里云 KMS 托管密钥 | ~500 元/年 | KMS 配置 | ☐ 经验具备 ☐ 需要学习 |
| O-15 | HPA + PDB | K8s 水平扩缩 + Pod 中断预算 | 含在集群内 | K8s 高级调度 | ☐ 经验具备 ☐ 需要学习 |
| O-16 | Alertmanager | 生产告警 5 条 P0 规则 + runbook | 含在 Grafana 生态 | 告警规则配置 | ☐ 经验具备 |
| O-17 | CDC 工具 | Debezium 或阿里云 DTS（S2 选型） | DTS 按量 ~100-500 元/月 | CDC 管道运维 | ☐ 经验具备 ☐ 需要学习 |

### 2.3 运维技能缺口自评

> 请曾正龙根据以下清单自评，标注需要补齐的技能和预计学习时间。

| 技能领域 | 具体技能 | 自评（熟练/了解/不会） | 预计补齐时间 |
|----------|----------|----------------------|-------------|
| 容器 | Docker Compose 编排 | ☐ | |
| 容器 | K8s 基础运维（Deployment/Service/ConfigMap） | ☐ | |
| 容器 | K8s 高级（HPA/PDB/滚动升级） | ☐ | |
| 数据库 | PostgreSQL RDS 运维 + Flyway | ☐ | |
| 数据库 | Redis 运维 | ☐ | |
| 认证 | Keycloak 26.x Realm/Client 配置 | ☐ | |
| 消息 | RocketMQ 5.x 配置 + 监控 | ☐ | |
| 可观测 | OTel Agent 配置 | ☐ | |
| 可观测 | Grafana + Prometheus + Loki + Tempo | ☐ | |
| 安全 | 阿里云 KMS + ack-secret-manager | ☐ | |
| CI/CD | GitHub Actions workflow 编写 | ☐ | |
| CDC | Debezium 或阿里云 DTS | ☐ | |

---

## 三、审计要求

### 许久明（架构审计）

请逐项审查第一节「技术选型清单」：
1. 每个选型的根本原因是否成立？是否有遗漏的 trade-off？
2. T-27~T-30 架构治理部分是否与 SAAC-HL-001 完全一致？
3. 是否存在选型之间的冲突或隐患？
4. HL-P6 自由检验（替换全部 S-L5 ≤ 10 人天）在当前选型下是否仍然成立？

### 曾正龙（运维审计）

请逐项确认第二节「运维就绪检查清单」：
1. 每个 ☐ 打勾或标注问题
2. 成本估算是否与阿里云实际价格匹配？给出你的修正值
3. 技能缺口自评表全部填写
4. 如需外部培训或支持，列出具体需求和时间

### 魏鹏（后端基础设施审计）

请审查以下实施可行性：
1. T-05 PostgreSQL 18 + Flyway：Schema 管理方案是否有坑？
2. T-07 RocketMQ 5.x serverless：Spring Boot 3.5.x 集成是否有已知问题？
3. T-11 Keycloak 26.x + hl-starter-security：JWT Claims 最小集实现路径是否清晰？
4. T-17 七个 Starters 的依赖关系：是否存在循环依赖或版本冲突风险？
5. T-14 OTel Java Agent + Spring Boot 3.5.x：是否有兼容性问题？

---

## 四、时间线

| 截止时间 | 动作 |
|----------|------|
| 收到后 3 天内 | 三人各自完成审计，在 Issue 评论区反馈 |
| 反馈后 2 天内 | 创始人汇总裁决，更新本文档为 v1.1 |
| 裁决后 | 纳入 R-053 执行计划，启动 S0 就绪检查 |

---

## 五、关联裁决索引

R-008, R-009, R-013, R-017, R-021, R-022, R-023, R-024, R-025, R-030, R-033, R-035, R-036, R-037, R-039, R-040, R-043, R-044, R-045, R-050, R-051, R-052, R-053, R-054, R-055, SAAC-HL-001 v1.0, B-1, B-2

---

*本文档由创始人发起，经三人审计后锁版。*
