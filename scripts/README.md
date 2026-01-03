# 🔧 Scripts 目录

这个目录包含 CodeMetrics 的安装和管理脚本。

## 📜 脚本列表

### install.sh
**一键安装脚本**

自动完成以下操作：
- ✅ 检查 Python 版本 (需要 >= 3.6)
- ✅ 设置可执行权限
- ✅ 创建符号链接到 `~/.local/bin/codemetrics`
- ✅ 检查并配置 PATH 环境变量

**使用方法：**
```bash
cd CodeMetrics
./scripts/install.sh
```

安装后，你可以在任何目录直接运行：
```bash
codemetrics /path/to/project -p embedded
```

---

### uninstall.sh
**卸载脚本**

安全地卸载 CodeMetrics：
- 🗑️ 删除 `~/.local/bin/codemetrics` 符号链接
- 🗑️ 可选删除配置文件

**使用方法：**
```bash
cd CodeMetrics
./scripts/uninstall.sh
```

---

## 🛠️ 手动安装（可选）

如果你不想使用安装脚本，也可以手动安装：

```bash
# 1. 复制主程序
cp codemetrics.py ~/.local/bin/codemetrics
chmod +x ~/.local/bin/codemetrics

# 2. 确保 ~/.local/bin 在 PATH 中
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📝 注意事项

1. **权限问题**：脚本会自动检查并设置正确的权限
2. **PATH 配置**：如果安装后无法运行 `codemetrics` 命令，请检查 PATH
3. **Python 版本**：需要 Python 3.6 或更高版本
4. **无需 root**：所有操作都在用户目录下进行，无需 sudo

---

## 🤝 贡献脚本

如果你想添加新的脚本或改进现有脚本，欢迎提交 PR！

