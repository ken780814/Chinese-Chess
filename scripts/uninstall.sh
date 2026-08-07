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

# 删除命令行快捷方式
echo "删除命令行快捷方式..."
rm -f /usr/local/bin/chinese-chess

# 删除安装目录
echo "删除安装目录..."
rm -rf /usr/local/share/chinese-chess

# 删除系统图标
echo "删除系统图标..."
rm -f /usr/share/icons/hicolor/256x256/apps/chinese-chess.png

# 卸载 Python 依赖（可选，注释掉以保留依赖）
# echo "卸载 Python 依赖..."
# pip3 uninstall -y PyQt5

echo ""
echo "=== 卸载完成 ==="
echo ""
echo "注意: 个人数据文件（如残局记录）可能需要手动删除"
echo "数据文件位置: ~/.local/share/chinese-chess/"
echo ""
