"""
在线更新模块
支持版本检测、增量/全量下载、自动重启
"""

import json
import os
import sys
import shutil
import subprocess
import tempfile
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
# 配置区 - 根据你的实际情况修改
# ============================================================

# 远程版本信息文件 URL（托管在 GitHub/Gitee 等平台）
# 示例：将 version.json 放到仓库的 raw 分支或 release 中
UPDATE_SERVER_URL = "https://gitee.com/XMU_xzy/game-ops-toolkit-releases/raw/master/"

# 版本信息文件名（放在远程服务器根目录）
VERSION_FILE = "version.json"

# 下载包文件名（zip 格式，包含完整的 V1 目录内容）
DOWNLOAD_FILE = "update.zip"

# 本地版本号（每次发版时修改此值）
CURRENT_VERSION = "1.0.0"

# 应用根目录（自动检测，通常不需要改）
APP_ROOT = Path(__file__).parent.parent

# 更新缓存目录
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

    def __repr__(self):
        return f"VersionInfo({self.version})"


# ============================================================
# 核心功能
# ============================================================

def get_local_version() -> str:
    """获取本地当前版本号"""
    return CURRENT_VERSION


def parse_version(v: str) -> tuple:
    """将版本字符串解析为可比较的元组，如 '1.2.3' -> (1, 2, 3)"""
    parts = v.replace("v", "").split(".")
    result = []
    for p in parts:
        # 提取数字部分
        num = ""
        for c in p:
            if c.isdigit():
                num += c
            else:
                break
        result.append(int(num) if num else 0)
    return tuple(result) if result else (0,)


def compare_versions(v1: str, v2: str) -> int:
    """
    比较两个版本号
    返回：1 = v1 > v2, 0 = v1 == v2, -1 = v1 < v2
    """
    p1, p2 = parse_version(v1), parse_version(v2)
    # 补齐长度
    max_len = max(len(p1), len(p2))
    p1 = p1 + (0,) * (max_len - len(p1))
    p2 = p2 + (0,) * (max_len - len(p2))
    if p1 > p2:
        return 1
    elif p1 < p2:
        return -1
    return 0


def fetch_remote_version(timeout: int = 10) -> Optional[VersionInfo]:
    """
    从远程服务器获取最新版本信息
    返回 VersionInfo 对象，失败返回 None
    """
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
    """
    检查是否有新版本可用
    返回新版 VersionInfo 对象，无更新或失败返回 None
    """
    remote = fetch_remote_version()
    if remote is None:
        return None

    cmp = compare_versions(remote.version, get_local_version())
    if cmp > 0:
        return remote
    return None


def download_update(
    remote: VersionInfo,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> Optional[Path]:
    """
    下载更新包到本地缓存目录
    progress_callback(downloaded_bytes, total_bytes)
    返回下载文件的路径，失败返回 None
    """
    download_url = remote.download_url or (UPDATE_SERVER_URL.rstrip("/") + "/" + DOWNLOAD_FILE)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    save_path = CACHE_DIR / DOWNLOAD_FILE

    try:
        req = urlopen_lib.Request(download_url, headers={
            "User-Agent": "GameOpsToolkit-Updater/1.0"
        })
        with urlopen_lib.urlopen(req, timeout=60) as resp:
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

            with open(save_path, "wb") as f:
                for c in chunks:
                    f.write(c)

        # 文件大小校验
        if remote.file_size > 0 and save_path.stat().st_size != remote.file_size:
            print(f"[Updater] 文件大小不匹配: {save_path.stat().st_size} != {remote.file_size}")
            save_path.unlink(missing_ok=True)
            return None

        # SHA256 校验
        if remote.file_hash:
            _hash = _compute_sha256(save_path)
            if _hash.lower() != remote.file_hash.lower():
                print(f"[Updater] 文件哈希不匹配")
                save_path.unlink(missing_ok=True)
                return None

        return save_path

    except Exception as e:
        print(f"[Updater] 下载失败: {e}")
        return None


def apply_update(zip_path: Path, backup: bool = True) -> bool:
    """
    将下载的更新包解压并覆盖到应用目录
    成功返回 True
    """
    try:
        # 创建备份（可选）
        if backup:
            backup_dir = APP_ROOT.parent / f"{APP_ROOT.name}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            # 只备份核心代码文件，不备份 __pycache__ 和临时文件
            _copy_dir(APP_ROOT, backup_dir, exclude={"__pycache__", "_update_cache", "*.pyc"})

        # 解压覆盖
        extract_dir = CACHE_DIR / "_extracted"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_dir)

        # 查找解压后的应用目录（兼容不同打包结构）
        app_in_extract = _find_app_dir(extract_dir)
        if app_in_extract is None:
            print("[Updater] 无法在更新包中找到应用目录")
            return False

        # 复制文件覆盖到应用目录
        _copy_dir(app_in_extract, APP_ROOT, exclude={"__pycache__"})

        # 清理缓存
        shutil.rmtree(extract_dir, ignore_errors=True)
        zip_path.unlink(missing_ok=True)

        print(f"[Updater] 更新成功，已应用至 {APP_ROOT}")
        return True

    except Exception as e:
        print(f"[Updater] 应用更新失败: {e}")
        return False


def restart_app():
    """重启应用程序"""
    print("[Updater] 正在重启应用...")
    # 使用当前 Python 解释器重新启动主程序
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

def _compute_sha256(file_path: Path) -> str:
    """计算文件的 SHA256 哈希"""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _copy_dir(src: Path, dst: Path, exclude: set = None):
    """递归复制目录，排除指定模式"""
    if exclude is None:
        exclude = set()

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        name = item.name
        # 检查是否匹配排除规则
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
    """
    在解压目录中查找应用根目录
    优先找包含 main.py 的目录
    """
    # 检查自身是否就是目标
    if (base / "main.py").exists():
        return base

    # 遍历一级子目录
    for child in base.iterdir():
        if child.is_dir() and (child / "main.py").exists():
            return child

    return None


# ============================================================
# 便捷函数：一键更新流程
# ============================================================

def do_update(
    on_progress: Optional[Callable[[str, int, int], None]] = None,
    on_error: Optional[Callable[[str], None]] = None,
) -> bool:
    """
    执行完整的一键更新流程：
    检测版本 -> 下载 -> 安装 -> 重启
    返回是否成功触发重启
    """
    def report_progress(msg: str, current: int = 0, total: int = 0):
        if on_progress:
            on_progress(msg, current, total)
        print(f"[Updater] {msg}")

    # Step 1: 检查更新
    report_progress("正在检查更新...")
    remote = check_update()
    if remote is None:
        report_progress("已是最新版本")
        if on_error:
            on_error("已是最新版本，无需更新")
        return False

    # Step 2: 下载
    report_progress(f"发现新版本 v{remote.version}，正在下载...")

    def download_cb(downloaded, total):
        report_progress(
            f"下载中... {_format_size(downloaded)} / {_format_size(total)}",
            downloaded, total
        )

    zip_path = download_update(remote, progress_callback=download_cb)
    if zip_path is None:
        report_progress("下载失败")
        if on_error:
            on_error("下载更新包失败，请检查网络连接")
        return False

    # Step 3: 安装
    report_progress("正在安装更新...")
    if not apply_update(zip_path):
        report_progress("安装失败")
        if on_error:
            on_error("更新安装失败，可能文件被占用")
        return False

    report_progress("更新完成，即将重启...")
    return True


def _format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
