# PM Capability Lane Taskbook: biz.service.order v1.0

Status: DISPATCH_READY_FOR_PM_READINESS
Date: 2026-06-15
Owner: Zou Cong / `zoucong121`
Capability: `biz.service.order`
Lane: PM-led capability package lane
Parent HK issue: https://github.com/huanlongAI/hl-dispatch/issues/253
Source PM issue: https://github.com/huanlongAI/hl-dispatch/issues/192
Founder dispatch approval: 2026-06-15 Codex thread option `A 启动 ServiceOrder`

## 1. Purpose

This taskbook moves `biz.service.order` from candidate-only PM draft evidence into the PM-led capability package workflow.

It is meant to create a clear handoff from PM business semantics to engineer HPRD, then to bounded implementation after PM HPRD pass. It does not start production runtime work, does not register active contracts, and does not expand the current HK mainline engineering PR.

## 2. Current GitHub Facts

```yaml
capability: biz.service.order
pm_owner: zoucong121
source_issue: https://github.com/huanlongAI/hl-dispatch/issues/192
candidate_cap_spec_pr: https://github.com/huanlongAI/hl-contracts/pull/111
candidate_pr_state: MERGED
candidate_merge_commit: f5a12a3f242b011eaa9d9e626969a4016d139c5a
current_maturity: merged_draft_candidate
active_contract_authorized: false
runtime_authorized: false
engineering_start_authorized_by_candidate_merge: false
```

Current candidate evidence may be used as input. It is not an active contract, not a frozen implementation baseline, and not production authorization.

## 3. Workflow

```text
Founder / AI capability taskbook sign-off
-> Zou Cong completes Cap-Spec / requirements design readiness pack
-> Founder / Gate names engineer for HPRD / technical implementation plan
-> engineer submits HPRD / technical implementation plan
-> Zou Cong reviews HPRD against the Cap-Spec
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

Zou Cong should produce a Founder-readable PM readiness pack based on the merged candidate baseline:

- confirm the current `biz.service.order` business boundary in plain language;
- list the exact candidate files from `hl-contracts#111` that should be treated as PM source input;
- identify what is ready for engineer HPRD;
- identify unresolved Contract Gaps, especially formal service order creation, signed service order draft, service source types, split / merge / partial fulfillment, cancellation, backfill, reminders, customer asset lock / deduction, and booking fulfillment owner boundaries;
- define the first bounded implementation slice that should be safe after PM HPRD pass;
- define PM acceptance checks for that first slice.

## 5. PM Scope Out

Zou Cong must not:

- authorize active contract registration;
- authorize runtime, production, deploy, release, secrets, or real user data;
- authorize provider/payment/billing/refund/settlement work;
- ask engineers to modify `hl-contracts` without a separate Founder / Gate decision;
- turn Feishu, CI green, PM Draft, candidate merge, or semantic support into engineering authorization;
- absorb SalesOrder, CustomerAsset, BookingFulfillment, PaymentCheckout, CustomerProfile, aftersale, invoice, tax, promotion, or commission scope into ServiceOrder.

## 6. Required PM Output

Zou Cong replies in GitHub with:

```yaml
pm_capability_readiness_pack:
  owner: zoucong121
  capability: biz.service.order
  source_candidate_pr: https://github.com/huanlongAI/hl-contracts/pull/111
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
- Zou Cong submits `ready_for_engineer_hprd`;
- Founder / Gate names the engineer and first bounded implementation slice.

The engineer HPRD must explain:

- what service order means in this capability;
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

Founder has confirmed this taskbook is dispatch-ready for PM readiness work only.

The Feishu message must include background, GitHub entrypoint, one next action, expected GitHub reply location, and authorization boundary. GitHub remains the only source of truth.
