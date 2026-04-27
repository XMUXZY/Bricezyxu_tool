"""
占测养成计算器 - 纯计算模块
从 pages/tool_zhance.py 提取，不含任何 UI 依赖。

支持两种计算模式：
  模式一：已知材料 → 计算可达阶数与重数
  模式二：已知目标 → 计算所需材料数量
"""

from utils.data_loader import load_game_data

# ============================================================
# 一、数据加载
# ============================================================

_json = load_game_data("zhance_data.json")

SERIES_CONFIG = _json["series_config"]
SERIES_ORDER = _json["series_order"]

# 每阶最大重数（JSON key 为字符串，需转为 int）
TIER_MAX_LEVELS = {int(k): v for k, v in _json["tier_max_levels"].items()}

# 所有阶的顺序
ALL_TIERS = list(range(1, 18))

# 阶 → 系列映射
TIER_SERIES = {}
for _series, _cfg in SERIES_CONFIG.items():
    for _t in _cfg['tiers']:
        TIER_SERIES[_t] = _series

# 逐级明细数据：(阶, 重) → {mat1, mat2, copper}
LEVEL_DATA = {}
for _k, _v in _json["level_data"].items():
    _tier, _level = _k.split("_")
    LEVEL_DATA[(int(_tier), int(_level))] = _v


# ============================================================
# 二、构建累计数据
# ============================================================

def _build_cumulative_data() -> dict:
    """构建全局累计消耗数据"""
    cum_data = {}
    cum = {
        '普通': {'mat1': 0, 'mat2': 0, 'copper': 0},
        '玄':   {'mat1': 0, 'mat2': 0, 'copper': 0},
        '地':   {'mat1': 0, 'mat2': 0, 'copper': 0},
    }

    for tier in ALL_TIERS:
        max_lv = TIER_MAX_LEVELS[tier]
        series = TIER_SERIES[tier]
        for lv in range(1, max_lv + 1):
            key = (tier, lv)
            info = LEVEL_DATA.get(key, {'mat1': 0, 'mat2': 0, 'copper': 0})
            cum[series]['mat1'] += info['mat1']
            cum[series]['mat2'] += info['mat2']
            cum[series]['copper'] += info['copper']
            cum_data[key] = {
                s: {'mat1': cum[s]['mat1'], 'mat2': cum[s]['mat2'], 'copper': cum[s]['copper']}
                for s in SERIES_ORDER
            }

    return cum_data


CUM_DATA = _build_cumulative_data()

# 清理模块级临时变量
del _json


# ============================================================
# 三、工具函数
# ============================================================

def pos_to_index(tier: int, level: int) -> int:
    """将(阶,重)转为全局序号，用于比较先后"""
    idx = 0
    for t in ALL_TIERS:
        if t < tier:
            idx += TIER_MAX_LEVELS[t]
        elif t == tier:
            idx += level
            break
    return idx


def format_number(num) -> str:
    """格式化数字（加千分位）"""
    if isinstance(num, int):
        return f"{num:,}"
    return str(num)


# ============================================================
# 四、计算函数
# ============================================================

