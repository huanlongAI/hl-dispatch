# 测试团队 QA Bootstrap 启动执行指南 v1.0

> 日期：2026-05-07  
> 状态：PUBLISHED  
> 适用对象：测试组长（李云峰，兼架构师）+ 测试成员 3 人  
> 依据：`QA-BOOTSTRAP-TASKBOOK-2026-05-06-v0.4.md`，大辉子最终复核 `PASS`  
> 入口：`https://huanlongai.github.io/hl-dispatch/pages/qa.html#qa-bootstrap-start-guide`

## 1. 启动原则

1. 测试团队内部只有两类角色：测试组长与测试成员。
2. 测试组长兼架构师，拥有 manifest、G-026、Evidence Pack、qa-verdict checklist 的最终口径。
3. 测试成员按组长分配执行，不拥有 `qa-verdict = PASS` 签字权。
4. 后端、运维、PM 只作为支持方，不拥有 QA 基建验收权或 qa-verdict 签字权。
5. 样例 PR 可用等价模拟 dry run；真实首包进入 QA 放行 / 合并门禁前，必须接入真实 `qa-verdict` required status check。

## 2. 启动前准备

测试组长先完成：

- 打开测试团队频道：`qa.html#qa-bootstrap-v04` 与 `qa.html#qa-bootstrap-start-guide`。
- 确认样例能力包名称：默认 `biz.demo.acceptance`。
- 指定 3 名测试成员分别承担：Manifest 样例、JUnit 5 骨架、Evidence Pack / dry run 记录。
- 向后端确认是否能提供 Testcontainers PostgreSQL 18.x 最小样例。
- 向运维确认 required status check 的 dry run 方式与真实首包接入方式。

测试成员先完成：

- 拉取最新 `hl-platform` 与 `hl-dispatch`。
- 阅读 `qa.html#quickstart`、`qa.html#qa-workflow`、`qa.html#qa-bootstrap-v04`。
- 准备本地 Codex 工作区，不在未确认范围内修改业务代码。

## 3. 云效消费仓库与流水线规则

测试团队将在云效 / Codeup 消费仓库，但流水线口径必须遵守“双轨”规则：

- GitHub / `hl-dispatch` / `hl-contracts` 是治理与规格真源，承载任务书、契约、验收口径、PR 留痕与 required status checks。
- Codeup / 云效是开发执行面，承载工程师日常开发、构建、测试、部署执行与流水线日志。
- 云效当前 post-merge 部署流水线不能替代 GitHub pre-merge required check。
- 发布前必须证明 GitHub main、Codeup main、云效构建 commit 一致。

### 3.1 测试团队如何消费仓库

| 仓库 | 云效/Codeup 用途 | 测试团队权限口径 | 禁止事项 |
|------|------------------|------------------|----------|
| `hl-contracts` | 查 DD-TEST、TECH-STACK、Cap-Spec / Case-ID | 只读消费 | 不在云效侧改契约真源 |
| `hl-dispatch` | 查任务书、启动指南、Evidence Pack 模板、复盘归档 | 读为主；文档更新走 PR / 受控提交 | 不在飞书或云效评论替代正式文档 |
| `hl-platform` | 放置 `biz.demo.acceptance`、manifest、G-026、JUnit 5、Testcontainers 样例 | 在授权分支开发，走 PR / MR | 不直接推 main，不绕过 QA verdict |

建议分支：

```text
qa/bootstrap-biz-demo
qa/<capability-id>-acceptance
```

### 3.2 云效流水线中 QA 要看什么

| 阶段 | QA 关注点 | 通过条件 | 失败归口 |
|------|-----------|----------|----------|
| L1 编译 / 类型 / 格式 | 构建是否可运行，测试代码是否破坏基础编译 | L1 全绿 | 工程师修复；QA 不签 PASS |
| L2 契约 / 模块 / G-026 | `acceptance-manifest.yaml` 是否存在、字段完整、mode/status 合法 | G-026 PASS，非法 manifest 必须 FAIL | 测试组长定口径；测试成员修 manifest；后端修脚本 |
| L3 单元 / 集成 / G-023 | JUnit 5、Testcontainers、验收场景回放是否通过 | API_EXEC / AUDIT_EXEC 对应 G-023 PASS | 工程师修实现；QA 修验收映射；后端/运维修环境 |
| Evidence Pack | 是否有 G-026、G-023、manifest hash、Reviewer、Approver、Timestamp | 字段完整且测试组长 Approver | 测试成员补证据；测试组长判定 |
| qa-verdict | 质量放行是否机读化 | 测试组长确认 PASS，required status check 生效 | 测试组长 / 运维 |

