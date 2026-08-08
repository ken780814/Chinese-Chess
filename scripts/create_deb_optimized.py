#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 优化打包脚本
减小文件大小
"""

import os
import subprocess
import shutil

APP_NAME = "chinese-chess"
VERSION = "1.0.0"

def run_command(cmd, check=True):
    """运行命令"""
    print(f" 运行: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout[-500:])
    if result.stderr:
        print(result.stderr[-500:])
    return result

def main():
    print("=== 优化打包 DEB 包 ===\n")
    
    # 清理
    print("清理旧文件...")
    shutil.rmtree("deb-build", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    if os.path.exists(f"{APP_NAME}.spec"):
        os.remove(f"{APP_NAME}.spec")
    for f in os.listdir("dist"):
        if f.endswith(".deb") or f == APP_NAME:
            os.remove(os.path.join("dist", f))
    
    # 创建目录
    print("创建目录结构...")
    pkg_dir = f"deb-build/{APP_NAME}_{VERSION}"
    os.makedirs(f"{pkg_dir}/usr/bin", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/applications", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/icons/hicolor/256x256/apps", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/{APP_NAME}/assets", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/{APP_NAME}/engine", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/{APP_NAME}/gui", exist_ok=True)
    os.makedirs(f"{pkg_dir}/usr/share/{APP_NAME}/data", exist_ok=True)
    os.makedirs(f"{pkg_dir}/DEBIAN", exist_ok=True)
    
    # 构建应用程序 - 使用优化选项
    print("构建应用程序（优化版）...")
    run_command([
        "pyinstaller", "--onefile", "--windowed", "--name", APP_NAME,
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
        "--exclude-module=tkinter",
        "--exclude-module=unittest",
        "--exclude-module=pydoc",
        "--noconfirm", "--clean",
        "main.py"
    ])
    
    # 复制可执行文件
    print("复制文件...")
    exe_path = f"dist/{APP_NAME}"
    if not os.path.exists(exe_path):
        exe_path = "dist/main"
    
    if os.path.exists(exe_path):
        # 复制到包目录
        dest_path = f"{pkg_dir}/usr/bin/{APP_NAME}"
        shutil.copy2(exe_path, dest_path)
        os.chmod(dest_path, 0o755)
        
        # 尝试 strip 减小体积
        print("优化文件大小...")
        run_command(["strip", "--strip-all", dest_path], check=False)
        
        # 显示文件大小
        size = os.path.getsize(dest_path) / (1024 * 1024)
        print(f"  可执行文件大小: {size:.1f} MB")
    else:
        print("错误: 找不到可执行文件")
        return
    
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
Installed-Size: 20000
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
    print("打包 DEB...")
    os.makedirs("dist", exist_ok=True)
    run_command(["dpkg-deb", "--build", "--root-owner-group", pkg_dir, 
                 f"dist/{APP_NAME}_{VERSION}_amd64.deb"])
    
    # 清理
    shutil.rmtree("deb-build")
    shutil.rmtree("build", ignore_errors=True)
    if os.path.exists(f"{APP_NAME}.spec"):
        os.remove(f"{APP_NAME}.spec")
    
    # 显示结果
    deb_path = f"dist/{APP_NAME}_{VERSION}_amd64.deb"
    if os.path.exists(deb_path):
        size = os.path.getsize(deb_path) / (1024 * 1024)
        print(f"\n✅ DEB 包已创建: dist/{APP_NAME}_{VERSION}_amd64.deb")
        print(f"   大小: {size:.1f} MB")
        
        print("\n依赖检查:")
        result = subprocess.run(["dpkg-deb", "--field", deb_path, "Depends"],
                              capture_output=True, text=True)
        print(f"  {result.stdout.strip()}")
    else:
        print("\n错误: DEB 包创建失败")

if __name__ == "__main__":
    main()
