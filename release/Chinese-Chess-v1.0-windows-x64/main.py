#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 主程序入口
"""

import sys
import argparse
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QMessageBox,
                             QStackedWidget)
from PyQt5.QtCore import Qt
from gui.board import BoardWidget
from gui.endgame import EndgameWidget


class ChineseChessApp(QMainWindow):
    """中国象棋主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中国象棋 - Chinese Chess")
        self.setMinimumSize(900, 700)
        
        # 创建中央容器
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主菜单
        self.main_menu = self._create_main_menu()
        self.central_widget.addWidget(self.main_menu)
        
        # 创建游戏界面
        self.game_widget = BoardWidget()
        self.game_widget.move_requested.connect(self._on_game_move)
        self.central_widget.addWidget(self.game_widget)
        
        # 创建残局界面
        self.endgame_widget = EndgameWidget()
        self.endgame_widget.move_requested.connect(self._on_endgame_move)
        self.central_widget.addWidget(self.endgame_widget)
        
        # 当前屏幕
        self.current_screen = 'menu'
    
    def _create_main_menu(self):
        """创建主菜单"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title_label = QLabel("中国象棋")
        title_label.setFont(QFont("SimHei", 48, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Chinese Chess")
        subtitle_label.setFont(QFont("Arial", 20))
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        layout.addStretch()
        
        # 开始游戏按钮
        play_btn = QPushButton("开始游戏")
        play_btn.setFont(QFont("SimHei", 24))
        play_btn.setMinimumHeight(70)
        play_btn.clicked.connect(self._start_game)
        layout.addWidget(play_btn)
        
        # 残局挑战按钮
        endgame_btn = QPushButton("残局挑战")
        endgame_btn.setFont(QFont("SimHei", 24))
        endgame_btn.setMinimumHeight(70)
        endgame_btn.clicked.connect(self._start_endgame)
        layout.addWidget(endgame_btn)
        
        layout.addStretch()
        
        # 退出按钮
        quit_btn = QPushButton("退出游戏")
        quit_btn.setFont(QFont("SimHei", 20))
        quit_btn.setMinimumHeight(50)
        quit_btn.clicked.connect(self._quit_game)
        layout.addWidget(quit_btn)
        
        return widget
    
    def _start_game(self):
        """开始游戏"""
        self.current_screen = 'game'
        self.central_widget.setCurrentWidget(self.game_widget)
        self.game_widget.restart_game()
    
    def _start_endgame(self):
        """开始残局挑战"""
        self.current_screen = 'endgame'
        self.central_widget.setCurrentWidget(self.endgame_widget)
    
    def _on_game_move(self, from_row, from_col, to_row, to_col):
        """处理游戏移动"""
        game_over = self.game_widget.make_move(from_row, from_col, to_row, to_col)
        
        if not game_over:
            self._make_ai_move()
    
    def _on_endgame_move(self, from_row, from_col, to_row, to_col):
        """处理残局移动"""
        self.endgame_widget.make_move(from_row, from_col, to_row, to_col)
    
    def _make_ai_move(self):
        """让 AI 走棋"""
        import time
        start_time = time.time()
        
        move = self.game_widget.ai.get_best_move(self.game_widget.board, self.game_widget.ai_color)
        
        elapsed = time.time() - start_time
        print(f"AI 思考时间: {elapsed:.2f}s")
        
        if move:
            from_row, from_col, to_row, to_col = move
            self.game_widget.make_move(from_row, from_col, to_row, to_col)
    
    def _quit_game(self):
        """退出游戏"""
        reply = QMessageBox.question(
            self, 
            '确认退出', 
            '确定要退出中国象棋吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()
    
    def go_back_to_menu(self):
        """返回主菜单"""
        self.current_screen = 'menu'
        self.central_widget.setCurrentWidget(self.main_menu)


def main():
    parser = argparse.ArgumentParser(description='中国象棋')
    parser.add_argument('--mode', type=str, choices=['game', 'endgame'],
                       default='game', help='游戏模式')
    parser.add_argument('--no-sound', action='store_true', help='禁用音效')
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    window = ChineseChessApp()
    
    if args.no_sound:
        print("音效已禁用")
    
    if args.mode == 'game':
        window._start_game()
    elif args.mode == 'endgame':
        window._start_endgame()
    
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
