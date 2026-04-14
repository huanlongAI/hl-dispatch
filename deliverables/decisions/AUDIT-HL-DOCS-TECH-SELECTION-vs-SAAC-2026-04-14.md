---
id: AUDIT-HL-DOCS-TECH-SELECTION-vs-SAAC-2026-04-14
title: hl-docs 站点技术选型 vs SAAC 推导链——审计报告
scope: ONLY /sessions/bold-fervent-fermi/mnt/Workspace/hl-docs/（站点）
out_of_scope:
  - 飞书公告（本次不看）
  - WS-C / 旧工程 / 3 月过渡裁决（彻底排除，不作为证据）
authority_chain:
  - SAAC-HL-001 v1.1（宪法层）
  - SAAC-HL-EP-001 v1.1（Phase 0 执行层）
  - TECH-STACK-SPEC v3（版本锁定）
  - DD-ORM / DD-AUTH / DD-CACHE / BRIDGE-DERIVATION v1（推导文）
  - RULINGS.md（仅引未被覆盖条目，如 H-002）
  - TEAM-COLLAB-SPEC v2.1 Pilot-Locked（团队结构真源，仅用于理解文档描述对象）
created_at: 2026-04-14
status: closed_with_closure_section
---

# hl-docs 站点技术选型 vs SAAC 推导链——审计报告

## 0. 范围与方法

**范围**：只审 `/sessions/bold-fervent-fermi/mnt/Workspace/hl-docs/` 14 个 HTML 文件的技术选型表述。飞书公告、站点之外的口径、3 月过渡裁决、WS-C / 旧工程相关内容**全部排除**，不作为冲突源也不作为证据。

**方法**：逐文件对照 SAAC → EP → TECH-STACK-SPEC → DD-* 推导链，凡偏离锁定结论或无据引入的即为冲突。红 = 硬冲突必改；黄 = 表述/口径需统一；紫 = 无 SAAC 锁定源，需创始人裁决是否补推导；绿 = 已对齐。

**真源链的优先级（只用这条，不用别的）**：

```
SAAC-HL-001 v1.1
  ↓
SAAC-HL-EP-001 v1.1  （P0-0 ~ P0-6 + D1-D10）
  ↓
TECH-STACK-SPEC v3    （Kotlin 2.1.10 / JVM 21 / Spring Boot 3.5.11 / Spring Modulith 1.3.4 / JUnit 5.10.2 / PG 18.x）
  ↓
DD-ORM / DD-AUTH / DD-CACHE / BRIDGE-DERIVATION v1
  ↓
RULINGS.md（仅引未被 v2.1 覆盖的技术类条目，如 H-002 LOCKED = ORM）
```

---

## 1. 站点范围与文件清单

| # | 文件 | 行数 |
|---|------|-----:|
| 1 | index.html | 693 |
| 2 | pages/delivery-steps.html | 730 |
| 3 | pages/engineering.html | 655 |
| 4 | pages/frontend-design.html | 662 |
| 5 | pages/gate-levels.html | 832 |
| 6 | pages/global.html | 899 |
| 7 | pages/glossary.html | 254 |
| 8 | pages/governance-docs.html | 835 |
| 9 | pages/ops.html | 515 |
| 10 | pages/power-separation.html | 524 |
| 11 | pages/product.html | 460 |
| 12 | pages/qa-process.html | 1045 |
| 13 | pages/qa.html | 593 |
| 14 | pages/repo-directory.html | 721 |

技术选型冲突集中在 **engineering.html / ops.html / frontend-design.html / repo-directory.html** 四页。

---

## 2. 冲突清单（精确到文件 + 行号）

### 2.1 红类（硬冲突，必改）

