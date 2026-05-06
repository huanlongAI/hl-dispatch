# 测试团队首个能力包接入前启动任务书 v0.4

> 日期：2026-05-06  
> 状态：PUBLISHED，已吸收大辉子主脑二次评审 P1/P2 修正，并经 Founder 授权发布  
> 面向对象：李云峰 / 测试组长（兼架构师）+ 测试成员 3 人  
> 目标：在首个真实能力包进入 QA 放行 / 合并门禁前，完成 QA Bootstrap 基建，确保测试团队可以独立执行“先审阅，再批准发布”的 qa-verdict 工作流。  
> 发布边界：本文已发布到测试团队频道 `qa.html`，用于测试团队启动执行；不自动改平台代码。  
> v0.2 修订来源：大辉子主脑评审 `air-dispatch-20260506T100627Z-NODE-C-dahuizi`，结论 `CONDITIONAL PASS`。  
> v0.3 修订来源：Founder 口径确认“组长即架构师，角色不要分太多，只有组长与成员”。  
> v0.4 修订来源：大辉子主脑二次评审 `air-dispatch-20260506T101912Z-NODE-C-dahuizi`，结论 `CONDITIONAL PASS`。  
> v0.4 最终复核：大辉子主脑 `air-dispatch-20260506T102316Z-NODE-C-dahuizi`，结论 `PASS`。  
> 发布授权：Founder 指令“发布并通知”。

## 0. v0.4 修订摘要

本版在 v0.3 基础上修正大辉子二次评审提出的 P1/P2 问题，并保留大辉子主脑 v0.2 评审提出的 4 个关键修正：

1. 将 `qa-verdict Required Status Check` 从“草案/可选”升级为首包前硬门槛。
2. 澄清 `UI_AUTO / PENDING / G-023` 边界：首包绿线只覆盖 `API_EXEC` / `AUDIT_EXEC`；`UI_AUTO` 在 Phase 1 前不进入阻断门禁，除非已有稳定实现。
3. 收紧首包准入豁免权：P0/P1 门槛不得由测试组长单独豁免，必须 Founder 或指定治理 Owner 批准。
4. 为关键交付物指定单一 DRI，工程支持只做实现协助，不拥有 QA verdict 或 QA 基建验收权。
5. 按 Founder 口径收敛测试团队角色模型：测试团队内部只设“测试组长（兼架构师）”与“测试成员”，不再拆分多层测试角色。
6. 区分样例 PR dry run 与真实首包门禁：样例 PR 可等价模拟，真实首包进入 QA 放行 / 合并门禁前必须落地真实 `qa-verdict` required status check。
7. 修正 G-026 交付权责：测试组长拥有 G-026 QA 基建 DRI 与最终验收权，后端只做技术实现与技术确认。

## 1. 任务背景

测试团队已经被定义为质量与验收责任方，不再是单纯手动测试执行者。首个能力包接入后，QA 需要独立承担：

- `acceptance-manifest.yaml` 验收映射。
- 验收测试套件设计与执行。
- Evidence Pack 证据审阅。
- `qa-verdict` Required Status Check 质量放行。
- 回归基线维护。

如果等首个能力包 PR 打开后再准备模板、脚本和证据标准，QA 会成为交付瓶颈。因此必须先做一轮 QA Bootstrap。

## 2. 权威依据

本任务书消费以下真源，不替代真源：

- `hl-contracts/governance/DD-TEST-v1.md`：测试工程推导 v1.2。
- `hl-contracts/governance/TECH-STACK-SPEC-v3.md`：技术栈 v3.4，含测试工具锁定。
- `hl-dispatch/deliverables/decisions/TEAM-COLLABORATION-SPEC-v2.1.md`：测试团队质量与验收责任、能力包流。
- `hl-dispatch/deliverables/decisions/TOOLCHAIN-GUIDE-v1.md`：测试工具、门禁与 required status checks 操作指南。
- 站点投影：`https://huanlongai.github.io/hl-dispatch/pages/qa.html`

冲突仲裁规则：

- 任务书与 DD-TEST / TECH-STACK 冲突时，以 `hl-contracts` 为准。
- 任务书与 TEAM-COLLAB 冲突时，以 TEAM-COLLAB 为准。
- 任务书与站点投影冲突时，以站点背后的源文档为准。

## 3. 启动目标

### 3.1 必达目标

首个真实能力包进入 QA 放行 / 合并门禁前，测试团队必须具备以下能力：

