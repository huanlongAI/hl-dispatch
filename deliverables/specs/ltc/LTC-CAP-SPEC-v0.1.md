# LTC Cap-Spec v0.1

**状态**：创始人审查草案；已并入大辉子评审 M1-M8  
**日期**：2026-05-06  
**负责人**：NODE-A  
**能力包**：LTC-Endpoint

## 1. 目标

将 LTC-Endpoint 建设为大辉子的企业端点工具和哨兵基础设施。

LTC 从员工工作设备采集合规的 AI 驱动工程元数据，完成清洗和聚合，并向大辉子发布证据引用，用于工程治理和绩效管理。

## 2. 非目标

LTC 不得：

- 裁决绩效分。
- 排名员工。
- 建议薪酬。
- 决定纪律处分。
- 采集 prompt text（提示词文本）。
- 采集 completion text（模型输出文本）。
- 采集 transcript（会话转写）。
- 采集 source file content（源文件内容）。
- 采集 patch content（补丁内容）。
- 采集 URL、窗口标题、剪贴板、按键、截图、屏幕录制或浏览器历史。
- 采集完整命令参数或 shell history（命令历史）。
- 采集非工程应用清单。
- 推断 idle / away time（空闲/离开时间）或 break time（休息时长）。
- 提供员工可控的本地关闭、退出、卸载或绕过路径。
- 把 break-chain 自动解释为绩效负面结论。
- 在 R4/R5 dry run 阶段进入正式绩效台账、公告、薪酬、纪律或考核结论。
- 参与公司资产管理。
- 接入 MDM 或类似资产 / 设备管理平台。

## 3. 产品用户

| 用户 | 需求 |
|---|---|
| 大辉子 | 消费 evidence feed（证据流），依据制度分析绩效，写入飞书台账和公告。 |
| 创始人 / 管理层 | 查看合规证据，以及由大辉子产出的绩效结果。 |
| 员工 | 查看自身采集字段类别、端点状态、断链记录、更正、申诉和异常说明路径。 |
| 管理员 | 按人工指定和登记结果，在公司固定资产电脑上安装、绑定、更新、停用或卸载 LTC。 |
| 审计者 | 校验字段范围、签名、留存、访问和制度版本一致性。 |

## 4. 能力边界

### 4.1 包含

- 企业受管端点安装。
- 公司固定资产电脑绑定。
- 员工工程身份绑定。
- 常驻运行和开机自启。
- 签名心跳。
- 端点健康和降级状态。
- 当前安装电脑硬件配置信息采集。
- 从已批准来源观察 AI 工具元数据。
- scope-first / banned 字段策略。
- sanitized event 生成。
- aggregate 生成。
- evidence reference 生成。
- break-chain event 检测。
- 员工 owner view。
- 更正、申诉和异常说明路径。
- 发给大辉子的 evidence feed。
- 管理员操作和访问审计。

### 4.2 不包含

- LTC 写入飞书绩效台账。
- LTC 发布飞书公告。
- LTC 计算绩效分。
- LTC 做薪酬或纪律处分决策。
- raw event 导出到大辉子或飞书。
- raw observation 持久化、日志化或展示。
- 内核级防篡改。
- 黑箱不可审计的强制机制。
- MDM 或类似平台接入。
- 公司资产管理。

## 5. 数据形态

下游数据形态：

- `sanitized event`
- `aggregate`
- `evidence reference`

R2 alpha0-lite 只允许 synthetic fixture。R2 不得读取真实员工 runtime 数据，不得产生真实员工 raw event。

R3 以后 raw observation 只能作为内存候选输入存在，不得持久化、日志化、导出、展示或进入错误消息、metrics label、debug dump、测试快照。raw observation 不进入大辉子、飞书台账、飞书公告或 App。

## 6. 字段层级

### 6.1 allow

