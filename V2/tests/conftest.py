"""
pytest 全局配置
确保项目根目录在 sys.path 中，以便测试可以正确导入 calculators 包。
"""

import sys
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 确保项目根在 sys.path 最前
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
