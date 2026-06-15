# hl-dispatch — Codex Entry

本文件是 Codex 入口。完整项目规则见 `CLAUDE.md`；若与上级 tzhOS / AUM / team-memory 真源冲突，以当前真源和任务契约为准。

## 执行约束

- 先执行 Repo Sync 预检；dirty、diverged、behind dirty 时先报告。
- 唤龙领域 Write-Owner 为 `NODE-E`；`NODE-M` 仅按受控写入、验证门禁、branch protection 与明确 push 确认执行。
- GitHub Issue / PR / repo file 是任务与反馈 SSOT；飞书、Project、Base 均为 projection。
- 修改本仓 Agent 入口或投影规则后，运行 Sentinel D-10 / AGENTS 治理漂移检查。

## 当前入口纪律

- 每条推进线只能有一个当前执行入口；HPRD、PM 评审和受限实现优先在同一入口连续推进，不默认新开 Issue / taskbook / PR。
- GitHub 写入前必须先确认：是否推进真实状态；是否会新增入口；是否只是状态刷新、反链、reconciliation 或旧治理回填。若只是解释或刷新，不写入。
- 禁止把 `继续` 理解为继续发评论、继续建入口、继续补总账；默认先只读核实状态，再报告唯一下一步。
- 禁止主动回填 M1-M5、旧 Issue reconciliation、历史总账同步或流程噪音；除非 Founder 明确裁决要求。
- 飞书只在 Founder 明确要求催办或通知时发送；飞书送达、已读、完成或评论不得作为 GitHub 状态真源。
- 必须区分 PM readiness、HPRD、PM HPRD pass、工程实现、runtime 授权；不得把 Issue 指派、taskbook 合并、CI green、PR review、Feishu 投影解释成 runtime 或生产授权。
- ServiceOrder 当前执行入口为 `hl-dispatch#267`；不得为同一 ServiceOrder HPRD 再新开 HPRD Issue 或新 taskbook，除非 Founder 另行裁决。
