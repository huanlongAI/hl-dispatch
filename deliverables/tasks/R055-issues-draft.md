# R-055 衍生任务 Issue 草稿

> 生成日期：2026-03-13
> 关联裁决：R-055 HK 服务化开放策略（LOCKED）

---

## Issue 1/3：验证 deny-check CI gate 覆盖 HK 内部包隔离

**模板**：任务派发
**标签**：`task-assign`, `architect`, `priority-p0`
**指派**：Gate-H（gate-h-internal）
**优先级**：P0 - 紧急（当天完成）
**期望完成**：2026-03-14

### 任务清单

- [ ] 确认 `deny-check` gate 当前检查范围：是否覆盖 S-L4 能力包对 HK 内部实现包（`hk.*.internal`）的 import 拦截
- [ ] 确认 `gate-spring-isolation.sh`（R-054 Q4）覆盖 HK domain/model 包对 `org.springframework.*` 的零依赖检查
- [ ] 如有遗漏，列出缺失规则并提 PR 补齐
- [ ] 在 hl-platform 仓库本地跑一次完整 gate 验证，截图或贴输出

### 验收标准

- `deny-check` 能拦截 S-L4 → HK 内部实现包的非法 import（需实际测试用例证明）
- `gate-spring-isolation` 能拦截 HK domain 包引入 Spring 注解（需实际测试用例证明）
- 无遗漏 = 任务关闭；有遗漏 = 提补丁 PR 后关闭

### 背景说明

R-055 裁决 HK Phase 0–2 仅作内部治理内核，不以独立进程部署。为确保未来 Phase 3 可平滑抽离，当前 CI gate 必须严格保证 HK 内部实现不被能力包直接耦合。这是"独立部署就绪设计"的第一步验证。

关联裁决：R-055、R-054 Q4、SAAC-HL-001 §7.1 禁止事项 #1

---

## Issue 2/3：hl-contracts API 契约预留 external scope 目录结构

**模板**：任务派发
**标签**：`task-assign`, `architect`, `priority-p1`
**指派**：Gate-H（gate-h-internal）
**优先级**：P1 - 重要（3 天内完成）
**期望完成**：S2 Sprint 内（具体日期跟随 R-053 排期）

### 任务清单

- [ ] 在 `hl-contracts/apis/` 下新建 `external/` 目录，放入 README.md 说明用途和启用时机
- [ ] 现有 `hk.*.internal.openapi.v1.yaml` 文件保持不动，确认命名中 `internal` 标识清晰
- [ ] 编写 `external/README.md`，内容包括：scope 定义（internal vs external）、启用前置条件（R-055 两个 AND 条件）、与 internal 契约的语义一致性要求
- [ ] 确认此变更不影响现有 CI gate 和构建流程

### 验收标准

- `hl-contracts/apis/external/` 目录存在且含 README.md
- README 中明确引用 R-055 的两个必要条件（业务周期 + 创始人裁决）
- 现有 internal 契约和 CI 流程零影响（编译/gate 全通过）

### 背景说明

R-055 裁决 Phase 3 才开放 external API 面。当前只需要在目录结构上预留位置，不生成实际 external 契约文件。目的是让团队在日常开发中看到这个占位，形成"internal/external 双 scope"的心智模型。

关联裁决：R-055、R-050（恒定层/桥梁层）

---

## Issue 3/3：ADR 立项 — HK Deployment Modes（含 Audit 模块特殊性）

**模板**：任务派发
**标签**：`task-assign`, `architect`, `priority-p1`
**指派**：Gate-H（gate-h-internal）
**优先级**：P1 - 重要（3 天内完成）
**期望完成**：S3 Sprint 内（首包稳定后有实际数据再填充）

### 任务清单

- [ ] 在 `hl-dispatch/deliverables/decisions/` 下创建 `ADR-HK-DEPLOYMENT-MODES.md` 骨架
- [ ] 骨架需包含以下章节占位（内容 S3 填充）：
  - 背景与动机（引用 R-055）
  - 模式 A：SDK/Library 内嵌（当前模式）
  - 模式 B：独立微服务（HTTP/gRPC）
  - 模式 C：混合模式（内嵌 + Gateway API）
  - hk.audit 特殊性分析：同步审计 vs Outbox+CDC 异步审计的 trade-off
  - 各模式延迟预算与一致性要求
  - 推荐路径（待 Phase 3 前裁决）
- [ ] 骨架 PR 提交，创始人 review

### 验收标准

- ADR 骨架文件存在，章节结构完整
- hk.audit 同步/异步审计 trade-off 章节明确存在（这是 GPT 分析遗漏、我们补充的关键点）
- 骨架内容标注"S3 填充"，不含未经验证的结论

### 背景说明

R-055 要求 Phase 3 开放前需产出此 ADR。当前只立骨架，不填结论——结论需要首包实际运行数据支撑。特别注意 hk.audit 模块：它必须与被审计动作在同一事务边界内，未来远程化时是保留进程内还是走异步，是影响整个 HK 服务化方案的关键 trade-off。

关联裁决：R-055、R-050、R-054、SAAC-HL-001 §2.2

