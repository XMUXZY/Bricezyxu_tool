@echo off
chcp 936 >nul
title Release Tool

echo ============================================
echo   Game Ops Toolkit - Release
echo ============================================
echo.

:: Git repo root is one level up
cd /d "%~dp0\.."

set /p VERSION=Enter version (e.g. 2.1.0): 
if "%VERSION%"=="" (
    echo [Error] Version cannot be empty
    pause
    exit /b 1
)

echo.
echo Will release v%VERSION%
echo   1. Update version in config files
echo   2. Git commit
echo   3. Delete old tag if exists
echo   4. Create new tag and push to GitHub
echo.
set /p CONFIRM=Confirm? (Y/N): 
if /i not "%CONFIRM%"=="Y" (
    echo Cancelled
    pause
    exit /b 0
)

echo.
echo [1/5] Updating version to %VERSION% ...

powershell -Command "(Get-Content 'V23-tauri\src-tauri\tauri.conf.json' -Encoding UTF8) -replace '\"version\": \"[^\"]+\"', '\"version\": \"%VERSION%\"' | Set-Content 'V23-tauri\src-tauri\tauri.conf.json' -Encoding UTF8"
powershell -Command "(Get-Content 'V23-tauri\package.json' -Encoding UTF8) -replace '\"version\": \"[^\"]+\"', '\"version\": \"%VERSION%\"' | Set-Content 'V23-tauri\package.json' -Encoding UTF8"
powershell -Command "(Get-Content 'V23-tauri\src-tauri\Cargo.toml' -Encoding UTF8) -replace 'version = \"[^\"]+\"', 'version = \"%VERSION%\"' | Set-Content 'V23-tauri\src-tauri\Cargo.toml' -Encoding UTF8"

echo [OK] Version updated
echo.

echo [2/5] Git commit ...
git add .
git commit -m "v%VERSION%"
echo.

echo [3/5] Removing old tag v%VERSION% if exists ...
git tag -d v%VERSION% 2>nul
git push github :refs/tags/v%VERSION% 2>nul
echo.

echo [4/5] Creating tag v%VERSION% ...
git tag v%VERSION%
echo.

echo [5/5] Pushing to GitHub ...
git push github master --tags
if %errorlevel% neq 0 (
    echo [Error] Push failed, check network or GitHub credentials
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Released v%VERSION% successfully!
echo ============================================
echo.
echo GitHub Actions is building (~5-10 min)
echo Progress: https://github.com/XMUXZY/Bricezyxu_tool/actions
echo Releases: https://github.com/XMUXZY/Bricezyxu_tool/releases
echo.
pause
