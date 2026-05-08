# Cap-Spec-1｜biz.booking.fulfillment / booking v0.1

> 状态：DRAFT，等待 Founder / Gate 审查
> 范围：仅 booking（预约）子段，不覆盖 fulfillment（履约）
> 当前不写代码，不作为工程开工输入
> 本文是把 PM 已完成的预约阶段对话整理为 GitHub 可审查草稿，不是最终裁决，不替代 `hl-contracts` Tier 1 SSOT。

## 0. 阅读声明

本文中的业务规则、状态名、动作名、字段名、通知场景码和 reason_code 均为 PM 当前草稿判断，除明确引用的上游文件外，均待 Founder / Gate 确认。

本文只做 booking 子段可审查整理，目的在于让 Founder / Gate 能逐段评论、修正和裁决；工程团队不得据此直接开工。

本文不复制 `hl-contracts` Tier 1 SSOT 内容，只列引用路径和待补契约缺口。

## 1. 上游引用

### 1.1 正式上游

- `hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md`
- `hl-dispatch/deliverables/decisions/PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS-v0.1.md`
- `hl-dispatch/deliverables/decisions/PRD-REDEFINITION-SPEC.md`
- `hl-dispatch` Issue #40：`[任务] PM-2 邹骢启动客户与预约履约能力包 Cap-Spec`

### 1.2 Tier 1 SSOT 引用要求

后续进入正式契约或工程前，需要只引用并服从 `hl-contracts` 中与以下内容相关的真源路径：

- HK Kernel（HK.Policy / HK.Audit / HK.ID / HK.Consent）
- Gateway / Protocol Gate
- capability registry
- key_action registry
- reason_code registry
- facts / rules / OpenAPI / event contracts

具体 Tier 1 路径、注册方式和命名归属待 Gate 确认。

### 1.3 过程材料

- `C:\Users\ROG\AI workflow\biz.booking.fulfillment\WORKING-biz.booking.fulfillment-QA-context.md`

该文件仅作为 PM 过程上下文，不是真源，不自动升级为最终决定。

## 2. 能力目标

`biz.booking.fulfillment / booking` 子段的目标是把预约意图稳定转成可确认、可审计、可释放资源的正式预约事实。

首版 booking 需要覆盖客户自助预约、员工代客预约、门店主动预约、预约资源暂占、门店确认、预约取消、到店完成、逾期未到、爽约、手艺人分配与改派等预约闭环节点。

booking 子段的闭环终点是“客户到店并成功创建 / 绑定当天客户服务流动线容器”，预约单进入 `completed`。后续项目服务、资产消耗、服务履约、退款等不由预约状态承载，归后续服务流 / 履约 / 资产 / 支付等能力处理。

首版草稿需要让 Founder / Gate 审查以下内容是否可作为后续契约输入：

- 预约场景与发起方边界
- 预约状态枚举与状态流转矩阵
- 预约动作与 key_action 候选
- 资源 hold / release 规则
- reason_code 分组口径
- 预约单字段模型
- 权限、审批、客户确认与通知边界

## 3. 非目标

本草稿不覆盖以下内容：

- 不进入 fulfillment（履约）业务设计，不定义服务履约单生命周期。
- 不进入 `biz.customer.profile`，不定义客户档案、客户合并、手机号补全、客户资产主模型。
- 不定义 `biz.offer.catalog` 的服务项目主数据、服务能力词典、项目价格规则。
- 不定义 `biz.store.resource` 的长期资源主数据、排班主模型、房间 / 服务位主数据。
- 不定义支付、定金、退款、资产扣减、资产消耗规则。
- 不定义通知能力的模板、通道、发送、补偿、通知详情页实现。
- 不定义数据库表结构、API、事件、UI 交互稿或工程实现。
- 不注册正式 capability_id、key_action、reason_code 或 OpenAPI。
- 不让工程师开工。

## 4. 角色与发起方