| 编号 | 位置 | 站点原文（节选） | SAAC 推导链结论 | 判定 |
|------|------|-----------------|-----------------|------|
| **R-01** | `engineering.html:579` | **PostgreSQL 16 + JOOQ** "JOOQ 生成类型安全 DSL" | TECH-STACK-SPEC v3 §3.1 + **RULINGS H-002 LOCKED**：ORM = Spring Data JPA + Hibernate 6.5；PG = **18.x** | JOOQ 违反 H-002；PG 版本误标 |
| **R-02** | `engineering.html:571` | "把 **70%** 常规编码交给 AI" | SAAC §1.3：AI-first 编码（默认 AI 生成，人工可补，统一过 gate）；EP §7.1 仅"AI 生成代码一次通过 CI > 50%"（交付侧指标，非工作量 70%） | "70%" 无据，工程语义错误 |
| **R-03** | `engineering.html:583` | "Claude Code / Codex 强制使用——日常编码的 **70%** 由 AI 产出" | 同上 | "70%" 无据（重复） |
| **R-04** | `ops.html:442` | **Kubernetes (K3s)** "生产编排" | **EP-001 P0-4 LOCKED**：Phase 0 = **ECS 4C8G + Docker Compose**，K8s 属于 Phase 0 不预置清单 | 违反 Phase 0 执行约束 |
| **R-05** | `ops.html:455-456` | "第一周：K3s + Helm 基础……第二周：Terraform + GitHub Actions……" | 同 R-04 | 训练路径以禁用栈为目标，放大 R-04 |
| **R-06** | `ops.html:397` | "用 AI 辅助生成 Terraform/Docker/**K8s** 配置" | 同 R-04 | K8s 引用违反 Phase 0 |
| **R-07** | `frontend-design.html:594` | **Design Tokens (W3C)** 链接 `tr.designtokens.org/format/` | 该规范实际由 **DTCG（Design Tokens Community Group）** 维护，非 W3C。同页 line 561 已正确写 DTCG | 规范组织名错（且一页内自我矛盾） |
| **R-08** | `frontend-design.html:586`<br>`engineering.html:580`<br>`glossary.html:179` | "前端统一 Flutter + Dart（覆盖 Web / Desktop / Mobile 三端）" / "前端统一 Flutter 技术栈" | SAAC §4.1 **C-L1 = SwiftUI + 光合设计系统（GHKit）**（平台控制台）；**C-L2 = Flutter**（租户/消费者端）；R-016 Apple 原生化 LOCKED | 前端被错误单一化为 Flutter；SwiftUI/GHKit 在全站不是一等公民 |
| **R-09** | `frontend-design.html:105` 局部正确<br>但全站未定义 **光合 GHKit** | "hl-console-native……与前端团队无关" 只此一处承认原生端 | SAAC §4.1 要求 C-L1 SwiftUI + 光合 GHKit 是生产级设计系统；应在站点顶层（global / frontend-design / repo-directory）显名 | GHKit 缺位，设计系统真源未显示 |
| **R-10** | `repo-directory.html:531` | "OpenAPI / **gRPC** 契约定义" | EP-001 Phase 0 **不预置 gRPC**（属 D-* 桥梁层，Phase 0 只用 HTTP/REST） | gRPC 违反 Phase 0 不预置清单 |

### 2.2 黄类（表述需统一）

| 编号 | 位置 | 问题 | 修正方向 |
|------|------|------|----------|
| **Y-01** | `frontend-design.html:561 ↔ :594` | 同一页 561 写 "DTCG 标准格式"，594 又写 "Design Tokens (W3C)"——口径冲突 | 全站统一为 **DTCG**；W3C 字样清除 |
| **Y-02** | `ops.html:444` | Terraform 列入 Phase 0 表，但 SAAC / EP 未锁 IaC | 要么删除（Phase 0 最小化），要么创始人补 DD-IaC 推导 |
| **Y-03** | `engineering.html:571/583` | "AI 工具强制使用" 的口径叙述可保留（四权分离下的工具收敛合理），但须剥离"70%"数字 | 改为 "AI-first 编码，默认 AI 生成初稿，工程师作 reviewer，过 gate"（SAAC §1.3 原词） |
| **Y-04** | `frontend-design.html` 全页 | 8 处 "Flutter 三端统一"，零处提及 **C-L1 SwiftUI / GHKit** 作为平台控制台技术栈 | 新增一段"前端分治：C-L1 平台控制台 = SwiftUI + 光合 GHKit；C-L2 租户/消费者端 = Flutter + Dart + DTCG" |
| **Y-05** | `repo-directory.html` | 仓库卡片只列 `hl-app` / `hl-design-system`（Flutter），未突出 `hl-console-native`（SwiftUI） 的对等地位 | 补 hl-console-native + GHKit 仓库卡 |

