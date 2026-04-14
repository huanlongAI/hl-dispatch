# 新会话首条消息 · Flyway 锁回填 hl-contracts

> 整段复制到新会话。开始前先在新会话里把 `hl-contracts` 本地克隆目录挂给 Cowork（"添加文件夹"），然后粘贴这段。

---

## 新会话首条消息（整段复制 ↓ ）

```
任务：把 Flyway 正式锁回填到 hl-contracts 仓的 TECH-STACK-SPEC v3 和 RULINGS 两个文件。

【背景，不用问我】
2026-04-14 创始人裁决"同意入锁"，归档 DD-DB-MIGRATION-FLYWAY（见前次会话）。
站点侧已全部对齐（hl-docs tech-selection.html v1.2.0 · commit 051c4fd + 后续）。
剩下唯一动作：在 hl-contracts 真源层补两处条目。本次就做这件事。

【前提】
你应当能看到 hl-contracts 的本地克隆目录（我已经把它挂上来了）。
如果看不到，告诉我——我重挂。

【权威来源】
本次要写入的两段内容完全来自已归档的 DD-DB-MIGRATION-FLYWAY（2026-04-14 LOCKED），
不需要新的推演，直接照搬。

【动作顺序】

1. 先读 hl-contracts 仓的目录结构，定位这两个文件（命名可能有差异）：
   a. TECH-STACK-SPEC：文件名形如 TECH-STACK-SPEC*.md / tech-stack-spec*.md，
      通常在 governance/ 或 specs/ 下
   b. RULINGS：文件名形如 RULINGS.md / rulings.md

2. 读 TECH-STACK-SPEC v3 的 Lock-in Table（数据层分区），
   定位 PostgreSQL 18 / Spring Data JPA 行所在位置。

3. 在该位置紧跟一行新增 Flyway（照搬下表，按 Spec 既有表格格式调整）：

   | 组件 | 版本 | 用途 | 来源裁决 |
   |---|---|---|---|
   | **Flyway** | 10.x LTS | 数据库 Schema 治理唯一方案（Phase 0 起） | DD-DB-MIGRATION-FLYWAY · 2026-04-14 |

   同时在 Spec 的相关章节（执行细则 / §数据层 / §9 等）补一段：

   > Phase 0 起 DB Schema 治理由 Flyway 独占承担。所有 DDL / Schema / 初始化
   > 变更走 Flyway Migration PR；生产由 GitHub Actions 执行 flyway migrate；
   > `ddl-auto=validate`（禁 update/create）；L2 门禁加 flyway:validate +
   > Testcontainers 全量迁移回放。

   Spec 版本号 bump（v3 → v3.1 或按仓内命名规则）。

4. 读 RULINGS.md，末尾追加下面的 H-003 条目（照搬）：

   ```markdown
   ## H-003 — Flyway 入锁
   - **日期**：2026-04-14
   - **裁决人**：L0-Founder
   - **状态**：🔒 LOCKED
   - **上游议题**：J-04（tech-selection 图谱）· GREENFIELD T-05（2026-03-13）
   - **结论**：Flyway 10.x LTS 成为 Phase 0 起 DB Schema 治理唯一方案；
     L2 门禁加 flyway:validate + Testcontainers 全量回放
   - **消解的历史反对**：手动维护 · 格式严格 · 启动阻塞
     （在 AI-first 编码 + Testcontainers 先验下全部消解）
   - **详情**：见 decisions/DD-DB-MIGRATION-FLYWAY-2026-04-14.md
   - **相关**：H-002（ORM 锁定 Spring Data JPA + Hibernate 6.5）
   ```

5. 做完之后：
   - git add + git commit 可以做（commit message 参考下方）
   - git push 不要做（沙箱代理被拦，我本地推）

6. 提交 commit 后，告诉我：
   - 改了哪两个文件（完整路径）
   - Spec 新版本号是什么
   - commit hash
   我验证完会自己 push。

【commit message 模板】
docs(tech-stack): lock Flyway 10.x LTS (H-003)

Backfill upstream truth per DD-DB-MIGRATION-FLYWAY (2026-04-14 LOCKED).

- TECH-STACK-SPEC v3.x: add Flyway row to Lock-in Table (data layer section)
- RULINGS.md: append H-003 entry

Related: J-04 resolved · GREENFIELD T-05 closed · hl-docs tech-selection.html v1.2.0

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

【做完后的收尾】
等我确认 push 成功后，请在我上一轮会话里提到的
decisions/HANDOFF-HL-CONTRACTS-FLYWAY-LOCKIN-2026-04-14.md §5
追加一行签名：
- [x] 完成 — 2026-04-14 — L0-Founder — Spec 版本号：v3.x

并在 hl-docs/pages/tech-selection.html §10 变更日志追加一条 v1.2.1 iter-entry：
"真源层回填完成 — H-003 入锁 · TECH-STACK-SPEC v3.x bump · 站点 §3 Flyway 行与 §8 J-04 行的'待回填'小字可删"，
然后帮我把这两处小字删掉，bump 页面徽章和 footer 到 v1.2.1。

【禁止】
- 不要动 hl-contracts 仓的其他文件
- 不要改变 TECH-STACK-SPEC v3 已有的其他锁定条目
- 不要推到远端
- 不要重开 J-04（已 RESOLVED）
- 如果 hl-contracts 结构与预期差异很大（例如 Lock-in Table 不是表格形式），
  先把差异告诉我再动手
```

---

## 副本保管

本指令已落盘 `decisions/NEXT-SESSION-FLYWAY-BACKFILL.md`，执行完可标 🗄️ ARCHIVED。
