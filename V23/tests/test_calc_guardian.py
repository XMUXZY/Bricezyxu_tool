"""
test_calc_guardian.py - 守护神养成计算器 v4 单元测试
覆盖: 数据常量、期望残念计算、分布展开、核心计算逻辑
"""

import math
import pytest

from calculators.calc_guardian import (
    STAR_CUM, GROUPS, QUALITY_COLORS, EXP_MAP, REMNANT_PER_DRAW,
    get_group_names, find_group, get_group_guardians, get_guardian_info,
    get_exp_per_ticket,
    expand_distribution, expand_distribution_typical,
    calc_remnant_gap, gap_to_tickets,
    calc_simple, calc_precise,
)


# ============================================================
# 一、数据常量
# ============================================================
class TestConstants:
    def test_star_cum(self):
        assert STAR_CUM == {0: 0, 1: 20, 2: 40, 3: 80, 4: 160, 5: 320}

    def test_groups_count(self):
        assert len(GROUPS) == 6

    def test_group_names(self):
        names = get_group_names()
        assert "四值功曹" in names
        assert "日直六星" in names
        assert "九歌地神" in names
        assert "云海天神" in names
        assert "五德真君" in names
        assert "天元九歌" in names

    def test_group_guardian_counts(self):
        expected = {"四值功曹": 4, "日直六星": 6, "九歌地神": 4,
                    "云海天神": 4, "五德真君": 5, "天元九歌": 4}
        for name, count in expected.items():
            assert len(get_group_guardians(name)) == count

    def test_quality_colors(self):
        for q in ["蓝(2)", "蓝绿(3)", "紫(4)", "金(5)"]:
            assert q in QUALITY_COLORS

    def test_remnant_per_draw(self):
        assert REMNANT_PER_DRAW == 10


# ============================================================
# 二、期望残念计算（v4核心）
# ============================================================
class TestExpMap:
    """验证期望残念速查表与文档3.2节一致"""

    def test_exp_map_structure(self):
        """每组每个守护神都有期望残念"""
        for g in GROUPS:
            gname = g["name"]
            assert gname in EXP_MAP
            for guardian in g["guardians"]:
                assert guardian["name"] in EXP_MAP[gname]
                assert EXP_MAP[gname][guardian["name"]] > 0

    # 按文档3.2节速查表验证（精度到4位小数）
    def test_sizhi_gonacao(self):
        m = EXP_MAP["四值功曹"]
        assert round(m["值时功曹"], 4) == 4.9180
        assert round(m["值日功曹"], 4) == 2.4590
        assert round(m["值月功曹"], 4) == 2.4590
        assert round(m["值年功曹"], 4) == 0.4176

    def test_rizhi_liuxing(self):
        m = EXP_MAP["日直六星"]
        assert round(m["显道神"], 4) == 3.2258
        assert round(m["开路神"], 4) == 3.2258
        assert round(m["增福神"], 4) == 1.6129
        assert round(m["损福神"], 4) == 1.6129
        assert round(m["日游神"], 4) == 0.2446
        assert round(m["夜游神"], 4) == 0.2446

    def test_jiuge_dishen(self):
        m = EXP_MAP["九歌地神"]
        assert round(m["河伯"], 4) == 6.5934
        assert round(m["山鬼"], 4) == 3.2967
        assert round(m["湘夫人"], 4) == 0.1383
        assert round(m["湘君"], 4) == 0.1383

    def test_yunhai_tianshen(self):
        m = EXP_MAP["云海天神"]
        assert round(m["地安神"], 4) == 6.6593
        assert round(m["天时神"], 4) == 3.3296
        assert round(m["阴光神"], 4) == 0.0770
        assert round(m["阳炁神"], 4) == 0.0770

    def test_wude_zhenjun(self):
        m = EXP_MAP["五德真君"]
        assert round(m["地侯星君"], 4) == 5.6484
        assert round(m["重华星君"], 4) == 2.8242
        assert round(m["伺辰星君"], 4) == 1.4121
        assert round(m["荧惑星君"], 4) == 0.2309
        assert round(m["太白星君"], 4) == 0.0094

    def test_tianyuan_jiuge(self):
        m = EXP_MAP["天元九歌"]
        assert round(m["大司命"], 4) == 6.6007
        assert round(m["云中君"], 4) == 3.3003
        assert round(m["东君"], 4) == 0.0995
        assert round(m["少司命"], 4) == 0.0995