1. 能读懂 Cap-Spec-2 Case-ID，并判断是否可测。
2. 能按标准创建 `acceptance-manifest.yaml`。
3. 能运行 G-026 manifest YAML 校验。
4. 能编写最小 JUnit 5 参数化验收测试。
5. 能理解 Testcontainers + PostgreSQL 18.x 的集成测试证据。
6. 能按 Evidence Pack 模板审阅证据。
7. 能按 checklist 判断 `qa-verdict = PASS / FAIL`。
8. 能用一个样例 PR 演练完整流程。
9. 能证明 `qa-verdict` required check 在缺证据、G-026 失败、G-023 缺失、G-023 失败时不能通过。

### 3.2 首包绿线范围

首包前 QA 绿线只覆盖：

- `API_EXEC`：JUnit 5 参数化验收测试。
- `AUDIT_EXEC`：确定性审计脚本 / Gradle task / 可复现命令。
- G-026：manifest YAML 结构与覆盖声明校验。
- G-023：已标记为 `COVERED` 的 API / AUDIT 验收场景回放。
- Evidence Pack：证据完整性审阅。
- `qa-verdict`：required status check。

首包前不进入阻断门禁：

- `UI_AUTO`：在 Phase 1 前只能作为非阻断候选或 UAT 里程碑项，除非已有稳定自动化实现并经 Founder / 治理 Owner 批准。
- Playwright：学习入口，不是 PR 绿线。
- PIT / SonarQube：Phase 1+ 候选，不是首包前置绿线。
- QA 指标仪表板：可选增强，不阻断首包。

### 3.3 不做事项

本启动任务不做以下事项：

- 不把 Playwright 变成 PR 绿线。
- 不提前引入 PIT / SonarQube 作为阻断门禁。
- 不用 H2 替代 Testcontainers。
- 不新增 Kotest `FunSpec` / `StringSpec` 风格测试。
- 不让 PM 或工程师代签 `qa-verdict`。
- 不把 `qa-verdict` 等同于 PM acceptance 或生产发布批准。

## 4. 团队分工与 DRI

### 4.1 角色职责

| 角色 | 人数 | 启动期职责 |
|------|------|------------|
| 测试组长 / 李云峰（兼架构师） | 1 | 统筹任务书执行；制定 manifest 标准、G-026 规则、验收测试骨架、质量度量与 Evidence Pack 结构；确认 QA verdict 签字边界；组织样例 PR 演练；向 Founder 汇报阻塞项 |
| 测试成员 | 3 | 按测试组长分配完成样例 `acceptance-manifest.yaml`、Case-ID 映射清单、JUnit 5 参数化验收测试样例、Evidence Pack 模板、CI 报告解读手册、qa-verdict checklist 与演练执行 |
| 后端工程师支持 | 1-2 | 协助 Testcontainers / Gradle / CI 接口，不拥有 QA verdict |
| 运维支持 | 1 | 协助 required status check / GitHub Actions / 云效回推方案，不拥有 QA verdict |
| PM 支持 | 1 | 提供样例 Cap-Spec-2 Case-ID，不拥有 QA verdict |

### 4.2 单一 DRI 表

| 交付物 | DRI | 支持方 | 最终验收 |
|--------|-----|--------|----------|
| Manifest 模板与样例 | 测试组长 | 测试成员 | 测试组长 |
| G-026 规则标准 | 测试组长 | 测试成员 | 测试组长 |
| G-026 脚本实现接入 | 测试组长 | 后端工程师支持 / 测试成员 | 测试组长 |
| G-026 技术实现可运行性确认 | 后端工程师支持 | 测试组长 | 后端负责人技术确认，不作为 QA 基建验收 |
| JUnit 5 验收测试骨架 | 测试成员 | 后端工程师支持 | 测试组长 |
| Testcontainers 证据样例 | 后端工程师支持 | 测试成员 | 测试组长 |
| Evidence Pack 模板 | 测试组长 | 测试成员 | 测试组长 |
| qa-verdict checklist | 测试组长 | 测试成员 | Founder |
| required status check 样例 PR dry run 验证 | 运维支持 | 测试组长 / 后端工程师支持 | Founder 或指定治理 Owner |
| 真实首包 required status check 接入目标 repo / branch protection / CI | 运维支持 | 测试组长 / 后端工程师支持 | Founder 或指定治理 Owner |
| 样例 PR 演练报告 | 测试组长 | 测试成员 | Founder |

DRI 规则：

