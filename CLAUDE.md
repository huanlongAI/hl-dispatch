# hl-dispatch — AI 编码指引

> **Write-Owner: NODE-E** — tzhOS R-0122；当前执行投影以本行声明为准，历史本地投影不得作为依据
> **NODE-M 操作权限**：`NODE-M` 可按 Repo Sync、SSOT、验证门禁、branch protection 与明确 push 确认执行受控写入、push 与 Draft PR；这不改变唤龙领域 Write-Owner = `NODE-E`。
> 跨域写入须遵循 §3.4 Cross-Domain Write Protocol
> 最后修订：2026-05-22

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

## GitHub Issue 中文门禁

- 本仓 GitHub Issue / Comment 面向团队协作，标题、正文和评论必须包含足够简体中文说明；英文术语、命令、路径、字段名和日志可以保留，但不能提交纯英文内容。
- 在执行 `gh issue create`、`gh issue comment` 或 `gh issue edit` 前，必须先把即将写入的标题/正文/评论传给 `scripts/preflight-github-language-write.py` 本地验证。
- 本地 preflight 失败时禁止写入 GitHub；GitHub Actions language gate 是事后检测，不能替代写前检查。
- 结构化负责人 YAML 只有在 `check-github-language-gate.py` 明确允许的格式下可以不含中文；普通 AI 状态同步、投影回写、执行结果和裁决简报不得使用纯英文。
- 普通 Issue / PR 回填正文不得使用裸 `#编号` 指代 GitHub 对象；跨仓库或可能跨仓库的引用必须写成全限定 Markdown 链接，例如 `[huanlongAI/<repo>#<number>](https://github.com/huanlongAI/<repo>/pull/<number>)` 或 `[huanlongAI/<repo>#<number>](https://github.com/huanlongAI/<repo>/issues/<number>)`，避免 GitHub 自动把 `#编号` 解析成本仓同编号 Issue / PR。

## 任务派发防错规则

涉及前端 App / 场景前端构建、云效触发入口、Codeup 同步、构建日志、产物版本、包号或分发入口时，必须先按下面规则判断 Owner：

- 云效流水线可能只是前端 App 构建触发入口，不等于真实构建位置。
- 前端 App / 场景前端真实构建证据（真实构建位置、执行人、输入 commit SHA、构建日志/截图、产物版本/包号、分发入口）派给 Frontend-Lead / 胡杰威，不派给 Gate-R / 曾正龙。
- GitHub main -> Codeup / 云效代码仓同步、同步证据、一致性证明派给 Infra-A / 魏鹏。
- Gate-R / 曾正龙只负责其有权限的运维发布、部署、回滚路径；不要因为任务出现“云效”二字就默认派给运维。
- 人员与飞书 ID 以 `TEAM.yml` 为本仓派发入口，长期记忆与背景证据见 `team-memory` 的 `CLAUDE.md`、`00-index/TEAM-ROSTER.md`、`indexes/INDEX-org-collaboration.md`。
- GitHub SSOT Issue / PR 已存在时，owner、DRI、verifier 或 evidence 的飞书私聊催办必须先走 `hl-owner-confirmation-dispatch` 做 route / dry-run 投影预检，再用 `scripts/feishu-direct-message.rb` 发送；禁止绕过 helper 直接裸调 `lark-cli im +messages-send`。
- 飞书私聊只做提醒投影，不改变 owner/action、confirmation、review 或 evidence 状态；有效回复仍必须回到 GitHub SSOT。

## Cowork 行为约定

- 本仓库领域 Write-Owner 为 NODE-E；NODE-M 可按 Repo Sync、验证门禁、branch protection 与明确 push 确认执行受控写入、push 与 Draft PR
- 其他节点如需修改，须通过 GitHub Issue 提案或创始人授权的 `[CROSS-DOMAIN]` commit
- 详见 `tzhOS/40-PPR/MULTI-NODE-COWORK-SPEC.md` §3.4
