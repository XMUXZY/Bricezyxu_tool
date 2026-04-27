"""
法宝升阶养成计算器 - 纯计算模块
从 pages/tool_fabao.py 提取，不含任何 UI 依赖。

支持两种模式：
  模式一：材料 → 进度（可达阶数及剩余）
  模式二：目标 → 材料（所需碎片 + 所需第二材料）
"""

from utils.data_loader import load_game_data

# ============================================================
# 一、数据加载
# ============================================================

_FABAO_JSON = load_game_data("fabao_data.json")

SIXIANG_COST = _FABAO_JSON["sixiang_cost"]
SANCAI_CHIP_COST = _FABAO_JSON["sancai_chip_cost"]
SANCAI_MAT2_COST = _FABAO_JSON["sancai_mat2_cost"]

# 法宝信息表：(name, grade, formation, chip_name, mat2_name)
FABAO_LIST = [
    (f["name"], f["grade"], f["formation"], f["chip"], f["mat2"])
    for f in _FABAO_JSON["fabao_list"]
]

# 法阵类型分组映射
FORMATION_TYPES = _FABAO_JSON["formation_types"]

# 法阵颜色映射
FORMATION_COLORS = _FABAO_JSON["formation_colors"]

del _FABAO_JSON  # 释放临时变量


# ============================================================
# 二、工具函数
# ============================================================

def get_cost_tables(formation_type: str) -> tuple:
    """根据法阵类型获取消耗表 -> (chip_cost_table, mat2_cost_table)"""
    data_set = FORMATION_TYPES.get(formation_type, "SIXIANG")
    if data_set == "SANCAI":
        return SANCAI_CHIP_COST, SANCAI_MAT2_COST
    else:
        return SIXIANG_COST, [0] * 100


def has_mat2(formation_type: str) -> bool:
    """该法阵类型是否有第二材料"""
    return formation_type in ("三才阵", "归藏阵")


def get_fabao_display_name(fabao: tuple) -> str:
    """获取法宝的显示名称"""
    name, grade, formation, chip_name, mat2_name = fabao
    if grade != "凡" and formation == "四象阵":
        return f"{name}({grade})"
    return name


def get_fabao_by_formation(formation_type: str) -> list:
    """按法阵类型获取法宝列表"""
    return [f for f in FABAO_LIST if f[2] == formation_type]


# ============================================================
# 三、计算函数
# ============================================================

def calc_by_materials(fabao: tuple, cur_level: int,
                      owned_chips: int, owned_mat2: int = 0) -> dict:
    """
    模式一：材料 → 可达阶数

    参数:
        fabao:        法宝元组 (name, grade, formation, chip_name, mat2_name)
        cur_level:    当前阶数 (0~99)
        owned_chips:  持有碎片数
        owned_mat2:   持有第二材料数

    返回:
        {
            "error": str|None,
            "reach_level": int,
            "remaining_chips": int,
            "remaining_mat2": int,
            "stop_reason": str,
            "table_data": list,
        }
    """
    name, grade, formation, chip_name, mat2_name = fabao

    if cur_level < 0 or cur_level > 99:
        return {"error": "当前阶数范围 0~99"}
    if owned_chips < 0:
        return {"error": "碎片数量不能为负"}

    has_m2 = has_mat2(formation)
    chip_cost_table, mat2_cost_table = get_cost_tables(formation)

    remaining_chips = owned_chips
    remaining_mat2 = owned_mat2
    reach_level = cur_level
    table_data = []
    stop_reason = ""

    for lv in range(cur_level, 100):
        c_cost = chip_cost_table[lv]
        m_cost = mat2_cost_table[lv] if has_m2 else 0

        if remaining_chips < c_cost:
            stop_reason = f"碎片不足（需{c_cost}，剩余{remaining_chips}）"
            break
        if has_m2 and m_cost > 0 and remaining_mat2 < m_cost:
            stop_reason = f"{mat2_name}不足（需{m_cost}，剩余{remaining_mat2}）"
            break

        remaining_chips -= c_cost
        if has_m2 and m_cost > 0:
            remaining_mat2 -= m_cost
        reach_level = lv + 1

        if has_m2:
            table_data.append([
                f"{lv}阶→{lv+1}阶",
                f"{c_cost}",
                f"{m_cost}" if m_cost > 0 else "—",
                f"{remaining_chips}",
                f"{remaining_mat2}" if m_cost > 0 or lv >= 19 else "—",
            ])
        else:
            table_data.append([
                f"{lv}阶→{lv+1}阶",
                f"{c_cost}",
                f"{remaining_chips}",
            ])

    # 下一阶信息
    next_info = None
    if reach_level < 100:
        next_chip = chip_cost_table[reach_level]
        next_mat2 = mat2_cost_table[reach_level] if has_m2 else 0
        next_info = {
            'next_chip': next_chip,
            'chip_gap': max(0, next_chip - remaining_chips),
            'next_mat2': next_mat2,
            'mat2_gap': max(0, next_mat2 - remaining_mat2) if has_m2 else 0,
        }

    return {
        "error": None,
        "reach_level": reach_level,
        "remaining_chips": remaining_chips,
        "remaining_mat2": remaining_mat2,
        "stop_reason": stop_reason,
        "table_data": table_data,
        "next_info": next_info,
        "has_mat2": has_m2,
    }


