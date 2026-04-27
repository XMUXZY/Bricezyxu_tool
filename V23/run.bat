@echo off
chcp 65001 >nul
title 游戏运营工具合集 - 开发运行

echo ========================================
echo   游戏运营工具合集 - 开发启动脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [*] 启动应用程序...
echo.

C:\Users\bricezyxu\.workbuddy\binaries\python\versions\3.14.3\python.exe main.py

if errorlevel 1 (
    echo.
    echo [!] 程序运行出错，请检查错误信息
    pause
    exit /b 1
)

echo.
echo [√] 程序已关闭
pause
