"""
test_calc_star_map.py - 星图养成计算引擎 单元测试
覆盖: 数据常量、工具函数(get_material_for_weight)、
      计算函数(calc_upgrade_material, calc_quick_expected, simulate_hammer)
"""

import pytest

from calculators.calc_star_map import (
    STAR_MAPS, MAX_WEIGHT, MAX_LEVEL,
    WEIGHT_MATERIAL_COST, HAMMER_EXPECTED, HAMMER_PARAMS,
    get_material_for_weight,
    calc_upgrade_material, simulate_hammer, calc_quick_expected,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_star_maps_non_empty(self):
        assert len(STAR_MAPS) > 0

    def test_max_weight(self):
        assert MAX_WEIGHT > 0

    def test_max_level(self):
        assert MAX_LEVEL > 0

    def test_weight_material_cost(self):
        for w in range(1, MAX_WEIGHT + 1):
            assert w in WEIGHT_MATERIAL_COST
            assert WEIGHT_MATERIAL_COST[w] == w * 10

    def test_hammer_expected_non_empty(self):
        assert len(HAMMER_EXPECTED) > 0

    def test_hammer_params_non_empty(self):
        assert len(HAMMER_PARAMS) > 0

    def test_hammer_params_structure(self):
        for key, val in HAMMER_PARAMS.items():
            assert "star_map" in val
            assert "weight" in val
            assert "level" in val
            assert "base_rate" in val
            assert "cost" in val
            assert 0 <= val["base_rate"] <= 1


# ============================================================
# 二、工具函数
# ============================================================

class TestGetMaterialForWeight:
    def test_low_weight(self):
        for w in range(1, 5):
            assert get_material_for_weight(w) == "碧木星砂"

    def test_mid_weight(self):
        for w in range(5, 8):
            assert get_material_for_weight(w) == "云隐星砂"

    def test_high_weight(self):
        for w in range(8, MAX_WEIGHT + 1):
            assert get_material_for_weight(w) == "龙威星砂"


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcUpgradeMaterial:
    def test_basic(self):
        star_map = next(iter(STAR_MAPS))
        result = calc_upgrade_material(star_map, [], 0, 1)
        assert result["total"] > 0
        assert result["per_official"] > 0
        assert "mat_name" in result
        assert len(result["details"]) == 1

    def test_multiple_weights(self):
        star_map = next(iter(STAR_MAPS))
        result = calc_upgrade_material(star_map, [], 0, 3)
        assert len(result["details"]) == 3
        assert result["total"] == sum(d["total"] for d in result["details"])

    def test_specific_officials(self):
        star_map = next(iter(STAR_MAPS))
        info = STAR_MAPS[star_map]
        officials = info["officials"][:2]  # 选前2个
        result = calc_upgrade_material(star_map, officials, 0, 1)
        assert result["count"] == 2


class TestCalcQuickExpected:
    def test_basic(self):
        star_map = next(iter(STAR_MAPS))
        result = calc_quick_expected(star_map, 0, 2)
        assert result["total"] >= 0
        assert len(result["by_w"]) == 2  # weight 1, 2

    def test_return_structure(self):
        star_map = next(iter(STAR_MAPS))
        result = calc_quick_expected(star_map, 0, 1)
        assert "total" in result
        assert "by_w" in result
        if 1 in result["by_w"]:
            assert "expected" in result["by_w"][1]
            assert "mat" in result["by_w"][1]


class TestSimulateHammer:
    def test_basic_simulation(self):
        """蒙特卡洛模拟基本测试（小样本）"""
        star_map = next(iter(STAR_MAPS))
        # 使用小规模模拟
        result = simulate_hammer(star_map, 1, 1, 1, 2, n=100)
        assert "expected" in result
        assert "median" in result
        assert "min" in result
        assert "max" in result
        assert result["min"] <= result["median"] <= result["max"]
        assert result["n"] == 100
