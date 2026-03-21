# SKU 版本化方案——架构反馈

**回复对象**：邹骢（PM）
**回复日期**：2026-03-20
**你的提案**：PM-PROPOSAL-SKU-VERSION-001

---

邹骢，

你的方案分析做得很扎实，三方案对比逻辑清晰，A/B 类字段的分类也合理。但我在审读后发现，方案建立在一个前提上——"需要新建一张表来记录 SKU 变更历史"——而这个前提在唤龙平台的架构中并不成立。

下面详细说明原因。

---

## 一、你遗漏了 HK.Audit 的一个关键能力

唤龙平台的治理三步范式是 Can → Action → Audit。每一个 key_action（包括商品创建、编辑、上下架、定价变更）在执行时，都必须调用 HK.Audit 签发 event_id，同时写入一个**必填字段** `before_after_ref`：

```yaml
# hk.audit.internal.openapi.v1.yaml — AuditSignRequest
before_after_ref:
  type: string
  description: 变更前后状态引用（oss:// URI）
  pattern: "^oss://.*"
```

这意味着：**每次 SKU 发生任何 key_action 变更，HK.Audit 已经自动存储了变更前后的完整状态快照**（以 JSON 形式存入 OSS，审计记录中保留 URI 引用）。

你在方案文档中提到的两个核心需求：

| 需求 | 你的方案 | HK.Audit 已有能力 |
|------|---------|-------------------|
| 运营查看历史价格和业务参数变更 | sku_version 表 | `before_after_ref` 已记录每次变更的完整前后状态 |
| 查看某字段的变更历史 | 方案 B 的 field_log 或方案 C 的 A 类快照 | 查询 `object_ref = sku:{id}` 的审计事件列表，点击任意事件即可对比前后状态 |

换句话说，**你方案 C 中 sku_version 表要做的事情，HK.Audit 已经在做了，而且做得更完整**——它不区分 A/B 类，所有字段的所有变更都有完整的 before/after 记录。

如果再建一张 sku_version 表，就会出现两个地方记录同一件事的情况，违反了唤龙平台的 SSOT（单一事实源）原则。

---

## 二、订单快照不是 biz.product 的职责

你方案中的另一个核心需求是"某个订单下单时，商品处于什么状态"。你设计的方案是：biz.product 维护 version_no → biz.order 下单时记录 sku_id + version_no → 事后通过 version_no 回查。

这个方案有一个架构问题：**它让订单的完整性依赖于商品侧的版本管理逻辑**。如果 biz.product 的 version_no 递增逻辑有 bug，或者在并发场景下出现 race condition，订单关联的版本就会错误。订单是交易凭证，它的完整性不应该依赖另一个能力包的额外逻辑。

正确的做法是**订单侧快照**——这是淘宝、Shopify、Stripe 等所有成熟交易系统的标准做法：

biz.order 在创建订单时，把下单时刻 SKU 的交易条款直接以 JSONB 冻结到订单行项中：

```sql
-- 这是未来 biz.order 的设计，不是现在要做的
CREATE TABLE biz_order.order_line_item (
    ...
    sku_id        UUID NOT NULL,
    sku_snapshot  JSONB NOT NULL,  -- 下单时 SKU 完整交易状态冻结
    ...
);
```

这样做的好处：

1. **订单自包含**——不需要回查 biz.product 的任何表就能还原下单时的商品状态
2. **零跨能力包依赖**——biz.order 的完整性只依赖自己
3. **biz.product 保持干净**——只管商品生命周期（CRUD + 上下架 + 定价），不承担版本管理

---

## 三、结论

**不需要新建 sku_version 表。** 原因总结：

| 需求 | 正确的解决位置 | 理由 |
|------|---------------|------|
| 运营查看 SKU 变更历史 | HK.Audit（已有） | `before_after_ref` 记录完整前后状态，无需重复建表 |
| 订单回溯下单时商品状态 | biz.order（订单侧快照） | 订单自包含，不依赖商品侧版本号 |
| 已售卡项核销参考原始条款 | biz.order（同上） | 核销时读订单自带的快照，不受商品后续变更影响 |

这意味着 **biz.product 的 DDL 不需要增加任何新表**，你原来设计的 3 张表（product / sku / category）就是完整的。

---

## 四、这对你的 PRD 工作意味着什么

**不需要做的**：
- 不需要在 MVP 规格中设计版本化数据模型
- 不需要写 A/B 类字段分类规则
- 不需要设计版本历史查看入口（Phase 2 也不需要单独做，HK.Audit 的审计查询就是入口）

**需要做的**：
- 在 MVP 规格的"与 HK.Audit 交互"章节，明确写清楚：每个 key_action 的 `before_after_ref` 必须包含 SKU 的完整状态 JSON（不只是变更字段）
- 在验收用例中新增：修改 SKU 价格后 → 通过 HK.Audit 查询该 SKU 的审计事件 → 验证 before_after_ref 包含变更前后的完整状态
- 在 biz.product 的 Out of Scope 中明确注明：**订单时点商品快照由 biz.order 承载**，biz.product 不维护版本号

**你可以带走的认知**：
- 唤龙平台的 HK.Audit 不是简单的"操作日志"，它是一个完整的证据仓库，before_after_ref 存储了每次变更的完整前后状态快照
- 能力包的边界划分原则：谁消费数据，谁负责冻结。订单需要冻结商品状态，这是订单的职责，不是商品的

---

你的分析能力没有问题，三方案对比的逻辑很清晰。这次遗漏的是对 HK.Audit 已有能力的了解——这不是你的问题，是我之前没有把 HK.Audit 的 `before_after_ref` 机制在商品中心启动规格中讲清楚。后续我会在 LAUNCH 模板中补充"HK.Audit 已覆盖能力清单"，避免其他能力包的 PM 踩同样的坑。

接下来请继续推进 MVP 规格的编写，方向调整为上面"需要做的"三点。有问题随时提。

童正辉
