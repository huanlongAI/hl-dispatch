# DS-11A Formal Object Chain ServiceOrder Lifecycle Observation Facts Proposal Decision

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-10

## Scope

This file records the Founder / Gate direction after DS-10A acceptance: continue only into a narrower docs-only facts registry proposal for exactly one DS-10A proposed family.

After this PR merges, this repo file and PR become the GitHub SSOT selecting DS-11A: `hl-contracts` docs-only ServiceOrder lifecycle observation facts registry proposal.

DS-11A selects exactly one proposed family from DS-10A: lifecycle observation facts. It does not authorize writing `facts/facts-catalog.md`, creating formal fact IDs, creating fact partitions, active contract, active registry write, events registry write, OpenAPI creation, reasoncodes registry write, HPRD, design.md, formal runtime, production, provider, payment, billing, refund, settlement, CustomerAsset deduction, service fulfillment, workflow, deploy/release, secrets, or real user data work.

## Task Snapshot

```yaml
package_id: MP-DELIVERY-RECOVERY-v0.1
slice_id: DS-11A
track: docs_only_service_order_lifecycle_observation_facts_registry_proposal
maturity: founder_gate_decision_recorded
type: decision_request
state: ds11a_lifecycle_observation_facts_proposal_selected
risk_path: Yellow
current_date: 2026-06-10
upstream_decision_pr: https://github.com/huanlongAI/hl-dispatch/pull/220
upstream_contracts_pr: https://github.com/huanlongAI/hl-contracts/pull/117
upstream_readback_pr: https://github.com/huanlongAI/hl-dispatch/pull/221
selected_scope: hl-contracts docs-only ServiceOrder lifecycle observation facts registry proposal
selected_boundary: lifecycle observation facts family only
selected_family: lifecycle_observation_facts
current_status: DS-11A selected for docs-only proposal after this PR merges.
next_action: hl-contracts creates one DS-11A docs-only lifecycle observation facts registry proposal PR with trace/index/changelog and deterministic tests.
blocked_by: Facts registry write, formal fact IDs, formal fact partitions, active registry, active contract, events registry write, OpenAPI creation, reasoncodes registry write, HPRD, design.md, formal runtime design, production guard, provider/payment/billing/refund/settlement boundary, CustomerAsset deduction, service fulfillment, workflow, deploy/release, secrets, and real user data authorization remain absent.
unblock_condition: This dispatch decision PR merges and the contracts PR stays inside docs-only lifecycle observation facts registry proposal.
authorization: decision record for docs-only lifecycle observation facts registry proposal only
contracts_authorization: "docs_only_lifecycle_observation_facts_registry_proposal_authorized_after_merge"
facts_catalog_write_authorization: "not_authorized"
facts_registry_write_authorization: "not_authorized"
formal_fact_id_authorization: "not_authorized"
formal_fact_partition_authorization: "not_authorized"
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
  slice_id: DS-11A
  selected_answer: authorize_ds11a_docs_only_service_order_lifecycle_observation_facts_registry_proposal
  selected_boundary: lifecycle observation facts family only
  selected_repo: hl-contracts
  selected_family: lifecycle_observation_facts
  allowed_scope:
    - ServiceOrder lifecycle observation facts registry proposal document
    - proposed future registry rows for lifecycle observation facts only
    - proposed observation fields for observed state, source, observed_at, recorder, evidence, and trace
    - fact non-judgment constraints
    - INDEX.md pointer
    - TRACEABILITY.yaml entry
    - CHANGELOG.md entry
    - deterministic tests
  blocked_scope:
    - facts_catalog_write
    - facts_registry_write
    - formal_fact_id_allocation
    - formal_fact_partition_creation
    - active_contract
    - active_registry_write
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
  required_contracts_pr_title: "contracts: add DS-11A service order lifecycle observation facts proposal"
  required_acceptance_readback: "docs(dispatch): add DS-11A service order lifecycle observation facts evidence"
```

## Boundary Selection

DS-11A selects lifecycle observation facts because it is the narrowest DS-10A family that remains inside the Huanlong Facts invariant:

Reality -> Facts -> Decisions -> Actions -> new Facts.

Allowed: docs-only proposal that describes how future ServiceOrder lifecycle observation facts may capture observed lifecycle state, state source, observation time, recorder evidence, evidence reference, and trace reference.

Facts proposal constraints:

- Facts describe what happened or what was observed.
- Facts must not encode `can`, `eligible`, `should`, approval, authorization, permission, policy judgment, entitlement, payment result, asset deduction result, or fulfillment result.
- Proposed fields are not formal fact IDs.
- Proposed fields are not a registry partition.
- Proposed fields are not runtime persistence design.
- Proposed fields are not production capture behavior.

Blocked DS-10A families for this slice:

- source reference facts
- operator evidence facts
- audit trace facts

Blocked adjacent lanes:

- direct `facts/facts-catalog.md` write
- formal fact ID allocation
- formal fact partition creation
- events proposal
- OpenAPI proposal
- reasoncodes proposal
- active registry write
- HPRD / design.md
- formal runtime

## E Dual Review

### E1 Evidence Audit

