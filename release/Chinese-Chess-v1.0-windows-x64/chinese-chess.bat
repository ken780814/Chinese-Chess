@echo off
chcp 65001 >nul
title 中国象棋 - Chinese Chess
cd /d "%~dp0"
python main.py %*
pause