| 角色 / 发起方 | booking 中的含义 | 当前边界 |
|---|---|---|
| 客户 | 通过客户自助端提交预约、取消预约、确认必要信息、在特定场景确认手艺人改派。 | 客户主体必须可识别。正式客户与散客客户均需有系统内 `customer_id`。待 Founder / Gate 确认。 |
| 员工 | 代客户创建、修改、取消预约，或根据线下沟通确认预约安排。 | 必须受权限、门店范围和审计约束。 |
| 店长 / 门店管理 | 门店确认、取消、分配手艺人、处理分配逾期、处理高风险异常。 | 默认具备较高预约治理权限，但具体权限模型待 Gate 确认。 |
| 排班负责人 | 处理无手艺人预约分配、分配逾期、改派。 | 具体角色名和授权方式待 Gate 确认。 |
| 手艺人 | 可主动预约自己的客户，也可能作为预约资源 / 履约责任人。 | “手艺人”是统一术语。 |
| 系统 / AI | AI 生成预约草稿；系统触发自动确认、自动分配、到店逾期、自动爽约、资源释放等。 | AI 只生成候选或草稿，不替用户确认正式业务事实。 |
| 通知能力 | 承接预约侧通知需求。 | booking 只提出通知场景和变量，不实现通知。 |

## 5. 员工预约流程

以下为 PM 当前判断，待 Founder / Gate 确认。

### 5.1 员工 / 门店主动预约类型

| 场景 | 预约语义 | 结果模式 |
|---|---|---|
| 仅门店预约 | 门店主动约客户到店咨询，不选项目、不选手艺人。 | `store_visit`，生成门店默认半小时日程。 |
| 手艺人预约 | 手艺人或门店主动预约客户，并明确项目和手艺人。 | `service_assigned`。 |
| 第三方平台项目预约 | 门店根据抖音 / 美团等第三方订单预约客户到店核销。 | 默认 `service_unassigned`；若第三方信息能匹配内部手艺人，可为 `service_assigned`。 |
| 客户剩余资产预约 | 门店主动基于客户已有资产约客户到店消耗。 | 门店发起时必须选择手艺人，生成 `service_assigned`。 |

### 5.2 员工预约主流程

1. 员工选择客户。若客户只有名称 / 称呼，需先有系统内散客客户主体。
2. 员工选择门店和预约时间。
3. 根据场景选择项目、资产、手艺人或第三方订单引用。
4. 系统判断预约模式：`store_visit`、`service_unassigned` 或 `service_assigned`。
5. 系统执行必要元素校验、资源校验和 hold 创建。
6. 员工确认提交后，门店发起类预约通常直接进入 `confirmed`。
7. 如果存在冲突但门店配置允许重复登记 / 宽松管控，员工可代客确认风险，但必须记录冲突提示、配置命中、操作人和代客确认事实。
8. 若后续取消、改派、分配、改期或异常处理，均按权限、资源和审计规则执行。

### 5.3 员工预约特殊规则

- 员工代客创建预约不强制客户本人二次确认，前提是员工有权限并记录线下沟通或代客操作事实。
- 员工端取消预约必须填写取消原因。
- 员工取消成功后需要通知客户，并保留客户可见原因和内部审计原因。
- 员工主动创建的预约，客户自助端不一定允许自行修改，具体权限待 Gate 确认。

## 6. 客户预约流程

以下为 PM 当前判断，待 Founder / Gate 确认。

### 6.1 客户自助预约类型

| 场景 | 预约语义 | 结果模式 |
|---|---|---|
| 门店项目预约 | 客户从门店支持项目列表进入，可购买并立即预约。系统推荐可做该项目且有空的手艺人，客户可确认或更换。 | 最终应为 `service_assigned`。 |
| 手艺人预约 | 客户先选手艺人，再选该手艺人可做项目和时间。 | `service_assigned`。 |
| 客户资产预约 | 客户基于已有资产预约到店消耗。客户可选手艺人，也可选择由门店安排。 | 选手艺人为 `service_assigned`；不选手艺人为 `service_unassigned`。 |

客户自助端首版不允许创建仅门店 `store_visit` 预约。

### 6.2 客户预约主流程

1. 客户进入项目、手艺人或资产预约入口。
2. 系统识别客户主体、门店、时间、项目 / 资产等必要元素。
3. 若客户未明确选择手艺人，系统可推荐可用手艺人。
4. 客户确认必要信息后执行 `submit_booking`。
5. 系统创建正式预约单编号，并执行资源校验、hold 创建、资产 / 支付预处理。
6. 若门店开启“客户预约免门店确认”，预约直接进入 `confirmed`，但需记录系统按门店配置自动确认的事实。
7. 若门店关闭“客户预约免门店确认”，预约进入 `pending_store_confirm`，门店需在 hold 有效期内确认、修改后确认或打回重新提交。
8. 门店确认后进入 `confirmed`；超时或打回后释放资源，进入 `submit_expired` 或重新提交链路。

