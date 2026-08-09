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

| 平台 | 文件 | 下载 / 说明 |
|------|------|------|
| 🐧 Linux (DEB) | `chinese-chess_2.4.0_amd64.deb` (1.4MB) | [下载](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.4) |
| 🪟 Windows | 需本地构建（见下方说明） | 源码 `scripts/package_windows.sh` |
| 🍎 macOS | 需本地构建（见下方说明） | 源码 `scripts/package_macos.sh` |
| 📱 Android | 需本地编译 APK | 源码 `buildozer.spec` |
| 📱 iOS | 需 Mac 环境编译 | 源码 `main_mobile.py` |

> **当前仅发布 Linux DEB 包**（V2.4.0）。Windows / macOS / Android / iOS 的打包脚本与源码已就绪，但未在 CI 中预构建，请按下方「本地构建」章节自行编译。

---

## 🚀 快速安装 / Installation

### Linux (DEB 包) — 推荐

```bash
# 下载并安装 V2.4 (1.4MB，含 AI 生成木质棋子素材)
wget https://github.com/ken780814/Chinese-Chess/releases/download/v2.4/chinese-chess_2.4.0_amd64.deb
sudo apt install ./chinese-chess_2.4.0_amd64.deb

# 运行
chinese-chess
```

依赖（`python3-pyqt5`、`python3-pil`、`python3-pygame`、`libgl1` 等）由 apt 自动安装。

### Windows / macOS（本地构建）

仓库已提供打包脚本，需在对应平台上运行：

```bash
# Windows（在 Windows 上执行）
git clone https://github.com/ken780814/Chinese-Chess.git
cd Chinese-Chess
bash scripts/package_windows.sh   # 产出 dist/chinese-chess.exe

# macOS（在 macOS 上执行）
bash scripts/package_macos.sh     # 产出 .app
```

### Android（本地编译 APK）

```bash
pip3 install kivy buildozer cython
buildozer android debug   # 产出 bin/*.apk
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

### v2.4 (2026-08-09)
- **🎨 立体感恢复**: 棋子采用羽化 alpha，保留圆盘立体高光环，消除 V2.3 扁片感
- **📐 比例优化**: 棋子绘制尺寸从 1.02 格距缩到 0.9 格距，留白更舒适
- **🐧 仅发布 Linux DEB** (1.4MB)

### v2.3 (2026-08-09)
- **✂️ 棋子透明化**: floodfill + 圆形硬遮罩，棋盘外 100% 透明
- **🐛 修复**: 消除棋子周围白色方形/圆形背景遮挡棋盘线

### v2.2 (2026-08-09)
- **📏 棋盘线修复**: AI 纹理改为高斯模糊只留木色，代码绘制唯一一套清晰网格线
- **✂️ 棋子遮罩**: 圆形 alpha 遮罩，圆盘外透明

### v2.1 (2026-08-09)
- **🎨 素材升级**: 用 Agnes AI 生成木质棋子（14 枚）+ 棋盘纹理，替换代码黑体棋子
- **🀄 传统样式**: 双方本体同色木盘，红/黑书法文字区分敌我

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
