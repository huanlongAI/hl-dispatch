# LTC 领域模型 v0.1

**状态**：创始人审查草案；已并入大辉子评审 M1-M8  
**日期**：2026-05-06  
**负责人**：NODE-A  
**范围**：LTC-Endpoint 的 R1 DDD（领域驱动设计）模型

## 1. 领域陈述

LTC-Endpoint 将大辉子的能力延展到员工工作设备。它观察经批准的 AI 驱动工程元数据，完成清洗和聚合，并为大辉子的工程治理和绩效管理工作流提供证据。

该领域必须同时处理企业治理、制度告知与签字确认、端点强制运行、AI 使用可见性、证据完整性、员工自查和绩效证据边界。

## 2. Bounded Context（限界上下文）

| 上下文 | 职责 | 不负责 |
|---|---|---|
| Endpoint Sentinel（端点哨兵） | 公司固定资产电脑安装、设备绑定、常驻运行、心跳、健康状态、断链检测。Windows 优先，Mac 第二平台。 | 绩效裁决、内容检查、飞书写入、资产管理。 |
| AI Usage Telemetry（AI 使用遥测） | 从已批准本地来源观察 AI 工具元数据，并把候选输入交给清洗策略。 | prompt、completion、transcript、源文件内容、URL、窗口标题、剪贴板、按键、raw observation 持久化。 |
| Sanitization Policy（清洗策略） | 执行 scope-first / banned 字段策略、hash、时间桶、拒绝和泄漏检查。 | 业务判断或 HR 判断。 |
| Policy & Field Governance（制度与字段治理） | 管理制度版本、字段范围版本、字段先行范围、重新确认要求。 | runtime 采集逻辑、绩效裁决。 |
| Employment Acknowledgement（用工确认） | 跟踪制度告知与签字确认、用途、留存、申诉路径和重新确认状态。 | 把强制基础设施解释为可自由撤回的自愿同意。 |
| Evidence Feed（证据流） | 向大辉子生产 sanitized event、aggregate 和 evidence reference 批次。 | 飞书台账写入、绩效公告发布、raw event 共享。 |
| Performance Evidence（绩效证据） | 建模证据完整性、采集链路状态、制度版本一致性和大辉子可引用证据。 | 最终绩效评分、员工态度判断、纪律处分。 |
| Employee Owner View（员工自查视图） | 展示采集字段类别、端点状态、断链记录、更正、申诉和异常说明路径。 | runtime 绕过、本地关闭、改写已签名 evidence。 |
| Retention & Access Control（留存与访问控制） | 管理留存期限、访问授权、删除、冻结、导出限制和访问审计。 | 绩效业务解释。 |
| Compliance Audit（合规审计） | 跟踪签名、留存、访问、制度版本、确认版本和审计轨迹。 | 绩效业务解释。 |

## 3. Aggregate（聚合）

### 3.1 EndpointDevice（端点设备）

表示一台公司固定资产电脑。设备由公司分配给员工使用，由人工指定和登记；LTC 只记录当前安装电脑的硬件配置信息，不参与资产管理。

关键字段：

- `machineIdHash`
- `boundUserId`
- `agentVersion`
- `installState`
- `runtimeState`
- `healthStatus`
- `lastHeartbeatAt`
- `policyVersion`
- `consentVersion`
- `osName`
- `osVersion`
- `machineModel`
- `cpuModel`
- `memoryGB`
- `diskCapacityGB`
- `gpuModel`
- `hardwareFingerprintHash`

不变量：

- 设备必须绑定一个有效工程用户后，才能发布 evidence feed。
- 没有有效制度版本和确认版本时，设备不得输出下游证据。
- 员工本地关闭、退出、卸载或绕过不是合法状态迁移。
- 强制部署只覆盖公司固定资产电脑。
- 员工个人电脑不纳入强制范围；自愿安装不作为制度规定或资产管理依据。
- LTC 不负责资产归属、资产流转或资产台账维护。

### 3.2 EngineeringUser（工程用户）

