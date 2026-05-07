# LTC 留存与访问控制 v0.1

**状态**：R1 留存访问规格草案
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：evidence、审计、owner view 和大辉子消费

## 1. 原则

留存和访问必须最小化、可审计、可冻结、可删除。raw observation 和 banned 字段不进入留存范围。

## 2. 证据类别

| 类别 | 是否留存 | 说明 |
|---|---|---|
| raw observation | 否 | 仅内存候选输入。 |
| sanitized event | 是 | 下游最小事件。 |
| aggregate | 是 | 聚合指标。 |
| evidence reference | 是 | 大辉子和飞书台账引用。 |
| audit log | 是 | 管理员、大辉子、审计访问记录。 |
| employee explanation | 是 | 员工说明和申诉材料。 |

## 3. 访问角色

| 角色 | 可见范围 |
|---|---|
| 员工 | 自身字段类别、制度版本、确认版本、端点状态、断链、说明状态。 |
| 管理员 | 设备运行状态、安装绑定、健康、管理员动作审计。 |
| 大辉子 | sanitized event、aggregate、evidence reference、断链摘要、说明状态。 |
| 创始人 | 管理视图和裁决所需证据引用。 |
| 审计者 | 访问日志、签名、留存、版本一致性。 |

## 4. 禁止访问

任何角色都不得访问：

- raw observation。
- prompt。
- completion。
- transcript。
- 文件内容。
- URL。
- 窗口标题。
- 剪贴板。
- 按键。
- 截图。
- 屏幕录制。

## 5. 留存策略待参数化

以下参数需要在 R3 前落入制度版本：

- sanitized event 留存期限。
- aggregate 留存期限。
- evidence reference 留存期限。
- audit log 留存期限。
- employee explanation 留存期限。
- 申诉冻结期限。
- 审计冻结解除条件。

默认草案：

- R2 合成样本：随测试产物保留。
- R3/R4 试点证据：短期保留，需单独制度参数。
- R5/R6 正式证据：按绩效周期和公司制度留存。

## 6. 导出控制

- 默认禁止导出。
- 审计导出需要创始人或授权审计角色批准。
- 导出必须脱敏，并记录导出人、时间、范围和目的。
- 导出不得包含 raw observation 或 banned 字段。

## 7. 删除与冻结

- 无申诉、无审计冻结、达到留存期限后可删除。
- 员工申诉期间冻结相关 evidence reference、审计日志和说明。
- 审计期间冻结相关 evidence reference 和访问日志。
- 删除动作必须签名并进入审计。
