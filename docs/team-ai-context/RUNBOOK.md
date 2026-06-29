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

## 本地命令

### 生成 session package

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py start \
  --task-id HL-AI-C1 \
  --goal "派发 server_deployment 给 ops，并先走本地 dry-run。" \
  --actor codex \
  --repo huanlongAI/hl-dispatch
```

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
