---
id: AUDIT-QA-TEAM-WORKFLOW-REMEDIATION-2026-05-06
title: 测试团队技术选型、分工指南与工作流修订清单
scope:
  - https://huanlongai.github.io/hl-dispatch/pages/global.html
  - hl-dispatch-gh-pages/pages/qa.html
  - hl-dispatch-gh-pages/pages/qa-process.html
  - hl-dispatch-gh-pages/pages/gate-levels.html
  - hl-dispatch-gh-pages/pages/tech-selection.html
status: local_verified_pending_publish
created_at: 2026-05-06
owner: NODE-A / air-codex-cto
authority_chain:
  - TEAM-COLLABORATION-SPEC-v2.1
  - DD-TEST v1.2
  - TOOLCHAIN-GUIDE v1
  - hl-factory/specs/verification-gates.md v0.2
  - TECH-STACK-SPEC v3.3
---

# 测试团队技术选型、分工指南与工作流修订清单

## 0. 结论

测试团队页面与全局工作流存在硬冲突，主要集中在：

- `acceptance-manifest.yaml` schema 在多页被写成三种不兼容格式。
- G-026 的含义被错误写成 `covered` 比例 / JaCoCo 覆盖率，而真源是 manifest-based L2 确定性校验。
- JUnit 5 / Kotest 的主从关系写反。
- `qa-verdict` 的出具主体在“QA 团队成员”“李云峰 QA Owner”“旧 TEAM.yml 的 LUXBYA / Gate-3”之间漂移。
- 站点采用 2026-04-11 后的新组织模型，但 `team-memory` 仍保留 2026-04-03 旧指南，未标注 superseded。

本清单按 P0/P1/P2 排序，只定义修订动作，不直接替代上游真源。

---

## P0 必修：会阻断自动化或误导 QA 执行

| ID | 问题 | 证据 | 真源 | 修订动作 | 验证方式 |
|---|---|---|---|---|---|
| P0-01 | `acceptance-manifest.yaml` schema 三套并存 | `qa.html` 使用 `capability/version/scenarios/id/status/test_class/cap_spec_ref`；`qa-process.html` 使用 `capability_id/version/scenarios/title/steps/expected/test_class/status` | `DD-TEST v1.2` 定义 `manifest_version/capability_id/cap_spec_version/cases/caseId/mode/gate/testClass/testMethod/status` | 统一 `qa.html` 和 `qa-process.html` 示例、字段表、FAQ，全部改为 DD-TEST schema；删除 `scenario` 旧词，统一为 `cases` | `rg -n "scenarios:|test_class|not_applicable|deferred|cap_spec_ref" hl-dispatch-gh-pages/pages/qa*.html` 不再命中旧 schema |
| P0-02 | G-026 被写成覆盖率比例和 JaCoCo 数字 | `qa.html` 写 `covered 占比必须达到 60%`，工具表写 `G-026 门禁直接读 JaCoCo + Codecov 数字` | `DD-TEST v1.2`：G-026 对比 Cap-Spec-2 Case-ID 与 `acceptance-manifest.yaml`，校验 `mode != UI_MANUAL` 的 case 为 `COVERED` 且 `testClass` 非空；`verification-gates.md` 同口径 | 删除 `60% Pilot 阈值`、`80%`、`JaCoCo/Codecov 供 G-026 读取`；G-026 文案统一为 manifest-based L2 YAML 解析 | `rg -n "60%|80%|JaCoCo.*G-026|Codecov.*G-026|covered 占比" hl-dispatch-gh-pages/pages` 不再命中 |
| P0-03 | `status` 枚举漂移 | `qa.html` 用 `covered/pending/not_applicable`；`qa-process.html` 用 `covered/deferred/not-applicable` | `DD-TEST v1.2` 用 `COVERED/PENDING/EXCLUDED`，UI 人工场景示例用 `UAT_MILESTONE` | 页面示例必须使用大写枚举；`UI_MANUAL` 的人工验收状态单独说明，不纳入 PR 门禁 | `rg -n "covered|pending|deferred|not-applicable|not_applicable" hl-dispatch-gh-pages/pages/qa*.html` 不再命中枚举正文 |
| P0-04 | JUnit 5 / Kotest 主从关系写反 | `qa.html` 写 Kotest 是单元/集成框架，JUnit 5 是兼容层 | `DD-TEST v1.2`：JUnit 5.10.2 是唯一主测试框架，Kotest Property 5.9.1 是属性测试补充库；禁止新增 FunSpec/StringSpec | `qa.html` 技术选型表改为 `JUnit 5 = 主测试框架 + 推荐 runner`，`Kotest Property = 属性测试补充库`；不得推荐 Kotest DSL 作为常规测试风格 | `rg -n "Kotest.*单元/集成|JUnit 5.*兼容层|DSL 风格易读" hl-dispatch-gh-pages/pages/qa.html` 不再命中 |

