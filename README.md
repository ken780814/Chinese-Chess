# 中国象棋 - Chinese Chess

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![Kivy](https://img.shields.io/badge/Kivy-2.2.0+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)

**🇨🇳 一款跨平台的中国象棋桌面游戏**

[📥 下载 Release v2.0](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.0) · [📖 文档](#) · [🐛 反馈](#)

</div>

---

## ✨ 功能特性 / Features

- 🎯 **四级 AI 难度** — 初级 / 中级 / 高级 / 终极高手
- ⏱️ **计时系统** — 每方 60 秒，超时自动判负
- 🏯 **残局挑战** — 12 个经典残局
- 🎨 **高清棋子** — 使用 PNG 棋子图片
- 🔊 **音效支持** — 走棋、吃子、将军、胜利、失败、超时提示
- 🖥️ **跨平台** — Linux / Windows / macOS 原生支持
- 📱 **移动端** — Android / iOS (Kivy)
- 📏 **自适应** — 窗口缩放时棋盘自动等比缩放

---

## 📥 下载 / Download

| 平台 | 文件 | 下载 |
|------|------|------|
| 🐧 Linux | `chinese-chess_2.0.0_amd64.deb` (68KB) | [下载](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.0) |
| 🐧 Linux | `Chinese-Chess-v2.0-linux-x64.tar.gz` | [下载](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.0) |
| 🪟 Windows | `Chinese-Chess-v2.0-windows-x64.tar.gz` | [下载](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.0) |
| 🍎 macOS | `中国象棋.app` | [下载](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.0) |
| 📱 Android | `chinese_chess-2.0.0-debug.apk` | [下载](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.0) |
| 📱 iOS | 需要本地编译 | [源码](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.0) |

---

## 🚀 快速安装 / Installation

### Linux (DEB 包)

```bash
# 下载并安装 V2.0 (68KB 轻量包)
wget https://github.com/ken780814/Chinese-Chess/releases/download/v2.0/chinese-chess_2.0.0_amd64.deb
sudo apt install ./chinese-chess_2.0.0_amd64.deb

# 运行
chinese-chess
```

### Linux (tar.gz 压缩包)

```bash
wget https://github.com/ken780814/Chinese-Chess/releases/download/v2.0/Chinese-Chess-v2.0-linux-x64.tar.gz
tar -xf Chinese-Chess-v2.0-linux-x64.tar.gz
cd Chinese-Chess-v2.0-linux-x64
./chinese-chess
```

### Windows

```cmd
REM 下载 Windows 版本
curl -L https://github.com/ken780814/Chinese-Chess/releases/download/v2.0/Chinese-Chess-v2.0-windows-x64.tar.gz -o chinese-chess.zip
REM 解压并运行 chinese-chess.exe
```

### macOS

```bash
brew install python@3.11
pip3 install PyQt5 pygame pillow
# Clone and run
git clone https://github.com/ken780814/Chinese-Chess.git
cd Chinese-Chess
python3 main.py
```

### Android

```bash
# 本地编译 APK
pip3 install kivy pygame pillow
pip3 install buildozer cython
buildozer android debug
```

---

## 🎮 游戏操作 / Gameplay

### 鼠标操作
| 操作 | 说明 |
|------|------|
| 点击棋子 | 选中己方棋子 |
| 点击绿点 | 移动到目标位置 |
| 新游戏按钮 | 重置棋盘 |
| 难度下拉 | 切换 AI 等级 |

### 键盘快捷键
| 按键 | 功能 |
|------|------|
| `N` | 新游戏 |
| `R` | 重新开始 |
| `ESC` | 返回主菜单 |

---

## 📦 项目结构 / Project Structure

```
Chinese-Chess/
├── main.py                    # 主程序入口 (桌面)
├── main_mobile.py             # 移动端入口 (Kivy)
├── engine/
│   ├── rules.py               # 棋规引擎 (449 行)
│   ├── ai.py                  # AI 对弈引擎 (202 行)
│   └── sound.py               # 音效管理 (172 行)
├── gui/
│   ├── board.py               # 棋盘界面
│   └── endgame.py             # 残局界面 (375 行)
├── data/
│   ├── endgames.py            # 12 个残局数据 (253 行)
│   └── __init__.py
├── assets/
│   ├── icon.png               # 应用图标 (256x256)
│   ├── *_red.png              # 红方棋子 (7 个)
│   ├── *_black.png            # 黑方棋子 (7 个)
│   └── sounds/                # 音效文件
├── scripts/
│   ├── create_deb.py          # DEB 打包
│   ├── package.sh             # PyInstaller 打包
│   └── package_mobile.sh      # 移动端打包
├── buildozer.spec             # Android 构建配置
├── README.md                  # 项目文档
├── README-Linux.md           # Linux 安装指南
├── README-Windows.md         # Windows 使用指南
├── README-macOS.md           # macOS 使用指南
├── README-Mobile.md          # 移动端说明
├── INSTALL-GUIDE.md          # 安装指南
└── requirements.txt           # Python 依赖
```

---

## 🛠️ 开发环境 / Development

### 安装依赖

```bash
# 桌面版本
pip3 install PyQt5 pygame pillow

# 移动端
pip3 install kivy pygame pillow
```

### 运行游戏

```bash
# 桌面
python3 main.py

# 移动端
python3 main_mobile.py
```

### 打包 DEB

```bash
python3 scripts/create_deb.py
```

---

## 🆕 版本更新 / Changelog

### v2.0 (2026-08-09)
- **⚡ 体积优化**: DEB 包从 73MB 减小到 68KB (99.9% 减少)
- **📦 依赖重构**: 使用系统 Python Qt 库，不再打包 Qt
- **🎨 界面优化**: 棋子使用图片绘制，棋盘代码绘制
- **🖱️ 交互修复**: 修复点击事件处理
- **📏 自适应**: 棋盘自动等比缩放
- **🐛 Bug 修复**: 修复导入路径、初始化问题
- **📱 多平台更新**: Windows / macOS / Android / iOS 同步修复

### v1.0 (2026-08-07)
- 初始版本发布
- 四级 AI 对弈
- 12 个残局挑战
- Linux / Windows / macOS 支持
- 移动端 (Kivy)

---

## 🤝 贡献 / Contributing

欢迎提交 Pull Request 和 Issue！

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some feature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📄 许可证 / License

MIT License - 详见 [LICENSE](LICENSE)

---

## 🌟 支持项目

如果这个项目对你有帮助，请点 ⭐ 支持一下！

[![GitHub stars](https://img.shields.io/github/stars/ken780814/Chinese-Chess?style=social)](https://github.com/ken780814/Chinese-Chess/stars)
[![GitHub forks](https://img.shields.io/github/forks/ken780814/Chinese-Chess?style=social)](https://github.com/ken780814/Chinese-Chess/network)

---

<div align="center">

**Made with ❤️ by [ken780814](https://github.com/ken780814)**

</div>
