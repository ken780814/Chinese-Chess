#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 程序图标生成器
生成 PNG 格式的图标文件
"""

import sys
from PIL import Image, ImageDraw, ImageFont


def create_chess_icon(output_path='assets/icon.png', size=256):
    """创建中国象棋图标"""
    
    # 创建画布
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景圆形（红色）
    center = size // 2
    radius = size // 2 - 10
    draw.ellipse([center - radius, center - radius, center + radius, center + radius],
                 fill=(220, 20, 60), outline=(180, 0, 0), width=5)
    
    # 尝试加载字体，如果失败则使用默认字体
    try:
        # 尝试加载中文字体
        font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", size // 3)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", size // 3)
        except:
            font = ImageFont.load_default()
    
    # 绘制棋子文字
    piece_text = "棋"
    bbox = draw.textbbox((0, 0), piece_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = center - text_width // 2
    text_y = center - text_height // 2 - bbox[1]
    
    draw.text((text_x, text_y), piece_text, fill=(255, 215, 0), font=font)
    
    # 保存图标
    img.save(output_path, 'PNG')
    print(f"图标已保存到: {output_path}")


def create_chess_piece_icons(output_dir='assets'):
    """创建各个棋子的图标"""
    
    pieces = {
        'K_red': ('帅', (220, 20, 60), (255, 215, 0)),
        'K_black': ('将', (30, 30, 30), (255, 255, 255)),
        'A_red': ('仕', (220, 20, 60), (255, 215, 0)),
        'A_black': ('士', (30, 30, 30), (255, 255, 255)),
        'B_red': ('相', (220, 20, 60), (255, 215, 0)),
        'B_black': ('象', (30, 30, 30), (255, 255, 255)),
        'N_red': ('马', (220, 20, 60), (255, 215, 0)),
        'N_black': ('马', (30, 30, 30), (255, 255, 255)),
        'R_red': ('车', (220, 20, 60), (255, 215, 0)),
        'R_black': ('车', (30, 30, 30), (255, 255, 255)),
        'C_red': ('炮', (220, 20, 60), (255, 215, 0)),
        'C_black': ('炮', (30, 30, 30), (255, 255, 255)),
        'P_red': ('兵', (220, 20, 60), (255, 215, 0)),
        'P_black': ('卒', (30, 30, 30), (255, 255, 255)),
    }
    
    size = 64
    
    for name, (text, bg_color, text_color) in pieces.items():
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制圆形背景
        draw.ellipse([5, 5, size - 5, size - 5], fill=bg_color, outline=(0, 0, 0), width=2)
        
        # 绘制文字
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", size // 2)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (size - text_width) // 2
        text_y = (size - text_height) // 2 - bbox[1]
        
        draw.text((text_x, text_y), text, fill=text_color, font=font)
        
        # 保存
        img.save(f'{output_dir}/{name}.png', 'PNG')
        print(f"已创建: {name}.png")


if __name__ == '__main__':
    import os
    
    # 创建资源目录
    os.makedirs('assets', exist_ok=True)
    
    # 创建主图标
    create_chess_icon('assets/icon.png', 256)
    
    # 创建棋子图标
    create_chess_piece_icons('assets')
    
    print("\n所有图标创建完成！")
