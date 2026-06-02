# hl-dispatch

> 唤龙平台 · 协作调度中心

## 定位

hl-dispatch 是唤龙平台仓库体系中的**协作调度仓库**，承载创始人（Cowork）与团队成员之间的异步协作流程。

```
创始人 (Cowork)          团队成员 (GitHub)
    │                        │
    ├─ 创建 Issue/PR ───────→│ 收到通知
    │                        ├─ 审查 / 反馈 / 完成
    │← GitHub 通知 ──────────┤
    ├─ 拉取反馈              │
    ├─ 裁决推进              │
    └─ 关闭归档              │
```

## 协作角色（2026-05-11 对齐 active 派发通讯录，核心组 6 人）

> 详细职责定义见 `deliverables/decisions/TEAM-COLLABORATION-SPEC-v1.0.md`（已升级 v1.2 LOCKED）
> **AI 驱动模型**：所有 Kotlin 代码由创始人 + AI 生成，团队负责审计 + 业务定义 + 运维。不设业务开发者岗位。

| 环 | 角色 | 成员代号 | GitHub 身份 | 职责 |
|----|------|----------|------------|------|
| 裁决层 | 创始人 / 架构师 | L0-Founder | Owner（internal-managed） | 产品决策、架构裁决、全部 Kotlin 代码生成（AI 协同）、PR 合并、里程碑签字 |
| 守护者 | Gate H 守护者 | Gate-H | Collaborator（internal-managed） | 审计 AI 生成代码、架构合规、hl-framework 5 Starters + BOM、Gate H 签字 |
| 守护者 | Gate R 守护者 | Gate-R | Collaborator（internal-managed） | PG18 运维、Docker Compose 环境、Flyway 流水线、Grafana 监控、Gate R 签字 |
| 业务 | 产品经理 | PM-A | Collaborator（internal-managed） | 能力包 MVP 规格、Facts、reason_codes、验收用例、UAT 签收 |
| 业务 | 产品经理 | PM-B | Collaborator（internal-managed） | 能力包 MVP 规格、Facts、reason_codes、验收用例、UAT 签收 |
| 基础设施 | 后端基础设施 | Infra-A | Collaborator（internal-managed） | starter-security JWT / starter-observability / HK Client SDK / 性能基线 |

## 协作模式

### 模式 A：文档审查（Issue）

适用于：培训包、审计报告、架构文档审查

1. Cowork 创建 Issue（使用 `doc-review` 模板）
2. 附文档文件或链接
3. 指派 reviewer + 打标签
4. 团队在 Issue 评论区反馈
5. 创始人裁决后关闭

### 模式 B：任务派发（Issue + Checklist）

适用于：OPS 清单执行、配置确认、环境搭建

1. Cowork 创建 Issue（使用 `task-assign` 模板）
2. 包含任务清单（Checklist）
3. 指派执行人
4. 执行人勾选完成项 + 评论进展
5. 全部完成后创始人验收关闭

### 模式 C：代码/契约变更（PR）

适用于：代码审查、契约文件变更

1. Cowork 在对应仓库（hl-platform / hl-contracts）提 PR
2. 指派 reviewer
3. 团队通过 PR Review 批注
4. 创始人合并

## 协作通讯体系

遵循 **FEISHU-GITHUB-COLLABORATION-SPEC v1.0** 标准，采用飞书群 + GitHub 双通道协作机制：

### 飞书群组与职能

| 协作通道 | 用途 | 成员 |
|----------|------|------|
| 工程通知通道（`AI native工程通知`） | PR/Issue/CI 等主线进程自动推送；GitHub secret: `FEISHU_WEBHOOK_ENGINEERING` | 全团队 |
| 任务协同通道 | 日常任务讨论主阵地 | 业务/工程/基础设施 |
| PM 工作台通道 | PM 规格讨论专用 | PM + 相关 Reviewer |
| 指挥台通道 | 全局状态汇总、裁决通告 | Cowork + Gate 守护者 |

### 核心铁律

**GitHub 是 SSOT（Single Source of Truth）**

飞书群中的讨论结论必须在 **24 小时内** 落地到 GitHub Issue/PR，具体形式：
- 如无 Issue/PR，创建新 Issue 并关联讨论要点
- 如已有 Issue/PR，在评论区补充飞书讨论摘要（@相关人员）
- PM 规格讨论的结论写入 `deliverables/contracts/` 契约文件

**禁止状态**：
- 重大决策仅存在于飞书消息中
- PR Merge 前未在 Issue 区完成异步审查
- 变更记录不关联 Issue/PR

### 主线与个人通知分流

主线进程通知进入工程群，个人进展只走飞书私聊：

