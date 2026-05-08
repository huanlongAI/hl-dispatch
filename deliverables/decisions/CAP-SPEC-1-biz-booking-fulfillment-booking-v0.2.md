# Cap-Spec-1｜biz.booking.fulfillment / booking v0.2

> 状态：DRAFT，等待 Founder / Gate 审查
> 范围：仅 booking（预约）子段，不覆盖 fulfillment（履约）
> 当前不写代码，不作为工程开工输入
> 本文是基于 Q001-Q386 对 `CAP-SPEC-1-biz-booking-fulfillment-booking-v0.1.md` 做 coverage repair，不新增业务推演，不替代 `hl-contracts` Tier 1 SSOT。

## 0. 阅读声明

本文只把 PM 已完成的 Q001-Q386 booking 对话沉淀为 GitHub 可审查草稿。除已明确引用的上游文件外，本文中的状态名、动作名、字段名、原因码、通知场景码、权限规则和流程规则均为“PM 当前草稿，待 Founder / Gate 确认”。

本文不复制 `hl-contracts` Tier 1 SSOT 内容，只列引用路径和待补契约缺口。工程团队不得据此直接开工。

## 1. Coverage Gap List｜v0.1 -> v0.2 修复清单

| Q 段 | 主题 | v0.1 覆盖情况 | v0.2 修复动作 |
|---|---|---|---|
| Q027-Q036 | 冲突 / 重复预约 | 只概括员工代客接受冲突，缺门店配置与客户确认规则。 | 新增“冲突 / 重复预约规则”。 |
| Q045-Q046 | 第三方平台预约 | 仅列场景，缺核销意向与实际核销事实分离。 | 新增“第三方平台预约”。 |
| Q072-Q090 | 预约变更 / 资产锁定 | 只在状态矩阵和 release 中概括，缺改期、改项目、资产锁定顺序。 | 新增“预约变更与资产锁定”。 |
| Q129-Q154 | 快速预约 | 只作为待确认问题出现。 | 新增“快速预约”，纳入 booking v0.1 审查范围。 |
| Q156-Q178 | `pending_store_confirm` | 只列主流程，缺倒计时、门店修改后直接确认、支付 / 资产边界。 | 扩展“pending_store_confirm 细节”。 |
| Q183-Q195 | 取消规则 | 只写员工取消原因和通知，缺资源释放、取消分类、短信 / 内部消息边界。 | 新增“取消规则”。 |
| Q200-Q215 | 通知契约 | 只列 12 个通知场景，缺契约字段和一期边界。 | 扩展“通知契约”。 |
| Q221-Q225 | 草稿生命周期 | 只定义 `draft`，缺草稿生成场景和自动清理。 | 新增“草稿生命周期”。 |
| Q348-Q358 | reason_code 体系 | 只出现字段和待确认，缺 8 个原因域。 | 新增“reason_code 体系”。 |
| Q361-Q370 | 字段模型 | 只列字段名，缺类型、必填、唯一、只读 / 可变规则。 | 扩展“预约单字段模型”。 |
| Q386 | 12 个通知场景 | 已列，但未与通知契约统一收束。 | 保留并纳入覆盖矩阵。 |

## 2. 上游引用

### 2.1 正式上游

- `hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md`
- `hl-dispatch/deliverables/decisions/PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS-v0.1.md`
- `hl-dispatch/deliverables/decisions/PRD-REDEFINITION-SPEC.md`
- `hl-dispatch` Issue #40：`[任务] PM-2 邹骢启动客户与预约履约能力包 Cap-Spec`

### 2.2 Tier 1 SSOT 引用要求

后续进入正式契约或工程前，需要只引用并服从 `hl-contracts` 中与以下内容相关的真源路径：

- HK Kernel（HK.Policy / HK.Audit / HK.ID / HK.Consent）
- Gateway / Protocol Gate
- capability registry
- key_action registry
- reason_code registry
- facts / rules / OpenAPI / event contracts

具体 Tier 1 路径、注册方式和命名归属待 Gate 确认。

### 2.3 过程材料

- `C:\Users\ROG\AI workflow\biz.booking.fulfillment\WORKING-biz.booking.fulfillment-QA-context.md`

该文件仅作为 PM 过程上下文，不是真源，不自动升级为最终决定。

## 3. 能力目标

`biz.booking.fulfillment / booking` 子段的目标是把自然交互、客户自助、员工代客和门店主动产生的预约意图，稳定转成可确认、可审计、可释放资源的正式预约事实。

首版 booking 需要覆盖预约草稿、客户主体引用、Appointment Intent Hold、Qualified Resource Hold、GUI Confirm、正式预约单、门店确认、预约取消、到店完成、逾期未到、爽约、手艺人分配与改派、快速预约、通知需求和审计证据引用。

booking 子段的闭环终点是“客户到店并成功创建 / 绑定当天客户服务流动线容器”，预约单进入 `completed`。后续项目服务、资产消耗、服务履约、退款等不由预约状态承载，归后续服务流 / 履约 / 资产 / 支付等能力处理。

## 4. 非目标

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

## 5. 角色与发起方

