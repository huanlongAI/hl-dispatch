# DS-10A Formal Object Chain ServiceOrder Facts Proposal Decision

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-10

## Scope

This file records the Founder direction to select DS-10A after DS-9 completed docs-only ServiceOrder lifecycle contract planning.

After this PR merges, this repo file and PR become the GitHub SSOT selecting DS-10A: `hl-contracts` docs-only ServiceOrder lifecycle facts proposal.

DS-10A does not authorize active contract, active registry write, facts registry write, events registry write, OpenAPI creation, reasoncodes registry write, HPRD, design.md, formal runtime, production, provider, payment, billing, refund, settlement, CustomerAsset deduction, service fulfillment, workflow, deploy/release, secrets, or real user data work.

## Task Snapshot

```yaml
package_id: MP-DELIVERY-RECOVERY-v0.1
slice_id: DS-10A
track: docs_only_service_order_lifecycle_facts_proposal
maturity: founder_gate_decision_recorded
type: decision_request
state: ds10a_facts_proposal_selected
risk_path: Yellow
current_date: 2026-06-10
upstream_decision_pr: https://github.com/huanlongAI/hl-dispatch/pull/218
upstream_contracts_pr: https://github.com/huanlongAI/hl-contracts/pull/116
upstream_readback_pr: https://github.com/huanlongAI/hl-dispatch/pull/219
selected_scope: hl-contracts docs-only ServiceOrder lifecycle facts proposal
selected_boundary: ServiceOrder lifecycle facts proposal only
current_status: DS-10A selected for docs-only proposal after this PR merges.
next_action: hl-contracts creates one DS-10A docs-only facts proposal PR with trace/index/changelog and deterministic tests.
blocked_by: Active registry, facts registry write, events registry write, OpenAPI creation, reasoncodes registry write, HPRD, design.md, formal runtime design, production guard, provider/payment/billing/refund/settlement boundary, CustomerAsset deduction, service fulfillment, workflow, deploy/release, secrets, and real user data authorization remain absent.
unblock_condition: This dispatch decision PR merges and the contracts PR stays inside docs-only facts proposal.
authorization: decision record for docs-only facts proposal only
contracts_authorization: "docs_only_facts_proposal_authorized_after_merge"
facts_registry_write_authorization: "not_authorized"
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
  slice_id: DS-10A
  selected_answer: authorize_ds10a_docs_only_service_order_lifecycle_facts_proposal
  selected_boundary: ServiceOrder lifecycle facts proposal only
  selected_repo: hl-contracts
  allowed_scope:
    - ServiceOrder lifecycle facts proposal document
    - proposed fact families only
    - fact naming constraints
    - fact non-judgment constraints
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
  required_contracts_pr_title: "contracts: add DS-10A service order lifecycle facts proposal"
  required_acceptance_readback: "docs(dispatch): add DS-10A service order facts proposal evidence"
```

## Boundary Selection

DS-10A selects facts proposal first because Facts are upstream in the Huanlong world model:

Reality -> Facts -> Decisions -> Actions -> new Facts.

Allowed: docs-only proposal that describes what future ServiceOrder lifecycle facts may need to capture, without adding or changing `facts/facts-catalog.md`.

Facts proposal constraints:

- Facts describe what happened or what was observed.
- Facts must not encode `can`, `eligible`, `should`, approval, authorization, permission, or policy judgment.
- Facts proposal must not create fact IDs, registry partitions, runtime persistence, or production behavior.

Blocked adjacent lanes:

- events proposal
- OpenAPI proposal
- reasoncodes proposal
- facts registry write
- active registry write
- HPRD / design.md
- formal runtime

## E Dual Review

### E1 Evidence Audit

| Question | DS-10A answer |
| --- | --- |
| Current GitHub SSOT | This PR becomes the DS-10A GitHub SSOT after merge. |
| Upstream evidence | `hl-dispatch#218`, `hl-contracts#116`, and `hl-dispatch#219` completed DS-9 docs-only planning. |
| DS-10A explicitly authorized? | Yes, after this PR merges, only for docs-only `hl-contracts` facts proposal. |
| Candidate-only status | SalesOrder, CustomerAsset, ServiceOrder, and PaymentCheckout remain candidate-only / draft candidate evidence. |
| Active / HPRD / runtime authorization | Not present and not granted. |
| Facts registry write authorization | Not present and not granted. |
| Missing evidence | Active registry decision, facts registry write, events registry write, OpenAPI creation, reasoncodes registry write, HPRD, design.md, formal runtime design, tests for runtime, rollback for runtime, production/provider/payment/billing/refund/settlement boundaries, CustomerAsset deduction authorization, service fulfillment authorization, workflow authorization, deploy/release authorization, secrets authorization, and real user data authorization remain absent. |

