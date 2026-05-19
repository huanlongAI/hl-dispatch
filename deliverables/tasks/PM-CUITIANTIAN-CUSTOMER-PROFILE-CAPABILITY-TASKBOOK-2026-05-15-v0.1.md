# PM 崔田恬正式能力包规划：`biz.customer.profile` v0.1

> 日期：2026-05-15
> 状态：FORMAL TASKBOOK DRAFT / owner confirmed via `hl-dispatch#109` / pending PR merge to main
> 建议 Owner：PM 崔田恬（GitHub: `cuitiantian0704`）
> 建议能力包：`biz.customer.profile`（客户档案）
> 规划来源：基于 `hl-dispatch#39/#40/#80/#98/#99/#109`、`hl-contracts#29/#30/#35/#38/#40/#42/#43/#44`、`hl-contracts#36`、`team-memory` 崔田恬 readiness 记录
> 边界：本文件是正式 taskbook，不修改 `hl-contracts`，不注册 reason_code，不写 OpenAPI / facts / events / runtime code，不授权工程开工。GitHub PR / Issue / repo files 是 SSOT；飞书 / Project / Base 只做 projection，不承载正式真源。

## 0. 结论

建议将崔田恬的首个正式能力包规划为：

```text
biz.customer.profile
中文名：客户档案
首版目标：定义“谁来预约”以及客户主体如何被创建、识别、合并、停用，并如何与 AI Draft / booking draft / confirmed booking 建立可审计关联。
```

原因：

1. 朱阳主线已进入 `biz.store.resource` Draft PR 收尾阶段，继续派供给侧能力包会造成 owner 重叠。
2. 邹骢主线当前仍限定在 `biz.booking.fulfillment / booking`；`hl-contracts#43/#44` 已完成 booking OpenAPI 契约落库，但 `biz.customer.profile` 仍无 merged baseline。
3. `hl-dispatch#98` 已明确 `biz.customer.profile` 当前是 `blocked`：Founder Signed 已立项，但未看到已合并 `prd/biz` 基线包。
4. 崔田恬已完成 `hl-dispatch#80` readiness 与 team-memory 链路准备，适合接一个边界清晰、但能补齐 booking 主链缺口的 PM 能力包。

注意：`HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6` 原始分工中 `biz.customer.profile` 属于 PM-2 邹骢。`hl-dispatch#109` 已作为 Owner Confirmation SSOT 接受崔田恬承接本包；在本文件进入 `hl-dispatch main` 前，#109 仍将 `work_state` 保持为 `blocked`，不得发布 implementation assignment。#109 正文或评论不得替代本正式 taskbook SSOT。

## 0.1 最新 GitHub 状态（2026-05-16）

- `hl-dispatch#109`：崔田恬已用 GitHub 账号 `cuitiantian0704` 回复结构化 YAML，`confirmation_state=confirmed`。
- `hl-dispatch#109` 当前阻塞：taskbook 在 `hl-dispatch main@9e4a597` 不可见；本文件发布并合入 main 后可解除“缺少任务书可见性”这一前置阻塞，但仍不授权工程开工。
- `hl-contracts#43/#44`：booking OpenAPI contract 已合并，`hl-contracts#43` 已关闭；`hl-contracts#30` 仍是 Draft business baseline。
- `hl-contracts#36`：`biz.store.resource` 仍为 Draft PR，checks 通过，等待 review / Gate。
- `hl-dispatch#99`：工程前置仍为 `PARTIAL / ENGINEERING_PREP_IN_PROGRESS / NOT_RUNTIME_READY`，本包只能进入 PM Cap-Spec Draft，不进入 runtime。


## 0.2 状态维度与 SSOT 边界

本任务使用四个独立状态维度，禁止混用：

| 维度 | 当前值 | 含义 | 变更条件 |
|---|---|---|---|
| `dispatch_state` | `taskbook_pr_pending` | 正式 taskbook 已在本分支发布，等待 PR 审查 / 合并 | PR 合并到 `main` 后可改为 `taskbook_visible_on_main` |
| `confirmation_state` | `confirmed` | `hl-dispatch#109` 已完成 Founder / owner confirmation | 仅 GitHub Issue / PR 证据可变更 |
| `work_state` | `blocked_until_taskbook_main` | 在 taskbook 未合入 `main` 前，不进入正式 Draft PR 执行 | taskbook 合入 `main` 后可移到 `ready-for-formal-Draft-PR`；仍不授权工程开工 |
| `projection_state` | `projection_only` | 飞书 / Project / Base 可提醒和展示，但不是事实真源 | 只能由 GitHub PR / Issue / repo 文件投影更新 |

SSOT 边界：GitHub PR / Issue / repo files 是正式事实真源；飞书、Project、Base、群聊与个人转述仅为 projection，不得替代 taskbook、PR 或 Issue 证据。

## 1. 当前进展基线

| 主线 | 当前状态 | 对崔田恬规划的影响 |
|---|---|---|
| `biz.offer.catalog` | `hl-contracts#29` 已合并，性质为 DRAFT Cap-Spec evidence baseline | 可作为客户档案的非直接参考；不得复制其 gap / reason_code 提案为已生效契约 |
| `biz.store.resource` | `hl-contracts#36` Draft PR 已存在，最新回填显示 checks 通过，等待 review / Gate | 不建议崔田恬介入，避免供给侧 owner 重叠 |
| `biz.booking.fulfillment / booking` | `hl-contracts#30` 仍 Draft；`#35/#38/#40/#42/#44` 已合并，`#43` 已关闭 | 客户档案必须服务 booking，但不得改写 booking 状态机或 hold 生命周期 |
| `biz.customer.profile` | 尚无 merged baseline；`#98` 标记为 blocked；`#109` owner confirmation 已 confirmed | 正好作为崔田恬首包候选；本文件发布后 PM 可继续 SDD 厘清与 Draft 准备 |
| 工程接入 | `#99` 总状态仍是 `PARTIAL / NOT_RUNTIME_READY` | 本包只能做 Cap-Spec，不授权 runtime |
| QA / 测试链路 | `#61/#79` 仍未闭环 | 不作为工程开工依据 |
| 旧 Java 事实 | `#94` 已有客户 / 门店 / 资产 / 店铺主相关事实提取 | 仅作为历史事实与验收样本输入，不作为新系统 SSOT |
| PHP 店铺主事实 | `#96` 已因 owner 离职归档 | 店铺主 / invest 不进入本包首版，只进 Contract Gap 或后续营销能力包候选 |

## 2. 能力包边界

### 2.1 一句话定义

`biz.customer.profile` 定义客户主体识别、基础档案、客户创建 / 更新 / 合并 / 停用，以及客户与预约草稿、正式预约的业务关联。