- DRI 对交付物完整性负责。
- 支持方只协助实现，不拥有最终口径。
- `qa-verdict` 的签字权只属于测试组长，不属于测试成员、工程、PM、运维。
- 后端负责人可以对脚本可运行性做技术确认，但不拥有 G-026 规则口径或 QA 基建验收权。

## 5. 启动计划

### D0：Kickoff 与边界确认

目标：所有参与者先对齐“QA 是独立质量责任方”。

任务：

- 测试组长组织 30 分钟启动会。
- 全员阅读 `qa.html#quickstart` 与 `qa.html#qa-workflow`。
- 测试组长带读 DD-TEST v1.2 中 JUnit 5 / Kotest Property / Testcontainers / G-026 / G-023 关键条款。
- 明确首轮样例能力包使用 `biz.demo.acceptance`，只做演练，不进入产品发布。
- 明确 `UI_AUTO` 在 Phase 1 前不进入首包阻断门禁。

交付物：

- `QA Bootstrap Kickoff Notes`。
- 参与人员名单。
- 风险与问题清单初版。

验收标准：

- 每个成员能说清楚 `qa-verdict` 与 PM acceptance 的差异。
- 每个成员能说清楚 `UI_MANUAL` 不进 PR 自动化门禁。
- 每个成员能说清楚首包绿线只覆盖 `API_EXEC` / `AUDIT_EXEC`。
- 测试组长确认本启动任务不引入新绿线工具。

### D1：Manifest 标准与样例

目标：先让“验收场景如何变成可执行映射”标准化。

任务：

- 测试组长定义 `acceptance-manifest.yaml` 模板。
- 模板必须包含 `manifest_version` / `schema_version` 字段。
- 测试成员用 `biz.demo.acceptance` 写 6-10 个样例 Case。
- 样例 Case 集合至少覆盖以下 mode：
  - `API_EXEC`
  - `AUDIT_EXEC`
  - `UI_AUTO`，仅标记为 Phase 1 候选或 UAT 里程碑，不进入首包阻断门禁
  - `UI_MANUAL`
- 定义 status 规则：
  - `COVERED`
  - `PENDING`
  - `EXCLUDED`
  - `UAT_MILESTONE`
  - `PHASE1_CANDIDATE`
- 定义 manifest 内部审阅 checklist。

建议产物路径：

```text
hl-platform/app/biz-demo/acceptance/acceptance-manifest.yaml
hl-platform/app/biz-demo/acceptance/README.md
hl-dispatch/deliverables/tasks/QA-BOOTSTRAP-MANIFEST-CHECKLIST.md
```

验收标准：

- manifest 中每个 Case-ID 都能追溯到样例 Cap-Spec-2。
- `API_EXEC` / `AUDIT_EXEC` 场景明确 `gate: G-023`。
- `API_EXEC` / `AUDIT_EXEC` 且准备进入 PR 门禁的场景不允许空 `testClass` / `testMethod`。
- `UI_AUTO` 在 Phase 1 前不得写成阻断性 G-023 绿线，除非已有稳定实现并经 Founder / 治理 Owner 批准。
- `UI_MANUAL` 明确写入 UAT 里程碑，不伪装成自动化覆盖。

### D2：G-026 校验雏形

目标：让 manifest 不是人工看表，而是能被确定性脚本检查。

任务：

- 测试组长定义 G-026 规则最小集。
- 后端工程师支持实现 YAML 校验脚本雏形。
- 测试成员提供合法与非法 manifest 样例。
- 后端工程师支持 Gradle / script 接入方式。
- 用样例 manifest 证明脚本能发现错误。

G-026 最小规则：

| 规则 | 说明 |
|------|------|
| R1 | 每个能力包 acceptance 目录必须存在 `acceptance-manifest.yaml` |
| R2 | manifest 中 `caseId` 必须能对应 Cap-Spec-2 Case-ID |
| R3 | `API_EXEC` / `AUDIT_EXEC` 进入首包绿线时必须是 `COVERED` |
| R4 | `API_EXEC` / `AUDIT_EXEC` 且 `status = COVERED` 时必须有 `testClass` / `testMethod` |
| R5 | `UI_MANUAL` 必须有 UAT 说明，不参与 PR 自动化覆盖率 |
| R6 | `UI_AUTO` 在 Phase 1 前只能是 `PHASE1_CANDIDATE` 或 UAT 里程碑，不作为 G-023 阻断项 |
| R7 | 脚本只解析 YAML，不读取 JaCoCo / Codecov 覆盖率数字 |
| R8 | manifest 必须声明 `schema_version`，脚本必须校验版本兼容 |

