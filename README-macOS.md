# 中国象棋 - macOS 版本

## 系统要求

- macOS 10.13 (High Sierra) 或更高
- 256MB 内存以上
- 100MB 磁盘空间

## 运行方式

### 方式一：双击运行
直接双击 `中国象棋.app`

### 方式二：命令行运行
```bash
open 中国象棋.app              # 启动游戏
open -a 中国象棋 --args --mode=endgame  # 残局挑战
```

### 方式三：命令行运行
```bash
./中国象棋.app/Contents/MacOS/chinese-chess
./中国象棋.app/Contents/MacOS/chinese-chess --mode=endgame
./中国象棋.app/Contents/MacOS/chinese-chess --no-sound
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--mode=endgame` | 残局挑战模式 |
| `--no-sound` | 禁用音效 |

## 常见问题

### Q: 提示"无法打开，因为无法验证开发者"
A: 右键点击 app → 打开 → 点击"打开"即可

### Q: 黑屏或无法显示
A: 请确保 macOS 已更新到最新版本，显卡驱动正常

### Q: 音效不播放
A: 检查系统音量设置，或运行 `--no-sound` 禁用音效

## 文件说明

| 文件 | 说明 |
|------|------|
| `中国象棋.app` | 应用程序包 |
| `README.md` | 说明文档 |

## 许可证

MIT License
