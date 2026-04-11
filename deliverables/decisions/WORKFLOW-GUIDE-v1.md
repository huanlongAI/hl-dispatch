# 唤龙平台流程分流指南

## WORKFLOW-GUIDE v1 — 非能力包流程最小定义

---

**文档编号**：WORKFLOW-GUIDE-001
**版本**：v1.0
**日期**：2026-04-11
**状态**：DRAFT
**文档性质**：TEAM-COLLABORATION-SPEC v2.1 附属文件（§5.1 F-10 声明）
**派生链**：TEAM-COLLAB-SPEC v2.1 R-TEAM-011 / Pilot-Lock 裁决 → 本文档

---

## 1. 定位声明

TEAM-COLLAB-SPEC v2.1 §5.1 完整定义了**能力包流**（Capability Flow）。本文档补齐其余三类变更的最小流程定义，确保团队在 T1 试运行期间遇到非能力包变更时有章可循。

**本文档不是完整制度**——它是试运行期间的最小可用流程。T1 试运行结束后，基于实际数据评估是否升级为正式流程或合并回 TEAM-COLLAB-SPEC v2.2。

---

## 2. 流程分类总览

每个 PR 必须通过 PR 分类字段（TEAM-COLLAB-SPEC v2.1 §5.3）声明 `change_class`：

| change_class | 走哪个流程 | 定义文档 |
|-------------|-----------|---------|
| `capability` | 能力包流 | TEAM-COLLAB-SPEC v2.1 §5.1 |
| `bugfix` | Bugfix 流 | 本文档 §3 |
| `tech-improvement` | 技术改动流 | 本文档 §4 |
| `governance` | 治理/内核流 | 本文档 §5 |

**分类原则**：如果不确定归哪类，默认走 `capability`（更严格、更安全）。

---

## 3. Bugfix 流

### 3.1 适用范围

已上线功能的缺陷修复。不引入新的业务语义、不变更 Cap-Spec、不触碰契约核心路径。

### 3.2 最小流程

```
报告 Bug（QA / PM / 运维 / 用户）
  │
  ├── 判定严重级别（P0 紧急 / P1 高 / P2 中 / P3 低）
  │
  ├── P0 紧急：
  │     工程师直接修复 → 最小 review（1 名工程师）→ CI L1-L3 全绿
  │     → qa-verdict = PASS → merge → 立即发布
  │     → 事后补 Root Cause Analysis
  │
  └── P1-P3 常规：
        工程师修复 → Draft PR（change_class = bugfix）
        → CI L1-L3 全绿 → qa-verdict = PASS
        → code owner review → merge
        → 跟随下一次常规发布
```

### 3.3 与能力包流的差异

| 环节 | 能力包流 | Bugfix 流 |
|------|---------|----------|
| Cap-Spec | 必须 | 不需要 |
| HPRD | 必须 + pm-hprd-pass | 不需要 |
| design.md | 需要 | P0 免除，P1-P3 可选 |
| pm-acceptance | 必须 | P0 事后补，P1-P3 QA 代行 |
| qa-verdict | 必须 | **必须**（不可免除） |
| CI L1-L3 | 必须 | **必须**（不可免除） |
| 创始人审批 | 仅 contract_touch | 仅 kernel/gateway 路径变更 |

### 3.4 防滥用规则

- Bugfix PR 不得引入新 API、新 reason_code、新事件 schema。如果修复需要变更这些，升级为 `capability` 流。
- 单个 Bugfix PR 不得超过 500 行变更（不含测试）。超出说明可能是功能变更伪装成 Bugfix。

---

## 4. 技术改动流

### 4.1 适用范围

不影响业务语义的技术改进：依赖升级、重构、性能优化、基础设施调整、CI 配置变更。

### 4.2 最小流程

```
工程师 / 架构师提出技术改进
  │
  ├── 影响评估：是否触碰 kernel / gateway / framework？
  │     ├── 是 → founder_required = true → 创始人审批
  │     └── 否 → 工程师互审即可
  │
  ├── Draft PR（change_class = tech-improvement）
  │     简要说明改进目的和影响范围（不需要 Cap-Spec / HPRD）
  │
  ├── CI L1-L3 全绿（**必须**，确保不引入回归）
  │
  ├── code owner review
  │
  └── merge → 跟随下一次常规发布
```

