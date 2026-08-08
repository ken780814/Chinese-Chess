#!/bin/bash
# 中国象棋 - 安装说明脚本

cat << 'EOF'
========================================
  中国象棋 - Linux 安装说明
  Chinese Chess - Linux Installation Guide
========================================

【安装方式一：使用 apt 安装（推荐）】
Method 1: Use apt to install (Recommended)
--------------------------------------------
sudo apt install ./chinese-chess_1.0.0_amd64.deb

apt 会自动处理所有依赖关系。

apt will automatically handle all dependencies.


【安装方式二：使用 dpkg 安装】
Method 2: Use dpkg to install
--------------------------------------------
# 1. 安装依赖
# Install dependencies
sudo apt-get install -y libgl1 libglib2.0-0 libsm6 libxtst6

# 2. 安装 DEB 包
# Install DEB package
sudo dpkg -i chinese-chess_1.0.0_amd64.deb

# 3. 修复依赖
# Fix dependencies
sudo apt-get install -f


【卸载方式】
Uninstall
--------------------------------------------
sudo apt remove chinese-chess


【运行方式】
How to Run
--------------------------------------------
# 方法1: 桌面启动器
# Method 1: Desktop launcher
在应用菜单中搜索 "中国象棋" 或 "Chinese Chess"
Search for "Chinese Chess" in the application menu

# 方法2: 命令行
# Method 2: Command line
chinese-chess                    # 开始游戏
chinese-chess --mode=endgame     # 残局挑战
chinese-chess --no-sound         # 禁用音效


【常见问题】
FAQ
--------------------------------------------

Q: 安装时提示缺少 libgl1-mesa-glx
Q: Missing libgl1-mesa-glx error
A: 运行: sudo apt-get install -y libgl1 libgl1-mesa-glx

A: Run: sudo apt-get install -y libgl1 libgl1-mesa-glx


Q: 黑屏或无法显示
Q: Black screen or display issues
A: 请确保已安装 OpenGL 驱动
   Ensure OpenGL drivers are installed

A: Please ensure OpenGL drivers are installed


Q: 音效不播放
Q: Sound not playing
A: 检查系统音量，或运行 --no-sound 禁用音效
   Check system volume, or run with --no-sound to disable

A: Check system volume settings, or run with --no-sound flag


【系统要求】
System Requirements
--------------------------------------------
- Ubuntu 18.04+ / Debian 10+ / Linux Mint 19+
- x86_64 架构
- 256MB 内存以上
- OpenGL 支持
- 100MB 磁盘空间

- Ubuntu 18.04+ / Debian 10+ / Linux Mint 19+
- x86_64 architecture
- 256MB RAM or more
- OpenGL support
- 100MB disk space

========================================
EOF
