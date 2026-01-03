# CodeMetrics - 代码度量分析工具

## 📋 设计文档 v1.0

### 1. 项目概述

**CodeMetrics** 是一个功能丰富的代码度量分析工具，结合了 cloc、tokei、scc 等工具的优点，
提供目录树结构展示、多维度代码分析、开发成本估算等功能。

#### 1.1 设计目标
- 🎯 **易用性**: 单文件 Python 脚本，无需安装依赖
- 🚀 **高性能**: 支持大型项目，并行处理
- 📊 **全面性**: 多维度统计分析
- 🎨 **美观性**: 彩色输出，多种格式支持
- 🔧 **可扩展**: 易于添加新语言支持

---

### 2. 功能设计

#### 2.1 核心功能

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 目录树展示 | 按树形结构显示文件和统计 | P0 |
| 行数统计 | 代码行/注释行/空行 分离统计 | P0 |
| 文件大小 | 显示每个文件和目录的大小 | P0 |
| 语言识别 | 自动识别 50+ 编程语言 | P0 |
| 按语言汇总 | 分语言统计表格 | P0 |

#### 2.2 增强功能

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 代码健康度 | 注释率、平均文件大小等指标 | P1 |
| COCOMO 估算 | 开发成本、人月、工期估算 | P1 |
| Top N 分析 | 最大文件、代码最多文件排行 | P1 |
| 复杂度警告 | 大文件、低注释率警告 | P1 |
| 多输出格式 | Terminal/Markdown/JSON/HTML | P1 |
| .gitignore | 自动过滤忽略文件 | P2 |
| 自定义过滤 | --exclude 参数 | P2 |

---

### 3. 数据结构设计

```python
@dataclass
class FileStats:
    """单个文件的统计信息"""
    path: str               # 文件路径
    language: str           # 编程语言
    size: int               # 文件大小(字节)
    total_lines: int        # 总行数
    code_lines: int         # 代码行数
    comment_lines: int      # 注释行数
    blank_lines: int        # 空行数

@dataclass
class DirStats:
    """目录的汇总统计"""
    path: str               # 目录路径
    file_count: int         # 文件数量
    total_size: int         # 总大小
    total_lines: int        # 总行数
    code_lines: int         # 代码行数
    comment_lines: int      # 注释行数
    blank_lines: int        # 空行数
    children: List          # 子项(文件或目录)

@dataclass
class LanguageStats:
    """按语言的汇总统计"""
    language: str           # 语言名称
    file_count: int         # 文件数
    total_lines: int        # 总行数
    code_lines: int         # 代码行数
    comment_lines: int      # 注释行数
    blank_lines: int        # 空行数
    total_size: int         # 总大小

@dataclass
class ProjectStats:
    """项目总统计"""
    root_path: str          # 项目根目录
    scan_time: float        # 扫描耗时
    dir_tree: DirStats      # 目录树
    by_language: Dict       # 按语言统计
    totals: Dict            # 总计
    health_metrics: Dict    # 健康度指标
    cocomo: Dict            # COCOMO 估算
```

---

### 4. 语言识别规则

```python
LANGUAGE_EXTENSIONS = {
    # 系统编程
    '.c': 'C',
    '.h': 'C Header',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.hpp': 'C++ Header',
    '.rs': 'Rust',
    '.go': 'Go',
    
    # 脚本语言
    '.py': 'Python',
    '.rb': 'Ruby',
    '.pl': 'Perl',
    '.sh': 'Shell',
    '.bash': 'Bash',
    
    # Web
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'React JSX',
    '.tsx': 'React TSX',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.vue': 'Vue',
    
    # JVM
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.groovy': 'Groovy',
    
    # 配置
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.toml': 'TOML',
    '.xml': 'XML',
    '.ini': 'INI',
    
    # 文档
    '.md': 'Markdown',
    '.rst': 'reStructuredText',
    '.txt': 'Text',
    
    # 其他
    '.sql': 'SQL',
    '.dockerfile': 'Dockerfile',
    '.makefile': 'Makefile',
}

# 特殊文件名识别
SPECIAL_FILES = {
    'Makefile': 'Makefile',
    'Dockerfile': 'Dockerfile',
    'Kconfig': 'Kconfig',
    'CMakeLists.txt': 'CMake',
}
```

---

### 5. 注释识别规则

