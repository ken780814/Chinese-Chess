# 中国象棋 - Windows 版本
# Chinese Chess - Windows Version

## 系统要求 / System Requirements

- Windows 10/11 (64位)
- DirectX 9.0c 或更高
- 256MB 内存以上
- Windows 10/11 (64-bit)
- DirectX 9.0c or higher
- 256MB RAM or more

## 运行方式 / How to Run

### 方式一：双击运行 / Method 1: Double-click to Run
直接双击 `chinese-chess.exe` 或 `chinese-chess.bat`
Double-click `chinese-chess.exe` or `chinese-chess.bat`

### 方式二：命令行运行 / Method 2: Command Line
```cmd
chinese-chess.exe              # 开始游戏
chinese-chess.exe --mode=endgame  # 残局挑战
chinese-chess.exe --no-sound   # 禁用音效
```

## 安装 / Installation

### 方式一：手动安装 / Method 1: Manual Installation
1. 解压下载的压缩包
2. 双击 `chinese-chess.exe` 运行
3. 可选：右键桌面快捷方式 → 固定到任务栏
1. Extract the downloaded archive
2. Double-click `chinese-chess.exe` to run
3. Optional: Right-click desktop shortcut → Pin to taskbar

### 方式二：使用安装脚本 / Method 2: Using Install Script
```powershell
# 以管理员身份运行 PowerShell
cd Chinese-Chess-v1.0-windows-x64
python install_windows.py
```

## 卸载 / Uninstallation

### 方式一：手动卸载 / Method 1: Manual Uninstallation
1. 删除游戏文件夹
2. 删除桌面快捷方式（如有）
1. Delete the game folder
2. Delete desktop shortcut (if any)

### 方式二：使用卸载脚本 / Method 2: Using Uninstall Script
```powershell
python install_windows.py uninstall
```

## 文件说明 / File Description

| 文件/文件夹 | 说明 |
|-------------|------|
| `chinese-chess.exe` | 主程序（打包版本） |
| `chinese-chess.bat` | 启动脚本 |
| `assets/` | 资源文件（图标、音效） |
| `engine/` | 游戏引擎 |
| `gui/` | 图形界面 |
| `data/` | 数据文件 |
| `main.py` | 主程序源码 |
| `README.md` | 说明文档 |

| File/Folder | Description |
|-------------|------|
| `chinese-chess.exe` | Main executable (packaged) |
| `chinese-chess.bat` | Startup script |
| `assets/` | Resource files (icons, sounds) |
| `engine/` | Game engine |
| `gui/` | Graphics interface |
| `data/` | Data files |
| `main.py` | Main program source |
| `README.md` | Documentation |

## 常见问题 / FAQ

### Q: 运行时提示缺少 DLL
A: 请安装 [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
**Q: DLL missing error when running**
A: Please install [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Q: 黑屏或无法显示
A: 请确保显卡驱动已更新，支持 OpenGL
**Q: Black screen or display issues**
A: Ensure your graphics driver is updated and supports OpenGL

### Q: 音效不播放
A: 检查系统音量设置，或运行 `chinese-chess.exe --no-sound` 禁用音效
**Q: Sound not playing**
A: Check system volume settings, or run `chinese-chess.exe --no-sound` to disable sound

## 许可证 / License

MIT License
