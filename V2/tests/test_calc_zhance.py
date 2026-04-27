"""
test_calc_zhance.py - 占测养成计算器 单元测试
覆盖: 数据常量、工具函数(pos_to_index, format_number)、
      计算函数(calc_by_materials, calc_by_target)
"""

import pytest

from calculators.calc_zhance import (
    SERIES_CONFIG, SERIES_ORDER, TIER_MAX_LEVELS, ALL_TIERS,
    TIER_SERIES, LEVEL_DATA, CUM_DATA,
    pos_to_index, format_number,
    calc_by_materials, calc_by_target,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_series_order(self):
        assert SERIES_ORDER == ['普通', '玄', '地']

    def test_series_config_keys(self):
        for series in SERIES_ORDER:
            cfg = SERIES_CONFIG[series]
            assert 'tiers' in cfg
            assert 'mat1_name' in cfg
            assert 'mat2_name' in cfg

    def test_all_tiers(self):
        assert ALL_TIERS == list(range(1, 18))

    def test_tier_max_levels(self):
        for tier in ALL_TIERS:
            assert tier in TIER_MAX_LEVELS
            assert TIER_MAX_LEVELS[tier] > 0

    def test_tier_series_coverage(self):
        for tier in ALL_TIERS:
            assert tier in TIER_SERIES
            assert TIER_SERIES[tier] in SERIES_ORDER

    def test_level_data_non_empty(self):
        assert len(LEVEL_DATA) > 0

    def test_level_data_keys(self):
        for key, val in LEVEL_DATA.items():
            assert isinstance(key, tuple) and len(key) == 2
            assert 'mat1' in val
            assert 'mat2' in val
            assert 'copper' in val

    def test_cum_data_non_empty(self):
        assert len(CUM_DATA) > 0


# ============================================================
# 二、工具函数
# ============================================================

class TestPosToIndex:
    def test_first_position(self):
        idx = pos_to_index(1, 1)
        assert idx == 1

    def test_zero_level(self):
        idx = pos_to_index(1, 0)
        assert idx == 0

    def test_increasing_order(self):
        """高阶高重序号应更大"""
        idx1 = pos_to_index(1, 1)
        idx2 = pos_to_index(2, 1)
        assert idx2 > idx1

    def test_same_tier_increasing(self):
        idx1 = pos_to_index(1, 1)
        idx2 = pos_to_index(1, 2)
        assert idx2 > idx1


class TestFormatNumber:
    def test_integer(self):
        assert format_number(1000) == "1,000"

    def test_non_integer(self):
        result = format_number("abc")
        assert result == "abc"


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcByMaterials:
    def test_invalid_start_level(self):
        max_lv = TIER_MAX_LEVELS[1]
        materials = {(s, t): 0 for s in SERIES_ORDER for t in ('mat1', 'mat2')}
        result = calc_by_materials(1, max_lv + 1, materials, 0)
        assert result["error"] is not None

    def test_zero_materials(self):
        materials = {(s, t): 0 for s in SERIES_ORDER for t in ('mat1', 'mat2')}
        result = calc_by_materials(1, 0, materials, 0)
        assert result["error"] is not None  # "请输入至少一种材料的数量"

    def test_basic_calc(self):
        materials = {(s, t): 9999 for s in SERIES_ORDER for t in ('mat1', 'mat2')}
        result = calc_by_materials(1, 0, materials, 9999999)
        assert result["error"] is None
        assert result["final_tier"] >= 1
        assert result["final_level"] >= 1

    def test_return_structure(self):
        materials = {(s, t): 100 for s in SERIES_ORDER for t in ('mat1', 'mat2')}
        result = calc_by_materials(1, 0, materials, 10000)
        assert "final_tier" in result
        assert "final_level" in result
        assert "used" in result
        assert "used_copper" in result
        assert "path" in result

    def test_stopped_reason(self):
        """材料不足应有停止原因"""
        materials = {(s, t): 1 for s in SERIES_ORDER for t in ('mat1', 'mat2')}
        result = calc_by_materials(1, 0, materials, 100)
        assert result["error"] is None
        assert "stopped_reason" in result


class TestCalcByTarget:
    def test_invalid_start(self):
        result = calc_by_target(1, 999, 2, 1)
        assert result["error"] is not None

    def test_invalid_target(self):
        result = calc_by_target(1, 0, 1, 999)
        assert result["error"] is not None

    def test_target_less_than_start(self):
        result = calc_by_target(2, 1, 1, 1)
        assert result["error"] is not None

    def test_basic_calc(self):
        result = calc_by_target(1, 0, 1, TIER_MAX_LEVELS[1])
        assert result["error"] is None
        assert result["required_copper"] > 0
        assert len(result["path"]) > 0

    def test_cross_tier(self):
        """跨阶计算"""
        result = calc_by_target(1, 0, 2, 1)
        assert result["error"] is None
        assert len(result["path"]) > 0

    def test_return_structure(self):
        result = calc_by_target(1, 0, 1, 2)
        assert "required" in result
        assert "required_copper" in result
        assert "path" in result