### 2.2 首版目标

- 明确客户主体是什么：自然人消费者、门店客户关系、联系方式与最小可识别信息。
- 明确客户如何被创建：客户自助、员工代建、AI Draft 触发候选创建。
- 明确客户如何被用于 booking：AI Draft、booking draft、confirmed booking 如何引用客户。
- 明确客户资料变化的 key_action、审计证据和 reason_code 提案边界。
- 明确客户合并、重复客户识别、停用的业务语义与风险。
- 明确哪些客户资产 / 会员 / 权益 / 店铺主信息不得进入首版。

### 2.3 首版非目标

- 不做储值、次卡、权益、会员等级、客户资产。
- 不做店铺主 / invest / 分销身份 / 营销方案。
- 不做支付、结算、钱包、佣金、抵扣金。
- 不定义 booking 状态机、resource hold、confirmed booking 生命周期。
- 不定义 offer / store resource 主数据。
- 不写 HK.ID、HK.Consent、HK.Audit 的 Tier 1 SSOT，只引用其触发点。
- 不注册正式 reason_code、OpenAPI、event、facts、DB schema 或 runtime code。

## 3. 必读材料

崔田恬启动正式能力包前，Codex 需先读取：

1. `hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md`
2. `hl-dispatch/deliverables/decisions/PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS-v0.1.md`
3. `hl-dispatch/deliverables/decisions/PRD-REDEFINITION-SPEC.md`
4. `hl-dispatch#40` 与 `hl-contracts#30/#35/#38/#40/#42/#43/#44`
5. `hl-dispatch#98/#99`
6. `hl-dispatch#94` 中旧 Java 客户 / member / profile 相关事实
7. `team-memory/sessions/cuitiantian0704/2026-05-14-pm-cuitiantian-pre-capability-startup.md`
8. `team-memory/sessions/cuitiantian0704/2026-05-14-team-memory-capture-install.md`

## 4. 首轮盘问问题

崔田恬不应直接生成最终文档。先按“一次一问”逼清以下问题：

1. 客户主体到底是“自然人”还是“客户-门店关系”？
2. 首版最小可识别字段是什么：手机号、姓名、门店、来源、同意记录是否必需？
3. 员工代客创建客户时，哪些字段可以缺省，哪些字段必须由 GUI Confirm 补齐？
4. AI Draft 识别到新客户时，是创建正式客户，还是只生成客户候选？
5. 一个手机号对应多门店客户关系时，是否允许多个 customer profile？
6. 重复客户识别只提示，还是允许合并？合并是否是 key_action？
7. 客户停用后，历史 booking、audit evidence 和统计口径如何保留？
8. 客户备注、偏好、过敏、禁忌等敏感信息是否进入首版？
9. `#94` 中客户资产、权益、店铺主身份、分销身份哪些只作为 Contract Gap，不进入首版？
10. 客户资料变化何时触发 HK.Consent / HK.Audit / Gateway / reason_code？

## 5. SDD 厘清决策树模式

本包启动复用邹骢 booking 主线的方法，按 SDD（Spec-Driven Development / 规格驱动开发）的 PM 前置阶段执行：先做 Specification-Driven Discovery（规格驱动厘清），再产出可审查的 Cap-Spec。

### 5.1 复用规范

来自邹骢 booking 的可复用方法：

1. **一次只问一个问题**：每个问题都说明为什么重要、选错的后果、推荐选项。
2. **问题编号持续递增**：建议使用 `CP-Q001`、`CP-Q002`，不要删除旧问题。
3. **修订不删除**：如果后续答案推翻前序答案，在旧问题下标注“被 CP-Qxxx 修订 / 取代”。
4. **四类归档**：每轮沉淀必须区分 Facts（事实）、Assumptions（假设）、Judgments（PM 当前判断）、Open Questions（待 Founder / Gate 确认）。
5. **缺口不补答案**：凡涉及 registry、reason_code、OpenAPI、facts、events、HK 触发点的未落位事项，只进 Contract Gap。
6. **过程不等于真源**：决策树和问答过程只用于起草 Cap-Spec，不替代 `hl-contracts` 或 Founder / Gate 裁决。
7. **先最小可审查 PR**：目标不是一次写完美，而是形成 Founder 可以逐段评论的 Draft PR。

### 5.2 决策树主干

`biz.customer.profile` 的厘清决策树按 7 条主干推进。每条主干必须先问关键分叉，再落 Cap-Spec。

| 主干 | 决策目标 | 典型问题 | 产出位置 |
|---|---|---|---|
| A. 主体模型 | 定义客户主体与客户-门店关系 | 客户是自然人、门店客户关系，还是二者分层？ | Cap-Spec-1 / Contract Gap |
| B. 创建路径 | 定义正式客户、候选客户、散客客户 | AI Draft 能否创建正式客户？员工代建需要哪些字段？ | Cap-Spec-1 / Acceptance |
| C. 识别与去重 | 定义手机号、姓名、门店、来源的识别规则 | 一个手机号多门店是否多 profile？重复客户如何提示？ | Cap-Spec-1 / Contract Gap |
| D. 合并与停用 | 定义 merge / disable 的业务语义 | 合并是否改写历史 booking？停用后能否新建预约？ | Cap-Spec-1 / Reason-Codes |
| E. Booking 引用 | 定义客户档案与 booking 的连接方式 | booking draft / confirmed booking 持有 customer_id 还是快照？ | Cap-Spec-1 / Acceptance |
| F. 敏感与同意 | 定义联系方式、备注、偏好、禁忌的治理边界 | 哪些字段需要 HK.Consent？哪些字段需要权限拒绝？ | Contract Gap / Reason-Codes |
| G. Legacy 输入 | 定义旧 Java / PHP 事实的继承边界 | `client-user`、资产、店铺主、分销身份哪些不进首版？ | Contract Gap |

### 5.3 单个问题模板

每个问题按以下模板记录：

```markdown
### CP-Q001

问题：客户主体到底是“自然人”还是“客户-门店关系”？

为什么重要：
- 决定 `customer_id`、门店客户关系、booking 引用和历史快照的边界。

如果选错：
- 可能导致一个客户跨门店数据被错误合并，或同一自然人在不同门店的服务历史被错误拆散。

候选答案：
- A. 以自然人为主对象，门店关系作为从属关系。
- B. 以客户-门店关系为主对象，自然人只做可选归并线索。
- C. 分层：全局自然人主体 + 门店客户关系，首版只定义门店客户关系。

推荐：
- C。更贴近 booking 首切片，也能避免过早承诺跨门店统一客户。

PM 回答：
- 待崔田恬确认。

归类：
- Facts:
- Assumptions:
- Judgments:
- Open Questions:

影响：
- Cap-Spec-1:
- Acceptance:
- Reason-Codes:
- Contract Gap:
```

