# Team AI Context Stage C Entry v0.1

Date: 2026-06-25

Status: STAGE_C_LOCAL_TEAM_ENTRY_DRY_RUN

## 中文摘要

本文定义唤龙团队 AI 上下文工程 Stage C 的本地团队入口。Stage C 只在 `hl-dispatch` 内提供 `hl-ai start` / `hl-ai submit` dry-run 契约、会话包样例和 adapter 输入包，不写 GitHub、飞书、云效、Context Atlas、team-memory 或生产运行态。

Stage C 的目标不是启用 `TEAM-CONTEXT-ENFORCED`，而是让团队成员先用自然语言目标生成本地 session package，再把候选 AI 输出提交给 `AI_ADMISSION_GATE` 形成可审计结果。只有本地证据稳定后，后续 push / PR / required check / 云效 / Context Atlas / ai_loop_control 才进入新的 Founder 裁决。

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

## Negative regression 第一批

| 场景 | 期望状态 | 原因码 |
|---|---|---|
| snapshot 过期 | `admission_rejected` | `snapshot_expired` |
| candidate action 试图直接发布 | `failed_closed` | `candidate_action_requires_external_write_decision` |
| downstream preflight 要求已有 receipt 但候选缺失 | `failed_closed` | `admission_receipt_missing` |
| 非 GitHub / 云效 surface | `admission_review_required` | `unsupported_formal_surface` |

## 样例包

| 文件 | 用途 |
|---|---|
| `docs/team-ai-context/fixtures/stage-c/session-package.json` | `hl-ai start` 输出样例 |
| `docs/team-ai-context/fixtures/stage-c/github-issue-candidate.json` | 普通 GitHub Issue 候选输出样例 |
| `docs/team-ai-context/fixtures/stage-c/fresh-snapshot.json` | `engineering-command-snapshot:v0.2` 新鲜快照样例 |

## 边界

- 只允许本地 dry-run。
- 不创建 GitHub Issue，不发 PR comment，不发飞书，不触发云效。
- 不写 Context Atlas 实体，不写 team-memory approved knowledge。
- 不实现 `ai_loop_control` 状态机，只保留 evidence contract 对接位。
- 不启用 required check，不修改 branch protection。

## 验证

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-ai-cli.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-ai-admission-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-team-assignment-publisher.py
```
