# 数据库 Schema 治理方案裁决 — Flyway 入锁

**文档编号**：DD-DB-MIGRATION-FLYWAY
**议题编号**：J-04（原 tech-selection 图谱 §8）
**版本**：v1.0（2026-04-14 裁决归档）
**裁决人**：L0-Founder（创始人）
**接收人**：Gate-R（运维）、Gate-H（架构）、Infra-A（后端）、QA、PM
**状态**：🔒 LOCKED — 已裁决，Flyway 进入 TECH-STACK-SPEC v3 Lock-in Table
**关联**：GREENFIELD-TECH-OPS-AUDIT T-05（本裁决为 T-05 结项）· RULINGS H-002（ORM 锁定）

---

## 一、裁决结论

**Phase 0 起唤龙平台数据库 Schema 治理由 Flyway 独占承担。所有 Schema / DDL / 数据初始化变更必须走 Flyway Migration PR，非 Flyway 路径不允许进入生产。**

执行要点：

1. `hl-platform` 每个 Modulith 模块在 `src/main/resources/db/migration/` 下维护本模块的 `V{n}__{desc}.sql`，命名符合 Flyway 规范。
2. 生产环境由 GitHub Actions 在发布阶段自动执行 `flyway migrate`；非 Actions 流程执行迁移视为 L2 红线。
3. CI 在 L2 门禁增加两道检查：<br/>
   (a) **Flyway dry-run / validate** — 在合并 PR 前验证新迁移可加载、checksum 一致；<br/>
   (b) **Testcontainers 全量回放** — 用真实 PG 18 从零跑过全部历史迁移 + 新迁移，覆盖"启动阻塞"历史反对点。
4. ORM 侧（Spring Data JPA + Hibernate 6.5，H-002 LOCKED）`ddl-auto=validate`；生产禁止 `update` / `create`。

---

## 二、裁决背景

### 2.1 真实状态考古

| 来源文件 | 引用方式 | 性质 |
|---|---|---|
| `DECISION-2026-03-13-GREENFIELD-TECH-OPS-AUDIT.md` T-05 | 审查清单第 1 条："PostgreSQL 18 + Flyway：Schema 管理方案是否有坑？" | **未结问题** |
| 同文件 O-03 / 能力具备度表 | 把 Flyway 列入"PG 基础运维 + Flyway 迁移" | 隐含前提 |
| `TEAM-COLLABORATION-SPEC-v1.0.md` Gate R 职责 | "PG18 运维；Docker Compose 开发环境；**Flyway 流水线**" | 职责层提及 |
| 同文件 权限矩阵 | "Flyway 迁移脚本执行（生产）" 入表 | 权限分配 |
| `PM-SPEC-GUIDE006-GAP-ANALYSIS.md` / `PM-BRANCH-LAUNCH-TEMPLATE.md` / `LAUNCH-PRODUCT-CENTER.md` / `PM-PRACTICAL-HANDBOOK-v1.0.md` | Sprint / DDL / 交付模板中直接引用 Flyway | 当默认手段使用 |
| **TECH-STACK-SPEC v3 Lock-in Table** | — | **无 Flyway 独立锁定条目** |
| **RULINGS** | — | **无 Flyway 独立 Ruling** |
| **SAAC / EP v1.1** | — | **无直接表态** |

**结论**：Flyway 事实上被多处当作默认手段使用，但从未经过正式 Ruling 锁定；属于"隐式共识"而非"制度真源"。本裁决补齐此缺失。

### 2.2 历史隐式反对意见（从未归档）

1. **开发需手动维护**：每次 Schema 变更都要手写 `V__xxx.sql`，与直接改 ORM 实体相比多一道工序。
2. **格式严格**：文件命名、版本号连续性、checksum 不匹配都会失败。
3. **错误阻塞服务启动**：迁移失败时 Spring Boot 启动阶段直接抛 `FlywayException`，对不熟悉的开发者是高压事件。

### 2.3 AI-first 编码下反对意见的消解

| 原反对 | AI-first 下的状态 |
|---|---|
| 手动维护 `V__xxx.sql` | AI 依据 JPA 实体差异自动生成迁移脚本，工程师 reviewer 过 gate 即可。成本 ≈ 零。 |
| 格式严格 | AI 直接生成符合 Flyway 规范的文件名与结构；CI 中加 Flyway validate 自动校验。 |
| 启动阻塞 | **L2 门禁在合并前已用 Testcontainers 跑过完整迁移链**，生产启动不可能见到"未测过"的迁移。错误被左移到 PR 阶段。 |

原反对意见在 AI-first 编码 + Testcontainers 先验的复合方案下完全消解。

---

## 三、决定性因素（六因子自评）

