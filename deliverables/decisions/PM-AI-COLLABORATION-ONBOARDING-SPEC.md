# PM AI 驱动协作接入规格

## PM-AI-COLLABORATION-ONBOARDING-SPEC v2.0

---

**文档编号**：PM-ONBOARD-SPEC-001
**版本**：v2.0
**日期**：2026-03-30
**状态**：RULED（创始人已裁决 D-1~D-5，2026-03-30）
**派生链**：TEAM-COLLABORATION-SPEC v1.2 → R-056/R-057/R-058 → GPT 范式讨论 → PRD-REDEFINITION-SPEC v2.0 → 创始人 2026-03-30 纠正 → 本文档
**适用对象**：邹骢、朱阳（PM 角色，产线责任人）

---

## 0. 推导声明

| 编号 | 输入 | 关键约束 |
|------|------|----------|
| I-1 | TEAM-COLLABORATION-SPEC v1.2 LOCKED | 三环模型、协作流程、权限矩阵 |
| I-2 | R-056/R-057/R-058 LOCKED | AI 100% 代码、不设业务开发者、不设独立 QA |
| I-3 | GPT 范式讨论（2026-03-30） | 两套治理宇宙、四层质量保障 |
| I-4 | MULTI-NODE-COWORK-SPEC v0.3 | Write-Owner 模型、跨域写入协议 |
| I-5 | PRD-REDEFINITION-SPEC v2.0 | PM = 产线责任人，Cap-Spec 工件集，工具/平台不限定 |
| I-6 | PM 交互先例（R-061/R-062） | 邹骢已有效参与架构讨论 |
| I-7 | 创始人 2026-03-30 纠正 | PM 是产线责任人，驱动规格→AI 编码→测试→验收完整闭环 |

**推导逻辑**：

```
创始人定义上游（唤龙契约 + 运行态架构 + 治理裁决）
  → PM 接入上游，成为能力包/产品线的完整责任人
  → PM 自主驱动：Cap-Spec 规格 → AI 编码 → 测试 → 业务验收
  → 交付技术验收官（架构评审 + 代码审计）
  → 创始人里程碑签收
  → 工具与 AI 平台不作强制限定
```

---

## 1. PM 角色定位

### 1.1 核心定位：产线责任人

PM 在所负责的能力包/产品线范围内，是**完整的产线责任人**。PM 基于创始人已给定的上游——唤龙运行态治理体系与契约法典——接入开始，全权驱动规格驱动开发的完整闭环。

| 流程步骤 | PM 角色 | 说明 |
|---------|--------|------|
| ① 接入上游 | **消费者** | 接入创始人已定义的 contracts + governance |
| ② 规格定义 | **驱动者** | 编写 Cap-Spec 工件集（能力规格 + 验收场景 + 业务码） |
| ③ AI 编码 | **驱动者** | PM 使用 AI 完成代码实现（工具/平台自主选择） |
| ④ 测试 | **驱动者** | 编写测试用例，驱动 AI 生成测试代码 |
| ⑤ 业务验收 | **执行者** | 基于验收场景集逐条验证 |
| ⑥ 技术验收 | **交付者** | 交技术验收官把关审计 |
| ⑦ 签收 | — | 创始人里程碑签收 |

### 1.2 与创始人的分界

| 层面 | 创始人（上游） | PM（产线责任人） |
|------|-------------|----------------|
| 唤龙契约 hl-contracts | **主导定义与裁决** | 消费与引用 |
| 运行态架构 | **主导设计与决策** | 在架构内实现 |
| 能力包立项 | **裁决** | 推荐与建议 |
| 能力包规格 | 审批 | **编写与驱动** |
| AI 编码 | — | **PM 驱动 AI 完成** |
| 测试用例 | — | **PM 编写与驱动** |
| 业务验收 | 里程碑签收 | **PM 执行** |
| 技术验收 | — | 交付技术验收官 |

### 1.3 硬边界

