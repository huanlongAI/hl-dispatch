# PM 实操手册

## PM-PRACTICAL-HANDBOOK v1.0 — 唤龙平台产线责任人操作指南

---

**文档编号**：PM-HANDBOOK-001
**版本**：v1.0
**日期**：2026-03-30
**状态**：DRAFT
**派生链**：PM-AI-COLLABORATION-ONBOARDING-SPEC v2.0 + PRD-REDEFINITION-SPEC v2.0 + TEAM-COLLABORATION-SPEC v1.2 → 本文档
**适用对象**：邹骢、朱阳（PM 角色，产线责任人）

---

## 0. 本手册用途

PM-AI-COLLABORATION-ONBOARDING-SPEC 定义了"PM 是什么、能做什么、不能做什么"。本手册解决"PM 具体怎么做"——从打开编辑器到代码合并的每一步操作。

**阅读前提**：已完成 PM-AI-COLLABORATION-ONBOARDING-SPEC §3 Phase 3 知识体系学习。

---

## 1. PM 一天的工作节奏

```
上午                                下午                          收尾
──────────────────────────────────────────────────────────────────────
飞书 + GitHub 通知                  AI 编码 / 测试                 落地 + 提交
├ 飞书 #PM工作台 看 review 通知      ├ 基于 Cap-Spec 驱动 AI         ├ 代码 PR / Cap-Spec PR
├ 飞书 #工程通知 看 CI 状态          ├ 修复 CI 失败                  ├ 更新 Issue 状态
├ GitHub PR review 评论             └ 补充验收场景                   └ 飞书讨论结论写入 GitHub
└ 创始人裁决回复

周一：飞书 #任务协同 对齐本周目标     周五：更新 Bitable 看板 + 关闭已完成 Issue
```

**核心原则**：PM 不等人。创始人给定上游后，PM 自主驱动规格→编码→测试→验收。遇到上游问题提 Issue 推动，不原地等待。

---

## 2. Cap-Spec-1 能力规格书：怎么写

### 2.1 写之前做什么

1. **读上游契约**：打开 hl-contracts，找到与你能力包相关的文件
   ```
   hl-contracts/
   ├── decisions/          ← 设计裁决（如 biz.product 看 DEC-PRODUCT-*.md）
   ├── rules/              ← 业务规则 YAML
   ├── facts/              ← 事实数据定义
   ├── apis/               ← OpenAPI YAML
   ├── reasoncodes/        ← reason_codes.csv
   └── glossary/           ← 术语表
   ```

2. **读启动规格**：找到 `hl-dispatch/deliverables/decisions/LAUNCH-{MODULE}.md`
   - 如果还没有，PM 需要先创建（见 §2.5）

3. **读已有裁决回复**：搜索 `REPLY-PM-{你的名字}-R*.md`，确认之前的裁决是否影响规格

### 2.2 文件命名与存放

```
文件名：Cap-Spec-{Domain}.{Module}.v{X.Y}.md
存放位置：hl-contracts/prd/{domain}/
示例：hl-contracts/prd/biz/Cap-Spec-Biz.Product.v1.0.md
```

### 2.3 必含章节模板

```markdown
# Cap-Spec-{Domain}.{Module} v{X.Y}

## §0 一句话定义

{≤50 字，说清楚是什么、解决什么问题}

## §1 业务背景与目标

### 目标用户
- {角色 A}：{痛点 + 期望}
- {角色 B}：{痛点 + 期望}

### 业务目标
1. {目标描述}
2. {目标描述}

## §2 能力边界

### 做什么
- {核心能力 1}
- {核心能力 2}

### 不做什么（至少 3 条）
- {非目标 1，说明原因}
- {非目标 2，说明原因}
- {非目标 3，说明原因}

## §3 业务规则概述

> ⚠️ 只描述意图，不复制 rules YAML 原文。

### 关键规则
1. {规则意图描述}（对应 contracts: rules/{file}.yaml）
2. {规则意图描述}

### 状态机（如适用）
{描述实体状态流转的业务含义}

## §4 上游引用索引

| 引用类型 | 路径 | 说明 |
|---------|------|------|
| 设计裁决 | decisions/{file}.md | {一句话} |
| 业务规则 | rules/{file}.yaml | {一句话} |
| API 定义 | apis/{file}.openapi.yaml | {一句话} |
| 事实数据 | facts/facts-catalog.md #{section} | {一句话} |
| 业务码 | reasoncodes/reasoncodes.csv | {行范围} |

## §5 依赖与时序

### 上游依赖
- {HK.OrgLink → 组织关系必须先建立}

### 下游影响
- {biz.order 依赖本包的商品数据}

### 并行关系
- {biz.inventory 可与本包并行开发}
```

