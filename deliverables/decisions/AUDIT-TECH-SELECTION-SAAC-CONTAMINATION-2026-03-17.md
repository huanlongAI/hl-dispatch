# SAAC 污染审计报告 — 技术选型清单

> **文档编号**：AUDIT-TECH-SELECTION-SAAC-CONTAMINATION-2026-03-17
> **审计日期**：2026-03-17
> **审计范围**：DECISION-2026-03-13-GREENFIELD-TECH-OPS-AUDIT v1.0
> **审计对照**：SAAC-HL-001 v1.1 + TECH-STACK-SPEC v3 + RULINGS.md（截至 2026-03-17）
> **审计人**：架构 AI 助理（创始人督导）
> **裁决人**：L0-Founder（创始人）

---

## 一、审计背景

技术选型清单 v1.0 编写于 2026-03-13，但此后工作区发生了重大变更：

1. **D1 Kotlin 裁决**：S 域实现语言从 Java 21 变更为 Kotlin 2.1.10 / JVM 21
2. **DD-CACHE 推导**：推翻 R-054 Q3 Caffeine/Redis 分层方案，Phase 0 不预置任何缓存
3. **DD-AUTH 推导**：Phase 0 使用 Spring Security 内建 JWT，Keycloak 退为 Phase 1+ 引入条件
4. **R-054 Q1 冲突裁决**：EP-001 §2.2 优先，外部 MQ Phase 0 暂缓
5. **SAAC-HL 升级**：v1.0 → v1.1（2026-03-13）
6. **TECH-STACK-SPEC v3 发布**：完整推导链版本锁定
7. **R-037/R-040/R-028 标注 NEEDS-REVISION**：Kotlin 化后 starter 收敛为 5 个

上述变更导致 v1.0 清单与当前架构推导链存在 **17 项偏移**，需全面修正。

---

## 二、发现项（按严重度排序）

### 🔴 红色偏移（选型与推导链结论直接矛盾）

| 编号 | 条目 | v1.0 内容 | 工作区当前状态 | 处置 |
|------|------|-----------|--------------|------|
| A-1 | T-01 语言 | Java 21 LTS | Kotlin 2.1.10 / JVM 21（D1） | ✅ 已修正 v1.1 |
| A-2 | T-07 MQ | RocketMQ 5.x Phase 0 引入 | Phase 0 不预置外部 MQ（R-054 Q1 降级） | ✅ 已修正 v1.1 |
| A-3 | T-08 缓存 | Caffeine Phase 0 L1 | Phase 0 不预置缓存（DD-CACHE, R-054 Q3 SUPERSEDED） | ✅ 已修正 v1.1 |
| A-4 | T-11 认证 | Keycloak 26.x Phase 0 | Phase 0: Spring Security 内建 JWT（DD-AUTH） | ✅ 已修正 v1.1 |
| A-5 | T-17 Starters | 7 个 | 5 个（R-037 修订：砍 mybatis+cache+mq） | ✅ 已修正 v1.1 |

### 🟡 黄色偏移（引用过时或描述不完整）

| 编号 | 条目 | v1.0 内容 | 工作区当前状态 | 处置 |
|------|------|-----------|--------------|------|
| A-6 | §0 SAAC 版本 | v1.0 | v1.1 | ✅ 已修正 v1.1 |
| A-7 | T-02 定位 | "Modulith 唯一成熟选择" | "仅作 adapter/runtime 容器"（P0-0） | ✅ 已修正 v1.1 |
| A-8 | T-09 裁决列 | R-054 Q2 | 追加 R-027→SUPERSEDED | ✅ 已修正 v1.1 |
| A-9 | T-12 R-042 | R-008/R-009/R-013 | R-042 已 SUPERSEDED（2026-03-13） | ✅ 已修正 v1.1 |
| A-10 | T-20 CI Gate | 4 道 | 8 道（TECH-STACK-SPEC v3 §10） | ✅ 已修正 v1.1 |
| A-11 | 推导权威链 | 未声明 | SAAC→BRIDGE→DD→EP→TECH-STACK-SPEC v3 | ✅ 已修正 v1.1 |

### 🟢 前轮裁决未落地

| 编号 | 裁决 | 用户决定 | RULINGS.md 状态 | 处置 |
|------|------|----------|----------------|------|
| A-12 | R-027 | SUPERSEDED | 原 LOCKED | ✅ 已更新 RULINGS.md |
| A-13 | R-015 | SUPERSEDED | 原 LOCKED（待修订） | ✅ 已更新 RULINGS.md |
| A-14 | R-035.A | 措辞修订 | 旧系统语言残留 | ✅ 已更新 RULINGS.md |

### ✅ 确认无误项

| 条目 | 说明 |
|------|------|
| T-28 / R-055 | R-055 存在且有效（HK 服务化开放策略 LOCKED），引用正确 |
| T-05 PostgreSQL 18 | 与 TECH-STACK-SPEC v3 一致 |
| T-03 Gradle 8.12 | 与 TECH-STACK-SPEC v3 一致 |
| T-22/T-23 客户端 | R-052 未变更 |
| T-27~T-30 架构治理 | 与 SAAC-HL v1.1 一致（T-27 模块数从 6→4 已在 v1.1 反映） |

---

## 三、新增条目

| 条目 | 说明 | 来源 |
|------|------|------|
| T-16 Spring Modulith 1.3.4 | 从 T-29 独立为精确版本条目 | TECH-STACK-SPEC v3 §3.2 |
| T-19b JUnit 5.10.2 | 测试框架条目 | TECH-STACK-SPEC v3 §5 |
| T-05b Spring Data JPA | ORM 明确条目 | DD-ORM |
| T-11b Keycloak Phase 1+ | 从 T-11 拆分分阶段 | DD-AUTH |
| T-15b Phase 0 可观测 | Actuator + Logback + Micrometer | TECH-STACK-SPEC v3 §9 |
| T-18b starter-cache/mq 已砍 | DD-CACHE/EP-001 联动 | TECH-STACK-SPEC v3 §9 |
| T-31～T-36 | CDC/Outbox + 智能态 + 数据态 | SAAC-HL §7.2 + 三态模型 |
| §7 Phase 0 不预置清单 | 新增整章 | TECH-STACK-SPEC v3 §7 |

---

## 四、处置总结

| 统计 | 数量 |
|------|------|
| 红色偏移（已修正） | 5 |
| 黄色偏移（已修正） | 6 |
| 前轮裁决落地 | 3 |
| 新增条目 | 7 类 |
| 确认无误 | 5 |
| **总计审计项** | **26** |

所有审计项已在 DECISION-2026-03-13-GREENFIELD-TECH-OPS-AUDIT v1.1 中闭环处理。

---

*审计完成，2026-03-17。*
