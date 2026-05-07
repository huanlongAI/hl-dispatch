# LTC 旧 P0 文档处置评估 v0.1

**状态**：安全删除评估结论  
**日期**：2026-05-06  
**负责人**：NODE-A  
**范围**：`huanlong/ltc-endpoint` 旧 P0 reset package

## 1. 评估结论

结论：当前不安全删除。

理由：

- 旧 P0 reset package 包含创始人裁决、法务 / 运营通过记录、字段白名单、测试计划、状态快照和 CI 迁移记录。
- 旧 P0 中存在大量已被新基线替代的口径，但它们也是漂移审计证据。
- `ltc-endpoint` 是独立仓库，当前 R1 规格主线落在 `hl-dispatch`；跨仓库删除需要单独执行和审计。
- 删除旧文档可能破坏历史 commit、交接记录、README 引用和测试证据链。

## 2. 推荐处置

本轮采用“历史保留 + 活跃基线索引替代”方案：

- 保留旧 P0 文档。
- 在 `hl-dispatch` 建立 `LTC-ACTIVE-BASELINE-INDEX-v0.1.md`。
- 新基线明确废止旧 P0 中与当前裁决冲突的口径。
- 后续如要清理 `ltc-endpoint`，优先改 README / AGENTS / reset package 首页，标注 Historical Only / Superseded。

## 3. 已废止旧口径

| 旧口径 | 新口径 |
|---|---|
| LTC 不用于 HR / 绩效。 | LTC 是大辉子绩效管理的正式证据输入，但不直接裁决绩效。 |
| 员工可以停止 endpoint agent。 | 公司固定资产电脑上的 LTC 员工无本地关闭、退出、卸载或绕过权限。 |
| 不安装 runtime。 | R3 起进入公司固定资产电脑 runtime，Windows 优先，Mac 第二平台。 |
| 不实现 daemon / collector。 | R3 起实现端点哨兵 runtime；但仍禁止 banned 字段和 raw observation 落盘。 |
| 不接入 evidence feed。 | R5 接入大辉子 evidence feed；R4/R5 不进入正式绩效台账或公告。 |
| alpha0-lite local-only 是长期边界。 | alpha0-lite 只是 R2 字段安全验证切片。 |

## 4. 永久保留边界

- 不采集 prompt。
- 不采集 completion。
- 不采集 transcript。
- 不采集文件内容。
- 不采集 URL。
- 不采集窗口标题。
- 不采集剪贴板。
- 不采集按键。
- 不截图或屏幕录制。
- 不采集非工程应用清单。
- LTC 不直接输出绩效分、员工排名、薪酬建议或纪律处分结论。

## 5. 后续安全删除条件

只有同时满足以下条件，才可以考虑删除旧 P0 文档：

- `ltc-endpoint` 仓库拥有明确写入授权。
- 所有旧文档引用已迁移到 active baseline 索引。
- 历史审计证据已在替代位置保全。
- CI、README、AGENTS、DEPS 不再引用被删除路径。
- 删除行为有单独 commit 和说明。

在条件未满足前，只允许标注 Historical Only / Superseded，不直接删除。
