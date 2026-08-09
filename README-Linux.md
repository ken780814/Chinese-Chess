# 中国象棋 - Linux 安装与启动指南

## 📥 下载 / Download

```bash
wget https://github.com/ken780814/Chinese-Chess/releases/download/v2.0/chinese-chess_2.0.0_amd64.deb
```

## 📦 安装 / Installation

### 方法 1：使用 apt (推荐)

```bash
sudo apt install ./chinese-chess_2.0.0_amd64.deb
```

### 方法 2：创建安装脚本

```bash
chmod +x install_chinese_chess.sh
./install_chinese_chess.sh
```

## 🚀 启动 / Launch

### 桌面启动 / Desktop

- 在应用菜单搜索 "Chinese Chess" 或 "中国象棋"
- 点击图标启动

### 命令行启动 / Command Line

```bash
chinese-chess                    # 启动游戏
chinese-chess --mode=endgame     # 进入残局模式
chinese-chess --no-sound         # 关闭音效
```

## 🗑️ 卸载 / Uninstall

```bash
sudo apt remove chinese-chess
sudo apt autoremove
```

## 🔧 安装后路径 / Installation Paths

| 文件类型 | 路径 |
|---------|------|
| 可执行文件 | `/usr/bin/chinese-chess` |
| 主程序 | `/usr/share/chinese-chess/main.py` |
| 棋子图片 | `/usr/share/chinese-chess/assets/` |
| 游戏引擎 | `/usr/share/chinese-chess/engine/` |
| 残局数据 | `/usr/share/chinese-chess/data/` |
| 桌面快捷方式 | `/usr/share/applications/chinese-chess.desktop` |
| 图标 | `/usr/share/icons/hicolor/256x256/apps/chinese-chess.png` |

## ❓ 常见问题 / FAQ

### Q1: 提示找不到 python3？
```bash
sudo apt install python3 python3-pyqt5 python3-pil python3-pygame
```

### Q2: 游戏启动后立即退出？
尝试安装所有依赖：
```bash
sudo apt-get install -y python3 python3-pyqt5 libgl1 libglib2.0-0 libsm6 libxtst6 libx11-6 python3-pil python3-pygame
```

### Q3: 声音没有反应？
- 检查系统音量
- 使用 `--no-sound` 参数静默模式

### Q4: 棋子图片不显示？
可能缺少字体或图片权限，请重新安装：
```bash
sudo apt install --reinstall chinese-chess
```

## 📞 支持 / Support

- **GitHub Issues**: https://github.com/ken780814/Chinese-Chess/issues
- **项目仓库**: https://github.com/ken780814/Chinese-Chess

---

© 2026 Chinese Chess Project. MIT License.
