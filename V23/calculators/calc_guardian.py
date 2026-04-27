"""
守护神养成计算器 v4 — 纯计算模块
基于配置表真实出货概率 + 幸运值保底 + 次数保底（四值功曹）

支持两种模式：
  简单模式：输入平均星级 → 消耗最少 / 最常见方案
  精确模式：输入各守护神星级 → 精确结果

总消耗采用"并行模型"：一张符同时为所有守护神积累残念，
因此总消耗 = max(各守护神独立需求)，而非 sum。

所有数据来源于 game_data/guardian_data.json
"""

import math
from utils.data_loader import load_game_data


# ============================================================
# 一、数据加载
# ============================================================

_DATA = load_game_data("guardian_data.json")

# 升星累计残念表  {0:0, 1:20, 2:60, 3:140, 4:300, 5:300}
STAR_CUM = {int(k): v for k, v in _DATA["guardian_config"]["star_cum"].items()}

# 品质颜色映射
QUALITY_COLORS = _DATA["guardian_config"]["quality_colors"]

# 每次抽卡获得残念数
REMNANT_PER_DRAW = _DATA["guardian_config"]["remnant_per_draw"]

# 神仙谱组数据: list of dict
GROUPS = _DATA["groups"]

del _DATA


# ============================================================
# 二、期望残念计算（核心公式）
# ============================================================

def _calc_exp_remnant_map():
    """
    根据 v4 公式计算每个守护神每张符的期望残念。

    每张符期望残念[X] = 普通出货期望 + 幸运值保底贡献 + 次数保底贡献

    普通出货期望 = (权重 / 总权重) × 10
    幸运值保底贡献 = (1/保底神数量) × 10 / 保底触发次数  (仅保底守护神)
    次数保底贡献 = 10 / 115  (仅四值功曹-值年功曹)

    返回：{组名: {守护神名: 期望残念/张符}}
    """
    result = {}
    for group in GROUPS:
        gname = group["name"]
        guardians = group["guardians"]
        total_weight = sum(g["weight"] for g in guardians)

        pity_trigger = group["pity_trigger"]       # 幸运值保底触发次数
        pity_guardians = group.get("pity_guardians", [])  # 保底守护神列表
        pity_count = len(pity_guardians)

        count_pity = group.get("count_pity")        # 次数保底（仅四值功曹=115）
        count_pity_target = group.get("count_pity_target")  # 次数保底目标

        group_map = {}
        for g in guardians:
            name = g["name"]
            weight = g["weight"]

            # 普通出货期望
            normal_exp = (weight / total_weight) * REMNANT_PER_DRAW

            # 幸运值保底贡献
            pity_exp = 0.0
            if name in pity_guardians and pity_count > 0:
                pity_exp = (1 / pity_count) * REMNANT_PER_DRAW / pity_trigger

            # 次数保底贡献
            count_exp = 0.0
            if count_pity and count_pity_target == name:
                count_exp = REMNANT_PER_DRAW / count_pity

            group_map[name] = normal_exp + pity_exp + count_exp

        result[gname] = group_map
    return result


# 期望残念速查表：{组名: {守护神名: 期望残念/张符}}
EXP_MAP = _calc_exp_remnant_map()


# ============================================================
# 三、工具函数
# ============================================================

def get_group_names() -> list[str]:
    """获取所有组名列表"""
    return [g["name"] for g in GROUPS]


def find_group(group_name: str) -> dict | None:
    """按名称查找组，返回组字典或 None"""
    for g in GROUPS:
        if g["name"] == group_name:
            return g
    return None


def get_group_guardians(group_name: str) -> list[dict]:
    """获取指定组的守护神列表"""
    g = find_group(group_name)
    return g["guardians"] if g else []


def get_group_ticket(group_name: str) -> str:
    """获取指定组对应的请神符名称，如'功曹请神符'"""
    g = find_group(group_name)
    return g["ticket"] if g else "请神符"