### 2.4 biz.product 实操示例

以邹骢负责的商品中心为例，§0~§2 的实际写法：

```markdown
# Cap-Spec-Biz.Product v1.0

## §0 一句话定义

管理商品全生命周期（SPU/SKU 创建、上下架、定价），提供全平台商品数据 SSOT。

## §1 业务背景与目标

### 目标用户
- 品牌方运营（Claim 关系持有方）：创建管理自有品牌商品
- 合作商户（Cooperate 关系方）：查看可售商品、设置渠道价格
- 平台管理员：审核商品、维护分类体系

### 业务目标
1. 统一商品数据源——所有交易类能力包从 biz.product 获取商品信息
2. 跨租户商品授权——品牌方商品通过 OrgLink Cooperate 关系授权给合作商户
3. 全链路审计——商品创建/上下架/价格变更经 HK.Audit 留痕

## §2 能力边界

### 做什么
- SPU 创建/编辑/上下架
- SKU 挂载、价格设置（R-061 裁决：先建 SPU 再挂 SKU）
- 商品分类管理
- 跨租户商品可见性控制

### 不做什么
- 库存扣减（归 biz.inventory）
- 订单履约（归 biz.order）
- 支付结算（归 biz.payment）
- 营销活动价（归 biz.promotion，biz.product 只管基础定价）
```

### 2.5 没有 LAUNCH 文档怎么办

如果你的能力包还没有 `LAUNCH-{MODULE}.md`，先创建它再写 Cap-Spec：

1. 复制 `PM-BRANCH-LAUNCH-TEMPLATE.md` 为 `LAUNCH-{MODULE}.md`
2. 填写 §1 模块身份卡 + §2 业务域分析
3. 提交 PR 到 hl-dispatch，等创始人 review
4. merge 后再开始写 Cap-Spec

---

## 3. Cap-Spec-2 验收场景集：怎么写

### 3.1 核心原则

验收场景集是 PM 最高价值的产出。它同时服务两个目的：PM 业务验收的检查清单 + AI 编码的测试用例驱动源。

**好的场景**：输入明确、输出可判定、覆盖正常+异常路径。
**差的场景**：只说"用户能创建商品"，不说输入输出和边界。

### 3.2 文件命名与存放

```
文件名：Cap-Spec-{Domain}.{Module}.Acceptance.v{X.Y}.md
存放位置：hl-contracts/prd/{domain}/
示例：hl-contracts/prd/biz/Cap-Spec-Biz.Product.Acceptance.v1.0.md
```

### 3.3 场景编写格式

```markdown
### Case-{编号}：{场景名称}

**前置条件**：
- {条件 1}
- {条件 2}

**输入**：
```json
{
  "tenant_id": "T001",
  "spu_name": "...",
  "sku_list": [...]
}
```

**预期输出**：
```json
{
  "code": "biz.product.create.ok",
  "data": { "spu_id": "..." }
}
```

**验收方式**：
- [x] API 调用验证
- [ ] UI 人工验证
- [x] 审计日志验证（HK.Audit 有记录）
```

### 3.4 场景覆盖检查清单

每个能力包的验收场景集至少覆盖以下类型：

| 类型 | 最低数量 | 示例 |
|------|:------:|------|
| 正常路径（Happy Path） | 3+ | 创建商品成功、编辑商品成功、上架成功 |
| 权限拒绝 | 2+ | 非 Claim 持有方创建 → deny、无 admin 操作 → deny |
| 业务规则拒绝 | 3+ | 裸 SKU 创建 → deny、价格低于底价 → deny |
| 边界条件 | 2+ | 商品名称空值、超长文本 |
| 跨租户场景 | 1+ | Cooperate 商户查看授权商品 |
| 审计追溯 | 1+ | 商品上下架操作审计记录可查 |

