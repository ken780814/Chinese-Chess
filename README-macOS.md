# 中国象棋 - macOS 版本
# Chinese Chess - macOS Version

## 系统要求 / System Requirements

- macOS 10.13 (High Sierra) 或更高
- 256MB 内存以上
- 100MB 磁盘空间
- macOS 10.13 (High Sierra) or later
- 256MB RAM or more
- 100MB disk space

## 下载 / Download

**V2.0 版本**: [下载 macOS 版本](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.0)

## 安装方式 / Installation

### 方式一：直接运行 / Method 1: Run Directly

```bash
brew install python@3.11
pip3 install PyQt5 pygame pillow
# 或使用 requirements.txt
pip3 install -r requirements.txt

# 克隆并运行
git clone https://github.com/ken780814/Chinese-Chess.git
cd Chinese-Chess
python3 main.py
```

### 方式二：使用打包脚本 / Method 2: Use Package Script

```bash
bash scripts/package_macos.sh
# 生成的 .app 在 dist/ 目录
open "dist/中国象棋.app"
```

## 运行参数 / Parameters

```bash
python3 main.py --mode=endgame  # 残局模式
python3 main.py --no-sound      # 静音模式
```

## 功能特性 / Features

- ✅ 四级 AI 难度
- ✅ 12 个经典残局
- ✅ 计时系统
- ✅ 音效支持
- ✅ 图片棋子
- ✅ 窗口缩放自适应

## 卸载 / Uninstall

```bash
rm -rf Chinese-Chess
```

---

© 2026 Chinese Chess Project. MIT License.
