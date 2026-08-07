#!/bin/bash
# 中国象棋 - macOS 打包脚本

echo "=== 中国象棋 macOS 打包程序 ==="

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

echo "开始打包 macOS 版本..."

# 使用 PyInstaller 打包
pyinstaller --onefile --windowed --name "chinese-chess" \
    --add-data "assets:assets" \
    --add-data "data:data" \
    --add-data "gui:gui" \
    --add-data "engine:engine" \
    --icon=assets/icon.icns \
    --noconfirm \
    main.py 2>&1

# 创建 macOS 应用包结构
APP_NAME="中国象棋.app"
APP_DIR="dist/$APP_NAME"
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"
mkdir -p "$APP_DIR/Contents/Frameworks"

# 复制可执行文件
cp dist/chinese-chess "$APP_DIR/Contents/MacOS/chinese-chess"
chmod +x "$APP_DIR/Contents/MacOS/chinese-chess"

# 复制资源文件
cp -r assets "$APP_DIR/Contents/Resources/"
cp -r engine "$APP_DIR/Contents/Resources/"
cp -r gui "$APP_DIR/Contents/Resources/"
cp -r data "$APP_DIR/Contents/Resources/"

# 创建 Info.plist
cat > "$APP_DIR/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>zh_CN</string>
    <key>CFBundleExecutable</key>
    <string>chinese-chess</string>
    <key>CFBundleIconFile</key>
    <string>icon</string>
    <key>CFBundleIdentifier</key>
    <string>com.chinese-chess.app</string>
    <key>CFBundleName</key>
    <string>中国象棋</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>xqi</string>
            </array>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
        </dict>
    </array>
</dict>
</plist>
EOF

# 创建 README
cat > "$APP_DIR/Contents/Resources/README.txt" << 'EOF'
中国象棋 - Chinese Chess v1.0 (macOS)
=====================================

运行方式：
  1. 双击「中国象棋.app」
  2. 或命令行: open 中国象棋.app
  3. 或命令行: ./dist/中国象棋.app/Contents/MacOS/chinese-chess

参数：
  --mode=endgame     残局挑战模式
  --no-sound         禁用音效

系统要求：
  - macOS 10.13 (High Sierra) 或更高
  - 256MB 内存以上
  - 100MB 磁盘空间

功能特性：
  - 四级 AI 难度
  - 12 个经典残局
  - 计时系统
  - 音效支持
  - 美观的棋盘界面

许可证：MIT
EOF

echo ""
echo "=== 打包完成 ==="
echo "发布目录: $APP_DIR"
ls -lh "$APP_DIR/Contents/MacOS/"
echo ""
echo "使用方法："
echo "  open $APP_DIR"
