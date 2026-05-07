# 大辉子评审任务：LTC R0/R1 规格草案

**日期**：2026-05-06
**来源**：NODE-A Codex Desktop 会话
**目标智能体**：大辉子（二级节点领域智能体）
**模式**：只读评审 / 裁决建议
**目标仓库**：`/Users/node-a/Workspace/01_Repos/huanlong/hl-dispatch`

## 背景

创始人已重新裁决 LTC 的产品定位：

LTC-Endpoint 是大辉子的企业端点工具与哨兵基础设施。它部署在员工工作设备上，采集 AI 驱动工作过程的规范化元数据，生成 `sanitized event`、`aggregate` 和 `evidence reference`，供大辉子依据制度文件进行工程治理、绩效分析、统计裁决，并发布到飞书台账和公告。

LTC 本身不直接输出绩效分、员工排名、薪酬建议或纪律处分结论。员工无本地关闭、退出、卸载或绕过权限。禁止采集 prompt、completion、transcript、文件内容、URL、窗口标题、剪贴板、按键、截图、屏幕录制、非工程应用清单等 banned 字段。

## 待评审文件

请评审以下 4 份中文规格草案：

1. `deliverables/specs/ltc/LTC-GOVERNANCE-REBASELINE-v0.1.md`
2. `deliverables/specs/ltc/LTC-DOMAIN-MODEL-v0.1.md`
3. `deliverables/specs/ltc/LTC-CAP-SPEC-v0.1.md`
4. `deliverables/specs/ltc/LTC-IMPLEMENTATION-ROADMAP-v0.1.md`

## 评审重点

请从大辉子作为二级节点领域智能体的角度评审：

1. 这 4 份规格是否准确表达“大辉子是绩效裁决主体，LTC 是端点工具”的边界。
2. D0-D8 决策树是否完整，是否还有必须先由创始人裁决的缺口。
3. DDD 领域模型中的 bounded context、aggregate、domain event、state machine 是否足以支撑后续实现。
4. SDD 规格路径是否符合“先规格、后实现”的原则。
5. R0-R6 阶段边界是否合理，是否存在过早进入 runtime、绩效集成或字段扩张的风险。
6. 是否存在与企业绩效制度、员工签字确认、飞书台账和公告流程的冲突或缺项。
7. 是否存在法务/用工治理、隐私、合规或组织执行层面的高风险表述。
8. 哪些旧 P0 文档口径必须被明确废止，哪些安全边界必须永久保留。

## 输出要求

请只输出评审结论，不直接修改文件、不提交、不推送。

输出结构：

```markdown
# 大辉子评审结论：LTC R0/R1 规格草案

## 总体结论

- 结论：通过 / 有条件通过 / 不通过
- 核心理由：

## 必须修改

| 编号 | 文件 | 问题 | 建议修改 |
|---|---|---|---|

## 建议修改

| 编号 | 文件 | 问题 | 建议修改 |
|---|---|---|---|

## 需创始人裁决

| 编号 | 裁决问题 | 推荐口径 | 原因 |
|---|---|---|---|

## 实施前门禁

- [ ] 门禁项

## 风险清单

| 风险 | 等级 | 缓解建议 |
|---|---|---|
```

## 禁止事项

- 不得直接实施。
- 不得改写仓库文件。
- 不得把 LTC 解释为直接绩效评分器。
- 不得建议采集 banned 字段。
- 不得建议员工拥有本地关闭、退出、卸载或绕过权限。

## 评审回写

**派发任务 ID**：`air-dispatch-20260506T080428Z-NODE-C-dahuizi`
**评审结论**：有条件通过
**回写时间**：2026-05-06
**执行状态**：已按大辉子 M1-M8 必须修改项修订 LTC R0/R1 规格草案，尚未进入代码实施。

### 核心裁决

- 规格总体准确表达“大辉子是绩效裁决主体，LTC 是端点工具、证据生产者和哨兵基础设施”。
- banned 字段、raw boundary、LTC 不直接评分/排名/薪酬/纪律处分等核心安全边界成立。
- 实施前必须补齐用工确认、raw observation 留存、字段范围版本、R4/R5/R6 绩效集成边界、飞书公告流程和合规治理。

### 已并入规格的必须修改项

| 编号 | 并入口径 |
|---|---|
| M1 | R2 仅 synthetic fixture；R3 以后 raw observation 只能作为内存候选输入，不得持久化、日志化、导出或展示。 |
| M2 | `riskFlags`、`evidenceCompleteness`、`breakChainSummary` 只表示证据完整性、采集链路状态、制度版本一致性，不表示员工态度、绩效风险或 HR 标签。 |
| M3 | 大辉子原建议为 conditional 字段逐项审批；创始人后续裁决为字段可以先行，在采集范围内尽量齐全，但必须版本化、员工可见并通过 banned 泄漏测试。 |
| M4 | 增加 PolicyVersion、FieldScopeVersion、RetentionPolicy、EvidenceAccessGrant、AuditAccessLog 等治理聚合。 |
| M5 | R4/R5 dry run 或 evidence feed 接入不得进入正式绩效台账、公告、薪酬、纪律或考核结论。 |
| M6 | 使用“制度告知与签字确认”口径，`consentVersion` 解释为制度确认版本。 |
| M7 | 增加飞书台账与公告门禁，大辉子写入/发布前必须校验版本、证据引用、说明关联、可见范围和敏感信息排除。 |
| M8 | 旧 P0 文档必须标注 Superseded / Historical Only，并指向新治理重基线。 |

### 创始人后续裁决回写

- C1：强制部署仅限公司固定资产电脑；优先 Windows，再 Mac，仅支持 Windows / macOS 双平台。
- C2：员工个人电脑不纳入强制范围；员工自愿选择可安装，不作制度规定。
- C3：安装前置工作由行政部门处理完毕；LTC 接入视为前提合规流程已完毕，未处理不会进入安装环节。
- C5：暂不接入 MDM 等平台；公司资产由公司分配给员工使用，人工指定和登记；LTC 只采集当前安装电脑硬件配置信息，不参与资产管理。
- C6：字段可以先行，在采集范围内尽量齐全；banned 字段永久禁止。
- C8：首批工具来源为 Codex 订阅和 `heiyucode.com` API 密钥使用。
- C9-C13：同意大辉子建议。
- C14：旧 P0 文档如能安全删除则优先删除，不能安全删除则采取 Historical Only / Superseded 标注方案。
