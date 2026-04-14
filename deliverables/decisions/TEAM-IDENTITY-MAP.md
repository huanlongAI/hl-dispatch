# 唤龙团队身份映射表

> 版本：v1.2 | 更新日期：2026-04-02
> 维护人：L0-Founder

---

## 核心组（7 人）

| # | 成员代号 | GitHub 账号 | GitHub 邮箱 | 团队角色 | 环 | GitHub Team |
|---|----------|------------|------------|---------|-----|------------|
| 1 | L0-Founder | `internal-managed` | `redacted` | 创始人 / 架构师 | 裁决层 | `founder-only` |
| 2 | Gate-H | `internal-managed` | `redacted` | Gate H 守护者 | 守护者环 | `guardian-team` |
| 3 | Gate-R | `internal-managed` | `redacted` | Gate R 守护者 | 守护者环 | `guardian-team` |
| 4 | PM-A | `internal-managed` | `redacted` | PM（商品） | 领域环 | `pm-team` |
| 5 | PM-B | `internal-managed` | `redacted` | PM（交易） | 领域环 | `pm-team` |
| 6 | Infra-A | `internal-managed` | `redacted` | 后端基础设施 | 基础设施环 | `infra-team` |
| 7 | Gate-3 | `internal-managed` | `redacted` | 技术验收官（Gate 3） | 基础设施环 | `infra-team` |

## 组织成员（当前）

| GitHub 账号 | 对应成员代号 | 组织角色 | 状态 |
|-------------|--------------|---------|------|
| `internal-managed` | L0-Founder | owner | ✅ 已加入 |
| `internal-managed` | Gate-H | member | ✅ 已加入 |
| `internal-managed` | Gate-R | member | ✅ 已加入（guardian-team） |

## 待接受邀请（4 人）

| GitHub 账号 | 成员代号 | 邮箱 | Team | 状态 |
|-------------|----------|------|------|------|
| `internal-managed` | PM-A | `redacted` | `pm-team` | ✉️ 待接受 |
| `internal-managed` | PM-B | `redacted` | `pm-team` | ✉️ 待接受 |
| `internal-managed` | Gate-3 | `redacted` | `infra-team` | ✉️ 待接受 |
| `internal-managed` | Infra-A | `redacted` | `infra-team` | ✉️ 待接受 |

## 飞书群成员映射

| 协作通道 | 成员 |
|----------|------|
| 工程通知通道 | L0-Founder、Gate-H、Gate-R、PM-A、PM-B、Infra-A、Gate-3 |
| 任务协同通道 | L0-Founder、Gate-H、Gate-R、PM-A、PM-B、Infra-A、Gate-3 |
| PM 工作台通道 | L0-Founder、PM-A、PM-B、Gate-3 |
| 指挥台通道 | L0-Founder |

## GitHub Team 权限矩阵

| Team | hl-contracts | hl-platform | hl-framework | hl-dispatch | hl-console-native | hl-factory |
|------|-------------|-------------|--------------|-------------|-------------------|------------|
| `founder-only` | admin | admin | admin | admin | admin | admin |
| `pm-team` | **write** | read | — | read | — | — |
| `guardian-team` | read | **write** | **write** | — | — | — |
| `infra-team` | — | **write** | **write** | — | — | — |

## 操作记录

- [x] Gate-3 身份映射已确认
- [x] 收集全部 7 个协作角色的 GitHub 账号与联系信息（明细已转内控存储）
- [x] GitHub 组织席位 4 → 7（2026-04-02）
- [x] 5 人邀请已发送（PM-A、PM-B、Gate-3、Gate-R、Infra-A）
- [x] 创建 `guardian-team`（id: redacted）— Gate-H 已加入，Gate-R 待接受邀请后加入
- [x] 创建 `infra-team`（id: redacted）— Infra-A、Gate-3 待接受邀请后加入
- [x] 仓库权限已配置：guardian-team → hl-platform/framework write, hl-contracts read
- [x] 仓库权限已配置：infra-team → hl-platform/framework write
- [x] Gate-R 已接受邀请，已加入 guardian-team（2026-04-02）
- [x] PM-A / PM-B GitHub 身份映射已确认
- [x] 已重新发送邀请：PM-A + PM-B 绑定 pm-team，Gate-3 + Infra-A 绑定 infra-team
- [ ] 4 人接受邀请后，自动加入对应 Team

---

> 本文档由 NODE-M (Cowork) 自动生成，依据 TEAM-COLLABORATION-SPEC v1.3 + GitHub API 数据。