### 3.3 Evidence Pack 必须记录的云效信息

每次 dry run 或真实能力包验收，都必须记录：

- GitHub PR 链接。
- Codeup MR / 分支链接。
- 云效流水线 run 链接。
- 云效构建 commit SHA。
- GitHub main SHA、Codeup main SHA；发布前必须一致。
- G-026 日志链接与结论。
- G-023 日志链接与结论。
- Testcontainers 运行证据。
- manifest hash 与 PR commit 对应关系。

### 3.4 失败分流规则

| 失败类型 | 先找谁 | 测试团队动作 |
|----------|--------|--------------|
| 拉不到仓库 / 无云效权限 | Founder / 运维 | 记录阻塞，不自行换仓库 |
| Codeup 与 GitHub 内容不一致 | 技术负责人 / 运维 | 暂停验收，要求给出对齐证据 |
| L1 失败 | 工程师 | 不进入 QA PASS |
| G-026 失败 | 测试组长 + 测试成员 + 后端支持 | 判断是 manifest 问题还是脚本问题 |
| G-023 失败 | 工程师 + 测试成员 | 判断是实现失败、验收映射错误还是测试数据问题 |
| Testcontainers 环境失败 | 后端支持 + 运维 | 确认 Docker / PostgreSQL 18.x / CI runner |
| Evidence Pack 缺字段 | 测试成员 | 补齐后再审 |
| qa-verdict 无法回写 required check | 运维 | 样例 PR 可模拟；真实首包前必须真实接入 |

### 3.5 需要 Founder 配合的支持

请 Founder 或指定治理 Owner 确认：

- 测试组长和测试成员在云效 / Codeup 中可见 `hl-platform`、`hl-dispatch`、必要的 `hl-contracts` 镜像或只读入口。
- 测试团队可以创建 `qa/bootstrap-*` 分支或等价 MR。
- 云效流水线日志对测试团队可读，至少能看到 L1 / L2 / L3 结果、commit SHA、run URL。
- 运维明确真实首包 `qa-verdict` required status check 的接入责任人和目标 repo / branch protection / CI。
- 后端支持人明确协助 G-026、JUnit 5、Testcontainers 的技术可运行性。

## 4. D0-D5 执行步骤

### D0：Kickoff 与边界确认

负责人：测试组长

具体步骤：

1. 组织 30 分钟启动会。
2. 带读 DD-TEST v1.2、TECH-STACK v3.4、QA Bootstrap v0.4。
3. 明确 QA verdict 与 PM acceptance 的边界。
4. 明确首包绿线只覆盖 `API_EXEC` / `AUDIT_EXEC`、G-026、G-023、Evidence Pack、qa-verdict。
5. 明确 `UI_AUTO` 不进入首包阻断门禁。

交付物：

- `QA Bootstrap Kickoff Notes`
- 参与人员名单
- 阻塞项清单

验收：

- 每个成员能解释 qa-verdict 与 PM acceptance 的差异。
- 每个成员能解释 `UI_MANUAL` 与 `UI_AUTO` 的首包边界。

### D1：Manifest 标准与样例

负责人：测试组长  
执行：测试成员

具体步骤：

1. 定义 `acceptance-manifest.yaml` 模板。
2. 模板必须包含 `manifest_version`、`schema_version`、`capability_id`、`cap_spec_version`。
3. 用 `biz.demo.acceptance` 写 6-10 个样例 Case。
4. 样例 Case 集合覆盖 `API_EXEC` / `AUDIT_EXEC` / `UI_AUTO` / `UI_MANUAL`。
5. 标记 `UI_AUTO` 为 `PHASE1_CANDIDATE` 或 UAT 里程碑，不写成首包 G-023 阻断项。

建议路径：

```text
hl-platform/app/biz-demo/acceptance/acceptance-manifest.yaml
hl-platform/app/biz-demo/acceptance/README.md
hl-dispatch/deliverables/tasks/QA-BOOTSTRAP-MANIFEST-CHECKLIST.md
```

