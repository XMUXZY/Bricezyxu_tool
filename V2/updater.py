"""
在线更新模块
支持 EXE 打包模式和源码模式的版本检测、下载、自动更新与重启
"""

import json
import os
import sys
import shutil
import subprocess
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable, Dict, Any

try:
    import urllib.request as urlopen_lib
    from urllib.error import URLError, HTTPError
except ImportError:
    pass


# ============================================================
# 配置区
# ============================================================

# 远程版本信息文件 URL
UPDATE_SERVER_URL = "https://gitee.com/XMU_xzy/game-ops-toolkit-releases/raw/master/"

# 版本信息文件名
VERSION_FILE = "version.json"

# 本地版本号（每次发版时修改此值）
CURRENT_VERSION = "1.1.0"


# ============================================================
# 运行环境检测
# ============================================================

def is_frozen() -> bool:
    """判断是否运行在 PyInstaller 打包的 EXE 环境中"""
    return getattr(sys, 'frozen', False)


def get_exe_path() -> Optional[Path]:
    """获取当前 EXE 的路径（仅在 frozen 模式下有效）"""
    if is_frozen():
        return Path(sys.executable)
    return None


def get_app_dir() -> Path:
    """
    获取应用根目录
    - EXE 模式：EXE 所在目录
    - 源码模式：main.py 所在目录
    """
    if is_frozen():
        return Path(sys.executable).parent
    return Path(__file__).parent


# 应用根目录
APP_ROOT = get_app_dir()

# 更新缓存目录（放在 EXE 同级目录下）
CACHE_DIR = APP_ROOT / "_update_cache"


# ============================================================
# 数据结构
# ============================================================

class VersionInfo:
    """远程版本信息"""
    def __init__(self, data: Dict[str, Any]):
        self.version = data.get("version", "0.0.0")
        self.release_date = data.get("release_date", "")
        self.download_url = data.get("download_url", "")
        self.changelog = data.get("changelog", [])
        self.force_update = data.get("force_update", False)
        self.min_version = data.get("min_version", "0.0.0")
        self.file_hash = data.get("file_hash", "")  # SHA256 校验
        self.file_size = data.get("file_size", 0)
        # EXE 更新专用字段
        self.exe_download_url = data.get("exe_download_url", "")
        self.exe_hash = data.get("exe_hash", "")
        self.exe_size = data.get("exe_size", 0)

    def __repr__(self):
        return f"VersionInfo({self.version})"


# ============================================================
# 核心功能
# ============================================================

def get_local_version() -> str:
    """获取本地当前版本号"""
    return CURRENT_VERSION


def parse_version(v: str) -> tuple:
    """将版本字符串解析为可比较的元组"""
    parts = v.replace("v", "").split(".")
    result = []
    for p in parts:
        num = ""
        for c in p:
            if c.isdigit():
                num += c
            else:
                break
        result.append(int(num) if num else 0)
    return tuple(result) if result else (0,)


def compare_versions(v1: str, v2: str) -> int:
    """比较两个版本号：1 = v1 > v2, 0 = v1 == v2, -1 = v1 < v2"""
    p1, p2 = parse_version(v1), parse_version(v2)
    max_len = max(len(p1), len(p2))
    p1 = p1 + (0,) * (max_len - len(p1))
    p2 = p2 + (0,) * (max_len - len(p2))
    if p1 > p2:
        return 1
    elif p1 < p2:
        return -1
    return 0


def fetch_remote_version(timeout: int = 10) -> Optional[VersionInfo]:
    """从远程服务器获取最新版本信息"""
    url = UPDATE_SERVER_URL.rstrip("/") + "/" + VERSION_FILE
    try:
        req = urlopen_lib.Request(url, headers={
            "User-Agent": "GameOpsToolkit-Updater/1.0"
        })
        with urlopen_lib.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return VersionInfo(data)
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as e:
        print(f"[Updater] 获取版本信息失败: {e}")
        return None


def check_update() -> Optional[VersionInfo]:
    """检查是否有新版本可用"""
    remote = fetch_remote_version()
    if remote is None:
        return None
    cmp = compare_versions(remote.version, get_local_version())
    if cmp > 0:
        return remote
    return None


# ============================================================
# 下载功能
# ============================================================

