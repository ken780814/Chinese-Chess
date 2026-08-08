#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 测试脚本（检查路径问题）
"""

import os
import sys
import tempfile
import shutil

def test_paths():
    """测试路径处理"""
    print("=== 路径测试 ===\n")
    
    # 测试 1: 检查 Frozen 状态
    print(f"1. Frozen 状态: {getattr(sys, 'frozen', False)}")
    
    # 测试 2: 检查 MEIPASS
    if getattr(sys, 'frozen', False):
        print(f"2. MEIPASS: {sys._MEIPASS}")
    else:
        print("2. 非 Frozen 模式")
    
    # 测试 3: 模拟安装后的路径
    print("\n3. 模拟安装后的路径:")
    simulated_base = "/tmp/chinese-chess-test/usr/bin"
    simulated_assets = "/tmp/chinese-chess-test/usr/share/chinese-chess/assets"
    
    os.makedirs(simulated_assets, exist_ok=True)
    
    # 复制资源
    src_assets = os.path.join(os.getcwd(), "assets")
    if os.path.exists(src_assets):
        shutil.copytree(src_assets, simulated_assets, dirs_exist_ok=True)
        print(f"   已复制资源到: {simulated_assets}")
    
    # 测试资源路径
    test_paths = [
        simulated_assets,
        os.path.join(simulated_base, "assets"),
        os.path.join(os.getcwd(), "assets"),
    ]
    
    for path in test_paths:
        exists = os.path.exists(path)
        icon_exists = os.path.exists(os.path.join(path, "icon.png")) if exists else False
        print(f"   {path}: {'存在' if exists else '不存在'}, icon.png: {'存在' if icon_exists else '不存在'}")
    
    # 测试 4: 检查当前目录的资源
    print("\n4. 当前目录资源:")
    current_assets = os.path.join(os.getcwd(), "assets")
    if os.path.exists(current_assets):
        print(f"   存在: {current_assets}")
        print(f"   内容: {os.listdir(current_assets)[:10]}")
    
    # 清理
    shutil.rmtree("/tmp/chinese-chess-test", ignore_errors=True)
    
    print("\n=== 测试完成 ===")


def test_pyinstaller_bundle():
    """测试 PyInstaller 打包内容"""
    print("\n=== PyInstaller 打包测试 ===\n")
    
    # 检查 dist 目录
    dist_path = os.path.join(os.getcwd(), "dist")
    if os.path.exists(dist_path):
        for f in os.listdir(dist_path):
            if f.endswith(".deb"):
                deb_path = os.path.join(dist_path, f)
                print(f"DEB 包: {deb_path}")
                
                # 检查 DEB 内容
                import subprocess
                result = subprocess.run(
                    ["dpkg-deb", "--contents", deb_path],
                    capture_output=True, text=True
                )
                
                # 查找 assets 相关文件
                lines = result.stdout.split("\n")
                asset_lines = [l for l in lines if "assets" in l.lower()]
                print(f"   包含 assets 相关文件: {len(asset_lines)} 个")
                
                # 检查 icon.png
                icon_lines = [l for l in lines if "icon.png" in l.lower()]
                print(f"   包含 icon.png: {len(icon_lines)} 个")
                for line in icon_lines[:5]:
                    print(f"      {line}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_paths()
    test_pyinstaller_bundle()
