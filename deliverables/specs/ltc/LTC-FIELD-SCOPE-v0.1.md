# LTC 字段范围规格 v0.1

**状态**：R1 字段范围规格草案
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：scope-first / banned 字段模型

## 1. 原则

创始人裁决：字段可以先行，在采集范围内尽量齐全。字段齐全不改变 banned 字段永久禁止边界。

字段必须：

- 写入字段范围版本。
- 员工 owner view 可见。
- 通过 banned 泄漏测试。
- 支持禁用和回滚。
- 不包含内容值。

## 2. 基础允许字段

| 字段 | 说明 |
|---|---|
| `toolName` | 工具名。 |
| `toolVersion` | 工具版本。 |
| `provider` | 工具提供方。 |
| `modelId` | 模型标识。 |
| `inputTokens` | 输入 token 数。 |
| `outputTokens` | 输出 token 数。 |
| `requestCount` | 请求次数。 |
| `windowStart` | 聚合窗口开始。 |
| `windowEnd` | 聚合窗口结束。 |
| `durationSec` | 持续时间秒数。 |
| `machineIdHash` | 设备标识 hash。 |
| `userId` | 员工工程身份。 |
| `agentVersion` | LTC agent 版本。 |
| `recordedAt` | 记录时间。 |
| `degradationLevel` | 降级等级。 |
| `breakChainReason` | 断链原因。 |
| `consentVersion` | 制度确认版本。 |
| `policyVersion` | 制度版本。 |

## 3. 硬件配置字段

| 字段 | 说明 | 限制 |
|---|---|---|
| `osName` | 操作系统名。 | 仅 Windows / macOS。 |
| `osVersion` | 操作系统版本。 | 不含用户名、主机路径。 |
| `machineModel` | 设备型号。 | 不表示资产归属。 |
| `cpuModel` | CPU 型号。 | 只采集型号。 |
| `memoryGB` | 内存容量。 | 数值。 |
| `diskCapacityGB` | 磁盘总容量。 | 数值，不采文件列表。 |
| `gpuModel` | GPU 型号。 | 可为空。 |
| `hardwareFingerprintHash` | 硬件指纹 hash。 | 不可逆 hash。 |

## 4. scope-first 字段

| 字段 | 说明 | 限制 |
|---|---|---|
| `processName` | 工程白名单进程名。 | 只限批准工具，不采非工程应用清单。 |
| `foregroundBackgroundState` | 批准工具前后台状态。 | 不推断空闲、离开或休息。 |
| `cwdHash` | 工作目录 hash。 | 不保存路径明文，不可逆。 |
| `fileCount` | 文件数量。 | 不含文件名。 |
| `linesAdded` | 新增行数。 | 聚合数字，不含 patch。 |
| `linesRemoved` | 删除行数。 | 聚合数字，不含 patch。 |
| `testFileCount` | 测试文件数量。 | 不含文件名。 |
| `repoHash` | 仓库 hash。 | 不保存仓库路径或 URL。 |
| `branchHash` | 分支 hash。 | 不保存分支明文。 |
| `taskId` | 任务 ID。 | 只能来自任务系统，不从本机内容推断。 |
| `issueId` | Issue ID。 | 只能来自 GitHub 或任务系统。 |
| `prId` | PR ID。 | 只能来自 GitHub 或任务系统。 |
| `subscriptionIdHash` | Codex 订阅标识 hash。 | 不保存明文订阅标识。 |
| `apiKeyIdHash` | API key 标识 hash。 | 不保存明文密钥。 |
| `apiHost` | API host。 | 当前只允许 `heiyucode.com`。 |
| `keyUsageCount` | API key 调用次数。 | 不含请求内容。 |
| `quotaConsumed` | 配额消耗。 | 可取得才记录，不推断内容。 |

## 5. 大辉子 evidence envelope 字段

| 字段 | 说明 | 限制 |
|---|---|---|
| `schemaVersion` | evidence envelope schema 版本。 | 只表示证据包格式版本。 |
| `producer` | 生产方。 | 当前固定为 `ltc-endpoint`。 |
| `consumer` | 消费方。 | 当前固定为 `dahuizi`。 |
| `ltcRole` | LTC 角色。 | 固定为 `evidence_producer_only`。 |
| `performanceAuthority` | 绩效裁决权归属。 | 固定为 `dahuizi`，LTC 不裁决。 |
| `feishuWriteMode` | 飞书写入模式。 | 固定为 `not_written_by_ltc`。 |
| `toolEvidenceCount` | 工具证据引用数量。 | 计数，不含 raw event。 |
| `toolEvidence` | 工具证据引用列表。 | 只含 sanitized aggregate 和 hash reference。 |
| `evidenceHash` | 证据包 hash。 | 不可逆 hash。 |
| `evidenceSignature` | 证据包签名。 | 不包含 signing key 明文。 |
| `deliveryMode` | 交付模式。 | 当前固定为 dry run。 |
| `deliveryStatus` | 交付状态。 | 当前固定为 evidence held，不表示真实消费。 |
| `idempotencyKey` | 幂等键。 | 基于 evidence hash 生成。 |
| `networkAction` | 网络动作状态。 | 当前固定为 `not_executed_by_ltc`。 |
| `retryRequired` | 是否需要重试。 | 只用于 dry-run plan。 |
| `retryPolicy` | 重试策略。 | 只含策略参数，不执行网络请求。 |
| `deliverySignature` | delivery plan 签名。 | 不包含 signing key 明文。 |
| `rawDataIncluded` | 是否含 raw 数据。 | 固定为 false。 |

