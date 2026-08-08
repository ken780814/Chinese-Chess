#!/bin/bash
# 中国象棋 - 依赖检查和修复脚本

set -e

echo "=== 中国象棋依赖检查和修复 ==="

# 检查是否是 root
if [ "$EUID" -ne 0 ]; then
    echo "请以 root 权限运行此脚本"
    exit 1
fi

echo ""
echo "检查并安装所需依赖..."
echo ""

# 更新包列表
apt-get update -qq

# 安装依赖
echo "正在安装依赖..."
apt-get install -y \
    python3 \
    python3-dev \
    libgl1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxtst6 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxrandr2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    2>&1 | tail -10

echo ""
echo "=== 依赖安装完成 ==="
echo ""
echo "现在可以安装中国象棋了："
echo "  sudo dpkg -i chinese-chess_1.0.0_amd64.deb"
echo "  sudo apt-get install -f"
