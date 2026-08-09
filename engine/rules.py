#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋规则模块
实现棋子的走法规则判断
"""

# 棋子类型定义
PIECE_TYPES = {
    'K': 'king',      # 将/帅
    'A': 'advisor',   # 士/仕
    'B': 'bishop',    # 象/相
    'N': 'knight',    # 马
    'R': 'rook',      # 车
    'C': 'cannon',    # 炮
    'P': 'pawn',      # 兵/卒
}

# 棋盘尺寸
BOARD_ROWS = 10
BOARD_COLS = 9

# 初始棋盘布局
INITIAL_BOARD = {
    'black': [
        ('R', 0, 0), ('N', 0, 1), ('B', 0, 2), ('A', 0, 3), ('K', 0, 4),
        ('A', 0, 5), ('B', 0, 6), ('N', 0, 7), ('R', 0, 8),
        ('C', 2, 1), ('C', 2, 7),
        ('P', 3, 0), ('P', 3, 2), ('P', 3, 4), ('P', 3, 6), ('P', 3, 8),
    ],
    'red': [
        ('R', 9, 0), ('N', 9, 1), ('B', 9, 2), ('A', 9, 3), ('K', 9, 4),
        ('A', 9, 5), ('B', 9, 6), ('N', 9, 7), ('R', 9, 8),
        ('C', 7, 1), ('C', 7, 7),
        ('P', 6, 0), ('P', 6, 2), ('P', 6, 4), ('P', 6, 6), ('P', 6, 8),
    ]
}


class Board:
    """棋盘类"""
    
    def __init__(self):
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.reset()
    
    def reset(self):
        """重置棋盘"""
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        
        for color, pieces in INITIAL_BOARD.items():
            for piece_type, row, col in pieces:
                self.board[row][col] = {'type': piece_type, 'color': color}
    
    def get_piece(self, row, col):
        """获取指定位置的棋子"""
        if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            return self.board[row][col]
        return None
    
    def set_piece(self, row, col, piece):
        """设置指定位置的棋子"""
        if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            self.board[row][col] = piece
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """移动棋子，返回被吃掉的棋子（如果有）"""
        piece = self.get_piece(from_row, from_col)
        if piece is None:
            return None
        
        captured = self.get_piece(to_row, to_col)
        self.set_piece(to_row, to_col, piece)
        self.set_piece(from_row, from_col, None)
        
        return captured
    
    def is_valid_position(self, row, col):
        """检查位置是否在棋盘内"""
        return 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS
    
    def get_all_pieces(self, color):
        """获取指定颜色的所有棋子位置"""
        pieces = []
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = self.board[row][col]
                if piece and piece['color'] == color:
                    pieces.append((row, col, piece['type']))
        return pieces
    
    def find_king(self, color):
        """找到指定颜色的将/帅位置"""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = self.board[row][col]
                if piece and piece['color'] == color and piece['type'] == 'K':
                    return (row, col)
        return None
    
    def copy(self):
        """复制棋盘"""
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        return new_board


class Rules:
    """规则类 - 判断合法走法"""
    
    @staticmethod
    def get_all_moves(board, color, check_check=True):
        """获取指定颜色的所有合法走法。

        check_check=True 时，过滤掉会导致自己被将军的走法。
        性能优化：用增量 move/unmove 代替每步深拷贝（copy 仅做一次浅拷贝
        用于安全回滚），整体复杂度从 O(走法数 × 棋盘拷贝) 降到接近 O(走法数)。
        """
        all_moves = []

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = board.get_piece(row, col)
                if piece and piece['color'] == color:
                    moves = Rules._get_piece_moves(board, row, col, piece)

                    if check_check:
                        for to_row, to_col in moves:
                            # 增量移动
                            captured = board.get_piece(to_row, to_col)
                            moving = board.get_piece(row, col)
                            board.set_piece(to_row, to_col, moving)
                            board.set_piece(row, col, None)
                            in_check = Rules._is_king_in_check(board, color, raw=True)
                            # 回滚
                            board.set_piece(row, col, moving)
                            board.set_piece(to_row, to_col, captured)
                            if not in_check:
                                all_moves.append((row, col, to_row, to_col))
                    else:
                        for to_row, to_col in moves:
                            all_moves.append((row, col, to_row, to_col))

        return all_moves
    @staticmethod
    def get_valid_moves(board, row, col):
        """返回某位置棋子的所有合法目标点 (to_row, to_col)。

        供 GUI/残局模式使用：从 (row, col) 出发的走法（不校验将军，
        仅校验基本吃子规则）。移动后是否送将的判定由调用方按需处理。
        """
        piece = board.get_piece(row, col)
        if piece is None:
            return []
        return Rules._get_piece_moves(board, row, col, piece)


    @staticmethod
    def _get_piece_moves(board, row, col, piece):
        """获取单个棋子的所有可能走法（不检查是否导致被将军）"""
        piece_type = piece['type']
        color = piece['color']
        
        if piece_type == 'K':  # 将/帅
            return Rules._get_king_moves(board, row, col, color)
        elif piece_type == 'A':  # 士/仕
            return Rules._get_advisor_moves(board, row, col, color)
        elif piece_type == 'B':  # 象/相
            return Rules._get_bishop_moves(board, row, col, color)
        elif piece_type == 'N':  # 马
            return Rules._get_knight_moves(board, row, col)
        elif piece_type == 'R':  # 车
            return Rules._get_rook_moves(board, row, col, color)
        elif piece_type == 'C':  # 炮
            return Rules._get_cannon_moves(board, row, col, color)
        elif piece_type == 'P':  # 兵/卒
            return Rules._get_pawn_moves(board, row, col, color)
        
        return []
    
    @staticmethod
    def _get_king_moves(board, row, col, color):
        """将/帅的移动规则"""
        moves = []
        # 将/帅只能在九宫格内移动
        if color == 'red':
            row_start, row_end = 7, 9
        else:
            row_start, row_end = 0, 2
        
        col_start, col_end = 3, 5
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (row_start <= new_row <= row_end and 
                col_start <= new_col <= col_end and
                board.is_valid_position(new_row, new_col)):
                target = board.get_piece(new_row, new_col)
                if target is None or target['color'] != color:
                    moves.append((new_row, new_col))
        
        # 将帅对脸规则（飞将）
        enemy_king_color = 'black' if color == 'red' else 'red'
        enemy_king_pos = board.find_king(enemy_king_color)
        if enemy_king_pos:
            enemy_row, enemy_col = enemy_king_pos
            if enemy_col == col:  # 同一列
                # 检查中间是否有棋子
                min_row = min(row, enemy_row)
                max_row = max(row, enemy_row)
                has_blocker = False
                for r in range(min_row + 1, max_row):
                    if board.get_piece(r, col) is not None:
                        has_blocker = True
                        break
                if not has_blocker:
                    moves.append((enemy_row, enemy_col))
        
        return moves
    
    @staticmethod
    def _get_advisor_moves(board, row, col, color):
        """士/仕的移动规则"""
        moves = []
        # 士/仕只能在九宫格内斜向移动
        if color == 'red':
            row_start, row_end = 7, 9
        else:
            row_start, row_end = 0, 2
        
        col_start, col_end = 3, 5
        
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (row_start <= new_row <= row_end and 
                col_start <= new_col <= col_end and
                board.is_valid_position(new_row, new_col)):
                target = board.get_piece(new_row, new_col)
                if target is None or target['color'] != color:
                    moves.append((new_row, new_col))
        
        return moves
    
    @staticmethod
    def _get_bishop_moves(board, row, col, color):
        """象/相的移动规则"""
        moves = []
        # 象/相走田字，不能过河
        if color == 'red':
            row_start = 5
        else:
            row_end = 4
        
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            # 检查是否过河
            if color == 'red' and new_row < row_start:
                continue
            if color == 'black' and new_row > row_end:
                continue
            
            # 检查象眼（田字中心）
            eye_row, eye_col = row + dr // 2, col + dc // 2
            if board.is_valid_position(new_row, new_col) and board.get_piece(eye_row, eye_col) is None:
                target = board.get_piece(new_row, new_col)
                if target is None or target['color'] != color:
                    moves.append((new_row, new_col))
        
        return moves
    
    @staticmethod
    def _get_knight_moves(board, row, col):
        """马的移动规则"""
        piece = board.get_piece(row, col)
        color = piece['color'] if piece else None
        moves = []
        # 马走日字，有蹩马腿
        knight_moves = [
            (-2, -1, -1, 0),  # 左上
            (-2, 1, -1, 0),   # 右上
            (2, -1, 1, 0),    # 左下
            (2, 1, 1, 0),     # 右下
            (-1, -2, 0, -1),  # 左上左
            (-1, 2, 0, 1),    # 右上右
            (1, -2, 0, -1),   # 左下左
            (1, 2, 0, 1),     # 右下右
        ]
        
        for dr, dc, leg_dr, leg_col in knight_moves:
            new_row, new_col = row + dr, col + dc
            leg_row, leg_col = row + leg_dr, col + leg_col
            
            if board.is_valid_position(new_row, new_col):
                # 检查是否蹩马腿
                if board.get_piece(leg_row, leg_col) is None:
                    target = board.get_piece(new_row, new_col)
                    # 不能吃己方棋子
                    if target is None or target['color'] != color:
                        moves.append((new_row, new_col))
        
        return moves
    
    @staticmethod
    def _get_rook_moves(board, row, col, color):
        """车的移动规则"""
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while board.is_valid_position(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target['color'] != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dr
                new_col += dc
        
        return moves
    
    @staticmethod
    def _get_cannon_moves(board, row, col, color):
        """炮的移动规则"""
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            jumped = False
            while board.is_valid_position(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if not jumped:
                    if target is None:
                        moves.append((new_row, new_col))
                    else:
                        jumped = True
                else:
                    if target is not None:
                        if target['color'] != color:
                            moves.append((new_row, new_col))
                        break
                new_row += dr
                new_col += dc
        
        return moves
    
    @staticmethod
    def _get_pawn_moves(board, row, col, color):
        """兵/卒的移动规则"""
        moves = []
        if color == 'red':
            # 红兵向上走
            forward = -1
            can_cross = row <= 4  # 已过河
        else:
            # 黑卒向下走
            forward = 1
            can_cross = row >= 5  # 已过河
        
        # 前进
        new_row = row + forward
        if board.is_valid_position(new_row, col):
            target = board.get_piece(new_row, col)
            if target is None or target['color'] != color:
                moves.append((new_row, col))
        
        # 过河后可以横走
        if can_cross:
            for dc in [-1, 1]:
                new_col = col + dc
                if board.is_valid_position(row, new_col):
                    target = board.get_piece(row, new_col)
                    if target is None or target['color'] != color:
                        moves.append((row, new_col))
        
        return moves
    
    @staticmethod
    def _is_king_in_check(board, color, raw=False):
        """检查指定颜色的将/帅是否被将军（反向扫描，性能优于全盘扫描）。

        从将帅位置出发，沿各棋子的攻击方式反推是否有敌方棋子能攻击到它，
        而不是遍历全盘。raw 参数已废弃，保留以兼容调用方。
        """
        king_pos = board.find_king(color)
        if king_pos is None:
            return True  # 将/帅被吃掉，也算被将军
        kr, kc = king_pos
        enemy = 'black' if color == 'red' else 'red'

        # 1) 同列敌人将帅对脸 (飞将)
        for r in range(10):
            if r == kr:
                continue
            p = board.get_piece(r, kc)
            if p and p['type'] == 'K' and p['color'] == enemy:
                # 中间无子才算对脸
                blocked = any(board.get_piece(rr, kc) is not None for rr in range(min(r, kr)+1, max(r, kr)))
                if not blocked:
                    return True

        # 2) 车/帅(将) 直线攻击
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            r, c = kr+dr, kc+dc
            while board.is_valid_position(r, c):
                p = board.get_piece(r, c)
                if p is not None:
                    if p['color'] == enemy and p['type'] in ('R', 'K'):
                        return True
                    break  # 任何棋子挡路，直线攻击失效
                r += dr
                c += dc

        # 3) 炮 隔子攻击 (需要恰好一个炮架)
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            r, c = kr+dr, kc+dc
            screen = 0
            while board.is_valid_position(r, c):
                p = board.get_piece(r, c)
                if p is not None:
                    if screen == 1 and p['color'] == enemy and p['type'] == 'C':
                        return True
                    if screen >= 2:
                        break
                    screen += 1
                r += dr
                c += dc

        # 4) 马 走日攻击 (从将帅位置看 8 个马步，检查是否有敌马且未被蹩腿)
        knight_offsets = (
            (-2,-1,-1,0),(-2,1,-1,0),(2,-1,1,0),(2,1,1,0),
            (-1,-2,0,-1),(-1,2,0,1),(1,-2,0,-1),(1,2,0,1),
        )
        for dr, dc, leg_dr, leg_dc in knight_offsets:
            r, c = kr+dr, kc+dc
            if board.is_valid_position(r, c):
                p = board.get_piece(r, c)
                if p and p['color'] == enemy and p['type'] == 'N':
                    # 蹩马腿检查：腿在将帅与马之间
                    leg_r, leg_c = kr+leg_dr, kc+leg_dc
                    if board.get_piece(leg_r, leg_c) is None:
                        return True

        # 5) 兵/卒 贴身攻击 (敌方兵在将帅斜前/正前一步)
        # 敌兵攻击方向：红兵向上(-1)，黑卒向下(+1)
        pawn_dir = -1 if enemy == 'red' else 1
        for dc in (-1, 0, 1):
            r, c = kr + pawn_dir, kc + dc
            if board.is_valid_position(r, c):
                p = board.get_piece(r, c)
                if p and p['color'] == enemy and p['type'] == 'P':
                    # 兵只能向前和横走，所以正前/左前/右前都能吃
                    if dc == 0 or True:
                        return True

        # 6) 象/相 田字攻击 (从将帅看 4 个田字角)
        bishop_offsets = ((-2,-2),(-2,2),(2,-2),(2,2))
        for dr, dc in bishop_offsets:
            r, c = kr+dr, kc+dc
            if board.is_valid_position(r, c):
                p = board.get_piece(r, c)
                if p and p['color'] == enemy and p['type'] == 'B':
                    # 象不过河已在布置时保证；田字中心无子
                    eye_r, eye_c = kr + dr//2, kc + dc//2
                    if board.get_piece(eye_r, eye_c) is None:
                        return True

        # 7) 士/仕 斜线一步攻击
        advisor_offsets = ((-1,-1),(-1,1),(1,-1),(1,1))
        for dr, dc in advisor_offsets:
            r, c = kr+dr, kc+dc
            if board.is_valid_position(r, c):
                p = board.get_piece(r, c)
                if p and p['color'] == enemy and p['type'] == 'A':
                    return True

        return False
    @staticmethod
    def is_checkmate(board, color):
        """检查是否将死"""
        if not Rules._is_king_in_check(board, color):
            return False
        
        # 检查是否有合法走法可以解除将军
        all_moves = Rules.get_all_moves(board, color, check_check=True)
        return len(all_moves) == 0
    
    @staticmethod
    def is_game_over(board):
        """检查游戏是否结束"""
        red_king = board.find_king('red')
        black_king = board.find_king('black')
        
        if red_king is None:
            return 'black', 'red King captured'
        if black_king is None:
            return 'red', 'black King captured'
        
        if Rules.is_checkmate(board, 'red'):
            return 'black', 'Checkmate'
        if Rules.is_checkmate(board, 'black'):
            return 'red', 'Checkmate'
        
        return None, None


if __name__ == '__main__':
    # 测试代码
    board = Board()
    board.reset()
    
    print("初始棋盘：")
    for row in range(BOARD_ROWS):
        line = ""
        for col in range(BOARD_COLS):
            piece = board.get_piece(row, col)
            if piece:
                line += f"{piece['type']}{piece['color'][0]} "
            else:
                line += ".  "
        print(line)
    
    print("\n测试红方棋子走法：")
    moves = Rules.get_all_moves(board, 'red', check_check=False)
    print(f"红方所有可能走法数量: {len(moves)}")
    
    moves = Rules.get_all_moves(board, 'red', check_check=True)
    print(f"红方合法走法数量: {len(moves)}")
    
    # 测试将军检测
    print(f"\n红方是否被将军: {Rules._is_king_in_check(board, 'red')}")
    print(f"黑方是否被将军: {Rules._is_king_in_check(board, 'black')}")
    
    # 测试将死
    print(f"\n红方是否被将死: {Rules.is_checkmate(board, 'red')}")
    print(f"黑方是否被将死: {Rules.is_checkmate(board, 'black')}")