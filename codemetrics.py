#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeMetrics - 代码度量分析工具

一个功能丰富的代码度量工具，提供:
- 目录树结构展示
- 代码行/注释行/空行统计
- 多语言支持
- COCOMO 成本估算
- 代码健康度分析

Author: CodeMetrics Team
License: MIT
Version: 1.1.0
"""

import os
import sys
import argparse
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from collections import defaultdict
import time
import fnmatch
from datetime import datetime

# ============================================================================
# 版本信息
# ============================================================================
__version__ = "1.1.0"
__author__ = "CodeMetrics Team"

# ============================================================================
# 默认配置
# ============================================================================
DEFAULT_CONFIG = {
    "name": "CodeMetrics 配置文件",
    "version": "1.0",
    
    # 输出设置
    "output": {
        "dir": "codemetrics_output",      # 输出目录名
        "formats": ["terminal", "json", "markdown", "html"],  # 输出格式
        "auto_open": False,              # 是否自动打开 HTML 报告
    },
    
    # 排除规则
    "exclude": {
        "patterns": [
            "docs/*",
            "*.md",
            "*.json",
            "*.html",
            "*.txt",
            "*.pdf",
            "*.png",
            "*.jpg",
            "*.gif",
        ],
        "dirs": [
            ".git",
            ".svn",
            "node_modules",
            "__pycache__",
            "build",
            "dist",
            ".venv",
            "venv",
        ],
    },
    
    # COCOMO 设置
    "cocomo": {
        "project_type": "semi-detached",  # organic / semi-detached / embedded
        "cost_per_month_usd": 5000,
        "cost_per_month_cny": 30000,
    },
    
    # 健康度阈值
    "health": {
        "comment_ratio_min": 0.15,
        "comment_ratio_max": 0.30,
        "avg_file_lines_min": 100,
        "avg_file_lines_max": 500,
        "large_file_threshold": 800,
        "low_comment_threshold": 0.05,
    },
    
    # 显示选项
    "display": {
        "show_tree": True,
        "show_cocomo": True,
        "show_health": True,
        "top_n": 10,
        "use_colors": True,
    },
}

CONFIG_FILENAME = ".codemetrics.json"
GLOBAL_CONFIG_FILENAME = "config.json"  # 工具目录下的全局配置

# ============================================================================
# 颜色定义 (ANSI)
# ============================================================================
class Colors:
    """终端颜色"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # 前景色
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # 亮色
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

# 是否启用颜色
USE_COLORS = sys.stdout.isatty()

def color(text: str, c: str) -> str:
    """给文本添加颜色"""
    if USE_COLORS:
        return f"{c}{text}{Colors.RESET}"
    return text

# ============================================================================
# 语言定义
# ============================================================================
LANGUAGE_EXTENSIONS = {
    # 系统编程
    '.c': 'C',
    '.h': 'C/C++ Header',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.hpp': 'C++ Header',
    '.hxx': 'C++ Header',
    '.rs': 'Rust',
    '.go': 'Go',
    '.asm': 'Assembly',
    '.s': 'Assembly',
    '.S': 'Assembly',
    
    # 脚本语言
    '.py': 'Python',
    '.pyw': 'Python',
    '.rb': 'Ruby',
    '.pl': 'Perl',
    '.pm': 'Perl',
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.zsh': 'Zsh',
    '.fish': 'Fish',
    '.lua': 'Lua',
    '.tcl': 'Tcl',
    '.awk': 'AWK',
    
    # Web 前端
    '.js': 'JavaScript',
    '.mjs': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'React JSX',
    '.tsx': 'React TSX',
    '.html': 'HTML',
    '.htm': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.less': 'Less',
    '.vue': 'Vue',
    '.svelte': 'Svelte',
    
    # JVM
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.kts': 'Kotlin',
    '.scala': 'Scala',
    '.groovy': 'Groovy',
    '.clj': 'Clojure',
    
    # .NET
    '.cs': 'C#',
    '.fs': 'F#',
    '.vb': 'Visual Basic',
    
    # 函数式
    '.hs': 'Haskell',
    '.ml': 'OCaml',
    '.mli': 'OCaml',
    '.erl': 'Erlang',
    '.ex': 'Elixir',
    '.exs': 'Elixir',
    
    # 配置
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.toml': 'TOML',
    '.xml': 'XML',
    '.ini': 'INI',
    '.cfg': 'Config',
    '.conf': 'Config',
    '.properties': 'Properties',
    
    # 文档
    '.md': 'Markdown',
    '.markdown': 'Markdown',
    '.rst': 'reStructuredText',
    '.txt': 'Text',
    '.tex': 'LaTeX',
    
    # 数据库
    '.sql': 'SQL',
    
    # DevOps
    '.dockerfile': 'Dockerfile',
    '.tf': 'Terraform',
    '.hcl': 'HCL',
    
    # 其他
    '.r': 'R',
    '.R': 'R',
    '.m': 'MATLAB/Objective-C',
    '.swift': 'Swift',
    '.dart': 'Dart',
    '.php': 'PHP',
    '.proto': 'Protocol Buffers',
    '.thrift': 'Thrift',
}

# 特殊文件名
SPECIAL_FILES = {
    'Makefile': 'Makefile',
    'makefile': 'Makefile',
    'GNUmakefile': 'Makefile',
    'Dockerfile': 'Dockerfile',
    'dockerfile': 'Dockerfile',
    'Kconfig': 'Kconfig',
    'CMakeLists.txt': 'CMake',
    'meson.build': 'Meson',
    'BUILD': 'Bazel',
    'BUILD.bazel': 'Bazel',
    'WORKSPACE': 'Bazel',
    'Cargo.toml': 'Cargo',
    'go.mod': 'Go Module',
    'package.json': 'npm',
    'requirements.txt': 'pip',
    'Gemfile': 'Ruby Gems',
    '.gitignore': 'Git Config',
    '.gitattributes': 'Git Config',
}

