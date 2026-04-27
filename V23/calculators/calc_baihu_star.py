"""
白虎星图锤炼计算引擎
纯数据 + 纯计算函数，不依赖任何 UI 框架。

三个星官：奎木狼、胃土雉、娄金星官
每个星官 10重×6级，锤炼为概率事件，默认使用保底材料。
"""

import math
from utils.data_loader import load_game_data


# ============================================================
# 一、数据加载
# ============================================================

_DATA = load_game_data("baihu_star_data.json")

MAX_WEIGHT = _DATA["max_weight"]       # 10
MAX_LEVEL = _DATA["max_level"]         # 6
GUARANTEE_MAT = _DATA["guarantee_material"]  # "白虎之灵"

# 星官数据: [{name, hammer_material, levels: [{weight, level, ...}]}]
OFFICIALS = _DATA["officials"]

del _DATA


# ============================================================
# 二、工具函数
# ============================================================

def get_official_names() -> list[str]:
    """获取所有星官名称"""
    return [o["name"] for o in OFFICIALS]


def find_official(name: str) -> dict | None:
    """按名称查找星官"""
    for o in OFFICIALS:
        if o["name"] == name:
            return o
    return None


def get_level_info(official_name: str, weight: int, level: int) -> dict | None:
    """获取指定星官某重某级的锤炼参数"""
    off = find_official(official_name)
    if not off:
        return None
    for lv in off["levels"]:
        if lv["weight"] == weight and lv["level"] == level:
            return lv
    return None


def state_to_index(weight: int, level: int) -> int:
    """将(重数, 等级)转换为线性序号。
    0重0级=0（未开始），1重1级=1，1重6级=6，2重1级=7，...，10重6级=60
    """
    if weight == 0 and level == 0:
        return 0
    return (weight - 1) * MAX_LEVEL + level


def index_to_state(idx: int) -> tuple[int, int]:
    """将线性序号转换为(重数, 等级)"""
    if idx <= 0:
        return (0, 0)
    weight = (idx - 1) // MAX_LEVEL + 1
    level = (idx - 1) % MAX_LEVEL + 1
    return (weight, level)


# ============================================================
# 三、核心计算：从 A 状态到 B 状态的材料消耗（期望值）
# ============================================================

def calc_material_cost(official_name: str,
                       cur_weight: int, cur_level: int,
                       tgt_weight: int, tgt_level: int) -> dict:
    """
    计算从当前状态到目标状态所需的锤炼材料和保底材料（期望值）。

    每一级锤炼的期望消耗 = 单次材料消耗 × 期望尝试次数

    Args:
        official_name: 星官名称
        cur_weight: 当前重数 (0=未开始, 1~10)
        cur_level: 当前等级 (0=未开始, 1~6)
        tgt_weight: 目标重数 (1~10)
        tgt_level: 目标等级 (1~6)

    Returns:
        {
            "error": str|None,
            "official_name": str,
            "hammer_material": str,
            "guarantee_material": str,
            "cur_state": (weight, level),
            "tgt_state": (weight, level),
            "total_hammer": float,      # 总锤炼材料（期望值）
            "total_guarantee": float,   # 总保底材料（期望值）
            "details": [{weight, level, hammer_per, guarantee_per, tries, hammer_total, guarantee_total}],
        }
    """
    off = find_official(official_name)
    if not off:
        return {"error": f"未找到星官: {official_name}"}

    cur_idx = state_to_index(cur_weight, cur_level)
    tgt_idx = state_to_index(tgt_weight, tgt_level)

    if tgt_idx <= cur_idx:
        return {"error": "目标必须高于当前状态"}

    if tgt_weight > MAX_WEIGHT or tgt_level > MAX_LEVEL:
        return {"error": f"最高支持 {MAX_WEIGHT}重{MAX_LEVEL}级"}

    # 从当前状态的下一级开始计算
    start_idx = cur_idx + 1
    total_hammer = 0.0
    total_guarantee = 0.0
    details = []

    for idx in range(start_idx, tgt_idx + 1):
        w, l = index_to_state(idx)
        info = get_level_info(official_name, w, l)
        if not info:
            return {"error": f"找不到 {official_name} {w}重{l}级的数据"}

        tries = info["expected_tries"]
        h_per = info["hammer_cost"]
        g_per = info["guarantee_cost"]
        h_total = h_per * tries
        g_total = g_per * tries

        total_hammer += h_total
        total_guarantee += g_total

        details.append({
            "weight": w,
            "level": l,
            "hammer_per": h_per,
            "guarantee_per": g_per,
            "base_rate": info["base_rate"],
            "tries": round(tries, 2),
            "hammer_total": round(h_total, 1),
            "guarantee_total": round(g_total, 1),
        })

    return {
        "error": None,
        "official_name": official_name,
        "hammer_material": off["hammer_material"],
        "guarantee_material": GUARANTEE_MAT,
        "cur_state": (cur_weight, cur_level),
        "tgt_state": (tgt_weight, tgt_level),
        "total_hammer": round(total_hammer, 1),
        "total_guarantee": round(total_guarantee, 1),
        "details": details,
    }


