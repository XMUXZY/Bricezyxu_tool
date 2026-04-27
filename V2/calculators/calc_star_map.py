"""
星图养成计算引擎
纯数据 + 纯计算函数，不依赖任何 UI 框架。
"""

import random
from utils.data_loader import load_game_data

# ============================================================
# 从 JSON 加载常量
# ============================================================
_SM_JSON = load_game_data("star_map_data.json")

STAR_MAPS = _SM_JSON["star_maps"]
MAX_WEIGHT = _SM_JSON["max_weight"]
MAX_LEVEL = _SM_JSON["max_level"]

WEIGHT_MATERIAL_COST = {w: w * 10 for w in range(1, MAX_WEIGHT + 1)}

HAMMER_EXPECTED = {}
for _k, _v in _SM_JSON["hammer_expected"].items():
    _name, _w = _k.rsplit("_", 1)
    HAMMER_EXPECTED[(_name, int(_w))] = _v

HAMMER_PARAMS = {}


def _init_hammer_params():
    _inc_rate = _SM_JSON["inc_rate"]
    for name, data in _SM_JSON["hammer_raw_data"].items():
        for w_str, levels in data.items():
            w = int(w_str)
            for lvl, (base, demote, cost) in enumerate(levels, 1):
                key = f"{name}_{w}_{lvl}"
                HAMMER_PARAMS[key] = {
                    "star_map": name, "weight": w, "level": lvl,
                    "base_rate": base / 100.0,
                    "inc_rate": _inc_rate[name],
                    "max_rate": 1.0,
                    "demote_prob": demote / 100.0,
                    "cost": cost,
                }

_init_hammer_params()
del _SM_JSON


# ============================================================
# 纯函数
# ============================================================

def get_material_for_weight(weight: int) -> str:
    if weight <= 4: return "碧木星砂"
    elif weight <= 7: return "云隐星砂"
    else: return "龙威星砂"


def calc_upgrade_material(star_map: str, officials: list, cur_w: int, tgt_w: int) -> dict:
    info = STAR_MAPS[star_map]
    selected = officials if officials else info["officials"]
    total_per_official = sum(WEIGHT_MATERIAL_COST.get(w, 0) for w in range(cur_w + 1, tgt_w + 1))
    total = total_per_official * len(selected)
    details = [{"weight": w, "per": WEIGHT_MATERIAL_COST[w], "total": WEIGHT_MATERIAL_COST[w] * len(selected)}
               for w in range(cur_w + 1, tgt_w + 1)]
    return {"total": total, "per_official": total_per_official, "mat_name": info["material_name"],
            "count": len(selected), "details": details}


def simulate_hammer(star_map, sw, sl, tw, tl, n=10000):
    results = []
    inc = HAMMER_PARAMS[f"{star_map}_1_1"]["inc_rate"]
    for _ in range(n):
        cost, cw, cl, bonus = 0, sw, sl, 0.0
        while (cw < tw) or (cw == tw and cl < tl):
            p = HAMMER_PARAMS[f"{star_map}_{cw}_{cl}"]
            cost += p["cost"]
            if random.random() < min(p["base_rate"] + bonus, p["max_rate"]):
                bonus = 0; cl += 1
                if cl > MAX_LEVEL: cl = 1; cw += 1
            else:
                bonus += inc
                if random.random() < p["demote_prob"]:
                    cl -= 1
                    if cl < 1:
                        if cw > sw: cw -= 1; cl = MAX_LEVEL
                        else: cl = 1
            if cost > 50000: break
        results.append(cost)
    results.sort()
    rn = len(results)
    return {
        "expected": sum(results)/rn, "median": results[rn//2],
        "p10": results[int(rn*0.10)], "p90": results[int(rn*0.90)],
        "min": results[0], "max": results[-1], "n": n,
        "mat": get_material_for_weight(sw),
    }


def calc_quick_expected(star_map, sw, tw):
    result = {"total": 0, "by_w": {}}
    for w in range(sw + 1, tw + 1):
        e = HAMMER_EXPECTED.get((star_map, w), 0)
        result["by_w"][w] = {"expected": e, "mat": get_material_for_weight(w)}
        result["total"] += e
    return result
