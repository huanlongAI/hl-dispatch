# Team AI Context Plan v0.3

Date: 2026-06-29

Status: PLAN_REPO_SSOT_ACTIVE

## 中文摘要

本文是唤龙团队 AI 上下文工程与复合准入系统 v0.3 在 `hl-dispatch` 的 repo SSOT。原始上传包 `00-唤龙团队AI上下文工程总实施计划-v0.3.md` 是来源材料；自本文合入后，`docs/team-ai-context/PLAN-v0.3.md` 是团队 AI 上下文工程的计划真源，`TRACKER.md`、`DECISIONS.md`、`ROLLOUT.md` 和 `RUNBOOK.md` 是配套执行真源。

当前状态不是 `TEAM-CONTEXT-ENFORCED`。截至本文日期，已生效范围只限 `hl-dispatch` 内本地 dry-run、repo file、CLI contract、fixtures 和测试；GitHub required check、云效、Context Atlas 实体、team-memory、飞书、多维表格、生产链路和 `ai_loop_control` 状态机均未启用。

## 术语说明

- repo SSOT：仓库内唯一计划真源；后续状态以本目录文件为准，不再依赖 Downloads 上传包。
- 复合准入：同一道 `AI_ADMISSION_GATE` 同时检查上下文、职责、授权、任务绑定、输出契约、安全和发布面。
- 正式 AI 产出：准备进入共享、权威、执行或审计系统，并可能改变团队行为、工程状态、发布状态、产品承诺或治理判断的 AI 产出。
- dry-run：只在本地生成和校验结果，不执行外部写入。
- required check：GitHub 分支保护里的必过检查；当前未启用。
- `TEAM-CONTEXT-ENFORCED`：所有正式发布路径强制使用统一上下文与准入规则；当前为 false。

## 权威文件

| 文件 | 责任 |
|---|---|
| `docs/team-ai-context/PLAN-v0.3.md` | 总计划与目标架构 |
| `docs/team-ai-context/TRACKER.md` | 阶段状态、证据、下一动作 |
| `docs/team-ai-context/DECISIONS.md` | Founder 已裁决事项和未来条件触发裁决 |
| `docs/team-ai-context/ROLLOUT.md` | Stage D-G 推进、试运行、全面启用和回滚计划 |
| `docs/team-ai-context/RUNBOOK.md` | 本地运行、验证、门禁、异常处理 |
| `docs/team-ai-context/AI_ADMISSION_GATE_v0.1.md` | 准入闸接口和证据契约 |
| `docs/team-ai-context/CORE-IDENTITIES.md` | 团队 AI 启动必须读取的核心身份和 AI 路由事实 |
| `docs/team-ai-context/TEAM_AI_CONTEXT_LONG_LOOP_v0.1.md` | 长程闭环状态摘要 |

历史阶段文件保留为证据，不再作为唯一当前真源。

## 当前状态

```yaml
schema: team-ai-context-plan:v0.3
repo: huanlongAI/hl-dispatch
plan_status: PLAN_REPO_SSOT_ACTIVE
current_operating_state: CONTEXT_ENTRY_IMPLEMENTED_LOCAL_DRY_RUN
team_context_enforced: false
github_required_check_enabled: false
branch_protection_changed_by_this_plan: false
external_writes_enabled: false
context_atlas_entity_written: false
ai_loop_control_implemented: false
pilot_started: false
production_or_runtime_authorized: false
next_recommended_entry: STAGE_D_CONTEXT_ATLAS_SLICE_DECISION_PACKAGE
```

## 架构边界

| 信息 | 唯一真源 |
|---|---|
| GitHub Issue / PR 当前状态 | GitHub |
| 工程工作项与流水线执行 | 云效 |
| 工程指挥状态、职责、生命周期和授权规则 | `hl-dispatch` |
| 角色与人员映射 | `hl-dispatch` |
| 核心 AI 身份、节点路由和非人员 owner 解析 | `docs/team-ai-context/CORE-IDENTITIES.md` + PPR / AUM registries |
| 上下文发现、选择和装载规则 | `tzh-context-atlas` |
| AI 任务状态、轨迹、成本、重试和协调 | `ai_loop_control` |
| 业务契约 | `hl-contracts` |
| 工程实现 | 对应源代码仓库 |
| 团队共享知识 | team-memory |
| 个人查阅与可视化 | Obsidian |

`hl-dispatch` 不复制 Context Atlas 的完整上下文，不复制云效工作项，不复制 team-memory approved knowledge。Context Atlas 不保存动态快照正文，不成为角色或授权真源。`ai_loop_control` 不绕过 `AI_ADMISSION_GATE`，不自行裁决组织职责。

## 正式 AI 产出范围

正式 AI 产出包括：

- GitHub Issue、PR、正式评论和治理记录。
- 云效工作项、流水线参数和发布输入。
- 正式团队任务分派。
- 代码、配置、契约、迁移和发布候选。
- deploy、runtime、production、release。
- Payment、Provider、真实用户数据相关内容。
- 拟写入 team-memory approved knowledge 的内容。
- 任何对动态真源的写操作。

不包括：

- 本地探索对话。
- 未提交草稿。
- 明确标记为 sandbox 的实验。
- 不会进入共享系统的个人思考。

