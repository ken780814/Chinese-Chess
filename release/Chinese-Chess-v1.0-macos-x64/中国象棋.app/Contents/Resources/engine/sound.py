#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国象棋 - 音效模块
使用 pygame 播放音效
"""

import os
import sys
import pygame


class SoundManager:
    """音效管理器"""
    
    def __init__(self, sound_dir='assets/sounds'):
        self.sound_dir = sound_dir
        self.sounds = {}
        self.music_playing = False
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        
        # 音效文件名映射
        self.sound_files = {
            'move': 'move.wav',
            'capture': 'capture.wav',
            'check': 'check.wav',
            'checkmate': 'checkmate.wav',
            'select': 'select.wav',
            'game_start': 'game_start.wav',
            'game_over_win': 'win.wav',
            'game_over_lose': 'lose.wav',
            'timeout': 'timeout.wav',
        }
        
        self._load_sounds()
    
    def _load_sounds(self):
        """加载音效文件"""
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Warning: Could not initialize pygame mixer: {e}, sounds disabled")
            return
        
        os.makedirs(self.sound_dir, exist_ok=True)
        
        for name, filename in self.sound_files.items():
            filepath = os.path.join(self.sound_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[name] = pygame.mixer.Sound(filepath)
                    self.sounds[name].set_volume(self.sfx_volume)
                except Exception as e:
                    print(f"Warning: Could not load {filepath}: {e}")
    
    def play(self, sound_name):
        """播放指定音效"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def play_move(self):
        """播放走棋音效"""
        self.play('move')
    
    def play_capture(self):
        """播放吃子音效"""
        self.play('capture')
    
    def play_check(self):
        """播放将军音效"""
        self.play('check')
    
    def play_checkmate(self):
        """播放将死音效"""
        self.play('checkmate')
    
    def play_select(self):
        """播放选中音效"""
        self.play('select')
    
    def play_game_start(self):
        """播放游戏开始音效"""
        self.play('game_start')
    
    def play_win(self):
        """播放胜利音效"""
        self.play('game_over_win')
    
    def play_lose(self):
        """播放失败音效"""
        self.play('game_over_lose')
    
    def play_timeout(self):
        """播放超时音效"""
        self.play('timeout')
    
    def set_volume(self, volume):
        """设置音量"""
        self.master_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.master_volume * self.sfx_volume)
    
    def mute(self):
        """静音"""
        for sound in self.sounds.values():
            sound.set_volume(0)
    
    def unmute(self):
        """取消静音"""
        for sound in self.sounds.values():
            sound.set_volume(self.master_volume * self.sfx_volume)
    
    def is_available(self):
        """检查音效是否可用"""
        return len(self.sounds) > 0


def create_test_sounds():
    """创建测试音效（需要 soundfile 和 numpy）"""
    try:
        import numpy as np
        import soundfile as sf
    except ImportError:
        print("需要安装 soundfile 和 numpy 来生成测试音效")
        print("运行: pip3 install soundfile numpy")
        return
    
    sound_dir = 'assets/sounds'
    os.makedirs(sound_dir, exist_ok=True)
    
    # 简单的提示音生成
    sample_rate = 44100
    duration = 0.2
    
    # 走棋声（短促的"嗒"声）
    t = np.linspace(0, duration, int(sample_rate * duration))
    move_sound = np.sin(800 * 2 * np.pi * t) * np.exp(-5 * t)
    sf.write(f'{sound_dir}/move.wav', move_sound, sample_rate)
    
    # 吃子声（较重的"砰"声）
    capture_sound = np.sin(400 * 2 * np.pi * t) * np.exp(-3 * t)
    sf.write(f'{sound_dir}/capture.wav', capture_sound, sample_rate)
    
    # 将军声（警示音）
    check_t = np.linspace(0, 0.5, int(sample_rate * 0.5))
    check_sound = np.sin(600 * 2 * np.pi * check_t) * np.exp(-2 * check_t)
    check_sound = np.concatenate([check_sound, np.sin(800 * 2 * np.pi * check_t) * np.exp(-2 * check_t)])
    sf.write(f'{sound_dir}/check.wav', check_sound, sample_rate)
    
    print("测试音效已生成")


if __name__ == '__main__':
    # 测试音效模块
    sys.path.insert(0, '.')
    
    pygame.init()
    sound_mgr = SoundManager()
    
    if sound_mgr.is_available():
        print("音效模块测试通过")
        sound_mgr.play_game_start()
        import time
        time.sleep(1)
    else:
        print("音效模块未初始化（可能是缺少音频文件）")
        print("运行 'python3 engine/sound.py' 生成测试音效")
