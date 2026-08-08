#!/bin/bash
# 中国象棋 - DEB 包依赖修复脚本
# 用于修复已安装包的依赖问题

set -e

echo "=== 中国象棋 DEB 包依赖修复 ==="
echo ""

# 检查是否安装了 chinese-chess
if ! dpkg -l chinese-chess &>/dev/null; then
    echo "chinese-chess 未安装，无需修复。"
    echo ""
    echo "请重新下载 DEB 包并安装："
    echo "  wget https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/chinese-chess_1.0.0_amd64.deb"
    echo "  sudo apt install ./chinese-chess_1.0.0_amd64.deb"
    exit 0
fi

echo "检测到已安装的 chinese-chess，正在修复..."
echo ""

# 卸载有问题的包
echo "1. 卸载当前包..."
sudo dpkg --remove --force-remove-reinstreq chinese-chess

# 安装依赖
echo ""
echo "2. 安装依赖..."
sudo apt-get install -y libgl1 libgl1-mesa-glx libglib2.0-0 libsm6 libxtst6 libx11-6

# 重新安装
echo ""
echo "3. 重新安装 chinese-chess..."
sudo apt install ./chinese-chess_1.0.0_amd64.deb

echo ""
echo "=== 修复完成 ==="
echo "运行游戏：chinese-chess"