| 角色 / 发起方 | booking 中的含义 | 当前边界 |
|---|---|---|
| 客户 | 通过客户自助端提交预约、取消预约、确认必要信息、在特定场景确认手艺人改派。 | 客户主体必须可识别。正式客户与散客客户均需有系统内 `customer_id`。PM 当前草稿，待 Founder / Gate 确认。 |
| 员工 | 代客户创建、修改、取消预约，或根据线下沟通确认预约安排。 | 必须受权限、门店范围和审计约束。 |
| 店长 / 门店管理 | 门店确认、取消、分配手艺人、处理分配逾期、处理高风险异常。 | 默认具备较高预约治理权限，但具体权限模型待 Gate 确认。 |
| 排班负责人 | 处理无手艺人预约分配、分配逾期、改派。 | 具体角色名和授权方式待 Gate 确认。 |
| 手艺人 | 可主动预约自己的客户，也可能作为预约资源 / 履约责任人。 | “手艺人”是统一术语。 |
| 系统 / AI | AI 生成预约草稿；系统触发自动确认、自动分配、到店逾期、自动爽约、资源释放等。 | AI 只生成候选或草稿，不替用户确认正式业务事实。 |
| 通知能力 | 承接预约侧通知需求。 | booking 只提出通知场景和变量，不实现通知。 |

## 6. 预约全场景流程

以下为 PM 当前草稿，待 Founder / Gate 确认。

### 6.1 员工 / 门店主动预约类型

| 场景 | 预约语义 | 结果模式 |
|---|---|---|
| 仅门店预约 | 门店主动约客户到店咨询，不选项目、不选手艺人。 | `store_visit`，生成门店默认半小时日程。 |
| 手艺人预约 | 手艺人或门店主动预约客户，并明确项目和手艺人。 | `service_assigned`。 |
| 第三方平台项目预约 | 门店根据第三方订单预约客户到店核销。 | 默认 `service_unassigned`；若第三方信息能匹配内部手艺人，可为 `service_assigned`。 |
| 客户剩余资产预约 | 门店主动基于客户已有资产约客户到店消耗。 | 门店发起时必须选择手艺人，生成 `service_assigned`。 |

### 6.2 员工预约主流程

1. 员工选择客户；若客户只有名称 / 称呼，需要先有系统内散客客户主体。
2. 员工选择门店和预约时间。
3. 根据场景选择项目、资产、手艺人或第三方订单引用。
4. 系统判断预约模式：`store_visit`、`service_unassigned` 或 `service_assigned`。
5. 系统执行必要元素校验、资源校验和 hold 创建。
6. 员工确认提交后，门店发起类预约通常直接进入 `confirmed`。
7. 如果存在冲突但门店配置允许重复登记 / 宽松管控，员工可代客确认风险，但必须记录冲突提示、配置命中、操作人和代客确认事实。
8. 若后续取消、改派、分配、改期或异常处理，均按权限、资源和审计规则执行。

### 6.3 客户自助预约类型

| 场景 | 预约语义 | 结果模式 |
|---|---|---|
| 门店项目预约 | 客户从门店支持项目列表进入，可购买并立即预约。系统推荐可做该项目且有空的手艺人，客户可确认或更换。 | 最终应为 `service_assigned`。 |
| 手艺人预约 | 客户先选手艺人，再选该手艺人可做项目和时间。 | `service_assigned`。 |
| 客户资产预约 | 客户基于已有资产预约到店消耗。客户可选手艺人，也可选择由门店安排。 | 选手艺人为 `service_assigned`；不选手艺人为 `service_unassigned`。 |

客户自助端首版不允许创建仅门店 `store_visit` 预约。

### 6.4 客户预约主流程

1. 客户进入项目、手艺人或资产预约入口。
2. 系统识别客户主体、门店、时间、项目 / 资产等必要元素。
3. 若客户未明确选择手艺人，系统可推荐可用手艺人。
4. 客户确认必要信息后执行 `submit_booking`。
5. 系统创建正式预约单编号，并执行资源校验、hold 创建、资产 / 支付预处理。
6. 若门店开启“客户预约免门店确认”，预约直接进入 `confirmed`，但需记录系统按门店配置自动确认的事实。
7. 若门店关闭“客户预约免门店确认”，预约进入 `pending_store_confirm`，门店需在 hold 有效期内确认、修改后确认或打回重新提交。
8. 门店确认后进入 `confirmed`；超时或打回后释放资源，进入 `submit_expired` 或重新提交链路。

### 6.5 客户自助选手艺人与改派确认

- 客户主动选择的手艺人包括：手艺人预约入口选择、项目预约中主动更换并确认、资产预约中主动选择。
- 客户主动选定手艺人后，后续门店改派必须客户确认。
- 系统自动推荐 / 自动匹配不等于客户主动选择。
- 客户自助端更换手艺人必须重新校验资源并创建新 hold；新 hold 未确认前，旧预约保持有效。

## 7. 第三方平台预约

以下为 PM 当前草稿，待 Founder / Gate 确认。

第三方平台项目预约是门店根据第三方平台订单或团购券信息，主动预约客户到店核销。预约创建时表达的是“核销意向”，不是最终服务事实。

