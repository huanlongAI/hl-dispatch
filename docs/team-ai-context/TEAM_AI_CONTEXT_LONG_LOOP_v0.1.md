# Team AI Context Long Loop v0.1

Date: 2026-06-25

Status: LONG_LOOP_LOCAL_TRACKER_ACTIVE

## 中文摘要

本文把唤龙团队 AI 上下文工程剩余步骤重规划为长程闭环。当前闭环只在 `hl-dispatch` 本地 repo file 和 dry-run 脚本中生效，不代表总计划完结，不代表 `TEAM-CONTEXT-ENFORCED`，不代表 required check、云效、Context Atlas 或生产链路已经启用。

## 当前状态分层

```yaml
schema: team-ai-context-long-loop:v0.1
repo: huanlongAI/hl-dispatch
status: LONG_LOOP_LOCAL_TRACKER_ACTIVE
team_context_enforced: false
github_required_check_enabled: false
external_writes_enabled: false
context_atlas_entity_written: false
ai_loop_control_implemented: false
next_recommended_entry: STAGE_C_TEAM_ENTRY_LOCAL_CLI_DRY_RUN
```

## 长程闭环

| 阶段 | 状态 | 目标 | 退出证据 |
|---|---|---|---|
| Stage B-A | done | 本地 `AI_ADMISSION_GATE` dry-run | [huanlongAI/hl-dispatch#405](https://github.com/huanlongAI/hl-dispatch/pull/405) |
| Stage B-B | done | 正式 publisher 可接 admission gate | [huanlongAI/hl-dispatch#406](https://github.com/huanlongAI/hl-dispatch/pull/406) |
| Stage B-C | done | Tracker / Decisions / 验收矩阵 repo file | [huanlongAI/hl-dispatch#407](https://github.com/huanlongAI/hl-dispatch/pull/407) |
| Stage C-1 | active | `hl-ai start` / `hl-ai submit` 本地团队入口 | `scripts/hl-ai.py`、`scripts/test-hl-ai-cli.py` |
| Stage C-2 | active | session package 与 adapter input package 样例 | `docs/team-ai-context/fixtures/stage-c/` |
| Stage C-3 | active | negative regression 第一批 | `scripts/test-hl-ai-cli.py` |
| Stage D | deferred | Context Atlas `huanlong_platform` slice | future_condition_triggered_decision |
| Stage E | deferred | `ai_loop_control` 状态机 | future_condition_triggered_decision |
| Stage F | deferred | GitHub required check / 云效挂载 | future_condition_triggered_decision |
| Stage G | deferred | 两周试运行与全面启用 | future_condition_triggered_decision |

## 已裁决

- Stage B 写入限 `hl-dispatch`。
- 正式 AI 输出范围按方案 4.1。
- TTL30 / WIP4。
- GitHub 最小硬闸先 dry-run；required check 另裁决。
- Context Atlas 只允许未来在现有 `huanlong_platform` 加 slice，不新建 View。
- `ai_loop_control` 暂缓，仅定义接口和证据契约。
- 本地实施允许；push / PR / merge 另裁决。

## 等待 owner/action

当前唯一 owner：NODE-E / dahuizi。

当前唯一动作：完成 Stage C 本地 CLI dry-run、样例包、负向回归和状态记录。

当前真实阻塞：无本地阻塞；远端发布、跨仓写入、外部系统挂载都不是当前动作。

## 未来条件触发裁决

| 条件 | 裁决事项 |
|---|---|
| Stage C 本地测试和文档完成 | 是否允许 push / PR |
| 进入真实团队试运行 | 是否允许创建 GitHub Issue 或团队入口 |
| 需要写 Context Atlas 实体 | 是否允许写 `_infra/tzh-context-atlas` 或相关仓 |
| 需要实现 `ai_loop_control` | 确认仓库、状态机范围和写入边界 |
| dry-run 证据连续稳定 | 是否启用 GitHub required check |
| 需要云效或生产链路 | 是否进入正式挂载阶段 |

## 不得误判为生效

- CI green 不等于团队上下文全面生效。
- PR merge 不等于 production/runtime 授权。
- 飞书送达、Issue 指派或 PM readiness 不等于 `TEAM-CONTEXT-ENFORCED`。
- Stage C 的本地 receipt 不等于 required check。
