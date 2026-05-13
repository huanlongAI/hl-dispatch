# PM 崔田恬正式能力包前置启动任务书 v0.1

> 日期：2026-05-13
> 状态：PUBLISHED
> GitHub Issue：`huanlongAI/hl-dispatch#80`
> 面向对象：PM 崔田恬（GitHub: `cuitiantian0704`）
> 目标：在正式能力包下发前，完成 PM Cap-Spec 工作流、GitHub 证据链、Issue / PR 节奏、Gate 反馈处理的前置演练。
> 边界：本任务不分配正式能力包，不写 `hl-contracts` 契约，不注册 reason_code，不写代码，不授权工程开工。

## 发布记录

| 时间 | 事项 | 证据 |
|---|---|---|
| 2026-05-13 | 创建 GitHub Issue | `hl-dispatch#80` |
| 2026-05-13 | 发布到飞书 PM工作台 | message_id `om_x100b6f762aba60a4c393d1ead098a4e` |
| 2026-05-13 | 回填执行入口 | `hl-dispatch#80` comment `4439039076` |
| 2026-05-13 | 处理 D0 权限反馈 | `hl-dispatch` 已补 Write；`team-memory` 受 GitHub `seat_limit` 阻塞 |

## 0. 设计依据

本任务单对齐以下当前事实：

1. PM-1 朱阳主线：`hl-dispatch#39`。
   - `biz.offer.catalog` 四件套已通过 `hl-contracts#29` 合入。
   - 合入性质是 DRAFT Cap-Spec evidence baseline，不是 Founder / Gate 最终批准。
   - `biz.store.resource` 已启动盘问，但截至 2026-05-13 尚未形成 `hl-contracts` PR。
2. PM-2 邹骢主线：`hl-dispatch#40`。
   - `hl-contracts#30` 是 `biz.booking.fulfillment / booking` Draft PR，checks 通过。
   - G8 已接受 #30 为 booking 业务基线 Draft，但 #30 继续 Draft、不 Ready、不 Merge、不授权工程开工。
   - G9 后续顺序已定：registry / legacy mapping -> facts / events -> reasoncodes -> outcome classification -> OpenAPI。
   - `hl-contracts#34` 是 registry + legacy mapping 任务 Issue。
   - `hl-contracts#35` 是 G9 step 1 Draft PR，checks 全绿，等待 Founder / Gate G10 / G11 裁决。
3. 团队记忆状态：
   - `team-memory/00-index/TEAM-ROSTER.md` 记录崔田恬状态为“GitHub 已接入·待首条记忆沉淀”。
4. 最新 PM 口径：
   - 采用 `PRD-REDEFINITION-SPEC v3.0` 的收敛口径：PM 聚焦业务语义 SSOT、Cap-Spec、HPRD 审批、PM acceptance；不直接驱动工程代码。

## 1. 启动目标

崔田恬在正式能力包下发前，需要先具备以下能力：

1. 能读懂一个 PM 能力包 Issue 的正文、评论链、验收口径和当前状态。
2. 能区分“DRAFT evidence baseline”“已生效契约”“Founder / Gate 裁决”“工程开工授权”。
3. 能复述 Cap-Spec 四件套：Cap-Spec-1、Cap-Spec-2、Cap-Spec-3 reason_code 提案、Contract Gap。
4. 能从 Issue / PR 评论中提取当前阻塞点、下一步动作、禁止事项。
5. 能把飞书或 Codex 过程讨论回填到 GitHub，不停留在私聊或 AI 对话中。
6. 能识别 Gate false positive 与文档规避的边界：遇到 Gate 误报时回填 `NEEDS_GATE_FIX`，不使用不可审查的绕过写法。
7. 能完成首条 team-memory session 沉淀，证明工作过程可接续。

## 2. 不做事项

本任务明确不做以下事项：

- 不给崔田恬分配正式能力包。
- 不让崔田恬创建 `hl-contracts/prd/biz/` 能力包四件套。
- 不修改 `reasoncodes.csv`。
- 不写 OpenAPI / facts / events / registry / runtime code。
- 不让工程师基于本任务开工。
- 不把朱阳或邹骢的 DRAFT 当作最终契约。
- 不把 `biz.offer.catalog` 的 Contract Gap 或 reason_code 提案当作已生效契约。
- 不把 `hl-contracts#30` 或 `hl-contracts#35` 的 Draft 状态解释为可合并或可开发。