def calc_for_target(fabao: tuple, cur_level: int, tgt_level: int) -> dict:
    """
    模式二：目标阶数 → 所需材料

    参数:
        fabao:      法宝元组 (name, grade, formation, chip_name, mat2_name)
        cur_level:  当前阶数 (0~99)
        tgt_level:  目标阶数 (1~100)

    返回:
        {
            "error": str|None,
            "total_chips": int,
            "total_mat2": int,
            "has_mat2": bool,
            "table_data": list,
            "segments": list,   # 分段汇总
        }
    """
    name, grade, formation, chip_name, mat2_name = fabao

    if cur_level < 0 or cur_level > 99:
        return {"error": "当前阶数范围 0~99"}
    if tgt_level < 1 or tgt_level > 100:
        return {"error": "目标阶数范围 1~100"}
    if tgt_level <= cur_level:
        return {"error": "目标阶数必须大于当前阶数"}

    has_m2 = has_mat2(formation)
    chip_cost_table, mat2_cost_table = get_cost_tables(formation)

    total_chips = 0
    total_mat2 = 0
    table_data = []
    cum_chips = 0
    cum_mat2 = 0

    for lv in range(cur_level, tgt_level):
        c_cost = chip_cost_table[lv]
        m_cost = mat2_cost_table[lv] if has_m2 else 0
        total_chips += c_cost
        total_mat2 += m_cost
        cum_chips += c_cost
        cum_mat2 += m_cost

        if has_m2:
            table_data.append([
                f"{lv}阶→{lv+1}阶",
                f"{c_cost}",
                f"{m_cost}" if m_cost > 0 else "—",
                f"{cum_chips:,}",
                f"{cum_mat2}" if cum_mat2 > 0 else "—",
            ])
        else:
            table_data.append([
                f"{lv}阶→{lv+1}阶",
                f"{c_cost}",
                f"{cum_chips:,}",
            ])

    # 分段汇总（每5阶）
    segments = []
    seg_start = cur_level
    while seg_start < tgt_level:
        seg_end = min(((seg_start // 5) + 1) * 5, tgt_level)
        seg_chips = sum(chip_cost_table[lv] for lv in range(seg_start, seg_end))
        seg_mat2 = sum(mat2_cost_table[lv] for lv in range(seg_start, seg_end)) if has_m2 else 0
        segments.append({
            'from': seg_start, 'to': seg_end - 1,
            'chips': seg_chips, 'mat2': seg_mat2,
        })
        seg_start = seg_end

    return {
        "error": None,
        "total_chips": total_chips,
        "total_mat2": total_mat2,
        "has_mat2": has_m2,
        "table_data": table_data,
        "segments": segments,
    }
