# DS-15 Formal Object Chain Lifecycle Observation Facts Option B Decision

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-10

## Scope

DS-15 records the Founder / Gate selection of Option B after DS-14.

Option B is authorized only as a minimal, exact, docs-only `hl-contracts` facts catalog write subset. The approved subset contains exactly one descriptive fact:

- `service_order.lifecycle.observed_state`

This decision does not authorize active contract, active registry beyond this exact facts catalog row, HPRD, design.md, formal runtime, events registry write, OpenAPI creation, reasoncodes registry write, rules registry write, provider, payment, billing, refund, settlement, CustomerAsset deduction, service fulfillment, production, workflow, deploy / release, secrets, or real user data work.

`service_order.lifecycle.observed_state` must stay descriptive only: it names an observed ServiceOrder lifecycle state value from bounded evidence. It must not encode can / eligible / should / approval / authorization / permission / policy judgment, state-machine transition authority, fulfillment authority, payment authority, asset deduction authority, or workflow action semantics.

## Task Snapshot

```yaml
package_id: MP-DELIVERY-RECOVERY-v0.1
slice_id: DS-15
track: Option B
maturity: founder_gate_decision_recorded
type: decision_request
state: dispatch_decision_only
risk_path: Yellow
current_date: 2026-06-10
source_selection:
  channel: active_cowork_thread
  selected_option: Option B
  selected_at: 2026-06-10
previous_slices:
  ds14_readback: https://github.com/huanlongAI/hl-dispatch/pull/226
  ds13_readback: https://github.com/huanlongAI/hl-dispatch/pull/225
  ds12_readback: https://github.com/huanlongAI/hl-dispatch/pull/224
  ds11a_decision: https://github.com/huanlongAI/hl-dispatch/pull/222
  ds11a_contracts: https://github.com/huanlongAI/hl-contracts/pull/118
  ds11a_readback: https://github.com/huanlongAI/hl-dispatch/pull/223
decision: authorize_exact_facts_catalog_write_subset
approved_repository: huanlongAI/hl-contracts
approved_files:
  - facts/facts-catalog.md
  - CONTEXT.md
  - INDEX.md
  - TRACEABILITY.yaml
  - CHANGELOG.md
  - tests
approved_fact_subset:
  - service_order.lifecycle.observed_state
approved_fact_limit: exactly_one_descriptive_fact
next_action: Create one hl-contracts PR that writes only the approved fact subset with deterministic tests, evidence, and rollback.
blocked_by: Any request to add fields beyond service_order.lifecycle.observed_state, or to expand into runtime, provider/payment/billing/refund/settlement, CustomerAsset deduction, service fulfillment, production, workflow, secrets, or real user data.
authorization: exact facts catalog write subset only.
close_condition: DS-15 decision PR merges, the bounded hl-contracts facts catalog PR merges with checks, and dispatch acceptance readback merges.
```

## Decision

```yaml
option_b_decision:
  decision_id: DS-15-OPTION-B-SERVICE-ORDER-LIFECYCLE-OBSERVED-STATE
  selected_option: Option B
  option_name: authorize_exact_facts_catalog_write_subset
  selected_subset:
    - service_order.lifecycle.observed_state
  field_semantics:
    service_order.lifecycle.observed_state:
      class: descriptive_observation_fact
      meaning: The lifecycle state value observed from bounded ServiceOrder evidence.
      prohibited_semantics:
        - can
        - eligible
        - should
        - approval
        - authorization
        - permission
        - policy_judgment
        - state_machine_transition_authority
        - fulfillment_authority
        - payment_authority
        - asset_deduction_authority
        - workflow_action
  allowed_contracts_scope:
    - facts_catalog_write_for_exact_subset
    - facts_catalog_last_confirmed_if_required_by_current_repo_rules
    - index_trace_changelog_updates
    - deterministic_tests
  not_authorized:
    - additional_service_order_lifecycle_facts
    - facts_registry_expansion_beyond_exact_subset
    - active_contract_expansion
    - active_registry_expansion_beyond_exact_subset
    - events_registry_write
    - openapi_creation
    - reasoncodes_registry_write
    - rules_registry_write
    - hprd
    - design_md
    - formal_runtime
    - provider_integration
    - real_payment_provider
    - payment
    - billing
    - refund
    - settlement
    - customer_asset_deduction
    - service_fulfillment
    - production
    - deploy_release
    - workflow_change
    - secrets
    - real_user_data
```

## E Dual Review

### E1 Evidence Audit

