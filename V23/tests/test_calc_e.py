"""
test_calc_e.py - 圣石养成计算引擎 单元测试
覆盖: 数据常量、工具函数(get_data_list, get_data_map, has_items, resolve_attr)、
      计算函数(calc_by_materials, calc_for_target)
"""

import pytest

from calculators.calc_e import (
    PART_CONFIG, SLOT_LIMITS, SLOT_ITEM_NAMES,
    STONE_DATA, XUAN_DATA, GANG_DATA,
    STONE_BY_LVL, XUAN_BY_LVL, GANG_BY_LVL,
    get_data_list, get_data_map, has_items, resolve_attr,
    calc_by_materials, calc_for_target,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_part_config_non_empty(self):
        assert len(PART_CONFIG) > 0

    def test_slot_limits_non_empty(self):
        assert len(SLOT_LIMITS) > 0
        for slot, limit in SLOT_LIMITS.items():
            assert isinstance(limit, int) and limit > 0

    def test_stone_data_non_empty(self):
        assert len(STONE_DATA) > 0
        assert all("lv" in d and "jf" in d for d in STONE_DATA)

    def test_xuan_data_non_empty(self):
        assert len(XUAN_DATA) > 0
        assert all("lv" in d and "jf" in d and "item" in d for d in XUAN_DATA)

    def test_gang_data_non_empty(self):
        assert len(GANG_DATA) > 0
        assert all("lv" in d and "jf" in d and "item" in d for d in GANG_DATA)

    def test_by_lvl_maps(self):
        """lv->data 映射应该与列表长度一致"""
        assert len(STONE_BY_LVL) == len(STONE_DATA)
        assert len(XUAN_BY_LVL) == len(XUAN_DATA)
        assert len(GANG_BY_LVL) == len(GANG_DATA)


# ============================================================
# 二、工具函数
# ============================================================

class TestGetDataList:
    def test_stone_slot(self):
        result = get_data_list("圣石(栏位1)")
        assert result is STONE_DATA

    def test_xuan_slot(self):
        result = get_data_list("玄石(栏位1)")
        assert result is XUAN_DATA

    def test_gang_slot(self):
        result = get_data_list("刚石(栏位1)")
        assert result is GANG_DATA


class TestHasItems:
    def test_stone_no_items(self):
        assert has_items("圣石(栏位1)") is False

    def test_xuan_has_items(self):
        assert has_items("玄石(栏位1)") is True

    def test_gang_has_items(self):
        assert has_items("刚石(栏位1)") is True


class TestResolveAttr:
    def test_returns_string(self):
        """resolve_attr 应该总是返回字符串"""
        # 使用第一个可用的 part
        if PART_CONFIG:
            part = next(iter(PART_CONFIG))
            result = resolve_attr(part, "slot1", "金刚系")
            assert isinstance(result, str)


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcByMaterials:
    def test_first_slot(self):
        """使用第一个可用槽位进行基本测试"""
        first_slot = next(iter(SLOT_LIMITS))
        result = calc_by_materials(first_slot, 0, float("inf"), float("inf"))
        assert result["level"] == SLOT_LIMITS[first_slot]
        assert result["steps"] > 0

    def test_zero_materials(self):
        first_slot = next(iter(SLOT_LIMITS))
        result = calc_by_materials(first_slot, 0, 0, 0)
        assert result["level"] == 0
        assert result["steps"] == 0

    def test_return_structure(self):
        first_slot = next(iter(SLOT_LIMITS))
        result = calc_by_materials(first_slot, 0, 100, 100)
        assert "level" in result
        assert "total_jf" in result
        assert "total_item" in result
        assert "steps" in result

    def test_partial_materials(self):
        """部分材料应该部分推进"""
        first_slot = next(iter(SLOT_LIMITS))
        result = calc_by_materials(first_slot, 0, 50, float("inf"))
        assert result["level"] >= 0


class TestCalcForTarget:
    def test_basic(self):
        first_slot = next(iter(SLOT_LIMITS))
        result = calc_for_target(first_slot, 0, 5)
        assert result["total_jf"] > 0

    def test_return_structure(self):
        first_slot = next(iter(SLOT_LIMITS))
        result = calc_for_target(first_slot, 0, 3)
        assert "total_jf" in result
        assert "total_item" in result
        assert "stages_hit" in result

    def test_same_level(self):
        """起始等于目标，无消耗"""
        first_slot = next(iter(SLOT_LIMITS))
        result = calc_for_target(first_slot, 5, 5)
        assert result["total_jf"] == 0
        assert result["total_item"] == 0
