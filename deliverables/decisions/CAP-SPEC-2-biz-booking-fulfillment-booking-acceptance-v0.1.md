# Cap-Spec-2｜biz.booking.fulfillment / booking Acceptance Scenarios v0.1

> 状态：DRAFT，等待 Founder / Gate 审查
> 范围：仅 booking（预约）子段，不覆盖 fulfillment（履约）
> 当前不写代码，不作为工程开工输入
> 本文只写业务验收场景，不写代码测试；涉及状态、key_action、reason_code 的正式命名均待 Gate 确认。

## 1. 上游引用

- `hl-dispatch/deliverables/decisions/HL-FIRST-CAPABILITY-PACKS-UPSTREAM-v0.6.md`
- `hl-dispatch/deliverables/decisions/PM-CODEX-START-GUIDE-FIRST-CAPABILITY-PACKS-v0.1.md`
- `hl-dispatch/deliverables/decisions/CAP-SPEC-1-biz-booking-fulfillment-booking-v0.2.md`
- `hl-dispatch/deliverables/decisions/CONTRACT-GAP-biz-booking-fulfillment-booking-v0.1.md`

## 2. 验收说明

每条场景均用于 Founder / Gate / PM 审查 booking 业务语义是否清楚，不代表工程测试代码已经存在。

`reason_code` 采用 Cap-Spec-1 v0.2 中的 PM 草稿原因域和原因码；正式 code 是否进入 `reasoncodes.csv` 待 Gate 确认。

## 3. 验收场景

### 场景 1：客户正常创建门店项目预约并自动确认

- 前置条件：
  - 客户已有系统内 `customer_id`。
  - 门店开启“客户预约免门店确认”。
  - 客户选择门店项目、预约时间，并确认系统推荐或客户选择的手艺人。
  - 目标时间段资源可用，Qualified Resource Hold 可创建。
- 操作步骤：
  - 客户在自助端提交预约。
  - 系统执行必要元素校验、项目可预约校验、手艺人 / 房间 / 服务位资源校验。
  - 系统创建 Qualified Resource Hold，并按门店配置自动确认。
- 预期结果：
  - 生成正式预约单编号。
  - 预约状态进入 `confirmed`。
  - hold 转为正式预约占用，并保留 `hold_id -> booking_id` 追溯关系。
  - 客户和门店可查看已确认预约详情。
- 涉及状态：
  - `draft -> confirmed`
- 涉及 key_action：
  - `submit_booking`
- 涉及 reason_code：
  - 成功场景无失败 reason_code。
  - 自动确认事实对应 reason_code / audit fact 命名待 Gate 确认。
- 是否需要审计证据：
  - 是。需记录客户提交、资源校验、hold 创建、系统按门店配置自动确认。

### 场景 2：员工代客创建仅门店预约

- 前置条件：
  - 员工具备代客预约权限。
  - 客户已有系统内 `customer_id`；若为散客，已创建散客客户主体。
  - 员工选择门店和到店时间，不选择项目和手艺人。
- 操作步骤：
  - 员工创建仅门店预约。
  - 系统按到店时间 + 默认接待时长生成可排程日程。
  - 员工确认提交。
- 预期结果：
  - 生成正式预约单编号。
  - 预约模式为 `store_visit`。
  - 预约状态进入 `confirmed`。
  - 生成门店默认半小时日程，具体默认值待 Gate 确认。
- 涉及状态：
  - `draft -> confirmed`
- 涉及 key_action：
  - `create_booking`（生成业务草稿时）
  - `submit_booking`
- 涉及 reason_code：
  - 成功场景无失败 reason_code。
- 是否需要审计证据：
  - 是。需记录员工、客户、门店、时间、创建入口、代客事实。

### 场景 3：AI Draft 后 GUI 人工确认生成预约

- 前置条件：
  - 自然交互识别到预约意图。
  - 系统能够识别或创建系统内客户主体。
  - AI Draft 已生成，但尚未成为正式预约事实。
- 操作步骤：
  - AI 生成预约草稿，补齐或引导补齐客户、门店、时间、项目 / 手艺人等必要元素。
  - GUI 展示正式生效影响、资源状态和风险提示。
  - 客户或授权员工在 GUI 中确认提交。
- 预期结果：
  - AI Draft 不直接生成正式预约。
  - 人工确认后执行 `submit_booking`。
  - 资源校验成功时创建 Qualified Resource Hold。
  - 根据门店配置进入 `pending_store_confirm` 或 `confirmed`。
- 涉及状态：
  - `draft -> pending_store_confirm` 或 `draft -> confirmed`
