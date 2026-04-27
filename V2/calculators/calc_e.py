"""
圣石养成计算引擎
纯数据 + 纯计算函数，不依赖任何 UI 框架。
"""

from utils.data_loader import load_game_data

# ============================================================
# 从 JSON 加载配置数据
# ============================================================
_JSON = load_game_data("shengshi_data.json")

PART_CONFIG = _JSON["part_config"]
SLOT_LIMITS = _JSON["slot_limits"]

# JSON key 格式 "圣石(栏位1)_气海" → 还原为 tuple key
SLOT_ITEM_NAMES = {}
for _k, _v in _JSON["slot_item_names"].items():
    _slot, _series = _k.rsplit("_", 1)
    SLOT_ITEM_NAMES[(_slot, _series)] = _v

# ============================================================
# 从 JSON 加载逐级消耗数据并转换为统一字典格式
# ============================================================
_stone_raw = _JSON["stone_raw"]
_xuan_raw = _JSON["xuan_raw"]
_gang_raw = _JSON["gang_raw"]

STONE_DATA = [{"lv": r[0], "jf": r[1], "stage": bool(r[2] > 0), "stage_jf": r[2]} for r in _stone_raw]
XUAN_DATA = [{"lv": r[0], "jf": r[1], "item": r[2], "stage": bool(r[3] > 0), "stage_jf": r[3]} for r in _xuan_raw]
GANG_DATA = [{"lv": r[0], "jf": r[1], "item": r[2], "stage": bool(r[3] > 0), "stage_jf": r[3], "stage_item": r[4]} for r in _gang_raw]
del _stone_raw, _xuan_raw, _gang_raw, _JSON

# 数据字典索引: lv -> data dict
STONE_BY_LVL = {d["lv"]: d for d in STONE_DATA}
XUAN_BY_LVL = {d["lv"]: d for d in XUAN_DATA}
GANG_BY_LVL = {d["lv"]: d for d in GANG_DATA}


# ============================================================
# 辅助函数
# ============================================================

def get_data_list(slot: str):
    """根据槽位返回对应的数据列表"""
    if "圣石" in slot:
        return STONE_DATA
    if "玄石" in slot:
        return XUAN_DATA
    return GANG_DATA


def get_data_map(slot: str):
    """根据槽位返回对应的 lv->data 映射"""
    if "圣石" in slot:
        return STONE_BY_LVL
    if "玄石" in slot:
        return XUAN_BY_LVL
    return GANG_BY_LVL


def has_items(slot: str) -> bool:
    """该槽位是否消耗道具"""
    return "圣石" not in slot


def resolve_attr(part: str, slot_key: str, selected_attr: str = "金刚系") -> str:
    """解析当前部位的属性系"""
    cfg = PART_CONFIG.get(part, {})
    series = cfg.get(slot_key, "")
    if "可选" in series:
        return "金刚" if "金" in selected_attr else "灵柔"
    elif "极意" in series or "(威霆)" in series:
        return "极意"
    elif "气海" in series or "(渊泽)" in series:
        return "气海"
    return "气海"


# ============================================================
# 计算函数
# ============================================================

def calc_by_materials(slot: str, cur_lv: int, jf: float, item_val: float) -> dict:
    """
    根据材料计算可达等级。

    参数:
        slot: 槽位名称
        cur_lv: 当前等级
        jf: 积分数量 (float('inf') 表示无限)
        item_val: 道具数量 (float('inf') 表示无限)

    返回:
        dict: {level, total_jf, total_item, steps}
    """
    max_lv = SLOT_LIMITS[slot]
    data_map = get_data_map(slot)
    lv = cur_lv
    total_jf = 0.0
    total_item = 0.0
    steps = 0

    while lv < max_lv:
        next_lv = lv + 1
        entry = data_map.get(next_lv)
        if not entry:
            break

        need_jf = entry.get("jf", 0)
        need_item = entry.get("item", 0)
        stage_jf = entry.get("stage_jf", 0)
        stage_item = entry.get("stage_item", 0)

        # 检查升阶
        if entry.get("stage") and stage_jf > 0:
            if jf != float("inf") and jf < stage_jf:
                break
            if jf != float("inf"):
                jf -= stage_jf
                total_jf += stage_jf
            if item_val != float("inf") and stage_item > 0 and item_val < stage_item:
                break
            if item_val != float("inf"):
                item_val -= stage_item
                total_item += stage_item

        # 正常升级
        cost_ok = True
        if need_jf > 0:
            if jf != float("inf") and jf < need_jf:
                cost_ok = False
            elif jf != float("inf"):
                jf -= need_jf
                total_jf += need_jf

        if need_item > 0 and has_items(slot):
            if item_val != float("inf") and item_val < need_item:
                cost_ok = False
            elif item_val != float("inf"):
                item_val -= need_item
                total_item += need_item

        if not cost_ok:
            break

        lv = next_lv
        steps += 1

    return {
        "level": lv,
        "total_jf": total_jf,
        "total_item": total_item,
        "steps": steps,
        "remaining_jf": jf,
        "remaining_item": item_val,
    }


def calc_for_target(slot: str, start_lv: int, target_lv: int) -> dict:
    """
    根据目标等级计算所需材料。

    返回:
        dict: {total_jf, total_item, stages_hit}
    """
    data_map = get_data_map(slot)
    total_jf = 0
    total_item = 0
    stages_hit = []

    for lv in range(start_lv + 1, target_lv + 1):
        entry = data_map.get(lv)
        if not entry:
            continue
        total_jf += entry.get("jf", 0)
        total_item += entry.get("item", 0)
        if entry.get("stage"):
            sj = entry.get("stage_jf", 0)
            si = entry.get("stage_item", 0)
            total_jf += sj
            total_item += si
            stages_hit.append(lv)

    return {
        "total_jf": total_jf,
        "total_item": total_item,
        "stages_hit": stages_hit,
    }
