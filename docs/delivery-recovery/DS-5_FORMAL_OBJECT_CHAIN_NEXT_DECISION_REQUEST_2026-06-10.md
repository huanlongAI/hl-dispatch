# DS-5 Formal Object Chain Next Decision Request

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-10

## Scope

DS-5 is a dispatch-only decision request after the DS-4 check-only read path.

It does not add contracts, platform runtime, provider integration, production config, payment, billing, refund, settlement, asset deduction, service fulfillment, workflow changes, deploy changes, release changes, secrets, or real user data access.

The only purpose is to make the next authorized action explicit before any engineering work expands beyond the DS-4 sandbox / embedded evidence resolver.

## Task Snapshot

```yaml
package_id: MP-DELIVERY-RECOVERY-v0.1
slice_id: DS-5
maturity: decision_request_ready
type: decision_request
state: dispatch_docs_only
risk_path: Green for this document; Yellow or Red for any downstream expansion without a new GitHub SSOT
previous_slice: DS-4 Formal Object Chain Read Path
previous_evidence:
  contracts_pr: https://github.com/huanlongAI/hl-contracts/pull/113
  platform_pr: https://github.com/huanlongAI/hl-platform/pull/131
  dispatch_pr: https://github.com/huanlongAI/hl-dispatch/pull/208
current_status: DS-4 check-only read path is merged; all four formal objects remain candidate-only.
decision_needed: Founder / Gate must choose whether the next action is acceptance only, contract activation planning, HPRD / design planning, or a blocked runtime expansion request.
default_recommendation: Accept DS-4 as closed check-only evidence and do not authorize active contract, HPRD, design.md, formal runtime, provider, payment, billing, refund, settlement, asset deduction, service fulfillment, production, deploy, release, secrets, workflow, or real user data work from DS-4 evidence alone.
blocked_by: Missing active contract registry decision, HPRD, design.md, runtime design, provider/billing/refund/settlement authorization, production authorization, and real user data authorization.
unblock_condition: A separate GitHub SSOT decision names exactly one downstream track, owner, boundary, tests, rollback, and non-authorization list.
authorization: decision_request only; no implementation authorization.
close_condition: Founder / Gate records the selected next track in GitHub, or confirms DS-4 acceptance-only closeout.
last_material_change: 2026-06-10 hl-dispatch#208 merge
```

## Decision Request

```yaml
decision_request:
  class: decision_request
  question: Which single next track, if any, is authorized after DS-4 check-only Formal Object Chain evidence?
  requested_owner:
    - Founder
    - Gate
    - Package Owner if explicitly assigned
  default_answer: accept_ds4_only
  required_before_engineering_expansion:
    - GitHub SSOT decision
    - named scope
    - named owner
    - affected repositories
    - tests / evidence lane
    - rollback plan
    - explicit non-authorization list
  not_authorized_by_this_request:
    - active_contract
    - active_contract_registry
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
```

## Options

| Option | Decision | Risk | What it authorizes | What remains blocked |
| --- | --- | --- | --- | --- |
| A | Accept DS-4 only | Green | Close DS-4 as check-only evidence and keep the platform resolver as sandbox / embedded demo evidence. | Any active registry, HPRD, design.md, formal runtime, provider, payment, billing, refund, settlement, asset deduction, service fulfillment, production, deploy, release, secrets, workflow, or real user data expansion. |
| B | Contract activation planning | Yellow | A separate contracts docs-only planning slice for exactly one named object or object-chain segment. | Active registry write, runtime, production, provider, payment, billing, refund, settlement, asset deduction, fulfillment, and real data until a later explicit decision. |
| C | HPRD / design planning | Yellow | A separate HPRD / design.md planning slice for exactly one named capability, still non-runtime. | Runtime implementation and active contracts until the HPRD / design scope is approved and linked to a contract decision. |
| D | Runtime expansion request | Red until prerequisites exist | Nothing from this DS-5 document. | Blocked until active contract registry, HPRD, design.md, provider/billing/refund/settlement decisions where relevant, security review, tests, rollback, and production boundary are all present as GitHub SSOT. |

