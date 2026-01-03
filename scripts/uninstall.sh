#!/bin/bash
#
# CodeStats 卸载脚本
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          📊 CodeStats 卸载程序                               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

LINK_PATH="$HOME/.local/bin/codemetrics"

if [ -L "$LINK_PATH" ] || [ -f "$LINK_PATH" ]; then
    echo -e "${YELLOW}🗑️  删除符号链接: $LINK_PATH${NC}"
    rm -f "$LINK_PATH"
    echo -e "${GREEN}   ✅ 已删除${NC}"
else
    echo -e "${YELLOW}   ⚠️  符号链接不存在，跳过${NC}"
fi

echo ""
echo -e "${GREEN}✅ 卸载完成${NC}"
echo ""
echo -e "${CYAN}注意: 源代码目录未删除，如需完全删除请手动执行:${NC}"
echo -e "  ${YELLOW}rm -rf $(dirname "${BASH_SOURCE[0]}")${NC}"
echo ""

