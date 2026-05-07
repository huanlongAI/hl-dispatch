# LTC 实施路线图 v0.1

**状态**：创始人审查草案；已并入大辉子评审 M1-M8
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：R0-R6 分阶段交付计划

## 1. 原则

LTC 必须先设计，再实施。

交付顺序：

```text
R0 治理重基线
  -> R1 DDD / SDD 规格
  -> R2 alpha0-lite
  -> R3 Endpoint Sentinel Alpha
  -> R4 Internal Beta
  -> R5 DahuiZi Evidence Feed
  -> R6 Performance Integrated
```

R0 和 R1 不创建 runtime 代码。R2 证明字段安全。R3 和 R4 引入端点 runtime。R5 和 R6 接入大辉子与绩效工作流。

跨阶段硬边界：

- R2 只使用 synthetic fixture，不读取真实员工 runtime 数据。
- 字段可以先行，采集范围内尽量齐全；banned 字段永久禁止。
- R3 优先 Windows 公司固定资产电脑，再 Mac，仅支持 Windows / macOS 双平台。
- 员工个人电脑不纳入强制范围；员工自愿选择可安装，不作制度规定。
- 暂不接入 MDM 或类似平台，由人工指定和登记。
- R4/R5 只允许 dry run 或证据接入验证，不得进入正式绩效台账、公告、薪酬、纪律或考核结论。
- LTC 始终不写飞书台账、不发飞书公告、不直接评分、不直接排名。
- LTC 只采集当前安装电脑硬件配置信息，不参与资产管理。

## 2. R0 治理重基线

目标：

- 建立新的 active baseline。
- 替代旧 P0-only 边界。
- 锁定 D0-D8 决策树。
- 吸收大辉子 M1-M8 评审阻断项。
- 明确 LTC 是大辉子的端点工具和企业哨兵基础设施。

交付物：

- `LTC-GOVERNANCE-REBASELINE-v0.1.md`
- 旧文档处置
- 决策树
- 大辉子评审修订清单

出口标准：

- 创始人批准 active baseline。
- 旧“不用于 HR / 绩效”口径被替代。
- 旧 P0 文档标注 Superseded / Historical Only。
- 永久 banned 字段边界继续有效。
- raw observation 不落盘、不日志化、不下游化规则写入 R1 规格。

## 3. R1 DDD / SDD 规格

目标：

- 在实现前完成完整产品规格和技术规格。

交付物：

- `LTC-DOMAIN-MODEL-v0.1.md`
- `LTC-CAP-SPEC-v0.1.md`
- `LTC-HPRD-v0.1.md`
- `LTC-DESIGN-v0.1.md`
- `LTC-FIELD-SCOPE-v0.1.md`
- `LTC-TOOL-SOURCE-REGISTRY-v0.1.md`
- `LTC-CAP-SPEC-ACCEPTANCE-v0.1.md`
- `LTC-EVENT-REASON-CODES-v0.1.md`
- `LTC-ACCEPTANCE-MANIFEST.yaml`
- `LTC-TDD-MATRIX-v0.1.md`
- `LTC-RETENTION-ACCESS-CONTROL-v0.1.md`
- `LTC-FEISHU-GATE-v0.1.md`
- `LTC-OWNER-VIEW-APPEAL-v0.1.md`
- `LTC-PLATFORM-RUNTIME-SPEC-v0.1.md`
- `LTC-ACTIVE-BASELINE-INDEX-v0.1.md`
- `LTC-P0-DISPOSITION-ASSESSMENT-v0.1.md`

出口标准：

- 领域上下文、聚合、事件和状态机完成审查。
- Cap-Spec 和验收场景通过审查。
- event / reason / status code 提案通过审查。
- TDD 矩阵覆盖 scope-first、banned、断链、owner view、raw observation、日志泄漏、硬件配置和 evidence feed 行为。
- 字段范围版本、留存访问、飞书门禁完成规格。
- 安装前置由行政部门完成的边界写入规格。

## 4. R2 alpha0-lite

目标：

- 证明已批准元数据可以被安全提取和清洗。

允许：

- Codex 订阅和 `heiyucode.com` API 密钥使用的合成样本。
- 只使用 synthetic fixture。
- sanitizer / parser。
- 本地输出。
- banned 字段泄漏测试。
- Tool Source Registry 原型。

不允许：

- 真实员工 runtime 数据。
- 安装。
- 常驻 runtime。
- 受管 launch daemon。
- banned 字段。
- 大辉子 evidence feed。
- 飞书台账。
- 绩效集成。

出口标准：

- RED 测试证明 sanitizer 缺失时失败。
- GREEN 测试通过。
- banned 字段不出现在输出、日志、错误消息、debug dump、metrics label 或测试快照中。
- 输出只包含 allow 字段。
- raw event 不跨越本地测试边界。
- 未登记工具来源不能进入 sanitizer。
- Codex 订阅和 `heiyucode.com` API 密钥使用样本通过 banned 泄漏测试。

## 5. R3 Endpoint Sentinel Alpha

目标：

- 在受控内部设备上构建最小端点哨兵 runtime。

范围：

- 默认 Windows 公司固定资产电脑。
- Mac 为第二平台。
- 设备必须完成制度告知与签字确认。
- 员工个人电脑不进入强制部署范围；自愿安装不作制度规定。
- Linux、移动端和其他平台不支持。

允许：

- 企业受管安装原型。
- 设备绑定。
- 员工工程身份绑定。
- 开机自启原型。
- 常驻 runtime。
- 签名心跳。
- 健康状态。
- 本地 owner view 原型。
- raw observation 内存候选输入。
- 当前安装电脑硬件配置信息采集。
- 人工指定和登记设备。

不允许：