### 5.4 SDD 阶段门

| 阶段 | 名称 | 目标 | 退出条件 |
|---|---|---|---|
| S0 | Source Alignment | 读取上游和当前主线 | Codex 能复述范围、非范围、禁止事项 |
| S1 | Decision Tree Clarification | 一次一问厘清关键分叉 | 7 条主干均有最小答案或 Open Question |
| S2 | Classification | 把问答归为 Facts / Assumptions / Judgments / Open Questions | 没有把假设写成事实 |
| S3 | Spec Drafting | 生成四件套 DRAFT | 文件均写明 DRAFT / 非工程开工 |
| S4 | Gap Hardening | 收敛 Contract Gap | 未落位契约均进入 gap，不补成答案 |
| S5 | Review Intake | 准备 PR 和 Issue 回填 | Founder / Gate 可逐段评论 |

### 5.5 决策树首批问题

正式启动时，先不要一次性问完全部问题。Codex 应按依赖顺序推进：

1. CP-Q001：客户主体是自然人、门店客户关系，还是分层模型？
2. CP-Q002：首版客户创建的最小字段是什么？
3. CP-Q003：散客客户是否允许无手机号，但必须有系统内 customer_id？
4. CP-Q004：AI Draft 识别到新客时，是正式创建、候选创建，还是提示人工确认？
5. CP-Q005：客户资料补全是否是 key_action？
6. CP-Q006：手机号补录后如何处理潜在重复客户？
7. CP-Q007：客户合并是否保留历史 booking 原 customer_id？
8. CP-Q008：客户停用后，历史预约和审计如何查询？
9. CP-Q009：客户敏感备注 / 偏好 / 禁忌是否进入首版？
10. CP-Q010：旧 Java 客户资产、权益、店铺主、分销身份如何从首版排除？

### 5.6 PM 心智：这不是模块，也不是传统 PRD

崔田恬启动本包时，首先要切换心智：

```text
能力包不是系统模块。
能力包不是传统大 PRD。
能力包是一个用户价值流闭环的可审查规格切片。
```

`biz.customer.profile` 不是要一次性交付一个“客户模块”，也不是把客户管理页面、字段、接口、数据库、权限、资产、会员全写成一个大需求。它只回答首版价值流里最关键的问题：

```text
用户/员工要完成预约时，系统如何可靠地知道“这个客户是谁”，
如何创建或引用客户，
如何在 booking draft / confirmed booking 中留下可审计证据，
以及哪些内容必须先停在 Contract Gap，不能伪装成已确认契约。
```

判断一个内容能不能进入首版，不看“它是不是客户模块的一部分”，而看它是否直接服务这条闭环：

```text
预约意图出现
→ 识别或候选创建客户
→ 人工确认必要信息
→ booking draft 引用客户
→ confirmed booking 保留客户快照
→ 客户资料变化可审计
→ 未确认的资产 / 会员 / 权益 / 店铺主信息进入 Contract Gap
```

### 5.7 三种错误工作方式

| 错误方式 | 表现 | 为什么不适合本包 | 正确方式 |
|---|---|---|---|
| 模块思维 | 先列“客户管理模块”页面、字段、菜单、接口 | 容易把资产、会员、营销、店铺主全部塞进来 | 从预约价值流反推客户档案必须承担的最小责任 |
| 传统 PRD 思维 | 写完整需求背景、功能列表、交互说明、全部字段 | 容易形成一个不可审查的大需求 | 用 CP-Q001... 决策树逐个厘清关键分叉 |
| 大需求交付思维 | 想一次性定义客户全生命周期 | 会阻塞首版，也会越过 Founder / Gate 裁决 | 只交付可审查的 DRAFT 四件套和 Contract Gap |

### 5.8 价值流闭环检查法

每当 Codex 或 PM 想往文档里加入一段内容，先问 5 个问题：

1. 这段内容是否服务“谁来预约”的识别、创建、引用或审计？
2. 它是否影响 booking draft / confirmed booking 对客户的引用？
3. 它是否只是资产、会员、权益、营销、店铺主、分销身份的后续问题？
4. 如果现在不确认，会不会影响首版客户档案进入 Draft PR？
5. 它是 PM 当前判断，还是需要 Founder / Gate 裁决的 Contract Gap？

处理规则：

| 判断结果 | 放置位置 |
|---|---|
| 直接服务首版预约价值流闭环 | Cap-Spec-1 / Acceptance |
| 是拒绝、缺字段、权限、合并、停用等业务结果 | Reason-Codes DRAFT 提案 |
| 需要正式契约、registry、OpenAPI、facts、events、HK 触发点 | Contract Gap |
| 属于资产、会员、权益、店铺主、营销、分销 | Contract Gap 或后续候选能力包，不进首版 |
| 只是页面或字段细节，但不影响价值流 | 暂缓，不写成首版必交付 |

### 5.9 轻量上手流程

崔田恬第一次启动时，不需要先写完整文档。按下面顺序走即可：

1. 先用 Prompt 0 对齐边界，确认 Codex 没把本包当“客户模块”。
2. 用 Prompt 1 从 CP-Q001 开始，一次只回答一个问题。
3. 每回答 3-5 个问题，就让 Codex 做一次 Facts / Assumptions / Judgments / Open Questions 归类。
4. 如果某个问题答不出来，不要卡住整包；按 Prompt 9 回填“卡点 / 请求协助”，再把该项放入 Contract Gap。
5. 七条主干都有最小答案或 Open Question 后，再生成四件套 Draft。
6. Draft PR 只求可审查，不求一次性完美；Founder / Gate 能逐段评论就是合格的第一版。

### 5.10 产品背景：运行态、智能态与自然交互优先

崔田恬做 `biz.customer.profile` 时，必须先理解唤龙新系统的基本产品背景：

```text
唤龙不是以 GUI 后台为默认入口的新 SaaS。
唤龙的新系统优先从自然交互进入，由智能态理解意图、生成候选；
再由运行态完成治理裁决、正式写入和审计存证。
GUI 不是默认起点，而是确认、主动操作、降级、治理和审计界面。
```

#### 5.10.1 三态分工

| 态 | 主要职责 | 对 PM 的影响 |
|---|---|---|
| 运行态 Runtime Plane | 业务请求进入后，经过 Gateway / Protocol Gate、HK Kernel、能力包执行、HK.Audit 审计 | `customer profile` 里的正式客户、正式 booking 引用、key_action、event_id、reason_code 都必须服从运行态 |
| 智能态 Intelligence Plane | AI 理解意图、自然交互、交互路由、智能辅助、候选生成 | AI 可以识别客户意图、生成客户候选或预约草稿，但不能替用户确认正式业务事实 |
| 数据态 Data Plane | 事务数据沉淀、CDC/ETL、分析与洞察 | 不属于本包首版主线；客户分析、分群、会员资产等不得提前塞进首版 |