def calc_by_materials(start_tier: int, start_level: int,
                      materials: dict, copper_available: int) -> dict:
    """
    模式一：根据持有材料计算可达等级

    参数:
        start_tier:       起始阶数
        start_level:      起始重数
        materials:        材料持有量 {(系列名, 'mat1'|'mat2'): 数量}
        copper_available:  铜钱持有量

    返回:
        {
            "error": str|None,
            "final_tier": int,
            "final_level": int,
            "used": dict,
            "used_copper": int,
            "path": list,
            "stopped_reason": str,
        }
    """
    max_lv = TIER_MAX_LEVELS.get(start_tier, 0)
    if start_level > max_lv:
        return {"error": f"{start_tier}阶最大{max_lv}重"}

    all_zero = all(v == 0 for v in materials.values()) and copper_available == 0
    if all_zero:
        return {"error": "请输入至少一种材料的数量"}

    used = {(s, t): 0 for s in SERIES_ORDER for t in ('mat1', 'mat2')}
    used_copper = 0
    path = []

    current_tier = start_tier
    current_level = start_level

    for tier in ALL_TIERS:
        if tier < start_tier:
            continue

        series = TIER_SERIES[tier]
        tier_max_lv = TIER_MAX_LEVELS[tier]
        cfg = SERIES_CONFIG[series]

        if tier == start_tier:
            from_lv = start_level + 1
        else:
            from_lv = 1

        for lv in range(from_lv, tier_max_lv + 1):
            key = (tier, lv)
            info = LEVEL_DATA.get(key)
            if not info:
                continue

            mat1_need = info['mat1']
            mat2_need = info['mat2']
            copper_need = info['copper']

            mat1_avail = materials.get((series, 'mat1'), 0) - used[(series, 'mat1')]
            mat2_avail = materials.get((series, 'mat2'), 0) - used[(series, 'mat2')]
            copper_avail = copper_available - used_copper

            if mat1_avail >= mat1_need and mat2_avail >= mat2_need and copper_avail >= copper_need:
                used[(series, 'mat1')] += mat1_need
                used[(series, 'mat2')] += mat2_need
                used_copper += copper_need

                current_tier = tier
                current_level = lv

                path.append({
                    'tier': tier, 'level': lv,
                    'mat1': mat1_need, 'mat2': mat2_need, 'copper': copper_need,
                    'mat1_name': cfg['mat1_name'],
                    'mat2_name': cfg['mat2_name'],
                    'series': series,
                })
            else:
                # 材料不足
                reasons = []
                if mat1_avail < mat1_need:
                    reasons.append(f"{cfg['mat1_name']}不足（需{mat1_need}，剩{max(0, mat1_avail)}）")
                if mat2_avail < mat2_need:
                    reasons.append(f"{cfg['mat2_name']}不足（需{mat2_need}，剩{max(0, mat2_avail)}）")
                if copper_avail < copper_need:
                    reasons.append(f"铜钱不足（需{format_number(copper_need)}，剩{format_number(max(0, copper_avail))}）")
                stop_reason = f"升{tier}阶{lv}重时: " + "、".join(reasons)

                return {
                    "error": None,
                    "final_tier": current_tier,
                    "final_level": current_level,
                    "used": used,
                    "used_copper": used_copper,
                    "path": path,
                    "stopped_reason": stop_reason,
                }

    return {
        "error": None,
        "final_tier": current_tier,
        "final_level": current_level,
        "used": used,
        "used_copper": used_copper,
        "path": path,
        "stopped_reason": "已达当前数据最高等级（17阶4重）",
    }


def calc_by_target(start_tier: int, start_level: int,
                   target_tier: int, target_level: int) -> dict:
    """
    模式二：根据目标等级计算所需材料

    参数:
        start_tier:   起始阶数
        start_level:  起始重数
        target_tier:  目标阶数
        target_level: 目标重数

    返回:
        {
            "error": str|None,
            "required": dict,
            "required_copper": int,
            "path": list,
        }
    """
    s_max = TIER_MAX_LEVELS.get(start_tier, 0)
    if start_level > s_max:
        return {"error": f"{start_tier}阶最大{s_max}重"}

    t_max = TIER_MAX_LEVELS.get(target_tier, 0)
    if target_level < 1 or target_level > t_max:
        return {"error": f"{target_tier}阶重数范围为1-{t_max}"}

    start_idx = pos_to_index(start_tier, start_level)
    target_idx = pos_to_index(target_tier, target_level)
    if target_idx <= start_idx:
        return {"error": "目标等级必须高于当前等级"}

    required = {(s, t): 0 for s in SERIES_ORDER for t in ('mat1', 'mat2')}
    required_copper = 0
    path = []

    for tier in ALL_TIERS:
        if tier < start_tier or tier > target_tier:
            continue

        series = TIER_SERIES[tier]
        tier_max_lv = TIER_MAX_LEVELS[tier]
        cfg = SERIES_CONFIG[series]

        if tier == start_tier:
            from_lv = start_level + 1
        else:
            from_lv = 1

        if tier == target_tier:
            to_lv = target_level
        else:
            to_lv = tier_max_lv

        for lv in range(from_lv, to_lv + 1):
            key = (tier, lv)
            info = LEVEL_DATA.get(key)
            if not info:
                continue

            required[(series, 'mat1')] += info['mat1']
            required[(series, 'mat2')] += info['mat2']
            required_copper += info['copper']

            path.append({
                'tier': tier, 'level': lv,
                'mat1': info['mat1'], 'mat2': info['mat2'], 'copper': info['copper'],
                'mat1_name': cfg['mat1_name'],
                'mat2_name': cfg['mat2_name'],
                'series': series,
            })

    return {
        "error": None,
        "required": required,
        "required_copper": required_copper,
        "path": path,
    }