# ============================================================
# 三、工具函数
# ============================================================
class TestToolFunctions:
    def test_find_group_valid(self):
        g = find_group("四值功曹")
        assert g is not None
        assert g["name"] == "四值功曹"

    def test_find_group_invalid(self):
        assert find_group("不存在的组") is None

    def test_get_group_guardians_valid(self):
        result = get_group_guardians("四值功曹")
        assert len(result) == 4

    def test_get_group_guardians_invalid(self):
        assert get_group_guardians("不存在的组") == []

    def test_get_guardian_info_valid(self):
        g = get_guardian_info("四值功曹", "值时功曹")
        assert g is not None
        assert g["name"] == "值时功曹"

    def test_get_guardian_info_invalid(self):
        assert get_guardian_info("四值功曹", "不存在") is None

    def test_get_exp_per_ticket(self):
        exp = get_exp_per_ticket("四值功曹", "值时功曹")
        assert round(exp, 4) == 4.9180


# ============================================================
# 四、分布展开算法
# ============================================================
class TestExpandDistribution:
    def test_optimistic_4(self):
        result = expand_distribution(2.0, 4, 'optimistic')
        assert sum(result) == 8
        assert all(0 <= x <= 5 for x in result)
        assert result[0] >= result[-1]  # 降序

    def test_pessimistic_4(self):
        result = expand_distribution(2.0, 4, 'pessimistic')
        assert sum(result) == 8
        assert all(0 <= x <= 5 for x in result)
        assert result[0] <= result[-1]  # 升序

    def test_optimistic_6(self):
        result = expand_distribution(3.5, 6, 'optimistic')
        assert sum(result) == 21
        assert all(0 <= x <= 5 for x in result)

    def test_pessimistic_6(self):
        result = expand_distribution(3.5, 6, 'pessimistic')
        assert sum(result) == 21
        assert all(0 <= x <= 5 for x in result)

    def test_boundary_zero(self):
        result = expand_distribution(0.0, 4, 'optimistic')
        assert result == [0, 0, 0, 0]

    def test_boundary_max(self):
        result = expand_distribution(5.0, 4, 'optimistic')
        assert result == [5, 5, 5, 5]

    def test_3_5_example(self):
        """4人组平均3.5星（总14）乐观分布应为集中分配"""
        result = expand_distribution(3.5, 4, 'optimistic')
        assert sum(result) == 14
        # 贪心算法结果：[5,5,4,0]（从高到低填满）
        assert result == [5, 5, 4, 0]

    def test_distributions_differ(self):
        """乐观和悲观分布应该不同（除非平均值为0或5）"""
        opt = expand_distribution(2.5, 4, 'optimistic')
        pes = expand_distribution(2.5, 4, 'pessimistic')
        assert opt != pes


class TestExpandDistributionTypical:
    """测试最常见分布展开算法"""

    def test_basic_sum(self):
        """总星级应等于 round(avg * n)"""
        result = expand_distribution_typical(2.5, "四值功曹")
        assert sum(result) == round(2.5 * 4)

    def test_range(self):
        """每个星级都在 [0,5] 范围内"""
        result = expand_distribution_typical(3.0, "日直六星")
        assert all(0 <= x <= 5 for x in result)

    def test_length(self):
        """返回长度等于组内守护神数量"""
        result = expand_distribution_typical(2.0, "五德真君")
        assert len(result) == 5

    def test_low_quality_higher_star(self):
        """低品质（高期望）守护神应分配到更高星级"""
        result = expand_distribution_typical(2.5, "四值功曹")
        # 四值功曹顺序：值时功曹(4.918) > 值日功曹(2.459) > 值月功曹(2.459) > 值年功曹(0.418)
        # 期望高的分到更高星级
        assert result[0] >= result[-1], "高期望守护神应分到更高星级"

    def test_all_zero(self):
        """平均0星时全部为0"""
        result = expand_distribution_typical(0.0, "四值功曹")
        assert result == [0, 0, 0, 0]

    def test_all_max(self):
        """平均5星时全部为5"""
        result = expand_distribution_typical(5.0, "四值功曹")
        assert result == [5, 5, 5, 5]

    def test_invalid_group(self):
        """无效组名返回空列表"""
        result = expand_distribution_typical(3.0, "不存在的组")
        assert result == []

    def test_typical_between_extremes(self):
        """最常见分布应介于乐观和悲观之间（或等于某一端）"""
        n = 4
        typ = expand_distribution_typical(2.5, "四值功曹")
        opt = sorted(expand_distribution(2.5, n, 'optimistic'))
        pes = sorted(expand_distribution(2.5, n, 'pessimistic'))
        typ_sorted = sorted(typ)
        assert sum(typ) == sum(opt) == sum(pes)


