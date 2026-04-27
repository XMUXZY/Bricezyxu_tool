"""
test_calc_zhu_ling.py - 注灵养成计算器 单元测试
覆盖: 数据常量、查询函数(get_set_data, get_materials, set_display)、
      计算函数(calc_by_materials, calc_by_target)
"""

import pytest

from calculators.calc_zhu_ling import (
    PART_NAMES, SET_NAMES, DATA,
    get_set_data, get_materials, set_display,
    calc_by_materials, calc_by_target,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_part_names_non_empty(self):
        assert len(PART_NAMES) > 0

    def test_set_names_non_empty(self):
        assert len(SET_NAMES) > 0

    def test_data_non_empty(self):
        assert len(DATA) > 0

    def test_data_keys(self):
        for d in DATA:
            assert "套装" in d
            assert "等级" in d
            assert "开启名" in d
            assert "开启全位" in d

    def test_set_names_unique(self):
        assert len(SET_NAMES) == len(set(SET_NAMES))


# ============================================================
# 二、查询函数
# ============================================================

class TestGetSetData:
    def test_valid_set(self):
        first_set = SET_NAMES[0]
        data = get_set_data(first_set)
        assert len(data) > 0
        assert all(d["套装"] == first_set for d in data)

    def test_invalid_set(self):
        data = get_set_data("不存在的套装")
        assert data == []


class TestGetMaterials:
    def test_valid_set(self):
        first_set = SET_NAMES[0]
        mats = get_materials(first_set)
        assert len(mats) > 0

    def test_invalid_set(self):
        mats = get_materials("不存在的套装")
        assert mats == []


class TestSetDisplay:
    def test_valid_set(self):
        first_set = SET_NAMES[0]
        display = set_display(first_set)
        assert first_set in display
        assert "Lv." in display
        assert "解" in display

    def test_invalid_set(self):
        display = set_display("不存在的套装")
        assert display == "不存在的套装"


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcByMaterials:
    def test_invalid_set(self):
        result = calc_by_materials("不存在的套装", 0, {})
        assert result["error"] is not None

    def test_max_level(self):
        result = calc_by_materials(SET_NAMES[0], 10, {})
        assert result["error"] is not None  # 已满级

    def test_no_materials(self):
        result = calc_by_materials(SET_NAMES[0], 0, {})
        assert result["error"] is None
        assert result["reachable_lv"] == 0

    def test_sufficient_materials(self):
        """给大量材料应该能升级"""
        first_set = SET_NAMES[0]
        mats_names = get_materials(first_set)
        # 获取所有需要的材料名
        set_data = get_set_data(first_set)
        all_mat_names = set()
        for row in set_data:
            all_mat_names.add(row["开启名"])
            all_mat_names.add(row["刷新主名"])
            all_mat_names.add(row["刷新保名"])
        holdings = {m: 999999 for m in all_mat_names}
        result = calc_by_materials(first_set, 0, holdings)
        assert result["error"] is None
        assert result["reachable_lv"] > 0

    def test_return_structure(self):
        result = calc_by_materials(SET_NAMES[0], 0, {})
        assert "error" in result
        assert "reachable_lv" in result
        assert "table_data" in result


class TestCalcByTarget:
    def test_invalid_set(self):
        result = calc_by_target("不存在的套装", 0, 5)
        assert result["error"] is not None

    def test_target_less_than_start(self):
        result = calc_by_target(SET_NAMES[0], 5, 3)
        assert result["error"] is not None

    def test_basic_calc(self):
        result = calc_by_target(SET_NAMES[0], 0, 3)
        assert result["error"] is None
        assert len(result["table_data"]) == 3

    def test_return_structure(self):
        result = calc_by_target(SET_NAMES[0], 0, 2)
        assert "unlock" in result
        assert "total_open" in result
        assert "total_refresh_m" in result
        assert "total_refresh_b" in result
        assert "table_data" in result

    def test_total_consistency(self):
        """总消耗应等于逐级之和"""
        result = calc_by_target(SET_NAMES[0], 0, 5)
        assert result["error"] is None
        # table_data 的行数应等于目标等级
        assert len(result["table_data"]) == 5
