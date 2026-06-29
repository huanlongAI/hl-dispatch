# Team AI Context Rollout

Date: 2026-06-29

Status: ROLLOUT_REPO_SSOT_ACTIVE

## 中文摘要

本文定义唤龙团队 AI 上下文工程 v0.3 从当前本地 dry-run 到全面启用的分阶段 rollout。当前 rollout 不授权写 Context Atlas、云效、飞书、team-memory、生产链路或 `ai_loop_control`；这些只在对应阶段触发后用裁决简报推进。

## 术语说明

- rollout：从本地能力逐步进入团队试运行和正式强制的发布路径。
- pilot：小范围试运行，要求成员、任务类型、次数和连续时间都有统计。
- rollback：阶段失败时撤回该阶段强制能力，保留只读证据。
- fail closed：门禁不可用、回执缺失或授权不清时，正式产出不能发布。

## 当前起点

```yaml
current_state: CONTEXT_ENTRY_IMPLEMENTED_LOCAL_DRY_RUN
source_of_truth: docs/team-ai-context/PLAN-v0.3.md
team_context_enforced: false
next_stage: Stage D
```

## Stage D：Context Atlas 条件切片

目标：在不新建 View 的前提下，为现有 `huanlong_platform` 设计并准备 `engineering_command_context` slice。

准入条件：

- `PLAN-v0.3.md`、`TRACKER.md`、`DECISIONS.md` 已合入 main。
- Founder 裁决允许读取并可能写入 Context Atlas 目标仓。
- 已确认目标仓 AGENTS / CLAUDE / schema / validator。

退出证据：

- slice schema 或配置变更。
- Atlas 版本回执。
- Usage Summary 扩展或明确 gap。
- rollback 说明。

暂停条件：需要写 `_infra/tzh-context-atlas`、新建 View、扩大上下文权限或触碰凭证时暂停并提交裁决简报。

## Stage E：`ai_loop_control` 最小状态机

目标：实现或接入唤龙工程指挥循环的最小状态机，首个自动循环只覆盖 merge-readback。

最小状态：

```text
DRAFT
CONTEXT_RESOLVING
CONTEXT_READY
AI_RUNNING
OUTPUT_READY
GATE_VALIDATING
REVIEW_REQUIRED
READY_TO_PUBLISH
PUBLISHED
EXECUTING
EVIDENCE_COLLECTED
READBACK_PENDING
COMPLETED
LEARNING_PATCH_REQUIRED
```

退出证据：

- 状态机测试。
- 运行回执。
- 成本记录。
- merge-readback evidence。

暂停条件：未确认真实仓库、需要生产权限、需要外部发送、需要 Agent Manager 身份变更时暂停。

## Stage F：GitHub required check / 云效挂载

目标：让同一 `AI_ADMISSION_GATE` 在正式入口 fail closed，不另写规则。

GitHub 最小硬闸范围：

- 缺回执。
- 过期快照。
- 回执不匹配。
- 敏感信息。
- 明确授权越界。
- 候选动作误发布。
- 正式任务内嵌动态快照正文。

云效挂载范围：

- 先查清工作项创建或流水线前置入口。
- 只接同一校验器。
- 不复制规则。

退出证据：

- required check 或 dry-run required-check 证据。
- 云效挂载设计或执行证据。
- 失败关闭与人工例外流程。
- 回滚演练记录。

暂停条件：修改 branch protection、required check、云效配置、生产发布路径或权限时必须裁决。

## Stage G：小范围试运行与全面启用

试运行范围：

- 成员：大辉子、技术总监、一名后端或产品负责人。
- 任务：工程主线盘点、Issue / PR 对账和合并回读、团队任务拆分与派发。
- 规模：至少 20 次正式 AI 运行，至少连续两周。

晋级指标：

- 负向回归 100%。
- 过期快照正式使用 0。
- 授权误读 0。
- 候选动作误发布 0。
- 无回执正式产出 0。
- 已知职责越界 0。
- 禁止来源误用 0。
- 敏感信息泄漏 0。
- 门禁绕过成功 0。
- 合并回读完成率 100%。
- 误拒率和人工例外率可测。
- 启动耗时和手工找资料时间下降。

通过后状态：`TEAM-CONTEXT-PILOT-PASSED`。全面强制完成后状态：`TEAM-CONTEXT-ENFORCED`。

## 回滚策略

每一阶段必须可独立回滚：

- 关闭 GitHub 必需检查。
- 禁用统一入口发布能力。
- 恢复人工发布。
- 保留只读日志和证据。
- 不回滚职责或授权真源。
- 不删除已生成回执和运行记录。
