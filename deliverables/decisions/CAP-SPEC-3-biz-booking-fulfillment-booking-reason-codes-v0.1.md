# Cap-Spec-3｜biz.booking.fulfillment / booking Reason Code Proposal v0.1

> 状态：DRAFT，等待 Gate 审查
> 范围：仅 booking（预约）子段，不覆盖 fulfillment（履约）
> 当前不写代码，不作为工程开工输入
> 本文是 reason_code 提案，不是最终注册；所有 code 均为 DRAFT / 待 Gate 确认，尚未写入 registry。

## 1. 上游引用

- `hl-dispatch/deliverables/decisions/CAP-SPEC-1-biz-booking-fulfillment-booking-v0.2.md`
- `hl-dispatch/deliverables/decisions/CAP-SPEC-2-biz-booking-fulfillment-booking-acceptance-v0.1.md`
- `hl-dispatch/deliverables/decisions/CONTRACT-GAP-biz-booking-fulfillment-booking-v0.1.md`
- `C:\Users\ROG\AI workflow\biz.booking.fulfillment\WORKING-biz.booking.fulfillment-QA-context.md`

过程文件仅作为 PM 草稿整理依据，不是真源，不替代 `hl-contracts` Tier 1 SSOT。

## 2. 提案原则

- 本文只提出 booking 子段 reason_code 候选，不声称已注册。
- 所有 `reason_code` 均需 Gate 审查后，才能进入正式 `reasoncodes.csv` 或对应 registry。
- PM 当前草稿采用三层原因表达：`reason_code`、`reason_text`、`customer_visible_reason`。
- `reason_code` 服务工程分支、统计、审计追踪；`reason_text` 服务内部说明；`customer_visible_reason` 服务客户展示。

## 3. reason_code 提案表

