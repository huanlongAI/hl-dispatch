# PM 分支业务启动模板

## PM Branch Launch Template — 唤龙平台能力包启动规格

---

**模板编号**：TPL-PM-LAUNCH-001
**版本**：v1.0
**日期**：2026-03-17
**适用阶段**：Phase 1 S3/S4（R-053 LOCKED）
**创建者**：L0-Founder
**治理根**：SAAC-HL-001 v1.1 → R-053 → R-055 → HK-NAMING-SPEC-KOTLIN-v1

---

## 0. 模板说明

本模板是唤龙平台业务能力包（`biz.*`）从「裁决 → 设计 → 开发 → 验收」全流程的标准化启动规格。每启动一个新的 PM 分支业务（商品中心、订单中心、库存中心等），从本模板派生一份实例文档，填充具体业务内容。

**模板使用时机**：R-053 S2 治理层投产中期，讨论并裁决首批 3-5 个能力包清单后，为每个能力包生成一份启动规格。

**模板与治理文档的关系**：

```
SAAC-HL-001 v1.1（架构宪法）
  → TECH-STACK-SPEC v3（技术选型锁定）
    → R-053（执行计划 Phase 0→1）
      → TPL-PM-LAUNCH-001（本模板）
        → LAUNCH-{MODULE}.md（每个能力包的实例文档）
```

---

## 1. 模块身份卡

> 填写说明：确立能力包在唤龙体系中的唯一身份。命名必须遵循 R-019（去品牌化）。

| 字段 | 填写内容 |
|------|---------|
| **能力包 ID** | `biz.{module_name}`（全小写，R-019 去品牌化） |
| **中文名称** | 例：商品中心 |
| **一句话定义** | 用一句话说清楚这个能力包做什么、不做什么 |
| **所属 Phase** | Phase 1 S3(demo) / S4(正式) |
| **优先级批次** | S4 首批 / S4 次批 / 延后 |
| **PM 负责人** | 姓名 |
| **后端 Owner** | 姓名 |
| **前端 Owner** | 姓名 |
| **验收人** | Gate H（Gate-H）+ Gate R（Gate-R） |

---

## 2. 业务域分析

### 2.1 用户价值链推导

> R-053 明确：能力包清单从用户价值链推导，不从旧系统映射。此节必须回答「用户为什么需要这个能力包」。

**目标用户角色**（基于 R-003 网络拓扑模型）：

| 角色 | TenantSpace 节点类型 | 与本能力包的关系 |
|------|---------------------|-----------------|
| _（填写）_ | Claim / Cooperate | _（填写）_ |

**核心价值主张**：
- _（1-3 条，聚焦用户价值，非功能清单）_

### 2.2 能力包边界

> 定义「做什么」和「不做什么」，防止能力包膨胀。

**做（In Scope）**：
- _（列举本能力包的核心职责）_

**不做（Out of Scope）**：
- _（明确排除的功能，引用其他能力包或 HK 模块承载）_

### 2.3 与 HK 治理层交互矩阵

> 每个能力包必须声明与 HK 6 模块的交互关系。这决定了契约注册和审计链路的设计。

| HK 模块 | 交互方式 | 说明 |
|---------|---------|------|
| HK.Identity | ☐ 消费 / ☐ 无 | _（身份解析需求）_ |
| HK.OrgLink | ☐ 消费 / ☐ 无 | _（租户关系/跨租户场景）_ |
| HK.Policy | ☐ 消费 / ☐ 无 | _（策略评估 Can 判定）_ |
| HK.Consent | ☐ 消费 / ☐ 无 | _（授权同意需求）_ |
| HK.Audit | ☑ 消费（必选） | Can→Action→Audit 铁律（H3） |
| HK.ReasonDict | ☑ 消费（必选） | reason_code 注册（P0-4） |

---

## 3. 契约清单（hl-contracts 交付物）

> 契约优先（H4）：所有跨域通信必须在 hl-contracts 定义。能力包启动的第一步不是写代码，而是注册契约。

### 3.1 reason_codes 注册

> P0-4 铁律：reason_code 零硬编码。所有新增 code 必须先注册到 reason_codes.csv。

