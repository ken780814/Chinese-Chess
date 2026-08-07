#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 性能基准测试
"""

import time
from engine.rules import Board, Rules
from engine.ai import AI


def benchmark_rules():
    """基准测试规则模块"""
    board = Board()
    board.reset()
    
    start = time.time()
    for _ in range(100):
        moves = Rules.get_all_moves(board, 'red', check_check=True)
    elapsed = time.time() - start
    
    print(f"规则模块: 100次计算共 {elapsed:.3f}s")
    print(f"  平均每次: {elapsed/100*1000:.2f}ms")
    print(f"  走法数量: {len(moves)}")


def benchmark_ai():
    """基准测试AI模块"""
    board = Board()
    board.reset()
    
    for difficulty in ['easy', 'medium', 'hard', 'expert']:
        ai = AI(difficulty=difficulty)
        
        start = time.time()
        move = ai.get_best_move(board, 'red')
        elapsed = time.time() - start
        
        print(f"AI ({difficulty}): {elapsed:.3f}s, 推荐走法: {move}")


def benchmark_endgames():
    """基准测试残局加载"""
    from data.endgames import list_endgames
    
    start = time.time()
    for _ in range(1000):
        endgames = list_endgames()
    elapsed = time.time() - start
    
    print(f"残局加载: 1000次共 {elapsed:.3f}s")
    print(f"  平均每次: {elapsed/1000*1000000:.2f}μs")
    print(f"  残局数量: {len(endgames)}")


if __name__ == '__main__':
    print("=" * 50)
    print("中国象棋性能基准测试")
    print("=" * 50)
    
    benchmark_rules()
    print()
    benchmark_ai()
    print()
    benchmark_endgames()
    
    print("\n" + "=" * 50)
    print("测试完成")
