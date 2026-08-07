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
        "solution": "车九进九，将4进1，车九退一，将4退1，车九平七，士5退4，车七进一，将4进1，车七退一，将4退1，车七平六"
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
        "solution": "车一平二，士5退6，车二进九，将4进1，车二退一，将4退1，车二平四"
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
        "solution": "马三进四，将4进1，炮五平六，士5进4，马四退六，将4平5，马六进七"
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
        "solution": "车五平六，士5退4，车六进一，将4进1，车六平七，士4进5，车七退一"
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
        "solution": "马三进四，将4进1，马五进七，将4平5，马七退六，将5退1，马四退六"
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


if __name__ == '__main__':
    print("中国象棋残局库")
    print("=" * 40)
    
    for endgame in ENDGAMES:
        print(f"\n{endgame['id']}. {endgame['name']}")
        print(f"   描述: {endgame['description']}")
        print(f"   解法: {endgame['solution'][:50]}...")