### 6.3 客户自助改派 / 选手艺人

- 客户主动选择的手艺人包括：手艺人预约入口选择、项目预约中主动更换并确认、资产预约中主动选择。
- 客户主动选定手艺人后，后续门店改派必须客户确认。
- 系统自动推荐 / 自动匹配不等于客户主动选择。
- 客户自助端更换手艺人必须重新校验资源并创建新 hold；新 hold 未确认前，旧预约保持有效。

## 7. 状态定义

以下 9 个 `booking_status` 为 PM 当前草稿，待 Founder / Gate 确认。

| 状态 | 类型 | 定义 | 关键边界 |
|---|---|---|---|
| `draft` | 过程状态 | 被保存的预约草稿或 AI Draft，可继续编辑。 | 不占资源，不生成正式 hold，不算正式预约。 |
| `pending_store_confirm` | 过程状态 | 客户自助提交后，因门店关闭免确认开关，需要门店确认。 | 已生成正式预约单编号，可能已有短时 hold，不是草稿。 |
| `confirmed` | 过程状态 | 预约已确认，等待客户到店或等待分配等后续动作。 | GUI 可展示为“待到店”，不另设状态。 |
| `arrival_overdue` | 过程状态 | 超过预约后置到店宽限仍未成功到店 / 绑定服务流。 | 当天仍可到店并转 `completed`。 |
| `assignment_overdue` | 过程状态 | 无手艺人预约过手动分配截止，且系统自动分配失败。 | 需要门店人工处理，不自动取消。 |
| `completed` | 终态 | 客户到店并成功创建 / 绑定当天客户服务流动线容器。 | 不表示服务项目已履约完成。 |
| `cancelled` | 终态 | 预约取消且预约资源释放成功。 | 不可恢复，只能快速重新预约。 |
| `no_show` | 终态 | 预约当天结束后客户仍未到店，预约资源释放成功。 | 第二天或之后到店按无预约服务流处理。 |
| `submit_expired` | 终态 | 待门店确认超时或打回后，提交链路中断且资源释放成功。 | 不回 draft，不复用旧 hold。 |

### 7.1 终态规则

`completed`、`cancelled`、`no_show`、`submit_expired` 均不可恢复、不可覆盖、不可复用旧 hold。继续预约只能生成新草稿、新预约单和新 hold，并保留来源链路。

### 7.2 到店完成口径

`service_flow_bound` 在 booking 草稿中表示“创建 / 绑定当天客户服务流动线容器”，不等于必须创建服务履约单。该口径待 Founder / Gate 确认。

## 8. 状态流转矩阵

以下矩阵为 PM 当前草稿，待 Founder / Gate 确认。正式 Cap-Spec 后续应补齐每行的完整 reason_code、通知和审计字段。

