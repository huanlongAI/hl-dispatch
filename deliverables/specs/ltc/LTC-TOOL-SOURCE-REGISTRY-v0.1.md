# LTC 工具来源登记 v0.1

**状态**：R1 工具来源规格草案  
**日期**：2026-05-06  
**负责人**：NODE-A  
**范围**：Codex 订阅、`heiyucode.com` API 密钥使用、硬件配置与内部证据模型来源

## 1. 登记原则

未登记工具来源不得进入 sanitizer。工具来源必须通过 banned 泄漏测试后，才能进入 R2 以后阶段。

## 2. 首批来源

| Source ID | 来源 | 采集目标 | 禁止 |
|---|---|---|---|
| `SRC-CODEX-SUBSCRIPTION` | Codex 订阅 | 订阅使用元数据、工具版本、模型、token、请求次数、时间窗口。 | prompt、completion、transcript、命令参数、文件内容。 |
| `SRC-HEIYUCODE-API-KEY` | `heiyucode.com` API 密钥 | API key 使用元数据、调用次数、配额消耗、模型、时间窗口。 | 明文 API key、请求体、响应体、URL 路径、prompt、completion。 |
| `SRC-HARDWARE-PROFILE` | 当前安装电脑硬件配置 | 操作系统、机型、CPU、内存、磁盘、GPU 和硬件指纹 hash。 | 资产归属、人工资产编号、分配员工、序列号明文。 |
| `SRC-WINDOWS-SERVICE-OBSERVATION` | Windows service 外部观察结果 | running、auto、service plan hash、heartbeat signature 等可信观察事实。 | shell command、PowerShell transcript、raw command output。 |
| `SRC-OWNER-VIEW-INPUT` | owner view 内部聚合输入 | runtime、断链、管理员动作状态和硬件摘要。 | 员工说明明文、管理员理由明文、绩效结论。 |
| `SRC-DAHUIZI-EVIDENCE-INPUT` | 大辉子 evidence envelope 内部聚合输入 | sanitized aggregate、hash reference、runtime/health/admin/owner 状态摘要。 | raw event、绩效裁决 payload、飞书写入 payload。 |

## 3. 登记字段

- `sourceId`
- `toolName`
- `toolVersion`
- `provider`
- `collectionMethod`
- `fieldMappingVersion`
- `allowedFields`
- `bannedLeakageTestStatus`
- `approvedAt`
- `approvedBy`
- `rollbackPlan`

## 4. Codex 订阅来源

允许：

- `toolName`
- `toolVersion`
- `provider`
- `modelId`
- `subscriptionIdHash`
- `inputTokens`
- `outputTokens`
- `requestCount`
- `windowStart`
- `windowEnd`

禁止：

- prompt。
- completion。
- transcript。
- shell command argument。
- project path。
- file content。
- URL。

## 5. `heiyucode.com` API 密钥来源

允许：

- `apiHost`，固定为 `heiyucode.com`。
- `apiKeyIdHash`。
- `modelId`。
- `keyUsageCount`。
- `quotaConsumed`。
- `requestCount`。
- `windowStart`。
- `windowEnd`。

禁止：

- 明文 API key。
- 请求体。
- 响应体。
- prompt。
- completion。
- URL path 或 query。
- IP 地址，除非后续制度单独批准。

## 6. R2 合成样本要求

R2 不读取真实员工 runtime 数据。R2 只使用合成样本：

- Codex 订阅使用安全样本。
- `heiyucode.com` API key 使用安全样本。
- 含 banned 字段的负样本。
- 日志、错误、metrics、debug dump 泄漏负样本。

合成样本必须能证明 sanitizer 缺失时 RED 失败，sanitizer 完成后 GREEN 通过。

## 7. R5 大辉子证据来源要求

`SRC-DAHUIZI-EVIDENCE-INPUT` 是 LTC 内部证据聚合来源，不代表真实大辉子接口调用。

允许：

- sanitized tool usage aggregate。
- evidence hash reference。
- runtime status。
- health status。
- admin action status。
- owner view state。
- endpoint / machine / hardware hash。
- envelope hash。
- envelope signature。
- dry-run delivery mode。
- idempotency key。
- retry policy。
- delivery signature。

禁止：

- raw event。
- raw prompt / completion / transcript。
- raw local path。
- performance decision / judgment。
- Feishu ledger record。
- Feishu announcement。
- Feishu write payload。

R5 draft GREEN 只证明 LTC 可生成签名证据包；不证明大辉子已消费、不证明飞书已写入、不证明绩效集成已完成。

R5 dry-run delivery GREEN 只证明 LTC 可生成幂等交付计划和重试策略；不证明真实网络调用完成。
