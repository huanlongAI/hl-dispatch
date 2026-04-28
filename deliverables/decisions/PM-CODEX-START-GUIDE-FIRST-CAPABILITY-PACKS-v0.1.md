# PM Codex 启动指南：首批能力包 v0.1

## PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS

---

**文档编号**：PM-CODEX-START-FIRST-CAPS-001
**版本**：v0.1
**日期**：2026-04-28
**状态**：GUIDE（PM 启动手册）
**派生自**：HL-FIRST-CAPABILITY-PACKS-UPSTREAM v0.6（Founder Signed）
**适用对象**：PM-1 朱阳、PM-2 邹骢
**用途**：让 PM 第一次打开 Codex 后，可以直接启动首批能力包 Cap-Spec 工作
**边界**：本指南是操作引导，不是新的裁决；正式上游以 `HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md` 为准

---

## 0. 先说结论

你现在要做的不是写代码，也不是让工程师立刻开工。

你要做的是用 Codex 把自己负责的能力包写成 Cap-Spec（能力包规格）：

- 这个能力包做什么。
- 不做什么。
- 依赖哪些上游契约。
- 有哪些 key_action（关键治理动作）。
- 需要哪些 reason_code（业务码）。
- 怎么验收才算做对。
- 还缺哪些契约，需要 Founder / Gate / 工程补齐。

PM 的当前交付物是“能让工程师理解、能让契约审查、能让后续开发不跑偏”的规格文件，不是代码。

---

## 1. 你负责什么

### PM-1 朱阳：供给侧语义

你负责两个能力包：

| 能力包 ID | 中文名 | 你要讲清楚的问题 |
|---|---|---|
| `biz.offer.catalog` | 供给目录 | 商户提供什么服务？每项服务需要什么资源？服务规则是什么？ |
| `biz.store.resource` | 门店与资源（供给资源配置） | 门店实际有什么资源？房间、服务位、手艺人如何支持预约？ |

你的核心目标：把“服务”和“资源”定义清楚，避免后面的预约、履约、客户能力包各自发明一套说法。

### PM-2 邹骢：客户与预约履约

你负责两个能力包：

| 能力包 ID | 中文名 | 你要讲清楚的问题 |
|---|---|---|
| `biz.customer.profile` | 客户档案 | 谁来预约？客户主体怎么识别、创建、关联预约？ |
| `biz.booking.fulfillment` | 预约与履约 | 自然交互如何生成草稿、暂占资源、人工确认、形成正式预约并履约？ |

你的核心目标：把“客户是谁、预约如何从草稿变成正式单据、资源如何被暂占和释放”定义清楚。

---

## 2. 打开 Codex 前先记住 5 条

1. **GitHub 是正式真源，飞书不是。** 飞书只用来提醒和沟通，结论要落到 GitHub。
2. **Founder 签字文件是上游。** 你不能把自己的理解覆盖掉上游裁决。
3. **AI 输出先是草稿。** Codex 给你的内容，未经你确认和 PR 审查，不是决定。
4. **一次只推进一个能力包。** 不要四个包一起写，否则边界会混。
5. **当前不写代码。** PM 当前只做 Cap-Spec、验收场景、业务码提案和契约缺口。

---

## 3. Codex 打开哪个仓库

优先打开 `hl-contracts`，因为 PM 最终要提交的 Cap-Spec 应该进入契约仓。

同时让 Codex 读取 `hl-dispatch` 中的上游任务书：

```text
hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md
```

如果 Codex 当前只打开了一个仓库，第一句话就让它检查是否能读到这些仓库：

```text
请先检查你是否能读取 hl-contracts 和 hl-dispatch 两个仓库。
如果不能读取，请告诉我缺哪个仓库，不要猜。
```

---

## 4. 第一次打开 Codex，直接复制这段

### 通用启动语

