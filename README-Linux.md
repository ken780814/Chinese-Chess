# 中国象棋 - Linux 版本
# Chinese Chess - Linux Version

## 系统要求 / System Requirements

- Ubuntu 18.04+ / Debian 10+ / Linux Mint 19+ / CentOS 8+ / Fedora 33+
- x86_64 架构
- 256MB 内存以上
- OpenGL 支持
- 100MB 磁盘空间

- Ubuntu 18.04+ / Debian 10+ / Linux Mint 19+ / CentOS 8+ / Fedora 33+
- x86_64 architecture
- 256MB RAM or more
- OpenGL support
- 100MB disk space

## 安装方式 / Installation

### 方式一：使用 apt 安装（推荐） / Method 1: Use apt (Recommended)
```bash
sudo apt install ./chinese-chess_1.0.0_amd64.deb
```

### 方式二：使用 dpkg 安装 / Method 2: Use dpkg
```bash
# 1. 安装依赖 / Install dependencies
sudo apt-get install -y libgl1 libglib2.0-0 libsm6 libxtst6

# 2. 安装 DEB 包 / Install DEB package
sudo dpkg -i chinese-chess_1.0.0_amd64.deb

# 3. 修复依赖 / Fix dependencies
sudo apt-get install -f
```

### 方式三：从源码编译 / Method 3: Build from Source
```bash
git clone https://github.com/ken780814/Chinese-Chess.git
cd Chinese-Chess
pip3 install -r requirements.txt
python3 main.py
```

## 运行方式 / How to Run

### 方式一：桌面启动器 / Method 1: Desktop Launcher
在应用菜单中搜索 "中国象棋" 或 "Chinese Chess"
Search for "Chinese Chess" in the application menu

### 方式二：命令行运行 / Method 2: Command Line
```bash
chinese-chess                    # 开始游戏
chinese-chess --mode=endgame     # 残局挑战
chinese-chess --no-sound         # 禁用音效
```

## 卸载 / Uninstallation

```bash
sudo apt remove chinese-chess
```

## 依赖 / Dependencies

| 包名 | 说明 |
|------|------|
| python3 (>= 3.8) | Python 3.8+ |
| libgl1 | OpenGL 支持 |
| libglib2.0-0 | GLib 库 |
| libsm6 | X11 SM 库 |
| libxtst6 | X11 XTest 库 |
| libx11-6 | X11 库 |

| Package | Description |
|---------|-------------|
| python3 (>= 3.8) | Python 3.8+ |
| libgl1 | OpenGL support |
| libglib2.0-0 | GLib library |
| libsm6 | X11 SM library |
| libxtst6 | X11 XTest library |
| libx11-6 | X11 library |

## 常见问题 / FAQ

### Q: 安装时提示缺少 libgl1-mesa-glx
A: 运行 `sudo apt-get install -y libgl1 libgl1-mesa-glx` 自动修复
**Q: Missing libgl1-mesa-glx error**
A: Run `sudo apt-get install -y libgl1 libgl1-mesa-glx` to fix automatically

### Q: 黑屏或无法显示
A: 请确保已安装 OpenGL 驱动
**Q: Black screen or display issues**
A: Ensure OpenGL drivers are installed

### Q: 音效不播放
A: 检查系统音量，或运行 `--no-sound` 禁用音效
**Q: Sound not playing**
A: Check system volume, or run with `--no-sound` to disable

## 许可证 / License

MIT License
