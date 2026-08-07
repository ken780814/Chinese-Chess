#!/bin/bash
# 中国象棋安装脚本

echo "=== 中国象棋安装程序 ==="

# 检查是否为 root
if [ "$EUID" -ne 0 ]; then
    echo "请以 root 权限运行此脚本"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements.txt

# 创建桌面快捷方式
echo "创建桌面快捷方式..."
cat > /usr/share/applications/chinese-chess.desktop << 'EOF'
[Desktop Entry]
Name=中国象棋
Name[zh_CN]=中国象棋
Exec=/usr/local/bin/chinese-chess
Icon=/usr/local/share/icons/chinese-chess.png
Type=Application
Categories=Game;BoardGame;
Comment=A Chinese Chess game with AI
Comment[zh_CN]=一款带 AI 的中国象棋游戏
EOF

# 复制可执行文件
echo "安装可执行文件..."
cp main.py /usr/local/bin/chinese-chess
chmod +x /usr/local/bin/chinese-chess

# 复制资源文件
echo "复制资源文件..."
mkdir -p /usr/local/share/chinese-chess/gui
mkdir -p /usr/local/share/chinese-chess/engine
mkdir -p /usr/local/share/chinese-chess/data
mkdir -p /usr/local/share/icons

cp -r gui/* /usr/local/share/chinese-chess/gui/
cp -r engine/* /usr/local/share/chinese-chess/engine/
cp -r data/* /usr/local/share/chinese-chess/data/

# 创建图标（简化版，使用文本图标）
cat > /usr/local/share/icons/chinese-chess.png << 'EOF'
# This is a placeholder for the icon
# Replace with actual icon file
EOF

echo "安装完成！"
echo "可以通过桌面快捷方式或命令行运行 'chinese-chess'"
