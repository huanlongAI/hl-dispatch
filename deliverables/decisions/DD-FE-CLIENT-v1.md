# 场景前端 App 技术决策派生 — Flutter 3.41 / Dart 3.x 锁定

**文档编号**：DD-FE-CLIENT
**议题编号**：J-A2（场景前端裁决 · M5 组 2）
**版本**：v1.0（2026-04-20 裁决归档）
**裁决人**：L0-Founder（创始人 · cat）· Cowork 对话信道
**接收人**：Gate-H（架构）、前端团队、SRE、QA、PM
**状态**：🔒 LOCKED — 与 R-FE-CLIENT-001 同步入库（R-FE-CLIENT-001 LOCKED + amend-001 已入 `hl-contracts` main · PR #13 + PR #16 · 2026-04-23）
**关联**：
- 上位真源：R-FE-CLIENT-001 LOCKED + amend-001（`hl-contracts/governance/RULINGS.md`）
- 宪法锚：R-060 amend-001 · R-036 amend-001 · R-044 · R-052 · R-016（`hl-contracts/governance/RULINGS.md`）
- SAAC 立宪：SAAC-HL-EP-001 v1.2 amend-001 · §0.3 + P1-FE-1~5（计划中 · 后续 PR · 方案 3）
- 总规：TECH-STACK-SPEC v3.2 §8 amend（计划中 · 后续 PR · 方案 4）
- 推导链：`team-memory/03-approved/decisions/DEC-20260420-002-frontend-flutter-derivation-chain.md`
- BRIDGE 模板：`09_Staging/drift-elimination-2026-04-18/j-a2-frontend-saac/04-bridge-layer-template.md §2.1.M5-FOUNDER`（M5 阶段推导起点 · 2026-04-23 已归档）

> **术语说明**：本文档"场景前端"（Scene Frontend）= M5 时期历史称"消费者端"· 与 SAAC-HL-001 v1.1 `:297-298` 同义 · 覆盖所有非治理后台业务前端（C 端消费者 + B 端客户 + 门店员工）· 以 **R-FE-CLIENT-001 amend-001**（2026-04-23）为 scope 权威。

---

## §1. 概述

### 1.1 场景前端 App 身份

- **仓**：`huanlongAI/hl-scene-app`（J-A1 M4 锁定 · R-060 amend-001 确认 Flutter LOCKED）
- **技术栈**：Flutter 3.41 稳定通道（2026-02 主版本发布线 · patch 跟进当前最新稳定通道 · 不触发 amend）· Dart 3.x（随 Flutter 自带）· Impeller 渲染引擎
- **范式**：一套代码跨端编译（iOS + Android · Phase 1 起）· Desktop / Web 视 Q6.1 方案 B 加分场景择期拓展
- **生命周期**：与 Phase 1 场景前端 App 同步（2026 Q2 启动 · DD-FE-CLIENT v2 重评条件见 §4）

### 1.2 本 DD 的作用

- **对上**：承接 R-FE-CLIENT-001 LOCKED 的 13 字段纪律 · 逐字段落地具体技术细节
- **对下**：为场景前端 App 代码仓 `CLAUDE.md` + CI 规则 + 依赖管理提供权威引用源
- **可替换性**：DD 可随 R-FE-CLIENT-001 重评走 v2 · 不属宪法层 · 属执行层决策派生

### 1.3 推导链引用

本 DD 不重复推导过程 · 完整六维复核 + 三前提失效 + 反向意见预置见：
- `team-memory/03-approved/decisions/DEC-20260420-002-frontend-flutter-derivation-chain.md`
- `09_Staging/drift-elimination-2026-04-18/j-a2-frontend-saac/99-external-reviews/founder-final-decision-flutter-2026-04-20.md`

---

## §2. 13 项技术字段派生

每字段格式：**值 + 理由（指向 source-of-truth）+ 退出条件**

### 2.1 字段 1 · 语言 = Dart 3.x

- **值**：Dart 3.x（随 Flutter 3.41 自带 · 具体 patch 与 Flutter 同步）
- **理由**：Flutter 3.41 原生语言 · 2-3 周上手曲线（4 Web 基线）· 团队 1 名已在职 Flutter 开发者 in-house mentor
- **source-of-truth**：R-FE-CLIENT-001 字段 1 · `04 §2.1.M5-FOUNDER` 行 "Flutter 3.x LTS / Dart 3.x"
- **退出条件**：Dart 主版本停止维护（近 5 年内不可见）· 或 Flutter 移除 Dart 依赖 → 触发 DD-FE-CLIENT v2

### 2.2 字段 2 · 框架 = Flutter 3.41 稳定通道