| 因子 | 自评 | 理由 |
|---|---|---|
| ① 业务阶段（Phase 0 极简） | ✅ | Flyway 是 Phase 0 范围内唯一需要引入的 Schema 治理组件；相对于手写 SQL 脚本目录，Flyway 本身即是最小化方案。 |
| ② 团队规模（运维 1 人） | ✅ | Flyway 嵌入应用启动流程，无需独立服务。1 人运维可维护。 |
| ③ 契约驱动 | ✅ | `V__xxx.sql` 即 Schema 契约；Migration PR 天然对应 L2 门禁的契约变更评审。 |
| ④ AI-first 编码 | ✅（**本裁决的关键新因素**） | AI 起稿 + CI 校验 + Testcontainers 回放，工程师成本结构发生根本变化。 |
| ⑤ 四环三面 | ✅ | 迁移脚本按模块分目录（`db/migration/{module}/`），与 Spring Modulith 边界一致，不破坏模块边界。 |
| ⑥ 版本锁与供应链 | ✅ | Flyway 10 LTS 成熟稳定；与 Spring Boot 3.5 官方 starter 集成。 |

六因子全绿，无一阻断项。

---

## 四、执行细则

### 4.1 目录约定

```
hl-platform/
├── biz-product/src/main/resources/db/migration/
│   ├── V1__product_base.sql
│   └── V2__product_sku_extend.sql
├── biz-identity/src/main/resources/db/migration/
│   ├── V1__identity_base.sql
│   └── ...
└── starter-data-jpa/
    └── src/main/resources/db/migration/
        └── V1__shared_baseline.sql
```

**命名规范**：`V{递增编号}__{下划线分隔的描述}.sql`；描述全英文小写，不超过 40 字符。Flyway 默认版本比较按整数递增。

### 4.2 CI 门禁（L2 新增两道检查）

| 门禁 | 作用 | 失败即阻塞 |
|---|---|---|
| `flyway:validate` | 校验新迁移 checksum、命名、SQL 可解析 | ✅ PR 合并前 |
| `flyway:testcontainers-replay` | 起 PG 18 容器从零跑 baseline + 全部历史 + 新迁移，同时跑回滚脚本（若存在） | ✅ PR 合并前 |

### 4.3 运行时约定

- `spring.flyway.enabled=true`（所有环境）
- `spring.jpa.hibernate.ddl-auto=validate`（所有环境，含本地）—— **禁止 `update` / `create` / `create-drop`**
- 生产环境 `flyway migrate` 由 GitHub Actions 的发布 job 执行，不随应用启动执行；应用启动仅做 `validate`（双保险，防手工直连）。
- Docker Compose 本地开发允许应用启动时自动 `migrate`（便于新人开箱即用）。

### 4.4 回滚策略

1. **首选**：不回滚，写一条新的 `V{n+1}__revert_{xx}.sql` 前向修复（契约驱动原则——Schema 不倒流）。
2. **应急**：对于非破坏性变更（如新增列、加索引）可以通过 DDL 逆向脚本回滚；破坏性变更（drop / alter type）必须走 DB 备份恢复。
3. `hl-contracts` 仓库维护一份《DB 变更风险分级表》，破坏性变更 PR 必须在 PR 描述中声明风险等级。

### 4.5 例外处理

- 手工 hotfix（绕过 Flyway 直连数据库）**仅限 P0 线上事故**，事后必须补写对应迁移脚本回填 Flyway schema_history 表，由 Gate-R 审批。
- 非事故场景下的手工 DDL 变更视为 L2 红线，PR 退回。

---

## 五、验证与结项

### 5.1 GREENFIELD-TECH-OPS-AUDIT T-05 结项

> T-05 原问题："PostgreSQL 18 + Flyway：Schema 管理方案是否有坑？"

**结项答复**：本 DD 锁定 Flyway 作为唯一方案；CI 加两道门禁（validate + testcontainers replay）消解启动阻塞风险；AI-first 消解手动维护成本。T-05 状态转为 **✅ RESOLVED**。

### 5.2 TECH-STACK-SPEC v3 Lock-in Table 更新动作

- [ ] 在 v3 Lock-in Table 新增一行：**Flyway · 最新 10.x LTS · DD-DB-MIGRATION-FLYWAY**
- [ ] 发布 v3.x bump，更新 hl-contracts 仓库
- [ ] RULINGS 目录下挂一条引用（Ruling ID 可沿用 DD 编号或新编 H-003，视 RULINGS 命名规则）

### 5.3 站点回填动作

- [ ] `pages/tech-selection.html` §3 后端选型表 Flyway 行：⏳ PENDING (J-04) → 🔒 LOCKED，来源列改为"DD-DB-MIGRATION-FLYWAY（2026-04-14）"
- [ ] §8 待决清单 J-04 标 **RESOLVED** 并移入历史
- [ ] §10 变更日志新增 v1.0.2 条目
- [ ] `pages/engineering.html` §tech-stack Flyway 表述改回断言
- [ ] 页面徽章升级到 v1.0.2

---

## 六、变更日志

| 日期 | 版本 | 动作 |
|---|---|---|
| 2026-04-14 | v1.0 | 首次发布。结项 GREENFIELD T-05；锁定 Flyway 为 DB Schema 治理唯一方案。 |
