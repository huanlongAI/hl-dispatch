# 飞书×GitHub 协作落地执行清单

> 依据：FEISHU-GITHUB-COLLABORATION-SPEC v1.0 LOCKED (2026-03-30)
> 生成日期：2026-03-31
> 执行人：创始人（童正辉）

---

## Phase F-0：飞书建群（~30 分钟）

### 0.1 创建飞书群

- [ ] 创建群 **#唤龙-工程通知**
  - 群类型：内部群
  - 群描述：PR / Issue / CI 事件自动推送（只读为主）
- [ ] 创建群 **#唤龙-任务协同**
  - 群类型：内部群
  - 群描述：任务讨论、进度同步、即时沟通（日常主阵地）
- [ ] 创建群 **#唤龙-PM工作台**
  - 群类型：内部群
  - 群描述：PM 规格讨论、Cap-Spec 审查、业务问题
- [ ] 创建群 **#唤龙-创始人指挥台**
  - 群类型：内部群
  - 群描述：全局状态汇总、审批提醒、关键指标

### 0.2 邀请成员

| 群 | 成员 |
|----|------|
| #唤龙-工程通知 | 童正辉、许久明、曾正龙、邹骢、朱阳、魏鹏、李旭阳 |
| #唤龙-任务协同 | 童正辉、许久明、曾正龙、邹骢、朱阳、魏鹏、李旭阳 |
| #唤龙-PM工作台 | 童正辉、邹骢、朱阳、李旭阳 |
| #唤龙-创始人指挥台 | 仅童正辉 |

- [ ] #唤龙-工程通知 — 7 人已邀请
- [ ] #唤龙-任务协同 — 7 人已邀请
- [ ] #唤龙-PM工作台 — 4 人已邀请
- [ ] #唤龙-创始人指挥台 — 仅自己

### 0.3 添加 Custom Bot

每个群添加一个「自定义机器人」（Custom Bot），用于接收 GitHub Webhook 推送。

- [ ] #唤龙-工程通知 → 添加 Bot，命名 `GitHub-工程通知`
  - 复制 Webhook URL → 记为 `WEBHOOK_URL_ENGINEERING`
  - 开启签名校验 → 记录 Secret
- [ ] #唤龙-任务协同 → 添加 Bot，命名 `GitHub-任务协同`
  - 复制 Webhook URL → 记为 `WEBHOOK_URL_TASK`
  - 开启签名校验 → 记录 Secret
- [ ] #唤龙-PM工作台 → 添加 Bot，命名 `GitHub-PM工作台`
  - 复制 Webhook URL → 记为 `WEBHOOK_URL_PM`
  - 开启签名校验 → 记录 Secret
- [ ] #唤龙-创始人指挥台 → 添加 Bot，命名 `GitHub-指挥台`
  - 复制 Webhook URL → 记为 `WEBHOOK_URL_COMMAND`
  - 开启签名校验 → 记录 Secret

### 0.4 验证

- [ ] 在每个群发一条测试消息确认群功能正常
- [ ] 记录 4 个 Webhook URL，下一步 F-1 需要

---

## Phase F-1：GitHub Webhook 配置（~30 分钟）

### 方案选择（D-3 裁决：GitHub 原生飞书 App）

优先使用 **GitHub 官方飞书集成 App**（最快上线）。如不可用则退回 Webhook + 转发脚本。

### 1.1 hl-platform Webhook

- [ ] GitHub → huanlongAI/hl-platform → Settings → Webhooks → Add webhook
  - Payload URL：`WEBHOOK_URL_ENGINEERING`
  - Content type：`application/json`
  - Secret：对应 Bot 的签名密钥
  - Events：选 "Let me select individual events"
    - [x] Pull requests
    - [x] Pull request reviews
    - [x] Workflow runs（CI 状态）
    - [x] Push（仅 main 分支关注）
- [ ] 点击 "Add webhook" 并确认 delivery 显示 ✅

### 1.2 hl-contracts Webhook

