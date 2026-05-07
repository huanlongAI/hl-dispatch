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
| `LTC_EVT_WINDOWS_SERVICE_EXECUTION_VERIFIED` | Windows service 外部执行观察结果已验证。 |
| `LTC_EVT_WINDOWS_SERVICE_VERIFIED` | Windows service 外部观察结果已验证。 |
| `LTC_EVT_HEARTBEAT_SIGNED` | 心跳已签名。 |
| `LTC_EVT_HEALTH_REPORTED` | 健康状态已上报。 |
| `LTC_EVT_HARDWARE_PROFILE_RECORDED` | 当前安装电脑硬件配置已记录。 |
| `LTC_EVT_TOOL_SOURCE_OBSERVED` | 已观察工具来源元数据。 |
| `LTC_EVT_TELEMETRY_REJECTED` | 遥测候选被拒绝。 |
| `LTC_EVT_EVIDENCE_SANITIZED` | 证据已清洗。 |
| `LTC_EVT_DAHUIZI_EVIDENCE_READY` | 大辉子 evidence envelope 已生成；仅表示 LTC 产出证据包，不表示大辉子已消费或飞书已写入。 |
| `LTC_EVT_DAHUIZI_DELIVERY_DRY_RUN_PREPARED` | 大辉子 dry-run delivery plan 已生成；不表示真实网络调用完成。 |
| `LTC_EVT_EVIDENCE_BATCH_PUBLISHED` | evidence feed 批次已发布。 |
| `LTC_EVT_BREAK_CHAIN_DETECTED` | 断链已检测。 |
| `LTC_EVT_BREAK_CHAIN_EXPLAINED` | 员工已提交断链说明。 |
| `LTC_EVT_ADMIN_ACTION_RECORDED` | 管理员动作已记录。 |
| `LTC_EVT_OWNER_VIEW_OPENED` | 员工打开 owner view。 |
| `LTC_EVT_FEISHU_GATE_CHECKED` | 飞书门禁已检查。 |

## 2. 原因码

| Reason Code | 说明 |
|---|---|
| `LTC_REASON_HEARTBEAT_MISSING` | 心跳缺失。 |
| `LTC_REASON_AGENT_DEGRADED` | agent 降级。 |
| `LTC_REASON_ADMIN_DISABLED` | 管理员停用。 |
| `LTC_REASON_ADMIN_UNINSTALLED` | 管理员卸载。 |
| `LTC_REASON_LOCAL_TAMPER_ATTEMPT` | 本地绕过或篡改尝试。 |
| `LTC_REASON_BANNED_FIELD_PRESENT` | 候选输入存在 banned 字段。 |
| `LTC_REASON_RAW_BOUNDARY_VIOLATION` | raw observation 边界违规。 |
| `LTC_REASON_FIELD_SCOPE_MISSING` | 字段未进入字段范围版本。 |
| `LTC_REASON_TOOL_SOURCE_UNREGISTERED` | 工具来源未登记。 |
| `LTC_REASON_NOT_COMPANY_ASSET` | 候选设备不是公司固定资产，不进入强制 runtime。 |
| `LTC_REASON_PLATFORM_UNSUPPORTED` | 候选设备平台不在 Windows / macOS 支持范围内。 |
| `LTC_REASON_INSTALL_PRECONDITION_MISSING` | 行政与制度前置流程未完成，不进入安装绑定。 |
| `LTC_REASON_SIGNING_KEY_MISSING` | runtime 绑定缺少签名密钥，不能生成可信心跳。 |
| `LTC_REASON_WINDOWS_VERIFICATION_ENV_REQUIRED` | Windows service 验证必须在 Windows 验证环境或可信观察结果中完成。 |
| `LTC_REASON_SERVICE_OBSERVATION_UNTRUSTED` | Windows service 观察结果缺少 running / auto / heartbeat signature 等必要事实。 |
| `LTC_REASON_SERVICE_PLAN_INVALID` | Windows service 计划形状或前置字段无效，不能进入执行契约。 |
| `LTC_REASON_EVIDENCE_ENVELOPE_INVALID` | 大辉子 evidence envelope 形状、hash 或签名缺失。 |
| `LTC_REASON_ADMIN_CONTROL_NOT_IN_R3_MINIMAL_SCOPE` | 管理员停用 / 卸载不在 R3 minimal runtime core 当前切片内。 |
| `LTC_REASON_FEISHU_GATE_BLOCKED` | 飞书门禁阻断。 |
| `LTC_REASON_DRY_RUN_ISOLATION` | dry run 隔离阻断。 |

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
| `LTC_STATUS_EVIDENCE_HELD` | evidence 因版本或确认问题暂挂。 |
| `LTC_STATUS_BREAK_CHAIN_OPEN` | 断链打开。 |
| `LTC_STATUS_BREAK_CHAIN_RESOLVED` | 断链已解决。 |

## 4. 命名规则

- 事件码只描述事实，不描述绩效结论。
- 原因码不得包含员工态度、绩效等级或 HR 标签。
- 状态码不得表达薪酬、纪律或排名。
- 飞书相关状态只表示门禁结果，不表示 LTC 拥有飞书写权限。