- `issues.opened` / `issues.labeled` / `issues.closed` / `issue_comment.created` 进入 `AI native工程通知`。
- `issues.assigned` 是个人进展通知，只私聊被指派人，不再发送到群。

- `issues.assigned` 事件优先读取 `TEAM.yml`，按 GitHub handle 找到飞书 `open_id` 后通过 bot 私聊被指派人。
- 私聊发送主体推荐使用飞书机器人 `node-c 技术合伙人`；将该应用的凭据配置为仓库 secrets `FEISHU_BOT_APP_ID` 和 `FEISHU_BOT_APP_SECRET`。
- 该飞书应用必须具备 bot 发消息权限，并且可见范围覆盖 `TEAM.yml` 中的个人通知对象。
- bot secrets 缺失、成员缺少 `open_id`、成员状态非活跃或私聊发送失败时，workflow 只写 warning 并 fail-open，不发送群 fallback。
- 每次成功投递都会在 GitHub Actions step summary 写入脱敏投递台账：route、recipient、recipient_github、status、content_template、target_url、message_preview。
- 本机手动私发使用 `scripts/feishu-direct-message.rb`，默认 dry-run；只有显式传 `--execute` 才会发送。脚本优先读取 `FEISHU_BOT_APP_ID` / `FEISHU_BOT_APP_SECRET`，未设置时才退回当前 `lark-cli` profile。

示例：

```bash
ruby scripts/feishu-direct-message.rb --github wp159951 --text "请查看 GitHub Issue 链接"
ruby scripts/feishu-direct-message.rb --github wp159951 --text "请查看 GitHub Issue 链接" --execute
```

检查通知投递：

```bash
gh run list --repo huanlongAI/hl-dispatch --workflow "Feishu Notification" --limit 10
gh run view <run_id> --repo huanlongAI/hl-dispatch --json jobs
gh run view <run_id> --repo huanlongAI/hl-dispatch --log | rg FEISHU_DELIVERY_LEDGER_JSON
```

在对应 run 的 summary 中查看 `Feishu delivery ledger`，或用日志里的 `FEISHU_DELIVERY_LEDGER_JSON` 单行 JSON 做命令行检查。台账不记录飞书 `open_id`、密钥或私聊会话全文；内容准确性以 GitHub Issue / comment 的标题、标签、指派人和 URL 为准。

## 标签体系

| 标签 | 颜色 | 用途 |
|------|------|------|
| `doc-review` | 🔵 蓝 | 文档审查请求 |
| `task-assign` | 🟢 绿 | 任务派发 |
| `decision-request` | 🟣 紫 | 裁决征询 |
| `architect` | 🟠 橙 | 指派架构审计师 |
| `ops` | 🟡 黄 | 指派运维工程师 |
| `pm` | 🟢 浅绿 | 指派项目经理 |
| `priority-p0` | 🔴 红 | 紧急 |
| `priority-p1` | 🟠 橙 | 重要 |
| `feedback-given` | 🔵 蓝 | 已反馈待裁决 |
| `approved` | 🟢 绿 | 已通过 |
| `blocked` | 🔴 红 | 阻塞中 |

## 目录结构

```
hl-dispatch/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── doc-review.yml        # 文档审查模板
│   │   ├── task-assign.yml       # 任务派发模板
│   │   └── decision-request.yml  # 裁决征询模板
│   └── workflows/
│       ├── setup-repo.yml        # 标签初始化
│       └── sensitive-scan.yml    # 敏感信息扫描
├── deliverables/                  # Cowork 产出物存放
│   ├── decisions/                 # 技术决策文档
│   ├── training/                  # 培训包
│   ├── audit-reports/             # 审计报告
│   ├── contracts/                 # 契约变更草案
│   └── tasks/                     # 任务相关附件
├── TEAM.yml                       # 团队角色映射
├── SECURITY-POLICY.md             # 安全策略
├── README.md
└── CODEOWNERS
```

## 关联仓库

| 仓库 | 定位 |
|------|------|
| [hl-contracts](https://github.com/huanlongAI/hl-contracts) | 契约法典 SSOT |
| [hl-platform](https://github.com/huanlongAI/hl-platform) | Java 后端 Modulith 实现 |
| [hl-console-native](https://github.com/huanlongAI/hl-console-native) | SwiftUI 原生客户端 |
| [hl-factory](https://github.com/huanlongAI/hl-factory) | AI-Ops 超级工厂 |
| [hl-framework](https://github.com/huanlongAI/hl-framework) | 公司级统一框架（Starters + BOM） |
| **hl-dispatch** | 协作调度中心（本仓库） |
