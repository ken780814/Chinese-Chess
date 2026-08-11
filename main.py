#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 主程序入口
"""

import sys
import os
import argparse

# 检查是否是 PyInstaller 打包模式
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    # DEB 安装模式：源码位于 /usr/share/chinese-chess
    _INSTALL_PATH = '/usr/share/chinese-chess'
    if os.path.isdir(os.path.join(_INSTALL_PATH, 'gui')):
        base_path = _INSTALL_PATH
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

# 设置资源路径
ASSETS_PATH = os.path.join(base_path, 'assets')
if not os.path.exists(ASSETS_PATH):
    alt_paths = [
        os.path.join(base_path, 'share', 'chinese-chess', 'assets'),
        os.path.join(base_path, '..', 'share', 'chinese-chess', 'assets'),
        '/usr/share/chinese-chess/assets',
    ]
    for alt in alt_paths:
        if os.path.exists(alt):
            ASSETS_PATH = alt
            break

os.environ['ASSETS_PATH'] = ASSETS_PATH

# 添加模块路径
sys.path.insert(0, os.path.join(base_path, 'engine'))
sys.path.insert(0, os.path.join(base_path, 'gui'))
sys.path.insert(0, os.path.join(base_path, 'data'))

from PyQt5.QtWidgets import QApplication
from gui.board import GameWidget


def main():
    parser = argparse.ArgumentParser(description='中国象棋')
    parser.add_argument('--mode', choices=['game', 'endgame'], default='game')
    parser.add_argument('--no-sound', action='store_true')
    
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = GameWidget()
    window.setWindowTitle('中国象棋 - Chinese Chess')
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
