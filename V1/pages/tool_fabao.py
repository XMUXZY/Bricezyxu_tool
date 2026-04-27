"""
法宝升阶养成计算器
支持两种模式：
1. 材料→进度：输入当前阶数 + 持有碎片/第二材料 → 可达阶数及剩余
2. 目标→材料：输入当前阶数 + 目标阶数 → 所需碎片 + 所需第二材料
"""

import customtkinter as ctk


class ToolFaBao(ctk.CTkFrame):
    """法宝升阶养成计算器"""

    # ── 四象阵/八卦两仪阵 碎片消耗表（index=阶数, value=该阶→下阶碎片消耗） ──
    SIXIANG_COST = [
        1, 1, 1, 1, 1,         # 0~4
        2, 2, 2, 2, 2,         # 5~9
        3, 3, 3, 3, 3,         # 10~14
        4, 4, 4, 4, 4,         # 15~19
        5, 5, 5, 5, 5,         # 20~24
        6, 6, 6, 6, 6,         # 25~29
        7, 7, 7, 7, 7,         # 30~34
        8, 8, 8, 8, 8,         # 35~39
        10, 10, 10, 10, 10,    # 40~44
        12, 12, 12, 12, 12,    # 45~49
        15, 15, 15, 15, 15,    # 50~54
        18, 18, 18, 18, 18,    # 55~59
        20, 20, 20, 20, 20,    # 60~64
        22, 22, 22, 22, 22,    # 65~69
        25, 25, 25, 25, 25,    # 70~74
        30, 30, 30, 30, 30,    # 75~79
        30, 35, 35, 35, 35,    # 80~84
        40, 40, 40, 40, 40,    # 85~89
        40, 45, 45, 45, 45,    # 90~94
        50, 50, 50, 50, 50,    # 95~99
    ]

    # ── 三才阵/归藏阵 碎片消耗表 ──
    SANCAI_CHIP_COST = [
        1, 1, 1, 1, 1,         # 0~4
        2, 2, 2, 2, 2,         # 5~9
        3, 3, 3, 3, 3,         # 10~14
        4, 4, 4, 4, 4,         # 15~19
        4, 4, 4, 4, 4,         # 20~24
        5, 5, 5, 5, 5,         # 25~29
        6, 6, 6, 6, 6,         # 30~34
        7, 7, 7, 7, 7,         # 35~39
        8, 8, 8, 8, 8,         # 40~44
        10, 10, 10, 10, 10,    # 45~49
        12, 12, 12, 12, 12,    # 50~54
        15, 15, 15, 15, 15,    # 55~59
        16, 16, 16, 16, 16,    # 60~64
        18, 18, 18, 18, 18,    # 65~69
        20, 20, 20, 20, 20,    # 70~74
        24, 24, 24, 24, 24,    # 75~79
        24, 28, 28, 28, 28,    # 80~84
        32, 32, 32, 32, 32,    # 85~89
        32, 36, 36, 36, 36,    # 90~94
        36, 40, 40, 40, 40,    # 95~99
    ]

    # ── 三才阵/归藏阵 第二材料消耗表 ──
    SANCAI_MAT2_COST = [
        0, 0, 0, 0, 0,         # 0~4
        0, 0, 0, 0, 0,         # 5~9
        0, 0, 0, 0, 0,         # 10~14
        0, 0, 0, 0, 0,         # 15~19
        1, 1, 1, 1, 1,         # 20~24
        1, 1, 1, 1, 1,         # 25~29
        1, 1, 1, 1, 1,         # 30~34
        1, 1, 1, 1, 1,         # 35~39
        2, 2, 2, 2, 2,         # 40~44
        2, 2, 2, 2, 2,         # 45~49
        3, 3, 3, 3, 3,         # 50~54
        3, 3, 3, 3, 3,         # 55~59
        4, 4, 4, 4, 4,         # 60~64
        4, 4, 4, 4, 4,         # 65~69
        5, 5, 5, 5, 5,         # 70~74
        6, 6, 6, 6, 6,         # 75~79
        6, 7, 7, 7, 7,         # 80~84
        8, 8, 8, 8, 8,         # 85~89
        8, 9, 9, 9, 9,         # 90~94
        9, 10, 10, 10, 10,     # 95~99
    ]

    # ── 法宝信息表 ──
    # (法宝名, 档次, 法阵类型, 碎片名, 第二材料名/None)
    FABAO_LIST = [
        # 四象阵 - 凡
        ("打神鞭", "凡", "四象阵", "打神鞭碎片", None),
        ("斩仙刀", "凡", "四象阵", "斩仙刀碎片", None),
        ("轩辕剑", "凡", "四象阵", "轩辕剑碎片", None),
        ("伏羲琴", "凡", "四象阵", "伏羲琴碎片", None),
        ("玄天伞", "凡", "四象阵", "玄天伞碎片", None),
        ("遮天幡", "凡", "四象阵", "遮天幡碎片", None),
        ("混沌钟", "凡", "四象阵", "混沌钟碎片", None),
        ("玉清瓶", "凡", "四象阵", "玉清瓶碎片", None),
        ("乾坤圈", "凡", "四象阵", "乾坤圈碎片", None),
        ("翻天印", "凡", "四象阵", "翻天印碎片", None),
        ("盘古斧", "凡", "四象阵", "盘古斧碎片", None),
        ("昊天塔", "凡", "四象阵", "昊天塔碎片", None),
        # 四象阵 - 尊
        ("打神鞭", "尊", "四象阵", "打神鞭碎片", None),
        ("斩仙刀", "尊", "四象阵", "斩仙刀碎片", None),
        ("轩辕剑", "尊", "四象阵", "轩辕剑碎片", None),
        ("伏羲琴", "尊", "四象阵", "伏羲琴碎片", None),
        ("玄天伞", "尊", "四象阵", "玄天伞碎片", None),
        ("遮天幡", "尊", "四象阵", "遮天幡碎片", None),
        ("混沌钟", "尊", "四象阵", "混沌钟碎片", None),
        ("玉清瓶", "尊", "四象阵", "玉清瓶碎片", None),
        ("乾坤圈", "尊", "四象阵", "乾坤圈碎片", None),
        ("翻天印", "尊", "四象阵", "翻天印碎片", None),
        ("盘古斧", "尊", "四象阵", "盘古斧碎片", None),
        ("昊天塔", "尊", "四象阵", "昊天塔碎片", None),
        # 四象阵 - 仙
        ("打神鞭", "仙", "四象阵", "打神鞭碎片", None),
        ("斩仙刀", "仙", "四象阵", "斩仙刀碎片", None),
        ("轩辕剑", "仙", "四象阵", "轩辕剑碎片", None),
        ("伏羲琴", "仙", "四象阵", "伏羲琴碎片", None),
        ("玄天伞", "仙", "四象阵", "玄天伞碎片", None),
        ("遮天幡", "仙", "四象阵", "遮天幡碎片", None),
        ("混沌钟", "仙", "四象阵", "混沌钟碎片", None),
        ("玉清瓶", "仙", "四象阵", "玉清瓶碎片", None),
        ("乾坤圈", "仙", "四象阵", "乾坤圈碎片", None),
        ("翻天印", "仙", "四象阵", "翻天印碎片", None),
        ("盘古斧", "仙", "四象阵", "盘古斧碎片", None),
        ("昊天塔", "仙", "四象阵", "昊天塔碎片", None),
        # 八卦两仪阵
        ("紫阳锤", "凡", "八卦两仪阵", "紫阳锤碎片", None),
        ("玄阴索", "凡", "八卦两仪阵", "玄阴索碎片", None),
        # 三才阵
        ("天禹剑", "凡", "三才阵", "天禹剑碎片", "血叶金"),
        ("地脉罩", "凡", "三才阵", "地脉罩碎片", "碧落断魂"),
        ("人皇山", "凡", "三才阵", "人皇山碎片", "通天柏"),
        # 归藏阵
        ("天衍卦", "凡", "归藏阵", "天衍卦碎片", "灵羲石"),
        ("玄冥网", "凡", "归藏阵", "玄冥网碎片", "玄冰丝"),
        ("五行石", "凡", "归藏阵", "五行石碎片", "娲皇焱"),
        ("造化芦", "凡", "归藏阵", "造化芦碎片", "青玉藤"),
    ]

    # 法阵类型分组映射
    FORMATION_TYPES = {
        "四象阵": "SIXIANG",
        "八卦两仪阵": "SIXIANG",
        "三才阵": "SANCAI",
        "归藏阵": "SANCAI",
    }

    # 法阵颜色映射
    FORMATION_COLORS = {
        "四象阵": "#e94560",
        "八卦两仪阵": "#ab47bc",
        "三才阵": "#00bfa5",
        "归藏阵": "#ffa000",
    }

    def __init__(self, parent, colors=None):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors or {
            "text": "#ffffff",
            "text_dim": "#888888",
            "nav_active": "#0f3460",
        }
        self._build_ui()

    # ================================================================
    #  数据查询方法
    # ================================================================
    def _get_cost_tables(self, formation_type):
        """根据法阵类型获取消耗表"""
        data_set = self.FORMATION_TYPES.get(formation_type, "SIXIANG")
        if data_set == "SANCAI":
            return self.SANCAI_CHIP_COST, self.SANCAI_MAT2_COST
        else:
            return self.SIXIANG_COST, [0] * 100

    def _has_mat2(self, formation_type):
        """该法阵类型是否有第二材料"""
        return formation_type in ("三才阵", "归藏阵")

    def _get_fabao_display_name(self, fabao):
        """获取法宝的显示名称"""
        name, grade, formation, chip_name, mat2_name = fabao
        if grade != "凡" and formation == "四象阵":
            return f"{name}({grade})"
        return name

    def _get_fabao_by_formation(self, formation_type):
        """按法阵类型获取法宝列表"""
        return [f for f in self.FABAO_LIST if f[2] == formation_type]

    # ================================================================
    #  UI 构建
    # ================================================================
    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # 标题
        ctk.CTkLabel(
            scroll, text="🏺 法宝升阶计算器",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        ctk.CTkLabel(
            scroll,
            text="四象阵 · 八卦两仪阵 · 三才阵 · 归藏阵 · 0~100阶升阶材料计算",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"], anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # 标签页切换
        tab_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["📦 材料 → 可达阶数", "🎯 目标阶数 → 所需材料"],
            height=34, font=ctk.CTkFont(size=13),
            selected_color=self.colors.get("nav_active", "#0f3460"),
            unselected_color="#0f0f1a",
            selected_hover_color="#164080",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("📦 材料 → 可达阶数")

        # ── Tab 1: 材料 → 可达阶数 ──
        self.tab1_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self._build_tab1()

        # ── Tab 2: 目标阶数 → 所需材料 ──
        self.tab2_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self._build_tab2()

        # ── 使用说明 ──
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            info_inner, text="📖 使用说明",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).pack(fill="x", pady=(0, 8))

        rules = [
            "• 模式1：输入法宝 + 当前阶数 + 持有材料数 → 计算可升到几阶及剩余",
            "• 模式2：输入法宝 + 当前阶数 + 目标阶数 → 计算所需碎片和第二材料",
            "",
            "核心机制：",
            "  - 升阶成功率 100%，无失败风险，材料消耗确定",
            "  - 碎片消耗按阶数分段递增，每5阶为一档",
            "  - 四象阵/八卦两仪阵：全程只消耗法宝专属碎片（满阶共需 1,780 碎片）",
            "  - 三才阵/归藏阵：0~19阶仅碎片，20阶起同时消耗第二材料（满阶共需 1,443 碎片 + 332 第二材料）",
            "",
            "法阵分类：",
            "  - 四象阵（110级）：打神鞭/斩仙刀/轩辕剑等12种（凡/尊/仙三档）",
            "  - 八卦两仪阵（170级）：紫阳锤/玄阴索",
            "  - 三才阵（240级）：天禹剑/地脉罩/人皇山",
            "  - 归藏阵（331级）：天衍卦/玄冥网/五行石/造化芦",
        ]
        for rule in rules:
            ctk.CTkLabel(
                info_inner, text=rule,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"], anchor="w",
            ).pack(fill="x", pady=1)

    # ────────────────────────────────────────────────
    #  Tab 1 : 材料 → 可达阶数
    # ────────────────────────────────────────────────
    def _build_tab1(self):
        inner = ctk.CTkFrame(self.tab1_frame, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        row = 0
        ctk.CTkLabel(
            inner, text="选择法宝",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 8))
        row += 1

        # 法阵类型选择
        ctk.CTkLabel(inner, text="法阵类型",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        ctk.CTkLabel(inner, text="法宝名称",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        row += 1

        formation_types = ["四象阵", "八卦两仪阵", "三才阵", "归藏阵"]
        self.t1_formation_var = ctk.StringVar(value=formation_types[0])
        ctk.CTkOptionMenu(
            inner, variable=self.t1_formation_var,
            values=formation_types, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
            command=self._on_formation_change_t1,
        ).grid(row=row, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

        # 法宝名称选择
        first_fabaos = self._get_fabao_by_formation("四象阵")
        fabao_names = [self._get_fabao_display_name(f) for f in first_fabaos]
        self.t1_fabao_var = ctk.StringVar(value=fabao_names[0])
        self.t1_fabao_menu = ctk.CTkOptionMenu(
            inner, variable=self.t1_fabao_var,
            values=fabao_names, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t1_fabao_menu.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        row += 1

        # 当前阶数
        ctk.CTkLabel(
            inner, text="当前阶数",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 3))
        row += 1

        ctk.CTkLabel(inner, text="输入当前阶数（0~99）",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        row += 1

        self.t1_cur_level = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_cur_level.insert(0, "0")
        self.t1_cur_level.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        row += 1

        # 持有碎片数量
        ctk.CTkLabel(
            inner, text="持有材料",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 3))
        row += 1

        ctk.CTkLabel(inner, text="持有碎片数量",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t1_mat2_label = ctk.CTkLabel(
            inner, text="持有第二材料数量",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"], anchor="w")
        self.t1_mat2_label.grid(row=row, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        row += 1

        self.t1_chip_entry = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_chip_entry.insert(0, "0")
        self.t1_chip_entry.grid(row=row, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))

        self.t1_mat2_entry = ctk.CTkEntry(inner, placeholder_text="0（不适用可留空）", height=32, corner_radius=6)
        self.t1_mat2_entry.insert(0, "0")
        self.t1_mat2_entry.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=(0, 12))
        row += 1

        # 计算按钮
        ctk.CTkButton(
            inner, text="▶  计算可达阶数",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#0f3460", hover_color="#16213e",
            command=self._calc_mode1,
        ).grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        row += 1

        # 结果区域
        self.t1_result = ctk.CTkTextbox(
            inner, height=300, corner_radius=8,
            fg_color="#0f0f1a",
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=12),
        )
        self.t1_result.grid(row=row, column=0, columnspan=2, sticky="ew")
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")
        self._bind_mousewheel(self.t1_result)

        # 初始化第二材料显示
        self._update_mat2_visibility_t1()

    # ────────────────────────────────────────────────
    #  Tab 2 : 目标阶数 → 所需材料
    # ────────────────────────────────────────────────
    def _build_tab2(self):
        inner = ctk.CTkFrame(self.tab2_frame, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        row = 0
        ctk.CTkLabel(
            inner, text="选择法宝",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 8))
        row += 1

        # 法阵类型选择
        ctk.CTkLabel(inner, text="法阵类型",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        ctk.CTkLabel(inner, text="法宝名称",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        row += 1

        formation_types = ["四象阵", "八卦两仪阵", "三才阵", "归藏阵"]
        self.t2_formation_var = ctk.StringVar(value=formation_types[0])
        ctk.CTkOptionMenu(
            inner, variable=self.t2_formation_var,
            values=formation_types, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
            command=self._on_formation_change_t2,
        ).grid(row=row, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

        first_fabaos = self._get_fabao_by_formation("四象阵")
        fabao_names = [self._get_fabao_display_name(f) for f in first_fabaos]
        self.t2_fabao_var = ctk.StringVar(value=fabao_names[0])
        self.t2_fabao_menu = ctk.CTkOptionMenu(
            inner, variable=self.t2_fabao_var,
            values=fabao_names, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t2_fabao_menu.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        row += 1

        # 阶数设置
        ctk.CTkLabel(
            inner, text="阶数设置",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 3))
        row += 1

        ctk.CTkLabel(inner, text="当前阶数（0~99）",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        ctk.CTkLabel(inner, text="目标阶数（1~100）",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        row += 1

        self.t2_cur_level = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_cur_level.insert(0, "0")
        self.t2_cur_level.grid(row=row, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

        self.t2_tgt_level = ctk.CTkEntry(inner, placeholder_text="100", height=32, corner_radius=6)
        self.t2_tgt_level.insert(0, "100")
        self.t2_tgt_level.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        row += 1

        # 计算按钮
        ctk.CTkButton(
            inner, text="▶  计算所需材料",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#2e7d32", hover_color="#1b5e20",
            command=self._calc_mode2,
        ).grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        row += 1

        # 结果区域
        self.t2_result = ctk.CTkTextbox(
            inner, height=300, corner_radius=8,
            fg_color="#0f0f1a",
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=12),
        )
        self.t2_result.grid(row=row, column=0, columnspan=2, sticky="ew")
        self.t2_result.insert("1.0", "等待计算...\n")
        self.t2_result.configure(state="disabled")
        self._bind_mousewheel(self.t2_result)

    # ================================================================
    #  事件回调
    # ================================================================
    def _on_tab_change(self, value):
        if value == "📦 材料 → 可达阶数":
            self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2_frame.grid_forget()
        else:
            self.tab2_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1_frame.grid_forget()

    def _on_formation_change_t1(self, _value):
        formation = self.t1_formation_var.get()
        fabaos = self._get_fabao_by_formation(formation)
        names = [self._get_fabao_display_name(f) for f in fabaos]
        self.t1_fabao_menu.configure(values=names)
        self.t1_fabao_var.set(names[0])
        self._update_mat2_visibility_t1()

    def _on_formation_change_t2(self, _value):
        formation = self.t2_formation_var.get()
        fabaos = self._get_fabao_by_formation(formation)
        names = [self._get_fabao_display_name(f) for f in fabaos]
        self.t2_fabao_menu.configure(values=names)
        self.t2_fabao_var.set(names[0])

    def _update_mat2_visibility_t1(self):
        """更新Tab1第二材料输入的可见性提示"""
        formation = self.t1_formation_var.get()
        if self._has_mat2(formation):
            # 获取当前选中法宝的第二材料名
            fabao = self._find_fabao_t1()
            if fabao and fabao[4]:
                self.t1_mat2_label.configure(text=f"持有{fabao[4]}数量", text_color=self.colors["text_dim"])
            else:
                self.t1_mat2_label.configure(text="持有第二材料数量", text_color=self.colors["text_dim"])
            self.t1_mat2_entry.configure(state="normal", placeholder_text="0")
        else:
            self.t1_mat2_label.configure(text="第二材料（不适用）", text_color="#555555")
            self.t1_mat2_entry.delete(0, "end")
            self.t1_mat2_entry.insert(0, "0")
            self.t1_mat2_entry.configure(state="disabled")

    def _find_fabao_t1(self):
        """查找Tab1当前选中的法宝数据"""
        formation = self.t1_formation_var.get()
        display_name = self.t1_fabao_var.get()
        for f in self._get_fabao_by_formation(formation):
            if self._get_fabao_display_name(f) == display_name:
                return f
        return None

    def _find_fabao_t2(self):
        """查找Tab2当前选中的法宝数据"""
        formation = self.t2_formation_var.get()
        display_name = self.t2_fabao_var.get()
        for f in self._get_fabao_by_formation(formation):
            if self._get_fabao_display_name(f) == display_name:
                return f
        return None

    # ================================================================
    #  工具方法
    # ================================================================
    def _show_result(self, textbox, text):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")

    def _show_error(self, textbox, msg):
        self._show_result(textbox, f"⚠️ {msg}\n")

    def _bind_mousewheel(self, widget):
        def on_mousewheel(event):
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        widget.bind("<Button-4>", lambda e: (widget._parent_canvas.yview_scroll(-1, "units"), "break")[1], add="+")
        widget.bind("<Button-5>", lambda e: (widget._parent_canvas.yview_scroll(1, "units"), "break")[1], add="+")

    # ================================================================
    #  模式1 计算: 材料 → 可达阶数
    # ================================================================
    def _calc_mode1(self):
        fabao = self._find_fabao_t1()
        if not fabao:
            self._show_error(self.t1_result, "请选择有效的法宝")
            return

        name, grade, formation, chip_name, mat2_name = fabao

        # 读取输入
        try:
            cur_level = int(self.t1_cur_level.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的当前阶数")
            return
        if cur_level < 0 or cur_level > 99:
            self._show_error(self.t1_result, "当前阶数范围 0~99")
            return

        try:
            owned_chips = int(self.t1_chip_entry.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的碎片数量")
            return
        if owned_chips < 0:
            self._show_error(self.t1_result, "碎片数量不能为负")
            return

        try:
            owned_mat2 = int(self.t1_mat2_entry.get() or "0")
        except ValueError:
            owned_mat2 = 0

        has_m2 = self._has_mat2(formation)
        chip_cost_table, mat2_cost_table = self._get_cost_tables(formation)

        display_name = self._get_fabao_display_name(fabao)

        # 逐阶模拟
        remaining_chips = owned_chips
        remaining_mat2 = owned_mat2
        reach_level = cur_level
        table_data = []
        stop_reason = ""

        for lv in range(cur_level, 100):
            c_cost = chip_cost_table[lv]
            m_cost = mat2_cost_table[lv] if has_m2 else 0

            # 检查碎片是否足够
            if remaining_chips < c_cost:
                stop_reason = f"碎片不足（需{c_cost}，剩余{remaining_chips}）"
                break
            # 检查第二材料是否足够
            if has_m2 and m_cost > 0 and remaining_mat2 < m_cost:
                stop_reason = f"{mat2_name}不足（需{m_cost}，剩余{remaining_mat2}）"
                break

            remaining_chips -= c_cost
            if has_m2 and m_cost > 0:
                remaining_mat2 -= m_cost
            reach_level = lv + 1

            # 记录表格数据
            if has_m2:
                table_data.append([
                    f"{lv}阶→{lv+1}阶",
                    f"{c_cost}",
                    f"{m_cost}" if m_cost > 0 else "—",
                    f"{remaining_chips}",
                    f"{remaining_mat2}" if m_cost > 0 or lv >= 19 else "—",
                ])
            else:
                table_data.append([
                    f"{lv}阶→{lv+1}阶",
                    f"{c_cost}",
                    f"{remaining_chips}",
                ])

        # 构建文本结果
        output = f"✅ 计算完成\n\n"
        output += f"{'='*50}\n"
        output += f"法宝: {display_name}（{formation}）\n"
        output += f"碎片: {chip_name}\n"
        if has_m2 and mat2_name:
            output += f"第二材料: {mat2_name}\n"
        output += f"{'='*50}\n\n"

        output += f"📊 起始阶数: {cur_level}阶\n"
        output += f"📊 投入碎片: {owned_chips:,} 个\n"
        if has_m2:
            output += f"📊 投入{mat2_name}: {owned_mat2:,} 个\n"

        output += f"\n{'='*50}\n"
        output += f"🏆 可升至: {reach_level}阶\n"
        output += f"📈 共提升: {reach_level - cur_level} 阶\n"
        output += f"💎 剩余碎片: {remaining_chips:,} 个\n"
        if has_m2:
            output += f"💎 剩余{mat2_name}: {remaining_mat2:,} 个\n"

        if reach_level >= 100:
            output += f"\n🎉 恭喜! 已满阶（100阶）!\n"
        else:
            output += f"\n⏸ 停止原因: {stop_reason}\n"
            # 显示到下阶还需多少
            next_chip = chip_cost_table[reach_level]
            next_mat2 = mat2_cost_table[reach_level] if has_m2 else 0
            chip_gap = max(0, next_chip - remaining_chips)
            output += f"\n📋 下一阶({reach_level}→{reach_level+1}): 需碎片 {next_chip}"
            if chip_gap > 0:
                output += f"（还差 {chip_gap}）"
            if has_m2 and next_mat2 > 0:
                mat2_gap = max(0, next_mat2 - remaining_mat2)
                output += f"，需{mat2_name} {next_mat2}"
                if mat2_gap > 0:
                    output += f"（还差 {mat2_gap}）"
            output += "\n"

        self._show_result(self.t1_result, output)

    # ================================================================
    #  模式2 计算: 目标阶数 → 所需材料
    # ================================================================
    def _calc_mode2(self):
        fabao = self._find_fabao_t2()
        if not fabao:
            self._show_error(self.t2_result, "请选择有效的法宝")
            return

        name, grade, formation, chip_name, mat2_name = fabao

        try:
            cur_level = int(self.t2_cur_level.get() or "0")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的当前阶数")
            return
        try:
            tgt_level = int(self.t2_tgt_level.get() or "100")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的目标阶数")
            return

        if cur_level < 0 or cur_level > 99:
            self._show_error(self.t2_result, "当前阶数范围 0~99")
            return
        if tgt_level < 1 or tgt_level > 100:
            self._show_error(self.t2_result, "目标阶数范围 1~100")
            return
        if tgt_level <= cur_level:
            self._show_error(self.t2_result, "目标阶数必须大于当前阶数")
            return

        has_m2 = self._has_mat2(formation)
        chip_cost_table, mat2_cost_table = self._get_cost_tables(formation)
        display_name = self._get_fabao_display_name(fabao)

        # 逐阶累加
        total_chips = 0
        total_mat2 = 0
        table_data = []
        cum_chips = 0
        cum_mat2 = 0

        for lv in range(cur_level, tgt_level):
            c_cost = chip_cost_table[lv]
            m_cost = mat2_cost_table[lv] if has_m2 else 0
            total_chips += c_cost
            total_mat2 += m_cost
            cum_chips += c_cost
            cum_mat2 += m_cost

            if has_m2:
                table_data.append([
                    f"{lv}阶→{lv+1}阶",
                    f"{c_cost}",
                    f"{m_cost}" if m_cost > 0 else "—",
                    f"{cum_chips:,}",
                    f"{cum_mat2}" if cum_mat2 > 0 else "—",
                ])
            else:
                table_data.append([
                    f"{lv}阶→{lv+1}阶",
                    f"{c_cost}",
                    f"{cum_chips:,}",
                ])

        # 构建文本结果
        output = f"✅ 计算完成\n\n"
        output += f"{'='*50}\n"
        output += f"法宝: {display_name}（{formation}）\n"
        output += f"碎片: {chip_name}\n"
        if has_m2 and mat2_name:
            output += f"第二材料: {mat2_name}\n"
        output += f"目标: {cur_level}阶 → {tgt_level}阶\n"
        output += f"{'='*50}\n\n"

        output += f"📊 共需升阶: {tgt_level - cur_level} 次\n\n"

        # 分段汇总
        output += f"【分段消耗明细】\n"
        seg_start = cur_level
        while seg_start < tgt_level:
            seg_end = min(((seg_start // 5) + 1) * 5, tgt_level)
            seg_chips = sum(chip_cost_table[lv] for lv in range(seg_start, seg_end))
            seg_mat2 = sum(mat2_cost_table[lv] for lv in range(seg_start, seg_end)) if has_m2 else 0
            line = f"  {seg_start}~{seg_end-1}阶: 碎片 {seg_chips}"
            if has_m2 and seg_mat2 > 0:
                line += f" + {mat2_name} {seg_mat2}"
            output += line + "\n"
            seg_start = seg_end

        output += f"\n{'='*50}\n"
        output += f"🏆 所需材料总计:\n"
        output += f"  💎 {chip_name}: {total_chips:,} 个\n"
        if has_m2:
            output += f"  💎 {mat2_name}: {total_mat2:,} 个\n"
            if total_mat2 == 0:
                output += f"  ℹ️ 该阶数段不消耗第二材料\n"

        self._show_result(self.t2_result, output)
