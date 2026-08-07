#!/bin/bash
# 中国象棋 - Android 构建配置

# 项目配置
app_name = ChineseChess
package.name = chinese_chess
package.domain = org.chinesechess
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy,pygame
orientation = portrait
android.api = 31
android.minapi = 21
android.ndk = 23b
android.sdk = 31
log_level = 2
wheels = 
p4a.keep_venv = 1

# 权限
android.permissions =

# 图标
android.icon = assets/icon.png
android.apptheme = @android:style/Theme.NoTitleBar

# 启动画面
android.splash = assets/icon.png
