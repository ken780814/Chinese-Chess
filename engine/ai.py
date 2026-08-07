#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 AI 引擎
实现不同难度级别的 AI
"""

import random
from engine.rules import Board, Rules


class AI:
    """AI 基类"""
    
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.search_depth = self._get_search_depth()
    
    def _get_search_depth(self):
        """根据难度返回搜索深度"""
        depths = {
            'easy': 1,
            'medium': 2,
            'hard': 3,
            'expert': 4
        }
        return depths.get(self.difficulty, 2)
    
    def get_best_move(self, board, color):
        """获取最佳走法"""
        if self.difficulty == 'easy':
            return self._easy_move(board, color)
        elif self.difficulty == 'medium':
            return self._minimax_move(board, color, depth=2)
        elif self.difficulty == 'hard':
            return self._minimax_move(board, color, depth=3)
        elif self.difficulty == 'expert':
            return self._minimax_move(board, color, depth=4)
        else:
            return self._minimax_move(board, color, depth=2)
    
    def _easy_move(self, board, color):
        """初级 AI - 随机走法"""
        all_moves = []
        for row in range(10):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece and piece['color'] == color:
                    moves = Rules.get_valid_moves(board, row, col)
                    for to_row, to_col in moves:
                        all_moves.append((row, col, to_row, to_col))
        
        if all_moves:
            return random.choice(all_moves)
        return None
    
    def _minimax_move(self, board, color, depth):
        """中级及以上 AI - Minimax + α-β 剪枝"""
        best_score = float('-inf')
        best_move = None
        
        alpha = float('-inf')
        beta = float('inf')
        
        all_moves = self._get_all_moves(board, color)
        
        for move in all_moves:
            from_row, from_col, to_row, to_col = move
            
            # 模拟走法
            temp_board = Board()
            temp_board.board = [row[:] for row in board.board]
            temp_board.move_piece(from_row, from_col, to_row, to_col)
            
            # 调用 minimax
            score = self._minimax(temp_board, depth - 1, alpha, beta, False, color)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # 剪枝
        
        return best_move
    
    def _minimax(self, board, depth, alpha, beta, is_maximizing, player_color):
        """Minimax 算法"""
        if depth == 0:
            return self._evaluate_board(board, player_color)
        
        enemy_color = 'black' if player_color == 'red' else 'red'
        
        if is_maximizing:
            max_score = float('-inf')
            moves = self._get_all_moves(board, player_color)
            
            for move in moves:
                from_row, from_col, to_row, to_col = move
                temp_board = Board()
                temp_board.board = [row[:] for row in board.board]
                temp_board.move_piece(from_row, from_col, to_row, to_col)
                
                score = self._minimax(temp_board, depth - 1, alpha, beta, False, player_color)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            
            return max_score
        else:
            min_score = float('inf')
            moves = self._get_all_moves(board, enemy_color)
            
            for move in moves:
                from_row, from_col, to_row, to_col = move
                temp_board = Board()
                temp_board.board = [row[:] for row in board.board]
                temp_board.move_piece(from_row, from_col, to_row, to_col)
                
                score = self._minimax(temp_board, depth - 1, alpha, beta, True, player_color)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            
            return min_score
    
    def _get_all_moves(self, board, color):
        """获取指定颜色的所有合法走法"""
        all_moves = []
        for row in range(10):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece and piece['color'] == color:
                    moves = Rules.get_valid_moves(board, row, col)
                    for to_row, to_col in moves:
                        all_moves.append((row, col, to_row, to_col))
        return all_moves
    
    def _evaluate_board(self, board, player_color):
        """评估棋盘分数"""
        # 棋子价值
        piece_values = {
            'K': 10000,
            'R': 900,
            'C': 450,
            'N': 400,
            'B': 200,
            'A': 200,
            'P': 100
        }
        
        score = 0
        for row in range(10):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece:
                    value = piece_values.get(piece['type'], 0)
                    if piece['color'] == player_color:
                        score += value
                        # 位置加成
                        score += self._position_bonus(piece, row, col)
                    else:
                        score -= value
        
        return score
    
    def _position_bonus(self, piece, row, col):
        """位置加成"""
        bonus = 0
        piece_type = piece['type']
        color = piece['color']
        
        if piece_type == 'P':
            # 兵过河后价值更高
            if color == 'red' and row < 5:
                bonus += 50
            elif color == 'black' and row > 4:
                bonus += 50
            # 靠近对方底线价值更高
            if color == 'red' and row < 3:
                bonus += 30
            elif color == 'black' and row > 6:
                bonus += 30
        
        return bonus


if __name__ == '__main__':
    # 测试代码
    from engine.rules import Board
    
    board = Board()
    board.reset()
    
    ai = AI(difficulty='easy')
    move = ai.get_best_move(board, 'red')
    print(f"Easy AI 推荐走法: {move}")
    
    ai = AI(difficulty='medium')
    move = ai.get_best_move(board, 'red')
    print(f"Medium AI 推荐走法: {move}")
