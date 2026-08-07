# 中国象棋 - Chinese Chess

一款功能丰富的中国象棋桌面游戏，支持多种 AI 难度和残局挑战。

## 功能特性

- 🎮 双人本地对战
- 🤖 四级 AI 难度：初级、中级、高级、终极高手
- ⏱️ 计时系统：每方 60 秒，超时自动走棋
- 🧩 残局挑战模式（12个经典残局）
- 🖼️ 美观的棋盘界面
- 📦 一键安装/卸载

## 系统要求

- Python 3.8+
- PyQt5
- Linux / Windows / macOS

## 安装

### 方式一：直接运行

```bash
python main.py              # 开始游戏
python main.py --mode=endgame  # 残局挑战
```

### 方式二：使用安装脚本（Linux）

```bash
chmod +x scripts/install.sh
sudo ./scripts/install.sh
chinese-chess               # 运行游戏
```

### 方式三：创建桌面快捷方式

安装后会在桌面创建快捷方式，双击即可启动。

## 卸载

```bash
sudo ./scripts/uninstall.sh
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

## 残局挑战

游戏内置 12 个经典残局：

| 编号 | 残局名 | 难度 | 描述 |
|------|--------|------|------|
| 1 | 单车破士 | 简单 | 单车对单士 |
| 2 | 双车挫 | 简单 | 双车对士象全 |
| 3 | 马后炮 | 中等 | 马炮配合杀局 |
| 4 | 一车十子寒 | 中等 | 单车胜士象全 |
| 5 | 双马饮泉 | 中等 | 双马配合杀局 |
| 6 | 车兵临门 | 简单 | 车兵配合杀局 |
| 7 | 炮双兵胜 | 中等 | 炮双兵对士象全 |
| 8 | 马兵胜士象 | 困难 | 马兵对士象全 |
| 9 | 双炮胜 | 简单 | 双炮对单士 |
| 10 | 车炮争雄 | 困难 | 车炮对车士 |
| 11 | 三子归边 | 困难 | 车马炮配合杀局 |
| 12 | 钓鱼马 | 中等 | 马兵胜单士 |

## 项目结构

```
Chinese-Chess/
├── main.py                  # 主程序入口
├── gui/
│   ├── __init__.py
│   ├── board.py             # 棋盘界面
│   └── endgame.py           # 残局界面
├── engine/
│   ├── __init__.py
│   ├── rules.py             # 游戏规则
│   └── ai.py                # AI 引擎
├── data/
│   ├── __init__.py
│   └── endgames.py          # 残局数据
├── assets/
│   ├── icon.png             # 程序图标
│   └── *.png                # 棋子图标
├── tests/
│   ├── __init__.py
│   ├── test_chinese_chess.py # 单元测试
│   └── benchmark.py          # 性能测试
├── scripts/
│   ├── install.sh           # 安装脚本
│   └── uninstall.sh         # 卸载脚本
├── requirements.txt         # Python 依赖
├── .gitignore
├── README.md                # 项目说明
└── Chinese-Chess-dev-plan.md  # 开发计划
```

## 测试

运行单元测试：
```bash
python -m unittest tests/test_chinese_chess.py -v
```

运行性能测试：
```bash
python tests/benchmark.py
```

## 开发进度

- [x] 项目初始化
- [x] 基本规则实现
- [x] AI 引擎基础框架
- [x] 棋盘界面
- [x] 残局挑战模式
- [x] 单元测试
- [x] 程序图标
- [ ] 音效支持
- [ ] 打包发布为 .deb

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
