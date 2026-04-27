"""
宝石磨砺养成计算器模块
QQ华夏手游经典区 · 宝石磨砺养成系统计算工具

支持两种计算模式：
  模式一：根据已有材料计算可达到的磨砺等级（含期望值）
  模式二：根据目标等级计算所需材料（确定消耗 + 考虑失败的期望值）

数据来源：宝石磨砺养成计算数据_经典区.xlsx · AI计算数据_机器可读 Sheet
"""

import customtkinter as ctk




# ============================================================
# 一、逐级消耗数据表（方案1=镶嵌位1/2，方案9=镶嵌位3）
# 字段: level(目标等级), stage(阶段), mat_name(材料名), qty(单次消耗),
#       base_prob(基础成功率%), fail_acc(失败累积%/次), unlock(解锁条件)
# ============================================================

# 镶嵌位1/2 数据 (与方案1-8相同)
GRIND_DATA_POS12 = [
    # 第1阶段: 青暗紫砂 (1-20级)
    {"level": 1,  "stage": 1, "mat": "青暗紫砂", "qty": 4,  "prob": 100, "acc": 5},
    {"level": 2,  "stage": 1, "mat": "青暗紫砂", "qty": 8,  "prob": 100, "acc": 5},
    {"level": 3,  "stage": 1, "mat": "青暗紫砂", "qty": 8,  "prob": 100, "acc": 5},
    {"level": 4,  "stage": 1, "mat": "青暗紫砂", "qty": 16, "prob": 100, "acc": 5},
    {"level": 5,  "stage": 1, "mat": "青暗紫砂", "qty": 16, "prob": 90,  "acc": 5},
    {"level": 6,  "stage": 1, "mat": "青暗紫砂", "qty": 24, "prob": 90,  "acc": 5},
    {"level": 7,  "stage": 1, "mat": "青暗紫砂", "qty": 24, "prob": 90,  "acc": 5},
    {"level": 8,  "stage": 1, "mat": "青暗紫砂", "qty": 32, "prob": 90,  "acc": 5},
    {"level": 9,  "stage": 1, "mat": "青暗紫砂", "qty": 32, "prob": 80,  "acc": 4},
    {"level": 10, "stage": 1, "mat": "青暗紫砂", "qty": 40, "prob": 80,  "acc": 4, "unlock": "玩家等级≥210"},
    {"level": 11, "stage": 1, "mat": "青暗紫砂", "qty": 40, "prob": 80,  "acc": 4},
    {"level": 12, "stage": 1, "mat": "青暗紫砂", "qty": 48, "prob": 80,  "acc": 4},
    {"level": 13, "stage": 1, "mat": "青暗紫砂", "qty": 48, "prob": 70,  "acc": 3},
    {"level": 14, "stage": 1, "mat": "青暗紫砂", "qty": 56, "prob": 70,  "acc": 3},
    {"level": 15, "stage": 1, "mat": "青暗紫砂", "qty": 56, "prob": 70,  "acc": 3},
    {"level": 16, "stage": 1, "mat": "青暗紫砂", "qty": 64, "prob": 60,  "acc": 2},
    {"level": 17, "stage": 1, "mat": "青暗紫砂", "qty": 64, "prob": 60,  "acc": 2},
    {"level": 18, "stage": 1, "mat": "青暗紫砂", "qty": 72, "prob": 60,  "acc": 2},
    {"level": 19, "stage": 1, "mat": "青暗紫砂", "qty": 72, "prob": 50,  "acc": 2},
    {"level": 20, "stage": 1, "mat": "青暗紫砂", "qty": 80, "prob": 50,  "acc": 2},
    # 第2阶段: 墨紫玉砂 (21-29级)
    {"level": 21, "stage": 2, "mat": "墨紫玉砂", "qty": 4,  "prob": 80,  "acc": 4},
    {"level": 22, "stage": 2, "mat": "墨紫玉砂", "qty": 8,  "prob": 80,  "acc": 4},
    {"level": 23, "stage": 2, "mat": "墨紫玉砂", "qty": 8,  "prob": 70,  "acc": 3},
    {"level": 24, "stage": 2, "mat": "墨紫玉砂", "qty": 16, "prob": 70,  "acc": 3},
    {"level": 25, "stage": 2, "mat": "墨紫玉砂", "qty": 16, "prob": 70,  "acc": 3},
    {"level": 26, "stage": 2, "mat": "墨紫玉砂", "qty": 24, "prob": 60,  "acc": 2},
    {"level": 27, "stage": 2, "mat": "墨紫玉砂", "qty": 24, "prob": 60,  "acc": 2},
    {"level": 28, "stage": 2, "mat": "墨紫玉砂", "qty": 32, "prob": 50,  "acc": 2},
    {"level": 29, "stage": 2, "mat": "墨紫玉砂", "qty": 40, "prob": 40,  "acc": 2},
    # 第3阶段: 琉璃灵砂 (30-40级)
    {"level": 30, "stage": 3, "mat": "琉璃灵砂", "qty": 4,  "prob": 60,  "acc": 5},
    {"level": 31, "stage": 3, "mat": "琉璃灵砂", "qty": 4,  "prob": 60,  "acc": 5},
    {"level": 32, "stage": 3, "mat": "琉璃灵砂", "qty": 8,  "prob": 50,  "acc": 5},
    {"level": 33, "stage": 3, "mat": "琉璃灵砂", "qty": 8,  "prob": 45,  "acc": 4},
    {"level": 34, "stage": 3, "mat": "琉璃灵砂", "qty": 16, "prob": 45,  "acc": 4},
    {"level": 35, "stage": 3, "mat": "琉璃灵砂", "qty": 16, "prob": 40,  "acc": 4},
    {"level": 36, "stage": 3, "mat": "琉璃灵砂", "qty": 24, "prob": 35,  "acc": 3},
    {"level": 37, "stage": 3, "mat": "琉璃灵砂", "qty": 24, "prob": 30,  "acc": 3},
    {"level": 38, "stage": 3, "mat": "琉璃灵砂", "qty": 32, "prob": 25,  "acc": 3},
    {"level": 39, "stage": 3, "mat": "琉璃灵砂", "qty": 32, "prob": 20,  "acc": 3},
    {"level": 40, "stage": 3, "mat": "琉璃灵砂", "qty": 40, "prob": 20,  "acc": 3},
]

