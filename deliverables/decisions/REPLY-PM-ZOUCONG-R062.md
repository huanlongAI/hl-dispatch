# SKU 版本化方案裁决回复

**回复对象**：邹骢（PM）
**回复日期**：2026-03-20
**裁决编号**：R-062（已录入 RULINGS.md，LOCKED）
**你的提案**：PM-PROPOSAL-SKU-VERSION-001

---

邹骢，

你提交的 SKU 版本化方案建议质量很高，三方案对比清晰，A/B 类字段分类准确。四项待裁决事项的结果如下。

---

## 裁决结果

### Q1：版本化方案 → 方案 C（A 类快照 + B 类复用 Audit）

采用你的推荐方案。理由与你的分析一致：订单回溯 O(1)、版本历史无噪音、与 HK.Audit 天然对齐。

### Q2：A 类字段清单 → 按你提交的清单执行

你列出的 12 个 A 类字段全部确认，无增减：

price / channel_price / floor_price / total_count / consume_count / total_points / validity_value / validity_unit / validity_start / max_use_count / redemption_mode / card_services

**维护规则**：后续新增 A 类字段时，必须同步更新 sku_version 表 DDL 和版本快照逻辑，Gate H（许久明）审计把关。

### Q3：版本历史查看入口 → Phase 2

MVP 只建数据层（sku_version 表 + 写入逻辑 + 查询 API），不做前端版本历史 UI。Phase 2 补充商品详情页「变更历史」面板。

这意味着你在写 MVP 规格时，**不需要**设计版本历史的前端交互，但需要在 PRD 数据规则章节写明版本化的数据模型和触发条件。

### Q4：订单关联 version_no → biz.product 提供接口，biz.order 调用存入

职责分离：

| 能力包 | 职责 |
|--------|------|
| biz.product | 提供 `GET /biz/product/sku/{id}/current-version` 接口，返回当前 version_no |
| biz.order | 下单时调用上述接口，将 `sku_id + version_no` 存入订单记录 |

这意味着 biz.product 的 API 端点清单新增了两个查询接口：
- `GET /biz/product/sku/{id}/current-version`（MVP 交付）
- `GET /biz/product/sku/{id}/versions`（Phase 2 前端入口就绪后启用）

---

## 已完成的文档更新

以下文件已同步更新，你可以直接引用：

| 文件 | 变更 |
|------|------|
| `hl-contracts/governance/RULINGS.md` | R-062 完整裁决正文 + DDL + 变更日志 |
| `hl-dispatch/.../LAUNCH-PRODUCT-CENTER.md` | v1.1 → v1.2：DDL 补充 sku_version 表 + RLS + 索引；API 补充 2 个版本查询端点；版本历史更新 |
| `hl-contracts/governance/PROGRESS.md` | R-062 进度记录 |

---

## 你的下一步行动

**立即**：

1. **更新 MVP 规格**（`PRD-Biz.Product.MVP.v1.0.md`）中的数据规则章节，写入以下内容：
   - 版本化范围定义：A 类字段（12 个）变更时生成新版本
   - 版本表结构：`biz_product.sku_version`，version_no 从 1 开始递增
   - B 类字段历史通过 HK.Audit event_id 追溯
   - 订单关联方式：sku_id + version_no

2. **补充验收用例**（与李旭阳协作），新增以下场景：
   - 修改 A 类字段（如 price）→ 验证 sku_version 新增一条记录，version_no 递增
   - 修改 B 类字段（如名称）→ 验证 sku_version 不新增记录
   - 同时修改 A+B 类字段 → 验证只生成一个新版本，只快照 A 类字段
   - 查询 `current-version` 接口 → 验证返回最新 version_no

**后续（biz.order 启动时）**：

3. 与朱阳协作，确认 biz.order 下单流程中调用 `current-version` 接口的时机和事务边界

---

方案分析做得很扎实，继续保持这个水准。

童正辉