建议产物路径：

```text
hl-platform/scripts/qa/check-acceptance-manifest.py
hl-platform/app/biz-demo/acceptance/acceptance-manifest.invalid.yaml
hl-platform/app/biz-demo/acceptance/acceptance-manifest.yaml
```

验收标准：

- 对合法 manifest 返回 PASS。
- 对缺失 `caseId`、空 `testClass`、错误 mode、`API_EXEC` / `AUDIT_EXEC` 自动化场景 `PENDING` 返回 FAIL。
- 对 `UI_AUTO = PHASE1_CANDIDATE` 不返回阻断 FAIL，但必须输出非阻断提示。
- 输出能被 CI 日志读懂，必须包含失败 Case-ID 和失败原因。

### D3：JUnit 5 验收测试骨架

目标：让 QA 能把 manifest 中的 `API_EXEC` / `AUDIT_EXEC` Case 变成可执行测试。

任务：

- 测试成员创建 JUnit 5 参数化验收测试样例。
- 定义测试命名约定。
- 定义 tag 约定，例如 `@Tag("acceptance")`。
- 定义失败断言输出格式。
- 定义 `API_EXEC` / `AUDIT_EXEC` 的测试模式差异。

建议产物路径：

```text
hl-platform/app/biz-demo/acceptance/src/test/kotlin/.../DemoAcceptanceTest.kt
hl-platform/app/biz-demo/acceptance/src/test/kotlin/.../DemoAuditAcceptanceTest.kt
hl-dispatch/deliverables/tasks/QA-BOOTSTRAP-JUNIT5-STYLE.md
```

验收标准：

- 测试可由 Gradle 或 CI 命令执行。
- 至少 1 个 `API_EXEC` 样例通过。
- 至少 1 个 `AUDIT_EXEC` 样例通过。
- 失败输出包含 Case-ID、输入、期望、实际结果。
- 不新增 Kotest Spec 风格测试。

### D4：Testcontainers 与 Evidence Pack

目标：把“测试通过”变成可审阅证据，而不是口头结论。

任务：

- 后端工程师支持提供 Testcontainers PostgreSQL 18.x 启动样例。
- 测试成员编写 Evidence Pack 模板。
- 测试组长定义 QA 审阅 checklist。
- 测试组长确认 Evidence Pack 是 `qa-verdict` 前置条件。

Evidence Pack 最小字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| Capability ID | 是 | 能力包 ID |
| PR / Commit | 是 | 对应 PR 和 commit |
| Cap-Spec-2 Version | 是 | 验收场景版本 |
| acceptance-manifest hash | 是 | 当前 manifest 指纹 |
| manifest schema_version | 是 | manifest schema 版本 |
| G-026 Result | 是 | PASS / FAIL + 日志链接 |
| G-023 Result | 是 | 验收场景回放结果；无 `API_EXEC` / `AUDIT_EXEC` 时必须说明 |
| Unit / Integration Result | 是 | 工程测试结果 |
| Testcontainers Evidence | 条件必填 | 涉及数据库时必填 |
| UI_MANUAL UAT Record | 条件必填 | 有 UI_MANUAL 时必填 |
| UI_AUTO Candidate Note | 条件必填 | 有 UI_AUTO 候选时必填，说明不阻断原因 |
| Known Risks | 是 | 遗留风险 |
| QA Reviewer | 是 | 审阅人 |
| QA Approver | 是 | 批准人 |
| Review Timestamp | 是 | 审阅时间 |
| QA Review Decision | 是 | PASS / Request Changes |

建议产物路径：

```text
hl-dispatch/deliverables/tasks/QA-EVIDENCE-PACK-TEMPLATE.md
hl-dispatch/deliverables/tasks/QA-VERDICT-CHECKLIST.md
```

验收标准：

- QA 能根据 Evidence Pack 模板独立判断是否可放行。
- 缺少 G-026 / G-023 / manifest hash / reviewer / approver / timestamp 时 checklist 明确禁止 PASS。
- Evidence Pack 能作为 PR 评论或附件使用。
- Evidence Pack 中 QA Decision 与 PM Decision 分开记录。
- `QA Reviewer` 可由测试成员担任；`QA Approver` 必须为测试组长，且只有测试组长可触发或确认 `qa-verdict = PASS`。

### D5：qa-verdict Required Check 与样例 PR 演练