- 涉及 key_action：
  - `create_booking`（生成 AI Draft / 草稿记录时）
  - `submit_booking`
- 涉及 reason_code：
  - `submit_failure.missing_required_elements`（待 Gate 确认）：必要元素缺失。
  - `submit_failure.customer_identity_required`（待 Gate 确认）：无法形成客户主体。
- 是否需要审计证据：
  - 是。需记录 AI Draft 输入来源、人工确认人、确认内容、资源校验结果。

### 场景 4：资源 hold 创建成功但尚未正式确认

- 前置条件：
  - 客户提交预约。
  - 门店关闭客户预约免确认，预约需要进入 `pending_store_confirm`。
  - 资源校验通过，Qualified Resource Hold 创建成功。
- 操作步骤：
  - 客户提交预约。
  - 系统创建 Qualified Resource Hold。
  - 系统向门店展示待确认预约和倒计时。
- 预期结果：
  - 生成正式预约单编号。
  - 预约状态进入 `pending_store_confirm`。
  - 客户侧和门店端展示确认倒计时。
  - 资源在 hold TTL 内被短时暂占。
- 涉及状态：
  - `draft -> pending_store_confirm`
- 涉及 key_action：
  - `submit_booking`
- 涉及 reason_code：
  - 成功场景无失败 reason_code。
- 是否需要审计证据：
  - 是。需记录 hold 创建、TTL、预约单编号、客户提交事实。

### 场景 5：资源不足导致提交失败

- 前置条件：
  - 客户或员工提交预约。
  - 目标时间段手艺人、房间、服务位或其他关键资源不可用。
- 操作步骤：
  - 发起 `submit_booking`。
  - 系统执行资源校验。
  - 资源校验失败或 hold 创建失败。
- 预期结果：
  - 不生成已确认预约。
  - 不进入 `pending_store_confirm` 或 `confirmed`。
  - 如果已有草稿，草稿保持可编辑或返回提交失败。
  - 用户 / 员工看到明确失败原因和可重新选择入口。
- 涉及状态：
  - `draft -> draft` 或提交失败不改变状态。
- 涉及 key_action：
  - `submit_booking`
- 涉及 reason_code：
  - `submit_failure.resource_unavailable`（待 Gate 确认）
  - `resource_failure.hold_create_failed`（待 Gate 确认）
  - `resource_failure.artisan_conflict` / `room_conflict` / `schedule_conflict`（按失败对象，待 Gate 确认）
- 是否需要审计证据：
  - 是。需记录提交人、失败阶段、资源校验结果、reason_code。

### 场景 6：hold 超时释放并进入提交过期

- 前置条件：
  - 预约处于 `pending_store_confirm`。
  - 门店未在 hold TTL 内确认。
  - 当前 hold 可释放。
- 操作步骤：
  - 系统触发 confirm timeout。
  - 系统释放当前预约资源 hold。
  - 系统标记原提交链路结束。
- 预期结果：
  - 预约状态进入 `submit_expired`。
  - 原 hold 被释放。
  - 客户可以基于原信息重新提交，但必须生成新预约单和新 hold。
  - 原预约单保持 `submit_expired`，不可恢复。
- 涉及状态：
  - `pending_store_confirm -> submit_expired`
- 涉及 key_action：
  - `resubmit_booking`（后续重新提交时）
  - 超时释放触发是否作为独立 key_action 待 Gate 确认。
- 涉及 reason_code：
  - `store_return.schedule_not_available` 不适用，仅门店打回时使用，待 Gate 确认。
  - `resource_failure.hold_release_failed`（释放失败时，待 Gate 确认）
- 是否需要审计证据：
  - 是。需记录超时时间、资源释放结果、原预约与后续新预约链路。

### 场景 7：客户未到店前取消预约

- 前置条件：
  - 预约处于 `pending_store_confirm`、`confirmed`、`arrival_overdue` 或 `assignment_overdue`。
  - 客户尚未到店，预约未进入终态。
  - 预约资源可释放。
- 操作步骤：
  - 客户在自助端点击取消预约。
  - 系统执行权限和状态校验。
  - 系统释放预约资源。
- 预期结果：
  - 资源释放成功后，预约进入 `cancelled`。
  - 客户取消原因可选填。
  - 门店端收到预约取消通知。
  - 支付、定金、资产释放 / 退款按对应能力处理，不阻塞预约终态。
- 涉及状态：
  - `pending_store_confirm -> cancelled`
  - `confirmed -> cancelled`
  - `arrival_overdue -> cancelled`
  - `assignment_overdue -> cancelled`
