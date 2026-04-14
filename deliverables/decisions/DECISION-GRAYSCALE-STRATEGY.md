# 灰度发布策略决策文档

**文档编号**：DECISION-2026-03-04-GRAYSCALE
**版本**：v1.2（2026-03-04 补丁：稳定哈希规范 + 扩量门禁 + 租户级可观测 + 时序修正 + Feature Toggle F1）
**裁决人**：L0-Founder（创始人）
**接收人**：Gate-R（运维）、Infra-A（后端）、Gate-H（架构）、PM-Ops（能力包适配团队项目）
**背景**：2026-03-04 对齐沟通会上，Gate-R团队提出灰度策略需要明确路由机制及后端功能归属

---

## 一、问题回顾

R-034 执行计划中定义了灰度切流路径 `1%→10%→50%→100%`，但未明确：

1. 灰度路由的维度（按什么分流？）
2. 路由功能由谁开发（后端功能 vs 运维配置）
3. 运维的操作边界（调参数 vs 建功能）

Gate-R团队指出：**灰度路由是后端功能，运维负责使用而非开发**。这个判断完全正确。

---

## 二、裁决结论

### 2.1 灰度路由策略

采用 **租户 ID 哈希（tenant_id）** 作为主路由维度，分两个阶段执行：

| 阶段 | 策略 | 路由方式 | 目的 |
|------|------|---------|------|
| 金丝雀（1%） | **白名单模式** | 指定 2~3 个内部测试租户走新版本 | 精确观察，快速发现问题 |
| 扩量（10%→50%→100%） | **tenant_id 哈希** | `Murmur3(tenant_id) % 100 < threshold` | 均匀扩量，同一租户体验一致 |

### 2.2 选择 tenant_id 哈希的理由

| 维度 | 评估 |
|------|------|
| 与 HK 模型契合度 | 唤龙平台是多租户 SaaS，tenant_id 是天然的最小隔离单元。同一租户的所有请求走同一版本，体验一致 |
| 可回退性 | 回退时只需将该租户从新版本摘除，其数据和状态不会出现版本混杂 |
| 问题排查 | 出问题时可精确定位到哪些租户受影响，比随机比例路由更容易排查 |
| 实现复杂度 | Gateway 已有 tenant_id filter（S1 交付物），灰度路由在同一位置扩展即可 |

### 2.3 稳定哈希规范 `[v1.1 补丁 G1]`

Java `hashCode()` 跨 JVM 版本/实现不保证稳定，跨语言更不可用。灰度路由的哈希必须满足：**同一 tenant_id 永远落同一桶**。

| 规范项 | 约定值 |
|--------|--------|
| 哈希算法 | Guava `Hashing.murmur3_32_fixed()` 或等价 Murmur3-32 实现 |
| 输入编码 | `tenant_id` 原始字符串，UTF-8 字节序列 |
| 盐（seed） | 固定值 `0x48_4C_47_52`（"HLGR" ASCII），写入配置不可变 |
| 取模 | `(hash & 0x7FFF_FFFF) % 100`（确保非负） |
| 版本号 | 哈希规范版本 = `1`，写入 Nacos 配置；未来变更必须新增版本号 + 双跑验证 |

**验证要求**：单元测试覆盖以下不变量：

- 同一 tenant_id 多次调用结果一致
- 不同 JVM 实例（同版本）结果一致
- 已知向量表（≥10 个 tenant_id → 期望桶号）硬编码到测试用例

**未采用的方案及原因**：

| 方案 | 未采用原因 |
|------|----------|
| 请求比例随机 | 同一租户可能两次请求到不同版本，体验不一致；排查困难 |
| 地域/设备 | Phase 1 为单集群部署，地域区分无意义 |
| 时间窗口 | 不适合 SaaS 场景，某些租户营业时间不同 |

---

## 三、实现方案

### 3.1 Gateway 灰度路由 Filter

在 Gateway 现有 filter 链中新增 `GrayscaleRoutingFilter`，位于 `TenantIdFilter` 之后、`ProtocolGateFilter` 之前：

```
请求进入 → TenantIdFilter（提取 tenant_id）
         → GrayscaleRoutingFilter（决定走新版本还是旧版本）
         → FeatureToggleFilter [v1.1]（检查目标功能模块是否已启用）
         → ProtocolGateFilter（协议合规检查）
         → 路由到目标服务
```

### 3.1.1 Feature Toggle — 模块级功能开关 `[v1.1 补丁 F1]`

**问题**：灰度路由解决"流量切到哪个版本"，但不解决"这个版本里哪些功能可用"。如果 S2 只交付了 HK 7 模块但 Consent 联调未完成，灰度用户会触达未就绪接口。

