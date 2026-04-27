"""
星录养成计算引擎
纯数据 + 纯计算函数，不依赖任何 UI 框架。
"""

# ============================================================
# 一、星录基础配置
# ============================================================

XINLU_CONFIG = {
    "太微": {
        "max_chong": 20,
        "low_mat": "南明离火", "mid_mat": "九幽玄火", "high_mat": "红莲业火",
        "guard": "灵运石", "upgrade": "升重石",
        "unlock_lv": 0, "pre_req": "无",
    },
    "紫微": {
        "max_chong": 20,
        "low_mat": "破军寒玉", "mid_mat": "贪狼煞玉", "high_mat": "天府瑞玉",
        "guard": "仙运石",
        "unlock_lv": 108, "pre_req": "太微达7重",
    },
    "天市": {
        "max_chong": 22,
        "low_mat": "通财幽泉", "mid_mat": "朔雪寒泉", "high_mat": "星河神泉",
        "guard": "吉运石", "upgrade": "天市升重圭",
        "unlock_lv": 220, "pre_req": "紫微达7重",
    },
    "启明": {
        "max_chong": 20,
        "low_mat": "百炼赤金", "mid_mat": "千锻精金", "high_mat": "万融庚金",
        "guard": "福运石",
        "unlock_lv": 260, "pre_req": "天市达5重",
    },
}

XINLU_NAMES = list(XINLU_CONFIG.keys())

# ============================================================
# 二、锤炼消耗数据
# ============================================================

_FORGE_RAW = [
    (1,1,1,1.18,1.2,1,1.2),(1,2,1,1.18,1.2,1,1.2),(1,3,2,1.33,2.7,1,1.3),
    (1,4,2,1.33,2.7,1,1.3),(1,5,3,1.54,4.6,1,1.5),(1,6,3,1.54,4.6,1,1.5),
    (2,1,1,1.18,1.2,2,2.4),(2,2,1,1.18,1.2,2,2.4),(2,3,2,1.33,2.7,2,2.7),
    (2,4,2,1.33,2.7,2,2.7),(2,5,3,1.54,4.6,2,3.1),(2,6,3,1.54,4.6,2,3.1),
    (3,1,1,1.18,1.2,3,3.5),(3,2,1,1.18,1.2,3,3.5),(3,3,2,1.33,2.7,3,4),
    (3,4,2,1.33,2.7,3,4),(3,5,3,1.54,4.6,3,4.6),(3,6,3,1.54,4.6,3,4.6),
    (4,1,1,1.18,1.2,4,4.7),(4,2,1,1.18,1.2,4,4.7),(4,3,2,1.33,2.7,4,5.3),
    (4,4,2,1.33,2.7,4,5.3),(4,5,3,1.54,4.6,4,6.2),(4,6,3,1.54,4.6,4,6.2),
    (5,1,1,1.18,1.2,5,5.9),(5,2,1,1.18,1.2,5,5.9),(5,3,2,1.33,2.7,5,6.7),
    (5,4,2,1.33,2.7,5,6.7),(5,5,3,1.54,4.6,5,7.7),(5,6,3,1.54,4.6,5,7.7),
    (6,1,5,2,10,3,6),(6,2,5,2,10,3,6),(6,3,10,2.5,25,3,7.5),
    (6,4,10,2.5,25,3,7.5),(6,5,15,3.33,50,3,10),(6,6,15,3.33,50,3,10),
    (7,1,15,2,30,4,8),(7,2,15,2,30,4,8),(7,3,20,2.5,50,4,10),
    (7,4,20,2.5,50,4,10),(7,5,25,3.33,83.2,4,13.3),(7,6,25,3.33,83.2,4,13.3),
    (8,1,25,2,50,5,10),(8,2,25,2,50,5,10),(8,3,30,2.5,75,5,12.5),
    (8,4,30,2.5,75,5,12.5),(8,5,35,3.33,116.5,5,16.6),(8,6,35,3.33,116.5,5,16.6),
    (9,1,35,2.5,87.5,6,15),(9,2,35,2.5,87.5,6,15),(9,3,40,3.33,133.2,6,20),
    (9,4,40,3.33,133.2,6,20),(9,5,45,5,225,6,30),(9,6,45,5,225,6,30),
    (10,1,40,2.5,100,7,17.5),(10,2,40,2.5,100,7,17.5),(10,3,45,3.33,149.8,7,23.3),
    (10,4,45,3.33,149.8,7,23.3),(10,5,50,5,250,7,35),(10,6,50,5,250,7,35),
    (11,1,10,6.67,66.7,4,26.7),(11,2,10,6.67,66.7,4,26.7),(11,3,15,6.67,100,4,26.7),
    (11,4,15,6.67,100,4,26.7),(11,5,20,6.67,133.4,4,26.7),(11,6,20,6.67,133.4,4,26.7),
    (12,1,15,6.67,100,5,33.4),(12,2,15,6.67,100,5,33.4),(12,3,20,6.67,133.4,5,33.4),
    (12,4,20,6.67,133.4,5,33.4),(12,5,25,6.67,166.8,5,33.4),(12,6,25,6.67,166.8,5,33.4),
    (13,1,20,6.67,133.4,6,40),(13,2,20,6.67,133.4,6,40),(13,3,25,6.67,166.8,6,40),
    (13,4,25,6.67,166.8,6,40),(13,5,30,6.67,200.1,6,40),(13,6,30,6.67,200.1,6,40),
    (14,1,25,10,250,7,70),(14,2,25,10,250,7,70),(14,3,30,10,300,7,70),
    (14,4,30,10,300,7,70),(14,5,35,10,350,7,70),(14,6,35,10,350,7,70),
    (15,1,30,10,300,8,80),(15,2,30,10,300,8,80),(15,3,35,10,350,8,80),
    (15,4,35,10,350,8,80),(15,5,40,10,400,8,80),(15,6,40,10,400,8,80),
    (16,1,5,10,50,8,80),(16,2,5,10,50,8,80),(16,3,10,10,100,8,80),
    (16,4,10,10,100,8,80),(16,5,15,10,150,8,80),(16,6,15,10,150,8,80),
    (17,1,5,10,50,9,90),(17,2,5,10,50,9,90),(17,3,10,10,100,9,90),
    (17,4,10,10,100,9,90),(17,5,20,10,200,9,90),(17,6,20,10,200,9,90),
    (18,1,5,10,50,10,100),(18,2,5,10,50,10,100),(18,3,15,10,150,10,100),
    (18,4,15,10,150,10,100),(18,5,20,10,200,10,100),(18,6,20,10,200,10,100),
    (19,1,10,20,200,11,220),(19,2,10,20,200,11,220),(19,3,15,20,300,11,220),
    (19,4,15,20,300,11,220),(19,5,20,20,400,11,220),(19,6,20,20,400,11,220),
    (20,1,10,20,200,12,240),(20,2,10,20,200,12,240),(20,3,15,20,300,12,240),
    (20,4,15,20,300,12,240),(20,5,25,20,500,12,240),(20,6,25,20,500,12,240),
    (21,1,15,20,300,20,400),(21,2,15,20,300,20,400),(21,3,20,20,400,25,500),
    (21,4,20,20,400,25,500),(21,5,25,20,500,30,600),(21,6,25,20,500,30,600),
    (22,1,20,20,400,25,500),(22,2,20,20,400,25,500),(22,3,25,20,500,30,600),
    (22,4,25,20,500,30,600),(22,5,30,20,600,40,800),(22,6,30,20,600,40,800),
]

