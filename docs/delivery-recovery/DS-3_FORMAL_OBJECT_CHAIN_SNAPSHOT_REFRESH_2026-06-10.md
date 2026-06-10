# DS-3 Formal Object Chain Snapshot Refresh

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-10

## Scope

DS-3 records the current GitHub evidence for the formal object chain:

- `biz.sales.order`
- `biz.customer.asset`
- `biz.service.order`
- `biz.payment.checkout`
- DS-2 Tenant Entitlement check-only pilot context

This refresh supersedes the 2026-06-08 readback for current status only. The older snapshot remains historical evidence. This file is a docs-only evidence resolver artifact, not a runtime authorization, active contract authorization, production authorization, payment provider authorization, Feishu projection, or task ledger.

## Task Snapshot

```yaml
package_id: MP-DELIVERY-RECOVERY-v0.1
slice_id: DS-3
maturity: current_readback
type: evidence
state: refreshed_after_contracts_merge
risk_path: Yellow
DRI: Founder temporary DS-3 reviewer until Package Owner assignment is explicit
current_status: SalesOrder, CustomerAsset, ServiceOrder, and PaymentCheckout are merged as hl-contracts candidate-only draft materials; DS-2 Tenant Entitlement is completed as a check-only pilot.
next_action: Treat the formal object chain as candidate-only evidence in main; open a separate Founder / Gate decision only if any capability is proposed for active registry, HPRD, design.md, runtime, provider, billing, refund, settlement, or production.
blocked_by: none for snapshot publication; all capability-level runtime and active-contract gates remain blocked.
unblock_condition: Separate GitHub SSOT decision for each next phase, with explicit scope and non-production / production boundary.
authorization: docs-only snapshot refresh; no HPRD, design, runtime, merge-to-active, staging, MVP, production, provider, secret, real user data, billing, refund, settlement, or real payment path authorization.
close_condition: Founder or Package Owner accepts this refresh as current readback or requests a concrete correction.
last_material_change: 2026-06-10 GitHub readback after hl-contracts#112 merge
```

## Evidence Rules

The following non-equivalences are active for this snapshot:

- checks SUCCESS does not mean ready.
- Draft PR does not mean active contract.
- Merged candidate-only docs do not mean active contract.
- PM preflight does not mean HPRD, design.md, runtime, or engineering start authorization.
- Feishu projection does not change GitHub state.
- AI draft does not create a formal business object.
- PaymentCheckout candidate docs do not authorize real payment provider, real billing, real refund, real settlement, or production.
- DS-2 check-only pilot does not authorize full Tenant Entitlement runtime, real billing, reserve / confirm / refund, or production.

## GitHub Readback

| Repository | Open PR status on 2026-06-10 | Evidence |
| --- | --- | --- |
| `huanlongAI/hl-dispatch` | `[]` | `gh pr list --state open` returned no open PRs. |
| `huanlongAI/hl-contracts` | `[]` | `gh pr list --state open` returned no open PRs after #112 merge. |
| `huanlongAI/hl-platform` | `[]` | `gh pr list --state open` returned no open PRs. |

## Capability Snapshot