| 规则 | 草稿定义 |
|---|---|
| 预约模式 | 默认 `service_unassigned`；如果第三方订单明确带有手艺人且可匹配门店内部手艺人，可生成 `service_assigned`。 |
| 预定项目 | 预约节点保存 `intended_redemption_project`，表示门店根据第三方平台信息预定的核销意向项目。 |
| 实际核销项目 | 客户到店后实际核销项目由后续核销 / 服务流节点记录为 `actual_redemption_project`。 |
| 不覆盖原则 | 如果预定项目 A 与实际核销项目 B 不一致，不覆盖原预约节点。预约意向和实际核销事实分别追加记录、清晰留痕。 |
| 跨包边界 | 第三方订单、券核销、结算归对应能力；booking 只保存预约意向引用和链路关系。 |

## 8. 草稿生命周期

以下为 PM 当前草稿，待 Founder / Gate 确认。

### 8.1 草稿生成场景

| 场景 | 是否生成草稿 | 说明 |
|---|---|---|
| AI Draft | 是 | 自然交互识别出预约意图后，形成可补齐的候选草稿。 |
| 多步骤客户自助预约 | 需要跨步骤保存时生成 | 仅打开创建页不一定生成草稿。 |
| 员工代客持续编辑 | 需要暂存时生成 | 便于员工稍后继续补齐客户、门店、时间、项目等信息。 |
| 被门店打回后重新编辑 | 可基于原信息生成新编辑态 | 原提交链路结束，重新提交必须重新校验并创建新 hold。 |
| 快速预约未完成 | 用户继续操作时才生成 | 快速预约失败后不默认保留草稿。 |
| 第三方核销意向待补齐 | 需要跨步骤保存时生成 | 保存第三方平台订单 / 券引用与预约意向。 |

### 8.2 草稿边界

- `draft` 不占资源，不生成正式 hold，不算正式预约。
- `create_booking` 只有生成草稿、AI Draft、后台代客草稿等业务记录时才算 key_action；纯前端会话态或仅打开创建页面不算 key_action。
- `submit_booking` 是进入正式预约链路的边界动作。
- 第一阶段不做完整草稿管理业务，但需要明确草稿自动清理机制。
- 草稿保留期作为后台配置项；到期后自动清理，清理后不可恢复。
- 草稿清理不触发资源释放，因为草稿本身不占资源。

## 9. 状态定义

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

### 9.1 终态规则

`completed`、`cancelled`、`no_show`、`submit_expired` 均不可恢复、不可覆盖、不可复用旧 hold。继续预约只能生成新草稿、新预约单和新 hold，并保留来源链路。

### 9.2 到店完成口径

`service_flow_bound` 在 booking 草稿中表示“创建 / 绑定当天客户服务流动线容器”，不等于必须创建服务履约单。仅门店 / 无项目预约到店后，即使客户咨询后未购买、未消耗、未创建服务履约单就离店，预约仍可进入 `completed`，后续结果由当天客户服务流继续记录。该口径待 Founder / Gate 确认。

## 10. 状态流转矩阵

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

### 10.1 统一 fail-secure 规则

凡进入 `cancelled`、`no_show`、`submit_expired` 等需要释放预约资源的流转，如果资源释放失败，不得进入目标终态，应保持原状态并触发 `resolve_resource_release_failure`。

凡 `submit_booking`、`resubmit_booking`、`confirm_booking`、`assign_artisan`、`reassign_artisan` 等需要创建、替换或锁定资源的动作，如果资源校验失败、hold 创建失败、hold 替换失败或关键资源锁定失败，不得进入目标状态。

## 11. pending_store_confirm 细节

以下为 PM 当前草稿，待 Founder / Gate 确认。

| 规则 | 草稿定义 |
|---|---|
| 适用范围 | 仅客户自助预约且门店关闭“客户预约免门店确认”时进入。员工代客、门店主动预约不进入该状态。 |
| 正式性 | `pending_store_confirm` 属于正式预约状态，不是草稿；`submit_booking` 已成功并生成正式预约单编号。 |
| 资源占用 | 客户提交时创建 Qualified Resource Hold，门店确认后转 `confirmed`；打回或超时释放资源。 |
| 倒计时 | 首版复用 15 分钟 TTL，最长 30 分钟规则。客户侧和门店端均展示倒计时和资源即将释放提醒。 |
| 门店打回 | 门店不确认客户预约时，填写原因并释放原 hold；客户重新提交必须重新校验并创建新 hold。 |
| 门店修改后直接确认 | 门店可线下联系客户沟通一致后，修改预约信息并直接确认，减少客户反复提交。 |
| 修改资源字段 | 修改时间、手艺人、房间、项目等影响资源的信息时，必须重新校验并创建 / 替换 hold。 |
| 审计差异 | 必须记录客户原提交、门店修改后确认信息、修改原因、线下沟通说明、操作人、旧 hold 与新 hold 替换关系。 |
| 客户可见说明 | 客户侧展示最新预约信息和客户可见变更摘要；内部审计说明不直接暴露给客户。 |
| 修改后客户取消 | 若客户因门店调整后不接受而取消，取消仍是 `cancel_booking`，但取消原因需关联门店调整确认记录。 |
| 支付 / 资产边界 | 门店确认前只做必要预校验或预授权；门店确认后再完成支付确认或资产锁定转正式占用。 |
| 确认失败 | 支付确认或资产正式锁定失败时，预约不能转 `confirmed`，应释放资源并回到可重新提交链路。 |