def _compute_sha256(file_path: Path) -> str:
    """计算文件的 SHA256 哈希"""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _download_file(
    url: str,
    save_path: Path,
    expected_hash: str = "",
    expected_size: int = 0,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> bool:
    """通用文件下载（带校验）"""
    try:
        req = urlopen_lib.Request(url, headers={
            "User-Agent": "GameOpsToolkit-Updater/1.0"
        })
        with urlopen_lib.urlopen(req, timeout=120) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            chunks = []

            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                chunks.append(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total)

            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "wb") as f:
                for c in chunks:
                    f.write(c)

        # 文件大小校验
        if expected_size > 0 and save_path.stat().st_size != expected_size:
            print(f"[Updater] 文件大小不匹配: {save_path.stat().st_size} != {expected_size}")
            save_path.unlink(missing_ok=True)
            return False

        # SHA256 校验
        if expected_hash:
            actual_hash = _compute_sha256(save_path)
            if actual_hash.lower() != expected_hash.lower():
                print(f"[Updater] 文件哈希不匹配")
                save_path.unlink(missing_ok=True)
                return False

        return True

    except Exception as e:
        print(f"[Updater] 下载失败: {e}")
        return False


# ============================================================
# EXE 模式更新（核心新增）
# ============================================================

def _get_exe_download_url(remote: VersionInfo) -> str:
    """获取 EXE 下载地址"""
    if remote.exe_download_url:
        return remote.exe_download_url
    # 默认约定：远程仓库根目录下的 update.exe
    return UPDATE_SERVER_URL.rstrip("/") + "/update.exe"


