"""
风水录养成计算器模块
QQ华夏手游经典区 · 风水录养成系统计算工具

支持两种计算模式：
  模式一：目标规划（已知起终点，求材料）
  模式二：资源评估（已知材料，求可达等级）

数据来源：风水录养成计算器参考数据.xlsx
"""

import customtkinter as ctk


# ============================================================
# 一、风水点数据（来自 AI计算参考数据 Sheet）
# ============================================================

# 索引: 风水点ID (1~24)
FENG_SHUI_POINTS = {
    # --- 北郡 (ID 1~6) ---
    1: {"name": "平原村", "map": "北郡", "main_mat": "神兽石", "main_per": 2,
        "sub_mat": None, "sub_per": 0,
        "progress": [0, 250, 380, 500, 630, 850],
        "card_star": 1, "card_extra": 6},
    2: {"name": "寂幻坛", "map": "北郡", "main_mat": "神兽石", "main_per": 2,
        "sub_mat": None, "sub_per": 0,
        "progress": [0, 250, 380, 500, 630, 850],
        "card_star": 1, "card_extra": 6},
    3: {"name": "东夷祭坛", "map": "北郡", "main_mat": "神兽石", "main_per": 2,
        "sub_mat": None, "sub_per": 0,
        "progress": [0, 250, 380, 500, 630, 850],
        "card_star": 1, "card_extra": 6},
    4: {"name": "天羽村", "map": "北郡", "main_mat": "神兽石", "main_per": 1,
        "sub_mat": None, "sub_per": 0,
        "progress": [0, 250, 380, 500, 630, 850],
        "card_star": 1, "card_extra": 4},
    5: {"name": "遗逐村", "map": "北郡", "main_mat": "神兽石", "main_per": 1,
        "sub_mat": None, "sub_per": 0,
        "progress": [0, 250, 380, 500, 630, 850],
        "card_star": 1, "card_extra": 4},
    6: {"name": "百果祀", "map": "北郡", "main_mat": "神兽石", "main_per": 1,
        "sub_mat": None, "sub_per": 0,
        "progress": [0, 250, 380, 500, 630, 850],
        "card_star": 1, "card_extra": 4},

    # --- 琅琊盆地 (ID 7~12) ---
    7: {"name": "神祀", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 2,
        "sub_mat": "神兽石·星", "sub_per": 2,
        "progress": [0, 380, 760, 950, 1140, 1340],
        "card_star": 0, "card_extra": 0},
    8: {"name": "七迷洞", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 2,
        "sub_mat": "神兽石·星", "sub_per": 2,
        "progress": [0, 380, 760, 950, 1140, 1340],
        "card_star": 0, "card_extra": 0},
    9: {"name": "琅琊山", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 2,
        "sub_mat": "神兽石·星", "sub_per": 2,
        "progress": [0, 380, 760, 950, 1140, 1340],
        "card_star": 0, "card_extra": 0},
    10: {"name": "长股村落", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 1,
         "sub_mat": "神兽石·星", "sub_per": 2,
         "progress": [0, 380, 760, 950, 1140, 1340],
         "card_star": 0, "card_extra": 0},
    11: {"name": "长右村落", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 1,
         "sub_mat": "神兽石·星", "sub_per": 2,
         "progress": [0, 380, 760, 950, 1140, 1340],
         "card_star": 0, "card_extra": 0},
    12: {"name": "东海崖", "map": "琅琊盆地", "main_mat": "缠山图", "main_per": 1,
         "sub_mat": "神兽石·星", "sub_per": 2,
         "progress": [0, 380, 760, 950, 1140, 1340],
         "card_star": 0, "card_extra": 0},

    # --- 昆仑 (ID 13~18) ---
    13: {"name": "翔舞部落", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 2,
          "sub_mat": "寻龍图", "sub_per": 2,
          "progress": [0, 540, 1090, 1360, 1630, 1900],
          "card_star": 0, "card_extra": 0},
    14: {"name": "延维聚落", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 2,
          "sub_mat": None, "sub_per": 0,
          "progress": [0, 540, 1090, 1360, 1630, 1900],
          "card_star": 0, "card_extra": 0},
    15: {"name": "昆仑山", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 1,
          "sub_mat": "寻龍图", "sub_per": 2,
          "progress": [0, 540, 1090, 1360, 1630, 1900],
          "card_star": 0, "card_extra": 0},
    16: {"name": "不冻泉", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 2,
          "sub_mat": None, "sub_per": 0,
          "progress": [0, 540, 1090, 1360, 1630, 1900],
          "card_star": 0, "card_extra": 0},
    17: {"name": "蜃楼", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 1,
          "sub_mat": "寻龍图", "sub_per": 2,
          "progress": [0, 540, 1090, 1360, 1630, 1900],
          "card_star": 0, "card_extra": 0},
    18: {"name": "玉珠峰", "map": "昆仑", "main_mat": "神兽石·月", "main_per": 2,
          "sub_mat": "寻龍图", "sub_per": 2,
          "progress": [0, 540, 1090, 1360, 1630, 1900],
          "card_star": 0, "card_extra": 0},

    # --- 轩辕 (ID 19~24) ---
    19: {"name": "银明山", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2,
          "sub_mat": "镇龍锁", "sub_per": 2,
          "progress": [0, 1070, 2160, 2690, 3220, 3760],
          "card_star": 0, "card_extra": 0},
    20: {"name": "蛮牛野", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2,
          "sub_mat": None, "sub_per": 0,
          "progress": [0, 1070, 2160, 2690, 3220, 3760],
          "card_star": 0, "card_extra": 0},
    21: {"name": "城西山", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2,
          "sub_mat": None, "sub_per": 0,
          "progress": [0, 1070, 2160, 2690, 3220, 3760],
          "card_star": 0, "card_extra": 0},
    22: {"name": "城西村", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2,
          "sub_mat": None, "sub_per": 0,
          "progress": [0, 1070, 2160, 2690, 3220, 3760],
          "card_star": 0, "card_extra": 0},
    23: {"name": "轩辕台", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2,
          "sub_mat": "镇龍锁", "sub_per": 2,
          "progress": [0, 1070, 2160, 2690, 3220, 3760],
          "card_star": 0, "card_extra": 0},
    24: {"name": "银明台", "map": "轩辕", "main_mat": "神兽石·日", "main_per": 2,
          "sub_mat": "镇龍锁", "sub_per": 2,
          "progress": [0, 1070, 2160, 2690, 3220, 3760],
          "card_star": 0, "card_extra": 0},
}

