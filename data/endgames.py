#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋残局数据
包含经典残局布局
"""

ENDGAMES = [
    {
        "id": 1,
        "name": "单车破士",
        "description": "单车对单士，红方先行",
        "fen": "4k3/8/8/8/8/8/8/4K3/r7 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "R", "color": "red", "row": 9, "col": 0},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
        ],
        "solution": "车九进九，将4进1，车九退一，将4退1，车九平七，士5退4，车七进一，将4进1，车七退一，将4退1，车七平六",
        "difficulty": "简单"
    },
    {
        "id": 2,
        "name": "双车挫",
        "description": "双车对士象全",
        "fen": "3k4/8/8/8/8/8/8/3K4/R7 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "R", "color": "red", "row": 9, "col": 0},
            {"type": "R", "color": "red", "row": 8, "col": 1},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
            {"type": "A", "color": "black", "row": 0, "col": 5},
            {"type": "B", "color": "black", "row": 0, "col": 2},
            {"type": "B", "color": "black", "row": 0, "col": 6},
        ],
        "solution": "车一平二，士5退6，车二进九，将4进1，车二退一，将4退1，车二平四",
        "difficulty": "简单"
    },
    {
        "id": 3,
        "name": "马后炮",
        "description": "马炮配合杀局",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "N", "color": "red", "row": 7, "col": 3},
            {"type": "C", "color": "red", "row": 5, "col": 4},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
        ],
        "solution": "马三进四，将4进1，炮五平六，士5进4，马四退六，将4平5，马六进七",
        "difficulty": "中等"
    },
    {
        "id": 4,
        "name": "一车十子寒",
        "description": "单车胜士象全",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "R", "color": "red", "row": 5, "col": 4},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
            {"type": "A", "color": "black", "row": 0, "col": 5},
            {"type": "B", "color": "black", "row": 0, "col": 2},
            {"type": "B", "color": "black", "row": 0, "col": 6},
            {"type": "P", "color": "black", "row": 3, "col": 0},
            {"type": "P", "color": "black", "row": 3, "col": 2},
            {"type": "P", "color": "black", "row": 3, "col": 4},
            {"type": "P", "color": "black", "row": 3, "col": 6},
            {"type": "P", "color": "black", "row": 3, "col": 8},
        ],
        "solution": "车五平六，士5退4，车六进一，将4进1，车六平七，士4进5，车七退一",
        "difficulty": "中等"
    },
    {
        "id": 5,
        "name": "双马饮泉",
        "description": "双马配合杀局",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "N", "color": "red", "row": 6, "col": 3},
            {"type": "N", "color": "red", "row": 6, "col": 5},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
            {"type": "A", "color": "black", "row": 0, "col": 5},
        ],
        "solution": "马三进四，将4进1，马五进七，将4平5，马七退六，将5退1，马四退六",
        "difficulty": "中等"
    },
    {
        "id": 6,
        "name": "车兵临门",
        "description": "车兵配合杀局",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "R", "color": "red", "row": 6, "col": 4},
            {"type": "P", "color": "red", "row": 5, "col": 3},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
            {"type": "A", "color": "black", "row": 0, "col": 5},
        ],
        "solution": "兵三平四，将5平4，车六进三，将4进1，兵四进一",
        "difficulty": "简单"
    },
    {
        "id": 7,
        "name": "炮双兵胜",
        "description": "炮双兵对士象全",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "C", "color": "red", "row": 5, "col": 4},
            {"type": "P", "color": "red", "row": 4, "col": 3},
            {"type": "P", "color": "red", "row": 4, "col": 5},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
            {"type": "A", "color": "black", "row": 0, "col": 5},
            {"type": "B", "color": "black", "row": 0, "col": 2},
            {"type": "B", "color": "black", "row": 0, "col": 6},
        ],
        "solution": "炮五平六，士5进4，兵四平五，将5平4，兵五进一",
        "difficulty": "中等"
    },
    {
        "id": 8,
        "name": "马兵胜士象",
        "description": "马兵对士象全",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "N", "color": "red", "row": 5, "col": 4},
            {"type": "P", "color": "red", "row": 4, "col": 4},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
            {"type": "A", "color": "black", "row": 0, "col": 5},
            {"type": "B", "color": "black", "row": 0, "col": 2},
            {"type": "B", "color": "black", "row": 0, "col": 6},
        ],
        "solution": "马五进三，将5平4，兵四进一，士5进6，马三退四",
        "difficulty": "困难"
    },
    {
        "id": 9,
        "name": "双炮胜",
        "description": "双炮对单士",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "C", "color": "red", "row": 6, "col": 0},
            {"type": "C", "color": "red", "row": 6, "col": 8},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
        ],
        "solution": "炮二平五，士5退4，炮五进四，士4进5，炮八平五",
        "difficulty": "简单"
    },
    {
        "id": 10,
        "name": "车炮争雄",
        "description": "车炮对车士",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "R", "color": "red", "row": 5, "col": 4},
            {"type": "C", "color": "red", "row": 4, "col": 4},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "R", "color": "black", "row": 2, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
        ],
        "solution": "车五进三，将4进1，炮四进七，士5退6，车五退一",
        "difficulty": "困难"
    },
    {
        "id": 11,
        "name": "三子归边",
        "description": "车马炮配合杀局",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "R", "color": "red", "row": 6, "col": 2},
            {"type": "N", "color": "red", "row": 5, "col": 4},
            {"type": "C", "color": "red", "row": 4, "col": 4},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
            {"type": "A", "color": "black", "row": 0, "col": 5},
        ],
        "solution": "车六进三，将4进1，马五进七，将4平5，炮四进七",
        "difficulty": "困难"
    },
    {
        "id": 12,
        "name": "钓鱼马",
        "description": "马兵胜单士",
        "fen": "3k4/8/8/8/8/8/8/3K4 w - - 0 1",
        "pieces": [
            {"type": "K", "color": "red", "row": 9, "col": 4},
            {"type": "N", "color": "red", "row": 6, "col": 2},
            {"type": "P", "color": "red", "row": 5, "col": 4},
            {"type": "K", "color": "black", "row": 0, "col": 4},
            {"type": "A", "color": "black", "row": 0, "col": 3},
        ],
        "solution": "马二进三，将5平4，兵四平五，士5进6，马三退四",
        "difficulty": "中等"
    }
]


def get_endgame(endgame_id):
    """获取指定残局"""
    for endgame in ENDGAMES:
        if endgame["id"] == endgame_id:
            return endgame
    return None


def list_endgames():
    """列出所有残局"""
    return ENDGAMES


def get_endgames_by_difficulty(difficulty):
    """按难度筛选残局"""
    return [e for e in ENDGAMES if e.get('difficulty') == difficulty]


def get_endgames_by_id_range(start, end):
    """按ID范围获取残局"""
    return [e for e in ENDGAMES if start <= e['id'] <= end]


if __name__ == '__main__':
    print("中国象棋残局库")
    print("=" * 50)
    print(f"共收录 {len(ENDGAMES)} 个残局\n")
    
    for endgame in ENDGAMES:
        print(f"[{endgame['id']}] {endgame['name']} ({endgame['difficulty']})")
        print(f"    描述: {endgame['description']}")
        print(f"    解法: {endgame['solution'][:40]}...")
        print()
    
    # 测试筛选功能
    print("=" * 50)
    print("按难度筛选:")
    for diff in ['简单', '中等', '困难']:
        count = len(get_endgames_by_difficulty(diff))
        print(f"  {diff}: {count} 个")