## 3. 必读材料

崔田恬启动前先读取：

1. `hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md`
2. `hl-dispatch/deliverables/decisions/PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS-v0.1.md`
3. `hl-dispatch/deliverables/decisions/PRD-REDEFINITION-SPEC.md`
4. `hl-dispatch#39`：PM-1 朱阳供给侧能力包主线。
5. `hl-contracts#29`：朱阳 `biz.offer.catalog` PR。
6. `hl-dispatch#40`：PM-2 邹骢客户与预约履约能力包主线。
7. `hl-contracts#30`：邹骢 booking Cap-Spec Draft PR。
8. `hl-contracts#34` / `hl-contracts#35`：booking registry + legacy mapping 任务与 PR。
9. `team-memory/00-index/TEAM-ROSTER.md`
10. `team-memory/CLAUDE.md`

## 4. D0-D2 前置任务

### D0：环境与身份确认

目标：确认崔田恬能进入正式协作链路。

任务：

1. 确认 GitHub 账号为 `cuitiantian0704`。
2. 确认能访问 `huanlongAI/hl-dispatch` 与 `huanlongAI/team-memory`。
3. 在 Cowork / Codex 中确认 AI 能读取本任务单和 `TEAM-ROSTER.md`。
4. 完成一次 team-memory session 沉淀，主题建议为：
   - `2026-05-13-pm-cuitiantian-pre-capability-startup.md`

验收：

- 在本任务对应 GitHub Issue 下回填：

```markdown
## 崔田恬 D0 回填：环境与记忆链路

GitHub：cuitiantian0704

已确认：
- 可读取 hl-dispatch：
- 可读取 team-memory：
- 已完成首条 team-memory 沉淀：

当前卡点：
- 无 / 列出
```

### D1：对齐朱阳与邹骢两条 PM 主线

目标：通过真实 Issue / PR 学会 PM 能力包推进方式，而不是先写自己的能力包。

任务：

1. 阅读 `hl-dispatch#39`，输出朱阳主线状态摘要。
2. 阅读 `hl-contracts#29`，输出 `biz.offer.catalog` PR 的合入性质。
3. 阅读 `hl-dispatch#40`，输出邹骢主线状态摘要。
4. 阅读 `hl-contracts#30`、`#34`、`#35`，输出 booking 从 PM Draft 到契约落位拆分的过程。
5. 对比两条主线，列出至少 8 条可复用 PM 工作纪律。

必须覆盖的观察点：

- 为什么朱阳 #29 可以 merge，但仍不代表工程开工。
- 为什么朱阳 `biz.store.resource` 不能继续只停留在 Codex 对话中。
- 为什么邹骢 387 轮对话后必须先收束成 GitHub 可审查 PR。
- 为什么 #30 被接受为业务基线 Draft 后仍不 Ready / 不 Merge。
- 为什么 #35 checks 通过后仍等待 G10 / G11，而不是自动合并。
- 为什么 reason_code 提案不等于 `reasoncodes.csv` 注册。
- 为什么 Contract Gap 不能被补写成最终答案。
- 为什么 Issue / PR 是 SSOT，飞书只做提醒。

验收：

- 在本任务对应 GitHub Issue 下回填一条不超过 2000 字的状态对齐报告。

### D2：PM Cap-Spec 前置演练

目标：不写正式能力包，只演练“如何准备接手能力包”。

任务：

1. 基于 D1 对齐结果，写一份 `PM Readiness Report`。
2. 报告建议落在 `hl-dispatch`，而不是 `hl-contracts`。
3. 文件建议：
   - `deliverables/decisions/PM-CUITIANTIAN-READINESS-REPORT-v0.1.md`
4. 该报告只写工作法，不写具体能力包规格。

报告必须包含：

- 我理解的 PM 角色边界。
- 我理解的 Cap-Spec 四件套。
- 我理解的 DRAFT / baseline / contract / engineering start 的区别。
- 朱阳案例给我的 3 条提醒。
- 邹骢案例给我的 3 条提醒。
- 我正式接手能力包前还需要 Founder 明确的 3 个问题。
- 我会如何在正式能力包中做 GitHub 回填。

验收：

- 创建 `hl-dispatch` PR，标题建议：

```text
[PM] 崔田恬正式能力包前置准备报告 v0.1
```