FORGE_DATA = {}
for _row in _FORGE_RAW:
    _chong, _star, _, _, _exp_mat, _guard_per, _exp_guard = _row
    FORGE_DATA[(_chong, _star)] = {
        "exp_mat": _exp_mat,
        "exp_guard": _exp_guard,
    }
del _FORGE_RAW

# 启明17-20重保级消耗特殊值
QIMING_GUARD_OVERRIDE = {
    (17, 1): 12, (17, 2): 12, (17, 3): 12, (17, 4): 12, (17, 5): 12, (17, 6): 12,
    (18, 1): 21, (18, 2): 21, (18, 3): 21, (18, 4): 21, (18, 5): 21, (18, 6): 21,
    (19, 1): 34, (19, 2): 34, (19, 3): 34, (19, 4): 34, (19, 5): 34, (19, 6): 34,
    (20, 1): 49, (20, 2): 49, (20, 3): 49, (20, 4): 49, (20, 5): 49, (20, 6): 49,
}


# ============================================================
# 纯函数
# ============================================================

def get_mat_tier(chong):
    """根据重数返回材料阶次: 'low'(1-10), 'mid'(11-15), 'high'(16+)"""
    if chong <= 10:
        return "low"
    elif chong <= 15:
        return "mid"
    else:
        return "high"


def get_mat_name(xinlu_name, tier):
    """获取某星录某阶次的实际材料名"""
    cfg = XINLU_CONFIG[xinlu_name]
    return cfg[f"{tier}_mat"]


