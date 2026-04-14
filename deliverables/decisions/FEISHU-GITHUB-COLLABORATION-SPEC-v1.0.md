# 唤龙平台飞书 + GitHub 协作规格

## FEISHU-GITHUB-COLLABORATION-SPEC v1.0

---

**文档编号**：HL-FEISHU-COLLAB-001
**版本**：v1.0
**日期**：2026-03-30
**状态**：LOCKED（创始人已裁决 D-1~D-6，2026-03-30）
**派生链**：super-founder/FEISHU-INTEGRATION-PLAN v4.0（飞书集成架构参考）+ TEAM-COLLABORATION-SPEC v1.2（唤龙协作模型）→ 本文档
**适用对象**：唤龙平台核心组全体成员（7 人）

---

## 0. 推导声明

| 编号 | 输入 | 关键约束 |
|------|------|----------|
| I-1 | TEAM-COLLABORATION-SPEC v1.2 LOCKED | 三环模型、GitHub Issue 三模式、门禁体系 |
| I-2 | super-founder/FEISHU-INTEGRATION-PLAN v4.0 | 四群分流、双通道原则、卡片模板、Bitable 投影 |
| I-3 | R-IM-001（飞书为唯一 IM 平台） | 不使用钉钉/微信作为工程协作通道 |
| I-4 | R-IM-002（双通道分流：Custom Bot + App Bot） | 推送免配额 / 双向消耗配额 |
| I-5 | PM-AI-COLLABORATION-ONBOARDING-SPEC v2.0 | PM 产线责任人模式、Cap-Spec 工件集 |

**推导逻辑**：

```
super-founder 的飞书架构（四群分流 + 双通道 + Bitable）
  → 唤龙团队有 7 人 + GitHub 六仓库 → 需要更贴合多人协作的群结构
  → 唤龙核心协作载体是 GitHub Issue/PR → 飞书为辅助通知+即时沟通
  → 结论：GitHub 是 SSOT，飞书是即时通讯层 + 可视化投影层
```

**核心原则：GitHub 是事实真源，飞书不存储决策。**

任何需要留痕的决策、规格变更、裁决，必须在 GitHub Issue/PR 中完成。飞书用于即时讨论和通知推送，但飞书聊天记录不作为决策依据。

---

## 1. 飞书群结构

### 1.1 群规划

从 super-founder 四群模型适配唤龙团队场景：

| # | 群名 | 成员 | 职责 | 对应 GitHub 事件源 |
|---|------|------|------|-------------------|
| 1 | **工程通知通道** | 核心组全员 | PR / Issue / CI 事件自动推送 | hl-platform / hl-framework / hl-contracts 的 Webhook |
| 2 | **任务协同通道** | 核心组全员 | 任务讨论、进度同步、即时沟通 | hl-dispatch Issue 变更 |
| 3 | **PM 工作台通道** | 创始人 + PM-A + PM-B + 技术验收官 | PM 规格讨论、Cap-Spec 审查、业务问题 | hl-contracts PR |
| 4 | **指挥台通道** | 仅创始人 | 全局状态汇总、审批提醒、关键指标 | 跨仓库汇总 |

**与 super-founder 的差异**：

| super-founder 群 | 唤龙适配 | 变更原因 |
|-----------------|---------|--------|
| #工程通知 | 工程通知通道 | 加前缀区分产品线 |
| #任务中枢 | 任务协同通道 | 唤龙团队更强调多人协同而非单向派发 |
| #文档动态 | 合并入 PM 工作台通道 | 唤龙文档变更主要由 PM 驱动，合并减少群数 |
| #创始人指挥台 | 指挥台通道 | 保持 |

### 1.2 群行为规范

**工程通知通道**（只读为主）
- Bot 自动推送 GitHub 事件，人类一般不在此群讨论
- 如需讨论某个 PR/Issue，发飞书消息时附上 GitHub 链接，讨论在 GitHub 上完成
- 每周一创始人在此群发布周报/本周目标

**任务协同通道**（日常沟通主阵地）
- 任务相关即时讨论在此进行
- 讨论产出结论后，责任人将结论写入 GitHub Issue comment
- 禁止仅在飞书达成共识而不更新 GitHub（违反 SSOT 原则）

**PM 工作台通道**（PM 专属）
- PM 规格方向讨论、Cap-Spec 初稿讨论
- 创始人对 PM decision-request 的快速预沟通（正式裁决仍走 GitHub）
- 技术验收官对 PM 代码 PR 的即时反馈