- **值**：Flutter 3.41（"Year of the Fire Horse" · 2026-02 主版本发布线 · patch 跟进当前最新稳定通道 · 不触发 amend）
- **理由**：创始人 2026-04-20 最终裁决反转两份 Agent 一致 X-2 RN · 决定性维度存量 mentor + uni-app 同构 + 中文资源量 10x CMP + AI 编码助手成熟度
- **升级策略**：patch 随滚（`flutter analyze && flutter test` 无 breaking 即 PR）· minor（3.42+）独立 F-任务 + Phase 1 spike 3-5 天 + v1.x amend · major（4.x）触发 v2 重评
- **source-of-truth**：R-FE-CLIENT-001 字段 2 · DEC-20260420-002 §3
- **退出条件**：Flutter 3.41 线停止维护且 3.42+/4.x 未就绪 · 或 Impeller 生产性退化无回退 · 触发 v2 重评

### 2.3 字段 3 · 渲染引擎 = Impeller

- **值**：Impeller（iOS + Android · 2026 Q2 生产就绪）
- **理由**：Flutter 官方替代 Skia 的新渲染栈 · 自绘像素级一致性（Q7-amend 4% 弱加分场景亲合）· 2026 Q2 全量 production-ready
- **source-of-truth**：R-FE-CLIENT-001 字段 3 · Flutter 3.41 官方 release notes
- **退出条件**：目标设备范围出现性能/稳定性退化且无 Skia 回退方案 · 触发字段 amend 或 v2 重评

### 2.4 字段 4 · 状态管理 = flutter_bloc

- **值**：flutter_bloc（备选 Riverpod · 待 Phase 1 spike 决）
- **理由**：R-044 AI 驱动 · 明确状态机 · pattern 齐全利 AI 编码助手 · 官方推荐之一
- **source-of-truth**：R-FE-CLIENT-001 字段 4 · `04 §2.1.M5-FOUNDER` 行
- **Phase 1 spike 触发条件**：若 BLoC 样板代码阻塞率过高（PR 样板率 > 40%）· 切换 Riverpod 走 DD-FE-CLIENT v1.x amend
- **退出条件**：flutter_bloc 停止维护或被官方废弃 · 触发字段 amend

### 2.5 字段 5 · 路由 = go_router

- **值**：go_router（Flutter 官方）
- **理由**：声明式 · 深链路支持 · 与 BLoC 状态协同良好
- **source-of-truth**：R-FE-CLIENT-001 字段 5
- **退出条件**：停止维护 / 深链路支持不足 · 触发字段 amend

### 2.6 字段 6 · 网络 = dio + retrofit_generator

- **值**：dio 5.x（HTTP client）· retrofit_generator（接口生成）
- **理由**：dio 是 Flutter 社区事实标准 · retrofit_generator 类型安全接口 · 与字段 8 openapi-generator-cli 同生态
- **HTTP 拦截器约束**：
  - 统一注入 `Authorization: Bearer <token>`（从 flutter_secure_storage 读）
  - 生成 `trace_id`（UUID v4 或 W3C Trace Context · 对齐 HK.Audit）
  - **禁止自造** `X-Event-Id` / `X-Reason-Code-Context` 等未入 hk.audit 契约的 header（H4 契约法典硬规则）
- **source-of-truth**：R-FE-CLIENT-001 字段 6 · hk.audit.internal.openapi.v1.yaml
- **退出条件**：dio 停止维护或出现重大安全漏洞 · 触发字段 amend

### 2.7 字段 7 · 本地持久化 = drift + flutter_secure_storage

- **值**：
  - drift（SQLite ORM · 类型安全 · migration 工具成熟）· 业务数据层
  - flutter_secure_storage（iOS Keychain + Android Keystore/EncryptedSharedPreferences）· token / 密钥层
- **理由**：drift 是 Dart 首选 SQLite · 类型安全 · 自带 codegen · flutter_secure_storage 是认证体系标准搭配
- **source-of-truth**：R-FE-CLIENT-001 字段 7
- **退出条件**：drift 停止维护 · 或场景前端改为后端下沉存储 · 触发字段 amend

### 2.8 字段 8 · OpenAPI 代码生成 = openapi-generator-cli(dart-dio-next)

- **值**：openapi-generator-cli · 模板 `dart-dio-next`
- **理由**：hl-contracts OpenAPI YAML → Dart 类型 · 与字段 6 dio 同生态
- **自动化**：hl-contracts 主分支发版 → GitHub Actions → 发 PR 更新场景前端 `packages/api-client`
- **约束**：场景前端 `api-client` 版本与 hl-contracts 版本一一对应 · 发版后 48 小时内同步（参 SAAC P1-FE-2）
- **source-of-truth**：R-FE-CLIENT-001 字段 8 · `04 §3 契约对接` 段落
- **退出条件**：`dart-dio-next` 模板停止维护 · 或 hl-contracts 改用其他契约格式 · 触发字段 amend

