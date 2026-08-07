#!/bin/bash
# 中国象棋 - 移动端一键打包脚本
# 支持 Android APK 和 iOS IPA

set -e

echo "=== 中国象棋移动端打包程序 ==="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements-mobile.txt -q
pip3 install buildozer cython -q

# 清理旧构建
rm -rf .buildozer dist bin

# 检查参数
if [ "$1" == "android" ]; then
    echo "开始打包 Android APK..."
    buildozer android debug
    echo ""
    echo "=== Android 打包完成 ==="
    ls -lh bin/*.apk 2>/dev/null || echo "APK 文件在 bin/ 目录"
elif [ "$1" == "ios" ]; then
    echo "开始打包 iOS IPA..."
    buildozer ios debug
    echo ""
    echo "=== iOS 打包完成 ==="
    ls -lh dist/*.ipa 2>/dev/null || echo "IPA 文件在 dist/ 目录"
else
    echo "用法:"
    echo "  bash scripts/package_mobile.sh android  # 打包 Android APK"
    echo "  bash scripts/package_mobile.sh ios      # 打包 iOS IPA"
    echo ""
    echo "注意: iOS 打包需要 macOS 系统和 Xcode"
fi
