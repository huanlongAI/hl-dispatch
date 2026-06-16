# HL AI-Native Capability Operating Rules v0.3

> 状态：DOCS_ONLY_RULE_PATCH_FOR_FOUNDER_REVIEW
> 日期：2026-06-15
> Owner：Founder / hl-dispatch operating layer
> 范围：能力调度、readiness 跟踪、A 模式交付规则、B-Lite spike 边界
> 边界：本文不授权 runtime、生产发布、schema、registry、manifest、HPRD 启动或真实业务数据接入。
> Review-first / Founder decision required：任何从 dispatch 文档进入 contracts、runtime、schema、registry、manifest、config、release 或真实业务操作的动作，都需要单独 Founder / Gate 决策。

## 0. Source Set / 证据源集合

本文是基于当前仓库证据和 v0.2 运行规则形成的 v0.3 docs-only patch。预期的 2026-06-13 planning review 材料在本轮 review 中未找到，因此不得复制、补写或提升为仓库 SSOT。

本 patch 使用的证据：

- `hl-dispatch/docs/delivery-recovery/HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md`
- `hl-dispatch/docs/delivery-recovery/CAPABILITY-READINESS-LEDGER-v0.1.yaml`
- `hl-dispatch/docs/delivery-recovery/HL-CAPABILITY-FULL-LANDING-EXECUTION-PLAN-v0.1-2026-06-15.md`
- `hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md`
- `hl-contracts/docs/governance/dual-end-pm-audit-matrix.md`
- `hl-platform/biz/booking-fulfillment/capability-manifest.yaml`
- `hl-platform/biz/tenant-entitlement/capability-manifest.yaml`
- `hl-platform/biz/demo/capability-manifest.yaml`

## 1. 目标

本文定义唤龙 AI-native capability 工作从规划语言进入可 review 执行面的规则，避免把 draft、staging evidence、pilot manifest、PM readiness 或探索 spike 误读为 runtime / release 授权。

Founder D-003 指定原句：

A is the formal delivery channel. B-Lite is not a delivery channel.

运行目标不是增加重治理，而是提升判断质量：

1. 让 Capability DRI 在低风险 A 模式工作中默认推进；
2. 让 GATED A 模式工作提前暴露 Gateway、Human End、Agent End、证据和审计路径缺口；
3. 防止 AI 生成物自证完成；
4. 允许 Founder-led learning spike，但不创建平行交付系统；
5. 将可复用教训吸收到 A 模式规则、模板、gate、owner review 或 defer decision。

## 2. SSOT 边界

| 层级 | 仓库 | 权威内容 | 本文权限 |
|---|---|---|---|
| Contract SSOT | `hl-contracts` | capability registry、rules、reason_code、OpenAPI、events、facts、PM capability specs | 只能引用 |
| Dispatch / recovery | `hl-dispatch` | taskbooks、recovery snapshots、operating rules、readiness ledger、decision logs | 可创建和更新文档 |
| Runtime | `hl-platform` | runtime implementation、module manifests、readiness gate、handlers、fixtures | 只能引用 |

`hl-dispatch` 中的任何文件都不得成为 `hl-contracts` 或 `hl-platform` 的新 SSOT。

## 3. 非授权边界

以下材料不授权 runtime 或 release：

1. DRAFT Cap-Spec。
2. PM readiness pack。
3. checks success。
4. staging evidence。
5. pilot manifest。
6. runtime candidate manifest。
7. Ledger entry。
8. Evidence Bundle index。
9. Founder discussion in chat。
10. AI audit report。
11. B-Lite spike output。

runtime、release、schema、registry、taxonomy、payment、billing、entitlement、customer identity、privacy、contract、production data 变更，必须通过对应仓库证据链取得明确 Gate / Founder 授权。

## 4. A 模式：正式交付通道

A 模式是 capability 工作唯一正式交付通道。

formal capability status、contract movement、runtime movement、M0-M9 maturity progression、Gate decision、production authorization 和 release claim，只能通过 A 模式 artifacts 与 evidence 建立。

