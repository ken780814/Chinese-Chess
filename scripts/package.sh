#!/bin/bash
# 中国象棋打包发布脚本

echo "=== 中国象棋打包发布程序 ==="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 检查 pyinstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "正在安装 PyInstaller..."
    pip3 install pyinstaller -q
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements.txt -q

# 创建输出目录
mkdir -p dist
mkdir -p release

# 清理旧构建
rm -rf build
rm -f chinese-chess.spec

echo "开始打包..."

# 使用 spec 文件打包
pyinstaller chinese-chess.spec --noconfirm

# 复制图标到可执行文件目录
if [ -f "dist/chinese-chess/chinese-chess" ]; then
    cp assets/icon.png dist/chinese-chess/
    echo "图标已复制到可执行文件目录"
fi

# 创建发布目录
RELEASE_DIR="release/Chinese-Chess-$(date +%Y%m%d)"
mkdir -p "$RELEASE_DIR"

# 复制可执行文件
cp -r dist/chinese-chess "$RELEASE_DIR/"

# 创建 README
cat > "$RELEASE_DIR/README.txt" << 'EOF'
中国象棋 - Chinese Chess
========================

运行方式：
  ./chinese-chess          # 开始游戏
  ./chinese-chess --mode=endgame  # 残局挑战
  ./chinese-chess --no-sound  # 禁用音效

系统要求：
  - Linux (x86_64)
  - Python 3.8+ (已内置)
  - 显卡支持 OpenGL

功能特性：
  - 四级 AI 难度
  - 12 个经典残局
  - 计时系统 (60秒/方)
  - 音效支持
  - 美观的棋盘界面

许可证：MIT
EOF

echo ""
echo "=== 打包完成 ==="
echo "发布目录: $RELEASE_DIR"
echo ""
ls -la "$RELEASE_DIR/"