## 12. Key Action 表

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

## 13. 资源 Hold / Release

以下规则为 PM 当前草稿，待 Founder / Gate 确认。

### 13.1 Hold 类型

| Hold 类型 | booking 草稿含义 | 资源承诺 |
|---|---|---|
| Appointment Intent Hold | 对客户、门店、时间窗口的预约意向保留。 | 不锁具体手艺人 / 房间，可用于意向阶段。 |
| Qualified Resource Hold | 对可审计、可排程、可冲突校验的资源承诺做短时暂占。 | 支持 `store_visit`、`service_unassigned`、`service_assigned`，不一定总是具体手艺人。 |

### 13.2 TTL 与确认

- 上游任务书要求 Hold TTL 15 分钟，最长 30 分钟。
- PM 草稿判断：`pending_store_confirm` 首版复用 Qualified Resource Hold 的 15 分钟 TTL，最长 30 分钟。待 Gate 确认。
- `GUI Confirm` 发生在 Qualified Resource Hold 创建之后，确认前资源短时暂占。
- 生成正式预约前必须重新校验客户、门店、项目、资源、hold 有效性和 hold 归属。

### 13.3 Release 规则

| 场景 | release 规则 |
|---|---|
| hold 超时未确认 | 自动释放资源，用户继续时必须重新校验并创建新 hold。 |
| pending_store_confirm 超时 / 打回 | 释放原 hold，进入 `submit_expired` 或重新提交链路。 |
| 预约取消 | 预约资源释放成功后才进入 `cancelled`。 |
| 自动 no_show | 预约资源释放成功后才进入 `no_show`。 |
| 快速重新预约 / 重新提交 | 不复用旧 hold，必须创建新 hold。 |
| 改期 / 改派 / 改资源 | 新 hold 创建并确认成功后，释放旧资源并启用新资源。 |
| release 失败 | fail-secure，保持原状态，触发异常处理。 |

## 14. 冲突 / 重复预约规则

以下为 PM 当前草稿，待 Founder / Gate 确认。

| 规则 | 草稿定义 |
|---|---|
| 门店配置 | 首版按全店统一配置，不按项目、房型、手艺人角色细分。 |
| 宽松管控 | 门店允许重复预约 / 重复登记时，系统提醒但不默认阻断。 |
| 手艺人冲突 | 指定手艺人预约如命中重复预约，必须提示并由客户或操作人确认。 |
| 房间 / 服务位冲突 | 指定房间 / 服务位如命中重复登记，必须提示并确认。 |
| 客户自助端 | 客户自己在线预约遇到冲突时，必须展示风险并由客户确认，不能无感接受。 |
| 员工代客 | 员工可代客接受冲突，不强制客户本人在线确认；系统记录员工身份、冲突提示、门店配置命中和代客确认事实。 |
| 可选备注 | 员工代客接受冲突时不强制填写代客确认原因，但可填写备注。 |
| 审计归属 | 冲突接受不单独拆动作，并入 `confirm_booking` 或提交确认动作的 `conflict_acceptance` 审计子记录。 |
| 自动分配例外 | 系统自动分配手艺人时，即使门店允许重复，也不能自动分配到已有冲突的手艺人。 |

## 15. 预约变更与资产锁定

以下为 PM 当前草稿，待 Founder / Gate 确认。

### 15.1 预约变更

| 场景 | 草稿规则 |
|---|---|
| 改期 | 视为预约变更，不是取消后重新预约；保留主记录或业务编号，生成变更版本。 |
| 变更新 hold | 变更时先校验并暂占新资源；客户或授权操作人确认前，旧预约保持不变。 |
| 新 hold 超时 | 新 hold 自动释放，变更请求失效或回到待重新选择，不影响旧预约。 |
| 变更成功 | 在同一治理动作中释放旧资源，使新资源转正式占用，并记录变更版本。 |
| 跨门店 | 客户自助不允许跨门店变更；多数跨门店场景应取消原预约后重新预约新门店。特殊同级直营店变更待 Gate 确认。 |
| 改项目 | 属于资源相关变更，需重新校验项目、时长、手艺人能力、资源、价格 / 资产依赖。 |
| 临近改项目 | 到达后台配置边界时间后，默认进入审批；命中不可逆备料、强资源占用或门店禁止规则时拒绝。 |

### 15.2 客户自助项目变更

| 客户预约场景 | 项目变更规则 |
|---|---|
| 门店项目预约 | 不可直接修改项目；要换项目只能取消当前项目预约，再预约新项目。 |
| 手艺人预约，先购买项目再预约 | 不可直接修改项目；需先处理定金退款或全额退款。 |
| 手艺人预约，项目来自历史资产 | 可以修改项目，本质是解除历史资产锁定占用并重新锁定。 |
| 客户资产预约 | 可以修改项目，本质是解除历史资产锁定占用，并重新选择资产 / 项目。 |

### 15.3 员工代客项目变更

员工代客修改项目原则上遵循客户自助端限制。员工可发起高风险或例外处理，例如协助退款、换购、资产释放后重锁定，但必须走 Can / 审批 / 审计，不能直接覆盖原预约事实。

### 15.4 资产锁定边界

