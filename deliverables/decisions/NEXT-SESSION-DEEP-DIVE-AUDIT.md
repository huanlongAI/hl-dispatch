# 新会话续作指令 · 深入专题页审计

> 把下方"新会话首条消息"整段贴到新会话里。不需要解释、不需要问我、就按这段执行。

---

## 新会话首条消息（整段复制 ↓ ）

```
启动新审计线：hl-docs 站点的"深入专题"页 vs SAAC 推导链一致性审计。

【背景，不用问我】
唤龙平台治理已完成三轮对齐：
- 2026-04-14 tech-selection 线结项（见 decisions/AUDIT-HL-DOCS-TECH-SELECTION-vs-SAAC-2026-04-14.md §6 结项记录）
- tech-selection.html 已升到 v1.2.0，与 GREENFIELD 36 T-项一一对齐
- J-04 Flyway 已入锁（DD-DB-MIGRATION-FLYWAY）；J-05 / J-06 / J-07 新议题在 §8 留痕
- 剩余上游动作：hl-contracts 回填（见 HANDOFF-HL-CONTRACTS-FLYWAY-LOCKIN-2026-04-14.md），非阻塞

本轮新任务：把同样的审计方法论应用到 hl-docs 的"深入专题页"上，对齐 SAAC / EP / TEAM-COLLAB-SPEC v2.1 / 已锁 DD。

【审计范围】
pages/workflow-states.html        12 状态机详解
pages/gate-levels.html            L1-L4 门禁详解
pages/power-separation.html       四权分离详解
pages/delivery-steps.html         五步交付流详解
pages/governance-docs.html        治理文档体系详解
pages/qa-process.html             测试流程与分工详解
pages/repo-directory.html         六仓库架构详解

不审范围：tech-selection.html（已结项）· index.html / global.html / 角色导览页（上一轮已顺带对齐）。

【真源链 · 只用这条】
1. SAAC-HL-001 v1.1（宪法层）
2. SAAC-HL-EP-001 v1.1（Phase 0 执行层 · P0-0~P0-6 · D1-D10）
3. TEAM-COLLAB-SPEC v2.1 Pilot-Locked 2026-04-11
4. TECH-STACK-SPEC v3 / DD-ORM / DD-AUTH / DD-TEST v1.2 / DD-CACHE / DD-DB-MIGRATION-FLYWAY
5. TOOLCHAIN-GUIDE v1 · WORKFLOW-GUIDE v1 · PRD-REDEFINITION-SPEC v2.0
6. RULINGS（H-002 ORM · H-006 Gradle · R-016 Apple 原生化 · R-021 OTel · R-025 GHA · 其他）
7. DECISION-2026-03-13-GREENFIELD-TECH-OPS-AUDIT（36 T-项 + O-项）

【严格排除】
- 2026-03 期过渡裁决（R-034 / R-056 / R-058 / R-059 / R-060 / WS-C / 核心组 7 人 / 不设 QA / 不设设计）
- 飞书公告（不在本次证据链）
- hl-contracts 仓内部（只关站点）

【审计方法论 · 沿用上一轮 §6.6】
1. 新覆盖旧：飞书 > v2.1 Pilot-Locked > TECH-STACK-SPEC v3 > RULINGS > EP > SAAC
2. 范围严格收束：本轮只审上述 7 个深入专题页，不扩散
3. 发现隐式共识即留痕：像 Flyway 那样"事实在用但无 Ruling"的条目，先降级 DRAFT/PENDING 开议题
4. F 清单精确到行号：冲突必须对应到具体文件 + 行号
5. 连带发现允许就地处置

【交付物】
1. decisions/AUDIT-HL-DOCS-DEEP-DIVE-vs-SAAC-{今日日期}.md
   - 参照 decisions/AUDIT-HL-DOCS-TECH-SELECTION-vs-SAAC-2026-04-14.md 结构
   - R/Y/J 清单 + F-01~F-N 修正动作 + 待创始人裁决项
2. 每页的具体修正 PR（在 hl-docs 仓 gh-pages 分支）
3. 如果发现新的隐式锁（类似 J-04 Flyway），开 J-08 / J-09 ... 议题，在 tech-selection.html §8 留痕
4. 结项时在审计报告末尾加 §6 结项记录 + tech-selection.html 变更日志同步追加 iter-entry（但 tech-selection 本身不改版本号，因本轮不是 tech-selection 范畴）

【工作顺序】
Phase 1 · 读取授权：先读 authority_chain 里存在于 decisions/ 的全部文件，再读 7 个深入专题页
Phase 2 · 生成审计报告（R/Y/J 清单 + F 清单），提交创始人审阅
Phase 3 · 收到"同意，实施"后一次性完成所有 F 清单修正 + commit + 报告 §6 结项
Phase 4 · 交接未闭环议题（若有）给下一轮

【启动动作】
先读以下文件（按顺序）：
1. decisions/INDEX.md
2. decisions/AUDIT-HL-DOCS-TECH-SELECTION-vs-SAAC-2026-04-14.md（看 §6 方法论）
3. decisions/DECISION-2026-03-13-GREENFIELD-TECH-OPS-AUDIT.md
4. decisions/TEAM-COLLABORATION-SPEC-v2.1.md
5. decisions/TOOLCHAIN-GUIDE-v1.md
6. decisions/WORKFLOW-GUIDE-v1.md
7. decisions/PRD-REDEFINITION-SPEC.md
8. Workspace/hl-docs/pages/workflow-states.html
9. Workspace/hl-docs/pages/gate-levels.html
10. Workspace/hl-docs/pages/power-separation.html
11. Workspace/hl-docs/pages/delivery-steps.html
12. Workspace/hl-docs/pages/governance-docs.html
13. Workspace/hl-docs/pages/qa-process.html
14. Workspace/hl-docs/pages/repo-directory.html

读完后直接起草审计报告（R/Y/J + F 清单），不要先问我要不要开始——我已经授权开始审计了。报告出来后我会看，然后说"同意，实施"或提出修改。

【禁止】
- 不要推到远端 git（沙箱代理拦截；我本地 push）
- 不要修改 decisions/ 里已归档文件
- 不要重开已结项的 tech-selection 审计
- 不要扩范围到 index.html / 角色导览页
- 不要污染本次审计（严格排除清单见上）
```

---

## 副本保管

本指令副本已落盘到：`decisions/NEXT-SESSION-DEEP-DIVE-AUDIT.md`。

新会话开始后删掉这份指令文件（或标 🗄️ ARCHIVED 保留）都可以。
