# 商品中心启动规格

## LAUNCH-PRODUCT-CENTER — biz.product 能力包启动实例

---

**文档编号**：LAUNCH-BIZ-PRODUCT-001
**版本**：v1.1
**日期**：2026-03-18
**派生自**：TPL-PM-LAUNCH-001 v1.0（PM 分支业务启动模板）
**适用阶段**：Phase 1 S3(demo 候选) / S4(正式)
**状态**：DRAFT（待创始人裁决确认）

---

## 1. 模块身份卡

| 字段 | 内容 |
|------|------|
| **能力包 ID** | `biz.product` |
| **中文名称** | 商品中心 |
| **一句话定义** | 管理商品的完整生命周期（创建、编辑、上下架、定价、分类），为订单/库存/营销等下游能力包提供商品数据 SSOT；不涉及库存扣减、订单履约、支付结算 |
| **所属 Phase** | Phase 1 — S3 demo 候选（中等复杂度 + 跨租户场景，符合 R-053 S3 选型原则）；或 S4 首批 |
| **优先级批次** | 建议 S4 首批（商品是订单/库存/营销的前置依赖） |
| **PM 负责人** | 邹骢 |
| **代码生成** | 创始人 + AI（R-057：全覆盖模型） |
| **Gate H 审计** | 许久明（代码质量 + 架构合规） |
| **Gate 3 验收** | 李旭阳（端到端业务正确性） |
| **Gate R 发布** | 曾正龙（运维 + 发布验证） |
| **前端** | 待指定（hl-console-native + 消费者端） |

---

## 2. 业务域分析

### 2.1 用户价值链推导

商品是唤龙平台所有交易类业务的起点。用户（商户/品牌方）必须先创建和管理商品，才能进行定价、上架、销售、库存管理。商品中心的价值链位置：

```
商户入驻 → 组织关系建立(HK.OrgLink) → 【商品创建/管理】→ 上架/定价 → 订单 → 库存 → 结算
                                        ↑ 本能力包
```

**目标用户角色**（R-003 网络拓扑）：

| 角色 | TenantSpace 节点类型 | 与 biz.product 的关系 |
|------|---------------------|----------------------|
| 品牌方运营 | Claim 关系（品牌拥有商品） | 创建、编辑、上下架商品 |
| 合作商户 | Cooperate 关系（代销/分销） | 查看可售商品、设置门店价格 |
| 平台管理员 | 平台节点 | 审核商品、管理分类体系 |
| 消费者 | 终端节点 | 浏览商品（只读，通过消费者端） |

**核心价值主张**：

1. 商品数据 SSOT——全平台唯一商品真源，避免多系统商品数据不一致
2. 跨租户商品共享——基于 OrgLink Cooperate 关系实现品牌方→合作商户的商品授权
3. 全链路可审计——商品创建/上下架/价格变更等关键操作可追溯（HK.Audit）

### 2.2 能力包边界

**做（In Scope）**：

- 商品 CRUD（创建、读取、更新、删除/归档）
- 商品分类管理（品类树维护）
- 商品上下架状态管理
- 商品定价（基础价格，非促销价）
- SPU-SKU 二级模型（**统一 SPU 入口，R-061**：所有商品必须先建 SPU 再挂 SKU，即使只有单规格也必须经过 SPU → 默认 SKU 链路，不允许裸 SKU 直接入库）
- 商品图片/富文本描述绑定（存储引用，非文件服务本身）
- 跨租户商品授权查看（基于 OrgLink Cooperate）

**不做（Out of Scope）**：

- 库存管理（`biz.inventory` 承载）
- 订单关联（`biz.order` 承载）
- 促销/优惠券定价（`biz.promotion` 承载）
- 商品搜索引擎（Phase 2+ ES/OpenSearch）
- 文件存储服务（独立基础设施）
- 商品推荐算法（D 域数据平台）

### 2.3 与 HK 治理层交互矩阵

