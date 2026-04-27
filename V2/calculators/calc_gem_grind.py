"""
宝石磨砺养成计算器 - 纯计算模块
从 pages/tool_gem_grind.py 提取，不含任何 UI 依赖。

支持两种计算模式：
  模式一：根据已有材料计算可达到的磨砺等级（含期望值）
  模式二：根据目标等级计算所需材料（确定消耗 + 考虑失败的期望值）
"""

# ============================================================
# 一、逐级消耗数据表
# ============================================================

# 镶嵌位1/2 数据
GRIND_DATA_POS12 = [
    {"level": 1,  "stage": 1, "mat": "青暗紫砂", "qty": 4,  "prob": 100, "acc": 5},
    {"level": 2,  "stage": 1, "mat": "青暗紫砂", "qty": 8,  "prob": 100, "acc": 5},
    {"level": 3,  "stage": 1, "mat": "青暗紫砂", "qty": 8,  "prob": 100, "acc": 5},
    {"level": 4,  "stage": 1, "mat": "青暗紫砂", "qty": 16, "prob": 100, "acc": 5},
    {"level": 5,  "stage": 1, "mat": "青暗紫砂", "qty": 16, "prob": 90,  "acc": 5},
    {"level": 6,  "stage": 1, "mat": "青暗紫砂", "qty": 24, "prob": 90,  "acc": 5},
    {"level": 7,  "stage": 1, "mat": "青暗紫砂", "qty": 24, "prob": 90,  "acc": 5},
    {"level": 8,  "stage": 1, "mat": "青暗紫砂", "qty": 32, "prob": 90,  "acc": 5},
    {"level": 9,  "stage": 1, "mat": "青暗紫砂", "qty": 32, "prob": 80,  "acc": 4},
    {"level": 10, "stage": 1, "mat": "青暗紫砂", "qty": 40, "prob": 80,  "acc": 4, "unlock": "玩家等级≥210"},
    {"level": 11, "stage": 1, "mat": "青暗紫砂", "qty": 40, "prob": 80,  "acc": 4},
    {"level": 12, "stage": 1, "mat": "青暗紫砂", "qty": 48, "prob": 80,  "acc": 4},
    {"level": 13, "stage": 1, "mat": "青暗紫砂", "qty": 48, "prob": 70,  "acc": 3},
    {"level": 14, "stage": 1, "mat": "青暗紫砂", "qty": 56, "prob": 70,  "acc": 3},
    {"level": 15, "stage": 1, "mat": "青暗紫砂", "qty": 56, "prob": 70,  "acc": 3},
    {"level": 16, "stage": 1, "mat": "青暗紫砂", "qty": 64, "prob": 60,  "acc": 2},
    {"level": 17, "stage": 1, "mat": "青暗紫砂", "qty": 64, "prob": 60,  "acc": 2},
    {"level": 18, "stage": 1, "mat": "青暗紫砂", "qty": 72, "prob": 60,  "acc": 2},
    {"level": 19, "stage": 1, "mat": "青暗紫砂", "qty": 72, "prob": 50,  "acc": 2},
    {"level": 20, "stage": 1, "mat": "青暗紫砂", "qty": 80, "prob": 50,  "acc": 2},
    {"level": 21, "stage": 2, "mat": "墨紫玉砂", "qty": 4,  "prob": 80,  "acc": 4},
    {"level": 22, "stage": 2, "mat": "墨紫玉砂", "qty": 8,  "prob": 80,  "acc": 4},
    {"level": 23, "stage": 2, "mat": "墨紫玉砂", "qty": 8,  "prob": 70,  "acc": 3},
    {"level": 24, "stage": 2, "mat": "墨紫玉砂", "qty": 16, "prob": 70,  "acc": 3},
    {"level": 25, "stage": 2, "mat": "墨紫玉砂", "qty": 16, "prob": 70,  "acc": 3},
    {"level": 26, "stage": 2, "mat": "墨紫玉砂", "qty": 24, "prob": 60,  "acc": 2},
    {"level": 27, "stage": 2, "mat": "墨紫玉砂", "qty": 24, "prob": 60,  "acc": 2},
    {"level": 28, "stage": 2, "mat": "墨紫玉砂", "qty": 32, "prob": 50,  "acc": 2},
    {"level": 29, "stage": 2, "mat": "墨紫玉砂", "qty": 40, "prob": 40,  "acc": 2},
    {"level": 30, "stage": 3, "mat": "琉璃灵砂", "qty": 4,  "prob": 60,  "acc": 5},
    {"level": 31, "stage": 3, "mat": "琉璃灵砂", "qty": 4,  "prob": 60,  "acc": 5},
    {"level": 32, "stage": 3, "mat": "琉璃灵砂", "qty": 8,  "prob": 50,  "acc": 5},
    {"level": 33, "stage": 3, "mat": "琉璃灵砂", "qty": 8,  "prob": 45,  "acc": 4},
    {"level": 34, "stage": 3, "mat": "琉璃灵砂", "qty": 16, "prob": 45,  "acc": 4},
    {"level": 35, "stage": 3, "mat": "琉璃灵砂", "qty": 16, "prob": 40,  "acc": 4},
    {"level": 36, "stage": 3, "mat": "琉璃灵砂", "qty": 24, "prob": 35,  "acc": 3},
    {"level": 37, "stage": 3, "mat": "琉璃灵砂", "qty": 24, "prob": 30,  "acc": 3},
    {"level": 38, "stage": 3, "mat": "琉璃灵砂", "qty": 32, "prob": 25,  "acc": 3},
    {"level": 39, "stage": 3, "mat": "琉璃灵砂", "qty": 32, "prob": 20,  "acc": 3},
    {"level": 40, "stage": 3, "mat": "琉璃灵砂", "qty": 40, "prob": 20,  "acc": 3},
]