| reason_code | 场景 | 触发方 | 关联状态 | 是否 key_action | 审计要求 | 备注 |
|---|---|---|---|---|---|---|
| `booking.submit_failure.missing_required_elements` | 创建 / 提交预约时缺少客户、门店、时间、项目、资产或手艺人等必要元素。 | customer / staff / artisan / system | `draft` | 是，关联 `submit_booking` | 记录缺失字段、提交主体、入口、校验时间。 | DRAFT / 待 Gate 确认。 |
| `booking.submit_failure.customer_identity_required` | 无法形成系统内客户主体，预约不能进入 hold 或正式链路。 | customer / staff / system | `draft` | 是，关联 `submit_booking` | 记录识别输入、失败原因、是否尝试创建散客主体。 | DRAFT / 待 Gate 确认；客户主体本体归 `biz.customer.profile`。 |
| `booking.submit_failure.store_not_supported` | 选择的门店不支持预约或不可预约。 | customer / staff / system | `draft` | 是，关联 `submit_booking` | 记录门店、预约入口、门店营业 / 配置状态引用。 | DRAFT / 待 Gate 确认。 |
| `booking.submit_failure.project_not_supported_by_store` | 选择项目当前门店不支持或已下架。 | customer / staff / system | `draft` | 是，关联 `submit_booking` | 记录项目、门店、项目快照、校验结果。 | DRAFT / 待 Gate 确认；项目本体归供给目录。 |
| `booking.submit_failure.asset_validation_failed` | 客户资产不可用、已用完、过期或不覆盖预约项目。 | customer / staff / system | `draft` | 是，关联 `submit_booking` | 记录资产引用、资产能力返回结果、是否可转普通项目预约。 | DRAFT / 待 Gate 确认；资产本体归客户资产能力。 |
| `booking.submit_failure.payment_precheck_failed` | 预约提交前支付预检、定金预授权或支付前置校验失败。 | customer / staff / system | `draft` / `pending_store_confirm` | 是，关联 `submit_booking` / `confirm_booking` | 记录支付订单引用、预检阶段、失败原因。 | DRAFT / 待 Gate 确认；支付本体归支付能力。 |
| `booking.submit_failure.policy_not_satisfied` | 提交预约时命中门店、租户或平台策略限制。 | customer / staff / system | `draft` | 是，关联 `submit_booking` | 记录命中的 policy、Can 判定结果、客户可见原因。 | DRAFT / 待 Gate 确认。 |
| `booking.resource_failure.resource_unavailable` | 目标时间段资源不足，无法创建预约 hold。 | customer / staff / system | `draft` | 是，关联 `submit_booking` | 记录资源类型、时间段、校验失败详情。 | DRAFT / 待 Gate 确认；覆盖资源不足场景。 |
| `booking.resource_failure.hold_create_failed` | Qualified Resource Hold 创建失败。 | customer / staff / system | `draft` | 是，关联 `submit_booking` / `resubmit_booking` | 记录 hold 请求、资源快照、失败原因。 | DRAFT / 待 Gate 确认。 |
| `booking.resource_failure.hold_replace_failed` | 改期、改派、门店修改确认时，新 hold 创建或替换失败。 | staff / store_manager / scheduler / system | `pending_store_confirm` / `confirmed` / `arrival_overdue` | 是，关联 `confirm_booking` / `reassign_artisan` / 变更 command | 记录旧 hold、新 hold 请求、替换阶段、失败原因。 | DRAFT / 待 Gate 确认；变更 command 是否独立待确认。 |
| `booking.resource_failure.hold_release_failed` | 取消、no_show、submit_expired 或变更确认时释放旧资源失败。 | customer / staff / store_manager / system | `pending_store_confirm` / `confirmed` / `arrival_overdue` / `assignment_overdue` | 是，关联 `cancel_booking` / `resolve_resource_release_failure` | 记录释放目标、失败资源、原动作、异常处理入口。 | DRAFT / 待 Gate 确认；覆盖系统释放失败。 |
| `booking.resource_failure.artisan_conflict` | 指定手艺人或新手艺人在目标时间段存在冲突。 | customer / staff / store_manager / scheduler / system | `draft` / `confirmed` / `arrival_overdue` | 是，关联 `submit_booking` / `reassign_artisan` | 记录冲突手艺人、冲突预约、是否允许冲突提示后确认。 | DRAFT / 待 Gate 确认。 |
| `booking.resource_failure.room_conflict` | 房间、服务位或整房资源存在冲突。 | customer / staff / store_manager / system | `draft` / `pending_store_confirm` / `confirmed` | 是，关联 `submit_booking` / `confirm_booking` | 记录冲突资源、门店配置、客户或员工确认事实。 | DRAFT / 待 Gate 确认。 |
| `booking.resource_failure.schedule_conflict` | 预约时间与门店日程、手艺人排班或其他预约冲突。 | customer / staff / system | `draft` / `confirmed` | 是，关联 `submit_booking` / 变更 command | 记录冲突时间段、冲突对象、门店宽松配置命中情况。 | DRAFT / 待 Gate 确认。 |
| `booking.resource_failure.resource_policy_blocked` | 资源策略或门店配置拒绝预约、改期、改派或冲突接受。 | customer / staff / store_manager / system | `draft` / `confirmed` / `arrival_overdue` | 是，关联对应 action | 记录 policy、Can 判定、拒绝原因。 | DRAFT / 待 Gate 确认；覆盖审批拒绝 / 策略拒绝。 |
| `booking.store_return.schedule_not_available` | 门店待确认时认为当前时间不可安排，打回客户重新提交。 | store_staff / store_manager | `pending_store_confirm` -> `submit_expired` | 是，关联门店打回 / `confirm_booking` 未成功 | 记录门店操作人、客户可见原因、hold 释放结果。 | DRAFT / 待 Gate 确认。 |
| `booking.store_return.artisan_not_available` | 门店待确认时发现手艺人不可安排，打回客户。 | store_staff / store_manager | `pending_store_confirm` -> `submit_expired` | 是，关联门店打回 | 记录手艺人、原预约信息、门店说明。 | DRAFT / 待 Gate 确认。 |
| `booking.store_return.room_not_available` | 门店待确认时发现房间 / 服务位不可安排，打回客户。 | store_staff / store_manager | `pending_store_confirm` -> `submit_expired` | 是，关联门店打回 | 记录房间 / 服务位、资源释放结果。 | DRAFT / 待 Gate 确认。 |
| `booking.store_return.booking_info_needs_adjustment` | 门店认为预约信息需要客户调整后重新提交。 | store_staff / store_manager | `pending_store_confirm` -> `submit_expired` | 是，关联门店打回 | 记录需调整字段、客户可见说明、内部说明。 | DRAFT / 待 Gate 确认。 |
| `booking.cancel_reason.customer_requested_cancel` | 客户主动取消未到店预约。 | customer | `pending_store_confirm` / `confirmed` / `arrival_overdue` / `assignment_overdue` -> `cancelled` | 是，关联 `cancel_booking` | 记录取消发起方、取消时间、资源释放结果、可选原因。 | DRAFT / 待 Gate 确认；覆盖用户取消。 |
| `booking.cancel_reason.staff_cancel_on_behalf` | 员工根据客户线下沟通代客取消。 | staff / store_manager | 非终态正式预约 -> `cancelled` | 是，关联 `cancel_booking` | 记录员工、权限、线下沟通说明、客户可见原因、资源释放结果。 | DRAFT / 待 Gate 确认。 |
| `booking.cancel_reason.store_schedule_full` | 门店因日程已满或无法安排取消预约。 | store_manager / authorized_staff | 非终态正式预约 -> `cancelled` | 是，关联 `cancel_booking` | 记录门店原因、操作人、客户可见原因、内部审计原因。 | DRAFT / 待 Gate 确认。 |
| `booking.cancel_reason.artisan_unavailable` | 手艺人请假、调班、不可服务且无法替代，导致取消。 | store_manager / system | `confirmed` / `arrival_overdue` / `assignment_overdue` -> `cancelled` | 是，关联 `cancel_booking` / system cancel | 记录手艺人、不可用原因、是否尝试改派。 | DRAFT / 待 Gate 确认。 |
| `booking.cancel_reason.room_unavailable` | 房间 / 服务位不可用且无法替代，导致取消。 | store_manager / system | `confirmed` / `arrival_overdue` -> `cancelled` | 是，关联 `cancel_booking` / system cancel | 记录资源、不可用原因、是否尝试替换。 | DRAFT / 待 Gate 确认。 |
| `booking.cancel_reason.store_closed_or_suspended` | 门店闭店、歇业或暂停营业导致取消。 | store_manager / system | 非终态正式预约 -> `cancelled` | 是，关联 `cancel_booking` / system cancel | 记录门店状态、取消批次、客户通知需求。 | DRAFT / 待 Gate 确认。 |
| `booking.cancel_reason.duplicate_booking` | 重复预约或客户 / 门店确认不需要保留当前预约。 | customer / staff / store_manager | 非终态正式预约 -> `cancelled` | 是，关联 `cancel_booking` | 记录重复对象、保留预约、取消原因。 | DRAFT / 待 Gate 确认。 |
| `booking.cancel_reason.wrong_booking_info` | 预约信息错误，取消后重新预约。 | customer / staff / store_manager | 非终态正式预约 -> `cancelled` | 是，关联 `cancel_booking` | 记录错误字段、是否触发快速重新预约。 | DRAFT / 待 Gate 确认。 |
| `booking.arrival_reason.early_arrival` | 客户早于准时窗口到店并被门店接待。 | store_staff / system | `confirmed` -> `completed` | 是，关联到店 / check-in action，名称待 Gate 确认 | 记录预约时间、实际到店时间、触发来源、服务流绑定。 | DRAFT / 待 Gate 确认。 |
| `booking.arrival_reason.on_time_arrival` | 客户在准时窗口内到店。 | store_staff / system | `confirmed` -> `completed` | 是，关联到店 / check-in action，名称待 Gate 确认 | 记录到店时间、准时窗口配置、服务流绑定。 | DRAFT / 待 Gate 确认。 |
| `booking.arrival_reason.late_arrival` | 客户超过准时窗口但当天仍到店。 | store_staff / system | `arrival_overdue` -> `completed` 或 `confirmed` -> `completed` | 是，关联到店 / check-in action，名称待 Gate 确认 | 记录迟到事实、曾进入 arrival_overdue 的状态历史。 | DRAFT / 待 Gate 确认。 |
| `booking.arrival_reason.arrival_overdue_no_arrival` | 超过后置到店宽限仍未识别到店。 | system | `confirmed` -> `arrival_overdue` | 否 / 系统触发是否 key_action 待 Gate 确认 | 记录触发时间、预约时间、门店、未到店事实。 | DRAFT / 待 Gate 确认。 |
| `booking.arrival_reason.auto_no_show_next_day` | 第二天自动标记爽约。 | system | `arrival_overdue` -> `no_show` | 是 / 是否注册独立 key_action 待 Gate 确认 | 记录自动标记时间、资源释放结果、通知门店事实。 | DRAFT / 待 Gate 确认；覆盖 hold / 资源系统释放。 |
| `booking.arrival_reason.service_flow_bound` | 客户到店并成功创建 / 绑定当天客户服务流动线容器。 | store_staff / system | `confirmed` / `arrival_overdue` / `assignment_overdue` -> `completed` | 是，关联到店 / check-in action，名称待 Gate 确认 | 记录服务流 ID、到店触发来源、完成时间。 | DRAFT / 待 Gate 确认。 |
| `booking.arrival_reason.service_flow_bind_failed` | 客户到店事实存在，但服务流创建 / 绑定失败。 | store_staff / system | 保持原状态 | 是，关联到店 / check-in action，名称待 Gate 确认 | 记录失败阶段、是否回滚到店事实、人工处理入口。 | DRAFT / 待 Gate 确认。 |
| `booking.assignment_failure.manual_assignment_overdue` | 无手艺人预约超过手动分配截止。 | system | `confirmed` | 否 / 系统触发是否 key_action 待 Gate 确认 | 记录手动分配截止时间、预约类型、门店。 | DRAFT / 待 Gate 确认。 |
| `booking.assignment_failure.auto_assignment_failed` | 系统自动分配手艺人失败后进入分配逾期。 | system | `confirmed` -> `assignment_overdue` | 是 / 是否独立 key_action 待 Gate 确认 | 记录候选范围、失败原因、通知门店事实。 | DRAFT / 待 Gate 确认。 |
| `booking.assignment_failure.no_available_artisan` | 无已排班、可服务、无冲突手艺人可分配。 | system / store_manager | `confirmed` / `assignment_overdue` | 是，关联 `assign_artisan` / `resolve_assignment_overdue` | 记录候选条件、排班状态、项目能力要求。 | DRAFT / 待 Gate 确认。 |
| `booking.assignment_failure.artisan_skill_not_matched` | 手艺人能力 / 资质不匹配预约项目。 | store_manager / scheduler / system | `confirmed` / `assignment_overdue` | 是，关联 `assign_artisan` | 记录手艺人、项目、能力校验结果。 | DRAFT / 待 Gate 确认。 |
| `booking.assignment_failure.temporary_take_order_failed` | 店长选择临时接单但处理失败。 | store_manager / scheduler | `assignment_overdue` | 是，关联 `resolve_assignment_overdue` | 记录临时接单原因、失败阶段、操作人。 | DRAFT / 待 Gate 确认。 |
| `booking.assignment_failure.schedule_patch_failed` | 店长选择同时补排班，但补排班失败。 | store_manager / scheduler | `assignment_overdue` | 是，关联 `resolve_assignment_overdue` | 记录补排班请求、排班能力返回结果、是否允许重新选择临时接单。 | DRAFT / 待 Gate 确认。 |
| `booking.reassignment_reason.customer_confirm_required` | 客户主动选定手艺人后，门店改派需客户确认。 | store_manager / scheduler | `confirmed` / `arrival_overdue` | 是，关联 `reassign_artisan` | 记录客户主动选择来源、候选新手艺人、通知客户事实。 | DRAFT / 待 Gate 确认。 |
| `booking.reassignment_reason.customer_confirmed` | 客户确认接受候选改派。 | customer | `confirmed` / `arrival_overdue` | 是，关联 `confirm_artisan_reassignment` | 记录客户确认时间、新旧资源切换、原资源释放结果。 | DRAFT / 待 Gate 确认。 |
| `booking.reassignment_reason.customer_rejected` | 客户拒绝候选改派。 | customer | `confirmed` / `arrival_overdue` | 是，关联 `confirm_artisan_reassignment` | 记录拒绝时间、原预约保持不变、后续处理入口。 | DRAFT / 待 Gate 确认。 |
| `booking.reassignment_reason.customer_confirm_timeout` | 客户未在配置时间内确认候选改派。 | system | `confirmed` / `arrival_overdue` | 是 / 是否独立 key_action 待 Gate 确认 | 记录超时时间、候选安排失效、原安排保持。 | DRAFT / 待 Gate 确认。 |
| `booking.reassignment_reason.candidate_hold_failed` | 改派候选新资源 hold 创建失败。 | store_manager / scheduler / system | `confirmed` / `arrival_overdue` | 是，关联 `reassign_artisan` | 记录候选手艺人、资源校验失败原因。 | DRAFT / 待 Gate 确认。 |
| `booking.reassignment_reason.original_resource_release_failed` | 客户确认改派后释放原资源失败。 | customer / system | `confirmed` / `arrival_overdue` | 是，关联 `confirm_artisan_reassignment` / `resolve_resource_release_failure` | 记录原资源、释放失败原因、异常处理入口。 | DRAFT / 待 Gate 确认。 |
| `booking.reassignment_reason.permission_denied` | 改派或确认改派权限不足。 | staff / store_manager / customer | `confirmed` / `arrival_overdue` | 是，关联 `reassign_artisan` / `confirm_artisan_reassignment` | 记录操作人、权限判定、拒绝原因。 | DRAFT / 待 Gate 确认。 |
| `booking.system_cancel_reason.store_closed` | 门店闭店导致系统取消预约。 | system | 非终态正式预约 -> `cancelled` | 是，关联 system cancel / `cancel_booking` | 记录门店状态、影响预约、客户通知。 | DRAFT / 待 Gate 确认。 |
| `booking.system_cancel_reason.store_suspended` | 门店暂停营业导致系统取消预约。 | system | 非终态正式预约 -> `cancelled` | 是，关联 system cancel / `cancel_booking` | 记录暂停原因、取消批次、通知门店和客户。 | DRAFT / 待 Gate 确认。 |
| `booking.system_cancel_reason.temporary_business_stop` | 门店临时歇业导致系统取消预约。 | system / store_manager | 非终态正式预约 -> `cancelled` | 是，关联 system cancel / `cancel_booking` | 记录歇业时间段、受影响预约、补救尝试。 | DRAFT / 待 Gate 确认。 |
| `booking.system_cancel_reason.artisan_leave_or_shift_change` | 手艺人请假 / 调班且无可替代安排。 | system / store_manager | `confirmed` / `arrival_overdue` -> `cancelled` | 是，关联 system cancel / `cancel_booking` | 记录原手艺人、是否尝试改派、取消原因。 | DRAFT / 待 Gate 确认。 |
| `booking.system_cancel_reason.critical_resource_unavailable` | 关键房间、服务位、设备或整房资源不可用且无替代。 | system / store_manager | 非终态正式预约 -> `cancelled` | 是，关联 system cancel / `cancel_booking` | 记录关键资源、不可用原因、替代失败。 | DRAFT / 待 Gate 确认。 |
| `booking.system_cancel_reason.project_disabled_or_invalid` | 项目被禁用或失效，预约无法继续履约。 | system / store_manager | 非终态正式预约 -> `cancelled` | 是，关联 system cancel / `cancel_booking` | 记录项目、禁用来源、客户通知。 | DRAFT / 待 Gate 确认。 |
| `booking.system_cancel_reason.force_majeure` | 天气、突发事件等不可抗力导致取消。 | system / store_manager | 非终态正式预约 -> `cancelled` | 是，关联 system cancel / `cancel_booking` | 记录事件类型、影响范围、通知结果。 | DRAFT / 待 Gate 确认。 |