# 宝图 → 该宝图下的所有风水点ID列表
MAP_POINTS = {
    "北郡": list(range(1, 7)),
    "琅琊盆地": list(range(7, 13)),
    "昆仑": list(range(13, 19)),
    "轩辕": list(range(19, 25)),
}

# 所有材料名称集合（用于模式二的输入）
ALL_MATERIALS = sorted({
    p["main_mat"] for p in FENG_SHUI_POINTS.values()
} | {
    p["sub_mat"] for p in FENG_SHUI_POINTS.values() if p["sub_mat"]
})


class ToolFengShuiPage(ctk.CTkFrame):
    """风水录养成计算器界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self._build_ui()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # ---- 标题 ----
        ctk.CTkLabel(scroll, text="🏔 风水录养成计算器",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(scroll, text="QQ华夏手游经典区 · 4张宝图 · 24个风水点 · 材料精确计算",
                     font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"], anchor="w"
                     ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # ---- 标签页切换 ----
        tab_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["🎯 目标规划（算材料）", "📊 资源评估（算可达等级）"],
            height=34, font=ctk.CTkFont(size=13),
            selected_color=self.colors["nav_active"],
            unselected_color="#0f0f1a",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("🎯 目标规划（算材料）")

        # ===== Tab 1: 目标规划 =====
        self.tab1 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self._build_tab1()

        # ===== Tab 2: 资源评估 =====
        self.tab2 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self._build_tab2()

        # ---- 说明区域 ----
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(info_inner, text="📖 养成说明", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").pack(fill="x", pady=(0, 8))

        rules = [
            "· 共 4 张宝图：北郡 / 琅琊盆地(180级) / 昆仑(221级) / 轩辕(221级)",
            "· 每张宝图含 6 个风水点，各点独立升级",
            "· 升级消耗 = 进度差 × 每次消耗量 + 卡点额外量（跨越卡点时）",
            "· 北郡各点在 1 星有卡点，需额外消耗主材料才能继续",
            "· 不同宝图的主材料不通用：神兽石 / 缠山图+神兽石·星 / 神兽石·月+寻龍图 / 神兽石·日+镇龍锁",
        ]
        for r in rules:
            ctk.CTkLabel(info_inner, text=r, font=ctk.CTkFont(size=12),
                         text_color=self.colors["text_dim"], anchor="w").pack(fill="x", pady=1)

    # ================================================================
    # Tab 1: 目标规划 — 已知起终点，求材料
    # ================================================================

    def _build_tab1(self):
        inner = ctk.CTkFrame(self.tab1, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        # 选择范围
        ctk.CTkLabel(inner, text="选择范围", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.t1_scope = ctk.CTkOptionMenu(
            inner,
            values=["🗺 整图计算（该宝图全部6个风水点）", "📍 单点查询（选择具体风水点）"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_t1_scope_change,
        )
        self.t1_scope.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t1_scope.set("🗺 整图计算（该宝图全部6个风水点）")

        # 选择宝图
        ctk.CTkLabel(inner, text="选择宝图", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 6))

        self.t1_map_sel = ctk.CTkOptionMenu(
            inner, values=["① 北郡", "② 琅琊盆地", "③ 昆仑", "④ 轩辕"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t1_map_sel.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t1_map_sel.set("① 北郡")

        # 单点选择（默认隐藏）
        self.t1_point_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t1_point_lbl = ctk.CTkLabel(self.t1_point_frame, text="选择风水点",
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         text_color="#ffffff", anchor="w")
        self.t1_point_lbl.pack(anchor="w", pady=(0, 6))
        self.t1_point_sel = ctk.CTkOptionMenu(
            self.t1_point_sel if False else self.t1_point_frame,
            values=[], height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t1_point_sel = ctk.CTkOptionMenu(
            self.t1_point_frame, values=[""], height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t1_point_sel.pack(fill="x")

        # 起始星级
        ctk.CTkLabel(inner, text="起始状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 6))

        ctk.CTkLabel(inner, text="起始星级 (0~5)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]
                     ).grid(row=5, column=0, sticky="w", padx=(0, 8))
        self.t1_start = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_start.grid(row=6, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t1_start.insert(0, "0")

        ctk.CTkLabel(inner, text="目标星级 (0~5)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]
                     ).grid(row=5, column=1, sticky="w", padx=(8, 0))
        self.t1_target = ctk.CTkEntry(inner, placeholder_text="5", height=32, corner_radius=6)
        self.t1_target.grid(row=6, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t1_target.insert(0, "5")

        # 按钮 + 结果
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 8))

        ctk.CTkButton(btn_row, text="▶ 计算所需材料",
                      font=ctk.CTkFont(size=14, weight="bold"), height=40, corner_radius=8,
                      fg_color="#2e7d32", hover_color="#1b5e20",
                      command=self._calc_target).pack(fill="x")

        self.t1_result = ctk.CTkTextbox(inner, height=280, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13))
        self.t1_result.grid(row=8, column=0, columnspan=2, sticky="ew")
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")
        self._bind_mousewheel(self.t1_result)

    def _on_t1_scope_change(self, val):
        if "单点" in val:
            self._refresh_t1_points()
            self.t1_point_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
            self.t1_map_sel.grid_forget()
        else:
            self.t1_point_frame.grid_forget()
            self.t1_map_sel.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

    def _refresh_t1_points(self):
        map_name = self._get_map_name(self.t1_map_sel.get())
        pids = MAP_POINTS.get(map_name, [])
        names = [f"#{pid} {FENG_SHUI_POINTS[pid]['name']}" for pid in pids]
        self.t1_point_sel.configure(values=names if names else [""])
        if names:
            self.t1_point_sel.set(names[0])

    # ================================================================
    # Tab 2: 资源评估 — 已知材料，求可达等级
    # ================================================================

    def _build_tab2(self):
        inner = ctk.CTkFrame(self.tab2, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        # 选择范围
        ctk.CTkLabel(inner, text="选择范围", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.t2_scope = ctk.CTkOptionMenu(
            inner,
            values=["🗺 整图计算（该宝图全部6个风水点）", "📍 单点查询（选择具体风水点）"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_t2_scope_change,
        )
        self.t2_scope.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t2_scope.set("🗺 整图计算（该宝图全部6个风水点）")

        # 选择宝图
        ctk.CTkLabel(inner, text="选择宝图", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 6))

        self.t2_map_sel = ctk.CTkOptionMenu(
            inner, values=["① 北郡", "② 琅琊盆地", "③ 昆仑", "④ 轩辕"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_t2_map_change,
        )
        self.t2_map_sel.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t2_map_sel.set("① 北郡")

        # 单点选择框
        self.t2_point_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t2_point_lbl = ctk.CTkLabel(self.t2_point_frame, text="选择风水点",
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         text_color="#ffffff", anchor="w")
        self.t2_point_lbl.pack(anchor="w", pady=(0, 6))
        self.t2_point_sel = ctk.CTkOptionMenu(
            self.t2_point_frame, values=[""], height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t2_point_sel.pack(fill="x")

        # 当前星级
        ctk.CTkLabel(inner, text="当前星级 (0~5)", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 6))
        self.t2_cur_star = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_cur_star.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t2_cur_star.insert(0, "0")

        # 材料输入（根据宝图动态显示）
        self.t2_mat_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t2_mat_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self._refresh_t2_materials()

        # 按钮 + 结果
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(8, 6))

        ctk.CTkButton(btn_row, text="▶ 计算可达等级",
                      font=ctk.CTkFont(size=14, weight="bold"), height=40, corner_radius=8,
                      fg_color="#0f3460", hover_color="#16213e",
                      command=self._calc_resource).pack(fill="x")

        self.t2_result = ctk.CTkTextbox(inner, height=300, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13))
        self.t2_result.grid(row=8, column=0, columnspan=2, sticky="ew")
        self.t2_result.insert("1.0", "等待计算...\n")
        self.t2_result.configure(state="disabled")
        self._bind_mousewheel(self.t2_result)

    def _on_t2_scope_change(self, val):
        if "单点" in val:
            self._refresh_t2_points()
            self.t2_point_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
            self.t2_map_sel.grid_forget()
        else:
            self.t2_point_frame.grid_forget()
            self.t2_map_sel.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

    def _on_t2_map_change(self, _val=None):
        self._refresh_t2_materials()

    def _refresh_t2_materials(self):
        for w in self.t2_mat_frame.winfo_children():
            w.destroy()
        map_name = self._get_map_name(self.t2_map_sel.get())
        mats = self._get_map_materials(map_name)
        self.t2_mat_entries = {}
        for i, mat_name in enumerate(mats):
            lbl = ctk.CTkLabel(self.t2_mat_frame, text=f"{mat_name}:",
                               font=ctk.CTkFont(size=12),
                               text_color=self.colors["text_dim"])
            lbl.grid(row=i, column=0, sticky="w", pady=(3, 2))
            entry = ctk.CTkEntry(self.t2_mat_frame, placeholder_text="数量",
                                 height=32, corner_radius=6)
            entry.grid(row=i, column=1, sticky="ew", padx=(8, 0), pady=(3, 2))
            self.t2_mat_entries[mat_name] = entry
        self.t2_mat_frame.grid_columnconfigure(1, weight=1)

    def _refresh_t2_points(self):
        map_name = self._get_map_name(self.t2_map_sel.get())
        pids = MAP_POINTS.get(map_name, [])
        names = [f"#{pid} {FENG_SHUI_POINTS[pid]['name']}" for pid in pids]
        self.t2_point_sel.configure(values=names if names else [""])
        if names:
            self.t2_point_sel.set(names[0])

    # ================================================================
    # 标签页切换
    # ================================================================

    def _on_tab_change(self, value):
        if value.startswith("🎯"):
            self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2.grid_forget()
        else:
            self.tab2.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1.grid_forget()

    # ================================================================
    # 辅助方法
    # ================================================================

    @staticmethod
    def _get_map_name(option_str: str) -> str:
        m = {"① 北郡": "北郡", "② 琅琊盆地": "琅琊盆地", "③ 昆仑": "昆仑", "④ 轩辕": "轩辕"}
        return m.get(option_str, "北郡")

    def _get_selected_pids_tab1(self) -> list:
        scope = self.t1_scope.get()
        map_name = self._get_map_name(self.t1_map_sel.get())
        base_ids = MAP_POINTS.get(map_name, [])
        if "单点" in scope:
            sel = self.t1_point_sel.get()
            pid_str = sel.split("#")[1].split()[0] if "#" in sel else ""
            try:
                return [int(pid_str)]
            except ValueError:
                return base_ids
        return base_ids

    def _get_selected_pids_tab2(self) -> list:
        scope = self.t2_scope.get()
        map_name = self._get_map_name(self.t2_map_sel.get())
        base_ids = MAP_POINTS.get(map_name, [])
        if "单点" in scope:
            sel = self.t2_point_sel.get()
            pid_str = sel.split("#")[1].split()[0] if "#" in sel else ""
            try:
                return [int(pid_str)]
            except ValueError:
                return base_ids
        return base_ids

    @staticmethod
    def _get_map_materials(map_name: str) -> list:
        """获取某宝图涉及的所有材料名"""
        pids = MAP_POINTS.get(map_name, [])
        mat_set = set()
        for pid in pids:
            p = FENG_SHUI_POINTS[pid]
            mat_set.add(p["main_mat"])
            if p["sub_mat"]:
                mat_set.add(p["sub_mat"])
        return sorted(mat_set)


    def _show_result(self, tb: ctk.CTkTextbox, text: str):
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.insert("1.0", text)
        tb.configure(state="disabled")

    def _show_error(self, tb: ctk.CTkTextbox, msg: str):
        self._show_result(tb, f"[!] {msg}\n")
    
    def _bind_mousewheel(self, widget):
        """绑定滚轮事件，阻止事件冒泡"""
        def on_mousewheel(event):
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        widget.bind("<Button-4>", lambda e: (widget._parent_canvas.yview_scroll(-1, "units"), "break")[1], add="+")
        widget.bind("<Button-5>", lambda e: (widget._parent_canvas.yview_scroll(1, "units"), "break")[1], add="+")

    @staticmethod
    def _fmt(num: int) -> str:
        return f"{num:,}"

    @staticmethod
    def _parse_int(val: str, default: int) -> int:
        try:
            v = int((val or "").strip())
            return v
        except (ValueError, AttributeError):
            return default

    # ================================================================
    # 核心计算：单个风水点 X星→Y星 的材料消耗
    # ================================================================

    @staticmethod
    def calc_point_cost(pid: int, start_star: int, target_star: int) -> dict:
        """
        计算单个风水点从 start_star 升到 target_star 的材料消耗。
        返回 {"main_mat": str, "main_cost": int, "sub_mat": str|None, "sub_cost": int}
        """
        pt = FENG_SHUI_POINTS[pid]
        prog = pt["progress"]

        delta = prog[target_star] - prog[start_star]
        main_cost = delta * pt["main_per"]
        sub_cost = 0
        if pt["sub_mat"]:
            sub_cost = delta * pt["sub_per"]

        # 卡点额外消耗：如果跨越了卡点星级
        card_extra_main = 0
        cs = pt["card_star"]
        if cs > 0 and start_star < cs <= target_star:
            card_extra_main = pt["card_extra"]

        main_cost += card_extra_main

        return {
            "main_mat": pt["main_mat"],
            "main_cost": main_cost,
            "sub_mat": pt["sub_mat"],
            "sub_cost": sub_cost,
        }

    # ================================================================
    # 模式一：目标规划 — 计算所需材料
    # ================================================================

    def _calc_target(self):
        try:
            pids = self._get_selected_pids_tab1()
            start_s = self._parse_int(self.t1_start.get(), 0)
            target_s = self._parse_int(self.t1_target.get(), 5)

            if not pids:
                self._show_error(self.t1_result, "未找到有效风水点"); return
            if not (0 <= start_s <= 5):
                self._show_error(self.t1_result, "起始星级需在 0~5 之间"); return
            if not (0 <= target_s <= 5):
                self._show_error(self.t1_result, "目标星级需在 0~5 之间"); return
            if target_s <= start_s:
                self._show_error(self.t1_result, "目标星级必须大于起始星级"); return

            # 按材料汇总
            mat_summary = {}  # {material_name: total_count}
            point_details = []

            for pid in pids:
                pt = FENG_SHUI_POINTS[pid]
                cost = self.calc_point_cost(pid, start_s, target_s)
                point_details.append((pt["name"], cost))

                mat_summary[cost["main_mat"]] = mat_summary.get(cost["main_mat"], 0) + cost["main_cost"]
                if cost["sub_mat"] and cost["sub_cost"] > 0:
                    mat_summary[cost["sub_mat"]] = mat_summary.get(cost["sub_mat"], 0) + cost["sub_cost"]

            # 输出结果
            lines = []
            is_single = len(pids) == 1
            if is_single:
                pt0 = FENG_SHUI_POINTS[pids[0]]
                lines.append(f"━━━ 目标规划结果 ━━━\n")
                lines.append(f"风水点：{pt0['name']} ({pt0['map']})")
            else:
                map_name = FENG_SHUI_POINTS[pids[0]]["map"]
                lines.append(f"━━━ 目标规划结果 ━━━\n")
                lines.append(f"宝图：{map_name} · 全部 {len(pids)} 个风水点\n")
            lines.append(f"从 {start_s}星 → {target_s}星\n")

            # 各点明细
            if not is_single:
                lines.append("┌──────────────────────────────────────┐")
                lines.append(f"│ {'风水点':<10} {'主材料':>8} {'副材料':>10} │")
                lines.append("├──────────────────────────────────────┤")
                for name, cost in point_details:
                    main_str = f"{cost['main_cost']:>6,d}"
                    if cost["sub_mat"]:
                        sub_str = f"{cost['sub_cost']:>8,d}"
                    else:
                        sub_str = f"{'无':>8}"
                    lines.append(f"│ {name:<10} {main_str:>8} {sub_str:>10} │")
                lines.append("└──────────────────────────────────────┘\n")

            # 汇总表
            lines.append("━━ 材料汇总 ━━")
            lines.append("┌────────────────────────────┐")
            lines.append(f"│ {'材料':<16} {'数量':>12} │")
            lines.append("├────────────────────────────┤")
            for mat_name in sorted(mat_summary.keys()):
                cnt = mat_summary[mat_name]
                lines.append(f"│ {mat_name:<16} {self._fmt(cnt):>12} │")
            lines.append("└────────────────────────────┘")

            self._show_result(self.t1_result, "\n".join(lines) + "\n")

        except Exception as ex:
            self._show_error(self.t1_result, f"计算出错: {ex}")

    # ================================================================
    # 模式二：资源评估 — 计算可达等级
    # ================================================================

    def _calc_resource(self):
        try:
            pids = self._get_selected_pids_tab2()
            cur_s = self._parse_int(self.t2_cur_star.get(), 0)

            if not pids:
                self._show_error(self.t2_result, "未找到有效风水点"); return
            if not (0 <= cur_s <= 5):
                self._show_error(self.t2_result, "当前星级需在 0~5 之间"); return

            # 解析材料输入
            mat_amounts = {}
            has_input = False
            for mat_name, entry in self.t2_mat_entries.items():
                val_str = entry.get().strip()
                if val_str:
                    try:
                        amt = int(val_str)
                        mat_amounts[mat_name] = amt
                        has_input = True
                    except ValueError:
                        pass

            if not has_input:
                self._show_error(self.t2_result, "请至少输入一种材料的数量！"); return

            lines = []
            is_single = len(pids) == 1

            if is_single:
                pt0 = FENG_SHUI_POINTS[pids[0]]
                lines.append(f"━━━ 资源评估结果 ━━━\n")
                lines.append(f"风水点：{pt0['name']} ({pt0['map']})")
            else:
                map_name = FENG_SHUI_POINTS[pids[0]]["map"]
                lines.append(f"━━━ 资源评估结果 ━━━\n")
                lines.append(f"宝图：{map_name} · 全部 {len(pids)} 个风水点\n")

            # 对每个风水点计算可达等级
            all_results = []
            for pid in pids:
                pt = FENG_SHUI_POINTS[pid]
                result = self._eval_single_point(pid, cur_s, dict(mat_amounts))
                all_results.append((pt["name"], result))

                # 更新剩余材料（整图模式下共享材料池，逐点扣除）
                if not is_single:
                    for mat_name in mat_amounts:
                        mat_amounts[mat_name] -= result.get("used_" + mat_name.replace("·", "_").replace("·", "_").replace("-", "_"), 0)
                        # 用 used 字典更可靠的方式
                    for k, v in result.get("used", {}).items():
                        if k in mat_amounts:
                            mat_amounts[k] -= v

            # 输出
            if is_single:
                name, res = all_results[0]
                lines.append(f"\n▸ 可达等级：{res['reach_star']}星")
                lines.append(f"  从 {cur_s}星 出发\n")
                lines.append("━ 消耗明细 ━")
                if res["used"]:
                    for mat, cnt in res["used"].items():
                        lines.append(f"  {mat}: {self._fmt(cnt)}")
                remain = {}
                for mat, orig in dict(res["original"]).items():
                    consumed = sum(v for k, v in res["used"].items() if k == mat)
                    # 直接用 original 和 used 计算
                # 重算剩余
                orig_mats = res["original"]
                for mn, oc in orig_mats.items():
                    uc = res["used"].get(mn, 0)
                    if oc > uc:
                        if "remain" not in locals():
                            remain = {}
                        remain[mn] = oc - uc
                if remain:
                    lines.append("\n━ 剩余材料 ━")
                    for mn, rc in remain.items():
                        lines.append(f"  {mn}: {self._fmt(rc)}")
            else:
                lines.append(f"从 {cur_s}星 出发（材料共享，按顺序分配）\n")
                lines.append("┌─────────────────────────────────────────────────┐")
                lines.append(f"│ {'风水点':<8} {'可达':>4} {'主材消耗':>10} {'副材消耗':>10} │")
                lines.append("├─────────────────────────────────────────────────┤")
                for name, res in all_results:
                    reach = f"{res['reach_star']}星"
                    main_used = res["used"].get(FENG_SHUI_POINTS[
                        next(pid for pid in pids if FENG_SHUI_POINTS[pid]["name"] == name)]["main_mat"], 0)
                    # 简化显示
                    u_items = list(res["used"].items())
                    main_str = f"{u_items[0][1]:>8,d}" if u_items else f"{'0':>8}"
                    sub_str = f"{u_items[1][1]:>8,d}" if len(u_items) > 1 else f"{'-':>8}"
                    lines.append(f"│ {name:<8} {reach:>4} {main_str:>10} {sub_str:>10} │")
                lines.append("└─────────────────────────────────────────────────┘")

            self._show_result(self.t2_result, "\n".join(lines) + "\n")

        except Exception as ex:
            self._show_error(self.t2_result, f"计算出错: {ex}")

    def _eval_single_point(self, pid: int, cur_star: int, materials: dict) -> dict:
        """
        对单个风水点，根据持有材料计算可达最高星级。
        返回: {"reach_star": int, "used": {mat: count}, "original": {mat: count}}
        """
        pt = FENG_SHUI_POINTS[pid]
        prog = pt["progress"]
        available = dict(materials)  # 复制一份
        original = dict(materials)
        used = {}

        star = cur_star
        while star < 5:
            next_star = star + 1
            cost_info = self.calc_point_cost(pid, star, next_star)

            # 检查主材料是否足够
            main_need = cost_info["main_cost"]
            main_mat = cost_info["main_mat"]
            have_main = available.get(main_mat, 0)

            if have_main < main_need:
                break

            # 检查副材料是否足够
            sub_mat = cost_info["sub_mat"]
            sub_need = cost_info["sub_cost"]
            if sub_mat and sub_need > 0:
                have_sub = available.get(sub_mat, 0)
                if have_sub < sub_need:
                    break

            # 扣除材料
            available[main_mat] = have_main - main_need
            used[main_mat] = used.get(main_mat, 0) + main_need
            if sub_mat and sub_need > 0:
                available[sub_mat] = have_sub - sub_need
                used[sub_mat] = used.get(sub_mat, 0) + sub_need

            star = next_star

        return {"reach_star": star, "used": used, "original": original}
