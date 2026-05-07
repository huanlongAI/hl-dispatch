# LTC 飞书台账与公告门禁 v0.1

**状态**：R1 飞书门禁规格草案
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：大辉子写入飞书绩效台账和公告前置检查

## 1. 边界

LTC 无飞书写权限。飞书绩效台账和公告只能由大辉子执行。

## 2. 台账写入前置门禁

大辉子写入台账前必须校验：

- evidence reference 存在且可追溯。
- evidence feed 批次签名有效。
- 制度版本有效。
- 字段范围版本有效。
- 制度确认版本有效。
- raw event 未进入输出。
- banned 字段未进入输出。
- 员工说明和申诉状态已关联。
- R4/R5 dry run 不进入正式台账。
- connector dry-run response 不包含 raw request body、raw response body、飞书 payload 或绩效裁决 payload。
- connector dry-run response 只能作为审计证据，不能作为大辉子已消费或飞书已写入证据。

## 3. 公告发布前置门禁

大辉子发布公告前必须校验：

- 公告范围符合制度。
- 不包含 raw event。
- 不包含 banned 字段。
- 不包含不必要个人细节。
- 员工说明状态已关联。
- 需要人工或创始人审批的场景已审批。
- 公告内容只引用 evidence reference 或大辉子裁决结果。

## 4. 阻断条件

以下任一情况必须阻断：

- LTC 试图直接写飞书。
- 公告包含 prompt、completion、文件内容、URL、窗口标题、截图等 banned 字段。
- R4/R5 dry run 被用于正式绩效结论。
- LTC connector dry-run response 被当作真实大辉子消费确认。
- break-chain 被自动转成绩效负面结论。
- 缺制度版本、字段范围版本或确认版本。

## 5. 审计记录

每次台账写入或公告发布必须记录：

- 大辉子执行 ID。
- evidence batch ID。
- evidence reference。
- 制度版本。
- 字段范围版本。
- 确认版本。
- 员工说明状态。
- 审批记录。
- 发布时间。