# 注释风格
COMMENT_STYLES = {
    'C': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'C/C++ Header': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'C++': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'C++ Header': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'Java': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'JavaScript': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'TypeScript': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'Go': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'Rust': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'Swift': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'Kotlin': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'Scala': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'C#': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'PHP': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    'Dart': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    
    'Python': {'line': '#', 'block_start': '"""', 'block_end': '"""'},
    'Ruby': {'line': '#', 'block_start': '=begin', 'block_end': '=end'},
    'Shell': {'line': '#', 'block_start': None, 'block_end': None},
    'Bash': {'line': '#', 'block_start': None, 'block_end': None},
    'Perl': {'line': '#', 'block_start': '=pod', 'block_end': '=cut'},
    'R': {'line': '#', 'block_start': None, 'block_end': None},
    'YAML': {'line': '#', 'block_start': None, 'block_end': None},
    'TOML': {'line': '#', 'block_start': None, 'block_end': None},
    'Makefile': {'line': '#', 'block_start': None, 'block_end': None},
    'Dockerfile': {'line': '#', 'block_start': None, 'block_end': None},
    'Kconfig': {'line': '#', 'block_start': None, 'block_end': None},
    
    'HTML': {'line': None, 'block_start': '<!--', 'block_end': '-->'},
    'XML': {'line': None, 'block_start': '<!--', 'block_end': '-->'},
    'CSS': {'line': None, 'block_start': '/*', 'block_end': '*/'},
    'SCSS': {'line': '//', 'block_start': '/*', 'block_end': '*/'},
    
    'SQL': {'line': '--', 'block_start': '/*', 'block_end': '*/'},
    'Lua': {'line': '--', 'block_start': '--[[', 'block_end': ']]'},
    'Haskell': {'line': '--', 'block_start': '{-', 'block_end': '-}'},
    
    'Lisp': {'line': ';', 'block_start': None, 'block_end': None},
    'Clojure': {'line': ';', 'block_start': None, 'block_end': None},
    
    'Assembly': {'line': ';', 'block_start': None, 'block_end': None},
}

# 默认注释风格
DEFAULT_COMMENT_STYLE = {'line': '#', 'block_start': None, 'block_end': None}

# ============================================================================
# COCOMO 模型参数
# ============================================================================
COCOMO_PARAMS = {
    'organic': {'a': 2.4, 'b': 1.05, 'c': 2.5, 'd': 0.38, 'desc': '简单项目'},
    'semi-detached': {'a': 3.0, 'b': 1.12, 'c': 2.5, 'd': 0.35, 'desc': '中等项目'},
    'embedded': {'a': 3.6, 'b': 1.20, 'c': 2.5, 'd': 0.32, 'desc': '复杂/嵌入式'},
}

COST_PER_PERSON_MONTH_USD = 5000
COST_PER_PERSON_MONTH_CNY = 30000

# ============================================================================
# 数据结构
# ============================================================================
@dataclass
class FileStats:
    """单个文件的统计信息"""
    path: str
    name: str
    language: str
    size: int
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int

@dataclass
class DirStats:
    """目录的汇总统计"""
    path: str
    name: str
    file_count: int = 0
    dir_count: int = 0
    total_size: int = 0
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    children: List = field(default_factory=list)

@dataclass  
class LanguageStats:
    """按语言的汇总统计"""
    language: str
    file_count: int = 0
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    total_size: int = 0

# ============================================================================
# 核心功能
# ============================================================================
def detect_language(file_path: str) -> str:
    """检测文件的编程语言"""
    name = os.path.basename(file_path)
    
    # 检查特殊文件名
    if name in SPECIAL_FILES:
        return SPECIAL_FILES[name]
    
    # 检查扩展名
    ext = os.path.splitext(name)[1].lower()
    if ext in LANGUAGE_EXTENSIONS:
        return LANGUAGE_EXTENSIONS[ext]
    
    # 检查 shebang
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline()
            if first_line.startswith('#!'):
                if 'python' in first_line:
                    return 'Python'
                elif 'bash' in first_line or 'sh' in first_line:
                    return 'Shell'
                elif 'ruby' in first_line:
                    return 'Ruby'
                elif 'perl' in first_line:
                    return 'Perl'
                elif 'node' in first_line:
                    return 'JavaScript'
    except:
        pass
    
    return 'Unknown'


def count_lines(file_path: str, language: str) -> Tuple[int, int, int, int]:
    """
    统计文件行数
    
    Returns:
        (total_lines, code_lines, comment_lines, blank_lines)
    """
    style = COMMENT_STYLES.get(language, DEFAULT_COMMENT_STYLE)
    
    total = 0
    code = 0
    comment = 0
    blank = 0
    in_block_comment = False
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total += 1
                stripped = line.strip()
                
                # 空行
                if not stripped:
                    blank += 1
                    continue
                
                # 块注释处理
                if in_block_comment:
                    comment += 1
                    if style['block_end'] and style['block_end'] in stripped:
                        in_block_comment = False
                    continue
                
                # 检查块注释开始
                if style['block_start'] and style['block_start'] in stripped:
                    # 检查是否同行结束
                    if style['block_end'] and style['block_end'] in stripped:
                        # 同行开始和结束，如 /* comment */
                        idx_start = stripped.find(style['block_start'])
                        idx_end = stripped.find(style['block_end'])
                        if idx_end > idx_start:
                            # 检查块注释外是否有代码
                            before = stripped[:idx_start].strip()
                            after = stripped[idx_end + len(style['block_end']):].strip()
                            if before or after:
                                code += 1
                            else:
                                comment += 1
                            continue
                    else:
                        in_block_comment = True
                        # 检查块注释开始前是否有代码
                        idx = stripped.find(style['block_start'])
                        if stripped[:idx].strip():
                            code += 1
                        else:
                            comment += 1
                        continue
                
                # 行注释
                if style['line'] and stripped.startswith(style['line']):
                    comment += 1
                    continue
                
                # 代码行
                code += 1
                
    except Exception as e:
        # 无法读取的文件
        pass
    
    return total, code, comment, blank


def get_file_size(file_path: str) -> int:
    """获取文件大小"""
    try:
        return os.path.getsize(file_path)
    except:
        return 0


def format_size(size: int) -> str:
    """格式化文件大小"""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.1f} GB"


def format_number(num: int) -> str:
    """格式化数字，添加千位分隔符"""
    return f"{num:,}"


def should_ignore(path: str, ignore_patterns: List[str]) -> bool:
    """检查路径是否应该被忽略"""
    name = os.path.basename(path)
    
    # 默认忽略
    default_ignore = [
        '.git', '.svn', '.hg', '.bzr',
        '__pycache__', '.pytest_cache', '.mypy_cache',
        'node_modules', 'bower_components',
        '.idea', '.vscode', '.vs',
        'venv', '.venv', 'env', '.env',
        'build', 'dist', 'target', 'out',
        '*.pyc', '*.pyo', '*.o', '*.obj', '*.ko',
        '*.so', '*.dll', '*.dylib', '*.a', '*.lib',
        '*.exe', '*.bin',
        '*.jpg', '*.jpeg', '*.png', '*.gif', '*.ico',
        '*.pdf', '*.doc', '*.docx',
        '*.zip', '*.tar', '*.gz', '*.rar',
    ]
    
    all_patterns = default_ignore + ignore_patterns
    
    for pattern in all_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    
    return False


