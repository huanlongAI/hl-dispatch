# HL AI-Native Value Stream Operating Model v1.0

> Status: ACTIVE_OPERATING_MODEL
> Effective Date: 2026-06-25
> Owner: Founder / hl-dispatch operating layer
> Supersedes:
> - HL-AI-NATIVE-CAPABILITY-OPERATING-RULES-v0.2.md
> - HL-CAPABILITY-OPERATING-RULES-IMPLEMENTATION-PLAN-v0.1.md for execution

## 中文摘要
本文档将唤龙 AI 原生价值流运行模型锁定为当前正式运行模型。
它不是试点、实验、仪表盘、模板扩写或历史治理回填计划。
它规定团队如何把一个能力价值切片从任务书推进到可运行制品、独立验证和 Founder 最终验收。
核心变化是：工作不再围绕分散任务、状态回填和反复催办组织，而是围绕一个完整价值结果、一个唯一 DRI、一个中文上下文面、一个可运行制品和一次最终验收组织。
本文档不授权 production runtime、active registry、formal OpenAPI、facts / events / reason_code 注册、真实客户数据、真实资产变更、payment、database、deploy、release 或 MVP / production 声明。

## 术语说明

| 术语 | 中文说明 |
|---|---|
| `ACTIVE_OPERATING_MODEL` | 当前生效的组织运行模型状态。 |
| Capability Value Slice | 能力价值切片，指一个可独立验收的最小完整价值结果。 |
| 唯一 DRI | 一个切片只有一个直接负责人，负责结果、范围、证据和下一步。 |
| 中文上下文 | 团队成员必读的中文任务书和上下文包。 |
| 触发式 owner pull | 只有出现明确触发事实时才拉入判断域 owner。 |
| 独立验证 | 非作者 reviewer 对制品、证据、边界和失败路径进行验证。 |
| Learning Patch | 切片关闭后沉淀的一条紧凑复利规则或上下文修正。 |
| Founder final acceptance | Founder 对完整结果做一次最终整体验收。 |

## 1. Founder 模型锁定
Founder 已将本文档锁定为唤龙 dispatch 侧当前正式运行模型。
该模型用于真实能力价值流执行，而不是用于证明是否应该采用该模型。
后续 activation wave 只验证执行一致性、边界有效性和可复用参数，不重新讨论 v1.0 是否生效。
如果旧文档、旧提示词、旧任务书或历史评论仍使用 pilot、experiment、试跑、接受 / 拒绝 DRI 等语言，以本文档为当前执行口径。
如果具体仓库的安全边界、branch protection、CODEOWNERS、runtime 权限或 contract 权限比本文档更严格，以更严格规则为准。

## 2. 第一性目标
本模型的目标是改变真实工作方式。
工作必须围绕以下对象组织：

1. 一个明确的价值结果；
2. 一个能力价值切片；
3. 一个唯一 DRI；
4. 一个中文上下文面；
5. 一个可运行、可测试、可独立验证的制品；
6. 一次 Founder 最终整体验收。
本模型反对以下漂移：

1. 主要交付治理文档而没有可运行结果；
2. 用 Ledger 或状态评论替代制品；
3. 把多人共享责任误当成 DRI；
4. 要求成员阅读英文提示词后才能开工；
5. 对 CP0-CP2 普通动作反复请求 Founder 批准；
6. 用飞书已读、CI green 或 AI 自检替代 GitHub SSOT 证据；
7. 每个中间状态都产生新的模板、仪表盘或 Learning Patch。

## 3. Active Model、Activation Wave 与 M0-M9

`ACTIVE_OPERATING_MODEL` 表示本文档是当前运行权威。
Activation Wave 是把该模型应用到真实能力切片上的一轮执行。
Activation Wave 只验证模型执行质量，不决定模型是否仍然有效。

M0-M9 是能力成熟度视图。
一个切片可以在 v1.0 下执行，但不自动改变该能力的 M0-M9 成熟度。
Ledger 必须区分以下状态面：

