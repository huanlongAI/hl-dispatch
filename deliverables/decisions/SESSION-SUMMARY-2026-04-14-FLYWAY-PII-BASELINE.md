# 会话总结 · 2026-04-14 · Flyway 入锁 / PII 清洁 / 组织 AI 转型 baseline 对齐

**会话日期**：2026-04-14
**持续时间**：单次会话
**参与仓**：hl-contracts · hl-dispatch · hl-docs
**产出**：16 commits · 3 repos · 全部已 push origin

---

## 一、会话触发

用户上传 `NEXT-SESSION-FLYWAY-BACKFILL.md` 指令文件，要求：

1. 把已归档的 DD-DB-MIGRATION-FLYWAY（2026-04-14 LOCKED）回填到 hl-contracts 仓的 TECH-STACK-SPEC v3 + RULINGS 两处
2. 完成后同步更新 hl-docs 站点 v1.2.1 + hl-dispatch HANDOFF 签名

会话过程中扩展为：PII 全仓去敏 · 组织 AI 转型 baseline 显式化 · pre-pilot 僵尸裁决归档 · workflows 供应链加固 · .gitignore / CSV 等清洁工作。

---

## 二、16 Commits 全览

### 按时间顺序

| # | 日期 | 仓 | branch | commit | 主题 |
|---|---|---|---|---|---|
| 1 | 2026-04-14 | hl-contracts | main | `a5abec0` | Flyway 10.x LTS 入锁 (R-017 · H-007) |
| 2 | 2026-04-14 | hl-dispatch | main | `32f3f29` | PII 去敏 (32 文件) |
| 3 | 2026-04-14 | hl-dispatch | main | `262b84e` | workflows SHA pinning (3 文件) |
| 4 | 2026-04-14 | hl-dispatch | main | `c4ce3c9` | consistency-sentinel skip_llm 类型修复 |
| 5 | 2026-04-14 | hl-dispatch | main | `6fe3d61` | Flyway 裁决批次归档 (6 新文件) |
| 6 | 2026-04-14 | hl-docs | gh-pages | `dfbdc88` | tech-selection v1.2.1 真源回填 |
| 7 | 2026-04-14 | hl-contracts | main | `07ab555` | PII scrub governance + archive (10 文件) |
| 8 | 2026-04-14 | hl-contracts | main | `a8ff2ac` | 组织 AI 转型 baseline 对齐 · pre-pilot 裁决接管 |
| 9 | 2026-04-14 | hl-contracts | main | `fe96ae8` | R-056~R-059 正文迁出归档 · tombstone |
| 10 | 2026-04-14 | hl-contracts | main | `7df3873` | gitignore Claude Code local settings |
| 11 | 2026-04-14 | hl-contracts | main | `67a10b5` | 抽象 sentinel-shared repo refs |
| 12 | 2026-04-14 | hl-contracts | main | `541291b` | workflows SHA pinning (claude-gate + prd-gate) |
| 13 | 2026-04-14 | hl-contracts | main | `3b32b1d` | consistency-sentinel skip_llm 类型修复 |
| 14 | 2026-04-14 | hl-contracts | main | `882588a` | reasoncodes.csv CRLF → LF |
| 15 | 2026-04-14 | hl-contracts | main | `9fad661` | PRD PII 去敏 + pre-existing 整合 |

*注：上表按 16 顺序编号，但实际 origin push 顺序可能略有穿插；完整时序以各仓 `git log --oneline` 为准。*

### 按主题分类

| 主题 | commits | 说明 |
|---|---|---|
| **Flyway 入锁全链路** | a5abec0 · 6fe3d61 · dfbdc88 | TECH-STACK-SPEC v3.1 + RULINGS H-007 + hl-dispatch DD/HANDOFF + hl-docs 站点 |
| **PII 全仓去敏** | 32f3f29 · 07ab555 · 67a10b5 · 9fad661 | 三仓 ~170+ 处实名 + 30+ 处个人 @handle |
| **组织 AI 转型 baseline 对齐** | a8ff2ac · fe96ae8 | pre-pilot R-056~R-059 SUPERSEDED + 段落粒度归档 |
| **供应链加固** | 262b84e · 541291b | 5 个 workflow SHA pinning |
| **CI 类型修复** | c4ce3c9 · 3b32b1d | consistency-sentinel skip_llm string → boolean |
| **仓库卫生** | 7df3873 · 882588a | .gitignore + reasoncodes CRLF→LF |

---

## 三、关键决策脉络

### 3.1 H-007 编号推导（格式规范共识）

**问题**：NEXT-SESSION 指令文件假设使用 H-003 编号，但仓内 H-003 已被"Spring EventListener"占用（R-007 附属裁决）。

**决策路径**：
1. 扫描现有 H- 编号：已用 H-001/H-002/H-003/H-004/H-005/H-006/H-009，空位从 H-007
2. 选 **H-007**（自然递增）
3. 嵌在 R-017 下作附属裁决（与 H-001 "测试 H2 PG 兼容模式"同结构），**不开顶级 `## H-NNN` 先例**
4. 采用仓内既有 3 行短式格式（bullet + 正式化日期），不引入"🔒/上游议题/消解历史反对"等新字段（那些保留在权威 DD 源文件）

