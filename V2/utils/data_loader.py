"""
游戏数据加载工具
从 game_data/ 目录加载 JSON 配置文件
支持开发环境和 PyInstaller 打包后的 EXE 环境
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any


def _get_base_dir() -> Path:
    """获取项目根目录（兼容 PyInstaller 打包环境）"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后，资源解压到 sys._MEIPASS 临时目录
        return Path(sys._MEIPASS)
    else:
        # 开发环境：utils/data_loader.py -> 上级目录就是项目根目录
        return Path(__file__).parent.parent


class DataLoader:
    """游戏数据加载器"""
    
    # 数据目录路径（兼容打包环境）
    DATA_DIR = _get_base_dir() / "game_data"
    
    # 数据缓存
    _cache: Dict[str, Any] = {}
    
    @classmethod
    def load(cls, filename: str, use_cache: bool = True) -> Dict[str, Any]:
        """加载 JSON 数据文件
        
        Args:
            filename: 文件名（如 "dunjia_data.json"）
            use_cache: 是否使用缓存（默认 True）
        
        Returns:
            解析后的 JSON 数据（字典）
        
        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON 格式错误
        """
        # 检查缓存
        if use_cache and filename in cls._cache:
            return cls._cache[filename]
        
        # 读取文件
        file_path = cls.DATA_DIR / filename
        if not file_path.exists():
            raise FileNotFoundError(f"数据文件不存在: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 缓存数据
        if use_cache:
            cls._cache[filename] = data
        
        return data
    
    @classmethod
    def clear_cache(cls):
        """清除数据缓存（用于热重载）"""
        cls._cache.clear()
    
    @classmethod
    def reload(cls, filename: str) -> Dict[str, Any]:
        """重新加载数据文件（不使用缓存）
        
        Args:
            filename: 文件名
        
        Returns:
            最新的数据
        """
        # 清除指定文件的缓存
        cls._cache.pop(filename, None)
        return cls.load(filename, use_cache=False)


# 便捷函数
def load_game_data(filename: str) -> Dict[str, Any]:
    """加载游戏数据的快捷函数
    
    Args:
        filename: 数据文件名
    
    Returns:
        数据字典
    """
    return DataLoader.load(filename)
