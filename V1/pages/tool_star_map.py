"""
星图养成计算器模块
支持两种计算模式：
  模式一：升重材料计算 —— 输入当前重数和目标重数，计算所需碎晶数量
  模式二：锤炼期望消耗 —— 输入当前等级/目标等级，模拟计算期望星砂消耗

数据来源：星图系统养成分析.xlsx
"""

import customtkinter as ctk
import random
import threading


# ============================================================
# 常量定义
# ============================================================

STAR_MAPS = {
    "青龙": {
        "officials": ["角木蛟", "亢金龙", "氐土貉", "房日兔", "心月狐", "尾火虎", "箕水豹"],
        "material_name": "青龙碎晶",
    },
    "白虎": {
        "officials": ["奎木狼", "娄金狗", "胃土雉", "昴日鸡", "毕月乌", "参水猿", "觜火猴"],
        "material_name": "白虎碎晶",
    },
}

MAX_WEIGHT = 10
MAX_LEVEL = 6

WEIGHT_MATERIAL_COST = {w: w * 10 for w in range(1, MAX_WEIGHT + 1)}

HAMMER_PARAMS = {}

HAMMER_EXPECTED = {
    ("青龙", 1): 210, ("青龙", 2): 411, ("青龙", 3): 660, ("青龙", 4): 1098,
    ("青龙", 5): 577, ("青龙", 6): 1045, ("青龙", 7): 1680, ("青龙", 8): 775,
    ("青龙", 9): 2749, ("青龙", 10): 4400,
    ("白虎", 1): 622, ("白虎", 2): 1164, ("白虎", 3): 2014, ("白虎", 4): 2911,
    ("白虎", 5): 1559, ("白虎", 6): 2404, ("白虎", 7): 4984, ("白虎", 8): 1868,
    ("白虎", 9): 3214, ("白虎", 10): 4400,
}


def _get_material_for_weight(weight: int) -> str:
    if weight <= 4: return "碧木星砂"
    elif weight <= 7: return "云隐星砂"
    else: return "龙威星砂"


def _init_hammer_params():
    qinglong_data = {
        1: [(70,0,15),(70,15,15),(60,10,20),(60,15,20),(50,20,25),(50,20,25)],
        2: [(65,0,30),(65,15,30),(55,20,35),(50,20,35),(45,20,40),(40,25,40)],
        3: [(60,0,45),(60,15,45),(50,20,50),(45,20,50),(40,25,55),(35,25,55)],
        4: [(50,0,60),(45,20,60),(40,25,65),(35,25,65),(30,30,75),(30,30,75)],
        5: [(50,0,30),(45,20,32),(40,25,34),(35,25,36),(30,30,38),(30,30,40)],
        6: [(40,0,42),(40,25,44),(30,30,46),(30,30,48),(20,35,50),(20,35,54)],
        7: [(40,0,60),(40,25,66),(30,30,72),(30,30,78),(20,35,84),(15,35,96)],
        8: [(25,0,18),(20,25,22),(15,30,26),(15,30,28),(10,35,32),(10,35,36)],
        9: [(15,0,32),(10,35,32),(10,40,36),(5,40,36),(5,40,40),(5,40,40)],
        10:[(10,0,44),(10,40,44),(10,40,48),(5,40,48),(5,40,52),(5,40,52)],
    }
    baihu_data = {
        1: [(70,0,15),(70,15,15),(60,10,20),(60,15,20),(50,20,25),(50,20,25)],
        2: [(60,0,30),(55,15,30),(50,20,35),(45,20,35),(40,20,40),(35,25,40)],
        3: [(50,0,45),(45,15,45),(40,20,50),(35,20,50),(30,25,55),(25,25,55)],
        4: [(30,0,60),(25,20,60),(20,25,65),(15,25,65),(10,30,75),(10,30,75)],
        5: [(20,0,30),(20,20,32),(15,25,34),(15,25,36),(10,30,38),(10,30,40)],
        6: [(15,0,42),(15,25,44),(15,30,46),(10,30,48),(10,35,50),(10,35,54)],
        7: [(15,0,60),(15,25,66),(10,30,72),(10,30,78),(10,35,84),(5,35,90)],
        8: [(15,0,20),(15,30,20),(10,35,24),(10,35,24),(5,35,28),(5,35,28)],
        9: [(15,0,32),(10,35,32),(10,40,36),(5,40,36),(5,40,40),(5,40,40)],
        10:[(10,0,44),(10,40,44),(10,40,48),(5,40,48),(5,40,52),(5,40,52)],
    }
    for name, data in [("青龙", qinglong_data), ("白虎", baihu_data)]:
        for w, levels in data.items():
            for lvl, (base, demote, cost) in enumerate(levels, 1):
                key = f"{name}_{w}_{lvl}"
                HAMMER_PARAMS[key] = {
                    "star_map": name, "weight": w, "level": lvl,
                    "base_rate": base / 100.0,
                    "inc_rate": 0.15 if name == "青龙" else 0.10,
                    "max_rate": 1.0,
                    "demote_prob": demote / 100.0,
                    "cost": cost,
                }

