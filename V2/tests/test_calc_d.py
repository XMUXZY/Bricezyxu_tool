"""
test_calc_d.py - 星录养成计算引擎 单元测试
覆盖: 配置常量、工具函数(get_mat_tier, get_mat_name, get_guard_exp, get_forge_exp_mat)、
      计算函数(calc_by_materials, calc_for_target)
"""

import pytest

from calculators.calc_d import (
    XINLU_CONFIG, XINLU_NAMES, FORGE_DATA, QIMING_GUARD_OVERRIDE,
    get_mat_tier, get_mat_name, get_guard_exp, get_forge_exp_mat,
    calc_by_materials, calc_for_target,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_xinlu_names(self):
        assert XINLU_NAMES == ["太微", "紫微", "天市", "启明"]

    def test_xinlu_config_keys(self):
        for name in XINLU_NAMES:
            cfg = XINLU_CONFIG[name]
            assert "max_chong" in cfg
            assert "low_mat" in cfg
            assert "mid_mat" in cfg
            assert "high_mat" in cfg
            assert "guard" in cfg

    def test_max_chong_values(self):
        assert XINLU_CONFIG["太微"]["max_chong"] == 20
        assert XINLU_CONFIG["天市"]["max_chong"] == 22

    def test_forge_data_non_empty(self):
        assert len(FORGE_DATA) > 0

    def test_forge_data_keys(self):
        for key, val in FORGE_DATA.items():
            assert isinstance(key, tuple) and len(key) == 2
            assert "exp_mat" in val
            assert "exp_guard" in val

    def test_qiming_guard_override(self):
        """启明 17-20 重有保级消耗特殊值"""
        assert (17, 1) in QIMING_GUARD_OVERRIDE
        assert (20, 6) in QIMING_GUARD_OVERRIDE


# ============================================================
# 二、工具函数
# ============================================================

class TestGetMatTier:
    def test_low_tier(self):
        for chong in range(1, 11):
            assert get_mat_tier(chong) == "low"

    def test_mid_tier(self):
        for chong in range(11, 16):
            assert get_mat_tier(chong) == "mid"

    def test_high_tier(self):
        for chong in range(16, 23):
            assert get_mat_tier(chong) == "high"


class TestGetMatName:
    def test_taiwei_materials(self):
        assert get_mat_name("太微", "low") == "南明离火"
        assert get_mat_name("太微", "mid") == "九幽玄火"
        assert get_mat_name("太微", "high") == "红莲业火"

    def test_all_xinlu(self):
        for name in XINLU_NAMES:
            for tier in ("low", "mid", "high"):
                result = get_mat_name(name, tier)
                assert isinstance(result, str) and len(result) > 0


class TestGetForgeExpMat:
    def test_valid_key(self):
        result = get_forge_exp_mat(1, 1)
        assert result > 0

    def test_invalid_key(self):
        result = get_forge_exp_mat(999, 1)
        assert result == 0


class TestGetGuardExp:
    def test_normal(self):
        result = get_guard_exp("太微", 1, 1)
        assert result >= 0

    def test_qiming_special(self):
        """启明 17-20 重保级消耗有特殊值"""
        result = get_guard_exp("启明", 17, 1)
        assert result > 0

    def test_non_qiming_no_override(self):
        """非启明不受 override 影响"""
        normal = get_guard_exp("太微", 17, 1)
        assert isinstance(normal, (int, float))


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcByMaterials:
    def test_zero_materials(self):
        result = calc_by_materials("太微", 1, 0, 0, 0, 0, 0)
        assert result["chong"] == 1
        assert result["star"] == 0
        assert all(v == 0 for v in result["used"].values())

    def test_infinite_materials(self):
        result = calc_by_materials("太微", 1, 0,
                                   float("inf"), float("inf"), float("inf"), float("inf"))
        assert result["chong"] == 20  # 太微最高 20 重
        assert result["star"] == 6

    def test_return_structure(self):
        result = calc_by_materials("太微", 1, 0, 100, 100, 100, 100)
        assert "chong" in result
        assert "star" in result
        assert "used" in result
        assert set(result["used"].keys()) == {"low", "mid", "high", "guard"}

    def test_tianshi_max(self):
        """天市最高22重"""
        result = calc_by_materials("天市", 1, 0,
                                   float("inf"), float("inf"), float("inf"), float("inf"))
        assert result["chong"] == 22
        assert result["star"] == 6


class TestCalcForTarget:
    def test_basic(self):
        result = calc_for_target("太微", 1, 0, 2, 0)
        assert result["error"] is None
        assert result["used"]["low"] > 0 or result["used"]["guard"] > 0

    def test_same_target(self):
        """起始和目标相同应该没有消耗"""
        result = calc_for_target("太微", 1, 0, 1, 0)
        assert result["error"] is None
        assert all(v == 0 for v in result["used"].values())

    def test_exceed_max_non_tianshi(self):
        """非天市不能超过20重"""
        result = calc_for_target("太微", 1, 0, 21, 0)
        assert result["error"] is not None

    def test_return_structure(self):
        result = calc_for_target("太微", 1, 0, 5, 6)
        assert "used" in result
        assert "error" in result