# 镶嵌位3 材料映射
POS3_MAT_MAP = {
    "青暗紫砂": "邃夜黑砂",
    "墨紫玉砂": "乌金玉砂",
    "琉璃灵砂": "黑曜灵砂",
}

# 镶嵌位3 数据（材料名不同，数量相同）
GRIND_DATA_POS3 = []
for _row in GRIND_DATA_POS12:
    _new = dict(_row)
    _new["mat"] = POS3_MAT_MAP.get(_row["mat"], _row["mat"])
    GRIND_DATA_POS3.append(_new)

COPPER_PER_LEVEL = 10000
MAX_LEVEL = 40


# ============================================================
# 二、工具函数
# ============================================================

def get_data(is_pos3: bool) -> list:
    """根据镶嵌位获取对应数据表"""
    return GRIND_DATA_POS3 if is_pos3 else GRIND_DATA_POS12


def format_number(num) -> str:
    """格式化数字（与原页面 _fmt 一致）"""
    if isinstance(num, float):
        if num == int(num):
            return f"{int(num):,}"
        return f"{num:,.1f}"
    return f"{num:,}"


# ============================================================
# 三、计算函数
# ============================================================

def calc_by_materials(cur_lv: int, is_pos3: bool, use_expected: bool,
                      mats: dict, copper: float) -> dict:
    """
    模式一：根据材料计算可达等级

    参数:
        cur_lv:        当前磨砺等级 (0~40)
        is_pos3:       是否为镶嵌位3
        use_expected:  是否使用期望值模式
        mats:          材料持有量 {材料名: 数量}，float('inf') 表示无限
        copper:        铜钱持有量 (float)，float('inf') 表示无限

    返回:
        {
            "error": str|None,
            "final_level": int,
            "used_mats": dict,
            "used_copper": float,
            "table_data": list,   # 逐级明细 (UI 可直接使用)
        }
    """
    if cur_lv < 0 or cur_lv > MAX_LEVEL:
        return {"error": f"磨砺等级需在 0 ~ {MAX_LEVEL}"}

    data = get_data(is_pos3)

    # 检查是否全部为无限
    all_empty = (
        all(v == float("inf") for v in mats.values())
        and copper == float("inf")
    )
    if all_empty:
        return {"error": "请至少输入一种材料的数量！"}

    lv = cur_lv
    remaining_mats = dict(mats)
    remaining_copper = copper
    used_mats = {k: 0.0 for k in mats}
    used_copper = 0.0
    table_data = []

    for row in data:
        if lv >= row["level"]:
            continue

        qty = row["qty"]
        prob = row["prob"]

        if use_expected and prob < 100:
            cost_qty = qty / (prob / 100.0)
        else:
            cost_qty = qty

        cost_copper = COPPER_PER_LEVEL

        # 检查材料是否足够
        mat_ok = True
        copper_ok = True
        if remaining_mats[row["mat"]] != float("inf"):
            if remaining_mats[row["mat"]] < cost_qty:
                mat_ok = False
        if remaining_copper != float("inf"):
            if remaining_copper < cost_copper:
                copper_ok = False

        if not mat_ok or not copper_ok:
            lack_info = []
            if not mat_ok:
                lack = cost_qty - remaining_mats[row["mat"]]
                lack_info.append(f"材料差{format_number(lack)}")
            if not copper_ok:
                lack_info.append(f"铜钱差{format_number(cost_copper - remaining_copper)}")

            table_data.append([
                row["level"], row["mat"], format_number(cost_qty),
                f"{cost_copper / 10000:.1f}万", f"{prob}%",
                row.get("unlock", ""), f"❌ {', '.join(lack_info)}"
            ])
            break

        # 扣除材料
        if remaining_mats[row["mat"]] != float("inf"):
            remaining_mats[row["mat"]] -= cost_qty
            used_mats[row["mat"]] += cost_qty
        if remaining_copper != float("inf"):
            remaining_copper -= cost_copper
            used_copper += cost_copper

        lv = row["level"]

        if prob < 100:
            prob_note = "期望值" if use_expected else "忽略概率"
        else:
            prob_note = "必成功"

        table_data.append([
            row["level"], row["mat"], format_number(cost_qty),
            f"{cost_copper / 10000:.1f}万", f"{prob}%",
            row.get("unlock", ""), f"✅ {prob_note}"
        ])

    return {
        "error": None,
        "final_level": lv,
        "used_mats": used_mats,
        "used_copper": used_copper,
        "table_data": table_data,
    }