---

## P1 高优先：会造成分工、按钮权和工作流漂移

| ID | 问题 | 证据 | 真源 | 修订动作 | 验证方式 |
|---|---|---|---|---|---|
| P1-01 | `qa-verdict` 出具主体不一致 | `qa.html` 写 QA 团队成员 approve 即 PASS；`github-yunxiao-pipeline.html` 写李云峰 QA Owner；`team-leads.html` 写按钮权随 QA Owner | `TEAM-COLLAB v2.1` 只锁 required status check；站点后续补充将李云峰列为 QA Owner / qa-verdict 管理员 | 在 `qa.html` 明确区分“QA 团队执行验收”和“qa-verdict 物理按钮 / owner”；以 `github-yunxiao-pipeline.html` 和 `team-leads.html` 的 Owner 口径为准 | `rg -n "QA 团队成员 approve|qa-verdict = PASS" hl-dispatch-gh-pages/pages/qa.html` 命中处改为 Owner 口径 |
| P1-02 | `TEAM.yml` 仍是 R-034 旧核心组映射 | `TEAM.yml` 注释为 R-034 核心团队，只有 `java-qa: LUXBYA`，无 QA Lead / QA team | 站点 `global.html` / `team-leads.html` 已采用 6 Lead + QA x4 口径 | 补一个 `TEAM.yml` v2 迁移任务：增加 `qa-lead`、`qa-team` 或明确 TEAM.yml 只服务旧派发语义；避免自动派发“测试团队”落到 Gate-3 旧角色 | `rg -n "R-034|java-qa|LUXBYA|qa-lead|qa-team" hl-dispatch/TEAM.yml` 人工复核 |
| P1-03 | UI 自动化工具锁定状态模糊 | `qa.html` 把 Playwright / patrol 放在技术选型表；`tech-selection.html` 写 patrol 是 `PENDING (J-03)`，当前锁定绿线是 `integration_test` | `DD-FE-CLIENT-v1`：Flutter CI 绿线是 `integration_test`；`tech-selection.html`：patrol 未入锁 | `qa.html` 表格增加状态列：`LOCKED / PENDING / LEARNING`；Playwright、patrol 标为候选或学习入口，不能写成已锁定主栈 | `rg -n "Playwright|patrol" hl-dispatch-gh-pages/pages/qa.html` 周边必须出现 `PENDING` 或 `学习入口` |
| P1-04 | Cap-Spec-2 / QA 协作边界容易被误读 | `qa.html` 说 QA 编写验收场景，但 `TEAM-COLLAB v2.1` 明确 Cap-Spec-2 owner 是 PM，QA 是 collaborator/reviewer | `TEAM-COLLAB v2.1 F-5`：Cap-Spec-2 owner = PM；QA = collaborator/reviewer | 页面统一为：PM 定义验收场景，QA 将可自动化场景映射到 manifest 并实现验收测试；QA 可反馈缺口，但不替代 PM 定义业务需求 | `rg -n "QA 编写验收场景|编写验收场景" hl-dispatch-gh-pages/pages/qa.html` 逐条复核上下文 |

