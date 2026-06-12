# Founder Spec Lane v0.1 / 创始人规格直达通道 v0.1

Status: active recovery-period lane
Scope: Delivery Recovery Mode v0.1
Owner: Founder / Gate
Default DRI: one named engineer

Founder Spec Lane is a formal Delivery Recovery lane for bounded taskbooks supplied by Founder. It is not a Founder privilege lane, not a shortcut around evidence, and not a production authorization path.

It exists to move recovery work out of ledger drift, Draft drift, HPRD drift, Gate drift, Feishu projection drift, and Founder micro-decision loops, and back into signed taskbook, dispatch to named implementer, bounded implementation, PR or gap report, review, test, human cross audit, and Founder acceptance.

The lane separates taskbook creation from implementation:

- Founder and AI create the taskbook. Complex judgment-heavy taskbooks use Judgment Harness before sign-off.
- Engineers, designers, or PMs consume the signed taskbook. They do not re-run Judgment Harness and do not need a second start authorization unless they hit new scope, missing context, or forbidden authority.
- Gates and audits check implementation output after a PR, artifact, or `gap_report` exists. They are not a standing pre-start approval loop.

## 1. When To Use

Use this lane only when all conditions are true:

- Founder provides a complete taskbook or explicitly approves a taskbook drafted from current GitHub facts.
- The objective is bounded engineering implementation, closeout, audit, fill-in, test, acceptance packaging, or a bounded delivery recovery step.
- Contract direction and non-goals are clear enough that one DRI can execute without inventing scope.
- The work can exit through PR, deterministic test evidence, demo evidence, or `gap_report`.
- Founder acceptance can verify the result from GitHub evidence.

Do not use this lane for:

- open-ended discovery;
- multi-party semantic negotiation;
- production runtime implementation or production release;
- real user data;
- real payment, billing, refund, settlement, or provider integration;
- provider secrets or secret-store changes;
- tasks without a test, demo, or evidence entrypoint;
- tasks without explicit acceptance criteria.

## 2. Flow

```text
Founder + AI Taskbook Draft
-> Judgment Harness only when the task is judgment-heavy
-> Founder Sign-off
-> Dispatch to named engineer / designer / PM
-> 24h Implementation Plan or equivalent role plan
-> PR or gap_report
-> Gate A: Dahuizi contract / business / redline review
-> Gate B: Xiaofeifei code / test / security / regression review
-> Human Cross Audit
-> Founder Acceptance
-> merge / conditional pass / follow-up / reject
```

This flow may authorize bounded HK engineering implementation when the Founder-signed taskbook says so. After sign-off and GitHub SSOT publication, the named assignee should start within the taskbook boundary. It does not authorize production by itself. Any production runtime, active contract registry write, real provider, real billing, real refund, real settlement, real customer impact, release, deployment, or secrets expansion requires a separate Founder / Gate GitHub SSOT decision.

## 3. Required Taskbook Fields

Every Founder Spec Lane taskbook must include:

- taskbook_id
- version
- assignee
- human_cross_auditor
- GitHub SSOT links
- context engineering preflight
- objective
- current confirmed facts with evidence
- scope in
- scope out
- authorization boundary
- expected output: PR, `gap_report`, or both
- human-readable output standard
- required evidence
- Gate A checklist
- Gate B checklist
- Human Cross Audit checklist
- Founder Acceptance criteria
- allowed notification projection
- forbidden interpretations

The taskbook is the scope baseline. Version `v1.0` freezes scope. Version `v1.1+` may clarify wording by editing the taskbook file. New scope, new acceptance standards, or new runtime authority must be follow-up work, not comment-only expansion.

## 4. Engineer Output

Within 24h of dispatch, the engineer must provide exactly one of:

- implementation plan with branch / PR plan, files touched, commands to run, risks, and expected evidence;
- PR with Founder-readable acceptance pack and verification evidence;
- `gap_report` explaining the missing context, blocker, unauthorized scope, or infeasible acceptance path.

`gap_report` is an acceptable delivery outcome. It is not a failed task when the report prevents unauthorized runtime work, false readiness, or evidence fabrication.

## 5. Context Engineering

Founder Spec Lane taskbooks must prevent AI or engineers from guessing context from long issue history, chat-only memory, Feishu projection, or jargon-heavy summaries.

When a Context Atlas entry exists, the taskbook may reference it as a read-only navigation aid:

- Context Atlas answers what to read and how to report read scope.
- It is not source truth, authorization, acceptance evidence, runtime permission, or production approval.
- Draft Context Views remain draft. They must not be promoted to active through a Founder Spec Lane taskbook.
- If no dedicated task route exists, the taskbook must state the temporary route and the gap.

Every PR, implementation plan, `gap_report`, or acceptance pack should include a short context usage summary:

```yaml
context_usage_summary:
  context_id: "<context id or none>"
  context_route: "<DR-* route or none>"
  files_read:
    - "<GitHub URL or repo-relative file>"
  missing_or_stale_context:
    - "<none or concrete gap>"
  context_not_authorization: true
```

Missing context is not a reason to guess. It is a reason to submit `gap_report`.

## 6. Human-Readable Gate

Founder Spec Lane does not use a 30-second hard gate, but it does require human-readable task and acceptance output.

Every taskbook, PR summary, `gap_report`, Gate report, and acceptance pack must make these items clear to a human reader:

- one-sentence conclusion;
- evidence;
- current state;
- exactly one next action and owner;
- unresolved uncertainty;
- plain-language explanation for task-specific terms.

