# HL Progress Governance Loop Taskbook v0.1

日期：2026-06-12

状态：ACTIVE_GOAL_DISPATCH

Owner：大辉子 / `NODE-E`

任务类型：Engineering progress governance / AI-friendly task management workflow

GitHub SSOT：

- Progress governance contract: `docs/delivery-recovery/HL_PROGRESS_GOVERNANCE_LOOP_v0.1.md`
- Existing recovery contract: `docs/delivery-recovery/DELIVERY_RECOVERY_IMPLEMENTATION_CONTRACT_v0.1.md`
- Existing action projection helper: `docs/delivery-recovery/ACTION_PROJECTION_EXPORTER_v0.1.md`
- Existing Feishu / GitHub collaboration baseline: `deliverables/decisions/FEISHU-GITHUB-COLLABORATION-SPEC-v1.0.md`
- Founder instruction: 2026-06-12 当前 Cowork 线程同意建议方案，并要求转化为追求目标模式的长程闭环任务。

## 1. 任务定位

本 taskbook 将“GitHub SSOT + 飞书多维表格投影 + `hl-progress` 轻量 AI 适配层”的方案转化为 Huanlong 可执行的长程闭环任务。

本任务不是新项目管理 SaaS 采购任务，不是自建完整任务平台，不是 Feishu-first 流程，不是生产授权，不改变 route / mode / 权限。

## 2. 目标

在 hl-dispatch 建立工程项目与任务进度治理闭环，使大辉子可以围绕 GitHub SSOT 持续跟踪：

- Huanlong taskbook
- PR
- gap_report
- gate
- evidence
- owner
- blocker
- Founder decision-required state

输出必须能被 AI 低摩擦读取、汇总、验证和投影，同时让 Founder / PM / 工程成员通过飞书多维表格或报告看到可扫描进度。

## 3. Scope In

允许做：

- 固化 `hl-progress` 目标、数据模型、状态机、投影规则和阶段门禁。
- 将现有 `action-projection:v0.1` 作为 P1 read-only exporter 的参考基线。
- 建立 `hl-progress-work-item:v0.1` 最小字段模型。
- 设计 GitHub -> JSON / Markdown -> Feishu Bitable 的一向投影路径。
- 为后续 read-only exporter、Founder packet、Bitable projection 建立 Work Unit。
- 在计划内对 Green docs / read-only tooling PR 做验证、push、PR、merge。

## 4. Scope Out

禁止做：

- 修改 route / mode / role / registry / profile / branch protection。
- 直接 push 到 `main`。
- 把 Feishu / Bitable / dashboard / chat summary 当作事实源或完成证据。
- 让 Bitable 写回 GitHub，除非另有 Founder / Gate GitHub SSOT。
- 接入 secrets、生产数据、真实用户数据、支付、计费、退款、结算、provider、deploy、release。
- 替代 PM 业务语义 Owner。
- 替代 Founder 最终裁决权。
- 让大辉子最终审计自身主导的重大架构。

## 5. Long-Running Goal Loop

```yaml
goal_mode:
  name: hl-progress-governance-loop
  owner: dahuizi
  fact_source: github
  projection_targets:
    - markdown
    - json
    - feishu_bitable_after_separate_projection_gate
  cadence:
    daily:
      - scan_github_deltas
      - normalize_work_items
      - surface_blockers
      - surface_stale_items
      - surface_decision_required_items
    weekly:
      - founder_packet
      - accepted_evidence_rollup
      - next_green_yellow_red_work_units
  hard_rules:
    - No Evidence, No Done
    - No Action, No Notification
    - No Context, No AI Guess
    - GitHub SSOT before projection
```

## 6. Phase Plan

| Phase | Status | Output | Owner | Gate |
|-------|--------|--------|-------|------|
| P0 | active | Contract, taskbook, README index. | 大辉子 | Docs verification + PR merge. |
| P1 | next | Read-only `hl-progress` exporter design and implementation. | 大辉子 / engineering agent | Offline deterministic tests. |
| P2 | planned | Feishu Bitable projection mapping and dry-run ledger. | 大辉子 + Founder / Feishu operator | Separate Feishu projection gate. |
| P3 | gated | Controlled GitHub writeback proposal. | 大辉子 + Gate | Separate Founder / Gate SSOT. |
| P4 | optional | External SaaS adapter assessment, if GitHub + Bitable is insufficient. | 大辉子 | Separate tool decision. |

## 7. First Work Units

### HLPROG-P0-WU1：闭环契约落地

Risk：Green

Output：

- `docs/delivery-recovery/HL_PROGRESS_GOVERNANCE_LOOP_v0.1.md`
- `deliverables/tasks/HL-PROGRESS-GOVERNANCE-LOOP-TASKBOOK-2026-06-12-v0.1.md`
- `docs/delivery-recovery/README.md` index update

Acceptance：

- 文件明确 GitHub SSOT、Feishu Bitable projection、`hl-progress` read-only first。
- 文件明确不改 route / mode / 权限 / branch protection / production。
- 本地验证命令通过。
- PR 合并后成为 GitHub SSOT。

### HLPROG-P1-WU1：read-only exporter 对齐设计

Risk：Green

Output：

- 将现有 `scripts/export-action-projection.py` 能力映射到 `hl-progress-work-item:v0.1`。
- 设计输入：GitHub Issues / PRs / repo files。
- 设计输出：JSON + Markdown Founder packet。

Acceptance：

- 不写 GitHub。
- 不写 Feishu。
- 不需要 secrets。
- 缺字段输出 `unknown` 和 `warnings`，不靠 AI 猜测补齐。

### HLPROG-P1-WU2：Founder packet fixture

Risk：Green

Output：

- 离线 fixture。
- 生成 active / blocked / decision-required / review-waiting / accepted evidence 汇总。

Acceptance：

- deterministic test。
- 输出包含 GitHub source URL。
- 无 source URL 的行必须带 warning。

### HLPROG-P2-WU1：Feishu Bitable 投影设计

Risk：Yellow

Output：

- Bitable 字段映射。
- dry-run ledger。
- projection-only 文案。

Acceptance：

- 需要单独 Feishu projection gate。
- 一向 GitHub -> Bitable。
- 不允许 Bitable 作为验收证据。

## 8. Verification Plan

P0 验证：

```bash
git diff --check
python3 scripts/test-action-projection-exporter.py
rg -n "HL Progress|hl-progress|GitHub SSOT|Feishu Bitable|No Evidence, No Done|route / mode|branch protection" docs/delivery-recovery/HL_PROGRESS_GOVERNANCE_LOOP_v0.1.md deliverables/tasks/HL-PROGRESS-GOVERNANCE-LOOP-TASKBOOK-2026-06-12-v0.1.md docs/delivery-recovery/README.md
```

P1 验证：

```bash
python3 scripts/test-action-projection-exporter.py
python3 scripts/export-action-projection.py --input <fixture> --generated-at <fixed timestamp>
```

P2 验证：

```bash
# dry-run only until a separate Feishu projection gate exists
hl-progress bitable --dry-run --input <projection.json>
```

## 9. Done Definition

This taskbook is done only when:

- P0 PR is merged.
- Verification evidence is recorded.
- No permission / route / mode / branch-protection expansion appears in the diff.
- Next P1 issue or PR path is clear from GitHub SSOT.

P1 / P2 / P3 are separate follow-on work units and must not be reported as done by this P0 task.