# ============================================================
# 五、残念缺口与请神符
# ============================================================
class TestCalcRemnantGap:
    def test_0_to_5(self):
        assert calc_remnant_gap(0, 5) == 320

    def test_3_to_5(self):
        assert calc_remnant_gap(3, 5) == 240

    def test_4_to_5(self):
        assert calc_remnant_gap(4, 5) == 160

    def test_with_held(self):
        assert calc_remnant_gap(0, 5, 50) == 270

    def test_held_enough(self):
        assert calc_remnant_gap(0, 5, 320) == 0

    def test_same_star(self):
        assert calc_remnant_gap(3, 3) == 0


class TestGapToTickets:
    def test_zero(self):
        assert gap_to_tickets(0) == 0

    def test_exact(self):
        assert gap_to_tickets(10, 10.0) == 1

    def test_round_up(self):
        assert gap_to_tickets(15, 10.0) == 2

    def test_real_exp(self):
        """用真实期望值：值时功曹 0→5星 = ceil(320/4.91803...) = 66张"""
        exp = EXP_MAP["四值功曹"]["值时功曹"]
        assert gap_to_tickets(320, exp) == 66

    def test_real_exp_zhinian(self):
        """值年功曹 0→5星 = 320/0.4176 = 767张"""
        exp = EXP_MAP["四值功曹"]["值年功曹"]
        assert gap_to_tickets(320, exp) == 767