| 状态面 | 说明 |
|---|---|
| active operating model | 团队如何组织工作 |
| activation wave | 当前正在执行哪些真实价值切片 |
| M0-M9 maturity | 能力本身成熟度 |
| runtime authorization | 是否被授权进入运行态或正式注册 |
任何 activation wave 都不得被解释为 production、release、MVP、active contract 或 runtime 授权。

## 4. 十条不变量

1. 正式工作单元是完整 Capability Value Slice。
2. 一个切片只有一个唯一 DRI。
3. DRI 由组织任命，任命默认生效。
4. AI 必须先编译中文上下文，供团队直接开工。
5. DRI 在锁定范围内自主推进。
6. 判断域 owner 只在触发事实出现时被拉入。
7. Founder 不做日常中间审批和催办。
8. 交付必须是完整可运行制品，并经过独立验证。
9. A-only Ledger 是唯一运行状态面，只保留一个当前下一步。
10. Learning Patch 在切片关闭后判断，不在每个中间状态产生。
这些不变量优先于旧习惯和旧流程词汇。

若要改变这些不变量，必须有新的 Founder 明确裁决。

## 5. Capability Value Slice 定义
Capability Value Slice 是一个能力中最小的完整价值结果。
它必须能被用户、操作员、reviewer 或下游系统独立观察和验收。
一个合格切片至少包含：

1. 明确的价值陈述；
2. capability id；
3. slice id；
4. scope in；
5. scope out / not_authorized；
6. 唯一 DRI；
7. 实现或制品入口；
8. 单命令或等价可运行验收面；
9. 正向、失败、边界、无副作用证据；
10. 独立验证；
11. Founder 最终验收包；
12. Ledger 收口；
13. Learning Patch 判断。

只有任务书、状态表、模板、scorecard、dashboard、Ledger row 或链接集合，不构成完整价值切片。

## 6. 角色与责任

### 6.1 Founder
Founder 负责锁定价值目标、边界、必要的人选裁决和最终验收。
Founder 不负责 CP0-CP2 普通推进批准。
Founder 不做日常代码 review。
Founder 不为类名、字段名、fixture 命名、测试 ID 或可逆内部结构做决策。
Founder 只在明确触发事实出现时介入。

### 6.2 AI Context Compiler

AI Context Compiler 负责把分散证据整理成中文任务书和中文上下文包。

上下文包必须说明：

1. 来源；
2. 中文结论；
3. 本任务如何使用；
4. scope in；
5. scope out；
6. not_authorized；
7. 当前唯一下一步。

AI 不得把英文提示词、旧治理材料或分散链接直接丢给团队成员自行拼装。

### 6.3 DRI
DRI 是 Directly Responsible Individual，即直接负责人。
DRI 负责一个完整切片的结果，而不是只负责代码开发。
DRI 可以委托劳动、请求 review、拉入 owner、组织修复和准备最终验收候选。
DRI 必须持续维护唯一下一步。
DRI 不拥有 runtime、contract、production、payment、privacy、database 或 release 授权。
DRI 不需要回复是否接受任务。
DRI 的已阅回执只证明上下文送达、当前理解和下一步动作。

### 6.4 Judgment Owner

Judgment Owner 是被触发式拉入的判断域 owner。

典型 owner 包括 PM、Gate、Engineering、Security、Finance、Privacy、Contract 或相关 capability owner。
owner 被拉入时，应收到有事实、有选项、有默认安全处理的决策请求。
owner 不应被模糊请求“请指导”或“请确认下一步”。

### 6.5 Independent Verifier

Independent Verifier 是非作者 reviewer。

独立验证检查：

1. 制品是否可运行；
2. 证据是否覆盖正向路径；
3. 证据是否覆盖失败路径；
4. scope 隔离是否成立；
5. 越权意图是否被拒绝；
6. 无副作用声明是否有证据；
7. 是否触碰 not_authorized；
8. 是否存在 AI 自写自证。

AI 自检、CI green 和作者说明都是证据材料，但不能替代独立验证。

## 7. 标准 F0-F8 工作流

