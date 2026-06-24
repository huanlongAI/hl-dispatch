# Team AI Context Stage B-C Status v0.1

Date: 2026-06-24

Status: STAGE_BC_TRACKER_DECISION_STATE_LOCAL

## 中文摘要

本文是唤龙团队 AI 上下文工程 Stage B-C 的本地状态、Tracker 和 Decisions 记录。它只在 `hl-dispatch` 仓库内收敛已合并的 Stage B-A / B-B 证据、上线验收清单差距和下一执行入口，不启用 GitHub required check，不修改分支保护，不写飞书、多维表格、云效、team-memory 或 Context Atlas 实体。

当前结论：Stage B 已完成本地 dry-run 基础设施和正式发布器预检接入；尚未达到 `TEAM-CONTEXT-ENFORCED`。下一阶段应先进入团队入口和试运行准备，而不是直接启用 required check 或云效正式挂载。

## 术语说明

- Stage B-A：本地 `AI_ADMISSION_GATE`、`engineering-command-snapshot:v0.2`、TTL30/WIP4 和基础负向测试落地阶段。
- Stage B-B：正式发布器 dry-run 接入 `AI_ADMISSION_GATE` 的阶段。
- Stage B-C：本文件定义的状态收敛阶段，目标是把验收状态、待办队列和后续裁决点落到 repo file。
- Tracker：本文件中的分阶段待办表，只是本地计划和状态记录，不创建 GitHub Issue。
- Decisions：已经由 Founder 明确选择并在本阶段回读的裁决，不得重复要求同一裁决。
- 暂缓项：已有裁决或边界要求当前不得实施的能力，只记录未来触发条件。

## 当前状态

```yaml
schema: team-ai-context-stage-status:v0.1
status: STAGE_BC_TRACKER_DECISION_STATE_LOCAL
repo: huanlongAI/hl-dispatch
local_repo_path: /Users/tzhEngineering/Workspace/01_Repos/huanlong/hl-dispatch
current_truth_file: docs/team-ai-context/TEAM_AI_CONTEXT_STAGE_BC_STATUS_v0.1.md
supporting_contract: docs/team-ai-context/AI_ADMISSION_GATE_v0.1.md
formal_publisher_doc: docs/team-context/README.md
github_required_check_enabled: false
branch_protection_changed: false
external_writes_enabled: false
team_context_enforced: false
next_recommended_entry: STAGE_C_TEAM_ENTRY_LOCAL_CLI_DRY_RUN
```

## 已裁决事项

| ID | 裁决 | 当前投影 | 证据 |
|---|---|---|---|
| D1 | Stage B 写入限 `hl-dispatch` | 已遵守 | PR #405、PR #406 均只改 `hl-dispatch` |
| D2 | 正式 AI 输出范围按方案 4.1 | 已投影到 gate 文档和脚本 | `docs/team-ai-context/AI_ADMISSION_GATE_v0.1.md` |
| D3 | TTL30 / WIP4 | 已进入 snapshot policy | `scripts/export-hl-progress.py`、`scripts/ai-admission-gate.py` |
| D4 | GitHub 最小硬闸先 dry-run，required check 另裁决 | 已遵守 | PR #405、PR #406 未改 branch protection 或 required check |
| D5 | Context Atlas 只在现有 `huanlong_platform` 加 slice，不新建 View | 当前只定义 slice contract，未写 Atlas 实体 | `docs/team-ai-context/AI_ADMISSION_GATE_v0.1.md` |
| D6 | `ai_loop_control` 暂缓，仅定义接口/证据契约 | 已遵守 | `ai-loop-control-evidence:v0.1` 仅为接口说明 |
| D7 | 允许本地实施，push 另裁决 | 已按两次 Founder 后续裁决完成 PR #405、#406 | PR #405、PR #406 |
| D8 | Stage B-B 限 `hl-dispatch`，不启用 required check | 已遵守 | PR #406 |

## 合并证据

| PR | 内容 | Merge commit | Checks | 状态 |
|---|---|---|---|---|
| #405 | Stage B-A：snapshot v0.2、AI admission gate、本地 dry-run 基础设施 | `49ea77762854bed4e21f31715f5916e679f97808` | `sentinel` success、`context-engineering-template-gate` success、`scan` success | MERGED |
| #406 | Stage B-B：正式发布器 dry-run 接入 `AI_ADMISSION_GATE` | `73f722674e6daf630db76e074755a15bbbda7cf6` | `sentinel` success、`scan` success | MERGED |

## 上线验收矩阵

状态枚举：

- `done`：已有 repo file、脚本、测试或 GitHub 回读证据。
- `partial`：已有局部能力，但未覆盖清单完整语义。
- `deferred`：已明确暂缓或需要后续 Founder 裁决。
- `not_started`：当前无本地实现证据。