## 4. 覆盖说明

| 要求覆盖 | 已覆盖 code |
|---|---|
| 创建 | `booking.submit_failure.*` |
| 确认 | `booking.store_return.*`、`booking.resource_failure.hold_replace_failed`、`booking.submit_failure.payment_precheck_failed` |
| 取消 | `booking.cancel_reason.*`、`booking.system_cancel_reason.*` |
| 改期 | `booking.resource_failure.hold_replace_failed`、`booking.resource_failure.resource_policy_blocked` |
| 资源不足 | `booking.resource_failure.resource_unavailable`、`booking.resource_failure.artisan_conflict`、`booking.resource_failure.room_conflict`、`booking.resource_failure.schedule_conflict` |
| hold 超时 | `booking.resource_failure.hold_release_failed`；submit_expired 的专用 reason_code 是否需要新增待 Gate 确认 |
| 审批拒绝 | `booking.resource_failure.resource_policy_blocked`、`booking.reassignment_reason.permission_denied` |
| 系统释放 | `booking.resource_failure.hold_release_failed`、`booking.arrival_reason.auto_no_show_next_day` |

## 5. 待 Gate 确认问题

| 问题 | 影响 |
|---|---|
| reason_code 命名是否使用 `booking.<domain>.<code>` 三段式 | 影响 `reasoncodes.csv` 和工程错误分支。 |
| submit_expired / hold 超时是否需要独立 reason_code | 影响待门店确认超时和重新提交链路审计。 |
| 到店 / check-in 是否注册独立 key_action，以及其 reason_code 域归属 | 影响 `arrival_reason.*` 的 key_action 标记。 |
| 系统触发类状态变化是否都属于 key_action | 影响 `arrival_overdue`、`auto_no_show`、`auto_assignment_failed` 审计强度。 |
| 审批拒绝是否使用独立 `approval_denied` 域，还是归入 `resource_failure` / `reassignment_reason` | 影响审批能力与 booking 的边界。 |