---

## P2 整理：降低培训与 onboarding 误导

| ID | 问题 | 证据 | 修订动作 | 验证方式 |
|---|---|---|---|---|
| P2-01 | `team-memory` 旧指南未退场 | `GUIDE-20260403-005` 写“不设独立 QA”；`GUIDE-20260403-006` 写 PM 自主驱动 AI 编码、测试与业务验收 | 在旧指南 frontmatter 或开头加 `SUPERSEDED by TEAM-COLLAB-SPEC v2.1` 提示，或新建 `GUIDE-20260506-QA-TEAM-ONBOARDING` 替代入口 | `rg -n "不设独立 QA|创始人 \\+ AI.*100%|PM \\+ AI.*编码" team-memory/00-index` 能看到 superseded 提示 |
| P2-02 | `qa.html` 治理来源写 `DD-TEST v1.1` | `qa.html` 顶部引用 `DD-TEST v1.1` | 改为 `DD-TEST v1.2`，并与 `tech-selection.html` 引用一致 | `rg -n "DD-TEST v1.1" hl-dispatch-gh-pages/pages` 不再命中 |
| P2-03 | 学习路线缺少“工具分级” | QA 页把正式栈、候选栈和学习工具混在同一表 | QA 技术表按三档拆分：治理锁定、推荐实践、候选/学习入口；沿用 `TOOLCHAIN-GUIDE v1` 三档语言 | 页面人工检查，确保每个工具有状态和真源 |
| P2-04 | `qa-process.html` 与 `qa.html` 内容重叠但口径不同 | 两页都讲 manifest、G-026、qa-verdict，但各自维护不同示例 | 指定一个页面为“操作手册”，另一个只做入口；减少重复 schema 和门禁规则正文 | `rg -n "acceptance-manifest|G-026|qa-verdict" hl-dispatch-gh-pages/pages/qa*.html` 后续只在一个页面保留完整规范正文 |

---

## 建议执行顺序

1. 先改 `qa.html` / `qa-process.html` 的 manifest schema、G-026、JUnit/Kotest 文案，形成一个站点 PR。
2. 同 PR 修 `gate-levels.html` 中的 `60%` 文案，避免全局门禁页继续传播阈值。
3. 第二个 PR 处理 `qa-verdict` Owner、`TEAM.yml` 映射和 `team-leads` 交叉引用。
4. 第三个 PR 处理 `team-memory` 旧指南退场；该仓为团队共享知识库，变更前需确认是否直接加 superseded banner，还是另起新版指南。

---

## 执行日志