| 场景 | 草稿规则 |
|---|---|
| 客户资产预约创建 | 锁定客户资产占用属于 key_action，但动作本体归客户资产能力。booking 记录调用结果和审计 ID。 |
| 预约确认失败 | 若资产锁定成功但预约确认失败，必须立即释放资产锁定。 |
| 预约取消 | 取消预约时释放资产锁定，除非资产能力返回不可释放或已有消耗事实。 |
| 资产 A 改资产 B | 先锁定新资产 B；变更确认成功后释放旧资产 A。新资产锁定失败时，旧预约和旧资产锁定保持不变。 |
| 到店后消耗 | 预约确认和 check-in 都不直接消耗资产；资产在服务履约单确认消耗时转为实际消耗。 |
| 到店但未服务 | 服务流结束或门店确认未服务时释放资产锁定。 |
| no_show | 自动转 `no_show` 时同步释放资产锁定，并写审计。 |

资产本体规则、资产释放失败处理和资产消耗事实归客户资产能力；booking 只记录引用、结果和关联审计 ID。

## 16. 取消规则

以下为 PM 当前草稿，待 Founder / Gate 确认。

### 16.1 取消入口

- 客户未到店前始终保留取消预约权利；首版不做“短时免责取消窗口”。
- 员工端也保留取消入口，但需要店长以上或授权权限。
- `cancel_booking` 适用于未到店且非终态的正式预约状态：`pending_store_confirm`、`confirmed`、`arrival_overdue`、`assignment_overdue`。
- `draft` 放弃或清理由草稿机制处理，不属于正式取消。
- `completed`、`cancelled`、`no_show`、`submit_expired` 都是终态，不允许再取消。

### 16.2 取消分类

| 取消类型 | 草稿定义 |
|---|---|
| `customer_cancel` | 客户自助取消。客户取消原因可选填。 |
| `staff_cancel_on_behalf` | 员工根据客户电话、微信、线下沟通等代客取消。必须受权限和审计约束。 |
| `store_cancel` | 门店因资源不可用、门店安排变化等原因取消。 |
| `system_cancel` | 系统在闭店、歇业、关键资源不可用且无替代等不可逆 / 无法履约场景取消。 |

### 16.3 取消终态与资源释放

- `booking.cancel` 权限校验通过，且预约资源释放成功后，预约单立即进入 `cancelled`。
- 支付、定金、资产释放 / 退款等后续处理作为关联事实或待处理任务，不阻塞预约进入 `cancelled`，但由对应能力负责。
- 如果预约资源释放失败，取消动作失败，预约不得进入 `cancelled`，必须返回明确原因并触发 `resolve_resource_release_failure`。

### 16.4 取消原因与通知

| 场景 | 草稿规则 |
|---|---|
| 员工端取消 | 必须填写取消原因，记录操作人、权限校验、资源释放结果。 |
| 客户自助取消 | 不强制填写取消原因，系统记录发起方、取消时间和资源释放结果。 |
| 客户可见原因 | 员工 / 门店取消时，需区分客户可见取消原因与内部审计原因。 |
| 内部审计原因 | 可记录更详细的门店背景、权限校验、操作人、资源释放情况。 |
| 客户短信 | 员工端取消预约成功后，需要通知客户，短信模板包含客户可见取消原因、门店名称、预约时间等。 |
| 内部消息 | 客户或员工取消成功后，应通知门店管理端、关联手艺人或排班负责人，包含资源释放结果。 |
| 通知失败 | 通知发送失败不阻塞预约进入 `cancelled`；第一期通知不做补偿机制。 |

## 17. 快速预约

以下为 PM 当前草稿，待 Founder / Gate 确认。快速预约纳入 booking v0.1 审查范围，不再只作为开放问题。

### 17.1 定义

快速预约是基于历史已完成服务 / 履约记录或已取消预约，把原信息带入，让客户或员工只重新选择时间的预约效率入口。它不是复用旧预约事实，而是创建全新预约。

### 17.2 来源与入口

| 规则 | 草稿定义 |
|---|---|
| 来源对象 | 首版只支持历史已完成服务 / 履约记录、已取消预约。 |
| 不支持来源 | `no_show` 爽约预约和任意状态预约不作为首版快速预约来源。 |
| 客户入口 | 客户自助端可基于自己的历史服务或已取消预约快速预约。 |
| 员工入口 | 员工端可代客基于客户历史服务或已取消预约快速预约，受员工权限和客户可见范围控制。 |
| 门店开关 | 客户自助端快速预约受门店级开关控制；关闭后客户侧不展示入口，不置灰。 |
| 员工端开关 | 员工端不受客户自助端快速预约开关控制，但必须受权限控制。 |

### 17.3 主路径规则

- 首版快速预约主路径只允许重新选择时间。
- 项目、手艺人、门店等原信息必须在确认页展示。
- 如果用户想改项目、手艺人或门店，退出快速预约主路径，进入普通预约流程。
- 快速预约不新增独立预约类型，只记录来源标记，例如 `source_type=quick_booking`。

### 17.4 重新校验

快速预约确认前必须重新校验项目、手艺人、资源、资产 / 支付状态。原项目不可用、原手艺人不可用或资源不可用时，系统提示原因并引导用户重新选择，不能无感替换。