| 步骤 | 名称 | 结果 |
|---:|---|---|
| F0 | 模型与 live-state precheck | repo、Issue、branch、PR、权限和旧状态完成对账 |
| F1 | 中文上下文编译 | 一个中文任务书和上下文包 |
| F2 | Dispatch lock | DRI、范围、分支、Ledger row、verifier 路径锁定 |
| F3 | Executable spine | 最小可运行路径或 failing acceptance test 出现 |
| F4 | Artifact completion | 完整制品、测试、fixture、证据形成 |
| F5 | Independent verification | 非作者 review 给出结论和 actionable finding |
| F6 | Founder final acceptance packet | 一个整合验收包 |
| F7 | Close | Founder 接受后合并、关闭、Ledger、Learning Patch |
| F8 | Next wave packet | 给出下一波候选，不重开模型设计 |
如果 v1.0 激活时某个切片已经部分完成，应以 live GitHub 和当前 repo 证据判断它处于哪一步。
不得为了匹配过期本地记录而把工作倒退。

## 8. 组织任命 DRI 与中文已阅
DRI 由组织任命。

任命立即生效。
标准回执为：

```text
DRI已阅

当前理解：
<1-3 句话复述完整交付结果>

下一步唯一动作：
<一个立即可执行动作>

预计首次可运行骨架时间：
<时间>

需要拉入 owner：
无
或
<触发事实、对象、所需决策>
```
如果存在客观阻塞，使用：

```text
DRI阻塞报告

阻塞事实：
影响：
已尝试：
建议处理：
最晚需要裁决时间：
```
禁止使用：

1. `DRI_ACCEPTED`；
2. `DRI_DECLINED`；
3. `Do you accept?`；
4. `是否愿意承担？`。
一个工作日没有回执，记为沟通或容量 blocker。
它不是拒绝。

## 9. 触发式 Owner Pull
owner pull 只由明确事实触发。

允许触发：

1. 价值结果或验收语义出现两种以上合理解释；
2. 需要触碰 not_authorized；
3. 需要 runtime、registry、formal contract、real data、mutation、payment、privacy、identity 或 database；
4. 独立验证出现重大证据失败；
5. DRI 对不可逆决策置信度不足；
6. owner 冲突阻塞切片；
7. DRI 沟通或容量 blocker 阻止继续推进。
owner pull 必须使用：

```text
触发事实：
为什么现在必须决策：
可选方案：
DRI 建议：
默认安全处理：
最晚需要决策时间：
```
以下事项不得触发 owner pull：

1. 类名；
2. 方法名；
3. fixture 字段名；
4. 测试 ID；
5. 可逆代码结构；
6. 普通 review comment；
7. 分支细节；
8. 可逆文案调整。

## 10. Ledger 规则
Ledger 是 dispatch 侧唯一运行状态面。
Ledger 规则：

1. 一个 active execution item 对应一行；
2. 一个 DRI；
3. 一个 current next_action；
4. 一个 risk_class；
5. 一个 execution_state；
6. 明确 not_authorized；
7. 链接 GitHub SSOT，不复制整个 Issue；
8. 只记录当前证据链接；
9. 不创建第二状态表；
10. 不用 Ledger row 宣称 maturity 升级。
Ledger 只能跟随真实 checkpoint 更新。
不得把广义 readiness 历史回填当作交付。

## 11. PR 与最终验收证据
证据应集成在 implementation PR、control PR 和最终 Founder 验收包中。

最小证据包括：

1. 单命令验收面；
2. 确定性合成输入；
3. 确定性输出；
4. 正向路径；
5. 失败路径；
6. 缺失或错误上下文；
7. scope 隔离；
8. 显式和嵌套越权意图拒绝；
9. 重复运行无副作用；
10. 仓库测试或门禁；
11. 非作者独立验证。

只有在仓库既有规则要求时，才创建单独 Evidence Bundle 文件。
不得默认新增证据模板家族。

## 12. Learning Patch 规则
Learning Patch 在切片关闭后选择。

每个切片最多选择一类：

