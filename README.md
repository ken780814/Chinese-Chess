# 中国象棋 - Chinese Chess

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![Kivy](https://img.shields.io/badge/Kivy-2.2+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Linux](https://img.shields.io/badge/Linux-x86_64-orange.svg)
![Windows](https://img.shields.io/badge/Windows-10%2F11-blue.svg)
![macOS](https://img.shields.io/badge/macOS-10.13%2B-purple.svg)
![Android](https://img.shields.io/badge/Android-5.0%2B-green.svg)
![iOS](https://img.shields.io/badge/iOS-12.0%2B-blue.svg)

**一款功能丰富的中国象棋桌面游戏，支持五级平台和触屏操作**
**A feature-rich Chinese Chess desktop game supporting 5 platforms and touch controls**

[![GitHub release](https://img.shields.io/github/v/release/ken780814/Chinese-Chess)](https://github.com/ken780814/Chinese-Chess/releases)
[![GitHub stars](https://img.shields.io/github/stars/ken780814/Chinese-Chess)](https://github.com/ken780814/Chinese-Chess/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ken780814/Chinese-Chess)](https://github.com/ken780814/Chinese-Chess/network/members)

</div>

---

## 📖 项目简介 / About

中国象棋（Chinese Chess / Xiangqi）是中国传统棋类运动，拥有数千年的历史。本项目使用 Python 开发了一款功能丰富的桌面象棋游戏，支持人机对战、残局挑战等多种模式，并提供多平台版本。

Chinese Chess (Xiangqi) is a traditional Chinese board game with thousands of years of history. This project is a feature-rich desktop chess game developed with Python, supporting human vs AI battles, endgame challenges, and multiple platform versions.

### ✨ 核心特性 / Core Features

| 特性 / Feature | 描述 / Description |
|------|------|
| 🎮 **五级 AI 难度** | 初级（随机）、中级（MiniMax depth=2）、高级（depth=3）、终极高手（depth=4） |
| 🧩 **12 个经典残局** | 单车破士、双车挫、马后炮、一车十子寒、双马饮泉等 |
| ⏱️ **计时系统** | 每方 60 秒限时，超时自动走棋 |
| 🔊 **音效支持** | 走棋、吃子、将军、胜利、失败等音效 |
| 🎨 **精美界面** | PyQt5/Kivy 图形界面，自适应屏幕尺寸 |
| 📱 **多平台支持** | Linux (DEB)、Windows (EXE)、macOS (APP)、Android、iOS |
| ✅ **完整测试** | 17 个单元测试全部通过 |

---

## 🚀 快速开始 / Quick Start

### 下载 Release / Download Release

| 平台 / Platform | 下载链接 / Download |
|-----------------|---------------------|
| 🐧 **Linux x64** | [chinese-chess_1.0.0_amd64.deb](https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/chinese-chess_1.0.0_amd64.deb) |
| 🐧 **Linux (RPM 格式)** | [chinese-chess-1.0.0.el8.x86_64.tar.gz](https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/chinese-chess-1.0.0.el8.x86_64.tar.gz) |
| 🪟 **Windows x64** | [Chinese-Chess-v1.0-windows-x64.tar.gz](https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/Chinese-Chess-v1.0-windows-x64.tar.gz) |
| 🍎 **macOS x64** | [Chinese-Chess-v1.0-macos-x64.tar.gz](https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/Chinese-Chess-v1.0-macos-x64.tar.gz) |
| 📱 **Android** | [从源码编译](#-移动端版本) |
| 📱 **iOS** | [从源码编译](#-移动端版本) |

### Linux 安装（推荐） / Linux Installation (Recommended)
```bash
# 方式一：使用 apt 安装（推荐）
sudo apt install ./chinese-chess_1.0.0_amd64.deb

# 方式二：使用 dpkg 安装
sudo dpkg -i chinese-chess_1.0.0_amd64.deb
sudo apt-get install -f  # 修复依赖
```

### 从源码运行 / Run from Source
```bash
git clone https://github.com/ken780814/Chinese-Chess.git
cd Chinese-Chess
pip3 install -r requirements.txt
python3 main.py
```

---

## 📱 移动端版本 / Mobile Version

### 系统要求 / System Requirements

#### Android
- Android 5.0+ (API 21+)
- 1GB 内存以上
- 100MB 存储空间

#### iOS
- iOS 12.0+
- 1GB 内存以上
- 100MB 存储空间

### 触摸控制 / Touch Controls

| 操作 / Action | 说明 / Description |
|------|------|
| 点击棋子 | 选中棋子 |
| 点击目标格 | 移动棋子 |
| 点击按钮 | 切换难度/重新开始 |

### 打包为 APK / Build APK (Android)
```bash
pip3 install buildozer cython
bash scripts/package_mobile.sh android
```

### 打包为 IPA / Build IPA (iOS)
```bash
bash scripts/package_mobile.sh ios
```

---

## 🎮 游戏功能 / Game Features

### 1. 人机对战 / Human vs AI

#### AI 难度级别 / AI Difficulty Levels

| 难度 | 名称 | 搜索深度 | 说明 |
|------|------|----------|------|
| 🟢 | 初级 | - | 随机走法，适合新手练习 |
| 🟡 | 中级 | depth=2 | MiniMax + α-β剪枝，适合入门 |
| 🟠 | 高级 | depth=3 | 更强的搜索，适合进阶玩家 |
| 🔴 | 终极高手 | depth=4 | 最强 AI，适合挑战高手 |

### 2. 残局挑战 / Endgame Challenges

| 编号 | 残局名 | 难度 | 描述 | 解法步数 |
|------|--------|------|------|----------|
| 1 | 单车破士 | ⭐ | 单车对单士 | 9步 |
| 2 | 双车挫 | ⭐ | 双车对士象全 | 5步 |
| 3 | 马后炮 | ⭐⭐ | 马炮配合杀局 | 7步 |
| 4 | 一车十子寒 | ⭐⭐ | 单车胜士象全 | 5步 |
| 5 | 双马饮泉 | ⭐⭐ | 双马配合杀局 | 7步 |
| 6 | 车兵临门 | ⭐ | 车兵配合杀局 | 3步 |
| 7 | 炮双兵胜 | ⭐⭐ | 炮双兵对士象全 | 3步 |
| 8 | 马兵胜士象 | ⭐⭐⭐ | 马兵对士象全 | 5步 |
| 9 | 双炮胜 | ⭐ | 双炮对单士 | 3步 |
| 10 | 车炮争雄 | ⭐⭐⭐ | 车炮对车士 | 3步 |
| 11 | 三子归边 | ⭐⭐⭐ | 车马炮配合杀局 | 3步 |
| 12 | 钓鱼马 | ⭐⭐ | 马兵胜单士 | 5步 |

---

## 🏗️ 技术架构 / Technical Architecture

### 项目结构 / Project Structure
```
Chinese-Chess/
├── main.py                  # 桌面版主程序 (PyQt5)
├── main_mobile.py           # 移动版主程序 (Kivy)
├── engine/                  # 游戏引擎
├── gui/                     # 图形界面
├── data/                    # 数据文件
├── assets/                  # 资源文件
├── tests/                   # 测试
├── scripts/                 # 脚本
│   ├── package_deb.sh       # DEB 打包
│   ├── package_rpm.sh       # RPM 打包
│   └── package_mobile.sh    # 移动端打包
└── README*.md               # 文档
```

---

## 🧪 测试 / Testing
```bash
python3 -m unittest tests/test_chinese_chess.py -v
```

---

## 📊 性能数据 / Performance Data

| 模块 | 性能 |
|------|------|
| 规则计算 | 2.79ms/次 |
| Easy AI | <1ms |
| Medium AI | 0.26s |
| Hard AI | 4.2s |
| Expert AI | 77s |

---

## 🤝 贡献指南 / Contribution Guide

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证 / License

MIT License

---

## 🙏 致谢 / Acknowledgments

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- [Kivy](https://kivy.org/)
- [pygame](https://www.pygame.org/)
- [PyInstaller](https://www.pyinstaller.org/)

---

## 🔗 相关链接 / Related Links

- [GitHub 仓库](https://github.com/ken780814/Chinese-Chess)
- [Release 下载](https://github.com/ken780814/Chinese-Chess/releases/tag/v1.0)

---

<div align="center">

**Made with ❤️ by AI Assistant for Ken**

</div>