### 3.5 reason_code 与场景的对应

每个场景的预期输出中的 `code` 字段必须是 `reasoncodes.csv` 中已定义或即将通过 Cap-Spec-3 PR 新增的 reason_code。不允许发明临时 code。

**检查方法**：打开 `hl-contracts/reasoncodes/reasoncodes.csv`，搜索你的 `biz.{module}` 前缀，确认每个场景的 code 都能对上。

---

## 4. Cap-Spec-3 业务码提案：怎么提 PR

### 4.1 reason_code 命名规则

```
格式：{domain}.{module}.{action}.{outcome}

domain = biz（业务能力包都用 biz）
module = product / order / inventory / ...
action = create / update / shelve / unshelve / price.set / ...
outcome = ok / denied.{reason} / error.{type}

示例：
  biz.product.create.ok                    → 创建成功
  biz.product.create.denied.no_permission  → 无权限创建
  biz.product.create.denied.dup_spu_code   → SPU 编码重复
  biz.product.price.set.denied.below_floor → 低于品牌底价
```

### 4.2 CSV 格式

在 `reasoncodes.csv` 中追加行，遵循已有格式：

```csv
code,decision_type,decision_key,outcome,visibility,default_message,action_hint
biz.product.create.ok,create,biz.product.create.can,success,public,商品创建成功,
biz.product.create.denied.no_permission,create,biz.product.create.can,deny,public,无权限创建商品,
biz.product.create.denied.dup_spu_code,create,biz.product.create.can,deny,public,SPU 编码已存在,
```

**PM 需要填的列**：

| 列 | PM 填写 | 说明 |
|----|:------:|------|
| code | ✅ | 按命名规则构造 |
| decision_type | ✅ | create / update / query / delete / eligibility |
| decision_key | ✅ | `biz.{module}.{action}.can`（3 级概念层 + `.can` 后缀，如 `biz.product.create.can`） |
| outcome | ✅ | success / deny |
| visibility | ✅ | public（用户可见） / internal（仅日志） |
| default_message | ✅ | 中文描述 |
| action_hint | 可选 | 用户引导提示（如 contact_support） |

### 4.3 提 PR 步骤

```bash
# 1. 切新分支
cd ~/huanlong-pm/hl-contracts
git checkout main && git pull
git checkout -b pm/biz-product-reasoncodes

# 2. 编辑 reasoncodes.csv，在对应区块追加行
# 建议在文件中按 domain 分区，找到 biz.product 区域（如没有就新建）

# 3. 暂存并提交
git add reasoncodes/reasoncodes.csv
git commit -m "feat(biz.product): add reason_codes for Cap-Spec-Biz.Product

新增 {N} 条 reason_code，覆盖商品创建/上下架/定价拒绝场景。
对应 Cap-Spec-Biz.Product.Acceptance.v1.0 全部场景。"

# 4. 推送并创建 PR
git push -u origin pm/biz-product-reasoncodes
```

在 GitHub 上创建 PR 时，Description 使用以下模板：

```markdown
## 变更摘要
新增 biz.product 能力包的 {N} 条 reason_code。

## 业务说明
| code | 触发场景 |
|------|--------|
| biz.product.create.ok | 品牌方创建商品成功 |
| biz.product.create.denied.no_permission | 非 Claim 持有方尝试创建 |
| ... | ... |

## 对应文档
- Cap-Spec-Biz.Product.v1.0.md（§3 业务规则概述）
- Cap-Spec-Biz.Product.Acceptance.v1.0.md（Case-001~Case-{N}）

## Checklist
- [ ] code 命名符合 `biz.{module}.{action}.{outcome}` 格式
- [ ] decision_key 3 级深度 `biz.{module}.{action}.can`
- [ ] 无拼写错误
- [ ] 每条 code 在验收场景集中有对应 Case
```

---

## 5. AI 编码实操指南

### 5.1 工作流总览

