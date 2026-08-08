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
                             QGroupBox, QFrame, QSizePolicy, QStackedWidget,
                             QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon

# 导入游戏模块 - 使用正确的路径
from engine.rules import Rules
from engine.ai import AI
from gui.endgame import EndgameMode

class ChineseChessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rules = Rules()
        self.ai = AI(self.rules)
        self.board = self.rules.initial_board()
        self.current_turn = 'red'  # red 先走
        self.selected_piece = None
        self.game_mode = 'game'  # 'game' or 'endgame'
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_timer)
        self.red_time = 60
        self.black_time = 60
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle('中国象棋 - Chinese Chess')
        self.setGeometry(100, 100, 800, 700)
        
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
        
        # 计时器显示
        self.timer_label = QLabel('红方: 60秒 | 黑方: 60秒')
        control_layout.addWidget(self.timer_label)
        
        main_layout.addLayout(control_layout)
        
        # 棋盘区域
        self.board_widget = BoardWidget(self.rules, self.board)
        self.board_widget.piece_clicked.connect(self.on_piece_clicked)
        self.board_widget.cell_clicked.connect(self.on_cell_clicked)
        main_layout.addWidget(self.board_widget)
        
        # 状态栏
        self.status_label = QLabel('红方走棋')
        main_layout.addWidget(self.status_label)
        
        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)
        
        # 启动计时器
        self.timer.start(1000)
        
    def switch_mode(self, index):
        if index == 0:
            self.game_mode = 'game'
        else:
            self.game_mode = 'endgame'
            self.start_endgame()
        self.new_game()
        
    def start_endgame(self):
        """开始残局模式"""
        self.endgame_mode = EndgameMode()
        self.current_endgame = 0
        self.show_endgame(self.current_endgame)
        
    def show_endgame(self, index):
        """显示残局"""
        endgame = self.endgame_mode.get_endgame(index)
        if endgame:
            self.board = endgame['board']
            self.board_widget.update_board(self.board)
            self.status_label.setText("残局 %d: %s" % (index + 1, endgame['name']))
            
    def new_game(self):
        """新游戏"""
        self.board = self.rules.initial_board()
        self.current_turn = 'red'
        self.selected_piece = None
        self.red_time = 60
        self.black_time = 60
        self.board_widget.update_board(self.board)
        self.update_timer_label()
        self.status_label.setText('红方走棋')
        self.timer.start(1000)
        
    def on_piece_clicked(self, row, col):
        """点击棋子"""
        piece = self.board[row][col]
        if piece and piece['color'] == self.current_turn:
            self.selected_piece = (row, col)
            self.board_widget.highlight_piece(row, col)
            
    def on_cell_clicked(self, row, col):
        """点击格子"""
        if self.selected_piece:
            from_row, from_col = self.selected_piece
            moves = self.rules.get_valid_moves(self.board, from_row, from_col)
            if (row, col) in moves:
                self.make_move(from_row, from_col, row, col)
            self.selected_piece = None
            self.board_widget.clear_highlight()
            
    def make_move(self, from_row, from_col, to_row, to_col):
        """执行走棋"""
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        # 执行走棋
        self.board = self.rules.make_move(self.board, from_row, from_col, to_row, to_col)
        
        # 切换回合
        self.current_turn = 'black' if self.current_turn == 'red' else 'red'
        
        # 更新显示
        self.board_widget.update_board(self.board)
        
        turn_name = '红方' if self.current_turn == 'red' else '黑方'
        self.status_label.setText(turn_name + '走棋')
        
        # 检查游戏结束
        if self.rules.is_checkmate(self.board, self.current_turn):
            winner = '黑方' if self.current_turn == 'red' else '红方'
            QMessageBox.information(self, '游戏结束', winner + '获胜!')
            self.timer.stop()
        elif self.rules.is_check(self.board, self.current_turn):
            check_name = '红方' if self.current_turn == 'red' else '黑方'
            self.status_label.setText(check_name + '被将军!')
        
        # AI 走棋
        if self.current_turn == 'black' and self.game_mode == 'game':
            self.timer.stop()
            difficulty = self.difficulty_combo.currentIndex()
            ai_move = self.ai.get_best_move(self.board, difficulty)
            if ai_move:
                from_row, from_col, to_row, to_col = ai_move
                self.make_move(from_row, from_col, to_row, to_col)
            self.timer.start(1000)
            
    def check_timer(self):
        """检查计时器"""
        if self.current_turn == 'red':
            self.red_time -= 1
            if self.red_time <= 0:
                QMessageBox.warning(self, '时间到', '红方超时，黑方获胜!')
                self.timer.stop()
        else:
            self.black_time -= 1
            if self.black_time <= 0:
                QMessageBox.warning(self, '时间到', '黑方超时，红方获胜!')
                self.timer.stop()
        self.update_timer_label()
        
    def update_timer_label(self):
        """更新计时器显示"""
        self.timer_label.setText('红方: %d秒 | 黑方: %d秒' % (self.red_time, self.black_time))


