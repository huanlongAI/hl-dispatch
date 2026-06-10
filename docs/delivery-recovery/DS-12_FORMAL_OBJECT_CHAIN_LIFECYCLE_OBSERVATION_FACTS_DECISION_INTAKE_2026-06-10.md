# DS-12 Formal Object Chain Lifecycle Observation Facts Decision Intake

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-10

## Scope

DS-12A is a dispatch-only decision intake and acceptance readback after DS-11A.

The DS-11A decision gate was checked for a separate Founder / Gate GitHub SSOT selecting one next option:

- Option A: keep DS-11A as proposal evidence only.
- Option B: authorize an exact `facts/facts-catalog.md` write subset.
- Option C: authorize another DS-10A family docs-only proposal.
- Option D: request runtime expansion.

No separate Founder / Gate GitHub SSOT selecting Option A, B, C, or D was found. Therefore DS-12A does not authorize `facts/facts-catalog.md` write, facts registry write, formal fact ID allocation, formal fact partition creation, active contract, active registry write, HPRD, design.md, formal runtime, provider, payment, billing, refund, settlement, CustomerAsset deduction, service fulfillment, production, workflow, deploy / release, secrets, or real user data work.

The only accepted action is to keep DS-11A closed as docs-only ServiceOrder lifecycle observation facts proposal evidence until Founder / Gate records a separate exact next decision in GitHub.

## Task Snapshot

```yaml
package_id: MP-DELIVERY-RECOVERY-v0.1
slice_id: DS-12
track: DS-12A
maturity: decision_intake_completed
type: acceptance_report
state: dispatch_docs_only
risk_path: Green
current_date: 2026-06-10
previous_slices:
  ds11a_decision: https://github.com/huanlongAI/hl-dispatch/pull/222
  ds11a_contracts: https://github.com/huanlongAI/hl-contracts/pull/118
  ds11a_readback: https://github.com/huanlongAI/hl-dispatch/pull/223
upstream_facts_proposal:
  ds10a_contracts: https://github.com/huanlongAI/hl-contracts/pull/117
decision_gate_result: no_separate_founder_gate_ssot_found
selected_next_track: ds12a_decision_intake_acceptance_readback
current_status: DS-11A remains docs-only proposal evidence; Formal Object Chain objects remain candidate-only.
next_action: Founder / Gate may record exactly one DS-11A next option in GitHub, including exact scope, affected files, tests, rollback, and non-authorization boundaries.
blocked_by: Missing exact facts catalog write decision, facts registry write decision, formal fact ID decision, formal fact partition decision, active registry decision, HPRD, design.md, formal runtime design, provider/payment/billing/refund/settlement boundaries, production authorization, deploy/release authorization, workflow authorization, secrets authorization, real user data authorization, CustomerAsset deduction authorization, and service fulfillment authorization.
unblock_condition: A separate Founder / Gate GitHub SSOT chooses Option A, B, C, or D with exact owner, scope, affected repositories, files, tests, rollback, and exclusions.
authorization: acceptance readback only; no implementation authorization.
close_condition: This DS-12 dispatch PR merges with verification evidence and no open PR remains.
last_material_change: 2026-06-10 hl-dispatch#223 merge
```

## Decision Gate Intake

