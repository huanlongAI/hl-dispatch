# LTC 事件码 / 原因码 / 状态码 v0.1

**状态**：R1 代码表草案
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：LTC evidence、runtime、字段、断链和飞书门禁

## 1. 事件码

| Event Code | 说明 |
|---|---|
| `LTC_EVT_ENDPOINT_INSTALLED` | 端点已安装。 |
| `LTC_EVT_ENDPOINT_BOUND` | 端点已绑定员工工程身份。 |
| `LTC_EVT_WINDOWS_SERVICE_PLAN_CREATED` | Windows service 计划已生成，但尚未表示真实服务注册完成。 |
| `LTC_EVT_WINDOWS_SERVICE_EXECUTION_CONTRACT_CREATED` | Windows service 外部管理员执行契约已生成。 |
| `LTC_EVT_WINDOWS_SERVICE_EXECUTION_OBSERVATION_ACCEPTED` | Windows service 外部执行观察结果形状已接受；不表示真实安装执行完成。 |
| `LTC_EVT_WINDOWS_SERVICE_OBSERVATION_ACCEPTED` | Windows service 外部观察结果形状已接受；不表示真实服务注册或运行完成。 |
| `LTC_EVT_WINDOWS_SERVICE_VERIFICATION_RUNNER_CONTRACT_CREATED` | Windows service 外部验证运行器契约已生成；不执行真实服务命令。 |
| `LTC_EVT_WINDOWS_SERVICE_RUNNER_OBSERVATION_ACCEPTED` | Windows service runner 观察结果形状已接受；service registration / startup persistence claim 固定为 LTC 不声明。 |
| `LTC_EVT_WINDOWS_SERVICE_ALPHA_OBSERVATION_VERIFIED` | Windows Endpoint Alpha sanitized observation 已校验；只表示外部 Windows 观察证据形状可信，不表示 LTC 执行了服务注册。 |
| `LTC_EVT_WINDOWS_INSTALLER_MANIFEST_CREATED` | Windows installer artifact manifest 已生成；不表示真实安装包已构建或安装已执行。 |
| `LTC_EVT_WINDOWS_INSTALLER_MANIFEST_VALIDATED` | Windows installer artifact manifest 已校验；不表示真实安装包已构建或安装已执行。 |
| `LTC_EVT_HEARTBEAT_SIGNED` | 心跳已签名。 |
| `LTC_EVT_HEALTH_REPORTED` | 健康状态已上报。 |
| `LTC_EVT_ENDPOINT_EVIDENCE_CHAIN_SUMMARIZED` | Endpoint evidence chain hash-only 摘要已生成；不包含绩效结论。 |
| `LTC_EVT_HARDWARE_PROFILE_RECORDED` | 当前安装电脑硬件配置已记录。 |
| `LTC_EVT_TOOL_SOURCE_OBSERVED` | 已观察工具来源元数据。 |
| `LTC_EVT_TELEMETRY_REJECTED` | 遥测候选被拒绝。 |
| `LTC_EVT_EVIDENCE_SANITIZED` | 证据已清洗。 |
| `LTC_EVT_DAHUIZI_EVIDENCE_READY` | 大辉子 evidence envelope 已生成；仅表示 LTC 产出证据包，不表示大辉子已消费或飞书已写入。 |
| `LTC_EVT_DAHUIZI_DELIVERY_DRY_RUN_PREPARED` | 大辉子 dry-run delivery plan 已生成；不表示真实网络调用完成。 |
| `LTC_EVT_DAHUIZI_CONNECTOR_ACK_DRY_RUN_VERIFIED` | DahuiZi connector v2 dry-run ack 已校验；不表示真实大辉子消费。 |
| `LTC_EVT_EVIDENCE_BATCH_PUBLISHED` | evidence feed 批次已发布。 |
| `LTC_EVT_BREAK_CHAIN_DETECTED` | 断链已检测。 |
| `LTC_EVT_BREAK_CHAIN_EXPLAINED` | 员工已提交断链说明。 |
| `LTC_EVT_ADMIN_ACTION_RECORDED` | 管理员动作已记录。 |
| `LTC_EVT_OWNER_VIEW_OPENED` | 员工打开 owner view。 |
| `LTC_EVT_OWNER_EXPLANATION_AMENDMENT_RECORDED` | 员工说明 amendment 已以 hash-only 方式关联 evidence package；不覆盖原 evidence。 |
| `LTC_EVT_FEISHU_GATE_CHECKED` | 飞书门禁已检查。 |

## 2. 原因码

