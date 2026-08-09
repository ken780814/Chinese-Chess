#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""棋子图美化成干净透明背景，同时保留圆盘立体感：
1) floodfill 粗略去掉四角最远的纯背景
2) 按到图中心的距离做羽化 alpha：
   - r <= R_in  : 完全不透明（圆盘主体，含立体高光环）
   - R_in~R_out : 平滑衰减（保留柔和外发光/边缘过渡，无硬白边）
   - r >= R_out : 全透明
这样圆盘外不再有方形/圆形白底遮挡棋盘线，但棋子仍保持立体。
"""
import sys, os
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_feathered_alpha(src_path, r_in_ratio=0.34, r_out_ratio=0.46, flood_thresh=55):
    im = Image.open(src_path).convert('RGBA')
    w, h = im.size
    cx, cy = w / 2.0, h / 2.0
    R_in = min(w, h) * r_in_ratio
    R_out = min(w, h) * r_out_ratio

    # 1) 粗略去最远的纯背景（四角）
    try:
        ImageDraw.floodfill(im, (0, 0), (0, 0, 0, 0), thresh=flood_thresh)
        for seed in [(w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
            ImageDraw.floodfill(im, seed, (0, 0, 0, 0), thresh=flood_thresh)
    except Exception:
        pass

    px = im.load()
    for y in range(h):
        for x in range(w):
            dx, dy = x - cx, y - cy
            r = (dx * dx + dy * dy) ** 0.5
            if r <= R_in:
                continue  # 保持原 alpha（不透明主体）
            elif r >= R_out:
                px[x, y] = (0, 0, 0, 0)
            else:
                # 平滑衰减 1 -> 0
                t = (r - R_in) / (R_out - R_in)
                a0 = px[x, y][3]
                px[x, y] = (px[x, y][0], px[x, y][1], px[x, y][2],
                            int(a0 * (1.0 - t)))
    return im


def main():
    if len(sys.argv) > 1:
        targets = [sys.argv[1]]
    else:
        pieces = os.path.join(BASE, 'assets', 'pieces')
        targets = [os.path.join(pieces, f) for f in sorted(os.listdir(pieces))
                   if f.endswith('.png')]
    for p in targets:
        out = make_feathered_alpha(p)
        out.save(p, 'PNG', optimize=True)
        print('feather:', os.path.basename(p), os.path.getsize(p) // 1024, 'KB')


if __name__ == '__main__':
    main()