| Question | DS-15 answer |
| --- | --- |
| Current GitHub SSOT before this PR | DS-11A proposal and DS-12/13/14 readbacks are merged; none authorized facts catalog write. |
| New Founder / Gate selection | The active Cowork thread selected Option B on 2026-06-10; this PR becomes the GitHub SSOT only after merge. |
| `facts/facts-catalog.md` write authorization | Authorized only after this PR merges, and only for `service_order.lifecycle.observed_state`. |
| Proposal / candidate-only status | Formal Object Chain objects remain candidate-only. This decision does not make SalesOrder, CustomerAsset, ServiceOrder, or PaymentCheckout active contracts. |
| Active / HPRD / design / runtime authorization | Not present. Runtime, provider/payment, CustomerAsset deduction, service fulfillment, production, workflow, secrets, and real user data remain blocked. |
| Missing evidence after this PR | Contracts implementation PR, focused RED/GREEN test evidence, adjacent tests, registry guard, checks, merge evidence, and dispatch acceptance readback. |

### E2 Impact Audit

| Area | Impact |
| --- | --- |
| contracts | Allows one bounded `hl-contracts` PR to write `service_order.lifecycle.observed_state` into `facts/facts-catalog.md` and update Last Confirmed / INDEX / TRACEABILITY / CHANGELOG / deterministic tests as required by current repo rules. |
| platform | No platform impact. No backend code, API, persistence, provider, payment, asset, fulfillment, production config, workflow, secrets, or real data path is authorized. |
| dispatch | This decision PR plus a later acceptance readback after the contracts PR merges. |
| rollback | Revert the contracts PR, then revert the dispatch acceptance readback and this decision PR if the decision itself must be removed. |
| misread risk | Main risk is treating `service_order.lifecycle.observed_state` as a policy decision, state machine, fulfillment gate, or runtime capture contract. The approved field must remain descriptive-only and cannot imply action authority. |

## Acceptance Criteria

```yaml
acceptance_criteria:
  decision_pr:
    - merges_as_github_ssot_before_contracts_write
    - contains_exact_subset
    - contains_e_dual_review
    - contains_non_authorization_boundaries
  contracts_pr:
    - writes_exactly_one_fact_key
    - keeps_fact_descriptive_only
    - updates_required_indexes_trace_changelog
    - includes_focused_red_green_test_evidence
    - includes_adjacent_ds_tests
    - includes_yaml_parse_if_traceability_changes
    - includes_registry_guard_for_events_apis_reasoncodes_rules_runtime
    - includes_git_diff_checks
  dispatch_readback:
    - records_contracts_merge_evidence
    - repeats_non_runtime_boundaries
    - records_tests_and_rollback
```

## Commands Run

### Dispatch verification

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
command: rg -n "task-snapshot:v1|DS-15|Option B|authorize_exact_facts_catalog_write_subset|service_order.lifecycle.observed_state|facts/facts-catalog.md|descriptive_observation_fact|No Evidence, No Done|DS15-OPTION-B-DECISION|DS15-CONTRACTS-EXACT-SUBSET" docs/delivery-recovery/DS-15_FORMAL_OBJECT_CHAIN_LIFECYCLE_OBSERVATION_FACTS_OPTION_B_DECISION_2026-06-10.md docs/delivery-recovery/README.md
result: pass
output summary: required DS-15 markers found
```

## Action Projection

| action_id | Owner | Trigger | Evidence exit |
| --- | --- | --- | --- |
| `DS15-OPTION-B-DECISION` | Founder / Gate | This PR merges | GitHub SSOT authorizes exact `facts/facts-catalog.md` write subset. |
| `DS15-CONTRACTS-EXACT-SUBSET` | Contracts Owner | After this PR merges | Add only `service_order.lifecycle.observed_state` to `facts/facts-catalog.md` with required trace/index/changelog/tests. |
| `DS15-BLOCK-EXPANSION` | Gate / Contracts / Engineering | Any request exceeds the exact subset | Block and link this decision. |
| `DS15-BLOCK-RUNTIME` | Gate / Engineering | Any runtime/provider/payment/asset/fulfillment/production request appears | Block until separate active registry, HPRD, design.md, runtime design, tests, rollback, and boundaries exist as GitHub SSOT. |
| `DS15-ACCEPTANCE-READBACK` | Dispatch | After contracts PR merges | Record acceptance, checks, changed files, rollback, and remaining blocked scope. |

## No Evidence, No Done

No Evidence, No Done remains active.

DS-15 is done only as an Option B decision after this PR merges and validation passes. The facts catalog write is not done until the separate `hl-contracts` PR merges with evidence.

## Exclusions

This decision does not authorize:

- more than one fact key
- any fact key other than `service_order.lifecycle.observed_state`
- can / eligible / should / approval / authorization / permission / policy judgment
- state-machine transition authority
- active contract beyond the exact facts catalog row
- active registry expansion beyond the exact facts catalog row
- events registry write
- OpenAPI creation
- reasoncodes registry write
- rules registry write
- HPRD
- design.md
- formal runtime route
- production release
- real provider path
- real payment provider path
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

Rollback order:

1. Revert the `hl-contracts` facts catalog PR if it has merged.
2. Revert the dispatch acceptance readback PR if it has merged.
3. Revert this DS-15 decision PR if the Option B decision itself must be removed.

No runtime, provider, payment, customer asset, service fulfillment, production, secret, deployment, workflow, or real user state exists to unwind.
