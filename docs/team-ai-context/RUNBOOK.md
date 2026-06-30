# Team AI Context Runbook

Date: 2026-06-29

Status: RUNBOOK_REPO_SSOT_ACTIVE

## 中文摘要

本文是唤龙团队 AI 上下文工程 v0.3 当前阶段的本地运行手册。它只描述 `hl-dispatch` 内已合入的 dry-run 能力和计划推进动作，不授权外部发送、生产发布、Context Atlas 实体写入、required check 或 `ai_loop_control` 实现。

## 术语说明

- 本地运行：只在本机和 repo 文件中生成结果，不写 GitHub / 飞书 / 云效 / Context Atlas / team-memory。
- 准入结果：`ACCEPT`、`REJECT`、`REVIEW_REQUIRED` 三种决定。
- 机器回执：由可信控制面生成的 receipt；模型声明不能替代机器回执。
- 收口：把已发生的 GitHub / CI / merge 事实回写到 repo 状态文件。
- GitHub SSOT Dependency Sweep：在 owner/action 回填、状态推进、飞书提醒或 Founder 简报前，先扫 principal Issue/PR 与跨仓依赖；当前只做 dry-run / warn-only。

## 本地命令

### 生成 session package

输出包会携带 `required_context_artifacts`、`identity_resolution_rules` 和 `required_preflight_checks`。执行器必须读取 `docs/team-ai-context/CORE-IDENTITIES.md`，并把 `xinzhehui -> NODE-D` 识别为 AI 路由，不得等待普通 GitHub / 飞书账号。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py start \
  --task-id HL-AI-C1 \
  --goal "派发 server_deployment 给 ops，并先走本地 dry-run。" \
  --actor codex \
  --repo huanlongAI/hl-dispatch
```

### GitHub SSOT Dependency Sweep dry-run

`hl-ai start` 当前会把 `required_preflight_checks.github_ssot_dependency_sweep` 写入 session package 和所有 adapter input package。该预检只提醒执行器补扫依赖，不会阻塞命令、不写外部系统、不成为 GitHub required check。

执行器在以下动作前必须人工使用该合同复核 GitHub SSOT：

- owner/action 回填。
- 状态从等待推进到 ready / blocked / needs decision。
- 飞书私聊提醒投影。
- Founder 简报。

最小复核规则：

- 必须使用完整跨仓引用格式，例如 `huanlongAI/hl-platform#142`，不得让裸 `#142` 或 `#156` 被当前仓库自动解析。
- principal `huanlongAI/hl-dispatch#281` 必须补扫 `huanlongAI/hl-platform#142`，确认 auth / route / BFF 前置意见是否仍影响 smoke。
- 若只有 image 或 artifact 准备好，状态写为 `READY_FOR_SMOKE_IMAGE_ONLY`。
- 若 auth / route / BFF 方案仍缺报告，状态写为 `WAITING_AUTH_ROUTE_BFF_GAP_REPORT`。
- 若发现新 scope、权限、生产、凭证或验收边界变化，再输出 Founder 裁决简报。

### 提交候选输出到准入闸

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py submit \
  --session docs/team-ai-context/fixtures/stage-c/session-package.json \
  --candidate docs/team-ai-context/fixtures/stage-c/github-issue-candidate.json \
  --snapshot docs/team-ai-context/fixtures/stage-c/fresh-snapshot.json \
  --now 2026-06-25T00:10:00Z
```

### 生成 Landing intake 本地 outbox

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py execute \
  --bundle <hl-change-bundle-v1.json> \
  --outbox /tmp/hl-landing-outbox
```

### 读取 Landing 机器回执

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py readback \
  --receipt <hl-landing-receipt-v1.json>
```

### 按 closure policy 本地判断关闭

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py close \
  --receipt <hl-landing-receipt-v1.json> \
  --closure-policy POLICY_CLOSE
```

## 验证命令

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-ai-cli.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-ai-admission-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-team-assignment-publisher.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-exporter.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-github-language-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_context_engineering_templates.py
git diff --check
```

若修改正式中文文档，运行 Sentinel D-12：

```bash
python3 /Users/tzhEngineering/Workspace/01_Repos/huanlong/sentinel-shared/scripts/check-pr-doc-readability.py \
  --config .sentinel/config.yaml \
  --mode enforce
```

若修改 `AGENTS.md` 或投影入口规则，运行 Sentinel D-10 / AGENTS 治理漂移检查；若本地没有命令，必须在最终报告中列为远端 CI gap。

## 失败处理

| 现象 | 处理 |
|---|---|
| snapshot 过期 | 重新生成或刷新快照；不得复用旧回执 |
| 缺 admission receipt | fail closed，不发布正式产出 |
| candidate action 尝试外部发布 | fail closed，提交裁决简报 |
| `REVIEW_REQUIRED` | 不自行补职责或授权，交由 Founder / Gate |
| `LANDING_DONE` 但 `VALUE_SLICE_NOT_CLOSED` | 不关闭业务价值切片 |
| 文档中文可读性失败 | 补充中文摘要、术语说明和明确边界 |

## 禁止事项

- 不把 CI green 解释为生产授权。
- 不把 Issue assignee 解释为实现授权。
- 不把 PM readiness 解释为 runtime / release 授权。
- 不把飞书提醒或已读解释为 GitHub SSOT。
- 不把 Obsidian 或 team-memory 投影视为动态状态真源。
- 不复制完整动态快照正文到正式产物。
- 不把 `LANDING_DONE` 解释为 `VALUE_SLICE_CLOSED`。

## 暂停条件

需要 push、PR、合并、删除远端分支、GitHub Issue/comment 写入、飞书/邮件/云效/Bitable 外部发送、凭证、生产数据、权限扩大、branch protection、required check、Context Atlas 实体写入、`ai_loop_control` 实现、team-memory approved knowledge、破坏性操作、NODE-F、R phase、rollback route、route/profile/settings/registry 变更时暂停，并先输出中文裁决简报。
