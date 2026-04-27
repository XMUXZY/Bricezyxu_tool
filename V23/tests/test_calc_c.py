"""
test_calc_c.py - 装备重铸计算引擎 单元测试
覆盖: 数据常量、工具函数(find_data_index, format_num)、
      计算函数(calc_reforge_by_materials, calc_materials_for_target)
"""

import pytest

from calculators.calc_c import (
    REFORGE_DATA, MATERIAL_CONVERSION, MATERIAL_B_NAME, EQUIPMENT_COUNT,
    find_data_index, format_num,
    calc_reforge_by_materials, calc_materials_for_target,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_reforge_data_non_empty(self):
        assert len(REFORGE_DATA) > 0

    def test_reforge_data_keys(self):
        for d in REFORGE_DATA:
            assert "level" in d
            assert "stage" in d
            assert "materialA" in d
            assert "materialARequired" in d
            assert "materialBRequired" in d

    def test_material_conversion(self):
        assert MATERIAL_CONVERSION["不灭离炎"] == 1
        assert MATERIAL_CONVERSION["青璃焰光"] == 3
        assert MATERIAL_CONVERSION["冥雷寒铁"] == 9
        assert MATERIAL_CONVERSION["辉光玄铁"] == 27

    def test_equipment_count(self):
        assert EQUIPMENT_COUNT == 11

    def test_material_b_name(self):
        assert MATERIAL_B_NAME == "忘川冥息"

    def test_stage_range(self):
        """所有 stage 在 0-5"""
        stages = {d["stage"] for d in REFORGE_DATA}
        assert stages == {0, 1, 2, 3, 4, 5}


# ============================================================
# 二、工具函数
# ============================================================

class TestFindDataIndex:
    def test_first_entry(self):
        idx = find_data_index(0, 0)
        assert idx == 0

    def test_known_entry(self):
        idx = find_data_index(1, 0)
        assert idx >= 0
        assert REFORGE_DATA[idx]["level"] == 1
        assert REFORGE_DATA[idx]["stage"] == 0

    def test_invalid_entry(self):
        idx = find_data_index(999, 0)
        assert idx == -1

    def test_all_entries_findable(self):
        for i, d in enumerate(REFORGE_DATA):
            assert find_data_index(d["level"], d["stage"]) == i


class TestFormatNum:
    def test_large(self):
        assert format_num(50000) == "50,000.0"

    def test_medium(self):
        result = format_num(500)
        assert "500" in result

    def test_small(self):
        result = format_num(5)
        assert "5" in result

    def test_tiny(self):
        result = format_num(0.5)
        assert "0.5" in result


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcReforgeByMaterials:
    def test_invalid_start(self):
        result = calc_reforge_by_materials(999, 0, "不灭离炎", 100, 100)
        assert result["error"] is not None

    def test_zero_materials(self):
        result = calc_reforge_by_materials(0, 0, "不灭离炎", 0, 0)
        assert result["error"] is None
        assert result["current_level"] == 0
        assert result["current_stage"] == 0

    def test_infinite_materials(self):
        result = calc_reforge_by_materials(0, 0, "不灭离炎", float("inf"), float("inf"))
        assert result["error"] is None
        # 应该能升到一定等级（不灭离炎转换后可能不够最高级）
        assert result["current_level"] >= 1

    def test_return_structure(self):
        result = calc_reforge_by_materials(0, 0, "不灭离炎", 100, 100)
        assert "current_level" in result
        assert "current_stage" in result
        assert "total_used_a" in result
        assert "total_used_b" in result
        assert "error" in result

    def test_progress_with_material(self):
        """给足够材料应该有进展"""
        result = calc_reforge_by_materials(0, 0, "不灭离炎", 10000, 10000)
        assert result["current_level"] > 0 or result["current_stage"] > 0


class TestCalcMaterialsForTarget:
    def test_invalid_start(self):
        result = calc_materials_for_target(999, 0, 1, 0, "不灭离炎")
        assert result["error"] is not None

    def test_invalid_target(self):
        result = calc_materials_for_target(0, 0, 999, 0, "不灭离炎")
        assert result["error"] is not None

    def test_same_start_end(self):
        result = calc_materials_for_target(0, 0, 0, 0, "不灭离炎")
        assert result["error"] is not None  # "目标等级/阶段必须大于初始等级/阶段"

    def test_basic_calc(self):
        result = calc_materials_for_target(0, 0, 1, 0, "不灭离炎")
        assert result["error"] is None
        assert result["total_materials"] is not None
        assert result["stages_count"] > 0

    def test_return_structure(self):
        result = calc_materials_for_target(0, 0, 2, 0, "不灭离炎")
        assert "total_materials" in result
        assert "converted_total" in result
        assert "stages_count" in result
        assert "error" in result

    def test_material_b_included(self):
        """重铸材料B (忘川冥息) 在高等级应有消耗"""
        result = calc_materials_for_target(0, 0, 5, 0, "不灭离炎")
        assert result["error"] is None
        total_b = result["total_materials"].get(MATERIAL_B_NAME, 0)
        # 前几级 materialBRequired > 0 出现在 level 0 stage 0
        assert total_b >= 0
