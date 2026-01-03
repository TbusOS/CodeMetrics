# 📊 CodeMetrics

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/TbusOS/CodeMetrics.svg?style=social&label=Star)](https://github.com/TbusOS/CodeMetrics)

**一个功能丰富的代码度量分析工具**

[English](README.md) | [中文](README_zh.md)

</div>

---

## ✨ 功能特性

- 🌳 **目录树展示** - 直观的树形结构显示
- 📊 **详细统计** - 代码行/注释行/空行分离统计
- 🌐 **多语言支持** - 支持 50+ 编程语言
- 💰 **COCOMO 估算** - 开发成本、人月、工期估算
- 🏥 **健康度分析** - 注释率、大文件警告等
- 📈 **Top N 分析** - 最大文件、代码最多文件排行
- 🎨 **多输出格式** - Terminal/JSON/Markdown/HTML
- 📁 **自动保存报告** - 一键生成多格式报告
- ⚙️ **全局配置文件** - 自定义排除规则
- 🚀 **零依赖** - 纯 Python 标准库实现

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/TbusOS/CodeMetrics.git
cd CodeMetrics

# 一键安装
./scripts/install.sh
```

安装脚本会自动：
- ✅ 检查 Python 版本 (需要 >= 3.6)
- ✅ 设置执行权限
- ✅ 创建符号链接到 `~/.local/bin/codemetrics`
- ✅ 检查并配置 PATH

## 🚀 快速开始

```bash
# 分析嵌入式项目（驱动代码）
codemetrics /path/to/driver -p embedded

# 分析 Web 项目（中等复杂度）
codemetrics /path/to/webapp -p semi-detached

# 分析工具脚本（简单项目）
codemetrics /path/to/scripts -p organic
```

**默认输出包含：**
- 📂 目录树结构
- 📊 语言统计表
- 💰 COCOMO 成本估算
- 🏥 代码健康度分析
- 📈 Top 10 最大文件

## 📋 命令行参数

| 参数 | 简写 | 描述 |
|------|------|------|
| `path` | - | 要分析的目录路径 (必需) |
| `--project-type` | `-p` | **必需** COCOMO 项目类型: organic/semi-detached/embedded |
| `--top N` | `-n N` | Top N 文件数量 (默认: 10) |
| `--exclude` | `-e` | 额外排除的模式 (逗号分隔) |
| `--no-color` | - | 禁用颜色输出 |
| `--no-save` | - | 不保存报告 |

## 📊 项目类型说明

| 类型 | 描述 | 适用场景 |
|------|------|----------|
| **organic** | 简单项目 | 小团队、熟悉的技术栈 |
| **semi-detached** | 中等项目 | 中型团队、混合经验 |
| **embedded** | 复杂项目 | 嵌入式、驱动、实时系统、硬件相关 |

## 📖 使用示例

### 基本分析
```bash
codemetrics /path/to/project -p embedded
```

### 保存报告
```bash
# 自动保存 JSON/Markdown/HTML 报告
codemetrics /path/to/project -p embedded
# 报告保存在工具目录的 output 文件夹
```

### 显示 Top 20 文件
```bash
codemetrics /path/to/project -p embedded -n 20
```

### 额外排除目录
```bash
codemetrics /path/to/project -p embedded -e "test/*,docs/*"
```

## 📊 输出格式

CodeMetrics 自动生成多种格式的报告：

### 1. 终端输出（默认）
- 彩色树形结构
- 格式化的统计表格
- 实时进度显示

### 2. JSON 格式
```bash
# 位置：output/report_YYYYMMDD_HHMMSS.json
```
适合程序解析、CI/CD 集成、数据分析

### 3. Markdown 格式
```bash
# 位置：output/report_YYYYMMDD_HHMMSS.md
```
适合文档生成、GitHub/GitLab 展示

### 4. HTML 格式
```bash
# 位置：output/report_YYYYMMDD_HHMMSS.html
```
适合浏览器查看、团队分享、演示展示

## 🌐 支持的语言

**系统编程**: C, C++, Rust, Go, Assembly

**脚本语言**: Python, Ruby, Perl, Shell, Bash, Lua

**Web 前端**: JavaScript, TypeScript, React JSX, React TSX, HTML, CSS, SCSS, Vue

**JVM 语言**: Java, Kotlin, Scala, Groovy

**.NET 平台**: C#, F#

**配置文件**: JSON, YAML, TOML, XML, INI

**文档**: Markdown, reStructuredText

**其他**: SQL, Dockerfile, Makefile, CMake

等 50+ 编程语言。

## ⚙️ 配置文件

全局配置文件位于工具目录下：`config.json`

```json
{
  "name": "CodeMetrics 全局配置文件",
  "exclude": {
    "patterns": ["*.md", "*.json", "*.o", "*.ko"],
    "dirs": [".git", "node_modules", "__pycache__", "build"]
  },
  "cocomo": {
    "cost_per_month_usd": 5000,
    "cost_per_month_cny": 30000
  },
  "health": {
    "comment_ratio_min": 0.15,
    "comment_ratio_max": 0.30,
    "large_file_threshold": 800
  }
}
```

## 🧮 COCOMO 模型说明

COCOMO (Constructive Cost Model) 是 Barry Boehm 提出的软件成本估算模型。

### 计算公式

```
人月 (PM) = a × (KLOC)^b
工期 (月) = c × (PM)^d
团队规模 = PM / 工期
```

### 模型参数

| 类型 | a | b | c | d | 适用场景 |
|------|---|---|---|---|----------|
| organic | 2.4 | 1.05 | 2.5 | 0.38 | 简单项目 |
| semi-detached | 3.0 | 1.12 | 2.5 | 0.35 | 中等项目 |
| embedded | 3.6 | 1.20 | 2.5 | 0.32 | 复杂项目 |

## 🏥 健康度指标

| 指标 | 建议值 | 说明 |
|------|--------|------|
| 注释率 | 15-30% | 代码可维护性 |
| 平均文件行数 | 100-500 | 模块化程度 |
| 大文件 (>800行) | 0 | 建议拆分 |
| 低注释文件 (<5%) | 0 | 建议添加注释 |

## 📖 文档

- 📘 [使用示例](examples/README.md) - 详细的使用场景和示例
- 📗 [设计文档](docs/DESIGN.md) - 项目架构和设计说明
- 📙 [贡献指南](CONTRIBUTING.md) - 如何参与贡献
- 📕 [更新日志](CHANGELOG.md) - 版本历史和更新记录
- 📖 [COCOMO 模型](docs/COCOMO.md) - 成本估算模型详解

## 🎯 适用场景

- 📱 **嵌入式开发** - Linux 内核驱动、固件开发、实时系统
- 🌐 **Web 开发** - React/Vue 前端、Node.js/Django/Flask 后端
- 🔧 **工具脚本** - Shell 脚本、Python 自动化工具、DevOps 脚本
- 📚 **项目评估** - 代码审查、成本估算、技术债分析
- 🎓 **教学科研** - 代码度量研究、软件工程课程

## 🤝 参与贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解详情。

### 贡献方式

- 🐛 报告 bug 和问题
- 💡 提出新功能建议
- 📖 改进文档
- 🔧 提交 Pull Request
- 🌍 添加其他语言的翻译

## ❓ 常见问题

### Q: 需要安装额外的 Python 包吗？
A: 不需要！CodeMetrics 使用纯 Python 标准库实现，零依赖。

### Q: 支持 Windows 吗？
A: 主要针对 Linux/macOS，Windows 下需要使用 WSL 或 Git Bash。

### Q: 如何卸载？
A: 运行 `./scripts/uninstall.sh` 即可。

### Q: 输出报告保存在哪里？
A: 默认保存在工具目录下的 `<项目名>_output/` 目录。

### Q: 可以自定义 COCOMO 参数吗？
A: 可以！编辑 `config.json` 文件中的 `cocomo` 部分。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

- [GitHub 仓库](https://github.com/TbusOS/CodeMetrics)
- [问题追踪](https://github.com/TbusOS/CodeMetrics/issues)
- [Pull Requests](https://github.com/TbusOS/CodeMetrics/pulls)

---

<div align="center">

**用 ❤️ 为全球开发者打造**

[⭐ 给项目加星](https://github.com/TbusOS/CodeMetrics) 如果它对你有帮助！

</div>

