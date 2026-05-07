# LTC 活跃基线索引 v0.1

**状态**：R0/R1 活跃基线索引
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：LTC-Endpoint 新基线与旧 P0 文档处置

## 1. 活跃基线

以下文档构成 LTC 当前活跃产品与规格基线：

| 类型 | 文件 | 用途 |
|---|---|---|
| 治理 | `LTC-GOVERNANCE-REBASELINE-v0.1.md` | 定义 LTC 新定位、永久禁止字段、runtime 和飞书边界。 |
| 领域 | `LTC-DOMAIN-MODEL-v0.1.md` | 定义 DDD 限界上下文、聚合、领域事件和状态机。 |
| 能力 | `LTC-CAP-SPEC-v0.1.md` | 定义能力边界、业务规则和验收场景。 |
| 裁决 | `LTC-DECISION-CHECKLIST-v0.1.md` | 记录 C1-C14 创始人裁决。 |
| 路线图 | `LTC-IMPLEMENTATION-ROADMAP-v0.1.md` | 定义 R0-R6 分阶段交付和门禁。 |
| HPRD | `LTC-HPRD-v0.1.md` | 定义人类可审阅的产品需求。 |
| 技术设计 | `LTC-DESIGN-v0.1.md` | 定义 R1 技术方案和 R2/R3 实现边界。 |
| 字段 | `LTC-FIELD-SCOPE-v0.1.md` | 定义 scope-first / banned 字段范围。 |
| 工具来源 | `LTC-TOOL-SOURCE-REGISTRY-v0.1.md` | 定义 Codex 订阅和 `heiyucode.com` API 密钥使用登记。 |
| 验收 | `LTC-CAP-SPEC-ACCEPTANCE-v0.1.md` | 定义验收场景明细。 |
| 事件码 | `LTC-EVENT-REASON-CODES-v0.1.md` | 定义事件码、原因码、状态码。 |
| 测试 | `LTC-TDD-MATRIX-v0.1.md` | 定义 RED-GREEN 测试矩阵。 |
| Manifest | `LTC-ACCEPTANCE-MANIFEST.yaml` | 机器可读验收清单。 |
| 留存访问 | `LTC-RETENTION-ACCESS-CONTROL-v0.1.md` | 定义留存、访问、导出、冻结和审计。 |
| 飞书门禁 | `LTC-FEISHU-GATE-v0.1.md` | 定义大辉子写台账和公告前置门禁。 |
| Owner View | `LTC-OWNER-VIEW-APPEAL-v0.1.md` | 定义员工自查、说明和申诉路径。 |
| 平台 runtime | `LTC-PLATFORM-RUNTIME-SPEC-v0.1.md` | 定义 Windows 优先、Mac 第二平台的 runtime 规格。 |
| 旧 P0 处置 | `LTC-P0-DISPOSITION-ASSESSMENT-v0.1.md` | 定义旧 P0 文档安全删除评估。 |

## 2. 旧 P0 文档处置

旧 P0 文档位于：

- `/Users/node-a/Workspace/01_Repos/huanlong/ltc-endpoint/docs/reset-package/2026-04-23/`
- `/Users/node-a/Workspace/01_Repos/huanlong/ltc-endpoint/README.md`
- `/Users/node-a/Workspace/01_Repos/huanlong/ltc-endpoint/AGENTS.md`
- `/Users/node-a/Workspace/01_Repos/huanlong/ltc-endpoint/DEPS.md`

处置口径：

- 不在本轮直接删除旧 P0 文档。
- 旧 P0 文档含审计、裁决、状态、CI、测试依据和迁移链路，当前不满足安全删除条件。
- 旧 P0 中的“不用于 HR / 绩效”“员工可以停止 endpoint agent”“不安装 runtime”“不实现 daemon / collector”等口径已被新基线替代。
- 旧 P0 中的 banned 字段边界和 LTC 不直接绩效裁决边界继续保留。

## 3. 执行规则

- 新工作必须引用本索引中的活跃基线。
- 不得把旧 P0 当作当前产品边界。
- 如必须读取旧 P0，只能作为历史证据和漂移来源，不作为实现授权。
- 旧 P0 删除、移动或标注需要单独在 `ltc-endpoint` 仓库执行，并遵守该仓库写入权限和审计要求。