- 涉及 key_action：
  - `cancel_booking`
- 涉及 reason_code：
  - `cancel_reason.customer_requested_cancel`（待 Gate 确认）
  - `resource_failure.hold_release_failed`（释放失败时，待 Gate 确认）
- 是否需要审计证据：
  - 是。需记录取消发起方、取消时间、资源释放结果、可选取消原因。

### 场景 8：员工代客改期成功

- 前置条件：
  - 预约处于 `confirmed`。
  - 客户尚未到店。
  - 员工具备代客变更权限。
  - 新时间段资源可用。
- 操作步骤：
  - 员工根据线下沟通发起改期。
  - 系统校验新时间、新手艺人 / 房间 / 服务位资源。
  - 系统创建新 hold。
  - 员工确认变更。
- 预期结果：
  - 预约保留主记录或业务编号，并生成变更版本。
  - 新 hold 确认成功后释放旧资源。
  - 当前预约展示新时间。
  - 变更历史可追溯。
- 涉及状态：
  - `confirmed -> confirmed`
- 涉及 key_action：
  - 预约变更 command 是否单列 action_type 待 Gate 确认。
  - 可关联 `submit_booking` / `confirm_booking` / `reassign_artisan` 的资源替换审计，待 Gate 确认。
- 涉及 reason_code：
  - 成功场景无失败 reason_code。
  - `resource_failure.hold_replace_failed`（替换失败时，待 Gate 确认）
  - 高风险审批拒绝 reason_code 待 Gate 确认。
- 是否需要审计证据：
  - 是。需记录原时间、新时间、操作人、线下沟通说明、新旧资源替换关系。

### 场景 9：门店打回客户重新提交

- 前置条件：
  - 客户自助预约处于 `pending_store_confirm`。
  - 门店判断当前预约信息需要调整，且不直接修改确认。
  - 当前 hold 可释放。
- 操作步骤：
  - 门店填写不确认 / 打回原因。
  - 系统释放当前 hold。
  - 客户收到重新提交提示。
- 预期结果：
  - 原提交链路进入 `submit_expired`。
  - 客户可基于原信息重新编辑并重新提交。
  - 重新提交必须重新校验并创建新 hold。
- 涉及状态：
  - `pending_store_confirm -> submit_expired`
- 涉及 key_action：
  - `confirm_booking` 不执行成功。
  - 打回动作是否独立 key_action 待 Gate 确认；PM 草稿倾向作为关键治理动作审计。
- 涉及 reason_code：
  - `store_return.booking_info_needs_adjustment`（待 Gate 确认）
  - `store_return.artisan_not_available` / `room_not_available` / `schedule_not_available`（按原因，待 Gate 确认）
- 是否需要审计证据：
  - 是。需记录门店操作人、打回原因、资源释放结果、客户可见说明。

### 场景 10：门店修改客户预约后直接确认

- 前置条件：
  - 客户自助预约处于 `pending_store_confirm`。
  - 门店已与客户线下沟通一致。
  - 门店需要修改时间、手艺人、房间或项目等预约信息。
- 操作步骤：
  - 门店修改预约信息。
  - 系统重新校验资源并创建 / 替换 hold。
  - 门店填写修改原因 / 线下沟通说明并确认。
- 预期结果：
  - 预约进入 `confirmed`。
  - 客户侧展示门店调整后的最新预约信息和客户可见变更摘要。
  - 内部审计保留客户原提交、门店修改后确认、旧 / 新 hold 替换关系。
- 涉及状态：
  - `pending_store_confirm -> confirmed`
- 涉及 key_action：
  - `confirm_booking`
- 涉及 reason_code：
  - 成功场景无失败 reason_code。
  - `resource_failure.hold_replace_failed`（替换失败时，待 Gate 确认）
- 是否需要审计证据：
  - 是。需记录修改前后差异、沟通说明、操作人、资源替换链路。

### 场景 11：审批失败导致高风险变更不可执行

- 前置条件：
  - 员工或门店发起高风险预约变更，例如临近服务开始、跨门店、影响其他预约或涉及高风险资源。
  - 该变更命中审批规则。
  - 审批未通过或规则直接拒绝。
- 操作步骤：
  - 操作人提交变更请求。
  - 系统执行 Can 判定和审批 / 拒绝规则。
  - 审批失败或被拒绝。
- 预期结果：
  - 原预约保持不变。
  - 新 hold 如已创建但未确认，应释放或失效。
  - 操作人看到审批失败 / 不允许变更原因。