| from_status | action_or_trigger | to_status | allowed_actor | resource_gate | failure_behavior |
|---|---|---|---|---|---|
| `draft` | `submit_booking` | `pending_store_confirm` | customer | 必要元素校验通过、资源校验通过、hold 创建成功；客户自助且门店关闭免确认。 | 保持 `draft` 或提交失败，返回原因码。 |
| `draft` | `submit_booking` | `confirmed` | customer / staff | 必要元素校验通过、资源校验通过、hold 创建成功；客户自助免确认或员工 / 门店发起。 | 保持 `draft` 或提交失败，返回原因码。 |
| `pending_store_confirm` | `confirm_booking` | `confirmed` | store_staff / store_manager | hold 有效；若门店修改资源字段，需替换 hold 成功。 | 保持 `pending_store_confirm`，返回原因码。 |
| `pending_store_confirm` | `cancel_booking` | `cancelled` | customer / staff / store_manager / system | 预约资源释放成功。 | 保持原状态并触发 `resolve_resource_release_failure`。 |
| `pending_store_confirm` | `confirm_timeout` / `store_return_for_resubmit` | `submit_expired` | system / store_staff / store_manager | 预约资源释放成功。 | 保持原状态并触发 `resolve_resource_release_failure`。 |
| `confirmed` | `arrival_success` / `service_flow_bound` | `completed` | store_staff / store_manager / system_trigger | 到店事实记录成功，服务流动线容器创建 / 绑定成功。 | 保持 `confirmed`，记录异常。 |
| `confirmed` | `cancel_booking` | `cancelled` | customer / staff / store_manager / system | 预约资源释放成功。 | 保持 `confirmed` 并触发资源释放失败处理。 |
| `confirmed` | `arrival_grace_expired` | `arrival_overdue` | system_trigger | 不释放资源，保留当天预约资源。 | 保持 `confirmed`，记录状态更新失败。 |
| `confirmed` | `assignment_deadline_expired` / `auto_assign_failed` | `assignment_overdue` | system_trigger | 不释放资源，不绑定冲突手艺人。 | 保持 `confirmed`，记录分配逾期失败。 |
| `arrival_overdue` | `arrival_success` / `service_flow_bound` | `completed` | store_staff / store_manager / system_trigger | 当天到店，服务流动线容器创建 / 绑定成功。 | 保持 `arrival_overdue`，记录异常。 |
| `arrival_overdue` | `cancel_booking` | `cancelled` | customer / staff / store_manager / system | 预约资源释放成功。 | 保持 `arrival_overdue` 并触发资源释放失败处理。 |
| `arrival_overdue` | `next_day_no_arrival` / `auto_no_show` | `no_show` | system_trigger | 预约资源释放成功。 | 保持 `arrival_overdue` 并触发资源释放失败处理。 |
| `assignment_overdue` | `assign_artisan` / `resolve_assignment_overdue` | `confirmed` | store_manager / scheduler / system_trigger | 手艺人能力、时间、冲突校验通过，绑定成功。 | 保持 `assignment_overdue`，返回原因码。 |
| `assignment_overdue` | `arrival_success` / `service_flow_bound` | `completed` | store_staff / store_manager / system_trigger | 先完成分配 / 临时接单 / 补排班治理，再绑定服务流。 | 保持 `assignment_overdue`，记录异常。 |
| `assignment_overdue` | `cancel_booking` | `cancelled` | customer / staff / store_manager / system | 预约资源释放成功。 | 保持 `assignment_overdue` 并触发资源释放失败处理。 |
| `assignment_overdue` | `arrival_grace_expired` | `arrival_overdue` | system_trigger | 不释放资源，保留当天预约资源。 | 保持 `assignment_overdue`，记录异常。 |
| terminal statuses | `quick_rebook` / `resubmit_booking` | 新草稿或新预约链路 | customer / staff | 新资源、新 hold、新预约单重新校验。 | 原终态不覆盖，新链路失败只记录失败事实。 |
| `confirmed` | `assign_artisan` | `confirmed` | store_manager / scheduler / system_trigger | service_unassigned 首次绑定手艺人成功。 | 主状态不变，记录失败原因。 |
| `confirmed` | `reassign_artisan` | `confirmed` | store_manager / scheduler / authorized_staff | 新手艺人校验通过；如需客户确认则候选安排先不生效。 | 原安排保持不变。 |
| `arrival_overdue` | `reassign_artisan` | `arrival_overdue` | store_manager / scheduler / authorized_staff | 同改派规则，保留逾期到店历史。 | 原安排保持不变。 |
| `confirmed` | `confirm_artisan_reassignment` | `confirmed` | customer | 客户确认候选改派后启用新安排并释放原资源。 | 拒绝或超时则候选失效，原安排不变。 |
| `arrival_overdue` | `confirm_artisan_reassignment` | `arrival_overdue` | customer | 同客户确认改派规则，保留逾期状态。 | 拒绝或超时则候选失效，原安排不变。 |

### 8.1 统一 fail-secure 规则

凡进入 `cancelled`、`no_show`、`submit_expired` 等需要释放预约资源的流转，如果资源释放失败，不得进入目标终态，应保持原状态并触发 `resolve_resource_release_failure`。

凡 `submit_booking`、`resubmit_booking`、`confirm_booking`、`assign_artisan`、`reassign_artisan` 等需要创建、替换或锁定资源的动作，如果资源校验失败、hold 创建失败、hold 替换失败或关键资源锁定失败，不得进入目标状态。

## 9. Key Action 表

以下 `booking_action_type` 为 PM 当前草稿，待 Founder / Gate 确认。正式 key_action 名称和注册位置待 Gate 确认。