| 边界 | 含义 |
|------|------|
| **上游不可改** | PM 不可直接修改 hl-contracts Tier 1 SSOT（需走 PR + 创始人审批） |
| **技术验收不可跳过** | PM 交付物必须经技术验收官架构评审 + 代码审计 |
| **产线不可越界** | PM 只在自己负责的能力包范围内行使驱动权 |
| **治理规则不可自创** | 能力包内不得发明不在 contracts 中的治理规则 |

---

## 2. PM 权限矩阵

### 2.1 PM 可自主执行（无需审批）

| 动作 | 范围 | 产出 |
|------|------|------|
| 编写 Cap-Spec-1 能力规格书 | 已裁决立项的能力包 | Cap-Spec-{Domain}.{Module}.v1.0.md |
| 编写 Cap-Spec-2 验收场景集 | 已裁决立项的能力包 | Cap-Spec-{Domain}.{Module}.Acceptance.v1.0.md |
| 提交 Cap-Spec-3 业务码 PR | 已裁决立项的能力包 | reasoncodes.csv PR |
| 驱动 AI 编码 | 已裁决立项的能力包 | 代码实现 + 测试 |
| 执行业务验收 | 已裁决立项的能力包 | 验收记录 |
| 创建 hl-dispatch Issue | doc-review / task-assign | Issue |
| 提出架构反馈 | 任何已读文档 | hl-dispatch Issue (decision-request) |
| 提交提案 | 任何业务域问题 | PM-PROPOSAL-{ID}.md |
| 选择规格驱动工具 | 自身工作 | — |
| 选择 AI 编码平台 | 自身工作 | — |

### 2.2 PM 需创始人审批

| 动作 | 审批人 | 流程 |
|------|--------|------|
| 提交 hl-contracts PR（reason_codes / Cap-Spec） | **创始人 + Gate H** | PM 提交 PR → 审批 → merge |
| 发起 decision-request | **创始人** | PM 提交 Issue → 创始人裁决 |
| 推荐能力包立项 | **创始人** | PM 推荐 → Gate H 评估 → 创始人裁决 |

### 2.3 PM 不可执行

| 禁止动作 | 原因 |
|---------|------|
| 直接 merge 任何 PR | 仅创始人可 merge |
| 修改 RULINGS.md | 仅创始人可写入 |
| 修改 glossary.md | Gate H 守护术语 SSOT |
| 修改 CI 门禁脚本 | 创始人主导 |
| 覆盖已 LOCKED 的 reason_code | 需创始人新 Ruling |
| 跳过技术验收官审计 | 执行者与审计者不同源 |

---

## 3. PM 接入 SOP

### Phase 1：GitHub 权限配置（~15 分钟，创始人执行）

| # | 动作 | 验证 |
|---|------|------|
| 1.1 | 确认 PM GitHub 账号：邹骢 @zoucong121、朱阳 @{TBD} | 账号可访问 |
| 1.2 | 邀请加入 huanlongAI GitHub Organization | org 成员列表可见 |
| 1.3 | 配置仓库权限（见 §3.1 权限表） | PM 可 clone 指定仓库 |
| 1.4 | 更新 TEAM.yml 录入朱阳信息 | TEAM.yml 含两名 PM |

#### 3.1 GitHub 仓库权限表

| 仓库 | PM 权限级别 | 说明 |
|------|:---------:|------|
| **hl-contracts** | Write | PM 提交 Cap-Spec + reason_codes PR，不可直接 merge |
| **hl-dispatch** | Write | PM 创建 Issue + 提交协调文档 PR |
| **hl-platform** | Write | PM 驱动 AI 编码后提交代码 PR，不可直接 merge |
| **hl-framework** | Read | PM 参考 Starter 定义 |
| **hl-factory** | Read | PM 参考 AI-Ops |
| **hl-console-native** | Write | PM 驱动 AI 编码后提交代码 PR（如涉及控制台能力） |

### Phase 2：PM 本地环境配置（~20 分钟，PM 自行执行）

