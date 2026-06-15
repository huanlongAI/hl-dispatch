# Biz Tenant Entitlement Check-only Operating Slice v0.1

Status: DRAFT_FOR_PR_REVIEW
Date: 2026-06-15
Operating Cycle: 1
Capability: `biz.tenant.entitlement`
Task: `TE-01-CHECK-ONLY`

## 中文摘要

本文件只落 `biz.tenant.entitlement` 的 check-only 运行片。
它的作用是把已有 mock / seed / demo 配额检查证据整理成可复查闭环，
不是 Tenant Entitlement 完整能力包授权。

术语说明：

- Check-only：只做资格或配额检查，不做保留、确认、扣减、退款或结算。
- Mock / seed / demo：模拟、种子、演示数据边界，不代表商业租户真实状态。
- REVERSIBLE：当前片段可回退；一旦触碰 live billing、entitlement deduction、quota mutation 或 commercial tenant state mutation，立即升级为 GATED。
- Evidence Bundle：独立证据包，必须包含独立验证和失败路径。

## Scope

```yaml
capability_id: biz.tenant.entitlement
task_id: TE-01-CHECK-ONLY
execution_state: THIN_SLICE
risk_class: REVERSIBLE
allowed_repo_path: hl-dispatch/docs/delivery-recovery/
contract_refs:
  - hl-contracts/prd/biz/CONTRACT-GAP-Biz.TenantEntitlement.RRS-TE-0-QuotaCheckOnly.v0.1.md
  - hl-contracts/prd/biz/CONTRACT-GAP-Biz.TenantEntitlement.v0.1.md
runtime_refs_read_only:
  - hl-platform/biz/tenant-entitlement/capability-manifest.yaml
goal_mode_task_ref: docs/delivery-recovery/HL-CAPABILITY-OPERATING-RULES-GOAL-MODE-TASK-LEDGER-v0.1-2026-06-14.yaml#TE-01-CHECK-ONLY
owner_policy: TBD_FOUNDER_DECISION allowed initially
```

## Boundary

Boundary: this slice may define docs-only check-only scenarios, evidence
expectations, failure paths, and ledger status for `biz.tenant.entitlement`.
It must not change contracts, runtime implementation, schemas, registries,
manifests, configs, or live tenant state.

Review-first: this slice is evidence preparation for Founder / Gate review. It
does not grant production, runtime, full-capability, billing, quota mutation, or
commercial tenant authorization.

Founder decision required: any work outside
`hl-dispatch/docs/delivery-recovery/`, any live billing or entitlement effect,
and any attempt to treat the full Tenant Entitlement capability as active work
requires a separate Founder / Gate decision.

## Not Authorized

Not Authorized:

1. `hl-contracts` changes.
2. `hl-platform` changes.
3. Runtime, schema, registry, manifest, or config mutation.
4. Live billing mutation.
5. Live entitlement mutation, deduction, reservation, confirmation, refund, or settlement.
6. Live quota mutation.
7. Commercial tenant state mutation.
8. Production, MVP, release, or active contract claim.
9. Full Tenant Entitlement runtime workstream.
10. Gateway / HK Kernel / Can -> Action -> Audit bypass.

## Source Evidence

| source | current reading | effect |
|---|---|---|
| `CONTRACT-GAP-Biz.TenantEntitlement.RRS-TE-0-QuotaCheckOnly.v0.1.md` | Check-only RRS is the allowed narrow path. | Allows mock / seed / demo quota check evidence only. |
| `CONTRACT-GAP-Biz.TenantEntitlement.v0.1.md` | Full capability remains draft / candidate. | Full runtime work remains blocked. |
| `hl-platform/biz/tenant-entitlement/capability-manifest.yaml` | Existing pilot surface is read-only evidence input. | Referenced only; not modified or re-authorized. |
| Goal-mode task ledger | `TE-01-CHECK-ONLY` asks for a check-only evidence packet. | This file is the docs-only operating slice for that task. |

## Check-only Scenario Matrix

| scenario_id | scenario | expected result | required evidence | failure path |
|---|---|---|---|---|
| TE-CHECK-01 | Known tenant, feature in scope, quota available. | Check may return allowed / has quota. | Fixture or seed case, input identity, result, trace, and timestamp. | If evidence cannot show fixture boundary, do not advance. |
| TE-CHECK-02 | Known tenant, feature in scope, quota exhausted or absent. | Check must return not allowed / no quota. | Negative fixture, result, trace, and reason evidence. | If the result mutates quota, stop and reclassify to GATED. |
| TE-CHECK-03 | Unknown tenant or missing tenant context. | Check must fail closed or return unknown. | Input with missing tenant and failure result. | If unknown tenant creates state, stop and mark not authorized. |
| TE-CHECK-04 | Feature not entitled. | Check must return not entitled. | Feature-scope fixture and denial result. | If denial reason is absent, record evidence gap. |
| TE-CHECK-05 | Live mode, live billing, or commercial tenant flag appears. | Hard stop, no check-only progression. | Config / input readback proving no live flag was used. | Escalate to Founder / Gate; do not run or accept evidence. |
| TE-CHECK-06 | Stale seed data or generated-only evidence. | Cannot progress beyond draft evidence. | Independent verifier notes stale / generated-only gap. | Keep ledger blocked until independent verification is added. |

## Independent Verification Standard

The Evidence Bundle must include:

1. Source path and immutable commit or PR reference where possible.
2. At least one positive check and two negative / failure checks.
3. A verifier other than the generator of this package.
4. Explicit statement that no live billing, entitlement deduction, quota
   mutation, or commercial tenant state mutation occurred.
5. Failure path for accidental live-mode input, missing fixture boundary, stale
   seed data, and generated-only evidence.

Generated-only evidence is acceptable for drafting the packet, but it cannot
advance `TE-01-CHECK-ONLY` to completed evidence without independent verification.

## Ledger Update Rule

The ledger may mark this task as `check_only_operating_slice_prepared_for_review`
only after this docs-only PR exists. It must not mark Tenant Entitlement as
production authorized, release ready, MVP, active contract, or live runtime.

Any attempt to move from check-only to reservation, confirmation, deduction,
refund, billing, commercial tenant mutation, or quota mutation must become a new
Founder / Gate decision packet.

## Acceptance Criteria

1. The check-only boundary is explicit and review-first.
2. Full Tenant Entitlement remains blocked / draft-only.
3. Evidence Bundle lists independent verification and failure path.
4. Learning Patch identifies which check-only judgment can become a future rule,
   template, gate, or agent instruction.
5. Ledger remains non-authorizing and does not claim production, release, MVP,
   active contract, or live runtime.

## Validation Commands

```bash
git diff --check
git diff --name-only origin/main...HEAD
ruby -e 'require "yaml"; ARGV.each{|f| YAML.load_file(f); puts "YAML_OK: #{f}" }' docs/delivery-recovery/BIZ-TENANT-ENTITLEMENT-CHECK-ONLY-EVIDENCE-BUNDLE-v0.1-2026-06-15.yaml docs/delivery-recovery/BIZ-TENANT-ENTITLEMENT-CHECK-ONLY-LEARNING-PATCH-v0.1-2026-06-15.yaml docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml
rg -n "Boundary|Not Authorized|Review-first|Founder decision required|TE-01-CHECK-ONLY|check-only|mock|seed|demo" docs/delivery-recovery
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-github-language-gate.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-action-projection-exporter.py
```
