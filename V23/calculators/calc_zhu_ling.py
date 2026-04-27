"""
注灵养成计算器 - 纯计算模块
从 pages/tool_zhu_ling.py 提取，不含任何 UI 依赖。

支持两种计算模式：
  模式一：根据持有材料 → 算可达到的注灵等级
  模式二：根据目标等级 → 算全套/单部位材料需求
"""

from utils.data_loader import load_game_data

# ============================================================
# 一、数据加载
# ============================================================

_JSON = load_game_data("zhuling_data.json")
_DATA = _JSON["data"]
_PART_NAMES = _JSON["part_names"]

_SET_NAMES = [d["套装"] for d in _DATA if d["等级"] == 1]

# 预建套装数据索引：{套装名: [逐级数据列表]}
_SET_DATA_CACHE: dict = {}
for _d in _DATA:
    _SET_DATA_CACHE.setdefault(_d["套装"], []).append(_d)

# 预建材料名缓存：{套装名: [材料名列表]}
_MAT_CACHE: dict = {}
for _sn in _SET_NAMES:
    _seen: list = []
    for _r in _SET_DATA_CACHE[_sn]:
        if _r["开启名"] not in _seen:
            _seen.append(_r["开启名"])
        if _r["刷新保名"] not in _seen:
            _seen.append(_r["刷新保名"])
    _MAT_CACHE[_sn] = _seen


# ============================================================
# 二、数据查询
# ============================================================

PART_NAMES = _PART_NAMES
SET_NAMES = _SET_NAMES
DATA = _DATA


def get_set_data(set_name: str) -> list:
    """获取指定套装的逐级数据列表"""
    return _SET_DATA_CACHE.get(set_name, [])


def get_materials(set_name: str) -> list:
    """获取指定套装的材料名列表"""
    return _MAT_CACHE.get(set_name, [])


def set_display(name: str) -> str:
    """套装显示名（加解锁等级）"""
    for d in _DATA:
        if d["套装"] == name:
            return f"{name}(Lv.{d['解锁']}解)"
    return name


# ============================================================
# 三、计算函数
# ============================================================

def calc_by_materials(set_name: str, start_lv: int, holdings: dict) -> dict:
    """
    模式一：根据材料计算可达等级

    参数:
        set_name:   套装名称
        start_lv:   起始等级 (0~9)
        holdings:   材料持有量 {材料名: 数量}

    返回:
        {
            "error": str|None,
            "reachable_lv": int,
            "table_data": list,   # 逐级明细
        }
    """
    rows = get_set_data(set_name)
    if not rows:
        return {"error": "未找到套装数据。"}

    if start_lv >= 10:
        return {"error": "已满级(10级)，无需继续提升。"}

    current_holdings = dict(holdings)
    reachable_lv = start_lv
    table_data = []

    for lv_idx in range(start_lv, len(rows)):
        row_data = rows[lv_idx]
        lv = row_data["等级"]

        open_cost_name = row_data["开启名"]
        open_need = row_data["开启全位"]
        refresh_main_total = row_data["单级刷新主总"]
        refresh_bao_total = row_data["单级刷新保总"]
        refresh_bao_name = row_data["刷新保名"]
        refresh_main_name = row_data["刷新主名"]

        open_avail = current_holdings.get(open_cost_name, 0)
        refresh_main_avail = current_holdings.get(refresh_main_name, 0)
        bao_avail = current_holdings.get(refresh_bao_name, 0)

        can_open = open_avail >= open_need
        can_refresh = (refresh_main_avail >= refresh_main_total and
                       bao_avail >= refresh_bao_total)

        if not can_open or not can_refresh:
            open_lack = f"(差{open_need - open_avail})" if not can_open else ""
            main_lack = f"(差{refresh_main_total - refresh_main_avail})" if refresh_main_avail < refresh_main_total else ""
            bao_lack = f"(差{refresh_bao_total - bao_avail})" if bao_avail < refresh_bao_total else ""

            table_data.append([
                f"Lv.{lv}",
                open_cost_name, open_need, open_lack,
                refresh_main_name, refresh_main_total, main_lack,
                refresh_bao_name, refresh_bao_total, bao_lack,
                "❌ 材料不足"
            ])
            break
        else:
            current_holdings[open_cost_name] = open_avail - open_need
            current_holdings[refresh_main_name] = refresh_main_avail - refresh_main_total
            current_holdings[refresh_bao_name] = bao_avail - refresh_bao_total
            reachable_lv = lv

            table_data.append([
                f"Lv.{lv}",
                open_cost_name, open_need, "",
                refresh_main_name, refresh_main_total, "",
                refresh_bao_name, refresh_bao_total, "",
                "✅ 已达成"
            ])

    return {
        "error": None,
        "reachable_lv": reachable_lv,
        "table_data": table_data,
    }


def calc_by_target(set_name: str, start_lv: int, target_lv: int) -> dict:
    """
    模式二：根据目标等级计算材料需求

    参数:
        set_name:   套装名称
        start_lv:   起始等级
        target_lv:  目标等级

    返回:
        {
            "error": str|None,
            "unlock": str|int,
            "total_open": dict,
            "total_refresh_m": dict,
            "total_refresh_b": dict,
            "table_data": list,
        }
    """
    rows = get_set_data(set_name)
    if not rows:
        return {"error": "未找到套装数据。"}

    if target_lv <= start_lv:
        return {"error": "目标等级需大于起始等级。"}

    unlock = rows[0]["解锁"]

    table_data = []
    total_open = {}
    total_refresh_m = {}
    total_refresh_b = {}

    for lv_idx in range(start_lv, target_lv):
        r = rows[lv_idx]
        lv = r["等级"]
        oname = r["开启名"]
        oqty = r["开启全位"]
        rn = r["刷新主名"]
        rq = r["单级刷新主总"]
        bn = r["刷新保名"]
        bq = r["单级刷新保总"]

        total_open[oname] = total_open.get(oname, 0) + oqty
        total_refresh_m[rn] = total_refresh_m.get(rn, 0) + rq
        total_refresh_b[bn] = total_refresh_b.get(bn, 0) + bq

        table_data.append([
            f"Lv.{lv}",
            oname, oqty,
            rn, rq,
            bn, bq,
            "全套11部位"
        ])

    return {
        "error": None,
        "unlock": unlock,
        "total_open": total_open,
        "total_refresh_m": total_refresh_m,
        "total_refresh_b": total_refresh_b,
        "table_data": table_data,
    }