| # | 动作 | 验证 |
|---|------|------|
| 2.1 | 安装 Git | `git --version` |
| 2.2 | 配置 Git 身份 | `git config user.name` / `git config user.email` |
| 2.3 | 配置 SSH 密钥 | `ssh -T git@github.com` |
| 2.4 | Clone 工作仓库 | 见下方脚本 |
| 2.5 | 选择并配置规格驱动工具（自主选择） | 可打开并编写 .md 文件 |
| 2.6 | 选择并配置 AI 编码平台（自主选择） | AI 可读取仓库上下文 |

```bash
# PM 仓库克隆脚本
mkdir -p ~/huanlong-pm && cd ~/huanlong-pm

# 可写仓库（PM 提交 PR）
git clone git@github.com:huanlongAI/hl-contracts.git
git clone git@github.com:huanlongAI/hl-dispatch.git
git clone git@github.com:huanlongAI/hl-platform.git
git clone git@github.com:huanlongAI/hl-console-native.git

# 只读仓库（参考用）
git clone git@github.com:huanlongAI/hl-framework.git
git clone git@github.com:huanlongAI/hl-factory.git
```

### Phase 3：知识体系学习（~2 小时，PM 自行阅读）

| 优先级 | 文档 | 路径 | 学习目标 |
|:-----:|------|------|----------|
| P0 | PRD-REDEFINITION-SPEC v2.0 | hl-dispatch/deliverables/decisions/ | 理解 PM 产线责任人定位、Cap-Spec 工件集 |
| P0 | TEAM-COLLABORATION-SPEC v1.2 | hl-dispatch/deliverables/decisions/ | 理解角色定义、协作流程、权限矩阵 |
| P0 | PM-BRANCH-LAUNCH-TEMPLATE v1.0 | hl-dispatch/deliverables/decisions/ | 掌握能力包启动全流程模板 |
| P0 | LAUNCH-PRODUCT-CENTER v1.2 | hl-dispatch/deliverables/decisions/ | 学习首个实例（biz.product） |
| P1 | REPLY-PM-ZOUCONG-R061/R062 | hl-dispatch/deliverables/decisions/ | 理解架构反馈→裁决的交互模式 |
| P1 | hl-contracts/glossary/glossary.md | hl-contracts/glossary/ | 掌握业务术语标准定义 |
| P1 | hl-contracts/prd/README.md | hl-contracts/prd/ | 理解能力规格存放规范 |
| P2 | SAAC-HL-001 v1.1（§1.3） | hl-contracts/governance/ | 理解为什么不设业务开发者 |

### Phase 4：首次任务演练（~1 小时，PM + 创始人）

| # | 动作 | 产出 | 验证 |
|---|------|------|------|
| 4.1 | PM 创建一个 doc-review Issue | hl-dispatch Issue | Issue 格式正确 |
| 4.2 | PM 创建一个 decision-request Issue | hl-dispatch Issue | 创始人能接收并回复 |
| 4.3 | PM 编写一份简化的 Cap-Spec-1（对已有能力包） | Cap-Spec 文档 | 格式符合规范 |
| 4.4 | PM 使用自选 AI 平台完成一次小规模代码生成 | 代码 PR | PR 可提交、CI 可通过 |
| 4.5 | 创始人 review + merge（或打回） | merge 结果 | PM 理解完整 PR 生命周期 |

### Phase 5：验证清单（全部通过 = PM 就绪）

| # | 检查项 | 验证方式 | 期望结果 |
|---|--------|---------|----------|
| 5.1 | GitHub org 成员 | huanlongAI 成员列表 | PM 可见 |
| 5.2 | hl-contracts clone | `git remote -v` | 正确 URL |
| 5.3 | hl-platform clone | `git remote -v` | 正确 URL（PM 需要写代码 PR） |
| 5.4 | Issue 创建成功 | hl-dispatch Issues 列表 | Issue 可见 |
| 5.5 | PR 提交成功 | hl-contracts PR 列表 | PR 可见 |
| 5.6 | AI 编码环境可用 | PM 演示 AI 生成代码 | 可生成并提交 |
| 5.7 | PM 能说出 Cap-Spec 三件套名称和用途 | 口头/文字确认 | 能力规格 + 验收场景 + 业务码 PR |
| 5.8 | PM 能说出 reason_code 命名规则 | 口头/文字确认 | `biz.{module}.{action}.{outcome}` |
| 5.9 | PM 能说出"产线责任人"的权责边界 | 口头/文字确认 | 驱动闭环但不可改上游、不可跳过技术验收 |
| 5.10 | TEAM.yml 两名 PM 均已录入 | 文件内容 | 邹骢 + 朱阳 |