**指挥台通道**（仅创始人）
- 汇总各群关键事件
- 待审批 PR/Issue 提醒
- Bitable 仪表盘快速入口

---

## 2. GitHub → 飞书通知规则

### 2.1 自动通知映射

沿用 super-founder 的事件路由模式，适配唤龙六仓库：

| GitHub 事件 | 仓库范围 | 目标群 | 卡片内容 |
|------------|---------|--------|--------|
| PR opened | hl-platform / hl-framework | 工程通知通道 | 标题 + 作者 + 分支 + [查看PR] 按钮 |
| PR merged | 全部仓库 | 工程通知通道 | 标题 + 合并者 + commit 数 |
| PR review requested | 全部仓库 | 工程通知通道 + **@被指派人** | "你有一个待审查 PR" |
| Issue opened | hl-dispatch | 任务协同通道 | 标签 + 标题 + 指派人 + [查看Issue] 按钮 |
| Issue labeled `decision-request` | hl-dispatch | 指挥台通道 | "有新的裁决请求" |
| CI workflow failed | hl-platform / hl-framework | 工程通知通道 | 失败步骤 + PR 链接 + 作者 |
| CI workflow passed | hl-platform | 工程通知通道（静默） | 仅更新 Bitable 状态，不发群消息 |
| Push to main | hl-contracts | 工程通知通道 | "契约更新" + commit 消息 |
| Cap-Spec PR opened | hl-contracts（pm/ 分支） | PM 工作台通道 | "新的能力规格待审查" |

### 2.2 @提醒规则

飞书群消息中 @特定成员的触发规则：

| 触发条件 | @谁 | 群 |
|---------|-----|-----|
| PR reviewer 被指派 | @被指派人 | 工程通知通道 |
| Issue 被 assign | @被指派人 | 任务协同通道 |
| decision-request Issue | @创始人 | 指挥台通道 |
| Gate H 审查完成 | @PR 作者 | 工程通知通道 |
| PM 的 Cap-Spec PR | @创始人 + @Gate H | PM 工作台通道 |
| 3 天未回复的 PR review | @被指派人 | 任务协同通道 |

### 2.3 通知静默规则

以下事件不推送飞书，避免噪音：

- CI 正常通过（非 main 分支的常规 push 成功）
- Draft PR 的创建和更新
- Bot 自动生成的 commit（如 dependabot）
- hl-factory 仓库的内部操作（AI-Ops 工具链）

---

## 3. 飞书 ↔ GitHub 协作流程

### 3.1 PM 能力包全流程中的飞书触点

```
① 创始人裁决立项
    ↓  飞书：PM 工作台通道 通知 PM "biz.{module} 已裁决，你可以开始了"

② PM 编写 Cap-Spec
    ↓  飞书：PM 工作台通道 即时讨论规格方向
    ↓  GitHub：PM 提交 Cap-Spec PR（正式产出）
    ↓  飞书：PM 工作台通道 自动通知 "Cap-Spec PR 待审查"

③ 创始人 + Gate H review
    ↓  飞书：review comment 自动推送 PM 工作台通道
    ↓  GitHub：正式 review 和 approval

④ PM 驱动 AI 编码
    ↓  飞书：如有技术问题，在 任务协同通道 即时讨论
    ↓  GitHub：PM 提交代码 PR
    ↓  飞书：工程通知通道 自动通知 "新代码 PR"

⑤ CI 门禁
    ↓  飞书：CI 失败 → 工程通知通道 @PM "CI 失败，请检查"
    ↓  飞书：CI 通过 → 静默

⑥ 技术验收官审计
    ↓  飞书：PR review 自动通知 工程通知通道 @技术验收官
    ↓  飞书：review comment 推送 PM 工作台通道

⑦ 创始人签收
    ↓  飞书：指挥台通道 "里程碑待签收"
```

### 3.2 Gate 守护者日常流程中的飞书触点

**Gate H（Gate-H）日常**：
```
上午                              下午
────────────────────────────────────────
飞书 工程通知通道               飞书同步审查进度
├ 检查新 PR 通知                  ├ 在 GitHub 提交 review
├ 筛选需要 Gate H 的 PR           └ 飞书 任务协同通道 同步状态
└ 打开 GitHub 开始审查
```

