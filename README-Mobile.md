# 中国象棋 - 移动端版本
# Chinese Chess - Mobile Version

## 系统要求 / System Requirements

### Android
- Android 5.0+ (API 21+)
- 1GB 内存以上
- 100MB 存储空间

### iOS
- iOS 12.0+
- 1GB 内存以上
- 100MB 存储空间

### Android
- Android 5.0+ (API 21+)
- 1GB RAM or more
- 100MB storage

### iOS
- iOS 12.0+
- 1GB RAM or more
- 100MB storage

## 功能特性 / Features

- ✅ 完整中国象棋规则
- ✅ 四级 AI 难度
- ✅ 12 个经典残局
- ✅ 计时系统 (60秒/方)
- ✅ 触屏操作优化
- ✅ 屏幕自适应

- ✅ Complete Chinese chess rules
- ✅ 4-level AI difficulty
- ✅ 12 classic endgames
- ✅ Timer system (60s per side)
- ✅ Touch control optimized
- ✅ Screen adaptation

## 屏幕自适应 / Screen Adaptation

- 自动适配不同屏幕尺寸
- 竖屏设计，适合手机操作
- 触控友好，点击即走棋
- 高清显示支持

- Auto-adapt to different screen sizes
- Portrait design, suitable for mobile
- Touch-friendly, tap to move
- HD display support

## 运行方式 / How to Run

### 方式一：直接运行 / Method 1: Direct Run
```bash
pip3 install -r requirements-mobile.txt
python3 main_mobile.py
```

### 方式二：打包为 APK / Method 2: Build APK (Android)
```bash
# 安装 Buildozer
pip3 install buildozer cython

# 打包
bash scripts/package_mobile.sh android
```

### 方式三：打包为 IPA / Method 3: Build IPA (iOS)
```bash
# 需要 macOS 和 Xcode
bash scripts/package_mobile.sh ios
```

## 触摸控制 / Touch Controls

| 操作 | 说明 |
|------|------|
| 点击棋子 | 选中棋子 |
| 点击目标格 | 移动棋子 |
| 点击按钮 | 切换难度/重新开始 |

| Action | Description |
|------|------|
| Tap piece | Select piece |
| Tap target | Move piece |
| Tap button | Switch difficulty / restart |

## 技术栈 / Tech Stack

- **GUI 框架**: Kivy
- **音频**: pygame
- **打包工具**: Buildozer
- **开发语言**: Python 3.8+

- **GUI Framework**: Kivy
- **Audio**: pygame
- **Packaging**: Buildozer
- **Language**: Python 3.8+

## 常见问题 / FAQ

### Q: 为什么没有预编译的 APK/IPA？
A: 由于移动端打包需要特定的开发环境（Android SDK / Xcode），目前仅提供源码和打包脚本，用户可自行编译。

**Q: Why no pre-compiled APK/IPA?**
A: Mobile packaging requires specific development environments (Android SDK / Xcode), so only source code and build scripts are provided for users to compile.

### Q: 如何编译 APK？
A: 
```bash
pip3 install buildozer cython
buildozer android debug
```

**Q: How to compile APK?**
A: 
```bash
pip3 install buildozer cython
buildozer android debug
```

### Q: 如何编译 IPA？
A: 需要 macOS 系统：
```bash
pip3 install buildozer cython
buildozer ios debug
```

**Q: How to compile IPA?**
A: Requires macOS system:
```bash
pip3 install buildozer cython
buildozer ios debug
```

## 许可证 / License

MIT License