Black-box governance phrases are not acceptable delivery output, including:

- "继续推进整体治理"
- "需要进一步确认"
- "当前上下文显示"
- "可能已经处理过"
- "runtime 那个"
- "HPRD 已确认但无证据"

If the work cannot be explained in this shape, submit `gap_report` instead of a PR that only contains jargon.

## 7. Dual AI Gates

Gate A and Gate B must be anti-correlated:

- Gate A checks contract, business semantics, authorization boundary, taskbook scope, and redlines.
- Gate B checks code, tests, security, regressions, reproducibility, and operational risk.
- Different model, runtime, prompt, or reviewer profile is preferred.
- Each gate writes independent P0 / P1 / P2 findings.
- Any P0 blocks Founder Acceptance until resolved or explicitly re-scoped by Founder / Gate.

CI green, Draft PR green, PM Draft, HPRD draft, Feishu done, or Gate readback is evidence only. None of them is production authorization.

## 8. Human Cross Audit

Human Cross Audit has veto power.

Minimum audit actions:

- independently read at least three core files or evidence entries;
- run or verify at least one relevant command, check, demo, or evidence artifact;
- check at least one Founder-readable summary, context usage summary, or `gap_report` for human readability;
- write at least one observation not already mentioned by the AI gates;
- return exactly one verdict: `PASS`, `CONDITIONAL_PASS`, or `FAIL`.

If Human Cross Audit returns `FAIL`, Founder Acceptance is blocked unless Founder / Gate explicitly re-scopes the taskbook.

## 9. Feishu Projection

Feishu is projection only.

Allowed Feishu use:

- notify assignee and human cross auditor that a GitHub taskbook is ready;
- point to the GitHub SSOT issue / PR / taskbook;
- remind the owner to reply in GitHub.

Forbidden Feishu interpretations:

- Feishu sent means authorized;
- Feishu read means accepted;
- Feishu done means GitHub done;
- Feishu comment means owner confirmation;
- Feishu message means production runtime permission.

No GitHub SSOT action item means no Feishu notification.

## 10. PM And Capability Package Workflow

Founder Spec Lane does not remove PM ownership of business semantics. It stops PM Drafts and HPRD drafts from becoming indefinite blockers, while preserving a clear PM-owned capability-package lane.

### 10.1 Founder-Signed Engineering Taskbook

When a Founder-signed taskbook already provides a bounded implementation baseline:

- PM Draft, HPRD draft, PM Feishu approval, or PM workbench status must not block the assignee from starting the bounded engineering slice.
- PM may be named as semantic reviewer, gap owner, or follow-up owner, but PM is not the engineering start authority.
- If the assignee finds business semantic ambiguity, the assignee must submit a PR note or `gap_report`; PM responds in GitHub with the smallest business semantic answer that can unblock the decision.
- PM response can clarify business semantics but cannot expand scope, authorize production, authorize active contracts, or authorize registry writes.
- Founder / Gate decides whether PM input changes the taskbook version, becomes a follow-up, or remains out of scope.

### 10.2 PM-Led Capability Package Lane

When the task is a capability package that still needs complete product specification, use this lane:

```text
Founder + AI capability taskbook
-> PM complete Cap-Spec / requirements design
-> engineer HPRD / technical implementation plan
-> PM review of HPRD against the Cap-Spec
-> bounded engineering implementation starts immediately after PM HPRD pass
-> PR / demo / test evidence
-> PM acceptance
-> Gate A / Gate B
-> Human Cross Audit
-> Founder Acceptance
-> merge / conditional pass / follow-up / reject
```

In this lane, PM-approved Cap-Spec plus PM-reviewed HPRD is the start trigger for bounded engineering implementation inside the signed capability taskbook. It still does not authorize production runtime, active contracts, real users, real payments, providers, secrets, release, or deployment.

PM must not hand engineers a vague Draft and then block indefinitely. If the PM cannot complete a spec, the output is a `gap_report` with the smallest missing Founder / Gate decision.

For the current HK recovery taskbook, PM semantic support is bounded by named taskbooks:

- 朱阳 / `zhuyang1204`: customer / payment / asset semantic gaps.
- 邹骢 / `zoucong121`: booking / service / payment semantic gaps.
- 崔田恬 / `cuitiantian0704`: sales / customer profile semantic gaps.

These PM support taskbooks do not create standing action items. A PM acts only when a GitHub PR, `gap_report`, Gate, or Founder / Gate comment asks a bounded semantic question.

## 11. Current Huanlong Recovery Boundary

As of 2026-06-11:

- `hl-dispatch#195` completed the booking staging pilot acceptance.
- `hl-platform#106` is merged evidence for the booking staging pilot and DS-0 readiness path.
- `hl-dispatch#177`, `hl-contracts#103`, and `hl-platform#113` completed DS-2 Tenant Entitlement quota check-only evidence.
- `hl-dispatch#196` is closed as superseded for DS-2 check-only.
- `hl-dispatch#194` remains the HK mainline parent, but current next action is none unless Founder / Gate opens a new GitHub SSOT decision.

Allowed interpretation: staging / sandbox / check-only evidence.

Forbidden interpretation:

- production runtime authorization;
- MVP pass;
- active contract registration;
- additional facts, events, OpenAPI, reasoncodes, or registry writes;
- payment, billing, refund, settlement, provider, secrets, or real user data expansion.
