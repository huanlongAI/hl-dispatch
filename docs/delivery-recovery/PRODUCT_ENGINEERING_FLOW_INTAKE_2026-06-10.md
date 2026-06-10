# Product Engineering Flow Recovery Intake

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-10

## Scope

This file is the GitHub SSOT readback, decision request, and bounded task dispatch package for product-engineering flow landing during Delivery Recovery Mode v0.1.

It answers two different questions and keeps them separate:

1. Delivery Recovery Mode v0.1 is active as a recovery-period delivery-control flow because DS-4 through DS-8 were completed with GitHub PR, test, review, and acceptance evidence.
2. Delivery Recovery Mode v0.1 has not been upgraded into the permanent unique Huanlong product-engineering process. That upgrade still requires a separate Founder / Gate GitHub SSOT decision.

This package allows bounded task dispatch for PM, Contracts / Architect, Engineering, and QA / Gate only within the non-runtime limits below. It does not create a runtime work order, active contract, active registry, HPRD, design.md, production task, provider task, payment task, billing task, refund task, settlement task, CustomerAsset deduction task, or service fulfillment task.

## Task Snapshot

```yaml
package_id: MP-DELIVERY-RECOVERY-v0.1
slice_id: PRODUCT-ENGINEERING-FLOW-INTAKE-20260610
maturity: flow_landing_decision_request_ready
type: decision_request
state: dispatch_docs_only
risk_path: Yellow
current_date: 2026-06-10
source_of_truth: GitHub PRs, Issues, and repository files
projection_only:
  - Feishu
  - Project
  - Bitable
current_answer_can_dispatch_tasks: true_bounded_docs_only_and_decision_tasks
current_answer_recovery_flow_status: active_recovery_period_flow_only
current_answer_permanent_flow_status: not_upgraded_no_founder_gate_ssot
close_condition: This dispatch PR merges with validation evidence and no open PR remains in hl-dispatch, hl-contracts, or hl-platform unless explicitly blocked.
authorization: process readback, decision request, and bounded non-runtime task dispatch only
runtime_authorization: "not_authorized"
active_contract_authorization: "not_authorized"
active_registry_authorization: "not_authorized"
hprd_authorization: "not_authorized"
design_md_authorization: "not_authorized"
production_authorization: "not_authorized"
```

## Current Evidence Readback