- raw observation 持久化、日志化、导出或展示。
- 大辉子生产 evidence feed。
- 飞书绩效台账写入。
- 内核级防篡改。
- 内容采集。
- banned 字段。
- MDM 或类似平台接入。
- LTC 参与资产管理。

出口标准：

- 端点可在受控设备上安装并绑定。
- 心跳被签名。
- 健康状态可见。
- owner view 显示采集字段类别、制度版本、确认版本和 runtime 状态。
- 员工本地关闭 / 卸载 / 绕过不可用。
- raw observation 不落盘、不日志化、不下游化测试通过。

## 6. R4 Internal Beta

目标：

- 在有限试点组中以企业基础设施方式运行 LTC。

前置：

- 人工指定和登记流程已完成。
- 字段范围版本机制已完成。
- 留存、访问、审计、申诉 SLA 已完成规格。

允许：

- 受管安装。
- 受管 launch daemon 或平台等价机制。
- 管理员控制停用 / 卸载。
- 管理员操作签名审计。
- 心跳缺失告警。
- 断链事件创建。
- 员工异常说明。
- 签名 evidence feed dry run（证据流试跑）。

不允许：

- raw event 导出。
- 未进入字段范围版本的字段。
- LTC 写入绩效台账。
- dry run 进入正式绩效台账、公告、薪酬、纪律或考核结论。
- 黑箱防篡改。
- MDM 或类似平台接入。
- LTC 参与资产管理。

出口标准：

- 试点组设备保持预期 runtime 状态。
- 断链事件已签名且可说明。
- owner view、evidence package 状态和 hash-only 说明 / 申诉路径可用。
- evidence feed dry run 只包含 sanitized aggregate 和 evidence reference。
- dry run 与正式绩效流程隔离可审计。

## 7. R5 DahuiZi Evidence Feed

目标：

- 将 LTC evidence feed 接入大辉子。

允许：

- 发布 sanitized aggregate。
- 发布 evidence reference。
- 发布 break-chain status（断链状态）。
- 发布 compliance status（合规状态）。
- 生成面向大辉子的 dry-run delivery plan 和 evidence reference；不证明大辉子已消费，也不产生正式绩效证据项。

不允许：

- LTC 绩效评分。
- LTC 写飞书台账。
- LTC 发飞书公告。
- raw event 共享。
- R5 evidence feed 自动进入正式绩效台账、公告、薪酬、纪律或考核结论。

出口标准：

- LTC 可生成面向大辉子的 evidence feed dry-run delivery plan。
- 大辉子真实消费和绩效证据项创建等待 R6 / 外部门禁，不作为 R5 完成项。
- evidence feed 包含制度版本、字段范围版本、确认版本、签名和期间。
- connector dry-run response 只包含 request hash、response status、retry policy 和 audit hash。
- banned 字段不进入大辉子。
- break-chain 只作为证据完整性和合规状态，不自动等价为绩效负面。
- 正式绩效使用必须等待 R6 门禁。

## 8. R6 Performance Integrated

目标：

- 通过大辉子完成绩效管理集成。

允许：

- 大辉子依据制度文件分析和统计绩效证据。
- 大辉子写入飞书绩效台账。
- 大辉子发布飞书公告。
- LTC 提供 evidence reference 和 aggregate。

不允许：

- LTC 直接评分。
- LTC 直接排名。
- LTC 提供薪酬建议。
- LTC 裁决纪律处分。
- LTC 直接写飞书台账或公告。
- 飞书公告暴露 raw event、banned 字段或不必要个人细节。

出口标准：

- 绩效台账引用 LTC 证据，但不暴露 raw event。
- 公告由大辉子发布。
- 公告可见范围、员工说明关联、敏感信息排除和必要审批完成。
- 审计轨迹关联制度版本、确认版本、证据引用和大辉子裁决记录。

## 9. 跨阶段门禁

| Gate | 要求 |
|---|---|
| G1 Field Gate | scope-first / banned 字段由测试强制执行，字段范围内尽量齐全。 |
| G2 Raw Boundary Gate | raw observation 不落盘、不日志化、不下游化。 |
| G3 Acknowledgement Gate | 下游证据必须包含制度版本、字段范围版本和制度确认版本。 |
| G4 Runtime Gate | R3 后员工本地关闭 / 卸载 / 绕过不可用。 |
| G5 Owner View Gate | 员工可查看字段类别、状态、断链、制度版本、说明和申诉路径。 |
| G6 Dahuizi Gate | 只有大辉子写入绩效台账和公告。 |
| G7 Audit Gate | 证据引用、签名、制度版本、确认版本、留存、访问和管理员动作可审计。 |
| G8 Field Scope Gate | 字段范围版本化、员工可见、通过 banned 泄漏测试并可回滚。 |
| G9 Dry Run Isolation Gate | R4/R5 dry run 不得进入正式绩效结论。 |
| G10 Feishu Gate | 飞书台账和公告不得包含 raw event、banned 字段或不必要个人细节。 |
| G11 Platform Gate | 强制部署仅限公司固定资产电脑；Windows 优先，再 Mac，仅支持双平台。 |
| G12 Asset Boundary Gate | LTC 只采集安装电脑硬件配置，不参与资产管理，不接入 MDM。 |

## 10. 近期下一步

实施前必须先完成：

1. 审查并批准 R0 active baseline。
2. 完成 R1 验收场景。
3. 完成 R1 HPRD。
4. 完成 R1 技术设计。
5. 完成 R1 event / reason / status code。
6. 完成 R1 TDD 矩阵。
7. 完成字段范围版本规格。
8. 完成留存与访问控制规格。
9. 完成飞书台账与公告门禁规格。
10. 然后才能启动 R2 alpha0-lite 实现。