| Capability | GitHub evidence | Current maturity | Current state | DRI | Next action | Not authorized |
| --- | --- | --- | --- | --- | --- | --- |
| `biz.sales.order` | [hl-dispatch#184](https://github.com/huanlongAI/hl-dispatch/issues/184), [hl-contracts#99](https://github.com/huanlongAI/hl-contracts/pull/99) | M5 `merged_draft_candidate` | SalesOrder candidate-only Cap-Spec merged into `hl-contracts` on 2026-06-08. Merge commit `3c6ca26296a92b4777e977655595ff66b6baed43`. It remains draft_candidate material, not active registry or runtime. | `cuitiantian0704` / Gate reviewer | If next phase is desired, create a separate GitHub SSOT decision for active registry, HPRD, design.md, runtime, or keep as candidate-only evidence. | Active contract, HPRD, design.md, runtime, engineering start, production. |
| `biz.customer.asset` | [hl-dispatch#183](https://github.com/huanlongAI/hl-dispatch/issues/183), [hl-contracts#96](https://github.com/huanlongAI/hl-contracts/pull/96) | M5 `merged_draft_candidate` | CustomerAsset standard Cap-Spec candidate merged into `hl-contracts` on 2026-06-08. Merge commit `9b81dc92562cbf93661e241bd450257618001c1d`. It remains draft_candidate material, not active registry or runtime. | `zhuyang1204` / Gate reviewer | If next phase is desired, resolve active registry / cross-capability gaps in a separate GitHub SSOT decision. | Active contract, HPRD, design.md, runtime, engineering start, production. |
| `biz.service.order` | [hl-dispatch#192](https://github.com/huanlongAI/hl-dispatch/issues/192), [hl-contracts#111](https://github.com/huanlongAI/hl-contracts/pull/111) | M5 `merged_draft_candidate` | ServiceOrder candidate-only Cap-Spec merged into `hl-contracts` on 2026-06-09. Merge commit `f5a12a3f242b011eaa9d9e626969a4016d139c5a`. It remains draft_candidate material, not active registry or runtime. | `zoucong121` / Gate reviewer | If next phase is desired, create a separate GitHub SSOT decision for active registry, HPRD, design.md, runtime, or keep as candidate-only evidence. | Active contract, HPRD, design.md, runtime, engineering start, production. |
| `biz.payment.checkout` | [hl-dispatch#198](https://github.com/huanlongAI/hl-dispatch/issues/198), submitted PM draft [comment](https://github.com/huanlongAI/hl-dispatch/issues/198#issuecomment-4665613430), [hl-contracts#112](https://github.com/huanlongAI/hl-contracts/pull/112) | M5 `merged_draft_candidate` | PaymentCheckout PM preflight was submitted in #198 on 2026-06-10. Candidate-only Cap-Spec PR #112 merged into `hl-contracts` on 2026-06-10. Head commit `75a115151bcf4dc27fc439cb56a18e8dc19f7598`; merge commit `53564550a2f20d4dbcdfd44990cd9f1f5cdf76bf`. It remains draft_candidate material, not active registry or runtime. | `zoucong121` / Gate reviewer | If next phase is desired, create a separate GitHub SSOT decision for active registry or risk-retirement scope. Do not start provider, billing, refund, settlement, HPRD, design.md, runtime, or production from this snapshot. | Active contract, HPRD, design.md, runtime, engineering start, real payment provider, real billing, real refund, real settlement, production. |
| `biz.tenant.entitlement` DS-2 | [hl-contracts#103](https://github.com/huanlongAI/hl-contracts/pull/103), [hl-platform#113](https://github.com/huanlongAI/hl-platform/pull/113) | M6 `check_only_pilot_completed` | DS-2 Tenant Entitlement Quota Check-only pilot completed on 2026-06-08. Contracts merge commit `e962c8ee381c6432b7c14bd468f79320014420af`; platform merge commit `4ab682fdf070e33fb3d18c27a6173c3cdc79bca0`. This is check-only / non-production scoped evidence. | Gate / runtime reviewer | Keep as check-only pilot evidence unless a separate GitHub SSOT decision expands scope. | Full Tenant Entitlement runtime, production, real billing, quota deduction, reserve / confirm / refund, payment provider path. |

## Action Projection

| action_id | Owner | Due / trigger | Evidence exit |
| --- | --- | --- | --- |
| `DS3-SALES-READBACK` | `cuitiantian0704` / Gate reviewer | When SalesOrder is proposed for next phase | Separate GitHub SSOT decision for active registry / HPRD / design.md / runtime, or explicit keep-candidate decision. |
| `DS3-CUSTOMER-ASSET-READBACK` | `zhuyang1204` / Gate reviewer | When CustomerAsset is proposed for next phase | Separate GitHub SSOT decision resolving active registry and cross-capability gaps, or explicit keep-candidate decision. |
| `DS3-SERVICE-READBACK` | `zoucong121` / Gate reviewer | When ServiceOrder is proposed for next phase | Separate GitHub SSOT decision for active registry / HPRD / design.md / runtime, or explicit keep-candidate decision. |
| `DS3-PAYMENT-CANDIDATE-READBACK` | `zoucong121` / Gate reviewer | After #112 merge | This file records #198 submitted and #112 merged. Any provider / billing / refund / settlement / runtime scope requires separate GitHub SSOT. |
| `DS3-DS2-CHECKONLY-READBACK` | Gate / runtime reviewer | When Tenant Entitlement is proposed beyond check-only | Separate GitHub SSOT decision for any scope beyond DS-2 check-only pilot. |

## Exclusions

This snapshot does not authorize:

- `biz.aftersale.case`
- `biz.promotion.discount`
- `biz.performance.commission`
- invoice / settlement implementation
- runtime expansion
- production release
- real payment provider path
- real billing
- real refund
- real settlement
- Feishu, Bitable, Project, dashboard, or chat summary as fact source
- new total ledger issue

## Rollback

Rollback is documentation-only:

1. Revert this refresh file.
2. Revert the `docs/delivery-recovery/README.md` pointer update.

This does not affect `hl-contracts#112` or any runtime state. If the PaymentCheckout candidate itself must be reverted, revert `hl-contracts#112` in `hl-contracts`.

## DS-3 Acceptance Condition

DS-3 can move from refreshed readback to accepted only when a human reviewer confirms that this table reflects current GitHub evidence and that each capability has one next action, one DRI, and an evidence exit.

Until then, this file is a current readback snapshot, not an acceptance report and not an active-contract promotion.
