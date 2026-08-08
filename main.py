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
    # 打包模式：使用临时解压目录
    base_path = sys._MEIPASS
else:
    # 源码模式：使用脚本所在目录
    base_path = os.path.dirname(os.path.abspath(__file__))

# 设置资源路径（关键修复）
ASSETS_PATH = os.path.join(base_path, 'assets')
if not os.path.exists(ASSETS_PATH):
    # 尝试其他路径
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

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QComboBox,
                             QMessageBox)
from PyQt5.QtCore import Qt, QTimer

# 导入游戏模块 - 使用正确的类名
from gui.board import BoardWidget
from gui.endgame import EndgameWidget


class ChineseChessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_mode = 'game'  # 'game' or 'endgame'
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle('中国象棋 - Chinese Chess')
        self.setGeometry(100, 100, 700, 750)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 顶部控制栏
        control_layout = QHBoxLayout()
        
        # 模式选择
        mode_label = QLabel('游戏模式:')
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['人机对战', '残局挑战'])
        self.mode_combo.currentIndexChanged.connect(self.switch_mode)
        
        # 难度选择
        difficulty_label = QLabel('AI 难度:')
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(['初级', '中级', '高级', '终极高手'])
        
        # 新游戏按钮
        new_game_btn = QPushButton('新游戏')
        new_game_btn.clicked.connect(self.new_game)
        
        control_layout.addWidget(mode_label)
        control_layout.addWidget(self.mode_combo)
        control_layout.addWidget(difficulty_label)
        control_layout.addWidget(self.difficulty_combo)
        control_layout.addWidget(new_game_btn)
        control_layout.addStretch()
        
        main_layout.addLayout(control_layout)
        
        # 创建游戏界面容器
        self.game_container = QWidget()
        self.game_layout = QVBoxLayout(self.game_container)
        
        # 初始显示人机对战界面
        self.board_widget = BoardWidget()
        self.board_widget.move_requested.connect(self.on_move_requested)
        self.game_layout.addWidget(self.board_widget)
        
        main_layout.addWidget(self.game_container)
        
        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)
        
    def switch_mode(self, index):
        """切换游戏模式"""
        if index == 0:
            # 人机对战模式
            self.current_mode = 'game'
            if hasattr(self, 'endgame_widget'):
                self.game_layout.removeWidget(self.endgame_widget)
                self.endgame_widget.hide()
                self.endgame_widget.deleteLater()
                delattr(self, 'endgame_widget')
            
            # 创建新的棋盘
            self.board_widget = BoardWidget()
            self.board_widget.move_requested.connect(self.on_move_requested)
            self.game_layout.addWidget(self.board_widget)
            self.board_widget.show()
        else:
            # 残局挑战模式
            self.current_mode = 'endgame'
            if hasattr(self, 'board_widget'):
                self.game_layout.removeWidget(self.board_widget)
                self.board_widget.hide()
                self.board_widget.deleteLater()
                delattr(self, 'board_widget')
            
            # 创建残局界面
            self.endgame_widget = EndgameWidget()
            self.endgame_widget.move_requested.connect(self.on_move_requested)
            self.game_layout.addWidget(self.endgame_widget)
            self.endgame_widget.show()
            
    def on_move_requested(self, from_row, from_col, to_row, to_col):
        """处理走棋请求"""
        pass
        
    def new_game(self):
        """新游戏"""
        if self.current_mode == 'game':
            if hasattr(self, 'board_widget'):
                self.board_widget.restart_game()
        else:
            if hasattr(self, 'endgame_widget'):
                self.endgame_widget.start_endgame()


def main():
    parser = argparse.ArgumentParser(description='中国象棋')
    parser.add_argument('--mode', choices=['game', 'endgame'], default='game',
                       help='游戏模式')
    parser.add_argument('--no-sound', action='store_true',
                       help='禁用音效')
    
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    window = ChineseChessApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
