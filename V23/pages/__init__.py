"""
页面模块包
所有工具页面均在此目录下，每个工具对应一个独立文件。
"""

from .base_tool import BaseToolPage
from .home import HomePage
from .tool_a import ToolAPage
from .tool_b import ToolBPage
from .tool_c import ToolCPage
from .tool_d import ToolDPage
from .tool_e import ToolEPage
from .tool_star_map import ToolStarMapPage
from .tool_feng_shui import ToolFengShuiPage
from .tool_gem_grind import ToolGemGrindPage
from .tool_zhu_ling import ToolZhuLingPage
from .tool_dunjia import ToolDunJia
from .tool_fabao import ToolFaBao
from .tool_baihu_star import ToolBaihuStar
from .table_demo import TableDemoPage
from .settings import SettingsPage

__all__ = [
    "BaseToolPage",
    "HomePage",
    "ToolAPage",
    "ToolBPage",
    "ToolCPage",
    "ToolDPage",
    "ToolEPage",
    "ToolStarMapPage",
    "ToolFengShuiPage",
    "ToolGemGrindPage",
    "ToolZhuLingPage",
    "ToolDunJia",
    "ToolBaihuStar",
    "TableDemoPage",
    "SettingsPage",
]