- 涉及状态：
  - `confirmed -> confirmed`
  - `arrival_overdue -> arrival_overdue`
- 涉及 key_action：
  - 预约变更 command 是否独立 key_action 待 Gate 确认。
  - 相关资源动作可能涉及 `reassign_artisan`。
- 涉及 reason_code：
  - `resource_failure.resource_policy_blocked`（待 Gate 确认）
  - `reassignment_reason.permission_denied`（改派权限不足时，待 Gate 确认）
  - 审批拒绝 reason_code 待 Gate 确认。
- 是否需要审计证据：
  - 是。需记录 Can 判定、审批结果、拒绝原因、操作人、原预约未变更事实。

### 场景 12：审计证据留存覆盖完整预约链路

- 前置条件：
  - 存在一条从客户自助提交到已确认、到店完成的预约链路。
  - 链路中包含资源 hold、确认、到店、服务流绑定。
- 操作步骤：
  - 审查该预约的关键业务节点。
  - 核对每个 key_action 是否有审计事实引用。
  - 核对预约单是否只保存审计摘要和审计引用，而非完整审计日志。
- 预期结果：
  - 可以追溯谁、何时、基于什么输入、确认了什么。
  - 可以追溯 hold 创建、hold 消耗、预约确认、到店事实、服务流绑定。
  - 如果存在失败、取消、打回、异常，可追溯 reason_code、reason_text、customer_visible_reason。
- 涉及状态：
  - `draft -> pending_store_confirm / confirmed -> completed`
- 涉及 key_action：
  - `create_booking`
  - `submit_booking`
  - `confirm_booking`
  - 到店 / check-in 对应 key_action 名称待 Gate 确认
- 涉及 reason_code：
  - 成功链路无失败 reason_code。
  - 审计 fact / evidence 字段命名待 Gate 确认。
- 是否需要审计证据：
  - 是。该场景本身用于验收审计证据留存。

### 场景 13：无手艺人预约分配逾期后人工处理

- 前置条件：
  - 客户资产预约未选择手艺人，预约模式为 `service_unassigned`。
  - 预约已进入 `confirmed`。
  - 超过手动分配截止时间后，系统自动分配失败。
- 操作步骤：
  - 系统将预约标记为分配逾期。
  - 店长或排班负责人进入分配逾期处理页。
  - 店长手动分配可服务手艺人，或选择临时接单 / 补排班处理。
- 预期结果：
  - 自动分配失败后进入 `assignment_overdue`。
  - 人工处理并成功分配后回到 `confirmed`。
  - 若涉及临时接单 / 补排班，记录高风险审计或审批结果。
- 涉及状态：
  - `confirmed -> assignment_overdue -> confirmed`
- 涉及 key_action：
  - `assign_artisan`
  - `resolve_assignment_overdue`
- 涉及 reason_code：
  - `assignment_failure.auto_assignment_failed`（待 Gate 确认）
  - `assignment_failure.no_available_artisan`（待 Gate 确认）
- 是否需要审计证据：
  - 是。需记录自动分配失败、人工处理人、分配结果、是否临时接单 / 补排班。

### 场景 14：客户逾期未到后当天到店完成预约

- 前置条件：
  - 预约处于 `arrival_overdue`。
  - 预约尚未进入 `no_show`。
  - 客户当天到店并完成客户识别。
- 操作步骤：
  - 门店通过生物识别、GUI 点击到店、开始服务或到店新开单据触发到店事实。
  - 系统创建 / 绑定当天客户服务流动线容器。
- 预期结果：
  - 预约进入 `completed`。
  - 预约详情保留曾进入 `arrival_overdue` 的历史。
  - 记录 `late_arrival` 或逾期到店标签。
- 涉及状态：
  - `arrival_overdue -> completed`
- 涉及 key_action：
  - 到店 / check-in 对应 key_action 名称待 Gate 确认。
- 涉及 reason_code：
  - `arrival_reason.late_arrival`（待 Gate 确认）
  - `arrival_reason.service_flow_bound`（待 Gate 确认）
- 是否需要审计证据：
  - 是。需记录预约时间、实际到店时间、触发来源、服务流绑定结果。

### 场景 15：第二天自动标记爽约

- 前置条件：
  - 预约处于 `arrival_overdue`。
  - 预约当天结束后客户仍未到店。
  - 预约资源可释放。
- 操作步骤：
  - 系统在第二天触发自动爽约规则。
  - 系统释放预约资源。
  - 系统标记预约为爽约。
