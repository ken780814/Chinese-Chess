[app]
title = Chinese Chess
package.name = chinese_chess
package.domain = org.chinesechess
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.0.0
requirements = python3,kivy,pygame,pillow
orientation = portrait
android.api = 31
android.minapi = 21
android.ndk = 23b
log_level = 2
p4a.keep_venv = 1

[buildozer]
default = android

[android]
permissions =
icon = assets/icon.png
apptheme = @android:style/Theme.NoTitleBar
splash = assets/icon.png