**Gate R（Gate-R）日常**：
```
飞书 任务协同通道              GitHub
├ 检查 task-assign Issue          ├ 处理运维任务
├ 环境问题即时反馈                └ 更新 Issue 状态
└ 发布前在飞书确认各方就绪
```

### 3.3 关键协作场景的飞书+GitHub 配合

#### 场景 A：PM 提出裁决请求

```
1. PM 在飞书 PM 工作台通道 简要说明问题（即时沟通）
2. 创始人口头确认"这需要正式裁决"
3. PM 创建 hl-dispatch Issue（[decision-request] 标签）← SSOT
4. 飞书自动推送到 指挥台通道
5. 创始人在 GitHub Issue 中回复裁决（留痕）
6. 创始人在飞书 PM 工作台通道 简要同步"已裁决，见 Issue #xxx"
```

**反模式**：PM 只在飞书群讨论获得口头同意就开始执行，不创建 Issue → 违反 SSOT。

#### 场景 B：CI 失败处理

```
1. CI 失败 → 飞书 工程通知通道 自动 @PM "CI 门禁失败"
2. PM 点击飞书卡片中的 [查看详情] 按钮 → 跳转 GitHub Actions
3. PM 修复后 push → CI 重跑
4. CI 通过 → 静默（不打扰群）
5. CI 再次失败 → 飞书再次通知 + 同时 @Gate H 关注
```

#### 场景 C：发布前多方确认

```
1. 创始人在飞书 任务协同通道 发起："biz.product 准备发布，各方确认"
2. Gate H 飞书回复："代码审计通过 ✅"
3. Gate 3 飞书回复："E2E 验证通过 ✅"
4. Gate R 飞书回复："环境就绪 ✅"
5. PM 飞书回复："UAT 全部通过 ✅"
6. 创始人在 GitHub 创建 Release → 飞书 工程通知通道 自动通知
```

对应 GitHub 侧：每人在对应 Issue 中 comment 确认并附上证据链接。

---

## 4. 飞书多维表格（Bitable）投影

### 4.1 定位

沿用 super-founder R-IM-007：Bitable 是团队只读投影，不是 SSOT。数据来源是 GitHub，Bitable 自动同步展示。

团队成员（尤其非工程角色、管理层）通过 Bitable 看到项目进度的可视化总览，无需频繁打开 GitHub。

### 4.2 表结构设计

#### 表 1：能力包看板

| 字段 | 类型 | 数据源 |
|------|------|--------|
| 能力包 ID | 文本 | hl-contracts/capabilities.yaml |
| 中文名 | 文本 | LAUNCH-{MODULE}.md §1 |
| PM 负责人 | 人员 | TEAM.yml |
| 当前阶段 | 单选（规格/编码/审计/验收/完成） | GitHub PR 状态推导 |
| Cap-Spec PR | 链接 | hl-contracts PR URL |
| 代码 PR | 链接 | hl-platform PR URL |
| Gate H | 状态（待审/通过/打回） | PR review 状态 |
| Gate 3 | 状态 | PR review 状态 |
| Gate R | 状态 | Release 验证状态 |
| 最后更新 | 日期 | GitHub API |

#### 表 2：Sprint 进度

| 字段 | 类型 | 数据源 |
|------|------|--------|
| Sprint | 单选（S0~S4） | R-053 定义 |
| 角色 | 人员 | TEAM.yml |
| 交付物 | 文本 | TEAM-COLLABORATION-SPEC §2.4 |
| 状态 | 单选（未开始/进行中/完成/阻塞） | Issue 状态 |
| 阻塞原因 | 文本 | Issue comment |
| 关联 Issue | 链接 | hl-dispatch Issue URL |

#### 表 3：PR 审查看板

| 字段 | 类型 | 数据源 |
|------|------|--------|
| PR 标题 | 文本 | GitHub PR |
| 仓库 | 单选 | PR 仓库 |
| 作者 | 人员 | PR author |
| Reviewer | 人员 | PR requested_reviewers |
| 状态 | 单选（Open/Reviewing/Approved/Merged/Closed） | PR 状态 |
| CI 状态 | 单选（通过/失败/运行中） | CI workflow status |
| 等待天数 | 公式 | today - created_at |
| 链接 | URL | PR URL |

### 4.3 数据同步策略

| 方式 | 频率 | 适用场景 |
|------|------|--------|
| **GitHub Webhook → App → Bitable API** | 实时 | PR/Issue 状态变更（依赖 super-founder IM 集成完成） |
| **定时脚本（临时方案）** | 每日 1 次 | IM 集成完成前的过渡方案 |
| **人工更新** | 按需 | 非自动化覆盖的字段（如阻塞原因） |