```
Cap-Spec-1 + Cap-Spec-2 已 merge（规格就绪）
    │
    ▼
PM 在 AI 平台打开项目上下文
    │
    ▼
第一轮：contract 层接口（Pure Kotlin）                ← ~1 天
    │  PM review → 修正 → 本地编译通过
    ▼
第二轮：domain 层逻辑 + Can 服务                      ← ~2 天
    │  PM review → 验收场景逐条对照 → 修正
    ▼
第三轮：adapter 层（Controller / Repository / DDL）    ← ~1 天
    │  PM review → 本地集成测试
    ▼
第四轮：测试代码（P0-5 五必过）                        ← ~1 天
    │  PM review → CI 全绿
    ▼
提交代码 PR → CI 门禁 → 技术验收官审计
```

### 5.2 给 AI 的上下文准备

不论使用哪个 AI 平台，每次编码会话需要向 AI 提供以下上下文：

| 优先级 | 文件 | 目的 |
|:-----:|------|------|
| 必须 | Cap-Spec-1 能力规格书 | AI 理解要做什么 |
| 必须 | Cap-Spec-2 验收场景集 | AI 理解边界和预期输出 |
| 必须 | reasoncodes.csv（本包相关行） | AI 使用正确的 reason_code 常量 |
| 必须 | hl-contracts 中相关的 rules/ YAML | AI 实现正确的裁决逻辑 |
| 推荐 | 已有的 HK 模块代码示例（如 HK.Policy） | AI 遵循统一的 Can→Action→Audit 模式 |
| 推荐 | HK-NAMING-SPEC（命名规范） | AI 使用正确的类名和方法名 |
| 推荐 | hl-platform/CLAUDE.md | AI 了解项目的铁律和约束 |

### 5.3 分层编码提示词示例

**第一轮：contract 层**

```
请为 biz.product 商品中心生成 contract 层 Kotlin 接口。

要求：
1. Pure Kotlin，不依赖 Spring / JPA / 任何框架
2. 遵循 Can→Action 二元拆分：CanCreateProductService / CreateProductService
3. 输入用 data class（{Action}{Entity}Facts）
4. 输出用 sealed class（{Action}{Entity}Result）
5. reason_code 常量类 ProductReasonCodes，值从 reasoncodes.csv 获取

参考已有代码：hk.policy.CanEvaluatePolicyService.kt
遵循命名规范：HK-NAMING-SPEC-KOTLIN-v1

我的 Cap-Spec：[粘贴 Cap-Spec-1 §2~§3]
我的验收场景：[粘贴 Cap-Spec-2 前 3 个 Case]
我的 reason_codes：[粘贴相关行]
```

**第二轮：domain 层 Can 服务**

```
请基于 contract 层接口实现 CanCreateProductService。

裁决链规则：
R1: tenant_id 非空
R2: 操作者具有 admin 角色
R3: SPU 编码不重复
R4: 必须先建 SPU 再挂 SKU（R-061 裁决）
R5: ...

每个 deny 分支必须返回 matched_rule_id 和对应的 reason_code。
参考模式：CanEvaluatePolicyService.kt（R1~R8 裁决链）
```

### 5.4 AI 产出的自检清单

每次 AI 生成代码后，PM 按以下清单检查：

| # | 检查项 | 怎么检查 | 不通过则 |
|---|--------|---------|--------|
| 1 | reason_code 零硬编码 | 搜索 `"biz.product` 字符串，应只出现在 ReasonCodes 常量类中 | 让 AI 修正 |
| 2 | Can 服务每个 deny 有 rule_id | 检查每个 `deny(` 调用有 `matchedRuleId` 参数 | 让 AI 补齐 |
| 3 | API 路径合规 | Controller 的 `@RequestMapping` 路径是 `/biz/{module}/{action}` | 让 AI 修正 |
| 4 | 无 `@ComponentScan` | 全文搜索 | 让 AI 改用 `@Configuration + @Bean` |
| 5 | 无 `@Transactional` | 全文搜索 | 让 AI 改用 `TransactionTemplate` |
| 6 | 无 `@EventListener` | 全文搜索 | 让 AI 改用 `DomainEventPublisher` |
| 7 | 无 `!!` 操作符 | 全文搜索 | 让 AI 改用安全调用 |
| 8 | 本地编译通过 | `./gradlew build` | 修复编译错误后再提交 |

