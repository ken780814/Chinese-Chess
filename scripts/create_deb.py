#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 创建 DEB 包（修复导入问题）
"""

import os
import subprocess
import shutil

APP_NAME = "chinese-chess"
VERSION = "1.0.0"

def main():
    print("=== 创建 DEB 包（修复导入问题）===\n")
    
    # 清理
    shutil.rmtree("deb-build", ignore_errors=True)
    if os.path.exists("dist"):
        for f in os.listdir("dist"):
            if f.endswith(".deb"):
                os.remove(os.path.join("dist", f))
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists(f"{APP_NAME}.spec"):
        os.remove(f"{APP_NAME}.spec")
    
    # 创建目录
    pkg_dir = f"deb-build/{APP_NAME}_{VERSION}"
    os.makedirs(f"{pkg_dir}/usr/bin", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/applications", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/icons/hicolor/256x256/apps", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/{APP_NAME}/assets", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/{APP_NAME}/engine", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/{APP_NAME}/gui", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/{APP_NAME}/data", exist_ok=True)
    os.makedirs(f"{pkg_dir}/DEBIAN", exist_ok=True)
    
    # 构建应用程序 - 关键修复：使用正确的模块路径
    print("正在构建应用程序...")
    subprocess.run(["pyinstaller", "--onefile", "--windowed", "--name", APP_NAME,
                   "--add-data", f"assets:{APP_NAME}/assets",
                   "--add-data", f"engine:{APP_NAME}/engine",
                   "--add-data", f"gui:{APP_NAME}/gui",
                   "--add-data", f"data:{APP_NAME}/data",
                   "--hidden-import=engine.rules",
                   "--hidden-import=engine.ai",
                   "--hidden-import=engine.sound",
                   "--hidden-import=gui.board",
                   "--hidden-import=gui.endgame",
                   "--hidden-import=data.endgames",
                   "--noconfirm", "main.py"], check=True)
    
    # 复制文件
    print("正在复制文件...")
    shutil.copy2(f"dist/{APP_NAME}", f"{pkg_dir}/usr/bin/{APP_NAME}")
    os.chmod(f"{pkg_dir}/usr/bin/{APP_NAME}", 0o755)
    
    # 复制资源
    for src, dst in [("assets", "assets"), ("engine", "engine"), ("gui", "gui"), ("data", "data")]:
        if os.path.exists(src):
            shutil.copytree(src, f"{pkg_dir}/usr/share/{APP_NAME}/{dst}", dirs_exist_ok=True)
    
    # 创建桌面文件
    with open(f"{pkg_dir}/usr/share/applications/{APP_NAME}.desktop", "w") as f:
        f.write(f"""[Desktop Entry]
Name=Chinese Chess
Name[zh_CN]=中国象棋
Comment=A feature-rich Chinese Chess game
Comment[zh_CN]=一款功能丰富的中国象棋游戏
Exec=/usr/bin/{APP_NAME}
Icon=chinese-chess
Terminal=false
Type=Application
Categories=Game;BoardGame;
StartupNotify=false
""")
    
    # 复制图标
    if os.path.exists("assets/icon.png"):
        shutil.copy2("assets/icon.png", f"{pkg_dir}/usr/share/icons/hicolor/256x256/apps/chinese-chess.png")
    
    # 创建控制文件
    with open(f"{pkg_dir}/DEBIAN/control", "w") as f:
        f.write(f"""Package: {APP_NAME}
Version: {VERSION}
Section: games
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.8), libgl1, libglib2.0-0, libsm6, libxtst6, libx11-6
Installed-Size: 80000
Maintainer: AI Assistant
Author: AI Assistant for Ken
Description: A feature-rich Chinese Chess desktop game
 Homepage: https://github.com/ken780814/Chinese-Chess
""")
    
    # 创建 postinst
    with open(f"{pkg_dir}/DEBIAN/postinst", "w") as f:
        f.write("""#!/bin/sh
set -e
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q 2>/dev/null || true
fi
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
fi
exit 0
""")
    os.chmod(f"{pkg_dir}/DEBIAN/postinst", 0o755)
    
    # 创建 prerm
    with open(f"{pkg_dir}/DEBIAN/prerm", "w") as f:
        f.write("""#!/bin/sh
set -e
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
fi
exit 0
""")
    os.chmod(f"{pkg_dir}/DEBIAN/prerm", 0o755)
    
    # 打包
    os.makedirs("dist", exist_ok=True)
    subprocess.run(["dpkg-deb", "--build", "--root-owner-group", pkg_dir, 
                    f"dist/{APP_NAME}_{VERSION}_amd64.deb"], check=True)
    
    # 清理
    shutil.rmtree("deb-build")
    
    print(f"\n✅ DEB 包已创建: dist/{APP_NAME}_{VERSION}_amd64.deb")
    print("\n依赖检查:")
    result = subprocess.run(["dpkg-deb", "--field", f"dist/{APP_NAME}_{VERSION}_amd64.deb", "Depends"],
                          capture_output=True, text=True)
    print(f"  {result.stdout.strip()}")

if __name__ == "__main__":
    main()
