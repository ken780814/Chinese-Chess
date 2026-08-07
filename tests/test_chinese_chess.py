#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 单元测试
测试规则、AI和残局模块
"""

import unittest
from engine.rules import Board, Rules
from engine.ai import AI
from data.endgames import list_endgames, get_endgame


class TestBoard(unittest.TestCase):
    """棋盘测试"""
    
    def setUp(self):
        self.board = Board()
        self.board.reset()
    
    def test_initial_board(self):
        """测试初始棋盘布局"""
        # 红方应该有32个棋子
        red_pieces = self.board.get_all_pieces('red')
        black_pieces = self.board.get_all_pieces('black')
        
        self.assertEqual(len(red_pieces), 16, "红方应该有16个棋子")
        self.assertEqual(len(black_pieces), 16, "黑方应该有16个棋子")
    
    def test_get_piece(self):
        """测试获取棋子"""
        piece = self.board.get_piece(9, 0)
        self.assertIsNotNone(piece)
        self.assertEqual(piece['type'], 'R')
        self.assertEqual(piece['color'], 'red')
    
    def test_invalid_position(self):
        """测试无效位置"""
        piece = self.board.get_piece(-1, 0)
        self.assertIsNone(piece)
        
        piece = self.board.get_piece(10, 0)
        self.assertIsNone(piece)
    
    def test_move_piece(self):
        """测试移动棋子"""
        captured = self.board.move_piece(9, 0, 8, 0)
        self.assertIsNone(captured)
        
        piece = self.board.get_piece(8, 0)
        self.assertEqual(piece['type'], 'R')
        self.assertEqual(piece['color'], 'red')
    
    def test_find_king(self):
        """测试寻找将/帅"""
        red_king = self.board.find_king('red')
        black_king = self.board.find_king('black')
        
        self.assertEqual(red_king, (9, 4), "红帅应该在(9, 4)")
        self.assertEqual(black_king, (0, 4), "黑将应该在(0, 4)")


class TestRules(unittest.TestCase):
    """规则测试"""
    
    def setUp(self):
        self.board = Board()
        self.board.reset()
    
    def test_get_all_moves_red(self):
        """测试红方走法"""
        moves = Rules.get_all_moves(self.board, 'red', check_check=True)
        self.assertGreater(len(moves), 0, "红方应该有合法走法")
        self.assertEqual(len(moves), 44, "初始局面红方应该有44种合法走法")
    
    def test_get_all_moves_black(self):
        """测试黑方走法"""
        moves = Rules.get_all_moves(self.board, 'black', check_check=True)
        self.assertGreater(len(moves), 0, "黑方应该有合法走法")
    
    def test_king_can_move(self):
        """测试将/帅可以移动"""
        moves = Rules.get_all_moves(self.board, 'red', check_check=False)
        
        # 找到帅的走法
        king_moves = [m for m in moves if self.board.get_piece(m[0], m[1])['type'] == 'K']
        self.assertGreater(len(king_moves), 0, "帅应该有合法走法")
    
    def test_rook_can_move(self):
        """测试车可以移动"""
        moves = Rules.get_all_moves(self.board, 'red', check_check=False)
        
        # 找到车的走法
        rook_moves = [m for m in moves if self.board.get_piece(m[0], m[1])['type'] == 'R']
        self.assertGreater(len(rook_moves), 0, "车应该有合法走法")
    
    def test_is_not_check_initial(self):
        """测试初始局面不被将军"""
        self.assertFalse(Rules._is_king_in_check(self.board, 'red'))
        self.assertFalse(Rules._is_king_in_check(self.board, 'black'))
    
    def test_is_not_checkmate_initial(self):
        """测试初始局面不是将死"""
        self.assertFalse(Rules.is_checkmate(self.board, 'red'))
        self.assertFalse(Rules.is_checkmate(self.board, 'black'))


class TestAI(unittest.TestCase):
    """AI测试"""
    
    def setUp(self):
        self.board = Board()
        self.board.reset()
    
    def test_easy_ai(self):
        """测试初级AI"""
        ai = AI(difficulty='easy')
        move = ai.get_best_move(self.board, 'red')
        self.assertIsNotNone(move, "Easy AI应该返回一个走法")
        self.assertEqual(len(move), 4, "走法应该包含4个坐标")
    
    def test_medium_ai(self):
        """测试中级AI"""
        ai = AI(difficulty='medium')
        move = ai.get_best_move(self.board, 'red')
        self.assertIsNotNone(move, "Medium AI应该返回一个走法")
    
    def test_hard_ai(self):
        """测试高级AI"""
        ai = AI(difficulty='hard')
        move = ai.get_best_move(self.board, 'red')
        self.assertIsNotNone(move, "Hard AI应该返回一个走法")
    
    def test_expert_ai(self):
        """测试终极AI"""
        ai = AI(difficulty='expert')
        move = ai.get_best_move(self.board, 'red')
        self.assertIsNotNone(move, "Expert AI应该返回一个走法")


class TestEndgames(unittest.TestCase):
    """残局测试"""
    
    def test_list_endgames(self):
        """测试残局列表"""
        endgames = list_endgames()
        self.assertGreater(len(endgames), 0, "残局库应该不为空")
    
    def test_get_endgame(self):
        """测试获取单个残局"""
        endgame = get_endgame(1)
        self.assertIsNotNone(endgame)
        self.assertEqual(endgame['name'], '单车破士')
    
    def test_get_endgame_not_found(self):
        """测试不存在的残局"""
        endgame = get_endgame(999)
        self.assertIsNone(endgame)
    
    def test_endgame_pieces(self):
        """测试残局棋子数量"""
        endgame = get_endgame(1)
        self.assertEqual(len(endgame['pieces']), 4, "单车破士应该有4个棋子")


class TestPositionBonus(unittest.TestCase):
    """位置评估测试"""
    
    def test_pawn_bonus(self):
        """测试兵的过河加分"""
        board = Board()
        board.reset()
        
        ai = AI(difficulty='medium')
        
        # 红兵在初始位置
        piece = {'type': 'P', 'color': 'red', 'row': 6, 'col': 0}
        bonus = ai._position_bonus(piece, 6, 0)
        self.assertEqual(bonus, 0, "未过河的兵不应有加分")
        
        # 红兵过河
        piece = {'type': 'P', 'color': 'red', 'row': 4, 'col': 0}
        bonus = ai._position_bonus(piece, 4, 0)
        self.assertGreater(bonus, 0, "过河的兵应该有加分")


if __name__ == '__main__':
    unittest.main(verbosity=2)
