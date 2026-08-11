#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 创建 lightweight DEB 包
不打包 Qt 库，依赖系统库
"""

import os
import subprocess
import shutil

APP_NAME = "chinese-chess"
VERSION = "2.4.1"

def run_command(cmd, check=True):
    """运行命令"""
    print(f"  运行: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        lines = result.stdout.strip().split('\n')
        for line in lines[-3:]:
            print(f"    {line}")
    if result.stderr and check:
        lines = result.stderr.strip().split('\n')
        for line in lines[-3:]:
            print(f"    {line}")
    return result

def main():
    print("=== 创建 Lightweight DEB 包 ===\n")
    
    # 清理
    print("清理旧文件...")
    shutil.rmtree("deb-build", ignore_errors=True)
    os.makedirs("dist", exist_ok=True)
    
    # 删除旧的DEB包
    for f in os.listdir("dist"):
        if f.endswith(".deb"):
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
    
    # 复制 main.py 作为执行脚本
    print("复制主程序...")
    shutil.copy2("main.py", f"{pkg_dir}/usr/bin/{APP_NAME}")
    
    # 添加 shebang
    with open(f"{pkg_dir}/usr/bin/{APP_NAME}", 'r') as f:
        content = f.read()
    if not content.startswith('#!'):
        content = '#!/usr/bin/env python3\n' + content
        with open(f"{pkg_dir}/usr/bin/{APP_NAME}", 'w') as f:
            f.write(content)
    os.chmod(f"{pkg_dir}/usr/bin/{APP_NAME}", 0o755)
    
    # 复制资源
    print("复制资源文件...")
    for src, dst in [("assets", "assets"), ("engine", "engine"), ("gui", "gui"), ("data", "data")]:
        if os.path.exists(src):
            shutil.copytree(src, f"{pkg_dir}/usr/share/{APP_NAME}/{dst}", dirs_exist_ok=True)
    
    # 创建桌面文件
    print("创建桌面文件...")
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
    
    # 创建控制文件 - 关键：依赖 python3-pyqt5 而不是打包 Qt
    print("创建控制文件...")
    with open(f"{pkg_dir}/DEBIAN/control", "w") as f:
        f.write(f"""Package: {APP_NAME}
Version: {VERSION}
Section: games
Priority: optional
Architecture: all
Depends: python3 (>= 3.8), python3-pyqt5, libgl1, libglib2.0-0, libsm6, libxtst6, libx11-6, python3-pil, python3-pygame
Installed-Size: 5000
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
    run_command(["dpkg-deb", "--build", "--root-owner-group", pkg_dir, 
                 f"dist/{APP_NAME}_{VERSION}_all.deb"])
    
    # 清理
    shutil.rmtree("deb-build")
    
    # 显示结果
    deb_path = f"dist/{APP_NAME}_{VERSION}_all.deb"
    if os.path.exists(deb_path):
        size = os.path.getsize(deb_path) / (1024 * 1024)
        print(f"\n✅ DEB 包已创建: dist/{APP_NAME}_{VERSION}_all.deb")
        print(f"   大小: {size:.1f} MB")
        
        print("\n依赖检查:")
        result = run_command(["dpkg-deb", "--field", deb_path, "Depends"], check=False)
        print(f"  {result.stdout.strip()}")
        
        print("\n包内容:")
        result = run_command(["dpkg-deb", "--contents", deb_path], check=False)
        lines = result.stdout.split('\n')
        for line in lines[:30]:
            if line.strip():
                print(f"  {line}")

if __name__ == "__main__":
    main()