表示 LTC 使用的员工工程身份。

关键字段：

- `userId`
- `employmentStatus`
- `policyVersion`
- `consentVersion`
- `ownerViewEnabled`

不变量：

- `userId` 不是绩效分身份。
- 绩效裁决由大辉子依据制度文件完成，不由 LTC 完成。

### 3.3 PolicyVersion（制度版本）

表示 LTC 所依据的企业制度版本。

关键字段：

- `policyVersion`
- `effectiveAt`
- `scope`
- `performanceUseText`
- `employeeAcknowledgementRequired`
- `supersedes`

不变量：

- 任何字段范围、绩效用途、留存或部署范围的实质变化都必须产生新制度版本。
- 未生效或被替代的制度版本不得用于发布新 evidence feed。

### 3.4 FieldScopeVersion（字段范围版本）

表示字段先行范围与 banned 字段治理版本。创始人裁决为采集范围内尽量齐全，但 banned 字段永久禁止。

关键字段：

- `fieldScopeVersion`
- `allowFields`
- `scopeFirstFields`
- `bannedFields`
- `approvedAt`
- `approvedBy`

不变量：

- banned 字段不得被审批为 allow 或 scope-first。
- scope-first 字段必须员工可见、版本化，并通过 banned 泄漏测试。
- 字段范围内尽量齐全不代表可以采集 prompt、completion、文件内容、URL、窗口标题、剪贴板、按键、截图等 banned 字段。

### 3.5 SystemAcknowledgementRecord（制度确认记录）

表示员工对制度和 LTC 范围的告知签字确认。技术字段 `consentVersion` 在本领域内解释为制度确认版本，不表示可自由撤回的自愿同意。

关键字段：

- `userId`
- `policyVersion`
- `consentVersion`
- `fieldScopeVersion`
- `performanceUseAccepted`
- `retentionPolicyVersion`
- `confirmedAt`

不变量：

- 字段范围、绩效用途或留存策略发生实质变更时，必须升级版本并重新确认。
- 确认内容必须包含员工无本地关闭、卸载或绕过权限。
- 安装前置工作由行政部门处理完毕；LTC 接入视为前提合规流程已完毕。
- 未处理完成的员工或设备不会进入安装环节。
- LTC runtime 不处理拒签、未确认、离职、外包、试用期等用工前置流程。

### 3.6 ToolSourceRegistry（工具来源登记）

表示允许被 LTC 观察的 AI 工具来源。R2 首批工具来源为 Codex 订阅和 `heiyucode.com` API 密钥使用。

关键字段：

- `toolName`
- `toolVersion`
- `provider`
- `collectionMethod`
- `fieldMappingVersion`
- `leakageTestStatus`
- `approvedAt`
- `subscriptionIdHash`
- `apiKeyIdHash`
- `apiHost`
- `keyUsageCount`
- `quotaConsumed`

不变量：

- 未登记工具来源不得进入 sanitizer。
- 工具来源必须通过 banned 泄漏测试后才能进入 R2 以后阶段。
- Codex 订阅不得记录 prompt、completion 或 transcript。
- `heiyucode.com` API 密钥使用不得保存明文 API key。

### 3.7 TelemetryObservation（遥测观察）

表示清洗前的原始观察候选。

关键字段：

- `sourceTool`
- `observedAt`
- `candidateFields`
- `sourceClassification`

不变量：

- R2 只允许 synthetic fixture，不允许真实员工 raw event。
- R3 以后 raw observation 只能作为内存候选输入存在，不得持久化、日志化、导出或展示。
- raw observation 不能进入大辉子、飞书台账、飞书公告或 App。
- 含 banned 字段或 banned 值的观察必须在下游使用前被拒绝或转换，且不得落盘。

### 3.8 SanitizedEvidence（清洗证据）

表示可用于下游证据消费的一条清洗事件或聚合数据。

关键字段：

- `evidenceId`
- `employeeId`
- `machineIdHash`
- `period`
- `allowedFields`
- `aggregateFields`
- `evidenceRefs`
- `signature`
- `generatedAt`