**方案**：在 Nacos 新增 `feature-toggles.yaml`，每个 HK 模块有独立开关。Gateway 的 `FeatureToggleFilter` 位于 GrayscaleRoutingFilter 之后，拦截未启用模块的请求返回 `501 Not Implemented`。

**配置格式**（存储于 Nacos）：

```yaml
feature-toggles:
  config_version: 1
  modules:
    hk.identity:    { enabled: true,  since: "S1" }
    hk.tenant:      { enabled: true,  since: "S1" }
    hk.org:         { enabled: true,  since: "S1" }
    hk.policy:      { enabled: true,  since: "S2" }
    hk.consent:     { enabled: false, since: null }   # 未就绪，返回 501
    hk.audit:       { enabled: true,  since: "S2" }
    hk.perf-policy: { enabled: true,  since: "S2" }
```

**路由逻辑**：

1. 从请求路径提取模块标识（`/hk/{module}/...` → `hk.{module}`）
2. 查询 `feature-toggles` 配置
3. `enabled=true` → 放行
4. `enabled=false` → 返回 `501 Not Implemented`（body 含 `reason_code=FEATURE_NOT_READY`，`module={module_name}`）
5. 配置缺失或解析失败 → **fail-secure：返回 501**（未显式启用 = 不放行）

**与灰度路由的关系**：

| 维度 | GrayscaleRoutingFilter | FeatureToggleFilter |
|------|----------------------|---------------------|
| 解决的问题 | 流量走新版本还是旧版本 | 新版本里哪些功能可用 |
| 粒度 | 租户级 | 模块级 |
| 默认行为 | fail-secure → 旧版本 | fail-secure → 501 |
| 配置中心 | `grayscale.yaml` | `feature-toggles.yaml` |

**一句话**：灰度路由管"谁进来"，Feature Toggle 管"进来后能用什么"。两道门，缺一不可。

**ProtocolGateFilter 定性** `[v1.1 补丁]`：ProtocolGateFilter 是**版本无关**的统一协议合规检查（信封格式、必填字段、reason_code 合法性），不区分新旧版本业务协议。因此路由在前、Gate 在后的链路位置正确——无论路由到新旧版本，ProtocolGate 的校验逻辑一致。

**路由逻辑**：

1. 读取灰度配置（优先本地缓存，缓存 TTL = 30s）
2. 如果 `tenant_id ∈ 白名单` → 路由到新版本
3. 否则，如果 `Murmur3(tenant_id, seed=0x484C4752) & 0x7FFFFFFF % 100 < threshold` → 路由到新版本
4. 否则 → 路由到旧版本
5. 配置解析失败 → **fail-secure：路由到旧版本**（不默认走新版本）
6. 连续 3 次配置拉取失败 → 触发告警（R-022 P0 规则扩展），冻结当前阈值直至配置恢复

**灰度配置格式**（存储于 Nacos 配置中心）：

```yaml
grayscale:
  config_version: 1          # 配置版本号，变更必须递增
  hash_spec_version: 1       # 哈希规范版本（对应 §2.3）
  enabled: true
  whitelist:
    - "tenant_001"            # 内部测试租户
    - "tenant_002"
  threshold: 0                # 0~100，表示哈希扩量百分比
  fallback: old               # 配置异常时的默认路由
  local_cache_ttl_seconds: 30 # 本地缓存 TTL
```

### 3.2 分工与交付时间线

| 工作项 | 内容 | 负责人 | Sprint | 依赖 |
|--------|------|--------|--------|------|
| GrayscaleRoutingFilter 开发 | Gateway 层灰度路由 filter 实现 + 稳定哈希（Murmur3）+ 本地缓存 + 熔断 + 单元测试（含已知向量表） | L0-Founder + AI | S2 | TenantIdFilter（S1 已交付） |
| Nacos 灰度配置模板 | grayscale.yaml 配置模板 + config_version 机制 + 文档 | L0-Founder + AI | S2 | Nacos 集群（S0 Gate-R已部署） |
| FeatureToggleFilter 开发 `[v1.1 F1]` | Gateway 模块级功能开关 filter + feature-toggles.yaml 配置 + 单元测试 | L0-Founder + AI | S2 | GrayscaleRoutingFilter |
| S2 最小可用操作面 `[v1.1]` | 通过 Nacos 配置变更即可操作白名单/阈值/模块开关（无需 API），Gate-R获得 Nacos 灰度+功能开关配置命名空间写权限 | L0-Founder（配置设计）+ Gate-R（权限配置） | S2 | GrayscaleRoutingFilter + FeatureToggleFilter |
| 灰度操作 API | 查询/修改灰度比例的正式管理接口（封装 Nacos 操作，供运维调用） | L0-Founder + AI | S4（压测前） | — |
| 灰度操作 SOP（草案） `[v1.1]` | S3 出草案（基于 Nacos 直接操作），S5 升级为正式版（基于 API） | Gate-R | S3 草案 / S5 正式版 | S2 最小可用操作面 / S4 灰度 API |
| 灰度回滚演练 `[v1.1]` | 在 Staging 环境执行一次完整回滚演练，输出演练报告（≤5 分钟回滚验证） | Gate-R | S4（压测前） | SOP 草案 + Staging 环境 |
| 灰度切流执行 | 按 SOP 执行 1%→10%→50%→100% 切流 + 72h 观察（每档需满足扩量门禁） | Gate-R | S5 | 正式版 SOP + 扩量门禁表 |
| 灰度监控大盘 | 按 tenant_id 分组的请求量/错误率/p95 延迟/关键 reason_code 可视化（含扩量门禁指标） | Gate-R | S3~S4 | starter-observability（S1 Infra-A已交付） |