硬规则：智能态可以提出建议、生成候选、辅助审计，但最终治理裁决权属于运行态的 HK Kernel / Gateway 机制。任何 AI 输出转成正式动作前，都必须经过 Can → Action → Audit。

#### 5.10.2 自然交互优先，不是 GUI 优先

`R-002 NUI 优先原则` 已锁定：自然交互（NUI）是 Agent 的入口层，是首选交互模式。GUI 的角色是：

- Agent 不可用时的兜底。
- 强审计和确认环节。
- 用户主动进入的控制面板。
- 治理控制台和可追溯操作界面。

因此，崔田恬不要把 `biz.customer.profile` 设计成“客户管理后台先有一套页面，然后业务围绕页面运行”。正确理解是：

```text
用户通过语音 / LUI / 咨询室交谈表达预约或服务意图
→ 智能态识别“这个客户可能是谁”
→ 生成客户候选 / 预约草稿
→ 必要时弹出 GUI 草稿做人工确认
→ 运行态完成正式客户引用、booking 写入和审计证据
```

#### 5.10.3 运行态架构对本包的约束

Gateway + Protocol Gate 是运行态交互接入面的统一入口。所有 NUI + GUI 请求都必须经过 Gateway：

- Gateway 负责路由、上下文注入和 Protocol Gate 校验，不写业务逻辑。
- Protocol Gate 校验 trace_id、Resolve、跨租户裁决、event_id、reason_code 等铁律。
- HK Kernel 负责身份、组织链、策略、授权、审计和原因码等治理能力。
- HK.Audit 是全量证据仓库，为 key_action 签发 event_id，并用 trace_id 串联完整链路。

对 `biz.customer.profile` 的直接影响：

| 事项 | PM 该怎么写 |
|---|---|
| AI 识别到新客户 | 写成客户候选或待确认创建，不写成自动创建正式客户 |
| 客户资料正式创建 / 合并 / 停用 | 作为可能的 key_action / reason_code / audit gap 进入规格或 Contract Gap |
| booking draft 引用客户 | 说明引用客户候选、已有客户、客户快照的业务语义，不定义 booking 状态机 |
| confirmed booking 客户快照 | 需要说明正式预约确认时客户信息如何被快照化、如何追溯 |
| 客户敏感资料与同意 | 不补猜 HK.Consent 触发点，先列 Contract Gap |
| 旧系统客户 / 会员 / 资产字段 | 只作为历史输入，不当作新系统 SSOT |

#### 5.10.4 智能态规划对本包的启发

新美业 AI P0 规划给出了同一类产品哲学：AI 作为经营助理，负责把模糊输入变成结构化建议、清单和草稿；系统不自动执行交易、调度、打款、改价、改库存等动作，用户必须人工复核和确认。

迁移到 `biz.customer.profile`：

- AI 可以帮助识别“疑似新客户 / 可能重复客户 / 信息不足”。
- AI 可以把自然语言中的客户、时间、门店、服务意图整理成候选字段。
- AI 可以追问缺失信息，例如手机号、门店关系、客户同意、是否散客。
- AI 不能替用户确认客户合并、停用、正式预约或敏感资料写入。
- AI 输出必须保留为草稿、候选或建议，直到运行态完成确认和审计。

#### 5.10.5 崔田恬写 Customer Profile 时的正确落点

本包不是“客户资料页面”，而是自然交互预约闭环里“谁来预约”的运行态承接能力：

```text
自然交互意图
→ AI Draft / 客户候选
→ 人工确认必要客户信息
→ booking draft 引用客户
→ confirmed booking 保留客户快照
→ 客户资料变化、合并、停用留下审计证据
```

首版必须优先回答：

1. AI Draft 里识别到的“客户”是什么级别：自然人、门店客户关系，还是客户候选？
2. 信息不足时，什么情况下只允许生成客户候选，不能生成正式客户？
3. 什么时候必须弹出 GUI Confirm？
4. booking draft 引用的是客户候选、正式客户 ID，还是客户快照？
5. confirmed booking 形成时，客户信息如何留下可审计证据？
6. 客户资料合并、停用、敏感备注、手机号补录，哪些进入首版，哪些进入 Contract Gap？

判断标准：凡是不能直接服务“自然交互预约 → 客户识别/确认 → booking 引用 → 审计证据”这条闭环的内容，先不要写进首版。

## 6. 交付四件套

正式启动后，建议在 `hl-contracts` 创建分支：

```text
pm/cuitiantian-customer-profile-cap-spec-v01
```

建议文件：

1. `prd/biz/Cap-Spec-Biz.CustomerProfile.v0.1.md`
2. `prd/biz/Cap-Spec-Biz.CustomerProfile.Acceptance.v0.1.md`
3. `prd/biz/Cap-Spec-Biz.CustomerProfile.Reason-Codes.v0.1.md`
4. `prd/biz/CONTRACT-GAP-Biz.CustomerProfile.v0.1.md`

PR 标题建议：

```text
[PM-3] biz.customer.profile Cap-Spec v0.1
```

PR 描述必须写清：

- 本 PR 是 DRAFT Cap-Spec，不是最终契约。
- 本 PR 不授权工程开工。
- 本 PR 不注册 reason_code / OpenAPI / event / facts / registry。
- 如本包从 PM-2 改派给崔田恬，必须引用 Founder 显式确认的 Issue / comment。
- `#94` 旧系统事实只作为历史输入，不是 SSOT。

## 7. 验收场景最低覆盖

Cap-Spec-2 至少覆盖：

1. 员工代客创建最小客户档案。
2. 用户自助确认客户资料。
3. AI Draft 识别到疑似新客户，只生成候选而非正式客户。
4. booking draft 引用已有客户。
5. confirmed booking 形成后保留客户快照。
6. 客户手机号重复，系统提示潜在重复客户。
7. 人工合并重复客户，保留审计证据。
8. 客户停用后，不允许创建新的正式预约。
9. 客户资料更新触发审计记录。
10. 客户敏感备注缺少同意或权限时被拒绝。
11. 旧 Java customer/member 字段出现，但未进入新契约，记录为 Contract Gap。
12. 店铺主 / 会员资产字段出现，明确转入后续营销 / 资产能力包候选。

## 8. Contract Gap 最少应列