| HK 模块 | 交互方式 | 说明 |
|---------|---------|------|
| HK.Identity | ☑ 消费 | 操作人身份解析（principal_hlid） |
| HK.OrgLink | ☑ 消费 | 跨租户商品可见性——判断 Cooperate 关系是否存在；商品归属的 TenantSpace 确认 |
| HK.Policy | ☑ 消费 | 商品创建/上下架/定价变更的 Can 预检——策略引擎判定操作人是否有权 |
| HK.Consent | ☐ 无 | 商品管理不涉及授权同意流程（Phase 1 暂不需要） |
| HK.Audit | ☑ 消费（必选） | 全部 key_action 签发 event_id + 审计记录 |
| HK.ReasonDict | ☑ 消费（必选） | 商品相关 reason_code 注册与引用 |

---

## 3. 契约清单（hl-contracts 交付物）

### 3.1 reason_codes 注册

| code | constant | module | category | description |
|------|----------|--------|----------|-------------|
| `biz.product.create.can` | PRODUCT_CREATE_CAN | product | can | 商品创建权限检查标识 |
| `biz.product.create.success` | PRODUCT_CREATE_SUCCESS | product | outcome | 商品创建成功 |
| `biz.product.create.denied.no_permission` | PRODUCT_CREATE_DENIED_NO_PERM | product | deny | 无商品创建权限 |
| `biz.product.create.denied.tenant_mismatch` | PRODUCT_CREATE_DENIED_TENANT | product | deny | 租户空间不匹配 |
| `biz.product.create.denied.category_invalid` | PRODUCT_CREATE_DENIED_CAT | product | deny | 商品分类无效 |
| `biz.product.update.can` | PRODUCT_UPDATE_CAN | product | can | 商品编辑权限检查标识 |
| `biz.product.update.success` | PRODUCT_UPDATE_SUCCESS | product | outcome | 商品编辑成功 |
| `biz.product.update.denied.no_permission` | PRODUCT_UPDATE_DENIED_NO_PERM | product | deny | 无商品编辑权限 |
| `biz.product.update.denied.locked` | PRODUCT_UPDATE_DENIED_LOCKED | product | deny | 商品已锁定不可编辑 |
| `biz.product.publish.can` | PRODUCT_PUBLISH_CAN | product | can | 商品上架权限检查标识 |
| `biz.product.publish.success` | PRODUCT_PUBLISH_SUCCESS | product | outcome | 商品上架成功 |
| `biz.product.publish.denied.incomplete` | PRODUCT_PUBLISH_DENIED_INCOMPLETE | product | deny | 商品信息不完整，不可上架 |
| `biz.product.unpublish.can` | PRODUCT_UNPUBLISH_CAN | product | can | 商品下架权限检查标识 |
| `biz.product.unpublish.success` | PRODUCT_UNPUBLISH_SUCCESS | product | outcome | 商品下架成功 |
| `biz.product.price.can` | PRODUCT_PRICE_CAN | product | can | 价格变更权限检查标识 |
| `biz.product.price.success` | PRODUCT_PRICE_SUCCESS | product | outcome | 价格变更成功 |
| `biz.product.price.denied.below_floor` | PRODUCT_PRICE_DENIED_FLOOR | product | deny | 价格低于底价限制 |
| `biz.product.archive.can` | PRODUCT_ARCHIVE_CAN | product | can | 商品归档权限检查标识 |
| `biz.product.archive.success` | PRODUCT_ARCHIVE_SUCCESS | product | outcome | 商品归档成功 |

### 3.2 OpenAPI 契约

文件名：`biz.product.internal.openapi.v1.yaml`

**端点清单**：