_init_hammer_params()


# ============================================================
# 计算逻辑
# ============================================================

def calc_upgrade_material(star_map: str, officials: list, cur_w: int, tgt_w: int) -> dict:
    info = STAR_MAPS[star_map]
    selected = officials if officials else info["officials"]
    total_per_official = sum(WEIGHT_MATERIAL_COST.get(w, 0) for w in range(cur_w + 1, tgt_w + 1))
    total = total_per_official * len(selected)
    details = [{"weight": w, "per": WEIGHT_MATERIAL_COST[w], "total": WEIGHT_MATERIAL_COST[w] * len(selected)}
               for w in range(cur_w + 1, tgt_w + 1)]
    return {"total": total, "per_official": total_per_official, "mat_name": info["material_name"],
            "count": len(selected), "details": details}


def simulate_hammer(star_map, sw, sl, tw, tl, n=10000):
    results = []
    inc = HAMMER_PARAMS[f"{star_map}_1_1"]["inc_rate"]
    for _ in range(n):
        cost, cw, cl, bonus = 0, sw, sl, 0.0
        while (cw < tw) or (cw == tw and cl < tl):
            p = HAMMER_PARAMS[f"{star_map}_{cw}_{cl}"]
            cost += p["cost"]
            if random.random() < min(p["base_rate"] + bonus, p["max_rate"]):
                bonus = 0; cl += 1
                if cl > MAX_LEVEL: cl = 1; cw += 1
            else:
                bonus += inc
                if random.random() < p["demote_prob"]:
                    cl -= 1
                    if cl < 1:
                        if cw > sw: cw -= 1; cl = MAX_LEVEL
                        else: cl = 1
            if cost > 50000: break
        results.append(cost)
    results.sort()
    rn = len(results)
    return {
        "expected": sum(results)/rn, "median": results[rn//2],
        "p10": results[int(rn*0.10)], "p90": results[int(rn*0.90)],
        "min": results[0], "max": results[-1], "n": n,
        "mat": _get_material_for_weight(sw),
    }


def calc_quick_expected(star_map, sw, tw):
    result = {"total": 0, "by_w": {}}
    for w in range(sw + 1, tw + 1):
        e = HAMMER_EXPECTED.get((star_map, w), 0)
        result["by_w"][w] = {"expected": e, "mat": _get_material_for_weight(w)}
        result["total"] += e
    return result


# ============================================================
# 页面类
# ============================================================

class ToolStarMapPage(ctk.CTkFrame):

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self._build_ui()

    # ------------------------------------------------------------------
    # UI 构建
    # ------------------------------------------------------------------

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # 标题 + 副标题
        ctk.CTkLabel(scroll, text="☪️ 星图养成计算器",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(scroll, text="QQ华夏手游经典区 · 青龙+白虎 · 7星官/图 · 升重确定+锤炼概率期望值",
                     font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"], anchor="w"
                     ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # ---- 标签页切换 ----
        tab_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["📊 升重材料计算", "🎯 锤炼期望消耗"],
            height=34, font=ctk.CTkFont(size=13),
            selected_color=self.colors["nav_active"],
            unselected_color="#0f0f1a",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("📊 升重材料计算")

        # ===== Tab 1: 升重计算 =====
        self.tab1 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self._build_tab1()

        # ===== Tab 2: 锤炼计算 =====
        self.tab2 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self._build_tab2()

        # ---- 说明区域 ----
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(info_inner, text="📖 养成说明",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").pack(fill="x", pady=(0, 8))

        rules = [
            "· 星图分青龙、白虎两种，每种 7 个星官，各星官独立养成",
            "· 升重(重数)：确定性消耗，每重 N 需 N×10 碎晶/星官",
            "· 锤炼(等级)：概率事件，失败累积 10~15% 成功率，失败可能降级",
            "· 材料分段：碧木星砂(1~4重) → 云隐星砂(5~7重) → 龙威星砂(8~10重)",
            "· 白虎整体成功率低于青龙，消耗更大；白虎需青龙5重后解锁",
        ]
        for r in rules:
            ctk.CTkLabel(info_inner, text=r, font=ctk.CTkFont(size=12),
                         text_color=self.colors["text_dim"], anchor="w").pack(fill="x", pady=1)

    # ================================================================
    # Tab 1: 升重材料计算
    # ================================================================

    def _build_tab1(self):
        inner = ctk.CTkFrame(self.tab1, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        # -- 选择 --
        ctk.CTkLabel(inner, text="选择星图与星官", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.t1_starmap = ctk.CTkOptionMenu(
            inner, values=["① 青龙星图", "② 白虎星图"], height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t1_starmap.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t1_starmap.set("① 青龙星图")

        ctk.CTkLabel(inner, text="星官 (可单选或全部)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=2, column=0, sticky="w", padx=(0, 8))
        self.t1_official = ctk.CTkOptionMenu(
            inner, values=["全部星官"] + STAR_MAPS["青龙"]["officials"], height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t1_official.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.t1_official.set("全部星官")

        # -- 当前/目标重数 --
        ctk.CTkLabel(inner, text="重数设置", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(row=4, column=0, columnspan=2, sticky="w", pady=(6, 6))

        ctk.CTkLabel(inner, text="当前重数 (0=未激活)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=5, column=0, sticky="w", padx=(0, 8))
        self.t1_cur_w = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_cur_w.grid(row=6, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t1_cur_w.insert(0, "0")

        ctk.CTkLabel(inner, text="目标重数 (1~10)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=5, column=1, sticky="w", padx=(8, 0))
        self.t1_tgt_w = ctk.CTkEntry(inner, placeholder_text="10", height=32, corner_radius=6)
        self.t1_tgt_w.grid(row=6, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t1_tgt_w.insert(0, "10")

        # 按钮 + 结果
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 8))

        ctk.CTkButton(btn_row, text="▶  计算升重材料",
                      font=ctk.CTkFont(size=14, weight="bold"), height=40, corner_radius=8,
                      fg_color="#0f3460", hover_color="#16213e",
                      command=self._calc_upgrade).pack(fill="x")

        self.t1_result = ctk.CTkTextbox(inner, height=220, corner_radius=8,
                                         fg_color="#0f0f1a", font=ctk.CTkFont(size=13))
        self.t1_result.grid(row=8, column=0, columnspan=2, sticky="ew")
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")

    # ================================================================
    # Tab 2: 锤炼期望消耗
    # ================================================================

    def _build_tab2(self):
        inner = ctk.CTkFrame(self.tab2, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        # -- 选择星图 --
        ctk.CTkLabel(inner, text="选择星图", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.t2_starmap = ctk.CTkOptionMenu(
            inner, values=["① 青龙星图", "② 白虎星图"], height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t2_starmap.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.t2_starmap.set("① 青龙星图")

        # -- 起始状态 --
        ctk.CTkLabel(inner, text="起始状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 6))

        ctk.CTkLabel(inner, text="起始重数 (1~10)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=3, column=0, sticky="w", padx=(0, 8))
        self.t2_start_w = ctk.CTkEntry(inner, placeholder_text="1", height=32, corner_radius=6)
        self.t2_start_w.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t2_start_w.insert(0, "1")

        ctk.CTkLabel(inner, text="起始等级 (1~6)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=3, column=1, sticky="w", padx=(8, 0))
        self.t2_start_l = ctk.CTkEntry(inner, placeholder_text="1", height=32, corner_radius=6)
        self.t2_start_l.grid(row=4, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t2_start_l.insert(0, "1")

        # -- 目标状态 --
        ctk.CTkLabel(inner, text="目标状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(row=5, column=0, columnspan=2, sticky="w", pady=(8, 6))

        ctk.CTkLabel(inner, text="目标重数 (1~10)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=6, column=0, sticky="w", padx=(0, 8))
        self.t2_tgt_w = ctk.CTkEntry(inner, placeholder_text="10", height=32, corner_radius=6)
        self.t2_tgt_w.grid(row=7, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t2_tgt_w.insert(0, "10")

        ctk.CTkLabel(inner, text="目标等级 (1~6)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=6, column=1, sticky="w", padx=(8, 0))
        self.t2_tgt_l = ctk.CTkEntry(inner, placeholder_text="6", height=32, corner_radius=6)
        self.t2_tgt_l.grid(row=7, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t2_tgt_l.insert(0, "6")

        # -- 计算方式 --
        ctk.CTkLabel(inner, text="计算方式", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=8, column=0, sticky="w", padx=(0, 8), pady=(6, 4))
        self.t2_method = ctk.CTkOptionMenu(
            inner, values=["快速期望值(推荐)", "蒙特卡洛模拟(10000次)"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t2_method.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t2_method.set("快速期望值(推荐)")

        # 按钮 + 结果
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(8, 8))

        ctk.CTkButton(btn_row, text="▶  计算锤炼消耗",
                      font=ctk.CTkFont(size=14, weight="bold"), height=40, corner_radius=8,
                      fg_color="#2e7d32", hover_color="#1b5e20",
                      command=self._calc_hammer).pack(fill="x")

        self.t2_result = ctk.CTkTextbox(inner, height=240, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13))
        self.t2_result.grid(row=11, column=0, columnspan=2, sticky="ew")
        self.t2_result.insert("1.0", "等待计算...\n")
        self.t2_result.configure(state="disabled")

    # ================================================================
    # 标签页切换
    # ================================================================

    def _on_tab_change(self, value):
        if value == "📊 升重材料计算":
            self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2.grid_forget()
        else:
            self.tab2.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1.grid_forget()

    # ================================================================
    # 辅助方法
    # ================================================================

    @staticmethod
    def _show(tb: ctk.CTkTextbox, text: str):
        tb.configure(state="normal"); tb.delete("1.0", "end"); tb.insert("1.0", text); tb.configure(state="disabled")

    @staticmethod
    def _err(tb: ctk.CTkTextbox, msg: str):
        ToolStarMapPage._show(tb, f"⚠️ {msg}\n")

    @staticmethod
    def _int(val: str, default: int) -> int:
        try: return int((val or "").strip() or str(default))
        except: return default

    def _parse_star_map(self, opt: str) -> str:
        return "青龙" if "青龙" in opt else "白虎"

    def _sync_official_options(self):
        sm = self._parse_star_map(self.t1_starmap.get())
        officials = STAR_MAPS[sm]["officials"]
        current = self.t1_official.get()
        new_values = ["全部星官"] + officials
        self.t1_officials_box.configure(values=new_values)
        if current in new_values:
            self.t1_official.set(current)
        else:
            self.t1_official.set("全部星官")

    # ================================================================
    # Tab 1: 升重计算回调
    # ================================================================

    def _calc_upgrade(self):
        try:
            sm = self._parse_star_map(self.t1_starmap.get())
            cur_w = self._int(self.t1_cur_w.get(), 0)
            tgt_w = self._int(self.t1_tgt_w.get(), 10)
            official_choice = self.t1_official.get()
        except Exception:
            self._err(self.t1_result, "输入有误！"); return

        if not (0 <= cur_w <= MAX_WEIGHT):
            self._err(self.t1_result, f"当前重数需在 0 ~ {MAX_WEIGHT} 之间"); return
        if not (1 <= tgt_w <= MAX_WEIGHT):
            self._err(self.t1_result, f"目标重数需在 1 ~ {MAX_WEIGHT} 之间"); return
        if tgt_w <= cur_w:
            self._err(self.t1_result, "目标重数必须大于当前重数！"); return

        all_off = STAR_MAPS[sm]["officials"]
        selected = all_off if official_choice == "全部星官" else [official_choice]

        r = calc_upgrade_material(sm, selected, cur_w, tgt_w)
        lines = [
            f"━━━ 升重材料需求 ━━━\n",
            f"星图：{sm}  |  星官：{r['count']}个 ({', '.join(selected[:3])}{'...' if len(selected)>3 else ''})",
            f"从 {cur_w}重 → {tgt_w}重  (共提升 {tgt_w - cur_w} 重)\n",
            "┌──────────────────────────┐",
            f"│ {'材料':<16} {'数量':>10} │",
            "├──────────────────────────┤",
            f"│ {r['mat_name']:<16} {r['total']:>10,} │",
            f"│ (每个星官){'':<8} {r['per_official']:>10,} │",
            "└──────────────────────────┘",
            "",
            "各重详细消耗：",
        ]
        for d in r["details"]:
            lines.append(f"  {d['weight']}重：{d['per']:,} × {r['count']} = {d['total']:,}")

        if selected != all_off and len(selected) < len(all_off):
            full_total = r["total"] * len(all_off) // len(selected) if selected else 0
            lines.append(f"\n注：若全部 {len(all_off)} 个星官升至 {tgt_w}重，需 {full_total:,} {r['mat_name']}")

        self._show(self.t1_result, "\n".join(lines) + "\n")

    # ================================================================
    # Tab 2: 锤炼计算回调
    # ================================================================

    def _calc_hammer(self):
        try:
            sm = self._parse_star_map(self.t2_starmap.get())
            sw = self._int(self.t2_start_w.get(), 1)
            sl = self._int(self.t2_start_l.get(), 1)
            tw = self._int(self.t2_tgt_w.get(), 10)
            tl = self._int(self.t2_tgt_l.get(), 6)
            method = self.t2_method.get()
        except Exception:
            self._err(self.t2_result, "输入有误！"); return

        if not (1 <= sw <= MAX_WEIGHT and 1 <= tw <= MAX_WEIGHT):
            self._err(self.t2_result, f"重数需在 1 ~ {MAX_WEIGHT} 之间"); return
        if not (1 <= sl <= MAX_LEVEL and 1 <= tl <= MAX_LEVEL):
            self._err(self.t2_result, f"等级需在 1 ~ {MAX_LEVEL} 之间"); return
        if (tw, tl) <= (sw, sl):
            self._err(self.t2_result, "目标必须高于起始值！"); return

        if "蒙特卡洛" in method:
            self._run_mc(sm, sw, sl, tw, tl)
        else:
            self._run_quick(sm, sw, sl, tw, tl)

    def _run_quick(self, sm, sw, sl, tw, tl):
        r = calc_quick_expected(sm, sw, tw)
        lines = [
            f"━━━ 锤炼期望消耗 ━━━\n",
            f"星图：{sm}  |  方式：快速期望值",
            f"从 {sw}重{sl}级 → {tw}重{tl}级\n",
            f"  ✦ 总期望消耗：{r['total']:,}",
            "",
            "各重详情：",
        ]
        for w, info in sorted(r["by_w"].items()):
            lines.append(f"  {w}重 → {info['expected']:,} {info['mat']}")
        lines.extend(["", "提示：", "  · 期望值为平均消耗，实际因降级惩罚可能更高", "  · 白虎成功率更低，实际消耗常超期望值", "  · 如需区间估算请切换【蒙特卡洛模拟】"])
        self._show(self.t2_result, "\n".join(lines) + "\n")

    def _run_mc(self, sm, sw, sl, tw, tl):
        self._show(self.t2_result, "⏳ 正在运行 10000 次蒙特卡洛模拟...\n")

        def worker():
            r = simulate_hammer(sm, sw, sl, tw, tl, 10000)
            lines = [
                f"━━━ 锤炼消耗(蒙特卡洛) ━━━\n",
                f"星图：{sm}  |  模拟次数：{r['n']:,}",
                f"从 {sw}重{sl}级 → {tw}重{tl}级\n",
                f"  ✦ 期望值 E[x]：   {r['expected']:,.0f} {r['mat']}",
                f"  🟩 中位数 P50：   {r['median']:,.0f}",
                f"  🟨 乐观值 P10：   {r['p10']:.0f}   (仅10%的人比这幸运)",
                f"  🟥 悲观值 P90：   {r['p90']:.0f}   (90%的人花费不超过此)",
                f"  📊 极值范围：     {r['min']:,} ~ {r['max']:,}",
            ]
            self.after(0, lambda: self._show(self.t2_result, "\n".join(lines) + "\n"))

        threading.Thread(target=worker, daemon=True).start()