验收：

- 每个 Case-ID 可追溯到样例 Cap-Spec-2。
- `API_EXEC` / `AUDIT_EXEC` 且 `COVERED` 的场景必须有 `testClass` / `testMethod`。
- `UI_MANUAL` 不伪装成自动化覆盖。

### D2：G-026 校验雏形

负责人：测试组长  
技术实现支持：后端工程师

具体步骤：

1. 测试组长定义 G-026 最小规则。
2. 后端实现 YAML 校验脚本雏形。
3. 测试成员提供合法与非法 manifest 样例。
4. 脚本输出必须包含失败 Case-ID 与失败原因。
5. 后端负责人只做技术可运行性确认，不做 QA 基建验收。

建议路径：

```text
hl-platform/scripts/qa/check-acceptance-manifest.py
hl-platform/app/biz-demo/acceptance/acceptance-manifest.invalid.yaml
hl-platform/app/biz-demo/acceptance/acceptance-manifest.yaml
```

验收：

- 合法 manifest 返回 PASS。
- 缺 `caseId`、空 `testClass`、错误 mode、`API_EXEC` / `AUDIT_EXEC` 自动化场景 `PENDING` 返回 FAIL。
- `UI_AUTO = PHASE1_CANDIDATE` 只输出非阻断提示。

### D3：JUnit 5 验收测试骨架

负责人：测试成员  
验收：测试组长

具体步骤：

1. 创建 JUnit 5 参数化验收测试样例。
2. 定义 `@Tag("acceptance")`。
3. 至少提供 1 个 `API_EXEC` 样例与 1 个 `AUDIT_EXEC` 样例。
4. 失败输出必须包含 Case-ID、输入、期望、实际结果。
5. 不新增 Kotest `FunSpec` / `StringSpec` 风格测试。

建议路径：

```text
hl-platform/app/biz-demo/acceptance/src/test/kotlin/.../DemoAcceptanceTest.kt
hl-platform/app/biz-demo/acceptance/src/test/kotlin/.../DemoAuditAcceptanceTest.kt
hl-dispatch/deliverables/tasks/QA-BOOTSTRAP-JUNIT5-STYLE.md
```

验收：

- Gradle 或 CI 命令可执行。
- `API_EXEC` / `AUDIT_EXEC` 样例均可通过。

### D4：Evidence Pack 与 checklist

负责人：测试组长  
执行：测试成员

具体步骤：

1. 编写 Evidence Pack 模板。
2. 明确 `QA Reviewer` 可由测试成员担任。
3. 明确 `QA Approver` 必须为测试组长。
4. 缺 G-026 / G-023 / manifest hash / reviewer / approver / timestamp 时禁止 PASS。
5. QA Decision 与 PM Decision 分开记录。

建议路径：

```text
hl-dispatch/deliverables/tasks/QA-EVIDENCE-PACK-TEMPLATE.md
hl-dispatch/deliverables/tasks/QA-VERDICT-CHECKLIST.md
```

验收：

- Evidence Pack 可作为 PR 评论或附件使用。
- 只有测试组长可触发或确认 `qa-verdict = PASS`。

### D5：样例 PR dry run 与真实首包门禁准备

负责人：测试组长  
执行：测试成员、运维支持、后端支持

具体步骤：

1. 运维为样例 PR dry run 落地或等价模拟 `qa-verdict` required status check。
2. 运维确认真实首包 required status check 接入目标 repo / branch protection / CI 的方案。
3. 样例 PR 至少跑一次 FAIL → 修复 → PASS。
4. 故意制造至少 6 类失败：缺 Case-ID、自动化场景 `PENDING`、缺 G-023、缺 reviewer/approver/timestamp、manifest hash mismatch、G-023 FAIL。
5. 输出 dry run 报告。

建议路径：

```text
hl-dispatch/deliverables/tasks/QA-BOOTSTRAP-DRY-RUN-REPORT.md
hl-dispatch/deliverables/tasks/QA-VERDICT-REQUIRED-CHECK-DESIGN.md
```

验收：

- 样例 PR dry run 可模拟。
- 真实首包进入 QA 放行 / 合并门禁前，必须接入真实 required status check，不能只依赖模拟。

## 5. Codex 启动提示词