| code | constant | module | category | description |
|------|----------|--------|----------|-------------|
| `biz.{module}.{action}.can` | _{UPPER_SNAKE}_ | _{module}_ | can | _{说明}_ |
| `biz.{module}.{action}.success` | _{UPPER_SNAKE}_ | _{module}_ | outcome | _{说明}_ |
| `biz.{module}.{action}.denied.*` | _{UPPER_SNAKE}_ | _{module}_ | deny | _{说明}_ |
| _（续填）_ | | | | |

**注册流程**：PR → hl-contracts/reason_codes.csv → Gate H 审批 → merge → 代码引用

### 3.2 OpenAPI 契约

> 文件命名：`biz.{module}.internal.openapi.v1.yaml`（R-055：Phase 0-2 仅 internal）

**端点清单**（遵循 HK-NAMING-SPEC-KOTLIN-v1 §H3 命名）：

| HTTP | 路径 | 操作 | 类型 | key_action |
|------|------|------|------|-----------|
| POST | `/biz/{module}/{action}.can` | Can 预检 | Can | false |
| POST | `/biz/{module}/{action}` | 执行操作 | Action | true |
| _（续填每个 Action）_ | | | | |

**统一响应格式**（不可修改）：

```json
{
  "code": "biz.{module}.{action}.success",
  "msg": "操作成功",
  "data": { /* 业务数据 */ }
}
```

### 3.3 capabilities.yaml 注册

```yaml
- capability_id: biz.{module}
  version: v1
  routes:
    - path: /biz/{module}/**
      methods: [POST, GET]
      route_to: internal    # Phase 0-2 单 JVM，内部路由
  feature_toggle: biz_{module}_enabled
  required_hk:
    - hk.policy
    - hk.audit
    - hk.reasondict
```

### 3.4 Cap-Spec 文档集

> `biz.*` 能力包统一放在 `hl-contracts/prd/biz/`，不再复用 legacy `prd/core/` 目录。

| 文档 | 文件名 | 负责人 | 说明 |
|------|--------|--------|------|
| Cap-Spec-1 | `Cap-Spec-Biz.{Module}.v1.0.md` | PM | 目标、非目标、能力边界、业务规则意图 |
| Cap-Spec-2 | `Cap-Spec-Biz.{Module}.Acceptance.v1.0.md` | PM（QA collaborator） | Case-ID + 输入 / 预期 / 验收方式 |
| Cap-Spec-3 | `reasoncodes.csv` 提案 PR | PM | reason_code 新增/变更建议；需创始人先批 |

---

## 4. 代码架构规格（hl-platform 交付物）

### 4.1 Gradle 模块

> P0-2 模块边界：kernel 子模块只依赖 `:contract`。Gradle 物理隔离 + Modulith 语义双验证。

**新增模块位置**：

```
hl-platform/
├── contract/
│   └── src/main/kotlin/hk/
│       └── biz/{module}/           ← 契约层（Pure Kotlin，零依赖）
│           ├── {Action}{Entity}Port.kt       (接口)
│           ├── {Action}{Entity}Facts.kt      (data class)
│           ├── {Action}{Entity}Result.kt     (sealed class)
│           └── event/
│               └── {Entity}Events.kt         (sealed class)
│
├── kernel/biz-{module}/            ← 能力包模块（新建）
│   ├── build.gradle.kts
│   └── src/
│       ├── main/kotlin/hk/biz{module}/
│       │   ├── domain/             ← P0-1: 零 Spring/零 JPA import
│       │   │   ├── Can{Action}{Entity}Service.kt
│       │   │   ├── {Action}{Entity}Service.kt
│       │   │   └── model/
│       │   └── adapter/            ← Spring 仅在此层
│       │       ├── persistence/
│       │       │   ├── Jpa{Entity}Repository.kt
│       │       │   └── {Entity}JpaEntity.kt
│       │       ├── web/
│       │       │   └── {Module}Controller.kt
│       │       └── config/
│       │           └── Biz{Module}Configuration.kt
│       └── test/kotlin/hk/biz{module}/
│           └── domain/
│               └── {Action}{Entity}ServiceTest.kt   ← P0-5 五必过测试
```

**build.gradle.kts 依赖约束**：

