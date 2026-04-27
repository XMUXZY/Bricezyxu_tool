@echo off
chcp 65001 >nul
title 游戏运营工具合集 - 自动打包脚本

echo ============================================
echo   游戏运营工具合集 - 自动打包
echo ============================================
echo.

:: 检查 Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 18+
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node -v') do echo [OK] Node.js 版本: %%i

:: 检查 Rust
where rustc >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Rust，请先安装 Rust
    echo 安装命令: winget install Rustlang.Rustup
    echo 或访问: https://rustup.rs/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('rustc --version') do echo [OK] %%i

:: 进入项目目录
cd /d "%~dp0"
echo [OK] 工作目录: %cd%
echo.

:: 安装前端依赖
echo [1/3] 检查并安装前端依赖...
if not exist "node_modules" (
    echo      首次运行，正在安装依赖（可能需要几分钟）...
    call npm install
    if %errorlevel% neq 0 (
        echo [错误] npm install 失败
        pause
        exit /b 1
    )
) else (
    echo      node_modules 已存在，跳过安装
)
echo.

:: 前端构建
echo [2/3] 构建前端资源...
call npm run build
if %errorlevel% neq 0 (
    echo [错误] 前端构建失败，请检查代码是否有 TypeScript 错误
    pause
    exit /b 1
)
echo [OK] 前端构建完成
echo.

:: Tauri 打包
echo [3/3] 编译 Rust 后端并打包...
echo      首次编译可能需要 5-10 分钟，请耐心等待...
echo.
call npx tauri build

:: 检查产物是否生成（而非依赖退出码）
if exist "src-tauri\target\release\游戏运营工具合集.exe" (
    echo.
    echo ============================================
    echo   打包完成！
    echo ============================================
    echo.
    echo 产物位置:
    echo   EXE:  src-tauri\target\release\游戏运营工具合集.exe
    echo   NSIS: src-tauri\target\release\bundle\nsis\
    echo.
    explorer "src-tauri\target\release"
) else (
    echo.
    echo [错误] Tauri 打包失败，未找到产物 EXE
    echo 常见原因:
    echo   - 未安装 Visual Studio Build Tools (C++ 桌面开发)
    echo   - Rust 工具链不完整，尝试: rustup update
)

pause