A 模式保留 v0.2 的运行骨架：

1. Capability DRI。
2. PM readiness。
3. Engineering / Gate preflight。
4. Evidence Bundle。
5. Readiness Ledger。
6. Learning Patch。
7. 需要时进入 Founder / Gate decision。

`CAPABILITY-READINESS-LEDGER-v0.1.yaml` 继续只属于 A 模式。它记录 execution state、risk class、blockers、missing evidence、next action 与 non-authorization boundary；它不跟踪 B-Lite 进度。

## 5. 保留的 A 模式规则

### 5.1 DRI Pull Model

Capability DRI 负责推动 A 模式 capability item 形成：

1. Capability Execution Card。
2. Evidence Bundle。
3. Readiness Ledger update。
4. next-action proposal。
5. Learning Patch。

DRI 不拥有 runtime authorization、production release authorization、`hl-contracts` schema / registry modification、`hl-platform` runtime / manifest modification、Gate H approval、Founder approval，或 financial / identity / privacy / contract / live entitlement decision。

### 5.2 Pull Triggers

当工作触及 formal facts、resource occupancy、payment、refund、billing、settlement、entitlement、customer identity、privacy、contract、live data、Gateway / Can path、Human End、Agent manifest、retry / idempotency、reason trace、event、fact、audit evidence、low confidence 或 owner conflict 时，DRI 必须拉起 PM、Gate Owner、Engineering Owner 或 Founder。

### 5.3 Risk Class

在后续基于证据修订前，执行层只使用两类 risk class：

| risk_class | 定义 | 默认路径 |
|---|---|---|
| REVERSIBLE | 不创建或修改 formal business facts、live resource occupancy、money、billing、entitlement、customer identity、privacy、contract 或 production data；可回滚或丢弃。 | DRI 可带证据推进。 |
| GATED | 会修改或可能修改 formal facts、live resource occupancy、money、billing、entitlement、identity、privacy、contract、production data 或 bypass-sensitive runtime paths；或难以回滚。 | 推进前必须暴露 Gate / Human / Founder / independent evidence。 |

不明确时，按 GATED 处理。

### 5.4 Execution State

| execution_state | 含义 | 允许工作 | 不允许 |
|---|---|---|---|
| SPEC_ONLY | 只做规划、PM spec、gap analysis、readiness clarification。 | Cap-Spec review、Contract Gap、reason proposal、scope definition。 | runtime implementation、live object mutation、release claim。 |
| THIN_SLICE | 受控 mock / seed / demo / staging / check-only slice。 | fixtures、manifest review、check-only evidence、Gateway path exploration。 | live business operation 或 release claim。 |
| RELEASE_CANDIDATE | 证据接近 release review 完整度。 | release / security / product evidence assembly、rollback plan、Gate H review。 | 未获明确授权的 release。 |

Execution state 不替代 M0-M9 maturity。证据存在时，Ledger 必须同时记录两者。

### 5.5 Ledger Rules

1. Ledger 是 status surface，不是 registry。
2. Ledger 只引用 SSOT paths，不复制完整 contracts、key_action definitions、reason_code definitions、OpenAPI、events 或 facts。
3. 每个 active、PM-led 或 pilot closeout 的 A 模式 item 必须有 Ledger row。
4. owner 未知时使用 `TBD_FOUNDER_DECISION`，不得编造姓名。
5. 缺少 `not_authorized` 的 Ledger item 无效。
6. 缺少 Gateway / Can path evidence 的 GATED item 为 blocked 或 partial。
7. 只有 generated evidence 的 GATED item 不得推进。
8. Ledger 保持 A-only，不增加 B-Lite state。

### 5.6 Evidence And Learning

Evidence Bundle 是证据索引，不替代 acceptance manifest、readiness gate、release evidence 或 Gate H。

任何 GATED advancement 的 Evidence Bundle 必须包括 independent verifier、verification method、happy path evidence、failure path evidence、open risk list、rollback / exit path、gate decision state，以及关联的 SSOT / repo / issue / PR evidence。