| action_type | 适用状态 | 发起方 | 是否 key_action | 草稿说明 |
|---|---|---|---|---|
| `create_booking` | 无记录 / `draft` | customer / staff / artisan / AI | 条件是 | 只有生成草稿、AI Draft 或业务记录时才算；纯打开页面不算。 |
| `submit_booking` | `draft` | customer / staff / store_manager / artisan | 是 | 进入正式预约链路边界，生成正式预约单编号并创建 hold。 |
| `confirm_booking` | `pending_store_confirm` | store_staff / store_manager | 是 | 门店确认客户自助预约；可包含门店修改后直接确认。 |
| `resubmit_booking` | `submit_expired` 或被打回后的链路 | customer | 是 | 原提交链路中断后重新提交，生成新单和新 hold。 |
| `view_booking` | 所有状态 | customer / staff / store_manager / artisan | 否 | 查看预约详情或通知跳转，不改变业务事实。 |
| `cancel_booking` | `pending_store_confirm` / `confirmed` / `arrival_overdue` / `assignment_overdue` | customer / staff / store_manager / system | 是 | 取消正式预约，成功前必须释放预约资源。 |
| `assign_artisan` | `confirmed` / `assignment_overdue` | store_manager / scheduler / system_trigger | 是 | service_unassigned 首次分配手艺人。 |
| `reassign_artisan` | `confirmed` / `arrival_overdue` | store_manager / scheduler / authorized_staff | 是 | 已有手艺人后更换手艺人。 |
| `resolve_assignment_overdue` | `assignment_overdue` | store_manager / scheduler / authorized_staff | 是 | 处理分配逾期，可落到分配、临时接单、补排班等。 |
| `resolve_resource_release_failure` | 资源释放失败后的原状态 | store_manager / system_ops / authorized_staff | 是 | 处理资源释放失败，成功后原动作才能继续进入终态。 |
| `confirm_artisan_reassignment` | `confirmed` / `arrival_overdue` 的候选改派 | customer | 是 | 客户确认、拒绝或超时处理需要客户确认的改派。 |

## 10. 资源 Hold / Release

以下规则为 PM 当前草稿，待 Founder / Gate 确认。

### 10.1 Hold 类型

| Hold 类型 | booking 草稿含义 | 资源承诺 |
|---|---|---|
| Appointment Intent Hold | 对客户、门店、时间窗口的预约意向保留。 | 不锁具体手艺人 / 房间，可用于意向阶段。 |
| Qualified Resource Hold | 对可审计、可排程、可冲突校验的资源承诺做短时暂占。 | 支持 `store_visit`、`service_unassigned`、`service_assigned`，不一定总是具体手艺人。 |

### 10.2 TTL 与确认

- 上游任务书要求 Hold TTL 15 分钟，最长 30 分钟。
- PM 草稿判断：`pending_store_confirm` 首版复用 Qualified Resource Hold 的 15 分钟 TTL，最长 30 分钟。待 Gate 确认。
- `GUI Confirm` 发生在 Qualified Resource Hold 创建之后，确认前资源短时暂占。
- 生成正式预约前必须重新校验客户、门店、项目、资源、hold 有效性和 hold 归属。

### 10.3 Release 规则

| 场景 | release 规则 |
|---|---|
| hold 超时未确认 | 自动释放资源，用户继续时必须重新校验并创建新 hold。 |
| pending_store_confirm 超时 / 打回 | 释放原 hold，进入 `submit_expired` 或重新提交链路。 |
| 预约取消 | 预约资源释放成功后才进入 `cancelled`。 |
| 自动 no_show | 预约资源释放成功后才进入 `no_show`。 |
| 快速重新预约 / 重新提交 | 不复用旧 hold，必须创建新 hold。 |
| 改期 / 改派 / 改资源 | 新 hold 创建并确认成功后，释放旧资源并启用新资源。 |
| release 失败 | fail-secure，保持原状态，触发异常处理。 |

### 10.4 资产 / 支付边界

资产锁定、资产释放、资产消耗、支付确认、退款等动作归对应能力处理。booking 只记录引用、调用结果和审计 ID，不定义资产 / 支付本体规则。

## 11. 预约单字段模型

以下字段为 PM 当前草稿，待 Founder / Gate 确认。字段类型、唯一约束、只读规则和正式 schema 归后续契约审查。

