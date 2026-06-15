# HL Platform Decision Packet Capability Full Landing v0.1

Status: READY_FOR_FOUNDER_GATE_REVIEW
Date: 2026-06-15
Target repo: `hl-platform`

## 中文摘要

本文是 full landing 后续可能需要的 `hl-platform` 裁决包。它只准备 runtime
探索前的裁决面，不修改 platform 代码、不改 manifest、不跑 runtime、不授权生产。

## 术语说明

- platform decision packet：平台裁决包，用来请求是否允许未来改
  `hl-platform`。
- fixture plan：未来 runtime 验证可能需要的 fixture 计划，当前不创建。
- readiness gate：未来平台 gate，当前只做裁决输入。

## Candidate platform decisions

| Capability | Candidate target | Intent | Evidence refs | Owner |
|---|---|---|---|---|
| `biz.booking.fulfillment` | `hl-platform/biz/booking-fulfillment/**` | decide whether docs-only BF closeout can proceed to runtime exploration | BF rollup and decision packet | Gate-H + Engineering Owner |
| `biz.offer.catalog` | future module/UI/gateway surfaces | decide whether approval / visibility runtime work is needed | Offer Catalog gap pack | Gate-H + Engineering Owner |
| `biz.store.resource` | future module/state/QRH surfaces | decide whether resource state machine runtime work is needed | Store Resource gap pack | Gate-H + Engineering Owner |
| `biz.tenant.entitlement` | check-only fixture surfaces only if approved | decide whether independent check-only runtime evidence may be gathered | TE closure blocker | Gate-H |
| `biz.payment.checkout` | none until financial gate | keep blocked unless Founder/Gate explicitly authorizes preflight runtime exploration | Payment preflight packet | Founder/Gate |

## Requested Founder / Gate decision

Choose one:

```text
PREPARE_PLATFORM_CHANGE_PLAN_ONLY: <capability scope>
```

```text
HOLD_PLATFORM_WORK_BLOCKED: <owner/evidence gap>
```

```text
DEFER_PLATFORM_WORK: <reason>
```

## Rollback or defer option

If future platform work is not approved, no runtime rollback is needed because
this packet changes no runtime state.

## Not Authorized

Not Authorized: editing `hl-platform`, runtime code, manifest, config,
readiness gate implementation, fixture creation, production, release, MVP,
active contract, live booking, live payment, billing, entitlement deduction,
quota mutation, identity/privacy mutation, or formal business object mutation.