任何 A 模式状态推进后，DRI 必须产出 Learning Patch。没有 Learning Patch，则该推进不完整。

## 6. 初始组合策略

| Item | v0.3 policy |
|---|---|
| Booking staging pilot / `hl-platform#106` | 只做 closeout；没有 live evidence 不得声称 release。 |
| `biz.booking.fulfillment` | 第一个 A pilot candidate；PATCH 范围仅限 Human End、Agent manifest、override owner matrix、retry / duplicate policy、failure / audit evidence。不得称为 MVP、production、merged delivery 或 production-authorized。 |
| `biz.sales.order` | SPEC_ONLY / GATED；只进入 PM readiness。 |
| `biz.customer.asset` | SPEC_ONLY / GATED；只进入 PM readiness 与 Contract Gap decision。 |
| `biz.offer.catalog` | SPEC_ONLY / GATED；工程前先补 Gateway / OpenAPI / idempotency / approval matrix。 |
| `biz.store.resource` | SPEC_ONLY / GATED；工程前先补 Gateway / state machine / retry / idempotency。 |
| `biz.tenant.entitlement` | 第一个 B-Lite spike candidate 为 check-only；A 模式 Ledger 另行保持。 |
| `biz.payment.checkout` | SPEC_ONLY / GATED；只做 preflight / blocker。 |
| `biz.customer.profile` | dependency candidate / Founder-Gate contract phase；本周期不是 active runtime workstream。 |

## 7. B-Lite：Founder-Led AI Spike

B-Lite 是 Founder-led AI Spike，只服务于有限学习。它不是交付通道，不是 capability status，不是 engineering-start signal，也不是 runtime 或 contract authorization path。

六条硬规则：

1. B-Lite 只能是 Founder-led AI Spike。
2. B-Lite 必须 timeboxed，最长 2 天。
3. B-Lite 不得修改 `hl-contracts` truth source。
4. B-Lite 不得修改 production runtime、global config、production data、customer identity、privacy、payment、refund、settlement、contract、entitlement 或 real resource occupancy。
5. B-Lite artifacts 必须标记为 `B-SPIKE` 或 `lab`；不得使用 ready、done、MVP、production、authorized、active contract 或等价正式状态词。
6. B-Lite output 没有 formal status；除非后来被 A 通过 A artifacts、owner review、evidence chain 吸收。

B-SPIKE template：

```text
B-SPIKE: <capability / problem>
Timebox: <4h / 1d / 2d, max 2d>
Goal: <what to test>
Forbidden: <truth source / production / real data / payment / identity / runtime boundaries>
Output: <prototype / fixture / failure case / audit / gap list / B-NOTE>
```

B-NOTE template：

```text
B-NOTE: <B-SPIKE name>

1. Result:
2. Where I got stuck:
3. What A would have forced:
4. What A can reuse:
5. Decision: ABSORB / REJECT / RERUN / KEEP_AS_REFERENCE
```

第一个已批准 B-Lite spike 文本：

```text
B-SPIKE: biz.tenant.entitlement check-only
Timebox: 1d
Goal: Test whether Founder + Agent can produce quota check-only demo notes, fixtures, and failure cases that A can reuse.
Forbidden: No real billing, no real entitlement deduction, no production data, no production runtime, no `hl-contracts` truth source modification.
Output: lab notes, fixtures, failure case, and one B-NOTE.
```

B-Lite 不得创建编号化生命周期、实验状态表、转正包模板、多步流程、固定周节奏、额外就绪门禁或任何平行运行系统。若学习结果有价值，只能记录为短 B-NOTE，或在 A owner 吸收后转成 A 模式 Learning Patch。

## 8. 禁止事项

不得：

