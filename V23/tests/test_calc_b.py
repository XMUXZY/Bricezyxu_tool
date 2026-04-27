"""
test_calc_b.py - 装备淬炼计算引擎 单元测试
覆盖: 数据常量、工具函数(convert_material, format_number)、计算函数(calc_max_level, calc_materials_for_target)
"""

import math
import pytest

from calculators.calc_b import (
    MATERIAL_NAMES, MATERIAL2_NAME, REFINING_DATA,
    convert_material, to_lowest_material, from_lowest_material,
    format_number,
    calc_max_level, calc_materials_for_target,
)


# ============================================================
# 一、数据常量完整性
# ============================================================

class TestConstants:
    def test_material_names(self):
        assert len(MATERIAL_NAMES) == 4
        assert MATERIAL_NAMES[0] == "曜金矿石"
        assert MATERIAL_NAMES[3] == "诸法舍利"

    def test_material2_name(self):
        assert MATERIAL2_NAME == "蚀日之晶"

    def test_refining_data_length(self):
        # 共 98 级
        assert len(REFINING_DATA) == 98

    def test_refining_data_level_sequence(self):
        for i, data in enumerate(REFINING_DATA):
            assert data["level"] == i + 1

    def test_refining_data_keys(self):
        for data in REFINING_DATA:
            assert "level" in data
            assert "mat1Type" in data
            assert "mat1Count" in data
            assert "mat2Count" in data

    def test_mat1_type_ranges(self):
        """mat1Type 只有 0,1,2,3 四种类型"""
        types = {d["mat1Type"] for d in REFINING_DATA}
        assert types == {0, 1, 2, 3}

    def test_mat1_type_progression(self):
        """材料类型随等级递增"""
        prev_type = 0
        for d in REFINING_DATA:
            assert d["mat1Type"] >= prev_type
            prev_type = d["mat1Type"]


# ============================================================
# 二、工具函数
# ============================================================

class TestConvertMaterial:
    def test_same_type(self):
        assert convert_material(100, 0, 0) == 100
        assert convert_material(50, 2, 2) == 50

    def test_upgrade_one_step(self):
        # 5 个低级 = 1 个高级
        assert convert_material(25, 0, 1) == pytest.approx(5.0)

    def test_upgrade_two_steps(self):
        assert convert_material(125, 0, 2) == pytest.approx(5.0)

    def test_downgrade_one_step(self):
        assert convert_material(1, 1, 0) == pytest.approx(5.0)

    def test_downgrade_two_steps(self):
        assert convert_material(1, 2, 0) == pytest.approx(25.0)

    def test_to_lowest(self):
        assert to_lowest_material(10, 0) == 10
        assert to_lowest_material(10, 1) == pytest.approx(50.0)
        assert to_lowest_material(10, 2) == pytest.approx(250.0)
        assert to_lowest_material(10, 3) == pytest.approx(1250.0)

    def test_from_lowest(self):
        assert from_lowest_material(125, 0) == 125
        assert from_lowest_material(125, 1) == pytest.approx(25.0)
        assert from_lowest_material(125, 2) == pytest.approx(5.0)


class TestFormatNumber:
    def test_zero(self):
        assert format_number(0) == "0"

    def test_large_number(self):
        result = format_number(1500000)
        assert "," in result  # 包含千分位
        assert "." not in result or result.endswith(".0") is False

    def test_medium_number(self):
        result = format_number(12345)
        assert result == "12,345.0"

    def test_small_number(self):
        result = format_number(5.1234)
        # 5.1234 >= 1, < 10 -> 3位小数
        assert "5.123" in result


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcMaxLevel:
    def test_start_at_zero_with_infinite(self):
        """无限材料应该达到最高等级"""
        result = calc_max_level(0, 0, float("inf"), float("inf"))
        assert result["current_level"] == 98
        assert len(result["details"]) == 98

    def test_start_at_zero_no_materials(self):
        """零材料停留在起始等级"""
        result = calc_max_level(0, 0, 0, 0)
        assert result["current_level"] == 0
        assert result["used_mat1_lowest"] == 0.0
        assert result["used_mat2"] == 0.0

    def test_start_at_high_level(self):
        """从较高等级开始"""
        result = calc_max_level(50, 2, float("inf"), float("inf"))
        assert result["current_level"] == 98
        assert len(result["details"]) == 48  # 50->98 共 48 级

    def test_exact_material_for_one_level(self):
        """刚好够升一级"""
        first = REFINING_DATA[0]
        mat1_lowest = to_lowest_material(first["mat1Count"], first["mat1Type"])
        result = calc_max_level(0, first["mat1Type"], mat1_lowest, first["mat2Count"])
        assert result["current_level"] >= 1

    def test_return_structure(self):
        result = calc_max_level(0, 0, 100, 100)
        assert "current_level" in result
        assert "used_mat1_lowest" in result
        assert "used_mat2" in result
        assert "details" in result
        assert isinstance(result["details"], list)


class TestCalcMaterialsForTarget:
    def test_basic_range(self):
        result = calc_materials_for_target(0, 10)
        assert result["total_mat1_lowest"] > 0
        assert "mat1_type_usage" in result
        assert result["highest_mat1_type"] == 0  # 前10级都是type 0

    def test_single_level(self):
        """单级消耗"""
        result = calc_materials_for_target(0, 1)
        assert result["total_mat1_lowest"] > 0
        assert 0 in result["mat1_type_usage"]

    def test_full_range(self):
        """全范围 0->98"""
        result = calc_materials_for_target(0, 98)
        assert result["highest_mat1_type"] == 3  # 最终使用最高级材料

    def test_empty_range(self):
        """相同起止等级"""
        result = calc_materials_for_target(10, 10)
        assert result["total_mat1_lowest"] == 0
        assert result["total_mat2"] == 0

    def test_high_level_type(self):
        """高等级使用高级材料"""
        result = calc_materials_for_target(90, 98)
        assert result["highest_mat1_type"] == 3
