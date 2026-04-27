"""
守护神养成计算器
以请神符为核心货币，支持两种计算模式：
1. 持有请神符 → 可升到哪个星级
2. 目标星级 → 需要多少请神符
"""

import math
import customtkinter as ctk


class ToolGuardian(ctk.CTkFrame):
    """守护神养成计算器"""

    # ── 星级消耗表 ──
    # 升级段 -> 消耗残念数
    STAR_COST = {
        0: 20,   # 0→1星
        1: 40,   # 1→2星
        2: 80,   # 2→3星
        3: 160,  # 3→4星
        4: 0,    # 4→5星(供奉自动解锁)
    }
    # 累计消耗 (从0星到N星)
    STAR_CUM = {0: 0, 1: 20, 2: 60, 3: 140, 4: 300, 5: 300}

    # ── 神仙谱组配置 ──
    # 每组: (组名, 请神符名, 保底幸运值, [(守护神名, 品质, 精华单价, 出货权重), ...])
    GROUPS = [
        ("四值功曹", "功曹请神符", 6000, [
            ("值时功曹", "蓝(2)", 2, 40),
            ("值日功曹", "蓝绿(3)", 4, 25),
            ("值月功曹", "蓝绿(3)", 4, 25),
            ("值年功曹", "紫(4)", 60, 10),
        ]),
        ("日直六星", "日直六星请神符", 6000, [
            ("显道神", "蓝(2)", 4, 20),
            ("开路神", "蓝(2)", 4, 20),
            ("增福神", "蓝绿(3)", 8, 15),
            ("损福神", "蓝绿(3)", 8, 15),
            ("日游神", "紫(4)", 80, 5),
            ("夜游神", "紫(4)", 80, 5),
        ]),
        ("九歌地神", "九歌地神请神符", 6000, [
            ("河伯", "蓝(2)", 8, 35),
            ("山鬼", "蓝绿(3)", 16, 25),
            ("湘夫人", "紫(4)", 240, 5),
            ("湘君", "紫(4)", 240, 5),
        ]),
        ("云海天神", "云海天神请神符", 7000, [
            ("地安神", "蓝(2)", 32, 35),
            ("天时神", "蓝绿(3)", 64, 25),
            ("阴光神", "紫(4)", 999, 5),
            ("阳炁神", "紫(4)", 999, 5),
        ]),
        ("五德真君", "五德真君请神符", 8000, [
            ("地侯星君", "蓝(2)", 64, 30),
            ("重华星君", "蓝绿(3)", 128, 20),
            ("伺辰星君", "蓝绿(3)", 128, 20),
            ("荧惑星君", "紫(4)", 2000, 5),
            ("太白星君", "金(5)", 4000, 2),
        ]),
        ("天元九歌", "天元九歌请神符", 10000, [
            ("大司命", "蓝(2)", 640, 30),
            ("云中君", "蓝绿(3)", 1280, 20),
            ("东君", "紫(4)", 20000, 5),
            ("少司命", "紫(4)", 20000, 5),
        ]),
    ]

    # 品质颜色映射
    QUALITY_COLORS = {
        "蓝(2)": "#4a9eff",
        "蓝绿(3)": "#00bfa5",
        "紫(4)": "#ab47bc",
        "金(5)": "#ffa000",
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
    #  UI 构建
    # ================================================================
    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # 标题
        ctk.CTkLabel(
            scroll, text="🛡️ 守护神养成计算器",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        ctk.CTkLabel(
            scroll,
            text="6大神仙谱组 · 请神符→残念→星级 · 精华转化路径",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"], anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # 标签页切换
        tab_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["📦 请神符 → 可达星级", "🎯 目标星级 → 所需请神符"],
            height=34, font=ctk.CTkFont(size=13),
            selected_color=self.colors.get("nav_active", "#0f3460"),
            unselected_color="#0f0f1a",
            selected_hover_color="#164080",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("📦 请神符 → 可达星级")

        # ── Tab 1: 请神符 → 可达星级 ──
        self.tab1_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self._build_tab1()

        # ── Tab 2: 目标星级 → 所需请神符 ──
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
            "• 模式1：输入当前星级 + 持有请神符数量 → 计算可升到几星",
            "• 模式2：输入当前星级 + 目标星级 → 计算所需请神符数量",
            "",
            "核心机制：每次请神消耗1张请神符，若重复出货→获得10个残念",
            "星级消耗：0→1★(20) → 1→2★(40) → 2→3★(80) → 3→4★(160) → 4→5★(供奉解锁)",
            "精华路径：多余低品质残念→转化精华→购买高品质残念（推荐高品质守护神使用）",
            "出货权重：蓝色~20-40%，蓝绿~15-25%，紫色~5%，金色~2%",
        ]
        for rule in rules:
            ctk.CTkLabel(
                info_inner, text=rule,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"], anchor="w",
            ).pack(fill="x", pady=1)

    # ────────────────────────────────────────────────
    #  Tab 1 : 请神符 → 可达星级
    # ────────────────────────────────────────────────
    def _build_tab1(self):
        inner = ctk.CTkFrame(self.tab1_frame, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        row = 0
        ctk.CTkLabel(
            inner, text="选择神仙谱组",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 8))
        row += 1

        # 谱组选择
        ctk.CTkLabel(inner, text="神仙谱组",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        row += 1

        group_names = [g[0] for g in self.GROUPS]
        self.t1_group_var = ctk.StringVar(value=group_names[0])
        self.t1_group_menu = ctk.CTkOptionMenu(
            inner, variable=self.t1_group_var,
            values=group_names, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
            command=self._on_group_change_t1,
        )
        self.t1_group_menu.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        row += 1

        # 动态生成每个守护神的输入区域
        self.t1_guardian_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t1_guardian_frame.grid(row=row, column=0, columnspan=2, sticky="ew")
        row += 1

        # 持有请神符数量
        ctk.CTkLabel(
            inner, text="持有请神符数量",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(12, 3))
        row += 1

        self.t1_ticket_label = ctk.CTkLabel(
            inner, text="功曹请神符:",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text"], anchor="w")
        self.t1_ticket_label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t1_ticket_entry = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_ticket_entry.insert(0, "0")
        self.t1_ticket_entry.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        row += 1

        # 持有精华(可选)
        ctk.CTkLabel(inner, text="持有残念精华（可选）",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        row += 1

        self.t1_essence_entry = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_essence_entry.insert(0, "0")
        self.t1_essence_entry.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        row += 1

        # 计算按钮
        ctk.CTkButton(
            inner, text="▶  计算可达星级",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#0f3460", hover_color="#16213e",
            command=self._calc_mode1,
        ).grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        row += 1

        # 结果区域
        self.t1_result = ctk.CTkTextbox(
            inner, height=280, corner_radius=8,
            fg_color="#0f0f1a",
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=12),
        )
        self.t1_result.grid(row=row, column=0, columnspan=2, sticky="ew")
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")
        self._bind_mousewheel(self.t1_result)

        # 初始化守护神输入
        self.t1_star_vars = {}  # {守护神名: StringVar}
        self.t1_remnant_vars = {}  # {守护神名: StringVar} 直接持有残念
        self._refresh_guardian_inputs_t1()

    def _refresh_guardian_inputs_t1(self):
        """根据当前谱组刷新 Tab1 守护神输入区"""
        for w in self.t1_guardian_frame.winfo_children():
            w.destroy()
        self.t1_star_vars.clear()
        self.t1_remnant_vars.clear()

        group = self._current_group(self.t1_group_var.get())
        if not group:
            return

        _, _, _, guardians = group
        self.t1_ticket_label.configure(text=f"{group[1]}:")

        frame = self.t1_guardian_frame
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # 表头
        headers = ["守护神", "品质", "当前星级", "持有残念(可选)"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(frame, text=h, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color="#aaaaaa").grid(row=0, column=i, padx=4, pady=(0, 4), sticky="w")

        for idx, (name, quality, price, weight) in enumerate(guardians):
            r = idx + 1
            color = self.QUALITY_COLORS.get(quality, "#ffffff")

            ctk.CTkLabel(frame, text=name, font=ctk.CTkFont(size=12),
                         text_color=color).grid(row=r, column=0, padx=4, pady=2, sticky="w")
            ctk.CTkLabel(frame, text=quality, font=ctk.CTkFont(size=11),
                         text_color=color).grid(row=r, column=1, padx=4, pady=2, sticky="w")

            star_var = ctk.StringVar(value="0")
            self.t1_star_vars[name] = star_var
            ctk.CTkOptionMenu(
                frame, variable=star_var,
                values=["0", "1", "2", "3", "4", "5"],
                width=70, height=28, corner_radius=6,
                fg_color="#0f3460", button_color="#0f3460",
                button_hover_color="#16213e",
            ).grid(row=r, column=2, padx=4, pady=2, sticky="w")

            rem_var = ctk.StringVar(value="0")
            self.t1_remnant_vars[name] = rem_var
            ctk.CTkEntry(frame, textvariable=rem_var, width=80, height=28,
                         corner_radius=6, fg_color="#0f0f1a").grid(
                row=r, column=3, padx=4, pady=2, sticky="w")

    # ────────────────────────────────────────────────
    #  Tab 2 : 目标星级 → 所需请神符
    # ────────────────────────────────────────────────
    def _build_tab2(self):
        inner = ctk.CTkFrame(self.tab2_frame, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        row = 0
        # 选择守护神
        ctk.CTkLabel(
            inner, text="选择守护神",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 8))
        row += 1

        # 谱组选择
        ctk.CTkLabel(inner, text="神仙谱组",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        ctk.CTkLabel(inner, text="守护神",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        row += 1

        group_names = [g[0] for g in self.GROUPS]
        self.t2_group_var = ctk.StringVar(value=group_names[0])
        ctk.CTkOptionMenu(
            inner, variable=self.t2_group_var,
            values=group_names, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
            command=self._on_group_change_t2,
        ).grid(row=row, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

        first_group = self.GROUPS[0]
        guardian_names = [g[0] for g in first_group[3]]
        self.t2_guardian_var = ctk.StringVar(value=guardian_names[0])
        self.t2_guardian_menu = ctk.CTkOptionMenu(
            inner, variable=self.t2_guardian_var,
            values=guardian_names, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t2_guardian_menu.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        row += 1

        # 当前/目标星级
        ctk.CTkLabel(
            inner, text="星级设置",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 8))
        row += 1

        ctk.CTkLabel(inner, text="当前星级",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        ctk.CTkLabel(inner, text="目标星级",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        row += 1

        self.t2_cur_star_var = ctk.StringVar(value="0")
        ctk.CTkOptionMenu(
            inner, variable=self.t2_cur_star_var,
            values=["0", "1", "2", "3", "4"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        ).grid(row=row, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

        self.t2_tgt_star_var = ctk.StringVar(value="5")
        ctk.CTkOptionMenu(
            inner, variable=self.t2_tgt_star_var,
            values=["1", "2", "3", "4", "5"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        ).grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        row += 1

        # 直接持有残念(可选)
        ctk.CTkLabel(inner, text="直接持有残念（可选）",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        row += 1

        self.t2_remnant_entry = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_remnant_entry.insert(0, "0")
        self.t2_remnant_entry.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        row += 1

        # 计算按钮
        ctk.CTkButton(
            inner, text="▶  计算所需请神符",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#2e7d32", hover_color="#1b5e20",
            command=self._calc_mode2,
        ).grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        row += 1

        # 结果
        self.t2_result = ctk.CTkTextbox(
            inner, height=320, corner_radius=8,
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
        if value == "📦 请神符 → 可达星级":
            self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2_frame.grid_forget()
        else:
            self.tab2_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1_frame.grid_forget()

    def _on_group_change_t1(self, _value):
        self._refresh_guardian_inputs_t1()

    def _on_group_change_t2(self, _value):
        group = self._current_group(self.t2_group_var.get())
        if group:
            names = [g[0] for g in group[3]]
            self.t2_guardian_menu.configure(values=names)
            self.t2_guardian_var.set(names[0])

    # ================================================================
    #  工具方法
    # ================================================================
    def _current_group(self, group_name):
        for g in self.GROUPS:
            if g[0] == group_name:
                return g
        return None

    def _find_guardian(self, guardian_name):
        """查找守护神信息: (name, quality, price, weight, group_tuple)"""
        for g in self.GROUPS:
            for gd in g[3]:
                if gd[0] == guardian_name:
                    return (*gd, g)
        return None

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
    #  模式1 计算: 请神符 → 可达星级
    # ================================================================
    def _calc_mode1(self):
        group = self._current_group(self.t1_group_var.get())
        if not group:
            self._show_error(self.t1_result, "请选择有效的神仙谱组")
            return

        group_name, ticket_name, pity, guardians = group

        # 读取请神符数量
        try:
            tickets = int(self.t1_ticket_entry.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的请神符数量")
            return
        if tickets < 0:
            self._show_error(self.t1_result, "请神符数量不能为负")
            return

        # 读取持有精华
        try:
            owned_essence = int(self.t1_essence_entry.get() or "0")
        except ValueError:
            owned_essence = 0

        # 读取各守护神当前星级与持有残念
        guardian_info = []
        for name, quality, price, weight in guardians:
            try:
                star = int(self.t1_star_vars.get(name, ctk.StringVar(value="0")).get())
            except ValueError:
                star = 0
            try:
                remnant = int(self.t1_remnant_vars.get(name, ctk.StringVar(value="0")).get())
            except ValueError:
                remnant = 0
            guardian_info.append({
                'name': name,
                'quality': quality,
                'price': price,
                'weight': weight,
                'star': min(max(star, 0), 5),
                'remnant': max(remnant, 0),
            })

        # 检查：如果全部已5星且无符
        if all(g['star'] >= 5 for g in guardian_info) and tickets == 0:
            self._show_error(self.t1_result, "所有守护神已满5星，无需计算")
            return

        # ---- 计算 ----
        # 总权重
        total_weight = sum(g['weight'] for g in guardian_info)

        # 请神出货分配：按权重比例分配期望出货次数
        # 每次请神消耗1张符，若已有该守护神 → 10残念（重复出货）
        # 简化：假设第一次出货不给残念(获取守护神)，后续全部给残念
        output = f"✅ 计算完成\n\n"
        output += f"{'='*50}\n"
        output += f"神仙谱组: {group_name}\n"
        output += f"使用请神符: {ticket_name} × {tickets}\n"
        output += f"持有残念精华: {owned_essence}\n"
        output += f"{'='*50}\n\n"

        # 步骤1: 分配出货
        output += "【步骤1: 请神出货分配（按权重期望值）】\n"
        for g in guardian_info:
            prob = g['weight'] / total_weight
            expected_pulls = tickets * prob
            # 如果当前0星 → 第1次出货是获取守护神(不给残念)，后续才给残念
            if g['star'] == 0:
                repeat_pulls = max(0, expected_pulls - 1)
            else:
                repeat_pulls = expected_pulls  # 已拥有，所有出货都给残念
            gained_remnant = int(repeat_pulls) * 10
            g['gained_remnant'] = gained_remnant
            g['expected_pulls'] = expected_pulls

            output += f"  {g['name']}({g['quality']}): "
            output += f"权重{g['weight']}% → 期望{expected_pulls:.1f}次出货 → "
            output += f"获得 {gained_remnant} 残念\n"

        # 步骤2: 精华来源计算
        output += f"\n{'='*50}\n"
        output += "【步骤2: 精华来源】\n"

        total_excess_essence = owned_essence
        for g in guardian_info:
            # 该守护神到5星需要多少残念
            need_to_5 = max(0, self.STAR_CUM[5] - self.STAR_CUM[g['star']])
            total_have = g['remnant'] + g['gained_remnant']
            excess = max(0, total_have - need_to_5)
            if excess > 0:
                essence_from = excess * g['price']
                total_excess_essence += essence_from
                output += f"  {g['name']}: 多余残念 {excess} × {g['price']}精华/个 = {essence_from} 精华\n"
            g['excess'] = excess
            g['total_have'] = total_have

        output += f"  总可用精华: {total_excess_essence}\n"

        # 步骤3: 精华购买高品质残念
        output += f"\n{'='*50}\n"
        output += "【步骤3: 精华兑换高品质残念（优先购买精华单价高的）】\n"

        remaining_essence = total_excess_essence
        # 按精华单价从高到低排序，优先补贴高品质
        sorted_guardians = sorted(guardian_info, key=lambda x: x['price'], reverse=True)
        for g in sorted_guardians:
            need_to_5 = max(0, self.STAR_CUM[5] - self.STAR_CUM[g['star']])
            already_have = min(g['total_have'], need_to_5)  # 不超过5星所需
            shortfall = need_to_5 - already_have
            if shortfall > 0 and remaining_essence > 0 and g['price'] > 0:
                can_buy = remaining_essence // g['price']
                buy = min(can_buy, shortfall)
                cost = buy * g['price']
                remaining_essence -= cost
                g['bought_remnant'] = buy
                if buy > 0:
                    output += f"  购买 {g['name']}残念: {buy}个 (花费 {cost} 精华)\n"
            else:
                g['bought_remnant'] = 0

        output += f"  剩余精华: {remaining_essence}\n"

        # 步骤4: 计算最终可达星级
        output += f"\n{'='*50}\n"
        output += "【最终结果: 各守护神可达星级】\n\n"

        for g in guardian_info:
            total_remnant = g['remnant'] + g['gained_remnant'] + g.get('bought_remnant', 0)
            # 扣除多余部分(已计入精华的)
            if g['excess'] > 0:
                usable = total_remnant - g['excess']
            else:
                usable = total_remnant

            # 从当前星级逐级升星
            cur_star = g['star']
            remaining = usable
            while cur_star < 5:
                need = self.STAR_COST.get(cur_star, 0)
                if need == 0:
                    cur_star += 1  # 4→5星免费
                    continue
                if remaining >= need:
                    remaining -= need
                    cur_star += 1
                else:
                    break

            star_str = "⭐" * cur_star + "☆" * (5 - cur_star)
            color_name = self.QUALITY_COLORS.get(g['quality'], '')
            result_line = f"  {g['name']}({g['quality']}): {star_str} ({cur_star}星)"
            if cur_star < 5:
                next_need = self.STAR_COST.get(cur_star, 0)
                result_line += f"  [剩余{remaining}残念, 下一星还需{next_need}]"
            else:
                result_line += f"  ✅ 满星! 剩余{remaining}残念"
            output += result_line + "\n"

        # 建议
        output += f"\n{'='*50}\n"
        output += "【建议】\n"
        has_purple = any(g['quality'] in ("紫(4)", "金(5)") for g in guardian_info)
        if has_purple:
            output += "  💡 高品质(紫/金)守护神建议主要通过精华路径培养\n"
            output += "     用低品质谱组大量请神 → 产出多余残念 → 转化精华 → 购买高品质残念\n"

        self._show_result(self.t1_result, output)

    # ================================================================
    #  模式2 计算: 目标星级 → 所需请神符
    # ================================================================
    def _calc_mode2(self):
        guardian_name = self.t2_guardian_var.get()
        info = self._find_guardian(guardian_name)
        if not info:
            self._show_error(self.t2_result, "未找到该守护神信息")
            return

        name, quality, price, weight, group = info
        group_name, ticket_name, pity, guardians = group
        total_weight = sum(g[3] for g in guardians)

        try:
            cur_star = int(self.t2_cur_star_var.get())
            tgt_star = int(self.t2_tgt_star_var.get())
        except ValueError:
            self._show_error(self.t2_result, "请选择有效星级")
            return

        if tgt_star <= cur_star:
            self._show_error(self.t2_result, "目标星级必须大于当前星级")
            return

        try:
            owned_remnant = int(self.t2_remnant_entry.get() or "0")
        except ValueError:
            owned_remnant = 0

        # 计算残念缺口
        need_total = self.STAR_CUM[tgt_star] - self.STAR_CUM[cur_star]
        gap = max(0, need_total - owned_remnant)

        output = f"✅ 计算完成\n\n"
        output += f"{'='*50}\n"
        output += f"守护神: {name} ({quality})\n"
        output += f"神仙谱组: {group_name}\n"
        output += f"目标: {cur_star}★ → {tgt_star}★\n"
        output += f"{'='*50}\n\n"

        # 残念需求明细
        output += "【残念需求明细】\n"
        for s in range(cur_star, min(tgt_star, 4)):
            cost = self.STAR_COST[s]
            output += f"  {s}★ → {s+1}★: {cost} 残念\n"
        if tgt_star == 5:
            output += f"  4★ → 5★: 0 残念 (供奉自动解锁)\n"
        output += f"\n  总计需要: {need_total} 残念\n"
        output += f"  已持有残念: {owned_remnant}\n"
        output += f"  残念缺口: {gap}\n"

        if gap == 0:
            output += f"\n🎉 你已持有足够残念，无需额外请神符！\n"
            self._show_result(self.t2_result, output)
            return

        # 方案A: 纯请神路径
        output += f"\n{'='*50}\n"
        output += "【方案A: 纯请神路径】\n"
        repeat_needed = math.ceil(gap / 10)  # 每次重复出货10残念
        prob = weight / total_weight
        if prob > 0:
            tickets_a = math.ceil(repeat_needed / prob)
        else:
            tickets_a = float('inf')

        output += f"  需重复出货次数: {repeat_needed} (缺口{gap} ÷ 10)\n"
        output += f"  该守护神出货概率: {prob*100:.1f}%\n"
        output += f"  需要请神符: 约 {tickets_a:,} 张 {ticket_name}\n"

        if prob < 0.1:
            output += f"  ⚠️ 出货概率极低，纯请神路径效率极差！\n"

        # 方案B: 精华转化路径
        output += f"\n{'='*50}\n"
        output += "【方案B: 精华转化路径（推荐）】\n"
        essence_needed = gap * price
        output += f"  残念缺口: {gap} × 精华单价{price}/个 = {essence_needed:,} 精华\n\n"

        # 用最低价的残念来产精华（值时功曹，2精华/个）
        base_price = 2  # 值时功曹残念精华单价
        base_remnant_needed = math.ceil(essence_needed / base_price)
        base_repeat = math.ceil(base_remnant_needed / 10)
        # 值时功曹出货率约40%（在功曹组内）
        base_prob = 0.40
        base_tickets = math.ceil(base_repeat / base_prob)

        output += f"  推荐精华来源: 值时功曹残念 (最低精华单价: {base_price}/个)\n"
        output += f"  所需值时功曹残念: {base_remnant_needed:,} 个\n"
        output += f"  所需功曹请神符: 约 {base_tickets:,} 张\n"
        output += f"    (重复出货{base_repeat:,}次 ÷ 约40%出货率)\n"

        # 对比
        output += f"\n{'='*50}\n"
        output += "【方案对比】\n"
        output += f"  方案A ({ticket_name}): 约 {tickets_a:,} 张\n"
        output += f"  方案B (功曹请神符): 约 {base_tickets:,} 张\n"

        if tickets_a != float('inf') and base_tickets < tickets_a:
            savings = tickets_a - base_tickets
            output += f"\n  💡 方案B更优! 节省约 {savings:,} 张请神符\n"
            output += f"     且方案B还能同时提升功曹组其他守护神星级\n"
        elif quality in ("紫(4)", "金(5)"):
            output += f"\n  💡 高品质守护神强烈推荐方案B (精华路径)\n"
            output += f"     纯请神路径出货率极低，效率远不如精华转化\n"

        self._show_result(self.t2_result, output)
