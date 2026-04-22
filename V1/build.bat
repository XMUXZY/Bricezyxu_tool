@echo off
chcp 65001 >nul
title 游戏运营工具合集 - 打包工具

echo ========================================
echo   游戏运营工具合集 - EXE 打包脚本
echo ========================================
echo.

cd /d "%~dp0"

:: 检查 PyInstaller 是否安装
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo [!] 未检测到 PyInstaller，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo [x] 安装失败，请手动执行: pip install pyinstaller
        pause
        exit /b 1
    )
    echo [√] PyInstaller 安装成功
    echo.
)

:: 清理旧的构建产物
if exist "build" (
    echo [*] 清理旧构建目录...
    rmdir /s /q "build"
)
if exist "dist\游戏运营工具合集.exe" (
    echo [*] 清理旧的 exe...
    del /q "dist\游戏运营工具合集.exe"
)

echo [*] 开始打包...
echo.

pyinstaller --onefile --windowed --name "游戏运营工具合集" --add-data "pages;pages" main.py

if errorlevel 1 (
    echo.
    echo [x] 打包失败！请检查上方错误信息
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [√] 打包成功！
echo ========================================
echo.
echo   输出文件: %~dp0dist\游戏运营工具合集.exe
echo.

:: 打开输出文件夹
explorer "%~dp0dist"

pause