目标：在真实能力包前，用样例 PR 跑通完整闭环，并证明 `qa-verdict` required check 不会退化为口头放行。

任务：

- 运维支持为样例 PR dry run 落地或等价模拟 `qa-verdict` required status check。
- 运维支持为真实首包配置真实 `qa-verdict` required status check，并接入目标 repo / branch protection / CI。
- 测试组长确认 check 名称、触发方式、失败条件、责任方。
- 测试组长组织样例 PR 演练。
- 测试成员分别扮演 manifest author、reviewer、evidence reviewer。
- 故意制造至少 6 类失败：
  - manifest 缺 Case-ID
  - `API_EXEC` / `AUDIT_EXEC` 自动化场景 `PENDING`
  - Evidence Pack 缺 G-023 结果
  - Evidence Pack 缺 Reviewer / Approver / Review Timestamp
  - manifest hash 与 PR commit 不匹配
  - G-023 结果存在但为 FAIL
- 验证 `qa-verdict` 在 Evidence Pack 缺失、G-026 FAIL、G-023 缺失、G-023 FAIL 时不能通过。
- 验证样例 PR dry run 可使用等价模拟，但真实首包进入 QA 放行 / 合并门禁前不得只依赖模拟。
- 测试组长输出演练复盘。

建议产物路径：

```text
hl-dispatch/deliverables/tasks/QA-BOOTSTRAP-DRY-RUN-REPORT.md
hl-dispatch/deliverables/tasks/QA-VERDICT-REQUIRED-CHECK-DESIGN.md
```

验收标准：

- 样例 PR 至少经历一次 FAIL → 修复 → PASS。
- QA 团队能解释每一次 FAIL 的原因。
- 测试组长只在 Evidence Pack 完整后签出 PASS。
- 样例 PR dry run 可运行或有等价模拟验证证据。
- 真实首包 required status check 必须真实接入目标 repo / branch protection / CI，不能仅依赖模拟证据。
- PM acceptance 不参与 QA PASS 判断。
- 运维发布批准不被 QA 替代。

## 6. 总交付物清单

### 6.1 必交付

| 编号 | 交付物 | DRI | 验收人 |
|------|--------|-----|--------|
| QA-BS-D1 | `acceptance-manifest.yaml` 模板与样例 | 测试组长 | 测试组长 |
| QA-BS-D2 | G-026 规则标准 | 测试组长 | 测试组长 |
| QA-BS-D3 | G-026 YAML 校验脚本雏形 | 测试组长 | 测试组长 |
| QA-BS-D3T | G-026 技术实现可运行性确认 | 后端工程师支持 | 后端负责人技术确认，不作为 QA 基建验收 |
| QA-BS-D4 | JUnit 5 验收测试骨架 | 测试成员 | 测试组长 |
| QA-BS-D5 | Testcontainers PostgreSQL 18.x 证据样例 | 后端工程师支持 | 测试组长 |
| QA-BS-D6 | Evidence Pack 模板 | 测试组长 | 测试组长 |
| QA-BS-D7 | qa-verdict PASS / FAIL checklist | 测试组长 | Founder |
| QA-BS-D8 | qa-verdict required check 样例 PR dry run 验证 | 运维支持 | Founder 或指定治理 Owner |
| QA-BS-D8R | 真实首包 required status check 接入目标 repo / branch protection / CI | 运维支持 | Founder 或指定治理 Owner |
| QA-BS-D9 | 样例 PR 演练报告 | 测试组长 | Founder |

### 6.2 可选交付

| 编号 | 交付物 | 是否阻断首包 |
|------|--------|--------------|
| QA-BS-O1 | QA 指标仪表板草案 | 不阻断 |
| QA-BS-O2 | Playwright 学习记录 | 不阻断，不能作为 PR 绿线 |
| QA-BS-O3 | PIT / SonarQube 评估记录 | 不阻断，Phase 1+ 再评估 |

## 7. 首包接入准入门槛

首个真实能力包可以提前让 QA 参与需求澄清和测试设计，但不得进入 QA 放行 / 合并门禁，除非以下条件满足：