| HTTP | 路径 | 操作 | 类型 | key_action |
|------|------|------|------|-----------|
| POST | `/biz/product/create.can` | 商品创建 Can 预检 | Can | false |
| POST | `/biz/product/create` | 创建商品（SPU + 默认 SKU） | Action | true |
| POST | `/biz/product/update.can` | 商品编辑 Can 预检 | Can | false |
| POST | `/biz/product/update` | 编辑商品信息 | Action | true |
| POST | `/biz/product/publish.can` | 商品上架 Can 预检 | Can | false |
| POST | `/biz/product/publish` | 上架商品 | Action | true |
| POST | `/biz/product/unpublish.can` | 商品下架 Can 预检 | Can | false |
| POST | `/biz/product/unpublish` | 下架商品 | Action | true |
| POST | `/biz/product/price.can` | 定价变更 Can 预检 | Can | false |
| POST | `/biz/product/price` | 变更价格 | Action | true |
| POST | `/biz/product/archive.can` | 归档 Can 预检 | Can | false |
| POST | `/biz/product/archive` | 归档商品 | Action | true |
| GET | `/biz/product/list` | 查询商品列表 | Query | false |
| GET | `/biz/product/{id}` | 查询商品详情 | Query | false |
| GET | `/biz/product/category/tree` | 查询分类树 | Query | false |

### 3.3 capabilities.yaml 注册

```yaml
- capability_id: biz.product
  version: v1
  routes:
    - path: /biz/product/**
      methods: [POST, GET]
      route_to: internal
  feature_toggle: biz_product_enabled
  required_hk:
    - hk.identity
    - hk.orglink
    - hk.policy
    - hk.audit
    - hk.reasondict
```

### 3.4 PRD 文档集

| 文档 | 文件名 | 负责人 | 状态 |
|------|--------|--------|------|
| MVP 规格 | `PRD-Biz.Product.MVP.v1.0.md` | PM（邹骢） | 待编写 |
| Facts 定义 | `PRD-Biz.Product.MVP.Facts.v1.0.md` | PM + 创始人 | 待编写 |
| Decision Trace | `PRD-Biz.Product.MVP.Decision-Trace.v1.0.md` | 创始人+AI | 待编写 |
| API Return Codes | `PRD-Biz.Product.MVP.API-Return-Codes.v1.0.md` | 创始人+AI | 待编写 |
| 验收用例 | `PRD-Biz.Product.MVP.Core-Acceptance-Cases.v1.0.md` | PM + Gate 3（李旭阳） | 待编写 |
| Dev Checklist | `PRD-Biz.Product.MVP.Dev-Checklist.v1.0.md` | 创始人+AI | 待编写 |

---

## 4. 代码架构规格

### 4.1 模块结构