```yaml
decision_request:
  class: acceptance_report
  source_request: DS-11A ServiceOrder Lifecycle Observation Facts Proposal Acceptance
  source_pr: https://github.com/huanlongAI/hl-dispatch/pull/223
  gate_question: Which single next track, if any, is authorized after DS-11A docs-only proposal evidence?
  searched_for:
    - DS-12 ServiceOrder lifecycle observation facts
    - authorize_exact_facts_catalog_write_subset
    - facts/facts-catalog.md write subset ServiceOrder
    - DS-11A NEXT DECISION
    - Option B facts catalog write
    - service_order.lifecycle.observed_state
  result: no separate Founder / Gate GitHub SSOT found
  selected_track: DS-12A decision intake / acceptance readback
  default_answer: keep_ds11a_as_proposal_evidence_until_explicit_decision
  option_status:
    option_a_keep_ds11a_as_proposal_evidence_only: no_explicit_new_founder_gate_selection_found
    option_b_authorize_exact_facts_catalog_write_subset: not_authorized
    option_c_authorize_another_ds10a_family_docs_only_proposal: not_authorized
    option_d_runtime_expansion_request: blocked_missing_prerequisites
  not_authorized_by_this_intake:
    - facts_catalog_write
    - facts_registry_write
    - formal_fact_id_allocation
    - formal_fact_partition_creation
    - active_contract
    - active_registry_write
    - events_registry_write
    - openapi_creation
    - reasoncodes_registry_write
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
    - business_object_creation
    - production
    - deploy_release
    - workflow_change
    - secrets
    - real_user_data
```

## E Dual Review

### E1 Evidence Audit

| Question | DS-12 answer |
| --- | --- |
| Current GitHub SSOT | Present only for DS-11A docs-only lifecycle observation facts proposal: `hl-dispatch#222`, `hl-contracts#118`, and `hl-dispatch#223` are merged. |
| Contract SSOT | `hl-contracts` remains the contract SSOT for facts, decisions, reason codes, APIs, events, and governance registries. DS-12A is dispatch readback only and does not create contract authority. |
| Current open PR state | `hl-dispatch`, `hl-contracts`, and `hl-platform` open PR lists were empty during DS-12 intake. |
| New DS-11A next-option decision | No separate Founder / Gate GitHub SSOT selecting Option A, B, C, or D was found. |
| Proposal / candidate-only status | DS-11A remains proposal evidence only. SalesOrder, CustomerAsset, ServiceOrder, and PaymentCheckout remain candidate-only / draft candidate evidence from `hl-contracts#99`, `hl-contracts#96`, `hl-contracts#111`, and `hl-contracts#112`. |
| `facts/facts-catalog.md` write authorization | Not present. DS-11A explicitly says facts catalog write is not authorized. |
| Active / HPRD / design / runtime authorization | Not present. DS-11A and DS-12A do not grant active registry, HPRD, design.md, formal runtime, provider, payment, billing, refund, settlement, CustomerAsset deduction, service fulfillment, production, workflow, secrets, or real user data authorization. |
| Missing evidence | Exact facts catalog write decision, facts registry write, formal fact IDs, formal fact partitions, active registry decision, events registry write, OpenAPI creation, reasoncodes registry write, HPRD, design.md, formal runtime design, tests, rollback, provider/payment/billing/refund/settlement boundaries, production guard, workflow authorization, deploy/release authorization, secrets authorization, real user data authorization, CustomerAsset deduction authorization, and service fulfillment authorization remain absent. |

### E2 Impact Audit

| Area | Impact |
| --- | --- |
| contracts | No contract file change in DS-12A. The `hl-contracts` DS-12 worktree remains clean and was not used for writes because no exact `facts/facts-catalog.md` subset authorization was found. |
| platform | No platform change. No backend endpoint, CLI, persistence path, provider path, production config, test fixture, or real data path is authorized. |
| dispatch | This decision intake / acceptance readback and README pointer only. |
| rollback | Revert this dispatch PR. No facts catalog, contracts registry, runtime, provider, payment, asset, fulfillment, production, secret, deployment, workflow, or real user state exists to unwind. |
| misread risk | Main risk is treating DS-11A proposal rows as `facts/facts-catalog.md` entries or runtime authorization. DS-12A repeats that `service_order.lifecycle.observed_state` and adjacent proposed rows remain proposal-only until a separate exact GitHub SSOT authorizes otherwise. |

## Acceptance Report

