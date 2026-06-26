# Team AI Context Stage C Entry v0.1

Date: 2026-06-25

Status: STAGE_C_LOCAL_TEAM_ENTRY_DRY_RUN

## 中文摘要

本文定义唤龙团队 AI 上下文工程 Stage C 的本地团队入口。Stage C 只在 `hl-dispatch` 内提供 `hl-ai start` / `hl-ai submit` dry-run 契约、会话包样例和 adapter 输入包；Landing v1.0 baseline approved 后，本入口新增 `hl-ai execute` / `hl-ai readback` / `hl-ai close` client 命令，但它们仍不写 GitHub、飞书、云效、Context Atlas、team-memory 或生产运行态。

Stage C 的目标不是启用 `TEAM-CONTEXT-ENFORCED`，而是让团队成员先用自然语言目标生成本地 session package，再把候选 AI 输出提交给 `AI_ADMISSION_GATE` 形成可审计结果。只有本地证据稳定后，后续 push / PR / required check / 云效 / Context Atlas / ai_loop_control 才进入新的 Founder 裁决。

## 术语说明

- `hl-ai start`：从自然语言目标生成本地 session package 的命令。
- `hl-ai submit`：把候选 AI 输出、本地 session package 和 snapshot 组装成 `AI_ADMISSION_GATE` 输入并 dry-run 校验的命令。
- `hl-ai execute`：把不可信 `hl-change-bundle:v1` 包装成本地 `hl-landing-intake:v1` outbox envelope；hl-ai execute 只生成本地 Landing intake，不触发 publication / integration。
- `hl-ai readback`：读取可信 Landing Control Plane 生成的 `hl-landing-receipt:v1` 机器回执。
- `hl-ai close`：只在机器回执满足 closure policy 时形成本地 close 结果；`LANDING_DONE` 不等于 `VALUE_SLICE_CLOSED`。
- session package：一次 AI 协作入口的本地会话包，包含目标、边界和 adapter 输入。
- adapter input package：给 Codex、Claude、browser-ai 等执行器读取的薄输入包。
- candidate action：候选输出声明的动作；任何外部发布动作都必须 fail closed 并等待裁决。

## CLI contract

### start

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py start \
  --task-id HL-AI-C1 \
  --goal "派发 server_deployment 给 ops，并先走本地 dry-run。" \
  --actor codex \
  --repo huanlongAI/hl-dispatch
```

输出：

- `schema: hl-ai-session-package:v0.1`
- `mode: dry_run`
- `adapter_input_packages`: `codex`、`claude`、`browser-ai`
- `next_allowed_action: submit_candidate_to_ai_admission_gate`
- `github_write.enabled: false`
- `external_writes: []`

### submit

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py submit \
  --session docs/team-ai-context/fixtures/stage-c/session-package.json \
  --candidate docs/team-ai-context/fixtures/stage-c/github-issue-candidate.json \
  --snapshot docs/team-ai-context/fixtures/stage-c/fresh-snapshot.json \
  --now 2026-06-25T00:10:00Z
```

输出：

- `schema: hl-ai-submit-result:v0.1`
- `status: admission_accepted | admission_rejected | admission_review_required | failed_closed`
- `admission_request.schema: ai-admission-request:v0.1`
- `admission_gate.gate: AI_ADMISSION_GATE`
- `github_write.enabled: false`
- `external_writes: []`

### execute

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py execute \
  --bundle <hl-change-bundle-v1.json> \
  --outbox /tmp/hl-landing-outbox
```

输出：

- `schema: hl-ai-execute-result:v1`
- `intake.schema: hl-landing-intake:v1`
- `status: accepted_local_outbox`
- `next_allowed_action: trusted_landing_control_plane_readback`
- `github_write.enabled: false`
- `external_writes: []`

### readback

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py readback \
  --receipt <hl-landing-receipt-v1.json>
```

输出：

- `schema: hl-ai-readback-result:v1`
- `landing_state: LANDING_DONE | LANDING_NOT_DONE`
- `value_slice_state: VALUE_SLICE_CLOSED | VALUE_SLICE_NOT_CLOSED`
- `activation_state: INACTIVE`
- `github_write.enabled: false`

### close

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/hl-ai.py close \
  --receipt <hl-landing-receipt-v1.json> \
  --closure-policy POLICY_CLOSE
```

关闭规则：

- `LANDING_DONE` 只表示 Landing publication / integration / readback 完成。
- `VALUE_SLICE_CLOSED` 才表示业务价值切片可按 closure policy 关闭。
- `activation_state` 必须仍为 `INACTIVE`；本命令不得激活 Landing。
- 不写 GitHub，不发飞书，不修改外部系统。

## Negative regression 第一批

| 场景 | 期望状态 | 原因码 |
|---|---|---|
| snapshot 过期 | `admission_rejected` | `snapshot_expired` |
| candidate action 试图直接发布 | `failed_closed` | `candidate_action_requires_external_write_decision` |
| downstream preflight 要求已有 receipt 但候选缺失 | `failed_closed` | `admission_receipt_missing` |
| 非 GitHub / 云效 surface | `admission_review_required` | `unsupported_formal_surface` |
| `LANDING_DONE` 但 `VALUE_SLICE_NOT_CLOSED` | `blocked` | `value_slice_not_closed` |

## 样例包

| 文件 | 用途 |
|---|---|
| `docs/team-ai-context/fixtures/stage-c/session-package.json` | `hl-ai start` 输出样例 |
| `docs/team-ai-context/fixtures/stage-c/github-issue-candidate.json` | 普通 GitHub Issue 候选输出样例 |
| `docs/team-ai-context/fixtures/stage-c/fresh-snapshot.json` | `engineering-command-snapshot:v0.2` 新鲜快照样例 |

## 边界

- 只允许本地 dry-run。
- 不创建 GitHub Issue，不发 PR comment，不发飞书，不触发云效。
- `execute` 只生成本地 outbox envelope，不直接 push、开 PR、merge、cleanup 或激活。
- `readback` 只读取可信机器回执；模型声明不能替代机器回执。
- `close` 不得把 `LANDING_DONE` 解释为业务切片关闭。
- 不写 Context Atlas 实体，不写 team-memory approved knowledge。
- 不实现 `ai_loop_control` 状态机，只保留 evidence contract 对接位。
- 不启用 required check，不修改 branch protection。

## 验证

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-ai-cli.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-ai-admission-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-team-assignment-publisher.py
```