| 字段域 | 字段 | 说明 |
|---|---|---|
| 基础身份字段 | `booking_id`、`booking_no`、`tenant_id`、`store_id`、`customer_id`、`customer_type`、`customer_display_name`、`customer_phone_masked`、`created_by_actor_type`、`created_by_actor_id`、`created_channel`、`source_channel` | 预约身份、客户、门店、创建主体和来源渠道。 |
| 预约场景字段 | `booking_intent_type`、`booking_scene`、`booking_origin`、`booking_initiator_type`、`booking_service_mode`、`is_store_visit_only`、`is_project_required`、`is_asset_required`、`is_artisan_required_at_submit`、`is_room_required_at_submit` | 表达预约类型、入口、发起方和必要元素。 |
| 预约时间字段 | `scheduled_start_at`、`scheduled_end_at`、`requested_time_text`、`duration_minutes`、`default_reception_minutes`、`arrival_grace_before_minutes`、`arrival_grace_after_minutes`、`manual_assignment_deadline_at`、`confirm_deadline_at`、`draft_expire_at` | 表达预约开始结束、自然语言时间、接待时长、到店宽限和截止时间。 |
| 资源字段 | `hold_id`、`hold_status`、`hold_expires_at`、`artisan_id`、`artisan_selection_source`、`artisan_reassignment_requires_customer_confirm`、`room_id`、`room_required`、`resource_policy_snapshot_id`、`resource_conflict_policy`、`assignment_status` | 保存预约资源事实和资源策略引用，不定义长期资源主数据。 |
| 项目 / 资产 / 支付引用字段 | `project_id`、`project_snapshot_id`、`project_intent_text`、`asset_id`、`asset_snapshot_id`、`asset_lock_id`、`asset_lock_status`、`third_party_platform`、`third_party_order_ref`、`third_party_voucher_ref`、`payment_order_id`、`deposit_required`、`payment_precheck_status` | 只保存引用和快照，不定义项目、资产、支付本体。 |
| 状态与动作字段 | `booking_status`、`booking_action_type`、`last_action_at`、`last_action_actor_type`、`last_action_actor_id`、`previous_booking_id`、`resubmitted_from_booking_id`、`quick_rebook_from_booking_id`、`version`、`is_terminal` | 保存当前状态、最近动作和链路关系。 |
| 到店与服务流字段 | `arrival_status`、`arrival_detected_at`、`arrival_detected_by`、`arrival_result`、`service_flow_id`、`service_flow_bound_at`、`service_flow_bind_status`、`service_flow_bind_failure_reason`、`completed_at`、`no_show_marked_at` | 保存到店事实、到店偏差、服务流动线容器引用和完成 / 爽约时间。 |
| 原因与说明字段 | `reason_domain`、`reason_code`、`reason_text`、`customer_visible_reason`、`failure_stage`、`failure_recoverable`、`requires_manual_resolution` | 保存最近一次失败、取消、打回、异常或终态原因摘要。完整历史进审计事实。 |
| 通知字段 | `notification_required`、`notification_scene_code`、`expected_reach_type`、`notification_jump_target`、`last_notification_request_id`、`last_notified_at`、`notification_summary` | 保存通知需求与最近通知摘要。通知实现归通知能力。 |
| 审计字段 | `audit_correlation_id`、`created_at`、`updated_at`、`submitted_at`、`confirmed_at`、`cancelled_at`、`submit_expired_at`、`terminal_at`、`last_audit_fact_id`、`audit_evidence_ref` | 保存审计摘要、关键时间点和审计事实引用，不保存完整审计日志。 |

## 12. 权限与审批规则

以下规则为 PM 当前草稿，待 Founder / Gate 确认。

每条权限规则应至少包含：`action_type`、`allowed_actor`、`status_scope`、`scene_scope`、`approval_required`、`customer_confirm_required`、`notification_required`、`audit_required`、`risk_level`。

