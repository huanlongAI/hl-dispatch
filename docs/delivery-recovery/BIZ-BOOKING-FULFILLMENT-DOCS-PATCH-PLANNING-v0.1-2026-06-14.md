# Biz Booking Fulfillment Docs Patch Planning v0.1

<!-- task-snapshot:v1 -->

Snapshot date: 2026-06-14

## Scope

This file is the docs-only patch planning task packet authorized by
`BIZ-BOOKING-FULFILLMENT-FOUNDER-GATE-DECISION-READBACK-v0.1-2026-06-14.md`.

It converts the approved Founder / Gate decisions into bounded follow-up
documentation work for `biz.booking.fulfillment`.

This planning packet does not authorize `hl-contracts` changes, `hl-platform`
changes, runtime code, schema, registry, manifest, app resource, config,
OpenAPI, events, facts, reasoncodes, release, production operation, MVP pass,
active contract registration, live booking operation, live customer data,
payment, billing, entitlement mutation, identity/privacy mutation, or formal
business object mutation.

## Boundary

Boundary: this packet plans follow-up docs-only work under
`hl-dispatch/docs/delivery-recovery/`. It is not a contract registry, runtime
registry, capability manifest, schema, OpenAPI, events, facts, reasoncodes,
production approval, release approval, MVP pass, or live business operation
approval.

Review-first: follow-up packets must be reviewed as docs-only evidence before
any contract or runtime work is requested.

Founder decision required: any work outside `hl-dispatch/docs/delivery-recovery/`
or any contract/runtime/schema/registry/manifest/config mutation requires a
separate Founder / Gate GitHub SSOT.

## Not Authorized

Not Authorized:

1. `hl-contracts` changes.
2. `hl-platform` changes.
3. runtime implementation.
4. schema, registry, manifest, app resource, or config mutation.
5. OpenAPI, events, facts, or reasoncodes mutation.
6. production, release, MVP, active contract, or live booking operation.
7. payment, billing, entitlement, identity/privacy, sales order, customer asset,
   provider, service order, or formal business object mutation.
8. bypassing Gateway / HK Kernel / Can -> Action -> Audit.

## Task Snapshot

```yaml
capability_id: biz.booking.fulfillment
track: docs_only_patch_planning
state: planned
risk_class: GATED
execution_state: THIN_SLICE
maturity: M6_M7
current_date: 2026-06-14
dri: PM-A / 邹骢
pm_owner: PM-A / 邹骢
gate_owner: Gate-H / 许久明
decision_readback_ref: docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-FOUNDER-GATE-DECISION-READBACK-v0.1-2026-06-14.md
readiness_package_ref: docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-READINESS-PATCH-PACKAGE-v0.1-2026-06-14.md
evidence_bundle_ref: docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-EVIDENCE-BUNDLE-v0.1-2026-06-14.yaml
ledger_ref: docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml#biz.booking.fulfillment
allowed_repo: hl-dispatch
allowed_path: docs/delivery-recovery/
contract_authorization: not_authorized
runtime_authorization: not_authorized
production_authorization: not_authorized
ledger_state_progression: not_authorized_by_this_packet
```

## Current Result

The approved next phase is `GO_DOCS_PATCH_PLANNING_ONLY`.

`biz.booking.fulfillment` remains:

```yaml
execution_state: THIN_SLICE
risk_class: GATED
cap_spec_status: patch_package_prepared
pm_dual_end_review: PATCH_REQUIRED
runtime_authorization: not_authorized
active_contract_authorization: not_authorized
production_authorization: not_authorized
```

## Planning Lanes

| Lane | Owner | Required docs-only output | Acceptance |
|---|---|---|---|
| Human End patch | PM-A / 邹骢, Gate-H / 许久明 | Human End surface pack for NUI intent entry, GUI state anchor, confirmation, review, audit, exception handling, and deterministic non-chat controls. | Names surfaces, high-risk human confirmation thresholds, audit references, and exception review path without runtime authority. |
| Agent End patch | Gate-H / 许久明, PM-A / 邹骢 | Agent manifest readiness criteria for tool discovery, tool pruning, context budget, pagination, evidence summarization, schema preservation, Can-before-Action, and Action rechecks Can. | Blocks unpruned tools, fabricated availability, final booking authority, and Gateway bypass. |
| Gateway / Can / Action / Audit patch | Gate-H / 许久明 | Docs-only confirmation of fail-secure behavior, denied Can no-mutation rule, event_id / trace_id / reason_code / audit_ref preservation, and Action re-checks Can. | Every key action has a visible Can -> Action -> Audit trace requirement. |
| Override owner matrix | Gate-H / 许久明, PM-A / 邹骢 | Owner / approver / approval_ref matrix for critical override paths. | No breakglass, override, or approval_ref path becomes active unless recorded and separately authorized. |
| Retry / duplicate policy | Gate-H / 许久明, PM-A / 邹骢 | Retryable and non-retryable failure classes, idempotency replay result, duplicate submission result, conflict handling, internal error recovery, and duplicate audit behavior. | Duplicate and retry behavior is deterministic and auditable. |
| External dependency exit path | PM-A / 邹骢, Gate-H / 许久明 | StoreResource / QRH, CustomerProfile precheck, OfferCatalog requirement, and legacy mapping fail-secure or governed resubmit path. | Cross-capability effects are called out and blocked unless separately recorded. |
| Gate-H reuse readback | Gate-H / 许久明 | Explicit statement that the 2026-05-25 Gate-H record is historical engineering evidence only. | New runtime, contract, production, release, MVP, or active-contract claim requires a separate Founder / Gate decision. |

