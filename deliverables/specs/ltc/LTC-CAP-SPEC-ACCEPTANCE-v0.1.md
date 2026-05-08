# LTC 验收场景 v0.1

**状态**：R1 验收规格草案
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：LTC Cap-Spec 验收场景明细

## 1. 验收总则

验收必须覆盖字段安全、runtime 边界、员工自查、大辉子 evidence feed、飞书门禁和资产边界。

## 2. 验收场景

| ID | 场景 | 阶段 | 预期 |
|---|---|---|---|
| AC-001 | Codex 订阅合成样本进入 sanitizer。 | R2 | 输出只包含字段范围内元数据。 |
| AC-002 | `heiyucode.com` API key 合成样本进入 sanitizer。 | R2 | 明文 API key、请求体、响应体不出现。 |
| AC-003 | 输入包含 prompt / completion / transcript。 | R2 | 事件被拒绝；输出、日志、错误和 metrics 均不含 banned 值。 |
| AC-004 | 输入包含 URL、窗口标题、文件路径、剪贴板或按键。 | R2 | 事件被拒绝或转换；banned 值不落盘。 |
| AC-005 | 采集当前安装电脑硬件配置。 | R3 | 只输出硬件配置元数据和 hash，不出现资产管理字段。 |
| AC-006 | Windows 公司固定资产电脑安装并绑定。 | R3 | 端点进入 Running，心跳签名。 |
| AC-007 | Mac 公司固定资产电脑安装并绑定。 | R3 | 端点进入 Running，心跳签名。 |
| AC-008 | 员工尝试本地关闭 / 卸载 / 绕过。 | R3 | 本地不可执行；若发生异常则记录断链或合规事件。 |
| AC-009 | 员工个人电脑未强制安装。 | R3 | 不计入强制覆盖范围；自愿安装不作制度规定。 |
| AC-010 | raw observation 被尝试写入日志。 | R3 | 测试失败；实现必须阻断。 |
| AC-011 | 心跳缺失。 | R3 | 创建 BreakChainIncident，owner view 和 evidence feed 可见。 |
| AC-012 | 员工提交说明。 | R4 | 说明以 amendment / explanation 关联，不改写 evidence。 |
| AC-013 | 管理员停用端点。 | R4 | 管理动作签名并进入审计。 |
| AC-014 | R4 dry run 被写入正式绩效台账。 | R4 | 流程阻断。 |
| AC-015 | LTC 生成大辉子 evidence feed dry-run 消费计划。 | R5 | 只证明 LTC 可生成 sanitized aggregate、evidence reference 和 dry-run delivery plan；不证明大辉子已消费。 |
| AC-016 | 大辉子写飞书台账。 | R6 | 只有大辉子执行；LTC 无飞书写权限。 |
| AC-017 | 飞书公告包含 raw event 或 banned 字段。 | R6 | 公告阻断。 |
| AC-018 | break-chain 被自动转成绩效负面。 | R6 | 流程阻断；只能作为证据完整性 / 合规状态输入。 |

## 3. 验收输出

每个验收场景必须输出：

- 测试命令。
- 输入样本说明。
- 预期输出 schema。
- banned 泄漏检查结果。
- 通过 / 失败证据。

没有验收证据，不得进入下一阶段。
