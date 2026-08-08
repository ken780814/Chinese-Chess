#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - RPM 打包脚本
使用 rpm 库直接创建 RPM 包
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

def check_dependency(name, cmd):
    """检查依赖"""
    try:
        result = subprocess.run([cmd], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def create_rpm(package_dir, output_path):
    """创建 RPM 包"""
    import rpm
    
    ts = rpm.TransactionSet()
    
    # 创建 RPM 头信息
    h = rpm.newHeader()
    h[rpm.RPMTAG_NAME] = APP_NAME
    h[rpm.RPMTAG_VERSION] = VERSION
    h[rpm.RPMTAG_RELEASE] = f"{RELEASE}.el8"
    h[rpm.RPMTAG_ARCH] = ARCH
    h[rpm.RPMTAG_OS] = "linux"
    h[rpm.RPMTAG_LICENSE] = LICENSE
    h[rpm.RPMTAG_SUMMARY] = SUMMARY
    h[rpm.RPMTAG_DESCRIPTION] = DESCRIPTION
    h[rpm.RPMTAG_PACKAGER] = PACKAGER
    h[rpm.RPMTAG_VENDOR] = VENDOR
    h[rpm.RPMTAG_URL] = URL
    h[rpm.RPMTAG_GROUP] = "Games"
    h[rpm.RPMTAG_BUILDARCH] = rpm.RP_MACHTOARCH[ARCH]
    h[rpm.RPMTAG_BUILDTIME] = int(time.time())
    h[rpm.RPMTAG_SIZE] = 0  # 将在后续步骤中更新
    h[rpm.RPMTAG_RPMVERSION] = "4.11.3"
    
    # 添加文件
    files = []
    
    # 可执行文件
    exe_path = os.path.join(package_dir, "usr", "bin", APP_NAME)
    if os.path.exists(exe_path):
        files.append({
            "path": exe_path,
            "dest": f"/{APP_NAME}",
            "flags": rpm.RPFileEXEC | rpm.RPFileNODIGEST
        })
    
    # 桌面快捷方式
    desktop_path = os.path.join(package_dir, "usr", "share", "applications", f"{APP_NAME}.desktop")
    if os.path.exists(desktop_path):
        files.append({
            "path": desktop_path,
            "dest": f"/usr/share/applications/{APP_NAME}.desktop",
            "flags": rpm.RPFileCONFIG
        })
    
    # 图标
    icon_path = os.path.join(package_dir, "usr", "share", "icons", "hicolor", "256x256", "apps", "chinese-chess.png")
    if os.path.exists(icon_path):
        files.append({
            "path": icon_path,
            "dest": "/usr/share/icons/hicolor/256x256/apps/chinese-chess.png",
            "flags": rpm.RPFileNODIGEST
        })
    
    # 资源文件
    for subdir in ["assets", "engine", "gui", "data"]:
        src_dir = os.path.join(package_dir, "usr", "share", APP_NAME, subdir)
        if os.path.exists(src_dir):
            for root, dirs, filenames in os.walk(src_dir):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    rel_path = os.path.relpath(filepath, src_dir)
                    dest = f"/usr/share/{APP_NAME}/{subdir}/{rel_path}"
                    files.append({
                        "path": filepath,
                        "dest": dest,
                        "flags": rpm.RPFileNODIGEST
                    })
    
    # 添加文件到 RPM
    for f in files:
        h.addFile(f["path"], f["dest"], f["flags"])
    
    # 写入 RPM 文件
    fh = open(output_path, "wb")
    rpm.simpleWriteHeader(h, fh)
    
    for f in files:
        with open(f["path"], "rb") as pf:
            data = pf.read()
            fh.write(data)
            h[rpm.RPMTAG_SIZE] += len(data)
    
    fh.close()
    
    # 更新大小
    rpm.simpleWriteHeader(h, None)
    
    print(f"RPM 包已创建: {output_path}")
    print(f"文件大小: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

def main():
    """主函数"""
    print("=== 中国象棋 RPM 打包程序 ===\n")
    
    # 检查依赖
    print("检查依赖...")
    if not check_dependency("python3", "python3 --version"):
        print("错误: 未找到 python3")
        sys.exit(1)
    
    # 检查 rpm 模块
    try:
        import rpm
    except ImportError:
        print("错误: 未找到 rpm 模块")
        print("请安装: pip3 install rpm-py-installer")
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
    
    # 创建 RPM
    print("\n创建 RPM 包...")
    output_path = "dist/chinese-chess-1.0.0.el8.x86_64.rpm"
    os.makedirs("dist", exist_ok=True)
    
    create_rpm(package_dir, output_path)
    
    # 清理
    subprocess.run(["rm", "-rf", package_dir], check=False)
    
    print("\n=== 打包完成 ===")
    print(f"RPM 文件: {output_path}")
    print(f"\n安装方式:")
    print(f"  sudo dnf install {output_path}")
    print(f"  sudo yum install {output_path}")
    print(f"\n卸载方式:")
    print(f"  sudo dnf remove {APP_NAME}")
    print(f"  sudo yum remove {APP_NAME}")

if __name__ == "__main__":
    main()
