# LTC TDD 矩阵 v0.1

**状态**：R1 测试矩阵草案  
**日期**：2026-05-06  
**负责人**：NODE-A  
**范围**：R2-R6 测试驱动开发矩阵

## 1. TDD 原则

实现前必须先有失败测试。没有 RED，不写生产代码。

## 2. R2 alpha0-lite 测试

| Test ID | RED 条件 | GREEN 条件 |
|---|---|---|
| TDD-R2-001 | sanitizer 缺失时 Codex 订阅样本泄漏 banned 字段。 | 输出仅包含字段范围内元数据。 |
| TDD-R2-002 | sanitizer 缺失时 `heiyucode.com` API 样本泄漏明文 key 或请求体。 | 输出只包含 key hash、host、调用次数和配额元数据。 |
| TDD-R2-003 | 日志包含 prompt / completion。 | 日志不包含 banned 值。 |
| TDD-R2-004 | metrics label 包含 URL 或文件路径。 | metrics label 不包含 banned 值。 |
| TDD-R2-005 | 未登记工具来源进入 sanitizer。 | 事件被拒绝。 |

## 3. R3 runtime 测试

| Test ID | RED 条件 | GREEN 条件 |
|---|---|---|
| TDD-R3-001 | Windows 端点无法安装或绑定。 | 公司固定资产 Windows 电脑安装、绑定、心跳成功。 |
| TDD-R3-002 | Mac 端点无法安装或绑定。 | 公司固定资产 Mac 电脑安装、绑定、心跳成功。 |
| TDD-R3-003 | raw observation 写入磁盘。 | raw observation 仅内存存在。 |
| TDD-R3-004 | 硬件配置包含资产管理字段。 | 只包含硬件配置元数据和 hash。 |
| TDD-R3-005 | 员工本地可关闭或卸载。 | 本地关闭 / 卸载不可用，异常进入断链。 |
| TDD-R3-006 | 员工个人电脑被强制纳入 runtime。 | 个人电脑不进入强制 runtime，返回非公司固定资产原因码。 |
| TDD-R3-007 | 缺少 signing key 仍能绑定并生成心跳。 | 绑定前拒绝，返回签名密钥缺失原因码。 |
| TDD-R3-008 | service adapter 嵌入 `sc.exe` / PowerShell 等真实执行命令。 | 只生成声明式 service plan，不执行命令。 |
| TDD-R3-009 | 非 Windows 环境声称 service verification 完成。 | 返回 Windows 验证环境缺失原因码。 |
| TDD-R3-010 | service observation 缺少 heartbeat signature 仍被验证。 | 返回 service observation 不可信原因码。 |
| TDD-R3-011 | 员工角色创建 service execution contract。 | 返回本地篡改尝试原因码。 |
| TDD-R3-012 | execution contract 包含真实 shell commands 或 raw operator ID。 | 只包含 hash、动作清单和观察字段，不含命令或明文操作者。 |
| TDD-R3-013 | service execution observation 包含 raw command output 或 PowerShell transcript。 | 观察结果被 banned 字段门禁拒绝。 |
| TDD-R3-014 | 心跳缺失或超时未产生断链。 | 产生 BreakChainIncident，状态为 break-chain open。 |
| TDD-R3-015 | 断链自动成为绩效负面。 | 断链仅表示 evidence 完整性 / 合规状态，绩效由大辉子裁决。 |
| TDD-R3-016 | owner view 泄漏员工说明明文。 | owner view 只显示状态和说明入口，员工说明只保留 hash。 |
| TDD-R3-017 | 管理员停用 / 卸载无签名审计。 | 管理员动作生成签名审计事实。 |
| TDD-R3-018 | 员工角色记录管理员动作。 | 返回本地篡改尝试原因码。 |
| TDD-R3-019 | 管理员卸载审计模型执行本地卸载。 | 只记录审计事实，不执行本地卸载。 |
| TDD-R3-020 | owner view 泄漏管理员 ID 或理由明文。 | owner view 只显示状态和 hash。 |
| TDD-R3-021 | owner view 聚合 raw prompt、员工说明明文或管理员理由明文。 | 输入被 banned 字段门禁拒绝。 |
| TDD-R3-022 | owner view 缺少 runtime / 断链 / 管理员分区时静默隐藏状态。 | 空分区显式显示 unknown / none。 |

## 4. R4 beta 测试

| Test ID | RED 条件 | GREEN 条件 |
|---|---|---|
| TDD-R4-001 | 管理员停用无审计。 | 停用动作签名并进入审计。 |
| TDD-R4-002 | 断链无 owner view 可见性。 | 员工可见断链状态和说明入口。 |
| TDD-R4-003 | 员工说明改写 evidence。 | 说明只以 amendment / explanation 关联。 |
| TDD-R4-004 | dry run 写入正式绩效台账。 | dry run 被隔离并阻断。 |

## 5. R5 evidence feed 测试

| Test ID | RED 条件 | GREEN 条件 |
|---|---|---|
| TDD-R5-001 | evidence feed 不幂等。 | 相同 batchId 重试不重复记账。 |
| TDD-R5-002 | feed 包含 raw event。 | feed 只包含 sanitized aggregate 和 evidence reference。 |
| TDD-R5-003 | feed 缺少制度版本或确认版本。 | 发布被阻断。 |
| TDD-R5-004 | 大辉子消费失败无重试。 | 重试有退避、签名和审计。 |
| TDD-R5-005 | `ltc_endpoint.evidence_feed` 缺失，无法生成大辉子证据包。 | 生成 `LTC_EVT_DAHUIZI_EVIDENCE_READY` 签名 evidence envelope。 |
| TDD-R5-006 | evidence envelope 输入包含 prompt、raw path 等 banned 字段。 | 输入被 banned 字段门禁拒绝，错误不泄漏 banned 值。 |
| TDD-R5-007 | LTC evidence feed 接受绩效裁决或飞书写入 payload。 | 绩效裁决和飞书写入 payload 被拒绝，LTC role 固定为 evidence producer only。 |
| TDD-R5-008 | signing key 缺失仍生成 evidence envelope。 | 生成前阻断，返回签名密钥缺失原因码。 |
| TDD-R5-009 | camelCase 执行 payload alias 绕过 banned 门禁。 | banned key canonicalization 覆盖 snake_case 与 camelCase。 |
| TDD-R5-010 | evidence feed 不生成幂等 delivery key。 | 相同 evidence hash 生成相同 idempotency key。 |
| TDD-R5-011 | 真实 delivery 在 connector 未批准时可执行。 | 被 dry-run isolation 阻断。 |
| TDD-R5-012 | delivery 失败计划产生飞书或绩效副作用。 | 只生成退避重试策略和签名审计，不执行网络、飞书或绩效动作。 |
| TDD-R5-013 | evidence envelope 缺少 hash 或签名仍可交付。 | 返回 evidence envelope invalid 原因码。 |

## 6. R6 飞书测试

| Test ID | RED 条件 | GREEN 条件 |
|---|---|---|
| TDD-R6-001 | LTC 直接写飞书台账。 | 流程阻断，只有大辉子可写。 |
| TDD-R6-002 | 公告包含 banned 字段。 | 公告阻断。 |
| TDD-R6-003 | break-chain 自动成为绩效负面。 | 流程阻断。 |
| TDD-R6-004 | 员工说明未关联公告前置检查。 | 公告前检查说明状态。 |

## 7. 验证输出

每轮测试必须输出：

- RED 命令和失败摘要。
- GREEN 命令和通过摘要。
- banned 泄漏检查结果。
- 未覆盖风险。