def get_guardian_info(group_name: str, guardian_name: str) -> dict | None:
    """获取指定守护神信息"""
    for g in get_group_guardians(group_name):
        if g["name"] == guardian_name:
            return g
    return None


def get_exp_per_ticket(group_name: str, guardian_name: str) -> float:
    """获取指定守护神每张符的期望残念"""
    return EXP_MAP.get(group_name, {}).get(guardian_name, 0.0)


# ============================================================
# 四、基础计算函数
# ============================================================

def calc_remnant_gap(cur_star: int, tgt_star: int, held_remnant: int = 0) -> int:
    """
    计算单个守护神的残念缺口

    Args:
        cur_star: 当前星级 (0~5)
        tgt_star: 目标星级 (0~5)
        held_remnant: 已持有的残念数

    Returns:
        残念缺口（≥0）
    """
    need = STAR_CUM[tgt_star] - STAR_CUM[cur_star]
    return max(0, need - held_remnant)


def gap_to_tickets(nian_gap: int, exp_per_fu: float = 10.0) -> int:
    """
    残念缺口转换为请神符数量（v4修正：基于真实期望残念）

    Args:
        nian_gap: 残念缺口
        exp_per_fu: 每张符期望残念

    Returns:
        所需请神符数量（向上取整）
    """
    if nian_gap <= 0:
        return 0
    return math.ceil(nian_gap / exp_per_fu)


# ============================================================
# 五、分布展开算法（简单模式用）
# ============================================================

def expand_distribution(avg_star: float, n: int, mode: str) -> list[int]:
    """
    将平均星级展开为具体分布

    Args:
        avg_star: 平均星级（允许小数）
        n: 守护神数量
        mode: 'optimistic'（最乐观/集中）或 'pessimistic'（最悲观/分散）

    Returns:
        长度为n的星级列表，总和=round(avg_star*n)，每个值在[0,5]

    最乐观分布（消耗最少时的当前分布）：
        从高到低填满，尽量集中在少数守护神
        例：4人组平均2.0星 → [5,3,0,0]

    最悲观分布（消耗最多时的当前分布）：
        从低到高填满，低星多高星少
        例：4人组平均2.0星 → [0,0,3,5]
    """
    total = round(avg_star * n)
    total = max(0, min(5 * n, total))
    stars = [0] * n

    if mode == 'optimistic':
        # 从高往低分配，先尽量填5星
        remaining = total
        for i in range(n):
            give = min(5, remaining)
            stars[i] = give
            remaining -= give
        stars.sort(reverse=True)

    elif mode == 'pessimistic':
        # 从低往高分配
        remaining = total
        for i in range(n - 1, -1, -1):
            give = min(5, remaining)
            stars[i] = give
            remaining -= give
        stars.sort()

    return stars


def expand_distribution_typical(avg_star: float, group_name: str) -> list[int]:
    """
    最常见分布：按各守护神期望残念速率比例加权分配总星级。

    低品质神出货概率高 → 残念积累快 → 分配更高星级
    高品质神出货概率低 → 残念积累慢 → 分配更低星级

    Args:
        avg_star: 平均星级
        group_name: 神仙谱组名称

    Returns:
        长度为n的星级列表，总和=round(avg_star*n)，每个值在[0,5]
    """
    group = find_group(group_name)
    if not group:
        return []

    guardians = group["guardians"]
    n = len(guardians)
    group_exp = EXP_MAP.get(group_name, {})

    total_star = round(avg_star * n)
    total_star = max(0, min(5 * n, total_star))

    # 边界快速返回
    if total_star == 0:
        return [0] * n
    if total_star == 5 * n:
        return [5] * n

    total_exp = sum(group_exp.get(g["name"], 0) for g in guardians)
    if total_exp <= 0:
        # 兜底：均匀分配
        base = total_star // n
        return [min(5, base)] * n

    # 按期望残念比例分配星级
    raw = [total_star * group_exp.get(g["name"], 0) / total_exp for g in guardians]
    stars = [min(5, max(0, round(v))) for v in raw]

    # 修正总和误差（四舍五入可能导致总和偏差）
    diff = total_star - sum(stars)
    residuals = [(raw[i] - round(raw[i]), i) for i in range(n)]

    if diff > 0:
        # 残差最大的先+1
        residuals.sort(reverse=True)
        for _, i in residuals[:diff]:
            stars[i] = min(5, stars[i] + 1)
    elif diff < 0:
        # 残差最小的先-1
        residuals.sort()
        for _, i in residuals[:-diff]:
            stars[i] = max(0, stars[i] - 1)

    return stars


