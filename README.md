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
| 创始人 | 童正辉 | Owner (@tongzhenghui) | 创建 Issue/PR、合并裁决、最终审批 |
| 架构审计师 | 许久明 | Collaborator (@xujiuming) | 架构设计审查、契约变更、Gate H 技术验收 |
| 运维工程师 | 曾正龙 | Collaborator (@ZDragonMeta) | 基础设施、部署配置、环境搭建、Gate R 运维验收 |
| 项目经理 | 刘建成 | Collaborator (@jianchengl) | 项目管理、进度跟踪、WS-C 项目负责人 |
| 产品经理 | 邹骢 | Collaborator (@zoucong121) | 产品规划（后续另行分工） |
| Java · 技术验收 | 李旭阳 | Collaborator (@LUXBYA) | Java 工程师、WS-C 能力包适配、端到端验收 |
| 后端核心 | 魏鹏 | Collaborator (@wp159951) | Keycloak / Nacos / MQ / HK Client SDK |

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