1. `RULE_PATCH`；
2. `AGENT_PROMPT_PATCH`；
3. `CONTEXT_PATCH`；
4. `GATE_PATCH`；
5. `TEMPLATE_PATCH`；
6. `DEFER_PATCH`；
7. `NO_SYSTEM_PATCH_JUSTIFIED`。
Learning Patch 应紧凑，通常不超过十行。
它记录可复用经验，不复述整条任务流水。
不得在 CP0-CP2 为每次状态变化创建 Learning Patch。

## 13. Founder 不介入规则
Founder 的正常触点只有：

1. Day 0 价值与边界锁定；
2. 明确触发事实出现时的 bounded decision；
3. 最终整体验收。
Founder 不催办 DRI。
Founder 不批准普通 CP0-CP2 推进。
Founder 不做普通代码 review。
Founder 不审批中间工件。
Founder 简报必须区分：

1. 已裁决；
2. 等待 owner/action；
3. 未来条件触发裁决。

已经裁决的事项不得重复请求同一裁决。

## 14. Wave 0-4 Rollout
Wave 0：锁定 v1.0，并把正在执行的 bounded slice 转换为 v1.0 语言。
Wave 1：用一个真实 activation cycle 跑完整闭环。
Wave 2：提出两个下一波候选。
Wave 3：重复执行并提高 owner pull 信号质量。
Wave 4：复盘指标，删除浪费，保留有效机制。
Wave 用于验证可重复性。
Wave 不用于每轮重新设计模型。

## 15. 指标

### 15.1 结果指标

1. 完整可运行制品是否交付；
2. 独立验证是否完成；
3. Founder final acceptance 是否发生；
4. 是否未跨越 not_authorized；
5. Ledger 是否在关闭时准确；
6. Learning Patch 判断是否完成。

### 15.2 行为指标

1. CP0-CP2 Founder 普通审批次数；
2. Founder 催办次数；
3. owner pull 次数；
4. owner pull 是否有具体触发事实；
5. DRI readback 到 executable spine 的时间；
6. executable spine 到 independent verification 的时间。

### 15.3 Anti-Drift 指标

1. 额外 taskbook 数量；
2. 额外 dashboard 或 scorecard 数量；
3. 没有 action 的状态评论数量；
4. 裸 GitHub 编号导致误链接数量；
5. closure 前产生的 Learning Patch 数量。
目标不是零沟通。
目标是 ownership 清楚、虚假决策更少、真实交付更多。

## 16. 非授权边界
本文档不授权：

1. production runtime；
2. active registry；
3. formal OpenAPI；
4. facts / events / reason_code registration；
5. capability manifest 或 runtime fragment onboarding；
6. real customer data；
7. real asset mutation、lock、deduction、transfer；
8. payment、refund、settlement、billing；
9. database、JPA、Flyway、production table；
10. deploy 或 release；
11. MVP、production、ready、authorized 等正式声明。
任何进入这些区域的请求，都必须另行走对应仓库和对应 owner 的 Founder / Gate decision。

## 17. Anti-Overgovernance 规则

默认不创建：

1. 第二个 taskbook 文件；
2. 第二个 context pack 文件；
3. 新 scorecard；
4. dashboard；
5. weekly meeting spec；
6. 第二个 Ledger；
7. 新 maturity model；
8. 新 activation state machine；
9. 并行 B-Lite artifact；
10. 以治理回填为主要交付的任务。
运行模型已经锁定。
后续工作应产出价值切片。

## 18. 当前 Activation Cycle 1
Activation Cycle 1 的 principal issue 是 [huanlongAI/hl-dispatch#408](https://github.com/huanlongAI/hl-dispatch/issues/408)。
Capability 是 `biz.customer.asset`。

Slice 是 `CARD-002-SLICE-03_customer_asset_usage_eligibility_preview`。
DRI 是 `zhoufei1223`。

Preferred independent verifier 是 `wp159951`。

预期价值结果是在 fixture-only、无真实副作用边界内完成客户资产使用资格预览。
该 activation cycle 用于验证 v1.0 的执行一致性和参数调优。
它不重新决定 v1.0 是否生效。