def is_text_file(file_path: str) -> bool:
    """检查是否是文本文件"""
    # 通过扩展名快速判断
    ext = os.path.splitext(file_path)[1].lower()
    if ext in LANGUAGE_EXTENSIONS:
        return True
    
    name = os.path.basename(file_path)
    if name in SPECIAL_FILES:
        return True
    
    # 尝试读取
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:  # 二进制文件
                return False
        return True
    except:
        return False


def scan_file(file_path: str) -> Optional[FileStats]:
    """扫描单个文件"""
    if not is_text_file(file_path):
        return None
    
    language = detect_language(file_path)
    if language == 'Unknown':
        return None
    
    size = get_file_size(file_path)
    total, code, comment, blank = count_lines(file_path, language)
    
    return FileStats(
        path=file_path,
        name=os.path.basename(file_path),
        language=language,
        size=size,
        total_lines=total,
        code_lines=code,
        comment_lines=comment,
        blank_lines=blank,
    )


def scan_directory(dir_path: str, ignore_patterns: List[str] = None) -> DirStats:
    """递归扫描目录"""
    if ignore_patterns is None:
        ignore_patterns = []
    
    dir_stats = DirStats(
        path=dir_path,
        name=os.path.basename(dir_path) or dir_path,
    )
    
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return dir_stats
    
    for entry in entries:
        entry_path = os.path.join(dir_path, entry)
        
        if should_ignore(entry_path, ignore_patterns):
            continue
        
        if os.path.isdir(entry_path):
            # 递归扫描子目录
            sub_stats = scan_directory(entry_path, ignore_patterns)
            if sub_stats.file_count > 0:  # 只保留有文件的目录
                dir_stats.children.append(sub_stats)
                dir_stats.dir_count += 1 + sub_stats.dir_count
                dir_stats.file_count += sub_stats.file_count
                dir_stats.total_size += sub_stats.total_size
                dir_stats.total_lines += sub_stats.total_lines
                dir_stats.code_lines += sub_stats.code_lines
                dir_stats.comment_lines += sub_stats.comment_lines
                dir_stats.blank_lines += sub_stats.blank_lines
        else:
            # 扫描文件
            file_stats = scan_file(entry_path)
            if file_stats:
                dir_stats.children.append(file_stats)
                dir_stats.file_count += 1
                dir_stats.total_size += file_stats.size
                dir_stats.total_lines += file_stats.total_lines
                dir_stats.code_lines += file_stats.code_lines
                dir_stats.comment_lines += file_stats.comment_lines
                dir_stats.blank_lines += file_stats.blank_lines
    
    return dir_stats


def collect_by_language(dir_stats: DirStats) -> Dict[str, LanguageStats]:
    """按语言收集统计"""
    lang_stats = defaultdict(lambda: LanguageStats(language=''))
    
    def collect(node):
        if isinstance(node, FileStats):
            lang = node.language
            if not lang_stats[lang].language:
                lang_stats[lang].language = lang
            lang_stats[lang].file_count += 1
            lang_stats[lang].total_lines += node.total_lines
            lang_stats[lang].code_lines += node.code_lines
            lang_stats[lang].comment_lines += node.comment_lines
            lang_stats[lang].blank_lines += node.blank_lines
            lang_stats[lang].total_size += node.size
        elif isinstance(node, DirStats):
            for child in node.children:
                collect(child)
    
    collect(dir_stats)
    return dict(lang_stats)


def collect_all_files(dir_stats: DirStats) -> List[FileStats]:
    """收集所有文件"""
    files = []
    
    def collect(node):
        if isinstance(node, FileStats):
            files.append(node)
        elif isinstance(node, DirStats):
            for child in node.children:
                collect(child)
    
    collect(dir_stats)
    return files


def calculate_cocomo(code_lines: int, project_type: str = 'semi-detached') -> Dict:
    """计算 COCOMO 估算"""
    if code_lines == 0:
        return {
            'kloc': 0,
            'person_months': 0,
            'duration_months': 0,
            'team_size': 0,
            'cost_usd': 0,
            'cost_cny': 0,
            'project_type': project_type,
        }
    
    kloc = code_lines / 1000
    params = COCOMO_PARAMS.get(project_type, COCOMO_PARAMS['semi-detached'])
    
    person_months = params['a'] * (kloc ** params['b'])
    duration_months = params['c'] * (person_months ** params['d'])
    team_size = person_months / duration_months if duration_months > 0 else 0
    
    return {
        'kloc': round(kloc, 2),
        'person_months': round(person_months, 1),
        'duration_months': round(duration_months, 1),
        'team_size': round(team_size, 1),
        'cost_usd': int(person_months * COST_PER_PERSON_MONTH_USD),
        'cost_cny': int(person_months * COST_PER_PERSON_MONTH_CNY),
        'project_type': project_type,
        'project_type_desc': params['desc'],
    }


def calculate_health(dir_stats: DirStats, all_files: List[FileStats]) -> Dict:
    """计算代码健康度指标"""
    metrics = {}
    
    # 注释率
    if dir_stats.code_lines > 0:
        ratio = dir_stats.comment_lines / dir_stats.code_lines
        metrics['comment_ratio'] = {
            'value': round(ratio * 100, 1),
            'unit': '%',
            'status': 'good' if 0.15 <= ratio <= 0.30 else 
                      'warning' if 0.10 <= ratio <= 0.40 else 'bad',
            'desc': '注释率 (建议 15-30%)',
        }
    
    # 平均文件行数
    if dir_stats.file_count > 0:
        avg = dir_stats.total_lines / dir_stats.file_count
        metrics['avg_file_lines'] = {
            'value': int(avg),
            'unit': '行',
            'status': 'good' if 100 <= avg <= 500 else
                      'warning' if 50 <= avg <= 800 else 'bad',
            'desc': '平均文件行数 (建议 100-500)',
        }
    
    # 代码密度
    if dir_stats.total_lines > 0:
        density = dir_stats.code_lines / dir_stats.total_lines
        metrics['code_density'] = {
            'value': round(density * 100, 1),
            'unit': '%',
            'status': 'info',
            'desc': '代码密度 (代码行/总行)',
        }
    
    # 大文件警告
    large_files = [f for f in all_files if f.code_lines > 800]
    metrics['large_files'] = {
        'value': len(large_files),
        'unit': '个',
        'status': 'warning' if large_files else 'good',
        'desc': '大文件 (>800行代码)',
        'files': [{'path': f.path, 'lines': f.code_lines} for f in large_files[:5]],
    }
    
    # 低注释文件
    low_comment_files = [f for f in all_files 
                         if f.code_lines > 100 and 
                         f.comment_lines / f.code_lines < 0.05 if f.code_lines > 0]
    metrics['low_comment_files'] = {
        'value': len(low_comment_files),
        'unit': '个',
        'status': 'warning' if low_comment_files else 'good',
        'desc': '低注释文件 (<5%注释)',
        'files': [{'path': f.path, 'ratio': round(f.comment_lines/f.code_lines*100, 1) if f.code_lines > 0 else 0} 
                  for f in low_comment_files[:5]],
    }
    
    return metrics