# ============================================================
# 六、组内精华流转计算
# ============================================================

def _calc_essence_flow(group_name: str, details: list[dict],
                       held_essence: int = 0) -> dict:
    """
    计算组内精华流转

    Args:
        group_name: 组名
        details: 各守护神详情列表（含 cur_star, tgt_star, gap 等）
        held_essence: 持有精华数量

    Returns:
        更新后的详情和精华流转说明
    """
    guardians = get_group_guardians(group_name)
    if not guardians:
        return {"details": details, "essence_flow": {}}

    # 计算精华贡献（满5星后多余残念转精华）
    total_essence = held_essence
    contributors = []

    for i, d in enumerate(details):
        if d["tgt_star"] == 5 and d.get("held_remnant", 0) > 0:
            needed = STAR_CUM[d["tgt_star"]] - STAR_CUM[d["cur_star"]]
            surplus = max(0, d["held_remnant"] - max(0, needed))
            if surplus > 0:
                price = guardians[i]["price"]
                contrib = surplus * price
                total_essence += contrib
                contributors.append({
                    "name": d["name"],
                    "surplus_remnant": surplus,
                    "price": price,
                    "essence": contrib,
                })

    if total_essence <= 0:
        return {"details": details, "essence_flow": {
            "total_essence": held_essence,
            "contributors": [],
            "beneficiaries": [],
        }}

    # 精华优先补贴精华单价最高的守护神
    beneficiaries = []
    remaining_essence = total_essence

    # 按精华单价从高到低排序
    indexed = [(i, guardians[i]["price"]) for i in range(len(details))
               if details[i]["gap"] > 0]
    indexed.sort(key=lambda x: -x[1])

    for idx, price in indexed:
        if remaining_essence <= 0:
            break
        d = details[idx]
        gap = d["gap"]
        if gap <= 0:
            continue

        # 可购买残念数
        buyable = remaining_essence // price
        actual_buy = min(buyable, gap)
        if actual_buy > 0:
            cost = actual_buy * price
            remaining_essence -= cost
            d["gap"] -= actual_buy
            d["essence_subsidy"] = actual_buy
            beneficiaries.append({
                "name": d["name"],
                "bought_remnant": actual_buy,
                "cost_essence": cost,
                "price": price,
            })

    return {
        "details": details,
        "essence_flow": {
            "total_essence": total_essence,
            "held_essence": held_essence,
            "contributors": contributors,
            "beneficiaries": beneficiaries,
            "remaining_essence": remaining_essence,
        },
    }


# ============================================================
# 七、计算一组守护神（核心）
# ============================================================

