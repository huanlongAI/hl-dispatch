# HL Capability Discovery Value Loop v0.1

Status: LONGRUN_DOCS_ONLY_DISCOVERY_LOOP_PREPARED
Date: 2026-06-15

## 中文摘要

本文恢复 full landing 的上游产品价值判断循环。它回答哪些能力值得 DRI 槽位、
哪些价值可观察、哪些候选项应延期，以及 Founder 产品价值裁决与下游风险接受
裁决的边界。

## 术语说明

- DRI slot：直接负责人槽位，只有值得推进的能力项才应占用。
- observable value：用户或系统价值必须能被证据观察。
- discovery boundary：产品价值裁决边界，不等于 runtime 风险接受。

## Discovery questions

| Question | Owner | Output |
|---|---|---|
| Which capability deserves a DRI slot? | Founder / PM lead | DRI slot decision |
| What user/system value is observable? | PM owner | value evidence or deferral reason |
| What should stay candidate/deferred? | Founder / PM / Gate | candidate/defer list |
| Where does Founder product judgment end? | Founder | discovery decision boundary |
| Where does downstream risk acceptance start? | Gate-H | risk acceptance decision packet |

## Initial value readback

| Capability | Discovery state |
|---|---|
| `biz.booking.fulfillment` | Value already selected for closeout; next is Founder / Gate decision. |
| `biz.sales.order` | Candidate for contract decision after PM readiness. |
| `biz.customer.asset` | Candidate for contract decision after identity/privacy boundary review. |
| `biz.offer.catalog` | Candidate pending supply-side gap decision. |
| `biz.store.resource` | Candidate pending resource state / QRH decision. |
| `biz.tenant.entitlement` | Keep check-only until independent evidence. |
| `biz.payment.checkout` | Keep blocked until financial value/risk decision. |

## Not Authorized

Discovery does not authorize contract implementation, platform implementation,
runtime, production, release, MVP, active contract, live booking, live payment,
billing, entitlement deduction, quota mutation, identity/privacy mutation, or
formal business object mutation.