- 预期结果：
  - 预约进入 `no_show`。
  - 原预约不可恢复。
  - 第二天或之后客户到店，按无预约服务流处理。
- 涉及状态：
  - `arrival_overdue -> no_show`
- 涉及 key_action：
  - 自动 no_show 是否注册独立 key_action 待 Gate 确认。
- 涉及 reason_code：
  - `arrival_reason.auto_no_show_next_day`（待 Gate 确认）
  - `resource_failure.hold_release_failed`（释放失败时，待 Gate 确认）
- 是否需要审计证据：
  - 是。需记录自动标记时间、资源释放结果、通知门店事实。

### 场景 16：快速预约成功

- 前置条件：
  - 来源为历史已完成服务 / 履约记录或已取消预约。
  - 门店开放客户自助快速预约入口，或员工端具备代客快速预约权限。
  - 用户只重新选择时间。
  - 原项目、手艺人、门店、资产 / 支付状态重新校验通过。
- 操作步骤：
  - 用户点击快速预约入口。
  - 系统带入原预约 / 服务信息并展示确认页。
  - 用户选择新时间并确认。
- 预期结果：
  - 生成全新预约，不复用原预约编号。
  - 创建新 hold。
  - 新预约保留来源预约 / 来源服务记录引用。
- 涉及状态：
  - 终态来源记录保持原终态。
  - 新链路进入 `draft -> confirmed` 或 `draft -> pending_store_confirm`。
- 涉及 key_action：
  - `create_booking`
  - `submit_booking`
- 涉及 reason_code：
  - 成功场景无失败 reason_code。
- 是否需要审计证据：
  - 是。需记录来源对象、新预约编号、重新校验结果、新 hold。

### 场景 17：快速预约因原资源不可用失败

- 前置条件：
  - 用户从已取消预约或历史完成服务发起快速预约。
  - 原手艺人当前不可预约，或原项目已下架 / 门店不再支持，或原资产不可用。
- 操作步骤：
  - 系统执行快速预约重新校验。
  - 校验失败。
- 预期结果：
  - 不生成正式预约单。
  - 不默认保留草稿。
  - 系统提示失败原因和下一步入口，例如重新选时间、换手艺人、换项目或进入普通预约流程。
  - 原资产不可用时，可提示转为普通项目预约并进入支付链路，该口径待 Gate 确认。
- 涉及状态：
  - 来源预约 / 服务记录状态不变。
  - 新预约链路不进入正式状态。
- 涉及 key_action：
  - `create_booking` 是否生成草稿取决于是否保存业务记录，待 Gate 确认。
- 涉及 reason_code：
  - `submit_failure.project_not_supported_by_store`（待 Gate 确认）
  - `submit_failure.resource_unavailable`（待 Gate 确认）
  - `submit_failure.asset_validation_failed`（待 Gate 确认）
- 是否需要审计证据：
  - 是。需至少记录失败原因和来源对象；是否生成业务草稿审计待 Gate 确认。

### 场景 18：第三方平台预约到店后实际核销项目不同

- 前置条件：
  - 门店根据第三方平台订单为客户创建预约。
  - 预约节点保存预定核销项目 A。
  - 客户到店后实际核销项目为 B。
- 操作步骤：
  - 门店完成客户到店识别。
  - 后续核销 / 服务流节点记录实际核销项目 B。
- 预期结果：
  - 预约节点保留 `intended_redemption_project=A`。
  - 实际核销节点记录 `actual_redemption_project=B`。
  - 不覆盖原预约意向。
  - 两个节点之间保留链路关系。
- 涉及状态：
  - `confirmed -> completed`
- 涉及 key_action：
  - 到店 / check-in 对应 key_action 名称待 Gate 确认。
  - 核销动作本体不在 booking 中定义。
- 涉及 reason_code：
  - 成功场景无失败 reason_code。
  - 预定项目与实际核销项目不一致是否需要 reason_code 待 Gate 确认。
- 是否需要审计证据：
  - 是。需记录预约意向、实际核销引用和不可覆盖链路。

## 4. 覆盖矩阵

| 最低要求 | 覆盖场景 |
|---|---|
| 客户正常创建预约 | 场景 1 |
| 员工代客创建预约 | 场景 2 |
| AI Draft 后人工确认 | 场景 3 |
| 资源 hold 成功 | 场景 4 |
| 资源不足 | 场景 5 |
| hold 超时释放 | 场景 6 |
| 用户取消预约 | 场景 7 |
| 员工改期 | 场景 8 |
| 门店拒绝或审批失败 | 场景 9、场景 11 |
| 审计证据留存 | 场景 12 |
