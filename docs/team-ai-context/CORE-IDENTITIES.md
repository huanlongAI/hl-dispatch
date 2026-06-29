# Team AI Context Core Identities

## 术语说明

- Core identity：团队 AI 上下文启动时必须知道的基础身份事实，不等同于普通成员通讯录。
- Air Task Contract：跨节点派发前的任务合同，包含验收对象、GitHub SSOT、输入材料、验收矩阵、输出格式和禁止边界。
- GitHub SSOT：GitHub Issue / PR 是任务、证据和回执的唯一事实源；飞书、截图和聊天只能提示，不改变状态。

## 当前硬事实

新者辉不是普通成员账号，也不是等待 GitHub / 飞书账号认领的人员项。新者辉是 `xinzhehui -> NODE-D` 智能体路由，当前治理身份为 `NODE-D / Design / 新者辉 / xinzhehui`。

当前判定优先级：

1. `40-PPR/registries/ppr-node-registry.json#NODE-D` 是当前节点状态机器证据。
2. `_infra/tzh-agent-configs/routing/tier2-dispatch.registry.json#xinzhehui` 是当前 dispatch 路由机器证据。
3. `40-AUM/AUM-001.md` 和 `40-PPR/PPR.md` 是治理语义说明；若旧段落仍写 `draft / not_active`，以当前 registry 的 `active_first_window` 投影为准。
4. `TEAM.yml` 只登记人类团队成员和 GitHub / 飞书通讯入口；不要用 `TEAM.yml` 缺少新者辉来判断 NODE-D 不存在。

## NODE-D / 新者辉 接入流程

当任务需要“新者辉产品验收”“设计体验验收”“产品体验复审”或等价语义时，不能等待一个叫新者辉的普通成员账号。正确流程是：

1. 当前协调方生成 Air Task Contract。
2. 通过 tier2 dispatch 触发 `xinzhehui`。
3. mode 使用 `product-experience`、`review` 或其他 registry 允许的只读设计 / 体验模式；不要使用实现模式。
4. NODE-D 只读验收后，把回执写回 GitHub SSOT。
5. NODE-E / 当前协调方接回主流程：通过则提交 Founder merge / closeout 裁决简报；需要修改则回 DRI / owner；无法执行则记为 `NODE-D_DISPATCH_BLOCKED`，不是产品验收失败。

最小命令形态：

```bash
bash /Users/tzhEngineering/Workspace/01_Repos/_infra/tzh-agent-configs/cli-dispatch/scripts/air-dispatch.sh \
  --from air-codex-cso \
  --to xinzhehui \
  --mode product-experience \
  --workdir /Users/tzhEngineering/Workspace/01_Repos/huanlong/hl-scene-app \
  --prompt-file /tmp/xinzhehui-product-acceptance.md
```

## 输出格式

NODE-D 产品验收回执至少包含：

```text
NODE-D_PRODUCT_ACCEPTANCE

结论：
验收通过
或
需要修改：<actionable finding>

验收依据：
- <检查项>
- <证据链接>

边界确认：
不授权 merge / release / provider / payment / production。
```

## 禁止误判

- 不要把“新者辉”当成普通成员、GitHub handle、飞书 open_id 或 `TEAM.yml` roster 项。
- 不要因为 GitHub Issue 写了“产品验收 owner：新者辉”就等待账号回复。
- 不要由 NODE-E 代替 NODE-D 做产品体验最终验收。
- 不要把 NODE-D 回执解释成 merge、release、provider、payment 或 production 授权。
- 不要修改 `baozouhui -> NODE-D` transition hold，不启动 NODE-F，不启动 R phase。

## Source Refs

- `_governance/tzhOS/40-PPR/registries/ppr-node-registry.json#NODE-D`
- `_governance/tzhOS/40-PPR/PPR.md#Design 域`
- `_governance/tzhOS/40-AUM/AUM-001.md#Node-D / Design / xinzhehui / 新者辉`
- `_infra/tzh-agent-configs/routing/tier2-dispatch.registry.json#xinzhehui`