如果客户资产预约来源中的原资产已用完、过期或不可用，快速预约可提示原资产不可用，并转为普通项目预约进入支付链路。原手艺人可保留为默认选择，但必须重新校验。

### 17.5 新预约与审计

- 快速预约成功后生成全新预约，不复用原预约编号和旧 hold。
- 新预约引用来源预约或来源服务记录。
- 快速预约创建正式预约时属于 key_action。
- 快速预约失败时保留普通审计记录，但不生成业务预约单。
- 快速预约失败后不默认保留草稿；用户继续操作时才生成新草稿或 hold。

## 18. reason_code 体系

以下为 PM 当前草稿，待 Gate 确认。本文只做提案，不声称已进入 `reasoncodes.csv` 或正式 registry。

### 18.1 原因表达层级

| 层级 | 用途 |
|---|---|
| `reason_code` | 工程分支、统计、审计追踪使用的结构化原因码。 |
| `reason_text` | 门店、员工或系统补充说明。 |
| `customer_visible_reason` | 面向客户展示的合规、可理解、不暴露内部细节的原因。 |

### 18.2 原因域

| reason_domain | 代表性枚举 | 用途 |
|---|---|---|
| `submit_failure` | `missing_required_elements`、`store_not_supported`、`project_not_supported_by_store`、`resource_unavailable`、`hold_create_failed`、`asset_validation_failed`、`payment_precheck_failed`、`customer_identity_required`、`policy_not_satisfied`、`system_error` | 提交失败。 |
| `store_return` | `schedule_not_available`、`artisan_not_available`、`room_not_available`、`store_needs_contact_customer`、`customer_info_incomplete`、`booking_info_needs_adjustment`、`other_store_reason` | 门店不确认并打回客户重新提交。 |
| `cancel_reason` | `customer_cannot_arrive`、`customer_requested_cancel`、`store_schedule_full`、`artisan_unavailable`、`room_unavailable`、`store_closed_or_suspended`、`weather_or_emergency`、`duplicate_booking`、`wrong_booking_info`、`other_cancel_reason` | 取消预约。 |
| `resource_failure` | `hold_create_failed`、`hold_replace_failed`、`hold_release_failed`、`artisan_conflict`、`room_conflict`、`schedule_conflict`、`capacity_exceeded`、`resource_version_conflict`、`resource_not_found`、`resource_policy_blocked`、`system_error` | 资源校验、暂占、替换、释放失败。 |
| `arrival_reason` | `on_time_arrival`、`early_arrival`、`late_arrival`、`arrival_overdue_no_arrival`、`auto_no_show_next_day`、`manual_arrival_marked`、`biometric_arrival_detected`、`service_flow_bound`、`service_flow_bind_failed` | 到店、逾期、爽约和服务流绑定。 |
| `assignment_failure` | `no_available_artisan`、`artisan_skill_not_matched`、`artisan_schedule_conflict`、`manual_assignment_overdue`、`auto_assignment_failed`、`assignment_permission_denied`、`temporary_take_order_failed`、`schedule_patch_failed`、`system_error` | 手艺人分配失败。 |
| `reassignment_reason` | `artisan_unavailable`、`artisan_schedule_conflict`、`artisan_skill_not_matched`、`customer_confirm_required`、`customer_confirmed`、`customer_rejected`、`customer_confirm_timeout`、`candidate_hold_failed`、`original_resource_release_failed`、`permission_denied`、`system_error` | 手艺人改派与客户确认改派。 |
| `system_cancel_reason` | `store_closed`、`store_suspended`、`temporary_business_stop`、`artisan_leave_or_shift_change`、`critical_resource_unavailable`、`project_disabled_or_invalid`、`store_config_invalid`、`force_majeure`、`system_policy_cancelled`、`other_system_cancel_reason` | 系统取消。 |

## 19. 预约单字段模型

以下为 PM 当前草稿，待 Gate 确认。字段模型是业务字段模型，不是数据库 Schema / API Schema；后续必须通过 Gate 转换为 facts / OpenAPI / 工程契约。字段类型、必填、唯一、只读 / 可变规则均为业务规格草稿，不等于最终工程 schema。

### 19.1 字段域总览

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

### 19.2 字段规则摘要

