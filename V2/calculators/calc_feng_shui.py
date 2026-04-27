"""
风水录养成计算引擎
纯数据 + 纯计算函数，不依赖任何 UI 框架。
"""

# ============================================================
# 风水点数据
# ============================================================

FENG_SHUI_POINTS = {
    1: {"name": "平原村", "map": "北郡", "main_mat": "神兽石", "main_per": 2, "sub_mat": None, "sub_per": 0, "progress": [0, 250, 380, 500, 630, 850], "card_star": 1, "card_extra": 6},
    2: {"name": "寂幻坛", "map": "北郡", "main_mat": "神兽石", "main_per": 2, "sub_mat": None, "sub_per": 0, "progress": [0, 250, 380, 500, 630, 850], "card_star": 1, "card_extra": 6},
    3: {"name": "东夷祭坛", "map": "北郡", "main_mat": "神兽石", "main_per": 2, "sub_mat": None, "sub_per": 0, "progress": [0, 250, 380, 500, 630, 850], "card_star": 1, "card_extra": 6},
    4: {"name": "天羽村", "map": "北郡", "main_mat": "神兽石", "main_per": 1, "sub_mat": None, "sub_per": 0, "progress": [0, 250, 380, 500, 630, 850], "card_star": 1, "card_extra": 4},
    5: {"name": "遗逐村", "map": "北郡", "main_mat": "神兽石", "main_per": 1, "sub_mat": None, "sub_per": 0, "progress": [0, 250, 380, 500, 630, 850], "card_star": 1, "card_extra": 4},
    6: {"name": "百果祀", "map": "北郡", "main_mat": "神兽石", "main_per": 1, "sub_mat": None, "sub_per": 0, "progress": [0, 250, 380, 500, 630, 850], "card_star": 1, "card_extra": 4},
    7: {"name": "神祀", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 2, "sub_mat": "神兽石·星", "sub_per": 2, "progress": [0, 380, 760, 950, 1140, 1340], "card_star": 0, "card_extra": 0},
    8: {"name": "七迷洞", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 2, "sub_mat": "神兽石·星", "sub_per": 2, "progress": [0, 380, 760, 950, 1140, 1340], "card_star": 0, "card_extra": 0},
    9: {"name": "琅琊山", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 2, "sub_mat": "神兽石·星", "sub_per": 2, "progress": [0, 380, 760, 950, 1140, 1340], "card_star": 0, "card_extra": 0},
    10: {"name": "长股村落", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 1, "sub_mat": "神兽石·星", "sub_per": 2, "progress": [0, 380, 760, 950, 1140, 1340], "card_star": 0, "card_extra": 0},
    11: {"name": "长右村落", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 1, "sub_mat": "神兽石·星", "sub_per": 2, "progress": [0, 380, 760, 950, 1140, 1340], "card_star": 0, "card_extra": 0},
    12: {"name": "东海崖", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 1, "sub_mat": "神兽石·星", "sub_per": 2, "progress": [0, 380, 760, 950, 1140, 1340], "card_star": 0, "card_extra": 0},
    13: {"name": "翔舞部落", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 2, "sub_mat": "寻龍图", "sub_per": 2, "progress": [0, 540, 1090, 1360, 1630, 1900], "card_star": 0, "card_extra": 0},
    14: {"name": "延维聚落", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 2, "sub_mat": None, "sub_per": 0, "progress": [0, 540, 1090, 1360, 1630, 1900], "card_star": 0, "card_extra": 0},
    15: {"name": "昆仑山", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 1, "sub_mat": "寻龍图", "sub_per": 2, "progress": [0, 540, 1090, 1360, 1630, 1900], "card_star": 0, "card_extra": 0},
    16: {"name": "不冻泉", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 2, "sub_mat": None, "sub_per": 0, "progress": [0, 540, 1090, 1360, 1630, 1900], "card_star": 0, "card_extra": 0},
    17: {"name": "蜃楼", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 1, "sub_mat": "寻龍图", "sub_per": 2, "progress": [0, 540, 1090, 1360, 1630, 1900], "card_star": 0, "card_extra": 0},
    18: {"name": "玉珠峰", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 2, "sub_mat": "寻龍图", "sub_per": 2, "progress": [0, 540, 1090, 1360, 1630, 1900], "card_star": 0, "card_extra": 0},
    19: {"name": "银明山", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2, "sub_mat": "镇龍锁", "sub_per": 2, "progress": [0, 1070, 2160, 2690, 3220, 3760], "card_star": 0, "card_extra": 0},
    20: {"name": "蛮牛野", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2, "sub_mat": None, "sub_per": 0, "progress": [0, 1070, 2160, 2690, 3220, 3760], "card_star": 0, "card_extra": 0},
    21: {"name": "城西山", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2, "sub_mat": None, "sub_per": 0, "progress": [0, 1070, 2160, 2690, 3220, 3760], "card_star": 0, "card_extra": 0},
    22: {"name": "城西村", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2, "sub_mat": None, "sub_per": 0, "progress": [0, 1070, 2160, 2690, 3220, 3760], "card_star": 0, "card_extra": 0},
    23: {"name": "轩辕台", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2, "sub_mat": "镇龍锁", "sub_per": 2, "progress": [0, 1070, 2160, 2690, 3220, 3760], "card_star": 0, "card_extra": 0},
    24: {"name": "银明台", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2, "sub_mat": "镇龍锁", "sub_per": 2, "progress": [0, 1070, 2160, 2690, 3220, 3760], "card_star": 0, "card_extra": 0},
}