```kotlin
dependencies {
    // 仅允许依赖 contract 模块
    implementation(project(":contract"))

    // adapter 层允许 Spring
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-web")

    // domain 层禁止 Spring（CI gate 验证）
    // 禁止：starter-cache, starter-mq, mybatis（Phase 0 不预置）
}
```

### 4.2 三步铁律实现规格（H3: Can → Action → Audit）

> 不可变约束，每个 key_action 必须实现完整三步。

**Can 服务**（命名：`Can{Action}{Entity}Service`）：

```kotlin
// domain/ 层，零 Spring import
class CanCreateProductService(
    private val policyPort: PolicyPort,
    private val auditPort: AuditPort
) {
    fun evaluate(facts: CreateProductFacts): CanResult {
        val result = policyPort.evaluate(facts)
        auditPort.recordCanDecision(facts.traceId, result) // DENY 也必须审计
        return result
    }
}
```

**Action 服务**（命名：`{Action}{Entity}Service`）：

```kotlin
class CreateProductService(
    private val canService: CanCreateProductService,
    private val productPort: CreateProductPort,
    private val auditPort: AuditPort
) {
    fun execute(facts: CreateProductFacts): CreateProductResult {
        // Step 1: 复验 Can
        val canResult = canService.evaluate(facts)
        if (canResult is CanResult.Deny) {
            return CreateProductResult.Denied(canResult.code)
        }
        // Step 2: 执行业务
        val product = productPort.create(facts)
        // Step 3: 审计（仅 COMPLETED 后写入）
        auditPort.recordAction(facts.traceId, product.eventId, AuditOutcome.COMPLETED)
        return CreateProductResult.Success(product)
    }
}
```

### 4.3 P0-5 五必过测试

> 每个 key_action 必须有以下 5 个测试用例：

| # | 测试场景 | 断言 |
|---|---------|------|
| 1 | Deny 时：Action 未执行 | verify { productPort.create wasNot called } |
| 2 | Deny 时：Audit 记录存在 | assertThat(auditRecords).hasSize(1).allMatch { it.outcome == DENIED } |
| 3 | Completed 时：Audit 记录存在 | assertThat(auditRecords).hasSize(1).allMatch { it.outcome == COMPLETED } |
| 4 | Failed 时：业务回滚但 Audit 存在 | 业务表无数据 + audit 表有 FAILED 记录 |
| 5 | Completed Audit 写入失败：降级不崩溃 | 主业务成功 + fallback 补偿触发 |

### 4.4 数据库规格

**Schema 归属**：能力包业务表统一在 PG18 `biz_{module}` schema 下（R-035 两区模型，全新构建无 MySQL）。

**DDL 规范**：