- `toolName`
- `toolVersion`
- `provider`
- `modelId`
- `inputTokens`
- `outputTokens`
- `requestCount`
- `windowStart`
- `windowEnd`
- `durationSec`
- `machineIdHash`
- `userId`
- `agentVersion`
- `recordedAt`
- `degradationLevel`
- `breakChainReason`
- `consentVersion`
- `policyVersion`
- `osName`
- `osVersion`
- `machineModel`
- `cpuModel`
- `memoryGB`
- `diskCapacityGB`
- `gpuModel`
- `hardwareFingerprintHash`

### 6.2 scope-first

- `processName`
- `foregroundBackgroundState`
- `cwdHash`
- `fileCount`
- `linesAdded`
- `linesRemoved`
- `testFileCount`
- `repoHash`
- `branchHash`
- `taskId`
- `issueId`
- `prId`
- `subscriptionIdHash`
- `apiKeyIdHash`
- `apiHost`
- `keyUsageCount`
- `quotaConsumed`

创始人裁决为字段可以先行，采集范围内尽量齐全。scope-first 字段必须写入字段范围版本、员工可见，并通过 banned 泄漏测试。字段先行不改变 banned 字段永久禁止边界。

### 6.3 banned

完整 banned 字段清单见 `LTC-GOVERNANCE-REBASELINE-v0.1.md`。banned 字段永不采集、存储、导出、日志化或推断。

## 7. Tool Source Registry（工具来源登记）

R2 首批工具来源为 Codex 订阅和 `heiyucode.com` API 密钥使用。每个已批准 AI 工具来源必须登记：

- 工具名。
- 工具版本。
- 提供方。
- 采集方式。
- 字段映射。
- banned 泄漏测试结果。
- 审批人和审批时间。
- 回滚或停用方式。
- 订阅标识 hash 或 API key 标识 hash。
- API host；当前只允许 `heiyucode.com`。

未登记或未通过 banned 泄漏测试的工具来源不得进入 sanitizer。

## 8. 业务规则

| Rule ID | 规则 |
|---|---|
| LTC-R-001 | LTC 证据是大辉子绩效管理的正式输入。 |
| LTC-R-002 | LTC 不直接裁决绩效分、排名、薪酬或纪律处分。 |
| LTC-R-003 | raw event 不得跨越下游边界。 |
| LTC-R-004 | 所有下游证据必须包含制度版本、字段范围版本和确认版本。 |
| LTC-R-005 | banned 字段必须在下游发布前被拒绝，且不得出现在日志、错误消息、metrics label、debug dump 或测试快照中。 |
| LTC-R-006 | 员工不能本地关闭、退出、卸载或绕过 LTC。 |
| LTC-R-007 | 员工必须拥有 owner view、更正、申诉和异常说明路径。 |
| LTC-R-008 | 心跳缺失、runtime 降级、管理员停用、管理员卸载或自隔离必须产生断链或合规事件。 |
| LTC-R-009 | 字段范围、绩效用途或留存发生实质变更时，必须升级版本并重新确认。 |
| LTC-R-010 | 大辉子负责飞书绩效台账和公告写入。 |
| LTC-R-011 | R4/R5 dry run 不得进入正式绩效台账、公告、薪酬、纪律或考核结论。 |
| LTC-R-012 | break-chain 只表示证据完整性或合规状态，不自动等价为绩效负面结论。 |
| LTC-R-013 | 员工异常说明以 amendment / explanation 关联证据，不直接改写已签名 evidence。 |
| LTC-R-014 | scope-first 字段必须版本化、员工可见、通过 banned 泄漏测试并可回滚。 |
| LTC-R-015 | LTC 无飞书写权限，所有飞书台账和公告动作必须由大辉子执行。 |
| LTC-R-016 | LTC 只采集当前安装电脑硬件配置信息，不参与资产管理。 |
| LTC-R-017 | 强制部署仅限公司固定资产电脑，优先 Windows，再 Mac，仅支持 Windows / macOS 双平台。 |
| LTC-R-018 | 员工个人电脑不纳入强制范围，自愿安装不作制度规定。 |

