# LTC 治理重基线 v0.1

**状态**：创始人审查草案；已并入大辉子评审 M1-M8  
**日期**：2026-05-06  
**负责人**：NODE-A  
**范围**：LTC-Endpoint 的 R0 治理重基线

## 1. 目的

本文用于替换 LTC-Endpoint 旧 P0 阶段的临时解释，建立新的 active baseline（活跃基线），作为后续产品规划、领域建模、规格设计和工程实施的真源草案。

LTC-Endpoint 是大辉子的企业端点工具和哨兵基础设施。它运行在员工工作设备上，采集 AI 驱动工程工作的规范化元数据，生成 sanitized event（清洗事件）、aggregate（聚合数据）和 evidence reference（证据引用），供大辉子使用。

大辉子结合 LTC 证据和正式制度文件，进行绩效分析、统计、裁决，并发布到飞书台账和公告。LTC 本身不执行绩效裁决。

## 2. 新活跃基线

LTC-Endpoint 是：

- 企业基础设施组件。
- 大辉子的端点延展和哨兵工具。
- 工程治理和绩效管理的合规证据来源。
- 安装在员工工作设备上的受控 runtime（运行时）。
- sanitized event、aggregate、evidence reference 的生产者。

LTC-Endpoint 不是：

- 绩效评分引擎。
- 薪酬建议引擎。
- 员工排名引擎。
- 纪律处分决策引擎。
- 内容监控系统。
- 通用软件活动监控系统。

## 3. 已锁定裁决

| ID | 裁决 |
|---|---|
| D0 | LTC 是绩效管理的正式证据输入，但不直接裁决绩效结果。 |
| D1 | 字段范围采用 scope-first（范围先行）/ banned（禁止）模型。采集范围内字段尽量齐全，但 banned 字段永久禁止。 |
| D2 | 下游系统只接收 sanitized event、aggregate 和 evidence reference。raw event（原始事件）不进入大辉子、飞书台账、飞书公告或 App。 |
| D3 | 大辉子是二级节点领域智能体。大辉子依据制度文件进行绩效分析、统计、裁决和发布。LTC 是大辉子的端点工具。 |
| D4 | LTC 向大辉子输出证据。大辉子写入飞书绩效台账和公告。 |
| D5 | 员工确认覆盖制度版本、确认版本、工具用途、字段范围、绩效用途、数据形态、留存、断链策略、owner view（员工自查视图）、申诉路径和变更策略。 |
| D6 | LTC 是员工工作设备上的强制企业基础设施。员工没有本地关闭、退出、卸载或绕过权限。 |
| D6.1 | 允许人工指定和登记、公司固定资产电脑安装、受管 launch daemon（启动守护进程）或平台等价服务、签名服务、管理员控制停用/卸载和心跳缺失告警。不接入 MDM（移动设备管理）等平台。不允许内核级黑箱防篡改。 |
| D7 | LTC 按 R0-R6 分阶段交付。 |
| D8 | 旧 P0 重置文档保留为历史证据。新的 active baseline 从本 R0 治理重基线开始。 |

## 4. 大辉子评审后执行口径

以下口径进入 R1 规格设计，正式 LOCKED 前仍以创始人终签为准：

| ID | 口径 |
|---|---|
| F1 | 强制部署仅限公司固定资产电脑。优先 Windows，再 Mac，仅支持 Windows / macOS 双平台。 |
| F2 | 对员工使用“制度告知与签字确认”口径，不写成可自由撤回的自愿 consent。代码字段 `consentVersion` 在 LTC 内解释为“制度确认版本”。 |
| F3 | 员工个人电脑不纳入强制范围。员工自愿选择可安装，不作制度规定；自愿安装仍遵守 banned 字段和下游边界。 |
| F4 | 暂不接入 MDM 等平台。公司资产由公司分配给员工使用，设备由人工指定和登记。LTC 只采集当前安装电脑硬件配置信息，不参与资产管理。 |
| F5 | 字段可以先行，在采集范围内尽量齐全；字段范围必须版本化、员工可见并通过 banned 泄漏测试。 |
| F6 | break-chain 只作为证据完整性和合规状态输入，不自动等价为绩效负面结论。 |
| F7 | 飞书公告由大辉子发布，不暴露 raw event、banned 字段或不必要个人细节。 |
| F8 | 留存期限、访问角色、删除触发、申诉冻结规则必须在 R3 前形成可审计规格。 |