```sql
CREATE SCHEMA IF NOT EXISTS biz_{module};

-- 主实体表
CREATE TABLE biz_{module}.{entity} (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID            NOT NULL,       -- RLS 行级安全列
    -- ... 业务字段 ...
    event_id        UUID,                           -- 关联审计 event_id
    reason_code     VARCHAR(128),                   -- 最近操作 reason_code
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- RLS 策略（R-017 PG18）
ALTER TABLE biz_{module}.{entity} ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON biz_{module}.{entity}
    USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

---

## 5. 角色交付物与验收标准

### 5.1 PM（产品经理）

| 交付物 | 格式 | 验收标准 | 截止时间 |
|--------|------|---------|---------|
| MVP 规格 | PRD-Biz.{Module}.MVP.v1.0.md | 目标/非目标清晰；与 HK 交互矩阵完整 | Sprint 第 1 天 |
| Facts 定义 | PRD-Biz.{Module}.MVP.Facts.v1.0.md | 每个 Action 的输入 Facts 全覆盖 | Sprint 第 2 天 |
| reason_codes 初稿 | reason_codes.csv PR | 所有 deny 场景对应 code 已注册 | Sprint 第 2 天 |
| 验收用例 | Core-Acceptance-Cases.v1.0.md | 覆盖全部 key_action + 跨租户场景 | Sprint 第 3 天 |
| UAT 签收 | GitHub Issue Comment | 全部验收用例人工验证通过 | Sprint 结束前 |

### 5.2 后端开发

| 交付物 | 格式 | 验收标准 | 截止时间 |
|--------|------|---------|---------|
| contract 层接口 | Kotlin 代码 | Pure Kotlin，零依赖；命名符合 HK-NAMING-SPEC | Sprint 第 3 天 |
| OpenAPI 契约 | YAML | 端点、响应格式、reason_code 与 CSV 一致 | Sprint 第 3 天 |
| capabilities.yaml | YAML | feature_toggle 注册 + required_hk 声明 | Sprint 第 3 天 |
| domain 层实现 | Kotlin 代码 | P0-1 零 Spring import；三步铁律完整实现 | Sprint 第 7 天 |
| adapter 层实现 | Kotlin 代码 | JPA Entity + Repository + Controller | Sprint 第 7 天 |
| DDL 脚本 | SQL | RLS 策略 + tenant_id 列 + 索引 | Sprint 第 5 天 |
| 五必过测试 | Kotlin Test | 每个 key_action × 5 测试全部 green | Sprint 第 8 天 |
| Decision Trace | PRD doc | 裁决追踪 schema 完整 | Sprint 第 5 天 |
| Dev Checklist | PRD doc | 全部 checkbox ✅ | Sprint 结束前 |

### 5.3 前端开发（hl-console-native / 消费者端）

| 交付物 | 格式 | 验收标准 | 截止时间 |
|--------|------|---------|---------|
| 页面列表与交互线框 | Figma / Markdown | 覆盖全部用户角色的核心页面 | Sprint 第 3 天 |
| API 对接 | Swift (console) / Flutter (consumer) | 统一响应格式解析；reason_code 展示 | Sprint 第 7 天 |
| 审计回放集成 | UI 组件 | event_id 链路可追溯（控制台） | Sprint 第 8 天 |
| 端到端联调 | 截图 / 录屏 | 创建→查询→审计 完整链路通过 | Sprint 结束前 |

### 5.4 QA

| 交付物 | 格式 | 验收标准 | 截止时间 |
|--------|------|---------|---------|
| 测试计划 | Markdown | 覆盖 P0-5 五必过 + 并发/幂等 + 跨租户 | Sprint 第 4 天 |
| 自动化测试 | Kotlin Test | 端到端 Gateway → HK → biz → Audit | Sprint 第 8 天 |
| 性能基线 | 报告 | P99 < 200ms @ 基准 TPS（R-053 M4 标准） | Sprint 结束前 |
| 缺陷报告 | GitHub Issue | 全部 P0 缺陷关闭 | Sprint 结束前 |

### 5.5 DevOps

| 交付物 | 格式 | 验收标准 | 截止时间 |
|--------|------|---------|---------|
| Schema 迁移脚本 | Flyway SQL | 幂等 + 可回滚 | Sprint 第 5 天 |
| feature_toggle 配置 | application.yml / PG 策略表 | 灰度开关可独立控制 | Sprint 第 5 天 |
| 监控面板 | Grafana dashboard | 能力包专属指标（请求量/延迟/错误率/审计量） | Sprint 第 8 天 |
| Outbox 事件表监控 | Grafana alert | 未发布事件 > 阈值告警 | Sprint 第 8 天 |
| 上线 SOP | Markdown | 发布步骤 + 回滚方案 + 验证清单 | Sprint 结束前 |

---

## 6. CI 门禁检查清单

> 8 道 CI 门禁（TECH-STACK-SPEC v3 §10）必须全部通过。

| # | 门禁 | 检查内容 | 对应约束 |
|---|------|---------|---------|
| 1 | `check-domain-isolation.sh` | domain/ 层零 Spring import | P0-1 |
| 2 | `check-no-implicit-spring.sh` | domain/ 无 @Component/@Service/@Autowired | P0-0 |
| 3 | `check-jpa-isolation.sh` | domain/ 零 jakarta.persistence import | DD-ORM |
| 4 | `check-reason-codes.sh` | reason_code 零硬编码 | P0-4 |
| 5 | `gate-circular-dep.sh` | 无循环依赖 | P0-2 |
| 6 | `gate-deny-check.sh` | deny 路径审计覆盖 | P0-5 |
| 7 | `gate-spring-isolation.sh` | Spring 隔离综合检查 | P0-0 |
| 8 | `validate-contracts.sh` | 契约一致性 | P0-3 |

**新能力包首次提交前自查**：

- [ ] `./gradlew build` 全量编译通过（含新模块）
- [ ] 8 道 CI 脚本本地全部 green
- [ ] reason_codes.csv 新增行已 merge 到 hl-contracts main
- [ ] capabilities.yaml 已注册新能力包路由
- [ ] feature_toggle 默认值 = false（灰度控制）

---

## 7. 启动检查清单（Kickoff Checklist）

> 能力包正式开工前，以下各项必须全部 ✅。

### 7.1 裁决就绪

- [ ] 能力包 ID（`biz.{module}`）已在 R-053 S2/S4 裁决中确认
- [ ] 优先级批次已锁定（创始人裁决）
- [ ] 与其他能力包的边界无重叠（PM 联合确认）

### 7.2 契约就绪

- [ ] reason_codes.csv 新增行 PR 已 merge
- [ ] OpenAPI YAML 初稿已提交 hl-contracts
- [ ] capabilities.yaml 路由已注册
- [ ] PRD 文档集（MVP + Facts + Decision-Trace）已提交

### 7.3 代码就绪

- [ ] `contract/` 层接口定义已 merge（Pure Kotlin）
- [ ] `kernel/biz-{module}/` 模块骨架已创建
- [ ] `build.gradle.kts` 依赖仅包含 `:contract` + Spring adapter
- [ ] `settings.gradle.kts` 已 include 新模块

### 7.4 基础设施就绪

- [ ] PG18 schema `biz_{module}` 已创建（开发环境）
- [ ] RLS policy 已配置
- [ ] feature_toggle `biz_{module}_enabled = false` 已配置
- [ ] Grafana dashboard 模板已创建

### 7.5 团队就绪

- [ ] PM、后端、前端、QA、DevOps Owner 已指定
- [ ] Sprint 周期已确定（开始/结束日期）
- [ ] GitHub Issue 已创建（task-assign 模板）
- [ ] Kickoff 会议已完成（各角色确认交付物与时间线）

---

## 8. Phase 0 约束速查

> 以下技术在 Phase 0 **不可使用**（TECH-STACK-SPEC v3 §7 + 桥梁层递减 D10）。

| 禁用项 | 替代方案 | 引入条件 |
|--------|---------|---------|
| gRPC | Java 内部接口 | 能力包独立部署时 |
| RocketMQ / Kafka | Spring Events + Modulith Outbox | 跨进程异步需求 |
| Nacos | PG 策略表 + application.yml + env | 多服务部署时 |
| Keycloak | Spring Security 内建 JWT（DD-AUTH） | 联邦登录需求 |
| Caffeine / Redis | 无缓存（DD-CACHE） | 出现可测量性能瓶颈 |
| 微服务拆分 | 单 JVM Modulith | 多团队独立发布 |
| @Transactional | TransactionTemplate（P0-0 显式） | — |
| @ComponentScan | @Configuration + @Bean（P0-0 显式） | — |
| @EventListener | DomainEventPublisher（P0-0 显式） | — |

---

## 9. 裁决引用索引

| 裁决 | 状态 | 与本模板的关系 |
|------|------|--------------|
| R-003 | LOCKED | 网络拓扑世界模型——定义 TenantSpace 节点和 Claim/Cooperate 关系 |
| R-019 | LOCKED | 能力包去品牌化命名（`biz.*` 前缀） |
| R-035 | LOCKED | 两区数据模型——能力包用 PG18，无 MySQL |
| R-045 | LOCKED | 全新构建——无旧系统适配 |
| R-051 | LOCKED | 四阶段演进——Phase 1 首批能力包从零构建 |
| R-053 | LOCKED | 执行计划——S3 demo + S4 首批 3-5 包 |
| R-054 | LOCKED | 技术选型评估——Phase 0 不预置 MQ/Cache/Nacos |
| R-055 | LOCKED | HK 服务化开放——Phase 0-2 仅 internal API |
| DD-ORM | LOCKED | JPA 隔离——domain Entity ≠ JpaEntity |
| DD-AUTH | LOCKED | Phase 0 Spring Security JWT |
| DD-CACHE | LOCKED | Phase 0 无缓存框架 |

---

## 10. 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-17 | v1.0 | 初始版本，基于 SAAC-HL v1.1 + TECH-STACK-SPEC v3 + R-053 创建 |
