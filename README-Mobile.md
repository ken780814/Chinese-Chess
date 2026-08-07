# 中国象棋 - 移动端版本 (Android/iOS)

## 系统要求

### Android
- Android 5.0+ (API 21+)
- 1GB 内存以上
- 100MB 存储空间

### iOS
- iOS 12.0+
- 1GB 内存以上
- 100MB 存储空间

## 功能特性

- ✅ 完整中国象棋规则
- ✅ 四级 AI 难度
- ✅ 12 个经典残局
- ✅ 计时系统 (60秒/方)
- ✅ 触屏操作优化
- ✅ 屏幕自适应

## 屏幕自适应

- 自动适配不同屏幕尺寸
- 竖屏设计，适合手机操作
- 触控友好，点击即走棋
- 高清显示支持

## 运行方式

### 方式一：直接运行（需要 Python 环境）
```bash
pip3 install -r requirements-mobile.txt
python3 main_mobile.py
```

### 方式二：打包为 APK（Android）
```bash
# 安装 Buildozer
pip3 install buildozer cython

# 打包
bash scripts/package_mobile.sh
```

### 方式三：打包为 IPA（iOS）
```bash
# 需要 macOS 和 Xcode
bash scripts/package_mobile.sh
```

## 触摸控制

| 操作 | 说明 |
|------|------|
| 点击棋子 | 选中棋子 |
| 点击目标格 | 移动棋子 |
| 点击按钮 | 切换难度/重新开始 |

## 技术栈

- **GUI 框架**: Kivy
- **音频**: pygame
- **打包工具**: Buildozer
- **开发语言**: Python 3.8+

## 许可证

MIT License