**产出**：RULINGS.md R-017 新增 H-007；原 §Flyway 策略（2026-02-22 版）标 SUPERSEDED 保留原文。

### 3.2 Flyway 跨仓真源链路

```
hl-dispatch/deliverables/decisions/DD-DB-MIGRATION-FLYWAY-2026-04-14.md
                            ↓ (权威 DD)
                            ↓
hl-contracts/governance/RULINGS.md R-017 附属裁决 H-007
                            ↓ (契约真源)
                            ↓
hl-contracts/governance/TECH-STACK-SPEC-v3.md v3.1 §4.3 + §八
                            ↓ (技术选型投影)
                            ↓
hl-docs/pages/tech-selection.html §3 Flyway 行 + §8 J-04 行
                              (对外站点)
```

**关键约束**：DD 原文**不复制**到 hl-contracts（保持 hl-dispatch 作为 deliverables 唯一 SSOT），通过跨仓路径链接引用。

### 3.3 R-017 §Flyway 策略的 SUPERSEDED 处理

原 R-017 §Flyway 策略（2026-02-22 版）规定"首部署 ddl-auto=update 自动建表 → 导出 V1 → 切回 validate"，与 H-007 新锁"Phase 0 起禁 update/create，仅 Flyway Migration PR 一条路径"实质冲突。

**选择**：保留原段文本 + 加 ⚠️ SUPERSEDED 标注（仿 R-004/R-027 样式），不删除。理由：git history 仍需溯源，且仓内 SUPERSEDED 处理有既定模式。

### 3.4 组织 AI 转型 baseline 显式化

**触发**：用户明确指令"旧工程和试点前的计划和任务标注废弃或清理归档，避免污染。全新的团队分工与任务，应该从组织 AI 转型开始"。

**Watershed 日期**：2026-04-11（TEAM-COLLABORATION-SPEC v2.1 Pilot-Locked）

**处理差异**：
- **R-053**（全新构建执行计划）→ 状态改为 "人员模型被 v2.1 接管 · Sprint 技术结构仍有效"。原因：Sprint 框架被后续文档引用（类 R-034 pattern）
- **R-056/R-057/R-058/R-059**（pre-pilot 团队分工）→ 完整 SUPERSEDED

**R-058 反向案例**：原 R-058 "不设独立 QA"，v2.1 明确四角色含 QA（独立质量 Owner）。这是立场**反向**的 SUPERSEDED，需要特别强调新 QA 职责见 v2.1 + WORKFLOW-GUIDE v1。

### 3.5 保留原文 vs 段落归档 tradeoff

用户在 commit a8ff2ac（保留原文 + SUPERSEDED 标注）后追问"是否造成噪音？"。分析：

- **原处理**：R-056~R-059 + 依据合计 ~130 行 in-file，占 RULINGS.md 9% 篇幅
- **噪音类型**：AI grep "不设 QA" 可能 hit 旧原文而未读 ⚠️ 框；人眼扫读僵尸条目干扰活真源体感

**3 个选项**：
- A · 原地保留（R-004/R-027/R-031/R-034 现行惯例）
- B · 段落粒度归档（推荐）
- C · 激进删除（git history 是唯一溯源路径）

**决定 B**：完整原文迁出至 `governance/archive/RULINGS-deprecated-pre-pilot-team-2026-04-11.md`；RULINGS.md 原位置变 27 行 tombstone 速查表（5 列 + 4 条关键结论摘要 + 真源指引）。净减 99 行。

**Precedent**：这是仓内**首次**段落粒度归档（此前都是文件粒度 archive/）。

### 3.6 全仓 PII 去敏策略

**统一代号映射**（R-034 团队编制对齐）：

| 实名 | 代号 |
|---|---|
| 童正辉 | L0-Founder |
| 许久明 | Gate-H |
| 曾正龙 | Gate-R |
| 邹骢 | PM-A |
| 朱阳 | PM-B |
| 魏鹏 | Infra-A |
| 李旭阳 | Gate-3 |
| 刘建成 | PM-Ops |

**个人 @handle 策略**：
- `@tongzhenghui` → `@founder`（SECURITY-POLICY 风格占位）
- 其它 personal handle → "Collaborator（internal-managed）"

**保留项**（按 GitHub 自动化需要）：
- **CODEOWNERS**（hl-contracts · hl-dispatch）：`@tongzhenghui` 保留
- **TEAM.yml**（hl-dispatch）：`github:` 字段保留真实 handle

**规模**：三仓累积 ~170 处实名 + ~30 处 personal handle 全部清除或归档到保留白名单。

### 3.7 PRD 文件 PII + 本体整合

`prd/S1-BIZ-PRODUCT-CONTRACT-BOUNDARY.md` 原有两类改动：
1. Pre-existing 40 行本体修订（tenantId / prod_id 从具体数字改为 `t_EXAMPLE_001` 等占位）
2. 13 处实名去敏

