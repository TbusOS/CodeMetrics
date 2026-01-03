# 🚀 发布到 GitHub 指南

本文档说明如何将 CodeMetrics 项目发布到 GitHub 并让全球开发者使用。

---

## 📋 准备工作清单

在发布之前，确认以下内容：

- [x] ✅ 代码已完成并测试
- [x] ✅ 文档完整（README、CONTRIBUTING 等）
- [x] ✅ Git 仓库已初始化
- [x] ✅ 项目结构已优化
- [x] ✅ LICENSE 文件已添加
- [x] ✅ .gitignore 已配置
- [x] ✅ GitHub Actions 工作流已设置
- [x] ✅ 所有更改已提交

---

## 🌐 步骤 1: 在 GitHub 上创建仓库

### 1.1 登录 GitHub
访问 https://github.com 并登录你的账号

### 1.2 创建新仓库
1. 点击右上角的 `+` → `New repository`
2. 填写仓库信息：
   - **Repository name**: `CodeMetrics`
   - **Description**: `📊 A powerful code metrics and analysis tool with COCOMO estimation, health analysis, and multi-format reports`
   - **Visibility**: `Public` (让全球开发者可见)
   - **⚠️ 不要** 勾选以下选项：
     - [ ] Add a README file
     - [ ] Add .gitignore
     - [ ] Choose a license
   
   > 因为我们已经有这些文件了

3. 点击 `Create repository`

---

## 🔗 步骤 2: 关联本地仓库到 GitHub

在本地项目目录执行：

```bash
cd /home/zhangbh/cursor-tools/CodeMetrics

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/CodeMetrics.git

# 查看远程仓库
git remote -v

# 推送代码到 GitHub
git branch -M master
git push -u origin master
```

**提示**: 首次推送可能需要输入 GitHub 用户名和密码（或 Personal Access Token）

---

## 🏷️ 步骤 3: 创建第一个 Release

### 3.1 创建版本标签

```bash
cd /home/zhangbh/cursor-tools/CodeMetrics

# 创建带注释的标签
git tag -a v1.1.0 -m "Release v1.1.0 - First public release

✨ Features:
- Directory tree visualization
- Code metrics analysis for 50+ languages
- COCOMO cost estimation
- Health analysis
- Multi-format output (Terminal/JSON/Markdown/HTML)
- Zero dependencies
"

# 推送标签到 GitHub
git push origin v1.1.0
```

### 3.2 在 GitHub 上创建 Release

方式一：自动（通过 GitHub Actions）
- 推送标签后，GitHub Actions 会自动创建 Release

方式二：手动创建
1. 访问 `https://github.com/YOUR_USERNAME/CodeMetrics/releases`
2. 点击 `Create a new release`
3. 选择标签 `v1.1.0`
4. 填写 Release 信息：
   - **Release title**: `CodeMetrics v1.1.0 - First Public Release`
   - **Description**: 复制 `docs/RELEASE_NOTES.md` 的内容
5. 附加文件（可选）：
   - `codemetrics.py`
   - `config.json`
6. 点击 `Publish release`

---

## 🎨 步骤 4: 完善 GitHub 仓库设置

### 4.1 添加仓库描述
1. 访问你的仓库主页
2. 点击右上角的 `⚙️ Settings`
3. 在 General 设置中：
   - **Description**: `📊 A powerful code metrics and analysis tool with COCOMO estimation, health analysis, and multi-format reports`
   - **Website**: 如果有的话
   - **Topics**: 添加标签
     ```
     code-metrics, code-analysis, cocomo, python, cli-tool,
     developer-tools, code-quality, software-metrics, static-analysis
     ```

### 4.2 启用 Issues 和 Discussions
- ✅ Enable Issues
- ✅ Enable Discussions (可选，用于社区交流)

### 4.3 设置社交预览图（可选）
创建一个 1200x630 的图片作为分享时的预览图

---

## 📊 步骤 5: 添加 Badges 到 README

编辑 README.md，替换占位符：

```bash
cd /home/zhangbh/cursor-tools/CodeMetrics

# 使用你的 GitHub 用户名替换 YOUR_USERNAME
sed -i 's/YOUR_USERNAME/你的用户名/g' README.md

git add README.md
git commit -m "docs: 更新 README 中的 GitHub 链接"
git push origin master
```

---

## 🌟 步骤 6: 推广项目

### 6.1 社交媒体分享
分享到：
- Twitter
- Reddit (r/programming, r/Python)
- Hacker News
- LinkedIn
- 微信公众号
- 知乎
- V2EX
- CSDN

### 6.2 提交到工具列表
- [Awesome Python](https://github.com/vinta/awesome-python)
- [Awesome CLI Apps](https://github.com/agarrharr/awesome-cli-apps)
- [Awesome Code Analysis](https://github.com/analysis-tools-dev/static-analysis)

### 6.3 写一篇博客
介绍：
- 为什么创建这个工具
- 主要功能和特点
- 使用示例
- 与其他工具的对比

---

## 📈 步骤 7: 持续维护

### 7.1 响应 Issues
- 及时回复用户问题
- 标记 Issues（bug/enhancement/question）
- 关闭已解决的 Issues

### 7.2 审查 Pull Requests
- 感谢贡献者
- 代码审查
- 测试后合并

### 7.3 发布新版本
当有重要更新时：

```bash
# 更新 CHANGELOG.md
vim CHANGELOG.md

# 提交更改
git add .
git commit -m "chore: prepare for v1.2.0"
git push

# 创建新标签
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

---

## 📞 快速命令参考

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/CodeMetrics.git

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/CodeMetrics.git

# 推送代码
git push -u origin master

# 创建标签
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0

# 查看状态
git status
git log --oneline

# 更新远程仓库
git pull origin master
git push origin master
```

---

## ✅ 发布后检查清单

发布完成后，确认：

- [ ] 仓库在 GitHub 上可见
- [ ] README 正确显示
- [ ] 所有文件都已上传
- [ ] Release 已创建
- [ ] GitHub Actions 正常运行
- [ ] Issues 和 PR 模板可用
- [ ] Topics 标签已添加
- [ ] LICENSE 正确显示

---

## 🎉 成功发布！

恭喜！你的项目现在已经：

- ✨ 在 GitHub 上公开
- 🌍 全球开发者可以访问
- 📦 可以通过 git clone 安装
- 🤝 接受社区贡献
- 📈 开始收集 ⭐ Stars

**下一步**:
1. 分享到社交媒体
2. 邀请朋友试用
3. 收集反馈
4. 持续改进

---

## 🔗 有用的链接

- [GitHub Docs - Creating a Repository](https://docs.github.com/en/get-started/quickstart/create-a-repo)
- [GitHub Docs - Managing Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Awesome README](https://github.com/matiassingers/awesome-readme)

---

**祝你的开源项目成功！** 🚀✨

