#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - Chinese Chess Game
主程序入口
"""

import sys
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui.board import BoardWidget


class ChineseChessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中国象棋 - Chinese Chess")
        self.setMinimumSize(800, 600)
        
        # 创建棋盘
        self.board = BoardWidget(self)
        self.setCentralWidget(self.board)
        
        # 初始化游戏状态
        self.game_state = "new"  # new, playing, game_over
        self.current_player = "red"  # red or black
        
    def start_game(self):
        """开始新游戏"""
        self.game_state = "playing"
        self.current_player = "red"
        self.board.reset()
        
    def quit_game(self):
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


def main():
    parser = argparse.ArgumentParser(description='中国象棋')
    parser.add_argument('--difficulty', type=str, choices=['easy', 'medium', 'hard', 'expert'],
                       default='medium', help='AI难度级别')
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    window = ChineseChessApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