规则：探索可以无回执；探索准备进入正式系统时必须经过 `AI_ADMISSION_GATE`。

## 目标架构

```text
自然语言目标
  -> 团队 AI 工作入口
  -> 工程指挥快照与 Context Atlas 指针
  -> 统一会话包和回执骨架
  -> Codex / Claude / browser-ai
  -> 候选输出和复合回执
  -> AI_ADMISSION_GATE
  -> GitHub 治理或云效执行
  -> 合并回读与运行证据
  -> ai_loop_control 学习候选
```

## 分阶段计划

| 阶段 | 状态 | 目标 | 当前说明 |
|---|---|---|---|
| Stage A | done | 只读评审和裁决包 | 已完成并由 Founder 选择推荐方案 A |
| Stage B-A | done | 本地 `AI_ADMISSION_GATE` dry-run | [huanlongAI/hl-dispatch#405](https://github.com/huanlongAI/hl-dispatch/pull/405) |
| Stage B-B | done | 正式 publisher dry-run 接入准入闸 | [huanlongAI/hl-dispatch#406](https://github.com/huanlongAI/hl-dispatch/pull/406) |
| Stage B-C | done | Tracker / Decisions / 验收矩阵 repo file | [huanlongAI/hl-dispatch#407](https://github.com/huanlongAI/hl-dispatch/pull/407) |
| Stage C | done | 本地团队入口、session package、adapter input、核心身份装载、第一批负向回归 | [huanlongAI/hl-dispatch#415](https://github.com/huanlongAI/hl-dispatch/pull/415)、[huanlongAI/hl-dispatch#418](https://github.com/huanlongAI/hl-dispatch/pull/418) |
| Stage D | not_started | Context Atlas `huanlong_platform` 条件切片 | 只允许在未来裁决后写实体 |
| Stage E | not_started | `ai_loop_control` 状态机和 merge-readback | 当前只定义接口和证据契约 |
| Stage F | not_started | GitHub required check / 云效挂载 | 需要 Founder 单独裁决 |
| Stage G | not_started | 两周试运行、全面启用和生效记录 | 需要团队运行数据 |
| Stage H | deferred | 后续自动化与知识投影 | 仅在 `TEAM-CONTEXT-ENFORCED` 后逐步启用 |

## 上线验收矩阵

| 分组 | 当前状态 | 已有证据 | 主要缺口 |
|---|---|---|---|
| A. 计划与真源 | done | 本文件、`TRACKER.md`、`DECISIONS.md`、`ROLLOUT.md`、`RUNBOOK.md` | 需合入 main 后成为远端真源 |
| B. 快照 | partial | snapshot v0.2、TTL30、WIP4、source coverage、completeness、receipt、过期负向测试 | 发布前强制重新校验仍限本地 dry-run |
| C. 复合准入闸 | partial | `AI_ADMISSION_GATE`、receipt 绑定、防重放、本地预检、publisher fail closed | 无 required check、无云效挂载、人工例外流程未完整实现 |
| D. 团队入口 | partial | `hl-ai start`、`submit`、`execute`、`readback`、`close`、核心身份规则、fixtures、CLI tests | 仍未接真实团队使用和正式入口 |
| E. Context Atlas | not_started | 已有 slice 目标和边界 | 未写实体、无版本回执、无 Usage Summary |
| F. `ai_loop_control` | not_started | evidence contract | 未确认真实仓库能力、无状态机、无成本记录 |
| G. 负向回归 | partial | 已覆盖过期快照、缺 receipt、候选误发布、unsupported surface、Landing close 边界 | 缺完整 26 项负向回归 |
| H. 试运行 | not_started | 无 | 缺三名成员、三类任务、20 次、两周统计 |
| I. 全面启用 | deferred | 无 | required check、云效、旧绕过路径关闭、培训、心跳、生效记录 |

## 完成定义

总计划全部生效必须同时满足：

1. 所有正式 AI 任务使用统一准入规则。
2. 所有发布路径不可绕过。
3. 团队成员无需手工组装上下文。
4. 所有模型共用同一会话协议。
5. 正式产出绑定任务、仓库、分支、基线和输出。
6. 快照过期会被拒绝。
7. 候选动作不能直接发布。
8. 职责漏拆和越权被拒绝。
9. 授权不能被 PM、CI、提醒或指派推导。
10. Payment / Provider / production 需要明确 Founder/Gate 回执。
11. 敏感信息不会进入会话包和回执。
12. PR 合并自动进入回读。
13. 团队试运行指标达标。
14. 云效和 GitHub 使用同一准入逻辑。
15. team-memory / Obsidian 没有动态状态副本。
16. 运行心跳、失败通知和应急流程可用。
17. 全部实现、文档、测试、追踪和生效记录已合入相应主干。

## 非目标

首轮不做完整超级创始人应用界面、不做 Obsidian 动态工程状态库、不自动写飞书和 Bitable、不一次自动化所有循环、不为每种模型维护完整规则副本、不新建第三个 Context View、不由 AI 自行签发治理裁决、不把云效执行面迁移到 GitHub Actions、不让 Agent 接触真实凭证值。
