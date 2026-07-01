# Boundary Engine Outer Loop Contract v0.1

Status: manual-trigger only
Authority: APPROVE_BOUNDARY_ENGINE_OUTER_LOOP_V0_1_MANUAL_TRIGGER

## 中文摘要

本文定义 Boundary Engine 手动外环的最小操作契约。它只用于把唤龙低风险维护通道的重复粘贴指令收敛为仓库内可读规则，不启动自动调度、不创建运行时注入、不改变生产或权限边界。

## 术语说明

- Boundary Engine: 本文件中的维护边界执行规则集合。
- manual-trigger: 人工手动触发；没有计划任务、后台轮询或无人值守执行。
- low-risk maintenance lane: 低风险维护通道，仅处理已列明的 repo-local 维护事件。
- hard boundary: 硬停止边界；发现后必须排除、停止或升级，不得部分执行。
- digest: 每次手动运行的终态摘要。

## Purpose

This contract converts repeated pasted Boundary Engine maintenance prompts into a
Codex-readable manual outer loop for the Huanlong low-risk maintenance lane.

It is not unattended automation, scheduling, MCP, hooks, skills, subagents,
production control, or an AI_OS frozen artifact. A human must start each run.

## Active Scope

Active repositories:

- huanlongAI/hl-dispatch
- huanlongAI/hl-scene-design-system
- huanlongAI/hl-landing-conformance-sandbox
- huanlongAI/hl-portal
- huanlongAI/sentinel-shared
- huanlongAI/ltc-endpoint
- huanlongAI/hl-framework
- huanlongAI/guanghe

The lane is limited to repo-local low-risk maintenance and observation for this
scope unless a later approved manual trigger changes `BOUNDARY_ENGINE_STATE.md`.

## Allowed Maintenance Events

- BEHIND update branch and rerun checks.
- Stale checks rerun.
- Deterministic CI or gate repair, maximum 3 attempts.
- PR body or metadata repair.
- Docs command drift sync.
- Clean worktree replay.
- Local main fast-forward to origin/main when clean and fast-forward only.
- Post-merge hygiene.
- WAIT_CI, WAIT_REVIEW, WAIT_EXTERNAL.

Post-merge hygiene may delete a branch only when all are true:

- related PR is MERGED;
- branch is agent-owned or codex-owned;
- branch OID matches PR headRefOid or equivalent merge evidence;
- no open PR references the branch;
- no attached worktree exists;
- branch is not main, protected, release, production, or mainlike;
- deletion does not touch forbidden boundaries.

## Forbidden Boundaries

Stop or exclude when a request or discovered item touches:

- feature implementation;
- AGENTS/governance contract drafts unless separately authorized;
- governance or capability review drafts;
- provider, production, deploy, Yunxiao, portal or public readiness decisions;
- production, release, provider real write, registry real write;
- secrets, credentials, CASCADE_TOKEN, tokens, principals;
- payment, points, refund, invoice, settlement;
- customer data or customer-visible output;
- external send, Feishu, DahuiZi delivery;
- accepted/done SSOT or evidence mutation;
- branch protection modification;
- required review bypass;
- auth, payment, or security core;
- destructive migration;
- no-trigger governance artifact;
- AI_OS frozen artifact modification;
- new lane beyond low-risk maintenance.

Seeing and excluding a hard boundary is a pass condition. Executing an
unauthorized hard-boundary action is a violation.

## Special Repo Rules

### huanlongAI/sentinel-shared

Allowed only when the action does not weaken, bypass, or semantically alter
shared Sentinel gates. Exclude or stop for required-check semantics,
CASCADE_TOKEN handling, live cascade fan-out, secret handling, cross-repo gate
authority, caller-sync semantics, or required-check bypass behavior.

### huanlongAI/ltc-endpoint

Allowed only for low-risk maintenance and repo-local gate hygiene. Exclude or
stop for real parser, collector, daemon, launch agent, prompt/transcript/raw path
collection or processing, real DahuiZi or Feishu delivery, evidence accepted/done
mutation, credentials, tokens, principals, or long-running runtime behavior.

### huanlongAI/hl-framework

Allowed only for low-risk maintenance and repo-local gate hygiene. Exclude or
stop for BOM semantics, release workflow semantics, starter source semantics,
registry publish, artifact release, framework auth/security semantics,
production/customer-visible behavior, branch protection, or required review
behavior.

### huanlongAI/guanghe

Allowed only for low-risk maintenance and repo-local gate hygiene. Exclude or
stop for GHKit or GHComponents registry publish, package release, public design
token semantics, GHTheme semantics, brand or platform design authority, package
source semantics, customer-visible design-system behavior, branch protection, or
required review behavior.

## Transition Rules

1. If a pending Boundary Engine PR exists, follow up that PR to a terminal state.
2. If active scope has eligible low-risk maintenance, run queue-drain.
3. If two stable observations passed since last onboarding and a safe candidate
   exists, onboard exactly one repo by approved manual trigger.
4. If no eligible work exists, return WAIT_EXTERNAL.
5. If a hard boundary is discovered, return STOP_RISK_BOUNDARY or exclude it
   when the run's classification rules allow exclusion.
6. If evidence is ambiguous, return ESCALATED_BATCH with the exact unresolved
   decision or admin action.

## Budgets

- max active repos per observation: 8 unless state is updated by approval;
- max maintenance events processed per run: 4;
- max repair attempts per item: 3;
- max changed files per PR: 25;
- max changed lines per PR: 800;
- max runtime per item: 45 minutes;
- max onboarding expansion per onboarding run: 1 repo;
- no file changes during observation-only runs.

## Terminal States

- MERGED
- AUTO_MERGE_QUEUED
- PR_READY_WAITING_REVIEW
- PR_READY_NO_MERGE
- WAIT_CI
- WAIT_REVIEW
- WAIT_EXTERNAL
- ESCALATED_BATCH
- STOP_FAILED_GATE
- STOP_RISK_BOUNDARY
- STOP_BUDGET

## Digest Format

Every manual run returns one terminal digest only:

```text
repos_observed:
events_found:
events_processed:
terminal_states:
excluded_items:
verification_results:
engine_gates_used:
loss_budget_used:
hard_boundary_seen:
hard_gate_violation_count:
unnecessary_ask_count:
false_auto_action_count:
governance_artifact_created:
merge_mechanism, if any:
next_human_decision_required, if any:
FINAL LINE:
<run-specific digest-ready marker>
```