# ============================================================================
# 输出格式化
# ============================================================================
def generate_tree_text(node, prefix: str = "", is_last: bool = True) -> List[str]:
    """生成目录树的纯文本（用于保存到文件）"""
    lines = []
    connector = "└── " if is_last else "├── "
    
    if isinstance(node, DirStats):
        # 目录
        stats = f"[{node.file_count} files | {format_number(node.code_lines)} code | {format_size(node.total_size)}]"
        lines.append(f"{prefix}{connector}📁 {node.name}/ {stats}")
        
        # 子项
        new_prefix = prefix + ("    " if is_last else "│   ")
        children = node.children
        for i, child in enumerate(children):
            lines.extend(generate_tree_text(child, new_prefix, i == len(children) - 1))
    else:
        # 文件
        stats = f"[{node.code_lines}|{node.comment_lines}|{node.blank_lines}]"
        lines.append(f"{prefix}{connector}📄 {node.name} [{node.language}] {stats} {format_size(node.size)}")
    
    return lines


def print_tree(node, prefix: str = "", is_last: bool = True, show_details: bool = True):
    """打印目录树"""
    connector = "└── " if is_last else "├── "
    
    if isinstance(node, DirStats):
        # 目录
        icon = "📁"
        name = color(node.name + "/", Colors.BRIGHT_BLUE + Colors.BOLD)
        stats = color(f"[{node.file_count} files | {format_number(node.code_lines)} code | {format_size(node.total_size)}]", Colors.DIM)
        print(f"{prefix}{connector}{icon} {name} {stats}")
        
        # 子项
        new_prefix = prefix + ("    " if is_last else "│   ")
        children = node.children
        for i, child in enumerate(children):
            print_tree(child, new_prefix, i == len(children) - 1, show_details)
    else:
        # 文件
        icon = "📄"
        name = node.name
        lang = color(f"[{node.language}]", Colors.CYAN)
        if show_details:
            stats = color(f"[{node.code_lines}|{node.comment_lines}|{node.blank_lines}]", Colors.DIM)
            size = color(format_size(node.size), Colors.DIM)
            print(f"{prefix}{connector}{icon} {name} {lang} {stats} {size}")
        else:
            print(f"{prefix}{connector}{icon} {name} {lang}")


def print_language_table(lang_stats: Dict[str, LanguageStats]):
    """打印语言统计表格（简洁版）"""
    # 排序：按代码行数降序
    sorted_langs = sorted(lang_stats.values(), key=lambda x: x.code_lines, reverse=True)
    
    # 计算总计
    total = LanguageStats(language='Total')
    for ls in sorted_langs:
        total.file_count += ls.file_count
        total.total_lines += ls.total_lines
        total.code_lines += ls.code_lines
        total.comment_lines += ls.comment_lines
        total.blank_lines += ls.blank_lines
        total.total_size += ls.total_size
    
    print()
    print(color("Language Statistics", Colors.BOLD + Colors.CYAN))
    print(color("=" * 95, Colors.DIM))
    
    # 表头
    header = f"{'Language':<18} {'Files':>8} {'Code':>12} {'Comment':>12} {'Blank':>10} {'Total':>12} {'Size':>12}"
    print(color(header, Colors.BOLD))
    print(color("-" * 95, Colors.DIM))
    
    # 数据行
    for ls in sorted_langs:
        row = f"{ls.language:<18} {ls.file_count:>8} {ls.code_lines:>12,} {ls.comment_lines:>12,} {ls.blank_lines:>10,} {ls.total_lines:>12,} {format_size(ls.total_size):>12}"
        print(row)
    
    # 总计行
    print(color("-" * 95, Colors.DIM))
    total_row = f"{total.language:<18} {total.file_count:>8} {total.code_lines:>12,} {total.comment_lines:>12,} {total.blank_lines:>10,} {total.total_lines:>12,} {format_size(total.total_size):>12}"
    print(color(total_row, Colors.BOLD + Colors.GREEN))
    print(color("=" * 95, Colors.DIM))


def print_cocomo(cocomo: Dict):
    """打印 COCOMO 估算"""
    print()
    print(color("COCOMO Cost Estimation", Colors.BOLD + Colors.YELLOW))
    print(color("=" * 60, Colors.DIM))
    print(f"  Code Size:      {cocomo['kloc']:,.2f} KLOC ({int(cocomo['kloc'] * 1000):,} lines)")
    print(f"  Project Type:   {cocomo['project_type_desc']} ({cocomo['project_type']})")
    print(color("-" * 60, Colors.DIM))
    print(f"  Duration:       {cocomo['duration_months']:.1f} months")
    print(f"  Team Size:      {cocomo['team_size']:.1f} persons")
    print(f"  Person-Months:  {cocomo['person_months']:.1f} PM")
    print(color("-" * 60, Colors.DIM))
    print(color(f"  Cost (USD):     ${cocomo['cost_usd']:,}", Colors.GREEN))
    print(color(f"  Cost (CNY):     {cocomo['cost_cny']:,} CNY", Colors.GREEN))
    print(color("=" * 60, Colors.DIM))


