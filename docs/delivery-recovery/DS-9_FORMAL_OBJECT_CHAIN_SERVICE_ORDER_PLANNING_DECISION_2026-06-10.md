# DS-9 Formal Object Chain ServiceOrder Planning Decision

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-10

## Scope

This file records the Founder direction to enter DS-9 docs-only planning after `hl-dispatch#217` blocked contracts work for lack of explicit DS-9 GitHub SSOT.

After this PR merges, this repo file and PR become the GitHub SSOT selecting DS-9 docs-only contract planning for the ServiceOrder lifecycle boundary only.

DS-9 does not authorize active contract, active registry write, facts registry write, events registry write, OpenAPI creation, reasoncodes registry write, HPRD, design.md, formal runtime, production, provider, payment, billing, refund, settlement, CustomerAsset deduction, service fulfillment, workflow, deploy/release, secrets, or real user data work.

## Task Snapshot

```yaml
package_id: MP-DELIVERY-RECOVERY-v0.1
slice_id: DS-9
track: docs_only_service_order_lifecycle_contract_planning
maturity: founder_gate_decision_recorded
type: decision_request
state: ds9_docs_only_planning_selected
risk_path: Yellow
current_date: 2026-06-10
previous_blocker_pr: https://github.com/huanlongAI/hl-dispatch/pull/217
process_flow_intake_pr: https://github.com/huanlongAI/hl-dispatch/pull/214
ds8_contracts_pr: https://github.com/huanlongAI/hl-contracts/pull/115
ds8_readback_pr: https://github.com/huanlongAI/hl-dispatch/pull/213
selected_scope: hl-contracts docs-only planning for ServiceOrder lifecycle facts/events/OpenAPI/reasoncodes gaps
selected_boundary: ServiceOrder lifecycle boundary only
current_status: DS-9 selected for docs-only planning after this PR merges.
next_action: hl-contracts creates one DS-9 docs-only planning PR with trace/index/changelog and deterministic tests.
blocked_by: Active registry, HPRD, design.md, formal runtime design, production guard, provider/payment/billing/refund/settlement boundary, CustomerAsset deduction, service fulfillment, workflow, deploy/release, secrets, and real user data authorization remain absent.
unblock_condition: This dispatch decision PR merges and the contracts PR stays inside docs-only planning.
authorization: decision record for docs-only planning only
contracts_authorization: "docs_only_planning_authorized_after_merge"
runtime_authorization: "not_authorized"
active_contract_authorization: "not_authorized"
active_registry_authorization: "not_authorized"
hprd_authorization: "not_authorized"
design_md_authorization: "not_authorized"
production_authorization: "not_authorized"
close_condition: This dispatch PR merges with verification evidence and no open PR remains unless explicitly blocked.
```

## Decision

Founder / Gate selects:

```yaml
decision_request:
  class: decision_request
  slice_id: DS-9
  selected_answer: authorize_ds9_docs_only_contract_planning
  selected_boundary: ServiceOrder lifecycle boundary only
  selected_repo: hl-contracts
  allowed_scope:
    - ServiceOrder lifecycle facts planning gaps
    - ServiceOrder lifecycle events planning gaps
    - ServiceOrder lifecycle OpenAPI planning gaps
    - ServiceOrder lifecycle reasoncodes planning gaps
    - INDEX.md pointer
    - TRACEABILITY.yaml entry
    - CHANGELOG.md entry
    - deterministic tests
  blocked_scope:
    - active_contract
    - active_registry_write
    - facts_registry_write
    - events_registry_write
    - openapi_creation
    - reasoncodes_registry_write
    - HPRD
    - design_md
    - formal_runtime
    - provider_integration
    - payment
    - billing
    - refund
    - settlement
    - CustomerAsset_deduction
    - service_fulfillment
    - production
    - workflow_change
    - deploy_release
    - secrets
    - real_user_data
  required_contracts_pr_title: "contracts: add DS-9 service order lifecycle contract planning"
  required_acceptance_readback: "docs(dispatch): add DS-9 service order contract planning evidence"
```

## Boundary Selection

DS-9 selects the ServiceOrder lifecycle boundary row from the DS-8 matrix.

Allowed: docs-only planning that names the gaps between candidate-only ServiceOrder material and a future active ServiceOrder state model.

Blocked adjacent boundaries:

- SalesOrder source mutation or active SalesOrder interpretation
- CustomerAsset deduction, balance mutation, lock, reserve, consume, adjustment, or rollback
- PaymentCheckout provider, payment, billing, refund, settlement, reconciliation, or provider config
- service fulfillment start, completion, no-show, fulfillment event emission, inventory/resource mutation, or customer notification action

## E Dual Review

### E1 Evidence Audit

| Question | DS-9 answer |
| --- | --- |
| Current GitHub SSOT | This PR becomes the DS-9 GitHub SSOT after merge. Before merge, `hl-dispatch#217` remains the latest blocker readback. |
| DS-9 explicitly authorized? | Yes, after this PR merges, only for docs-only `hl-contracts` planning. |
| Candidate-only status | SalesOrder, CustomerAsset, ServiceOrder, and PaymentCheckout remain candidate-only / draft candidate evidence. |
| Active / HPRD / runtime authorization | Not present and not granted. |
| Docs-only planning authorization | Authorized only for ServiceOrder lifecycle facts/events/OpenAPI/reasoncodes planning gaps, trace/index/changelog, and deterministic tests. |
| Missing evidence | Active registry decision, active facts/events/OpenAPI/reasoncodes registry changes, HPRD, design.md, formal runtime design, tests for runtime, rollback for runtime, production/provider/payment/billing/refund/settlement boundaries, CustomerAsset deduction authorization, service fulfillment authorization, workflow authorization, deploy/release authorization, secrets authorization, and real user data authorization remain absent. |

