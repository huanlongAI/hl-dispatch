---
title: "JH2 Meirenji Agent Baseline Taskbook"
version: "v1.0"
status: "DISPATCH_READY_FOR_TASKBOOK_POINTERS"
date: "2026-06-11"
taskbook_id: "JH2-MP-MEIRENJI-AGENT-BASELINE"
product_id: "product.huanlong_ai.meirenji"
package_owner: "NODE-E / dahuizi"
server_owner: "xujiuming / Xu Jiuming"
client_owner: "663548110 / Hu Jiewei"
human_cross_auditor: "wp159951 / Wei Peng"
github_ssot: "https://github.com/huanlongAI/hl-dispatch/issues/158"
risk_path: "red"
current_gate: "blocked_server_baseline_incomplete"
---

# JH2 美人计智能体基线任务书 v1.0

<!-- task-snapshot:v1 -->

## 0. 任务定位

本任务书将 JH2-P2 美人计从催办、回填和总账刷新主线，调整为恢复期正式交付流：

```text
Mission Package
-> Founder Taskbook / Context Pack
-> PR or gap_report
-> Evidence Resolver
-> Gate A / Gate B
-> Human Cross Audit
-> Founder Acceptance
-> Close / Iterate / Archive
```

本任务书不宣称 `product.huanlong_ai.meirenji` real-provider baseline 已完成，不授权生产发布，不授权真实用户数据出境，不授权 App 暴露 provider secret、API key、endpoint 或 model route。

## 1. 当前事实

| Evidence | Current state | Boundary |
| --- | --- | --- |
| https://github.com/huanlongAI/hl-dispatch/issues/158 | OPEN | JH2-P2 GitHub SSOT，当前 gate 仍为 `blocked_server_baseline_incomplete`。 |
| https://github.com/huanlongAI/hl-platform/issues/107 | OPEN | server Work Unit 已派生，但尚无许久明 implementation plan、PR 或 `gap_report` 回填。 |
| https://github.com/huanlongAI/hl-scene-app/issues/47 | CLOSED | 客户端工程骨架 issue 已关闭。 |
| https://github.com/huanlongAI/hl-scene-app/pull/48 | MERGED | 客户端工程骨架已合并，CI 成功；不等于 real-provider baseline 完成。 |
| https://github.com/huanlongAI/hl-scene-app/issues/50 | OPEN | 美人计 App 正式构建流水线仍未收口。 |
| https://github.com/huanlongAI/hl-scene-app/pull/51 | OPEN / checks blocked | 源码目录收口 PR 仍需修复 CI 和 review。 |
| https://github.com/huanlongAI/hl-dispatch/pull/232 | MERGED | Founder Spec Lane v0.1 已作为恢复期通道生效。 |

没有 GitHub PR、commit、CI、artifact、taskbook 或结构化 `gap_report` 的事项，不得作为完成证据。

## 2. Mission Package

```yaml
taskbook_id: JH2-MP-MEIRENJI-AGENT-BASELINE
product_id: product.huanlong_ai.meirenji
version: v1.0
package_owner: NODE-E / dahuizi
server_owner: xujiuming / 许久明
client_owner: 663548110 / 胡杰威
human_cross_auditor: wp159951 / 魏鹏
github_ssot: https://github.com/huanlongAI/hl-dispatch/issues/158
current_gate: blocked_server_baseline_incomplete
current_status: iterate_blocked_server_red_path
expected_outputs:
  - implementation_plan
  - PR
  - gap_report
forbidden_interpretations:
  - production_release_authorization
  - real_user_data_provider_call
  - app_provider_secret_or_endpoint_or_model_route
  - Feishu_as_evidence
  - design_pass_equals_real_provider_complete
```

## 3. Delivery Slices

### Server Red Path Recovery

Owner: `xujiuming / 许久明`.

Required output within 24h after dispatch pointer:

- `implementation_plan`, or
- PR with reproducible evidence, or
- structured `gap_report`.

Provider outbound access, secret-store runtime injection, model route, endpoint, and server-side sandbox provider execution are Red Path prerequisites. Founder Spec Lane does not authorize those prerequisites by itself. If they are missing, the correct output is `gap_report`, not an unverifiable PR.

### Client Closeout

Owner: `663548110 / 胡杰威`.

Required output:

- close or unblock #50 with formal build pipeline evidence;
- unblock #51 with PR body issue reference, CI fixes, review-ready state, and no provider leakage;
- keep App free of provider secret, API key, endpoint, model route, hidden provider route logging, and forbidden permission drift.

Client closeout does not unblock the server gate.

### Agent Context Pack

Owner: `NODE-E / dahuizi` for context packaging; implementation owners consume it.

The context pack freezes:

