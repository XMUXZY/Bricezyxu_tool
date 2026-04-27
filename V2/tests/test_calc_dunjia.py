"""
test_calc_dunjia.py - 遁甲（强运）养成计算器 单元测试
覆盖: 配置常量、辅助查询、计算函数(calc_reachable_level, calc_required_materials)
"""

import pytest

from calculators.calc_dunjia import (
    GRADES, GRADE_ORDER, LEVEL_DATA,
    get_level_cost, get_cumulative_cost, get_ability,
    calc_reachable_level, calc_required_materials,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_grade_order(self):
        assert GRADE_ORDER == ['黄阶', '玄阶', '地阶', '天阶']

    def test_grades_config(self):
        for grade in GRADE_ORDER:
            cfg = GRADES[grade]
            assert "max_level" in cfg
            assert "material" in cfg
            assert cfg["max_level"] > 0

    def test_grades_max_levels(self):
        assert GRADES['黄阶']['max_level'] == 36
        assert GRADES['玄阶']['max_level'] == 49
        assert GRADES['地阶']['max_level'] == 64
        assert GRADES['天阶']['max_level'] == 100

    def test_level_data_coverage(self):
        """每个品阶每个等级都应有数据"""
        for grade in GRADE_ORDER:
            max_lv = GRADES[grade]['max_level']
            for lv in range(1, max_lv + 1):
                assert (grade, lv) in LEVEL_DATA, f"缺少 ({grade}, {lv})"

    def test_level_data_structure(self):
        """数据元组格式: (能力值, 单级消耗, 累计消耗)"""
        for key, val in LEVEL_DATA.items():
            assert isinstance(val, tuple) and len(val) == 3


# ============================================================
# 二、辅助查询
# ============================================================

class TestHelpers:
    def test_get_level_cost_valid(self):
        cost = get_level_cost('黄阶', 1)
        assert cost == 1  # 黄阶每级消耗1个

    def test_get_level_cost_invalid(self):
        cost = get_level_cost('无效品阶', 1)
        assert cost == 0

    def test_get_cumulative_cost(self):
        cum = get_cumulative_cost('黄阶', 5)
        assert cum == 5  # 黄阶每级消耗1，5级累计5

    def test_get_ability(self):
        ability = get_ability('黄阶', 1)
        assert ability == 55  # 黄阶起始能力55

    def test_ability_increasing(self):
        """能力值随等级递增"""
        prev = 0
        for lv in range(1, 37):
            ab = get_ability('黄阶', lv)
            assert ab > prev
            prev = ab

    def test_tian_cost_increasing(self):
        """天阶高等级消耗递增"""
        cost_80 = get_level_cost('天阶', 80)
        cost_90 = get_level_cost('天阶', 90)
        cost_100 = get_level_cost('天阶', 100)
        assert cost_80 <= cost_90 <= cost_100


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcReachableLevel:
    def test_invalid_grade(self):
        result = calc_reachable_level("无效品阶", 0, {"无效品阶": 100})
        assert result["error"] is not None

    def test_invalid_level(self):
        result = calc_reachable_level("黄阶", -1, {"黄阶": 100})
        assert result["error"] is not None

    def test_zero_materials(self):
        result = calc_reachable_level("黄阶", 0, {"黄阶": 0, "玄阶": 0, "地阶": 0, "天阶": 0})
        assert result["error"] is not None  # "请输入至少一种材料的数量"

    def test_basic_calculation(self):
        result = calc_reachable_level("黄阶", 0, {"黄阶": 10, "玄阶": 0, "地阶": 0, "天阶": 0})
        assert result["error"] is None
        assert result["final_grade"] == "黄阶"
        assert result["final_level"] == 10  # 每级消耗1，10个升10级

    def test_cross_grade(self):
        """跨品阶升级"""
        result = calc_reachable_level("黄阶", 0, {"黄阶": 36, "玄阶": 10, "地阶": 0, "天阶": 0})
        assert result["error"] is None
        assert result["final_grade"] == "玄阶"
        assert result["final_level"] == 10

    def test_return_structure(self):
        result = calc_reachable_level("黄阶", 0, {"黄阶": 5})
        assert "error" in result
        assert "final_grade" in result
        assert "final_level" in result
        assert "used_materials" in result
        assert "path" in result


class TestCalcRequiredMaterials:
    def test_invalid_grade(self):
        result = calc_required_materials("无效", 0, "黄阶", 10)
        assert result["error"] is not None

    def test_target_lower_than_start(self):
        result = calc_required_materials("黄阶", 10, "黄阶", 5)
        assert result["error"] is not None

    def test_basic_calc(self):
        result = calc_required_materials("黄阶", 0, "黄阶", 10)
        assert result["error"] is None
        assert result["required"]["黄阶"] == 10  # 每级1个，10级共10个

    def test_cross_grade_calc(self):
        result = calc_required_materials("黄阶", 0, "玄阶", 5)
        assert result["error"] is None
        assert result["required"]["黄阶"] == 36  # 黄阶满级36
        assert result["required"]["玄阶"] == 5   # 玄阶5级

    def test_return_structure(self):
        result = calc_required_materials("黄阶", 0, "黄阶", 5)
        assert "required" in result
        assert "path" in result
        assert "error" in result
