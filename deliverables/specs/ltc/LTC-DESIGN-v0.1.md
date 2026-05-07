# LTC 技术设计 v0.1

**状态**：R1 技术设计草案  
**日期**：2026-05-06  
**负责人**：NODE-A  
**范围**：R2 alpha0-lite 到 R5 evidence feed 的技术设计

## 1. 架构原则

- 先 sanitizer，再下游。
- raw observation 只存在于内存候选输入中。
- banned 字段永不落盘、日志化或下游化。
- LTC 不写飞书。
- LTC 不参与资产管理。
- Windows 优先，Mac 第二平台。

## 2. 模块

| 模块 | 职责 |
|---|---|
| `ToolSourceAdapter` | 读取 Codex 订阅和 `heiyucode.com` API key 使用元数据。 |
| `FieldScopePolicy` | 执行 scope-first / banned 字段范围。 |
| `Sanitizer` | 拒绝、转换、hash 和聚合候选输入。 |
| `EndpointRuntime` | 安装、常驻、心跳、健康、断链。 |
| `HardwareProfileCollector` | 采集当前安装电脑硬件配置。 |
| `OwnerView` | 员工自查和说明入口。 |
| `EvidenceFeedPublisher` | 生成签名 evidence feed 批次。 |
| `AuditLog` | 管理员动作、访问、导出、删除和冻结审计。 |

## 3. 数据流

```text
ToolSourceAdapter
  -> raw observation candidate in memory
  -> FieldScopePolicy
  -> Sanitizer
  -> sanitized event
  -> aggregate
  -> evidence reference
  -> EvidenceFeedPublisher
  -> Dahuizi
```

禁止路径：

```text
raw observation -> disk
raw observation -> logs
raw observation -> Feishu
raw observation -> Dahuizi
LTC -> Feishu Ledger
LTC -> Feishu Announcement
```

## 4. R2 alpha0-lite

R2 只实现：

- 合成样本。
- Codex 订阅样本 adapter。
- `heiyucode.com` API key 样本 adapter。
- FieldScopePolicy。
- Sanitizer。
- 本地输出。
- banned 泄漏测试。

R2 不实现：

- 安装。
- 常驻 runtime。
- 真实员工数据。
- 大辉子 evidence feed。
- 飞书台账。

## 5. R3 runtime

R3 实现：

- Windows 公司固定资产电脑 runtime。
- Mac 第二平台 runtime。
- 设备绑定。
- 员工身份绑定。
- 签名心跳。
- 健康检查。
- 硬件配置采集。
- owner view 原型。

R3 不实现：

- MDM。
- 资产管理。
- 飞书写入。
- 正式绩效集成。

## 6. evidence feed

批次字段：

- `batchId`
- `period`
- `schemaVersion`
- `policyVersion`
- `fieldScopeVersion`
- `consentVersion`
- `items`
- `signature`
- `generatedAt`

幂等规则：

- `batchId` 相同的重试不得重复记账。
- 批次签名失败必须拒绝。
- 缺制度版本、字段范围版本或确认版本必须拒绝。

## 7. 日志规范

日志允许：

- event code。
- reason code。
- status code。
- hash ID。
- 时间戳。
- 计数。

日志禁止：

- raw observation。
- prompt。
- completion。
- transcript。
- 文件内容。
- URL。
- 窗口标题。
- 明文 API key。
- 完整命令参数。

## 8. 实现前置

进入 R2 实现前必须完成：

- 本文审查。
- TDD 矩阵审查。
- 验收 manifest 审查。
- 字段范围审查。
- 工具来源登记审查。