- 客户主体 ID 与 HK.ID / 业务 customer_id 的边界。
- 客户-门店关系是否作为首版主对象。
- 客户联系方式、同意记录与 HK.Consent 的触发点。
- 重复客户识别与 merge 的正式 key_action 归属。
- 客户资料快照与 booking 快照的边界。
- 客户资产、权益、会员、店铺主、分销身份的后续能力包归属。
- 旧 Java `client-user` / `user-asset` / flow customer 引用的迁移口径。
- 敏感客户备注、偏好、禁忌信息是否进入首版。
- 客户删除、停用、匿名化、历史审计保留之间的边界。

## 9. Codex 启动提示词包

以下提示词可直接给崔田恬复制使用。使用原则与邹骢 booking 一致：按顺序执行，不跳步；每一步只做当前任务；缺口标待确认，不让 AI 猜。

### 使用前先读：本包的工作方式

崔田恬使用 Codex 时，要先把任务说成“价值流闭环厘清”，不要说成“写客户模块 PRD”。

推荐口径：

```text
这不是客户模块，不是传统 PRD，也不是一个大需求交付。
这是 biz.customer.profile 对“谁来预约”这条用户价值流闭环的 PM Cap-Spec Draft。

请只围绕预约价值流中客户识别、客户候选创建、人工确认、booking 引用、confirmed booking 快照、客户资料变化审计来厘清。
资产、会员、权益、店铺主、营销、分销身份全部先排除，必要时写入 Contract Gap。
```

### Prompt 0：启动与边界锁定

```text
我是崔田恬，准备承接唤龙平台能力包 biz.customer.profile。

当前任务采用 SDD（Spec-Driven Development / 规格驱动开发）模式。PM 阶段先执行 Specification-Driven Discovery（规格驱动厘清）：用厘清决策树把客户档案的业务语义问清楚，再生成 Cap-Spec 四件套 Draft。

请先锁定工作心智：
- 这不是“客户模块”建设。
- 这不是传统 PRD。
- 这不是一个大需求交付。
- 这是围绕“谁来预约”的用户价值流闭环做 PM Cap-Spec Draft。
- 判断内容能否进入首版时，只看它是否服务客户识别、候选创建、人工确认、booking 引用、confirmed booking 快照和审计闭环。

请先读取并对齐以下真源和上下文：
1. hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md
2. hl-dispatch/deliverables/decisions/PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS-v0.1.md
3. hl-dispatch/deliverables/decisions/PRD-REDEFINITION-SPEC.md
4. hl-dispatch/deliverables/tasks/PM-CUITIANTIAN-CUSTOMER-PROFILE-CAPABILITY-TASKBOOK-2026-05-15-v0.1.md
5. hl-dispatch#40 中 booking 主线当前状态
6. hl-dispatch#98/#99 中工程接入矩阵与禁止开工口径
7. hl-dispatch#94 中旧 Java 客户 / member / profile 事实

当前边界：
- 只处理 biz.customer.profile。
- 不进入 biz.booking.fulfillment 的 booking 状态机、hold、confirm、arrival、fulfillment。
- 不进入 biz.store.resource 或 biz.offer.catalog。
- 不进入客户资产、会员、权益、店铺主、分销身份。
- 不写代码。
- 不注册 reason_code / OpenAPI / facts / events / registry。
- 不让工程师开工。
- 不把旧 Java / PHP 事实当新系统 SSOT。
- 不确定内容统一标记为“待 Founder / Gate 确认”。

请先输出：
1. 你读取到的正式上游事实。
2. biz.customer.profile 的范围和非范围。
3. 你如何理解“这不是模块 / 不是传统 PRD / 不是大需求，而是用户价值流闭环”。
4. 你准备采用的 SDD 决策树主干。
5. 你发现的缺失信息。

不要开始写 Cap-Spec 文件，先等我确认。
```

### Prompt 1：建立厘清决策树

```text
请先建立 biz.customer.profile 的厘清决策树，不要直接写最终规格。

要求：
- 一次只问我一个问题。
- 每个问题必须包含：为什么重要、如果选错会造成什么后果、候选答案 A/B/C、你的推荐、需要我确认的点。
- 问题编号使用 CP-Q001、CP-Q002 递增。
- 如果后续问题修订前序答案，不删除旧答案，只标注“被 CP-Qxxx 修订 / 取代”。
- 每轮回答后，把内容归类为 Facts / Assumptions / Judgments / Open Questions。

先从 CP-Q001 开始：客户主体到底是自然人、客户-门店关系，还是分层模型？
```

### Prompt 2：问答归类，不新增推演

```text
请根据目前 CP-Q001 到 CP-Qxxx 的回答，只做提取和归类，不新增推演。

请按以下四类整理：
1. Facts（已明确事实）
2. Assumptions（仍是前提或假设）
3. Judgments（PM 当前判断）
4. Open Questions（待 Founder / Gate 确认问题）

重点覆盖：
- 客户主体模型
- 客户创建路径
- 散客客户
- 手机号补录
- 重复客户识别
- 客户合并
- 客户停用
- booking draft / confirmed booking 引用客户
- 客户敏感字段与同意
- 旧 Java / PHP 历史事实排除边界

输出时禁止把 Assumptions 或 Judgments 写成正式契约。
```

### Prompt 3：生成 Cap-Spec-1 草稿

```text
现在请基于 Facts / Assumptions / Judgments / Open Questions，生成 DRAFT 草稿：

prd/biz/Cap-Spec-Biz.CustomerProfile.v0.1.md

要求：
- 状态必须是 DRAFT。
- 明确写“当前不写代码，不作为工程开工输入”。
- 只覆盖 biz.customer.profile。
- 不覆盖 booking 状态机、hold、confirm、fulfillment。
- 不覆盖客户资产、会员、权益、店铺主、分销身份。
- 所有不确定内容必须标记为“待 Founder / Gate 确认”。
- 不复制 Tier 1 SSOT 内容，只引用路径。

文档结构必须包含：
1. 草案声明
2. 上游引用
3. 一句话定义
4. 目标与非目标
5. 核心业务对象
6. 客户主体模型
7. 客户创建路径
8. 散客客户与手机号补录
9. 重复客户识别与合并
10. 客户停用与历史审计
11. 与 booking 的引用关系
12. key_action / reason_code 提案范围
13. Contract Gap 摘要
14. 待确认问题

先生成完整草稿，然后自查：
- 有没有把假设写成事实？
- 有没有越过 customer profile 进入 booking / asset / marketing？
- 有没有写成工程实现？
- 有没有遗漏待确认问题？
```

### Prompt 4：生成 Contract Gap

