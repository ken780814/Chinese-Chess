#!/bin/bash
# 中国象棋 - DEB 包验证和依赖修复脚本

set -e

echo "=== 中国象棋 DEB 包验证脚本 ==="

DEB_FILE="${1:-chinese-chess_1.0.0_amd64.deb}"

if [ ! -f "${DEB_FILE}" ]; then
    echo "错误: 找不到 DEB 文件 ${DEB_FILE}"
    echo "用法: $0 [deb文件]"
    exit 1
fi

echo ""
echo "正在检查 DEB 包: ${DEB_FILE}"
echo ""

# 检查 DEB 包信息
echo "=== DEB 包信息 ==="
dpkg-deb --info "${DEB_FILE}"

echo ""
echo "=== 依赖检查 ==="
DEPENDS=$(dpkg-deb --field "${DEB_FILE}" Depends)
echo "依赖: ${DEPENDS}"

echo ""
echo "=== 检查依赖是否已安装 ==="
for dep in $(echo "${DEPENDS}" | tr ',' '\n' | sed 's/^ *//' | grep -v '^$'); do
    # 提取包名（去掉版本要求）
    pkg_name=$(echo "${dep}" | sed 's/[ (>].*//')
    
    # 检查是否安装
    if dpkg -s "${pkg_name}" &>/dev/null; then
        echo "  ✓ ${pkg_name} 已安装"
    else
        echo "  ✗ ${pkg_name} 未安装"
    fi
done

echo ""
echo "=== 安装建议 ==="
echo "1. 先安装依赖："
echo "   sudo apt-get install -y libgl1 libglib2.0-0 libsm6 libxtst6 libx11-6"
echo ""
echo "2. 然后安装 DEB 包："
echo "   sudo dpkg -i ${DEB_FILE}"
echo "   sudo apt-get install -f"
echo ""
echo "或者一步到位："
echo "   sudo apt install ./ ${DEB_FILE}"
