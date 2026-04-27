"""
遁甲（强运）养成计算器 - 纯计算模块
从 pages/tool_dunjia.py 提取，不含任何 UI 依赖。

支持两种计算模式：
  模式一：已知材料 → 计算可达等级
  模式二：已知目标 → 计算所需材料
"""

# ============================================================
# 一、品阶配置
# ============================================================

GRADES = {
    '黄阶': {'max_level': 36, 'material': '古迹灵石', 'material_id': 59011243},
    '玄阶': {'max_level': 49, 'material': '古迹灵石·玄', 'material_id': 59011248},
    '地阶': {'max_level': 64, 'material': '古迹灵石·地', 'material_id': 59011249},
    '天阶': {'max_level': 100, 'material': '古迹灵石·天', 'material_id': 59011250},
}

GRADE_ORDER = ['黄阶', '玄阶', '地阶', '天阶']


# ============================================================
# 二、构建逐级数据
# ============================================================

def _build_level_data() -> dict:
    """
    构建逐级数据字典：(品阶, 等级) -> (能力值, 单级消耗, 累计消耗)
    """
    data_dict = {}

    # 黄阶 1-36级，每级消耗1个
    ability = 55
    for lv in range(1, 37):
        data_dict[('黄阶', lv)] = (ability, 1, lv)
        ability += 110

    # 玄阶 1-49级，每级消耗1个
    ability = 40
    for lv in range(1, 50):
        data_dict[('玄阶', lv)] = (ability, 1, lv)
        ability += 60 + (lv - 1) * 30

    # 地阶 1-64级，每级消耗1个
    ability = 28
    for lv in range(1, 65):
        data_dict[('地阶', lv)] = (ability, 1, lv)
        ability += 14 + (lv - 1) * 36

    # 天阶 1-100级，消耗量递增
    ability = 1590
    cumulative = 0
    for lv in range(1, 101):
        if lv <= 81:
            cost = 1
        elif lv <= 83:
            cost = 2
        elif lv <= 85:
            cost = 3
        elif lv <= 87:
            cost = 4
        elif lv <= 89:
            cost = 6
        elif lv <= 91:
            cost = 8
        elif lv <= 93:
            cost = 10
        elif lv <= 95:
            cost = 12
        elif lv <= 97:
            cost = 14
        elif lv <= 99:
            cost = 16
        else:  # 100
            cost = 18

        cumulative += cost
        data_dict[('天阶', lv)] = (ability, cost, cumulative)
        ability += 9222

    return data_dict


LEVEL_DATA = _build_level_data()


# ============================================================
# 三、辅助查询
# ============================================================

def get_level_cost(grade: str, level: int) -> int:
    """获取指定品阶等级的升级消耗"""
    data = LEVEL_DATA.get((grade, level))
    return data[1] if data else 0


def get_cumulative_cost(grade: str, level: int) -> int:
    """获取品阶内累计消耗"""
    data = LEVEL_DATA.get((grade, level))
    return data[2] if data else 0


def get_ability(grade: str, level: int) -> int:
    """获取能力值"""
    data = LEVEL_DATA.get((grade, level))
    return data[0] if data else 0


# ============================================================
# 四、计算函数
# ============================================================