def _calc_group_plan(group_name: str, cur_stars: list[int], tgt_stars: list[int],
                     held_remnants: list[int] | None = None,
                     held_essence: int = 0) -> dict:
    """
    计算一组守护神的请神符消耗

    Args:
        group_name: 组名
        cur_stars: 当前各守护神星级列表
        tgt_stars: 目标各守护神星级列表
        held_remnants: 已持有各守护神残念列表（可选）
        held_essence: 持有精华数量

    Returns:
        {
            "error": None,
            "details": [{name, quality, exp_per_ticket, cur_star, tgt_star,
                         need, held_remnant, gap, essence_subsidy, tickets}],
            "total_tickets": int,
            "essence_flow": dict,
        }
    """
    guardians = get_group_guardians(group_name)
    n = len(guardians)

    if held_remnants is None:
        held_remnants = [0] * n

    details = []
    exp_full = []  # 完整浮点精度，用于计算
    for i, g in enumerate(guardians):
        cur = cur_stars[i]
        tgt = tgt_stars[i]
        held = held_remnants[i] if i < len(held_remnants) else 0
        need = STAR_CUM[tgt] - STAR_CUM[cur]
        gap = max(0, need - held)
        exp = get_exp_per_ticket(group_name, g["name"])
        exp_full.append(exp)

        details.append({
            "name": g["name"],
            "quality": g["quality"],
            "exp_per_ticket": round(exp, 4),  # 展示用（4位小数）
            "cur_star": cur,
            "tgt_star": tgt,
            "need": need,
            "held_remnant": held,
            "gap": gap,
            "essence_subsidy": 0,
            "tickets": 0,
        })

    # 应用精华流转
    flow_result = _calc_essence_flow(group_name, details, held_essence)
    details = flow_result["details"]
    essence_flow = flow_result["essence_flow"]

    # 计算各守护神所需请神符（使用完整浮点精度）
    # 一张符同时为所有守护神积累残念，因此总消耗 = 最慢到位的那个守护神的独立需求
    max_tickets = 0
    for i, d in enumerate(details):
        exp = exp_full[i]
        d["tickets"] = gap_to_tickets(d["gap"], exp) if exp > 0 else 0
        if d["tickets"] > max_tickets:
            max_tickets = d["tickets"]

    return {
        "error": None,
        "details": details,
        "total_tickets": max_tickets,
        "essence_flow": essence_flow,
    }


# ============================================================
# 八、简单模式
# ============================================================

