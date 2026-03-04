# hl-dispatch 安全策略

> 本仓库为 **public** 仓库，所有内容对外可见。提交前必须遵守以下规则。

## 禁止提交的内容

| 类别 | 示例 | 检测方式 |
|------|------|----------|
| API 密钥 / Token | `api_key=xxx`, `Bearer xxx` | CI 正则扫描 |
| 密码 | `password=xxx`, 数据库密码 | CI 正则扫描 |
| 云平台凭证 | AWS AKIA*, Aliyun LTAI* | CI 正则扫描 |
| 私钥文件 | `.pem`, `.key`, `.p12`, `.pfx` | CI 文件名扫描 |
| 环境配置 | `.env`, `credentials.json` | CI 文件名扫描 + .gitignore |
| 内网 IP / 域名 | `10.x.x.x`, `192.168.x.x`, 内部域名 | CI 正则扫描 |
| 数据库连接串 | `jdbc:postgresql://...`, `mysql://...` | CI 正则扫描 |
| 个人身份信息 | 身份证号、银行卡号 | CI 正则扫描 |
| 客户商业数据 | 合同金额、客户名单、定价策略 | 人工审查 |
| 源代码片段 | hl-platform / hl-contracts 代码 | 人工审查 |

## 允许提交的内容

- 技术架构方案文档（脱敏后）
- 团队协作模板（Issue template / workflow）
- 培训材料（不含客户数据）
- 公开的技术决策文档

## 防护机制

### 自动防护（CI）
1. **Sensitive Content Guard** — 每次 push/PR 自动扫描 8 类敏感模式
2. **GitHub Secret Scanning** — public 仓库自动启用，检测已知密钥格式
3. **GitHub Push Protection** — 阻止推送包含已知密钥的提交

### 流程防护
4. **Branch Protection** — main 分支要求 PR + Owner 审批，禁止直接 push
5. **CODEOWNERS** — 所有变更需 @tzhOS 审批

### 人工防护
6. **提交前自查** — 提交者必须确认内容不含上表禁止项
7. **季度审计** — 每季度扫描仓库历史，清理误提交内容

## 误提交处理

如果敏感信息已推送到 public 仓库：

1. **立即** 撤销/轮换泄露的密钥/密码
2. 使用 `git filter-repo` 从历史中彻底删除
3. 通知 @tzhOS 评估影响范围
4. 记录事件到 `docs/invariants/`

## 联系人

安全问题联系仓库 Owner: @tzhOS
