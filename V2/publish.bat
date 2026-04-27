@echo off
chcp 65001 >nul
title 游戏运营工具合集 - 发布更新包
setlocal EnableDelayedExpansion

echo ========================================
echo   游戏运营工具合集 - 发布更新包脚本
echo ========================================
echo.

cd /d "%~dp0"

:: 读取版本号
for /f "tokens=2 delims='""'" %%a in ('findstr "CURRENT_VERSION" updater.py') do set VERSION=%%a
echo [*] 当前版本号: %VERSION%
echo.

:: 创建发布目录
set RELEASE_DIR=release
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"

:: ========================================
:: 第 1 步：打包 EXE（使用 PyInstaller）
:: ========================================
echo [*] 正在打包 EXE...
echo.

:: 清理旧的构建产物
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

python -m PyInstaller app.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [x] EXE 打包失败！请检查上方错误信息
    pause
    exit /b 1
)

:: 复制 EXE 到发布目录
copy /y "dist\游戏运营工具合集.exe" "%RELEASE_DIR%\update.exe"
echo [√] EXE 已复制到 release\update.exe
echo.

:: ========================================
:: 第 2 步：打包源码更新包（给源码模式用户）
:: ========================================
echo [*] 正在打包源码更新包 update.zip ...

python -c "
import zipfile, os, sys

exclude_dirs = {'__pycache__', '_update_cache', 'build', 'dist', 'release', '.git', '参考文件'}
exclude_exts = {'.pyc', '.pyz', '.toc', '.exe', '.spec'}
exclude_files = {'publish.bat', 'build.bat', 'run.bat', '.python-version', '.gitignore'}

with zipfile.ZipFile('release/update.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            filepath = os.path.join(root, f)
            _, ext = os.path.splitext(f)
            if ext in exclude_exts:
                continue
            if f in exclude_files:
                continue
            if f.endswith('.md') and root == '.':
                continue
            arcname = filepath[2:]
            zf.write(filepath, arcname)

print('源码包打包完成')
"

if errorlevel 1 (
    echo [x] 源码包打包失败！
    pause
    exit /b 1
)

:: ========================================
:: 第 3 步：计算哈希并生成 version.json
:: ========================================
echo [*] 正在生成 version.json ...

python -c "
import hashlib, os, json, datetime

# 计算 EXE 的 SHA256 和大小
exe_path = 'release/update.exe'
h_exe = hashlib.sha256()
with open(exe_path, 'rb') as f:
    while True:
        chunk = f.read(8192)
        if not chunk:
            break
        h_exe.update(chunk)
exe_hash = h_exe.hexdigest()
exe_size = os.path.getsize(exe_path)
print(f'EXE SHA256: {exe_hash}')
print(f'EXE 大小: {exe_size} bytes')

# 计算源码包的 SHA256 和大小
zip_path = 'release/update.zip'
h_zip = hashlib.sha256()
with open(zip_path, 'rb') as f:
    while True:
        chunk = f.read(8192)
        if not chunk:
            break
        h_zip.update(chunk)
zip_hash = h_zip.hexdigest()
zip_size = os.path.getsize(zip_path)
print(f'ZIP SHA256: {zip_hash}')
print(f'ZIP 大小: {zip_size} bytes')

# 生成 version.json
version_info = {
    'version': '%VERSION%',
    'release_date': datetime.date.today().isoformat(),
    'download_url': '',
    'changelog': [
        '新增：法宝升阶养成计算器',
        '新增：占测养成计算器',
        '优化：移除法宝升阶计算弹窗，结果直接显示在页面内',
        '优化：支持 EXE 在线自动更新'
    ],
    'force_update': False,
    'min_version': '1.0.0',
    'file_hash': zip_hash,
    'file_size': zip_size,
    'exe_download_url': '',
    'exe_hash': exe_hash,
    'exe_size': exe_size
}
with open('release/version.json', 'w', encoding='utf-8') as f:
    json.dump(version_info, f, ensure_ascii=False, indent=2)
print('version.json 已生成')
"

if errorlevel 1 (
    echo [x] version.json 生成失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [√] 发布包准备完成！
echo ========================================
echo.
echo   输出目录: release\
echo   - update.exe      (EXE 更新包 - 同事直接更新)
echo   - update.zip      (源码更新包 - 源码模式用户)
echo   - version.json    (版本信息)
echo.
echo   下一步操作：
echo   1. 将 release\ 下的 3 个文件上传到 Gitee 仓库：
echo      https://gitee.com/XMU_xzy/game-ops-toolkit-releases
echo   2. 确保文件在 master 分支的根目录下
echo   3. 同事们打开软件后即可自动检测到更新
echo.

:: 打开输出目录
explorer "%RELEASE_DIR%"

pause
