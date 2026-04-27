"""
test_calc_feng_shui.py - 风水录养成计算引擎 单元测试
覆盖: 数据常量、工具函数(get_map_materials)、
      计算函数(calc_point_cost, eval_single_point)
"""

import pytest

from calculators.calc_feng_shui import (
    FENG_SHUI_POINTS, MAP_POINTS, ALL_MATERIALS,
    get_map_materials,
    calc_point_cost, eval_single_point,
)


# ============================================================
# 一、数据常量
# ============================================================

class TestConstants:
    def test_points_count(self):
        assert len(FENG_SHUI_POINTS) == 24

    def test_points_keys(self):
        for pid in range(1, 25):
            assert pid in FENG_SHUI_POINTS

    def test_point_structure(self):
        for pid, pt in FENG_SHUI_POINTS.items():
            assert "name" in pt
            assert "map" in pt
            assert "main_mat" in pt
            assert "main_per" in pt
            assert "sub_mat" in pt
            assert "progress" in pt
            assert len(pt["progress"]) == 6  # 0-5星的进度值

    def test_map_points(self):
        assert set(MAP_POINTS.keys()) == {"北郡", "琅琊盆地", "昆仑", "轩辕"}
        total = sum(len(v) for v in MAP_POINTS.values())
        assert total == 24

    def test_all_materials(self):
        assert isinstance(ALL_MATERIALS, list)
        assert len(ALL_MATERIALS) > 0
        assert ALL_MATERIALS == sorted(ALL_MATERIALS)  # 已排序

    def test_progress_ascending(self):
        """每个风水点的进度应递增"""
        for pid, pt in FENG_SHUI_POINTS.items():
            prog = pt["progress"]
            for i in range(1, len(prog)):
                assert prog[i] >= prog[i-1], f"风水点 {pid} 进度不递增"


# ============================================================
# 二、工具函数
# ============================================================

class TestGetMapMaterials:
    def test_beiqun(self):
        mats = get_map_materials("北郡")
        assert "神兽石" in mats

    def test_langya(self):
        mats = get_map_materials("琅琊盆地")
        assert "缠山图" in mats
        assert "神兽石·星" in mats

    def test_kunlun(self):
        mats = get_map_materials("昆仑")
        assert "神兽石·月" in mats

    def test_xuanyuan(self):
        mats = get_map_materials("轩辕")
        assert "神兽石·日" in mats

    def test_invalid_map(self):
        mats = get_map_materials("不存在的地图")
        assert mats == []

    def test_sorted_result(self):
        for map_name in MAP_POINTS:
            mats = get_map_materials(map_name)
            assert mats == sorted(mats)


# ============================================================
# 三、计算函数
# ============================================================

class TestCalcPointCost:
    def test_zero_to_one(self):
        """0→1星"""
        result = calc_point_cost(1, 0, 1)
        assert result["main_mat"] == "神兽石"
        assert result["main_cost"] > 0
        assert result["sub_mat"] is None
        assert result["sub_cost"] == 0

    def test_zero_to_five(self):
        """0→5星（全程）"""
        result = calc_point_cost(1, 0, 5)
        assert result["main_cost"] > 0

    def test_same_star(self):
        """同星级无消耗"""
        result = calc_point_cost(1, 3, 3)
        # progress[3] - progress[3] = 0，但可能有 card_extra
        # 对于 pid=1, card_star=1, 如果 start_star < 1 <= target_star 才有 extra
        # 这里 start=3, target=3，不触发
        assert result["main_cost"] == 0

    def test_with_sub_material(self):
        """琅琊盆地风水点有副材料"""
        result = calc_point_cost(7, 0, 1)
        assert result["sub_mat"] == "神兽石·星"
        assert result["sub_cost"] > 0

    def test_card_extra(self):
        """北郡风水点1在跨越card_star=1时有额外消耗"""
        pt = FENG_SHUI_POINTS[1]
        assert pt["card_star"] == 1

        # 从0升到2，跨越了star=1
        result = calc_point_cost(1, 0, 2)
        # 应包含 card_extra
        prog_delta = pt["progress"][2] - pt["progress"][0]
        expected_base = prog_delta * pt["main_per"]
        assert result["main_cost"] == expected_base + pt["card_extra"]


class TestEvalSinglePoint:
    def test_no_materials(self):
        result = eval_single_point(1, 0, {"神兽石": 0})
        assert result["reach_star"] == 0
        assert result["used"] == {}

    def test_abundant_materials(self):
        result = eval_single_point(1, 0, {"神兽石": 999999})
        assert result["reach_star"] == 5  # 最高5星

    def test_partial_materials(self):
        """少量材料应部分升级"""
        result = eval_single_point(1, 0, {"神兽石": 100})
        assert 0 <= result["reach_star"] <= 5

    def test_with_sub_mat(self):
        """琅琊盆地需要双材料"""
        result = eval_single_point(7, 0, {"缠山图": 999999, "神兽石·星": 999999})
        assert result["reach_star"] == 5

    def test_sub_mat_insufficient(self):
        """主材料足够但副材料不足"""
        result = eval_single_point(7, 0, {"缠山图": 999999, "神兽石·星": 0})
        assert result["reach_star"] == 0

    def test_return_structure(self):
        result = eval_single_point(1, 0, {"神兽石": 100})
        assert "reach_star" in result
        assert "used" in result
        assert "original" in result
