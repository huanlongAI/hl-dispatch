# Delivery Recovery Mode v0.1

Status: active recovery pattern
Window: 14-30 days
Scope: hl-dispatch coordination documents, GitHub Issue Forms, and PR templates

Delivery Recovery Mode is a temporary delivery-control mode for reducing context loss during recovery. It does not replace the normal Huanlong delivery process, and Delivery Slice is not a permanent unique workflow.

Canonical implementation contract: `DELIVERY_RECOVERY_IMPLEMENTATION_CONTRACT_v0.1.md`.

## Source Of Truth

- GitHub Issues, PRs, and repository files are the task and evidence SSOT.
- Feishu, Bitable, dashboards, and chat summaries are projections only.
- No total ledger issue is added by this mode.

## Terms

Mission Package is the bounded recovery objective. It carries `package_id`, DRI, target outcome, risk path, linked slices, and evidence expectations.

Delivery Slice is a 1-3 day execution slice inside a Mission Package. It carries `slice_id`, DRI, next action, evidence requirement, and risk path. It exists only for the recovery window.

Risk-Retirement Slice is a slice for Red Path risk removal, architecture spikes, provider blockers, secret blockers, or other unblock work. It must declare an unblock condition and decision deadline.

Work Unit is one assignable unit of work inside a Delivery Slice. It carries `work_unit_id`, owner, next action, acceptance evidence, test evidence, and explicit non-goals.

Context Pack is the minimum context set needed before a Work Unit or PR starts. It names the files, issues, PRs, decisions, and known gaps used by the actor.

Task Snapshot is the current readable task card. Use `task-snapshot:v1` when a task changes owner, context, risk path, or next action.

AI Output Contract is the required structure for AI-authored delivery output. Use `ai-output:v1` for completion, blocker, and review summaries.

## Gates

Context Validity Gate: before AI changes files, it must list the context it read and identify stale or missing context. If context is insufficient, report `NEEDS_CONTEXT`.

No Evidence, No Done: `DONE` requires command output, test result, artifact link, screenshot, or explicit reviewer/acceptance evidence.

No Context, No AI Guess: missing package, slice, owner, risk, or evidence context blocks AI conclusion-making.

No Action, No Notification: without a concrete action item, do not send Feishu notifications or refresh public status comments.

One Slice, Few Work Units: one Delivery Slice has at most 3-5 Work Units.

One DRI: each Work Unit has one direct responsible individual.

Risk Path: every Mission Package, Delivery Slice, Work Unit, and PR must declare `green`, `yellow`, or `red`.

No Package, No Planned Work: planned recovery work must attach to a Mission Package unless it is in the Exception Lane.

No Slice, No Delivery Plan: delivery planning must attach to a Delivery Slice or Risk-Retirement Slice unless it is in the Exception Lane.

No Structured Update, No Public Status Comment: public state comments must be `status_update`, `gap_report`, `decision_request`, or `acceptance_report`. Exceptions are PR review, CI failure, security incident, P0 incident, and blocker unblock.

## Minimal Flow

1. Open a Mission Package issue with `package_id`, DRI, risk path, next action, and evidence expectation.
2. Open Delivery Slice or Risk-Retirement Slice issues for the current 1-3 day recovery work.
3. Open Work Unit issues only when a slice needs assignable execution.
4. Attach a Context Pack before AI / Human Execution starts.
5. Use PR / Test / Review for delivery evidence.
6. Resolve evidence into Task Snapshot and Action Projection.
7. Close / iterate / archive only after acceptance.

## Exception Lane

These cases may skip package/slice planning at creation time, but must backfill context and evidence after the urgent action:

- P0 incident;
- trivial fix;
- CI failure fix;
- security urgent fix;
- blocker unblock.

Exception Lane work still follows No Evidence, No Done and must not use Feishu, Bitable, or Project as the evidence source.

After urgent action, backfill evidence, incident / fix report, close reason, and next prevention if applicable.

## Non-Goals

- Do not modify business logic for this mode.
- Do not modify Feishu notification workflow unless a separate PR targets notification behavior.
- Do not treat Feishu or Bitable as fact sources.
- Do not add a new total ledger issue.
- Do not build a full task platform before recovery work starts.
- Do not send Feishu notifications or refresh public status comments when there is no action item.