```yaml
acceptance_report:
  slice_id: DS-12
  track: DS-12A
  status: ready_for_acceptance
  evidence_source: GitHub PRs, GitHub search, and repository files
  no_evidence_no_done: true
  accepted_scope:
    - decision_intake
    - acceptance_readback
    - ds11a_docs_only_proposal_evidence_remains_current_state
    - no_facts_catalog_write_without_exact_github_ssot
  blocked_scope:
    - option_b_exact_facts_catalog_write_subset
    - option_c_another_ds10a_family_docs_only_proposal
    - option_d_runtime_expansion
    - active_contract_or_runtime_work
  not_authorized:
    - facts_catalog_write
    - facts_registry_write
    - formal_fact_id_allocation
    - formal_fact_partition_creation
    - active_contract
    - active_registry_write
    - events_registry_write
    - openapi_creation
    - reasoncodes_registry_write
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
    - business_object_creation
    - production
    - deploy_release
    - workflow_change
    - secrets
    - real_user_data
```

## Commands Run

### GitHub state and decision gate

```text
command: gh pr list -R huanlongAI/hl-dispatch --state open --json number,title,url,isDraft,headRefName
result: pass
output summary: []
```

```text
command: gh pr list -R huanlongAI/hl-contracts --state open --json number,title,url,isDraft,headRefName
result: pass
output summary: []
```

```text
command: gh pr list -R huanlongAI/hl-platform --state open --json number,title,url,isDraft,headRefName
result: pass
output summary: []
```

```text
command: gh pr view 223 -R huanlongAI/hl-dispatch --json title,state,mergedAt,mergeCommit,body,comments,reviews,url
result: pass
output summary: merged; merge commit 10e34e9b29a655ac84d25e0f6413d5296ddb478d; no facts catalog write authorization.
```

```text
command: gh pr view 222 -R huanlongAI/hl-dispatch --json title,state,mergedAt,mergeCommit,body,comments,reviews,url
result: pass
output summary: merged; merge commit a2fb52ffe26aa4cf8efb05b3500d203e2cceb634; DS-11A decision authorized docs-only proposal only.
```

```text
command: gh pr view 118 -R huanlongAI/hl-contracts --json title,state,mergedAt,mergeCommit,body,comments,reviews,url
result: pass
output summary: merged; merge commit 0be7beeaf0b6b1b89f387f8dd33532772afa354d; DS-11A proposal did not write facts/facts-catalog.md.
```

```text
command: gh pr view 117 -R huanlongAI/hl-contracts --json title,state,mergedAt,mergeCommit,body,comments,reviews,url
result: pass
output summary: merged; merge commit 1e4f5a1a2934cabb65240485d1d5646e03f5d16c; DS-10A facts proposal evidence only.
```

```text
command: gh search issues "DS-12 ServiceOrder lifecycle observation facts" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state open --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

```text
command: gh search issues "DS-12 ServiceOrder lifecycle observation facts" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state closed --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

```text
command: gh search issues "authorize_exact_facts_catalog_write_subset" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state open --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

```text
command: gh search issues "authorize_exact_facts_catalog_write_subset" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state closed --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

```text
command: gh search issues "facts/facts-catalog.md write subset ServiceOrder" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state open --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

```text
command: gh search issues "facts/facts-catalog.md write subset ServiceOrder" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state closed --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

```text
command: gh search issues "Option B facts catalog write" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state open --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

```text
command: gh search issues "Option B facts catalog write" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state closed --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

