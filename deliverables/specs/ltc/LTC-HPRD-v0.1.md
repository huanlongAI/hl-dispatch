# LTC HPRD v0.1

**状态**：R1 产品需求规格草案
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：LTC-Endpoint 人类可审阅产品需求

## 1. 产品定位

LTC-Endpoint 是大辉子的企业端点工具和哨兵基础设施。它部署在公司固定资产电脑上，采集合规的 AI 驱动工程元数据、安装电脑硬件配置信息和证据链状态，生成 sanitized event、aggregate 和 evidence reference，供大辉子进行工程治理和绩效管理分析。

LTC 不直接裁决绩效，不写飞书台账，不发飞书公告，不输出绩效分、员工排名、薪酬建议或纪律处分结论。

## 2. 目标用户

| 用户 | 目标 |
|---|---|
| 大辉子 | 稳定消费 LTC evidence feed，用于制度内分析、统计和绩效裁决。 |
| 创始人 / 管理层 | 查看大辉子基于 LTC 证据形成的治理和绩效结果。 |
| 员工 | 查看自身字段类别、端点状态、断链、说明和申诉路径。 |
| 管理员 | 按人工登记结果安装、绑定、更新、停用或卸载 LTC。 |
| 审计者 | 校验证据签名、字段范围、制度版本、确认版本、留存和访问记录。 |

## 3. 范围

包含：

- 公司固定资产电脑。
- Windows 优先，Mac 第二平台。
- Codex 订阅使用。
- `heiyucode.com` API 密钥使用。
- 当前安装电脑硬件配置信息。
- AI 工具使用元数据。
- 端点心跳、健康和断链。
- 员工 owner view。
- 员工说明和申诉入口。
- 大辉子 evidence feed。

不包含：

- 员工个人电脑强制部署。
- MDM 或类似平台接入。
- 公司资产管理。
- prompt、completion、transcript、文件内容、URL、窗口标题、剪贴板、按键、截图或屏幕录制。
- LTC 直接写飞书台账或公告。

## 4. 核心需求

| ID | 需求 |
|---|---|
| HPRD-001 | LTC 必须只能强制部署到公司固定资产电脑。 |
| HPRD-002 | LTC 首个 runtime 平台必须优先 Windows，再支持 Mac。 |
| HPRD-003 | LTC 必须记录安装电脑硬件配置元数据，但不得参与资产管理。 |
| HPRD-004 | LTC 必须支持 Codex 订阅和 `heiyucode.com` API 密钥使用的结构化元数据采集。 |
| HPRD-005 | LTC 必须采用 scope-first / banned 字段模型，采集范围内尽量齐全。 |
| HPRD-006 | banned 字段必须永久禁止采集、存储、导出、日志化或推断。 |
| HPRD-007 | raw observation 只能作为内存候选输入，不能落盘、日志化或下游化。 |
| HPRD-008 | 员工不得本地关闭、退出、卸载或绕过公司固定资产电脑上的 LTC。 |
| HPRD-009 | LTC 必须提供 owner view、说明和申诉入口。 |
| HPRD-010 | LTC 必须向大辉子输出 sanitized event、aggregate 和 evidence reference。 |
| HPRD-011 | R4/R5 dry run 不得进入正式绩效台账、公告、薪酬、纪律或考核结论。 |
| HPRD-012 | 飞书台账和公告只能由大辉子执行。 |

## 5. 阶段目标

| 阶段 | 产品目标 |
|---|---|
| R2 alpha0-lite | 用合成样本证明字段安全和 sanitizer 行为。 |
| R3 Endpoint Sentinel Alpha | 在 Windows 公司固定资产电脑上完成最小 runtime、心跳、硬件配置和 owner view 原型。 |
| R4 Internal Beta | 在有限试点中验证人工登记、常驻运行、断链、说明、审计和 dry run。 |
| R5 DahuiZi Evidence Feed | 大辉子消费 LTC evidence feed，但不进入正式绩效。 |
| R6 Performance Integrated | 大辉子依据制度写台账和公告，LTC 仅提供证据。 |

## 6. 成功标准

- banned 字段泄漏测试通过。
- raw observation 不落盘、不日志化、不下游化。
- Windows runtime 可安装、绑定、心跳、上报健康和硬件配置。
- 员工 owner view 可查看字段类别、制度版本、确认版本、端点状态和断链。
- evidence feed 可被大辉子幂等消费。
- LTC 不出现任何绩效评分、排名、薪酬建议、纪律处分或飞书写入行为。
