# Contract Gap｜biz.booking.fulfillment / booking v0.1

> 状态：DRAFT，等待 Founder / Gate 审查  
> 范围：仅 booking（预约）子段，不覆盖 fulfillment（履约）  
> 当前不写代码，不作为工程开工输入  
> 本文只列进入后续契约 / 工程前仍缺少的契约定义或裁决；缺口不是最终答案。

## 1. 上游引用

- `hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md`
- `hl-dispatch/deliverables/decisions/PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS-v0.1.md`
- `hl-dispatch/deliverables/decisions/PRD-REDEFINITION-SPEC.md`
- `hl-dispatch` Issue #40
- `hl-dispatch/deliverables/decisions/CAP-SPEC-1-biz-booking-fulfillment-booking-v0.2.md`
- `C:\Users\ROG\AI workflow\biz.booking.fulfillment\WORKING-biz.booking.fulfillment-QA-context.md`

过程文件仅作为 PM 草稿整理依据，不是真源，不替代 `hl-contracts` Tier 1 SSOT。

## 2. Contract Gap 清单

| 缺口 | 当前依据 | 当前判断 | 影响 | 建议处理 | 需要谁确认 | 优先级 |
|---|---|---|---|---|---|---|
| booking 是否先作为 `biz.booking.fulfillment` 的子交付审查 | Issue #40 最新修正任务；Cap-Spec-1 v0.2 §22 / §23 | PM 当前草稿建议先审 booking 子段，不进入 fulfillment。 | 影响 PR 范围、审查粒度、后续 fulfillment 是否另起草稿。 | 在 Issue #40 或 PR 中明确 booking 子交付审查口径。 | Founder / Gate | P0 |
| Cap-Spec 文件最终落点 | Issue #40 建议先放 `hl-dispatch/deliverables/decisions/`；PRD 重定义提到 Cap-Spec 路径可能归 `hl-contracts/prd/biz/` | PM 当前草稿先放 `hl-dispatch` 形成可审查证据链，后续是否迁移待确认。 | 影响 SSOT 层级、PR 目标仓、后续引用路径。 | 先在 `hl-dispatch` 审查；如 Gate 要求，再迁移 / 同步到 `hl-contracts` 指定目录。 | Founder / Gate | P0 |
| `biz.booking.fulfillment / booking` capability_id 是否需要独立子标识 | 上游只定义 `biz.booking.fulfillment`；Issue #40 当前聚焦 booking 子段 | PM 当前草稿使用 `biz.booking.fulfillment / booking` 表达子段，不声称有独立 capability_id。 | 影响 capability registry、路由、开关、后续 fulfillment 切分。 | Gate 确认是仅文档子段，还是需要 registry 层面的子能力标识。 | Gate | P0 |
| 状态命名是否需要 Gate 统一 | Q234-Q265；Cap-Spec-1 v0.2 §9 | PM 当前草稿提出 9 个状态：`draft`、`pending_store_confirm`、`confirmed`、`arrival_overdue`、`assignment_overdue`、`completed`、`cancelled`、`no_show`、`submit_expired`。 | 影响状态机、OpenAPI、事件、前端展示、审计事实。 | Gate 审查命名、终态 / 过程状态划分和是否需要进入正式枚举。 | Gate | P0 |
| 员工预约与客户预约是否共用同一状态机 | Q037-Q044、Q155-Q180、Q226-Q347；Cap-Spec-1 v0.2 §6 / §9 / §10 | PM 当前草稿共用同一 `booking_status` 状态机，以入口、发起方、场景字段和权限规则区分差异。 | 如果不确认，工程可能拆出多套状态，导致口径发散。 | Gate 确认共用状态机，或要求按入口拆子状态 / 子流程。 | Gate | P0 |
| 哪些动作必须成为 key_action | Q267-Q280；Cap-Spec-1 v0.2 §12 | PM 当前草稿提出 11 个 `booking_action_type`，除 `view_booking` 外，其余通常为 key_action；`create_booking` 为条件型 key_action。 | 影响 Can -> Action -> Audit、key_action registry、权限审计。 | Gate 逐项确认 action 命名、key_action 标记和 registry 落点。 | Gate | P0 |
| `create_booking` 条件型 key_action 口径 | Q216-Q225；Cap-Spec-1 v0.2 §8 / §12 | PM 当前草稿：生成草稿 / AI Draft / 业务记录时算 key_action；纯打开页面不算。 | 影响草稿审计边界，可能把浏览行为误纳入 key_action 或漏审 AI Draft。 | Gate 确认是否接受“条件型 key_action”，或要求拆分动作。 | Gate | P1 |
| Appointment Intent Hold 与 Qualified Resource Hold 的边界归属 | 上游任务书 §4 / §5；Q001-Q009；Cap-Spec-1 v0.2 §13 | PM 当前草稿：booking 定义预约侧语义和生命周期；资源可用性与长期资源主数据归资源能力。 | 影响 booking 与 `biz.store.resource` 的职责切分、hold API / event 归属。 | Gate 明确 hold 的契约 owner、事件 owner、资源事实 owner。 | Gate | P0 |
| `pending_store_confirm` 是否复用 Qualified Resource Hold TTL | Q156-Q178；Cap-Spec-1 v0.2 §11 / §13 | PM 当前草稿复用 15 分钟 TTL，最长 30 分钟；客户侧和门店端展示倒计时。 | 影响客户等待、门店确认、资源释放、submit_expired 触发。 | Gate 确认 TTL、刷新规则、超时事件和资源释放契约。 | Gate | P1 |
| `pending_store_confirm` 中门店修改后直接确认的审计契约 | Q172-Q178；Cap-Spec-1 v0.2 §11 | PM 当前草稿允许门店线下沟通后修改预约并直接确认，需记录修改前后差异、沟通说明、旧 / 新 hold 替换关系。 | 影响客户确认边界、争议追溯、审计事实字段。 | Gate 确认该动作仍归 `confirm_booking`，并定义审计 fact 必填字段。 | Gate | P1 |
| `service_flow_bound -> completed` 完成口径 | Q234-Q346；Cap-Spec-1 v0.2 §9.2 / §10 | PM 当前草稿：预约完成是到店并创建 / 绑定当天客户服务流动线容器，不等于服务履约完成。 | 影响 booking 与 fulfillment 的边界；若不确认，预约可能等待履约完成才终态。 | Founder / Gate 确认预约完成口径和服务流引用边界。 | Founder / Gate | P0 |
| 无预约服务流与 booking 首版边界 | Q056-Q063；Cap-Spec-1 v0.2 §23 标记 covered / deferred | PM 当前草稿只保留无预约到店服务流引用口径，不展开服务流模型。 | 影响是否越出 booking，是否误定义 customer.profile / fulfillment。 | Gate 确认无预约到店是否只作为 booking 关联边界，服务流模型后续另审。 | Gate | P1 |
| 客户主体 / 散客客户创建边界 | Q059-Q063；Cap-Spec-1 v0.2 §5 / §19 | PM 当前草稿：预约必须引用系统内 `customer_id`；正式客户和散客客户均可，但客户档案本体归 `biz.customer.profile`。 | 影响预约创建前置、customer_id 来源、客户合并后的历史预约查询。 | Gate 确认 booking 只引用客户 ID，不定义客户档案和合并逻辑。 | Gate | P0 |
| 冲突 / 重复预约配置与审计事实 | Q027-Q036；Cap-Spec-1 v0.2 §14 | PM 当前草稿：门店首版全店统一配置；冲突可提醒不阻断；客户自助必须确认风险；员工可代客确认；`conflict_acceptance` 并入确认审计。 | 影响资源冲突处理、客户风险提示、审计字段和门店责任边界。 | Gate 确认配置 owner、冲突审计字段、是否需要独立 reason_code / fact。 | Gate | P1 |
| 系统自动分配手艺人的规则归属 | Q104-Q115；Cap-Spec-1 v0.2 §10 / §20 / §23 | PM 当前草稿：自动分配只在已排班、可服务、无冲突手艺人中选择；高级策略后续完善。 | 影响 `assignment_overdue` 触发、排班能力边界、资源冲突治理。 | Gate 确认自动分配规则是 booking 提案还是资源 / 排班能力定义。 | Gate | P1 |
| 临时接单 / 补排班动作归属 | Q110-Q115；Cap-Spec-1 v0.2 §15 / §20 | PM 当前草稿：booking 引用补排班结果；补排班本体归门店资源 / 排班能力。 | 影响 `resolve_assignment_overdue` 的动作拆分和审计链路。 | Gate 确认补排班 contract owner 和 booking 需要保存的关联审计 ID。 | Gate | P1 |
| 预约变更是否保留主记录 / 生成版本 | Q072-Q077；Cap-Spec-1 v0.2 §15 | PM 当前草稿：改期是预约变更，保留主记录或业务编号并生成变更版本；新 hold 确认成功后释放旧资源。 | 影响版本模型、事件、审计事实、资源替换事务边界。 | Gate 确认变更版本模型和是否需要独立 command / action。 | Gate | P1 |
| 客户自助项目变更限制是否进入正式规则 | Q078-Q082；Cap-Spec-1 v0.2 §15.2 | PM 当前草稿按门店项目预约、手艺人预约、资产预约分别限制项目变更。 | 影响客户端可操作入口、支付 / 退款 / 资产释放前置。 | Founder / Gate 确认项目变更首版限制，避免工程实现过宽。 | Founder / Gate | P1 |
| 资产锁定 / 释放 / 消耗归属 | Q083-Q090；Cap-Spec-1 v0.2 §15.4 | PM 当前草稿：资产动作本体归资产能力；booking 记录调用结果和审计 ID。 | 影响预约确认、取消、no_show、变更时资产一致性。 | Gate 确认资产能力 contract owner、booking 记录字段和失败处理。 | Gate | P0 |
| 支付 / 定金确认与预约确认边界 | Q166-Q168；Cap-Spec-1 v0.2 §11 / §16 | PM 当前草稿：门店确认前只做预校验 / 预授权；确认后完成支付确认；支付失败不能转 confirmed。 | 影响支付能力边界、预约确认事务和失败回滚。 | Gate 确认支付 precheck / confirm 的契约与 booking 的依赖字段。 | Gate | P1 |
| 取消资源释放失败的 fail-secure 契约 | Q183-Q186、Q317-Q318；Cap-Spec-1 v0.2 §10 / §16 | PM 当前草稿：资源释放失败不得进入 `cancelled`、`no_show`、`submit_expired`，触发 `resolve_resource_release_failure`。 | 影响终态一致性、异常处理入口、审计事实。 | Gate 确认失败事件、重试 / 人工处理 owner、必填 reason_code。 | Gate | P0 |
| 系统取消场景边界 | Q278-Q280、Q356；Cap-Spec-1 v0.2 §16 / §18 | PM 当前草稿只把系统取消限定在闭店、歇业、关键资源不可用且无替代等不可逆场景。 | 影响系统自动动作权限、客户通知、门店补救流程。 | Founder / Gate 确认系统取消触发范围和是否需先通知门店补救。 | Founder / Gate | P1 |
| 快速预约是否正式纳入 booking v0.1 | Q129-Q154；Cap-Spec-1 v0.2 §17 | PM 当前草稿已纳入审查范围，不再只作为开放问题。 | 影响 quick_rebook 字段、验收场景、权限和入口开关。 | Founder / Gate 确认快速预约是否纳入首版，或拆到后续版本。 | Founder / Gate | P1 |
| 快速预约资产不可用转普通项目预约 | Q133-Q134；Cap-Spec-1 v0.2 §17.4 | PM 当前草稿允许提示原资产不可用，并转普通项目预约进入支付链路。 | 影响客户资产能力、支付链路和客户确认提示。 | Gate 确认该转换是否允许，以及是否需要单独 reason_code / audit fact。 | Gate | P2 |
| reason_code 是否先提案还是等待 registry 注册 | Q348-Q358；Cap-Spec-1 v0.2 §18 | PM 当前草稿列 8 个原因域和代表性枚举，只作为提案，不声称已注册。 | 影响 Cap-Spec-3、`reasoncodes.csv` PR 和工程错误分支。 | Gate 确认先以 Cap-Spec-3 提案，还是必须同步 registry PR。 | Gate | P0 |
| reason_code 三层表达契约 | Q357-Q358；Cap-Spec-1 v0.2 §18.1 | PM 当前草稿：`reason_code + reason_text + customer_visible_reason` 三层表达。 | 影响客户展示、短信模板、内部审计、统计分析。 | Gate 确认三层字段是否进入正式事实 / API 响应。 | Gate | P1 |
| 审计证据字段是否已有真源 | Q370；Cap-Spec-1 v0.2 §19 | PM 当前草稿列 `audit_correlation_id`、`last_audit_fact_id`、`audit_evidence_ref` 等字段，但未确认 Tier 1 真源。 | 影响 HK.Audit 接入、审计 fact 引用、证据链一致性。 | Gate 确认现有 HK.Audit fact / evidence 字段路径，或列为待补契约。 | Gate | P0 |
| 预约单字段模型是否作为 schema / facts / OpenAPI 输入 | Q361-Q370；Cap-Spec-1 v0.2 §19 | PM 当前草稿是业务字段模型，不是最终数据库或 API schema。 | 工程可能误把字段表当数据库表；也可能缺少正式 facts / OpenAPI。 | Gate 确认字段模型如何进入 facts / OpenAPI / event contracts。 | Gate | P0 |
| 通知场景由 booking 定义还是通知能力定义 | Q200-Q215、Q382-Q386；Cap-Spec-1 v0.2 §21 | PM 当前草稿：booking 定义通知需求、场景码、变量、跳转目标和示例；通知能力负责模板、通道、发送和补偿。 | 影响通知能力与 booking 的耦合、模板治理和点击跳转。 | Gate 确认通知契约 owner、场景码命名 owner 和实现边界。 | Gate | P1 |
| 第一期通知不做补偿机制是否可接受 | Q204-Q209；Cap-Spec-1 v0.2 §21.1 | PM 当前草稿：客户短信、内部消息、手机厂商推送均可作为一期通道，但不做通知补偿机制。 | 影响通知失败处理、审计要求和客户触达可靠性。 | Founder / Gate 确认一期通知可靠性边界。 | Founder / Gate | P1 |
| 通知详情页读取当前预约状态而非通知快照 | Q208-Q209；Cap-Spec-1 v0.2 §21.1 | PM 当前草稿：通知详情页读取当前预约最新状态。 | 影响通知详情页、争议追溯和通知快照存储需求。 | Gate 确认是否需要保存通知快照，或接受一期读取当前状态。 | Gate | P2 |
| 第三方平台预约字段与核销事实归属 | Q045-Q046；Cap-Spec-1 v0.2 §7 / §19 | PM 当前草稿：booking 保存 `intended_redemption_project` 和第三方订单引用；实际核销项目归核销 / 服务流节点。 | 影响第三方订单、券核销、服务流与预约的链路关系。 | Gate 确认第三方字段归属、核销事件 owner、预约节点不可覆盖规则。 | Gate | P1 |
| `store_visit` 仅门店预约是否可无项目完成 | Q049-Q052、Q345-Q346；Cap-Spec-1 v0.2 §6 / §9.2 | PM 当前草稿：仅门店预约到店并识别客户后可 completed，即使未开单。 | 影响到店咨询、服务流首节点和 completed 业务含义。 | Founder / Gate 确认该 completed 口径。 | Founder / Gate | P0 |
| 到店偏差类型和宽限配置 | Q244-Q250；Cap-Spec-1 v0.2 §18 / §19 | PM 当前草稿记录 `early_arrival`、`on_time_arrival`、`late_arrival`，默认前 30 后 15 为准时范围。 | 影响到店统计、arrival_overdue 触发和门店配置。 | Gate 确认宽限配置 owner 和默认值是否可进入首版。 | Gate | P2 |

## 3. 优先级说明

| 优先级 | 含义 |
|---|---|
| P0 | 进入后续契约 / 工程前必须裁决，否则会阻塞状态机、key_action、核心边界或审计。 |
| P1 | 首版强相关，建议在 Cap-Spec PR 审查中裁决；若暂未裁决，只能标为后续待处理项，不能默认实现。 |
| P2 | 可后续细化，但需要在文档中暴露，避免被误写成最终规则。 |

## 4. 当前不应做的事

- 不在本文直接注册 capability_id、key_action、reason_code。
- 不把 PM 过程文件当正式真源。
- 不把缺口补成最终答案。
- 不进入 fulfillment、客户档案、资产、支付、通知实现或门店资源主数据设计。
- 不让工程团队基于本文直接开工。