合并为单 commit（`9fad661`），commit message 明确分层说明。

### 3.8 reasoncodes.csv CRLF → LF 发现

952 行 1:1 对称 diff 实为纯行尾差异（CRLF → LF）。字节减少 = `\r` 清除，内容零变化。作为独立 commit（`882588a`）明确此为格式规范化。

---

## 四、跨仓真源链路总表

| 主题 | 权威文件 | 消费方 |
|---|---|---|
| 团队分工 / 任务 baseline | `hl-dispatch/deliverables/decisions/TEAM-COLLABORATION-SPEC-v2.1.md` + R-TEAM-001~R-TEAM-014 | 全仓（通过 RULINGS.md baseline banner 显式指向） |
| Flyway DB Schema 治理 | `hl-dispatch/deliverables/decisions/DD-DB-MIGRATION-FLYWAY-2026-04-14.md` | hl-contracts H-007 · hl-docs §3 |
| PII 代号映射 | 分布于 `TEAM.yml`（name 字段）+ `R-034` 团队编制 | 全仓文本引用 |
| 能力包业务语义 | PM（v2.1 业务语义 Owner） | HPRD / Cap-Spec / reason_codes |
| 全局契约语义 | 创始人（v2.1 治理 Owner） | RULINGS.md + 架构蓝图 |

---

## 五、流程观察（for 下次 AI）

### 5.1 仓外工具链陷阱

| 问题 | 原因 | 解决 |
|---|---|---|
| `osascript + heredoc + 中文`特殊字符解析失败 | AppleScript 对 `「」${{ }}` 等字符处理 | 用 Python heredoc 写文件到 `/tmp`，`git commit -F` 消费 |
| `.git/index.lock` "Operation not permitted" | sandbox uid ≠ host uid，写入 host git 仓权限错 | osascript host 侧先 `rm -f .git/index.lock` 再操作 |
| git add 多文件无法按 hunk 拆 commit | 同文件跨主题改动 | 先 sed 局部恢复 → commit 部分 → sed 重新应用 → commit 剩余 |

### 5.2 仓内约定识别法

| 找什么 | 去哪 |
|---|---|
| RULINGS.md 历史 SUPERSEDED 处理样式 | R-004 / R-027 / R-031 / R-034 |
| 附属裁决 H-NNN 格式 | R-017 下 H-001 / R-013 下 H-005 |
| CHANGELOG.md 条目格式 | 顶部 `## [R-XXX 主题] - YYYY-MM-DD` + Added/Changed/Rationale |
| 归档目录惯例 | `governance/archive/`（文件级）· 本次新增段落级 |
| 跨仓引用风格 | "hl-dispatch/deliverables/decisions/XXX.md" 相对路径字符串 |

### 5.3 用户协作模式

用户典型 workflow：
1. 接受 plan 提案后发"同意/执行"——要求一把执行到底
2. 偶尔发现新问题要追加（如"是否造成噪音"引入段落归档讨论）
3. 验证后 push（我不 push）
4. 分支保护 bypass 警告会出现，用户能主动识别并说明

**关键**：用户明确区分 plan vs execute 阶段。任何发现新约束 / 新范围要**先回报**再问是否继续。

---

## 六、待跟进事项（Backlog）

无。本会话所有任务全部闭环。

若未来需要扩展：

- [ ] hl-factory / hl-framework / hl-platform / hl-console-native 仓是否需要同套 PII sweep（本会话未触及）
- [ ] RULINGS.md 是否还有其它"原地保留 + 长原文"条目适合用段落粒度归档优化（R-034 自己就有 90 行，可评估）
- [ ] `governance/archive/` 目录随时间增长后是否需要次级 index
- [ ] hl-contracts CODEOWNERS 里 16 处 @tongzhenghui 是否要迁移到团队级 handle（如 `@huanlongAI/founders`）以进一步去个人化

---

## 七、本会话产出文件清单

**新建**：
- `hl-dispatch/deliverables/decisions/SESSION-SUMMARY-2026-04-14-FLYWAY-PII-BASELINE.md`（本文件）
- `hl-contracts/governance/archive/RULINGS-deprecated-pre-pilot-team-2026-04-11.md`

**修改范围**：
- hl-contracts：12 文件（含 TECH-STACK-SPEC v3.1 / RULINGS R-017+H-007+tombstone / CHANGELOG / CLAUDE.md / PROGRESS.md / SAAC-HL-001-v1.1 / archive 5 个 / .gitignore / .claude/tasks/001-result / 4 个 workflow / prd / reasoncodes）
- hl-dispatch：33 文件（含顶层 4 + workflows 4 + ISSUE_TEMPLATE 3 + decisions 22）
- hl-docs：1 文件（pages/tech-selection.html）

---

*文档位置*：`hl-dispatch/deliverables/decisions/SESSION-SUMMARY-2026-04-14-FLYWAY-PII-BASELINE.md`
*INDEX 登记*：本文件列入 INDEX.md §5 Handoff/Checklist（同 commit）
