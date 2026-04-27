"""
test_calc_fabao.py - 法宝升阶养成计算器 单元测试
覆盖: 数据常量、工具函数、计算函数(calc_by_materials, calc_for_target)
"""

import pytest

from calculators.calc_fabao import (
    SIXIANG_COST, SANCAI_CHIP_COST, SANCAI_MAT2_COST,
    FABAO_LIST, FORMATION_TYPES, FORMATION_COLORS,
    get_cost_tables, has_mat2, get_fabao_display_name, get_fabao_by_formation,
    calc_by_materials, calc_for_target,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_sixiang_cost_length(self):
        assert len(SIXIANG_COST) == 100

    def test_sancai_chip_cost_length(self):
        assert len(SANCAI_CHIP_COST) == 100

    def test_sancai_mat2_cost_length(self):
        assert len(SANCAI_MAT2_COST) == 100

    def test_fabao_list_non_empty(self):
        assert len(FABAO_LIST) > 0

    def test_fabao_tuple_structure(self):
        for f in FABAO_LIST:
            assert len(f) == 5  # (name, grade, formation, chip, mat2)

    def test_formation_types_non_empty(self):
        assert len(FORMATION_TYPES) > 0

    def test_formation_colors_non_empty(self):
        assert len(FORMATION_COLORS) > 0


# ============================================================
# 二、工具函数
# ============================================================

class TestGetCostTables:
    def test_sixiang(self):
        chip, mat2 = get_cost_tables("四象阵")
        assert chip is SIXIANG_COST
        assert all(v == 0 for v in mat2)

    def test_sancai(self):
        chip, mat2 = get_cost_tables("三才阵")
        assert chip is SANCAI_CHIP_COST
        assert mat2 is SANCAI_MAT2_COST


class TestHasMat2:
    def test_sancai_has(self):
        assert has_mat2("三才阵") is True

    def test_guicang_has(self):
        assert has_mat2("归藏阵") is True

    def test_sixiang_no(self):
        assert has_mat2("四象阵") is False


class TestGetFabaoDisplayName:
    def test_basic_name(self):
        """凡品四象阵只显示名字"""
        fabao = ("测试法宝", "凡", "四象阵", "碎片A", "")
        assert get_fabao_display_name(fabao) == "测试法宝"

    def test_non_fan_sixiang(self):
        """非凡品四象阵显示品质"""
        fabao = ("测试法宝", "良", "四象阵", "碎片A", "")
        assert get_fabao_display_name(fabao) == "测试法宝(良)"

    def test_sancai_no_grade(self):
        """三才阵不显示品质"""
        fabao = ("测试法宝", "良", "三才阵", "碎片A", "材料B")
        assert get_fabao_display_name(fabao) == "测试法宝"


class TestGetFabaoByFormation:
    def test_returns_list(self):
        result = get_fabao_by_formation("四象阵")
        assert isinstance(result, list)

    def test_all_same_formation(self):
        for ft in FORMATION_TYPES:
            result = get_fabao_by_formation(ft)
            for f in result:
                assert f[2] == ft


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcByMaterials:
    @pytest.fixture
    def sample_fabao(self):
        """取第一个法宝作为样本"""
        return FABAO_LIST[0]

    def test_invalid_level(self, sample_fabao):
        result = calc_by_materials(sample_fabao, -1, 100)
        assert result["error"] is not None

        result = calc_by_materials(sample_fabao, 100, 100)
        assert result["error"] is not None

    def test_negative_chips(self, sample_fabao):
        result = calc_by_materials(sample_fabao, 0, -1)
        assert result["error"] is not None

    def test_zero_chips(self, sample_fabao):
        result = calc_by_materials(sample_fabao, 0, 0)
        assert result["error"] is None
        assert result["reach_level"] == 0

    def test_large_chips(self, sample_fabao):
        result = calc_by_materials(sample_fabao, 0, 999999)
        assert result["error"] is None
        assert result["reach_level"] > 0

    def test_return_structure(self, sample_fabao):
        result = calc_by_materials(sample_fabao, 0, 100)
        assert "error" in result
        assert "reach_level" in result
        assert "remaining_chips" in result
        assert "table_data" in result


class TestCalcForTarget:
    @pytest.fixture
    def sample_fabao(self):
        return FABAO_LIST[0]

    def test_invalid_levels(self, sample_fabao):
        assert calc_for_target(sample_fabao, -1, 10)["error"] is not None
        assert calc_for_target(sample_fabao, 0, 0)["error"] is not None
        assert calc_for_target(sample_fabao, 0, 101)["error"] is not None

    def test_target_less_than_current(self, sample_fabao):
        result = calc_for_target(sample_fabao, 10, 5)
        assert result["error"] is not None

    def test_basic_calc(self, sample_fabao):
        result = calc_for_target(sample_fabao, 0, 10)
        assert result["error"] is None
        assert result["total_chips"] > 0
        assert len(result["table_data"]) == 10

    def test_segments(self, sample_fabao):
        result = calc_for_target(sample_fabao, 0, 15)
        assert result["error"] is None
        assert len(result["segments"]) > 0

    def test_return_structure(self, sample_fabao):
        result = calc_for_target(sample_fabao, 0, 5)
        assert "total_chips" in result
        assert "total_mat2" in result
        assert "table_data" in result
        assert "segments" in result
