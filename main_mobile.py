#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 移动端版本 (Android/iOS)
基于 Kivy 框架，支持触屏操作
"""

import sys
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle, Text
from kivy.clock import Clock
from kivy.config import Config

# 设置高 DPI 支持
Config.set('graphics', 'multisamples', '0')

# 导入游戏引擎
sys.path.insert(0, os.path.dirname(__file__))
from engine.rules import Board, Rules
from engine.ai import AI
from engine.sound import SoundManager


class ChessBoardWidget(BoxLayout):
    """象棋棋盘组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.board = Board()
        self.board.reset()
        
        self.selected_piece = None
        self.valid_moves = []
        
        self.player_color = 'red'
        self.ai_color = 'black'
        self.difficulty = 'medium'
        self.ai = AI(difficulty=self.difficulty)
        
        self.time_limit = 60
        self.red_time = self.time_limit
        self.black_time = self.time_limit
        self.current_timer = None
        
        self.sound_mgr = SoundManager()
        
        # 自适应计算
        self._calculate_layout()
        
        self.setup_ui()
        self.bind(size=self._on_resize)
        self.bind(pos=self._on_resize)
    
    def _calculate_layout(self):
        """计算布局参数"""
        # 获取窗口大小
        width, height = Window.size
        
        # 棋盘区域
        self.padding = width * 0.05
        self.cell_size = (width - 2 * self.padding) / 8
    
    def _on_resize(self, *args):
        """窗口大小改变时重新计算"""
        self._calculate_layout()
        self.board_widget.update()
    
    def setup_ui(self):
        """设置界面"""
        # 顶部控制面板
        top_layout = BoxLayout(size_hint_y=0.12)
        
        self.difficulty_label = Label(text='难度: 中级', size_hint_x=0.3)
        self.difficulty_btn = Button(text='难度', size_hint_x=0.2)
        self.difficulty_btn.bind(on_press=self._show_difficulty_menu)
        
        self.restart_btn = Button(text='重新开始', size_hint_x=0.3)
        self.restart_btn.bind(on_press=self.restart_game)
        
        top_layout.add_widget(self.difficulty_label)
        top_layout.add_widget(self.difficulty_btn)
        top_layout.add_widget(self.restart_btn)
        
        self.add_widget(top_layout)
        
        # 棋盘区域
        self.board_widget = BoardCanvas(self)
        self.board_widget.size_hint_y = 0.73
        self.add_widget(self.board_widget)
        
        # 底部信息栏
        bottom_layout = BoxLayout(size_hint_y=0.15)
        
        self.red_time_label = Label(
            text=f'红方: {self.red_time}s', 
            size_hint_x=0.5,
            halign='center',
            valign='middle'
        )
        self.black_time_label = Label(
            text=f'黑方: {self.black_time}s', 
            size_hint_x=0.5,
            halign='center',
            valign='middle'
        )
        
        bottom_layout.add_widget(self.red_time_label)
        bottom_layout.add_widget(self.black_time_label)
        
        self.add_widget(bottom_layout)
    
    def _show_difficulty_menu(self, instance):
        """显示难度选择菜单"""
        dropdown = DropDown()
        
        difficulties = [
            ('easy', '初级'),
            ('medium', '中级'),
            ('hard', '高级'),
            ('expert', '终极高手')
        ]
        
        for value, text in difficulties:
            btn = Button(text=text, size_hint_y=None, height=44)
            btn.bind(on_press=lambda btn, v=value: self._set_difficulty(v))
            dropdown.add_widget(btn)
        
        dropdown.open(instance)
    
    def _set_difficulty(self, difficulty):
        """设置难度"""
        self.difficulty = difficulty
        self.ai = AI(difficulty=difficulty)
        diff_names = {'easy': '初级', 'medium': '中级', 'hard': '高级', 'expert': '终极高手'}
        self.difficulty_label.text = f'难度: {diff_names[difficulty]}'
    
    def restart_game(self):
        """重新开始游戏"""
        self.board.reset()
        self.selected_piece = None
        self.valid_moves = []
        self.red_time = self.time_limit
        self.black_time = self.time_limit
        self.red_time_label.text = f'红方: {self.red_time}s'
        self.black_time_label.text = f'黑方: {self.black_time}s'
        self.current_timer = None
        self.sound_mgr.play_game_start()
        self.board_widget.update()
        self._start_timer('red')
    
    def _start_timer(self, color):
        """启动计时器"""
        if self.current_timer:
            Clock.unschedule(self._timer_callback)
        
        self.current_timer = color
        
        def update_timer(dt):
            if self.current_timer == 'red':
                self.red_time -= 1
                self.red_time_label.text = f'红方: {self.red_time}s'
                if self.red_time <= 0:
                    self.sound_mgr.play_timeout()
                    self._show_dialog('超时', '红方超时，黑方获胜！')
                    self.current_timer = None
            elif self.current_timer == 'black':
                self.black_time -= 1
                self.black_time_label.text = f'黑方: {self.black_time}s'
                if self.black_time <= 0:
                    self.sound_mgr.play_timeout()
                    self._show_dialog('超时', '黑方超时，红方获胜！')
                    self.current_timer = None
        
        self._timer_callback = update_timer
        Clock.schedule_interval(update_timer, 1.0)
    
    def _show_dialog(self, title, message):
        """显示对话框"""
        from kivy.uix.dialog import Dialog
        from kivy.uix.boxlayout import BoxLayout
        
        box = BoxLayout(orientation='vertical', padding=20, spacing=10)
        box.add_widget(Label(text=message, size_hint_y=None, height=50))
        
        close_btn = Button(text='确定', size_hint_y=None, height=44)
        close_btn.bind(on_press=lambda x: dialog.dismiss())
        box.add_widget(close_btn)
        
        dialog = Dialog(title=title, content=box, size_hint=(0.8, 0.4))
        dialog.open()
    
    def on_touch_down(self, touch):
        """处理触摸事件"""
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        
        # 转换坐标到棋盘网格
        board_x = touch.x - self.padding
        board_y = touch.y - self.padding
        
        col = int(board_x / self.cell_size)
        row = int((self.height - self.padding - board_y) / self.cell_size)
        
        if 0 <= row < 10 and 0 <= col < 9:
            self._on_board_tap(row, col)
        
        return True
    
    def _on_board_tap(self, row, col):
        """处理棋盘点击"""
        piece = self.board.get_piece(row, col)
        
        if self.selected_piece is None:
            if piece and piece['color'] == self.player_color:
                self.selected_piece = (row, col)
                self.valid_moves = self._get_valid_moves(row, col)
                self.sound_mgr.play_select()
                self.board_widget.update()
        else:
            if (row, col) in self.valid_moves:
                from_row, from_col = self.selected_piece
                self.make_move(from_row, from_col, row, col)
                self.selected_piece = None
                self.valid_moves = []
                self.board_widget.update()
            elif piece and piece['color'] == self.player_color:
                self.selected_piece = (row, col)
                self.valid_moves = self._get_valid_moves(row, col)
                self.sound_mgr.play_select()
                self.board_widget.update()
            else:
                self.selected_piece = None
                self.valid_moves = []
                self.board_widget.update()
    
    def _get_valid_moves(self, row, col):
        """获取合法走法"""
        moves = Rules.get_all_moves(self.board, self.player_color, check_check=True)
        return [(to_r, to_c) for fr, fc, to_r, to_c in moves if fr == row and fc == col]
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """执行移动"""
        captured = self.board.move_piece(from_row, from_col, to_row, to_col)
        
        if captured:
            self.sound_mgr.play_capture()
        else:
            self.sound_mgr.play_move()
        
        opponent_color = 'black' if self.player_color == 'red' else 'red'
        
        if Rules.is_checkmate(self.board, opponent_color):
            self.sound_mgr.play_checkmate()
            self._show_dialog('游戏结束', f'{self.player_color.capitalize()} 获胜！')
            return
        
        if Rules._is_king_in_check(self.board, opponent_color):
            self.sound_mgr.play_check()
        
        self._start_timer(opponent_color)
        
        # AI 走棋
        Clock.schedule_once(self._ai_think, 0.3)
    
    def _ai_think(self, dt):
        """AI 思考"""
        move = self.ai.get_best_move(self.board, self.ai_color)
        if move:
            from_row, from_col, to_row, to_col = move
            self.make_move(from_row, from_col, to_row, to_col)


