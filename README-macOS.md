# 中国象棋 - macOS 版本
# Chinese Chess - macOS Version

## 系统要求 / System Requirements

- macOS 10.13 (High Sierra) 或更高
- 256MB 内存以上
- 100MB 磁盘空间
- macOS 10.13 (High Sierra) or later
- 256MB RAM or more
- 100MB disk space

## 运行方式 / How to Run

### 方式一：双击运行 / Method 1: Double-click to Run
直接双击 `中国象棋.app`
Double-click `中国象棋.app`

### 方式二：命令行运行 / Method 2: Command Line
```bash
open 中国象棋.app
open -a 中国象棋 --args --mode=endgame
```

### 方式三：命令行运行 / Method 3: Run from Terminal
```bash
./中国象棋.app/Contents/MacOS/chinese-chess
./中国象棋.app/Contents/MacOS/chinese-chess --mode=endgame
./中国象棋.app/Contents/MacOS/chinese-chess --no-sound
```

## 参数说明 / Parameters

| 参数 | 说明 |
|------|------|
| `--mode=endgame` | 残局挑战模式 |
| `--no-sound` | 禁用音效 |

| Parameter | Description |
|------|------|
| `--mode=endgame` | Endgame challenge mode |
| `--no-sound` | Disable sound |

## 常见问题 / FAQ

### Q: 提示"无法打开，因为无法验证开发者"
A: 右键点击 app → 打开 → 点击"打开"即可
**Q: "App cannot be opened because the developer cannot be verified"**
A: Right-click the app → Open → Click "Open"

### Q: 黑屏或无法显示
A: 请确保 macOS 已更新到最新版本，显卡驱动正常
**Q: Black screen or display issues**
A: Ensure macOS is updated to the latest version and graphics driver is working

### Q: 音效不播放
A: 检查系统音量设置，或运行 `--no-sound` 禁用音效
**Q: Sound not playing**
A: Check system volume settings, or run with `--no-sound` to disable sound

## 文件说明 / File Description

| 文件 | 说明 |
|------|------|
| `中国象棋.app` | 应用程序包 |
| `README.md` | 说明文档 |

| File | Description |
|------|------|
| `中国象棋.app` | Application package |
| `README.md` | Documentation |

## 许可证 / License

MIT License
