#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 游戏界面
使用图片绘制棋盘和棋子，支持窗口缩放
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QMessageBox,
                             QComboBox, QSlider)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QPalette, QBrush
from engine.rules import Board, Rules
from engine.ai import AI
from engine.sound import SoundManager


class ChessBoardWidget(QWidget):
    """棋盘组件 - 使用图片绘制"""
    
    move_requested = pyqtSignal(int, int, int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 棋盘数据
        self.board = Board()
        self.board.reset()
        
        # 游戏状态
        self.selected_piece = None
        self.valid_moves = []
        self.player_color = 'red'
        self.ai_color = 'black'
        self.difficulty = 'medium'
        self.ai = AI(difficulty=self.difficulty)
        
        # 计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timeout)
        self.time_limit = 60
        self.red_time = self.time_limit
        self.black_time = self.time_limit
        self.current_timer = None
        
        # 音效
        self.sound_mgr = SoundManager()
        
        # 图片缓存
        self.piece_pixmap = {}
        self.board_pixmap = None
        self._load_images()
        
        # 设置属性
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        # 最小尺寸
        self.setMinimumSize(540, 640)
        
    def _load_images(self):
        """加载图片资源"""
        # 获取 assets 路径
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        assets_path = os.path.join(base_path, '..', 'assets')
        if not os.path.exists(assets_path):
            assets_path = os.path.join(os.path.dirname(base_path), 'assets')
        
        # 加载棋子图片
        piece_files = {
            'K_red': 'K_red.png', 'K_black': 'K_black.png',
            'A_red': 'A_red.png', 'A_black': 'A_black.png',
            'B_red': 'B_red.png', 'B_black': 'B_black.png',
            'N_red': 'N_red.png', 'N_black': 'N_black.png',
            'R_red': 'R_red.png', 'R_black': 'R_black.png',
            'C_red': 'C_red.png', 'C_black': 'C_black.png',
            'P_red': 'P_red.png', 'P_black': 'P_black.png',
        }
        
        for key, filename in piece_files.items():
            path = os.path.join(assets_path, filename)
            if os.path.exists(path):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    self.piece_pixmap[key] = pixmap
        
        # 创建棋盘背景
        self._create_board_background()
        
    def _create_board_background(self):
        """创建棋盘背景图片"""
        # 棋盘尺寸
        cell_size = 60
        padding = 40
        width = padding * 2 + 8 * cell_size
        height = padding * 2 + 9 * cell_size
        
        # 创建 pixmap
        self.board_pixmap = QPixmap(width, height)
        self.board_pixmap.fill(QColor(220, 179, 94))
        
        # 绘制
        painter = QPainter(self.board_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制棋盘线
        painter.setPen(QColor(139, 69, 19))
        
        # 横线
        for i in range(10):
            y = padding + i * cell_size
            painter.drawLine(padding, y, padding + 8 * cell_size, y)
        
        # 竖线
        for i in range(9):
            x = padding + i * cell_size
            if i == 0 or i == 8:
                painter.drawLine(x, padding, x, padding + 9 * cell_size)
            else:
                painter.drawLine(x, padding, x, padding + 4 * cell_size)
                painter.drawLine(x, padding + 5 * cell_size, x, padding + 9 * cell_size)
        
        # 九宫格斜线
        painter.drawLine(padding + 3 * cell_size, padding + 7 * cell_size,
                        padding + 5 * cell_size, padding + 9 * cell_size)
        painter.drawLine(padding + 5 * cell_size, padding + 7 * cell_size,
                        padding + 3 * cell_size, padding + 9 * cell_size)
        painter.drawLine(padding + 3 * cell_size, padding,
                        padding + 5 * cell_size, padding + 2 * cell_size)
        painter.drawLine(padding + 5 * cell_size, padding,
                        padding + 3 * cell_size, padding + 2 * cell_size)
        
        # 楚河汉界文字
        painter.setFont(QFont("SimSun", 20, QFont.Bold))
        painter.setPen(QColor(139, 69, 19))
        painter.drawText(padding + 2 * cell_size, int(padding + 4.5 * cell_size), "楚 河")
        painter.drawText(padding + 5 * cell_size, int(padding + 4.5 * cell_size), "汉 界")
        
        painter.end()
        
        # 存储尺寸
        self.cell_size = cell_size
        self.padding = padding
        self.board_width = width
        self.board_height = height
        
    def resizeEvent(self, event):
        """窗口大小改变时重新计算"""
        super().resizeEvent(event)
        self.update()
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 获取 widget 尺寸
        widget_width = self.width()
        widget_height = self.height()
        
        # 计算缩放比例（保持纵横比）
        scale_x = widget_width / self.board_width
        scale_y = widget_height / self.board_height
        scale = min(scale_x, scale_y, 2.0)  # 最大缩放 2 倍
        
        # 计算居中偏移
        scaled_width = self.board_width * scale
        scaled_height = self.board_height * scale
        offset_x = (widget_width - scaled_width) // 2
        offset_y = (widget_height - scaled_height) // 2
        
        # 绘制棋盘背景
        if self.board_pixmap:
            painter.drawPixmap(offset_x, offset_y, 
                             scaled_width, scaled_height,
                             self.board_pixmap)
        
        # 绘制棋子
        for row in range(10):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece:
                    x = offset_x + (self.padding + col * self.cell_size) * scale
                    y = offset_y + (self.padding + row * self.cell_size) * scale
                    piece_size = self.cell_size * scale
                    
                    # 获取棋子图片
                    piece_key = f"{piece['type']}_{piece['color']}"
                    pixmap = self.piece_pixmap.get(piece_key)
                    
                    if pixmap and not pixmap.isNull():
                        # 绘制棋子图片
                        painter.drawPixmap(int(x - piece_size/2), int(y - piece_size/2),
                                         int(piece_size), int(piece_size),
                                         pixmap.scaled(int(piece_size), int(piece_size),
                                                     Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
                    else:
                        # 如果没有图片，使用圆形代替
                        painter.setBrush(QColor(220, 20, 60) if piece['color'] == 'red' else QColor(30, 30, 30))
                        painter.setPen(QColor(0, 0, 0))
                        painter.drawEllipse(int(x - piece_size/2), int(y - piece_size/2),
                                          int(piece_size), int(piece_size))
        
        # 绘制选中提示
        if self.selected_piece:
            row, col = self.selected_piece
            x = offset_x + (self.padding + col * self.cell_size) * scale
            y = offset_y + (self.padding + row * self.cell_size) * scale
            piece_size = self.cell_size * scale
            
            painter.setPen(QColor(255, 0, 0))
            painter.setBrush(QColor(255, 0, 0, 50))
            painter.drawEllipse(int(x - piece_size/2), int(y - piece_size/2),
                              int(piece_size), int(piece_size))
        
        # 绘制合法走法提示
        for to_row, to_col in self.valid_moves:
            x = offset_x + (self.padding + to_col * self.cell_size) * scale
            y = offset_y + (self.padding + to_row * self.cell_size) * scale
            dot_size = 15 * scale
            
            painter.setPen(QColor(0, 255, 0))
            painter.setBrush(QColor(0, 255, 0, 100))
            painter.drawEllipse(int(x - dot_size/2), int(y - dot_size/2),
                              int(dot_size), int(dot_size))
        
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() != Qt.LeftButton:
            return
        
        # 获取点击坐标并转换为棋盘坐标
        widget_width = self.width()
        widget_height = self.height()
        
        scale_x = widget_width / self.board_width
        scale_y = widget_height / self.board_height
        scale = min(scale_x, scale_y, 2.0)
        
        offset_x = (widget_width - self.board_width * scale) // 2
        offset_y = (widget_height - self.board_height * scale) // 2
        
        click_x = event.x() - offset_x
        click_y = event.y() - offset_y
        
        # 转换为棋盘格子坐标
        col = int(click_x / (self.cell_size * scale) - 0.5)
        row = int(click_y / (self.cell_size * scale) - 0.5)
        
        # 边界检查
        if 0 <= row < 10 and 0 <= col < 9:
            self._on_cell_clicked(row, col)
            
    def _on_cell_clicked(self, row, col):
        """处理格子点击"""
        piece = self.board.get_piece(row, col)
        
        if self.selected_piece is None:
            # 未选中棋子，尝试选中
            if piece and piece['color'] == self.player_color:
                self.selected_piece = (row, col)
                self.valid_moves = self._get_valid_moves(row, col)
                self.sound_mgr.play_select()
                self.update()
        else:
            # 已选中棋子
            from_row, from_col = self.selected_piece
            
            if (row, col) in self.valid_moves:
                # 移动到合法位置
                self.move_requested.emit(from_row, from_col, row, col)
                self.selected_piece = None
                self.valid_moves = []
                self.update()
            elif piece and piece['color'] == self.player_color:
                # 选中其他己方棋子
                self.selected_piece = (row, col)
                self.valid_moves = self._get_valid_moves(row, col)
                self.sound_mgr.play_select()
                self.update()
            else:
                # 取消选中
                self.selected_piece = None
                self.valid_moves = []
                self.update()
                
    def _get_valid_moves(self, row, col):
        """获取合法走法"""
        piece = self.board.get_piece(row, col)
        if not piece:
            return []
        
        # 获取所有走法
        all_moves = Rules.get_all_moves(self.board, piece['color'])
        
        # 过滤出从 (row, col) 出发的走法
        valid = []
        for from_r, from_c, to_r, to_c in all_moves:
            if from_r == row and from_c == col:
                valid.append((to_r, to_c))
        
        return valid
        
    def make_move(self, from_row, from_col, to_row, to_col):
        """执行移动"""
        captured = self.board.move_piece(from_row, from_col, to_row, to_col)
        
        # 播放音效
        if captured:
            self.sound_mgr.play_capture()
        else:
            self.sound_mgr.play_move()
        
        self.update()
        return captured
        
    def _on_timeout(self):
        """超时处理"""
        if self.current_timer == 'red':
            self.red_time -= 1
            if self.red_time <= 0:
                self.sound_mgr.play_timeout()
                QMessageBox.warning(self, "超时", "红方超时，黑方获胜！")
                self.timer.stop()
                self.current_timer = None
                self.emit_game_over('black')
        elif self.current_timer == 'black':
            self.black_time -= 1
            if self.black_time <= 0:
                self.sound_mgr.play_timeout()
                QMessageBox.warning(self, "超时", "黑方超时，红方获胜！")
                self.timer.stop()
                self.current_timer = None
                self.emit_game_over('red')
                
    def emit_game_over(self, winner):
        """发送游戏结束信号"""
        pass  # 由父组件处理
        
    def set_time_labels(self, red_label, black_label):
        """设置时间标签"""
        self.red_time_label = red_label
        self.black_time_label = black_label
        
    def update_time_display(self):
        """更新时间显示"""
        if hasattr(self, 'red_time_label'):
            self.red_time_label.setText(f"红方: {self.red_time}s")
        if hasattr(self, 'black_time_label'):
            self.black_time_label.setText(f"黑方: {self.black_time}s")
            
    def start_timer(self, color):
        """启动计时器"""
        if self.current_timer:
            self.timer.stop()
        
        if color == 'red':
            self.red_time = self.time_limit
        else:
            self.black_time = self.time_limit
            
        self.current_timer = color
        self.timer.start(1000)
        self.update_time_display()
        
    def restart_game(self):
        """重新开始"""
        self.board.reset()
        self.selected_piece = None
        self.valid_moves = []
        self.red_time = self.time_limit
        self.black_time = self.time_limit
        self.current_timer = None
        self.timer.stop()
        self.update()
        self.start_timer('red')
        self.sound_mgr.play_game_start()


class GameWidget(QWidget):
    """游戏主界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.board_widget = ChessBoardWidget()
        self.ai = AI(difficulty='medium')
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 控制面板
        control_layout = QHBoxLayout()
        
        control_layout.addWidget(QLabel("难度:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(['初级', '中级', '高级', '终极高手'])
        self.difficulty_combo.currentTextChanged.connect(self._on_difficulty_changed)
        control_layout.addWidget(self.difficulty_combo)
        
        control_layout.addWidget(QLabel("音量:"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        control_layout.addWidget(self.volume_slider)
        
        self.restart_btn = QPushButton("重新开始")
        self.restart_btn.clicked.connect(self.restart_game)
        control_layout.addWidget(self.restart_btn)
        
        layout.addLayout(control_layout)
        
        # 棋盘
        layout.addWidget(self.board_widget)
        
        # 时间显示
        time_layout = QHBoxLayout()
        self.red_time_label = QLabel("红方: 60s")
        self.black_time_label = QLabel("黑方: 60s")
        time_layout.addWidget(self.red_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.black_time_label)
        layout.addLayout(time_layout)
        
        # 状态显示
        self.status_label = QLabel("游戏开始，红方先行")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 连接信号
        self.board_widget.move_requested.connect(self._on_move_requested)
        self.board_widget.set_time_labels(self.red_time_label, self.black_time_label)
        
        # 开始游戏
        self.board_widget.start_timer('red')
        
    def _on_move_requested(self, from_row, from_col, to_row, to_col):
        """处理走棋请求"""
        # 执行玩家走棋
        self.board_widget.make_move(from_row, from_col, to_row, to_col)
        
        # 检查游戏是否结束
        if self._check_game_over():
            return
        
        # AI 走棋
        self.board_widget.timer.stop()
        self._ai_move()
        
    def _ai_move(self):
        """AI 走棋"""
        import random
        
        # 获取 AI 走法
        board = self.board_widget.board
        color = self.board_widget.ai_color
        
        # 获取所有合法走法
        all_moves = Rules.get_all_moves(board, color)
        
        if all_moves:
            # 简单 AI：随机选择
            move = random.choice(all_moves)
            from_row, from_col, to_row, to_col = move
            
            # 执行 AI 走棋
            self.board_widget.make_move(from_row, from_col, to_row, to_col)
            
            # 检查游戏是否结束
            if not self._check_game_over():
                # 重新启动计时器
                self.board_widget.start_timer('red')
        
    def _check_game_over(self):
        """检查游戏是否结束"""
        board = self.board_widget.board
        current_color = self.board_widget.current_timer
        
        if Rules.is_checkmate(board, current_color):
            winner = 'black' if current_color == 'red' else 'red'
            self.status_label.setText(f"游戏结束！{winner}获胜！")
            QMessageBox.information(self, "游戏结束", f"{winner}获胜！")
            self.board_widget.timer.stop()
            return True
        return False
        
    def _on_difficulty_changed(self, difficulty):
        """难度改变"""
        difficulty_map = {
            '初级': 'easy',
            '中级': 'medium',
            '高级': 'hard',
            '终极高手': 'expert'
        }
        self.board_widget.difficulty = difficulty_map.get(difficulty, 'medium')
        self.board_widget.ai = AI(difficulty=self.board_widget.difficulty)
        
    def _on_volume_changed(self, value):
        """音量改变"""
        self.board_widget.sound_mgr.set_volume(value / 100)
        
    def restart_game(self):
        """重新开始"""
        self.board_widget.restart_game()
        self.status_label.setText("游戏开始，红方先行")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = GameWidget()
    window.setWindowTitle('中国象棋 - Chinese Chess')
    window.show()
    
    sys.exit(app.exec_())
