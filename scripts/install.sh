#!/bin/bash
# 中国象棋安装脚本

echo "=== 中国象棋安装程序 ==="

# 检查是否为 root
if [ "$EUID" -ne 0 ]; then
    echo "请以 root 权限运行此脚本"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到 pip3，请先安装 pip3"
    exit 1
fi

# 安装依赖
echo "正在安装 Python 依赖..."
pip3 install -r requirements.txt

# 创建安装目录
INSTALL_DIR="/usr/local/share/chinese-chess"
echo "创建安装目录: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# 复制文件
echo "复制程序文件..."
cp -r gui "$INSTALL_DIR/"
cp -r engine "$INSTALL_DIR/"
cp -r data "$INSTALL_DIR/"
cp -r assets "$INSTALL_DIR/"
cp main.py "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"

# 创建桌面快捷方式
echo "创建桌面快捷方式..."
cat > /usr/share/applications/chinese-chess.desktop << EOF
[Desktop Entry]
Name=中国象棋
Name[zh_CN]=中国象棋
Exec=python3 $INSTALL_DIR/main.py
Icon=$INSTALL_DIR/assets/icon.png
Type=Application
Categories=Game;BoardGame;
Comment=A Chinese Chess game with AI
Comment[zh_CN]=一款带 AI 的中国象棋游戏
Terminal=true
EOF

# 创建命令行别名
echo "创建命令行快捷方式..."
cat > /usr/local/bin/chinese-chess << EOF
#!/bin/bash
python3 $INSTALL_DIR/main.py "\$@"
EOF
chmod +x /usr/local/bin/chinese-chess

# 复制图标到系统图标目录
if [ -f "$INSTALL_DIR/assets/icon.png" ]; then
    cp "$INSTALL_DIR/assets/icon.png" /usr/share/icons/hicolor/256x256/apps/chinese-chess.png 2>/dev/null || \
    mkdir -p /usr/share/icons/hicolor/256x256/apps && \
    cp "$INSTALL_DIR/assets/icon.png" /usr/share/icons/hicolor/256x256/apps/chinese-chess.png
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "启动方式:"
echo "  1. 命令行: chinese-chess"
echo "  2. 桌面快捷方式: 在应用程序菜单中查找'中国象棋'"
echo "  3. 直接运行: python3 $INSTALL_DIR/main.py"
echo ""
echo "卸载方式:"
echo "  运行: ./scripts/uninstall.sh"
echo ""