```text
请生成 DRAFT 草稿：

prd/biz/CONTRACT-GAP-Biz.CustomerProfile.v0.1.md

目标：列出 biz.customer.profile 进入后续契约 / 工程前仍缺少的契约定义或裁决。

每条缺口使用表格：

| 缺口 | 当前依据 | 当前判断 | 影响 | 建议处理 | 需要谁确认 | 优先级 |
|---|---|---|---|---|---|---|

至少检查：
- customer_id 与 HK.ID / identity subject 的边界
- 客户-门店关系是否作为首版主对象
- 散客客户是否允许无手机号但必须有系统内 ID
- 手机号补录与 HK.Consent 的关系
- 客户合并是否是 key_action
- 合并后历史 booking 是否保留原 customer_id
- confirmed booking 是否保存客户快照
- 客户敏感备注 / 偏好 / 禁忌是否进入首版
- 客户资产、会员、权益、店铺主、分销身份的后续归属
- 旧 Java `client-user` / `user-asset` / flow customer 引用的迁移口径

不要把缺口补成最终答案。缺口就是缺口。
```

### Prompt 5：生成 Cap-Spec-2 验收场景

```text
请生成 DRAFT 草稿：

prd/biz/Cap-Spec-Biz.CustomerProfile.Acceptance.v0.1.md

要求：
- 只写业务验收场景，不写代码测试。
- 每条场景包含：前置条件、操作步骤、预期结果、涉及 key_action、涉及 reason_code、是否需要审计证据、待确认项。
- 对不确定的 reason_code 或 key_action，标记“待 Founder / Gate 确认”。

至少覆盖：
1. 员工代客创建最小客户档案。
2. AI Draft 识别到新客，只生成客户候选或待确认创建。
3. 散客客户无手机号但生成系统内 customer_id。
4. 客户补录手机号。
5. booking draft 引用已有客户。
6. confirmed booking 保留客户快照。
7. 手机号重复触发潜在重复客户提示。
8. 人工合并重复客户，历史 booking 不被改写。
9. 客户停用后禁止创建新的正式预约。
10. 敏感备注缺少权限或同意时被拒绝。
11. 旧 Java customer/member 字段只进入 Contract Gap。
12. 店铺主 / 会员资产 / 权益字段被排除出首版。
```

### Prompt 6：生成 Cap-Spec-3 reason_code 提案

```text
请生成 DRAFT 草稿：

prd/biz/Cap-Spec-Biz.CustomerProfile.Reason-Codes.v0.1.md

要求：
- 这是 reason_code 提案，不是最终注册。
- 所有 code 都必须标记为 DRAFT / 待 Gate 确认。
- 不要声称已经写入 reasoncodes.csv。
- 成功路径默认不强制 reason_code，除非 Gate 后续裁决。

表格格式：

| reason_code | 场景 | 触发方 | 关联动作 | 是否 key_action | 审计要求 | 备注 |
|---|---|---|---|---|---|---|

请覆盖：
- customer.create 缺少最小字段
- customer.create 未授权
- customer.update 缺少同意或权限
- customer.merge 存在冲突
- customer.disable 被 booking 依赖阻断
- customer.lookup 命中多个候选
- sensitive_note.write denied
```

### Prompt 7：提交前自查与 PR 说明

```text
请做一次提交前自查。

检查清单：
1. 是否只覆盖 biz.customer.profile？
2. 是否明确 DRAFT 状态？
3. 是否明确当前不写代码、不作为工程开工输入？
4. 是否把 Facts / Assumptions / Judgments / Open Questions 区分开？
5. 是否没有复制 Tier 1 SSOT，只引用路径？
6. 是否没有把 reason_code 冒充为已注册？
7. 是否列出了 Contract Gap？
8. 是否排除了客户资产、会员、权益、店铺主、分销身份？
9. 是否没有改写 booking 状态机、hold、confirm、fulfillment？
10. Founder 是否可以逐段评论？

如果有不合格，先修改文件。

然后准备 Draft PR：
- 仓库：huanlongAI/hl-contracts
- 分支名：pm/cuitiantian-customer-profile-cap-spec-v01
- PR 标题：[PM-3] biz.customer.profile Cap-Spec v0.1
- PR body 必须包含：
  1. 本 PR 只覆盖 biz.customer.profile。
  2. 当前全部为 DRAFT。
  3. 当前不写代码，不让工程开工。
  4. 已提交哪些文件。
  5. 需要 Founder / Gate 确认的问题。
  6. 关联任务 Issue。
  7. 如果本包从 PM-2 改派给崔田恬，引用 Founder 显式确认链接。

最后回到任务 Issue 评论 PR 链接、commit、checks 和边界确认。
```

### Prompt 8：信息不足时

```text
不要补猜。请输出“缺失信息清单”：

| 缺失信息 | 影响哪个文件 | 如果不确认会造成什么风险 | 建议问谁 | 建议暂存位置 |
|---|---|---|---|---|

然后基于已有信息继续生成 DRAFT，并把缺失处标记为“待 Founder / Gate 确认”或写入 Contract Gap。
```

### Prompt 9：遇到卡点时请求协助

```text
我在 biz.customer.profile 的 SDD 厘清中遇到卡点。

请不要继续猜答案，也不要扩大成完整客户模块。

请帮我整理一份 GitHub Issue / PR 回填评论，格式如下：

## biz.customer.profile 卡点回填

当前阶段：
- S0 Source Alignment / S1 Decision Tree / S2 Classification / S3 Spec Drafting / S4 Gap Hardening / S5 Review Intake

卡点问题：
- CP-Qxxx：

为什么卡住：
-

这影响的价值流闭环：
- 客户识别 / 候选创建 / 人工确认 / booking draft 引用 / confirmed booking 快照 / 审计证据 / Contract Gap

我当前能确认的事实：
-

我的当前判断：
-

我不确定、需要协助的点：
-

建议请求谁协助：
- PM / Founder / Gate / CTO / 相关能力包 owner

建议暂存位置：
- Cap-Spec DRAFT / Acceptance DRAFT / Reason-Codes DRAFT / Contract Gap / GitHub Issue comment

下一步最小动作：
-

要求：
- 不要把未确认内容写成事实。
- 不要把卡点扩成大需求。
- 能继续写 Draft 的部分继续写，不能确认的部分进入 Contract Gap。
```

### Prompt 10：Codex 跑偏时纠偏

```text
你刚才的输出有跑偏风险。

请按以下规则重写：
1. 不要把 biz.customer.profile 写成“客户模块”。
2. 不要写传统 PRD 的完整功能清单。
3. 不要把资产、会员、权益、店铺主、营销、分销身份放进首版。
4. 不要写工程实现、接口、数据库或 reason_code 注册。
5. 只围绕“谁来预约”的用户价值流闭环：客户识别、候选创建、人工确认、booking 引用、confirmed booking 快照、客户资料变化审计。
6. 不确定内容写入 Contract Gap，不要补猜。

请先说明你上一版哪里跑偏，再给出修正后的最小版本。
```