### 4.1 测试组长总控提示词

```text
你是唤龙平台测试组长（兼架构师），负责执行 QA Bootstrap v0.4。请先阅读：
1. https://huanlongai.github.io/hl-dispatch/pages/qa.html#qa-bootstrap-v04
2. hl-dispatch/deliverables/tasks/QA-BOOTSTRAP-TASKBOOK-2026-05-06-v0.4.md

目标：
- 在首个真实能力包进入 QA 放行 / 合并门禁前，完成 D0-D5 启动闭环。
- 测试团队内部只使用“测试组长 + 测试成员”两类角色。
- 你拥有 manifest、G-026、Evidence Pack、qa-verdict checklist 的最终口径。

工作要求：
- 不修改业务代码，除非 Founder 或任务书明确授权。
- 先列出 D0-D5 当前状态、缺口、负责人、下一步。
- 重点检查 qa-verdict required status check 是否区分样例 PR dry run 与真实首包门禁。
- 重点检查 G-026 QA 基建验收权是否仍归测试组长。

输出：
1. D0-D5 启动计划表
2. 今日待办清单
3. 阻塞项
4. 需要后端/运维/PM 支持的事项
5. 可直接发到飞书的同步摘要
```

### 4.2 Manifest 成员提示词

```text
你是测试成员，负责 QA Bootstrap D1：acceptance-manifest.yaml 样例。

请基于 biz.demo.acceptance 设计 6-10 个样例 Case，输出 acceptance-manifest.yaml 草案。

约束：
- 必须包含 manifest_version、schema_version、capability_id、cap_spec_version。
- 样例 Case 集合必须覆盖 API_EXEC / AUDIT_EXEC / UI_AUTO / UI_MANUAL。
- API_EXEC / AUDIT_EXEC 且 status=COVERED 时必须填写 testClass / testMethod。
- UI_AUTO 在 Phase 1 前只能标记 PHASE1_CANDIDATE 或 UAT 里程碑，不作为首包 G-023 阻断项。
- UI_MANUAL 必须进入 UAT_MILESTONE，不伪装成自动化覆盖。

输出：
1. YAML 草案
2. Case-ID 映射说明
3. 自查 checklist
4. 需要测试组长裁决的问题
```

### 4.3 G-026 校验提示词

```text
你是测试组长，负责定义 G-026 manifest YAML 校验规则；后端只做技术实现支持。

请输出 G-026 最小规则与脚本验收标准。

必须覆盖：
- acceptance 目录必须存在 acceptance-manifest.yaml
- caseId 必须能对应 Cap-Spec-2 Case-ID
- API_EXEC / AUDIT_EXEC 进入首包绿线时必须是 COVERED
- API_EXEC / AUDIT_EXEC 且 COVERED 时必须有 testClass / testMethod
- UI_MANUAL 必须有 UAT 说明，不参与 PR 自动化覆盖率
- UI_AUTO 在 Phase 1 前只能是 PHASE1_CANDIDATE 或 UAT 里程碑，不作为 G-023 阻断项
- manifest 必须声明 schema_version，脚本必须校验版本兼容

输出：
1. 规则表
2. 合法 manifest 样例
3. 非法 manifest 样例
4. PASS / FAIL 输出格式
5. 后端技术确认与 QA 验收边界
```

### 4.4 JUnit 5 骨架提示词

```text
你是测试成员，负责 QA Bootstrap D3：JUnit 5 参数化验收测试骨架。

请根据 acceptance-manifest.yaml 中 API_EXEC / AUDIT_EXEC 的 Case-ID，设计 JUnit 5 验收测试样例。

约束：
- 使用 JUnit 5，不新增 Kotest FunSpec / StringSpec。
- 使用 @Tag("acceptance")。
- 至少包含 1 个 API_EXEC 样例与 1 个 AUDIT_EXEC 样例。
- 失败输出必须包含 Case-ID、输入、期望、实际结果。
- 如需要数据库，使用 Testcontainers PostgreSQL 18.x，不使用 H2。

输出：
1. 测试类结构
2. 参数化测试样例
3. Gradle / CI 执行命令建议
4. 与 manifest testClass / testMethod 的映射表
```

### 4.5 Evidence Pack 审阅提示词

