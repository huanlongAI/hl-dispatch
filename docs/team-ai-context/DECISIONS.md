# Team AI Context Decisions

Date: 2026-06-29

Status: DECISIONS_REPO_SSOT_ACTIVE

## 中文摘要

本文记录唤龙团队 AI 上下文工程 v0.3 已裁决事项、当前投影和未来条件触发裁决。已裁决事项不得重复提交；未来事项只有在新证据、范围变化、阻塞或准备实施时再提交 Founder 裁决简报。

## 术语说明

- 已裁决：Founder 已给出选择，执行时只需按边界落实。
- 当前投影：该裁决在当前 repo 状态中的实际表现。
- 未来条件触发裁决：现在不是阻塞，只有条件出现后才进入裁决。
- 裁决简报：需要选择、批准、确认或授权时的中文结构化说明。

## 已裁决

| ID | 裁决 | 当前投影 | 证据 |
|---|---|---|---|
| D1 | Stage B / 当前本地实施限 `hl-dispatch` | 已遵守 | [huanlongAI/hl-dispatch#405](https://github.com/huanlongAI/hl-dispatch/pull/405)、[huanlongAI/hl-dispatch#406](https://github.com/huanlongAI/hl-dispatch/pull/406)、[huanlongAI/hl-dispatch#407](https://github.com/huanlongAI/hl-dispatch/pull/407)、[huanlongAI/hl-dispatch#415](https://github.com/huanlongAI/hl-dispatch/pull/415)、[huanlongAI/hl-dispatch#418](https://github.com/huanlongAI/hl-dispatch/pull/418) 均限 `hl-dispatch` |
| D2 | 正式 AI 输出范围按方案 4.1 | 已写入计划和 `AI_ADMISSION_GATE` | `PLAN-v0.3.md`、`AI_ADMISSION_GATE_v0.1.md` |
| D3 | TTL30 / WIP4 | 已作为当前运行策略投影 | snapshot v0.2 与相关测试 |
| D4 | GitHub 最小硬闸先 dry-run，required check 另裁决 | 未启用 required check | `github_required_check_enabled: false` |
| D5 | Context Atlas 只在现有 `huanlong_platform` 加 slice，不新建 View | 当前未写实体，仅保留未来边界 | Stage D 未开始 |
| D6 | `ai_loop_control` 暂缓，仅定义接口 / 证据契约 | 未实现状态机 | Stage E 未开始 |
| D7 | 允许本地实施，push 前另裁决 | 既往 push / PR / merge 已逐项裁决完成 | [huanlongAI/hl-dispatch#405](https://github.com/huanlongAI/hl-dispatch/pull/405)、[huanlongAI/hl-dispatch#406](https://github.com/huanlongAI/hl-dispatch/pull/406)、[huanlongAI/hl-dispatch#407](https://github.com/huanlongAI/hl-dispatch/pull/407)、[huanlongAI/hl-dispatch#415](https://github.com/huanlongAI/hl-dispatch/pull/415)、[huanlongAI/hl-dispatch#418](https://github.com/huanlongAI/hl-dispatch/pull/418) |
| D8 | Landing client 入口收敛可合入 | 已合入 main | [huanlongAI/hl-dispatch#418](https://github.com/huanlongAI/hl-dispatch/pull/418) |

## 当前状态约束

- `team_context_enforced: false`
- `github_required_check_enabled: false`
- `external_writes_enabled: false`
- `context_atlas_entity_written: false`
- `ai_loop_control_implemented: false`
- `pilot_started: false`

这些状态不是待裁决项本身；它们只是当前未生效事实。

## 未来条件触发裁决

| 条件 | 裁决事项 | 推荐准备材料 |
|---|---|---|
| 准备写 Context Atlas 实体 | 是否允许在现有 `huanlong_platform` 增加 `engineering_command_context` slice | schema / validator / rollback / Usage Summary 计划 |
| 准备实现 `ai_loop_control` | 确认实际仓库、状态机范围、成本记录和 merge-readback | 只读仓库事实、状态机契约、最小实现边界 |
| dry-run 证据稳定 | 是否启用 GitHub required check | 失败关闭清单、豁免流程、回滚方案 |
| 云效入口查清 | 是否挂载云效前置校验 | 云效创建路径、权限、失败关闭和回滚 |
| 准备真实团队试运行 | 是否创建 GitHub Issue 或团队入口 | 成员、任务类型、运行统计模板 |
| 试运行达标 | 是否进入 `TEAM-CONTEXT-ENFORCED` | 两周数据、20 次运行、误拒和例外指标 |

## 裁决简报要求

任何 push、PR 创建、合并、删远端分支、外部发送、权限扩大、生产数据、required check、branch protection、Context Atlas 写入、`ai_loop_control` 实现、team-memory approved knowledge、route/profile/settings/registry、NODE-F、R phase 或 rollback route 事项，都必须先输出中文裁决简报。