class BoardCanvas(BoxLayout):
    """棋盘画布"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        
        from kivy.canvas import Canvas
        from kivy.graphics import Callback
        
        with self.canvas:
            self.draw_callback = Callback(self._draw_board)
        
        self.bind(pos=self._update_rect)
        self.bind(size=self._update_rect)
    
    def _update_rect(self, *args):
        """更新画布位置"""
        pass
    
    def _draw_board(self, dt):
        """绘制棋盘"""
        self.canvas.clear()
        
        with self.canvas:
            parent = self.parent
            padding = parent.padding
            cell_size = parent.cell_size
            width = self.width
            height = self.height
            
            # 背景
            Color(0.86, 0.70, 0.37)
            Rectangle(pos=self.pos, size=self.size)
            
            # 棋盘网格
            Color(0.54, 0.27, 0.07)
            
            # 横线
            for i in range(10):
                y = padding + i * cell_size
                Line(points=[padding, y, padding + 8 * cell_size, y])
            
            # 竖线
            for i in range(9):
                x = padding + i * cell_size
                if i == 0 or i == 8:
                    Line(points=[x, padding, x, padding + 9 * cell_size])
                else:
                    Line(points=[x, padding, x, padding + 4 * cell_size])
                    Line(points=[x, padding + 5 * cell_size, x, padding + 9 * cell_size])
            
            # 九宫格斜线
            Line(points=[padding + 3*cell_size, padding + 7*cell_size, 
                        padding + 5*cell_size, padding + 9*cell_size])
            Line(points=[padding + 5*cell_size, padding + 7*cell_size, 
                        padding + 3*cell_size, padding + 9*cell_size])
            
            Line(points=[padding + 3*cell_size, padding, 
                        padding + 5*cell_size, padding + 2*cell_size])
            Line(points=[padding + 5*cell_size, padding, 
                        padding + 3*cell_size, padding + 2*cell_size])
            
            # 楚河汉界
            Text(text='楚 河', pos=[padding + 2*cell_size, padding + 4.3*cell_size], 
                 font_size=cell_size * 0.5)
            Text(text='汉 界', pos=[padding + 5*cell_size, padding + 4.3*cell_size], 
                 font_size=cell_size * 0.5)
            
            # 绘制棋子
            for row in range(10):
                for col in range(9):
                    piece = parent.board.get_piece(row, col)
                    if piece:
                        x = padding + col * cell_size
                        y = padding + row * cell_size
                        self._draw_piece(piece, x, y)
            
            # 选中提示
            if parent.selected_piece:
                row, col = parent.selected_piece
                x = padding + col * cell_size
                y = padding + row * cell_size
                Color(1, 0, 0, 0.5)
                Ellipse(pos=[x-25, y-25], size=[50, 50])
            
            # 合法走法提示
            for to_row, to_col in parent.valid_moves:
                x = padding + to_col * cell_size
                y = padding + to_row * cell_size
                Color(0, 1, 0, 0.5)
                Ellipse(pos=[x-12, y-12], size=[24, 24])
    
    def _draw_piece(self, piece, x, y):
        """绘制棋子"""
        piece_type = piece['type']
        color = piece['color']
        
        # 棋子背景
        if color == 'red':
            Color(0.86, 0.08, 0.24)
        else:
            Color(0.12, 0.12, 0.12)
        
        Ellipse(pos=[x-25, y-25], size=[50, 50])
        
        # 棋子文字
        if color == 'black':
            Color(1, 1, 1)
        else:
            Color(1, 0.85, 0)
        
        piece_names = {
            'K': '将' if color == 'black' else '帅',
            'A': '士' if color == 'black' else '仕',
            'B': '象' if color == 'black' else '相',
            'N': '马' if color == 'black' else '马',
            'R': '车' if color == 'black' else '车',
            'C': '炮' if color == 'black' else '炮',
            'P': '卒' if color == 'black' else '兵',
        }
        
        Text(text=piece_names.get(piece_type, '?'), pos=[x-15, y-10], font_size=20)
    
    def update(self):
        """更新棋盘"""
        self.canvas.clear()
        self._draw_board(0)


class ChineseChessMobileApp(App):
    """中国象棋移动端应用"""
    
    def build(self):
        Window.size = (480, 800)
        self.title = '中国象棋'
        return ChessBoardWidget()


if __name__ == '__main__':
    ChineseChessMobileApp().run()