## 5. 字段治理

### 5.1 allow（允许字段）

允许字段在测试证明 banned 内容不会泄漏后，可进入 alpha 和 beta 阶段：

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

### 5.2 scope-first（范围先行字段）

创始人裁决为字段可以先行，采集范围内尽量齐全。以下字段可进入字段范围版本，但必须员工可见、通过 banned 泄漏测试，并且不得包含内容值：

- `processName`：仅限工程白名单。
- `foregroundBackgroundState`：仅记录批准工具的前后台状态，不推断空闲或离开。
- `cwdHash`：仅在去重确有必要，且无法还原路径值时使用。
- `fileCount`：仅限未来 code-action（代码动作）阶段，不含文件名。
- `linesAdded` / `linesRemoved`：仅聚合数字，不含 patch content（补丁内容）。
- `testFileCount`：仅聚合数字，不含文件名。
- `repoHash` / `branchHash`：只允许 hash（哈希）形态，需要审批。
- `taskId` / `issueId` / `prId`：只能来自 GitHub 或任务系统，不得从本机内容推断。
- `subscriptionIdHash`：仅用于 Codex 订阅使用识别，不保存明文订阅标识。
- `apiKeyIdHash`：仅用于 `heiyucode.com` API 密钥使用识别，不保存明文密钥。
- `apiHost`：仅限 `heiyucode.com`，不得扩展为通用 URL 采集。
- `keyUsageCount`：API 密钥调用次数。
- `quotaConsumed`：可取得时记录配额消耗，不推断内容。

字段范围门禁：

- 必须说明字段目的、业务必要性和不可替代性。
- 必须通过 banned 泄漏测试，覆盖输出、日志、错误消息、debug dump、metrics label 和 fixture snapshot。
- 必须升级制度版本、字段范围版本和制度确认版本。
- 必须在员工重新完成制度告知与签字确认后，才能进入生产 evidence feed。
- 必须支持禁用和回滚，不得以兼容性为由永久保留字段。

### 5.3 banned（禁止字段）

禁止字段不得采集、存储、导出、日志化或推断：

- prompt text（提示词文本）
- completion text（模型输出文本）
- transcript（会话转写）
- source file content（源文件内容）
- patch content（补丁内容）
- full command arguments（完整命令参数）
- shell history（命令历史）
- URL
- window title（窗口标题）
- document path（文档路径）
- clipboard（剪贴板）
- keystroke（按键）
- screenshot（截图）
- screen recording（屏幕录制）
- browser history（浏览器历史）
- non-engineering app inventory（非工程应用清单）
- idle / away inference（空闲/离开推断）
- break time（休息时长）
- employee ranking（员工排名）
- performance score（绩效分）
- salary suggestion（薪酬建议）
- HR label（人力资源标签）
- subjective work attitude metric（主观工作态度指标）

banned 字段不得出现在下游数据、日志、错误消息、debug dump、metrics label、测试快照、飞书台账、飞书公告或员工 owner view 中。

## 6. raw observation 边界

R2 alpha0-lite 只允许 synthetic fixture（合成样本）。R2 不得读取真实员工 runtime 数据，不得产生真实员工 raw event。

R3 以后，raw observation（原始观察候选）只能作为内存中的清洗候选输入存在：

- 不得持久化。
- 不得日志化。
- 不得导出。
- 不得被员工、管理员、大辉子、飞书台账、飞书公告或 App 浏览。
- 不得进入指标 label、错误消息或调试转储。
- 含 banned 字段或 banned 值的候选必须拒绝或转换，并且不得落盘。

LTC 对下游只发布 sanitized event、aggregate 和 evidence reference。

## 7. runtime（运行时）治理

LTC 可以作为企业基础设施安装和管理。

允许：