### E2 Impact Audit

| Area | Impact |
| --- | --- |
| contracts | `hl-contracts` may add one docs-only DS-9 planning artifact, index / trace / changelog, and deterministic tests. It must not write active registry, facts registry, events registry, OpenAPI, reasoncodes registry, capability blueprint active state, or runtime work order. |
| platform | No platform change. No backend endpoint, CLI, persistence, provider path, production config, or real data path is authorized. |
| dispatch | This decision record now unblocks the bounded contracts docs-only PR; a later dispatch readback must record acceptance after contracts merges. |
| rollback | Revert this PR to restore DS-9 to blocked state from `hl-dispatch#217`. If a contracts PR merged after this decision, revert the dispatch acceptance readback first, then the contracts PR, then this decision if needed. |
| misread risk | Main risk is treating DS-9 planning as active ServiceOrder or runtime authorization. The PR body and contracts tests must repeat the blocked scope and require `active_contract_registry_write: false` and `runtime_authorization: "not_authorized"`. |

## Evidence Links

| Evidence | State | Meaning |
| --- | --- | --- |
| [hl-dispatch#214](https://github.com/huanlongAI/hl-dispatch/pull/214) | merged | Product-engineering flow recovery intake; DS-9 decision_request only. |
| [hl-dispatch#217](https://github.com/huanlongAI/hl-dispatch/pull/217) | merged | DS-9 blocker readback before this decision. |
| [hl-contracts#115](https://github.com/huanlongAI/hl-contracts/pull/115) | merged | DS-8 ServiceOrder lifecycle boundary gap docs-only evidence. |
| [hl-dispatch#213](https://github.com/huanlongAI/hl-dispatch/pull/213) | merged | DS-8 acceptance readback. |
| [hl-contracts#99](https://github.com/huanlongAI/hl-contracts/pull/99) | merged | SalesOrder candidate-only evidence. |
| [hl-contracts#96](https://github.com/huanlongAI/hl-contracts/pull/96) | merged | CustomerAsset candidate-only evidence. |
| [hl-contracts#111](https://github.com/huanlongAI/hl-contracts/pull/111) | merged | ServiceOrder candidate-only evidence. |
| [hl-contracts#112](https://github.com/huanlongAI/hl-contracts/pull/112) | merged | PaymentCheckout candidate-only evidence. |

## Commands Run

```text
command: git diff --check
result: pass
output summary: no whitespace errors
```

```text
command: PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-github-language-gate.py
result: pass
output summary: 14 tests OK
```

```text
command: PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-action-projection-exporter.py
result: pass
output summary: 6 tests OK
```

```text
command: rg -n "task-snapshot:v1|decision_request|No Evidence, No Done|DS-9|docs_only_service_order_lifecycle_contract_planning|hl-dispatch#217|hl-contracts#115|active registry|formal runtime|real payment provider|real user data|CustomerAsset deduction|service fulfillment" docs/delivery-recovery/DS-9_FORMAL_OBJECT_CHAIN_SERVICE_ORDER_PLANNING_DECISION_2026-06-10.md docs/delivery-recovery/README.md
result: pass
output summary: required DS-9 decision markers found
```

## Action Projection

| action_id | Owner | Trigger | Evidence exit |
| --- | --- | --- | --- |
| `DS9-AUTHORIZE-CONTRACTS-DOCS-ONLY` | Founder / Gate | This PR merges | `hl-contracts` may open the bounded DS-9 docs-only planning PR. |
| `DS9-BLOCK-ACTIVE-REGISTRY` | Contracts / Gate | Any DS-9 change writes active registry or active facts/events/OpenAPI/reasoncodes registry | Block and link this decision. |
| `DS9-BLOCK-RUNTIME` | Engineering / Gate | Any runtime/provider/payment/asset/fulfillment request | Require separate GitHub SSOT with active registry, HPRD, design.md, runtime design, tests, rollback, and production boundaries. |
| `DS9-ACCEPTANCE-READBACK` | Dispatch | After contracts DS-9 PR merges | Add DS-9 acceptance evidence in `hl-dispatch`. |

## No Evidence, No Done

No Evidence, No Done remains active.

DS-9 is selected only for a bounded docs-only planning PR after this GitHub PR merges. DS-9 is not done until contracts evidence, tests, and dispatch acceptance readback exist.

No Evidence, No Done remains active for every expansion beyond this scope.

## Exclusions

This decision does not authorize:

- active contract or active registry write
- facts registry write
- events registry write
- OpenAPI creation
- reasoncodes registry write
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
- Feishu, Project, Bitable, dashboard, or chat summary as fact source
- workflow change
- deploy or release change
- secrets
- new runtime work order

## Rollback

Rollback is a single revert of this dispatch decision PR if no downstream DS-9 contracts PR has merged.

If downstream DS-9 contracts and readback PRs have merged, rollback in reverse order:

1. Revert the DS-9 dispatch acceptance readback.
2. Revert the DS-9 `hl-contracts` docs-only planning PR.
3. Revert this dispatch decision PR.

No runtime/provider/payment/asset/fulfillment state exists to unwind.

## Next Stage

Proceed to `hl-contracts` DS-9 docs-only ServiceOrder lifecycle contract planning after this PR merges.

The next PR must keep `active_contract_registration: false`, `active_contract_registry_write: false`, `facts_registry_write: false`, `events_registry_write: false`, `openapi_creation: false`, `reasoncodes_registry_write: false`, and `runtime_authorization: "not_authorized"`.
