#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - Windows 安装脚本
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def get_install_dir():
    """获取安装目录"""
    install_dir = Path(os.environ.get('APPDATA', '~')) / 'Chinese-Chess'
    return install_dir.expanduser()

def install():
    """安装游戏"""
    print("=" * 50)
    print("中国象棋 - Windows 安装程序")
    print("=" * 50)
    
    # 检查 Python
    try:
        import pygame
    except ImportError:
        print("\n正在安装 pygame...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame', '-q'])
    
    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        print("\n正在安装 PyQt5...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyQt5', '-q'])
    
    # 创建安装目录
    install_dir = get_install_dir()
    install_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n安装目录: {install_dir}")
    
    # 复制文件
    script_dir = Path(__file__).parent
    source_files = ['main.py', 'gui', 'engine', 'data', 'assets', 'requirements.txt', 'README.md']
    
    for src in source_files:
        src_path = script_dir / src
        if src_path.exists():
            dst_path = install_dir / src
            if src_path.is_dir():
                if dst_path.exists():
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                print(f"  ✓ {src}/")
            else:
                shutil.copy2(src_path, dst_path)
                print(f"  ✓ {src}")
    
    # 创建桌面快捷方式
    create_shortcut(install_dir)
    
    print("\n" + "=" * 50)
    print("安装完成！")
    print("=" * 50)
    print(f"\n运行方式：")
    print(f"  1. 双击桌面快捷方式「中国象棋」")
    print(f"  2. 或运行: {install_dir}\\\\chinese-chess.bat")
    print(f"  3. 或运行: python {install_dir}\\\\main.py")
    print()

def create_shortcut(install_dir):
    """创建桌面快捷方式"""
    try:
        import winreg
        from pathlib import Path
        
        # 获取桌面路径
        desktop = Path.home() / 'Desktop'
        
        # 创建 .bat 文件
        bat_content = f'''@echo off
chcp 65001 >nul
cd /d "{install_dir}"
python main.py %*
'''
        bat_path = install_dir / 'chinese-chess.bat'
        bat_path.write_text(bat_content, encoding='utf-8')
        
        # 创建快捷方式 (.lnk) - 需要 pywin32
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(str(desktop / '中国象棋.lnk'))
            shortcut.TargetPath = str(bat_path)
            shortcut.WorkingDirectory = str(install_dir)
            shortcut.IconLocation = str(install_dir / 'assets' / 'icon.png')
            shortcut.Description = '中国象棋 - Chinese Chess'
            shortcut.save()
            print("  ✓ 桌面快捷方式已创建")
        except ImportError:
            print("  ℹ pywin32 未安装，快捷方式创建跳过")
            print("    运行: pip install pywin32")
        
    except Exception as e:
        print(f"  ⚠ 创建快捷方式失败: {e}")

def uninstall():
    """卸载游戏"""
    print("=" * 50)
    print("中国象棋 - 卸载程序")
    print("=" * 50)
    
    install_dir = get_install_dir()
    
    if not install_dir.exists():
        print(f"\n未找到安装目录: {install_dir}")
        return
    
    # 删除桌面快捷方式
    desktop = Path.home() / 'Desktop'
    shortcut = desktop / '中国象棋.lnk'
    if shortcut.exists():
        shortcut.unlink()
        print(f"  ✓ 已删除快捷方式")
    
    bat_path = install_dir / 'chinese-chess.bat'
    if bat_path.exists():
        bat_path.unlink()
    
    # 删除安装目录
    shutil.rmtree(install_dir)
    print(f"  ✓ 已删除安装目录: {install_dir}")
    
    print("\n" + "=" * 50)
    print("卸载完成！")
    print("=" * 50)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'uninstall':
        uninstall()
    else:
        install()