- 公司固定资产电脑安装。
- Windows 优先，Mac 第二平台。
- 人工指定和登记安装对象。
- 设备绑定。
- 员工工程身份绑定。
- 开机自启。
- 常驻运行。
- 受管 launch daemon 或等价平台服务。
- 签名心跳。
- 健康检查。
- 降级上报。
- break-chain event（断链事件）记录。
- 管理员控制停用或卸载。
- 管理员操作签名审计。
- 员工 owner view。
- 员工更正、申诉和异常说明。
- 当前安装电脑硬件配置信息采集。

不允许：

- 员工本地关闭、退出、卸载或绕过。
- 把员工个人电脑纳入强制部署。
- 把自愿安装个人电脑纳入强制覆盖率或资产管理。
- LTC 参与资产管理。
- MDM 或类似平台接入。
- kernel extension（内核扩展）或 system extension（系统扩展）防篡改。
- 黑箱且不可审计的强制机制。
- 内容采集。
- banned 字段采集。
- 未经版本确认的静默字段扩张。

## 8. 制度告知与员工自查

LTC 的员工侧治理口径是“制度告知与签字确认”，不是可自由撤回的自愿 consent。

确认内容必须覆盖：

- 制度版本。
- 制度确认版本。
- 工具用途。
- 字段范围。
- 绩效用途。
- 数据形态。
- 留存规则。
- 断链策略。
- 员工无本地关闭、退出、卸载或绕过权限。
- owner view。
- 更正、申诉和异常说明路径。
- 字段范围、绩效用途或留存变化时的重新确认策略。

员工说明以 amendment / explanation（补充说明）关联证据，不直接改写已签名 evidence。

安装前置工作由行政部门处理完毕。LTC 接入视为前提合规流程已完毕，未处理完成的员工或设备不会进入安装环节。LTC runtime 不处理拒签、未确认、离职、外包、试用期等用工前置流程。

## 9. 飞书台账与公告门禁

LTC 无飞书绩效台账写入权限，也无飞书公告发布权限。

大辉子写入飞书台账或发布公告前，必须满足：

- 制度版本和制度确认版本有效。
- evidence reference 可追溯。
- raw event 和 banned 字段未进入输出。
- 员工异常说明和申诉状态已关联。
- 公告可见范围已确认。
- 敏感信息排除规则已通过检查。
- 需要人工或创始人审批的场景已完成审批。

R4/R5 的 dry run 和 evidence feed 接入不得进入正式绩效台账、公告、薪酬、纪律或考核结论。

## 10. 留存与访问控制

R1 必须定义 RetentionPolicy（留存策略）和 EvidenceAccessGrant（证据访问授权）：

- 留存期限。
- 删除触发条件。
- 申诉或审计冻结规则。
- 可访问角色。
- 导出限制。
- 管理员访问审计。
- 大辉子消费审计。
- 飞书台账引用粒度。

访问、停用、卸载、导出、删除、冻结等管理动作必须签名并进入审计日志。

## 11. 旧文档处置

旧 P0 重置包保留为历史证据，不再作为 active product baseline（活跃产品基线）。

旧 P0 文档优先做安全删除评估。确认没有审计、引用、交接和追溯价值的旧 P0 文档可以删除。不能安全删除的旧 P0 文档首页或索引必须标注 Superseded / Historical Only，并指向本治理重基线。后续执行、开发和评审不得继续引用旧 P0 作为产品边界。

### 11.1 继续有效

以下旧边界继续有效：

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

### 11.2 已被替代

以下旧口径被新基线替代，或降级为历史 P0 阶段约束：

- “不用于 HR / 绩效”。
- “员工可以停止 endpoint agent”。
- “不安装 runtime”。
- “不实现 daemon / collector”。
- “不接入大辉子 evidence feed”。
- “alpha0-lite local-only 是长期产品边界”。

## 12. 治理门禁

在 R1 规格产物完成前，不得进入超出规格工作的实现。

R1 必须至少包含：

- LTC 领域模型。
- LTC Cap-Spec（能力规格）。
- LTC 验收场景。
- LTC 技术设计。
- LTC event code / reason code / status code（事件码/原因码/状态码）提案。
- LTC TDD（测试驱动开发）矩阵。
- 字段范围版本和 scope-first 字段门禁。
- raw observation 不落盘、不日志化、不下游化测试。
- 飞书台账与公告门禁。
- 留存与访问控制规格。
- owner view、更正、申诉和异常说明 SLA。
