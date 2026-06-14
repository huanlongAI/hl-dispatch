# Founder Decision Log — Capability Operating Rules v0.1

> Status: DECISION_LOG_DRAFT
> Date: 2026-06-14
> Scope: records Founder authorization for docs-only landing of capability operating rules, Ledger, implementation plan, and templates.
> Boundary: This log does not authorize runtime, production release, schema change, registry change, live business-data integration, live payment, live billing, live entitlement mutation, identity/privacy mutation, or contract mutation.

## Decision Record

| ID | Decision | Result |
|---|---|---|
| D-001 | Land rule doc at `hl-dispatch/docs/delivery-recovery/HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md` | APPROVED |
| D-002 | Land YAML Ledger at `hl-dispatch/docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml` | APPROVED |
| D-003 | First implementation only touches `hl-dispatch/docs/delivery-recovery/` | APPROVED |
| D-004 | Initial Ledger scope includes 8 items | APPROVED |
| D-005 | Booking pilot closeout must not be called release/production/merged without evidence | APPROVED |
| D-006 | `biz.customer.profile` remains dependency candidate / authorized contract phase only | APPROVED |
| D-007 | `biz.sales.order` and `biz.customer.asset` are PM readiness only | APPROVED |
| D-008 | `biz.offer.catalog` and `biz.store.resource` must patch gaps before engineering | APPROVED |
| D-009 | `biz.payment.checkout` remains preflight/blocker only | APPROVED |
| D-010 | `biz.tenant.entitlement` remains check-only mock/seed/demo only | APPROVED |
| D-011 | Owner fields may use `TBD_FOUNDER_DECISION`; owner assignment due within 48h | APPROVED |
| D-012 | Learning Patch required after state progression | APPROVED |
| D-013 | Evidence Bundle must include independent verification and failure path for GATED progression | APPROVED |
| D-014 | Founder behavior discipline is part of the operating rules | APPROVED |
| D-015 | Target branch safety policy required before landing | APPROVED |
| D-016 | Supplementary templates under dispatch docs allowed | APPROVED |
| D-017 | Proceed with docs, Ledger, and full plan landing | GO_IMPLEMENT_DOCS_LEDGER_PLAN |

## Non-Authorization Statement

This decision log records dispatch-layer operating-plan authorization only. It does not authorize:

1. `hl-contracts` changes.
2. `hl-platform` changes.
3. runtime implementation.
4. live release.
5. live business operation.
6. production data access.
7. live payment, billing, entitlement, identity, privacy, or contract mutation.

## Next Required Review

After Codex lands the docs-only plan, Founder must review:

1. diff summary;
2. initial Ledger rows;
3. owner gaps;
4. forbidden path check;
5. future contract decision packets;
6. future platform decision packets.