### 2.9 字段 9 · 单元测试 = flutter_test

- **值**：flutter_test（unit + widget）
- **理由**：Flutter 官方测试框架 · 涵盖 unit + widget
- **source-of-truth**：R-FE-CLIENT-001 字段 9

### 2.10 字段 10 · 集成测试 = integration_test

- **值**：integration_test（E2E · 取代旧 flutter_driver）
- **理由**：Flutter 官方 E2E 测试框架
- **CI 门禁**：`flutter analyze && flutter test && integration_test` 作为场景前端 App 最小绿线
- **source-of-truth**：R-FE-CLIENT-001 字段 10

### 2.11 字段 11 · Lint = flutter_lints

- **值**：flutter_lints（Flutter 官方推荐 lint 包）
- **理由**：与 `dart analyze` / `flutter analyze` 默认对齐 · 无需额外配置
- **source-of-truth**：R-FE-CLIENT-001 字段 11

### 2.12 字段 12 · 可观测性 = opentelemetry pub.dev

- **值**：opentelemetry（OTel Dart SDK · pub.dev 包）
- **理由**：trace_id 对齐 HK.Audit · 发送到 S-L1 Gateway · 与字段 6 dio 拦截器协同
- **审计约束**：
  - 场景前端**不自造 event_id**
  - key_action 调用链：场景前端调能力包 → 能力包在本地事务中调 HK.Audit `/hk/audit/sign`（`operationId: hk.audit.sign`）→ HK.Audit 签发 event_id 回传
  - reason_code 由 HK.Audit ReasonDict SSOT 校验 · 场景前端传入字符串参数 · 不硬编码枚举
- **source-of-truth**：R-FE-CLIENT-001 字段 12 · hk.audit.internal.openapi.v1.yaml `operationId: hk.audit.sign`

### 2.13 字段 13 · 认证 = flutter_appauth / openid_client

- **值**：flutter_appauth（首选）/ openid_client（备选 · 待 Phase 1 spike 决）
- **理由**：走 DD-AUTH v1 Bearer Token / OIDC · 场景前端存储 Keychain + Keystore/EncryptedSharedPreferences
- **Phase 1 spike 触发条件**：flutter_appauth 与 DD-AUTH v1 OIDC provider 对接出现阻塞 · 切换 openid_client 走字段 13 v1.x amend
- **source-of-truth**：R-FE-CLIENT-001 字段 13 · DD-AUTH v1

---

## §3. 验收指标（SLO）

所有指标为**发布门槛** · 不达标不得进 Phase 1 生产通道

| 指标 | 阈值 | 度量 | 责任 |
|---|---|---|---|
| 首屏时间 | ≤ 2s（冷启动到首帧可交互）P95 | 本地 dev + Sentry/APM | 场景前端 App 开发组 |
| 帧率 | ≥ 55fps（关键交互路径）P95 | Flutter DevTools + APM | 同上 |
| 崩溃率 | ≤ 0.1%（生产环境 · 滚动 7 日窗口）| APM · Sentry / Crashlytics | 同上 |
| trace_id 对齐率 | 100%（所有含 HK.Audit 请求）| CI 静态检查 + 生产抽样 | SRE + 场景前端 App |
| CI 绿线 | 每次 PR 过 `flutter analyze && flutter test && integration_test` | CI pipeline | CI 平台 |

---

## §4. 退出条件（触发 DD-FE-CLIENT v2 重评）

以下任一条件触发整条 DD 重评（v1 → v2）· **非 v1.x amend**（amend 适用于字段微调 · v2 适用于整条 RULING 级重评）：

1. Flutter 3.41 线官方停止维护 · 且 3.42+/4.x 未同步就绪
2. Impeller 在目标设备范围生产性退化 · 无回退方案
3. Phase 1 落地后出现渲染/性能/DS 构建**结构性问题**（非单字段能解决）
4. Direction B 规范完成后倾向非 Flutter 路径（不强制 · 由创始人择期）
5. 2027 年 CMP 生态 / 中文社区 / AI 编码助手成熟度追平 Flutter 水平 · 触发 Phase 2 CMP POC 评估（非自动 v2 · 需创始人裁决）

---

## §5. 交叉引用表

