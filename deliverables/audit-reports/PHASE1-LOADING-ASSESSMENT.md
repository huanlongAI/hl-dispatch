# Phase 1 约束加载评估

> 执行时间：2026-03-14
> 依据：EP-001 v1.1 §7.2 Phase 1 加载检查清单 + §2.2 暂缓约束表
> 前提：Phase 0 验收通过（14 项指标 12 通过 / 1 延后 / 1 N/A），GAP-1 已修复

---

## 评估总览

| 暂缓项 | 加载条件（EP-001 §2.2） | 条件是否满足 | Phase 1 建议 |
|--------|----------------------|------------|------------|
| 四层检查门禁 L1-L4 | Phase 1 稳定后 | 否（Phase 1 尚未开始） | **Phase 1 中期加载** |
| 能力来源标注 HL-P7 | 能力包引入时 | 否（无外部能力包） | **不加载** |
| DEVPACK 接入契约 | Phase 1 | 否（无外部能力包） | **不加载** |
| Gateway 独立进程 | 能力包独立部署时 | 否（单 JVM） | **不加载** |
| D 域 CDC 全链路 | S-L6 Outbox 就绪后 | 否（adapter 层未建） | **Phase 1 后期评估** |
| hl-framework 独立仓 | 按需 | 否（内建子模块足够） | **不加载** |
| 六模块物理拆分 | 团队 > 10 人 | 否（6 人团队） | **不加载** |

**结论：7 项暂缓约束中，0 项满足立即加载条件。Phase 1 应聚焦 adapter 层建设，而非约束加载。**

---

## 逐项评估

### 1. 四层检查门禁 L1-L4

**EP-001 加载条件**：Phase 1 稳定后

**当前状态**：Phase 0 CI 门禁 8 个脚本已就位（P0-6 最小检查集），但 CI runner 未激活（GitHub Actions build.yml 存在但未配置自动触发）。SAAC-HL §7.2 第 5 条定义的四层门禁（L1 编译 / L2 隔离 / L3 语义 / L4 集成）中，L1-L3 的脚本已齐备，L4（集成测试 + Modulith verify）需要 Spring 运行时环境。

**建议**：Phase 1 分两步加载：
- **Phase 1 前期**：激活 CI runner，把现有 8 个脚本挂入 GitHub Actions（L1-L3 立即生效）
- **Phase 1 中期**：adapter 层就绪后，加入 L4 集成测试 + Modulith verify

**人话**：脚本都写好了但还没通电，Phase 1 先通电、再加最后一层。

### 2. 能力来源标注体系 HL-P7

**EP-001 加载条件**：Phase 1 能力包引入时

**当前状态**：Phase 1 规划中无外部能力包（DEVPACK）引入。唤龙平台 Phase 1 目标是 adapter 层建设 + 首个可运行的 HTTP API，不涉及能力包生态。

**建议**：不加载。当第一个外部能力包（如第三方数据源、AI 能力接入）需求出现时再评估。

**人话**：没有外部能力包接进来，标注体系就没有标注对象，做了也是空转。

### 3. DEVPACK 能力包接入契约

**EP-001 加载条件**：Phase 1

**当前状态**：EP-001 §2.2 原定"Phase 1"加载，但 Phase 1 实际规划聚焦 S 域 adapter 层，不涉及外部能力包。DEVPACK 契约的前提是：有独立部署的能力包需要通过 Gateway 接入，而 Phase 1 仍是单 JVM Modulith。

**建议**：不加载。推迟到 Phase 2（生态开放）。

**人话**：能力包接入契约是给"别人的代码接进来"用的，Phase 1 还没有"别人"。

### 4. Gateway 独立进程部署

**EP-001 加载条件**：能力包独立部署时

**当前状态**：D9 明确 Phase 0-1 单 JVM Modulith。Gateway 当前是 hl-platform 内的 gradle 子模块，domain 层纯 Kotlin 决策逻辑。独立进程部署需要：HTTP 服务器 + 负载均衡 + 进程间通信协议，远超 Phase 1 范围。