**过渡期方案**：在 super-founder App 飞书集成（Phase IM-4）完成前，由创始人或 PM 每日手动更新关键字段。自动化后全部切为 Webhook 驱动。

---

## 5. 飞书沟通规范

### 5.1 消息格式

**日常沟通**：自然语言即可，无强制模板。

**关联 GitHub 事项时**：必须附上链接。

```
✅ 正确：biz.product 的 Cap-Spec 初稿写好了，PR 在这里：https://github.com/huanlongAI/hl-contracts/pull/42

❌ 错误：biz.product 的 Cap-Spec 写好了，你们看看。（没有链接，不知道在哪看）
```

**同步裁决/决策时**：

```
✅ 正确：SKU 变体上限已裁决为 100 个，详见 Issue #58。请以 GitHub Issue 为准。

❌ 错误：SKU 变体上限定了 100 个。（口头传达无留痕）
```

### 5.2 响应时效

| 消息类型 | 期望响应时间 | 说明 |
|---------|:----------:|------|
| @你 的审查请求 | ≤ 1 工作日 | PR review / doc-review |
| @你 的 CI 失败通知 | ≤ 4 小时 | 自己的 PR 失败需及时修复 |
| 裁决请求 | ≤ 3 工作日 | 创始人裁决，同 GitHub Issue SLA |
| 一般群讨论 | 无硬性要求 | 但建议当日内看过 |

### 5.3 飞书讨论 → GitHub 落地的铁律

```
飞书讨论产出结论 → 责任人 24h 内写入 GitHub Issue/PR comment
飞书口头达成共识 ≠ 正式裁决（必须走 GitHub decision-request）
飞书无法搜索 → 重要信息必须在 GitHub 留痕
```

---

## 6. 角色在飞书中的日常行为

### 6.1 PM（PM-A/PM-B）

| 时段 | 飞书动作 | GitHub 动作 |
|------|---------|------------|
| 上午 | 检查 PM 工作台通道 讨论 | 检查 PR review 评论 |
| | 检查 工程通知通道 CI 状态 | 修复 CI 失败 |
| 下午 | 规格方向在 PM 工作台通道 即时讨论 | AI 编码 → 提交 PR |
| | 技术问题在 任务协同通道 提问 | 更新 Issue 状态 |
| 收尾 | — | 将当日飞书讨论结论写入 GitHub |

### 6.2 Gate H 守护者（Gate-H）

| 时段 | 飞书动作 | GitHub 动作 |
|------|---------|------------|
| 上午 | 工程通知通道 看新 PR | 开始 PR review |
| 下午 | 任务协同通道 同步审查进度 | 提交 review comments |
| | 如有架构疑问，PM 工作台通道 讨论 | — |

### 6.3 Gate R 守护者（Gate-R）

| 时段 | 飞书动作 | GitHub 动作 |
|------|---------|------------|
| 上午 | 任务协同通道 看 task-assign Issue | 执行运维任务 |
| 下午 | 环境问题即时反馈 | 更新 Issue 状态 |
| 发布前 | 任务协同通道 确认发布就绪 | 创建 Release 验证 Issue |

### 6.4 技术验收官（Gate-3）

| 时段 | 飞书动作 | GitHub 动作 |
|------|---------|------------|
| 收到通知 | 工程通知通道 看 PM 代码 PR | Gate 3 审计 |
| 验收中 | PM 工作台通道 反馈问题 | 提交 review comments |
| 完成 | 任务协同通道 同步验收结果 | approve PR |

### 6.5 后端基础设施（Infra-A）

| 时段 | 飞书动作 | GitHub 动作 |
|------|---------|------------|
| 上午 | 工程通知通道 看 hl-framework PR | Starter 开发 / review |
| 下午 | 任务协同通道 同步进度 | 更新 Issue / 提交 PR |

### 6.6 创始人

| 时段 | 飞书动作 | GitHub 动作 |
|------|---------|------------|
| 上午 | 指挥台通道 总览 | 审批 PR / 回复裁决 |
| | PM 工作台通道 回应 PM 讨论 | |
| 周一 | 工程通知通道 发布周报 | 更新 Sprint 看板 |
| 周五 | 指挥台通道 检查里程碑 | 里程碑签收 |