| R-FE-CLIENT-001 字段 | DD-FE-CLIENT v1 §2 | j-a2 `04 §2.1.M5-FOUNDER` | SAAC P1-FE | TECH-STACK-SPEC §8 |
|---|---|---|---|---|
| 1 语言 Dart 3.x | §2.1 | 技术栈行 | P1-FE-1 | 引用真源 |
| 2 框架 Flutter 3.41 | §2.2 | 技术栈行 | P1-FE-1 | 引用真源 |
| 3 渲染引擎 Impeller | §2.3 | 技术栈行 | — | 引用真源 |
| 4 状态管理 flutter_bloc | §2.4 | 状态管理行 | — | 引用真源 |
| 5 路由 go_router | §2.5 | 路由行 | — | 引用真源 |
| 6 网络 dio | §2.6 | HTTP 客户端行 | — | 引用真源 |
| 7 本地持久化 drift | §2.7 | 本地存储行 | — | 引用真源 |
| 8 OpenAPI codegen | §2.8 | 契约类型生成行 | P1-FE-2 | 引用真源 |
| 9 单元测试 flutter_test | §2.9 | 测试栈行 | P1-FE-2 | 引用真源 |
| 10 集成测试 integration_test | §2.10 | 测试栈行 | P1-FE-2 | 引用真源 |
| 11 Lint flutter_lints | §2.11 | 测试栈行 | P1-FE-2 | 引用真源 |
| 12 OTel SDK | §2.12 | OTel SDK 行 | — | 引用真源 |
| 13 认证 flutter_appauth | §2.13 | OIDC 客户端行 | — | 引用真源 |

**口径纪律**：13 字段在以上 5 处必须完全一致 · 后续 PR（F-11 SAAC / F-12 TECH-STACK-SPEC）使用本表作 cross-check 工具。

---

### 5.1 DS 形态交叉引用（承接 R-036 amend-001 + R-FE-CLIENT-001 amend-001 scope）

**DS 形态**：Dart package（pub.dev 发布形态 · `huanlongAI/hl-scene-design-system` 仓 · 属 S 域 Scene Design System）

**权威源**：
- `04-bridge-layer-template.md §2.1.M5-FOUNDER` 表 "DS 包形态 · Dart package（pub.dev 发布形态 · hl-scene-design-system 仓）" 行
- R-FE-CLIENT-001 框架链派生（Flutter widgets → Dart package DS · 非 R-FE-CLIENT-001 13 字段之一 · 独立仓独立治理）
- R-036 amend-001（scope 限定 · C 域 HLDesignKit 作废 · S 域 `huanlongAI/hl-scene-design-system` 新建 · 两者不共享命运）

**C 域 / S 域边界**：

| 维度 | C 域 HLDesignKit（R-036 指向 · 作废）| S 域 `huanlongAI/hl-scene-design-system`（新建）|
|---|---|---|
| 域归属 | C 域 HLConsole 运营后台 | S 域 Scene 场景前端 |
| 仓 | `huanlongAI/hl-design-system` | `huanlongAI/hl-scene-design-system` |
| 技术栈 | React / TypeScript | Dart package · Flutter widgets |
| 生命周期 | 随 hl-console-native 迁移完成即删 | 与场景前端 App `hl-scene-app` 同生命周期 |
| 治理 | R-036 LOCKED（迁移完成即删纪律）| 本 DD §5.1 + R-036 amend-001 scope 限定 |

**为何 DS 形态不作 R-FE-CLIENT-001 13 字段之一**：
- R-FE-CLIENT-001 范围 = **场景前端 App 技术栈**（即 `hl-scene-app` 仓内部依赖）
- DS 包形态 = **场景前端 DS 独立仓**（即 `hl-scene-design-system` 仓的发布形态）· 两个仓独立治理
- 若把 DS 形态塞进 R-FE-CLIENT-001 13 字段 · 会导致 "R-FE-CLIENT-001 条目混入 DS 独立仓约束" · scope 污染
- 现分工：R-FE-CLIENT-001 锁 App 仓 13 字段；R-036 amend-001 锁 DS 仓的 scope 边界；DD-FE-CLIENT v1 §5.1（本小节）补 DS 形态交叉引用

**审计纪律**：未来 DS 仓变更（如改发布形态 / 改仓名）触发的是 **R-036 amend-002** + **DD-FE-CLIENT v1.x amend**（增补 §5.1）· 不触发 R-FE-CLIENT-001 重评。

---

## 变更日志

| 日期 | 版本 | 变更 | 签批 |
|---|---|---|---|
| 2026-04-20 | v1.0 | 初版 · 与 R-FE-CLIENT-001 LOCKED 同步入库 | L0-Founder cat（Cowork 信道 · PR #13 合入真源） |
