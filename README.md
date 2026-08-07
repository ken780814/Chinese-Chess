# 中国象棋 - Chinese Chess

一款功能丰富的中国象棋桌面游戏，支持多种 AI 难度和残局挑战。

## 功能特性

- 🎮 双人本地对战
- 🤖 四级 AI 难度：初级、中级、高级、终极高手
- ⏱️ 计时系统：每方 60 秒，超时自动走棋
- 🧩 残局挑战模式（开发中）
- 🖼️ 美观的棋盘界面

## 系统要求

- Python 3.8+
- PyQt5
- Linux / Windows / macOS

## 安装

### 方式一：直接运行

```bash
python main.py
```

### 方式二：使用安装脚本（Linux）

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### 方式三：创建桌面快捷方式

安装后会在桌面创建快捷方式，双击即可启动。

## 卸载

```bash
chmod +x scripts/uninstall.sh
./scripts/uninstall.sh
```

或通过包管理器：
```bash
sudo dpkg -r chinese-chess
```

## 使用

1. 启动游戏后，选择 AI 难度
2. 红方先行，点击棋子选中，再点击目标位置移动
3. 每方有 60 秒倒计时，超时后 AI 将自动走一步
4. 将死对方将/帅即可获胜

## 项目结构

```
Chinese-Chess/
├── main.py              # 主程序入口
├── gui/
│   └── board.py         # 棋盘界面
├── engine/
│   ├── rules.py         # 游戏规则
│   └── ai.py            # AI 引擎
├── data/
│   └── endgames.json    # 残局数据
├── assets/              # 资源文件
├── scripts/
│   ├── install.sh       # 安装脚本
│   └── uninstall.sh     # 卸载脚本
└── Chinese-Chess-dev-plan.md  # 开发计划
```

## 开发进度

- [x] 项目初始化
- [x] 基本规则实现
- [x] AI 引擎基础框架
- [x] 棋盘界面
- [ ] 残局挑战模式
- [ ] 音效与音乐
- [ ] 打包发布

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
