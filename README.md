# 唤龙平台 · 团队协作指南站点

基于 TEAM-COLLABORATION-SPEC v2.1（DRAFT）和 UI-DELIVERY-SPEC v1.0（DRAFT）生成的团队理解导览。

> **⚠️ 定位**：本站是 **Guide Layer**（理解导览层），不是制度真源层。
> 权威依据以 `hl-contracts` 仓库中的正式规范文档为准。
> 网页内容可能包含尚未锁定的候选方案（标记为 PROPOSED）。

## 部署方式（内部私有）

本站包含团队结构、仓库权限、门禁逻辑、CODEOWNERS 等内部治理信息，**必须以私有仓库部署**。

### 方式一：GitHub Pages（私有仓库，推荐）

```bash
# 1. 创建私有仓库
gh repo create hl-docs --private

# 2. 初始化并推送
cd hl-docs
git init
git add .
git commit -m "init: team collaboration guide site (internal)"
git branch -M main
git remote add origin https://github.com/<你的org>/hl-docs.git
git push -u origin main

# 3. 启用 GitHub Pages（需要 GitHub Team / Enterprise 计划才能私有仓库部署 Pages）
# Settings → Pages → Source: main / root
# 或使用 CLI：
gh api repos/<你的org>/hl-docs/pages -X POST -f source.branch=main -f source.path=/
```

> **注意**：GitHub Free 计划的私有仓库无法使用 GitHub Pages。
> 如果组织使用 Free 计划，请改用方式二或方式三。

### 方式二：使用 GitHub Actions 自动部署（私有仓库）

已提供 `.github/workflows/deploy.yml`，push 到 main 即自动部署。
同样需要 GitHub Team / Enterprise 计划。

### 方式三：静态文件内部托管

如果不使用 GitHub Pages，可将 `hl-docs/` 目录直接部署到内部服务器：

```bash
# 飞书网盘 / 内部 Nginx / 云服务器均可
# 本站为纯静态 HTML，无需后端服务
scp -r hl-docs/ your-server:/var/www/hl-docs/
```

## 站点结构

```
hl-docs/
├── index.html                # 首页（角色导航 + 详细目录）
├── docs-manifest.yaml        # 文档清单（版本 / 状态 / 源文档映射）
├── css/style.css             # 共享样式
├── js/main.js                # 共享脚本
├── pages/
│   ├── global.html           # 全局工作流（交互式）
│   ├── product.html          # 产品团队指南
│   ├── frontend-design.html  # 前端与设计团队指南
│   ├── engineering.html      # 工程师团队指南
│   ├── qa.html               # 测试团队指南
│   └── ops.html              # 运维人员指南
├── .nojekyll                 # 禁用 Jekyll 处理
└── .github/workflows/
    ├── deploy.yml            # 静态页面部署
    └── docs-ci.yml           # 文档 CI 检查（5 项）
```

## 文档 CI 检查（docs-ci.yml）

每次 push 自动运行 5 项检查：

| 检查项 | 失败条件 |
|--------|---------|
| version-sync-check | 网页版本号/状态与 docs-manifest.yaml 不一致 |
| placeholder-check | 存在 `alert(`、`TODO`、假链接、指向不存在的 `.md` 占位 |
| public-deploy-check | README / workflow 默认公开部署 |
| ratification-check | 页面声明 Pilot-Locked / Locked，但 docs-manifest 中源文档仍是 DRAFT |
| link-anchor-check | 内部链接或锚点失效 |

## 维护规则

1. **不要在网页中直接修改规则**——网页只反映 `hl-contracts` 中的正式规范
2. **每次源规范更新后**，更新 `docs-manifest.yaml` 的 version / status / last_verified
3. **新增内容**如果来自未锁定的规范，必须标注 `PROPOSED`
4. **锁版后**才能将对应章节的状态从 DRAFT 升级为 RATIFIED
