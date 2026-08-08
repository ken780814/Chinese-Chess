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

### 方式一：DEB 包安装 / Method 1: DEB Package
```bash
sudo dpkg -i chinese-chess_1.0.0_amd64.deb
sudo apt-get install -f  # 修复依赖
```

### 方式二：RPM 格式 (tar.gz) / Method 2: RPM Format (tar.gz)
```bash
# 由于服务器缺少 rpm-build 工具，使用 tar.gz 格式
sudo tar -xzf chinese-chess-1.0.0.el8.x86_64.tar.gz -C /
chinese-chess
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
# DEB 系统
sudo apt remove chinese-chess

# RPM 系统
sudo dnf remove chinese-chess
# 或
sudo yum remove chinese-chess

# Tar.gz 安装
sudo rm -rf /usr/bin/chinese-chess /usr/share/chinese-chess /usr/share/applications/chinese-chess.desktop
sudo rm -f /usr/share/icons/hicolor/256x256/apps/chinese-chess.png
```

## 依赖 / Dependencies

| 包名 | 说明 |
|------|------|
| python3 (>= 3.8) | Python 3.8+ |
| libgl1-mesa-glx | OpenGL 支持 |
| libglib2.0-0 | GLib 库 |
| libsm6 | X11 SM 库 |
| libxtst6 | X11 XTest 库 |

| Package | Description |
|---------|-------------|
| python3 (>= 3.8) | Python 3.8+ |
| libgl1-mesa-glx | OpenGL support |
| libglib2.0-0 | GLib library |
| libsm6 | X11 SM library |
| libxtst6 | X11 XTest library |

## 常见问题 / FAQ

### Q: 安装时提示缺少依赖
A: 运行 `sudo apt-get install -f` (DEB) 或 `sudo dnf install -y` (RPM) 自动修复
**Q: Missing dependencies during installation**
A: Run `sudo apt-get install -f` (DEB) or `sudo dnf install -y` (RPM) to fix automatically

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
