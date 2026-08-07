#!/bin/bash
# 中国象棋卸载脚本

echo "=== 中国象棋卸载程序 ==="

# 检查是否为 root
if [ "$EUID" -ne 0 ]; then
    echo "请以 root 权限运行此脚本"
    exit 1
fi

# 删除桌面快捷方式
echo "删除桌面快捷方式..."
rm -f /usr/share/applications/chinese-chess.desktop

# 删除可执行文件
echo "删除可执行文件..."
rm -f /usr/local/bin/chinese-chess

# 删除资源文件
echo "删除资源文件..."
rm -rf /usr/local/share/chinese-chess
rm -f /usr/local/share/icons/chinese-chess.png

# 卸载 Python 依赖（可选）
# pip3 uninstall -y PyQt5

echo "卸载完成！"