### 5.5 PM 代码 PR 提交

```bash
# 1. 切新分支
cd ~/huanlong-pm/hl-platform
git checkout main && git pull
git checkout -b pm/biz-product-impl

# 2. 添加 AI 生成的文件（逐一确认，不要 git add .）
git add biz-product/src/main/kotlin/...
git add biz-product/src/test/kotlin/...

# 3. 提交
git commit -m "feat(biz.product): implement product CRUD with Can→Action pattern

基于 Cap-Spec-Biz.Product.v1.0 驱动 AI 生成。
覆盖 Cap-Spec-2 Case-001~Case-{N} 全部场景。
{N} 个 reason_code 零硬编码。"

# 4. 推送
git push -u origin pm/biz-product-impl
```

**代码 PR Description 模板**：

```markdown
## 变更摘要
biz.product 能力包完整实现（contract + domain + adapter + DDL + 测试）。

## Cap-Spec 对齐
- Cap-Spec-Biz.Product.v1.0.md → 对齐
- Cap-Spec-Biz.Product.Acceptance.v1.0.md → Case-001~Case-{N} 全覆盖

## AI 编码自检
- [x] reason_code 零硬编码
- [x] Can 服务每个 deny 有 rule_id
- [x] API 路径 /biz/product/* 合规
- [x] 无 @ComponentScan / @Transactional / @EventListener / !!
- [x] 本地 `./gradlew build` 通过
- [x] P0-5 五必过测试通过

## 文件清单
{列出新增的关键文件}

## 待审批人
- [ ] 创始人 @tongzhenghui
- [ ] 技术验收官 @LUXBYA
```

---

## 6. Issue 使用指南

### 6.1 三种 Issue 类型

所有 Issue 提交到 **hl-dispatch** 仓库。

#### A. 文档审查（doc-review）

**用途**：请求团队成员审阅规格文档。

```markdown
标题：[doc-review] Cap-Spec-Biz.Product v1.0 请求审查

标签：doc-review, architect

---

**审查对象**：hl-contracts/prd/biz/Cap-Spec-Biz.Product.v1.0.md
**审查重点**：
1. §2 能力边界是否遗漏
2. §3 业务规则与 contracts 中 rules/ 是否一致

**期望回复时间**：3 个工作日
```

#### B. 任务派发（task-assign）

**用途**：请求运维/基础设施成员执行任务。

```markdown
标题：[task-assign] biz.product DDL Flyway 迁移请求

标签：task-assign, ops

---

**任务描述**：biz.product 代码 PR 已通过 Gate H，需要执行 Flyway 迁移脚本。
**DDL 文件**：hl-platform/biz-product/src/main/resources/db/migration/V1__product.sql
**目标环境**：Staging
**依赖**：PR #{PR_NUMBER} 已 merge
```

#### C. 裁决请求（decision-request）

**用途**：遇到上游模糊或边界争议，请求创始人裁决。

```markdown
标题：[decision-request] biz.product SKU 变体上限是否有硬约束

标签：decision-request

---

**问题背景**：
编写商品创建验收场景时，发现 contracts 中未定义单个 SPU 下 SKU 变体的数量上限。

**我的分析**：
1. 方案 A：不限制（前期简单，后期可能有性能问题）
2. 方案 B：限制 100 个（参考行业惯例）

**我的建议**：方案 B，限制 100 个。

**期望产出**：创始人裁决 + 是否需要新增 reason_code（如 biz.product.create.denied.sku_limit_exceeded）
```

### 6.2 Issue 跟踪习惯

- 自己创建的 Issue 自己负责跟进到关闭
- 裁决回复后，PM 需要在 Issue 下 comment 确认理解并标注后续动作
- 每周五检查自己所有 open 的 Issue，更新进度或关闭已完成的

---

## 7. 跨仓库操作速查

### 7.1 分支命名规范

```
hl-contracts:   pm/{module}-{desc}       例：pm/biz-product-capspec
                pm/{module}-reasoncodes   例：pm/biz-product-reasoncodes

hl-platform:    pm/{module}-{desc}       例：pm/biz-product-impl
                pm/{module}-test          例：pm/biz-product-test

hl-dispatch:    pm/{desc}                例：pm/biz-product-launch
```