### E2 Impact Audit

| Area | Impact |
| --- | --- |
| contracts | `hl-contracts` may add one docs-only DS-10A facts proposal artifact, index / trace / changelog, and deterministic tests. It must not write `facts/facts-catalog.md`, active registry, events registry, OpenAPI, reasoncodes registry, capability blueprint active state, or runtime work order. |
| platform | No platform change. No backend endpoint, CLI, persistence, provider path, production config, or real data path is authorized. |
| dispatch | This decision record unblocks the bounded contracts docs-only facts proposal PR; a later dispatch readback must record acceptance after contracts merges. |
| rollback | Revert this PR to return DS-10A to unselected state. If a contracts PR merged after this decision, revert the dispatch acceptance readback first, then the contracts PR, then this decision if needed. |
| misread risk | Main risk is treating facts proposal as facts registry write or runtime authorization. The PR body and contracts tests must repeat `facts_registry_write: false`, `active_contract_registry_write: false`, and `runtime_authorization: "not_authorized"`. |

## Evidence Links

| Evidence | State | Meaning |
| --- | --- | --- |
| [hl-dispatch#218](https://github.com/huanlongAI/hl-dispatch/pull/218) | merged | DS-9 decision selecting docs-only planning. |
| [hl-contracts#116](https://github.com/huanlongAI/hl-contracts/pull/116) | merged | DS-9 ServiceOrder lifecycle contract planning evidence. |
| [hl-dispatch#219](https://github.com/huanlongAI/hl-dispatch/pull/219) | merged | DS-9 acceptance readback and next stage recommendation. |
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
command: rg required DS-10A decision markers
result: pass
output summary: required DS-10A decision markers found
```

## Action Projection

| action_id | Owner | Trigger | Evidence exit |
| --- | --- | --- | --- |
| `DS10A-AUTHORIZE-CONTRACTS-FACTS-PROPOSAL` | Founder / Gate | This PR merges | `hl-contracts` may open the bounded DS-10A docs-only facts proposal PR. |
| `DS10A-BLOCK-FACTS-REGISTRY-WRITE` | Contracts / Gate | Any DS-10A change modifies `facts/facts-catalog.md` or creates formal fact IDs / partitions | Block and link this decision. |
| `DS10A-BLOCK-RUNTIME` | Engineering / Gate | Any runtime/provider/payment/asset/fulfillment request | Require separate GitHub SSOT with active registry, HPRD, design.md, runtime design, tests, rollback, and production boundaries. |
| `DS10A-ACCEPTANCE-READBACK` | Dispatch | After contracts DS-10A PR merges | Add DS-10A acceptance evidence in `hl-dispatch`. |

## No Evidence, No Done

No Evidence, No Done remains active.

DS-10A is selected only for a bounded docs-only facts proposal PR after this GitHub PR merges. DS-10A is not done until contracts evidence, tests, and dispatch acceptance readback exist.

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

Rollback is a single revert of this dispatch decision PR if no downstream DS-10A contracts PR has merged.

If downstream DS-10A contracts and readback PRs have merged, rollback in reverse order:

1. Revert the DS-10A dispatch acceptance readback.
2. Revert the DS-10A `hl-contracts` docs-only facts proposal PR.
3. Revert this dispatch decision PR.

No runtime/provider/payment/asset/fulfillment state exists to unwind.

## Next Stage

Proceed to `hl-contracts` DS-10A docs-only ServiceOrder lifecycle facts proposal after this PR merges.

The next PR must keep `facts_registry_write: false`, `active_contract_registration: false`, `active_contract_registry_write: false`, `events_registry_write: false`, `openapi_creation: false`, `reasoncodes_registry_write: false`, and `runtime_authorization: "not_authorized"`.