- [ ] 测试组长已确认任务书执行完成。
- [ ] 所有 P0/P1 豁免已列明范围、风险、补齐日期，并由 Founder 或指定治理 Owner 批准。
- [ ] Manifest 模板已通过内部审阅。
- [ ] Manifest 已包含 `schema_version` / `manifest_version`。
- [ ] G-026 最小校验可运行。
- [ ] 至少 1 个 JUnit 5 `API_EXEC` 验收测试样例可执行。
- [ ] 至少 1 个 `AUDIT_EXEC` 验收样例可执行或有明确等价脚本。
- [ ] Evidence Pack 模板已确认。
- [ ] qa-verdict checklist 已确认。
- [ ] 样例 PR 已完成 `qa-verdict` required check dry run；dry run 可使用等价模拟。
- [ ] 首个真实能力包进入 QA 放行 / 合并门禁前，真实 `qa-verdict` required status check 已接入目标 repo / branch protection / CI，并能实际阻断合并。
- [ ] 样例 PR 至少演练一次 FAIL → 修复 → PASS。
- [ ] 样例 PR 已验证 Evidence Pack 缺失、G-026 FAIL、G-023 缺失、G-023 FAIL 时 `qa-verdict` 不能通过。
- [ ] QA 团队已明确 `qa-verdict` 与 PM acceptance 的边界。
- [ ] `UI_AUTO` 已明确为 Phase 1 候选或 UAT 里程碑，不作为首包阻断绿线。

豁免规则：

- P0/P1 门槛不得由测试组长单独豁免。
- P0/P1 豁免必须由 Founder 或指定治理 Owner 批准。
- P2 项可由测试组长登记风险并设定补齐日期，但必须在 dry run 报告中披露。

## 8. 风险与缓解

| 风险 | 影响 | 缓解 |
|------|------|------|
| QA 等真实能力包来了才开始准备 | 首包 PR 阻塞 | 先用 `biz.demo.acceptance` 演练 |
| manifest 只写文档、不接脚本 | G-026 形同虚设 | D2 必须完成 YAML 校验雏形 |
| qa-verdict 被口头确认替代 | 独立质量权失效 | 样例 PR 可等价模拟；真实首包前必须接入真实 required status check |
| G-026 脚本验收权漂移到工程侧 | QA 基建权责失效 | 测试组长拥有 G-026 DRI 与最终验收权，后端只做技术实现确认 |
| PM acceptance 与 qa-verdict 混淆 | 职责漂移 | Evidence Pack 中分开记录 QA Decision 与 PM Decision |
| Testcontainers 环境不稳定 | 集成测试不可复现 | 先只做 PostgreSQL 18.x 最小样例 |
| 过早引入 Playwright / PIT / SonarQube | 工具链膨胀 | 明确列为非阻断项 |
| UI_AUTO 被误纳入首包绿线 | 首包门槛漂移 | UI_AUTO 在 Phase 1 前只做候选或 UAT 里程碑 |
| 测试组长单独豁免 P1 | 门禁失效 | P0/P1 豁免必须 Founder 或指定治理 Owner 批准 |

## 9. Founder 审阅点

请 Founder 裁决以下问题：

1. 是否批准以 `biz.demo.acceptance` 作为 QA Bootstrap 样例能力包。
2. 是否批准首包前必须完成 G-026 最小脚本。
3. 是否批准 Evidence Pack 缺失、G-026 缺失/失败、G-023 缺失/失败时，`qa-verdict` 必须 FAIL。
4. 是否批准 Playwright / PIT / SonarQube 不作为首包前置绿线。
5. 是否批准样例 PR 可用等价模拟 dry run，但首个真实能力包进入 QA 放行 / 合并门禁前必须接入真实 `qa-verdict Required Status Check`。
6. 是否批准 `UI_AUTO` 在 Phase 1 前不进入首包 PR 阻断门禁，除非已有稳定自动化实现。
7. 是否批准 P0/P1 豁免只能由 Founder 或指定治理 Owner 批准，不能由测试组长单独豁免。
8. 已按 Founder 指令发布到站点 `qa.html`，并作为内部任务包派发依据。

## 10. 完成定义

本启动任务完成的定义：

- 测试组长提交 `QA-BOOTSTRAP-DRY-RUN-REPORT.md`。
- 样例 PR 已完成 `qa-verdict` required check dry run，且真实首包进入 QA 放行 / 合并门禁前已接入真实 required status check。
- Founder 审阅并裁决 `PASS / CONDITIONAL PASS / FAIL`。
- 若 PASS，首个真实能力包可以进入 QA 放行 / 合并门禁。
- 若 CONDITIONAL PASS，必须列出不阻断项和补齐日期。
- 若 FAIL，真实能力包不得进入 QA 放行 / 合并门禁，直到 P0/P1 阻断项关闭。