# ============================================================
# 六、简单模式 (calc_simple)
# ============================================================
class TestCalcSimple:
    def test_valid(self):
        result = calc_simple("四值功曹", 0.0, 5.0)
        assert result["error"] is None
        assert isinstance(result["ticket_range"], list)
        assert len(result["ticket_range"]) == 2
        assert "plan_typical" in result

    def test_no_plan_max(self):
        """calc_simple 不再返回 plan_max"""
        result = calc_simple("四值功曹", 0.0, 5.0)
        assert "plan_max" not in result

    def test_all_max(self):
        """0→5满星：所有方案一样（都是全部升到5星）"""
        result = calc_simple("四值功曹", 0.0, 5.0)
        assert result["error"] is None
        mn, mx = result["ticket_range"]
        # 满星时最少=最多（都是每人0→5）
        assert mn == mx
        # 最常见也一样
        assert result["plan_typical"]["total_tickets"] == mn

    def test_target_less_than_current(self):
        result = calc_simple("四值功曹", 3.0, 2.0)
        assert result["error"] is not None

    def test_cur_out_of_range(self):
        result = calc_simple("四值功曹", -1.0, 3.0)
        assert result["error"] is not None

    def test_tgt_out_of_range(self):
        result = calc_simple("四值功曹", 3.0, 6.0)
        assert result["error"] is not None

    def test_ticket_range_valid(self):
        result = calc_simple("日直六星", 2.0, 4.0)
        assert result["error"] is None
        mn, mx = result["ticket_range"]
        assert 0 <= mn <= mx

    def test_day6(self):
        result = calc_simple("日直六星", 2.0, 4.0)
        assert result["error"] is None
        assert "plan_min" in result
        assert "plan_typical" in result

    def test_with_essence(self):
        result = calc_simple("日直六星", 0.0, 5.0, held_essence=1000)
        assert result["error"] is None

    def test_same_star_zero(self):
        result = calc_simple("四值功曹", 3.0, 3.0)
        assert result["error"] is None
        assert result["ticket_range"] == [0, 0]
        assert result["plan_typical"]["total_tickets"] == 0

    def test_typical_has_reasonable_value(self):
        """最常见方案消耗应为正数且合理"""
        result = calc_simple("四值功曹", 2.7, 5.0)
        assert result["error"] is None
        t_typ = result["plan_typical"]["total_tickets"]
        assert t_typ > 0

    def test_typical_all_groups(self):
        """所有组的最常见方案都应能正确计算"""
        for gname in get_group_names():
            result = calc_simple(gname, 2.0, 5.0)
            assert result["error"] is None
            pt = result["plan_typical"]
            assert pt["total_tickets"] > 0
            assert len(pt["details"]) == len(get_group_guardians(gname))

    def test_typical_distribution_weighted(self):
        """最常见方案中高期望守护神应分到更高星级"""
        result = calc_simple("九歌地神", 2.0, 5.0)
        assert result["error"] is None
        pt = result["plan_typical"]
        cur_dist = pt["cur_distribution"]
        assert cur_dist[0] >= cur_dist[-1]

    def test_min_typical_differ(self):
        """回归测试：非极端输入下消耗最少和最常见方案应不同"""
        result = calc_simple("四值功曹", 2.7, 5.0)
        assert result["error"] is None
        mn, mx = result["ticket_range"]
        assert mn <= mx

    def test_min_max_differ_jiuge(self):
        """回归测试：九歌地神分配应合理——最少方案让河伯/山鬼补缺口"""
        result = calc_simple("九歌地神", 3.0, 5.0)
        assert result["error"] is None
        mn, mx = result["ticket_range"]
        assert mn <= mx
        # 最少方案：高星分配给湘夫人/湘君（低期望），缺口由河伯/山鬼补
        pm = result["plan_min"]
        for d in pm["details"]:
            if d["name"] in ("湘夫人", "湘君"):
                assert d["tickets"] == 0, f"最少方案中{d['name']}应已达目标"

    def test_min_distribution_assignment(self):
        """验证消耗最少时高星分给低期望守护神"""
        result = calc_simple("九歌地神", 2.0, 5.0)
        assert result["error"] is None
        pm = result["plan_min"]
        # 最少方案：当前星级升序排列（高星分配给后面的低期望守护神）
        min_cur = pm["cur_distribution"]
        assert min_cur[0] <= min_cur[-1], "最少方案：低期望守护神应分到更高星级"

    def test_total_tickets_is_max_not_sum(self):
        """验证 total_tickets 是 max 而非 sum"""
        result = calc_simple("四值功曹", 0.0, 5.0)
        assert result["error"] is None
        plan = result["plan_typical"]
        max_t = max(d["tickets"] for d in plan["details"])
        assert plan["total_tickets"] == max_t


# ============================================================
# 七、精确模式 (calc_precise)
# ============================================================
class TestCalcPrecise:
    def test_valid(self):
        cur = [3, 3, 2, 2, 1, 1]
        tgt = [5, 5, 4, 4, 3, 3]
        result = calc_precise("日直六星", cur, tgt)
        assert result["error"] is None
        assert result["total_tickets"] > 0
        assert len(result["details"]) == 6

    def test_total_tickets_is_max(self):
        """total_tickets 应等于各守护神 tickets 的最大值（并行模型）"""
        cur = [3, 3, 2, 2, 1, 1]
        tgt = [5, 5, 4, 4, 3, 3]
        result = calc_precise("日直六星", cur, tgt)
        max_tickets = max(d["tickets"] for d in result["details"])
        assert max_tickets == result["total_tickets"]

    def test_target_less_than_current(self):
        cur = [3, 3, 2, 2, 1, 1]
        tgt = [2, 5, 4, 4, 3, 3]
        result = calc_precise("日直六星", cur, tgt)
        assert result["error"] is not None

    def test_already_maxed(self):
        cur = [5, 5, 5, 5, 5, 5]
        tgt = [5, 5, 5, 5, 5, 5]
        result = calc_precise("日直六星", cur, tgt)
        assert result["error"] is None
        assert result["total_tickets"] == 0

    def test_with_essence(self):
        cur = [0, 0, 0, 0, 0, 0]
        tgt = [5, 5, 5, 5, 5, 5]
        result = calc_precise("日直六星", cur, tgt, held_essence=5000)
        assert result["error"] is None

    def test_wrong_count(self):
        result = calc_precise("四值功曹", [0, 0], [5, 5])
        assert result["error"] is not None