---

## 7. 实施路线

### Phase F-0：飞书群建立（~30 分钟，创始人执行）

| # | 动作 | 验证 |
|---|------|------|
| 0.1 | 创建 工程通知通道 群 | 群可见 |
| 0.2 | 创建 任务协同通道 群 | 群可见 |
| 0.3 | 创建 PM 工作台通道 群 | 群可见 |
| 0.4 | 创建 指挥台通道 群 | 群可见 |
| 0.5 | 各群邀请对应成员（按 §1.1） | 成员列表正确 |
| 0.6 | 各群添加 Custom Bot（签名校验模式） | 拿到 4 个 Webhook URL |

### Phase F-1：GitHub Webhook 配置（~30 分钟，创始人执行）

| # | 动作 | 验证 |
|---|------|------|
| 1.1 | hl-platform 配置 Webhook → 工程通知通道 Bot | PR 事件推送到群 |
| 1.2 | hl-contracts 配置 Webhook → 工程通知通道 Bot | 契约更新推送到群 |
| 1.3 | hl-framework 配置 Webhook → 工程通知通道 Bot | Starter 变更推送 |
| 1.4 | hl-dispatch 配置 Webhook → 任务协同通道 Bot | Issue 变更推送 |

**注意**：Phase F-1 使用 GitHub 原生飞书集成（GitHub App for Feishu）或简单的 Webhook → Custom Bot 脚本。不依赖 super-founder App 的 IM 集成（那是 Phase IM-1 的事）。

### Phase F-2：Bitable 看板建立（~2 小时，创始人执行）

| # | 动作 | 验证 |
|---|------|------|
| 2.1 | 创建"唤龙项目看板"多维表格 | 可访问 |
| 2.2 | 建立表 1（能力包看板）+ 表 2（Sprint 进度）+ 表 3（PR 审查看板） | 字段齐全 |
| 2.3 | 初始数据录入 | 当前状态正确反映 |
| 2.4 | 分享给核心组成员（只读） | 成员可查看 |

### Phase F-3：自动化升级（super-founder IM 集成完成后）

待 super-founder App Phase IM-1~IM-4 完成后，将 GitHub → 飞书通知从简单 Webhook 升级为 App 内嵌处理，获得：

- 更精细的事件过滤和路由
- 更美观的交互卡片
- Bitable 实时自动同步
- 飞书 → App 双向交互

---

## 8. 待裁决事项

| # | 事项 | 裁决结果 | 裁决日期 |
|---|------|---------|----------|
| D-1 | 飞书群结构 | **✅ A) 四群清晰分流**（#工程通知 / #任务协同 / #PM工作台 / #创始人指挥台） | 2026-03-30 |
| D-2 | Bitable 更新责任 | **✅ B) PM 负责各自能力包行**，创始人负责全局字段 | 2026-03-30 |
| D-3 | GitHub → 飞书通知方式 | **✅ A) GitHub 原生飞书 App**，最快上线 | 2026-03-30 |
| D-4 | CI 通过是否静默 | **✅ B) main 分支不静默**，非 main CI 通过静默 | 2026-03-30 |
| D-5 | 飞书讨论落地 SLA | **✅ A) 24h 写入 GitHub**，铁律 | 2026-03-30 |
| D-6 | 是否启用飞书审批流 | **✅ A) 不启用**，审批走 GitHub PR，GitHub 是 SSOT | 2026-03-30 |

---

## 9. 关联文档修订清单

| 文档 | 修订内容 | 优先级 |
|------|---------|:-----:|
| PM-PRACTICAL-HANDBOOK v1.0 | 新增 §11 飞书协作指南（引用本文档） | P0 |
| TEAM-COLLABORATION-SPEC v1.2 | §2.3 日常协作模式追加飞书通道说明 | P1 |
| PM-AI-COLLABORATION-ONBOARDING-SPEC v2.0 | Phase 1 追加飞书群邀请步骤 | P1 |
| hl-dispatch/README.md | 补充飞书群信息 | P1 |

---

## 10. 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-30 | v1.0 | 初版——从 super-founder FEISHU-INTEGRATION-PLAN v4.0 适配唤龙团队 |
| 2026-03-30 | v1.0 LOCKED | 创始人裁决 D-1~D-6 全部通过：四群分流、PM 负责 Bitable、GitHub 原生飞书 App、main CI 不静默、24h 落地铁律、审批走 GitHub |