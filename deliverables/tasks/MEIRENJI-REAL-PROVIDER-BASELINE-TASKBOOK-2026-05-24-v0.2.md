# 美人计独立 AI 产品 real-provider baseline 任务书

**任务编号**：MEIRENJI-REAL-PROVIDER-BASELINE
**版本**：v0.2
**状态**：Founder approved for dispatch and repo landing
**日期**：2026-05-24
**GitHub SSOT Issue**：https://github.com/huanlongAI/hl-dispatch/issues/158
**产品线**：唤龙平台 / 唤龙 AI
**product_id**：`product.huanlong_ai.meirenji`
**团队可见标题**：`product.huanlong_ai.meirenji real-provider baseline`

---

## 0. 授权状态

Founder 已于 2026-05-24 授权以下事项：

```yaml
approve:
  task_contract_v0_2_accepted: true
  dispatch_allowed: true
  repo_landing_allowed: true
  sandbox_real_provider_call_allowed_once: true
  observation_protocol_enabled: true
```

授权仅覆盖本任务书定义的 real-provider baseline 建设、证据回填与审计观察，不授权生产发布或生产放量。

```yaml
runtime_authorization: false
production_release_authorization: false
real_user_data_provider_call_allowed: false
app_provider_secret_allowed: false
app_provider_endpoint_allowed: false
app_model_route_allowed: false
```

## 1. 产品与仓库边界

美人计是唤龙平台 / 唤龙 AI 产品线下的独立 AI 产品：

- `product_id = product.huanlong_ai.meirenji`
- 不并入 booking。
- 不并入 customer profile。
- 不并入 entitlement。
- 依赖既有租户订阅与 AI 用量权益能力包做 access control（访问控制）与 quota（额度）边界。

落地仓库与职责边界：

| 仓库 / 域 | 本阶段职责 | 禁止事项 |
|---|---|---|
| `hl-scene-app` | 美人计独立 AI 产品客户端接入、UI 状态、错误态、权益不足态 | 不得保存 provider secret / API key / endpoint / model route |
| `hl-platform` / HK | server-side model proxy、权益检查、用量记录、脱敏日志与错误码映射 | 不得使用真实用户数据做 provider 调用 |
| `hl-dispatch` | 本任务合同、派发、证据接入、观察台账 | 不承载实现代码 |
| `hl-contracts` | 只作为已存在契约和能力包边界参考 | 不因本任务自动新增 facts / events / reason code / OpenAPI |

## 2. real-provider baseline 硬边界

允许事项：

- 服务端侧进行 1 次 OpenAI sandbox 真实调用。
- 输入必须是 synthetic input（合成输入）。
- 证据必须脱敏，仅证明 server-side provider path 可用。
- 证据可包含 trace id、调用时间、synthetic prompt 摘要、响应摘要、token / usage 摘要、脱敏错误或成功状态。

禁止事项：

- App 侧出现 provider secret、API key、provider endpoint、model route。
- App 侧通过配置、日志、错误消息或埋点反推出 provider route。
- 使用真实用户、真实门店、真实客户、真实经营数据做 provider 调用。
- 把 sandbox evidence 解释为生产发布、生产放量或中国区公开上架模型策略。
- 把本任务并入 booking / customer profile / entitlement 的产品身份。

## 3. Owner 派发单元

| 单元 | Owner | GitHub / 节点口径 | 交付物 |
|---|---|---|---|
| 设计产出 | 童静 | `@tongjing2026-glitch` | 美人计独立 AI 产品设计 baseline，明确 product_id 与不并入三类能力边界 |
| 设计审计与验收 | 节点 D 设计智能体 | route 待调度方确认 | 对童静设计产出给出 `pass / needs_fix / blocked` |
| 服务端开发 | 许久明 | `@xujiuming` | `hl-platform` / HK server-side model proxy baseline 与 1 次 OpenAI sandbox synthetic evidence |
| 客户端开发 | 胡杰威 | `@663548110` | `hl-scene-app` 接入平台能力，证明客户端无 provider 泄漏 |
| 产品 / 合规 / 代码质量专项审计 | 节点 C 小飞飞 | route 待调度方确认 | 产品边界、合规、代码质量专项审计 |
| 工程与治理总审计 | 节点 E 大辉子 | `dahuizi` active route | 工程治理、SSOT、证据完整性与 go / no-go gate 结论 |
| 总控 | NODE-M | 不替代实现或审计 | 任务合同、派发、台账、观察与证据接入 |

当前 GitHub assignable 预检结果：

- `@663548110` 可 assign。
- `@tongjing2026-glitch` 当前不可 assign。
- `@xujiuming` 当前不可 assign。
- 因本任务跨多个 owner，GitHub Issue 默认不单点 assign，避免误归属。

## 4. 各单元验收标准

### 4.1 童静：设计产出

必须回填：

- 设计稿或设计说明链接。
- `product_id = product.huanlong_ai.meirenji` 的产品身份说明。
- 明确不并入 booking / customer profile / entitlement。
- 客户端界面不呈现 provider route 细节。
- 用户输入提示中必须避免真实敏感个人信息输入。

### 4.2 节点 D：设计审计与验收

必须回填：

- 审计对象版本。
- 设计边界是否忠于本任务书。
- 是否存在误导用户输入真实敏感数据、误导生产 provider 路径、误导能力包归属的问题。
- 结论只能是 `pass / needs_fix / blocked`。

### 4.3 许久明：服务端 baseline

必须回填：