## Minimum Follow-Up Packet Shape

Each follow-up docs-only packet must include:

```yaml
required_sections:
  - Boundary
  - Not Authorized
  - Review-first
  - Founder decision required
  - current PM dual-end blocker
  - affected action or surface list
  - owner and reviewer
  - evidence refs
  - acceptance criteria
  - failure path
  - rollback or exit path
  - validation commands
not_authorized_must_include:
  - hl-contracts changes
  - hl-platform changes
  - runtime implementation
  - schema / registry / manifest / config mutation
  - OpenAPI / events / facts / reasoncodes mutation
  - production / release / MVP / active contract
  - live booking operation
  - Gateway / HK Kernel / Can -> Action -> Audit bypass
```

## Proposed Follow-Up Files

These files are proposed next. They are not created by this packet unless a
later task explicitly asks to land them.

| Proposed file | Purpose |
|---|---|
| `BIZ-BOOKING-FULFILLMENT-HUMAN-END-PATCH-PACKET-v0.1-2026-06-14.md` | Human End surfaces and acceptance criteria. |
| `BIZ-BOOKING-FULFILLMENT-AGENT-END-PATCH-PACKET-v0.1-2026-06-14.md` | Agent End readiness, tool pruning, context budget, and audit preservation. |
| `BIZ-BOOKING-FULFILLMENT-GATEWAY-CAN-AUDIT-PATCH-PACKET-v0.1-2026-06-14.md` | Gateway / Can / Action / Audit trace preservation. |
| `BIZ-BOOKING-FULFILLMENT-OVERRIDE-RETRY-PATCH-PACKET-v0.1-2026-06-14.md` | Override owner matrix, approval_ref policy, retry, duplicate, and idempotency behavior. |
| `BIZ-BOOKING-FULFILLMENT-DEPENDENCY-EXIT-PATH-PACKET-v0.1-2026-06-14.md` | StoreResource, CustomerProfile, OfferCatalog, and legacy mapping exit paths. |

## Action Projection

| action_id | Owner | Trigger | Evidence exit |
|---|---|---|---|
| `BF-HUMAN-END-PACKET` | PM-A / 邹骢 | This planning packet merges | Human End patch packet PR merged in `hl-dispatch`. |
| `BF-AGENT-END-PACKET` | Gate-H / 许久明 | This planning packet merges | Agent End patch packet PR merged in `hl-dispatch`. |
| `BF-GATEWAY-CAN-AUDIT-PACKET` | Gate-H / 许久明 | This planning packet merges | Gateway / Can / Action / Audit packet PR merged in `hl-dispatch`. |
| `BF-OVERRIDE-RETRY-PACKET` | Gate-H / 许久明, PM-A / 邹骢 | This planning packet merges | Override and retry packet PR merged in `hl-dispatch`. |
| `BF-DEPENDENCY-EXIT-PACKET` | PM-A / 邹骢 | This planning packet merges | Dependency exit path packet PR merged in `hl-dispatch`. |
| `BF-BLOCK-CONTRACT-RUNTIME` | Gate / Engineering | Any contract or runtime mutation request | Stop and require separate Founder / Gate GitHub SSOT. |

## Stop Conditions

Stop and request a separate Founder / Gate decision if any next step attempts to:

1. modify `hl-contracts`;
2. modify `hl-platform`;
3. modify runtime code, schema, registry, manifest, config, OpenAPI, events, facts, reasoncodes, or capability blueprint;
4. claim release, production, MVP, active contract, runtime authorization, or live booking operation;
5. mutate customer identity, privacy, payment, billing, entitlement, sales order, customer asset, provider, service order, or formal booking object state;
6. allow Agent calls to bypass Gateway / HK Kernel / Can -> Action -> Audit.

## Validation Commands

```bash
git status --short --branch
git diff --check
rg -n "Boundary|Not Authorized|Review-first|Founder decision required|GO_DOCS_PATCH_PLANNING_ONLY|Gateway / HK Kernel / Can -> Action -> Audit|邹骢|许久明" docs/delivery-recovery/BIZ-BOOKING-FULFILLMENT-DOCS-PATCH-PLANNING-v0.1-2026-06-14.md
```

## No Evidence, No Done

This packet is complete only after it lands through GitHub PR with passing
checks and path-scope verification. It does not make any proposed follow-up
packet complete.
