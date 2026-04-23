# 唤龙治理文档索引 · Decision Record Index

**文档编号**：INDEX
**版本**：v1.0（2026-04-14）
**维护规则**：新增 DD / Ruling / Audit / Handoff / Spec 时必须在本索引登记一行。

> 本索引是决策记录的"图书馆卡片"——不承载内容，仅提供分类、状态、最近更新、快速引用。真源在各自文件；本索引只做检索。

---

## 图例

| 图标 | 含义 |
|---|---|
| 🔒 | LOCKED — 已裁决，变更需创始人审批 |
| ✅ | RESOLVED — 议题已闭环 |
| ⏳ | PENDING — 等待裁决 |
| 📝 | DRAFT — 草案中 / 在用 |
| 🗄️ | ARCHIVED — 历史留痕，已被新版取代 |
| 🧭 | GUIDE — 操作手册 |

---

## 1 · 顶层治理规范（Spec）

| 文件 | 状态 | 说明 |
|---|---|---|
| TEAM-COLLABORATION-SPEC-v2.1.md | 🔒 Pilot-Locked 2026-04-11 | 团队协作规范 v2.1，23 人编制真源。超越 v2.0 / v1.0。 |
| TEAM-COLLABORATION-SPEC-v2.0.md | 🗄️ ARCHIVED | 被 v2.1 取代 |
| TEAM-COLLABORATION-SPEC-v1.0.md | 🗄️ ARCHIVED | 初版团队协作规范，包含 WS-C / 核心组 7 人等过时概念；被 v2.1 全盘取代 |
| WORKFLOW-GUIDE-v1.md | 🧭 GUIDE | 五步交付流操作手册 |
| TOOLCHAIN-GUIDE-v1.md | 🧭 GUIDE | 工具链指南 · 三档分级（治理锁定 / 推荐 / 自选） |
| PRD-REDEFINITION-SPEC.md | 🔒 v2.0 | HPRD / Cap-Spec 重定义规范 |
| TEAM-IDENTITY-MAP.md | 🧭 | 团队身份映射（handle / 岗位 / 职责） |

## 2 · Design Decisions（DD）

| 文件 | 状态 | 议题 ID | 说明 |
|---|---|---|---|
| DD-DB-MIGRATION-FLYWAY-2026-04-14.md | 🔒 LOCKED 2026-04-14 | J-04 | Flyway 10.x LTS 为 Phase 0 起 DB Schema 治理唯一方案。结项 GREENFIELD T-05。 |
| DD-FE-CLIENT-v1.md | 🔒 LOCKED 2026-04-20 | J-A2 | 场景前端 App（`huanlongAI/hl-scene-app`）技术决策派生（Flutter 3.41 / Dart 3.x / 13 字段 + 性能 SLO + 依赖审计约束）· 承接 R-FE-CLIENT-001 LOCKED + amend-001（`hl-contracts/governance/RULINGS.md`）|

*（注：DD-ORM / DD-AUTH / DD-CACHE / DD-TEST v1.2 / BRIDGE-DERIVATION v1 等上游 DD 原则上存于 hl-contracts 仓，本目录仅收录本地产出的 DD）*

## 3 · 重大决策（Decision）

| 文件 | 状态 | 说明 |
|---|---|---|
| DECISION-2026-03-13-GREENFIELD-TECH-OPS-AUDIT.md | 🔒 (T-01~T-36) | Phase 0 绿地技术 + 运维审计 · 36 个 T-项的主锁定文件 |
| DECISION-DATA-ISOLATION-STRATEGY.md | 🔒 v2.0 | Phase 1 X-C 混合方案（映射区迁移 + 能力包保持 MySQL） |
| DECISION-GRAYSCALE-STRATEGY.md | 🔒 | 灰度策略 |

## 4 · 审计报告（Audit）

| 文件 | 状态 | 说明 |
|---|---|---|
| AUDIT-HL-DOCS-TECH-SELECTION-vs-SAAC-2026-04-14.md | ✅ CLOSED 2026-04-14 | hl-docs 站点 vs SAAC 技术选型审计 · F-01~F-10 + 延伸 J-04~J-07 · §6 结项记录 |
| AUDIT-TEAM-COLLABORATION-SPEC-2026-03-17.md | 🗄️ | v2.0 团队协作规范审计（已被 v2.1 超越） |
| AUDIT-TECH-SELECTION-SAAC-CONTAMINATION-2026-03-17.md | 🗄️ | 3 月技术选型污染审计（旧） |

## 5 · 交接单 / 清单 / 会话总结（Handoff / Checklist / Session Summary）