- server-side model proxy 路径说明。
- 权益检查与 AI 用量扣减 / 记录位置说明。
- 1 次 OpenAI sandbox synthetic input 调用脱敏证据。
- provider secret 不进入 App 的证明。
- 错误态、超时态、quota 不足态、provider failure 的映射证据。

服务端禁止：

- 在 issue、日志、截图、commit 或配置中泄露 secret / endpoint / model route。
- 用真实用户数据完成 provider 调用。

### 4.4 胡杰威：客户端 baseline

必须回填：

- `hl-scene-app` 接入点说明。
- UI 主路径、loading、error、quota insufficient、provider unavailable 的截图或录屏证据。
- 客户端配置 / 日志 / 错误消息中无 provider secret、API key、endpoint、model route 的源码或检查证据。
- 前端构建证据仍按既有前端 Owner 口径回填，不派给 Gate-R。

### 4.5 节点 C 小飞飞：专项审计

必须回填：

- 产品边界审计：是否保持独立 AI 产品。
- 合规审计：是否避免真实数据、医疗诊疗、疗效承诺、生产 provider 误导。
- 代码质量审计：服务端 / 客户端边界是否清晰，错误态和日志是否可审计。
- 结论：`pass / needs_fix / blocked`。

### 4.6 节点 E 大辉子：工程与治理总审计

必须回填：

- GitHub SSOT、任务合同、owner evidence 是否完整。
- `hl-scene-app` / `hl-platform` / HK 边界是否符合本任务书。
- 是否存在 provider 泄漏、真实数据调用、能力包越界、契约污染。
- 7d gate 结论：`go / no-go / needs-founder-ruling`。

## 5. Owner 回执模板

每个 owner 在 GitHub Issue 评论中使用以下 YAML 回执：

```yaml
owner_response:
  task_id: MEIRENJI-REAL-PROVIDER-BASELINE
  owner: "<姓名或节点>"
  unit: "<design_output | design_audit | server_baseline | client_baseline | audit_c | audit_e>"
  status: "<received | in_progress | evidence_submitted | blocked>"
  evidence_links:
    - "<GitHub PR / commit / comment / artifact link>"
  boundary_check:
    app_has_provider_secret: false
    app_has_provider_endpoint: false
    app_has_model_route: false
    real_user_data_used_for_provider_call: false
  blockers:
    - "<如无阻塞写 none>"
  next_step: "<下一步>"
```

## 6. Evidence Intake 标准

Evidence 必须满足：

- GitHub Issue / PR / commit / check / artifact 链接可追溯。
- OpenAI sandbox evidence 必须脱敏。
- 不接受飞书消息、截图转述、口头说明作为唯一证据。
- 不接受本地路径、下载目录、个人草稿作为团队 SSOT。
- 不接受未说明输入是否 synthetic 的 provider 调用证据。

## 7. 观察协议

```yaml
observation:
  24h:
    due_at: 2026-05-25 09:58 CST
    check:
      - owner 是否确认收到任务
      - 是否存在边界误读
      - 是否有人试图把 provider 信息放进 App
      - 是否需要 Founder 裁决
    output:
      - 状态快照
      - 阻塞点列表

  72h:
    due_at: 2026-05-27 09:58 CST
    check:
      - 设计 baseline 是否可审
      - server proxy 路径是否有可验证进展
      - client 是否保持无 provider 泄漏
      - sandbox 调用准备是否满足 synthetic / server-side / 脱敏要求
    output:
      - evidence intake 初筛
      - 风险分级

  7d:
    due_at: 2026-05-31 09:58 CST
    check:
      - 是否形成完整 real-provider baseline 证据包
      - C / D / E 审计是否完成或明确阻塞
      - 是否可进入下一阶段
    output:
      - go / no-go / needs-founder-ruling
```

## 8. 飞书投影记录

飞书仅作提醒投影，不作为 owner 回执、证据或确认真源。

| 时间 | 群 | chat_id | message_id | 验证 |
|---|---|---|---|---|
| 2026-05-24 10:05 CST | 任务协同 | `oc_5ef189f8db26e982a94aef8ebaa598fc` | `om_x100b6e119edb70a0c2d1b9323c99279` | `lark-cli im +messages-mget` verified |
| 2026-05-24 10:08 CST | AI native工程通知 | `oc_e261da13768e38e4791415b1d2cb89d0` | `om_x100b6e1197c150a4c10c3a603d48b07` | `lark-cli im +messages-mget` verified |

GitHub 台账事件：

- https://github.com/huanlongAI/hl-dispatch/issues/158#issuecomment-4527114183

## 9. 关联参考

- `hl-dispatch#84`：旧美人计观察侧设计输入任务，已关闭；不授权产品 baseline 或代码实现。
- `hl-dispatch#154`：P0.5 自然交互与 AI 草稿确认能力包；不等同本独立 AI 产品 real-provider baseline。
- `NEW-BEAUTY-AI-P0-GOVERNANCE-RULING-v0.1.md`：新美业 AI App 创始人建设范围与团队合并流程边界。
- `NEW-BEAUTY-AI-P0-PRODUCT-SPEC-v0.1.md`：P0 产品规格参考。
- `NEW-BEAUTY-AI-P0-SYSTEM-ARCH-v0.1.md`：P0 系统架构参考。

## 10. 当前阻塞 / 待确认项

- 节点 D 设计智能体 route 需在实际调度前确认可用性。
- 节点 C 小飞飞 route 需在实际调度前确认可用性。
- `hl-scene-app` 本地 main 当前 behind 1；客户端仓库读写前需 fast-forward。
- `hl-contracts` 当前分支存在未跟踪 `tests/__pycache__/`；本任务不写 `hl-contracts`，仅作为边界参考。