---

## gh CLI 创建命令（gh auth 恢复后执行）

```bash
# Issue 1: P0 验证 CI gate
gh issue create \
  --repo huanlongAI/hl-dispatch \
  --title "[任务] 验证 deny-check + gate-spring-isolation 覆盖 HK 内部包隔离（R-055）" \
  --label "task-assign,architect,priority-p0" \
  --assignee gate-h-internal \
  --body-file /dev/stdin <<'BODY'
## 任务派发

请按清单逐项执行，完成后勾选并在评论区说明。

**关联裁决**：R-055 HK 服务化开放策略（LOCKED）
**优先级**：P0 - 紧急
**期望完成**：2026-03-14

### 任务清单

- [ ] 确认 `deny-check` gate 当前检查范围：是否覆盖 S-L4 能力包对 HK 内部实现包（`hk.*.internal`）的 import 拦截
- [ ] 确认 `gate-spring-isolation.sh`（R-054 Q4）覆盖 HK domain/model 包对 `org.springframework.*` 的零依赖检查
- [ ] 如有遗漏，列出缺失规则并提 PR 补齐
- [ ] 在 hl-platform 仓库本地跑一次完整 gate 验证，截图或贴输出

### 验收标准

- `deny-check` 能拦截 S-L4 → HK 内部实现包的非法 import（需实际测试用例证明）
- `gate-spring-isolation` 能拦截 HK domain 包引入 Spring 注解（需实际测试用例证明）
- 无遗漏 = 任务关闭；有遗漏 = 提补丁 PR 后关闭

### 背景

R-055 裁决 HK Phase 0–2 仅作内部治理内核。为确保 Phase 3 可平滑抽离，CI gate 必须严格保证 HK 内部实现不被能力包直接耦合。
BODY

# Issue 2: P1 external scope 预留
gh issue create \
  --repo huanlongAI/hl-dispatch \
  --title "[任务] hl-contracts API 契约预留 external scope 目录结构（R-055）" \
  --label "task-assign,architect,priority-p1" \
  --assignee gate-h-internal \
  --body-file /dev/stdin <<'BODY'
## 任务派发

请按清单逐项执行，完成后勾选并在评论区说明。

**关联裁决**：R-055 HK 服务化开放策略（LOCKED）
**优先级**：P1 - 重要
**期望完成**：S2 Sprint 内

### 任务清单

- [ ] 在 `hl-contracts/apis/` 下新建 `external/` 目录，放入 README.md 说明用途和启用时机
- [ ] 现有 `hk.*.internal.openapi.v1.yaml` 文件保持不动，确认命名中 `internal` 标识清晰
- [ ] 编写 `external/README.md`：scope 定义、启用前置条件（R-055 两个 AND 条件）、与 internal 契约的语义一致性要求
- [ ] 确认此变更不影响现有 CI gate 和构建流程

### 验收标准

- `hl-contracts/apis/external/` 目录存在且含 README.md
- README 中明确引用 R-055 两个必要条件（业务周期 + 创始人裁决）
- 现有 internal 契约和 CI 流程零影响

### 背景

R-055 裁决 Phase 3 才开放 external API。当前只预留目录结构，不生成实际 external 契约文件。
BODY

# Issue 3: P1 ADR 骨架
gh issue create \
  --repo huanlongAI/hl-dispatch \
  --title "[任务] ADR 立项：HK Deployment Modes + Audit 模块特殊性（R-055）" \
  --label "task-assign,architect,priority-p1" \
  --assignee gate-h-internal \
  --body-file /dev/stdin <<'BODY'
## 任务派发

请按清单逐项执行，完成后勾选并在评论区说明。

**关联裁决**：R-055 HK 服务化开放策略（LOCKED）
**优先级**：P1 - 重要
**期望完成**：S3 Sprint 内（首包稳定后填充）

### 任务清单

- [ ] 在 `hl-dispatch/deliverables/decisions/` 下创建 `ADR-HK-DEPLOYMENT-MODES.md` 骨架
- [ ] 骨架需包含以下章节占位（内容 S3 填充）：
  - 背景与动机（引用 R-055）
  - 模式 A：SDK/Library 内嵌（当前模式）
  - 模式 B：独立微服务（HTTP/gRPC）
  - 模式 C：混合模式（内嵌 + Gateway API）
  - **hk.audit 特殊性分析**：同步审计 vs Outbox+CDC 异步审计的 trade-off
  - 各模式延迟预算与一致性要求
  - 推荐路径（待 Phase 3 前裁决）
- [ ] 骨架 PR 提交，创始人 review

### 验收标准

- ADR 骨架文件存在，章节结构完整
- hk.audit 同步/异步审计 trade-off 章节明确存在
- 骨架内容标注"S3 填充"，不含未经验证的结论

### 背景

R-055 要求 Phase 3 开放前产出此 ADR。当前只立骨架不填结论，结论需首包实际运行数据支撑。hk.audit 模块必须与被审计动作在同一事务边界内，未来远程化时的 trade-off 是整个 HK 服务化方案的关键决策点。
BODY
```