| 字段域 | 业务类型 | 必填口径 | 唯一性 | 只读 / 可变规则 |
|---|---|---|---|---|
| 基础身份字段 | ID / string / enum | `booking_id`、`booking_no`、`tenant_id`、`store_id`、`customer_id` 必填。 | `booking_id` 全局唯一；`booking_no` 在租户内唯一，待 Gate 确认。 | 创建后大多只读；客户合并不重写历史 `customer_id`。 |
| 预约场景字段 | enum / boolean / reference | 提交时必须能判断 `booking_service_mode` 和必要元素。 | 非唯一。 | 提交前可变；提交后变更需走预约变更规则。 |
| 预约时间字段 | datetime / integer / text | 正式提交必须有 `scheduled_start_at`；`store_visit` 可用默认接待时长生成结束时间。 | 非唯一。 | 提交后改时间需重新校验并创建新 hold。 |
| 资源字段 | ID / enum / boolean / reference | 进入正式链路后应有 hold 引用；指定资源场景需保存对应资源。 | 非唯一。 | 资源变更需走 assign / reassign / 变更规则。 |
| 项目 / 资产 / 支付引用字段 | ID / enum / text / boolean | 按预约场景条件必填。 | 非唯一。 | 不覆盖项目意向；第三方预定项目和实际核销事实分开记录。 |
| 状态与动作字段 | enum / datetime / ID / integer / boolean | 正式预约必须有 `booking_status`。 | 非唯一。 | 状态由动作和规则流转，不允许手工覆盖终态。 |
| 到店与服务流字段 | enum / datetime / ID | 到店完成时必须保存到店事实和服务流引用。 | 非唯一。 | 完成后只追加关联事实，不回滚预约终态。 |
| 原因与说明字段 | enum / text / boolean | 失败、取消、打回、异常或终态原因场景必填。 | 非唯一。 | 保存当前摘要；完整历史进入审计事实。 |
| 通知字段 | enum / ID / datetime / text / boolean | 需要通知时填写。 | 非唯一。 | 通知状态不阻塞预约终态。 |
| 审计字段 | ID / datetime / reference | key_action 和终态变化必须保留审计引用。 | 非唯一。 | 预约单只保存审计摘要和引用，完整审计不可覆盖。 |

## 20. 权限与审批规则

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

### 20.1 高风险审批因素

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

## 21. 通知契约与通知场景

以下通知规则为 PM 当前草稿，待 Founder / Gate 确认。booking 只定义通知需求契约，通知能力负责模板、通道、发送状态、重试和补偿。

### 21.1 通知契约边界

| 契约字段 / 规则 | 草稿定义 |
|---|---|
| `notification_scene_code` | 稳定场景码，表达预约业务语义。 |
| `receiver_type` | 接收人类型，例如客户、店长、前台、手艺人、排班负责人。 |
| `expected_reach_type` | 业务期望触达类型，不直接绑定实现通道。首版枚举：`customer_reminder`、`customer_important_notice`、`staff_internal_reminder`、`staff_action_required`。 |
| `business_variables` | 通知模板所需业务变量，例如客户名、门店、时间、手艺人、取消原因、跳转目标。 |
| `jump_target` | 通知点击后的预约详情页、预约编辑页、分配处理页或改派确认页。 |
| `action_required` | 表示通知是否要求接收人处理。 |
| `action_type` | 当 `action_required=true` 时，表达需要执行的预约动作，例如 `confirm_booking`、`resubmit_booking`、`assign_artisan`。 |
| 通知详情页 | 第一期读取当前预约最新状态，不展示通知产生时的完整快照。 |
| 一期通道边界 | 客户短信、内部消息、手机厂商通用推送均可作为发送通道；具体由通知能力定义。 |
| 补偿机制 | 第一期不做通知补偿机制。通知失败不阻塞预约终态。 |
| 审计边界 | 第一期不强制通知请求携带 `audit_correlation_id`，但必须能通过 `booking_id` 和跳转目标打开预约上下文。 |

### 21.2 12 个通知场景

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

## 22. 需要 Founder / Gate 确认的问题

| 疑问 | 关联 Q 段 | 影响章节 | 不确认的风险 | 需要谁确认 | 建议选项 |
|---|---|---|---|---|---|
| booking 是否作为 `biz.booking.fulfillment` 的独立子交付先审查 | Issue #40 | 全文 | PR 范围和后续 fulfillment 切分不清 | Founder / Gate | 建议先审 booking 子段 |
| v0.2 文件最终落点是否保留在 `hl-dispatch/deliverables/decisions/`，或后续迁入 `hl-contracts/prd/biz/` | Issue #40 / PRD 重定义 | 上游引用、PR 路径 | SSOT 层级不清 | Founder / Gate | 先在 hl-dispatch 审查，后续按 Gate 迁移 |
| 9 个 `booking_status` 是否接受为正式状态候选 | Q234-Q265 | 状态定义、矩阵 | 工程状态机无法稳定 | Gate | 建议按 v0.2 状态候选审查 |
| 11 个 `booking_action_type` 及 key_action 划分是否接受 | Q267-Q280 | Key Action 表、权限 | Can -> Action -> Audit 注册不清 | Gate | 建议先作为候选 |
| 快速预约是否正式纳入 booking v0.1 | Q129-Q154 | 快速预约、字段、验收 | `quick_rebook` 半进半出 | Founder / Gate | 建议纳入 |
| `service_flow_bound` 作为 `completed` 触发口径是否接受 | Q234-Q346 | 状态矩阵、到店完成 | booking 与 fulfillment 边界不清 | Founder / Gate | 建议接受“服务流动线容器”口径 |
| Hold 语义归属如何切分 | Q001-Q009 / Q156-Q157 | Hold / Release | booking 与 store.resource 互相重定义 | Gate | booking 定义预约侧语义，资源能力定义资源本体 |
| 通知场景码与通知契约字段是否由 booking 提案、通知能力统一实现 | Q200-Q215 / Q386 | 通知契约 | 通知能力与 booking 耦合 | Gate | booking 提案，通知能力实现 |
| reason_code 分组和枚举是否接受 | Q348-Q358 | reason_code 体系 | reasoncodes 提案缺 Gate 口径 | Gate | 先作为 Cap-Spec-3 输入 |
| 字段模型是否作为后续 schema / facts / OpenAPI 输入 | Q361-Q370 | 字段模型 | 工程误以为已是数据库设计 | Gate | 标记为业务字段草稿 |

