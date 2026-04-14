# Phase F-0 飞书建群操作清单

> 执行人：创始人（L0-Founder）
> 预计耗时：~30 分钟
> 前置：FEISHU-GITHUB-COLLABORATION-SPEC v1.0 LOCKED（D-1~D-6 已裁决）
> 日期：2026-03-30

---

## 第一步：创建 4 个飞书群

在飞书 App 中依次创建以下群聊：

### 1.1 工程通知通道

- **群类型**：内部群
- **群名**：工程通知通道
- **群描述**：GitHub PR / Issue / CI 事件自动推送。只读为主，讨论请移步任务协同通道。
- **邀请成员**（核心组全员 7 人）：

| 成员代号 | 角色 | 联系方式 |
|----------|------|---------|
| L0-Founder | 创始人 | （你自己） |
| Gate-H | Gate H 架构守护者 | 内部通讯录搜索 |
| Gate-R | Gate R 运维守护者 | 内部通讯录搜索 |
| PM-Ops | PM 项目管理 | 内部通讯录搜索 |
| PM-A | PM 产品 | 内部通讯录搜索 |
| Gate-3 | 技术验收官 | 内部通讯录搜索 |
| Infra-A | 后端基础设施 | 内部通讯录搜索 |

- **验证**：群成员 = 7 人 ✅

### 1.2 任务协同通道

- **群名**：任务协同通道
- **群描述**：任务讨论、进度同步、即时沟通。讨论结论 24h 内写入 GitHub Issue/PR。
- **邀请成员**：与工程通知通道相同（核心组全员 7 人）
- **验证**：群成员 = 7 人 ✅

### 1.3 PM 工作台通道

- **群名**：PM 工作台通道
- **群描述**：PM 规格讨论、Cap-Spec 审查、业务问题。正式裁决走 GitHub Issue。
- **邀请成员**（4 人）：

| 成员代号 | 角色 |
|----------|------|
| L0-Founder | 创始人 |
| PM-A | PM 产品 |
| PM-Ops | PM 项目管理 |
| Gate-3 | 技术验收官 |

- **验证**：群成员 = 4 人 ✅
- **备注**：PM-B 入组后加入此通道

### 1.4 指挥台通道

- **群名**：指挥台通道
- **群描述**：全局状态汇总、审批提醒、关键指标。仅创始人。
- **邀请成员**：仅 L0-Founder（1 人）
- **验证**：群成员 = 1 人 ✅

---

## 第二步：每个群添加 Custom Bot

在每个群中添加自定义 Bot，用于接收 GitHub Webhook 通知。

### 操作路径

```
群聊 → 右上角 ··· → 设置 → 群机器人 → 添加机器人 → 自定义机器人
```

### 逐群操作

| # | 群名 | Bot 名称 | 签名校验 |
|---|------|---------|---------|
| 1 | 工程通知通道 | GitHub-工程通知 | 开启（记录密钥） |
| 2 | 任务协同通道 | GitHub-任务协同 | 开启（记录密钥） |
| 3 | PM 工作台通道 | GitHub-PM通知 | 开启（记录密钥） |
| 4 | 指挥台通道 | GitHub-指挥台 | 开启（记录密钥） |

### 每个 Bot 创建后记录

```
群：工程通知通道
Webhook URL: https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx
签名密钥: xxxxxxxx

群：任务协同通道
Webhook URL: https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx
签名密钥: xxxxxxxx

群：PM 工作台通道
Webhook URL: https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx
签名密钥: xxxxxxxx

群：指挥台通道
Webhook URL: https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx
签名密钥: xxxxxxxx
```

> ⚠️ 将以上 4 组 URL + 密钥保存到安全位置（如 1Password / 本地加密备忘录）。Phase F-1 配置 GitHub Webhook 时需要。

---

## 第三步：发布群公告

在每个群发一条置顶消息，说明群的用途和规范。

### 工程通知通道公告模板

```
📢 群公告

本群用途：GitHub 工程事件自动推送（PR / Issue / CI）
规范：
1. Bot 自动推送，人类一般不在此讨论
2. 需要讨论的事项请移步任务协同通道
3. 每周一创始人发布本周目标

详见：FEISHU-GITHUB-COLLABORATION-SPEC v1.0
```

### 任务协同通道公告模板

```
📢 群公告

本群用途：任务讨论、进度同步、即时沟通
核心铁律：
1. 飞书讨论产出结论 → 24h 内写入 GitHub Issue/PR
2. 关联 GitHub 事项时必须附链接
3. 裁决请求必须走 GitHub Issue（[decision-request] 标签）

详见：FEISHU-GITHUB-COLLABORATION-SPEC v1.0
```

### PM 工作台通道公告模板

```
📢 群公告

本群用途：PM 规格讨论、Cap-Spec 审查、业务问题预沟通
规范：
1. 正式裁决走 GitHub Issue，飞书口头同意不算
2. Cap-Spec PR 提交后本群自动通知
3. 技术验收官在此反馈代码 PR 问题

参考：PM-PRACTICAL-HANDBOOK v1.0 §9
```

### 指挥台通道公告模板

```
📢 个人指挥台

用途：全局状态汇总 + 审批提醒
- 待审批 PR/Issue 自动推送
- decision-request 自动 @
- Bitable 仪表盘入口（F-2 后配置）
```

---

## 第四步：验证清单

完成所有操作后，逐项打勾确认：

```
□ 4 个群全部创建完成
□ 工程通知通道成员 = 7 人
□ 任务协同通道成员 = 7 人
□ PM 工作台通道成员 = 4 人（含 L0-Founder + PM-A + PM-Ops + Gate-3）
□ 指挥台通道成员 = 1 人
□ 4 个 Custom Bot 已添加，Webhook URL 已保存
□ 4 个群公告已发布并置顶
□ 向团队发消息：飞书群已建好，请查看群公告了解用途
```

---

## 完成后下一步

- **Phase F-1**（~30 分钟）：配置 GitHub Webhook → 飞书 Bot，实现自动通知
- **Phase F-2**（~2 小时）：建立 Bitable 项目看板，录入初始数据

---

> 本清单对应 FEISHU-GITHUB-COLLABORATION-SPEC v1.0 §7 Phase F-0。