```python
COMMENT_STYLES = {
    'C': {
        'line': ['//', '/*'],
        'block_start': '/*',
        'block_end': '*/',
    },
    'Python': {
        'line': ['#'],
        'block_start': '"""',
        'block_end': '"""',
        'alt_block_start': "'''",
        'alt_block_end': "'''",
    },
    'Shell': {
        'line': ['#'],
        'block_start': None,
        'block_end': None,
    },
    'HTML': {
        'line': [],
        'block_start': '<!--',
        'block_end': '-->',
    },
    # ... 更多语言
}
```

---

### 6. COCOMO 模型实现

#### 6.1 模型参数

```python
COCOMO_PARAMS = {
    'organic': {      # 简单项目
        'a': 2.4, 'b': 1.05,
        'c': 2.5, 'd': 0.38,
    },
    'semi-detached': { # 中等项目
        'a': 3.0, 'b': 1.12,
        'c': 2.5, 'd': 0.35,
    },
    'embedded': {      # 复杂/嵌入式项目
        'a': 3.6, 'b': 1.20,
        'c': 2.5, 'd': 0.32,
    },
}

# 成本参数(可配置)
COST_PER_PERSON_MONTH_USD = 5000   # 美元/人月
COST_PER_PERSON_MONTH_CNY = 30000  # 人民币/人月
```

#### 6.2 计算公式

```python
def calculate_cocomo(code_lines, project_type='semi-detached'):
    """
    计算 COCOMO 估算
    
    Returns:
        person_months: 人月数
        duration_months: 开发周期(月)
        team_size: 建议团队规模
        cost_usd: 成本估算(美元)
        cost_cny: 成本估算(人民币)
    """
    kloc = code_lines / 1000
    params = COCOMO_PARAMS[project_type]
    
    # 人月 = a * (KLOC)^b
    person_months = params['a'] * (kloc ** params['b'])
    
    # 工期 = c * (PM)^d
    duration_months = params['c'] * (person_months ** params['d'])
    
    # 团队规模 = PM / 工期
    team_size = person_months / duration_months if duration_months > 0 else 0
    
    # 成本
    cost_usd = person_months * COST_PER_PERSON_MONTH_USD
    cost_cny = person_months * COST_PER_PERSON_MONTH_CNY
    
    return {
        'person_months': round(person_months, 2),
        'duration_months': round(duration_months, 2),
        'team_size': round(team_size, 2),
        'cost_usd': round(cost_usd, 0),
        'cost_cny': round(cost_cny, 0),
    }
```

---

### 7. 健康度指标

```python
def calculate_health_metrics(stats):
    """计算代码健康度指标"""
    
    metrics = {}
    
    # 1. 注释率 (理想: 15-25%)
    comment_ratio = stats.comment_lines / stats.code_lines if stats.code_lines > 0 else 0
    metrics['comment_ratio'] = {
        'value': round(comment_ratio * 100, 1),
        'unit': '%',
        'status': 'good' if 0.15 <= comment_ratio <= 0.30 else 
                  'warning' if 0.10 <= comment_ratio <= 0.40 else 'bad',
        'suggestion': '建议注释率保持在 15-25%'
    }
    
    # 2. 平均文件大小 (理想: 100-500行)
    avg_lines = stats.total_lines / stats.file_count if stats.file_count > 0 else 0
    metrics['avg_file_lines'] = {
        'value': round(avg_lines, 0),
        'unit': '行',
        'status': 'good' if 100 <= avg_lines <= 500 else
                  'warning' if 50 <= avg_lines <= 800 else 'bad',
        'suggestion': '建议单文件保持在 100-500 行'
    }
    
    # 3. 代码密度 (代码行/总行)
    code_density = stats.code_lines / stats.total_lines if stats.total_lines > 0 else 0
    metrics['code_density'] = {
        'value': round(code_density * 100, 1),
        'unit': '%',
        'status': 'info',
        'suggestion': '代码密度反映有效代码占比'
    }
    
    # 4. 大文件警告
    large_files = [f for f in stats.files if f.code_lines > 1000]
    metrics['large_files'] = {
        'value': len(large_files),
        'unit': '个',
        'status': 'warning' if large_files else 'good',
        'files': [f.path for f in large_files[:5]],  # 最多显示5个
        'suggestion': '建议拆分超过 1000 行的大文件'
    }
    
    return metrics
```

---

### 8. 输出格式设计

