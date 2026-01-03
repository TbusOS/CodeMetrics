# 📚 CodeMetrics 使用示例

这个目录包含 CodeMetrics 的各种使用示例和输出样本。

## 🎯 基础示例

### 示例 1: 分析 C 驱动项目

```bash
# 分析嵌入式驱动代码
codemetrics /path/to/driver -p embedded

# 输出包含：
# - 目录树结构
# - 代码统计表
# - COCOMO 成本估算
# - 代码健康度分析
# - Top 10 最大文件
```

**适用场景**: 
- Linux 内核驱动
- 嵌入式固件
- 实时系统

---

### 示例 2: 分析 Web 项目

```bash
# 分析前端/后端项目
codemetrics /path/to/webapp -p semi-detached -n 20

# -p semi-detached: 中等复杂度项目
# -n 20: 显示 Top 20 文件
```

**适用场景**:
- React/Vue 前端项目
- Node.js/Django/Flask 后端
- 全栈 Web 应用

---

### 示例 3: 分析脚本工具

```bash
# 分析简单脚本集合
codemetrics /path/to/scripts -p organic

# -p organic: 简单项目类型
```

**适用场景**:
- Shell 脚本
- Python 自动化工具
- DevOps 脚本

---

## 🎨 高级用法

### 排除特定目录

```bash
# 排除测试和文档目录
codemetrics /path/to/project -p embedded -e "test/*,docs/*,vendor/*"
```

### 仅保存报告（不在终端显示）

```bash
# 使用 --no-save 选项
codemetrics /path/to/project -p embedded --no-save > /dev/null
```

### 纯文本输出（无颜色）

```bash
# 适合保存到文件或 CI/CD 环境
codemetrics /path/to/project -p embedded --no-color > report.txt
```

---

## 📊 输出格式示例

CodeMetrics 自动生成多种格式的报告：

### 1. 终端输出（默认）
- 彩色树形结构
- 格式化的统计表格
- 实时进度显示

### 2. JSON 格式
```bash
# 位置：codemetrics_output/report_YYYYMMDD_HHMMSS.json
```
适合：
- 程序解析
- CI/CD 集成
- 数据分析

### 3. Markdown 格式
```bash
# 位置：codemetrics_output/report_YYYYMMDD_HHMMSS.md
```
适合：
- 文档生成
- GitHub/GitLab 展示
- 项目汇报

### 4. HTML 格式
```bash
# 位置：codemetrics_output/report_YYYYMMDD_HHMMSS.html
```
适合：
- 浏览器查看
- 团队分享
- 演示展示

---

## 🔄 工作流示例

### CI/CD 集成

```yaml
# .github/workflows/code-metrics.yml
name: Code Metrics

on: [push]

jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install CodeMetrics
        run: |
          git clone https://github.com/YOUR_USERNAME/CodeMetrics.git
          cd CodeMetrics && ./scripts/install.sh
      
      - name: Run Analysis
        run: codemetrics . -p semi-detached
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: code-metrics-report
          path: codemetrics_output/
```

### Git Hook 示例

```bash
#!/bin/bash
# .git/hooks/pre-commit
# 在提交前自动分析代码

codemetrics . -p embedded --no-color > /tmp/codemetrics.txt
echo "📊 代码度量分析完成"
```

---

## 📈 实际项目示例

### Linux 驱动项目
```
项目规模: 15,000 行 C 代码
预估工期: 8.5 个月
建议团队: 2.3 人
成本估算: $97,500 USD
```

### React Web 应用
```
项目规模: 25,000 行 JS/TS 代码
预估工期: 11.2 个月
建议团队: 2.8 人
成本估算: $168,000 USD
```

### Python 工具集
```
项目规模: 5,000 行 Python 代码
预估工期: 4.2 个月
建议团队: 1.5 人
成本估算: $31,500 USD
```

---

## 🎓 教程

### 新手入门
1. 安装 CodeMetrics
2. 分析你的第一个项目
3. 理解输出结果
4. 根据健康度指标改进代码

### 进阶技巧
1. 自定义配置文件
2. 集成到开发工作流
3. 批量分析多个项目
4. 生成定期报告

---

## 💡 最佳实践

1. **定期分析**: 每周或每次发布前运行分析
2. **追踪趋势**: 保存历史报告，观察代码质量变化
3. **团队分享**: 将 HTML 报告分享给团队成员
4. **设定目标**: 根据健康度指标设定改进目标
5. **CI 集成**: 在 CI/CD 流程中自动运行

---

## 🤝 贡献示例

如果你有好的使用场景或示例，欢迎：
1. 添加到这个目录
2. 提交 Pull Request
3. 分享给社区

感谢你的贡献！🌟

