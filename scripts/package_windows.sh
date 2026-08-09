#!/bin/bash
# 中国象棋 - Windows 打包脚本 (V2.0)

echo "=== 中国象棋 Windows 打包程序 (V2.0) ==="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install pyinstaller PyQt5 pygame -q

# 清理旧构建
rm -rf build dist

echo "开始打包 Windows 版本..."

# 使用 PyInstaller 打包
pyinstaller --onefile --windowed --name "chinese-chess" \
    --add-data "assets:assets" \
    --add-data "data:data" \
    --add-data "gui:gui" \
    --add-data "engine:engine" \
    --hidden-import=engine.rules \
    --hidden-import=engine.ai \
    --hidden-import=engine.sound \
    --hidden-import=gui.board \
    --hidden-import=gui.endgame \
    --hidden-import=data.endgames \
    --icon=assets/icon.png \
    --noconfirm \
    main.py 2>&1

# 创建发布目录
RELEASE_DIR="release/Chinese-Chess-v2.0-windows-x64"
mkdir -p "$RELEASE_DIR"

# 复制文件
if [ -f "dist/chinese-chess.exe" ]; then
    cp dist/chinese-chess.exe "$RELEASE_DIR/"
    echo "可执行文件已复制"
fi

# 复制资源文件
cp -r assets "$RELEASE_DIR/"
cp -r engine "$RELEASE_DIR/"
cp -r gui "$RELEASE_DIR/"
cp -r data "$RELEASE_DIR/"
cp main.py "$RELEASE_DIR/"
cp requirements.txt "$RELEASE_DIR/"
cp README.md "$RELEASE_DIR/"
cp scripts/chinese-chess.bat "$RELEASE_DIR/"

# 创建 README
cat > "$RELEASE_DIR/README.txt" << 'EOF'
中国象棋 - Chinese Chess v2.0 (Windows)
========================================

运行方式：
  1. 双击 chinese-chess.exe
  2. 或双击 chinese-chess.bat
  3. 命令行: chinese-chess.exe --mode=endgame

参数：
  --mode=endgame     残局挑战模式
  --no-sound         禁用音效

系统要求：
  - Windows 10/11 (64位)
  - DirectX 9.0c 或更高
  - 256MB 内存以上

功能特性：
  - 四级 AI 难度
  - 12 个经典残局
  - 计时系统
  - 音效支持
  - 图片棋子，代码棋盘
  - 窗口缩放自适应

许可证：MIT
EOF

echo ""
echo "=== 打包完成 ==="
echo "发布目录: $RELEASE_DIR"
ls -lh "$RELEASE_DIR/"