Recommendation: choose Option A unless Founder / Gate explicitly needs Option B or Option C next. Do not choose Option D from DS-4 evidence alone.

## E Dual Review

### E1 Evidence Audit

| Question | DS-5 answer |
| --- | --- |
| Current GitHub SSOT | DS-4 evidence is merged in `hl-contracts#113`, `hl-platform#131`, and `hl-dispatch#208`. Earlier candidate-only object evidence remains `hl-contracts#96`, `#99`, `#111`, and `#112`. |
| Candidate-only status | SalesOrder, CustomerAsset, ServiceOrder, and PaymentCheckout remain candidate-only / draft candidate evidence. |
| Active / HPRD / runtime authorization | Not present. |
| Check-only / mock / embedded authorization | Present only for DS-4 sandbox / embedded read path evidence. |
| Missing evidence | Active contract registry decision, HPRD, design.md, OpenAPI, facts/events, formal reason code registry, provider, billing, refund, settlement, production, deploy/release, secrets, real user data, asset deduction, and service fulfillment authorization. |

### E2 Impact Audit

| Area | Impact |
| --- | --- |
| contracts | No change in DS-5. Any Option B work must be a separate PR and must not upgrade active registry without Founder / Gate SSOT. |
| platform | No runtime or test code change in DS-5. Any Option D request remains blocked until prerequisites exist. |
| dispatch | This decision request and README pointer only. |
| rollback | Revert this dispatch PR. No provider, payment, production, user data, contract registry, or runtime state exists to unwind. |
| misread risk | Main risk is treating DS-4 evidence as runtime or active-contract authorization. This DS-5 request repeats the non-authorization list and requires one named downstream track before work starts. |

## Contract Gap Judgment

No new `hl-contracts` PR is required for DS-5 because this slice is not a contract baseline, active registry change, or platform read path.

The remaining contract gaps are unchanged from DS-4:

- Active contract registry decision is absent.
- HPRD is absent.
- design.md is absent.
- Formal runtime route is absent.
- Provider, billing, refund, settlement, production, and real user data authorization are absent.

If the next selected track is Option B, the contract work must be a new bounded docs-only PR. If the next selected track is Option C or D, the missing HPRD / design / runtime prerequisites must be resolved first in GitHub.

## Commands Run

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
command: git diff --check
result: pass
output summary: no whitespace errors
```

```text
command: rg -n "task-snapshot:v1|decision_request|No Evidence, No Done|DS-5|accept_ds4_only|not_authorized_by_this_request|active_contract|formal_runtime|real_payment_provider|real_user_data" docs/delivery-recovery/DS-5_FORMAL_OBJECT_CHAIN_NEXT_DECISION_REQUEST_2026-06-10.md docs/delivery-recovery/README.md
result: pass
output summary: required DS-5 decision markers found
```

## Action Projection

| action_id | Owner | Trigger | Evidence exit |
| --- | --- | --- | --- |
| `DS5-DECIDE-NEXT-TRACK` | Founder / Gate | After this dispatch PR merges | GitHub decision selects Option A, B, C, or D with exact scope and owner. |
| `DS5-KEEP-DS4-BOUNDED` | Engineering | Any request tries to use DS-4 evidence as runtime or active-contract authorization | Block the request and link this DS-5 decision request plus DS-4 readback. |
| `DS5-OPTION-B-PREP` | Founder / Gate / Contracts Owner | Only if Option B is selected | New bounded contracts docs-only PR; no active registry write unless explicitly authorized. |
| `DS5-OPTION-C-PREP` | Founder / Gate / Product / Engineering | Only if Option C is selected | New HPRD / design planning PR with no runtime implementation. |

## No Evidence, No Done

No Evidence, No Done remains active.

DS-5 is done only when this decision request exists as GitHub / repository evidence and the PR validation passes. DS-5 does not make any downstream option done.

## Exclusions

This decision request does not authorize:

- active contract or active registry
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

Rollback is a single revert of this dispatch PR.

No provider, payment, customer asset, service fulfillment, production, secret, deployment, workflow, active registry, or real user state exists to unwind.
