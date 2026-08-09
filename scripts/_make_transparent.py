#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把棋子图处理为干净透明背景：
1) floodfill 去掉四角浅色背景（粗阈值）
2) 再叠加一个以图中心、半径 R 的圆形硬遮罩，圆外 100% 透明
   —— 彻底消除圆盘外的任何残留白边/投影，绝不盖住棋盘线。
"""
import sys, os
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_clean_alpha(src_path, radius_ratio=0.335, flood_thresh=60):
    im = Image.open(src_path).convert('RGBA')
    w, h = im.size
    # 1) floodfill 粗略去背景
    try:
        ImageDraw.floodfill(im, (0, 0), (0, 0, 0, 0), thresh=flood_thresh)
        for seed in [(w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
            ImageDraw.floodfill(im, seed, (0, 0, 0, 0), thresh=flood_thresh)
    except Exception:
        pass
    # 2) 圆形硬遮罩：圆内保留（与原图取交集），圆外透明
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    cx, cy = w // 2, h // 2
    r = int(min(w, h) * radius_ratio)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    # 用遮罩限制 alpha：圆外变 0
    px = im.load()
    mx = mask.load()
    for y in range(h):
        for x in range(w):
            if mx[x, y] == 0:
                px[x, y] = (0, 0, 0, 0)
    return im


def main():
    if len(sys.argv) > 1:
        targets = [sys.argv[1]]
    else:
        pieces = os.path.join(BASE, 'assets', 'pieces')
        targets = [os.path.join(pieces, f) for f in sorted(os.listdir(pieces))
                   if f.endswith('.png')]
    for p in targets:
        out = make_clean_alpha(p)
        out.save(p, 'PNG', optimize=True)
        print('clean:', os.path.basename(p), os.path.getsize(p) // 1024, 'KB')


if __name__ == '__main__':
    main()
