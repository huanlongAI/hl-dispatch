# hl-contracts 回填交接单 — Flyway 入锁

**交接类型**：上游真源回填（site / decisions 已完成，hl-contracts 待同步）
**日期**：2026-04-14
**源裁决**：`decisions/DD-DB-MIGRATION-FLYWAY-2026-04-14.md`（创始人 🔒 LOCKED）
**目标仓库**：`hl-contracts`
**执行人**：架构师（Gate-H 守护者）
**优先级**：中 —— 站点已对齐，补齐真源层避免长期漂移即可；非 Phase 0 阻塞项

---

## 一、为什么需要这张交接单

创始人于 2026-04-14 裁决 Flyway 入锁，DD 文档已落 `decisions/DD-DB-MIGRATION-FLYWAY-2026-04-14.md`，唤龙 hl-docs 站点已回填 v1.0.2。但 **真源层（hl-contracts）** 还有两处未更新：

1. `TECH-STACK-SPEC v3 Lock-in Table` 缺 Flyway 独立行
2. `RULINGS` 缺一条引用

此交接单列出精确的文本片段，架构师照搬即可。

---

## 二、待回填动作

### 2.1 TECH-STACK-SPEC v3 Lock-in Table 新增行

在 v3 Lock-in Table 的数据层分区中，紧跟 PostgreSQL 18 / Spring Data JPA 行之后插入：

| 组件 | 版本 | 用途 | 来源裁决 |
|---|---|---|---|
| **Flyway** | 10.x LTS | 数据库 Schema 治理唯一方案（Phase 0 起） | DD-DB-MIGRATION-FLYWAY · 2026-04-14 |

同时在 Spec 的执行细则章节补入一段（可直接复用 DD §四"执行细则"的 4.1–4.5 四小节原文）。

**动作**：bump TECH-STACK-SPEC 次要版本号（v3 → v3.x）。

### 2.2 RULINGS.md 新增条目

依据 hl-contracts 仓 RULINGS 的既有命名规则二选一：

**方案 A**（沿用 DD 编号）：

```markdown
## DD-DB-MIGRATION-FLYWAY — Flyway 入锁
- **日期**：2026-04-14
- **裁决人**：L0-Founder
- **状态**：🔒 LOCKED
- **结论**：Flyway 10.x LTS 成为 Phase 0 起 DB Schema 治理唯一方案；ddl-auto=validate 生产禁 update/create；L2 门禁加 flyway:validate + Testcontainers 全量回放
- **结项**：GREENFIELD-TECH-OPS-AUDIT T-05 ✅
- **详情**：见 decisions/DD-DB-MIGRATION-FLYWAY-2026-04-14.md
```

**方案 B**（新编 H 序列 Ruling ID，推荐）：

```markdown
## H-003 — Flyway 入锁
- **日期**：2026-04-14
- **裁决人**：L0-Founder
- **状态**：🔒 LOCKED
- **上游议题**：J-04（tech-selection 图谱）· GREENFIELD T-05（2026-03-13）
- **结论**：Flyway 10.x LTS 成为 Phase 0 起 DB Schema 治理唯一方案；L2 门禁加 flyway:validate + Testcontainers 全量回放
- **消解的历史反对**：手动维护 · 格式严格 · 启动阻塞（在 AI-first 编码 + Testcontainers 先验下全部消解）
- **详情**：见 decisions/DD-DB-MIGRATION-FLYWAY-2026-04-14.md
- **相关**：H-002（ORM 锁定 Spring Data JPA + Hibernate 6.5）
```

**推荐方案 B** —— 与现有 H-002（ORM 锁定）序列对齐，便于按议题检索。

---

## 三、回填完成后的收尾

1. 在此交接单末尾追加一行完成签名：`✅ 完成 — {日期} — {架构师 handle} — Spec 版本号：v3.x`
2. `pages/tech-selection.html` §3 Flyway 行的"TECH-STACK-SPEC v3 Lock-in Table 待回填"小字可删
3. `pages/tech-selection.html` §8 J-04 行的"待回填：TECH-STACK-SPEC v3 Lock-in Table + RULINGS 引用"小字可删
4. 在 §10 追加一条 iter-entry：`v1.0.3 真源层回填完成 — H-003 / TECH-STACK-SPEC v3.x`

---

## 四、无风险项

- 代码侧已有多处 `spring.flyway.enabled=true` / `db/migration/` 目录使用；本次回填属制度追认，不触发代码变更。
- 不影响任何 PR merge、部署、验收流程。
- 可与下一次 TECH-STACK-SPEC 常规版本升级合并一次性完成。

---

## 五、完成签名

- [ ] 完成 — 日期 — 架构师 handle — Spec 版本号：_________
- [x] 完成 — 2026-04-14 — L0-Founder — Spec 版本号：v3.1
      - commit: `a5abec0` on hl-contracts `main`（已 push origin）
      - 采用方案 B 变体：H 编号递增为 **H-007**（H-003 仓内已被 Spring EventListener 占用）
      - H-007 嵌入 R-017 下作附属裁决（沿用仓内既有"H 嵌 R"结构，非独立顶级条目）
      - R-017 原 §Flyway 策略（2026-02-22 "首部署 update→导出→validate"）标 SUPERSEDED 保留原文
      - 同步更新：CHANGELOG.md [H-007 Flyway 入锁] / governance/CLAUDE.md 三处摘要