| 文件 | 状态 | 说明 |
|---|---|---|
| SESSION-SUMMARY-2026-04-14-FLYWAY-PII-BASELINE.md | ✅ CLOSED 2026-04-14 | 2026-04-14 单次会话产出 16 commits 跨 3 仓：Flyway 入锁 / PII 全仓去敏 / 组织 AI 转型 baseline 对齐 / pre-pilot 僵尸裁决段落归档 / 供应链加固。关键决策脉络 · 跨仓真源链路 · 流程观察 for 下次 AI。 |
| HANDOFF-HL-CONTRACTS-FLYWAY-LOCKIN-2026-04-14.md | ✅ 已完成 2026-04-14 | 把 Flyway 锁回填到 hl-contracts 仓（TECH-STACK-SPEC v3.1 + RULINGS R-017 H-007，commit a5abec0）§5 签名完成 |
| FEISHU-GITHUB-LAUNCH-CHECKLIST.md | 🧭 | 飞书 / GitHub 联动启动清单 |
| PHASE-F0-FEISHU-SETUP-CHECKLIST.md | 🧭 | Phase F0 飞书设置清单 |
| FEISHU-GITHUB-COLLABORATION-SPEC-v1.0.md | 🧭 | 飞书 × GitHub 协作规范 |

## 6 · PM 手册 / 模板

| 文件 | 状态 | 说明 |
|---|---|---|
| PM-ONBOARDING-GUIDE-v1.1.md | 🧭 | PM 入职指南 |
| PM-PRACTICAL-HANDBOOK-v1.0.md | 🧭 | PM 实操手册 |
| PM-BRANCH-LAUNCH-TEMPLATE.md | 🧭 | 能力包分支启动模板 |
| PM-SPEC-GUIDE006-GAP-ANALYSIS.md | 🧭 | 规范指南 006 Gap 分析 |
| PM-AI-COLLABORATION-ONBOARDING-SPEC.md | 🧭 | PM × AI 协作入职规范 |
| PM-CLAUDE-MD-TEMPLATE-ZHUYANG.md | 🧭 | PM-B 的 CLAUDE.md 模板 |
| PM-CLAUDE-MD-TEMPLATE-ZOUCONG.md | 🧭 | PM-A 的 CLAUDE.md 模板 |
| LAUNCH-PRODUCT-CENTER.md | 🧭 | 产品中心启动文档 |

## 7 · 回复与咨询（Reply / Inquiry）

| 文件 | 状态 | 说明 |
|---|---|---|
| REPLY-PM-ZOUCONG-R061.md | 🗄️ | 回复 PM-A R-061 |
| REPLY-PM-ZOUCONG-R062.md | 🗄️ | 回复 PM-A R-062 |
| REPLY-PM-ZOUCONG-SKU-VERSIONING.md | 🗄️ | 回复 PM-A SKU Versioning |
| INQUIRY-DATA-SYNC-STRATEGY.md | 🗄️ | 数据同步策略咨询（已被 DECISION-DATA-ISOLATION-STRATEGY v2.0 取代） |

## 8 · 本索引（自引）

| 文件 | 状态 | 说明 |
|---|---|---|
| INDEX.md | 🧭 v1.0 | 本文件。新增任何 DD / Ruling / Audit / Handoff / Spec 时在对应分类追加一行。 |

---

## 附录 · 图谱外议题（Pending Rulings 速查）

来源：`../Workspace/hl-docs/pages/tech-selection.html §8`

| ID | 议题 | 当前状态 | 下一步 |
|----|------|--------|------|
| J-01 | Terraform 是否入锁 | ⏳ Phase 0 最小化（已删） | 创始人裁决，补 DD-IaC（可选） |
| J-02 | AI 三件套（Claude Code / Codex / Cursor）强制 vs 推荐 | ⏳ 站点表述为 "AI-first" | TOOLCHAIN-GUIDE v2 |
| J-03 | Widgetbook / patrol / Riverpod 是否锁为 C-L2 标配 | ⏳ DRAFT 推荐 | DD-FE 补锁 |
| J-04 | Flyway 作为 DB Schema 治理唯一方案 | ✅ LOCKED 2026-04-14 | — |
| J-05 | LLM 网关 LiteLLM 入锁 | ⏳ OPEN / Phase 1 | Phase 1 首批能力包验证后 |
| J-06 | CDC 工具 Debezium vs 阿里云 DTS | ⏳ Phase 1 S2 裁决 | S2 选型评估 |
| J-07 | Phase 2 数据平台栈（OLAP / 湖仓 / 数据目录） | ⏳ Phase 2 整体评估 | Phase 2 统一裁决 |

---

## 维护约定

1. **新增文件**：作者在 PR 中同时更新本索引对应分类。
2. **状态变更**：每次状态跃迁（PENDING→LOCKED / DRAFT→ARCHIVED 等）更新本索引。
3. **版本升级**：如 TEAM-COLLAB-SPEC v2.1 → v2.2 时，旧版标 🗄️ ARCHIVED，新版独立一行。
4. **删除禁止**：文件不删除，只标 🗄️ ARCHIVED。
5. **索引版本**：本索引每次结构性修改 bump minor；纯增行不 bump。

*v1.0 · 2026-04-14 · 初版*