| 时间 | 范围 | 状态 | 说明 |
|---|---|---|---|
| 2026-05-06 | P0-01 / P0-02 / P0-03 / P0-04 | applied locally | 已修改 `hl-dispatch-gh-pages/pages/qa.html`、`qa-process.html`、`gate-levels.html`：统一 DD-TEST v1.2 manifest schema；删除 G-026 60% Pilot 阈值和 JaCoCo/Codecov 输入口径；恢复 JUnit 5 主框架、Kotest Property 补充库口径；`gate-levels` L2 改为 `G-026 manifest 校验`。 |
| 2026-05-06 | P1-01 / P1-02 | applied locally | 已修改 `qa.html`、`global.html`、`gate-levels.html`：区分 QA team 执行验收/evidence 与 QA Owner 签发 `qa-verdict`；已修改 `hl-dispatch/TEAM.yml`：新增 `qa-owner` / `qa-team` 占位角色（`github: ""`，待身份映射确认），并将 `java-qa` 标注为 R-034 legacy Gate-3，禁止作为 v2.1 QA team 默认派发目标。 |
| 2026-05-06 | P1-03 / P1-04 | applied locally | 已修改 `qa.html`：Playwright 标为 `LEARNING`，patrol 标为 `PENDING`，当前 Flutter 绿线仍指向 `integration_test`；将“QA 编写验收场景 / QA 工程师出具 qa-verdict”口径改为“PM 持有验收场景，QA 映射 manifest 与提交 evidence，QA Owner 签发 verdict”。 |
| 2026-05-06 | P2-01 | applied locally | 用户继续后，已在 `team-memory/00-index/GUIDE-20260403-005-engineer-division.md` 与 `GUIDE-20260403-006-ai-team-overview.md` 顶部添加 `SUPERSEDED` 历史留痕提示，并将 `updated_at` 更新为 2026-05-06；旧正文保留用于追溯，不再作为当前执行依据。 |
| 2026-05-06 | local verification | passed | `rg` 复查活动页面与 `TEAM.yml`，旧 schema / 旧阈值 / 旧 QA approve / 旧技术选型口径无命中；正向检索确认 DD-TEST v1.2、G-026 manifest、QA Owner、`qa-owner` / `qa-team`、Playwright `LEARNING`、patrol `PENDING` 均存在；`team-memory` 旧指南检索可看到 `SUPERSEDED` 提示；`git diff --check` 通过。 |
| 2026-05-06 | publish status | pending | 已用线上 URL 复查，`https://huanlongai.github.io/hl-dispatch/pages/global.html` 仍是发布前旧内容；本地修订尚未 push / publish。 |

---

## 修订后的口径标准

### acceptance-manifest

- `Cap-Spec-2` 由 PM 持有，QA 是 collaborator/reviewer。
- QA 持有 `acceptance-manifest.yaml` 和 `acceptance/` 测试资产。
- `acceptance-manifest.yaml` 使用 `DD-TEST v1.2` schema。
- `API_EXEC` / `AUDIT_EXEC` / `UI_AUTO` 进入 G-023 自动化验收门禁；`UI_MANUAL` 不进 PR 门禁，进入 PM/UAT 里程碑验收。

### G-026

- G-026 是 L2 确定性门禁。
- 输入是 Cap-Spec-2 Case-ID 集合和 `acceptance-manifest.yaml`。
- 检查方式是 YAML 解析，不解析 Kotlin 源码，不读取 JaCoCo / Codecov。
- 失败条件是存在未覆盖的可自动化 Case-ID。

### 测试技术栈

- `JUnit 5.10.2` 是唯一主测试框架和推荐 runner。
- `Kotest Property 5.9.1` 是属性测试补充库。
- `Testcontainers 1.20.4` 是集成测试与 Flyway 全量迁移回放基础设施。
- 场景前端当前锁定绿线是 Flutter 官方 `integration_test`；`patrol` 仍是 J-03 候选。

### qa-verdict

- QA 团队负责验收执行、证据收集、回归基线维护。
- `qa-verdict` 必须是 GitHub required status check。
- 物理按钮权 / Owner 必须与 `team-leads.html`、`github-yunxiao-pipeline.html`、`TEAM.yml` 的可执行派发配置一致。

---

## 开放问题

| ID | 问题 | 建议 |
|---|---|---|
| O-01 | G-026 是否允许 Pilot 阶段低于 100% 的自动化覆盖？ | 如果允许，必须由 `DD-TEST` 或 `verification-gates.md` 明确阈值、适用窗口、退出条件；站点不能单独写 60%。 |
| O-02 | `qa-verdict` 是单 Owner 签字还是任一 QA 成员签字？ | 建议治理层定义为 QA Owner 持按钮，执行层允许 QA team 提供 evidence；避免任意成员 approve 直接放行。 |
| O-03 | Playwright 是否进入 Web / 小程序 / 控制台 E2E 绿线？ | 当前只可作为候选或学习入口；若入锁，需要补 DD-FE / TOOLCHAIN-GUIDE 变更。 |
