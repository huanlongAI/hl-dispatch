# HL Progress Controlled GitHub Writeback Proposal v0.1

Date: 2026-06-12

Status: P3_PROPOSAL_ONLY

This document is a proposal only. It does not authorize any real GitHub writeback.

## Separate Founder / Gate SSOT Required

No command in this proposal may be executed against GitHub until a later Founder / Gate GitHub SSOT explicitly authorizes a writeback work unit.

That later SSOT must name:

- Repository and target issue / PR scope.
- Exact allowed command or command family.
- Exact labels, comment class, issue template, or body template.
- Dry-run artifact hash and review link.
- Operator identity boundary without exposing account identifiers or credentials.
- Rollback plan and audit log location.
- Exclusions for route / mode / permission, branch protection, production, secrets, deploy, release, provider, payment, billing, refund, settlement, and real user data.

## Position

P3 exists to make selected `hl-progress-work-item:v0.1` state transitions reproducible and auditable in GitHub after explicit gate approval.

GitHub remains SSOT. Feishu, Bitable, dashboards, reports, and chat summaries remain projections. Feishu-originated state must not mutate GitHub unless it is first captured as GitHub SSOT by an explicitly authorized issue, PR comment, decision, or taskbook.

## Allowed Minimum Command Set

The controlled writeback surface should be limited to these command families after a separate gate:

| Command family | Intended use | Required precheck | Rollback |
|----------------|--------------|-------------------|----------|
| `gh issue comment` | Add `status_update`, `gap_report`, `decision_request`, or `acceptance_report` comment to an existing issue. | `gh issue view` confirms target, state, labels, and source links. | Add a correction comment referencing the original comment URL and audit entry. |
| `gh issue edit --add-label` | Add an allowed progress label such as `blocked`, `feedback-given`, or `approved` when the gate names it. | Pre-state label snapshot recorded. | `gh issue edit --remove-label` with the same label. |
| `gh issue edit --remove-label` | Remove an allowed stale progress label when the gate names it. | Pre-state label snapshot recorded. | `gh issue edit --add-label` with the same label. |
| `gh issue create` | Create a new GitHub SSOT issue from a pre-approved projection intake template. | Gate names title, labels, body template, owner, and source evidence. | Close the created issue with rollback reason and link audit entry. |
| `gh pr comment` | Add a bounded review / evidence / gap comment to an existing PR. | `gh pr view` confirms target PR and current state. | Add a correction comment referencing the original comment URL and audit entry. |
| `gh pr edit --add-label` | Add an allowed PR progress label named by the gate. | Pre-state label snapshot recorded. | Remove the same label with a gate-approved rollback command. |

The command set is intentionally smaller than the GitHub API surface. It excludes commits, file writes, branch updates, workflow changes, branch protection, token changes, project mutation, release changes, and repository setting changes.

## Permission Boundary

Allowed after a separate gate:

- Existing `hl-dispatch` issue comments.
- Existing `hl-dispatch` PR comments.
- Explicitly named label add / remove operations.
- Explicitly named new issue creation from a GitHub SSOT intake template.

Not allowed:

- `git push origin main`.
- Direct push to any protected branch.
- branch protection changes.
- route / mode / permission changes.
- production runtime, deploy, release, provider, payment, billing, refund, settlement, or real user data work.
- secrets, credentials, token, OAuth, app installation, webhook, or CI secret mutation.
- GitHub Actions workflow mutation.
- Feishu, Bitable, dashboard, report, or chat edits as source-truth updates.
- Closing, locking, deleting, transferring, or converting issues unless a later gate explicitly names that exact action.

## Rollback Plan

Every real writeback work unit must include a rollback table before execution.

| Write type | Rollback |
|------------|----------|
| Issue comment | Add a correction comment that cites the bad comment URL, states superseded status, and links the audit log entry. Do not silently delete unless the later gate explicitly permits deletion. |
| PR comment | Add a correction comment that cites the bad comment URL and audit entry. |
| Label add | Remove the same label after recording the rollback command and post-state. |
| Label remove | Re-add the same label after recording the rollback command and post-state. |
| New issue | Close the created issue with a rollback reason and link the audit entry. Do not delete the issue. |

Rollback must preserve evidence. Silent deletion is not the default rollback mechanism.

## Audit Log

Each writeback execution must emit an append-only audit entry before and after the command.

Required fields:

```yaml
schema: hl-progress-writeback-audit:v0.1
mode: gated_writeback
gate_ssot: "<GitHub issue / PR / file URL>"
operator_role: "<role only, no credential or account identifier>"
repo: "huanlongAI/hl-dispatch"
target: "<issue or PR URL>"
command_family: "<allowed command family>"
payload_hash: "<sha256 body/template hash>"
dry_run_artifact_hash: "<sha256 dry-run hash>"
pre_state:
  labels: []
  state: "<open | closed | merged | unknown>"
post_state:
  labels: []
  state: "<open | closed | merged | unknown>"
result_url: "<comment / issue / PR URL>"
rollback_command: "<exact rollback command family and target>"
warnings: []
```

The audit log must not contain secrets, tokens, private runtime principals, raw credentials, or private account identifiers.

## Rejected Actions

The following actions are rejected for P3 unless a later Founder / Gate SSOT creates a new scope outside this proposal:

- `git push origin main`.
- Direct file commits or repository file writes as part of writeback.
- branch protection changes.
- route / mode / permission changes.
- production deploy, release, runtime, provider, payment, billing, refund, settlement, real user data, or secrets work.
- GitHub workflow, environment, secret, token, OAuth, app installation, or webhook mutation.
- Closing / reopening / locking / deleting issues or PRs by default.
- Treating Feishu, Bitable, dashboard, report, chat summary, PM draft, CI green, or Gate readback as acceptance evidence.
- Letting the same agent perform final audit on a major architecture writeback it led.

## Feishu / Dashboard Reverse Pollution Prevention

Feishu / dashboard reverse pollution means a projection surface changes GitHub governance state without GitHub SSOT.

Rules:

- Feishu-originated state must not mutate GitHub.
- Bitable edits are notes until a GitHub issue, PR comment, decision request, or taskbook captures them.
- Dashboard status must not close work, mark evidence accepted, add labels, remove blockers, or request Founder acceptance.
- Writeback input must be regenerated from GitHub SSOT plus an approved dry-run artifact.
- Rows without GitHub links are invalid for writeback.
- `external_write: false` P2 ledgers cannot be treated as proof that Feishu or Bitable was updated.

## Verification Before Any Future Writeback

Before any later gated writeback:

1. Run P1 exporter and P2 dry-run projection with fixed artifact output.
2. Review source GitHub links for every row.
3. Record dry-run artifact hash.
4. Record `gh issue view` / `gh pr view` pre-state.
5. Confirm the gate names the exact command family and payload.
6. Execute the minimal command.
7. Record post-state and result URL.
8. Validate rollback command is still possible.

If any step is missing, report `NEEDS_CONTEXT` instead of writing.
