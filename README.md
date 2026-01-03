# 📊 CodeMetrics

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/TbusOS/CodeMetrics.svg?style=social&label=Star)](https://github.com/TbusOS/CodeMetrics)

**A Powerful Code Metrics and Analysis Tool**

[English](README.md) | [中文](README_zh.md)

</div>

---

## ✨ Features

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

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/TbusOS/CodeMetrics.git
cd CodeMetrics

# One-click installation
./scripts/install.sh
```

The installation script will automatically:
- ✅ Check Python version (requires >= 3.6)
- ✅ Set executable permissions
- ✅ Create symbolic link to `~/.local/bin/codemetrics`
- ✅ Check and configure PATH

## 🚀 Quick Start

```bash
# Analyze embedded project (driver code)
codemetrics /path/to/driver -p embedded

# Analyze web project (medium complexity)
codemetrics /path/to/webapp -p semi-detached

# Analyze utility scripts (simple project)
codemetrics /path/to/scripts -p organic
```

**Default output includes:**
- 📂 Directory tree structure
- 📊 Language statistics table
- 💰 COCOMO cost estimation
- 🏥 Code health analysis
- 📈 Top 10 largest files

## 📋 Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `path` | - | Directory path to analyze (required) |
| `--project-type` | `-p` | **Required** COCOMO project type: organic/semi-detached/embedded |
| `--top N` | `-n N` | Number of top files to display (default: 10) |
| `--exclude` | `-e` | Additional patterns to exclude (comma-separated) |
| `--no-color` | - | Disable colored output |
| `--no-save` | - | Don't save reports |

## 📊 Project Types

| Type | Description | Use Cases |
|------|-------------|-----------|
| **organic** | Simple projects | Small teams, familiar tech stack |
| **semi-detached** | Medium projects | Medium teams, mixed experience |
| **embedded** | Complex projects | Embedded systems, drivers, real-time systems, hardware-related |

## 📖 Usage Examples

### Basic Analysis
```bash
codemetrics /path/to/project -p embedded
```

### Save Reports
```bash
# Automatically save JSON/Markdown/HTML reports
codemetrics /path/to/project -p embedded
# Reports saved in the output folder of the tool directory
```

### Show Top 20 Files
```bash
codemetrics /path/to/project -p embedded -n 20
```

### Exclude Additional Directories
```bash
codemetrics /path/to/project -p embedded -e "test/*,docs/*"
```

## 📊 Output Formats

CodeMetrics automatically generates reports in multiple formats:

### 1. Terminal Output (Default)
- Colored tree structure
- Formatted statistics tables
- Real-time progress display

### 2. JSON Format
```bash
# Location: output/report_YYYYMMDD_HHMMSS.json
```
Suitable for program parsing, CI/CD integration, data analysis

### 3. Markdown Format
```bash
# Location: output/report_YYYYMMDD_HHMMSS.md
```
Suitable for documentation generation, GitHub/GitLab display

### 4. HTML Format
```bash
# Location: output/report_YYYYMMDD_HHMMSS.html
```
Suitable for browser viewing, team sharing, presentation demos

## 🌐 Supported Languages

**System Programming**: C, C++, Rust, Go, Assembly

**Scripting Languages**: Python, Ruby, Perl, Shell, Bash, Lua

**Web Frontend**: JavaScript, TypeScript, React JSX, React TSX, HTML, CSS, SCSS, Vue

**JVM Languages**: Java, Kotlin, Scala, Groovy

**.NET Platform**: C#, F#

**Configuration**: JSON, YAML, TOML, XML, INI

**Documentation**: Markdown, reStructuredText

**Others**: SQL, Dockerfile, Makefile, CMake

And 50+ more programming languages.

## ⚙️ Configuration

Global configuration file located in tool directory: `config.json`

```json
{
  "name": "CodeMetrics Global Configuration",
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

## 🧮 COCOMO Model

COCOMO (Constructive Cost Model) is a software cost estimation model proposed by Barry Boehm.

### Calculation Formula

```
Person-Months (PM) = a × (KLOC)^b
Duration (months) = c × (PM)^d
Team Size = PM / Duration
```

### Model Parameters

| Type | a | b | c | d | Use Case |
|------|---|---|---|---|----------|
| organic | 2.4 | 1.05 | 2.5 | 0.38 | Simple projects |
| semi-detached | 3.0 | 1.12 | 2.5 | 0.35 | Medium projects |
| embedded | 3.6 | 1.20 | 2.5 | 0.32 | Complex projects |

## 🏥 Health Metrics

| Metric | Recommended Value | Description |
|--------|-------------------|-------------|
| Comment Ratio | 15-30% | Code maintainability |
| Average File Lines | 100-500 | Modularity level |
| Large Files (>800 lines) | 0 | Should be split |
| Low Comment Files (<5%) | 0 | Should add comments |

## 📖 Documentation

- 📘 [Examples](examples/README.md) - Detailed usage scenarios and examples
- 📗 [Design Document](docs/DESIGN.md) - Project architecture and design
- 📙 [Contributing Guide](CONTRIBUTING.md) - How to contribute
- 📕 [Changelog](CHANGELOG.md) - Version history and updates
- 📖 [COCOMO Model](docs/COCOMO.md) - Cost estimation model details

## 🎯 Use Cases

- 📱 **Embedded Development** - Linux kernel drivers, firmware development, real-time systems
- 🌐 **Web Development** - React/Vue frontend, Node.js/Django/Flask backend
- 🔧 **Utility Scripts** - Shell scripts, Python automation tools, DevOps scripts
- 📚 **Project Assessment** - Code review, cost estimation, technical debt analysis
- 🎓 **Education & Research** - Code metrics research, software engineering courses

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📖 Improve documentation
- 🔧 Submit Pull Requests
- 🌍 Add translations to other languages

## ❓ FAQ

### Q: Do I need to install additional Python packages?
A: No! CodeMetrics is implemented using pure Python standard library with zero dependencies.

### Q: Does it support Windows?
A: Primarily targeted at Linux/macOS. Windows users need to use WSL or Git Bash.

### Q: How to uninstall?
A: Run `./scripts/uninstall.sh`.

### Q: Where are the output reports saved?
A: By default, saved in the `<project_name>_output/` directory within the tool directory.

### Q: Can I customize COCOMO parameters?
A: Yes! Edit the `cocomo` section in the `config.json` file.

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/TbusOS/CodeMetrics)
- [Issue Tracker](https://github.com/TbusOS/CodeMetrics/issues)
- [Pull Requests](https://github.com/TbusOS/CodeMetrics/pulls)

---

<div align="center">

**Made with ❤️ for developers worldwide**

[⭐ Star this project](https://github.com/TbusOS/CodeMetrics) if you find it helpful!

</div>