| 分组 | 当前状态 | 已有证据 | 主要缺口 |
|---|---|---|---|
| A. 计划与真源 | partial | 本文件创建 current status / Tracker / Decisions；PR #405/#406 为 GitHub merge evidence | 全局总计划尚未迁入 repo SSOT；其他仓库链接策略仍未正式落地 |
| B. 快照 | partial | `engineering-command-snapshot:v0.2`、TTL30、WIP4、source coverage、completeness、receipt、expired negative test | 发布前重新校验只在本地 dry-run hook 中覆盖；候选误发布负向测试仍需扩展 |
| C. 复合准入闸 | partial | `AI_ADMISSION_GATE` 输出 `ACCEPT / REJECT / REVIEW_REQUIRED`，支持 receipt 绑定、防重放、本地预检、发布器 fail closed | 无 GitHub required check、无云效挂载、无人工例外完整流程、敏感过滤仍是规则级而非全路径扫描 |
| D. 团队入口 | not_started | 无 | 缺 `hl-ai start`、`hl-ai submit`、会话包、Codex / Claude / 浏览器 AI 薄适配器 |
| E. Context Atlas | deferred | 已定义只允许现有 `huanlong_platform` slice contract | 未写 Atlas slice、无版本回执、无 Usage Summary 扩展 |
| F. `ai_loop_control` | deferred | 已定义 evidence contract | 未确认实际仓库与能力；无状态机、成本记录、merge-readback |
| G. 负向回归 | partial | 已覆盖快照过期、receipt 绑定、敏感授权缺失、unsupported surface、发布器 fail closed | 缺跨仓重放、基线变化、输出变化、候选动作、PM readiness、CI green、飞书提醒、Issue assignee、merge-readback 等负向项 |
| H. 试运行 | not_started | 无 | 缺三名成员、三类任务、20 次正式运行、两周连续统计和误拒/例外数据 |
| I. 全面启用 | deferred | 无 | required check、云效正式挂载、旧绕过路径关闭、团队培训、运行心跳、正式生效记录均需后续裁决 |

## Tracker

| 阶段 | 状态 | 目标结果 | 退出证据 | 边界 |
|---|---|---|---|---|
| Stage B-C | done | 当前状态、Decisions、Tracker、A-I 验收矩阵落到 repo file | 本文件存在；本地测试和 Sentinel 通过 | 只写 `hl-dispatch` repo file |
| Stage C-1 | queued | 设计 `hl-ai start` / `hl-ai submit` 本地 CLI dry-run 合同 | CLI 输入输出 contract、fixtures、tests | 不创建外部 Issue，不写飞书 |
| Stage C-2 | queued | 生成本地会话包与 AI adapter 输入包 | session package fixture、Codex/Claude adapter thin docs/tests | 不接真实账号、凭证或浏览器自动化 |
| Stage C-3 | queued | 扩展负向回归第一批 | 至少覆盖跨任务/跨仓/输出变化/候选动作误发布 | 不启用 required check |
| Stage D | deferred | Context Atlas `huanlong_platform` slice 实体接入 | Atlas 版本回执和 Usage Summary | 需要另行确认 Atlas 写入边界 |
| Stage E | deferred | `ai_loop_control` 状态机和 merge-readback | 状态机测试、成本记录、readback evidence | 需要确认实际仓库与实现授权 |
| Stage F | deferred | required check / 云效正式挂载 | GitHub branch protection / 云效挂载证据 | 需要 Founder 单独裁决 |
| Stage G | deferred | 两周试运行与全面启用 | 20 次运行统计、误读为 0、状态更新为 `TEAM-CONTEXT-ENFORCED` | 需要团队运行数据 |

## 下一执行入口

推荐下一入口：`STAGE_C_TEAM_ENTRY_LOCAL_CLI_DRY_RUN`。

目标结果：

1. 在 `hl-dispatch` 内设计 `hl-ai start` 和 `hl-ai submit` 的本地 dry-run contract。
2. 让成员用自然语言目标生成 session package，而不是手写 YAML。
3. CLI 输出只作为 `AI_ADMISSION_GATE` 输入，不写 GitHub、不发飞书、不触发云效。
4. 覆盖最小测试：普通 GitHub Issue 发布候选、过期 snapshot、缺 admission receipt、候选动作误发布。

暂停条件：

- 需要 push、PR、合并、GitHub Issue / comment 写入或外部发送；
- 需要启用 required check、修改 branch protection 或云效挂载；
- 需要写 Context Atlas 其他仓、team-memory approved knowledge 或 `ai_loop_control` 实现；
- 需要生产数据、凭证、权限扩大、NODE-F、R phase、rollback route 或 route/profile/settings/registry 变更。

## 未来条件触发裁决

这些不是当前阻塞，只在条件出现时再提交裁决简报：

| 条件 | 需要裁决的事项 |
|---|---|
| Stage C 本地 CLI contract 和测试通过 | 是否允许 push / PR |
| Stage C 进入真实团队使用 | 是否允许创建 GitHub Issue 或团队试运行入口 |
| 需要 Context Atlas 写入实体 slice | 是否允许写 `_infra/tzh-context-atlas` 或相关仓 |
| 需要 `ai_loop_control` 实现 | 确认实际仓库、状态机范围和写入边界 |
| dry-run 连续试运行证据足够 | 是否启用 GitHub required check |
| 需要云效或生产链路挂载 | 是否进入正式挂载阶段 |

## 未验证 gap

- 未读取或写入 Context Atlas 实体，只有 `hl-dispatch` 中的接口和状态投影。
- 未执行团队试运行，无法证明 H 组指标。
- 未检查 GitHub branch protection 设置，因为当前目标禁止启用或修改 required check。
- 未触发任何外部系统写入。
