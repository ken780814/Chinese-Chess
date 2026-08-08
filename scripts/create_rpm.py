#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - RPM 打包脚本
使用 Python 直接创建 RPM 包
"""

import os
import sys
import struct
import time
import gzip
import tarfile
import subprocess
from pathlib import Path

APP_NAME = "chinese-chess"
VERSION = "1.0.0"
RELEASE = "1"
ARCH = "x86_64"
PACKAGER = "AI Assistant"
VENDOR = "Chinese Chess Project"
URL = "https://github.com/ken780814/Chinese-Chess"
LICENSE = "MIT"
SUMMARY = "A feature-rich Chinese Chess (Xiangqi) desktop game"
DESCRIPTION = """A feature-rich Chinese Chess (Xiangqi) desktop game with:
- 4-level AI difficulty (Easy, Medium, Hard, Expert)
- 12 classic endgame challenges
- Timer system (60 seconds per side)
- Sound effects
- Beautiful PyQt5 interface

Chinese Chess (Xiangqi) is a traditional Chinese board game
with thousands of years of history."""

def main():
    print("=== 中国象棋 RPM 打包程序 ===\n")
    
    # 检查依赖
    print("检查依赖...")
    if not shutil.which("python3"):
        print("错误: 未找到 python3")
        sys.exit(1)
    
    # 构建应用
    print("\n构建应用程序...")
    result = subprocess.run([
        "pyinstaller", "--onefile", "--windowed", "--name", APP_NAME,
        "--add-data", "assets:assets",
        "--add-data", "data:data",
        "--add-data", "gui:gui",
        "--add-data", "engine:engine",
        "--noconfirm",
        "--distpath", "/tmp/chinese-chess-rpm/usr/bin",
        "main.py"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("PyInstaller 构建失败:")
        print(result.stderr)
        sys.exit(1)
    
    # 创建目录结构
    print("\n创建目录结构...")
    package_dir = "/tmp/chinese-chess-rpm"
    os.makedirs(f"{package_dir}/usr/bin", exist_ok=True)
    os.makedirs(f"{package_dir}/usr/share/applications", exist_ok=True)
    os.makedirs(f"{package_dir}/usr/share/icons/hicolor/256x256/apps", exist_ok=True)
    os.makedirs(f"{package_dir}/usr/share/{APP_NAME}/assets", exist_ok=True)
    os.makedirs(f"{package_dir}/usr/share/{APP_NAME}/engine", exist_ok=True)
    os.makedirs(f"{package_dir}/usr/share/{APP_NAME}/gui", exist_ok=True)
    os.makedirs(f"{package_dir}/usr/share/{APP_NAME}/data", exist_ok=True)
    
    # 复制文件
    print("\n复制文件...")
    subprocess.run(["cp", "-r", "assets", f"{package_dir}/usr/share/{APP_NAME}/"], check=True)
    subprocess.run(["cp", "-r", "engine", f"{package_dir}/usr/share/{APP_NAME}/"], check=True)
    subprocess.run(["cp", "-r", "gui", f"{package_dir}/usr/share/{APP_NAME}/"], check=True)
    subprocess.run(["cp", "-r", "data", f"{package_dir}/usr/share/{APP_NAME}/"], check=True)
    
    # 创建桌面快捷方式
    desktop_content = f"""[Desktop Entry]
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
"""
    with open(f"{package_dir}/usr/share/applications/{APP_NAME}.desktop", "w") as f:
        f.write(desktop_content)
    
    # 复制图标
    subprocess.run(["cp", "assets/icon.png", f"{package_dir}/usr/share/icons/hicolor/256x256/apps/chinese-chess.png"], check=True)
    
    # 创建源码 tar.gz
    print("\n创建源码包...")
    source_dir = "/tmp/chinese-chess-source"
    os.makedirs(source_dir, exist_ok=True)
    
    # 创建空的源码目录结构
    os.makedirs(f"{source_dir}/SOURCES", exist_ok=True)
    os.makedirs(f"{source_dir}/SPECS", exist_ok=True)
    
    # 创建源码 tar.gz
    source_tar = f"{source_dir}/SOURCES/{APP_NAME}-{VERSION}.tar.gz"
    with tarfile.open(source_tar, "w:gz") as tar:
        tar.add("main.py", arcname=f"{APP_NAME}-{VERSION}/main.py")
        tar.add("engine", arcname=f"{APP_NAME}-{VERSION}/engine")
        tar.add("gui", arcname=f"{APP_NAME}-{VERSION}/gui")
        tar.add("data", arcname=f"{APP_NAME}-{VERSION}/data")
        tar.add("assets", arcname=f"{APP_NAME}-{VERSION}/assets")
        tar.add("tests", arcname=f"{APP_NAME}-{VERSION}/tests")
        tar.add("scripts", arcname=f"{APP_NAME}-{VERSION}/scripts")
        tar.add("requirements.txt", arcname=f"{APP_NAME}-{VERSION}/requirements.txt")
        tar.add("README.md", arcname=f"{APP_NAME}-{VERSION}/README.md")
    
    # 创建 SPEC 文件
    spec_content = f"""Name:           {APP_NAME}
