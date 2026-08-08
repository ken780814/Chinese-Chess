# 中国象棋 - 安装与启动指南
# Chinese Chess - Installation & Launch Guide

## 📦 安装方式 / Installation

### 方法一：使用 apt 安装（推荐）/ Method 1: Use apt (Recommended)
```bash
# 下载 DEB 包
wget https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/chinese-chess_1.0.0_amd64.deb

# 安装（自动处理依赖）
sudo apt install ./chinese-chess_1.0.0_amd64.deb
```

### 方法二：使用 dpkg 安装 / Method 2: Use dpkg
```bash
# 下载 DEB 包
wget https://github.com/ken780814/Chinese-Chess/releases/download/v1.0/chinese-chess_1.0.0_amd64.deb

# 安装
sudo dpkg -i chinese-chess_1.0.0_amd64.deb

# 修复依赖
sudo apt-get install -f
```

---

## 🚀 启动方式 / How to Launch

### 方法一：桌面启动器 / Method 1: Desktop Launcher
```
点击桌面或应用菜单中的 "中国象棋" 或 "Chinese Chess" 图标
Click "Chinese Chess" in your application menu or desktop
```

### 方法二：命令行启动 / Method 2: Command Line
```bash
# 启动游戏
chinese-chess

# 启动残局挑战模式
chinese-chess --mode=endgame

# 禁用音效启动
chinese-chess --no-sound

# 查看帮助
chinese-chess --help
```

### 方法三：通过应用程序目录启动 / Method 3: From Application Directory
```bash
/usr/bin/chinese-chess
```

---

## 🎮 游戏控制 / Game Controls

### 鼠标操作 / Mouse Controls
| 操作 | 说明 |
|------|------|
| 点击棋子 | 选中棋子 |
| 点击绿点 | 移动到目标位置 |
| 点击按钮 | 切换模式/难度 |

### 键盘快捷键 / Keyboard Shortcuts
| 快捷键 | 功能 |
|--------|------|
| `N` | 新游戏 |
| `R` | 重新开始 |
| `Esc` | 返回主菜单 |

---

## 📂 安装位置 / Installation Location

| 文件类型 | 路径 |
|----------|------|
| 主程序 | `/usr/bin/chinese-chess` |
| 资源文件 | `/usr/share/chinese-chess/` |
| 桌面快捷方式 | `/usr/share/applications/chinese-chess.desktop` |
| 图标 | `/usr/share/icons/hicolor/256x256/apps/chinese-chess.png` |

---

## 🗑️ 卸载方式 / Uninstallation

```bash
# 使用 apt 卸载
sudo apt remove chinese-chess

# 清理配置文件
sudo apt autoremove
```

---

## ⚠️ 常见问题 / FAQ

### Q: 点击图标没反应
**A:** 尝试命令行启动查看详细错误：
```bash
chinese-chess 2>&1 | head -20
```

### Q: 显示黑屏或白屏
**A:** 检查 OpenGL 驱动：
```bash
glxinfo | grep "OpenGL"
```

### Q: 音效不播放
**A:** 使用 `--no-sound` 参数启动，或检查系统音量：
```bash
chinese-chess --no-sound
```

### Q: 提示缺少依赖
**A:** 安装所需依赖：
```bash
sudo apt-get install -y libgl1 libglib2.0-0 libsm6 libxtst6 libx11-6
```

---

## 📞 获取帮助 / Get Help

- GitHub Issues: https://github.com/ken780814/Chinese-Chess/issues
- Release 页面: https://github.com/ken780814/Chinese-Chess/releases