```text
你是测试组长，负责 QA Bootstrap D4：Evidence Pack 与 qa-verdict checklist。

请设计 Evidence Pack 模板，并给出 PASS / Request Changes 判定规则。

必须包含字段：
- Capability ID
- PR / Commit
- Cap-Spec-2 Version
- acceptance-manifest hash
- manifest schema_version
- G-026 Result
- G-023 Result
- Unit / Integration Result
- Testcontainers Evidence
- UI_MANUAL UAT Record
- UI_AUTO Candidate Note
- Known Risks
- QA Reviewer
- QA Approver
- Review Timestamp
- QA Review Decision

边界：
- QA Reviewer 可由测试成员担任。
- QA Approver 必须为测试组长。
- 缺 G-026 / G-023 / manifest hash / reviewer / approver / timestamp 时禁止 PASS。

输出：
1. Evidence Pack 模板
2. qa-verdict checklist
3. Request Changes 模板
4. PASS 模板
```

### 4.6 Dry Run 复盘提示词

```text
你是测试组长，负责 QA Bootstrap D5：样例 PR dry run 与复盘。

请根据样例 PR 的 Evidence Pack、G-026、G-023、manifest hash 和 qa-verdict 结果，输出 dry run 复盘。

必须验证以下失败：
- manifest 缺 Case-ID
- API_EXEC / AUDIT_EXEC 自动化场景 PENDING
- Evidence Pack 缺 G-023 结果
- Evidence Pack 缺 Reviewer / Approver / Review Timestamp
- manifest hash 与 PR commit 不匹配
- G-023 结果存在但为 FAIL

输出：
1. FAIL → 修复 → PASS 时间线
2. 每次 FAIL 的原因
3. 修复动作
4. 真实首包 required status check 接入状态
5. 是否允许首个真实能力包进入 QA 放行 / 合并门禁的建议
```

### 5.7 云效取证提示词

```text
你是测试团队 Codex 助手，负责在云效 / Codeup 消费仓库并整理 QA Bootstrap 取证。

请根据当前 Codeup 分支、云效流水线 run、GitHub PR / 任务书，输出流水线取证报告。

必须检查：
1. 当前 Codeup 分支与 commit SHA。
2. 对应 GitHub PR 或任务链接。
3. 云效流水线 run URL、触发 commit、执行时间。
4. L1 编译 / 类型 / 格式结果。
5. L2 契约 / 模块 / G-026 结果。
6. L3 单元 / 集成 / G-023 / Testcontainers 结果。
7. Evidence Pack 是否包含 G-026、G-023、manifest hash、Reviewer、Approver、Review Timestamp。
8. GitHub main、Codeup main、云效构建 commit 是否需要发布前一致性校验。

边界：
- 云效 post-merge 部署流水线不能替代 GitHub pre-merge required check。
- 样例 PR dry run 可模拟 qa-verdict；真实首包前必须真实接入 required status check。
- G-026 QA 基建验收权归测试组长，后端只做技术可运行性确认。

输出：
1. 流水线取证表
2. 失败分流建议
3. 是否允许进入 qa-verdict 审阅
4. 需要 Founder / 运维 / 后端支持的事项
```

## 6. 每日同步格式

```text
【QA Bootstrap 日报】
日期：
负责人：测试组长 / 李云峰

D0 Kickoff：
D1 Manifest：
D2 G-026：
D3 JUnit 5：
D4 Evidence Pack：
D5 Dry Run：
云效取证：

今日完成：
今日阻塞：
需要后端支持：
需要运维支持：
需要 PM 支持：
风险：
下一步：
```

## 7. 完成判定

只有同时满足以下条件，测试团队启动才算完成：

- D0-D5 产物全部提交。
- 样例 PR 至少经历一次 FAIL → 修复 → PASS。
- G-026 可运行并能阻断非法 manifest。
- Evidence Pack 模板与 qa-verdict checklist 已确认。
- 样例 PR dry run 已验证缺证据、G-026 FAIL、G-023 缺失、G-023 FAIL 时不能 PASS。
- 真实首包 required status check 已有接入目标 repo / branch protection / CI 的落地方案。
- 云效流水线取证包含 run URL、commit SHA、L1 / L2 / L3 结果、G-026 / G-023 日志与双 main 对齐状态。
- Founder 或指定治理 Owner 已批准 P0/P1 豁免项；无批准则不得豁免。