def calc_reachable_level(start_grade: str, start_level: int,
                         materials: dict) -> dict:
    """
    模式一：根据材料计算可达等级

    参数:
        start_grade:  起始品阶（黄阶/玄阶/地阶/天阶）
        start_level:  起始等级
        materials:    材料持有量 {品阶名: 数量}

    返回:
        {
            "error": str|None,
            "final_grade": str,
            "final_level": int,
            "used_materials": dict,
            "path": list,
        }
    """
    # 验证品阶
    if start_grade not in GRADES:
        return {"error": f"无效的品阶: {start_grade}"}

    max_level = GRADES[start_grade]['max_level']
    if start_level < 0 or start_level > max_level:
        return {"error": f"{start_grade}等级范围为0-{max_level}"}

    if all(v == 0 for v in materials.values()):
        return {"error": "请输入至少一种材料的数量"}

    start_idx = GRADE_ORDER.index(start_grade)
    current_level = start_level
    grade_name = start_grade

    path = []
    used_materials = {grade: 0 for grade in GRADES.keys()}

    for grade_idx in range(start_idx, len(GRADE_ORDER)):
        grade_name = GRADE_ORDER[grade_idx]
        max_lv = GRADES[grade_name]['max_level']
        material_name = GRADES[grade_name]['material']
        available = materials.get(grade_name, 0)

        if grade_idx == start_idx:
            start_lv = current_level
        else:
            start_lv = 0

        for lv in range(start_lv + 1, max_lv + 1):
            cost = get_level_cost(grade_name, lv)

            if used_materials[grade_name] + cost <= available:
                used_materials[grade_name] += cost
                current_level = lv

                cumulative = get_cumulative_cost(grade_name, lv)
                ability = get_ability(grade_name, lv)
                path.append([
                    grade_name,
                    f"Lv.{lv}",
                    ability,
                    f"{material_name} ×{cost}",
                    cumulative,
                    used_materials[grade_name]
                ])
            else:
                break

        if current_level < max_lv:
            break

        # 进阶
        if grade_idx < len(GRADE_ORDER) - 1:
            current_level = 0
            path.append([
                f"【{grade_name}满级】",
                "→",
                f"进阶到{GRADE_ORDER[grade_idx + 1]}",
                "无额外消耗",
                "-",
                "-"
            ])

    final_grade = grade_name
    final_level = current_level

    return {
        "error": None,
        "final_grade": final_grade,
        "final_level": final_level,
        "used_materials": used_materials,
        "path": path,
    }


def calc_required_materials(start_grade: str, start_level: int,
                            end_grade: str, end_level: int) -> dict:
    """
    模式二：根据目标计算所需材料

    参数:
        start_grade:  起始品阶
        start_level:  起始等级
        end_grade:    目标品阶
        end_level:    目标等级

    返回:
        {
            "error": str|None,
            "required": dict,   # {品阶名: 所需数量}
            "path": list,
        }
    """
    if start_grade not in GRADES or end_grade not in GRADES:
        return {"error": "无效的品阶"}

    start_idx = GRADE_ORDER.index(start_grade)
    end_idx = GRADE_ORDER.index(end_grade)

    if end_idx < start_idx or (end_idx == start_idx and end_level <= start_level):
        return {"error": "目标等级必须高于当前等级"}

    required = {grade: 0 for grade in GRADES.keys()}
    path = []

    for grade_idx in range(start_idx, end_idx + 1):
        grade_name = GRADE_ORDER[grade_idx]
        max_lv = GRADES[grade_name]['max_level']
        material_name = GRADES[grade_name]['material']

        if grade_idx == start_idx:
            from_lv = start_level
        else:
            from_lv = 0

        if grade_idx == end_idx:
            to_lv = end_level
        else:
            to_lv = max_lv

        for lv in range(from_lv + 1, to_lv + 1):
            cost = get_level_cost(grade_name, lv)
            required[grade_name] += cost

            cumulative = get_cumulative_cost(grade_name, lv)
            ability = get_ability(grade_name, lv)
            path.append([
                grade_name,
                f"Lv.{lv}",
                ability,
                f"{material_name} ×{cost}",
                cumulative,
                required[grade_name]
            ])

        if grade_idx < end_idx:
            path.append([
                f"【{grade_name}满级】",
                "→",
                f"进阶到{GRADE_ORDER[grade_idx + 1]}",
                "无额外消耗",
                "-",
                "-"
            ])

    return {
        "error": None,
        "start_grade": start_grade,
        "start_level": start_level,
        "end_grade": end_grade,
        "end_level": end_level,
        "required": required,
        "path": path,
    }
