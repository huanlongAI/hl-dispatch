# 微信小程序技术决策派生 — UniApp runtime v1

**文档编号**：DD-FE-MINIPROGRAM  
**版本**：v1.0（2026-04-28 裁决归档）  
**裁决人**：L0-Founder（创始人 · Codex 对话信道）  
**状态**：LOCKED — 承接 R-036 amend-002 / R-052 amend-001 / R-FE-CLIENT-001 amend-002  
**关联**：
- 上位真源：`hl-contracts/governance/RULINGS.md`
- 设计系统：`huanlongAI/hl-scene-design-system`
- 伴随 runtime：DD-FE-CLIENT v1.1（原生 App runtime · Flutter）

> 术语：本文档中的"微信小程序 runtime"属于 S 域场景前端，不属于 C 域治理客户端；它服务 C 端消费者轻入口，但治理域归 S-L4。

---

## §1. 裁决摘要

微信小程序开发技术选型锁定为 **UniApp + Vue 3 + TypeScript** 路线。该 runtime 与 Flutter 原生 App runtime 分治，但共享：

- `hl-contracts` 契约法典与 HK.Audit trace 纪律
- `hl-scene-design-system/packages/token-core/` 设计 token
- `hl-scene-design-system/docs/design-system/` 组件语义与使用规范

UniApp 组件源码应纳入 `hl-scene-design-system/packages/uniapp/rdesign_uniapp/` 管理维护，不得放入 `hl-scene-app` 或能力包业务仓作为私有组件。

---

## §2. 13 项技术字段

| # | 字段 | 锁定值 | 退出/修订条件 |
|---|---|---|---|
| 1 | 语言 | TypeScript | TS 主版本破坏性升级触发 v1.x amend |
| 2 | 框架 | UniApp + Vue 3 | UniApp 编译链无法稳定产出微信小程序，触发 v2 重评 |
| 3 | UI runtime | `hl-scene-design-system/packages/uniapp/rdesign_uniapp/` | 不得自建业务私有 DS |
| 4 | 状态管理 | Pinia（小程序轻量状态） | 状态复杂度超过单包边界，触发字段 amend |
| 5 | 路由 | UniApp pages + typed route manifest | 分包 / 深链路无法覆盖业务，触发字段 amend |
| 6 | 网络 | `uni.request` 封装 + OpenAPI 生成类型 | 必须统一注入 auth、trace_id；禁止自造审计 header |
| 7 | 本地存储 | `uni.setStorage` 封装 + 微信安全存储能力 | token / 敏感值不得明文散落 |
| 8 | OpenAPI 代码生成 | 从 hl-contracts OpenAPI YAML 生成 TS 类型 | 生成器细节可 v1.x amend |
| 9 | 单元测试 | Vitest | 覆盖 token transform 与纯函数逻辑 |
| 10 | 小程序集成 smoke | 微信开发者工具 CLI / miniprogram-ci | 不能接入时先以 build smoke 代替，并登记缺口 |
| 11 | Lint | ESLint + TypeScript strict | 关闭 strict 需创始人批准 |
| 12 | 可观测性 | trace_id 透传到 S 域 Gateway / HK.Audit 链路 | 不得在前端签发 event_id |
| 13 | 认证 | 复用 DD-AUTH v1 Bearer/OIDC 语义；小程序登录桥接另走后续 auth amend | 微信登录与平台 identity 绑定需独立 Cap-Spec |

---

## §3. 设计系统接入纪律

`hl-scene-design-system` 必须按以下结构落地：

```text
hl-scene-design-system/
├── packages/
│   ├── token-core/
│   ├── flutter/rdesign_component/
│   └── uniapp/rdesign_uniapp/
├── docs/design-system/
├── AGENTS.md
├── REPO-LAYOUT.md
└── .github/gate-policy.yaml
```

硬约束：

- UniApp adapter 只消费 `token-core`，不得反写 token。
- 组件必须登记 parity matrix：Flutter 与 UniApp 的组件名、状态、变体、缺口、截图证据。
- PR 必须按 runtime 拆分：治理骨架、token-core、Flutter adapter、UniApp adapter 分阶段提交。
- UniApp 组件不得夹带业务能力包逻辑、接口业务封装、鉴权流程实现。

---

## §4. SLO 与验收

| 指标 | 阈值 | 度量 |
|---|---|---|
| 小程序冷启动首屏 | P95 ≤ 2s | 微信开发者工具 + 真机抽测 |
| 主路径交互帧稳定性 | 无明显掉帧 / 卡顿 | 真机抽测 + 后续 APM |
| 构建绿线 | `npm run lint && npm run build:mp-weixin` | CI |
| token drift | 0 drift | token drift check |
| 组件 parity | 核心 12 组件必须登记 | PARITY-MATRIX.md |

---

## §5. 退出条件

以下任一条件触发 DD-FE-MINIPROGRAM v2 重评：

1. UniApp 微信小程序编译链在目标业务范围内无法稳定交付。
2. 微信审核规则导致当前技术路线无法满足上架/发布纪律。
3. token-core + UniApp adapter 无法保持组件 parity，且差异影响核心体验。
4. 微信原生小程序或 Taro 等替代方案在 AI 编码效率、维护成本、生态稳定性上出现明显优势，并经创始人裁决。

---

## §6. 变更日志

| 日期 | 版本 | 变更 | 签批 |
|---|---|---|---|
| 2026-04-28 | v1.0 | 初版 · 微信小程序 runtime 锁定 UniApp + Vue 3 + TypeScript；DS 组件源码归入 `hl-scene-design-system/packages/uniapp/rdesign_uniapp/` | L0-Founder cat（Codex 信道 · 明示"批准"） |
