# DS-7 Formal Object Chain Option B Decision

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-10

## Scope

This file records the Founder / Gate GitHub SSOT decision after DS-5 and DS-6.

Decision: choose DS-5 Option B, limited to DS-7 Formal Object Chain Activation Readiness Planning.

The authorization is intentionally narrow:

- allow `hl-contracts` docs-only / gap closeout / trace / index / changelog / deterministic tests
- center the first readiness pass on ServiceOrder-linked object-chain readiness
- keep every Formal Object Chain object candidate-only
- do not write the active contract registry
- do not authorize HPRD, design.md, formal runtime, provider, payment, billing, refund, settlement, asset deduction, service fulfillment, production, deploy/release, workflow, secrets, or real user data

## Task Snapshot

```yaml
package_id: MP-DELIVERY-RECOVERY-v0.1
slice_id: DS-7
decision_id: DS7-FORMAL-OBJECT-CHAIN-OPTION-B
maturity: github_ssot_decision_recorded
type: decision_request
state: option_b_authorized_for_contracts_docs_only_planning
risk_path: Yellow
source_prompt: Founder approved Option B recommendation on 2026-06-10 in the active Cowork thread.
selected_option: Option B
selected_track: Contract activation readiness planning docs-only
target_repo: hl-contracts
allowed_paths:
  - prd/biz/
  - INDEX.md
  - TRACEABILITY.yaml
  - CONTEXT.md
  - CHANGELOG.md
  - tests/
required_focus: ServiceOrder-centered Formal Object Chain readiness planning
blocked_scope:
  - active_contract
  - active_contract_registry_write
  - hprd
  - design_md
  - formal_runtime
  - provider_integration
  - real_payment_provider
  - real_billing
  - real_refund
  - real_settlement
  - customer_asset_deduction
  - service_fulfillment
  - business_object_creation
  - production
  - deploy_release
  - secrets
  - workflow_change
  - real_user_data
close_condition: hl-contracts DS-7 docs-only planning PR merges and hl-dispatch DS-7 acceptance readback records evidence.
```

## Decision Record

```yaml
decision_request:
  class: decision_request
  source_request: DS-5 Formal Object Chain Next Decision Request
  source_request_pr: https://github.com/huanlongAI/hl-dispatch/pull/209
  intake_readback_pr: https://github.com/huanlongAI/hl-dispatch/pull/210
  selected_option: option_b
  selected_option_label: Contract activation planning docs-only
  authorized_next_slice: DS-7 Formal Object Chain Activation Readiness Planning
  founder_gate_decision: approved
  github_ssot_artifact: this file after merge
  owner: NODE-E
  target_repository: huanlongAI/hl-contracts
  allowed_change_class:
    - docs_only
    - gap_closeout
    - traceability
    - deterministic_tests
  required_non_authorization:
    active_contract: false
    active_contract_registry_write: false
    hprd: false
    design_md: false
    formal_runtime: false
    provider_integration: false
    real_payment_provider: false
    real_billing: false
    real_refund: false
    real_settlement: false
    customer_asset_deduction: false
    service_fulfillment: false
    business_object_creation: false
    production: false
    deploy_release: false
    secrets: false
    workflow_change: false
    real_user_data: false
```

## E Dual Review

### E1 Evidence Audit

| Question | Decision answer |
| --- | --- |
| Current GitHub SSOT | DS-4 evidence is merged in `hl-contracts#113`, `hl-platform#131`, `hl-dispatch#208`; DS-5 request is merged in `hl-dispatch#209`; DS-6 intake is merged in `hl-dispatch#210`; this file records the Option B decision after merge. |
| Candidate-only status | SalesOrder, CustomerAsset, ServiceOrder, and PaymentCheckout remain candidate-only / draft candidate evidence. |
| Active / HPRD / runtime authorization | Not present and not granted here. |
| Docs-only / check-only authorization | Granted only for `hl-contracts` DS-7 activation readiness planning and deterministic tests. |
| Missing evidence | Active registry decision, HPRD, design.md, formal runtime design, provider/payment/billing/refund/settlement boundaries, production authorization, deploy/release authorization, secrets authorization, real user data path, asset deduction authorization, and service fulfillment authorization remain absent. |

### E2 Impact Audit

| Area | Impact |
| --- | --- |
| contracts | Allows one docs-only DS-7 planning PR with trace/index/changelog/tests. It must not write active registry. |
| platform | No platform change authorized. Platform may only be referenced as prior DS-4 evidence. |
| dispatch | This decision record and later DS-7 readback only. |
| rollback | Revert this decision PR and any dependent DS-7 contracts/readback PRs. No runtime/provider/customer/payment state exists to unwind. |
| misread risk | Main risk is reading "activation readiness" as active activation. The decision title and blocked scope require `active_contract_registry_write: false`. |

## Action Projection

| action_id | Owner | Trigger | Evidence exit |
| --- | --- | --- | --- |
| `DS7-CONTRACTS-READINESS-PLANNING` | NODE-E / Contracts Owner | After this decision PR merges | Open `hl-contracts` docs-only readiness planning PR. |
| `DS7-BLOCK-ACTIVE-REGISTRY` | Engineering / Gate | Any DS-7 change attempts active registry write | Block and link this decision record. |
| `DS7-BLOCK-RUNTIME` | Engineering / Gate | Any DS-7 change attempts platform runtime/provider/payment path | Block and require separate Founder / Gate GitHub SSOT. |
| `DS7-READBACK` | NODE-E / Dispatch | After contracts PR merges | Add dispatch acceptance readback with commands, tests, and non-authorization boundaries. |

## No Evidence, No Done

No Evidence, No Done remains active.

DS-7 is not done by this decision record alone. DS-7 requires the contracts docs-only planning PR, verification evidence, and dispatch acceptance readback.

## Exclusions

This decision does not authorize:

- active contract or active registry write
- HPRD
- design.md
- formal runtime route
- production release
- real payment provider path
- real billing
- real refund
- real settlement
- customer asset deduction
- service fulfillment
- business object creation
- real user data
- Feishu, Bitable, Project, dashboard, or chat summary as fact source
- workflow change
- deploy or release change
- new total ledger issue

## Rollback

Rollback is a single revert of this decision PR unless dependent DS-7 PRs have already merged.

If dependent PRs have merged, revert in reverse order:

1. DS-7 dispatch acceptance readback.
2. DS-7 `hl-contracts` readiness planning PR.
3. This decision PR.

No provider, payment, customer asset, service fulfillment, production, secret, deployment, workflow, active registry, formal runtime, or real user state exists to unwind.
