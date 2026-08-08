#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 残局挑战界面
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QMessageBox,
                             QScrollArea, QFrame, QGroupBox, QTextEdit,
                             QComboBox, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from engine.rules import Board, Rules
from engine.ai import AI
from data.endgames import get_endgame, list_endgames


class EndgameWidget(QWidget):
    """残局挑战组件"""
    
    move_requested = pyqtSignal(int, int, int, int)
    game_over = pyqtSignal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.board = Board()
        self.board.reset()
        
        self.current_endgame = None
        self.selected_piece = None
        self.valid_moves = []
        
        self.cell_size = 60
        self.padding = 40
        
        self.ai = AI(difficulty='easy')
        
        self.move_count = 0
        self.is_solving = False
        self.solution_moves = []
        self.solution_index = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 残局选择区域
        select_layout = QHBoxLayout()
        select_layout.addWidget(QLabel("选择残局:"))
        
        self.endgame_combo = QComboBox()
        self.endgame_combo.addItems([f"{i+1}. {e['name']}" for i, e in enumerate(list_endgames())])
        self.endgame_combo.currentIndexChanged.connect(self._on_endgame_selected)
        select_layout.addWidget(self.endgame_combo)
        
        self.start_btn = QPushButton("开始挑战")
        self.start_btn.clicked.connect(self.start_endgame)
        select_layout.addWidget(self.start_btn)
        
        layout.addLayout(select_layout)
        
        # 残局信息区域
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        
        self.endgame_title = QLabel("")
        self.endgame_title.setFont(QFont("SimHei", 16, QFont.Bold))
        self.endgame_title.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.endgame_title)
        
        self.endgame_desc = QLabel("")
        self.endgame_desc.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.endgame_desc)
        
        layout.addWidget(info_frame)
        
        # 棋盘区域
        self.paint_area = EndgamePaintArea(self)
        layout.addWidget(self.paint_area)
        
        # 控制按钮
        btn_layout = QHBoxLayout()
        
        self.hint_btn = QPushButton("提示")
        self.hint_btn.clicked.connect(self.show_hint)
        self.hint_btn.setEnabled(False)
        btn_layout.addWidget(self.hint_btn)
        
        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_endgame)
        self.reset_btn.setEnabled(False)
        btn_layout.addWidget(self.reset_btn)
        
        self.next_btn = QPushButton("下一关")
        self.next_btn.clicked.connect(self.next_endgame)
        self.next_btn.setEnabled(False)
        btn_layout.addWidget(self.next_btn)
        
        layout.addLayout(btn_layout)
        
        # 状态显示
        self.status_label = QLabel("请选择残局并开始挑战")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 步数显示
        self.move_label = QLabel("步数: 0")
        self.move_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.move_label)
    
    def _on_endgame_selected(self, index):
        """残局选择改变"""
        if index >= 0:
            endgame = get_endgame(index + 1)
            if endgame:
                self.current_endgame = endgame
                self.endgame_title.setText(endgame['name'])
                self.endgame_desc.setText(endgame['description'])
    
    def start_endgame(self):
        """开始残局挑战"""
        if not self.current_endgame:
            QMessageBox.warning(self, "警告", "请先选择一个残局")
            return
        
        # 加载残局
        self.load_endgame(self.current_endgame)
        
        # 启用按钮
        self.hint_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        self.next_btn.setEnabled(False)
        
        # 重置状态
        self.move_count = 0
        self.update_move_count()
        self.status_label.setText(f"残局开始: {self.current_endgame['name']}")
        
        # 准备解法
        self.solution_moves = self._parse_solution(self.current_endgame['solution'])
        self.solution_index = 0
        self.is_solving = False
    
    def load_endgame(self, endgame):
        """加载残局棋盘"""
        self.board = Board()
        self.board.reset()
        
        for piece_data in endgame['pieces']:
            self.board.set_piece(piece_data['row'], piece_data['col'], {
                'type': piece_data['type'],
                'color': piece_data['color']
            })
        
        self.paint_area.update()
    
    def _parse_solution(self, solution_str):
        """解析解法字符串"""
        # 简化解法解析
        moves = []
        parts = solution_str.split('，')
        for part in parts:
            part = part.strip()
            if part:
                moves.append(part)
        return moves
    
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
        painter.drawLine(self.padding + 3 * self.cell_size, self.padding + 7 * self.cell_size,
                        self.padding + 5 * self.cell_size, self.padding + 9 * self.cell_size)
        painter.drawLine(self.padding + 5 * self.cell_size, self.padding + 7 * self.cell_size,
                        self.padding + 3 * self.cell_size, self.padding + 9 * self.cell_size)
        
        painter.drawLine(self.padding + 3 * self.cell_size, self.padding,
                        self.padding + 5 * self.cell_size, self.padding + 2 * self.cell_size)
        painter.drawLine(self.padding + 5 * self.cell_size, self.padding,
                        self.padding + 3 * self.cell_size, self.padding + 2 * self.cell_size)
        
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
        
        if color == 'red':
            painter.setBrush(QColor(220, 20, 60))
            painter.setPen(QColor(180, 0, 0))
        else:
            painter.setBrush(QColor(30, 30, 30))
            painter.setPen(QColor(0, 0, 0))
        
        painter.drawEllipse(x - 25, y - 25, 50, 50)
        
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
        
        painter.drawText(int(x - 15), int(y + 7), piece_names.get(piece_type, '?'))
    
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
            if piece and piece['color'] == 'red':
                self.selected_piece = (row, col)
                self.valid_moves = Rules.get_valid_moves(self.board, row, col)
                self.update()
        else:
            if (row, col) in self.valid_moves:
                from_row, from_col = self.selected_piece
                self.make_move(from_row, from_col, row, col)
                self.selected_piece = None
                self.valid_moves = []
                self.update()
            elif piece and piece['color'] == 'red':
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
        self.move_count += 1
        self.update_move_count()
        
        # 检查是否将死
        if Rules.is_checkmate(self.board, 'black'):
            self.status_label.setText(f"挑战成功！用时 {self.move_count} 步")
            QMessageBox.information(self, "挑战成功", f"恭喜！你用了 {self.move_count} 步解决了残局！")
            self.next_btn.setEnabled(True)
            self.is_solving = False
            return True
        
        # 检查是否走错（简单检查：是否吃掉对方棋子）
        if Rules.is_checkmate(self.board, 'red'):
            self.status_label.setText("游戏结束！黑方获胜")
            QMessageBox.warning(self, "挑战失败", "黑方获胜，请重新挑战！")
            self.is_solving = False
            return True
        
        return False
    
    def update_move_count(self):
        """更新步数显示"""
        self.move_label.setText(f"步数: {self.move_count}")
    
    def show_hint(self):
        """显示提示"""
        if not self.current_endgame or self.solution_index >= len(self.solution_moves):
            return
        
        # 找到当前应该走的棋子
        hint = self.solution_moves[self.solution_index]
        QMessageBox.information(self, "提示", f"下一步: {hint}")
    
    def reset_endgame(self):
        """重置残局"""
        if self.current_endgame:
            self.load_endgame(self.current_endgame)
            self.move_count = 0
            self.update_move_count()
            self.selected_piece = None
            self.valid_moves = []
            self.solution_index = 0
            self.status_label.setText(f"已重置: {self.current_endgame['name']}")
            self.update()
    
    def next_endgame(self):
        """下一关"""
        current_id = self.current_endgame['id'] if self.current_endgame else 1
        next_id = current_id + 1
        
        if next_id <= len(list_endgames()):
            self.endgame_combo.setCurrentIndex(next_id - 1)
            self.start_endgame()
        else:
            QMessageBox.information(self, "恭喜", "所有残局已完成！")


class EndgamePaintArea(QWidget):
    """残局绘制区域"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(540, 640)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EndgameWidget()
    window.show()
    sys.exit(app.exec_())