不变量：

- 不得包含 banned 字段或 banned 值。
- 必须包含制度版本、字段范围版本和确认版本。
- 必须能通过可审计的转换元数据复现，同时不暴露原始内容。

### 3.9 BreakChainIncident（断链事件）

表示证据链中断。它是独立事件生命周期，不是员工绩效结论。

关键字段：

- `breakChainId`
- `machineIdHash`
- `employeeId`
- `reason`
- `startedAt`
- `resolvedAt`
- `explanationStatus`
- `source`

不变量：

- 心跳缺失、管理员停用、卸载、崩溃、自隔离或 runtime 降级必须产生断链或合规事件。
- 员工可以提交说明和申诉。
- 员工不能静默关闭或绕过 LTC。
- 断链只表示证据完整性或合规状态，不自动等价为绩效负面结论。

### 3.10 PerformanceEvidenceItem（绩效证据项）

表示大辉子消费的证据输入。

关键字段：

- `employeeId`
- `period`
- `policyVersion`
- `fieldScopeVersion`
- `consentVersion`
- `evidenceCompleteness`
- `aiUsageAggregate`
- `toolCoverage`
- `breakChainSummary`
- `riskFlags`
- `evidenceRefs`

不变量：

- 它是大辉子的输入，不是最终绩效结果。
- 它不得包含绩效分、员工排名、薪酬建议或纪律处分结论。
- `riskFlags`、`evidenceCompleteness`、`breakChainSummary` 只表示证据完整性、采集链路状态、制度版本一致性，不得表达员工表现、态度、纪律倾向、绩效等级或 HR 标签。

### 3.11 EvidenceFeedBatch（证据流批次）

表示 LTC 发给大辉子的签名批次。

关键字段：

- `batchId`
- `period`
- `items`
- `generatedAt`
- `signature`
- `schemaVersion`

不变量：

- 批次内容必须经过清洗。
- 批次内容必须版本化。
- 大辉子负责绩效分析、统计、裁决、飞书台账写入和公告发布。
- R4/R5 dry run 批次不得进入正式绩效台账、公告、薪酬、纪律或考核结论。

### 3.12 RetentionPolicy（留存策略）

表示 evidence 和审计记录的留存、删除和冻结规则。

关键字段：

- `retentionPolicyVersion`
- `retentionPeriod`
- `deleteTrigger`
- `appealHoldRule`
- `auditHoldRule`
- `exportRestriction`

不变量：

- 留存策略变化必须触发制度版本或确认版本检查。
- 申诉或审计冻结期间不得删除相关 evidence reference 和审计记录。

### 3.13 EvidenceAccessGrant（证据访问授权）

表示谁能访问什么粒度的证据。

关键字段：

- `grantId`
- `role`
- `scope`
- `evidenceGranularity`
- `grantedBy`
- `expiresAt`

不变量：

- 管理员、大辉子、审计者访问 evidence 必须有授权和审计记录。
- 访问授权不得扩展到 raw observation 或 banned 字段。

### 3.14 AuditAccessLog（访问审计日志）

表示访问、停用、卸载、导出、删除、冻结等治理动作。

关键字段：

- `auditLogId`
- `actorId`
- `action`
- `targetRef`
- `policyVersion`
- `signedAt`

不变量：

- 管理员停用、卸载、访问、导出必须签名并进入审计日志。
- 审计日志不得包含 raw observation 或 banned 字段。

## 4. Domain Event（领域事件）

