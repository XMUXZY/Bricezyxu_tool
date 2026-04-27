@echo off
chcp 65001 >nul
title 游戏运营工具合集 - 打包工具

echo ========================================
echo   游戏运营工具合集 - EXE 打包脚本
echo ========================================
echo.

cd /d "%~dp0"

:: 检查 Python 是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] 未检测到 Python，请确认已安装 Python 并添加到 PATH
    pause
    exit /b 1
)

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

:: 检查运行时依赖
echo [*] 检查运行时依赖...
pip install customtkinter openpyxl >nul 2>&1
echo [√] 依赖已就绪
echo.

:: 清理旧的构建产物
if exist "build" (
    echo [*] 清理旧构建目录...
    rmdir /s /q "build"
)
if exist "dist" (
    echo [*] 清理旧 dist 目录...
    rmdir /s /q "dist"
)

echo [*] 开始打包（使用 app.spec 配置文件）...
echo.

:: 使用英文名 spec 文件，避免 cmd 中文编码问题
python -m PyInstaller app.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [x] 打包失败！请检查上方错误信息
    echo.
    echo 常见问题排查：
    echo   1. 确认已安装: pip install pyinstaller customtkinter openpyxl
    echo   2. 确认 game_data/ 目录存在且包含 JSON 文件
    echo   3. 尝试先运行 python main.py 确认程序正常
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [√] 打包成功！
echo ========================================
echo.
echo   输出文件: dist\游戏运营工具合集.exe
echo.
echo   提示：可直接将 exe 发送给其他人使用，无需安装 Python
echo.

:: 打开输出文件夹
explorer "dist"

pause