### 2.3 紫类（无 SAAC 锁定源，待裁决）

| 编号 | 议题 | 选项 |
|------|------|------|
| **J-01** | Terraform 是否作为 Phase 0 IaC 入锁 | (A) 不入锁，从 ops.html 删除 / (B) 创始人签发 DD-IaC 推导后再写入 |
| **J-02** | "AI 工具强制收敛到 Claude Code / Codex / Cursor" 是否写入站点（作为团队工具规范） | (A) 写入并在 engineering.html 引用治理源 / (B) 不写入站点，只留在内部协作文件 |
| **J-03** | Widgetbook / patrol / Riverpod 等二级 Flutter 生态（frontend-design.html / qa.html / repo-directory.html）是否需要 DD-FE 推导背书 | (A) 纳入 DD-FE / (B) 作为非锁定推荐，不承诺 |

### 2.4 绿类（已与 SAAC 链对齐，无需动）

- `engineering.html`：Kotlin + Spring Boot 3 ✅
- `gate-levels.html`：Required Checks / qa-verdict / pm-acceptance ✅
- `governance-docs.html`：治理文档陈述结构 ✅
- `power-separation.html`：四权分离 ✅
- `workflow-states.html`：12 状态机 ✅
- `product.html` / `qa-process.html` 大部分描述（除 R-08 口径） ✅

---

## 3. 修正动作（F 清单）——仅针对站点

| 编号 | 动作 | 文件 | 引据 |
|------|------|------|------|
| **F-01** | `PostgreSQL 16 + JOOQ` → `PostgreSQL 18 + Spring Data JPA / Hibernate 6.5`（含链接替换） | engineering.html:579 | R-01 · H-002 · TECH v3 |
| **F-02** | 删除两处 "70%" 数值，改写为 SAAC §1.3 原词 | engineering.html:571/583 | R-02/R-03 |
| **F-03** | `Kubernetes (K3s) 生产编排` → `ECS 4C8G + Docker Compose（Phase 0）` | ops.html:442 | R-04 · EP P0-4 |
| **F-04** | 运维训练路径第 1/2 周改为 "Docker Compose + Compose Profiles；GitHub Actions + staging 自动化"，K3s 推迟到 Phase 1 评估节点 | ops.html:455-456 | R-05 |
| **F-05** | `Terraform / Docker / K8s` → `Docker Compose / GitHub Actions（Phase 0）`；K8s 字样移除 | ops.html:397 | R-06 |
| **F-06** | `Design Tokens (W3C)` → `Design Tokens (DTCG)`；链接仍可保留 designtokens.org；一页内口径统一 | frontend-design.html:594 · 561 | R-07 · Y-01 |
| **F-07** | `前端统一 Flutter……覆盖三端` 改为 "**C-L1 平台控制台 = SwiftUI + 光合 GHKit**（原生 macOS / iOS 26）；**C-L2 租户/消费者端 = Flutter + Dart + DTCG**"（双栈并行） | frontend-design.html:586 · engineering.html:580 · glossary.html:179 | R-08 · SAAC §4.1 · R-016 |
| **F-08** | 新增"光合 GHKit"为 C-L1 设计系统独立条目（至少在 global.html / frontend-design.html / repo-directory.html 各加一处） | 多处 | R-09 · SAAC §4.1 |
| **F-09** | `OpenAPI/gRPC 契约定义` → `OpenAPI 契约定义（Phase 0，gRPC 不预置）` | repo-directory.html:531 | R-10 · EP Phase 0 |
| **F-10** | Terraform 处置按 J-01 裁决执行：删除 或 补 DD-IaC 后保留 | ops.html:444 · 456 | J-01 |

