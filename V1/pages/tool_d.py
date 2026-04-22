"""
星录养成计算器模块
QQ华夏手游经典区 · 星录养成系统计算工具

支持两种计算模式：
  模式一：根据已有材料计算可达到的星录等级
  模式二：根据目标等级计算所需材料（升重石 + 灵运石期望值）

数据来源：星录养成数据_AI版.xlsx
"""

import customtkinter as ctk


# ============================================================
# 一、星录基础信息
# ============================================================
STAR_RECORDS = {
    1: {"name": "太微", "max_weight": 20, "upgrade_stone": "太微升重石", "visible_level": 0,
        "pre_record": None, "pre_weight": 0},
    2: {"name": "紫微", "max_weight": 20, "upgrade_stone": "紫微升重石", "visible_level": 108,
        "pre_record": "太微", "pre_weight": 7},
    3: {"name": "天市", "max_weight": 22, "upgrade_stone": "天市升重石", "visible_level": 220,
        "pre_record": "紫微", "pre_weight": 7},
    4: {"name": "启明", "max_weight": 20, "upgrade_stone": "启明升重石", "visible_level": 260,
        "pre_record": "天市", "pre_weight": 5},
}

STAR_COUNT = 8  # 每部星录8个星官

# ============================================================
# 二、锤炼消耗表（每重每星的期望材料消耗）
# 字段: 重数, 星级, 材料名称, 单次消耗量, 初始概率(%), 期望材料消耗
# 数据来自"锤炼消耗表"，4部星录规则完全相同
# ============================================================
REFINING_DATA = [
    # 重数1 (南明离火)
    {"weight": 1, "star": 1, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 1, "star": 2, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 1, "star": 3, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 1, "star": 4, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 1, "star": 5, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    {"weight": 1, "star": 6, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    # 重数2 (南明离火)
    {"weight": 2, "star": 1, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 2, "star": 2, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 2, "star": 3, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 2, "star": 4, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 2, "star": 5, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    {"weight": 2, "star": 6, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    # 重数3 (南明离火)
    {"weight": 3, "star": 1, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 3, "star": 2, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 3, "star": 3, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 3, "star": 4, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 3, "star": 5, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    {"weight": 3, "star": 6, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    # 重数4 (南明离火)
    {"weight": 4, "star": 1, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 4, "star": 2, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 4, "star": 3, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 4, "star": 4, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 4, "star": 5, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    {"weight": 4, "star": 6, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    # 重数5 (南明离火)
    {"weight": 5, "star": 1, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 5, "star": 2, "material": "南明离火", "consume": 1, "prob": 85, "expected": 1.2},
    {"weight": 5, "star": 3, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 5, "star": 4, "material": "南明离火", "consume": 2, "prob": 75, "expected": 2.7},
    {"weight": 5, "star": 5, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    {"weight": 5, "star": 6, "material": "南明离火", "consume": 3, "prob": 65, "expected": 4.6},
    # 重数6 (南明离火 - 概率突变)
    {"weight": 6, "star": 1, "material": "南明离火", "consume": 10, "prob": 10, "expected": 10.0},
    {"weight": 6, "star": 2, "material": "南明离火", "consume": 10, "prob": 10, "expected": 10.0},
    {"weight": 6, "star": 3, "material": "南明离火", "consume": 25, "prob": 10, "expected": 25.0},
    {"weight": 6, "star": 4, "material": "南明离火", "consume": 25, "prob": 10, "expected": 25.0},
    {"weight": 6, "star": 5, "material": "南明离火", "consume": 50, "prob": 10, "expected": 50.0},
    {"weight": 6, "star": 6, "material": "南明离火", "consume": 50, "prob": 10, "expected": 50.0},
    # 重数7 (南明离火)
    {"weight": 7, "star": 1, "material": "南明离火", "consume": 30, "prob": 10, "expected": 30.0},
    {"weight": 7, "star": 2, "material": "南明离火", "consume": 30, "prob": 10, "expected": 30.0},
    {"weight": 7, "star": 3, "material": "南明离火", "consume": 50, "prob": 10, "expected": 50.0},
    {"weight": 7, "star": 4, "material": "南明离火", "consume": 50, "prob": 10, "expected": 50.0},
    {"weight": 7, "star": 5, "material": "南明离火", "consume": 83.3, "prob": 6, "expected": 83.3},
    {"weight": 7, "star": 6, "material": "南明离火", "consume": 83.3, "prob": 6, "expected": 83.3},
    # 重数8 (南明离火)
    {"weight": 8, "star": 1, "material": "南明离火", "consume": 50, "prob": 10, "expected": 50.0},
    {"weight": 8, "star": 2, "material": "南明离火", "consume": 50, "prob": 10, "expected": 50.0},
    {"weight": 8, "star": 3, "material": "南明离火", "consume": 75, "prob": 8, "expected": 75.0},
    {"weight": 8, "star": 4, "material": "南明离火", "consume": 75, "prob": 8, "expected": 75.0},
    {"weight": 8, "star": 5, "material": "南明离火", "consume": 116.7, "prob": 6, "expected": 116.7},
    {"weight": 8, "star": 6, "material": "南明离火", "consume": 116.7, "prob": 6, "expected": 116.7},
    # 重数9 (南明离火)
    {"weight": 9, "star": 1, "material": "南明离火", "consume": 87.5, "prob": 8, "expected": 87.5},
    {"weight": 9, "star": 2, "material": "南明离火", "consume": 87.5, "prob": 8, "expected": 87.5},
    {"weight": 9, "star": 3, "material": "南明离火", "consume": 133.3, "prob": 6, "expected": 133.3},
    {"weight": 9, "star": 4, "material": "南明离火", "consume": 133.3, "prob": 6, "expected": 133.3},
    {"weight": 9, "star": 5, "material": "南明离火", "consume": 225, "prob": 4.4, "expected": 225.0},
    {"weight": 9, "star": 6, "material": "南明离火", "consume": 225, "prob": 4.4, "expected": 225.0},
    # 重数10 (南明离火)
    {"weight": 10, "star": 1, "material": "南明离火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 10, "star": 2, "material": "南明离火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 10, "star": 3, "material": "南明离火", "consume": 150, "prob": 6.7, "expected": 150.0},
    {"weight": 10, "star": 4, "material": "南明离火", "consume": 150, "prob": 6.7, "expected": 150.0},
    {"weight": 10, "star": 5, "material": "南明离火", "consume": 250, "prob": 4, "expected": 250.0},
    {"weight": 10, "star": 6, "material": "南明离火", "consume": 250, "prob": 4, "expected": 250.0},
    # 重数11 (九幽玄火)
    {"weight": 11, "star": 1, "material": "九幽玄火", "consume": 66.7, "prob": 15, "expected": 66.7},
    {"weight": 11, "star": 2, "material": "九幽玄火", "consume": 66.7, "prob": 15, "expected": 66.7},
    {"weight": 11, "star": 3, "material": "九幽玄火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 11, "star": 4, "material": "九幽玄火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 11, "star": 5, "material": "九幽玄火", "consume": 133.3, "prob": 7.5, "expected": 133.3},
    {"weight": 11, "star": 6, "material": "九幽玄火", "consume": 133.3, "prob": 7.5, "expected": 133.3},
    # 重数12 (九幽玄火)
    {"weight": 12, "star": 1, "material": "九幽玄火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 12, "star": 2, "material": "九幽玄火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 12, "star": 3, "material": "九幽玄火", "consume": 133.3, "prob": 7.5, "expected": 133.3},
    {"weight": 12, "star": 4, "material": "九幽玄火", "consume": 133.3, "prob": 7.5, "expected": 133.3},
    {"weight": 12, "star": 5, "material": "九幽玄火", "consume": 166.7, "prob": 6, "expected": 166.7},
    {"weight": 12, "star": 6, "material": "九幽玄火", "consume": 166.7, "prob": 6, "expected": 166.7},
    # 重数13 (九幽玄火)
    {"weight": 13, "star": 1, "material": "九幽玄火", "consume": 133.3, "prob": 7.5, "expected": 133.3},
    {"weight": 13, "star": 2, "material": "九幽玄火", "consume": 133.3, "prob": 7.5, "expected": 133.3},
    {"weight": 13, "star": 3, "material": "九幽玄火", "consume": 166.7, "prob": 6, "expected": 166.7},
    {"weight": 13, "star": 4, "material": "九幽玄火", "consume": 166.7, "prob": 6, "expected": 166.7},
    {"weight": 13, "star": 5, "material": "九幽玄火", "consume": 200, "prob": 5, "expected": 200.0},
    {"weight": 13, "star": 6, "material": "九幽玄火", "consume": 200, "prob": 5, "expected": 200.0},
    # 重数14 (九幽玄火)
    {"weight": 14, "star": 1, "material": "九幽玄火", "consume": 250, "prob": 4, "expected": 250.0},
    {"weight": 14, "star": 2, "material": "九幽玄火", "consume": 250, "prob": 4, "expected": 250.0},
    {"weight": 14, "star": 3, "material": "九幽玄火", "consume": 300, "prob": 3.3, "expected": 300.0},
    {"weight": 14, "star": 4, "material": "九幽玄火", "consume": 300, "prob": 3.3, "expected": 300.0},
    {"weight": 14, "star": 5, "material": "九幽玄火", "consume": 350, "prob": 2.9, "expected": 350.0},
    {"weight": 14, "star": 6, "material": "九幽玄火", "consume": 350, "prob": 2.9, "expected": 350.0},
    # 重数15 (九幽玄火)
    {"weight": 15, "star": 1, "material": "九幽玄火", "consume": 300, "prob": 3.3, "expected": 300.0},
    {"weight": 15, "star": 2, "material": "九幽玄火", "consume": 300, "prob": 3.3, "expected": 300.0},
    {"weight": 15, "star": 3, "material": "九幽玄火", "consume": 350, "prob": 2.9, "expected": 350.0},
    {"weight": 15, "star": 4, "material": "九幽玄火", "consume": 350, "prob": 2.9, "expected": 350.0},
    {"weight": 15, "star": 5, "material": "九幽玄火", "consume": 400, "prob": 2.5, "expected": 400.0},
    {"weight": 15, "star": 6, "material": "九幽玄火", "consume": 400, "prob": 2.5, "expected": 400.0},
    # 重数16 (红莲业火)
    {"weight": 16, "star": 1, "material": "红莲业火", "consume": 50, "prob": 20, "expected": 50.0},
    {"weight": 16, "star": 2, "material": "红莲业火", "consume": 50, "prob": 20, "expected": 50.0},
    {"weight": 16, "star": 3, "material": "红莲业火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 16, "star": 4, "material": "红莲业火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 16, "star": 5, "material": "红莲业火", "consume": 150, "prob": 6.7, "expected": 150.0},
    {"weight": 16, "star": 6, "material": "红莲业火", "consume": 150, "prob": 6.7, "expected": 150.0},
    # 重数17 (红莲业火)
    {"weight": 17, "star": 1, "material": "红莲业火", "consume": 50, "prob": 20, "expected": 50.0},
    {"weight": 17, "star": 2, "material": "红莲业火", "consume": 50, "prob": 20, "expected": 50.0},
    {"weight": 17, "star": 3, "material": "红莲业火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 17, "star": 4, "material": "红莲业火", "consume": 100, "prob": 10, "expected": 100.0},
    {"weight": 17, "star": 5, "material": "红莲业火", "consume": 200, "prob": 5, "expected": 200.0},
    {"weight": 17, "star": 6, "material": "红莲业火", "consume": 200, "prob": 5, "expected": 200.0},
    # 重数18 (红莲业火)
    {"weight": 18, "star": 1, "material": "红莲业火", "consume": 50, "prob": 20, "expected": 50.0},
    {"weight": 18, "star": 2, "material": "红莲业火", "consume": 50, "prob": 20, "expected": 50.0},
    {"weight": 18, "star": 3, "material": "红莲业火", "consume": 150, "prob": 6.7, "expected": 150.0},
    {"weight": 18, "star": 4, "material": "红莲业火", "consume": 150, "prob": 6.7, "expected": 150.0},
    {"weight": 18, "star": 5, "material": "红莲业火", "consume": 200, "prob": 5, "expected": 200.0},
    {"weight": 18, "star": 6, "material": "红莲业火", "consume": 200, "prob": 5, "expected": 200.0},
    # 重数19 (红莲业火)
    {"weight": 19, "star": 1, "material": "红莲业火", "consume": 200, "prob": 5, "expected": 200.0},
    {"weight": 19, "star": 2, "material": "红莲业火", "consume": 200, "prob": 5, "expected": 200.0},
    {"weight": 19, "star": 3, "material": "红莲业火", "consume": 300, "prob": 3.3, "expected": 300.0},
    {"weight": 19, "star": 4, "material": "红莲业火", "consume": 300, "prob": 3.3, "expected": 300.0},
    {"weight": 19, "star": 5, "material": "红莲业火", "consume": 400, "prob": 2.5, "expected": 400.0},
    {"weight": 19, "star": 6, "material": "红莲业火", "consume": 400, "prob": 2.5, "expected": 400.0},
    # 重数20 (红莲业火)
    {"weight": 20, "star": 1, "material": "红莲业火", "consume": 200, "prob": 5, "expected": 200.0},
    {"weight": 20, "star": 2, "material": "红莲业火", "consume": 200, "prob": 5, "expected": 200.0},
    {"weight": 20, "star": 3, "material": "红莲业火", "consume": 300, "prob": 3.3, "expected": 300.0},
    {"weight": 20, "star": 4, "material": "红莲业火", "consume": 300, "prob": 3.3, "expected": 300.0},
    {"weight": 20, "star": 5, "material": "红莲业火", "consume": 500, "prob": 2, "expected": 500.0},
    {"weight": 20, "star": 6, "material": "红莲业火", "consume": 500, "prob": 2, "expected": 500.0},
]

# ============================================================
# 三、升重石消耗表（单官每重消耗量）
# 升重是确定性的，固定数量
# ============================================================
UPGRADE_STONE_COST = {
    1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 2,
    11: 3, 12: 3, 13: 4, 14: 4, 15: 5, 16: 6, 17: 8, 18: 8, 19: 10, 20: 12,
    21: 15, 22: 20,  # 天市特有到22重
}


class ToolDPage(ctk.CTkFrame):
    """星录养成计算器界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self._build_ui()

    def _build_ui(self):
        """构建界面"""
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # ---- 标题 ----
        ctk.CTkLabel(scroll, text="⭐ 星录养成计算器",
                    font=ctk.CTkFont(size=22, weight="bold"),
                    text_color="#ffffff", anchor="w"
                    ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(scroll, text="QQ华夏手游经典区 · 4部星录 · 8星官/部 · 概率期望值计算",
                    font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"], anchor="w"
                    ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # ---- 标签页切换 ----
        tab_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["📊 根据材料算可达等级", "🎯 根据目标算所需材料"],
            height=34, font=ctk.CTkFont(size=13),
            selected_color=self.colors["nav_active"],
            unselected_color="#0f0f1a",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("📊 根据材料算可达等级")

        # ===== Tab 1: 根据材料计算 =====
        self.tab1 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self._build_tab1()

        # ===== Tab 2: 根据目标计算 =====
        self.tab2 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        # 不 grid，由 tab 切换控制
        self._build_tab2()

        # ---- 说明区域 ----
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(info_inner, text="📖 养成说明", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").pack(fill="x", pady=(0, 8))

        rules = [
            "· 每部星录含 8 个星官，各星官独立养成",
            "· 锤炼(星级)：概率事件，使用灵运石，结果为期望值",
            "· 升重(重数)：确定性事件，消耗固定升重石",
            "· 材料阶段：南明离火(1~10重)→ 九幽玄火(11~15重)→ 红莲业火(16~20重)",
            "· 太微上限20重 | 紫微上限20重 | 天市上限22重 | 启明上限20重",
        ]
        for r in rules:
            ctk.CTkLabel(info_inner, text=r, font=ctk.CTkFont(size=12),
                         text_color=self.colors["text_dim"], anchor="w").pack(fill="x", pady=1)

    # ================================================================
    # Tab 1 UI 构建
    # ================================================================

    def _build_tab1(self):
        inner = ctk.CTkFrame(self.tab1, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        # 星录类型选择
        ctk.CTkLabel(inner, text="选择星录", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.t1_star_type = ctk.CTkOptionMenu(
            inner, values=["① 太微星录", "② 紫微星录", "③ 天市星录", "④ 启明星录"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t1_star_type.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.t1_star_type.set("① 太微星录")

        # 当前状态
        ctk.CTkLabel(inner, text="当前状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 6))

        ctk.CTkLabel(inner, text="当前重数 (1~20/22)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=3, column=0, sticky="w", padx=(0, 8))
        self.t1_cur_weight = ctk.CTkEntry(inner, placeholder_text="1", height=32, corner_radius=6)
        self.t1_cur_weight.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t1_cur_weight.insert(0, "1")

        ctk.CTkLabel(inner, text="当前星级 (0~6)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=3, column=1, sticky="w", padx=(8, 0))
        self.t1_cur_star = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_cur_star.grid(row=4, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t1_cur_star.insert(0, "0")

        # 拥有材料
        ctk.CTkLabel(inner, text="拥有材料", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 6))

        for i, mat in enumerate(["南明离火", "九幽玄火", "红莲业火"]):
            ctk.CTkLabel(inner, text=f"{mat}:", font=ctk.CTkFont(size=12),
                         text_color=self.colors["text_dim"]).grid(
                row=6 + i, column=0, sticky="w", pady=(3, 2))
            entry = ctk.CTkEntry(inner, placeholder_text="留空=无限", height=32, corner_radius=6)
            entry.grid(row=6 + i, column=1, sticky="ew", padx=(8, 0), pady=(3, 2))

        self.t1_mats = {}
        self.t1_mats["南明"] = inner.winfo_children()[-3] if len(inner.winfo_children()) >= 3 else None
        self.t1_mats["九幽"] = inner.winfo_children()[-2] if len(inner.winfo_children()) >= 2 else None
        self.t1_mats["红莲"] = inner.winfo_children()[-1] if len(inner.winfo_children()) >= 1 else None

        # 用变量保存引用
        self.t1_mat_nanming = None
        self.t1_mat_jiuyou = None
        self.t_mat_honglian = None

        # 重新获取引用
        children = inner.winfo_children()
        idx = 0
        for child in children:
            if isinstance(child, ctk.CTkEntry):
                if self.t1_mat_nanming is None:
                    self.t1_mat_nanming = child
                elif self.t1_mat_jiuyou is None:
                    self.t1_mat_jiuyou = child
                else:
                    self.t_mat_honglian = child

        # 升重石
        ctk.CTkLabel(inner, text="升重石:", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(
            row=9, column=0, sticky="w", pady=(3, 2))
        self.t1_upgrade_stone = ctk.CTkEntry(inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_upgrade_stone.grid(row=9, column=1, sticky="ew", padx=(8, 0), pady=(3, 2))

        # 按钮 + 结果
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(10, 8))

        ctk.CTkButton(btn_row, text="▶ 计算可达到的等级",
                      font=ctk.CTkFont(size=14, weight="bold"), height=40, corner_radius=8,
                      fg_color="#0f3460", hover_color="#16213e",
                      command=self._calc_by_materials).pack(fill="x")

        self.t1_result = ctk.CTkTextbox(inner, height=220, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13))
        self.t1_result.grid(row=11, column=0, columnspan=2, sticky="ew")
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")

    # ================================================================
    # Tab 2 UI 构建
    # ================================================================

    def _build_tab2(self):
        inner = ctk.CTkFrame(self.tab2, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        # 星录类型
        ctk.CTkLabel(inner, text="选择星录", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.t2_star_type = ctk.CTkOptionMenu(
            inner, values=["① 太微星录", "② 紫微星录", "③ 天市星录", "④ 启明星录"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t2_star_type.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.t2_star_type.set("① 太微星录")

        # 起始状态
        ctk.CTkLabel(inner, text="起始状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 6))

        ctk.CTkLabel(inner, text="起始重数", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=3, column=0, sticky="w", padx=(0, 8))
        self.t2_start_w = ctk.CTkEntry(inner, placeholder_text="1", height=32, corner_radius=6)
        self.t2_start_w.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t2_start_w.insert(0, "1")

        ctk.CTkLabel(inner, text="起始星级", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=3, column=1, sticky="w", padx=(8, 0))
        self.t2_start_s = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_start_s.grid(row=4, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t2_start_s.insert(0, "0")

        # 目标状态
        ctk.CTkLabel(inner, text="目标状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(8, 6))

        ctk.CTkLabel(inner, text="目标重数", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=6, column=0, sticky="w", padx=(0, 8))
        self.t2_target_w = ctk.CTkEntry(inner, placeholder_text="20", height=32, corner_radius=6)
        self.t2_target_w.grid(row=7, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t2_target_w.insert(0, "20")

        ctk.CTkLabel(inner, text="目标星级", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=6, column=1, sticky="w", padx=(8, 0))
        self.t2_target_s = ctk.CTkEntry(inner, placeholder_text="6", height=32, corner_radius=6)
        self.t2_target_s.grid(row=7, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t2_target_s.insert(0, "6")

        # 按钮 + 结果
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(10, 8))

        ctk.CTkButton(btn_row, text="▶ 计算所需材料",
                      font=ctk.CTkFont(size=14, weight="bold"), height=40, corner_radius=8,
                      fg_color="#2e7d32", hover_color="#1b5e20",
                      command=self._calc_for_target).pack(fill="x")

        self.t2_result = ctk.CTkTextbox(inner, height=280, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13))
        self.t2_result.grid(row=9, column=0, columnspan=2, sticky="ew")
        self.t2_result.insert("1.0", "等待计算...\n")
        self.t2_result.configure(state="disabled")

    # ================================================================
    # 标签页切换
    # ================================================================

    def _on_tab_change(self, value):
        if value == "📊 根据材料算可达等级":
            self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2.grid_forget()
        else:
            self.tab2.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1.grid_forget()

    # ================================================================
    # 辅助方法
    # ================================================================

    def _get_record_id(self, option_str: str) -> int:
        _MAP = {"① 太微星录": 1, "② 紫微星录": 2, "③ 天市星录": 3, "④ 启明星录": 4}
        return _MAP.get(option_str, 1)

    def _show_result(self, tb: ctk.CTkTextbox, text: str):
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.insert("1.0", text)
        tb.configure(state="disabled")

    def _show_error(self, tb: ctk.CTkTextbox, msg: str):
        self._show_result(tb, f"⚠ {msg}\n")

    def _fmt(self, num: float) -> str:
        """格式化数字"""
        if num >= 10000: return f"{num:,.0f}"
        if num >= 100: return f"{num:,.1f}"
        if num >= 1: return f"{num:,.2f}"
        return f"{num:.3f}"

    def _parse_int(self, val: str, default: int) -> int:
        try: return int((val or "").strip() or str(default))
        except: return default

    def _parse_float_or_inf(self, val: str) -> float:
        v = val.strip()
        if not v: return float("inf")
        try: return float(v)
        except: return float("inf")

    def _get_refining_entry(self, weight: int) -> list:
        """获取某重数的所有星级数据"""
        return [r for r in REFINING_DATA if r["weight"] == weight]

    def _get_max_weight(self, record_id: int) -> int:
        return STAR_RECORDS[record_id]["max_weight"]

    # ================================================================
    # 模式一：根据材料计算可达等级
    # ================================================================

    def _calc_by_materials(self):
        try:
            rid = self._get_record_id(self.t1_star_type.get())
            cur_w = self._parse_int(self.t1_cur_weight.get(), 1)
            cur_s = self._parse_int(self.t1_cur_star.get(), 0)

            max_w = self._get_max_weight(rid)
            nanming = self._parse_float_or_inf(self.t1_mat_nanming.get())
            jiuyou = self._parse_float_or_inf(self.t1_mat_jiuyou.get())
            honglian = self._parse_float_or_inf(self.t_mat_honglian.get())
            upgrade = self._parse_float_or_inf(self.t1_upgrade_stone.get())

            if nanming == float("inf") and jiuyou == float("inf") and honglian == float("inf") and upgrade == float("inf"):
                self._show_error(self.t1_result, "请至少输入一种材料的数量！")
                return
            if cur_w < 1 or cur_w > max_w:
                self._show_error(self.t1_result, f"重数需在 1 ~ {max_w} 之间")
                return
            if cur_s < 0 or cur_s > 6:
                self._show_error(self.t1_result, "星级需在 0 ~ 6 之间")
                return

            # 开始模拟
            w, s = cur_w, cur_s
            total_nanming = 0.0
            total_jiuyou = 0.0
            total_honglian = 0.0
            total_upgrade = 0.0
            steps = 0

            try:
                while w <= max_w:
                    # 先打完当前重数的剩余星级 (从cur_s+1 到 6)
                    start_star = s + 1 if s < 6 else 99
                    if start_star <= 6:
                        entries = [r for r in REFINING_DATA if r["weight"] == w]
                        for star in range(start_star, 7):
                            match = next((e for e in entries if e["star"] == star), None)
                            if not match:
                                break
                            cost = match["expected"]
                            mat = match["material"]

                            can_afford = False
                            if mat == "南明离火" and nanming >= cost:
                                nanming -= cost; total_nanming += cost; can_afford = True
                            elif mat == "九幽玄火" and jiuyou >= cost:
                                jiuyou -= cost; total_jiuyou += cost; can_afford = True
                            elif mat == "红莲业火" and honglian >= cost:
                                honglian -= cost; total_honglian += cost; can_afford = True

                            if not can_afford:
                                s = star - 1
                                raise StopIteration
                            s = star
                            steps += 1

                    # 尝试升重
                    if w >= max_w:
                        break
                    u_cost = UPGRADE_STONE_COST.get(w + 1, 30)
                    if upgrade < u_cost:
                        raise StopIteration
                    upgrade -= u_cost
                    total_upgrade += u_cost
                    w += 1
                    s = 0

            except StopIteration:
                pass

            lines = []
            sr = STAR_RECORDS[rid]
            lines.append(f"━━━ 养成模拟结果 ━━━\n")
            lines.append(f"星录：{sr['name']}星录 (最大{sr['max_weight']}重)")
            lines.append(f"\n▸ 可达等级：{w}重{s}星")
            lines.append(f"  从 {cur_w}重{cur_s}星 出发，共推进 {steps} 个星级步骤\n")

            lines.append("━ 累计材料消耗 ━")
            if total_nanming > 0: lines.append(f"  南明离火: {self._fmt(total_nanming)}")
            if total_jiuyou > 0: lines.append(f"  九幽玄火: {self._fmt(total_jiuyou)}")
            if total_honglian > 0: lines.append(f"  红莲业火: {self._fmt(total_honglian)}")
            lines.append(f"  {sr['upgrade_stone']}: {self._fmt(total_upgrade)}")
            lines.append(f"\n(以上为单星官认为值 × 8星官)")

            self._show_result(self.t1_result, "\n".join(lines) + "\n")

            # 剩余提示
            remain_lines = []
            if nanming != float("inf") and nanming > 0:
                remain_lines.append(f"  剩余南明: {self._fmt(nanming)}")
            if jiuyou != float("inf") and jiuyou > 0:
                remain_lines.append(f"  剩余九幽: {self._fmt(jiuyou)}")
            if honglian != float("inf") and honglian > 0:
                remain_lines.append(f"  剩余红莲: {self._fmt(honglian)}")
            if upgrade != float("inf") and upgrade > 0:
                remain_lines.append(f"  剩余升重石: {self._fmt(upgrade)}")
            if remain_lines:
                old = self.t1_result.get("1.0", "end").strip()
                self._show_result(self.t1_result, old + "\n" + "\n".join(remain_lines) + "\n")

        except Exception as ex:
            self._show_error(self.t1_result, f"计算出错: {ex}")

    # ================================================================
    # 模式二：根据目标计算所需材料
    # ================================================================

    def _calc_for_target(self):
        try:
            rid = self._get_record_id(self.t2_star_type.get())
            start_w = self._parse_int(self.t2_start_w.get(), 1)
            start_s = self._parse_int(self.t2_start_s.get(), 0)
            target_w = self._parse_int(self.t2_target_w.get(), 20)
            target_s = self._parse_int(self.t2_target_s.get(), 6)

            max_w = self._get_max_weight(rid)

            if start_w < 1 or start_w > max_w:
                self._show_error(self.t2_result, f"起始重数需在 1 ~ {max_w}")
                return
            if target_w < 1 or target_w > max_w:
                self._show_error(self.t2_result, f"目标重数需在 1 ~ {max_w}")
                return
            if start_s < 0 or start_s > 6:
                self._show_error(self.t2_result, "起始星级 0~6"); return
            if target_s < 0 or target_s > 6:
                self._show_error(self.t2_result, "目标星级 0~6"); return
            if (target_w < start_w) or (target_w == start_w and target_s <= start_s):
                self._show_error(self.t2_result, "目标必须大于起始"); return

            # 累加材料
            tot_n = 0.0  # 南明
            tot_j = 0.0  # 九幽
            tot_h = 0.0  # 红莲
            tot_u = 0.0  # 升重石

            cw, cs = start_w, start_s

            while True:
                # 打完当前重剩余星级
                for star in range(cs + 1, 7):
                    match = next((r for r in REFINING_DATA if r["weight"] == cw and r["star"] == star), None)
                    if match:
                        exp = match["expected"]
                        mat = match["material"]
                        if mat == "南明离火": tot_n += exp
                        elif mat == "九幽玄火": tot_j += exp
                        elif mat == "红莲业火": tot_h += exp
                    cs = star

                if cw == target_w and cs >= target_s:
                    break
                if cw >= target_w:
                    break

                # 升重
                cw += 1
                cs = 0
                tot_u += UPGRADE_STONE_COST.get(cw, 30)

            # 输出
            lines = []
            sr = STAR_RECORDS[rid]
            lines.append(f"━━━ 所需材料 ━━━\n")
            lines.append(f"星录：{sr['name']}星录")
            lines.append(f"从 {start_w}重{start_s}星 → {target_w}重{target_s}星\n")
            lines.append("┌──────────────────────────────┐")
            lines.append(f"│ {'材料':<14} {'单星官':>10} {'×8星官':>10} │")
            lines.append("├──────────────────────────────┤")
            lines.append(f"│ 南明离火{'':<8}{self._fmt(tot_n):>10} {self._fmt(tot_n * 8):>10} │")
            lines.append(f"│ 九幽玄火{'':<8}{self._fmt(tot_j):>10} {self._fmt(tot_j * 8):>10} │")
            lines.append(f"│ 红莲业火{'':<8}{self._fmt(tot_h):>10} {self._fmt(tot_h * 8):>10} │")
            lines.append(f"│ {sr['upgrade_stone']}{'':<8}{self._fmt(tot_u):>10} {self._fmt(tot_u * 8):>10} │")
            lines.append("└──────────────────────────────┘")
            lines.append("\n⚠ 灵运石为期望值，实际可能 ±20% 浮动")

            self._show_result(self.t2_result, "\n".join(lines) + "\n")

        except Exception as ex:
            self._show_error(self.t2_result, f"计算出错: {ex}")