1. 将 DRAFT 当作 active contract；
2. 将 checks success 当作 readiness；
3. 将 staging evidence 当作 release；
4. 将 pilot manifest 当作 production authorization；
5. 让 Agent 绕过 Gateway / HK Kernel / Can -> Action -> Audit；
6. 只凭 PM readiness 启动 runtime；
7. 未经明确授权接入 live payment、billing、entitlement、identity、privacy、contract 或 production data；
8. 把 `hl-contracts` SSOT 复制进 Ledger；
9. 用 generated-only evidence 推进 GATED work；
10. 未经 Founder decision 把 candidate / deferred packages 扩成 active delivery；
11. 将 B-Lite output 当作 formal delivery status。

## 9. Traceability Matrix / 追溯矩阵

| 规则 | Source path + line | Target section | Patch summary |
|---|---|---|---|
| `hl-dispatch` docs 可引用但不得替代 `hl-contracts` / `hl-platform` SSOT | `HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md:L21-L29` | 2 | 保留 SSOT 边界。 |
| Draft、PM readiness、checks、staging evidence、pilot manifest、Ledger、AI audit 不授权 runtime 或 release | `HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md:L31-L47` | 3 | 将 B-Lite output 加入非授权清单。 |
| DRI 不拥有 runtime、production、contract、platform、Gate H、Founder、finance、identity、privacy 或 live entitlement decision | `HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md:L70-L80` | 5.1 | 保留 A 模式 DRI 边界。 |
| Ledger 是 status surface、引用 SSOT，且不能推进只有 generated evidence 的 GATED item | `HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md:L145-L154` | 5.5 | 保持 Ledger A-only 和非授权属性。 |
| Booking 是 PATCH / THIN_SLICE / GATED；Tenant Entitlement 未获后续授权前只做 check-only | `HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md:L220-L232` | 6 | 加入已批准的第一个 A candidate 和第一个 B-Lite spike。 |
| 既有 full landing plan 为 docs-only，不授权 contracts、platform、runtime、production、release、MVP、active contract 或 live operation | `HL-CAPABILITY-FULL-LANDING-EXECUTION-PLAN-v0.1-2026-06-15.md:L34-L39` | 3, 8 | 保留 docs-only 非授权边界。 |
| Readiness Ledger 不是 contract 或 runtime registry，且不授权 live operations | `CAPABILITY-READINESS-LEDGER-v0.1.yaml:L5-L9` | 4, 5.5 | 保持 Ledger A-only，防止 B-Lite tracking。 |
| Founder 已签第一批四个 capability packages | `HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md:L342-L354` | 6 | 使用首批背景，不改 SSOT。 |
| PM dual-end gate reports 13 BLOCKED、1 PATCH_REQUIRED、1 PASS_WITH_WAIVER | `hl-contracts/docs/governance/dual-end-pm-audit-matrix.md:L80-L85` | 4, 6 | 保留 A 模式 entry gate 背景。 |
| Booking platform manifest 为 pilot | `hl-platform/biz/booking-fulfillment/capability-manifest.yaml:L1-L5` | 6 | 防止把 staging / pilot 误读为 production。 |
| Tenant Entitlement manifest 为 pilot check-only | `hl-platform/biz/tenant-entitlement/capability-manifest.yaml:L1-L28` | 6, 7 | 锚定第一个 B-Lite check-only spike。 |
| Demo manifest 为 sample-exempt | `hl-platform/biz/demo/capability-manifest.yaml:L13-L23` | 3, 6 | 防止 demo sample 变成 formal capability status。 |

## 10. 验证命令

docs patch 后运行：

```bash
git status --short --branch
git diff --name-only
git diff --check
git ls-files --others --modified --exclude-standard
git ls-files --others --modified --exclude-standard | grep -E '^(../)?(hl-contracts|hl-platform|hl-scene-app)/' && exit 1 || true
# 按 Founder D-008 指定词表，对本文和 README 执行 B-Lite 过度治理关键词扫描；词表不在本文内重复，避免自引用命中。
```

## 11. 修订规则

v0.3 必须保持轻量。任何新增字段、角色、仪式或 gate，都必须证明它解决了现有 A 模式字段或短 B-Lite note 不能处理的重复失败或风险。