### 3.3 运维操作边界（回答Gate-R团队的问题）

明确划分"建功能"与"用功能"的边界：

| 类别 | 内容 | 负责人 |
|------|------|--------|
| **后端建设**（不是运维的活） | GrayscaleRoutingFilter 开发、灰度操作 API 开发、路由逻辑实现 | L0-Founder |
| **运维操作**（Gate-R的活） | 调用灰度 API 修改阈值、执行切流 SOP、监控观察、回滚执行 | Gate-R |
| **协作项** | 灰度监控大盘需要后端埋点（Micrometer）+ 运维配置 Grafana 面板 | Infra-A（埋点）+ Gate-R（面板） |

**一句话总结**：后端开发灰度路由功能和操作接口，运维通过接口和 SOP 执行灰度切流操作。运维不需要也不应该直接修改 Gateway 代码。

---

## 四、对 R-034 的影响

本裁决需要更新 R-034 以下条目：

| 变更项 | 原内容 | 新增/修改内容 |
|--------|--------|-------------|
| S2 L0-Founder交付物 | HK 7 模块 PG 集成 + 审计链路 + Gateway ProtocolGate | **新增**：GrayscaleRoutingFilter + Nacos 灰度配置模板 |
| S4 L0-Founder交付物 | hl-console-native API 联调 | **新增**：灰度操作 API |
| S5 Gate-R交付物 | 终检报告 + 灰度切流 SOP + 72h 观察报告 | 不变（SOP 内容需要包含灰度 API 调用方式） |
| RACI 灰度切流行 | A=L0-Founder, R=Gate-R | 不变（A 负责功能建设决策，R 负责切流执行） |

---

## 五、扩量门禁表 `[v1.1 补丁 G2]`

**硬规则**：每次扩量（1%→10%→50%→100%）前必须出具以下指标报告，全部达标才允许进入下一档。不满足任一条 → 冻结当前阈值，排查修复后重新申请扩量。

| 指标 | 阈值 | 数据源 | 观察窗口 |
|------|------|--------|---------|
| P0 告警数量 | **= 0** | Alertmanager（R-022） | 当前阶段全程 |
| 新版本 5xx 错误率 | **< 0.1%** | 灰度监控大盘（按 tenant_id 分组） | 最近 72h |
| 新版本 p95 延迟上涨幅度 | **< 10%**（相对旧版本同类接口） | 灰度监控大盘 | 最近 72h |
| 关键 reason_code 异常数 | **= 0**（deny 类 reason_code 不应出现在正常租户） | HK.Audit 审计链路 | 最近 72h |
| 业务验证用例通过率 | **= 100%** | 测试组回归报告 | 扩量前执行 |

**扩量审批流程**：Gate-R出具指标报告 → L0-Founder审批 → Gate-R执行阈值变更。

---

## 六、租户级可观测要求 `[v1.1 补丁 G3]`

灰度切流期间，监控大盘必须具备**按 tenant_id 分组**的以下视图：

| 视图 | 说明 | 实现方 |
|------|------|--------|
| 请求量分布 | 新/旧版本各接收多少请求，按租户分组 TOP-N | Gate-R（Grafana） |
| 错误率对比 | 新版本租户 vs 旧版本租户的 5xx/4xx 比率 | Gate-R（Grafana） |
| p95/p99 延迟对比 | 按版本分组的接口延迟百分位 | Gate-R（Grafana） |
| 关键 reason_code 分布 | deny/error 类 reason_code 按租户和版本聚合 | Infra-A（Micrometer 埋点）+ Gate-R（面板） |
| 灰度配置变更事件 | 配置版本号变更时间线 + 操作人 | Nacos 审计日志 |

