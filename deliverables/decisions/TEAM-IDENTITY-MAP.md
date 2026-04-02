# 唤龙团队身份映射表

> 版本：v1.1 | 更新日期：2026-04-02
> 维护人：童正辉（L0）

---

## 核心组（7 人）

| # | 飞书实名 | GitHub 账号 | GitHub 邮箱 | 团队角色 | 环 | GitHub Team |
|---|---------|------------|------------|---------|-----|------------|
| 1 | 童正辉 | `tongzhenghui` | gw.tzh@icloud.com | 创始人 / 架构师 | 裁决层 | `founder-only` |
| 2 | 许久明 | `xujiuming` | 18120580001@163.com | Gate H 守护者 | 守护者环 | `guardian-team` |
| 3 | 曾正龙 | `ZDragonMeta` | ZDragon.Share@gmail.com | Gate R 守护者 | 守护者环 | `guardian-team` |
| 4 | 邹骢 | 待接受邀请 | zoucong121@gmail.com | PM（商品） | 领域环 | `pm-team` |
| 5 | 朱阳 | 待接受邀请 | 644160417@qq.com | PM（交易） | 领域环 | `pm-team` |
| 6 | 魏鹏 | `wp159951` | 767510277@qq.com | 后端基础设施 | 基础设施环 | `infra-team` |
| 7 | 李旭阳 | `LUXBYA` | 790630573@qq.com | 技术验收官（Gate 3） | 基础设施环 | `infra-team` |

## 组织成员（当前）

| GitHub 账号 | 对应飞书实名 | 组织角色 | 状态 |
|-------------|------------|---------|------|
| `tongzhenghui` | 童正辉 | owner | ✅ 已加入 |
| `xujiuming` | 许久明 | member | ✅ 已加入 |

## 待接受邀请（5 人）

| GitHub 账号 | 飞书实名 | 邮箱 | Team | 状态 |
|-------------|---------|------|------|------|
| — | 邹骢 | zoucong121@gmail.com | `pm-team` | ✉️ 待接受 |
| — | 朱阳 | 644160417@qq.com | `pm-team` | ✉️ 待接受 |
| `LUXBYA` | 李旭阳 | 790630573@qq.com | `infra-team` | ✉️ 待接受 |
| `ZDragonMeta` | 曾正龙 | ZDragon.Share@gmail.com | `guardian-team` | ✉️ 待接受 |
| `wp159951` | 魏鹏 | 767510277@qq.com | `infra-team` | ✉️ 待接受 |

## 飞书群成员映射

| 飞书群 | 成员 |
|--------|------|
| #唤龙-工程通知 | 童正辉、许久明、曾正龙、邹骢、朱阳、魏鹏、李旭阳 |
| #唤龙-任务协同 | 童正辉、许久明、曾正龙、邹骢、朱阳、魏鹏、李旭阳 |
| #唤龙-PM工作台 | 童正辉、邹骢、朱阳、李旭阳 |
| #唤龙-创始人指挥台 | 童正辉 |

## GitHub Team 权限矩阵

| Team | hl-contracts | hl-platform | hl-framework | hl-dispatch | hl-console-native | hl-factory |
|------|-------------|-------------|--------------|-------------|-------------------|------------|
| `founder-only` | admin | admin | admin | admin | admin | admin |
| `pm-team` | **write** | read | — | read | — | — |
| `guardian-team` | read | **write** | **write** | — | — | — |
| `infra-team` | — | **write** | **write** | — | — | — |

## 操作记录

- [x] LUXBYA 确认为李旭阳（非魏鹏）
- [x] 收集全部 7 人 GitHub 账号 + 邮箱
- [x] GitHub 组织席位 4 → 7（2026-04-02）
- [x] 5 人邀请已发送（邹骢、朱阳、李旭阳、曾正龙、魏鹏）
- [x] 创建 `guardian-team`（id: 16914137）— 许久明已加入，曾正龙待接受邀请后加入
- [x] 创建 `infra-team`（id: 16914138）— 魏鹏、李旭阳待接受邀请后加入
- [x] 仓库权限已配置：guardian-team → hl-platform/framework write, hl-contracts read
- [x] 仓库权限已配置：infra-team → hl-platform/framework write
- [ ] 5 人接受邀请后，将其加入对应 Team

---

> 本文档由 NODE-M (Cowork) 自动生成，依据 TEAM-COLLABORATION-SPEC v1.3 + GitHub API 数据。
