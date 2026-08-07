#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 棋盘界面
使用 PyQt5 实现图形界面
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QMessageBox,
                             QComboBox, QFrame)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from engine.rules import Board, Rules
from engine.ai import AI


class BoardWidget(QWidget):
    """棋盘组件"""
    
    # 信号
    move_requested = pyqtSignal(int, int, int, int)  # from_row, from_col, to_row, to_col
    game_started = pyqtSignal(str)  # player color
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.board = Board()
        self.board.reset()
        
        self.selected_piece = None  # (row, col)
        self.valid_moves = []  # [(row, col), ...]
        
        self.cell_size = 60
        self.padding = 40
        
        self.player_color = 'red'
        self.ai_color = 'black'
        self.difficulty = 'medium'
        self.ai = AI(difficulty=self.difficulty)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timeout)
        
        self.time_limit = 60  # 秒
        self.red_time = self.time_limit
        self.black_time = self.time_limit
        self.current_timer = None
        
        self.setup_ui()
        self.setMinimumSize(600, 700)
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 控制面板
        control_layout = QHBoxLayout()
        
        # 难度选择
        control_layout.addWidget(QLabel("难度:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(['初级', '中级', '高级', '终极高手'])
        self.difficulty_combo.currentTextChanged.connect(self._on_difficulty_changed)
        control_layout.addWidget(self.difficulty_combo)
        
        # 重新开始按钮
        self.restart_btn = QPushButton("重新开始")
        self.restart_btn.clicked.connect(self.restart_game)
        control_layout.addWidget(self.restart_btn)
        
        layout.addLayout(control_layout)
        
        # 棋盘区域
        self.board_label = QLabel()
        self.board_label.setAlignment(Qt.AlignCenter)
        self.paint_area = PaintArea(self)
        layout.addWidget(self.paint_area)
        
        # 时间显示
        time_layout = QHBoxLayout()
        self.red_time_label = QLabel(f"红方: {self.red_time}s")
        self.black_time_label = QLabel(f"黑方: {self.black_time}s")
        time_layout.addWidget(self.red_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.black_time_label)
        layout.addLayout(time_layout)
        
        # 状态显示
        self.status_label = QLabel("游戏开始，红方先行")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
    
    def paintEvent(self, event):
        """绘制棋盘"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制棋盘背景
        painter.fillRect(0, 0, self.width(), self.height(), QColor(220, 179, 94))
        
        # 绘制棋盘网格
        painter.setPen(QColor(139, 69, 19))
        
        # 横线
        for i in range(10):
            y = self.padding + i * self.cell_size
            painter.drawLine(self.padding, y, self.padding + 8 * self.cell_size, y)
        
        # 竖线
        for i in range(9):
            x = self.padding + i * self.cell_size
            if i == 0 or i == 8:
                painter.drawLine(x, self.padding, x, self.padding + 9 * self.cell_size)
            else:
                painter.drawLine(x, self.padding, x, self.padding + 4 * self.cell_size)
                painter.drawLine(x, self.padding + 5 * self.cell_size, x, self.padding + 9 * self.cell_size)
        
        # 绘制九宫格斜线
        # 红方九宫
        painter.drawLine(self.padding + 3 * self.cell_size, self.padding + 7 * self.cell_size,
                        self.padding + 5 * self.cell_size, self.padding + 9 * self.cell_size)
        painter.drawLine(self.padding + 5 * self.cell_size, self.padding + 7 * self.cell_size,
                        self.padding + 3 * self.cell_size, self.padding + 9 * self.cell_size)
        
        # 黑方九宫
        painter.drawLine(self.padding + 3 * self.cell_size, self.padding,
                        self.padding + 5 * self.cell_size, self.padding + 2 * self.cell_size)
        painter.drawLine(self.padding + 5 * self.cell_size, self.padding,
                        self.padding + 3 * self.cell_size, self.padding + 2 * self.cell_size)
        
        # 绘制楚河汉界
        painter.setFont(QFont("SimSun", 24, QFont.Bold))
        painter.setPen(QColor(139, 69, 19))
        painter.drawText(self.padding + 2 * self.cell_size, self.padding + 4.5 * self.cell_size, "楚 河",)
        painter.drawText(self.padding + 5 * self.cell_size, self.padding + 4.5 * self.cell_size, "汉 界",)
        
        # 绘制棋子
        for row in range(10):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece:
                    x = self.padding + col * self.cell_size
                    y = self.padding + row * self.cell_size
                    self._draw_piece(painter, piece, x, y)
        
        # 绘制选中提示
        if self.selected_piece:
            row, col = self.selected_piece
            x = self.padding + col * self.cell_size
            y = self.padding + row * self.cell_size
            painter.setPen(QColor(255, 0, 0))
            painter.drawEllipse(x - 25, y - 25, 50, 50)
        
        # 绘制合法走法提示
        for to_row, to_col in self.valid_moves:
            x = self.padding + to_col * self.cell_size
            y = self.padding + to_row * self.cell_size
            painter.setPen(QColor(0, 255, 0))
            painter.drawEllipse(x - 10, y - 10, 20, 20)
    
    def _draw_piece(self, painter, piece, x, y):
        """绘制棋子"""
        piece_type = piece['type']
        color = piece['color']
        
        # 棋子背景
        if color == 'red':
            painter.setBrush(QColor(220, 20, 60))
            painter.setPen(QColor(180, 0, 0))
        else:
            painter.setBrush(QColor(30, 30, 30))
            painter.setPen(QColor(0, 0, 0))
        
        painter.drawEllipse(x - 25, y - 25, 50, 50)
        
        # 棋子文字
        painter.setPen(QColor(255, 255, 255) if color == 'black' else QColor(255, 215, 0))
        painter.setFont(QFont("SimHei", 20, QFont.Bold))
        
        piece_names = {
            'K': '将' if color == 'black' else '帅',
            'A': '士' if color == 'black' else '仕',
            'B': '象' if color == 'black' else '相',
            'N': '马' if color == 'black' else '马',
            'R': '车' if color == 'black' else '车',
            'C': '炮' if color == 'black' else '炮',
            'P': '卒' if color == 'black' else '兵',
        }
        
        painter.drawText(x - 15, y + 7, piece_names.get(piece_type, '?'))
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            x = event.x() - self.padding
            y = event.y() - self.padding
            
            col = int(x / self.cell_size)
            row = int(y / self.cell_size)
            
            if 0 <= row < 10 and 0 <= col < 9:
                self._on_cell_clicked(row, col)
    
    def _on_cell_clicked(self, row, col):
        """处理单元格点击"""
        piece = self.board.get_piece(row, col)
        
        if self.selected_piece is None:
            # 选择棋子
            if piece and piece['color'] == self.player_color:
                self.selected_piece = (row, col)
                self.valid_moves = Rules.get_valid_moves(self.board, row, col)
                self.update()
        else:
            # 尝试移动
            if (row, col) in self.valid_moves:
                from_row, from_col = self.selected_piece
                self.move_requested.emit(from_row, from_col, row, col)
                self.selected_piece = None
                self.valid_moves = []
                self.update()
            elif piece and piece['color'] == self.player_color:
                # 重新选择
                self.selected_piece = (row, col)
                self.valid_moves = Rules.get_valid_moves(self.board, row, col)
                self.update()
            else:
                self.selected_piece = None
                self.valid_moves = []
                self.update()
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """执行移动"""
        captured = self.board.move_piece(from_row, from_col, to_row, to_col)
        
        # 检查是否将死
        opponent_color = 'black' if self.player_color == 'red' else 'red'
        if Rules.is_checkmate(self.board, opponent_color):
            self.status_label.setText(f"游戏结束！{self.player_color.capitalize()} 获胜！")
            QMessageBox.information(self, "游戏结束", f"{self.player_color.capitalize()} 获胜！")
            return True
        
        # 切换回合
        self._start_timer(opponent_color)
        return False
    
    def _start_timer(self, color):
        """启动计时器"""
        if self.current_timer:
            self.current_timer.stop()
        
        if color == 'red':
            self.red_time = self.time_limit
            self.red_time_label.setText(f"红方: {self.red_time}s")
        else:
            self.black_time = self.time_limit
            self.black_time_label.setText(f"黑方: {self.black_time}s")
        
        self.current_timer = color
        self.timer.start(1000)
    
    def _on_timeout(self):
        """超时处理"""
        if self.current_timer == 'red':
            self.red_time -= 1
            self.red_time_label.setText(f"红方: {self.red_time}s")
            if self.red_time <= 0:
                self.status_label.setText("红方超时，黑方获胜！")
                QMessageBox.warning(self, "超时", "红方超时，黑方获胜！")
                self.timer.stop()
                self.current_timer = None
        elif self.current_timer == 'black':
            self.black_time -= 1
            self.black_time_label.setText(f"黑方: {self.black_time}s")
            if self.black_time <= 0:
                self.status_label.setText("黑方超时，红方获胜！")
                QMessageBox.warning(self, "超时", "黑方超时，红方获胜！")
                self.timer.stop()
                self.current_timer = None
    
    def _on_difficulty_changed(self, difficulty):
        """难度改变"""
        difficulty_map = {
            '初级': 'easy',
            '中级': 'medium',
            '高级': 'hard',
            '终极高手': 'expert'
        }
        self.difficulty = difficulty_map.get(difficulty, 'medium')
        self.ai = AI(difficulty=self.difficulty)
    
    def restart_game(self):
        """重新开始游戏"""
        self.board.reset()
        self.selected_piece = None
        self.valid_moves = []
        self.red_time = self.time_limit
        self.black_time = self.time_limit
        self.red_time_label.setText(f"红方: {self.red_time}s")
        self.black_time_label.setText(f"黑方: {self.black_time}s")
        self.current_timer = None
        self.timer.stop()
        self.status_label.setText("游戏开始，红方先行")
        self.update()
        
        # 开始红方计时
        self._start_timer('red')


class PaintArea(QWidget):
    """绘制区域"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(540, 640)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        # 这里可以绘制额外的图形
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BoardWidget()
    window.show()
    sys.exit(app.exec_())