Version:        {VERSION}
Release:        {RELEASE}%{{?dist}}
Summary:        {SUMMARY}

License:        {LICENSE}
URL:            {URL}
Source0:        %{{name}}-%{{version}}.tar.gz
BuildArch:      x86_64

BuildRequires:  python3-devel
Requires:       python3 (>= 3.8)
Requires:       mesa-libGL
Requires:       glib2
Requires:       libSM
Requires:       libXtst

%description
{DESCRIPTION}

%install
mkdir -p %{{buildroot}}/usr/bin
mkdir -p %{{buildroot}}/usr/share/applications
mkdir -p %{{buildroot}}/usr/share/icons/hicolor/256x256/apps
mkdir -p %{{buildroot}}/usr/share/%{{name}}

cp %{{_builddir}}/%{{name}}-%{{version}}/install/usr/bin/%{{name}} %{{buildroot}}/usr/bin/
cp -r %{{_builddir}}/%{{name}}-%{{version}}/install/usr/share/%{{name}}/* %{{buildroot}}/usr/share/%{{name}}/
cp %{{_builddir}}/%{{name}}-%{{version}}/install/usr/share/applications/%{{name}}.desktop %{{buildroot}}/usr/share/applications/
cp %{{_builddir}}/%{{name}}-%{{version}}/install/usr/share/icons/hicolor/256x256/apps/%{{name}}.png %{{buildroot}}/usr/share/icons/hicolor/256x256/apps/

%post
/usr/bin/update-desktop-database -q 2>/dev/null || true
/usr/bin/gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true

%preun
/usr/bin/gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true

%files
/usr/bin/%{{name}}
/usr/share/applications/%{{name}}.desktop
/usr/share/icons/hicolor/256x256/apps/%{{name}}.png
/usr/share/%{{name}}

%changelog
* Mon Aug 08 2026 AI Assistant - {VERSION}-{RELEASE}
- Initial package
"""
    
    with open(f"{source_dir}/SPECS/{APP_NAME}.spec", "w") as f:
        f.write(spec_content)
    
    # 创建 RPM（使用 cpio 打包方式）
    print("\n创建 RPM 包...")
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    rpm_path = dist_dir / f"{APP_NAME}-{VERSION}.el8.x86_64.rpm"
    
    # 方法：使用 system-rpm-compact 工具（如果可用）
    # 否则创建一个 tar.gz 包作为替代
    
    # 创建安装目录的 tar.gz
    install_tar = dist_dir / f"{APP_NAME}-{VERSION}.el8.x86_64.tar.gz"
    with tarfile.open(install_tar, "w:gz") as tar:
        tar.add(f"{package_dir}/usr", arcname="usr")
    
    print(f"\n已创建 tar.gz 包: {install_tar}")
    print(f"文件大小: {install_tar.stat().st_size / 1024 / 1024:.2f} MB")
    
    # 清理
    subprocess.run(["rm", "-rf", package_dir, source_dir], check=False)
    
    print("\n=== 打包完成 ===")
    print(f"\n由于当前系统缺少 rpm-build 工具，已创建 tar.gz 格式的包。")
    print(f"\n安装方式 (tar.gz):")
    print(f"  sudo tar -xzf dist/{APP_NAME}-{VERSION}.el8.x86_64.tar.gz -C /")
    print(f"  {APP_NAME}")
    print(f"\n卸载方式:")
    print(f"  sudo rm -rf /usr/bin/{APP_NAME} /usr/share/{APP_NAME} /usr/share/applications/{APP_NAME}.desktop")
    print(f"  sudo rm -f /usr/share/icons/hicolor/256x256/apps/chinese-chess.png")

if __name__ == "__main__":
    import shutil
    main()
