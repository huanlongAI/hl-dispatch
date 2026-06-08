# Capability Integration Baseline 2026-06-07

This baseline is a Delivery Recovery Mode v0.1 review artifact. It does not create a new ledger issue, does not authorize new runtime work, and does not replace the canonical implementation contract.

## Scope

Purpose:
- Put current capability packages into the Delivery Recovery process.
- Separate active delivery, risk retirement, waiting queues, candidate queues, and deferred work.
- Keep capability planning subordinate to PR / test / demo / acceptance.

Non-goals:
- Do not create a full task platform.
- Do not write into legacy long ledger comments.
- Do not authorize aftersale, promotion, or performance as active delivery.
- Do not authorize P0.5 runtime.
- Do not treat Tenant entitlement check-only as production runtime.
- Do not treat Booking staging evidence as MVP, production, or merged.

## Main Value Stream

Natural interaction intent
-> `intent_candidate`
-> AI draft
-> human confirmation / signature
-> formal booking / sales / service object
-> payment / asset / fulfillment linkage
-> audit evidence

## Global Red Lines

- Use `手艺人` and `服务人员`; do not write back `美疗师` or `美容师`.
- Do not assume one room, one bed, one person.
- AI can draft, suggest, execute code tasks, audit, compress context, and report gaps.
- AI cannot confirm, sign, reject, approve, create formal business objects, or replace human acceptance.
- GitHub Issues / PRs / comments are the task and decision evidence chain.
- Feishu is projection only.

## Capability Maturity M0-M9

| Level | Name | Meaning | Allowed Action | Forbidden Misread |
| --- | --- | --- | --- | --- |
| M0 | observation_candidate | Observed candidate | Record and classify | Do not dispatch or start engineering |
| M1 | session_candidate_locked | Session candidate locked | Enter review | Not a formal task |
| M2 | draft_candidate_baseline | Draft candidate baseline | Feed HPRD / gap review | Not an active contract |
| M3 | hprd_understanding_confirmed | HPRD understanding confirmed | Engineering understanding / low-risk preflight | Not runtime authorization |
| M4 | contract_draft_pr | Contract Draft PR | Review / fix / promote / close | Checks success is not ready |
| M5 | active_contract_baseline | Contract merged baseline | Controlled engineering breakdown | Not production ready |
| M6 | runtime_candidate | Runtime candidate | Sandbox / staging validation | Not MVP |
| M7 | staging_evidence_accepted | Staging evidence accepted | Merge / closeout / acceptance review | Not PR merged or production |
| M8 | internal_mvp_accepted | Internal MVP accepted | Internal use and feedback | Not production release |
| M9 | production_authorized | Production authorized | Production release | Requires release / security / product evidence |

## Current Capability Table

| Package | Current Lane | Maturity | Owner State | Next Action | Evidence Exit | Not Authorized |
| --- | --- | --- | --- | --- | --- | --- |
| P0.5-A `biz.intent.capture` | waiting_hprd_draft | M0-M1 | needs PM / product framing | Draft HPRD candidate and define confirmation boundary | HPRD draft / gap report | No runtime, no formal object creation |
| P0.5-B `biz.ai.draft.confirmation` | waiting_hprd_draft | M0-M1 | needs PM / product framing | Define AI draft -> human confirmation contract | HPRD draft / decision record | No AI confirmation/signature |
| P0.5-C 横切依赖 / cross-cutting dependencies | waiting_owner_action | M1-M2 | needs Package Owner mapping | Map dependencies to booking / sales / service / payment / asset | dependency map / blocker list | No broad platform build |
| `biz.customer.asset` | P1 formal object chain | M2-M3 | waiting_owner_action | Adjacent boundary and Contract Gap decision | decision record / contract gap closeout | No downstream runtime expansion |
| `biz.sales.order` | P1 formal object chain | M4 draft correction | waiting_owner_action | Fix terminology red line to `手艺人` / `服务人员` | Draft PR update / review evidence | Do not write `美疗师` or `美容师` |
| `biz.service.order` | P1 formal object chain | M2-M4 | waiting_pm_eta | Produce Draft PR, blocker, or ETA revision | Draft PR / blocker / ETA update | No service runtime authorization by default |
| `biz.payment.checkout` | P1 formal object chain | M2-M3 | waiting_pm_eta | PM preflight or blocker, aligned to ServiceOrder dependency | preflight report / blocker | No real charging or production payment |
| `biz.tenant.entitlement` | P2 engineering thin slice | M5 contract baseline / M6 check-only candidate | owner assigned for check-only | DS-2 check-only quota path with mock / seed data | PR + 3 case tests + demo response | No production, no real deduction, no real billing |
| Booking staging pilot | P0 closeout / DS-0 | M7 evidence accepted but open closeout | waiting_owner_action | Close out `hl-platform#106`: merge, split follow-up, or close superseded | PR / integration test / acceptance report | Do not call MVP, production, or merged until evidence exists |
| Supply / Resource | dependency / risk-retirement | M1-M3 | waiting_owner_action | Identify only blockers needed by booking / service / asset | blocker closeout / decision record | No broad supply runtime |
| CustomerProfile | dependency candidate | M1-M2 | waiting_hprd_draft | Clarify profile boundary with customer asset and identity | HPRD draft / decision record | No independent active delivery |
| HK 横切契约 / cross-cutting contracts | platform dependency | M5-M6 | waiting_owner_action | Keep runtime registry / reason code / event taxonomy aligned | gate output / contract drift report | No hidden contract changes |

## Waiting Queues

`waiting_owner_action`:
- Booking closeout / readiness decision.
- `biz.customer.asset` adjacent boundary and Contract Gap decision.
- `biz.sales.order` terminology red line fix.
- P0.5-C dependency mapping.
- Supply / Resource blocker mapping.
- HK cross-cutting contract drift handling.

`waiting_pm_eta`:
- `biz.service.order` Draft PR / blocker / ETA revision.
- `biz.payment.checkout` preflight / blocker.

`waiting_hprd_draft`:
- P0.5-A `biz.intent.capture`.
- P0.5-B `biz.ai.draft.confirmation`.
- CustomerProfile boundary.

## Candidate Queue

`candidate_queue`:

These remain candidate / observation only. They do not enter active delivery in the current recovery window:

- `biz.aftersale.case`
- `biz.promotion.discount`
- `biz.performance.commission`

Deferred:
- `biz.invoice.tax`
- `biz.payment.channel.settlement`

## Forbidden Misreads

- Checks SUCCESS is not ready.
- Draft PR is not active contract.
- HPRD draft is not runtime authorization.
- Staging accepted is not PR merged or production.
- Feishu done is not GitHub done.
- AI draft is not a formal business object.
- Founder dispatch accepted is not engineering start allowed.
- Booking staging pilot is not MVP / production / merged.
- Tenant entitlement check-only is not production runtime.

## Recommended Review Issue

Create a new independent GitHub Issue from:

`docs/delivery-recovery/CAPABILITY_REVIEW_ISSUE_BODY_2026-06-07.md`

Do not paste this baseline into legacy long ledger issues.

Suggested one-line pointer for `#173` only:

`当前能力包整合快照见 <新 Review Issue 链接>。`
