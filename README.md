# 📊 CodeMetrics

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/TbusOS/CodeMetrics.svg?style=social&label=Star)](https://github.com/TbusOS/CodeMetrics)

**一个功能丰富的代码度量分析工具**

[English](#english) | [中文](#中文)

</div>

---

## 中文

### ✨ 功能特性

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

### 📦 安装

```bash
# 克隆仓库
git clone https://github.com/TbusOS/CodeMetrics.git
cd CodeMetrics

# 一键安装
./scripts/install.sh
```

### 🚀 快速开始

```bash
# 分析驱动代码 (嵌入式项目)
codemetrics /path/to/driver -p embedded

# 分析 Web 项目 (中等复杂度)
codemetrics /path/to/webapp -p semi-detached

# 分析小工具脚本 (简单项目)
codemetrics /path/to/scripts -p organic
```

### 📋 命令行参数

| 参数 | 简写 | 描述 |
|------|------|------|
| `path` | - | 要分析的目录路径 (必需) |
| `--project-type` | `-p` | **必需** COCOMO 项目类型: organic/semi-detached/embedded |
| `--top N` | `-n N` | Top N 文件数量 (默认: 10) |
| `--exclude` | `-e` | 额外排除的模式 (逗号分隔) |
| `--no-color` | - | 禁用颜色输出 |
| `--no-save` | - | 不保存报告 |

### 📊 项目类型说明

| 类型 | 描述 | 适用场景 |
|------|------|----------|
| **organic** | 简单项目 | 小团队、熟悉的技术栈 |
| **semi-detached** | 中等项目 | 中型团队、混合经验 |
| **embedded** | 复杂项目 | 嵌入式、驱动、实时系统 |

### 🌐 支持的语言

C, C++, Python, Java, JavaScript, TypeScript, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, C#, Shell, Perl, Lua, R, SQL, HTML, CSS, SCSS, Vue, React, Markdown, YAML, JSON, XML, Makefile, Dockerfile, 等 50+ 语言。

### 📖 文档

- 📘 [使用示例](examples/README.md)
- 📗 [设计文档](docs/DESIGN.md)
- 📙 [贡献指南](CONTRIBUTING.md)
- 📕 [更新日志](CHANGELOG.md)

### 🤝 参与贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解详情。

### 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

## English

### ✨ Features

- 🌳 **Directory Tree** - Intuitive tree structure visualization
- 📊 **Detailed Statistics** - Separate code/comment/blank line counting
- 🌐 **Multi-language** - Support for 50+ programming languages
- 💰 **COCOMO Estimation** - Development cost, effort, and schedule estimation
- 🏥 **Health Analysis** - Comment ratio, large file warnings, etc.
- 📈 **Top N Analysis** - Ranking of largest and most complex files
- 🎨 **Multiple Formats** - Terminal/JSON/Markdown/HTML output
- 📁 **Auto-save Reports** - One-click multi-format report generation
- ⚙️ **Global Config** - Customizable exclusion rules
- 🚀 **Zero Dependencies** - Pure Python standard library implementation

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/TbusOS/CodeMetrics.git
cd CodeMetrics

# One-click installation
./scripts/install.sh
```

### 🚀 Quick Start

```bash
# Analyze driver code (embedded project)
codemetrics /path/to/driver -p embedded

# Analyze web project (medium complexity)
codemetrics /path/to/webapp -p semi-detached

# Analyze utility scripts (simple project)
codemetrics /path/to/scripts -p organic
```

### 📋 Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `path` | - | Directory path to analyze (required) |
| `--project-type` | `-p` | **Required** COCOMO project type: organic/semi-detached/embedded |
| `--top N` | `-n N` | Number of top files to display (default: 10) |
| `--exclude` | `-e` | Additional patterns to exclude (comma-separated) |
| `--no-color` | - | Disable colored output |
| `--no-save` | - | Don't save reports |

### 📊 Project Types

| Type | Description | Use Cases |
|------|-------------|-----------|
| **organic** | Simple projects | Small teams, familiar tech stack |
| **semi-detached** | Medium projects | Medium teams, mixed experience |
| **embedded** | Complex projects | Embedded, drivers, real-time systems |

### 🌐 Supported Languages

C, C++, Python, Java, JavaScript, TypeScript, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, C#, Shell, Perl, Lua, R, SQL, HTML, CSS, SCSS, Vue, React, Markdown, YAML, JSON, XML, Makefile, Dockerfile, and 50+ more languages.

### 📖 Documentation

- 📘 [Examples](examples/README.md)
- 📗 [Design Document](docs/DESIGN.md)
- 📙 [Contributing Guide](CONTRIBUTING.md)
- 📕 [Changelog](CHANGELOG.md)

### 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for developers worldwide**

[⭐ Star this project](https://github.com/TbusOS/CodeMetrics) if you find it helpful!

</div>