**建议**：不加载。推迟到 Phase 3（微服务化）。

**人话**：网关独立出去需要整套分布式基础设施，Phase 1 单机够用。

### 5. D 域 CDC 全链路

**EP-001 加载条件**：S-L6 Outbox 就绪后

**当前状态**：S-L6 Outbox 的前提是 adapter 层 Spring Events + Modulith Outbox 配置就绪。Phase 0 只有 domain 层，adapter 层未建。D 域（Data Domain）CDC 更是 Phase 2 以后的事情——需要数据变更捕获管道 + 下游消费者。

**建议**：不加载。Phase 1 后期 Outbox 就绪后再评估 D 域 CDC 的启动时机。

**人话**：CDC 的前提是 Outbox，Outbox 的前提是 adapter，adapter 还没建——三层依赖，不急。

### 6. hl-framework 独立仓

**EP-001 加载条件**：按需（D8 仓库策略）

**当前状态**：framework/ 目前是 hl-platform 内建子模块（5 starter + BOM），全部为骨架状态（仅 kotlin-stdlib）。Phase 1 填充 starter 实际依赖后，仍然是 hl-platform 单仓内的子模块——因为只有 hl-platform 消费这些 starter。独立仓的条件是：其他仓库也需要消费这些 starter（如 hl-console-native 的服务端、其他微服务）。

**建议**：不加载。Phase 1 维持内建子模块。当出现第二个消费者时独立。

**人话**：只有一个用户的内部库，没必要搬出去单独维护。

### 7. 六模块物理拆分评估

**EP-001 加载条件**：团队 > 10 人时评估

**当前状态**：当前 6 人 AI 驱动团队。Phase 0 的 4 工程模块（identity-org / governance / audit / reasondict）+ gateway 已经通过 Gradle multi-module 物理隔离。EP-001 §4.3 检验标准已满足（移除任一模块，其他编译不受影响）。六大治理能力在概念层完整保留，工程层按需合并。

**建议**：不加载。维持 4+1 工程模块结构。团队增长到 10+ 人或出现并行开发冲突时再拆分。

**人话**：4 个人改 4 个模块够了，拆成 6 个只会增加协调成本。

---

## Phase 1 应聚焦的工作

既然 7 项暂缓约束都不满足加载条件，Phase 1 应聚焦以下方向：

### Phase 1 核心目标：**从纯 domain 到可运行的 HTTP 服务**

| 优先级 | 工作项 | 产出 |
|--------|--------|------|
| **P1-1** | CI runner 激活 | GitHub Actions 自动执行 8 个门禁脚本 |
| **P1-2** | adapter/persistence 层 | JPA Entity + Repository（4 模块） |
| **P1-3** | adapter/web 层 | REST Controller + DTO 映射 |
| **P1-4** | adapter/config 层 | @Configuration + @Bean 显式装配 |
| **P1-5** | starter 填充 | 5 个 framework starter 从骨架到可用 |
| **P1-6** | Gateway HTTP 拦截 | Filter/Interceptor 调用 GatewayOrchestrator |
| **P1-7** | OpenAPI 自动生成 | Springdoc → hl-contracts 同步 |
| **P1-8** | Spring Modulith verify | ApplicationModules.verify() 接入 CI |

### Phase 1 准入条件（建议）

进入 Phase 1 前确认：

- [x] Phase 0 验收通过（12/14 指标通过）
- [x] TECH-STACK-SPEC v3.0 锁版
- [x] reason_codes.csv SSOT 链路完整
- [x] R-0077 跨仓库对齐检查通过
- [ ] CI runner 激活（可并入 Phase 1 P1-1）
- [ ] 创始人裁决：确认 Phase 1 启动

---

*本评估为只读分析。Phase 1 启动需创始人裁决。*