- [ ] GitHub → huanlongAI/hl-contracts → Settings → Webhooks → Add webhook
  - Payload URL：`WEBHOOK_URL_ENGINEERING`（工程通知群）
  - Events：
    - [x] Push（契约更新通知）
    - [x] Pull requests（Cap-Spec PR）
- [ ] 额外添加第二个 Webhook → `WEBHOOK_URL_PM`（PM 工作台群）
  - Events：
    - [x] Pull requests（Cap-Spec PR 专用通知）
- [ ] 确认两个 Webhook delivery 均 ✅

### 1.3 hl-framework Webhook

- [ ] GitHub → huanlongAI/hl-framework → Settings → Webhooks → Add webhook
  - Payload URL：`WEBHOOK_URL_ENGINEERING`
  - Events：
    - [x] Pull requests
    - [x] Pull request reviews
    - [x] Workflow runs
- [ ] 确认 delivery ✅

### 1.4 hl-dispatch Webhook

- [ ] GitHub → huanlongAI/hl-dispatch → Settings → Webhooks → Add webhook
  - Payload URL：`WEBHOOK_URL_TASK`（任务协同群）
  - Events：
    - [x] Issues
    - [x] Issue comments
- [ ] 额外添加第二个 Webhook → `WEBHOOK_URL_COMMAND`（创始人指挥台）
  - Events：
    - [x] Issues（用于 decision-request 标签 Issue 通知）
- [ ] 确认两个 Webhook delivery 均 ✅

### 1.5 端到端验证

- [ ] 在 hl-platform 创建一个 Draft PR → 确认 #唤龙-工程通知 收到通知
- [ ] 在 hl-dispatch 创建一个测试 Issue → 确认 #唤龙-任务协同 收到通知
- [ ] 在 hl-contracts 推一个小 commit → 确认 #唤龙-工程通知 收到"契约更新"
- [ ] 清理测试 PR / Issue

> 注意：GitHub 原生飞书 App 的消息格式可能较为简单。如需更精细的卡片模板（如 D-3 裁决提到的 [查看PR] 按钮），需要后续在 Phase F-3 通过 super-founder App 处理层升级。Phase F-1 以"能收到通知"为验收标准。

---

## Phase F-2：Bitable 看板建立（~2 小时）

### 2.1 创建多维表格

- [ ] 飞书 → 多维表格 → 新建 → 命名 **「唤龙项目看板」**
- [ ] 设置权限：核心组 7 人只读，创始人可编辑

### 2.2 表 1：能力包看板

创建字段：

| 字段名 | 类型 | 选项/说明 |
|--------|------|----------|
| 能力包 ID | 文本 | 如 `biz.product` |
| 中文名 | 文本 | 如 `商品中心` |
| PM 负责人 | 人员 | 邹骢 / 朱阳 |
| 当前阶段 | 单选 | 规格 / 编码 / 审计 / 验收 / 完成 |
| Cap-Spec PR | 链接 | hl-contracts PR URL |
| 代码 PR | 链接 | hl-platform PR URL |
| Gate H | 单选 | 待审 / 通过 / 打回 |
| Gate 3 | 单选 | 待审 / 通过 / 打回 |
| Gate R | 单选 | 待审 / 通过 / 就绪 |
| 最后更新 | 日期 | 手动更新 |

- [ ] 字段创建完成
- [ ] 初始数据录入 — biz.product（邹骢负责，当前阶段：规格）

### 2.3 表 2：Sprint 进度

| 字段名 | 类型 | 选项/说明 |
|--------|------|----------|
| Sprint | 单选 | S0 / S1 / S2 / S3 / S4 |
| 角色 | 人员 | |
| 交付物 | 文本 | |
| 状态 | 单选 | 未开始 / 进行中 / 完成 / 阻塞 |
| 阻塞原因 | 文本 | 手动填写 |
| 关联 Issue | 链接 | hl-dispatch Issue URL |

- [ ] 字段创建完成
- [ ] 按 TEAM-COLLABORATION-SPEC §2.4 录入当前 Sprint 各角色交付物

