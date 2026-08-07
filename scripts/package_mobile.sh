#!/bin/bash
# 中国象棋 - Android/iOS 打包脚本

echo "=== 中国象棋移动端打包程序 ==="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install kivy pygame cython buildozer -q

# 清理旧构建
rm -rf .buildozer dist

echo "开始打包..."

# 使用 Buildozer 打包
buildozer android debug 2>&1 || buildozer ios debug 2>&1

echo ""
echo "=== 打包完成 ==="
echo "输出目录: dist/"
