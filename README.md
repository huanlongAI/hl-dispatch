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

## 协作角色

| 角色 | 成员 | GitHub 身份 | 职责 |
|------|------|------------|------|
| 创始人 | 汤正辉 | Owner | 创建 Issue/PR、合并裁决、最终审批 |
| 架构审计师 | 许久明 | Collaborator | Review 架构设计、契约变更、代码规范 |
| 运维工程师 | 曾正龙 | Collaborator | Review 基础设施、部署配置、环境搭建 |

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

## 标签体系

| 标签 | 颜色 | 用途 |
|------|------|------|
| `doc-review` | 🔵 蓝 | 文档审查请求 |
| `task-assign` | 🟢 绿 | 任务派发 |
| `decision-request` | 🟣 紫 | 裁决征询 |
| `architect` | 🟠 橙 | 指派架构审计师 |
| `ops` | 🟡 黄 | 指派运维工程师 |
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
│       └── auto-label.yml        # 自动标签（预留）
├── deliverables/                  # Cowork 产出物存放
│   ├── training/                  # 培训包
│   ├── audit-reports/             # 审计报告
│   ├── contracts/                 # 契约变更草案
│   └── tasks/                     # 任务相关附件
├── README.md
└── CODEOWNERS
```

## 关联仓库

| 仓库 | 定位 |
|------|------|
| [hl-contracts](https://github.com/huanlongAI/hl-contracts) | 契约法典 SSOT |
| [hl-platform](https://github.com/huanlongAI/hl-platform) | Java 后端实现 |
| [hl-console-native](https://github.com/huanlongAI/hl-console-native) | SwiftUI 原生客户端 |
| [hl-factory](https://github.com/huanlongAI/hl-factory) | AI-Ops 超级工厂 |
| **hl-dispatch** | 协作调度中心（本仓库） |
