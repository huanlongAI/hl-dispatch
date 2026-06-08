# hl-dispatch Copilot Instructions

Use these instructions for AI-assisted edits in this repository.

## Source Of Truth

- GitHub Issues, PRs, and repository files are the SSOT for tasks, evidence, and delivery state.
- Feishu, Bitable, dashboards, and chat summaries are projections only.
- Do not infer current facts from memory or chat-only history.

## Context Validity Gate

Before proposing or making changes, state the files, issues, PRs, or docs used as context.

If required context is missing, stale, or contradictory, stop and report `NEEDS_CONTEXT`. Do not guess.

The old "30 秒说清" and steward-signature language is not a hard gate in Delivery Recovery Mode v0.1. A short summary can be useful, but the hard gate is context validity plus evidence.

## Delivery Recovery Mode

Delivery Recovery Mode v0.1 is a 14-30 day recovery mode. It does not make Delivery Slice a permanent unique workflow. The canonical implementation contract is `docs/delivery-recovery/DELIVERY_RECOVERY_IMPLEMENTATION_CONTRACT_v0.1.md`.

Use:

- Mission Package for the bounded recovery objective.
- Delivery Slice for a 1-3 day execution slice.
- Risk-Retirement Slice for Red Path risk removal, architecture spikes, provider blockers, secret blockers, or other unblock work.
- Work Unit for one assignable unit of work.
- `task-snapshot:v1` when task context changes.
- `ai-output:v1` for AI completion, blocker, review, or handoff output.

Before handling a Work Unit, require a Context Pack containing Mission Package, Delivery Slice / Risk-Retirement Slice, Task Snapshot, Evidence List, Allowed Action, and Authorization Boundary. If any part is missing, output only `gap_report`.

## Required Rules

No Evidence, No Done: do not claim completion without test, CI, artifact, demo, acceptance, or review evidence.

No Context, No AI Guess: do not invent package IDs, slice IDs, owners, risk paths, evidence, facts, or approval state.

No Package, No Planned Work.

No Slice, No Delivery Plan.

No Structured Update, No Public Status Comment. Public backfill comments must be one of: `status_update`, `gap_report`, `decision_request`, `acceptance_report`.

Exceptions: PR review, CI failure, security incident, P0 incident, and blocker unblock.

Public GitHub backfill must use:

```text
<!-- ai-output:v1 -->
【类型】
【结论】
【依据】
【当前状态】
【下一步唯一动作】
【需要人处理】
【不确定项】
```

Do not write "已完成", "已确认", "已授权", "已阻塞", "已通过", "可关闭", "runtime ready", or "production ready" without evidence and the required human role where applicable.

Do not write filler or black-box governance phrases: "收到 / 已知 / 继续推进", "继续推进整体治理", "需要进一步确认", "当前上下文显示", "可能已经处理过", "runtime 那个", or "HPRD 已确认但无证据".

AI may draft, suggest, execute, and audit. AI must not replace human confirmation, signature, rejection, approval, or acceptance.

Risk path must be explicit: `green`, `yellow`, or `red`.

Do not add a total ledger issue.

Do not change Feishu notification workflow, `issue_comment` workflow behavior, CI gates, secrets, route identity, or business logic unless the task explicitly asks for that scope.

Do not send Feishu notifications or refresh public status comments when there is no action item.

Use "手艺人" and "服务人员" for the current service-role terminology. Do not write back "美疗师 / 美容师".