## 6. Windows Endpoint Alpha verification 字段

| 字段 | 说明 | 限制 |
|---|---|---|
| `serviceNameHash` | Windows service name 的 hash。 | 不保存 service name 明文。 |
| `runningStatus` | 外部 Windows runner 观察到的运行状态。 | 只允许状态枚举，不含命令输出。 |
| `startupMode` | 外部 Windows runner 观察到的 startup mode。 | 当前 alpha 只接受 `auto`。 |
| `timestampBucket` | 观察时间桶。 | 不保存 PowerShell transcript。 |
| `heartbeatSignatureState` | heartbeat signature 是否存在。 | 只保存 state，不保存签名明文。 |
| `heartbeatSignatureHash` | heartbeat signature hash。 | canonical SHA-256。 |
| `servicePlanIdHash` | service plan hash。 | 不含 service binary path。 |
| `runnerIdHash` | verification runner hash。 | 不保存 runner ID 明文。 |
| `observationHash` | alpha observation hash。 | 不可逆 hash。 |

## 7. Windows installer manifest 字段

| 字段 | 说明 | 限制 |
|---|---|---|
| `installerVersion` | installer artifact 版本。 | 不表示已构建真实安装包。 |
| `servicePlanHash` | service plan hash。 | 不含 raw service path。 |
| `signingPolicy` | 签名策略。 | 不包含 signing key。 |
| `companyAssetScope` | 公司固定资产部署范围。 | 个人电脑不进入强制范围。 |
| `manifestHash` | installer manifest hash。 | 不可逆 hash。 |
| `installExecutionClaim` | 安装执行声明。 | 当前固定为 `not_executed_by_ltc`。 |
| `windowsBuildVerification` | Windows 构建验证要求。 | 当前固定为后续 Windows 验证机门禁。 |

## 8. Endpoint evidence chain summary 字段

| 字段 | 说明 | 限制 |
|---|---|---|
| `chainHash` | evidence chain 摘要 hash。 | 不可逆 hash。 |
| `segmentHashes` | heartbeat / service observation / admin action / owner amendment / evidence envelope 分段 hash。 | 不包含 raw segment。 |
| `reasonCodes` | evidence chain 原因码列表。 | 不含绩效原因或 HR 标签。 |
| `evidenceMutation` | evidence 是否被改写。 | 当前固定为 `not_permitted`。 |
| `performanceImpact` | 绩效影响。 | 当前固定为 `not_evaluated_by_ltc`。 |

## 9. DahuiZi connector response v2 dry-run ack 字段

| 字段 | 说明 | 限制 |
|---|---|---|
| `ackHash` | connector ack hash。 | 不包含 raw response body。 |
| `ackSignatureHash` | connector ack signature hash。 | 不保存 signing key 或签名明文。 |
| `requestHash` | dry-run request shape hash。 | 不包含 raw request body。 |
| `responseStatus` | 本地 dry-run observation status。 | 固定为本地状态，不透传大辉子真实响应。 |

## 10. banned 字段

以下字段永久禁止：

- prompt text。
- completion text。
- transcript。
- source file content。
- patch content。
- full command arguments。
- command output。
- PowerShell transcript。
- shell history。
- URL。
- window title。
- document path。
- clipboard。
- keystroke。
- screenshot。
- screen recording。
- browser history。
- non-engineering app inventory。
- idle / away inference。
- break time。
- employee ranking。
- performance score。
- performance decision。
- performance judgment。
- performance grade。
- performance rank。
- salary suggestion。
- salary adjustment。
- disciplinary decision。
- disciplinary action。
- Feishu ledger record。
- Feishu announcement。
- Feishu write payload。
- raw local path。
- raw service path。
- service binary path。
- raw request body。
- raw response body。
- operator ID 明文。
- HR label。
- subjective work attitude metric。

## 11. 字段门禁

- 字段进入采集前必须出现在本规格或后续字段范围版本中。
- 字段不得通过日志、错误消息、debug dump、metrics label 或测试快照泄漏 banned 值。
- 字段扩展必须更新制度版本、字段范围版本和制度确认版本。
- 字段扩展必须能回滚。
