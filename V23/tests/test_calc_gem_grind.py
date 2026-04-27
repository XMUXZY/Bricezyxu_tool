"""
test_calc_gem_grind.py - 宝石磨砺养成计算器 单元测试
覆盖: 数据常量、工具函数(get_data, format_number)、
      计算函数(calc_by_materials, calc_for_target)
"""

import pytest

from calculators.calc_gem_grind import (
    GRIND_DATA_POS12, GRIND_DATA_POS3, POS3_MAT_MAP,
    COPPER_PER_LEVEL, MAX_LEVEL,
    get_data, format_number,
    calc_by_materials, calc_for_target,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_pos12_data_length(self):
        assert len(GRIND_DATA_POS12) == MAX_LEVEL

    def test_pos3_data_length(self):
        assert len(GRIND_DATA_POS3) == MAX_LEVEL

    def test_data_keys(self):
        for d in GRIND_DATA_POS12:
            assert "level" in d
            assert "stage" in d
            assert "mat" in d
            assert "qty" in d
            assert "prob" in d
            assert "acc" in d

    def test_level_sequence(self):
        for i, d in enumerate(GRIND_DATA_POS12):
            assert d["level"] == i + 1

    def test_pos3_mat_mapping(self):
        """镶嵌位3的材料名正确映射"""
        for d12, d3 in zip(GRIND_DATA_POS12, GRIND_DATA_POS3):
            if d12["mat"] in POS3_MAT_MAP:
                assert d3["mat"] == POS3_MAT_MAP[d12["mat"]]

    def test_prob_range(self):
        for d in GRIND_DATA_POS12:
            assert 0 < d["prob"] <= 100

    def test_copper_per_level(self):
        assert COPPER_PER_LEVEL == 10000

    def test_max_level(self):
        assert MAX_LEVEL == 40

    def test_pos3_mat_names_different(self):
        """镶嵌位3和镶嵌位1/2的材料名不同"""
        pos12_mats = {d["mat"] for d in GRIND_DATA_POS12}
        pos3_mats = {d["mat"] for d in GRIND_DATA_POS3}
        # 映射后名字应不同（除非映射为自身）
        for m12, m3 in POS3_MAT_MAP.items():
            assert m12 != m3


# ============================================================
# 二、工具函数
# ============================================================

class TestGetData:
    def test_pos12(self):
        assert get_data(False) is GRIND_DATA_POS12

    def test_pos3(self):
        assert get_data(True) is GRIND_DATA_POS3


class TestFormatNumber:
    def test_integer(self):
        assert format_number(100) == "100"

    def test_float_whole(self):
        assert format_number(100.0) == "100"

    def test_float_decimal(self):
        result = format_number(123.4)
        assert "123.4" in result

    def test_large_integer(self):
        assert format_number(10000) == "10,000"


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcByMaterials:
    def _make_mats(self, is_pos3, val):
        data = get_data(is_pos3)
        mat_names = list({d["mat"] for d in data})
        return {m: val for m in mat_names}

    def test_invalid_level(self):
        mats = self._make_mats(False, 100)
        result = calc_by_materials(-1, False, False, mats, 999999)
        assert result["error"] is not None

        result = calc_by_materials(41, False, False, mats, 999999)
        assert result["error"] is not None

    def test_all_infinite_error(self):
        """全部无限应该报错"""
        mats = self._make_mats(False, float("inf"))
        result = calc_by_materials(0, False, False, mats, float("inf"))
        assert result["error"] is not None

    def test_zero_materials(self):
        mats = self._make_mats(False, 0)
        result = calc_by_materials(0, False, False, mats, 0)
        assert result["error"] is None
        assert result["final_level"] == 0

    def test_basic_calc(self):
        mats = self._make_mats(False, 9999)
        result = calc_by_materials(0, False, False, mats, 999999)
        assert result["error"] is None
        assert result["final_level"] > 0

    def test_expected_mode(self):
        """期望值模式消耗更多"""
        mats = self._make_mats(False, 500)
        det_result = calc_by_materials(0, False, False, mats.copy(), 999999)
        exp_result = calc_by_materials(0, False, True, mats.copy(), 999999)
        # 期望模式消耗更多材料，达到等级更低
        assert exp_result["final_level"] <= det_result["final_level"]

    def test_return_structure(self):
        mats = self._make_mats(False, 100)
        result = calc_by_materials(0, False, False, mats, 100000)
        assert "error" in result
        assert "final_level" in result
        assert "used_mats" in result
        assert "used_copper" in result
        assert "table_data" in result


class TestCalcForTarget:
    def test_invalid_levels(self):
        assert calc_for_target(-1, 10, False)["error"] is not None
        assert calc_for_target(0, 41, False)["error"] is not None
        assert calc_for_target(10, 5, False)["error"] is not None

    def test_basic_calc(self):
        result = calc_for_target(0, 10, False)
        assert result["error"] is None
        assert result["total_copper"] == 10 * COPPER_PER_LEVEL
        assert len(result["table_data"]) == 10

    def test_expected_higher(self):
        """期望消耗总是 >= 确定消耗"""
        result = calc_for_target(0, 20, False)
        assert result["error"] is None
        for mat, det_qty in result["total_mats_det"].items():
            exp_qty = result["total_mats_exp"].get(mat, 0)
            assert exp_qty >= det_qty

    def test_pos3_different_mats(self):
        """镶嵌位3使用不同材料名"""
        r12 = calc_for_target(0, 5, False)
        r3 = calc_for_target(0, 5, True)
        mats12 = set(r12["total_mats_det"].keys())
        mats3 = set(r3["total_mats_det"].keys())
        assert mats12 != mats3

    def test_return_structure(self):
        result = calc_for_target(0, 5, False)
        assert "total_mats_det" in result
        assert "total_mats_exp" in result
        assert "total_copper" in result
        assert "table_data" in result