### 2.4 表 3：PR 审查看板

| 字段名 | 类型 | 选项/说明 |
|--------|------|----------|
| PR 标题 | 文本 | |
| 仓库 | 单选 | hl-platform / hl-framework / hl-contracts / hl-console-native / hl-dispatch / hl-factory |
| 作者 | 人员 | |
| Reviewer | 人员 | |
| 状态 | 单选 | Open / Reviewing / Approved / Merged / Closed |
| CI 状态 | 单选 | 通过 / 失败 / 运行中 |
| 等待天数 | 公式 | `TODAY() - 创建日期` |
| 链接 | URL | PR URL |

- [ ] 字段创建完成

### 2.5 视图配置

- [ ] 表 1 添加「看板视图」— 按"当前阶段"分组
- [ ] 表 2 添加「看板视图」— 按"状态"分组
- [ ] 表 3 添加筛选视图「待审查」— 状态 = Open 或 Reviewing
- [ ] 在 #唤龙-创始人指挥台 群描述中添加 Bitable 链接

### 2.6 分享与验证

- [ ] 分享给核心组 7 人（只读权限）
- [ ] 在 #唤龙-任务协同 群发布 Bitable 链接公告
- [ ] 请 1 位成员确认可以打开并查看

---

## Phase F-2.5：关联文档修订（P0 + P1）

依据 SPEC §9 关联文档修订清单：

- [x] **P0** PM-PRACTICAL-HANDBOOK v1.0 → 已完成 §9 飞书协作指南（v1.1, 2026-03-31）
- [ ] **P1** TEAM-COLLABORATION-SPEC v1.2 → §2.3 日常协作模式追加飞书通道说明
- [ ] **P1** PM-AI-COLLABORATION-ONBOARDING-SPEC v2.0 → Phase 1 追加飞书群邀请步骤
- [ ] **P1** hl-dispatch/README.md → 补充飞书群信息

---

## Phase F-3：自动化升级（后续，依赖 super-founder IM 集成）

待 super-founder App Phase IM-1~IM-4 完成后执行，当前 **BLOCKED**。

- [ ] 升级 GitHub → 飞书通知为 App 内嵌处理
- [ ] 精细事件过滤和路由
- [ ] 交互卡片模板（[查看PR] 按钮等）
- [ ] Bitable 实时自动同步（替代手动更新）
- [ ] 飞书 → App 双向交互

---

## 执行节奏建议

| 日期 | 目标 | 预计耗时 |
|------|------|---------|
| Day 1 | F-0 建群 + 邀请 + Bot | 30 分钟 |
| Day 1 | F-1 Webhook 配置 + 端到端验证 | 30 分钟 |
| Day 2 | F-2 Bitable 3 张表 + 初始数据 | 2 小时 |
| Day 2 | F-2.5 关联文档 3 项 P1 修订（可派发 CLI） | 30 分钟 |
| Day 2 | 在 #唤龙-任务协同 群发布上线公告 | 10 分钟 |

**总计约 4 小时，可在 1~2 天内完成。**

---

## 上线公告模板

完成 F-0 + F-1 + F-2 后，在 #唤龙-任务协同 发布：

```
📢 唤龙飞书×GitHub 协作正式上线

各位好，飞书协作体系已配置完成：

🔔 #唤龙-工程通知 — PR/CI/契约变更自动推送
💬 #唤龙-任务协同 — 日常任务讨论主阵地
📋 #唤龙-PM工作台 — PM 规格讨论专用
📊 项目看板 — [Bitable 链接]

核心铁律：
① GitHub 是事实真源，飞书不存储决策
② 飞书讨论产出结论 → 24h 内写入 GitHub Issue/PR
③ 关联 GitHub 事项时必须附链接

详细规范见：FEISHU-GITHUB-COLLABORATION-SPEC v1.0
有问题在本群提出。
```

---

> 本清单由 Cowork NODE-M 自动生成，依据 FEISHU-GITHUB-COLLABORATION-SPEC v1.0 LOCKED。
