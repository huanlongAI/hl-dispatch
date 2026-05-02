# 新美业 AI App P0 治理裁决：创始人建设范围与团队合并流程边界

**文档编号**：NEW-BEAUTY-AI-P0-GOVERNANCE-RULING
**版本**：v0.1
**状态**：🔒 LOCKED
**日期**：2026-05-02
**裁决人**：L0-Founder（创始人）· Cowork 对话信道
**执行记录节点**：NODE-M / air-codex-cso
**适用范围**：新美业 AI 老板总助 App P0 / P0.5，`hl-scene-app`，`hl-dispatch`

**关联证据**：
- `hl-scene-app` Issue #9：P0.5 建立 LLM 调用边界 seam
- `hl-scene-app` PR #10：`feat: add P0.5 LLM boundary seam`
- PR #10 head：`8499546add597fb727fffb322ef854dadf38a773`
- PR #10 merged commit：`de7b20ec070b950efdee8d79281bd147438a55ec`
- Founder 裁决留痕：https://github.com/huanlongAI/hl-scene-app/pull/10#issuecomment-4362747160

---

## 1. 问题背景

P0.5 工程任务在 `hl-scene-app` 落库时，PR #10 遇到分支保护阻断：

- 普通 merge 被仓库策略拒绝：不允许 merge commits。
- squash merge 被分支保护拒绝：要求至少 1 个具备写权限的非作者 approval。
- PR 作者与当前执行账号同为创始人账号，GitHub 不允许 approve own PR。

经复核，PR #10 的内容是新美业 AI App 创始人建设范围内的 P0.5 App 层 LLM 边界 seam，不是能力包团队交付，也不涉及真实门店数据、能力包业务系统读写或团队成员负责的产品线落库。

因此，阻断根因不是代码不兼容、版本号不一致或 CI 失败，而是仓库级保护规则把“团队合并流程”误套到了创始人建设阶段。

## 2. 裁决结论

### 2.1 创始人建设范围

当任务仍处于新美业 AI App 的创始人建设范围阶段时，不启动团队合并流程，也不要求“另一个人”介入审批或合并。

该范围包括但不限于：

- P0 / P0.5 App shell、导航、占位页和 UI 壳。
- LLM 调用边界 seam、stub gateway、角色入口、场景路由、合规守门人。
- Prompt Registry、Eval Set、合成数据测试和权限禁区扫描。
- `hl-scene-design-system` Flutter adapter 的消费与页面映射。
- 不读取真实门店经营系统、不调用能力包真实业务接口的产品基线建设。

### 2.2 能力包团队流程触发条件

当能力包任务涉及 `hl-scene-app` 落库时，才启动团队合并流程。

触发信号包括但不限于：

- App 代码开始读取或写入能力包提供的真实业务数据。
- App 接入门店系统、预约、客户、排班、库存、营销、支付、财务等能力包接口。
- 任务改变能力包契约、reason_code、OpenAPI、业务事实或验收语义。
- 任务由 PM / 能力包产线责任人发起，并要求对应产品线签收。
- 任务涉及真实租户、真实用户数据、生产数据出境或生产执行闭环。

触发后，任务卡必须显式声明：

| 字段 | 要求 |
|---|---|
| `scope_classification` | `capability_pack_landing` 或 `mixed` |
| `merge_flow_required` | `true` |
| `business_owner` | 对应 PM / 产线责任人 |
| `technical_owner` | 对应工程执行节点 |
| `audit_owner` | NODE-R 或授权审计官 |
| `acceptance_evidence` | CI、源码审计、业务验收和合规证据 |

### 2.3 门禁不放松

创始人建设范围不要求他人审批，但不等于无门禁。

以下要求保持不变：

- 必须保留 GitHub Issue / PR / commit / comment 证据链。
- 必须保留 CI 与治理门禁；`governance-gate` 不得被绕过。
- 涉及工程落库时必须有源码级确认和可复跑验证。
- NODE-M 不得把自身判断伪装成 NODE-R / 大辉子等异源审计结论。
- 关键环节仍可按需派发 NODE-R 只读复审；大辉子作为独立评审和关键环节审计，不默认触发。

## 3. 分支保护处置

为落实本裁决，`hl-scene-app/main` 分支保护调整为：

| 项 | 调整后 |
|---|---|
| `required_approving_review_count` | `0` |
| `require_code_owner_reviews` | `false` |
| `require_last_push_approval` | `false` |
| `required_status_checks.strict` | `true` |
| required check | `governance-gate` |

能力包任务的团队合并要求不再通过全局“至少 1 个 reviewer approval”粗粒度实现，而通过任务卡 `scope_classification` 与 `merge_flow_required` 显式触发。

## 4. PR #10 落库结论

PR #10 已按本裁决完成 squash 合并：

- 合并时间：2026-05-02
- 合并 commit：`de7b20ec070b950efdee8d79281bd147438a55ec`
- 合并前证据：
  - `governance-gate` 通过。
  - `sentinel / 一致性检查` 通过。
  - `flutter analyze --no-pub` 通过。
  - `flutter test --no-pub` 20/20 通过。
  - `scripts/gate-local.sh` 通过。
  - NODE-M 源码级确认已留痕。
  - NODE-R 只读复审结论：PASS_WITH_CONCERNS，未发现 P0 blocker。

合并后观察项：

- `main` 合并后 `Consistency Sentinel` 已成功。
- `main` push 未重复生成 `governance-gate` 检查，列入 24h 观察，不影响本次合并前门禁证据。

## 5. 禁区保持

本裁决不改变新美业 AI App P0 / P0.5 禁区：

- 禁止使用光合设计系统，必须使用 `hl-scene-design-system`。
- 禁止真实门店数据、真实用户数据出境。
- 禁止智能眼镜、录音卡、持续录音、后台录音进入 P0。
- 禁止自主执行、自动群发、自动修改门店系统。
- 禁止医疗诊断、治疗建议、处方、疗效承诺。
- 禁止绕过 `hl-scene-design-system` 主线依赖。

## 6. 后续任务卡默认判定

后续新美业 AI App 任务卡默认先做以下判断：

| 判定问题 | `yes` 处理 |
|---|---|
| 是否只是创始人建设范围内的 App 基线、壳、LLM seam、提示词、Eval、UI 映射？ | 不启动团队合并流程；保留 CI、审计和证据链 |
| 是否接入或修改能力包真实业务数据、接口、契约、reason_code 或产品线验收语义？ | 启动团队合并流程 |
| 是否混合两类范围？ | 拆分任务；不能拆分时按能力包团队流程处理 |
| 是否触达医疗、真实数据出境、后台录音、自主执行等禁区？ | 阻断，需 Founder 重新裁决 |

---

## 7. 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-05-02 | v0.1 | 初版。记录创始人建设范围与能力包团队合并流程边界裁决。 |
