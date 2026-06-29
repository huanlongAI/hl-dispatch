# Team AI Context Tracker

Date: 2026-06-29

Status: TRACKER_REPO_SSOT_ACTIVE

## 中文摘要

本文记录唤龙团队 AI 上下文工程 v0.3 的阶段状态、证据和下一动作。Tracker 只记录里程碑、PR、验证和缺口，不复制完整运行日志。当前系统仍处于本地 dry-run 与 repo file 生效阶段，不是 `TEAM-CONTEXT-ENFORCED`。

## 术语说明

- done：已有 repo file、脚本、测试或 GitHub 合并证据。
- partial：已有局部能力，但未覆盖上线验收完整语义。
- not_started：当前无实现证据。
- deferred：已明确暂缓或只能在未来条件触发后裁决。
- blocker：当前唯一真实阻塞，不包括尚未触发的未来事项。

## 当前状态

```yaml
schema: team-ai-context-tracker:v0.3
status: TRACKER_REPO_SSOT_ACTIVE
current_state: CONTEXT_ENTRY_IMPLEMENTED_LOCAL_DRY_RUN
team_context_enforced: false
next_owner: NODE-E / dahuizi
next_action: STAGE_D_CONTEXT_ATLAS_SLICE_DECISION_PACKAGE
blocker: Founder decision required before Context Atlas entity write
```

## 阶段追踪

| 阶段 | 状态 | 证据 | 下一动作 |
|---|---|---|---|
| Stage A 只读评审 | done | Founder 选择推荐方案 A | 无 |
| Stage B-A 准入闸 dry-run | done | [huanlongAI/hl-dispatch#405](https://github.com/huanlongAI/hl-dispatch/pull/405) | 无 |
| Stage B-B publisher 接入 | done | [huanlongAI/hl-dispatch#406](https://github.com/huanlongAI/hl-dispatch/pull/406) | 无 |
| Stage B-C 状态收敛 | done | [huanlongAI/hl-dispatch#407](https://github.com/huanlongAI/hl-dispatch/pull/407) | 仅保留历史快照 |
| Stage C 本地团队入口 | done | [huanlongAI/hl-dispatch#415](https://github.com/huanlongAI/hl-dispatch/pull/415) | 无 |
| Stage C Landing client 收敛 | done | [huanlongAI/hl-dispatch#418](https://github.com/huanlongAI/hl-dispatch/pull/418) | 无 |
| Stage D Context Atlas slice | not_started | 仅有 D5 裁决和接口边界 | 准备裁决包，确认是否允许写 `_infra/tzh-context-atlas` |
| Stage E `ai_loop_control` | not_started | 仅有 evidence contract | 只读确认仓库和状态机边界 |
| Stage F required check / 云效 | not_started | 无 | 等 dry-run 与试运行证据后单独裁决 |
| Stage G 试运行与全面启用 | not_started | 无 | 等 Stage D-F 最小链路完成 |
| Stage H 自动化与知识投影 | deferred | 无 | 仅在 `TEAM-CONTEXT-ENFORCED` 后推进 |

## 验收追踪

| 分组 | 状态 | 说明 |
|---|---|---|
| A. 计划与真源 | done | 本文件组建立 repo SSOT；需后续 PR 合入 main 才远端生效 |
| B. 快照 | partial | 本地策略已有；正式发布前硬校验未强制 |
| C. 复合准入闸 | partial | 本地 dry-run 已有；required check 和云效未挂载 |
| D. 团队入口 | partial | CLI 本地入口已有；未团队试运行 |
| E. Context Atlas | not_started | 未写实体 |
| F. `ai_loop_control` | not_started | 未实现状态机 |
| G. 负向回归 | partial | 第一批已有；完整 26 项未覆盖 |
| H. 试运行 | not_started | 无两周和 20 次统计 |
| I. 全面启用 | deferred | 需要 Stage D-G 证据 |

## 当前唯一下一动作

准备 Stage D Context Atlas slice 裁决包。该动作在当前仓内只允许形成方案、边界和验证计划；真正写 `_infra/tzh-context-atlas` 或其他仓库必须另行裁决。