class BoardWidget(QFrame):
    piece_clicked = pyqtSignal(int, int)
    cell_clicked = pyqtSignal(int, int)
    
    def __init__(self, rules, board):
        super().__init__()
        self.rules = rules
        self.board = board
        self.selected_cell = None
        self.highlighted_cells = []
        
        self.setFixedSize(450, 500)
        self.setStyleSheet('QFrame { background-color: #F5DEB3; border: 2px solid #8B4513; }')
        
    def update_board(self, board):
        self.board = board
        self.highlighted_cells = []
        self.update()
        
    def highlight_piece(self, row, col):
        self.highlighted_cells = [(row, col)]
        self.update()
        
    def clear_highlight(self):
        self.highlighted_cells = []
        self.update()
        
    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QPen, QBrush, QFont
        from PyQt5.QtCore import Qt
        
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2))
        
        # 绘制棋盘
        cell_size = 50
        margin = 25
        
        # 横线
        for i in range(9):
            painter.drawLine(margin, margin + i * cell_size, 
                           margin + 8 * cell_size, margin + i * cell_size)
        
        # 竖线
        for i in range(9):
            if i == 0 or i == 8:
                painter.drawLine(margin + i * cell_size, margin,
                               margin + i * cell_size, margin + 8 * cell_size)
            else:
                # 上半部分
                painter.drawLine(margin + i * cell_size, margin,
                               margin + i * cell_size, margin + 4 * cell_size)
                # 下半部分
                painter.drawLine(margin + i * cell_size, margin + 5 * cell_size,
                               margin + i * cell_size, margin + 8 * cell_size)
        
        # 绘制楚河汉界
        painter.setFont(QFont('SimSun', 16))
        painter.drawText(margin + 2 * cell_size, margin + 4 * cell_size + 15, '楚河')
        painter.drawText(margin + 5 * cell_size, margin + 4 * cell_size + 15, '汉界')
        
        # 绘制棋子
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece:
                    x = margin + col * cell_size
                    y = margin + row * cell_size
                    
                    # 高亮选中
                    if (row, col) in self.highlighted_cells:
                        painter.setBrush(QBrush(Qt.yellow))
                    else:
                        painter.setBrush(QBrush(Qt.white))
                    
                    painter.drawEllipse(x - 20, y - 20, 40, 40)
                    
                    # 绘制棋子文字
                    painter.setPen(QPen(Qt.black if piece['color'] == 'red' else Qt.red, 2))
                    painter.setFont(QFont('SimSun', 14, QFont.Bold))
                    painter.drawText(x - 15, y + 5, piece['name'])
                    
                    # 绘制合法走法提示
                    if (row, col) in self.highlighted_cells:
                        moves = self.rules.get_valid_moves(self.board, row, col)
                        for mr, mc in moves:
                            mx = margin + mc * cell_size
                            my = margin + mr * cell_size
                            painter.setBrush(QBrush(Qt.green))
                            painter.drawEllipse(mx - 5, my - 5, 10, 10)
    
    def mousePressEvent(self, event):
        cell_size = 50
        margin = 25
        
        col = (event.x() - margin) // cell_size
        row = (event.y() - margin) // cell_size
        
        if 0 <= row <= 8 and 0 <= col <= 8:
            # 检查是否点击了棋子
            piece = self.board[row][col]
            if piece:
                self.piece_clicked.emit(row, col)
            else:
                self.cell_clicked.emit(row, col)


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