- PR 描述必须写清：
  - 本 PR 不分配能力包。
  - 本 PR 不修改 `hl-contracts`。
  - 本 PR 不授权工程开工。
  - 本 PR 是 readiness evidence。

## 5. 推荐 GitHub Issue 正文

如需直接创建 GitHub Issue，可使用以下正文。

```markdown
## 任务名称

PM 崔田恬正式能力包前置启动准备

## 执行角色

PM 崔田恬（GitHub: cuitiantian0704）

## 优先级

P1 - 正式能力包下发前完成

## 目标

在正式能力包分配前，先通过朱阳和邹骢两条已派发 PM 主线，完成 Cap-Spec 工作流、Issue / PR 证据链、Gate 反馈处理、team-memory 沉淀的前置演练。

## 读取范围

- hl-dispatch#39
- hl-contracts#29
- hl-dispatch#40
- hl-contracts#30
- hl-contracts#34
- hl-contracts#35
- team-memory/00-index/TEAM-ROSTER.md
- team-memory/CLAUDE.md
- hl-dispatch/deliverables/tasks/PM-CUITIANTIAN-PRE-CAPABILITY-STARTUP-TASKBOOK-2026-05-13-v0.1.md

## 任务清单

- [ ] D0：确认 GitHub 与 team-memory 链路。
- [ ] D0：完成首条 team-memory session 沉淀。
- [ ] D1：阅读朱阳 #39 / #29，输出状态摘要。
- [ ] D1：阅读邹骢 #40 / #30 / #34 / #35，输出状态摘要。
- [ ] D1：列出至少 8 条 PM 工作纪律。
- [ ] D2：创建 `PM-CUITIANTIAN-READINESS-REPORT-v0.1.md`。
- [ ] D2：向 `hl-dispatch` 提交 readiness PR。
- [ ] D2：在本 Issue 回填 PR 链接、commit、当前 checks、卡点。

## 验收标准

- 能准确复述朱阳与邹骢两条 PM 主线的当前状态。
- 能区分 DRAFT evidence baseline、已生效契约、Founder / Gate 裁决、工程开工授权。
- 能解释 Cap-Spec-1 / 2 / 3 / Contract Gap 的用途。
- 能说明 reason_code 提案不等于注册。
- 能说明 Contract Gap 不是最终答案。
- 能完成首条 team-memory 沉淀。
- 能提交一份 `hl-dispatch` readiness PR。

## 禁止事项

- 不启动正式能力包。
- 不修改 `hl-contracts`。
- 不写代码。
- 不注册 reason_code。
- 不写 OpenAPI / facts / events / registry。
- 不授权工程开工。
```

## 6. 崔田恬 Codex 启动提示词

崔田恬第一次打开 Codex 可直接复制：

```text
我是崔田恬，GitHub 是 cuitiantian0704。当前我还没有正式能力包任务。

请先读取：
1. hl-dispatch/deliverables/tasks/PM-CUITIANTIAN-PRE-CAPABILITY-STARTUP-TASKBOOK-2026-05-13-v0.1.md
2. team-memory/00-index/TEAM-ROSTER.md
3. team-memory/CLAUDE.md
4. hl-dispatch#39 与 hl-contracts#29
5. hl-dispatch#40 与 hl-contracts#30/#34/#35

当前边界：
- 不启动正式能力包。
- 不修改 hl-contracts。
- 不写代码。
- 不注册 reason_code。
- 不把 DRAFT 当最终契约。
- 不把飞书或 AI 对话当 SSOT。

请先输出：
1. 我当前的身份与任务边界。
2. 朱阳 PM 主线当前状态。
3. 邹骢 PM 主线当前状态。
4. 我需要完成的 D0-D2 任务清单。
5. 你发现的缺失信息或权限卡点。

不要开始写 PR，先等我确认。
```

## 7. Founder / Gate 可裁决点

1. 是否接受本任务作为崔田恬正式能力包前置准备任务。
2. 是否要求崔田恬只提交 readiness PR，不允许碰 `hl-contracts`。
3. 是否在 readiness PR 通过后再下发正式能力包。
4. 正式能力包下发时，是否沿用朱阳 / 邹骢的首条启动 Issue 模板。

推荐裁决：

- 接受本任务。
- 崔田恬第一轮只做 readiness evidence，不碰 `hl-contracts`。
- readiness PR 通过后，再由 Founder 下发正式能力包。