def print_health(health: Dict):
    """打印健康度指标"""
    print()
    print(color("Code Health Metrics", Colors.BOLD + Colors.MAGENTA))
    print(color("=" * 60, Colors.DIM))
    
    status_icons = {'good': '[OK]', 'warning': '[WARN]', 'bad': '[BAD]', 'info': '[INFO]'}
    status_colors = {'good': Colors.GREEN, 'warning': Colors.YELLOW, 'bad': Colors.RED, 'info': Colors.CYAN}
    
    for key, metric in health.items():
        icon = status_icons[metric['status']]
        clr = status_colors[metric['status']]
        line = f"  {icon:<8} {metric['desc']}: {metric['value']} {metric['unit']}"
        print(color(line, clr))
        
        if key in ['large_files', 'low_comment_files'] and metric['value'] > 0:
            for f in metric.get('files', [])[:3]:
                if 'lines' in f:
                    file_line = f"           - {os.path.basename(f['path'])} ({f['lines']} lines)"
                else:
                    file_line = f"           - {os.path.basename(f['path'])} ({f['ratio']}%)"
                print(color(file_line, Colors.DIM))
    
    print(color("=" * 60, Colors.DIM))


def print_top_files(all_files: List[FileStats], n: int = 10):
    """打印 Top N 文件"""
    print()
    print(color(f"Top {n} Files (by code lines)", Colors.BOLD))
    print(color("=" * 80, Colors.DIM))
    
    sorted_files = sorted(all_files, key=lambda x: x.code_lines, reverse=True)[:n]
    
    for i, f in enumerate(sorted_files, 1):
        ratio = f.comment_lines / f.code_lines * 100 if f.code_lines > 0 else 0
        print(f"  {i:2}. {os.path.basename(f.path)}")
        print(color(f"     {f.language} | {f.code_lines:,} 代码行 | {f.comment_lines:,} 注释行 ({ratio:.1f}%) | {format_size(f.size)}", Colors.DIM))


def generate_json(dir_stats: DirStats, lang_stats: Dict, cocomo: Dict, health: Dict) -> str:
    """生成 JSON 输出"""
    def node_to_dict(node):
        if isinstance(node, FileStats):
            return asdict(node)
        elif isinstance(node, DirStats):
            d = {
                'path': node.path,
                'name': node.name,
                'type': 'directory',
                'file_count': node.file_count,
                'dir_count': node.dir_count,
                'total_size': node.total_size,
                'total_lines': node.total_lines,
                'code_lines': node.code_lines,
                'comment_lines': node.comment_lines,
                'blank_lines': node.blank_lines,
                'children': [node_to_dict(c) for c in node.children],
            }
            return d
    
    result = {
        'tree': node_to_dict(dir_stats),
        'by_language': {k: asdict(v) for k, v in lang_stats.items()},
        'cocomo': cocomo,
        'health': health,
    }
    
    return json.dumps(result, indent=2, ensure_ascii=False)


def generate_markdown(dir_stats: DirStats, lang_stats: Dict, cocomo: Dict, health: Dict, all_files: List[FileStats] = None) -> str:
    """生成 Markdown 输出"""
    lines = []
    lines.append(f"# 📊 代码统计报告: {dir_stats.name}")
    lines.append("")
    lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## 📋 概览")
    lines.append("")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 文件数 | {dir_stats.file_count} |")
    lines.append(f"| 代码行 | {dir_stats.code_lines:,} |")
    lines.append(f"| 注释行 | {dir_stats.comment_lines:,} |")
    lines.append(f"| 空行 | {dir_stats.blank_lines:,} |")
    lines.append(f"| 总行数 | {dir_stats.total_lines:,} |")
    lines.append(f"| 总大小 | {format_size(dir_stats.total_size)} |")
    lines.append("")
    
    # 目录树
    lines.append("## 📂 目录结构")
    lines.append("")
    lines.append("> 📖 图例: `[代码行|注释行|空行]`")
    lines.append("")
    lines.append("```")
    tree_lines = generate_tree_text(dir_stats)
    lines.extend(tree_lines)
    lines.append("```")
    lines.append("")
    
    # 语言统计
    lines.append("## 📊 语言统计")
    lines.append("")
    lines.append("| 语言 | 文件 | 代码行 | 注释行 | 空行 | 总大小 |")
    lines.append("|------|------|--------|--------|------|--------|")
    
    sorted_langs = sorted(lang_stats.values(), key=lambda x: x.code_lines, reverse=True)
    for ls in sorted_langs:
        lines.append(f"| {ls.language} | {ls.file_count} | {ls.code_lines:,} | {ls.comment_lines:,} | {ls.blank_lines:,} | {format_size(ls.total_size)} |")
    
    # 总计
    lines.append(f"| **总计** | **{dir_stats.file_count}** | **{dir_stats.code_lines:,}** | **{dir_stats.comment_lines:,}** | **{dir_stats.blank_lines:,}** | **{format_size(dir_stats.total_size)}** |")
    lines.append("")
    
    # COCOMO
    lines.append("## 💰 开发成本估算 (COCOMO)")
    lines.append("")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 代码规模 | {cocomo['kloc']:.2f} KLOC ({int(cocomo['kloc']*1000):,} 行) |")
    lines.append(f"| 项目类型 | {cocomo['project_type_desc']} ({cocomo['project_type']}) |")
    lines.append(f"| 预估工期 | {cocomo['duration_months']:.1f} 个月 |")
    lines.append(f"| 建议团队 | {cocomo['team_size']:.1f} 人 |")
    lines.append(f"| 总人月数 | {cocomo['person_months']:.1f} 人月 |")
    lines.append(f"| 成本 (USD) | ${cocomo['cost_usd']:,} |")
    lines.append(f"| 成本 (CNY) | ¥{cocomo['cost_cny']:,} |")
    lines.append("")
    
    # 健康度
    lines.append("## 🏥 代码健康度")
    lines.append("")
    lines.append("| 指标 | 数值 | 状态 |")
    lines.append("|------|------|------|")
    
    status_emoji = {'good': '✅', 'warning': '⚠️', 'bad': '❌', 'info': 'ℹ️'}
    for key, metric in health.items():
        if key not in ['large_files', 'low_comment_files']:
            emoji = status_emoji.get(metric['status'], '')
            lines.append(f"| {metric['desc']} | {metric['value']} {metric['unit']} | {emoji} |")
    
    # 大文件
    if health.get('large_files', {}).get('value', 0) > 0:
        lines.append("")
        lines.append(f"### ⚠️ 大文件警告 ({health['large_files']['value']} 个)")
        lines.append("")
        for f in health['large_files'].get('files', [])[:10]:
            lines.append(f"- `{f['path']}` ({f['lines']} 行)")
    
    lines.append("")
    
    # Top 10
    if all_files:
        lines.append("## 📈 Top 10 文件")
        lines.append("")
        lines.append("| 排名 | 文件 | 语言 | 代码行 | 注释率 |")
        lines.append("|------|------|------|--------|--------|")
        
        sorted_files = sorted(all_files, key=lambda x: x.code_lines, reverse=True)[:10]
        for i, f in enumerate(sorted_files, 1):
            ratio = f.comment_lines / f.code_lines * 100 if f.code_lines > 0 else 0
            lines.append(f"| {i} | `{os.path.basename(f.path)}` | {f.language} | {f.code_lines:,} | {ratio:.1f}% |")
        
        lines.append("")
    
    return "\n".join(lines)