```text
你现在协助我作为唤龙平台 PM，启动首批能力包 Cap-Spec 工作。

请先读取并对齐以下文件：
1. hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md
2. hl-dispatch/deliverables/decisions/PRD-REDEFINITION-SPEC.md
3. hl-dispatch/deliverables/decisions/PM-AI-COLLABORATION-ONBOARDING-SPEC.md
4. hl-contracts 中与 HK Kernel、Gateway / Protocol Gate、reason_code、capability registry、rules、facts 相关的现有真源文件。

边界：
- 当前只做 Cap-Spec，不写代码。
- 不把 AI 草稿、飞书讨论、未经 Founder 确认的过程文件当真源。
- 不复制 Tier 1 SSOT，只引用真源路径。
- 遇到不确定概念先问我，不要猜。

请先输出：
1. 你读取到的正式上游事实。
2. 我负责的能力包边界。
3. 你认为当前最需要我裁决的 3 个问题。
4. 然后一次只问我 1 个问题，帮我把 Cap-Spec 写清楚。
```

### 朱阳启动语

```text
我是朱阳，负责 biz.offer.catalog 和 biz.store.resource。

请先从 biz.offer.catalog 开始，不要两个包同时写。
目标是产出 Cap-Spec-1 能力规格书初稿、Cap-Spec-2 验收场景集初稿、Cap-Spec-3 reason_code 提案、Contract Gap 清单。

请围绕“商户提供什么服务、服务需要什么资源、门店实际有什么资源、手艺人和服务位如何支持预约”来盘问我。
每次只问 1 个问题，并给出推荐答案选项。
```

### 邹骢启动语

```text
我是邹骢，负责 biz.customer.profile 和 biz.booking.fulfillment。

请先从 biz.booking.fulfillment 开始，因为它最能暴露客户、草稿、资源暂占、人工确认和审计闭环的边界。
目标是产出 Cap-Spec-1 能力规格书初稿、Cap-Spec-2 验收场景集初稿、Cap-Spec-3 reason_code 提案、Contract Gap 清单。

请围绕“自然交互意图 → AI Draft（AI 候选草稿） → Appointment Intent Hold（预约意向保留） → Qualified Resource Hold（合格资源暂占） → GUI Confirm（图形界面人工确认） → Confirmed Booking（正式预约） → Fulfillment（到店与履约） → Audit Evidence（审计证据）”来盘问我。
每次只问 1 个问题，并给出推荐答案选项。
```

---

## 5. PM 在 Codex 里按 6 步走

### 第一步：让 Codex 复述上游

目的：确认 Codex 没有猜、没读错、没把过程文件当真源。

你要看到它讲清楚：

- 4 个能力包分别是什么。
- 谁负责哪两个。
- 当前只做 Cap-Spec，不写代码。
- 工程开工前必须完成契约缺口和审查。
- GitHub main 中的上游任务书是正式真源。

如果 Codex 复述错了，先纠正，不要继续。

### 第二步：选定一个能力包

每次只做一个。

建议顺序：

| PM | 第一个能力包 | 原因 |
|---|---|---|
| 朱阳 | `biz.offer.catalog` | 先定义服务，后面资源和预约才能引用。 |
| 邹骢 | `biz.booking.fulfillment` | 预约链路最复杂，最容易暴露跨包边界。 |

### 第三步：用“一次一问”逼清边界

让 Codex 每次只问一个问题。你回答后，它再问下一个。

不要接受一口气 10 个问题的问卷。能力包启动阶段最重要的是把关键判断逼清楚，不是快速堆文档。

你可以这样要求：

```text
请一次只问我一个问题。
每个问题都要说明：为什么这个问题重要、如果选错会造成什么后果、你推荐哪个答案。
```

### 第四步：生成 4 份草稿

每个能力包至少生成 4 份草稿：

| 草稿 | 作用 |
|---|---|
| Cap-Spec-1（能力规格书） | 定义能力边界、目标、非目标、业务规则意图、上游引用。 |
| Cap-Spec-2（验收场景集） | 定义输入、预期、验收方式、审计要求。 |
| Cap-Spec-3（业务码提案） | 提出 reason_code，解释触发场景和业务含义。 |
| Contract Gap（契约缺口）清单 | 标出需要 Founder / Gate / 工程补齐的契约项。 |

注意：这些一开始都是草稿。你确认前，不能当决定。

### 第五步：让 Codex 做自查

草稿生成后，让 Codex 按下面清单自查：