**验收时点**：S3 末具备基本大盘（请求量+错误率），S4 末具备完整大盘（含 reason_code + 延迟），S5 扩量前全部就绪。

**与扩量门禁的绑定**：扩量门禁表（§五）中的指标数据必须从此大盘直接导出，不接受手工统计。

---

## 七、验收标准

| 验收项 | 标准 | 验收时点 |
|--------|------|---------|
| GrayscaleRoutingFilter | 白名单路由 + Murmur3 哈希路由 + fail-secure + 本地缓存 + 熔断，五条路径单元测试通过（含已知向量表） | S2 Gate H |
| 稳定哈希不变量 `[v1.1]` | 已知向量表（≥10 个 tenant_id→桶号）跨实例验证一致 | S2 Gate H |
| 灰度配置 | Nacos 动态刷新 ≤30s 生效（本地缓存 TTL）；配置格式错误时 fallback 到旧版本；连续失败触发告警 | S2 Gate H |
| FeatureToggleFilter `[v1.1 F1]` | 模块开关 enabled/disabled + fail-secure（未显式启用=501）+ 路径解析单元测试 | S2 Gate H |
| 最小可用操作面 `[v1.1]` | Gate-R可通过 Nacos 配置变更操作白名单/阈值/模块开关，无需代码部署 | S2 Gate H |
| 灰度监控大盘（基础） `[v1.1]` | 请求量分布 + 错误率对比按 tenant_id 分组可视化 | S3 末 |
| SOP 草案 `[v1.1]` | 基于 Nacos 操作的白名单/阈值变更步骤 + 回滚步骤 | S3 末 |
| 灰度操作 API | 查询当前配置 + 修改阈值 + 添加/移除白名单三个接口可用 | S4 Gate H |
| 灰度回滚演练 `[v1.1]` | Staging 环境完整回滚演练通过，≤5min 回滚，输出演练报告 | S4 Gate H |
| 灰度监控大盘（完整） `[v1.1]` | 含 reason_code 分布 + 延迟对比 + 配置变更事件，扩量门禁指标可直接导出 | S4 末 |
| 灰度切流 SOP（正式版） | 基于 API 的完整操作手册 + 扩量门禁检查清单 + 回滚步骤 | S5 Gate R |
| 72h 灰度观察 | 每档扩量前出具扩量门禁报告（§五），全部达标才允许下一档；出现 P0 → 按 SOP 回滚 | S5 M5 |

---

## 八、FAQ

**Q：为什么不用 Nginx upstream weight 做灰度？**
A：Nginx weight 是请求级随机分流，同一租户的两次请求可能到不同版本，造成数据和体验不一致。唤龙平台是多租户 SaaS，灰度粒度必须是租户级。

**Q：灰度路由会增加 Gateway 延迟吗？**
A：哈希计算和白名单查询均为内存操作，增加延迟 <1ms，可忽略。Nacos 配置本地缓存，不会每次请求远程查询。

**Q：如果某个大租户请求量特别大，哈希分流会不均匀吗？**
A：哈希是按租户 ID 分流，不是按请求量。大租户整体要么走新版本、要么走旧版本。扩量阶段可以通过调整 threshold 控制"有多少比例的租户走新版本"，但每个租户是原子切换的。

**Q：运维需要学什么新技能？**
A：S2~S3 阶段只需学会 Nacos 配置变更操作灰度白名单/阈值；S4 后改为调用灰度操作 API（REST 接口）。全程需读懂 Grafana 灰度监控大盘。不需要了解 Gateway 内部实现。

**Q：为什么不用 Java hashCode() 而用 Murmur3？** `[v1.1]`
A：Java `String.hashCode()` 虽然在同一 JVM 版本内稳定，但跨语言不可移植，且未来如果网关层引入非 Java 组件（如 Envoy sidecar）会导致同一 tenant_id 落桶不一致。Murmur3 是业界标准的非加密哈希，跨语言实现一致，且分布均匀性优于 hashCode。

**Q：扩量门禁会不会拖慢灰度进度？** `[v1.1]`
A：门禁是保护机制不是阻塞机制。如果系统健康（P0=0、5xx<0.1%、延迟正常），72h 观察 + 出具报告 + 审批可在 1 天内完成。门禁真正拦住的是"拍脑袋扩量"导致的大面积事故。

---

> **引用依据**：R-034（Phase 1 执行计划）、R-022（生产告警策略）、R-024（Keycloak Token Claims — tenant_id）、协作手册 v1.1
