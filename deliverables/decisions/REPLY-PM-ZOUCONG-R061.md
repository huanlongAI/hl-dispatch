# 商品中心架构反馈回复

**回复对象**：邹骢（PM）
**回复日期**：2026-03-18
**裁决编号**：R-061（已录入 RULINGS.md，LOCKED）

---

邹骢，

你提出的三项架构冲突已全部裁决完毕，LAUNCH-PRODUCT-CENTER.md 已升级至 v1.1。以下是裁决结果和你接下来需要推进的事项。

---

## 一、三项冲突裁决结果

### 冲突 1：SKU-SPU 关系 → 统一 SPU 入口

**裁决**：所有商品必须先建 SPU 再挂 SKU。即使只有单规格，也必须走 SPU → 默认 SKU 链路，不允许裸 SKU 直接入库。

**对你的影响**：MVP 规格中，商品创建流程必须设计为"先创建 SPU → 自动生成默认 SKU"，不要提供"直接创建 SKU"的入口。前端交互也请按此设计——用户感知上可以是一步完成，但底层必须是 SPU + SKU 两层。

### 冲突 2：SPU 定价模型 → SPU 保留建议零售价（只读参考）

**裁决**：SPU 表的 `base_price`（品牌建议零售价）和 `floor_price`（品牌底价）保留，但定义为只读参考，不参与实际交易计算。实际交易价格以 SKU 的 `price` 字段为准。

**对你的影响**：
- 品牌方创建商品时可以填写建议零售价和底价，但这两个字段在订单、结算等下游不会被引用
- SKU 的 `price` 才是真正的交易价格
- `floor_price` 的作用：作为渠道定价的下限约束（见冲突 3）

### 冲突 3：渠道定价权限 → 扩展 can_change_price 策略

**裁决**：原策略仅允许 Claim 持有方（品牌方）设置价格。现扩展为两条策略：

| 操作 | 谁能做 | 约束 |
|------|--------|------|
| 设置品牌价格 | 品牌方（Claim + admin） | 无额外约束 |
| 设置渠道价格 | 合作商户（Cooperate + admin） | 不得低于 SPU floor_price |

**对你的影响**：MVP 规格中需要区分两种定价场景。品牌方设置的是 SKU 的"标准价格"，合作商户设置的是"渠道价格"（channel_price）。验收用例需要覆盖"渠道价低于底价被拒绝"的场景。

---

## 二、团队模型已对齐 v1.2

LAUNCH-PRODUCT-CENTER.md 已同步更新为 v1.2 团队模型：

- **没有后端开发者和独立 QA**——所有 Kotlin 代码由创始人 + AI 生成
- 你（PM）负责定义"做什么"，创始人 + AI 负责"怎么做"，守护者负责审计"做对了吗"
- Sprint 时间线中你的关键节点是 D1（MVP 规格交付）、D2（Facts 定义）、D3（验收用例初稿）、D9-D10（UAT 验证 + 签收）

---

## 三、你的下一步行动

请按以下优先级推进：

**P0（本周）**：

1. **编写 MVP 规格**：`PRD-Biz.Product.MVP.v1.0.md`。重点关注：
   - 商品创建流程必须体现"统一 SPU 入口"（R-061 冲突 1）
   - 定价模块需区分品牌价格 vs 渠道价格（R-061 冲突 3）
   - SPU base_price / floor_price 在 UI 上标注为"参考价"，不要暗示它是交易价格

2. **编写 Facts 定义**：`PRD-Biz.Product.MVP.Facts.v1.0.md`（与创始人协作）

**P1（MVP 规格交付后）**：

3. **编写验收用例**：`PRD-Biz.Product.MVP.Core-Acceptance-Cases.v1.0.md`（与李旭阳协作）。必须覆盖的场景：
   - 单规格商品创建 → 验证自动生成默认 SKU
   - 合作商户设置渠道价 → 验证 floor_price 下限约束
   - 跨租户商品可见性 → Cooperate 关系下只能看到 PUBLISHED 商品

**P2（Sprint 启动前）**：

4. 与朱阳（第二 PM）沟通 biz.product 与后续能力包（biz.inventory / biz.order）的边界确认

---

## 四、参考文件

- 裁决详情：`hl-contracts/governance/RULINGS.md` → R-061
- 更新后的启动规格：`hl-dispatch/deliverables/decisions/LAUNCH-PRODUCT-CENTER.md` v1.1
- 团队协作规范：`hl-dispatch/deliverables/decisions/TEAM-COLLABORATION-SPEC-v1.0.md` v1.2

有问题随时提出。

童正辉
