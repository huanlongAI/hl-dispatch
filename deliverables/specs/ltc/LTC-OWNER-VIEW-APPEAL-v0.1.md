# LTC Owner View 与申诉规格 v0.1

**状态**：R1 员工自查规格草案
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：员工 owner view、异常说明、申诉路径

## 1. 目标

员工必须能查看 LTC 对自身相关的字段类别、制度版本、确认版本、端点状态、断链记录和说明入口。

Owner View 不提供关闭、退出、卸载或绕过 LTC 的能力。

## 2. 可见信息

| 类别 | 可见内容 |
|---|---|
| 制度 | 制度版本、制度确认版本、字段范围版本。 |
| 端点 | 安装状态、绑定状态、运行状态、健康状态、agent 版本。 |
| 字段 | 字段类别、字段说明、banned 字段说明。 |
| 证据 | evidence reference 摘要，不展示 raw observation。 |
| 断链 | 断链开始、结束、原因、说明状态。 |
| 说明 | 员工提交的 amendment / explanation 状态与 hash reference。 |
| 申诉 | 申诉入口、状态、处理记录。 |

## 3. 不可见信息

Owner View 不展示：

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
- 其他员工信息。

## 4. 员工说明

员工说明规则：

- 说明以 amendment / explanation 关联证据。
- 说明不改写已签名 evidence。
- 说明明文不得进入 owner view、evidence feed、日志、错误或测试快照。
- owner view 只保存 note hash、amendment ID hash、evidence hash 关联和处理状态。
- evidence package 可见性只展示状态和 hash，不展示 evidence signature 明文或 raw evidence。
- 说明状态进入大辉子 evidence feed。
- 飞书公告前必须检查说明状态。

## 5. 申诉路径

申诉至少包含：

- 申诉对象。
- 关联 evidence reference。
- 申诉理由。
- 附加说明。
- 提交时间。
- 处理状态。
- 处理记录。

申诉 SLA 需要在制度版本中参数化：

- 首次响应时限。
- 处理时限。
- 升级路径。
- 关闭条件。

## 6. 验收

- 员工可看到字段类别和制度版本。
- 员工不可看到 raw observation 或 banned 字段。
- 员工可以提交说明。
- 说明不改写 evidence。
- 说明 amendment 只保存 hash reference，不保存明文。
- owner view 展示 evidence package 状态和说明入口。
- 申诉状态可被大辉子引用。