---

## 4. 待创始人裁决

1. **J-01 ~ J-03**（§2.3）给出方向。
2. **F-01 ~ F-10** 批准 / 否决 / 修正。
3. 批准后 NODE-A 在 hl-docs 仓单一 PR 完成所有文件修改，commit 引用本报告编号。

**未经裁决，NODE-A 不动 hl-docs 任何文件。**

---

## 5. 证据索引（抽样）

- **R-01**：
  - 站点：`hl-docs/pages/engineering.html:579` 列 `PostgreSQL 16 + JOOQ`
  - 真源：`hl-contracts/governance/TECH-STACK-SPEC-v3.md §3.1`；`hl-contracts/governance/RULINGS.md H-002 LOCKED = ORM Spring Data JPA`
- **R-04**：
  - 站点：`hl-docs/pages/ops.html:442` 列 `Kubernetes (K3s)`
  - 真源：`hl-contracts/governance/SAAC-HL-EP-001-v1.1.md §P0-4`"Phase 0 = ECS 4C8G + Docker Compose"
- **R-08**：
  - 站点：`hl-docs/pages/frontend-design.html:586` + `engineering.html:580` 单一化 Flutter
  - 真源：`hl-contracts/governance/SAAC-HL-001-v1.1.md §4.1 C-L1 / C-L2`；R-016 Apple 原生化 LOCKED
- **R-10**：
  - 站点：`hl-docs/pages/repo-directory.html:531` 列 gRPC
  - 真源：`SAAC-HL-EP-001-v1.1.md §Phase 0 不预置清单`

---

*审计完毕。范围严格局限于站点；WS-C / 旧工程 / 飞书公告 / 3 月过渡裁决均已排除。等待创始人裁决。*

---

## 6. 结项记录（Closure · 2026-04-14）

**状态**：🔒 本审计已结项；F-01 ~ F-10 全部执行；额外发现 4 项隐式问题并就地修正。

### 6.1 F 清单执行结果

| 编号 | 状态 | commit | 说明 |
|------|-----|--------|------|
| F-01 | ✅ 完成 | `3f42236` | PG 版本 + ORM 锁定对齐 H-002 |
| F-02 | ✅ 完成 | `3f42236` | "70%" 数值移除，改为 SAAC §1.3 原词"AI-first 编码——默认由 AI 生成初稿，工程师作 reviewer 统一过 gate" |
| F-03 | ✅ 完成 | `3f42236` | K3s → ECS 4C8G + Docker Compose；引 EP P0-4 LOCKED |
| F-04 | ✅ 完成 | `3f42236` | 运维训练路径改为 Compose / GHA / Prom+Graf+Loki / release drill 四周 |
| F-05 | ✅ 完成 | `3f42236` | IaC 生成条目去 K8s 字样 |
| F-06 | ✅ 完成 | `3f42236` | DTCG 归属修正为 Design Tokens Community Group |
| F-07 | ✅ 完成 | `3f42236` | 前端分治落地（C-L1 SwiftUI + GHKit / C-L2 Flutter + Dart + DTCG）多处 |
| F-08 | ✅ 完成 | `3f42236` | GHKit 新增条目于 global.html / frontend-design.html / repo-directory.html / glossary.html |
| F-09 | ✅ 完成 | `3f42236` | gRPC 字样去除，改为 OpenAPI 契约定义（Phase 0 不预置 gRPC） |
| F-10 | ✅ 完成 | `3f42236` | Terraform 行按"Phase 0 最小化 / J-01 待裁决"默认删除；在 tech-selection §8 J-01 留痕 |

### 6.2 额外发现并修正（F 清单之外）