| 事件 | 生产者 | 消费者 |
|---|---|---|
| `PolicyVersionActivated` | Policy & Field Governance | Endpoint Sentinel, Evidence Feed, Compliance Audit |
| `FieldScopeUpdated` | Policy & Field Governance | Sanitization Policy, Employment Acknowledgement |
| `FieldScopeApproved` | Policy & Field Governance | Sanitization Policy, Compliance Audit |
| `ReconfirmationRequired` | Policy & Field Governance | Endpoint Sentinel, Employee Owner View |
| `EndpointInstalled` | Endpoint Sentinel | Compliance Audit |
| `EndpointBound` | Endpoint Sentinel | Employment Acknowledgement, Evidence Feed |
| `SystemAcknowledgementConfirmed` | Employment Acknowledgement | Endpoint Sentinel, Evidence Feed |
| `TelemetryObserved` | AI Usage Telemetry | Sanitization Policy |
| `TelemetryRejected` | Sanitization Policy | Compliance Audit, Owner View |
| `EvidenceSanitized` | Sanitization Policy | Evidence Feed |
| `HeartbeatSigned` | Endpoint Sentinel | Evidence Feed, Compliance Audit |
| `BreakChainDetected` | Endpoint Sentinel | Owner View, Evidence Feed, Dahuizi |
| `BreakChainExplained` | Owner View | Dahuizi, Compliance Audit |
| `EvidenceFeedPublished` | Evidence Feed | Dahuizi |
| `PerformanceEvidenceConsumed` | Dahuizi | Compliance Audit |
| `EvidenceAccessGranted` | Retention & Access Control | Compliance Audit |
| `EvidenceAccessLogged` | Retention & Access Control | Compliance Audit |

## 5. 状态机

### 5.1 端点 runtime 状态

```text
NotInstalled -> Installed -> Bound -> Running -> Degraded -> Running
Running -> AdminDisabled
Running -> AdminUninstalled
Running -> EvidenceHeldForReconfirmation -> Running
```

非法迁移：

- `Running -> EmployeeClosed`
- `Running -> EmployeeUninstalled`
- `Running -> SilentBypass`

### 5.2 断链事件状态

```text
Detected -> EmployeeExplanationPending -> Explained -> Reviewed -> Resolved
Detected -> AdminResolved -> Resolved
```

断链状态独立于 runtime 健康状态，不自动产生绩效负面结论。

### 5.3 证据状态

```text
CandidateObserved -> Rejected
CandidateObserved -> Sanitized -> Aggregated -> PublishedToDahuizi -> ConsumedByDahuizi
Sanitized -> HeldForReconfirmation -> PublishedToDahuizi
```

raw `CandidateObserved` 记录不得持久化、日志化或跨越下游边界。

### 5.4 确认状态

```text
Draft -> Confirmed -> Superseded
Confirmed -> ReconfirmationRequired -> Confirmed
```

字段范围、绩效用途或留存策略发生实质变化时，需要重新确认。未完成重新确认前，不得发布新的下游 evidence feed。

## 6. Context Map（上下文关系图）

```text
LTC Endpoint
  -> Endpoint Sentinel
  -> AI Usage Telemetry
  -> Sanitization Policy
  -> Evidence Feed
  -> Dahuizi

Dahuizi
  -> Feishu Ledger
  -> Feishu Announcement

Policy & Field Governance
  -> Employment Acknowledgement
  -> Endpoint Sentinel
  -> Evidence Feed
  -> Compliance Audit

Employee Owner View
  <- Endpoint Sentinel
  <- Sanitization Policy
  <- BreakChainIncident

Retention & Access Control
  -> Evidence Feed
  -> Compliance Audit
```

LTC 只向大辉子提供 evidence feed。LTC 不直接写入飞书台账，不直接发布飞书公告。

## 7. 已裁决口径

- 首个平台：R2 不绑定平台；R3 优先 Windows 公司固定资产电脑，Mac 为第二平台。仅支持 Windows / macOS 双平台。
- MDM 或类似平台：暂不接入。设备由人工指定和登记。
- 字段策略：字段可以先行，采集范围内尽量齐全，banned 字段永久禁止。
- `repoHash` / `branchHash`：可进入字段范围版本，但必须 hash 化、员工可见并通过 banned 泄漏测试。
- 飞书台账 schema：归大辉子 / 绩效系统所有，不归 LTC 所有。
- 员工个人电脑：不纳入强制范围，员工自愿选择可安装，不作制度规定。
- 安装前置：由行政部门处理完毕，未处理完成不会进入安装环节。
