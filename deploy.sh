#!/bin/bash
# 唤龙平台 · 团队协作指南 — 一键部署到 GitHub Pages
# 运行方式：在终端 cd 到 hl-docs 目录，执行 bash deploy.sh

set -e

ORG="huanlongAI"
REPO="hl-dispatch"
BRANCH="gh-pages"

echo "🐉 唤龙平台团队协作指南 — 部署到 GitHub Pages"
echo "  组织: $ORG"
echo "  仓库: $REPO"
echo "  分支: $BRANCH"
echo ""

# 检查 gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ 未找到 gh CLI。请先安装：brew install gh && gh auth login"
    exit 1
fi

# 检查认证
if ! gh auth status &> /dev/null 2>&1; then
    echo "❌ gh 未认证。请先运行：gh auth login"
    exit 1
fi

echo "✓ gh CLI 已认证"

# 创建 gh-pages 分支（orphan，不继承历史）
echo "→ 创建 orphan 分支 $BRANCH ..."
git checkout --orphan "$BRANCH" 2>/dev/null || git checkout "$BRANCH"

# 确保所有文件已暂存
git add -A

# 提交
git commit -m "deploy: team collaboration guide site (Internal Guide Layer)" --allow-empty

# 设置远程（如果尚未设置）
if ! git remote get-url origin &> /dev/null 2>&1; then
    echo "→ 添加远程仓库 ..."
    git remote add origin "https://github.com/$ORG/$REPO.git"
else
    echo "✓ 远程仓库已存在"
fi

# 推送
echo "→ 推送到 $ORG/$REPO ($BRANCH) ..."
git push -u origin "$BRANCH" --force

# 启用 GitHub Pages
echo "→ 启用 GitHub Pages (source: $BRANCH / root) ..."
gh api "repos/$ORG/$REPO/pages" -X POST \
    -f "source[branch]=$BRANCH" \
    -f "source[path]=/" 2>/dev/null || \
gh api "repos/$ORG/$REPO/pages" -X PUT \
    -f "source[branch]=$BRANCH" \
    -f "source[path]=/" 2>/dev/null || \
echo "  ⚠️ Pages 可能需要在 Settings → Pages 手动启用"

echo ""
echo "✅ 部署完成！"
echo ""
echo "📎 访问地址：https://$ORG.github.io/$REPO/"
echo ""
echo "如果链接暂时 404，请等 1-2 分钟让 GitHub 构建完成。"
echo "也可以在 https://github.com/$ORG/$REPO/settings/pages 确认 Pages 状态。"
