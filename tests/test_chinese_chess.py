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