```
hl-platform/
├── contract/src/main/kotlin/hk/biz/product/
│   ├── CreateProductPort.kt
│   ├── CreateProductFacts.kt
│   ├── CreateProductResult.kt
│   ├── UpdateProductPort.kt
│   ├── UpdateProductFacts.kt
│   ├── UpdateProductResult.kt
│   ├── PublishProductPort.kt
│   ├── PublishProductFacts.kt
│   ├── PublishProductResult.kt
│   ├── UnpublishProductPort.kt
│   ├── UnpublishProductFacts.kt
│   ├── UnpublishProductResult.kt
│   ├── ChangeProductPricePort.kt
│   ├── ChangeProductPriceFacts.kt
│   ├── ChangeProductPriceResult.kt
│   ├── ArchiveProductPort.kt
│   ├── ArchiveProductFacts.kt
│   ├── ArchiveProductResult.kt
│   ├── ProductQueryPort.kt
│   └── event/
│       └── ProductEvents.kt           (sealed class: Created, Updated, Published, ...)
│
├── kernel/biz-product/
│   ├── build.gradle.kts
│   └── src/
│       ├── main/kotlin/hk/bizproduct/
│       │   ├── domain/                 ← P0-1: 零 Spring/零 JPA
│       │   │   ├── CanCreateProductService.kt
│       │   │   ├── CreateProductService.kt
│       │   │   ├── CanUpdateProductService.kt
│       │   │   ├── UpdateProductService.kt
│       │   │   ├── CanPublishProductService.kt
│       │   │   ├── PublishProductService.kt
│       │   │   ├── CanUnpublishProductService.kt
│       │   │   ├── UnpublishProductService.kt
│       │   │   ├── CanChangeProductPriceService.kt
│       │   │   ├── ChangeProductPriceService.kt
│       │   │   ├── CanArchiveProductService.kt
│       │   │   ├── ArchiveProductService.kt
│       │   │   └── model/
│       │   │       ├── Product.kt      (domain model, NOT JpaEntity)
│       │   │       ├── Sku.kt
│       │   │       ├── Category.kt
│       │   │       └── ProductStatus.kt  (enum: DRAFT, PUBLISHED, UNPUBLISHED, ARCHIVED)
│       │   └── adapter/
│       │       ├── persistence/
│       │       │   ├── JpaProductRepository.kt
│       │       │   ├── ProductJpaEntity.kt
│       │       │   ├── SkuJpaEntity.kt
│       │       │   └── CategoryJpaEntity.kt
│       │       ├── web/
│       │       │   └── ProductController.kt
│       │       └── config/
│       │           └── BizProductConfiguration.kt
│       └── test/kotlin/hk/bizproduct/domain/
│           ├── CreateProductServiceTest.kt    ← 5 必过
│           ├── PublishProductServiceTest.kt   ← 5 必过
│           ├── ChangeProductPriceServiceTest.kt ← 5 必过
│           └── ArchiveProductServiceTest.kt   ← 5 必过
```

### 4.2 key_action 与五必过测试映射

| key_action | 5 测试文件 | 预计用例数 |
|-----------|-----------|----------|
| create | CreateProductServiceTest.kt | 5 + 并发幂等 2 |
| update | UpdateProductServiceTest.kt | 5 + 锁定状态 1 |
| publish | PublishProductServiceTest.kt | 5 + 完整性校验 2 |
| unpublish | UnpublishProductServiceTest.kt | 5 |
| price | ChangeProductPriceServiceTest.kt | 5 + 底价校验 1 |
| archive | ArchiveProductServiceTest.kt | 5 |

**总计最小测试用例**：6 × 5 = 30（五必过）+ 6（业务场景）= 36 用例

### 4.3 数据库设计

```sql
CREATE SCHEMA IF NOT EXISTS biz_product;

-- SPU 表
CREATE TABLE biz_product.product (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID            NOT NULL,
    category_id     UUID            NOT NULL,
    name            VARCHAR(256)    NOT NULL,
    description     TEXT,
    image_urls      JSONB           DEFAULT '[]'::jsonb,
    status          VARCHAR(32)     NOT NULL DEFAULT 'DRAFT',
    base_price      NUMERIC(12,2),   -- 品牌建议零售价（只读参考，不参与交易，R-061）
    floor_price     NUMERIC(12,2),   -- 品牌底价（只读参考，R-061）
    event_id        UUID,
    reason_code     VARCHAR(128),
    created_by      UUID            NOT NULL,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- SKU 表
CREATE TABLE biz_product.sku (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID            NOT NULL,
    product_id      UUID            NOT NULL REFERENCES biz_product.product(id),
    sku_code        VARCHAR(64)     NOT NULL,
    attributes      JSONB           NOT NULL DEFAULT '{}'::jsonb,
    price           NUMERIC(12,2)   NOT NULL,
    status          VARCHAR(32)     NOT NULL DEFAULT 'DRAFT',
    event_id        UUID,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, sku_code)
);

-- 分类表
CREATE TABLE biz_product.category (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID            NOT NULL,
    parent_id       UUID,
    name            VARCHAR(128)    NOT NULL,
    sort_order      INT             NOT NULL DEFAULT 0,
    level           INT             NOT NULL DEFAULT 1,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- 索引
CREATE INDEX idx_product_tenant ON biz_product.product(tenant_id);
CREATE INDEX idx_product_category ON biz_product.product(category_id);
CREATE INDEX idx_product_status ON biz_product.product(tenant_id, status);
CREATE INDEX idx_sku_product ON biz_product.sku(product_id);
CREATE INDEX idx_category_parent ON biz_product.category(parent_id);

-- RLS 策略
ALTER TABLE biz_product.product ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_product ON biz_product.product
    USING (tenant_id = current_setting('app.current_tenant')::uuid);

ALTER TABLE biz_product.sku ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_sku ON biz_product.sku
    USING (tenant_id = current_setting('app.current_tenant')::uuid);

ALTER TABLE biz_product.category ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_category ON biz_product.category
    USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

---

## 5. 跨租户场景设计

> biz.product 的跨租户场景是 S3 demo 选型的关键加分项（R-053：至少 1 个跨租户裁决场景）。

### 5.1 场景：品牌方授权合作商户查看商品

```
品牌方 A (TenantSpace)
    ├── Claim → 商品 P1, P2, P3
    └── Cooperate → 合作商户 B