## 23. Coverage Matrix｜Q001-Q386 覆盖矩阵

| Q 段 | 主题 | v0.2 落点 | 覆盖状态 | 备注 |
|---|---|---|---|---|
| Q001-Q009 | 客户主体、Intent Hold、Resource Hold、GUI Confirm、正式确认 | §5、§13 | covered | Q001-Q002 采用后续修订口径。 |
| Q010-Q017 | 资源变更审批、手艺人分配、接待人概念删除 | §20、§15 | covered | 接待人 / 顾问不进首版。 |
| Q018-Q022 | 仅门店到店咨询与服务履约单关系 | §3、§4、§9.2 | deferred | 不进入 fulfillment；仅保留预约完成与服务流引用口径。 |
| Q023-Q026 | 预约类型、时间、service_unassigned 校验 | §6、§13 | covered | 项目 / 资源细节待相关能力确认。 |
| Q027-Q036 | 冲突 / 重复预约 | §14 | covered | 待 Gate 确认正式命名。 |
| Q037-Q044 | 客户自助预约类型、资产预约是否选手艺人 | §6.3、§6.4 | covered | 客户资产能力本体不在本包。 |
| Q045-Q046 | 第三方平台预约 | §7 | covered | 预约意向与核销事实分离。 |
| Q047-Q050 | 门店主动资产预约、手艺人预约、仅门店预约、接待人概念 | §6.1、§6.2 | covered | 不建接待人模型。 |
| Q051-Q063 | 到店、无预约服务流、散客客户主体、客户合并边界 | §5、§9.2、§19 | covered / deferred | 服务流与客户档案本体 deferred 到对应能力；booking 保留引用。 |
| Q064-Q071 | arrival_overdue、no_show、取消、快速重约不复用 hold | §9、§10、§13、§16 | covered | no_show 后到店按无预约服务流。 |
| Q072-Q090 | 预约变更 / 资产锁定 | §15 | covered | 资产动作归资产能力。 |
| Q091-Q100 | 通用状态、completed 口径、服务流绑定 | §9、§10 | covered | `service_flow_bound` 待 Founder / Gate 确认。 |
| Q101-Q128 | service_unassigned 分配、自动分配、改派客户确认 | §6.5、§10、§20 | covered | 自动分配高级策略后续完善。 |
| Q129-Q154 | 快速预约 | §17 | covered | 纳入 booking v0.1 审查范围。 |
| Q155-Q180 | confirmed / pending_store_confirm / 门店修改后直接确认 | §11 | covered | 取消窗口相关旧口径被 Q183 废止。 |
| Q181-Q182 | 短时免责取消窗口 | §16 | superseded | 被 Q183 废止，不进入 v0.2 规则。 |
| Q183-Q195 | 取消规则 | §16 | covered | 资源释放成功才进 `cancelled`。 |
| Q196-Q199 | 通知失败与补偿归属 | §16、§21 | covered | 被 Q204-Q205 修订为一期不做补偿机制。 |
| Q200-Q215 | 通知契约边界 | §21.1 | covered | 通知实现归通知能力。 |
| Q216-Q225 | action_type、draft、草稿生命周期 | §8、§12 | covered | 草稿不占资源。 |
| Q226-Q233 | submit_booking、pending_store_confirm、submit_expired | §9、§10、§11 | covered | `submit_expired` 为终态。 |
| Q234-Q347 | 状态定义与状态流转矩阵 | §9、§10 | covered | 小概率异常状态不新增。 |
| Q348-Q358 | reason_code 体系 | §18 | covered | 先提案，不注册。 |
| Q359-Q370 | 字段模型 | §19 | covered | 补字段说明、类型、必填、唯一、只读 / 可变摘要。 |
| Q371-Q381 | 权限与审批规则 | §20 | covered | 高风险审批配置待 Gate 确认。 |
| Q382-Q386 | 通知场景清单 | §21 | covered | 12 个通知场景保留，手艺人术语统一。 |

## 24. v0.2 自查

| 检查项 | 结果 |
|---|---|
| 是否只覆盖 booking，不覆盖 fulfillment | 通过。本文只定义预约阶段；服务履约单生命周期 deferred。 |
| 是否明确 DRAFT 状态 | 通过。文首与阅读声明均已标注 DRAFT。 |
| 是否明确当前不写代码、不作为工程开工输入 | 通过。文首已明确。 |
| 是否不把过程文件当真源 | 通过。过程文件仅作为 coverage repair 材料。 |
| 是否不新增业务推演 | 通过。新增内容均来自 Q001-Q386 覆盖修复。 |
| 是否把快速预约纳入审查范围 | 通过。已新增 §17。 |
| 是否补全指定 9 块内容 | 通过。已补冲突、第三方、变更、快速预约、pending_store_confirm、取消、reason_code、字段模型、通知契约和草稿生命周期。 |
| 是否列出 Coverage Matrix | 通过。见 §23。 |
| 是否仍需 Founder / Gate 裁决 | 是。见 §22。 |