# 镶嵌位3 数据 — 材料不同，数量完全相同
POS3_MAT_MAP = {
    "青暗紫砂": "邃夜黑砂",
    "墨紫玉砂": "乌金玉砂",
    "琉璃灵砂": "黑曜灵砂",
}
GRIND_DATA_POS3 = []
for row in GRIND_DATA_POS12:
    new_row = dict(row)
    new_row["mat"] = POS3_MAT_MAP.get(row["mat"], row["mat"])
    GRIND_DATA_POS3.append(new_row)

COPPER_PER_LEVEL = 10000
MAX_LEVEL = 40


class ToolGemGrindPage(ctk.CTkFrame):
    """宝石磨砺养成计算器界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self._build_ui()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # ---- 标题 ----
        ctk.CTkLabel(scroll, text="⚒️ 宝石磨砺养成计算器",
                    font=ctk.CTkFont(size=22, weight="bold"),
                    text_color="#ffffff", anchor="w"
                    ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(scroll, text="QQ华夏手游经典区 · 40级上限 · 含成功率期望值计算",
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

        # ===== Tab 1 =====
        self.tab1 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self._build_tab1()

        # ===== Tab 2 =====
        self.tab2 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self._build_tab2()

        # ---- 说明区域 ----
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(info_inner, text="📖 磨砺规则说明",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").pack(fill="x", pady=(0, 8))

        rules = [
            "· 磨砺共40级，分3个材料阶段（1-20 / 21-29 / 30-40）",
            "· 每次升级消耗铜钱10000 + 对应阶段磨砺材料若干",
            "· 失败不消耗材料，但累积提升下次成功率（上限100%）",
            "· Lv1-4必成功，Lv5起有失败概率，Lv30后概率极低（20%~60%）",
            "· Lv10需角色达到210级才可继续升级",
            "· 期望值 = 单次消耗量 ÷ 成功率（考虑失败重试）",
        ]
        for r in rules:
            ctk.CTkLabel(info_inner, text=r, font=ctk.CTkFont(size=12),
                        text_color=self.colors["text_dim"], anchor="w").pack(fill="x", pady=1)

    # ================================================================
    # Tab 1 UI - 根据材料计算可达等级
    # ================================================================

    def _build_tab1(self):
        inner = ctk.CTkFrame(self.tab1, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        # 当前状态
        ctk.CTkLabel(inner, text="当前磨砺状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        ctk.CTkLabel(inner, text="当前磨砺等级 (0~40)",
                     font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"]
                     ).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.t1_cur_lv = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_cur_lv.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t1_cur_lv.insert(0, "0")

        ctk.CTkLabel(inner, text="镶嵌位置",
                     font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"]
                     ).grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(0, 4))
        self.t1_pos = ctk.CTkOptionMenu(
            inner, values=["位置1/2", "位置3"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t1_pos.grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))

        # 计算模式选择
        ctk.CTkLabel(inner, text="计算模式",
                     font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"]
                     ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 4))
        self.t1_mode = ctk.CTkOptionMenu(
            inner, values=["确定值（不考虑失败）", "期望值（含概率修正）"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t1_mode.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t1_mode.set("期望值（含概率修正）")

        # 拥有材料
        ctk.CTkLabel(inner, text="拥有材料（留空=无限）",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color="#ffffff", anchor="w"
                     ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 6))

        # 3个阶段的材料输入
        self.t1_mat_entries = {}
        mat_labels_pos12 = ["第1阶段 青暗紫砂:", "第2阶段 墨紫玉砂:", "第3阶段 琉璃灵砂:"]
        mat_labels_pos3 = ["第1阶段 邃夜黑砂:", "第2阶段 乌金玉砂:", "第3阶段 黑曜灵砂:"]
        mat_keys_pos12 = ["青暗紫砂", "墨紫玉砂", "琉璃灵砂"]
        mat_keys_pos3 = ["邃夜黑砂", "乌金玉砂", "黑曜灵砂"]

        for i in range(3):
            lbl = ctk.CTkLabel(inner, text=mat_labels_pos12[i], font=ctk.CTkFont(size=12),
                              text_color=self.colors["text_dim"])
            lbl.grid(row=6 + i, column=0, sticky="w", padx=(0, 8), pady=(3, 2))
            entry = ctk.CTkEntry(inner, placeholder_text="留空=不限", height=32, corner_radius=6)
            entry.grid(row=6 + i, column=1, sticky="ew", padx=(8, 0), pady=(3, 2))
            self.t1_mat_entries[mat_keys_pos12[i]] = {
                "lbl": lbl, "entry": entry,
                "lbl_alt": mat_labels_pos3[i], "key_alt": mat_keys_pos3[i],
            }

        # 铜钱
        ctk.CTkLabel(inner, text="铜钱 (万):", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=9, column=0, sticky="w", pady=(3, 2))
        self.t1_copper = ctk.CTkEntry(inner, placeholder_text="留空=不限", height=32, corner_radius=6)
        self.t1_copper.grid(row=9, column=1, sticky="ew", padx=(8, 0), pady=(3, 2))

        # 按钮 + 结果
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(10, 8))

        ctk.CTkButton(btn_row, text="▶ 计算可达到的等级",
                      font=ctk.CTkFont(size=14, weight="bold"), height=40, corner_radius=8,
                      fg_color="#0f3460", hover_color="#16213e",
                      command=self._calc_by_materials).pack(fill="x")

        self.t1_result = ctk.CTkTextbox(inner, height=260, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13))
        self.t1_result.grid(row=11, column=0, columnspan=2, sticky="ew")
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")
        # 阻止滚轮事件冒泡
        self._bind_mousewheel(self.t1_result)

    # ================================================================
    # Tab 2 UI - 根据目标等级计算所需材料
    # ================================================================

    def _build_tab2(self):
        inner = ctk.CTkFrame(self.tab2, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        # 目标设定
        ctk.CTkLabel(inner, text="目标设定", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        ctk.CTkLabel(inner, text="起始磨砺等级",
                     font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"]
                     ).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
        self.t2_start_lv = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_start_lv.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t2_start_lv.insert(0, "0")

        ctk.CTkLabel(inner, text="目标磨砺等级",
                     font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"]
                     ).grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(0, 4))
        self.t2_target_lv = ctk.CTkEntry(inner, placeholder_text="40", height=32, corner_radius=6)
        self.t2_target_lv.grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t2_target_lv.insert(0, "40")

        ctk.CTkLabel(inner, text="镶嵌位置",
                     font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"]
                     ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 4))
        self.t2_pos = ctk.CTkOptionMenu(
            inner, values=["位置1/2", "位置3"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t2_pos.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # 按钮
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 8))

        ctk.CTkButton(btn_row, text="▶ 计算所需材料",
                      font=ctk.CTkFont(size=14, weight="bold"), height=40, corner_radius=8,
                      fg_color="#2e7d32", hover_color="#1b5e20",
                      command=self._calc_for_target).pack(fill="x")

        self.t2_result = ctk.CTkTextbox(inner, height=320, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13))
        self.t2_result.grid(row=6, column=0, columnspan=2, sticky="ew")
        self.t2_result.insert("1.0", "等待计算...\n")
        self.t2_result.configure(state="disabled")

    # ================================================================
    # 标签页切换 & 辅助方法
    # ================================================================

    def _on_tab_change(self, value):
        if value == "📊 根据材料算可达等级":
            self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2.grid_forget()
        else:
            self.tab2.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1.grid_forget()

    def _get_data(self, is_pos3: bool) -> list:
        return GRIND_DATA_POS3 if is_pos3 else GRIND_DATA_POS12

    @staticmethod
    def _is_pos3(option_str: str) -> bool:
        return "位置3" in option_str

    def _show_result(self, tb: ctk.CTkTextbox, text: str):
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.insert("1.0", text)
        tb.configure(state="disabled")

    def _show_error(self, tb: ctk.CTkTextbox, msg: str):
        self._show_result(tb, f"⚠ {msg}\n")
    
    def _bind_mousewheel(self, widget):
        """绑定滚轮事件，阻止事件冒泡"""
        def on_mousewheel(event):
            # 只在widget内部处理滚轮事件，不让事件继续传播
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"  # 阻止事件冒泡
        
        # 绑定Windows/MacOS的滚轮事件
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        # 绑定Linux的滚轮事件
        widget.bind("<Button-4>", lambda e: (widget._parent_canvas.yview_scroll(-1, "units"), "break")[1], add="+")
        widget.bind("<Button-5>", lambda e: (widget._parent_canvas.yview_scroll(1, "units"), "break")[1], add="+")

    @staticmethod
    def _fmt(num) -> str:
        if num >= 10000:
            return f"{num:,.0f}"
        if num >= 100:
            return f"{num:,.1f}"
        return f"{num:.1f}"

    @staticmethod
    def _parse_int(val: str, default: int) -> int:
        try:
            return int((val or "").strip() or str(default))
        except ValueError:
            return default

    def _parse_float_or_inf(self, val: str) -> float:
        v = (val or "").strip()
        if not v:
            return float("inf")
        try:
            return float(v)
        except ValueError:
            return float("inf")

    def _update_t1_labels(self):
        is_p3 = self._is_pos3(self.t1_pos.get()) if hasattr(self, 't1_pos') else False
        for key, info in self.t1_mat_entries.items():
            if is_p3:
                info["lbl"].configure(text=info["lbl_alt"])
            else:
                info["lbl"].configure(text=key + ":")

    # ================================================================
    # 模式一：根据材料计算可达等级
    # ================================================================

    def _calc_by_materials(self):
        try:
            cur_lv = self._parse_int(self.t1_cur_lv.get(), 0)
            is_pos3 = self._is_pos3(self.t1_pos.get())
            use_expected = "期望" in self.t1_mode.get()

            if cur_lv < 0 or cur_lv > MAX_LEVEL:
                self._show_error(self.t1_result, f"磨砺等级需在 0 ~ {MAX_LEVEL}")
                return

            data = self._get_data(is_pos3)

            # 解析材料
            mats = {}  # mat_key -> amount (float)
            for key, info in self.t1_mat_entries.items():
                actual_key = info["key_alt"] if is_pos3 else key
                mats[actual_key] = self._parse_float_or_inf(info["entry"].get())

            copper_wan = self._parse_float_or_inf(self.t1_copper.get())
            copper = copper_wan * 10000 if copper_wan != float("inf") else float("inf")

            all_empty = (
                all(v == float("inf") for v in mats.values())
                and copper == float("inf")
            )
            if all_empty:
                self._show_error(self.t1_result, "请至少输入一种材料的数量！")
                return

            # 开始模拟升级
            lv = cur_lv
            used_mats = {k: 0.0 for k in mats}
            used_copper = 0.0
            table_data = []

            for row in data:
                if lv >= row["level"]:
                    continue

                qty = row["qty"]
                prob = row["prob"]

                if use_expected and prob < 100:
                    expected_qty = qty / (prob / 100.0)
                    cost_qty = expected_qty
                else:
                    cost_qty = qty

                cost_copper = COPPER_PER_LEVEL

                # 检查材料是否足够
                mat_ok = True
                copper_ok = True
                if mats[row["mat"]] != float("inf"):
                    if mats[row["mat"]] < cost_qty:
                        mat_ok = False
                if copper != float("inf"):
                    if copper < cost_copper:
                        copper_ok = False

                if not mat_ok or not copper_ok:
                    # 材料不足
                    lack_info = []
                    if not mat_ok:
                        lack = cost_qty - mats[row["mat"]]
                        lack_info.append(f"材料差{self._fmt(lack)}")
                    if not copper_ok:
                        lack_info.append(f"铜钱差{self._fmt(cost_copper - copper)}")
                    
                    table_data.append([
                        row["level"],
                        row["mat"],
                        f"{self._fmt(cost_qty)}",
                        f"{cost_copper / 10000:.1f}万",
                        f"{prob}%",
                        row.get("unlock", ""),
                        f"❌ {', '.join(lack_info)}"
                    ])
                    break

                # 扣除材料
                if mats[row["mat"]] != float("inf"):
                    mats[row["mat"]] -= cost_qty
                    used_mats[row["mat"]] += cost_qty
                if copper != float("inf"):
                    copper -= cost_copper
                    used_copper += cost_copper

                lv = row["level"]
                
                prob_note = ""
                if prob < 100:
                    if use_expected:
                        prob_note = f"期望值"
                    else:
                        prob_note = f"忽略概率"
                else:
                    prob_note = "必成功"
                
                unlock_info = row.get("unlock", "")
                
                table_data.append([
                    row["level"],
                    row["mat"],
                    f"{self._fmt(cost_qty)}",
                    f"{cost_copper / 10000:.1f}万",
                    f"{prob}%",
                    unlock_info,
                    f"✅ {prob_note}"
                ])

            # 添加汇总行
            if table_data:
                table_data.append(["", "", "", "", "", "", ""])  # 空行
                table_data.append([
                    "总计",
                    "累计消耗",
                    "",
                    "",
                    "",
                    "",
                    ""
                ])
                for k, v in used_mats.items():
                    if v > 0:
                        table_data.append([
                            "",
                            k,
                            f"{self._fmt(v)}",
                            "",
                            "",
                            "",
                            "已消耗"
                        ])
                if used_copper > 0:
                    table_data.append([
                        "",
                        "铜钱",
                        f"{self._fmt(used_copper)}",
                        f"{self._fmt(used_copper / 10000)}万",
                        "",
                        "",
                        "已消耗"
                    ])

            # 显示表格
            mode_str = "期望值模式" if use_expected else "确定值模式"
            pos_str = "位置3" if is_pos3 else "位置1/2"
            headers = ["目标等级", "材料名称", "材料数量", "铜钱", "成功率", "解锁条件", "状态"]
            title = f"宝石磨砺养成计算 ({mode_str} · {pos_str}) - {cur_lv}级→{lv}级"
            
            # 在文本框中显示详细结果
            output = f"✅ 计算完成\n\n"
            output += f"{'='*50}\n"
            output += f"起始等级: {cur_lv}级\n"
            output += f"可达等级: {lv}级\n"
            output += f"提升等级: {lv - cur_lv}级\n"
            output += f"镶嵌位置: {pos_str}\n"
            output += f"计算模式: {mode_str}\n"
            output += f"{'='*50}\n\n"
            
            output += "【累计消耗】\n"
            for k, v in used_mats.items():
                if v > 0:
                    output += f"  {k}: {self._fmt(v)}颗\n"
            if used_copper > 0:
                output += f"  铜钱: {self._fmt(used_copper)} ({self._fmt(used_copper/10000)}万)\n"
            
            output += f"\n{'='*50}\n\n"
            
            # 显示升级路径（每5级显示一次）
            output += "【升级路径】\n"
            for i, row in enumerate(table_data[:20]):  # 只显示前20级
                target_lv = row[0]
                mat_name = row[1]
                mat_qty = row[2]   # 已是格式化字符串
                copper = row[3]    # 已是格式化字符串
                rate = row[4]
                if isinstance(target_lv, int):
                    if target_lv % 5 == 0 or target_lv == lv or i < 3:
                        output += f"  Lv.{target_lv}: {mat_name} × {mat_qty}, 铜钱 {copper}, 成功率 {rate}\n"
            
            if len(table_data) > 20:
                output += f"\n... (共{len(table_data)}级，仅显示关键节点) ...\n"
            
            self._show_result(self.t1_result, output)

        except Exception as ex:
            self._show_error(self.t1_result, f"计算出错: {ex}")

    # ================================================================
    # 模式二：根据目标等级计算所需材料
    # ================================================================

    def _calc_for_target(self):
        try:
            start_lv = self._parse_int(self.t2_start_lv.get(), 0)
            target_lv = self._parse_int(self.t2_target_lv.get(), 40)
            is_pos3 = self._is_pos3(self.t2_pos.get())

            if start_lv < 0 or start_lv > MAX_LEVEL:
                self._show_error(self.t2_result, f"起始等级需在 0 ~ {MAX_LEVEL}")
                return
            if target_lv < 0 or target_lv > MAX_LEVEL:
                self._show_error(self.t2_result, f"目标等级需在 0 ~ {MAX_LEVEL}")
                return
            if target_lv <= start_lv:
                self._show_error(self.t2_result, "目标等级必须大于起始等级！")
                return

            data = self._get_data(is_pos3)

            # 累加确定消耗和期望消耗
            total_mats_det = {}  # 确定消耗
            total_mats_exp = {}  # 期望消耗
            total_copper = 0
            table_data = []

            for row in data:
                if row["level"] <= start_lv:
                    continue
                if row["level"] > target_lv:
                    break

                mat = row["mat"]
                qty = row["qty"]
                prob = row["prob"]
                cop = COPPER_PER_LEVEL

                # 确定
                total_mats_det[mat] = total_mats_det.get(mat, 0) + qty
                total_copper += cop

                # 期望
                if prob >= 100:
                    exp_qty = qty
                else:
                    exp_qty = qty / (prob / 100.0)
                total_mats_exp[mat] = total_mats_exp.get(mat, 0) + exp_qty

                # 构建表格行
                prob_note = "必成功" if prob >= 100 else f"{prob}%"
                unlock_info = row.get("unlock", "")
                extra = exp_qty - qty
                extra_note = f"(期望+{extra:.1f})" if extra > 0.01 else ""
                
                table_data.append([
                    row["level"],
                    mat,
                    qty,
                    f"{exp_qty:.1f}",
                    extra_note,
                    prob_note,
                    f"{cop / 10000:.1f}万",
                    unlock_info
                ])

            # 添加空行和汇总
            if table_data:
                table_data.append(["", "", "", "", "", "", "", ""])
                
                # 确定消耗汇总
                for mat, amt in total_mats_det.items():
                    exp_amt = total_mats_exp.get(mat, 0)
                    extra = exp_amt - amt
                    table_data.append([
                        "总计-确定",
                        mat,
                        amt,
                        "",
                        "",
                        "不考虑失败",
                        "",
                        ""
                    ])
                
                table_data.append([
                    "总计-确定",
                    "铜钱",
                    total_copper,
                    "",
                    "",
                    "",
                    f"{total_copper/10000:.1f}万",
                    ""
                ])
                
                table_data.append(["", "", "", "", "", "", "", ""])
                
                # 期望消耗汇总
                for mat, amt in total_mats_exp.items():
                    det_amt = total_mats_det.get(mat, 0)
                    extra = amt - det_amt
                    extra_note = f"+{extra:.1f}因失败" if extra > 0.01 else ""
                    table_data.append([
                        "总计-期望",
                        mat,
                        "",
                        f"{amt:.1f}",
                        extra_note,
                        "含概率修正",
                        "",
                        ""
                    ])
                
                table_data.append([
                    "总计-期望",
                    "铜钱",
                    total_copper,
                    "",
                    "",
                    "",
                    f"{total_copper/10000:.1f}万",
                    ""
                ])

            # 显示表格
            pos_str = "位置3" if is_pos3 else "位置1/2"
            headers = [
                "等级",
                "材料名称",
                "确定数量",
                "期望数量",
                "额外消耗",
                "成功率",
                "铜钱",
                "解锁条件"
            ]
            title = f"宝石磨砺材料需求 ({pos_str}) - Lv.{start_lv}→Lv.{target_lv} (共{target_lv-start_lv}级)"
            
            # 在文本框中显示详细结果
            output = f"✅ 计算完成\n\n"
            output += f"{'='*50}\n"
            output += f"起始等级: {start_lv}级\n"
            output += f"目标等级: {target_lv}级\n"
            output += f"提升等级: {target_lv - start_lv}级\n"
            output += f"镶嵌位置: {pos_str}\n"
            output += f"{'='*50}\n\n"
            
            output += "【确定消耗】(不考虑失败)\n"
            for mat, amt in total_mats_det.items():
                output += f"  {mat}: {amt}颗\n"
            output += f"  铜钱: {total_copper} ({total_copper/10000:.1f}万)\n\n"
            
            output += "【期望消耗】(含失败概率)\n"
            for mat, amt in total_mats_exp.items():
                det = total_mats_det.get(mat, 0)
                extra = amt - det
                output += f"  {mat}: {amt:.1f}颗 (+{extra:.1f})\n"
            output += f"  铜钱: {total_copper} ({total_copper/10000:.1f}万)\n\n"
            
            output += f"{'='*50}\n\n"
            
            # 显示逐级详情（选择性）
            output += "【逐级材料需求】\n"
            for i, row in enumerate(table_data[:15]):  # 只显示前15级
                if "总计" in str(row[0]):
                    # 确定数量在 row[2]，期望数量在 row[3]
                    qty_str = str(row[2]) if row[2] != "" else ""
                    exp_str = str(row[3]) if row[3] != "" else ""
                    if qty_str and exp_str:
                        output += f"\n>>> {row[0]}: {row[1]} 确定{qty_str}, 期望{exp_str}\n"
                    elif qty_str:
                        output += f"\n>>> {row[0]}: {row[1]} {qty_str}\n"
                    elif exp_str:
                        output += f"\n>>> {row[0]}: {row[1]} 期望{exp_str}\n"
                    else:
                        output += f"\n>>> {row[0]}: {row[1]}\n"
                elif isinstance(row[0], int):
                    lv = row[0]
                    if lv % 5 == 0 or lv == target_lv or i < 5:
                        # row[3] 已是格式化字符串，直接输出
                        output += f"  Lv.{lv}: {row[1]}, 确定{row[2]}颗, 期望{row[3]}颗\n"
            
            if len(table_data) > 18:
                output += f"\n... (仅显示部分，共{len(table_data)}行) ...\n"
            
            self._show_result(self.t2_result, output)

        except Exception as ex:
            self._show_error(self.t2_result, f"计算出错: {ex}")
