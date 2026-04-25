# 唤龙平台 · 团队协作指南站点

本仓库是 `huanlongAI/hl-dispatch` 的 GitHub Pages 站点工作树，当前发布分支为 `gh-pages`。站点基于 TEAM-COLLABORATION-SPEC v2.1（DRAFT）、TOOLCHAIN-GUIDE v1.0（DRAFT）及 `hl-contracts` 中的治理裁决整理，用于团队理解导览。

> **定位**：本站是 **Guide Layer**（理解导览层），不是制度真源层。
> 权威依据以 `huanlongAI/hl-contracts` 仓库中的正式规范、RULINGS、OpenAPI、ReasonCodes 与 Cap-Spec 为准。
> 网页内容可能包含尚未锁定的候选方案，相关状态以 `docs-manifest.yaml` 为准。

## 当前发布方式

当前站点从 `gh-pages` 分支根目录发布：

```bash
git checkout gh-pages
python3 .github/scripts/docs-ci.py
git status --short
```

发布链路：

1. 本地修改 HTML / CSS / manifest。
2. 运行 `python3 .github/scripts/docs-ci.py`，必须 5 项全部通过。
3. 提交到 `gh-pages`。
4. 经授权后 push 到 `origin/gh-pages`。
5. `.github/workflows/deploy.yml` 在 `gh-pages` push 后部署 GitHub Pages。

> 不要把未验证草稿直接发布。`drafts/` 是 Claude / Cowork 历史草案与缓存材料，不是站点发布真源；只有被人工吸收进 HTML 页面或 `docs-manifest.yaml` 的内容才进入 Guide Layer。

## 站点结构

```text
hl-dispatch gh-pages/
├── index.html
├── docs-manifest.yaml
├── css/
│   └── style.css
├── js/
│   └── main.js
├── pages/
│   ├── global.html
│   ├── architecture.html
│   ├── github-yunxiao-pipeline.html
│   ├── repo-directory.html
│   ├── delivery-steps.html
│   ├── workflow-states.html
│   ├── gate-levels.html
│   ├── product.html
│   ├── frontend-design.html
│   ├── engineering.html
│   ├── qa.html
│   ├── ops.html
│   ├── team-leads.html
│   ├── tech-selection.html
│   └── glossary.html
├── .github/workflows/
│   ├── deploy.yml
│   └── docs-ci.yml
└── .github/scripts/
    └── docs-ci.py
```

## 文档 CI 检查

每次 push / PR 到 `gh-pages` 自动运行 5 项检查：

| 检查项 | 失败条件 |
|--------|---------|
| version-sync-check | 网页版本号 / 状态与 `docs-manifest.yaml` 不一致 |
| placeholder-check | 存在 `alert(`、`TODO`、假交互或指向 `.md` 的旧占位链接 |
| public-deploy-check | README / workflow 出现显式公开部署配置，例如 `--public` |
| ratification-check | 页面声明 Locked，但 manifest 中源文档仍是 DRAFT |
| link-anchor-check | 内部链接或锚点失效 |

本地验证命令：

```bash
python3 .github/scripts/docs-ci.py
```

## 维护规则

1. 网页只反映真源，不在页面里发明制度。
2. 每次吸收 `hl-contracts` 或团队规范更新后，同步更新 `docs-manifest.yaml` 的 source doc、status、last_verified。
3. 来自未锁定规范的内容必须保留 DRAFT / PROPOSED 语义，不得伪装为 LOCKED。
4. `github-yunxiao-pipeline.html` 是 GitHub 主轨 + 云效并行执行器的导览页；Required Status Checks 的挂载位统一在 GitHub PR，L1-L3 由云效执行并通过 GitHub 执行身份回推。
5. Git push 需要人工确认，不从自动化会话直接推送。