| action_type | allowed_actor | 适用范围 | 审批 | 客户确认 | 通知 | 审计 |
|---|---|---|---|---|---|---|
| `submit_booking` | customer / staff / store_manager / artisan | 创建和正式提交预约 | 默认不审批 | 默认不需要 | 需要 | 需要 |
| `confirm_booking` | store_staff / store_manager | `pending_store_confirm` | 默认不审批 | 不需要 | 需要 | 需要 |
| `cancel_booking` | customer / staff / store_manager / system | 未到店、非终态正式预约 | 普通取消不审批；高风险可配置审批 | 不需要 | 需要 | 需要 |
| `assign_artisan` | store_manager / scheduler / system_trigger | `service_unassigned` 的 `confirmed` 或 `assignment_overdue` | 普通分配不审批；临时接单 / 补排班可配置审批或高风险审计 | 不需要 | 需要 | 需要 |
| `reassign_artisan` | store_manager / scheduler / authorized_staff | 已绑定手艺人的 `confirmed` 或 `arrival_overdue` | 高风险改派可配置审批 | 客户主动选定手艺人时需要 | 需要 | 需要 |
| `confirm_artisan_reassignment` | customer | 需要客户确认的候选改派 | 不审批 | 由客户执行确认 / 拒绝 | 需要 | 需要 |
| `resolve_assignment_overdue` | store_manager / scheduler / authorized_staff | `assignment_overdue` | 普通处理不审批；临时接单 / 补排班等可高风险审批 | 不需要 | 需要 | 需要 |
| `resolve_resource_release_failure` | store_manager / system_ops / authorized_staff | 资源释放失败异常 | 通常不审批，但高风险审计 | 不需要 | 至少通知门店或责任人 | 需要 |

### 12.1 高风险审批因素

以下因素需要在正式规则中进入 Can 判定，是否审批或拒绝待 Gate 确认：

- 临近服务开始时间。
- 客户已到店或已开始服务。
- 跨门店变更。
- 跨营业日 / 跨排班日。
- 影响手艺人班次结算。
- 员工代客修改但客户没有在线确认。
- 影响其他预约。
- 需要重新匹配资质、整房、设备或高风险资源。
- hold 过期后异常恢复。
- 命中门店或租户自定义审批规则。

## 13. 通知场景

以下通知场景为 PM 当前草稿，待 Founder / Gate 确认。booking 只定义通知需求契约，通知能力负责模板、通道、发送状态、重试和补偿。

| 场景码 | 触发点 | 接收人 | 期望触达 | 跳转目标 | 示例文案 |
|---|---|---|---|---|---|
| `booking_submitted_pending_store_confirm` | 客户提交后进入待门店确认 | 店长 / 前台 | `staff_action_required` | 待确认预约详情 | 客户张三提交了 7月22日10:25 的预约，请确认是否可安排。 |
| `booking_confirmed` | 预约进入已确认 | 客户 / 手艺人 / 门店 | `customer_important_notice` / `staff_internal_reminder` | 预约详情 | 您的预约已确认：7月22日10:25，武汉市胜利街美肤体验店。 |
| `booking_store_returned_for_resubmit` | 门店打回重新提交 | 客户 | `customer_important_notice` | 预约编辑页 | 门店需要您调整预约信息后重新提交，原因：手艺人时间需调整。 |
| `booking_cancelled_customer_notice` | 预约取消需告知客户 | 客户 | `customer_important_notice` | 预约详情 | 您的预约已取消，原因是手艺人服务日程已满，详情：7月22日10:25。 |
| `booking_cancelled_store_notice` | 客户 / 员工 / 系统取消需告知门店 | 店长 / 手艺人 / 前台 | `staff_internal_reminder` | 预约详情 | 客户张三的预约已取消，原因：客户确认无法按时到店。 |
| `booking_arrival_overdue_store_notice` | 超过到店后置宽限仍未到店 | 门店 / 前台 | `staff_internal_reminder` | 预约详情 | 客户张三预约时间已过，当前仍未识别到店，请关注。 |
| `booking_auto_no_show_store_notice` | 第二天自动标记爽约 | 门店 / 店长 | `staff_internal_reminder` | 预约详情 | 客户张三昨日预约未到店，系统已自动标记爽约。 |
| `booking_assignment_required` | 无手艺人预约需分配 | 店长 / 排班负责人 | `staff_action_required` | 分配处理页 | 客户张三的预约待分配手艺人，请在截止时间前处理。 |
| `booking_assignment_overdue` | 分配截止后仍未成功分配 | 店长 / 排班负责人 | `staff_action_required` | 分配逾期处理页 | 客户张三的预约已分配逾期，请尽快安排手艺人或处理异常。 |
| `booking_artisan_assigned` | 首次成功分配手艺人 | 手艺人 / 门店，必要时客户 | `staff_internal_reminder` | 预约详情 | 已为客户张三的预约分配手艺人李四，时间：7月22日10:25。 |
| `booking_artisan_reassignment_notice` | 改派无需客户确认但需告知 | 客户 / 原手艺人 / 新手艺人 / 门店 | `customer_important_notice` / `staff_internal_reminder` | 预约详情 | 您的预约手艺人已调整为李四，预约时间不变。 |
| `booking_artisan_reassignment_customer_confirm_required` | 客户手选手艺人改派需确认 | 客户 | `customer_important_notice` | 改派确认页 | 门店建议将您的预约手艺人调整为李四，请确认是否接受。 |