## 10. 建议 dispatch 节奏

### D0：Founder 分工确认

目标：确认 `biz.customer.profile` 是否正式由崔田恬承接。

当前状态：

- 已完成：`hl-dispatch#109` 已接受崔田恬 owner confirmation，`confirmation_state=confirmed`。
- 待解除：本 taskbook 需要进入 `hl-dispatch main`。#109 正文及评论不得替代正式 taskbook 真源。

回填要求：

- Founder 确认 comment / Issue 链接。
- 是否改派 PM-2 原职责。
- 是否允许崔田恬在 `hl-contracts/prd/biz/` 提 PR。

### D1：启动回填

崔田恬在任务 Issue 回填：

```markdown
## 崔田恬启动回填：biz.customer.profile

状态：READY / BLOCKED

我已读取：
- 上游任务书：
- #40 booking 主线：
- #98/#99 工程接入矩阵：
- #94 旧 Java 客户事实：

我理解的本包范围：
-

我理解的本包非范围：
-

我理解的工作方式：
- 这不是客户模块，不是传统 PRD，也不是一个大需求交付。
- 这是围绕“谁来预约”的用户价值流闭环做 PM Cap-Spec Draft。
- 我会用 CP-Q001... 决策树一次一问，把客户识别、候选创建、人工确认、booking 引用、confirmed booking 快照和审计闭环厘清。
- 我不会把资产、会员、权益、店铺主、营销、分销身份写进首版；不确定内容进入 Contract Gap。

我最先需要 Founder / Gate 确认的 3 个问题：
1.
2.
3.

下一步：
-
```

### D2：四件套 Draft PR

目标：创建 `hl-contracts` Draft PR，并在 task Issue 回填 PR / commit / checks。

### D3：Founder / Gate 预审

目标：审查是否存在跨包污染，尤其是：

- 是否把 booking 状态机写进 customer profile。
- 是否把会员 / 资产 / 店铺主 / 营销身份写进首版。
- 是否把旧 Java / PHP 事实当新系统真源。
- 是否把 reason_code 提案写成正式注册。

### D4：分工确认 Issue 正文草案

历史草案已落地为 `hl-dispatch#109`。后续不需要重复创建分工确认 Issue，除非 Founder 要求重新裁决。

如需复用本草案创建新的 owner confirmation Issue，正文建议如下：

```markdown
## 决策主题

确认 PM 崔田恬是否正式承接 `biz.customer.profile` v0.1 Cap-Spec。

## 决策类型

流程规范 / PM 能力包分工确认

## 背景

当前首批能力包进展：

- 朱阳：`biz.offer.catalog` 已合入 DRAFT baseline；`biz.store.resource` 已进入 `hl-contracts#36` Draft PR 收尾。
- 邹骢：`biz.booking.fulfillment / booking` 仍是 `hl-contracts#30` Draft；registry、events/facts、reasoncodes、outcome classification、OpenAPI 已按 G9 step 拆分推进，`hl-contracts#43/#44` 已完成 booking OpenAPI 契约落库。
- `hl-dispatch#98` 将 `biz.customer.profile` 标为 blocked：Founder Signed 已立项，但暂无 merged baseline。
- 崔田恬已完成 `hl-dispatch#80` readiness 和 team-memory 链路准备。

原上游 `HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6` 中 `biz.customer.profile` 属于 PM-2 邹骢。若改由崔田恬承接，必须由 Founder 在 GitHub 显式确认。

## 候选方案

### 方案 A：确认崔田恬承接 `biz.customer.profile` v0.1

- 优势：补齐当前 blocked 的客户档案基线；不干扰朱阳 store.resource 收尾；邹骢可继续聚焦 booking OpenAPI 审查。
- 劣势：需要明确这是 PM 分工调整，避免和原 PM-2 范围冲突。

### 方案 B：仍由邹骢承接 `biz.customer.profile`

- 优势：保持上游 v0.6 原分工。
- 劣势：邹骢 booking 主线仍在收尾，customer profile 可能继续阻塞。

### 方案 C：暂不启动 `biz.customer.profile`

- 优势：避免分工调整。
- 劣势：booking 主链继续缺客户档案 baseline，工程接入矩阵中的 blocked 状态无法解除。

## 建议裁决

建议选择方案 A：

```text
确认 PM 崔田恬正式承接 `biz.customer.profile` v0.1。
本次只授权 PM Cap-Spec 工作，不授权工程开工。
崔田恬只产出 CustomerProfile 四件套 Draft PR。
客户资产、会员、权益、店铺主、分销身份全部列入 Contract Gap 或后续候选，不进入首版。
```

## 约束条件

- 不启动 `biz.*` runtime 编码。
- 不改写 `HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6` 的其他分工。
- 不让崔田恬介入 `biz.store.resource` 或 `biz.booking.fulfillment` 收尾。
- 不把旧 Java / PHP 事实当新系统 SSOT。
- 正式 Cap-Spec PR 必须进入 `hl-contracts/prd/biz/`，并保持 DRAFT，等待 Founder / Gate review。
```

### D5：崔田恬任务 Issue 正文草案

Founder / owner confirmation 已通过 `hl-dispatch#109` 完成；如需要从 owner confirmation issue 拆出执行任务 Issue，可使用以下正文。若不拆新 Issue，则 #109 继续作为 GitHub 流转与证据 Issue；本文件是正式 taskbook SSOT。

