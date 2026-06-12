# HL Progress Governance Loop v0.1

Date: 2026-06-12

Status: ACTIVE_GOAL_CONTRACT

GitHub SSOT:

- Current repository file: `docs/delivery-recovery/HL_PROGRESS_GOVERNANCE_LOOP_v0.1.md`
- Current launch taskbook: `deliverables/tasks/HL-PROGRESS-GOVERNANCE-LOOP-TASKBOOK-2026-06-12-v0.1.md`
- Source decision: 2026-06-12 Founder approved the hybrid project / task progress management plan and requested a long-running closed-loop goal-mode execution.

## 1. Position

`hl-progress` is the Huanlong engineering progress governance loop.

It is not a full task platform, not a replacement for GitHub Issues / PRs / repository files, not a replacement for Product / PM semantic ownership, not a Feishu-first workflow, and not production runtime authorization.

The loop turns existing GitHub evidence into a normalized AI-friendly progress model, then projects selected state into Feishu Bitable / dashboards for human scanning. GitHub remains the source of truth. Bitable, Feishu, Project, dashboards, reports, and chat summaries remain projections.

Delivery Recovery Mode v0.1 remains a recovery-period flow. This document adds a long-running progress-governance loop on top of GitHub SSOT; it does not upgrade Delivery Recovery Mode into the permanent unique Huanlong product-engineering process.

## 2. Goal

The goal is to make Engineering project management, R&D delivery progress governance, engineering governance, and development discipline observable and actionable for AI and humans.

The loop must answer six questions from GitHub evidence:

1. What work is active?
2. Who owns it?
3. What gate or evidence is next?
4. What is blocked?
5. What needs Founder / Gate decision?
6. What is safe to mark accepted, rejected, or archived?

## 3. Authority Boundary

This contract authorizes docs-only planning and read-only progress projection until a later GitHub SSOT explicitly opens a writeback phase.

It does not authorize:

- route, mode, node, role, registry, profile, or runtime permission changes
- branch protection changes
- direct push to `main`
- production runtime, deploy, release, real user data, secrets, payment, billing, refund, settlement, or provider work
- treating Feishu, Bitable, Project, dashboard, chat summary, PM draft, CI green, or Gate readback as final evidence
- replacing PM business semantic ownership
- replacing Founder final decision authority
- allowing the same agent to perform final audit on major architecture it led

Within this goal taskbook only, plan-internal Green docs / read-only tooling changes may be pushed and merged after local verification and repository checks. This does not create standing authority outside the current goal. Yellow / Red expansion requires separate Founder / Gate GitHub SSOT with exact scope, affected files, tests, rollback, and exclusions.

## 4. Operating Model

```text
GitHub Issues / PRs / repo files
  -> hl-progress read model
  -> normalized task snapshots
  -> action projection / Bitable projection / Founder packet
  -> GitHub decision, PR, gap_report, gate, evidence, owner, blocker update
```

Rules:

- GitHub evidence is canonical.
- Projection output is disposable and reproducible.
- Any Feishu-originated signal must be converted into a GitHub issue, PR comment, decision request, or taskbook before it can drive engineering state.
- No Evidence, No Done remains active.
- No Action, No Notification remains active.
- No Context, No AI Guess remains active.
- Every generated report must include source links and projection timestamp.

## 5. Minimum Data Model

The normalized work item is `hl-progress-work-item:v0.1`.

```yaml
schema: hl-progress-work-item:v0.1
task_id: "<stable human-readable id>"
source:
  system: github
  repo: "<owner/repo>"
  issue_url: "<GitHub issue URL or empty>"
  pr_urls:
    - "<GitHub PR URL>"
  file_refs:
    - "<repo path or URL>"
owner:
  github: "<handle or unknown>"
  role: founder | dahuizi | pm | engineer | gate | qa | ops | unknown
status: intake | planned | ready | in_progress | blocked | review | gate_a | gate_b | human_cross_audit | founder_acceptance | done | rejected | archived
risk_path: green | yellow | red | unknown
evidence_state: none | claimed | linked | verified | accepted
next_gate: "<gate name or n/a>"
next_action: "<one concrete action or n/a>"
blocker:
  state: none | active | waiting_decision | external
  summary: "<short blocker summary or n/a>"
  owner: "<github handle / role / n/a>"
founder_decision_required: true | false
projection:
  target: none | bitable | dashboard | markdown | json
  generated_at: "<ISO-8601 timestamp>"
  source_hash: "<content hash or n/a>"
warnings:
  - "<missing field / stale evidence / inferred projection warning>"
```

Required invariants:

- `done` requires `evidence_state: accepted`.
- `blocked` requires `blocker.state != none`.
- `founder_acceptance` requires at least one GitHub source link.
- `projection.source_hash` must change when source facts change.
- Missing fields are reported as `unknown` plus `warnings`; they are not invented.

## 6. Status Semantics