通知契约字段建议包括：`notification_scene_code`、`trigger_action_or_status`、`receiver_type`、`expected_reach_type`、`business_variables`、`jump_target`、`sample_message`、`owned_by_notification_capability`、`booking_boundary_note`。

## 14. 待确认问题

以下问题必须在后续 PR 审查、Contract Gap 或 Founder / Gate 评论中确认。

| 问题 | 影响 | 建议确认方 |
|---|---|---|
| booking 是否作为 `biz.booking.fulfillment` 的独立子交付先审查 | 影响 PR 范围、后续 fulfillment 是否另起草稿。 | Founder / Gate |
| 本文件最终落点是否保留在 `hl-dispatch/deliverables/decisions/`，或后续迁入 `hl-contracts/prd/biz/` | 影响 SSOT 层级和后续 PR 路径。 | Founder / Gate |
| 9 个 `booking_status` 是否接受为正式状态候选 | 影响状态机、API、事件、前端展示和审计。 | Gate |
| 11 个 `booking_action_type` 是否接受，哪些需要注册为 key_action | 影响 Can -> Action -> Audit 和 registry。 | Gate |
| `create_booking` 条件型 key_action 口径是否接受 | 影响草稿、AI Draft 和普通浏览行为的审计边界。 | Gate |
| `service_flow_bound` 作为 `completed` 触发口径是否接受 | 影响 booking 与 fulfillment / 服务流的边界。 | Founder / Gate |
| `store_visit` 到店即 completed，后续服务流只建立链路的口径是否接受 | 影响仅门店预约和咨询后服务动线。 | Founder / Gate |
| Appointment Intent Hold 与 Qualified Resource Hold 的具体契约归属 | 影响 booking 与 store.resource 的职责切分。 | Gate |
| `pending_store_confirm` 是否复用 Qualified Resource Hold 的 15 分钟 TTL | 影响客户等待、门店确认和资源释放。 | Gate |
| 系统自动分配手艺人的首版优先级与不允许自动分配冲突手艺人的规则是否接受 | 影响分配体验和资源治理。 | Gate |
| reason_code 分组和枚举是否接受 | 影响 `reasoncodes.csv` 提案和工程错误处理。 | Gate |
| 预约单字段模型是否作为后续 schema / facts / OpenAPI 输入 | 影响契约生成和工程实现。 | Gate |
| 通知场景码与 `expected_reach_type` 是否由 booking 提案、通知能力统一实现 | 影响通知能力边界和模板治理。 | Gate |
| 员工预约与客户预约共用同一状态机是否接受 | 影响状态复杂度和验收场景组织。 | Founder / Gate |
| 快速预约是否纳入 booking v0.1 首版审查，或后续独立整理 | 影响首版范围控制。 | PM / Founder / Gate |

## 15. 草稿自查

| 检查项 | 结果 |
|---|---|
| 是否只覆盖 booking，不覆盖 fulfillment | 通过。本文只定义预约到店前后闭环，服务履约单生命周期未展开。 |
| 是否明确 DRAFT 状态 | 通过。文首与阅读声明均已标注 DRAFT。 |
| 是否明确当前不写代码、不作为工程开工输入 | 通过。文首已明确。 |
| 是否区分事实、PM 判断和待确认问题 | 通过。上游引用单列，业务内容标为 PM 当前草稿，待确认问题集中列出。 |
| 是否不复制 Tier 1 SSOT | 通过。本文只列路径和引用要求，不复制 Tier 1 规则正文。 |
| 是否避免把 reason_code 冒充为已注册 | 通过。reason_code 仅作为后续提案方向出现，未声称已注册。 |
| 是否遗漏待确认问题 | 初步通过。已列出状态、动作、hold、服务流、字段、通知、落点等主要缺口。 |