合作商户 B 发起 GET /biz/product/list
    → Gateway → HK.OrgLink 判断 B 与 A 是否存在 Cooperate 关系
    → 存在 → 返回 A 的已上架商品（PUBLISHED 状态）
    → 不存在 → 返回空列表（不报错，静默隔离）
```

### 5.2 策略规则

| 操作 | 策略 | HK.Policy 规则 |
|------|------|----------------|
| 创建商品 | 仅 Claim 关系持有方 | `can_create_product: edge_type == CLAIM AND role IN [owner, admin]` |
| 编辑商品 | 仅 Claim 关系持有方 | `can_update_product: edge_type == CLAIM AND product.tenant_id == caller.tenant_id` |
| 上架/下架 | 仅 Claim 关系持有方 + admin 角色 | `can_publish_product: edge_type == CLAIM AND role == admin` |
| 查看商品 | Claim 持有方 + Cooperate 合作方 | `can_view_product: edge_type IN [CLAIM, COOPERATE] AND product.status == PUBLISHED` |
| 设置品牌价格 | 仅 Claim 关系持有方 + admin 角色 | `can_change_price: edge_type == CLAIM AND role == admin` |
| 设置渠道价格 | Cooperate 合作方 + admin 角色 | `can_change_channel_price: edge_type == COOPERATE AND role == admin AND target == SKU.channel_price`（R-061：渠道价不得低于 SPU floor_price） |

---

## 6. Sprint 时间线（建议）

> 以 2 周 Sprint 为例（S4 首批，非 S3 demo）。

| 天 | PM（邹骢） | 创始人+AI | Gate H（许久明） | Gate 3（李旭阳） | 运维（曾正龙） | 前端 |
|----|-----------|-----------|------------------|------------------|----------------|------|
| D1 | MVP 规格交付 | 审读 MVP + 契约设计 | — | — | Schema DDL | 交互线框 |
| D2 | Facts 定义 + reason_codes PR | contract 层接口 | — | — | RLS + feature_toggle | — |
| D3 | 验收用例初稿 | OpenAPI + capabilities.yaml | 评审契约 | 评审验收用例 | Grafana 模板 | 页面设计确认 |
| D4 | — | 完整实现（domain + adapter + DDL + 测试） | — | — | — | API 对接开始 |
| D5 | — | 完整实现继续 | — | — | Flyway 脚本 | API 对接 |
| D6 | — | 实现完成 + CI green | Gate H 代码审计 | — | — | API 对接 |
| D7 | — | 审计修复 | Gate H 复审 | Gate 3 端到端验收 | — | 联调 |
| D8 | — | 联调 + 五必过测试通过 | — | Gate 3 业务回归 | Outbox 监控 | 审计回放集成 |
| D9 | UAT 验证 | bug fix | — | — | 上线 SOP | bug fix |
| D10 | UAT 签收 | Dev Checklist ✅ | 签收确认 | 签收确认 | 灰度发布 | 端到端截图 |

---

## 7. S3 Demo 适用性评估

> R-053 要求 S3 demo 包为中等复杂度 + 至少 1 个跨租户裁决场景。

| 评估维度 | biz.product 评分 | 说明 |
|---------|-----------------|------|
| key_action 数量 | 6 个（create/update/publish/unpublish/price/archive）| 中等，不会太简单（验不出 DX 问题）也不会太复杂（S3 拖期） |
| 跨租户场景 | 1 个核心场景（品牌方→合作商户商品可见性） | 满足 R-053 要求 |
| HK 模块消费 | 5/6（除 Consent 外全部消费） | 验证面广 |
| 下游依赖 | 无（商品是其他能力包的上游） | 可独立验证，不被阻塞 |
| 数据模型复杂度 | SPU-SKU 二级 + 分类树 | 中等 |
| 总评 | **适合作为 S3 demo 包** | 复杂度适中，覆盖面广，无外部依赖 |

---

## 8. 风险与缓解

| 风险 | 等级 | 缓解 |
|------|------|------|
| SPU-SKU 模型过度设计 | 中 | MVP 先做最简 1:N 关系，属性用 JSONB 灵活扩展 |
| 商品分类体系跨租户共享 vs 隔离 | 中 | Phase 1 先做租户隔离分类；平台级共享分类延后 |
| 商品图片存储依赖 | 低 | Phase 0 只存 URL 引用，文件服务独立规划 |
| 跨租户商品可见性性能 | 低 | Phase 0 量级下 OrgLink 查询 + PG 索引足够 |
| PM 商品域经验不足 | 中 | 参考旧系统 PM-A01/A02/A03 作为输入（R-015 已标注降级为参考） |

---

## 9. 启动检查清单

### 9.1 裁决就绪

- [ ] `biz.product` 已在 R-053 S2/S4 裁决中确认为首批能力包
- [ ] 优先级批次已锁定（创始人裁决）
- [ ] 与 biz.inventory / biz.order 边界已确认（PM 联合评审）

### 9.2 契约就绪

- [ ] 19 条 reason_codes PR 已 merge 到 hl-contracts
- [ ] `biz.product.internal.openapi.v1.yaml` 已提交
- [ ] capabilities.yaml 已注册 `biz.product` 路由
- [ ] PRD-Biz.Product.MVP.v1.0.md 已提交

### 9.3 代码就绪

- [ ] `contract/src/main/kotlin/hk/biz/product/` 接口层已 merge
- [ ] `kernel/biz-product/` 模块骨架已创建
- [ ] `settings.gradle.kts` 已 include `kernel:biz-product`
- [ ] `build.gradle.kts` 依赖仅 `:contract` + Spring adapter

### 9.4 基础设施就绪

- [ ] PG18 schema `biz_product` 已创建（dev 环境）
- [ ] 3 张表 RLS policy 已配置
- [ ] `biz_product_enabled = false` feature_toggle 已配置
- [ ] Grafana dashboard 已创建（请求量/延迟/错误率/审计量）

### 9.5 团队就绪

- [x] PM 已指定（邹骢）
- [x] 代码生成模型已确认（创始人+AI，R-057）
- [x] Gate H / Gate 3 / Gate R 审计人已确认（许久明 / 李旭阳 / 曾正龙）
- [ ] 前端 Owner 已指定
- [ ] Sprint 周期已确定
- [ ] GitHub Issue 已创建（hl-dispatch task-assign 模板）
- [ ] Kickoff 会议完成

---

## 10. 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-17 | v1.0 | DRAFT — 基于 TPL-PM-LAUNCH-001 首个实例，待创始人裁决确认 |
| 2026-03-18 | v1.1 | R-061 裁决应用：统一 SPU 入口 + SPU 价格只读参考 + Cooperate 渠道定价策略；v1.2 团队模型对齐（创始人+AI 全覆盖，无后端/QA 角色） |