def download_exe_update(
    remote: VersionInfo,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> Optional[Path]:
    """下载新版 EXE 到缓存目录"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    new_exe_path = CACHE_DIR / "update.exe"

    url = _get_exe_download_url(remote)
    success = _download_file(
        url=url,
        save_path=new_exe_path,
        expected_hash=remote.exe_hash,
        expected_size=remote.exe_size,
        progress_callback=progress_callback,
    )

    return new_exe_path if success else None


def apply_exe_update(new_exe_path: Path) -> bool:
    """
    通过 bat 脚本替换当前 EXE 并重启。
    流程：
    1. 生成一个 bat 脚本
    2. bat 脚本等待当前 EXE 退出
    3. 备份旧 EXE → 用新 EXE 覆盖 → 启动新 EXE → 删除自身
    """
    current_exe = get_exe_path()
    if current_exe is None:
        print("[Updater] 非 EXE 模式，无法执行 EXE 替换")
        return False

    exe_dir = current_exe.parent
    exe_name = current_exe.name
    backup_name = exe_name.replace(".exe", "_backup.exe")
    bat_path = CACHE_DIR / "_do_update.bat"

    # 生成替换脚本
    bat_content = f'''@echo off
chcp 65001 >nul
title 正在更新...
echo 正在更新，请稍候...

:: 等待原程序退出（最多等 30 秒）
set /a count=0
:wait_loop
tasklist /FI "PID eq %PARENT_PID%" 2>nul | find /I "{exe_name}" >nul
if not errorlevel 1 (
    timeout /t 1 /nobreak >nul
    set /a count+=1
    if %count% lss 30 goto wait_loop
)

:: 额外等 1 秒确保文件锁释放
timeout /t 1 /nobreak >nul

:: 备份旧 EXE
if exist "{exe_dir}\\{exe_name}" (
    if exist "{exe_dir}\\{backup_name}" del /f /q "{exe_dir}\\{backup_name}"
    move /y "{exe_dir}\\{exe_name}" "{exe_dir}\\{backup_name}"
)

:: 复制新 EXE
copy /y "{new_exe_path}" "{exe_dir}\\{exe_name}"

:: 启动新程序
start "" "{exe_dir}\\{exe_name}"

:: 清理备份和缓存
timeout /t 3 /nobreak >nul
if exist "{exe_dir}\\{backup_name}" del /f /q "{exe_dir}\\{backup_name}"
if exist "{CACHE_DIR}" rmdir /s /q "{CACHE_DIR}"

:: 删除自身
del /f /q "%~f0"
'''
    # 将 %PARENT_PID% 替换为实际的 PID
    bat_content = bat_content.replace("%PARENT_PID%", str(os.getpid()))

    bat_path.parent.mkdir(parents=True, exist_ok=True)
    with open(bat_path, "w", encoding="gbk", errors="replace") as f:
        f.write(bat_content)

    # 启动 bat 脚本（隐藏窗口）
    subprocess.Popen(
        ["cmd", "/c", str(bat_path)],
        cwd=str(exe_dir),
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    return True


# ============================================================
# 源码模式更新（保留原有逻辑）
# ============================================================

def download_source_update(
    remote: VersionInfo,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> Optional[Path]:
    """下载源码更新包（zip）"""
    download_url = remote.download_url or (UPDATE_SERVER_URL.rstrip("/") + "/update.zip")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    save_path = CACHE_DIR / "update.zip"

    success = _download_file(
        url=download_url,
        save_path=save_path,
        expected_hash=remote.file_hash,
        expected_size=remote.file_size,
        progress_callback=progress_callback,
    )

    return save_path if success else None


def apply_source_update(zip_path: Path, backup: bool = True) -> bool:
    """将下载的源码更新包解压并覆盖到应用目录"""
    try:
        if backup:
            backup_dir = APP_ROOT.parent / f"{APP_ROOT.name}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            _copy_dir(APP_ROOT, backup_dir, exclude={"__pycache__", "_update_cache", "*.pyc"})

        extract_dir = CACHE_DIR / "_extracted"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_dir)

        app_in_extract = _find_app_dir(extract_dir)
        if app_in_extract is None:
            print("[Updater] 无法在更新包中找到应用目录")
            return False

        _copy_dir(app_in_extract, APP_ROOT, exclude={"__pycache__"})

        shutil.rmtree(extract_dir, ignore_errors=True)
        zip_path.unlink(missing_ok=True)

        print(f"[Updater] 源码更新成功，已应用至 {APP_ROOT}")
        return True

    except Exception as e:
        print(f"[Updater] 应用源码更新失败: {e}")
        return False


def restart_app():
    """重启应用程序"""
    print("[Updater] 正在重启应用...")
    if is_frozen():
        # EXE 模式：重启 EXE 自身
        exe_path = get_exe_path()
        if exe_path:
            subprocess.Popen([str(exe_path)], cwd=str(exe_path.parent))
    else:
        # 源码模式：用 Python 重新运行 main.py
        python = sys.executable
        main_script = APP_ROOT / "main.py"
        subprocess.Popen([python, str(main_script)], cwd=str(APP_ROOT))
    sys.exit(0)


def cleanup_cache():
    """清理更新缓存"""
    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR, ignore_errors=True)


# ============================================================
# 内部工具函数
# ============================================================

def _copy_dir(src: Path, dst: Path, exclude: set = None):
    """递归复制目录，排除指定模式"""
    if exclude is None:
        exclude = set()
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        name = item.name
        skip = False
        for pattern in exclude:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    skip = True
                    break
            else:
                if name == pattern:
                    skip = True
                    break
        if skip:
            continue
        target = dst / name
        if item.is_dir():
            _copy_dir(item, target, exclude)
        else:
            shutil.copy2(item, target)


def _find_app_dir(base: Path) -> Optional[Path]:
    """在解压目录中查找应用根目录"""
    if (base / "main.py").exists():
        return base
    for child in base.iterdir():
        if child.is_dir() and (child / "main.py").exists():
            return child
    return None


# ============================================================
# 统一更新入口（自动判断 EXE / 源码模式）
# ============================================================

def do_update(
    on_progress: Optional[Callable[[str, int, int], None]] = None,
    on_error: Optional[Callable[[str], None]] = None,
) -> bool:
    """
    执行完整的一键更新流程（自动判断运行模式）。
    EXE 模式：下载新 EXE → bat 替换 → 退出（bat 负责重启）
    源码模式：下载 zip → 解压覆盖 → 返回 True（调用方重启）
    """
    def report(msg: str, current: int = 0, total: int = 0):
        if on_progress:
            on_progress(msg, current, total)
        print(f"[Updater] {msg}")

    # Step 1: 检查更新
    report("正在检查更新...")
    remote = check_update()
    if remote is None:
        report("已是最新版本")
        if on_error:
            on_error("已是最新版本，无需更新")
        return False

    def download_cb(downloaded, total):
        report(
            f"下载中... {_format_size(downloaded)} / {_format_size(total)}",
            downloaded, total
        )

    if is_frozen():
        # ---- EXE 模式 ----
        report(f"发现新版本 v{remote.version}，正在下载新程序...")
        new_exe = download_exe_update(remote, progress_callback=download_cb)
        if new_exe is None:
            report("下载失败")
            if on_error:
                on_error("下载更新包失败，请检查网络连接")
            return False

        report("正在准备更新...")
        if not apply_exe_update(new_exe):
            report("更新准备失败")
            if on_error:
                on_error("更新安装失败")
            return False

        report("更新完成，程序即将重启...")
        return True  # 调用方应在收到 True 后退出程序

    else:
        # ---- 源码模式 ----
        report(f"发现新版本 v{remote.version}，正在下载...")
        zip_path = download_source_update(remote, progress_callback=download_cb)
        if zip_path is None:
            report("下载失败")
            if on_error:
                on_error("下载更新包失败，请检查网络连接")
            return False

        report("正在安装更新...")
        if not apply_source_update(zip_path):
            report("安装失败")
            if on_error:
                on_error("更新安装失败，可能文件被占用")
            return False

        report("更新完成，即将重启...")
        return True


def _format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