| 发现 | 位置 | 处置 | commit |
|------|------|------|--------|
| `repo-directory.html:191` SVG 标 `Swift · AppKit` | hl-console-native 卡片 | 改为 `Swift · SwiftUI · GHKit` | `3f42236` |
| `repo-directory.html:537` hl-platform 技术栈含 Redis | repoData | 移除 Redis（Phase 0 不预置 Cache） | `3f42236` |
| `qa.html:524` Testcontainers 示例含 Redis | 工具行 | 改为 PG 18 + 注"Phase 0 不预置 Cache/外部 MQ" | `3f42236` |
| 站点缺少深入专题《技术选型》入口 | 全站 | 新增 `pages/tech-selection.html` 技术选型图谱 v1.0 + 15 页 nav 接入 + index 卡片 | `358a2ac` |

### 6.3 延伸议题的归档

本次审计起初只提 J-01/J-02/J-03 三项，执行过程中发现并处置：

| 议题 | 处置 | commit |
|------|------|--------|
| **J-04** Flyway 作为 DB Schema 治理唯一方案 | 先降级 LOCKED→PENDING（`2b2d041`），后创始人裁决"同意入锁"，归档 **DD-DB-MIGRATION-FLYWAY**（2026-04-14），站点 v1.0.2 升回 LOCKED | `e6d8680` + `15f47bf` |
| **J-05** LLM 网关 LiteLLM | Phase 1 OPEN，图谱 §8 留痕 | `051c4fd` |
| **J-06** CDC 工具 Debezium vs DTS | Phase 1 S2 裁决，图谱 §8 留痕 | `051c4fd` |
| **J-07** Phase 2 数据平台栈（OLAP / 湖仓 / 数据目录） | Phase 2 整体评估，图谱 §8 留痕 | `051c4fd` |

### 6.4 站点技术选型图谱的迭代轨迹

```
v1.0    2026-04-14  首次发布（F-01~F-10 修正后的初版）       358a2ac
v1.0.1  2026-04-14  Flyway LOCKED → PENDING (J-04)              2b2d041
v1.0.2  2026-04-14  J-04 RESOLVED — Flyway 正式 LOCKED         e6d8680
v1.1.0  2026-04-14  来源链校准 + 观测/测试栈补录               37a7bab
v1.1.1  2026-04-14  §0 新增"约束层级"三档分级                  5fdd466
v1.2.0  2026-04-14  覆盖补齐 — 对齐 GREENFIELD 36 T-项         051c4fd
```

### 6.5 尚未闭环的上游动作（非阻塞）

交接给架构师（Gate-H 守护者）在 hl-contracts 仓执行，不阻塞 Phase 0 交付：

- [ ] TECH-STACK-SPEC v3 Lock-in Table 新增 Flyway 10.x LTS 行（见 `HANDOFF-HL-CONTRACTS-FLYWAY-LOCKIN-2026-04-14.md`）
- [ ] RULINGS 新增条目（推荐 H-003，与 H-002 序列对齐）
- [ ] 完成后在 tech-selection.html §10 追加 v1.2.1 iter-entry 清理"待回填"小字

### 6.6 审计方法论总结

本轮审计的工作模式，可作为未来治理对齐的模板：

1. **按新覆盖旧读源**：飞书 2026-04-14 > v2.1 Pilot-Locked > TECH-STACK-SPEC v3 > RULINGS > EP > SAAC。3 月过渡裁决整体排除。
2. **范围严格收束**：一次只审一层——本轮只审 hl-docs 站点，飞书公告 / hl-contracts 真源 / WS-C 旧工程均不作为证据。
3. **发现隐式共识即留痕**：像 Flyway 这样"事实在用但无 Ruling"的条目，先降级 DRAFT/PENDING 开议题，由创始人裁决后再入锁。禁止"因为大家都这么用所以就 LOCKED"。
4. **F 清单精确到行号**：审计冲突必须对应到具体文件 + 行号，避免笼统表述。
5. **执行过程中二次发现允许即时处置**：F 清单之外的连带发现（如 AppKit / Redis 残留）无须另起审计，就地改正并记录在 §6.2。

---

*结项完毕。2026-04-14。站点已与审计真源一一对齐；本报告冻结归档，不再更新。后续扩展另起新审计。*
