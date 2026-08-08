#!/bin/bash
# 中国象棋 - DEB 打包脚本

set -e

echo "=== 中国象棋 DEB 打包程序 ==="

# 检查命令
if ! command -v dpkg-deb &> /dev/null; then
    echo "错误: 未找到 dpkg-deb，请安装 dpkg-dev"
    exit 1
fi

if ! command -v pyinstaller &> /dev/null; then
    echo "错误: 未找到 pyinstaller"
    exit 1
fi

APP_NAME="chinese-chess"
VERSION="1.0.0"
PACKAGE_DIR="deb-build/${APP_NAME}_${VERSION}"

# 清理旧构建
rm -rf "deb-build" "dist/${APP_NAME}_${VERSION}_amd64.deb"

# 创建目录结构
mkdir -p "${PACKAGE_DIR}/usr/bin"
mkdir -p "${PACKAGE_DIR}/usr/share/applications"
mkdir -p "${PACKAGE_DIR}/usr/share/icons/hicolor/256x256/apps"
mkdir -p "${PACKAGE_DIR}/usr/share/${APP_NAME}/assets"
mkdir -p "${PACKAGE_DIR}/usr/share/${APP_NAME}/engine"
mkdir -p "${PACKAGE_DIR}/usr/share/${APP_NAME}/gui"
mkdir -p "${PACKAGE_DIR}/usr/share/${APP_NAME}/data"

# 构建应用程序
echo "正在构建应用程序..."
pyinstaller --onefile --windowed --name "${APP_NAME}" \
    --add-data "assets:assets" \
    --add-data "data:data" \
    --add-data "gui:gui" \
    --add-data "engine:engine" \
    --noconfirm \
    main.py

# 复制文件
echo "正在复制文件..."
cp dist/${APP_NAME} "${PACKAGE_DIR}/usr/bin/${APP_NAME}"
chmod +x "${PACKAGE_DIR}/usr/bin/${APP_NAME}"

# 复制资源
cp -r assets/* "${PACKAGE_DIR}/usr/share/${APP_NAME}/assets/"
cp -r engine/* "${PACKAGE_DIR}/usr/share/${APP_NAME}/engine/"
cp -r gui/* "${PACKAGE_DIR}/usr/share/${APP_NAME}/gui/"
cp -r data/* "${PACKAGE_DIR}/usr/share/${APP_NAME}/data/"

# 创建桌面快捷方式
cat > "${PACKAGE_DIR}/usr/share/applications/${APP_NAME}.desktop" << 'EOF'
[Desktop Entry]
Name=Chinese Chess
Name[zh_CN]=中国象棋
Comment=A feature-rich Chinese Chess game
Comment[zh_CN]=一款功能丰富的中国象棋游戏
Exec=/usr/bin/chinese-chess
Icon=chinese-chess
Terminal=false
Type=Application
Categories=Game;BoardGame;
StartupNotify=false
EOF

# 复制图标
cp assets/icon.png "${PACKAGE_DIR}/usr/share/icons/hicolor/256x256/apps/chinese-chess.png"

# 创建控制文件
mkdir -p "${PACKAGE_DIR}/DEBIAN"
cat > "${PACKAGE_DIR}/DEBIAN/control" << 'EOF'
Package: chinese-chess
Version: 1.0.0
Section: games
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.8), libgl1-mesa-glx, libglib2.0-0, libsm6, libxtst6
Installed-Size: 80000
Maintainer: AI Assistant
Author: AI Assistant for Ken
Description: A feature-rich Chinese Chess desktop game
 Support 4-level AI difficulty, 12 classic endgames, timer system
 and beautiful PyQt5 interface.
 Chinese Chess (Xiangqi) is a traditional Chinese board game with
 thousands of years of history.
 Homepage: https://github.com/ken780814/Chinese-Chess
EOF

# 创建 postinst 脚本
cat > "${PACKAGE_DIR}/DEBIAN/postinst" << 'EOF'
#!/bin/bash
update-desktop-database -q /usr/share/applications 2>/dev/null || true
gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
exit 0
EOF
chmod 755 "${PACKAGE_DIR}/DEBIAN/postinst"

# 创建 prerm 脚本
cat > "${PACKAGE_DIR}/DEBIAN/prerm" << 'EOF'
#!/bin/bash
gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
exit 0
EOF
chmod 755 "${PACKAGE_DIR}/DEBIAN/prerm"

# 打包
echo "正在打包 DEB 文件..."
dpkg-deb --build --root-owner-group "${PACKAGE_DIR}" "dist/${APP_NAME}_${VERSION}_amd64.deb"

# 清理
rm -rf "${PACKAGE_DIR}"

echo ""
echo "=== 打包完成 ==="
ls -lh "dist/${APP_NAME}_${VERSION}_amd64.deb"
echo ""
echo "安装方式："
echo "  sudo dpkg -i dist/${APP_NAME}_${VERSION}_amd64.deb"
echo ""
echo "卸载方式："
echo "  sudo apt remove chinese-chess"