### 7.2 提交顺序铁律

```
Step 1: hl-dispatch  → LAUNCH-{MODULE}.md PR   → 创始人 review → merge
Step 2: hl-contracts → Cap-Spec + reasoncodes PR → 创始人 + Gate H review → merge
Step 3: hl-platform  → 代码实现 PR              → CI 门禁 + 创始人 + 技术验收官 review → merge
```

**绝对禁止**：Step 3 引用尚未 merge 的 Step 2 定义。如果 Step 2 PR 被打回修改，Step 3 必须暂停。

### 7.3 日常 Git 操作速查

```bash
# 同步最新代码
git checkout main && git pull

# 查看自己的分支状态
git branch -a | grep pm/

# 查看未提交修改
git status

# 查看 PR 状态（需安装 gh CLI）
gh pr list --author @me

# 查看 Issue 状态
gh issue list --assignee @me -R huanlongAI/hl-dispatch
```

---

## 8. 常见踩坑 & FAQ

### Q1：Cap-Spec 里可以复制 contracts 中的规则定义吗？

**不可以。** Cap-Spec §4 上游引用索引只列路径，不复制内容。复制会导致两处不一致，违反 SSOT 原则。

正确做法：
```markdown
## §4 上游引用索引
| 引用类型 | 路径 | 说明 |
|---------|------|------|
| 创建裁决 | rules/biz.product.create.can.yaml | 商品创建裁决链（7 条规则） |
```

错误做法：
```markdown
## §3 业务规则
R1: tenant_id 必须非空
R2: 操作者必须具有 admin 角色
...（从 rules YAML 复制）
```

### Q2：AI 生成的代码 CI 门禁没通过怎么办？

1. 仔细阅读 CI 报错信息（GitHub Actions 日志）
2. 对照 §5.4 自检清单，通常是以下几类：
   - `check-reason-codes.sh` 失败 → 有 reason_code 硬编码字符串
   - `check-domain-isolation.sh` 失败 → domain 层引入了 Spring import
   - `gate-deny-check.sh` 失败 → deny 路径缺少审计覆盖
3. 将 CI 报错信息喂给 AI，让 AI 修正
4. 修正后 commit + push，CI 会自动重跑

### Q3：创始人裁决迟迟不回复怎么办？

1. 3 个工作日未回复 → 在 Issue 下追加 comment 提醒
2. 5 个工作日未回复 → 钉钉/微信直接联系
3. 同时推进不依赖该裁决的其他工作，不要原地等待

### Q4：技术验收官打回了我的代码 PR 怎么办？

1. 逐条阅读 review comments
2. 区分"必须修"（blocking）和"建议改"（suggestion）
3. 必须修：让 AI 修正后 push 新 commit
4. 建议改：与验收官讨论后决定是否采纳
5. 所有 blocking 问题修复后 re-request review

### Q5：两个 PM 负责的能力包有交集怎么办？

1. 在 hl-dispatch 提 Issue 描述冲突点
2. 优先双方自行协商（在 Issue 下讨论）
3. 无法达成一致 → 升级为 decision-request，创始人仲裁
4. **原则**：能力包边界以 hl-contracts 中的定义为准，PM 不可自行调整

### Q6：我选用的 AI 平台生成代码质量不好怎么办？

1. 检查是否给 AI 提供了足够上下文（§5.2 清单）
2. 尝试分层给指令（§5.3），不要一次性要求生成全部代码
3. 用已有的 HK 模块代码作为参考示例喂给 AI
4. 如果持续不佳，考虑切换 AI 平台或向创始人请教 prompt 技巧
5. 记住：工具和平台的选择权在 PM 手中，选对工具也是产线责任人的能力之一

### Q7：我的 reason_code PR 被 Gate H 打回了怎么办？

通常原因：
- 命名不符合 `biz.{module}.{action}.{outcome}` 格式 → 修改命名
- decision_key 深度不是 3 级 → 调整为 `biz.{module}.{action}.can`
- 与已有 code 重复 → 复用已有 code 而非新增
- visibility 标注不当（内部错误标成 public） → 修改 visibility

