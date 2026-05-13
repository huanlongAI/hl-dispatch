# PM 崔田恬正式能力包前置准备报告 v0.1

> 日期：2026-05-13
> 关联任务：`huanlongAI/hl-dispatch#80`
> 执行角色：PM 崔田恬（GitHub: `cuitiantian0704`）
> 状态：DRAFT readiness evidence
> 范围：正式能力包下发前的工作流准备证明

## 0. 报告目的

本报告用于响应 `huanlongAI/hl-dispatch#80`，证明 PM 崔田恬已开始完成正式能力包接入前的准备工作。

本报告不是正式能力包规格，不分配能力包，不修改 `hl-contracts`，不注册 reason_code，不写 OpenAPI / facts / events / registry，不写代码，不授权工程开工。

## 1. 我理解的 PM 角色边界

PM 在能力包工作中的职责是业务语义 SSOT owner，负责在 Founder 给定的上游边界内产出 Cap-Spec、验收场景、reason_code 提案和 Contract Gap，并在 Issue / PR 中维护可审查证据链。

PM 不直接修改 Tier 1 SSOT，不绕过 Founder / Gate 裁决，不把 AI 草稿、飞书讨论或私聊过程当作正式真源，不让工程师基于未审查草稿开工。

## 2. 我理解的 Cap-Spec 四件套

1. Cap-Spec-1：能力规格书，说明能力目标、边界、非目标、业务规则意图和上游引用。
2. Cap-Spec-2：验收场景集，用业务场景定义输入、预期、状态、key_action、reason_code 和审计要求。
3. Cap-Spec-3：reason_code 提案，只是业务侧候选说明，不等于写入 `reasoncodes.csv`。
4. Contract Gap：契约缺口清单，用于暴露待 Founder / Gate / Engineering 补齐的契约项，不能补写成最终答案。

## 3. DRAFT / baseline / contract / engineering start 的区别

| 概念 | 含义 | 可做 | 不可做 |
|---|---|---|---|
| DRAFT | 草稿或待审查 PR 状态 | 可讨论、可审查、可继续修订 | 不可当最终契约 |
| evidence baseline | 已形成可审查证据基线 | 可作为后续审查输入 | 不等于 Founder / Gate 最终批准 |
| contract | 已按治理流程落入契约真源 | 可被后续实现引用 | 仍需遵守对应 gate 和 owner 规则 |
| engineering start | 明确授权工程开工 | 工程可进入实现 | 未授权前不得默认开工 |

## 4. 朱阳案例给我的 3 条提醒

1. `biz.offer.catalog` 四件套通过 `hl-contracts#29` 合入后，性质仍是 DRAFT Cap-Spec evidence baseline，不是最终契约，不注册 reason_code，不授权工程开工。
2. `biz.store.resource` 不能长期停留在 Codex / 飞书 / 私聊过程里；盘问完成后必须进入 GitHub 可审查 PR，并回填 PR、commit、checks 和卡点。
3. 后续能力包可以继承前一个 DRAFT baseline 的业务输入，但不能把其中的 Contract Gap 或 reason_code 提案当作已生效契约。

## 5. 邹骢案例给我的 3 条提醒

1. 387 轮对话不是证据链，必须收束成 GitHub PR，Founder / Gate 才能逐段审查。
2. `hl-contracts#30` 被 G8 接受为 booking 业务基线 Draft 后，仍保持 Draft、不 Ready、不 Merge、不授权工程开工。
3. `hl-contracts#35` checks 全绿后仍等待 G10 / G11；checks 通过只是必要条件，不等于 Founder / Gate 已授权合并或工程开工。

## 6. 我正式接手能力包前还需要 Founder 明确的 3 个问题

1. 我正式接手的能力包 ID、业务范围、非目标和优先级是什么。
2. 我应提交 Cap-Spec 的目标仓库、目录和分支命名规则是什么，尤其是是否直接进入 `hl-contracts/prd/biz/`。
3. reason_code / registry / facts / events / OpenAPI 的拆分顺序、owner 和 Gate 裁决点如何安排。

## 7. 我会如何在正式能力包中做 GitHub 回填

正式能力包下发后，我会按以下节奏回填：

1. 在任务 Issue 中确认身份、读取范围、当前边界和禁止事项。
2. 先输出上游事实、能力范围、非范围、待裁决问题，不直接写最终结论。
3. 形成 Cap-Spec 四件套 Draft PR，PR 描述明确 DRAFT、范围、非工程开工输入、未注册项和待裁决项。
4. 每轮 review 后在 Issue / PR 回填 commit、checks、修改摘要和剩余卡点。
5. Gate false positive 按 `NEEDS_GATE_FIX` 回填，不使用不可审查的文档规避写法绕过。
6. 等待 Founder / Gate 明确裁决后，再进入下一步拆分；未授权前不推动工程开工。

## 8. 当前准备度与卡点

已完成：

- GitHub 账号已确认为 `cuitiantian0704`。
- 已可读取 `huanlongAI/hl-dispatch`，并已在 `hl-dispatch#80` 回填 D0 / D1。
- 已对齐 `hl-dispatch#39` 与 `hl-dispatch#40` 中可见的朱阳、邹骢主线推进过程。

当前卡点：

- 当前账号无法直接读取 `huanlongAI/team-memory`，首条 team-memory session 沉淀仍被权限阻塞；Issue #80 最新回填显示阻塞原因为 GitHub `seat_limit`。
- 当前账号无法直接读取 `huanlongAI/hl-contracts`，#29/#30/#34/#35/#36 的细节只能基于 `hl-dispatch#39/#40/#80` 中可见回填对齐。
- 当前账号对 `hl-dispatch` 的权限已由管理侧提升为 `write`，本报告已通过 `codex/pm-cui-tiantian-readiness` 分支提交 PR。

## 9. 边界确认

本报告仅作为 readiness evidence。

本轮未启动正式能力包，未修改 `hl-contracts`，未写代码，未注册 reason_code，未写 OpenAPI / facts / events / registry，未授权工程开工。