| Evidence | Current state | Boundary |
| --- | --- | --- |
| [hl-contracts#113](https://github.com/huanlongAI/hl-contracts/pull/113) | merged | DS-4 Formal Object Chain read path baseline; docs-only / check-only. |
| [hl-platform#131](https://github.com/huanlongAI/hl-platform/pull/131) | merged | DS-4 sandbox / embedded CLI evidence resolver; no formal runtime route. |
| [hl-dispatch#208](https://github.com/huanlongAI/hl-dispatch/pull/208) | merged | DS-4 readback / acceptance. |
| [hl-dispatch#209](https://github.com/huanlongAI/hl-dispatch/pull/209) | merged | DS-5 next decision request. |
| [hl-dispatch#210](https://github.com/huanlongAI/hl-dispatch/pull/210) | merged | DS-6 decision intake. |
| [hl-dispatch#211](https://github.com/huanlongAI/hl-dispatch/pull/211) | merged | DS-7 Option B GitHub SSOT decision for hl-contracts docs-only planning. |
| [hl-contracts#114](https://github.com/huanlongAI/hl-contracts/pull/114) | merged | DS-7 activation readiness docs-only planning. |
| [hl-dispatch#212](https://github.com/huanlongAI/hl-dispatch/pull/212) | merged | DS-7 acceptance readback. |
| [hl-contracts#115](https://github.com/huanlongAI/hl-contracts/pull/115) | merged | DS-8 ServiceOrder lifecycle boundary gap docs-only planning. |
| [hl-dispatch#213](https://github.com/huanlongAI/hl-dispatch/pull/213) | merged | DS-8 acceptance readback. |
| [hl-contracts#99](https://github.com/huanlongAI/hl-contracts/pull/99) | merged | SalesOrder remains candidate-only / draft candidate material. |
| [hl-contracts#96](https://github.com/huanlongAI/hl-contracts/pull/96) | merged | CustomerAsset remains candidate-only / draft candidate material. |
| [hl-contracts#111](https://github.com/huanlongAI/hl-contracts/pull/111) | merged | ServiceOrder remains candidate-only / draft candidate material. |
| [hl-contracts#112](https://github.com/huanlongAI/hl-contracts/pull/112) | merged | PaymentCheckout remains candidate-only / draft candidate material. |

Open PR readback on 2026-06-10:

```yaml
open_prs:
  huanlongAI/hl-dispatch: []
  huanlongAI/hl-contracts: []
  huanlongAI/hl-platform: []
```

## Process Status Judgment

Delivery Recovery Mode v0.1 is currently effective for the recovery period because it has produced repeatable evidence from DS-4 through DS-8:

- a bounded slice / decision chain,
- PR-scoped evidence,
- test evidence,
- E dual review,
- explicit non-authorization boundaries,
- acceptance readbacks,
- no open PR residue in the three checked repositories.

This is not enough to declare a permanent product-engineering process. The permanent process decision is missing:

```yaml
permanent_process_upgrade:
  status: blocked_missing_founder_gate_github_ssot
  current_default: keep_delivery_recovery_mode_as_recovery_period_flow_only
  required_decision_source: Founder / Gate GitHub SSOT
  required_before_upgrade:
    - process name and version
    - scope after recovery window
    - affected repositories
    - owner model for PM, contracts, engineering, and QA / Gate
    - PR / Issue templates to keep or retire
    - required checks and gate policy impact
    - rollback route if the formal flow creates friction
```

## Decision Requests

### Decision Request 1 - Process Adoption

```yaml
decision_request:
  class: decision_request
  question: Should Delivery Recovery Mode v0.1 remain only a recovery-period flow, or should a separate Founder / Gate GitHub SSOT be opened to upgrade it into a formal product-engineering process?
  default_answer: remain_recovery_period_flow_only
  current_blocker: no_founder_gate_github_ssot_for_permanent_process_upgrade
  allowed_now:
    - keep using Delivery Recovery Mode v0.1 for bounded recovery work
    - dispatch docs-only decision and readback tasks through GitHub SSOT
    - use Feishu, Project, or Bitable only as projection after GitHub SSOT exists
  not_allowed_now:
    - declare permanent unique process
    - replace normal Huanlong delivery process
    - change branch protection, workflow, or gate policy
```

### Decision Request 2 - DS-9 Product / Contract Track

```yaml
decision_request:
  class: decision_request
  question: Should DS-9 enter ServiceOrder single lifecycle boundary facts/events/OpenAPI/reasoncodes docs-only planning, or should DS-8 remain only gap evidence?
  default_answer: keep_ds8_as_gap_evidence_until_founder_gate_selects_ds9
  requested_owner:
    - Founder
    - Gate
    - Package Owner if explicitly assigned
  required_before_contracts_work:
    - GitHub SSOT decision selecting DS-9
    - one ServiceOrder lifecycle boundary only
    - named contracts owner
    - affected files and expected tests
    - explicit non-authorization list
  not_authorized_by_this_request:
    - active_contract
    - active_registry_write
    - HPRD
    - design_md
    - formal_runtime
    - provider_integration
    - real_payment_provider
    - payment
    - billing
    - refund
    - settlement
    - CustomerAsset_deduction
    - service_fulfillment
    - business_object_creation
    - production
    - deploy_release
    - workflow_change
    - secrets
    - real_user_data
```

## Task Dispatch Package

Task dispatch is allowed now only as GitHub SSOT-backed docs-only / decision / review work. Projection to Feishu, Project, or Bitable may happen only after the GitHub target exists and must not be treated as acceptance evidence.

| Lane | Dispatch now? | Task | Evidence exit | Blocked until separate Founder / Gate GitHub SSOT |
| --- | --- | --- | --- | --- |
| PM | Yes | Decide whether DS-9 should enter ServiceOrder single lifecycle boundary facts/events/OpenAPI/reasoncodes docs-only planning, or keep DS-8 as gap evidence. | GitHub Issue, PR comment, or repo-file decision with one selected answer. | Any HPRD, design.md, runtime, production, provider, payment, billing, refund, settlement, CustomerAsset deduction, or service fulfillment request. |
| Contracts / Architect | Conditional | If DS-9 is selected, prepare only hl-contracts docs-only planning, trace, index, changelog, and deterministic tests for one ServiceOrder lifecycle boundary. | hl-contracts PR with tests and explicit no active registry write. | Active registry, formal facts/events/OpenAPI/reasoncodes registry writes, HPRD, runtime, or production work. |
| Engineering | No runtime dispatch | Read-only review or check-only / sandbox pre-research only after a GitHub SSOT names the exact question. | Review note, spike report, or check-only PR that states no runtime authorization. | Runtime implementation, formal route, provider path, data mutation, deploy/release, workflow, secrets, and production config. |
| QA / Gate | Yes | Check PR body, E dual review, No Evidence No Done, candidate-only boundaries, required checks, and no-misread wording. | GitHub review / check result / acceptance comment. | Any approval that implies active contract, runtime, production, payment, asset deduction, or service fulfillment authorization. |

## Now Dispatchable

- This hl-dispatch repo-file and PR as the process landing readback / decision_request / dispatch package.
- PM decision task for DS-9, limited to one question and GitHub SSOT evidence.
- QA / Gate review of this package and any later DS-9 decision PR / Issue.
- Contracts / Architect read-only preparation notes that do not modify hl-contracts unless DS-9 is selected.

## Must Wait

- hl-contracts DS-9 docs-only planning PR must wait for a DS-9 GitHub SSOT selection.
- Any HPRD or design.md task must wait for explicit HPRD / design authorization.
- Any platform engineering runtime task must wait for active contract, HPRD, design.md, runtime design, test plan, rollback, and production boundary SSOT.
- Any production, provider, payment, billing, refund, settlement, CustomerAsset deduction, or service fulfillment task must wait for separate GitHub SSOT and must not be derived from DS-4 through DS-8.

## E Dual Review

### E1 Evidence Audit

| Question | Answer |
| --- | --- |
| Has the recovery flow been exercised? | Yes. DS-4 through DS-8 show merged PR evidence, tests, readbacks, and non-authorization boundaries. |
| Is there permanent product-engineering process authorization? | No. No Founder / Gate GitHub SSOT upgrading Delivery Recovery Mode v0.1 into a permanent unique process was found. |
| Are Formal Object Chain objects active? | No. SalesOrder, CustomerAsset, ServiceOrder, and PaymentCheckout remain candidate-only / draft candidate materials. |
| Are active contract, active registry, HPRD, design.md, runtime, provider, payment, billing, refund, settlement, production, CustomerAsset deduction, or service fulfillment authorized? | No. They remain absent and blocked. |
| Can task dispatch happen now? | Yes, but only as GitHub SSOT-backed docs-only / decision / review tasks with explicit non-runtime boundaries. |

### E2 Impact Audit

| Area | Impact |
| --- | --- |
| PM | PM can receive a DS-9 decision task. PM cannot turn DS-8 into HPRD, design.md, or runtime authorization. |
| contracts | Contracts can proceed only if DS-9 is selected, and only as docs-only planning / trace / tests with no active registry. |
| platform | No runtime work is authorized. Check-only / sandbox pre-research requires a separate GitHub SSOT question. |
| dispatch | hl-dispatch becomes the process landing SSOT through this file and PR; README points to it. |
| QA / Gate | QA / Gate can enforce PR body quality, E dual review, No Evidence No Done, checks green, and boundary wording. |
| rollback | Revert this PR to remove the flow landing package and README pointer. DS-4 through DS-8 evidence remains intact unless separately reverted. |
| misread risk | Main risk is reading a successful recovery mode as permanent process authorization, or reading candidate-only objects as active contracts. This package repeats the distinction and blocks runtime expansion. |

## Action Projection

| action_id | Owner | Trigger | Evidence exit |
| --- | --- | --- | --- |
| `PE-FLOW-READBACK-MERGE` | Dispatch Owner | This PR merges | Product-engineering flow recovery intake is available as GitHub SSOT. |
| `PE-FLOW-PM-DS9-DECISION` | PM / Founder / Gate | After this PR merges | GitHub decision selects DS-9 docs-only planning or keeps DS-8 as gap evidence. |
| `PE-FLOW-CONTRACTS-DS9-PREP` | Contracts / Architect | Only after DS-9 GitHub SSOT selection | hl-contracts docs-only planning PR with trace and tests, no active registry write. |
| `PE-FLOW-ENGINEERING-BLOCK-RUNTIME` | Engineering / Gate | Any runtime request appears | Block and require separate active contract, HPRD, design.md, runtime design, tests, rollback, and production boundary SSOT. |
| `PE-FLOW-QA-GATE-CHECK` | QA / Gate | Any DS-9 or process-adoption PR opens | Verify PR body, E dual review, No Evidence No Done, checks green, and no-misread boundaries. |
| `PE-FLOW-PERMANENT-PROCESS-DECISION` | Founder / Gate | If recovery flow should become formal process | Separate GitHub SSOT decision naming process version, scope, owners, gates, rollback, and template changes. |

## No Evidence, No Done

No Evidence, No Done remains active.

This package is complete only after:

- it exists as a repository file,
- the README pointer exists,
- required local checks pass,
- the PR checks pass,
- the PR merges.

No downstream DS-9, formal process upgrade, HPRD, design.md, runtime, production, payment, asset deduction, or service fulfillment work is done or authorized by this package.

## Exclusions

This readback and dispatch package does not authorize:

- active contract
- active registry write
- HPRD
- design.md
- formal runtime route
- production release
- real provider path
- real payment provider
- payment
- billing
- refund
- settlement
- CustomerAsset deduction
- service fulfillment
- business object creation
- real user data
- workflow change
- deploy or release change
- secrets
- Feishu, Project, Bitable, dashboard, or chat summary as fact source
- new runtime work order

## Rollback

Rollback is a single revert of this dispatch PR.

Reverting this PR removes only the process landing package and README pointer. It does not revert DS-4 through DS-8 evidence and does not affect any runtime, provider, payment, asset, fulfillment, production, secret, workflow, or real user state because none is created here.

## Next Stage Recommendation

Keep Delivery Recovery Mode v0.1 as the recovery-period operating flow unless Founder / Gate opens and merges a separate permanent-process GitHub SSOT decision.

For DS-9, use the smallest safe next step: ask Founder / Gate whether to authorize docs-only planning for exactly one ServiceOrder lifecycle boundary across facts/events/OpenAPI/reasoncodes planning, with active registry and runtime still blocked. If no DS-9 decision is made, keep DS-8 as gap evidence.