---

## 9. 飞书 + GitHub 协作指南

> 详见 FEISHU-GITHUB-COLLABORATION-SPEC v1.0，本节为 PM 视角的操作速查。

### 9.1 PM 关注的飞书群

| 群 | PM 在这里做什么 |
|----|---------------|
| **#唤龙-PM工作台** | 规格方向讨论、与创始人预沟通、收 Cap-Spec PR review 通知 |
| **#唤龙-任务协同** | 技术问题提问、跨角色协调、进度同步 |
| **#唤龙-工程通知** | 看 CI 状态（失败了赶紧修）、看 PR 合并通知 |

### 9.2 飞书沟通铁律

1. **飞书讨论产出结论 → 24h 内写入 GitHub Issue/PR comment**。飞书聊天记录不是决策依据。
2. **关联 GitHub 事项时必须附链接**，不要说"那个 PR"，要贴 URL。
3. **裁决请求必须走 GitHub Issue**（[decision-request] 标签），飞书口头同意不算。
4. **CI 失败通知来了立刻处理**（≤ 4 小时），不要等到第二天。

### 9.3 PM 的飞书日常节奏

| 时段 | 飞书 | GitHub |
|------|------|--------|
| 上午 | #唤龙-PM工作台：看 review 评论 | 处理 PR review feedback |
| | #唤龙-工程通知：看 CI 状态 | 修复 CI 失败 |
| 下午 | #唤龙-PM工作台：讨论规格方向 | AI 编码 → 提交 PR |
| | #唤龙-任务协同：技术问题提问 | |
| 收尾 | — | **把今天飞书讨论结论写入 GitHub** |

### 9.4 典型场景速查

**想提裁决请求**：
1. 飞书 #唤龙-PM工作台 简要说明 → 2. 创建 GitHub Issue → 3. 飞书说"已建 Issue #xxx" → 4. 等创始人在 GitHub 裁决

**CI 挂了飞书通知你**：
1. 点飞书卡片 [查看详情] → 2. 看 GitHub Actions 日志 → 3. 修复 push → 4. CI 重跑

**Cap-Spec PR 被 review 了**：
1. 飞书收到 review 通知 → 2. 去 GitHub 看评论 → 3. 修改后 push → 4. 飞书说"已修改，请再看"

**周五收尾**：
1. 检查 Bitable 看板中自己负责的能力包状态
2. 更新状态（如果没自动同步的话）
3. 检查 open 的 Issue，关闭已完成的

---

## 10. 关键文档快速链接（含飞书协作）

| 文档 | 路径 | 用途 |
|------|------|------|
| TEAM.yml | hl-dispatch/TEAM.yml | 团队角色映射 |
| reasoncodes.csv | hl-contracts/reasoncodes/reasoncodes.csv | reason_code SSOT |
| PM-BRANCH-LAUNCH-TEMPLATE | hl-dispatch/deliverables/decisions/ | 启动规格模板 |
| LAUNCH-PRODUCT-CENTER | hl-dispatch/deliverables/decisions/ | biz.product 实例 |
| PM-AI-COLLABORATION-ONBOARDING-SPEC v2.0 | hl-dispatch/deliverables/decisions/ | PM 角色规格 |
| PRD-REDEFINITION-SPEC v2.0 | hl-dispatch/deliverables/decisions/ | Cap-Spec 定义 |
| TEAM-COLLABORATION-SPEC v1.2 | hl-dispatch/deliverables/decisions/ | 全团队协作规格 |
| HK.Policy 代码（参考实现） | hl-platform/hk-policy/ | Can→Action 模式示例 |
| **FEISHU-GITHUB-COLLABORATION-SPEC v1.0** | hl-dispatch/deliverables/decisions/ | **飞书+GitHub 协作规格** |

---

## 11. 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-30 | v1.0 | 初版——从 PM-AI-COLLABORATION-ONBOARDING-SPEC v2.0 推导实操指南 |
| 2026-03-30 | v1.1 | 新增 §9 飞书+GitHub 协作指南，关联 FEISHU-GITHUB-COLLABORATION-SPEC v1.0 |