def calc_simple(group_name: str, cur_avg: float, tgt_avg: float,
                held_remnants: list[int] | None = None,
                held_essence: int = 0) -> dict:
    """
    简单模式计算（输入平均星级）

    Args:
        group_name: 神仙谱组名称
        cur_avg: 当前平均星级
        tgt_avg: 目标平均星级
        held_remnants: 已持有各守护神残念列表
        held_essence: 已持有精华数量

    Returns:
        {
            "error": str|None,
            "group_name": str,
            "cur_avg": float,
            "tgt_avg": float,
            "plan_min": dict,      # 消耗最少方案
            "plan_typical": dict,  # 最常见方案
            "ticket_range": [min, max],
        }
    """
    # 参数校验
    if cur_avg < 0 or cur_avg > 5:
        return {"error": "当前平均星级范围 0.0 ~ 5.0"}
    if tgt_avg < 0 or tgt_avg > 5:
        return {"error": "目标平均星级范围 0.0 ~ 5.0"}
    if tgt_avg < cur_avg:
        return {"error": "目标平均星级不能低于当前平均星级"}

    group = find_group(group_name)
    if not group:
        return {"error": f"未找到神仙谱组: {group_name}"}

    n = len(group["guardians"])

    if tgt_avg == cur_avg:
        empty_details = [{
            "name": g["name"], "quality": g["quality"],
            "exp_per_ticket": round(get_exp_per_ticket(group_name, g["name"]), 4),
            "cur_star": 0, "tgt_star": 0, "need": 0, "held_remnant": 0,
            "gap": 0, "essence_subsidy": 0, "tickets": 0,
        } for g in group["guardians"]]
        empty_plan = {"error": None, "details": empty_details,
                      "total_tickets": 0, "essence_flow": {}}
        return {
            "error": None, "group_name": group_name,
            "cur_avg": cur_avg, "tgt_avg": tgt_avg,
            "plan_min": empty_plan, "plan_typical": empty_plan,
            "ticket_range": [0, 0],
        }

    # 展开分布
    cur_opt = expand_distribution(cur_avg, n, 'optimistic')   # 乐观：高星多
    tgt_pes = expand_distribution(tgt_avg, n, 'pessimistic')

    # ---- 星级分配策略 ----
    # 守护神在 GROUPS 中按权重从高到低排列（期望残念：高→低）
    # 消耗最少：高星分配给低期望（贵）守护神 → 当前星级升序排列
    #           目标也升序排列，使高期望守护神目标低、低期望守护神目标高

    # ---- 消耗最少方案 ----
    # 当前最乐观(集中) + 目标最悲观(分散)
    # 升序：高星给后面（低期望/贵守护神），低星给前面（高期望/便宜守护神）
    min_cur = sorted(cur_opt)
    min_tgt = sorted(tgt_pes)
    # 约束：目标不能低于当前
    for i in range(n):
        if min_tgt[i] < min_cur[i]:
            min_tgt[i] = min_cur[i]

    plan_min = _calc_group_plan(group_name, min_cur, min_tgt,
                                held_remnants, held_essence)
    plan_min["cur_distribution"] = min_cur
    plan_min["tgt_distribution"] = min_tgt

    # ---- 最常见方案 ----
    # 按期望残念速率比例加权分配星级
    typ_cur = expand_distribution_typical(cur_avg, group_name)
    typ_tgt = expand_distribution_typical(tgt_avg, group_name)
    # 约束：目标不能低于当前
    for i in range(n):
        if typ_tgt[i] < typ_cur[i]:
            typ_tgt[i] = typ_cur[i]

    plan_typical = _calc_group_plan(group_name, typ_cur, typ_tgt,
                                    held_remnants, held_essence)
    plan_typical["cur_distribution"] = typ_cur
    plan_typical["tgt_distribution"] = typ_tgt

    # ticket_range 取两个方案的最小值和最大值
    t_min_val = plan_min["total_tickets"]
    t_typical = plan_typical["total_tickets"]
    range_min = min(t_min_val, t_typical)
    range_max = max(t_min_val, t_typical)

    return {
        "error": None,
        "group_name": group_name,
        "cur_avg": cur_avg,
        "tgt_avg": tgt_avg,
        "plan_min": plan_min,
        "plan_typical": plan_typical,
        "ticket_range": [range_min, range_max],
    }


# ============================================================
# 九、精确模式
# ============================================================

def calc_precise(group_name: str, cur_stars: list[int], tgt_stars: list[int],
                 held_remnants: list[int] | None = None,
                 held_essence: int = 0) -> dict:
    """
    精确模式计算（输入各守护神星级）

    Args:
        group_name: 神仙谱组名称
        cur_stars: 当前各守护神星级列表
        tgt_stars: 目标各守护神星级列表
        held_remnants: 已持有各守护神残念列表
        held_essence: 已持有精华数量

    Returns:
        {
            "error": str|None,
            "details": list,
            "total_tickets": int,
            "essence_flow": dict,
        }
    """
    group = find_group(group_name)
    if not group:
        return {"error": f"未找到神仙谱组: {group_name}"}

    n = len(group["guardians"])

    if len(cur_stars) != n:
        return {"error": f"当前星级数量({len(cur_stars)})与该组守护神数量({n})不匹配"}
    if len(tgt_stars) != n:
        return {"error": f"目标星级数量({len(tgt_stars)})与该组守护神数量({n})不匹配"}

    # 校验范围
    for i in range(n):
        if cur_stars[i] < 0 or cur_stars[i] > 5:
            return {"error": f"{group['guardians'][i]['name']} 当前星级超出范围 [0,5]"}
        if tgt_stars[i] < 0 or tgt_stars[i] > 5:
            return {"error": f"{group['guardians'][i]['name']} 目标星级超出范围 [0,5]"}
        if tgt_stars[i] < cur_stars[i]:
            return {"error": f"{group['guardians'][i]['name']} 目标星级不能低于当前星级"}

    return _calc_group_plan(group_name, cur_stars, tgt_stars,
                            held_remnants, held_essence)
