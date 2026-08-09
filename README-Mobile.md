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

## 下载 / Download

**V2.0 版本**: [下载源码](https://github.com/ken780814/Chinese-Chess/releases/tag/v2.0)

> ⚠️ 移动端需要在本地编译 APK/IPA

## 功能特性 / Features

- ✅ 完整中国象棋规则
- ✅ 四级 AI 难度
- ✅ 12 个经典残局
- ✅ 计时系统
- ✅ 触屏操作
- ✅ 屏幕自适应

## 编译方式 / Build

### Android APK

```bash
# 安装依赖
pip3 install kivy pygame pillow
pip3 install buildozer cython

# 打包
buildozer android debug

# 输出: bin/chinese_chess-2.0.0-debug.apk
```

### iOS IPA

```bash
# 需要 macOS + Xcode
pip3 install kivy pygame pillow
pip3 install buildozer cython

buildozer ios debug
```

## 运行方式 / Run

```bash
# 直接运行 (需要 Kivy)
python3 main_mobile.py

# 或使用打包脚本
bash scripts/package_mobile.sh android
bash scripts/package_mobile.sh ios
```

## 技术栈 / Tech Stack

- **框架**: Kivy 2.2.0
- **引擎**: pygame
- **打包**: Buildozer
- **屏幕自适应**: 自动计算布局

## 项目结构 / Project Structure

```
Chinese-Chess/
├── main_mobile.py           # 移动端主程序 (Kivy)
├── buildozer.spec           # Android 构建配置
├── requirements-mobile.txt  # 移动端依赖
└── scripts/
    └── package_mobile.sh    # 打包脚本
```

---

© 2026 Chinese Chess Project. MIT License.
