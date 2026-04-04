# hl-dispatch — AI 编码指引

> **Write-Owner: NODE-A** — MULTI-NODE-COWORK-SPEC v0.3 §3.2
> 跨域写入须遵循 §3.4 Cross-Domain Write Protocol
> 最后修订：2026-04-05

## 仓库定位

hl-dispatch 是唤龙平台的团队协作调度枢纽，负责 Issue 管理、分工手册、决策文档和定时轮询。

## 目录结构

| 路径 | 用途 |
|------|------|
| `deliverables/decisions/` | PM-SPEC、DECISION 等决策文档 |
| `deliverables/specs/` | 能力包规格（Cap-Spec） |
| `.github/ISSUE_TEMPLATE/` | Issue 模板（doc-review / task-assign / decision-request） |

## Label 体系

doc-review / task-assign / decision-request / architect / ops / pm / priority-p0 / priority-p1 / feedback-given / approved / blocked

## 沟通机制

- 飞书通知 → GitHub SSOT（24h 内落库）
- 飞书群：#指挥台（cmd）/ #工程（eng）/ #任务（task）/ #PM工作台（pm）
- 详见 `FEISHU-GITHUB-COLLABORATION-SPEC.md`

## Cowork 行为约定

- 本仓库由 NODE-A 独占写入（Cowork 通过 GitHub MCP 可直写）
- 其他节点如需修改，须通过 GitHub Issue 提案或创始人授权的 `[CROSS-DOMAIN]` commit
- 详见 `tzhOS/40-PPR/MULTI-NODE-COWORK-SPEC.md` §3.4
