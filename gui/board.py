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
from PyQt5.QtGui import (QPainter, QColor, QFont, QPixmap, QPalette, QBrush,
                       QImage, QRadialGradient, QLinearGradient, QPainterPath, QPen)
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
        
        # 棋子图片目录（AI 生成的木质棋子素材）
        pieces_path = os.path.join(assets_path, 'pieces')
        if not os.path.exists(pieces_path):
            pieces_path = assets_path  # 回退到旧位置
        
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
            path = os.path.join(pieces_path, filename)
            if os.path.exists(path):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    # 加圆形 alpha 遮罩：圆心内不透明、方形四角透明，
                    # 避免棋子方形背景盖住棋盘网格线
                    self.piece_pixmap[key] = self._apply_circular_mask(pixmap)
        
        # 加载棋盘木质纹理（可选，用于底图）
        board_tex = os.path.join(assets_path, 'board_texture.png')
        self.board_texture = None
        if os.path.exists(board_tex):
            tex = QPixmap(board_tex)
            if not tex.isNull():
                self.board_texture = tex
        
        # 创建棋盘背景
        self._create_board_background()

    def _apply_circular_mask(self, pixmap):
        """棋子图已预处理为圆盘内不透明、圆盘外透明（自带 alpha）。
        这里只做居中正方形裁剪，保留原 alpha，不再叠加圆形遮罩。"""
        img = pixmap.toImage().convertToFormat(QImage.Format_ARGB32)
        w, h = img.width(), img.height()
        s = min(w, h)
        cx, cy = w // 2, h // 2
        square = QImage(s, s, QImage.Format_ARGB32)
        square.fill(Qt.transparent)
        sp = QPainter(square)
        sp.setRenderHint(QPainter.Antialiasing)
        sp.drawImage(0, 0, img, cx - s // 2, cy - s // 2, s, s)
        sp.end()
        return QPixmap.fromImage(square)

    def _create_board_background(self):
        """创建带质感和立体感的棋盘背景图片"""
        cell_size = 60
        padding = 40
        width = padding * 2 + 8 * cell_size
        height = padding * 2 + 9 * cell_size
        # 加一圈立体木框
        frame = 18
        total_w = width + frame * 2
        total_h = height + frame * 2

        self.board_pixmap = QPixmap(total_w, total_h)
        painter = QPainter(self.board_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # --- 外木框（立体渐变）---
        frame_grad = QLinearGradient(0, 0, total_w, total_h)
        frame_grad.setColorAt(0, QColor(120, 72, 33))
        frame_grad.setColorAt(0.5, QColor(96, 56, 24))
        frame_grad.setColorAt(1, QColor(70, 40, 16))
        painter.setBrush(QBrush(frame_grad))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, total_w, total_h, 14, 14)

        # 内框高光描边
        painter.setPen(QColor(180, 130, 70))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(3, 3, total_w - 6, total_h - 6, 12, 12)

        # --- 棋盘木质面（使用 AI 生成的木质纹理底图，平铺覆盖）---
        board_top = frame
        board_left = frame
        if self.board_texture and not self.board_texture.isNull():
            # 将纹理缩放铺满棋盘面，保留真实木纹质感
            scaled_tex = self.board_texture.scaled(
                width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            painter.setBrush(QBrush(scaled_tex))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(board_left, board_top, width, height, 6, 6)
            # 叠一层半透明木色统一色调
            face_grad = QLinearGradient(board_left, board_top, board_left + width, board_top + height)
            face_grad.setColorAt(0, QColor(232, 192, 120, 70))
            face_grad.setColorAt(1, QColor(196, 150, 78, 70))
            painter.setBrush(QBrush(face_grad))
            painter.drawRoundedRect(board_left, board_top, width, height, 6, 6)
        else:
            # 回退：纯渐变木色面
            face_grad = QLinearGradient(board_left, board_top, board_left + width, board_top + height)
            face_grad.setColorAt(0, QColor(232, 192, 120))
            face_grad.setColorAt(0.5, QColor(214, 168, 92))
            face_grad.setColorAt(1, QColor(196, 150, 78))
            painter.setBrush(QBrush(face_grad))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(board_left, board_top, width, height, 6, 6)

        # 木纹：随机浅色细纹（仅在无纹理底图时点缀）
        if not (self.board_texture and not self.board_texture.isNull()):
            import random
            rng = random.Random(20240809)
            painter.setPen(QColor(205, 160, 86, 90))
            for _ in range(60):
                x1 = board_left + rng.uniform(0, width)
                y1 = board_top + rng.uniform(0, height)
                x2 = x1 + rng.uniform(-30, 30)
                y2 = y1 + rng.uniform(20, 70)
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # 绘制棋盘线（深棕，加粗提高对比度）
        line_color = QColor(70, 38, 14)
        painter.setPen(QPen(line_color, 2.2))
        # 横线
        for i in range(10):
            y = board_top + padding + i * cell_size
            painter.drawLine(board_left + padding, y, board_left + padding + 8 * cell_size, y)
        # 竖线
        for i in range(9):
            x = board_left + padding + i * cell_size
            if i == 0 or i == 8:
                painter.drawLine(x, board_top + padding, x, board_top + padding + 9 * cell_size)
            else:
                painter.drawLine(x, board_top + padding, x, board_top + padding + 4 * cell_size)
                painter.drawLine(x, board_top + padding + 5 * cell_size, x, board_top + padding + 9 * cell_size)
        # 九宫格斜线
        palace = [
            (3, 7, 5, 9), (5, 7, 3, 9),
            (3, 0, 5, 2), (5, 0, 3, 2),
        ]
        for c1, r1, c2, r2 in palace:
            painter.drawLine(
                board_left + padding + c1 * cell_size, board_top + padding + r1 * cell_size,
                board_left + padding + c2 * cell_size, board_top + padding + r2 * cell_size)

        # 楚河汉界文字（使用衬线/楷体风格字体，更具书法韵味）
        serif_font = QFont("Noto Serif CJK SC", 24, QFont.Bold)
        if serif_font.family() == "Noto Serif CJK SC":
            painter.setFont(serif_font)
        else:
            painter.setFont(QFont("SimSun", 24, QFont.Bold))
        # 加深文字颜色，提高辨识度
        painter.setPen(QColor(60, 30, 10))
        mid = board_top + padding + 4.5 * cell_size + 8
        painter.drawText(int(board_left + padding + 1.6 * cell_size), int(mid), "楚  河")
        painter.drawText(int(board_left + padding + 5.1 * cell_size), int(mid), "漢  界")

        # 外圈投影（仅边缘内阴影，不覆盖棋盘面与文字）
        painter.setPen(Qt.NoPen)
        edge_shadow = QColor(40, 22, 8, 90)
        painter.setBrush(edge_shadow)
        # 用缩放后的棋子面绘制方式：先画暗色满面，再用清晰木面盖回中间
        # 这里改用描边阴影：在棋盘面四边各画一条渐隐暗线
        painter.setBrush(Qt.NoBrush)
        for d in range(6):
            a = 90 - d * 14
            painter.setPen(QColor(40, 22, 8, max(a, 0)))
            painter.drawRoundedRect(
                board_left + 1 + d, board_top + 1 + d,
                width - 2 - d * 2, height - 2 - d * 2, 6, 6)

        painter.end()

        self.cell_size = cell_size
        self.padding = padding
        self.frame_size = frame
        self.board_width = width
        self.board_height = height
    def resizeEvent(self, event):
        """窗口大小改变时重新计算"""
        super().resizeEvent(event)
        self.update()
        
    def _draw_3d_piece(self, painter, piece, cx, cy, size):
        """绘制一个带 3D 质感的棋子（径向渐变球面 + 投影 + 高光）。"""
        r = size / 2
        # 投影
        painter.setBrush(QColor(40, 22, 8, 90))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(cx - r * 0.98), int(cy - r * 0.82), int(r * 2.0), int(r * 1.9))

        # 外圈木托（暗环）
        base_grad = QRadialGradient(cx, cy - r * 0.3, r * 1.15)
        if piece['color'] == 'red':
            base_grad.setColorAt(0, QColor(235, 90, 80))
            base_grad.setColorAt(0.55, QColor(206, 44, 40))
            base_grad.setColorAt(1, QColor(150, 20, 22))
        else:
            base_grad.setColorAt(0, QColor(90, 90, 96))
            base_grad.setColorAt(0.55, QColor(48, 50, 56))
            base_grad.setColorAt(1, QColor(22, 24, 28))
        painter.setBrush(QBrush(base_grad))
        painter.setPen(QPen(QColor(30, 30, 30), 1.4))
        painter.drawEllipse(int(cx - r), int(cy - r), int(size), int(size))

        # 内圈面（浅色凹陷感）
        inner_r = r * 0.82
        face_grad = QRadialGradient(cx, cy - r * 0.35, inner_r * 1.2)
        if piece['color'] == 'red':
            face_grad.setColorAt(0, QColor(255, 150, 140))
            face_grad.setColorAt(0.6, QColor(228, 60, 54))
            face_grad.setColorAt(1, QColor(180, 34, 32))
        else:
            face_grad.setColorAt(0, QColor(150, 152, 158))
            face_grad.setColorAt(0.6, QColor(88, 90, 98))
            face_grad.setColorAt(1, QColor(40, 42, 48))
        painter.setBrush(QBrush(face_grad))
        painter.setPen(QPen(QColor(20, 20, 20, 160), 1.0))
        painter.drawEllipse(int(cx - inner_r), int(cy - inner_r), int(inner_r * 2), int(inner_r * 2))

        # 顶部高光
        hi = QRadialGradient(cx - r * 0.3, cy - r * 0.45, r * 0.7)
        hi.setColorAt(0, QColor(255, 255, 255, 170))
        hi.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(hi))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(cx - r * 0.7), int(cy - r * 0.8), int(r * 1.1), int(r * 0.9))

        # 棋子文字
        piece_names = {
            'K': '帅' if piece['color'] == 'red' else '将',
            'A': '仕' if piece['color'] == 'red' else '士',
            'B': '相' if piece['color'] == 'red' else '象',
            'N': '马', 'R': '车', 'C': '炮',
            'P': '兵' if piece['color'] == 'red' else '卒',
        }
        name = piece_names.get(piece['type'], '?')
        font = QFont("SimHei", int(size * 0.42), QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(255, 240, 200) if piece['color'] == 'red' else QColor(235, 238, 245))
        # 文字描边阴影
        painter.drawText(int(cx - size * 0.42), int(cy + size * 0.16), name)

    def paintEvent(self, event):
        """绘制事件（3D 质感渲染）"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        widget_width = self.width()
        widget_height = self.height()

        # 整图缩放（含立体边框）
        total_w = self.board_width + self.frame_size * 2
        total_h = self.board_height + self.frame_size * 2
        scale_x = widget_width / total_w
        scale_y = widget_height / total_h
        scale = min(scale_x, scale_y, 2.0)

        scaled_width = total_w * scale
        scaled_height = total_h * scale
        offset_x = (widget_width - scaled_width) // 2
        offset_y = (widget_height - scaled_height) // 2

        # 棋盘背景
        if self.board_pixmap:
            painter.drawPixmap(int(offset_x), int(offset_y),
                             int(scaled_width), int(scaled_height),
                             self.board_pixmap)

        # 棋格坐标 -> 屏幕坐标
        def cell_pos(row, col):
            x = offset_x + (self.frame_size + self.padding + col * self.cell_size) * scale
            y = offset_y + (self.frame_size + self.padding + row * self.cell_size) * scale
            return x, y

        piece_size = self.cell_size * scale

        # 棋子
        for row in range(10):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece:
                    x, y = cell_pos(row, col)
                    key = f"{piece['type']}_{piece['color']}"
                    pix = self.piece_pixmap.get(key)
                    if pix and not pix.isNull():
                        # 使用 AI 生成的木质棋子素材（本体木色，红/黑文字区分敌我）
                        draw_size = piece_size * 0.9
                        painter.drawPixmap(int(x - draw_size/2), int(y - draw_size/2),
                                         int(draw_size), int(draw_size), pix)
                    else:
                        # 回退：3D 绘制
                        self._draw_3d_piece(painter, piece, x, y, piece_size)

        # 选中提示（发光环）
        if self.selected_piece:
            row, col = self.selected_piece
            x, y = cell_pos(row, col)
            r = piece_size / 2
            glow = QRadialGradient(x, y, r * 1.2)
            glow.setColorAt(0, QColor(255, 210, 60, 0))
            glow.setColorAt(0.8, QColor(255, 210, 60, 60))
            glow.setColorAt(1, QColor(255, 180, 30, 220))
            painter.setBrush(QBrush(glow))
            painter.setPen(QPen(QColor(255, 200, 40), 2.5))
            painter.drawEllipse(int(x - r), int(y - r), int(piece_size), int(piece_size))

        # 合法走法提示（绿点 + 可吃子红圈）
        for to_row, to_col in self.valid_moves:
            x, y = cell_pos(to_row, to_col)
            if self.board.get_piece(to_row, to_col):
                # 可吃子：红色环
                painter.setPen(QPen(QColor(255, 80, 60), 2.5))
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(int(x - piece_size/2), int(y - piece_size/2),
                                   int(piece_size), int(piece_size))
            else:
                painter.setBrush(QColor(60, 200, 90, 200))
                painter.setPen(Qt.NoPen)
                dot = piece_size * 0.22
                painter.drawEllipse(int(x - dot/2), int(y - dot/2),
                                   int(dot), int(dot))
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() != Qt.LeftButton:
            return
        
        # 获取点击坐标并转换为棋盘坐标（与 paintEvent 保持一致，含立体边框）
        widget_width = self.width()
        widget_height = self.height()

        total_w = self.board_width + self.frame_size * 2
        total_h = self.board_height + self.frame_size * 2
        scale_x = widget_width / total_w
        scale_y = widget_height / total_h
        scale = min(scale_x, scale_y, 2.0)

        offset_x = (widget_width - total_w * scale) // 2
        offset_y = (widget_height - total_h * scale) // 2

        click_x = event.x() - offset_x
        click_y = event.y() - offset_y

        # 转换为棋盘格子坐标（去掉 frame 偏移）
        col = int((click_x / scale - self.frame_size - self.padding) / self.cell_size - 0.5)
        row = int((click_y / scale - self.frame_size - self.padding) / self.cell_size - 0.5)
        
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
        """AI 走棋 - 使用对应难度的 AI 引擎"""
        board = self.board_widget.board
        color = self.board_widget.ai_color
        move = self.ai.get_best_move(board, color)

        if move:
            from_row, from_col, to_row, to_col = move
            self.board_widget.make_move(from_row, from_col, to_row, to_col)
            if not self._check_game_over():
                self.board_widget.start_timer('red')

    def _check_game_over(self):
        """检查游戏是否结束（将死 / 将军 / 老将被抓）"""
        board = self.board_widget.board
        winner, _reason = Rules.is_game_over(board)
        if winner is not None:
            winner_cn = '红方' if winner == 'red' else '黑方'
            self.status_label.setText(f"游戏结束！{winner_cn}获胜！")
            QMessageBox.information(self, "游戏结束", f"{winner_cn}获胜！")
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