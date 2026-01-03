# 📝 更新日志

所有重要的项目更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### 计划中的功能
- [ ] COCOMO II 模型支持
- [ ] Git 历史分析
- [ ] 代码复杂度计算（圈复杂度）
- [ ] 依赖关系图
- [ ] 团队贡献统计
- [ ] Web 界面

---

## [1.1.0] - 2025-01-03

### ✨ 新增
- 🎉 首次公开发布
- 📊 目录树结构展示
- 📈 代码行/注释行/空行统计
- 🌐 支持 50+ 编程语言识别
- 💰 COCOMO 成本估算（三种项目类型）
- 🏥 代码健康度分析
- 📊 Top N 文件排行
- 🎨 多输出格式：Terminal/JSON/Markdown/HTML
- ⚙️ 全局配置文件支持
- 🚀 一键安装脚本
- 📚 完整文档

### 🌐 支持的语言
- **系统编程**: C, C++, Rust, Go, Assembly
- **脚本语言**: Python, Ruby, Perl, Shell, Lua
- **Web 前端**: JavaScript, TypeScript, React, Vue, HTML, CSS
- **JVM**: Java, Kotlin, Scala, Groovy
- **.NET**: C#, F#
- **配置**: JSON, YAML, TOML, XML
- **文档**: Markdown, reStructuredText
- **其他**: SQL, Dockerfile, Makefile, 等

### 📊 COCOMO 项目类型
- **organic**: 简单项目（小团队、熟悉的技术栈）
- **semi-detached**: 中等项目（中型团队、混合经验）
- **embedded**: 复杂项目（嵌入式、驱动、实时系统）

### 🏥 健康度指标
- 注释率分析（建议 15-30%）
- 平均文件大小检查
- 大文件警告（>800 行）
- 低注释文件提示（<5%）
- 代码密度统计

### 🎨 输出格式
- **Terminal**: 彩色树形结构，格式化表格
- **JSON**: 完整的机器可读数据
- **Markdown**: 适合文档和展示
- **HTML**: 美观的网页报告（深色主题）

### 🔧 工具特性
- 零依赖（纯 Python 标准库）
- 自动排除常见目录（.git, node_modules 等）
- 自定义排除规则
- 可配置的成本参数
- 自动路径解析
- 符号链接支持

---

## [1.0.0] - 2025-01-01 (内部版本)

### ✨ 初始开发
- 基础代码统计功能
- 语言识别
- 简单的输出格式

---

## 版本说明

### 版本号规则

`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 更改
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修正

### 标签说明

- ✨ **新增** (Added): 新功能
- 🔧 **修改** (Changed): 现有功能的更改
- 🗑️ **废弃** (Deprecated): 即将移除的功能
- ❌ **移除** (Removed): 已移除的功能
- 🐛 **修复** (Fixed): Bug 修复
- 🔒 **安全** (Security): 安全问题修复

---

## 链接

- [首页](README.md)
- [贡献指南](CONTRIBUTING.md)
- [发布说明](docs/RELEASE_NOTES.md)

---

**注**: 日期格式为 YYYY-MM-DD

