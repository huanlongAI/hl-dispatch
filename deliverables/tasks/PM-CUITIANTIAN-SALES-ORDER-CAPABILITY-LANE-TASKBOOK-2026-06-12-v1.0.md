# PM Capability Lane Taskbook: biz.sales.order v1.0

Status: DRAFT_FOR_FOUNDER_SIGNOFF
Date: 2026-06-12
Owner: Cui Tiantian / `cuitiantian0704`
Capability: `biz.sales.order`
Lane: PM-led capability package lane
Parent recovery issue: https://github.com/huanlongAI/hl-dispatch/issues/194

## 1. Purpose

This taskbook moves `biz.sales.order` from candidate-only PM draft evidence into the new PM-led capability package workflow.

It is meant to create a clear handoff from PM business semantics to engineer HPRD, then to bounded implementation after PM HPRD pass. It does not start production runtime work and does not register active contracts.

## 2. Current GitHub Facts

```yaml
capability: biz.sales.order
pm_owner: cuitiantian0704
source_issue: https://github.com/huanlongAI/hl-dispatch/issues/184
candidate_cap_spec_pr: https://github.com/huanlongAI/hl-contracts/pull/99
candidate_pr_state: MERGED
candidate_merge_commit: 3c6ca26296a92b4777e977655595ff66b6baed43
current_maturity: merged_draft_candidate
active_contract_authorized: false
runtime_authorized: false
engineering_start_authorized_by_candidate_merge: false
```

Current candidate evidence may be used as input. It is not an active contract, not a frozen implementation baseline, and not production authorization.

## 3. Workflow

```text
Founder / AI capability taskbook sign-off
-> Cui Tiantian completes Cap-Spec / requirements design readiness pack
-> Founder / Gate names engineer for HPRD / technical implementation plan
-> engineer submits HPRD / technical implementation plan
-> Cui Tiantian reviews HPRD against the Cap-Spec
-> PM HPRD pass starts bounded engineering implementation inside this taskbook
-> PR / demo / test evidence
-> PM acceptance
-> Gate A / Gate B
-> Human Cross Audit
-> Founder Acceptance
-> merge / conditional pass / follow-up / reject
```

PM HPRD pass means the engineer understood the business semantics and may start bounded implementation inside this signed taskbook. It does not authorize production, active contract registration, real user data, provider/payment/billing/refund/settlement, secrets, deploy, or release.

## 4. PM Scope In

Cui Tiantian should produce a Founder-readable PM readiness pack based on the merged candidate baseline:

- confirm the current `biz.sales.order` business boundary in plain language;
- list the exact candidate files from `hl-contracts#99` that should be treated as PM source input;
- identify what is ready for engineer HPRD;
- identify unresolved Contract Gaps, especially `completed` semantics, `manual_direct`, line item boundary, adjacent capability linkage, customer-side signing evidence, aftersale, performance attribution, solution sales, and backfill;
- define the first bounded implementation slice that should be safe after PM HPRD pass;
- define PM acceptance checks for that first slice.

## 5. PM Scope Out

Cui Tiantian must not:

- authorize active contract registration;
- authorize runtime, production, deploy, release, secrets, or real user data;
- authorize provider/payment/billing/refund/settlement work;
- ask engineers to modify `hl-contracts` without a separate Founder / Gate decision;
- turn Feishu, CI green, PM Draft, or candidate merge into engineering authorization;
- absorb CustomerAsset, PaymentCheckout, ServiceOrder, CustomerProfile, aftersale, invoice, tax, promotion, or commission scope into SalesOrder.

## 6. Required PM Output

Cui Tiantian replies in GitHub with:

```yaml
pm_capability_readiness_pack:
  owner: cuitiantian0704
  capability: biz.sales.order
  source_candidate_pr: https://github.com/huanlongAI/hl-contracts/pull/99
  conclusion: ready_for_engineer_hprd | needs_founder_gate_decision | blocked
  business_boundary_summary: "<3-8 plain-language sentences>"
  source_files:
    - "<repo-relative path from hl-contracts>"
  first_bounded_engineering_slice:
    name: "<one small implementation slice>"
    user_value: "<what changes for operator/customer/business user>"
    not_in_scope:
      - "<explicit exclusions>"
  contract_gaps:
    - id: "<gap id>"
      question: "<one bounded question>"
      required_decision_owner: Founder | Gate | PM | Engineering
  pm_acceptance_checks:
    - check: "<what PM will verify>"
      pass_condition: "<visible pass condition>"
      fail_condition: "<visible fail condition>"
  hprd_review_standard:
    - "<what the engineer HPRD must explain correctly>"
  not_authorized:
    - production_runtime
    - active_contract
    - active_registry
    - real_user_data
    - provider_payment_billing_refund_settlement
    - secrets
    - deploy_or_release
```

If the PM cannot complete the readiness pack, the output is a `gap_report` with the smallest missing Founder / Gate decision.

## 7. Engineer HPRD Trigger

Engineering HPRD starts only after:

- this taskbook is Founder-signed and published as GitHub SSOT;
- Cui Tiantian submits `ready_for_engineer_hprd`;
- Founder / Gate names the engineer and first bounded implementation slice.

The engineer HPRD must explain:

- what sales order means in this capability;
- which candidate contract files were read;
- what the first bounded slice implements;
- what remains out of scope;
- how to test the slice;
- what would require a `gap_report` instead of implementation.

## 8. Human-Readable Gate

Every PM reply, HPRD, PR, `gap_report`, Gate report, and acceptance pack must be readable by Founder, PM, and engineer:

- one-sentence conclusion;
- evidence links;
- current state;
- one next action and owner;
- unresolved uncertainty;
- plain-language explanation for necessary terms.

Black-box phrases such as "继续推进整体治理", "需要进一步确认", "当前上下文显示", or "runtime 那个" are not acceptable output.

## 9. Feishu Projection

Feishu may be sent only after Founder confirms this taskbook is dispatch-ready in GitHub.

The Feishu message must include background, GitHub entrypoint, one next action, expected GitHub reply location, and authorization boundary. GitHub remains the only source of truth.