def calc_for_target(start_lv: int, target_lv: int, is_pos3: bool) -> dict:
    """
    模式二：根据目标等级计算所需材料

    参数:
        start_lv:  起始等级
        target_lv: 目标等级
        is_pos3:   是否为镶嵌位3

    返回:
        {
            "error": str|None,
            "total_mats_det": dict,   # 确定消耗 {材料名: 数量}
            "total_mats_exp": dict,   # 期望消耗 {材料名: 数量}
            "total_copper": int,
            "table_data": list,
        }
    """
    if start_lv < 0 or start_lv > MAX_LEVEL:
        return {"error": f"起始等级需在 0 ~ {MAX_LEVEL}"}
    if target_lv < 0 or target_lv > MAX_LEVEL:
        return {"error": f"目标等级需在 0 ~ {MAX_LEVEL}"}
    if target_lv <= start_lv:
        return {"error": "目标等级必须大于起始等级！"}

    data = get_data(is_pos3)

    total_mats_det = {}
    total_mats_exp = {}
    total_copper = 0
    table_data = []

    for row in data:
        if row["level"] <= start_lv:
            continue
        if row["level"] > target_lv:
            break

        mat = row["mat"]
        qty = row["qty"]
        prob = row["prob"]
        cop = COPPER_PER_LEVEL

        total_mats_det[mat] = total_mats_det.get(mat, 0) + qty
        total_copper += cop

        if prob >= 100:
            exp_qty = qty
        else:
            exp_qty = qty / (prob / 100.0)
        total_mats_exp[mat] = total_mats_exp.get(mat, 0) + exp_qty

        prob_note = "必成功" if prob >= 100 else f"{prob}%"
        extra = exp_qty - qty
        extra_note = f"(期望+{extra:.1f})" if extra > 0.01 else ""

        table_data.append([
            row["level"], mat, qty, f"{exp_qty:.1f}", extra_note,
            prob_note, f"{cop / 10000:.1f}万", row.get("unlock", "")
        ])

    return {
        "error": None,
        "total_mats_det": total_mats_det,
        "total_mats_exp": total_mats_exp,
        "total_copper": total_copper,
        "table_data": table_data,
    }