| Question | DS-11A answer |
| --- | --- |
| Current GitHub SSOT | This PR becomes the DS-11A GitHub SSOT after merge. |
| Upstream evidence | `hl-dispatch#220`, `hl-contracts#117`, and `hl-dispatch#221` completed DS-10A docs-only ServiceOrder lifecycle facts proposal. |
| DS-11A explicitly authorized? | Yes, after this PR merges, only for `hl-contracts` docs-only lifecycle observation facts registry proposal. |
| Selected DS-10A family | lifecycle observation facts only. |
| Candidate-only status | SalesOrder, CustomerAsset, ServiceOrder, and PaymentCheckout remain candidate-only / draft candidate evidence. |
| Facts catalog / registry write authorization | Not present and not granted. |
| Active / HPRD / runtime authorization | Not present and not granted. |
| Missing evidence | Facts registry write, formal fact IDs, formal fact partitions, active registry decision, active contract, events registry write, OpenAPI creation, reasoncodes registry write, HPRD, design.md, formal runtime design, runtime tests, runtime rollback, production/provider/payment/billing/refund/settlement boundaries, CustomerAsset deduction authorization, service fulfillment authorization, workflow authorization, deploy/release authorization, secrets authorization, and real user data authorization remain absent. |

### E2 Impact Audit

| Area | Impact |
| --- | --- |
| contracts | `hl-contracts` may add one docs-only DS-11A lifecycle observation facts registry proposal artifact, index / trace / changelog, and deterministic tests. It must not write `facts/facts-catalog.md`, active registry, events registry, OpenAPI, reasoncodes registry, capability blueprint active state, or runtime work order. |
| platform | No platform change. No backend endpoint, CLI, persistence, provider path, production config, or real data path is authorized. |
| dispatch | This decision record unblocks the bounded contracts docs-only DS-11A PR; a later dispatch readback must record acceptance after contracts merges. |
| rollback | Revert this PR to return DS-11A to unselected state. If a contracts PR merged after this decision, revert the dispatch acceptance readback first, then the contracts PR, then this decision if needed. |
| misread risk | Main risk is treating registry proposal as registry write or runtime authorization. The PR body and contracts tests must repeat `facts_registry_write: false`, `facts_catalog_write: false`, `active_contract_registry_write: false`, and `runtime_authorization: "not_authorized"`. |

## Evidence Links

| Evidence | State | Meaning |
| --- | --- | --- |
| [hl-dispatch#220](https://github.com/huanlongAI/hl-dispatch/pull/220) | merged | DS-10A decision selecting docs-only facts proposal. |
| [hl-contracts#117](https://github.com/huanlongAI/hl-contracts/pull/117) | merged | DS-10A ServiceOrder lifecycle facts proposal evidence. |
| [hl-dispatch#221](https://github.com/huanlongAI/hl-dispatch/pull/221) | merged | DS-10A acceptance readback and next stage recommendation. |
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
command: rg required DS-11A decision markers
result: pass
output summary: required DS-11A decision markers found
```

## Action Projection

| action_id | Owner | Trigger | Evidence exit |
| --- | --- | --- | --- |
| `DS11A-AUTHORIZE-CONTRACTS-LIFECYCLE-OBSERVATION-FACTS-PROPOSAL` | Founder / Gate | This PR merges | `hl-contracts` may open the bounded DS-11A docs-only lifecycle observation facts registry proposal PR. |
| `DS11A-BLOCK-FACTS-CATALOG-WRITE` | Contracts / Gate | Any DS-11A change modifies `facts/facts-catalog.md` or creates formal fact IDs / partitions | Block and link this decision. |
| `DS11A-BLOCK-RUNTIME` | Engineering / Gate | Any runtime/provider/payment/asset/fulfillment request | Require separate GitHub SSOT with active registry, HPRD, design.md, runtime design, tests, rollback, and production boundaries. |
| `DS11A-ACCEPTANCE-READBACK` | Dispatch | After contracts DS-11A PR merges | Add DS-11A acceptance evidence in `hl-dispatch`. |

## No Evidence, No Done

No Evidence, No Done remains active.

DS-11A is selected only for a bounded docs-only lifecycle observation facts registry proposal PR after this GitHub PR merges. DS-11A is not done until contracts evidence, tests, and dispatch acceptance readback exist.

No Evidence, No Done remains active for every expansion beyond this scope.

## Exclusions

This decision does not authorize:

- `facts/facts-catalog.md` write
- facts registry write
- formal fact ID allocation
- formal fact partition creation
- active contract or active registry write
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

Rollback is a single revert of this dispatch decision PR if no downstream DS-11A contracts PR has merged.

If downstream DS-11A contracts and readback PRs have merged, rollback in reverse order:

1. Revert the DS-11A dispatch acceptance readback.
2. Revert the DS-11A `hl-contracts` docs-only lifecycle observation facts registry proposal PR.
3. Revert this dispatch decision PR.

No runtime/provider/payment/asset/fulfillment state exists to unwind.

## Next Stage

Proceed to `hl-contracts` DS-11A docs-only ServiceOrder lifecycle observation facts registry proposal after this PR merges.

The next PR must keep `facts_catalog_write: false`, `facts_registry_write: false`, `active_contract_registration: false`, `active_contract_registry_write: false`, `events_registry_write: false`, `openapi_creation: false`, `reasoncodes_registry_write: false`, and `runtime_authorization: "not_authorized"`.
