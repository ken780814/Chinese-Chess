# 中国象棋 - Linux 版本

## 系统要求

- Ubuntu 18.04+ / Debian 10+ / Linux Mint 19+
- x86_64 架构
- 256MB 内存以上
- OpenGL 支持
- 100MB 磁盘空间

## 安装方式

### 方式一：DEB 包安装
```bash
sudo dpkg -i chinese-chess_1.0.0_amd64.deb
sudo apt-get install -f  # 修复依赖
```

### 方式二：从源码编译
```bash
git clone https://github.com/ken780814/Chinese-Chess.git
cd Chinese-Chess
pip3 install -r requirements.txt
python3 main.py
```

## 运行方式

### 方式一：桌面启动器
在应用菜单中搜索 "中国象棋"

### 方式二：命令行运行
```bash
chinese-chess                    # 开始游戏
chinese-chess --mode=endgame     # 残局挑战
chinese-chess --no-sound         # 禁用音效
```

## 卸载
```bash
sudo apt remove chinese-chess
```

## 依赖
- python3 (>= 3.8)
- libgl1-mesa-glx
- libglib2.0-0
- libsm6
- libxtst6

## 常见问题

### Q: 安装时提示缺少依赖
A: 运行 `sudo apt-get install -f` 自动修复

### Q: 黑屏或无法显示
A: 请确保已安装 OpenGL 驱动

### Q: 音效不播放
A: 检查系统音量，或运行 `--no-sound` 禁用音效

## 许可证
MIT License