### 4.3 与能力包流的差异

| 环节 | 能力包流 | 技术改动流 |
|------|---------|-----------|
| Cap-Spec / HPRD | 必须 | 不需要 |
| pm-acceptance | 必须 | 不需要（不涉及业务语义变更） |
| qa-verdict | 必须 | 仅当改动影响用户可见行为时需要 |
| CI L1-L3 | 必须 | **必须** |
| 创始人审批 | 仅 contract_touch | 仅 kernel/gateway/framework 路径 |

### 4.4 防滥用规则

- 技术改动 PR 不得包含业务逻辑变更。如果同时修改了 `biz-*` 包的业务逻辑，拆分为 capability PR + tech-improvement PR。
- 依赖版本升级涉及 TECH-STACK-SPEC v3 锁定项（Kotlin / Spring Boot / Gradle 等）→ 自动升级为 `governance` 流。

---

## 5. 治理/内核流

### 5.1 适用范围

对 hl-contracts 核心路径、hl-factory 门禁规格、CODEOWNERS/rulesets、kernel/gateway/framework 架构的变更。

### 5.2 最小流程

```
创始人 / 架构师发起治理变更提案
  │
  ├── 创始人审批提案（必须）
  │
  ├── 变更实施
  │     ├── 契约变更 → 更新 hl-contracts 对应路径
  │     ├── 门禁变更 → 更新 hl-factory/specs/ 或 gates/
  │     ├── 内核变更 → 更新 hl-platform/kernel/ 或 gateway/
  │     └── 规则变更 → 更新 CODEOWNERS / rulesets
  │
  ├── CI L1-L3 全绿（**必须**）
  │
  ├── 创始人 code review + approve（**必须**）
  │
  ├── 影响评估：是否影响在进行中的能力包？
  │     ├── 是 → 通知相关 PM + 工程师，评估是否需要回退/调整
  │     └── 否 → 直接 merge
  │
  └── merge → 立即生效（治理变更不等发布窗口）
```

### 5.3 与能力包流的差异

| 环节 | 能力包流 | 治理/内核流 |
|------|---------|-----------|
| 发起人 | PM | 创始人 / 架构师 |
| Cap-Spec / HPRD | 必须 | 不需要 |
| 创始人审批 | 仅 contract_touch | **必须**（全程） |
| pm-acceptance | 必须 | 不需要 |
| qa-verdict | 必须 | 仅当内核变更影响行为性测试时需要 |
| CI L1-L3 | 必须 | **必须** |
| 生效时机 | 跟随发布 | 立即生效 |

---

## 6. 流程误配检测

### 6.1 自动检测规则

以下情况应触发 CI 警告或阻塞：

| 检测项 | 触发条件 | 动作 |
|--------|---------|------|
| Bugfix 包含新 API | `change_class = bugfix` 但 PR 新增了 `@RequestMapping` | ⚠️ 警告：建议升级为 capability |
| Bugfix 超大 | `change_class = bugfix` 但 diff > 500 行 | ⚠️ 警告：检查是否应为 capability |
| Tech 包含业务逻辑 | `change_class = tech-improvement` 但修改了 `biz-*/domain/` | ⚠️ 警告：建议拆分 |
| 缺少分类 | PR body 中未填写 `change_class` | ⛔ BLOCK：必须填写分类 |
| 分类与路径不一致 | `change_class = bugfix` 但修改了 kernel/ 路径 | ⚠️ 警告：建议核实分类 |

### 6.2 人工兜底

自动检测不可能覆盖所有情况。在 T1 试运行期间，创始人每周抽查 PR 分类准确性，采集 Non-Capability Misroute Count 指标（TEAM-COLLAB-SPEC v2.1 §9.2）。

---

## 变更日志

| 日期 | 版本 | 变更内容 |
|------|------|---------|
| 2026-04-11 | v1.0 | 初始版本——Bugfix / 技术改动 / 治理内核三类非能力包流程的最小定义。覆盖流程步骤、与能力包流差异对比、防滥用规则、流程误配检测。由 TEAM-COLLAB-SPEC v2.1 Pilot-Lock 裁决触发。 |
