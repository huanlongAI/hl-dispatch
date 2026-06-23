# hl-dispatch team responsibility gate and publisher

本目录是团队职责门禁与任务派发发布器的 repo file SSOT（唯一事实源）投影，用于在任务派发前统一校验“任务类型是否能派给某个角色”，并在门禁通过后收敛 GitHub Issue 发布入口。

## 中文摘要

本目录沉淀团队职责门禁的 P0 统一校验材料和 P1 发布器收敛材料。它把职责契约、当前 Owner 映射、输入 schema、回归用例、校验脚本、发布计划器和正式发布器预检放在同一个 repo file 路径下，供任务派发前判断是否可以把某类任务交给某个角色，并生成可审计的 GitHub Issue 发布请求。

P1 发布器默认仍是 dry-run：只在职责门禁 `ACCEPT`、formal publisher payload 存在、目标入口为 `github_issue`、GitHub Issue payload 存在且中文门禁通过后，输出精确 `gh issue create` 参数。只有显式 `--execute` 才会创建 GitHub Issue；本目录不写飞书、Project、Base，不授权真实支付、真实 provider、真实 secret、生产 runtime 或自动合并。商户私钥、真实支付流量、真实对账证据等未解析高风险项统一返回 `REVIEW_REQUIRED`。

## 术语说明

- P0：最低可用交付，建立职责真源、校验器和回归用例。
- P1：发布器收敛阶段，生成发布计划、正式发布 payload、发布预检和显式执行入口。
- SSOT：Single Source of Truth，唯一事实源；本目录使用 GitHub Issue / PR / repo file 作为任务和反馈真源。
- role id：稳定角色标识，例如 `ops`、`backend`、`frontend-lead`；职责契约绑定 role id，不绑定个人 handle。
- Owner 投影：从 `TEAM.yml` 派生的当前人员映射，只用于把 role id 映射到 GitHub handle。
- `REVIEW_REQUIRED`：需要 Founder / Gate 裁决后才能正式派发，不代表授权执行。

## Scope

- `ROLE-REGISTRY-v1.yaml`: 职责契约真源，绑定 role id，不绑定人员 handle。
- `ROLE-OWNERS-v1.yaml`: `TEAM.yml` 的 Owner 投影，只用于 role 到当前 GitHub handle 的映射。
- `TASK-ASSIGNMENT-SCHEMA-v1.json`: 回归 case / assignment payload 的输入 schema。
- `RESPONSIBILITY-REGRESSION-CASES-v1.yaml`: P0 必跑回归用例。
- `scripts/validate_task_assignment.py`: 单条任务派发统一校验器。
- `scripts/run_regression.py`: 回归用例 runner。
- `scripts/build_assignment_publish_plan.py`: P1 发布计划器，生成 dry-run 发布计划、裁决包和正式发布 payload。
- `scripts/preflight_formal_assignment_publisher.py`: P1 正式发布器预检与 GitHub Issue 发布入口；默认 dry-run，仅 `--execute` 写 GitHub。

P0 统一校验是发布器的前置硬门槛。P1 发布器只消费门禁 `ACCEPT` 后的 `formal_publisher_payload`，默认不创建 GitHub Issue；`REVIEW_REQUIRED` 和 `REJECT` 都 fail closed，不进入正式发布。

## Decision surface

校验器只输出三种裁决：

- `ACCEPT`: 任务类型和目标 role 在当前职责真源中匹配。
- `REJECT`: 当前派发违反明确职责边界、旧真源、授权引用或正式入口规则。
- `REVIEW_REQUIRED`: 未知任务类型或高风险未解析责任，需要 Founder / Gate 裁决后才能正式派发。

商户私钥、真实支付流量、真实对账证据等未解析高风险项在 P0 统一落到 `REVIEW_REQUIRED`。这不是授权，不代表可进入真实支付、真实 provider、真实 secret 或生产 runtime。

## Usage

单条校验：

```bash
python3 docs/team-context/scripts/validate_task_assignment.py \
  --input /path/to/assignment.json \
  --registry docs/team-context/ROLE-REGISTRY-v1.yaml \
  --owners docs/team-context/ROLE-OWNERS-v1.yaml
```

回归校验：

```bash
python3 docs/team-context/scripts/run_regression.py \
  --cases docs/team-context/RESPONSIBILITY-REGRESSION-CASES-v1.yaml \
  --registry docs/team-context/ROLE-REGISTRY-v1.yaml \
  --owners docs/team-context/ROLE-OWNERS-v1.yaml
```

生成发布计划：

```bash
python3 docs/team-context/scripts/build_assignment_publish_plan.py \
  --input /path/to/assignment.json \
  --registry docs/team-context/ROLE-REGISTRY-v1.yaml \
  --owners docs/team-context/ROLE-OWNERS-v1.yaml
```

正式发布器 dry-run 预检：

```bash
python3 docs/team-context/scripts/preflight_formal_assignment_publisher.py \
  --input /path/to/assignment-publish-plan.json \
  --publish \
  --repo huanlongAI/hl-dispatch
```

正式 GitHub Issue 写入必须先通过 dry-run 输出检查，再由人工明确授权后追加 `--execute`。该执行入口只允许 GitHub Issue，不写飞书、Project、Base 或生产 runtime。

`.yaml` 文件当前使用 JSON-compatible YAML 子集，避免给本仓新增运行时依赖；若环境提供 PyYAML，校验器也可解析普通 YAML。

## Source boundary

- GitHub Issue / PR / repo file 是任务和反馈 SSOT。
- Feishu、Project、Base、Context Atlas 都不能替代本目录的职责校验真源。
- 人员变化只更新 `ROLE-OWNERS-v1.yaml`；职责契约变化必须更新 `ROLE-REGISTRY-v1.yaml` 并补回归用例。
