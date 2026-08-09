#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 单元测试（更新版）
"""

import unittest
from engine.rules import Board, Rules
from engine.ai import AI
from data.endgames import list_endgames, get_endgame
from engine.sound import SoundManager


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.reset()
    
    def test_initial_board(self):
        red_pieces = self.board.get_all_pieces('red')
        black_pieces = self.board.get_all_pieces('black')
        self.assertEqual(len(red_pieces), 16)
        self.assertEqual(len(black_pieces), 16)
    
    def test_get_piece(self):
        piece = self.board.get_piece(9, 0)
        self.assertIsNotNone(piece)
        self.assertEqual(piece['type'], 'R')
        self.assertEqual(piece['color'], 'red')
    
    def test_find_king(self):
        self.assertEqual(self.board.find_king('red'), (9, 4))
        self.assertEqual(self.board.find_king('black'), (0, 4))
    
    def test_move_piece(self):
        captured = self.board.move_piece(9, 0, 8, 0)
        self.assertIsNone(captured)
        piece = self.board.get_piece(8, 0)
        self.assertEqual(piece['type'], 'R')


class TestRules(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.reset()
    
    def test_get_all_moves_red(self):
        moves = Rules.get_all_moves(self.board, 'red', check_check=True)
        self.assertGreater(len(moves), 0)
        self.assertEqual(len(moves), 44)
    
    def test_get_all_moves_black(self):
        moves = Rules.get_all_moves(self.board, 'black', check_check=True)
        self.assertGreater(len(moves), 0)
    
    def test_is_not_check_initial(self):
        self.assertFalse(Rules._is_king_in_check(self.board, 'red'))
        self.assertFalse(Rules._is_king_in_check(self.board, 'black'))
    
    def test_is_not_checkmate_initial(self):
        self.assertFalse(Rules.is_checkmate(self.board, 'red'))
        self.assertFalse(Rules.is_checkmate(self.board, 'black'))
    def test_knight_cannot_capture_own_piece(self):
        """防回归：马不能移动到有己方棋子的格子（修复前的死代码 bug）"""
        # 构造：红马(0,4)旁边放红兵(1,2)，马应能跳到(2,3)/(1,2)?
        # 实际跳日字：从(0,4)可达 (2,3),(2,5),(1,2),(1,6)。(1,2)放红兵应被排除
        board = Board()
        board.reset()
        # 清空，手动摆
        board.board = [[None for _ in range(9)] for _ in range(10)]
        board.set_piece(0, 4, {'type': 'N', 'color': 'red'})
        board.set_piece(1, 2, {'type': 'P', 'color': 'red'})  # 己方兵，马不能跳到这
        moves = Rules._get_knight_moves(board, 0, 4)
        self.assertNotIn((1, 2), moves)
        # 敌方兵则可吃
        board.set_piece(1, 2, {'type': 'P', 'color': 'black'})
        moves = Rules._get_knight_moves(board, 0, 4)
        self.assertIn((1, 2), moves)

    def test_get_valid_moves_public_api(self):
        """防回归：残局/GUI 调用的 Rules.get_valid_moves 必须存在且返回目标点"""
        board = Board()
        board.reset()
        # 红炮在 (7,1) 的合法目标点（不校验将军）
        moves = Rules.get_valid_moves(board, 7, 1)
        self.assertIsInstance(moves, list)
        self.assertGreater(len(moves), 0)
        # 每个元素应是 (to_row, to_col) 二元组
        for m in moves:
            self.assertEqual(len(m), 2)

    def test_king_in_check_reverse_scan(self):
        """防回归：反向扫描的将军检测与全盘语义一致，且覆盖将帅对脸"""
        # 场景1：黑车直线将军红帅
        board = Board()
        board.board = [[None for _ in range(9)] for _ in range(10)]
        board.set_piece(9, 4, {'type': 'K', 'color': 'red'})
        board.set_piece(0, 4, {'type': 'K', 'color': 'black'})
        board.set_piece(5, 4, {'type': 'R', 'color': 'black'})  # 同一列，红帅被将军
        self.assertTrue(Rules._is_king_in_check(board, 'red'))
        # 中间加个挡子，将军解除
        board.set_piece(7, 4, {'type': 'P', 'color': 'red'})
        self.assertFalse(Rules._is_king_in_check(board, 'red'))
        # 将帅对脸（中间无子）
        board2 = Board()
        board2.board = [[None for _ in range(9)] for _ in range(10)]
        board2.set_piece(9, 4, {'type': 'K', 'color': 'red'})
        board2.set_piece(0, 4, {'type': 'K', 'color': 'black'})
        self.assertTrue(Rules._is_king_in_check(board2, 'red'))


class TestAI(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.reset()
    
    def test_easy_ai(self):
        ai = AI(difficulty='easy')
        move = ai.get_best_move(self.board, 'red')
        self.assertIsNotNone(move)
        self.assertEqual(len(move), 4)
    
    def test_medium_ai(self):
        ai = AI(difficulty='medium')
        move = ai.get_best_move(self.board, 'red')
        self.assertIsNotNone(move)
    
    def test_hard_ai(self):
        ai = AI(difficulty='hard')
        move = ai.get_best_move(self.board, 'red')
        self.assertIsNotNone(move)
    
    def test_expert_ai(self):
        ai = AI(difficulty='expert')
        move = ai.get_best_move(self.board, 'red')
        self.assertIsNotNone(move)

    def test_easy_ai_never_leaves_self_in_check(self):
        """防回归：初级 AI 不能走出让自己被将军的废步"""
        board = self.board.copy()  # 用副本推进，不污染原局
        ai = AI(difficulty='easy')
        for _ in range(20):
            move = ai.get_best_move(board, 'red')
            self.assertIsNotNone(move)
            fr, fc, tr, tc = move
            board.move_piece(fr, fc, tr, tc)
            self.assertFalse(Rules._is_king_in_check(board, 'red', raw=True))
            # 黑方走一步合法棋，维持推进
            bm = Rules.get_all_moves(board, 'black', check_check=True)
            if not bm:
                break
            bfr, bfc, btr, btc = bm[0]
            board.move_piece(bfr, bfc, btr, btc)


class TestEndgames(unittest.TestCase):
    def test_list_endgames(self):
        endgames = list_endgames()
        self.assertGreater(len(endgames), 0)
    
    def test_get_endgame(self):
        endgame = get_endgame(1)
        self.assertIsNotNone(endgame)
        self.assertEqual(endgame['name'], '单车破士')
    
    def test_get_endgame_not_found(self):
        endgame = get_endgame(999)
        self.assertIsNone(endgame)
    
    def test_endgame_count(self):
        self.assertEqual(len(list_endgames()), 12)


class TestSound(unittest.TestCase):
    def test_sound_manager(self):
        sound_mgr = SoundManager()
        self.assertIsInstance(sound_mgr, SoundManager)
        # 在无音频设备环境下，音效模块应该能正常初始化（只是不加载音效）
        self.assertTrue(hasattr(sound_mgr, 'play_move'))
        self.assertTrue(hasattr(sound_mgr, 'play_capture'))


if __name__ == '__main__':
    unittest.main(verbosity=2)