#### 8.1 终端树形输出

```
📁 charge_dockv16/                         [24 files | 15,234 lines | 892 KB]
├── 📁 driver/                             [1 file | 327 lines | 12 KB]
│   └── 📄 charge_dock_drv.c               C        [285 | 32 | 10] 12.3 KB
├── 📁 include/                            [15 files | 3,456 lines | 156 KB]
│   ├── 📄 charge_dock_kapi.h              C Header [520 | 48 | 0] 24.5 KB
│   └── 📁 platform/                       [3 files | 890 lines | 32 KB]
│       ├── 📄 dts_parser.h                C Header [120 | 15 | 8] 4.2 KB
│       └── ...
├── 📁 platform/                           [4 files | 2,100 lines | 89 KB]
└── 📁 services/                           [6 files | 5,200 lines | 234 KB]

格式说明: [代码行 | 注释行 | 空行] 文件大小
```

#### 8.2 语言统计表格

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                              📊 语言统计                                      ║
╠════════════════╦═══════╦═════════╦═════════╦══════════╦══════════╦═══════════╣
║ 语言           ║ 文件  ║ 代码行  ║ 注释行  ║ 空行     ║ 总行数   ║ 大小      ║
╠════════════════╬═══════╬═════════╬═════════╬══════════╬══════════╬═══════════╣
║ C              ║    18 ║  12,456 ║   2,134 ║    1,023 ║   15,613 ║   623 KB  ║
║ C Header       ║    15 ║   2,890 ║     567 ║      234 ║    3,691 ║   156 KB  ║
║ Makefile       ║     2 ║     123 ║      45 ║       12 ║      180 ║   4.5 KB  ║
╠════════════════╬═══════╬═════════╬═════════╬══════════╬══════════╬═══════════╣
║ 总计           ║    35 ║  15,469 ║   2,746 ║    1,269 ║   19,484 ║   784 KB  ║
╚════════════════╩═══════╩═════════╩═════════╩══════════╩══════════╩═══════════╝
```

#### 8.3 COCOMO 估算输出

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           💰 开发成本估算 (COCOMO)                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 代码规模:     15,469 行代码 (15.47 KLOC)                                     ║
║ 项目类型:     嵌入式 (Embedded)                                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 📅 预估工期:     8.5 个月                                                     ║
║ 👥 建议团队:     2.3 人                                                       ║
║ ⏱️  总人月数:     19.5 人月                                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 💵 成本估算 (USD): $97,500                                                    ║
║ 💴 成本估算 (CNY): ¥585,000                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

### 9. 命令行接口

```bash
# 基本用法
codemetrics /path/to/project

# 常用选项
codemetrics /path/to/project --tree          # 显示目录树
codemetrics /path/to/project --summary       # 只显示汇总
codemetrics /path/to/project --top 10        # 显示 Top 10 文件
codemetrics /path/to/project --cocomo        # 显示成本估算
codemetrics /path/to/project --health        # 显示健康度指标

# 输出格式
codemetrics /path/to/project --format json   # JSON 输出
codemetrics /path/to/project --format md     # Markdown 输出
codemetrics /path/to/project --format html   # HTML 报告

# 过滤选项
codemetrics /path/to/project --exclude "test/*,docs/*"
codemetrics /path/to/project --lang "C,C++,Python"
codemetrics /path/to/project --gitignore     # 遵循 .gitignore

# 完整分析
codemetrics /path/to/project --all           # 启用所有功能
```

---

### 10. 项目结构

```
codemetrics/
├── DESIGN.md           # 设计文档 (本文件)
├── README.md           # 用户文档
├── LICENSE             # MIT 许可证
├── codemetrics.py        # 主程序 (单文件)
├── setup.py            # 安装脚本
└── examples/           # 示例输出
    ├── sample_output.txt
    ├── sample_output.json
    └── sample_output.html
```

---

### 11. 开发计划

| 阶段 | 内容 | 预计时间 |
|------|------|----------|
| Phase 1 | 核心功能: 目录树、行统计、语言识别 | 30分钟 |
| Phase 2 | 增强功能: COCOMO、健康度、Top N | 20分钟 |
| Phase 3 | 输出格式: Markdown、JSON、HTML | 15分钟 |
| Phase 4 | 文档和测试 | 10分钟 |

---

## 📝 更新日志

- v1.0 (2024-01-02): 初始设计

