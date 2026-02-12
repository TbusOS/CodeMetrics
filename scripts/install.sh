#!/bin/bash
#
# CodeMetrics 安装脚本
# 一键安装代码统计工具到用户环境
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 获取脚本所在目录的上级目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODESTATS_PY="${SCRIPT_DIR}/codemetrics.py"

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          📊 CodeMetrics 安装程序                               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 检查 codemetrics.py 是否存在
if [ ! -f "$CODESTATS_PY" ]; then
    echo -e "${RED}❌ 错误: 找不到 codemetrics.py${NC}"
    echo "   请确保在 codemetrics 目录下运行此脚本"
    exit 1
fi

# 检查 Python 版本
echo -e "${BLUE}🔍 检查 Python 环境...${NC}"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 6 ]; then
        echo -e "${GREEN}   ✅ Python $PYTHON_VERSION (符合要求 >= 3.6)${NC}"
    else
        echo -e "${RED}   ❌ Python $PYTHON_VERSION 版本过低，需要 >= 3.6${NC}"
        exit 1
    fi
else
    echo -e "${RED}   ❌ 未找到 Python3，请先安装 Python 3.6+${NC}"
    exit 1
fi

# 设置执行权限
echo -e "${BLUE}🔧 设置执行权限...${NC}"
chmod +x "$CODESTATS_PY"
echo -e "${GREEN}   ✅ 已设置 codemetrics.py 执行权限${NC}"

# 创建用户 bin 目录
LOCAL_BIN="$HOME/.local/bin"
if [ ! -d "$LOCAL_BIN" ]; then
    echo -e "${BLUE}📁 创建 ~/.local/bin 目录...${NC}"
    mkdir -p "$LOCAL_BIN"
    echo -e "${GREEN}   ✅ 目录已创建${NC}"
fi

# 创建符号链接
LINK_PATH="$LOCAL_BIN/codemetrics"
echo -e "${BLUE}🔗 创建符号链接...${NC}"

if [ -L "$LINK_PATH" ] || [ -f "$LINK_PATH" ]; then
    echo -e "${YELLOW}   ⚠️  发现已存在的 codemetrics，正在更新...${NC}"
    rm -f "$LINK_PATH"
fi

ln -s "$CODESTATS_PY" "$LINK_PATH"
echo -e "${GREEN}   ✅ 符号链接已创建: $LINK_PATH -> $CODESTATS_PY${NC}"

# 检查 PATH
echo -e "${BLUE}🔍 检查 PATH 配置...${NC}"

if echo "$PATH" | grep -q "$LOCAL_BIN"; then
    echo -e "${GREEN}   ✅ ~/.local/bin 已在 PATH 中${NC}"
else
    echo -e "${YELLOW}   ⚠️  ~/.local/bin 不在 PATH 中${NC}"
    echo ""
    echo -e "${CYAN}请将以下行添加到你的 shell 配置文件中:${NC}"
    echo ""
    
    # 检测 shell 类型
    SHELL_NAME=$(basename "$SHELL")
    case "$SHELL_NAME" in
        bash)
            RC_FILE="~/.bashrc"
            ;;
        zsh)
            RC_FILE="~/.zshrc"
            ;;
        *)
            RC_FILE="~/.profile"
            ;;
    esac
    
    echo -e "${GREEN}# 添加到 $RC_FILE${NC}"
    echo -e "${YELLOW}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
    echo ""
    echo -e "${CYAN}然后运行: ${YELLOW}source $RC_FILE${NC}"
    echo ""
    
    # 询问是否自动添加
    read -p "是否自动添加到 $RC_FILE? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        REAL_RC_FILE="${RC_FILE/#\~/$HOME}"
        echo '' >> "$REAL_RC_FILE"
        echo '# CodeMetrics - 添加 ~/.local/bin 到 PATH' >> "$REAL_RC_FILE"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$REAL_RC_FILE"
        echo -e "${GREEN}   ✅ 已添加到 $RC_FILE${NC}"
        echo -e "${YELLOW}   请运行: source $RC_FILE 或重新打开终端${NC}"
    fi
fi

# 验证安装
echo ""
echo -e "${BLUE}🧪 验证安装...${NC}"

if [ -x "$LINK_PATH" ]; then
    echo -e "${GREEN}   ✅ codemetrics 已成功安装${NC}"
else
    echo -e "${RED}   ❌ 安装验证失败${NC}"
    exit 1
fi

# 完成
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║               🎉 安装完成!                                   ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}使用方法:${NC}"
echo -e "  ${YELLOW}codemetrics /path/to/project -p embedded${NC}"
echo ""
echo -e "${CYAN}查看帮助:${NC}"
echo -e "  ${YELLOW}codemetrics${NC}"
echo ""
echo -e "${CYAN}文件位置:${NC}"
echo -e "  程序: ${YELLOW}$CODESTATS_PY${NC}"
echo -e "  链接: ${YELLOW}$LINK_PATH${NC}"
echo -e "  配置: ${YELLOW}$SCRIPT_DIR/config.json${NC}"
echo -e "  输出: ${YELLOW}$SCRIPT_DIR/output/${NC}"
echo ""