| Status | Meaning | Exit Evidence |
|--------|---------|---------------|
| `intake` | GitHub signal exists but not yet shaped into a taskbook / work item. | Taskbook, issue body, or rejection. |
| `planned` | Scope, owner, and expected evidence are named. | Ready gate or blocker. |
| `ready` | Context is sufficient for execution. | PR, implementation start, or gap_report. |
| `in_progress` | Owner is actively executing. | PR, evidence, blocker, or review request. |
| `blocked` | Progress cannot continue without named unblock action. | GitHub unblock evidence or decision. |
| `review` | Output is ready for review. | Gate A / Gate B / rejection. |
| `gate_a` | Dahuizi engineering-governance review is required. | GitHub review / gap_report. |
| `gate_b` | Cross-agent / second gate review is required. | GitHub review / gap_report. |
| `human_cross_audit` | Human audit or owner validation is required. | Audit comment / approval / rejection. |
| `founder_acceptance` | Founder acceptance is the next state transition. | Founder / Gate GitHub SSOT. |
| `done` | Evidence is accepted and work is closed. | Acceptance link. |
| `rejected` | Output is rejected or scope is cancelled. | Rejection reason and next action. |
| `archived` | No active action remains. | Archive reason. |

## 7. Feishu Bitable Projection

Feishu Bitable is a human dashboard projection. It may contain a subset of `hl-progress-work-item:v0.1`.

Recommended columns:

| Column | Source | Notes |
|--------|--------|-------|
| Task ID | GitHub issue / taskbook / PR | Stable display key. |
| Repo | GitHub | Owner/repo. |
| Owner | GitHub assignee / TEAM.yml mapping | Person display is projection only. |
| Status | normalized status | Derived from GitHub source. |
| Risk Path | normalized risk | Green / Yellow / Red / unknown. |
| Evidence State | normalized evidence state | Never mark accepted without GitHub evidence. |
| Next Gate | GitHub taskbook / PR / issue | Gate A / Gate B / audit / Founder. |
| Next Action | GitHub issue body / comment | One concrete action. |
| Blocker | GitHub issue / PR / gap_report | Empty if no active blocker. |
| Founder Decision | normalized boolean | Derived from `decision-request` / taskbook. |
| GitHub Link | GitHub URL | Mandatory for every row. |
| Last Synced | projection runtime | Projection timestamp. |
| Projection Warning | exporter warning | Missing / stale / inferred fields. |

Projection rules:

- GitHub -> Bitable is one-way by default.
- Bitable edits do not mutate GitHub unless a later writeback phase is separately authorized.
- Bitable rows without GitHub links are invalid for governance decisions.
- Manual Bitable edits must be treated as notes until captured in GitHub.

## 8. `hl-progress` Phases

| Phase | Scope | Write Surface | Exit Gate |
|-------|-------|---------------|-----------|
| P0 | Docs-only contract, data model, taskbook. | This repo docs only. | PR merged with verification. |
| P1 | Read-only exporter from GitHub Issues / PRs / repo files to JSON and Markdown. | Local artifact output only when explicitly requested. | Offline deterministic tests + live read-only smoke check. |
| P2 | Feishu Bitable projection. | Bitable rows only, no GitHub writeback. | Field mapping, dry-run, and projection ledger. |
| P3 | Controlled GitHub writeback for selected normalized commands. | GitHub comments / labels / issues only. | Separate Founder / Gate SSOT and rollback plan. |
| P4 | Optional external SaaS adapter, if needed. | Read-only first. | Separate tool-specific decision. |

P0 and P1 are Green if they remain docs-only or read-only. P2 is Yellow because it touches Feishu workspace state. P3 and P4 are Yellow or Red depending on write surface, secrets, and production coupling.

## 9. Dahuizi Governance Loop

Daily loop:

1. Read GitHub issue / PR / taskbook deltas.
2. Normalize active work into `hl-progress-work-item:v0.1`.
3. Report stale work, blockers, missing evidence, and decision-required items.
4. Produce action projection only for items with concrete `next_action`, decision, blocker, or acceptance signal.
5. Update Feishu / dashboard projection only after GitHub source exists.

Weekly Founder packet:

1. Active work by owner and risk path.
2. Top blockers and required decision owner.
3. PRs waiting review / merge / evidence.
4. Done items with accepted evidence.
5. Proposed next Green / Yellow / Red work units.

## 10. Acceptance Criteria

The loop is acceptable only if:

- GitHub remains the only fact source.
- The data model can represent Huanlong taskbook / PR / gap_report / gate / evidence / owner / blocker state.
- Projection can be regenerated from GitHub without hidden manual state.
- The first exporter is read-only and deterministic.
- Feishu Bitable projection has explicit one-way semantics before any writeback is considered.
- No route, mode, runtime permission, branch protection, or production authority expands through this contract.
- Verification evidence is recorded before any `done` claim.

## 11. Next Work Units

| Work Unit | Risk | Output | Gate |
|-----------|------|--------|------|
| `HLPROG-P0-WU1` | Green | This contract + taskbook + README index. | Docs PR verification. |
| `HLPROG-P1-WU1` | Green | Read-only exporter design mapped to existing `action-projection:v0.1`; implementation notes in `HL_PROGRESS_EXPORTER_v0.1.md`. | Offline tests. |
| `HLPROG-P1-WU2` | Green | JSON / Markdown Founder packet output via `scripts/export-hl-progress.py`. | Deterministic fixture tests. |
| `HLPROG-P2-WU1` | Yellow | Feishu Bitable field mapping and dry-run ledger in `HL_PROGRESS_BITABLE_DRY_RUN_v0.1.md`; local dry-run via `scripts/project-hl-progress-bitable.py`. | Separate Feishu projection decision before any external write. |
| `HLPROG-P3-WU1` | Yellow / Red | Controlled GitHub writeback proposal. | Separate Founder / Gate SSOT. |