---

## 4. PM 日常工作流

### 4.1 能力包全生命周期中的 PM 驱动流程

```
创始人裁决立项（RULINGS.md）— PM 接入上游
    │
    ▼
PM 编写 Cap-Spec-1 能力规格书                              ← Sprint D1
PM 编写 Cap-Spec-2 验收场景集                              ← Sprint D2
PM 提交 Cap-Spec-3 业务码 PR (reasoncodes.csv)             ← Sprint D2
    │
    ▼  PM 提交 Cap-Spec PR → 创始人 + Gate H review → merge
    │
PM 驱动 AI 编码（工具/平台自主选择）                         ← Sprint D3-D7
PM 编写/驱动 AI 生成测试用例                                ← Sprint D5-D7
    │
    ▼  PM 提交代码 PR → CI 门禁
    │
PM 执行业务验收（基于 Cap-Spec-2 逐条验证）                  ← Sprint D8-D9
PM 签字（GitHub Issue Comment）
    │
    ▼
技术验收官把关审计（架构评审 + 代码审计）                     ← Sprint D9-D10
    │
    ▼
创始人里程碑签收
```

### 4.2 PM 与创始人的交互模式

| 场景 | PM 动作 | 载体 | 创始人响应 |
|------|---------|------|------------|
| 需要上游裁决 | 提交 decision-request Issue | hl-dispatch | 裁决回复（REPLY-PM-{NAME}-R{xxx}.md） |
| 方案提议 | 提交 PM-PROPOSAL-{ID}.md | hl-dispatch PR | 裁决 + Ruling |
| 规格审批 | 提交 Cap-Spec PR | hl-contracts | 创始人 review + merge |
| 代码审批 | 提交代码 PR | hl-platform | 创始人/技术验收官 review |
| 边界争议 | 与 Gate H 讨论后升级 | hl-dispatch Issue | 创始人仲裁 |

### 4.3 跨仓库变更协同

PM 的规格驱动工作涉及多个仓库：

| 步骤 | 仓库 | PM 动作 | 先决条件 |
|------|------|---------|----------|
| 1 | hl-dispatch | 提交 LAUNCH-{MODULE}.md（启动规格） | 创始人已裁决立项 |
| 2 | hl-contracts | 提交 Cap-Spec + reason_codes PR | Step 1 merge 后 |
| 3 | hl-platform | PM 驱动 AI 编码，提交代码 PR | Step 2 PR merge 后 |
| 4 | — | 技术验收官审计 | Step 3 PR 提交后 |

---

## 5. 邹骢当前状态与行动项

### 5.1 已完成

| 项目 | 状态 | 证据 |
|------|:----:|------|
| GitHub 账号注册（@zoucong121） | ✅ | TEAM.yml |
| TEAM.yml 录入 | ✅ | hl-dispatch/TEAM.yml |
| biz.product 能力包分配 | ✅ | LAUNCH-PRODUCT-CENTER v1.2 |
| 架构反馈交互（R-061） | ✅ | REPLY-PM-ZOUCONG-R061.md |
| 方案提案交互（R-062） | ✅ | REPLY-PM-ZOUCONG-R062.md |

### 5.2 待完成

| 优先级 | 动作 | 产出 | 依赖 |
|:-----:|------|------|------|
| P0 | 编写 Cap-Spec-Biz.Product 能力规格书 | Cap-Spec-Biz.Product.v1.0.md | R-061/R-062 裁决已完成 |
| P0 | 编写 Cap-Spec-Biz.Product 验收场景集 | Cap-Spec-Biz.Product.Acceptance.v1.0.md | 与创始人协作 |
| P1 | 提交 19 条 reason_codes PR | reasoncodes.csv PR | Cap-Spec 完成后 |
| P1 | 驱动 AI 编码实现 biz.product | hl-platform 代码 PR | Cap-Spec merge 后 |
| P2 | 与朱阳沟通后续能力包边界 | 能力包清单讨论 | S2 中期启动 |