- synthetic input only for sandbox evidence;
- no real store, customer, user, face, health, medical, diagnosis, prescription, treatment, efficacy, suitability, or business operation data in provider calls;
- no autonomous customer contact, local browser operation, hardware recording, background recording, camera, microphone, location, Bluetooth, smart-glasses, or recording-card permission drift;
- quota insufficient, provider unavailable, timeout, blocked, and validation error states must be visible to the user without leaking provider route details.

### Evidence Resolver

Owner: `NODE-E / dahuizi`.

NODE-E only resolves evidence from:

- GitHub issue comments with structured YAML;
- PR body, commits, checks, and review comments;
- CI logs and artifacts that do not expose secrets;
- desensitized server-side sandbox evidence;
- structured `gap_report`.

Feishu, Figma link presence, screenshot relay, read receipt, oral statement, local path, or non-desensitized image is projection only.

### Audit / Acceptance

- Gate A: `NODE-E / dahuizi` contract, business, authorization, redline review.
- Gate B: `NODE-C / xiaofeifei` code, tests, security, regression review.
- Human Cross Audit: `wp159951 / 魏鹏`, with veto power.
- Founder Acceptance: final verdict after Gate A, Gate B, and Human Cross Audit.

Any P0 from Gate A, Gate B, or Human Cross Audit blocks Founder Acceptance until resolved or explicitly re-scoped by Founder / Gate.

## 4. Scope In

- Create Founder Spec Lane taskbooks and GitHub pointers for the current JH2 recovery work.
- Convert server work from reminder-driven status to PR or `gap_report` delivery.
- Convert client closeout from secondary evidence to its own acceptance path.
- Preserve #158 as the Mission Package SSOT.
- Keep Bitable, Project, Feishu, and dashboards as projection only.

## 5. Scope Out

- No production release, deploy, runtime expansion, active contract registry write, real provider production path, or real user data.
- No secret, API key, endpoint, model route, signing identity, or private runtime principal disclosure in GitHub, Feishu, screenshots, logs, or App artifacts.
- No medical diagnosis, treatment advice, prescription, efficacy promise, or medical-aesthetic suitability judgment.
- No client-side provider route, autonomous customer contact, local/browser operation, or permission drift.
- No daily ledger comment refresh without a structured `status_update`, `gap_report`, `decision_request`, or `acceptance_report`.

## 6. Engineer Output Contract

Within 24h, each named owner must output one of:

```yaml
engineer_output_type: implementation_plan | pr_submitted | gap_report
taskbook_ref: "<GitHub repo file or PR URL>"
owner: "<name / handle>"
branch_or_pr: "<GitHub branch or PR URL, if any>"
files_touched:
  - "<repo-relative path or none>"
founder_readable_summary: "<one sentence>"
verification:
  commands:
    - "<command or not_run_with_reason>"
  result_summary: "<pass | fail | not_run>"
risks_or_blockers:
  - "<none or blocker>"
not_authorized:
  - production_release
  - real_user_data
  - provider_secret_endpoint_model_route_publication
next_action: "<single next action>"
```

If blocked, `gap_report` must include:

```yaml
gap_report:
  blocker_type: "<outbound | secret_store | adapter_wiring | architecture_contract | client_build | CI | other>"
  missing_context: "<what is missing>"
  impact: "<what cannot be proven>"
  recovery_needed_from:
    - "<owner>"
  unblock_condition: "<single concrete condition>"
  next_pr_path: "<possible PR path or none>"
  next_action: "<single next action>"
```

`gap_report` is a qualified delivery outcome. It prevents false completion and evidence fabrication.

## 7. Acceptance Scenarios

- Server success: server-side synthetic sandbox evidence is desensitized; no real user data; no App provider route leakage.
- Server blocked: `gap_report` identifies outbound, secret-store, adapter wiring, architecture, or contract blocker with a concrete unblock condition.
- Client closeout: #50 and #51 have GitHub evidence, green checks or explicit blocker, and no provider secret, endpoint, model route, or permission drift.
- Agent compliance: forbidden medical, automated-contact, hardware recording, sensitive data, and permission-drift paths are denied.
- Evidence discipline: Feishu, Figma presence, oral statements, local files, and non-desensitized screenshots do not complete any gate.
- Gate sequence: P0 from Gate A, Gate B, or Human Cross Audit blocks Founder Acceptance.

## 8. Fallback

If no server PR or `gap_report` exists 48h after the taskbook pointer is dispatched, the fallback is `B 重派`. Do not restart daily催办 loops.

```yaml
fallback:
  selected: B_reassign
  trigger: no_server_pr_or_gap_report_after_48h
  next_action: founder_reassigns_server_recovery_owner_or_freezes_real_provider_baseline
```