```markdown
## 任务名称

PM 崔田恬启动 `biz.customer.profile` v0.1 Cap-Spec

## 执行角色

PM 崔田恬（GitHub: `cuitiantian0704`）

## 优先级

P1 - 重要（3 天内完成首轮 Draft PR）

## 任务目标

采用 SDD（Spec-Driven Development / 规格驱动开发）模式，复用邹骢 booking 的厘清决策树方法，完成 `biz.customer.profile` 的 PM Cap-Spec 四件套 Draft。

本任务不是“客户模块”建设，不是传统 PRD，也不是一个大需求交付。它只围绕“谁来预约”的用户价值流闭环做可审查规格切片：客户识别、客户候选创建、人工确认、booking draft 引用、confirmed booking 客户快照、客户资料变化审计，以及未确认事项的 Contract Gap。

## 任务清单

- [ ] 读取 Founder 分工确认 Issue / comment。
- [ ] 读取 `PM-CUITIANTIAN-CUSTOMER-PROFILE-CAPABILITY-TASKBOOK-2026-05-15-v0.1.md`。
- [ ] 按 Prompt 0 完成 Source Alignment，先复述范围、非范围、价值流闭环心智和禁止事项。
- [ ] 按 Prompt 1 建立 `CP-Q001...` 厘清决策树。
- [ ] 至少完成 7 条主干的首轮问题：主体模型、创建路径、识别去重、合并停用、Booking 引用、敏感与同意、Legacy 输入。
- [ ] 按 Prompt 2 输出 Facts / Assumptions / Judgments / Open Questions。
- [ ] 遇到卡点时按 Prompt 9 回填；发现 Codex 跑偏时按 Prompt 10 纠偏。
- [ ] 创建 `hl-contracts` 分支：`pm/cuitiantian-customer-profile-cap-spec-v01`。
- [ ] 生成 `prd/biz/Cap-Spec-Biz.CustomerProfile.v0.1.md`。
- [ ] 生成 `prd/biz/Cap-Spec-Biz.CustomerProfile.Acceptance.v0.1.md`。
- [ ] 生成 `prd/biz/Cap-Spec-Biz.CustomerProfile.Reason-Codes.v0.1.md`。
- [ ] 生成 `prd/biz/CONTRACT-GAP-Biz.CustomerProfile.v0.1.md`。
- [ ] 提交 Draft PR，标题：`[PM-3] biz.customer.profile Cap-Spec v0.1`。
- [ ] 回填 PR 链接、commit、checks、当前卡点和是否仍保持 DRAFT。

## 验收标准

- Issue 中有崔田恬本人启动回填，明确 READY / BLOCKED。
- 启动回填明确说明：这不是客户模块 / 传统 PRD / 大需求交付，而是用户价值流闭环的 PM Cap-Spec Draft。
- 决策树问题使用 `CP-Q001` 起编号，并保留修订关系。
- 问答归类明确区分 Facts / Assumptions / Judgments / Open Questions。
- Draft PR 只覆盖 `biz.customer.profile`。
- PR 明确 DRAFT、非工程开工输入、不注册 reason_code / OpenAPI / facts / events / registry。
- Cap-Spec 不进入 booking 状态机、hold、confirm、arrival、fulfillment。
- Cap-Spec 不把客户资产、会员、权益、店铺主、分销身份写入首版。
- Contract Gap 至少覆盖客户 ID / HK.ID、客户-门店关系、手机号补录与同意、客户合并、booking 快照、敏感备注、legacy 输入。
- 未决问题均标注“待 Founder / Gate 确认”。

## 背景说明 / 参考文档

- `hl-dispatch/deliverables/tasks/PM-CUITIANTIAN-CUSTOMER-PROFILE-CAPABILITY-TASKBOOK-2026-05-15-v0.1.md`
- `hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md`
- `hl-dispatch/deliverables/decisions/PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS-v0.1.md`
- `hl-dispatch/deliverables/decisions/PRD-REDEFINITION-SPEC.md`
- `hl-dispatch#40`
- `hl-dispatch#94`
- `hl-dispatch#98`
- `hl-dispatch#99`

## 期望完成时间

2026-05-18

## 禁止事项

- 不写代码。
- 不授权工程开工。
- 不修改 `reasoncodes.csv`。
- 不写 OpenAPI / facts / events / registry。
- 不把旧 Java / PHP 事实当新系统 SSOT。
- 不把飞书讨论当正式证据。
```

### D6：PM 工作台通知文案

Owner confirmation 已完成、taskbook 进入 main 后，可发 PM 工作台通知：

```text
【PM 能力包启动通知】

崔田恬将承接 `biz.customer.profile` v0.1 Cap-Spec。

本任务不是“客户模块”，不是传统 PRD，也不是一个大需求交付。

它是围绕“谁来预约”的用户价值流闭环做 PM Cap-Spec Draft：客户识别、候选创建、人工确认、booking 引用、confirmed booking 快照、客户资料变化审计，以及未确认事项的 Contract Gap。

本任务采用 SDD 模式，复用邹骢 booking 的厘清决策树方法：一次一问、Facts / Assumptions / Judgments / Open Questions 四类归档、Contract Gap 不补答案。

边界：
- 只做 PM Cap-Spec 四件套 Draft。
- 不写代码，不授权工程开工。
- 不进入 booking 状态机 / hold / confirm / fulfillment。
- 客户资产、会员、权益、店铺主、分销身份不进入首版。

正式执行与证据以 GitHub Issue / PR 为准，飞书只做提醒。

任务 Issue：`hl-dispatch#109`
规划 taskbook：`hl-dispatch/deliverables/tasks/PM-CUITIANTIAN-CUSTOMER-PROFILE-CAPABILITY-TASKBOOK-2026-05-15-v0.1.md`
```

## 11. 当前禁止事项

- 不启动 `biz.*` runtime 编码。
- 不把本规划当作工程开工证明；分工确认以 `hl-dispatch#109` 为准。
- 不继续改动 `HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6` 的其他 PM 分工，除非 Founder 在 GitHub 明确确认。
- 不让崔田恬同时接 `biz.customer.profile` 与营销 / 资产 / 店铺主能力包。
- 不把 `#94` 旧系统字段直接写成新契约字段。
- 不把客户资产、会员、权益、店铺主、分销身份塞进首版客户档案。
- 不用飞书回复替代 GitHub 证据链。

## 12. 后续候选能力包

本轮只建议派 `biz.customer.profile`。以下能力包暂不建议现在派给崔田恬：

| 候选 | 处置 | 原因 |
|---|---|---|
| `biz.customer.asset` | defer | 旧 Java / 店铺主 / 权益 / 钱包事实复杂，容易污染首包 |
| `biz.marketing.invest.owner` | defer | 依赖 #96 PHP 事实，且 #96 已归档等待新 owner |
| `biz.redemption` / 核销 | defer | 与 booking、权益、第三方渠道耦合，需要先裁决对象边界 |
| `biz.payment.checkout` | defer | 支付 / 结算 / 分佣不是当前 PM 首包 |
| `biz.store.resource` | no | 已由朱阳推进 `hl-contracts#36` |
| `biz.booking.fulfillment` | no | 邹骢主线仍在 booking Draft baseline / OpenAPI 合并后审查与收尾 |

## 13. 推荐结论

本 taskbook 的推荐结论已通过 `hl-dispatch#109` owner confirmation 进入 GitHub SSOT：

```text
建议确认 PM 崔田恬正式承接 `biz.customer.profile` v0.1。

本次为 PM Cap-Spec 任务，不授权工程开工。
崔田恬只产出 CustomerProfile 四件套 Draft PR。
客户资产、会员、权益、店铺主、分销身份全部列入 Contract Gap 或后续候选，不进入首版。
```