# ============================================================
# 四、反推计算：给定材料上限，能达到的最高等级
# ============================================================

def calc_max_reachable(official_name: str,
                       cur_weight: int, cur_level: int,
                       held_hammer: float, held_guarantee: float) -> dict:
    """
    根据持有材料计算可达到的最高重数和等级。

    逐级消耗材料，直到某一级材料不足时停止。

    Args:
        official_name: 星官名称
        cur_weight: 当前重数 (0=未开始, 1~10)
        cur_level: 当前等级 (0=未开始, 1~6)
        held_hammer: 持有锤炼材料数量
        held_guarantee: 持有保底材料数量

    Returns:
        {
            "error": str|None,
            "official_name": str,
            "hammer_material": str,
            "guarantee_material": str,
            "cur_state": (weight, level),
            "max_state": (weight, level),
            "used_hammer": float,
            "used_guarantee": float,
            "remaining_hammer": float,
            "remaining_guarantee": float,
            "levels_gained": int,
            "details": [...],
            "limiting_factor": str,  # "锤炼材料" / "保底材料" / "已满级"
        }
    """
    off = find_official(official_name)
    if not off:
        return {"error": f"未找到星官: {official_name}"}

    cur_idx = state_to_index(cur_weight, cur_level)
    max_idx = state_to_index(MAX_WEIGHT, MAX_LEVEL)

    if cur_idx >= max_idx:
        return {
            "error": None,
            "official_name": official_name,
            "hammer_material": off["hammer_material"],
            "guarantee_material": GUARANTEE_MAT,
            "cur_state": (cur_weight, cur_level),
            "max_state": (cur_weight, cur_level),
            "used_hammer": 0, "used_guarantee": 0,
            "remaining_hammer": held_hammer,
            "remaining_guarantee": held_guarantee,
            "levels_gained": 0,
            "details": [],
            "limiting_factor": "已满级",
        }

    remain_h = held_hammer
    remain_g = held_guarantee
    used_h = 0.0
    used_g = 0.0
    reached_idx = cur_idx
    details = []
    limiting = "已满级"

    for idx in range(cur_idx + 1, max_idx + 1):
        w, l = index_to_state(idx)
        info = get_level_info(official_name, w, l)
        if not info:
            break

        tries = info["expected_tries"]
        h_need = info["hammer_cost"] * tries
        g_need = info["guarantee_cost"] * tries

        if remain_h < h_need and remain_g < g_need:
            # 两种材料都不够
            if remain_h / h_need < remain_g / g_need:
                limiting = off["hammer_material"]
            else:
                limiting = GUARANTEE_MAT
            break
        elif remain_h < h_need:
            limiting = off["hammer_material"]
            break
        elif remain_g < g_need:
            limiting = GUARANTEE_MAT
            break

        remain_h -= h_need
        remain_g -= g_need
        used_h += h_need
        used_g += g_need
        reached_idx = idx

        details.append({
            "weight": w,
            "level": l,
            "hammer_per": info["hammer_cost"],
            "guarantee_per": info["guarantee_cost"],
            "tries": round(tries, 2),
            "hammer_total": round(h_need, 1),
            "guarantee_total": round(g_need, 1),
        })

    rw, rl = index_to_state(reached_idx)

    return {
        "error": None,
        "official_name": official_name,
        "hammer_material": off["hammer_material"],
        "guarantee_material": GUARANTEE_MAT,
        "cur_state": (cur_weight, cur_level),
        "max_state": (rw, rl),
        "used_hammer": round(used_h, 1),
        "used_guarantee": round(used_g, 1),
        "remaining_hammer": round(remain_h, 1),
        "remaining_guarantee": round(remain_g, 1),
        "levels_gained": reached_idx - cur_idx,
        "details": details,
        "limiting_factor": limiting,
    }