---

## 6. 朱阳接入行动项

| 优先级 | 动作 | 负责人 | 依赖 |
|:-----:|------|--------|------|
| P0 | 确认 GitHub 用户名 | **朱阳** | — |
| P0 | 邀请加入 huanlongAI org | **创始人** | 朱阳 GitHub 账号 |
| P0 | 更新 TEAM.yml 录入朱阳信息 | **NODE-A** | org 邀请完成 |
| P1 | 执行 Phase 2-3（本地环境 + AI 平台 + 知识学习） | **朱阳** | GitHub 权限到位 |
| P1 | 执行 Phase 4（首次任务演练，含 AI 编码验证） | **朱阳 + 创始人** | 知识学习完成 |
| P2 | 分配能力包（S2 中期讨论后） | **创始人** | S2 启动 |

---

## 7. 对齐验证

| 锁定结论 | 是否对齐 | 说明 |
|---------|:------:|------|
| 双治理宇宙分离（tzhOS vs huanlong） | ✅ | PM 仅接入 huanlong 仓库 |
| PM 基于创始人上游开展工作 | ✅ | §1.2 明确上游/下游分界 |
| hl-contracts 是企业定义真源 | ✅ | PM 通过 PR 贡献，创始人审批 merge |
| 执行者与审计者不同源 | ✅ | PM 驱动编码，技术验收官独立审计 |
| 创始人裁决在最上游 | ✅ | PM 推荐但不裁决，立项权在创始人 |
| 工具与 AI 平台不强制限定 | ✅ | §2.1 明确 PM 自主选择 |
| PM 是产线责任人（非规格整理者） | ✅ | §1.1 核心定位 |
| Cap-Spec 替代旧 PRD 6 卫星 | ✅ | PM 不复制 SSOT，只定义意图与验收 |

---

## 8. 待创始人裁决事项

| # | 事项 | 裁决结果 | 裁决日期 |
|---|------|---------|----------|
| D-1 | PM 产线责任人模式 | **✅ A) 确认** | 2026-03-30 |
| D-2 | PM 代码 PR 审批人 | **✅ C) 创始人 + 技术验收官两者均需** | 2026-03-30 |
| D-3 | PM hl-platform Write 权限 | **✅ A) 开放** | 2026-03-30 |
| D-4 | 朱阳 GitHub 用户名 | **待朱阳提供** | — |
| D-5 | 朱阳能力包分配时机 | **✅ B) S2 中期讨论后** | 2026-03-30 |

---

## 9. 关联文档修订清单

| 文档 | 修订内容 | 优先级 |
|------|---------|:-----:|
| hl-dispatch/TEAM.yml | 录入朱阳 GitHub 信息 | P0 |
| hl-contracts/prd/README.md | 追加 "Cap-Spec 规范（2026-03 起适用）" | P0 |
| hl-dispatch/README.md | 补充 PM 产线责任人接入说明 | P1 |
| TEAM-COLLABORATION-SPEC v1.2 | 附录追加 PM 产线责任人权限矩阵 | P1 |

---

## 10. 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-30 | v1.0 | DRAFT — PM 定位为规格整理者，CIS 三件套 |
| 2026-03-30 | v1.1 | 同步 CIS 术语到各章节 |
| 2026-03-30 | v2.0 | **重大修订** — 创始人纠正 PM 定位为产线责任人；PM 驱动 AI 编码完整闭环；废弃 CIS 改用 Cap-Spec；hl-platform 权限从 Read 升为 Write；工具/AI 平台不限定；新增 Phase 4 AI 编码验证步骤 |
| 2026-03-30 | v2.0 RULED | 创始人裁决 D-1~D-5：产线责任人模式✅、代码 PR 双审批✅、hl-platform Write✅、朱阳待提供 GitHub、S2 中期分配能力包✅ |