```text
command: gh search issues "service_order.lifecycle.observed_state" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state open --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

```text
command: gh search issues "service_order.lifecycle.observed_state" --repo huanlongAI/hl-dispatch --repo huanlongAI/hl-contracts --repo huanlongAI/hl-platform --state closed --include-prs --json repository,number,title,state,url,updatedAt --limit 50
result: pass
output summary: []
```

### Local repository evidence

```text
command: rg -n "DS-11A|DS-12|Option A|Option B|Option C|Option D|authorize_exact_facts_catalog_write_subset|facts/facts-catalog.md|facts catalog|lifecycle observation" docs deliverables README.md .github -S
result: pass
output summary: DS-11A readback says facts catalog write is not present and next decision is required; no DS-12 authorization record existed before this PR.
```

```text
command: rg -n "DS-11A|DS-12|authorize_exact_facts_catalog_write_subset|facts/facts-catalog.md|facts catalog|lifecycle observation|service_order.lifecycle.observed_state" prd facts INDEX.md TRACEABILITY.yaml CHANGELOG.md tests -S
result: pass
output summary: hl-contracts main contains DS-11A proposal-only evidence and confirms service_order.lifecycle.observed_state is absent from facts/facts-catalog.md.
```

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
command: rg -n "task-snapshot:v1|DS-12|DS-12A|decision_request|acceptance_report|No Evidence, No Done|Option A|Option B|Option C|Option D|authorize_exact_facts_catalog_write_subset|facts_catalog_write|facts/facts-catalog.md|service_order.lifecycle.observed_state|active_registry_write|formal_runtime|real_payment_provider|real_user_data|DS12-OPTION-B-REQUIRES-EXACT-SSOT" docs/delivery-recovery/DS-12_FORMAL_OBJECT_CHAIN_LIFECYCLE_OBSERVATION_FACTS_DECISION_INTAKE_2026-06-10.md docs/delivery-recovery/README.md
result: pass
output summary: required DS-12 markers found
```

## Action Projection

| action_id | Owner | Trigger | Evidence exit |
| --- | --- | --- | --- |
| `DS12-ACCEPT-DECISION-INTAKE` | Founder / Package Owner | After this dispatch PR merges | Accept DS-12A as the current decision intake / acceptance readback. |
| `DS12-KEEP-DS11A-PROPOSAL-ONLY` | Engineering / Contracts | Any request uses DS-11A as facts catalog write or runtime authorization | Block and link DS-11A and this DS-12 readback. |
| `DS12-OPTION-B-REQUIRES-EXACT-SSOT` | Founder / Gate / Contracts Owner | Before any `facts/facts-catalog.md` write | Record a separate GitHub SSOT with exact approved subset, affected files, tests, rollback, and exclusions. |
| `DS12-OPTION-C-REQUIRES-SSOT` | Founder / Gate / Contracts Owner | Before another DS-10A family proposal | Record a separate GitHub SSOT selecting the exact family and docs-only scope. |
| `DS12-OPTION-D-BLOCKED` | Founder / Gate / Engineering | Any runtime expansion request | Block until active registry, HPRD, design.md, runtime design, provider/payment/billing/refund/settlement boundaries if relevant, tests, rollback, and production boundary exist as GitHub SSOT. |

## No Evidence, No Done

No Evidence, No Done remains active.

DS-12A is done only for decision intake / acceptance readback after this PR merges and validation passes. DS-12A does not make Option A, Option B, Option C, or Option D done as a Founder / Gate decision.

No Evidence, No Done remains active for every expansion beyond DS-11A proposal evidence.

## Exclusions

This decision intake does not authorize:

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

Rollback is a single revert of this dispatch PR.

No facts catalog, facts registry, contract registry, provider, payment, customer asset, service fulfillment, production, secret, deployment, workflow, formal runtime, or real user state exists to unwind.

## Next Stage Recommendation

Keep DS-11A as proposal evidence unless Founder / Gate explicitly authorizes an exact `facts/facts-catalog.md` write subset or another exact DS-11A next option in GitHub.

If the next decision is Option B, it must name the exact approved subset, defaulting to at most one descriptive field such as `service_order.lifecycle.observed_state`, and must include affected files, deterministic tests, rollback, and exclusions. It must not authorize runtime, provider/payment/billing/refund/settlement, CustomerAsset deduction, service fulfillment, production, workflow, secrets, or real user data by implication.