def generate_html(dir_stats: DirStats, lang_stats: Dict, cocomo: Dict, health: Dict, all_files: List[FileStats] = None) -> str:
    """生成 HTML 报告"""
    
    # 语言统计表格行
    lang_rows = ""
    sorted_langs = sorted(lang_stats.values(), key=lambda x: x.code_lines, reverse=True)
    for ls in sorted_langs:
        lang_rows += f"""
            <tr>
                <td>{ls.language}</td>
                <td>{ls.file_count}</td>
                <td>{ls.code_lines:,}</td>
                <td>{ls.comment_lines:,}</td>
                <td>{ls.blank_lines:,}</td>
                <td>{format_size(ls.total_size)}</td>
            </tr>"""
    
    # Top 10 表格行
    top_rows = ""
    if all_files:
        sorted_files = sorted(all_files, key=lambda x: x.code_lines, reverse=True)[:10]
        for i, f in enumerate(sorted_files, 1):
            ratio = f.comment_lines / f.code_lines * 100 if f.code_lines > 0 else 0
            top_rows += f"""
            <tr>
                <td>{i}</td>
                <td title="{f.path}">{os.path.basename(f.path)}</td>
                <td>{f.language}</td>
                <td>{f.code_lines:,}</td>
                <td>{ratio:.1f}%</td>
            </tr>"""
    
    # 健康度状态
    def get_health_class(status):
        return {'good': 'good', 'warning': 'warning', 'bad': 'bad', 'info': 'info'}.get(status, '')
    
    health_rows = ""
    for key, metric in health.items():
        if key not in ['large_files', 'low_comment_files']:
            cls = get_health_class(metric['status'])
            health_rows += f"""
            <tr class="{cls}">
                <td>{metric['desc']}</td>
                <td>{metric['value']} {metric['unit']}</td>
            </tr>"""
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>代码统计报告 - {dir_stats.name}</title>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-yellow: #d29922;
            --accent-red: #f85149;
            --accent-purple: #a371f7;
            --border-color: #30363d;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: var(--accent-blue);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}
        
        h2 {{
            color: var(--text-primary);
            margin: 30px 0 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .timestamp {{
            color: var(--text-secondary);
            font-size: 14px;
            margin-bottom: 20px;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
        }}
        
        .card h3 {{
            color: var(--accent-purple);
            margin-bottom: 15px;
            font-size: 16px;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: var(--accent-blue);
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 14px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-secondary);
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 20px;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        
        th {{
            background: var(--bg-tertiary);
            color: var(--text-primary);
            font-weight: 600;
        }}
        
        tr:hover {{
            background: var(--bg-tertiary);
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        .good {{ background: rgba(63, 185, 80, 0.1); }}
        .warning {{ background: rgba(210, 153, 34, 0.1); }}
        .bad {{ background: rgba(248, 81, 73, 0.1); }}
        
        .cocomo-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        
        .cocomo-item {{
            text-align: center;
            padding: 15px;
            background: var(--bg-tertiary);
            border-radius: 8px;
        }}
        
        .cocomo-value {{
            font-size: 24px;
            font-weight: bold;
            color: var(--accent-yellow);
        }}
        
        .cost {{
            color: var(--accent-green);
        }}
        
        .tree-container {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            overflow-x: auto;
        }}
        
        .tree-content {{
            font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
            font-size: 13px;
            line-height: 1.8;
            white-space: pre;
            color: var(--text-primary);
        }}
        
        footer {{
            text-align: center;
            color: var(--text-secondary);
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 代码统计报告: {dir_stats.name}</h1>
        <p class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="grid">
            <div class="card">
                <h3>📁 文件数</h3>
                <div class="stat-value">{dir_stats.file_count}</div>
                <div class="stat-label">个文件</div>
            </div>
            <div class="card">
                <h3>💻 代码行</h3>
                <div class="stat-value">{dir_stats.code_lines:,}</div>
                <div class="stat-label">行代码</div>
            </div>
            <div class="card">
                <h3>💬 注释行</h3>
                <div class="stat-value">{dir_stats.comment_lines:,}</div>
                <div class="stat-label">行注释</div>
            </div>
            <div class="card">
                <h3>📦 总大小</h3>
                <div class="stat-value">{format_size(dir_stats.total_size)}</div>
                <div class="stat-label">文件大小</div>
            </div>
        </div>
        
        <h2>📂 目录结构</h2>
        <p style="color: var(--text-secondary); margin-bottom: 10px;">📖 图例: <code>[代码行|注释行|空行]</code></p>
        <div class="tree-container">
            <div class="tree-content">{chr(10).join(generate_tree_text(dir_stats))}</div>
        </div>
        
        <h2>📊 语言统计</h2>
        <table>
            <thead>
                <tr>
                    <th>语言</th>
                    <th>文件数</th>
                    <th>代码行</th>
                    <th>注释行</th>
                    <th>空行</th>
                    <th>大小</th>
                </tr>
            </thead>
            <tbody>
                {lang_rows}
                <tr style="font-weight: bold; background: var(--bg-tertiary);">
                    <td>总计</td>
                    <td>{dir_stats.file_count}</td>
                    <td>{dir_stats.code_lines:,}</td>
                    <td>{dir_stats.comment_lines:,}</td>
                    <td>{dir_stats.blank_lines:,}</td>
                    <td>{format_size(dir_stats.total_size)}</td>
                </tr>
            </tbody>
        </table>
        
        <h2>💰 开发成本估算 (COCOMO)</h2>
        <div class="card">
            <p style="margin-bottom: 15px;">
                代码规模: <strong>{cocomo['kloc']:.2f} KLOC</strong> ({int(cocomo['kloc']*1000):,} 行代码) | 
                项目类型: <strong>{cocomo['project_type_desc']}</strong>
            </p>
            <div class="cocomo-grid">
                <div class="cocomo-item">
                    <div class="cocomo-value">📅 {cocomo['duration_months']:.1f}</div>
                    <div class="stat-label">预估工期(月)</div>
                </div>
                <div class="cocomo-item">
                    <div class="cocomo-value">👥 {cocomo['team_size']:.1f}</div>
                    <div class="stat-label">建议团队(人)</div>
                </div>
                <div class="cocomo-item">
                    <div class="cocomo-value">⏱️ {cocomo['person_months']:.1f}</div>
                    <div class="stat-label">总人月数</div>
                </div>
                <div class="cocomo-item">
                    <div class="cocomo-value cost">💵 ${cocomo['cost_usd']:,}</div>
                    <div class="stat-label">成本 (USD)</div>
                </div>
                <div class="cocomo-item">
                    <div class="cocomo-value cost">💴 ¥{cocomo['cost_cny']:,}</div>
                    <div class="stat-label">成本 (CNY)</div>
                </div>
            </div>
        </div>
        
        <h2>🏥 代码健康度</h2>
        <table>
            <thead>
                <tr>
                    <th>指标</th>
                    <th>数值</th>
                </tr>
            </thead>
            <tbody>
                {health_rows}
            </tbody>
        </table>
        
        <h2>📈 Top 10 文件 (按代码行数)</h2>
        <table>
            <thead>
                <tr>
                    <th>排名</th>
                    <th>文件名</th>
                    <th>语言</th>
                    <th>代码行</th>
                    <th>注释率</th>
                </tr>
            </thead>
            <tbody>
                {top_rows}
            </tbody>
        </table>
        
        <footer>
            <p>Generated by <strong>CodeMetrics v{__version__}</strong> | 
            <a href="https://github.com/codemetrics" style="color: var(--accent-blue);">GitHub</a></p>
        </footer>
    </div>
</body>
</html>"""
    
    return html


def get_script_dir() -> str:
    """获取脚本真实所在目录（解析符号链接）"""
    script_path = os.path.abspath(__file__)
    # 解析符号链接，获取真实路径
    real_path = os.path.realpath(script_path)
    return os.path.dirname(real_path)


def load_config() -> Dict:
    """加载全局配置文件"""
    config = DEFAULT_CONFIG.copy()
    
    script_dir = get_script_dir()
    config_path = os.path.join(script_dir, GLOBAL_CONFIG_FILENAME)
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                for key, value in user_config.items():
                    if isinstance(value, dict) and key in config:
                        config[key].update(value)
                    else:
                        config[key] = value
        except Exception as e:
            print(f"⚠️ 配置加载失败: {e}")
    
    return config


def save_default_config(target_path: str):
    """保存项目级配置文件"""
    config_path = os.path.join(target_path, CONFIG_FILENAME)
    
    # 项目级配置只保存常用的覆盖项
    project_config = {
        "name": f"CodeMetrics 项目配置 - {os.path.basename(target_path)}",
        "version": "1.0",
        "_comment": "此配置会覆盖全局配置 (codemetrics/config.json)",
        
        "exclude": {
            "_comment": "添加此项目特有的排除规则",
            "patterns": [],
            "dirs": []
        },
        
        "cocomo": {
            "_comment": "organic(简单) / semi-detached(中等) / embedded(复杂)",
            "project_type": "semi-detached"
        }
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(project_config, f, indent=2, ensure_ascii=False)
    
    script_dir = get_script_dir()
    global_config_path = os.path.join(script_dir, GLOBAL_CONFIG_FILENAME)
    
    print(f"✅ 已创建项目配置: {config_path}")
    print(f"   全局配置位置: {global_config_path}")
    print("   项目配置会覆盖全局配置中的相同项")


def save_outputs(dir_stats: DirStats, lang_stats: Dict, 
                 cocomo: Dict, health: Dict, all_files: List[FileStats], project_name: str):
    """保存报告到脚本同级目录下的 项目名_output 目录"""
    
    script_dir = get_script_dir()
    # 使用项目名命名输出目录
    safe_name = project_name.replace('/', '_').replace('\\', '_')
    output_dir = os.path.join(script_dir, f"{safe_name}_output")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    saved_files = []
    
    # JSON
    json_path = os.path.join(output_dir, f"report_{timestamp}.json")
    json_content = generate_json(dir_stats, lang_stats, cocomo, health)
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json_content)
    saved_files.append(('JSON', json_path))
    
    # Markdown
    md_path = os.path.join(output_dir, f"report_{timestamp}.md")
    md_content = generate_markdown(dir_stats, lang_stats, cocomo, health, all_files)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    saved_files.append(('Markdown', md_path))
    
    # HTML
    html_path = os.path.join(output_dir, f"report_{timestamp}.html")
    html_content = generate_html(dir_stats, lang_stats, cocomo, health, all_files)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    saved_files.append(('HTML', html_path))
    
    # 创建 latest 文件
    import shutil
    for fmt, path in saved_files:
        ext = os.path.splitext(path)[1]
        latest_path = os.path.join(output_dir, f"latest{ext}")
        try:
            if os.path.exists(latest_path):
                os.remove(latest_path)
            shutil.copy2(path, latest_path)
        except:
            pass
    
    return output_dir, saved_files


# ============================================================================
# 主程序
# ============================================================================
def print_help_and_examples():
    """打印帮助信息和完整示例"""
    script_dir = get_script_dir()
    help_text = f"""
{color('╔' + '═' * 70 + '╗', Colors.CYAN)}
{color('║', Colors.CYAN)}  {color('📊 CodeMetrics v' + __version__ + ' - 代码度量分析工具', Colors.BOLD)}                          {color('║', Colors.CYAN)}
{color('╚' + '═' * 70 + '╝', Colors.CYAN)}

{color('📖 使用方法:', Colors.BOLD)}
  codemetrics <目录路径> -p <项目类型>

{color('⚠️  必需参数:', Colors.YELLOW)}
  <目录路径>              要分析的代码目录
  -p, --project-type     项目类型 (影响成本估算)
                         • organic       - 简单项目 (小团队、熟悉技术栈)
                         • semi-detached - 中等项目 (中型团队、混合经验)
                         • embedded      - 复杂项目 (嵌入式、驱动、实时系统)

{color('📋 可选参数:', Colors.BOLD)}
  -n, --top N            Top N 文件数量 (默认: 10)
  -e, --exclude PATTERN  额外排除的文件模式 (逗号分隔)
  --no-save              不保存报告（默认会自动保存）
  --no-color             禁用颜色输出
  -v, --version          显示版本号
  -h, --help             显示帮助信息

{color('📝 使用示例:', Colors.BOLD)}

  {color('# 分析驱动代码 (嵌入式项目)', Colors.GREEN)}
  codemetrics /path/to/driver -p embedded

  {color('# 分析 Web 项目 (中等复杂度)', Colors.GREEN)}
  codemetrics /path/to/webapp -p semi-detached

  {color('# 分析小工具脚本 (简单项目)', Colors.GREEN)}
  codemetrics /path/to/scripts -p organic

  {color('# 额外排除某些目录', Colors.GREEN)}
  codemetrics /path/to/project -p embedded -e "test/*,vendor/*"

  {color('# 显示 Top 20 文件', Colors.GREEN)}
  codemetrics /path/to/project -p embedded -n 20

{color('⚙️  配置文件:', Colors.BOLD)}
  {script_dir}/config.json
  (编辑此文件可自定义忽略规则)

{color('📁 输出目录:', Colors.BOLD)}
  {script_dir}/output/
  (使用 -s 参数后，报告保存在此目录)

{color('📊 项目类型说明 (COCOMO 模型):', Colors.BOLD)}
  ┌─────────────────┬────────────────────────────────────────┐
  │ organic         │ 简单项目: 小团队、熟悉的技术栈         │
  │ semi-detached   │ 中等项目: 中型团队、混合经验           │
  │ embedded        │ 复杂项目: 嵌入式/驱动/实时系统/硬件相关│
  └─────────────────┴────────────────────────────────────────┘
"""
    print(help_text)


def main():
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        print_help_and_examples()
        sys.exit(0)
    
    parser = argparse.ArgumentParser(
        description='CodeMetrics - 代码度量分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,  # 我们自己处理帮助
    )
    
    parser.add_argument('path', nargs='?', default=None, help='要分析的目录路径')
    parser.add_argument('--project-type', '-p', choices=['organic', 'semi-detached', 'embedded'], 
                        default=None, help='COCOMO 项目类型 (必需)')
    parser.add_argument('--no-save', action='store_true', help='不保存报告（默认会保存）')
    parser.add_argument('--top', '-n', type=int, default=10, help='Top N 文件数量 (默认: 10)')
    parser.add_argument('--exclude', '-e', type=str, default='', help='额外排除的模式 (逗号分隔)')
    parser.add_argument('--no-color', action='store_true', help='禁用颜色输出')
    parser.add_argument('--version', '-v', action='store_true', help='显示版本号')
    parser.add_argument('--help', '-h', action='store_true', help='显示帮助信息')
    
    args = parser.parse_args()
    
    # 处理颜色
    global USE_COLORS
    if args.no_color:
        USE_COLORS = False
    
    # 显示帮助
    if args.help:
        print_help_and_examples()
        sys.exit(0)
    
    # 显示版本
    if args.version:
        print(f"CodeMetrics v{__version__}")
        sys.exit(0)
    
    # 检查路径参数
    if args.path is None:
        print(color("❌ 错误: 请指定要分析的目录路径", Colors.RED))
        print()
        print("用法: codemetrics <目录路径> -p <项目类型>")
        print("示例: codemetrics /path/to/project -p embedded")
        print()
        print("运行 'codemetrics --help' 查看完整帮助")
        sys.exit(1)
    
    # 处理路径
    target_path = os.path.abspath(args.path)
    if not os.path.exists(target_path):
        print(f"❌ 错误: 路径不存在: {target_path}", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.isdir(target_path):
        print(f"❌ 错误: 不是目录: {target_path}", file=sys.stderr)
        sys.exit(1)
    
    # 检查项目类型参数
    if args.project_type is None:
        print(color("❌ 错误: 请指定项目类型 (-p 参数)", Colors.RED))
        print()
        print("项目类型选项:")
        print("  -p organic       简单项目 (小团队、熟悉技术栈)")
        print("  -p semi-detached 中等项目 (中型团队、混合经验)")
        print("  -p embedded      复杂项目 (嵌入式/驱动/实时系统)")
        print()
        print("示例: codemetrics /path/to/project -p embedded")
        sys.exit(1)
    
    # 加载全局配置文件
    config = load_config()
    
    # 获取排除规则
    ignore_patterns = config.get('exclude', {}).get('patterns', [])
    
    # 命令行额外排除规则
    if args.exclude:
        extra_patterns = [p.strip() for p in args.exclude.split(',') if p.strip()]
        ignore_patterns = ignore_patterns + extra_patterns
    
    # 项目类型 (必需参数，已在上面检查)
    project_type = args.project_type
    
    # 开始扫描
    start_time = time.time()
    
    print(color(f"\n🔍 正在扫描: {target_path}", Colors.BOLD))
    
    dir_stats = scan_directory(target_path, ignore_patterns)
    lang_stats = collect_by_language(dir_stats)
    all_files = collect_all_files(dir_stats)
    cocomo = calculate_cocomo(dir_stats.code_lines, project_type)
    health = calculate_health(dir_stats, all_files)
    
    scan_time = time.time() - start_time
    
    # 默认保存报告（除非指定 --no-save）
    if not args.no_save:
        project_name = os.path.basename(target_path)
        output_dir, saved_files = save_outputs(
            dir_stats, lang_stats, cocomo, health, all_files, project_name
        )
    
    # 终端输出 - 显示完整报告
    print(color(f"✅ 扫描完成 ({scan_time:.2f}s)\n", Colors.GREEN))
    
    # 1. 目录树
    print(color("📂 目录结构", Colors.BOLD))
    print(color("📖 图例: [代码行|注释行|空行]", Colors.DIM))
    print(color("─" * 80, Colors.DIM))
    print_tree(dir_stats, show_details=True)
    
    # 2. 语言统计表
    print_language_table(lang_stats)
    
    # 3. COCOMO 成本估算
    print_cocomo(cocomo)
    
    # 4. 健康度指标
    print_health(health)
    
    # 5. Top N 文件
    print_top_files(all_files, args.top)
    
    # 显示保存位置
    if not args.no_save:
        print()
        print(color(f"Report saved to: {output_dir}", Colors.GREEN))
    
    print()


if __name__ == '__main__':
    main()

