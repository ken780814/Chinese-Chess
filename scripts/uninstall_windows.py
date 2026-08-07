#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - Windows 卸载脚本
"""

import os
import sys
import shutil
from pathlib import Path

def get_install_dir():
    """获取安装目录"""
    return Path.home() / 'Chinese-Chess'

def uninstall():
    """卸载游戏"""
    print("=" * 50)
    print("中国象棋 - Windows 卸载程序")
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
    uninstall()
