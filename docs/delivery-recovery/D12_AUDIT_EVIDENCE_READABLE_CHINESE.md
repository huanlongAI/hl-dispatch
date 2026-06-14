# D12 可读性正样本验证

## 中文摘要

本文档用于验证 D-12 PR 文档中文可读性检查在 audit 模式下不会误伤合规中文治理文档。
它只作为 Gate Issue #257 的远端证据样本，不计划合入 main。
文档包含中文摘要和术语说明，并使用中文解释治理边界、证据来源、运行结果和回滚方式。

## 术语说明

- D-12：PR 文档中文可读性检查，作为 Sentinel 的确定性子检查运行。
- audit：审计模式，只报告扫描结果，不阻断合并。
- enforce：执行模式，发现违反规则时阻断 `sentinel / 一致性检查`。
- scanned_files：本次 PR diff 中实际被 D-12 扫描的 Markdown 文件列表。
- violations：D-12 发现的可读性问题，例如缺少中文正文、缺少中文摘要或缺少术语说明。

## 验证目标

这个正样本文档用于证明 D-12 能扫描 `docs/**/*.md` 范围内的 Markdown，
同时在文档具备中文摘要、术语说明和足够中文正文时保持 `violations` 为空。
这能补齐从 audit 切换到 enforce 前的误报风险证据。

## 预期结果

远端 PR 运行后，D-12 应输出 `mode=audit`、`passed=true`、`skipped=false`。
`scanned_files` 应包含本文档路径，`metrics` 应显示中文字符数量大于零，
`missing_required_sections` 应为空，`violations` 应为空。

## 收尾说明

该 PR 只用于采集远端 CI 证据。证据写回 Gate Issue #257 后，应关闭 PR，
不得将该验证文件合入 main。