## 9. 验收场景

| Case ID | 场景 | 预期 |
|---|---|---|
| LTC-AC-001 | 已批准 AI 工具元数据进入 sanitizer（清洗器）。 | sanitized event 只包含 allow 字段。 |
| LTC-AC-002 | 输入包含 prompt、completion、transcript、文件内容、URL、窗口标题、剪贴板或按键字段。 | 事件被拒绝或转换，下游不出现 banned 字段或值。 |
| LTC-AC-003 | banned 字段出现在错误路径、日志、debug dump、metrics label 或测试快照中。 | 测试失败；实现必须阻断泄漏。 |
| LTC-AC-004 | R3 以后出现 raw observation 持久化、日志化、导出或展示。 | 测试失败；raw observation 只能作为内存候选输入。 |
| LTC-AC-005 | 端点心跳缺失。 | 创建断链事件，并对员工 owner view 和大辉子 evidence feed 可见。 |
| LTC-AC-006 | 员工尝试本地关闭或卸载。 | 本地不可执行；如果检测到绕过，记录合规事件。 |
| LTC-AC-007 | 管理员通过受管控制停用端点。 | 管理员停用事件被签名，并进入断链 / 合规证据和审计日志。 |
| LTC-AC-008 | 员工提交异常说明。 | 说明状态被记录，并以 amendment / explanation 关联断链或证据引用。 |
| LTC-AC-009 | 大辉子消费 evidence feed。 | 大辉子收到 sanitized aggregate 和 evidence reference，不收到 raw event。 |
| LTC-AC-010 | 写入绩效台账。 | 写入由大辉子执行，不由 LTC 执行。 |
| LTC-AC-011 | 字段范围发生实质变更。 | 采集扩张前必须生成新的制度 / 字段范围 / 确认版本。 |
| LTC-AC-012 | 员工打开 owner view。 | 员工可以看到采集字段类别、端点状态、断链记录、制度版本和说明入口。 |
| LTC-AC-013 | scope-first 字段未进入字段范围版本但被采集。 | 测试失败，证据发布被阻断。 |
| LTC-AC-014 | R4/R5 dry run evidence 被用于正式绩效台账或公告。 | 测试失败，流程被阻断。 |
| LTC-AC-015 | LTC 采集当前安装电脑硬件配置。 | 只出现硬件配置元数据和 hash 标识，不出现资产管理台账或个人内容。 |
| LTC-AC-016 | 个人电脑未纳入强制部署。 | 不计入强制覆盖范围；自愿安装仍遵守 banned 字段和下游边界。 |

## 10. 飞书台账与公告门禁

LTC 不写飞书台账，不发飞书公告。

大辉子写入台账或公告前必须校验：

- 制度版本和确认版本有效。
- evidence reference 可追溯。
- raw event 和 banned 字段未进入输出。
- 员工异常说明和申诉状态已关联。
- 公告可见范围已确认。
- 敏感信息排除规则已通过。
- 需要人工或创始人审批的场景已完成审批。

## 11. 实施前必需规格

- 治理重基线。
- 领域模型。
- 验收场景。
- HPRD。
- 技术设计。
- event code / reason code / status code 提案。
- TDD 矩阵。
- CI 门禁定义。
- 字段范围版本和 scope-first 字段门禁。
- raw observation 不落盘、不日志化、不下游化测试。
- 留存与访问控制规格。
- owner view、更正、申诉和异常说明 SLA。

## 12. 首个实施切片

R2 alpha0-lite 仍然是第一个实施切片：

- Codex 订阅和 `heiyucode.com` API 密钥使用的合成样本。
- 只使用 synthetic fixture（合成样本）。
- 只实现 sanitizer / parser。
- 只输出本地结果。
- 不安装。
- 不常驻运行。
- 字段范围内尽量齐全，但不使用 banned 字段。
- 不接大辉子 evidence feed。
- 不接绩效台账。
