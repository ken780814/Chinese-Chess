# 中国象棋 - Chinese Chess

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Linux](https://img.shields.io/badge/Linux-x86_64-orange.svg)
![Windows](https://img.shields.io/badge/Windows-10%2F11-blue.svg)

**一款功能丰富的中国象棋桌面游戏，支持四级 AI 难度和残局挑战**

[![GitHub release](https://img.shields.io/github/v/release/ken780814/Chinese-Chess)](https://github.com/ken780814/Chinese-Chess/releases)
[![GitHub stars](https://img.shields.io/github/stars/ken780814/Chinese-Chess)](https://github.com/ken780814/Chinese-Chess/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ken780814/Chinese-Chess)](https://github.com/ken780814/Chinese-Chess/network/members)

</div>

---

## 📖 项目简介

中国象棋（Chinese Chess / Xiangqi）是中国传统棋类运动，拥有数千年的历史。本项目使用 Python 和 PyQt5 开发了一款功能丰富的桌面象棋游戏，支持人机对战、残局挑战等多种模式。

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🎮 **四级 AI 难度** | 初级（随机）、中级（MiniMax depth=2）、高级（depth=3）、终极高手（depth=4） |
| 🧩 **12 个经典残局** | 单车破士、双车挫、马后炮、一车十子寒、双马饮泉等 |
| ⏱️ **计时系统** | 每方 60 秒限时，超时自动走棋 |
| 🔊 **音效支持** | 走棋、吃子、将军、胜利、失败等音效 |
| 🎨 **精美界面** | PyQt5 图形界面，清晰美观的棋盘和棋子 |
| 📦 **一键安装** | 提供安装/卸载脚本，支持桌面快捷方式 |
| ✅ **完整测试** | 17 个单元测试全部通过 |

---

## 🚀 快速开始

### 系统要求

| 平台 | 要求 |
|------|------|
| **Linux** | Linux (x86_64), OpenGL/X11, 256MB 内存 |
| **Windows** | Windows 10/11 (64位), DirectX 9.0c, 256MB 内存 |

### 下载安装

#### Linux 版本

```bash
# 下载
wget https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/Chinese-Chess-v1.0-linux-x64.tar.gz
tar -xzf Chinese-Chess-v1.0-linux-x64.tar.gz
cd Chinese-Chess-v1.0

# 运行
./chinese-chess
```

#### Windows 版本

1. 下载 [Chinese-Chess-v1.0-windows-x64.tar.gz](https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/Chinese-Chess-v1.0-windows-x64.tar.gz)
2. 解压到任意目录
3. 双击 `chinese-chess.exe` 运行

```cmd
# 命令行运行
chinese-chess.exe              # 开始游戏
chinese-chess.exe --mode=endgame  # 残局挑战
chinese-chess.exe --no-sound   # 禁用音效
```

### 从源码运行

```bash
git clone https://github.com/ken780814/Chinese-Chess.git
cd Chinese-Chess
pip3 install -r requirements.txt
python3 main.py
```

---

## 🎮 游戏功能

### 1. 人机对战

#### AI 难度级别

| 难度 | 名称 | 搜索深度 | 说明 |
|------|------|----------|------|
| 🟢 | 初级 | - | 随机走法，适合新手练习 |
| 🟡 | 中级 | depth=2 | MiniMax + α-β剪枝，适合入门 |
| 🟠 | 高级 | depth=3 | 更强的搜索，适合进阶玩家 |
| 🔴 | 终极高手 | depth=4 | 最强 AI，适合挑战高手 |

#### 游戏控制

- **选择棋子**: 点击棋盘上的棋子
- **移动棋子**: 点击目标位置（绿色圆点提示合法走法）
- **重新开始**: 点击"重新开始"按钮
- **切换难度**: 使用下拉菜单选择 AI 难度

#### 计时系统

- 每方 **60 秒**限时
- 超时后 AI 自动走一步
- 实时显示剩余时间

### 2. 残局挑战

#### 残局列表

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

#### 残局功能

- **提示**: 显示下一步推荐走法
- **重置**: 回到残局初始状态
- **下一关**: 挑战下一个残局
- **步数统计**: 记录解题步数

---

## 🏗️ 技术架构

### 项目结构

```
Chinese-Chess/
├── main.py                  # 主程序入口
├── gui/
│   ├── board.py             # 棋盘界面 (PyQt5)
│   └── endgame.py           # 残局挑战界面
├── engine/
│   ├── rules.py             # 游戏规则引擎
│   ├── ai.py                # AI 引擎 (MiniMax + α-β剪枝)
│   └── sound.py             # 音效管理 (pygame)
├── data/
│   └── endgames.py          # 残局数据 (12个)
├── assets/
│   ├── icon.png             # 程序图标 (256x256)
│   └── *.png                # 棋子图标 (64x64)
├── tests/
│   ├── test_chinese_chess.py # 单元测试 (17个)
│   └── benchmark.py          # 性能测试
├── scripts/
│   ├── install.sh           # Linux 安装脚本
│   ├── uninstall.sh         # Linux 卸载脚本
│   ├── install_windows.py   # Windows 安装脚本
│   └── uninstall_windows.py # Windows 卸载脚本
├── requirements.txt         # Python 依赖
├── README.md                # 项目说明
└── README-Windows.md        # Windows 说明
```

### 技术栈

| 模块 | 技术 | 版本 |
|------|------|------|
| 图形界面 | PyQt5 | >=5.15.0 |
| 音频播放 | pygame | >=2.0.0 |
| 打包工具 | PyInstaller | 6.21.0 |
| 开发语言 | Python | 3.8+ |

---

## 🧪 测试

### 运行单元测试

```bash
python3 -m unittest tests/test_chinese_chess.py -v
```

### 性能测试

```bash
python3 tests/benchmark.py
```

### 测试结果

```
Ran 17 tests in 83.065s
OK
```

---

## 📊 性能数据

| 模块 | 性能 |
|------|------|
| 规则计算 | 2.79ms/次 |
| Easy AI | <1ms |
| Medium AI | 0.26s |
| Hard AI | 4.2s |
| Expert AI | 77s |
| 残局加载 | 0.04μs/次 |

---

## 📦 安装部署

### Linux 安装

```bash
chmod +x scripts/install.sh
sudo ./scripts/install.sh
chinese-chess
```

### Windows 安装

1. 解压下载的压缩包
2. 双击 `chinese-chess.exe` 运行
3. 可选：右键桌面快捷方式 → 固定到任务栏

### 卸载

#### Linux
```bash
sudo ./scripts/uninstall.sh
```

#### Windows
```powershell
python scripts/uninstall_windows.py
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 规范
- 添加必要的注释和文档字符串
- 提交前运行单元测试

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可。

---

## 🙏 致谢

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - 图形界面框架
- [pygame](https://www.pygame.org/) - 音频播放库
- [PyInstaller](https://www.pyinstaller.org/) - Python 打包工具
- 中国象棋残局数据库 - 提供经典残局布局

---

## 🔗 相关链接

- [GitHub 仓库](https://github.com/ken780814/Chinese-Chess)
- [Release 下载](https://github.com/ken780814/Chinese-Chess/releases/tag/v1.0)
  - [Linux 版本](https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/Chinese-Chess-v1.0-linux-x64.tar.gz)
  - [Windows 版本](https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/Chinese-Chess-v1.0-windows-x64.tar.gz)
- [开发计划](Chinese-Chess-dev-plan.md)

---

<div align="center">

**Made with ❤️ by AI Assistant for Ken**

</div>