MAP_POINTS = {
    "北郡": list(range(1, 7)),
    "琅琊盆地": list(range(7, 13)),
    "昆仑": list(range(13, 19)),
    "轩辕": list(range(19, 25)),
}

ALL_MATERIALS = sorted({
    p["main_mat"] for p in FENG_SHUI_POINTS.values()
} | {
    p["sub_mat"] for p in FENG_SHUI_POINTS.values() if p["sub_mat"]
})


# ============================================================
# 辅助函数
# ============================================================

def get_map_materials(map_name: str) -> list:
    """获取某宝图涉及的所有材料名"""
    pids = MAP_POINTS.get(map_name, [])
    mat_set = set()
    for pid in pids:
        p = FENG_SHUI_POINTS[pid]
        mat_set.add(p["main_mat"])
        if p["sub_mat"]:
            mat_set.add(p["sub_mat"])
    return sorted(mat_set)


# ============================================================
# 计算函数
# ============================================================

def calc_point_cost(pid: int, start_star: int, target_star: int) -> dict:
    """计算单个风水点从 start_star 升到 target_star 的材料消耗。"""
    pt = FENG_SHUI_POINTS[pid]
    prog = pt["progress"]

    delta = prog[target_star] - prog[start_star]
    main_cost = delta * pt["main_per"]
    sub_cost = 0
    if pt["sub_mat"]:
        sub_cost = delta * pt["sub_per"]

    card_extra_main = 0
    cs = pt["card_star"]
    if cs > 0 and start_star < cs <= target_star:
        card_extra_main = pt["card_extra"]

    main_cost += card_extra_main

    return {
        "main_mat": pt["main_mat"],
        "main_cost": main_cost,
        "sub_mat": pt["sub_mat"],
        "sub_cost": sub_cost,
    }


def eval_single_point(pid: int, cur_star: int, materials: dict) -> dict:
    """对单个风水点，根据持有材料计算可达最高星级。"""
    pt = FENG_SHUI_POINTS[pid]
    available = dict(materials)
    original = dict(materials)
    used = {}

    star = cur_star
    while star < 5:
        next_star = star + 1
        cost_info = calc_point_cost(pid, star, next_star)

        main_need = cost_info["main_cost"]
        main_mat = cost_info["main_mat"]
        have_main = available.get(main_mat, 0)

        if have_main < main_need:
            break

        sub_mat = cost_info["sub_mat"]
        sub_need = cost_info["sub_cost"]
        if sub_mat and sub_need > 0:
            have_sub = available.get(sub_mat, 0)
            if have_sub < sub_need:
                break

        available[main_mat] = have_main - main_need
        used[main_mat] = used.get(main_mat, 0) + main_need
        if sub_mat and sub_need > 0:
            available[sub_mat] = available.get(sub_mat, 0) - sub_need
            used[sub_mat] = used.get(sub_mat, 0) + sub_need

        star = next_star

    return {"reach_star": star, "used": used, "original": original}