# ============================================================
# 八、对照 Excel 预计算验证
# ============================================================
class TestExcelVerification:
    """对照 Excel Sheet04 的预计算示例验证（total_tickets 为并行模型取 max）"""

    def test_sizhi_0to5_all(self):
        """四值功曹 0→满星：各守护神独立需求不变，总消耗取 max = 767"""
        cur = [0, 0, 0, 0]
        tgt = [5, 5, 5, 5]
        result = calc_precise("四值功曹", cur, tgt)
        assert result["error"] is None
        details = result["details"]
        expected = {"值时功曹": 66, "值日功曹": 131, "值月功曹": 131, "值年功曹": 767}
        for d in details:
            assert d["tickets"] == expected[d["name"]], \
                f"{d['name']}: got {d['tickets']}, expected {expected[d['name']]}"
        assert result["total_tickets"] == 767

    def test_rizhi_0to5_all(self):
        """日直六星 0→满星：总消耗取 max = 1309"""
        cur = [0, 0, 0, 0, 0, 0]
        tgt = [5, 5, 5, 5, 5, 5]
        result = calc_precise("日直六星", cur, tgt)
        assert result["error"] is None
        expected = {"显道神": 100, "开路神": 100, "增福神": 199,
                    "损福神": 199, "日游神": 1309, "夜游神": 1309}
        for d in result["details"]:
            assert d["tickets"] == expected[d["name"]]
        assert result["total_tickets"] == 1309

    def test_jiuge_0to5_all(self):
        """九歌地神 0→满星：总消耗取 max = 2315"""
        cur = [0, 0, 0, 0]
        tgt = [5, 5, 5, 5]
        result = calc_precise("九歌地神", cur, tgt)
        assert result["error"] is None
        expected = {"河伯": 49, "山鬼": 98, "湘夫人": 2315, "湘君": 2315}
        for d in result["details"]:
            assert d["tickets"] == expected[d["name"]]
        assert result["total_tickets"] == 2315

    def test_yunhai_0to5_all(self):
        """云海天神 0→满星：总消耗取 max = 4158"""
        cur = [0, 0, 0, 0]
        tgt = [5, 5, 5, 5]
        result = calc_precise("云海天神", cur, tgt)
        assert result["error"] is None
        expected = {"地安神": 49, "天时神": 97, "阴光神": 4158, "阳炁神": 4158}
        for d in result["details"]:
            assert d["tickets"] == expected[d["name"]]
        assert result["total_tickets"] == 4158

    def test_wude_0to5_all(self):
        """五德真君 0→满星：总消耗取 max = 33992"""
        cur = [0, 0, 0, 0, 0]
        tgt = [5, 5, 5, 5, 5]
        result = calc_precise("五德真君", cur, tgt)
        assert result["error"] is None
        expected = {"地侯星君": 57, "重华星君": 114, "伺辰星君": 227,
                    "荧惑星君": 1386, "太白星君": 33992}
        for d in result["details"]:
            assert d["tickets"] == expected[d["name"]]
        assert result["total_tickets"] == 33992

    def test_tianyuan_0to5_all(self):
        """天元九歌 0→满星：总消耗取 max = 3216"""
        cur = [0, 0, 0, 0]
        tgt = [5, 5, 5, 5]
        result = calc_precise("天元九歌", cur, tgt)
        assert result["error"] is None
        expected = {"大司命": 49, "云中君": 97, "东君": 3216, "少司命": 3216}
        for d in result["details"]:
            assert d["tickets"] == expected[d["name"]]
        assert result["total_tickets"] == 3216
