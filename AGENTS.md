# hl-dispatch — Codex Entry

本文件是 Codex 入口。完整项目规则见 `CLAUDE.md`；若与上级 tzhOS / AUM / team-memory 真源冲突，以当前真源和任务契约为准。

## 执行约束

- 先执行 Repo Sync 预检；dirty、diverged、behind dirty 时先报告。
- 唤龙领域 Write-Owner 为 `NODE-E`；`NODE-M` 仅按受控写入、验证门禁、branch protection 与明确 push 确认执行。
- GitHub Issue / PR / repo file 是任务与反馈 SSOT；飞书、Project、Base 均为 projection。
- 执行 `gh issue create`、`gh issue comment` 或 `gh issue edit` 前，必须先用 `scripts/preflight-github-language-write.py` 对即将写入的标题/正文/评论做本地中文门禁；失败时禁止写入 GitHub。
- 修改本仓 Agent 入口或投影规则后，运行 Sentinel D-10 / AGENTS 治理漂移检查。

## 当前入口纪律

- 每条推进线只能有一个当前执行入口；HPRD、PM 评审和受限实现优先在同一入口连续推进，不默认新开 Issue / taskbook / PR。
- GitHub 写入前必须先确认：是否推进真实状态；是否会新增入口；是否只是状态刷新、反链、reconciliation 或旧治理回填。若只是解释或刷新，不写入。
- 禁止把 `继续` 理解为继续发评论、继续建入口、继续补总账；默认先只读核实状态，再报告唯一下一步。
- 禁止主动回填 M1-M5、旧 Issue reconciliation、历史总账同步或流程噪音；除非 Founder 明确裁决要求。
- 飞书只在 Founder 明确要求催办或通知时发送；飞书送达、已读、完成或评论不得作为 GitHub 状态真源。
- Huanlong GitHub SSOT 下的 owner / DRI / verifier / evidence 飞书私聊催办，必须先使用 `hl-owner-confirmation-dispatch` 做 route / dry-run 投影预检，再使用 `scripts/feishu-direct-message.rb` dry-run 和 `--execute` 发送；不得直接裸调 `lark-cli im +messages-send`。
- 必须区分 PM readiness、工程理解确认（legacy: HPRD）、PM understanding pass（legacy: PM HPRD pass）、工程实现、runtime 授权；不得把 Issue 指派、taskbook 合并、CI green、PR review、Feishu 投影解释成 runtime 或生产授权。
- ServiceOrder 当前执行入口为 `hl-dispatch#267`；不得为同一 ServiceOrder 工程理解确认再新开 HPRD Issue 或新 taskbook，除非 Founder 另行裁决。

## HPRD-lite 纪律

- Founder 于 2026-06-15 选择 `A`：废弃旧 HPRD 独立环节形态；旧 HPRD 模板仅可作为检查清单参考，不再作为默认独立 Issue、独立 taskbook、独立文档交付或治理回填要求。
- 当前执行口径中，HPRD 的可执行形态是同一 GitHub 入口内的轻量 `工程理解确认` / `Implementation Readiness`，用于确认工程 owner 是否读懂 PM 业务语义；它不是第二份 PRD，不是技术设计，不是 runtime / production / active contract 授权。
- PM-led capability 需要工程理解确认时，必须写在当前唯一入口内，至少包含：本轮做什么、本轮不做什么、DDD / SDD 对齐、验收与测试证据计划、需要 PM / Founder / Gate 裁决的问题。
- PM 审工程理解确认时，只回复三类结论：`通过`、`需修正`、`需 Founder/Gate 裁决`。通过只表示业务理解可接受，进入签定边界内的受限实现；不得解释为生产运行态、生效契约注册、真实用户数据、deploy 或 release 授权。
- HK 总任务书或已有明确工程 PR / merge evidence 的主线，不额外补 HPRD；只看实现证据、测试证据、Gate / 人工交叉验收和 Founder acceptance。