| Reason Code | 说明 |
|---|---|
| `LTC_REASON_HEARTBEAT_MISSING` | 心跳缺失。 |
| `LTC_REASON_AGENT_DEGRADED` | agent 降级。 |
| `LTC_REASON_ADMIN_DISABLED` | 管理员停用。 |
| `LTC_REASON_ADMIN_UNINSTALLED` | 管理员卸载。 |
| `LTC_REASON_LOCAL_TAMPER_ATTEMPT` | 本地绕过或篡改尝试。 |
| `LTC_REASON_SOURCE_ALLOWED` | 工具来源已登记且未发现 banned 字段。 |
| `LTC_REASON_BANNED_FIELD_PRESENT` | 候选输入存在 banned 字段。 |
| `LTC_REASON_RAW_BOUNDARY_VIOLATION` | raw observation 边界违规。 |
| `LTC_REASON_FIELD_SCOPE_MISSING` | 字段未进入字段范围版本。 |
| `LTC_REASON_TOOL_SOURCE_UNREGISTERED` | 工具来源未登记。 |
| `LTC_REASON_NOT_COMPANY_ASSET` | 候选设备不是公司固定资产，不进入强制 runtime。 |
| `LTC_REASON_PLATFORM_UNSUPPORTED` | 候选设备平台不在 Windows / macOS 支持范围内。 |
| `LTC_REASON_INSTALL_PRECONDITION_MISSING` | 行政与制度前置流程未完成，不进入安装绑定。 |
| `LTC_REASON_SIGNING_KEY_MISSING` | runtime 绑定缺少签名密钥，不能生成可信心跳。 |
| `LTC_REASON_WINDOWS_VERIFICATION_ENV_REQUIRED` | Windows service 验证必须在 Windows 验证环境或可信观察结果中完成。 |
| `LTC_REASON_WINDOWS_OBSERVATION_VERIFIED` | Windows Endpoint Alpha sanitized observation 已通过 hash-only 校验。 |
| `LTC_REASON_SERVICE_OBSERVATION_UNTRUSTED` | Windows service 观察结果缺少 running / auto / heartbeat signature 等必要事实。 |
| `LTC_REASON_SERVICE_PLAN_INVALID` | Windows service 计划形状或前置字段无效，不能进入执行契约。 |
| `LTC_REASON_INSTALLER_MANIFEST_INVALID` | Windows installer artifact manifest 缺少版本、service plan hash、签名策略、公司固定资产范围或 hash 字段无效。 |
| `LTC_REASON_HEARTBEAT_SIGNATURE_MISSING` | evidence chain summary 缺少签名 heartbeat，不能进入 healthy chain。 |
| `LTC_REASON_EVIDENCE_ENVELOPE_INVALID` | 大辉子 evidence envelope 形状、hash 或签名缺失。 |
| `LTC_REASON_EVIDENCE_GOVERNANCE_MISSING` | evidence envelope 缺少制度版本、字段范围版本、确认版本或期间。 |
| `LTC_REASON_ADMIN_CONTROL_NOT_IN_R3_MINIMAL_SCOPE` | 管理员停用 / 卸载不在 R3 minimal runtime core 当前切片内。 |
| `LTC_REASON_ADMIN_ACTION_UNSUPPORTED` | 管理员动作类型未登记，不能记录为 LTC 管理动作。 |
| `LTC_REASON_FEISHU_GATE_BLOCKED` | 飞书门禁阻断。 |
| `LTC_REASON_DRY_RUN_ISOLATION` | dry run 隔离阻断。 |
| `LTC_REASON_DAHUIZI_DRY_RUN_PLAN_INVALID` | DahuiZi dry-run delivery plan 缺少 evidence hash、signature hash、idempotency key 或 retry policy。 |
| `LTC_REASON_DAHUIZI_DRY_RUN_RESPONSE_INVALID` | DahuiZi connector dry-run response status 未登记或响应形状无效。 |
| `LTC_REASON_DAHUIZI_ACK_INVALID` | DahuiZi connector v2 ack 缺少 evidence hash、idempotency key、signature 或与 dry-run plan 不匹配。 |
| `LTC_REASON_OWNER_AMENDMENT_INVALID` | 员工说明 amendment 缺少 evidence hash、canonical note hash 或 amendment id。 |

## 3. 状态码

| Status Code | 说明 |
|---|---|
| `LTC_STATUS_NOT_INSTALLED` | 未安装。 |
| `LTC_STATUS_INSTALLED` | 已安装。 |
| `LTC_STATUS_BOUND` | 已绑定。 |
| `LTC_STATUS_RUNNING` | 运行中。 |
| `LTC_STATUS_DEGRADED` | 降级。 |
| `LTC_STATUS_ADMIN_DISABLED` | 管理员停用。 |
| `LTC_STATUS_ADMIN_UNINSTALLED` | 管理员卸载。 |
| `LTC_STATUS_EVIDENCE_READY` | evidence package 已生成并可作为 hash reference 展示；不表示下游已消费。 |
| `LTC_STATUS_EVIDENCE_HELD` | evidence 因版本或确认问题暂挂。 |
| `LTC_STATUS_EXTERNAL_OBSERVATION_RECORDED` | 外部观察结果已记录为证据；不表示 LTC 声明真实服务、安装或开机自启完成。 |
| `LTC_STATUS_VERIFICATION_NOT_RUN` | 当前环境未运行 Windows 验证。 |
| `LTC_STATUS_CHAIN_HEALTHY` | evidence chain summary 处于健康状态；不表示绩效结论。 |
| `LTC_STATUS_CHAIN_HEALTHY_WITH_ADMIN_ACTION` | evidence chain summary 处于健康状态并包含管理员动作证据；不表示绩效结论。 |
| `LTC_STATUS_CHAIN_DEGRADED` | evidence chain summary 降级，不能作为完整健康链。 |
| `LTC_STATUS_CHAIN_BREAK_OPEN` | evidence chain summary 存在断链。 |
| `LTC_STATUS_AMENDMENT_LINKED` | 员工说明 amendment 已以 hash-only 方式关联。 |
| `LTC_STATUS_BREAK_CHAIN_OPEN` | 断链打开。 |
| `LTC_STATUS_BREAK_CHAIN_RESOLVED` | 断链已解决。 |

## 4. 命名规则

- 事件码只描述事实，不描述绩效结论。
- 原因码不得包含员工态度、绩效等级或 HR 标签。
- 状态码不得表达薪酬、纪律或排名。
- 飞书相关状态只表示门禁结果，不表示 LTC 拥有飞书写权限。