def get_guard_exp(xinlu_name, chong, star):
    """获取某星录某(重数,星级)的期望保级消耗"""
    base = FORGE_DATA.get((chong, star), {}).get("exp_guard", 0)
    if xinlu_name == "启明" and (chong, star) in QIMING_GUARD_OVERRIDE:
        fd = FORGE_DATA.get((chong, star))
        if fd:
            base_guard_per = {17: 9, 18: 10, 19: 11, 20: 12}.get(chong, 0)
            if base_guard_per > 0:
                exp_times = base / base_guard_per
                special_per = QIMING_GUARD_OVERRIDE[(chong, star)]
                return round(exp_times * special_per, 1)
    return base


def get_forge_exp_mat(chong, star):
    """获取某(重数,星级)的期望主材料消耗"""
    return FORGE_DATA.get((chong, star), {}).get("exp_mat", 0)


# ============================================================
# 计算函数
# ============================================================

def calc_by_materials(xinlu_name: str, cur_chong: int, cur_star: int,
                      low_mat: float, mid_mat: float, high_mat: float,
                      guard: float) -> dict:
    """
    根据材料计算可达等级（单个星官）。

    参数:
        xinlu_name: 星录名称
        cur_chong: 当前重数
        cur_star: 当前星级
        low_mat/mid_mat/high_mat/guard: 各材料数量 (float('inf') 表示无限)

    返回:
        dict: {chong, star, used: {low, mid, high, guard}}
    """
    cfg = XINLU_CONFIG[xinlu_name]
    max_chong = cfg["max_chong"]

    used = {"low": 0, "mid": 0, "high": 0, "guard": 0}
    chong = cur_chong
    star = cur_star
    stopped = False

    while chong <= max_chong and not stopped:
        if chong > 20 and xinlu_name != "天市":
            break

        start_star = star + 1 if star < 6 else 7
        for s in range(start_star, 7):
            forge_key = (chong, s)
            if forge_key not in FORGE_DATA:
                stopped = True
                break

            exp_mat = get_forge_exp_mat(chong, s)
            exp_guard_val = get_guard_exp(xinlu_name, chong, s)
            tier = get_mat_tier(chong)

            mat_pool = {"low": low_mat, "mid": mid_mat, "high": high_mat}
            if mat_pool[tier] != float("inf") and mat_pool[tier] < exp_mat:
                stopped = True
                break
            if guard != float("inf") and guard < exp_guard_val:
                stopped = True
                break

            if mat_pool[tier] != float("inf"):
                if tier == "low":
                    low_mat -= exp_mat
                elif tier == "mid":
                    mid_mat -= exp_mat
                else:
                    high_mat -= exp_mat
            if guard != float("inf"):
                guard -= exp_guard_val

            used[tier] += exp_mat
            used["guard"] += exp_guard_val
            star = s

        if stopped:
            break

        if star == 6 and chong < max_chong:
            chong += 1
            star = 0
        elif star == 6 and chong == max_chong:
            break
        else:
            break

    return {"chong": chong, "star": star, "used": used}


def calc_for_target(xinlu_name: str, start_chong: int, start_star: int,
                    target_chong: int, target_star: int) -> dict:
    """
    根据目标计算所需材料（单个星官）。

    返回:
        dict: {used: {low, mid, high, guard}, error: str|None}
    """
    cfg = XINLU_CONFIG[xinlu_name]
    max_chong = cfg["max_chong"]

    if target_chong > 20 and xinlu_name != "天市":
        return {"error": f"{xinlu_name}最高{max_chong}重", "used": None}

    used = {"low": 0, "mid": 0, "high": 0, "guard": 0}
    chong = start_chong
    star = start_star

    while True:
        if chong > target_chong:
            break
        if chong == target_chong and star >= target_star:
            break

        next_star = star + 1
        if next_star <= 6:
            end_star_this_chong = 6 if chong < target_chong else target_star
            for s in range(next_star, end_star_this_chong + 1):
                forge_key = (chong, s)
                if forge_key not in FORGE_DATA:
                    break
                exp_mat = get_forge_exp_mat(chong, s)
                exp_guard_val = get_guard_exp(xinlu_name, chong, s)
                tier = get_mat_tier(chong)
                used[tier] += exp_mat
                used["guard"] += exp_guard_val
            star = end_star_this_chong
            if chong == target_chong:
                break
            if star == 6 and chong < target_chong:
                chong += 1
                star = 0
            else:
                break
        elif star == 6:
            if chong < target_chong:
                chong += 1
                star = 0
            else:
                break
        else:
            break

    return {"used": used, "error": None}