```text
请检查这份 Cap-Spec 草稿：
1. 是否越出了 Founder 上游任务书的边界？
2. 是否复制了 Tier 1 SSOT，而不是只引用路径？
3. 是否把 AI 草稿当成正式业务事实？
4. 是否遗漏 key_action、reason_code、审计证据或 Contract Gap？
5. 是否有跨包重定义：本包定义了别的包应该定义的东西？
6. 是否有纯英文术语没有中文备注？
```

### 第六步：准备 PR

当你确认草稿可进入审查后，再让 Codex 准备 PR。

PR 说明必须写清楚：

- 本次是哪个能力包。
- 引用的上游任务书是哪一份。
- 哪些内容是 PM 业务语义定义。
- 哪些内容是契约缺口，不是已经生效的契约。
- 哪些问题需要 Founder / Gate 裁决。

---

## 6. 四类问题怎么处理

| 遇到的问题 | 处理方式 |
|---|---|
| 上游任务书已经写清楚 | 直接引用，不重新发明。 |
| 业务上需要补充，但不影响契约 | 写进 Cap-Spec 草稿，标注为 PM 业务语义。 |
| 需要改 reason_code、capability registry、OpenAPI、rules、facts | 写入 Contract Gap，不要直接当成已生效契约。 |
| 需要 Founder 裁决 | 在 hl-dispatch 提 decision-request，或在 PR 中明确标注“待 Founder 裁决”。 |

---

## 7. 不要做的事

- 不要让 Codex 直接写工程代码。
- 不要跳过 Cap-Spec 直接让工程师开工。
- 不要把飞书里的讨论直接当结论。
- 不要把 AI 生成的草稿当正式文件。
- 不要复制 `hl-contracts` 里的 Tier 1 SSOT 内容，只引用路径。
- 不要在一个能力包里定义另一个能力包的主数据。
- 不要改 Founder Signed 的上游任务书。

---

## 8. 交付节奏建议

### 第 1 天

- Codex 读取上游。
- PM 选定第一个能力包。
- 完成 boundary（边界确认）和 grill（一次一问盘问）。
- 形成 Cap-Spec-1 初稿结构。

### 第 2 天

- 补齐 Cap-Spec-2 验收场景。
- 补齐 Cap-Spec-3 reason_code 提案。
- 补齐 Contract Gap 清单。
- 做自查，准备 PR。

### 第 3 天

- 提交 PR。
- 在 PM 工作台发 PR 链接。
- 根据 Founder / Gate review 修改。

如果第 2 天仍然写不出清楚边界，不要硬交。先把卡住的问题提出来，边界不清比延期更危险。

---

## 9. 飞书汇报模板

PM 每次阶段性推进后，在 PM 工作台用下面格式同步：

```text
【能力包启动同步】

我负责的能力包：
- 待填写能力包 ID

当前正在推进：
- 待填写当前能力包 / 当前阶段

已确认：
- 待填写已确认事实

还不确定：
- 待填写未决问题

需要 Founder / Gate 裁决：
- 待填写裁决事项

GitHub 链接：
- PR / Issue / 文档链接
```

不要只说“我已经看完了”或“我理解了”。要说清楚理解了什么、还缺什么、下一步产出在哪里。

---

## 10. 最小完成标准

一个能力包进入工程前，至少要满足：

1. Cap-Spec-1 / 2 / 3 已提交 PR。
2. Contract Gap 已列清楚。
3. key_action 和 reason_code 提案已列出。
4. HK Kernel（唤龙治理内核）和 Gateway / Protocol Gate（统一入口与协议门）的接入点已说明。
5. 验收场景能覆盖正常、拒绝、过期、取消、审计五类情况。
6. Founder / Gate 已审查通过。

在满足这些之前，工程团队不应直接开工。

---

## 11. 给 Codex 的结束语

每次会话结束前，复制给 Codex：

```text
请总结本次会话：
1. 已确认的事实。
2. 已做出的 PM 判断。
3. 仍未决的问题。
4. 下一次应该先问我的 1 个问题。
5. 哪些内容需要落到 GitHub Issue / PR。

不要替我做最终裁决；如果有未确认内容，请明确标注“待 PM / Founder 确认”。
```

*v0.1 · 2026-04-28 · PM Codex 启动指南*
