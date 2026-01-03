# 🤝 贡献指南

感谢你有兴趣为 CodeMetrics 做出贡献！

## 📋 贡献方式

### 🐛 报告 Bug
发现 Bug？请：
1. 检查 [Issues](https://github.com/YOUR_USERNAME/CodeMetrics/issues) 是否已有相关报告
2. 如果没有，创建新 Issue，包含：
   - 问题描述
   - 复现步骤
   - 期望行为
   - 实际行为
   - 系统环境（OS、Python 版本）
   - 错误日志

### 💡 提出新功能
有好点子？欢迎：
1. 创建 Feature Request Issue
2. 描述功能用途和使用场景
3. 等待社区反馈
4. 实现并提交 PR

### 📖 改进文档
文档永远可以更好！你可以：
- 修正拼写错误
- 改进表达
- 添加示例
- 翻译成其他语言

### 🔧 提交代码
请遵循以下流程：

#### 1. Fork 项目
```bash
# 在 GitHub 上点击 Fork 按钮
```

#### 2. 克隆到本地
```bash
git clone https://github.com/YOUR_USERNAME/CodeMetrics.git
cd CodeMetrics
```

#### 3. 创建分支
```bash
# 功能分支
git checkout -b feature/amazing-feature

# Bug 修复分支
git checkout -b fix/bug-description
```

#### 4. 进行修改
- 保持代码风格一致
- 添加必要的注释
- 更新相关文档

#### 5. 测试
```bash
# 测试基本功能
python3 codemetrics.py /path/to/test/project -p embedded

# 测试不同参数
python3 codemetrics.py /path/to/project -p organic -n 20
python3 codemetrics.py /path/to/project -p semi-detached --no-color
```

#### 6. 提交更改
```bash
git add .
git commit -m "feat: 添加新功能描述"

# 或
git commit -m "fix: 修复 Bug 描述"
git commit -m "docs: 更新文档"
```

#### 7. 推送到 GitHub
```bash
git push origin feature/amazing-feature
```

#### 8. 创建 Pull Request
1. 访问你的 Fork 页面
2. 点击 "New Pull Request"
3. 填写 PR 描述
4. 等待审核

---

## 📝 代码规范

### Python 风格
- 遵循 PEP 8
- 使用 4 空格缩进
- 函数和类添加文档字符串
- 变量名使用小写下划线

### 示例
```python
def calculate_metrics(file_path: str, language: str) -> Dict:
    """
    计算文件的度量指标
    
    Args:
        file_path: 文件路径
        language: 编程语言
        
    Returns:
        包含度量数据的字典
    """
    # 实现代码
    pass
```

### Commit 消息格式
使用语义化提交消息：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链更新

**示例：**
```
feat(cocomo): 添加 COCOMO II 模型支持

- 实现新的计算公式
- 添加配置选项
- 更新文档

Closes #123
```

---

## 🧪 测试清单

提交 PR 前请确认：

- [ ] 代码通过基本功能测试
- [ ] 没有引入新的错误
- [ ] 文档已更新
- [ ] Commit 消息符合规范
- [ ] 代码风格一致
- [ ] 添加了必要的注释

---

## 🌍 国际化

欢迎提交其他语言的翻译：

### 支持的语言
- 🇨🇳 中文（已支持）
- 🇺🇸 英文（待完善）
- 🇯🇵 日文（欢迎贡献）
- 🇰🇷 韩文（欢迎贡献）
- 🇪🇸 西班牙文（欢迎贡献）

### 翻译文件位置
```
docs/
├── README_zh.md  (中文)
├── README_en.md  (英文)
├── README_ja.md  (日文)
└── ...
```

---

## 📞 联系方式

有问题？可以通过以下方式联系：

- 💬 GitHub Issues
- 📧 Email: your-email@example.com
- 🐦 Twitter: @your_handle

---

## 🎖️ 贡献者

感谢所有贡献者！你们的名字将出现在这里：

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- 此处将自动列出所有贡献者 -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

---

## 📄 许可证

贡献的代码将在 MIT 许可证下发布。

---

**感谢你让 CodeMetrics 变得更好！** 🙏✨

