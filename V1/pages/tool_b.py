"""
装备淬炼计算器模块
根据材料量计算可达成淬炼等级，或根据目标等级计算所需材料。
"""

import customtkinter as ctk


# 材料类型名称
MATERIAL_NAMES = ["曜金矿石", "九转菩提", "摩诃水晶", "诸法舍利"]
MATERIAL2_NAME = "蚀日之晶"

# 淬炼材料消耗表数据
REFINING_DATA = [
    {"level": 1, "mat1Type": 0, "mat1Count": 33.0000, "mat2Count": 0},
    {"level": 2, "mat1Type": 0, "mat1Count": 36.4650, "mat2Count": 0},
    {"level": 3, "mat1Type": 0, "mat1Count": 54.2586, "mat2Count": 0},
    {"level": 4, "mat1Type": 0, "mat1Count": 67.8233, "mat2Count": 0},
    {"level": 5, "mat1Type": 0, "mat1Count": 122.5388, "mat2Count": 0},
    {"level": 6, "mat1Type": 0, "mat1Count": 122.5388, "mat2Count": 0},
    {"level": 7, "mat1Type": 0, "mat1Count": 175.4443, "mat2Count": 0},
    {"level": 8, "mat1Type": 0, "mat1Count": 204.4749, "mat2Count": 0},
    {"level": 9, "mat1Type": 0, "mat1Count": 266.9707, "mat2Count": 0},
    {"level": 10, "mat1Type": 0, "mat1Count": 396.6755, "mat2Count": 0},
    {"level": 11, "mat1Type": 0, "mat1Count": 307.9997, "mat2Count": 0},
    {"level": 12, "mat1Type": 0, "mat1Count": 197.9987, "mat2Count": 16.49989174},
    {"level": 13, "mat1Type": 0, "mat1Count": 281.5977, "mat2Count": 17.59985566},
    {"level": 14, "mat1Type": 0, "mat1Count": 351.9971, "mat2Count": 17.59985566},
    {"level": 15, "mat1Type": 0, "mat1Count": 454.0748, "mat2Count": 37.83956697},
    {"level": 16, "mat1Type": 0, "mat1Count": 573.9187, "mat2Count": 0},
    {"level": 17, "mat1Type": 0, "mat1Count": 721.6792, "mat2Count": 45.10494917},
    {"level": 18, "mat1Type": 0, "mat1Count": 811.8891, "mat2Count": 45.10494917},
    {"level": 19, "mat1Type": 0, "mat1Count": 1087.5835, "mat2Count": 51.78968825},
    {"level": 20, "mat1Type": 0, "mat1Count": 1642.8711, "mat2Count": 98.57226699},
    {"level": 21, "mat1Type": 1, "mat1Count": 75.6008, "mat2Count": 0},
    {"level": 22, "mat1Type": 1, "mat1Count": 77.0000, "mat2Count": 57.74999932},
    {"level": 23, "mat1Type": 1, "mat1Count": 103.1115, "mat2Count": 61.86688992},
    {"level": 24, "mat1Type": 1, "mat1Count": 111.7002, "mat2Count": 67.02009864},
    {"level": 25, "mat1Type": 1, "mat1Count": 133.6344, "mat2Count": 66.81720722},
    {"level": 26, "mat1Type": 1, "mat1Count": 147.1060, "mat2Count": 0},
    {"level": 27, "mat1Type": 1, "mat1Count": 214.7409, "mat2Count": 122.7090711},
    {"level": 28, "mat1Type": 1, "mat1Count": 245.4181, "mat2Count": 122.7090711},
    {"level": 29, "mat1Type": 1, "mat1Count": 359.6938, "mat2Count": 179.846885},
    {"level": 30, "mat1Type": 1, "mat1Count": 449.6172, "mat2Count": 179.846885},
    {"level": 31, "mat1Type": 1, "mat1Count": 226.8024, "mat2Count": 0},
    {"level": 32, "mat1Type": 1, "mat1Count": 154.0000, "mat2Count": 96.24999887},
    {"level": 33, "mat1Type": 1, "mat1Count": 185.6007, "mat2Count": 103.1114832},
    {"level": 34, "mat1Type": 1, "mat1Count": 223.4003, "mat2Count": 134.0401973},
    {"level": 35, "mat1Type": 1, "mat1Count": 244.9964, "mat2Count": 133.6344144},
    {"level": 36, "mat1Type": 1, "mat1Count": 294.2120, "mat2Count": 0},
    {"level": 37, "mat1Type": 1, "mat1Count": 368.1272, "mat2Count": 245.4181423},
    {"level": 38, "mat1Type": 1, "mat1Count": 398.8045, "mat2Count": 306.7726778},
    {"level": 39, "mat1Type": 1, "mat1Count": 629.4641, "mat2Count": 449.6172126},
    {"level": 40, "mat1Type": 1, "mat1Count": 674.4258, "mat2Count": 449.6172126},
    {"level": 41, "mat1Type": 2, "mat1Count": 189.0020, "mat2Count": 0},
    {"level": 42, "mat1Type": 2, "mat1Count": 269.5000, "mat2Count": 230.9999973},
    {"level": 43, "mat1Type": 2, "mat1Count": 288.7122, "mat2Count": 247.4675597},
    {"level": 44, "mat1Type": 2, "mat1Count": 312.7605, "mat2Count": 268.0803946},
    {"level": 45, "mat1Type": 2, "mat1Count": 311.8136, "mat2Count": 267.2688289},
    {"level": 46, "mat1Type": 2, "mat1Count": 343.2474, "mat2Count": 0},
    {"level": 47, "mat1Type": 2, "mat1Count": 460.1590, "mat2Count": 429.4817489},
    {"level": 48, "mat1Type": 2, "mat1Count": 460.1590, "mat2Count": 429.4817489},
    {"level": 49, "mat1Type": 2, "mat1Count": 674.4258, "mat2Count": 629.4640976},
    {"level": 50, "mat1Type": 2, "mat1Count": 674.4258, "mat2Count": 719.3875401},
    {"level": 51, "mat1Type": 2, "mat1Count": 283.5030, "mat2Count": 0},
    {"level": 52, "mat1Type": 2, "mat1Count": 288.7500, "mat2Count": 307.9999964},
    {"level": 53, "mat1Type": 2, "mat1Count": 309.3344, "mat2Count": 329.9567462},
    {"level": 54, "mat1Type": 2, "mat1Count": 335.1005, "mat2Count": 402.1205918},
    {"level": 55, "mat1Type": 2, "mat1Count": 334.0860, "mat2Count": 400.9032433},
    {"level": 56, "mat1Type": 2, "mat1Count": 367.7650, "mat2Count": 0},
    {"level": 57, "mat1Type": 2, "mat1Count": 490.8363, "mat2Count": 552.1908201},
    {"level": 58, "mat1Type": 2, "mat1Count": 490.8363, "mat2Count": 552.1908201},
    {"level": 59, "mat1Type": 2, "mat1Count": 719.3875, "mat2Count": 809.3109826},
    {"level": 60, "mat1Type": 2, "mat1Count": 719.3875, "mat2Count": 809.3109826},
    {"level": 61, "mat1Type": 2, "mat1Count": 302.4032, "mat2Count": 0},
    {"level": 62, "mat1Type": 2, "mat1Count": 308.0000, "mat2Count": 461.9999946},
    {"level": 63, "mat1Type": 2, "mat1Count": 329.9567, "mat2Count": 494.9351194},
    {"level": 64, "mat1Type": 2, "mat1Count": 357.4405, "mat2Count": 536.1607891},
    {"level": 65, "mat1Type": 2, "mat1Count": 356.3584, "mat2Count": 534.5376578},
    {"level": 66, "mat1Type": 2, "mat1Count": 392.2827, "mat2Count": 0},
    {"level": 67, "mat1Type": 2, "mat1Count": 521.5136, "mat2Count": 736.2544268},
    {"level": 68, "mat1Type": 2, "mat1Count": 521.5136, "mat2Count": 736.2544268},
    {"level": 69, "mat1Type": 2, "mat1Count": 764.3493, "mat2Count": 1079.08131},
    {"level": 70, "mat1Type": 2, "mat1Count": 764.3493, "mat2Count": 1079.08131},
    {"level": 71, "mat1Type": 2, "mat1Count": 321.3034, "mat2Count": 0},
    {"level": 72, "mat1Type": 2, "mat1Count": 327.2500, "mat2Count": 692.9999918},
    {"level": 73, "mat1Type": 2, "mat1Count": 350.5790, "mat2Count": 742.402679},
    {"level": 74, "mat1Type": 2, "mat1Count": 379.7806, "mat2Count": 804.2411837},
    {"level": 75, "mat1Type": 2, "mat1Count": 378.6308, "mat2Count": 801.8064866},
    {"level": 76, "mat1Type": 2, "mat1Count": 441.3180, "mat2Count": 0},
    {"level": 77, "mat1Type": 2, "mat1Count": 441.3180, "mat2Count": 882.6360807},
    {"level": 78, "mat1Type": 2, "mat1Count": 441.3180, "mat2Count": 882.6360807},
    {"level": 79, "mat1Type": 2, "mat1Count": 565.2668, "mat2Count": 1507.378065},
    {"level": 80, "mat1Type": 2, "mat1Count": 565.2668, "mat2Count": 1507.378065},
    {"level": 81, "mat1Type": 2, "mat1Count": 340.2036, "mat2Count": 0},
    {"level": 82, "mat1Type": 2, "mat1Count": 340.2036, "mat2Count": 907.2096},
    {"level": 83, "mat1Type": 2, "mat1Count": 368.9477, "mat2Count": 983.8606553},
    {"level": 84, "mat1Type": 2, "mat1Count": 368.9477, "mat2Count": 983.8606553},
    {"level": 85, "mat1Type": 2, "mat1Count": 400.9032, "mat2Count": 1069.075316},
    {"level": 86, "mat1Type": 2, "mat1Count": 423.1756, "mat2Count": 0},
    {"level": 87, "mat1Type": 2, "mat1Count": 465.8357, "mat2Count": 1471.060134},
    {"level": 88, "mat1Type": 2, "mat1Count": 465.8357, "mat2Count": 1471.060134},
    {"level": 89, "mat1Type": 2, "mat1Count": 628.0742, "mat2Count": 1884.222581},
    {"level": 90, "mat1Type": 2, "mat1Count": 628.0742, "mat2Count": 1884.222581},
    {"level": 91, "mat1Type": 3, "mat1Count": 535.6531, "mat2Count": 2571.135068},
    {"level": 92, "mat1Type": 3, "mat1Count": 657.2294, "mat2Count": 3154.700961},
    {"level": 93, "mat1Type": 3, "mat1Count": 788.6752, "mat2Count": 3154.700961},
    {"level": 94, "mat1Type": 3, "mat1Count": 1034.9925, "mat2Count": 4139.970131},
    {"level": 95, "mat1Type": 3, "mat1Count": 1149.9917, "mat2Count": 4139.970131},
    {"level": 96, "mat1Type": 3, "mat1Count": 788.6752, "mat2Count": 3505.223289},
    {"level": 97, "mat1Type": 3, "mat1Count": 788.6752, "mat2Count": 3505.223289},
    {"level": 98, "mat1Type": 3, "mat1Count": 1149.9917, "mat2Count": 4599.966813},
]


def convert_material(count, from_type, to_type):
    """将材料转换为指定类型（向上或向下转换）"""
    if from_type == to_type:
        return count
    diff = to_type - from_type
    if diff > 0:
        # 向上转换：5个低级 = 1个高级
        return count / (5 ** diff)
    else:
        # 向下转换：1个高级 = 5个低级
        return count * (5 ** abs(diff))


def to_lowest_material(count, mat_type):
    """将材料数量转换为最低级（曜金矿石）的等价数量"""
    return convert_material(count, mat_type, 0)


def from_lowest_material(count, to_type):
    """将最低级材料数量转换为指定类型"""
    return convert_material(count, 0, to_type)


# 预计算：每一级所需的最低级材料数量，避免计算时重复调用
_REFINING_LOWEST = [to_lowest_material(d["mat1Count"], d["mat1Type"]) for d in REFINING_DATA]


def format_number(num):
    """格式化数字（保留合适的小数位）"""
    if num == 0:
        return "0"
    if num >= 1000000:
        return f"{num:,.0f}"
    if num >= 10000:
        return f"{num:,.1f}"
    if num >= 100:
        return f"{num:,.2f}"
    if num >= 10:
        return f"{num:,.3f}"
    return f"{num:,.4f}"


class ToolBPage(ctk.CTkFrame):
    """装备淬炼计算器界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self._build_ui()

    def _build_ui(self):
        """构建淬炼计算器界面"""
        # 滚动容器
        scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # ---- 页面标题 ----
        ctk.CTkLabel(
            scroll,
            text="⚒️ 装备淬炼计算器",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        # ============================================================
        # 功能一：根据材料量计算可达成淬炼等级
        # ============================================================
        func1_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        func1_card.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        func1_inner = ctk.CTkFrame(func1_card, fg_color="transparent")
        func1_inner.pack(fill="x", padx=20, pady=18)
        func1_inner.grid_columnconfigure((0, 1), weight=1)

        # 功能一标题
        ctk.CTkLabel(
            func1_inner,
            text="📊 功能一：根据材料量计算可达成淬炼等级",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        # 初始淬炼等级
        ctk.CTkLabel(
            func1_inner, text="初始淬炼等级",
            font=ctk.CTkFont(size=13), text_color=self.colors["text"], anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 4))

        self.calc1_start_level = ctk.CTkEntry(
            func1_inner, placeholder_text="0", height=34, corner_radius=8,
        )
        self.calc1_start_level.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        self.calc1_start_level.insert(0, "0")

        # 材料1类型
        ctk.CTkLabel(
            func1_inner, text="材料1类型",
            font=ctk.CTkFont(size=13), text_color=self.colors["text"], anchor="w",
        ).grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 4))

        self.calc1_mat1_type = ctk.CTkOptionMenu(
            func1_inner,
            values=[
                "曜金矿石（最低级）",
                "九转菩提",
                "摩诃水晶",
                "诸法舍利（最高级）",
            ],
            height=34, corner_radius=8,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.calc1_mat1_type.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))

        # 材料1数量
        ctk.CTkLabel(
            func1_inner, text="材料1数量",
            font=ctk.CTkFont(size=13), text_color=self.colors["text"], anchor="w",
        ).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=(0, 4))

        self.calc1_mat1_count = ctk.CTkEntry(
            func1_inner, placeholder_text="留空=无限", height=34, corner_radius=8,
        )
        self.calc1_mat1_count.grid(row=4, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

        # 材料2（蚀日之晶）数量
        ctk.CTkLabel(
            func1_inner, text="材料2（蚀日之晶）数量",
            font=ctk.CTkFont(size=13), text_color=self.colors["text"], anchor="w",
        ).grid(row=3, column=1, sticky="w", padx=(10, 0), pady=(0, 4))

        self.calc1_mat2_count = ctk.CTkEntry(
            func1_inner, placeholder_text="留空=无限", height=34, corner_radius=8,
        )
        self.calc1_mat2_count.grid(row=4, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))

        # 计算按钮
        ctk.CTkButton(
            func1_inner,
            text="▶  计算可达成等级",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#0f3460", hover_color="#16213e",
            command=self._calculate_max_level,
        ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(5, 8))

        # 功能一结果区域
        self.calc1_result = ctk.CTkTextbox(
            func1_inner, height=180, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
        )
        self.calc1_result.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.calc1_result.insert("1.0", "等待计算...\n")
        self.calc1_result.configure(state="disabled")

        # ============================================================
        # 功能二：根据目标等级计算所需材料
        # ============================================================
        func2_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        func2_card.grid(row=2, column=0, sticky="ew", pady=(0, 15))

        func2_inner = ctk.CTkFrame(func2_card, fg_color="transparent")
        func2_inner.pack(fill="x", padx=20, pady=18)
        func2_inner.grid_columnconfigure((0, 1), weight=1)

        # 功能二标题
        ctk.CTkLabel(
            func2_inner,
            text="🎯 功能二：根据目标等级计算所需材料",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        # 初始淬炼等级
        ctk.CTkLabel(
            func2_inner, text="初始淬炼等级",
            font=ctk.CTkFont(size=13), text_color=self.colors["text"], anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 4))

        self.calc2_start_level = ctk.CTkEntry(
            func2_inner, placeholder_text="0", height=34, corner_radius=8,
        )
        self.calc2_start_level.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        self.calc2_start_level.insert(0, "0")

        # 目标淬炼等级
        ctk.CTkLabel(
            func2_inner, text="目标淬炼等级",
            font=ctk.CTkFont(size=13), text_color=self.colors["text"], anchor="w",
        ).grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 4))

        self.calc2_target_level = ctk.CTkEntry(
            func2_inner, placeholder_text="98", height=34, corner_radius=8,
        )
        self.calc2_target_level.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.calc2_target_level.insert(0, "98")

        # 计算按钮
        ctk.CTkButton(
            func2_inner,
            text="▶  计算所需材料",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#2e7d32", hover_color="#1b5e20",
            command=self._calculate_materials,
        ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(5, 8))

        # 功能二结果区域
        self.calc2_result = ctk.CTkTextbox(
            func2_inner, height=220, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
        )
        self.calc2_result.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.calc2_result.insert("1.0", "等待计算...\n")
        self.calc2_result.configure(state="disabled")

        # ============================================================
        # 材料转换说明
        # ============================================================
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            info_inner,
            text="📖 材料转换规则",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).pack(fill="x", pady=(0, 8))

        rules = [
            "• 5个低级材料 = 1个高级材料",
            "• 1个高级材料 = 5个低级材料",
            "",
            "材料等级（由低到高）：",
            "曜金矿石 < 九转菩提 < 摩诃水晶 < 诸法舍利",
        ]
        for rule in rules:
            ctk.CTkLabel(
                info_inner, text=rule,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"], anchor="w",
            ).pack(fill="x", pady=1)

    # ================================================================
    # 辅助方法
    # ================================================================

    def _get_mat1_type_index(self) -> int:
        """获取材料1类型的索引值"""
        type_map = {
            "曜金矿石（最低级）": 0,
            "九转菩提": 1,
            "摩诃水晶": 2,
            "诸法舍利（最高级）": 3,
        }
        return type_map.get(self.calc1_mat1_type.get(), 0)

    def _show_result(self, textbox: ctk.CTkTextbox, text: str):
        """在结果区域显示文本"""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")

    def _show_error(self, textbox: ctk.CTkTextbox, msg: str):
        """在结果区域显示错误信息"""
        self._show_result(textbox, f"⚠️ {msg}\n")

    # ================================================================
    # 功能一：根据材料量计算可达成淬炼等级
    # ================================================================

    def _calculate_max_level(self):
        """根据材料量计算可达成淬炼等级"""
        try:
            start_level = int(self.calc1_start_level.get() or "0")
        except ValueError:
            self._show_error(self.calc1_result, "初始等级请输入有效数字！")
            return

        mat1_type = self._get_mat1_type_index()
        mat1_input = self.calc1_mat1_count.get().strip()
        mat2_input = self.calc1_mat2_count.get().strip()

        has_mat1 = mat1_input != ""
        has_mat2 = mat2_input != ""

        if not has_mat1 and not has_mat2:
            self._show_error(self.calc1_result, "请至少输入一种材料的数量！")
            return

        try:
            mat1_lowest = to_lowest_material(float(mat1_input), mat1_type) if has_mat1 else float("inf")
            mat2_count = float(mat2_input) if has_mat2 else float("inf")
        except ValueError:
            self._show_error(self.calc1_result, "材料数量请输入有效数字！")
            return

        current_level = start_level
        used_mat1_lowest = 0.0
        used_mat2 = 0.0
        details = []

        # 从当前等级的下一级开始计算
        for i in range(start_level, len(REFINING_DATA)):
            data = REFINING_DATA[i]
            need_mat1_lowest = _REFINING_LOWEST[i]
            need_mat2 = data["mat2Count"]

            # 检查材料是否足够
            if (mat1_lowest - used_mat1_lowest < need_mat1_lowest or
                    mat2_count - used_mat2 < need_mat2):
                break

            used_mat1_lowest += need_mat1_lowest
            used_mat2 += need_mat2
            current_level = data["level"]
            details.append(data)

        # 计算剩余材料
        remaining_mat1_lowest = (mat1_lowest - used_mat1_lowest) if has_mat1 else None
        remaining_mat2 = (mat2_count - used_mat2) if has_mat2 else None

        # 构建结果文本
        lines = []
        lines.append(f"最高可提升到：{current_level} 级")
        lines.append(f"从 {start_level} 级 → {current_level} 级，共提升 {current_level - start_level} 级")
        lines.append("━" * 36)

        if has_mat1:
            used_mat1 = from_lowest_material(used_mat1_lowest, mat1_type)
            lines.append(f"消耗材料1：{format_number(used_mat1)} {MATERIAL_NAMES[mat1_type]}")
        else:
            lines.append("消耗材料1：无限")

        if has_mat2:
            lines.append(f"消耗材料2：{format_number(used_mat2)} {MATERIAL2_NAME}")
        else:
            lines.append("消耗材料2：无限")

        if remaining_mat1_lowest is not None and remaining_mat1_lowest > 0.0001:
            remaining_mat1 = from_lowest_material(remaining_mat1_lowest, mat1_type)
            lines.append(f"剩余材料1：{format_number(remaining_mat1)} {MATERIAL_NAMES[mat1_type]}")

        if remaining_mat2 is not None and remaining_mat2 > 0.0001:
            lines.append(f"剩余材料2：{format_number(remaining_mat2)} {MATERIAL2_NAME}")

        # 显示各级消耗详情
        if 0 < len(details) <= 10:
            lines.append("")
            lines.append("详细消耗：")
            for d in details:
                lines.append(
                    f"  {d['level']}级：{MATERIAL_NAMES[d['mat1Type']]}×{format_number(d['mat1Count'])}，"
                    f"{MATERIAL2_NAME}×{format_number(d['mat2Count'])}"
                )
        elif len(details) > 10:
            lines.append("")
            lines.append(f"共消耗 {len(details)} 个等级的升级材料")

        self._show_result(self.calc1_result, "\n".join(lines) + "\n")

    # ================================================================
    # 功能二：根据目标等级计算所需材料
    # ================================================================

    def _calculate_materials(self):
        """根据目标等级计算所需材料"""
        try:
            start_level = int(self.calc2_start_level.get() or "0")
            target_level = int(self.calc2_target_level.get() or "98")
        except ValueError:
            self._show_error(self.calc2_result, "等级请输入有效数字！")
            return

        if start_level >= target_level:
            self._show_error(self.calc2_result, "目标等级必须大于初始等级！")
            return

        if target_level > 98:
            self._show_error(self.calc2_result, "目标等级不能超过98！")
            return

        # 计算需要的总材料（转换为最低级）
        total_mat1_lowest = 0.0
        total_mat2 = 0.0
        mat1_type_usage = {}  # 记录各级别材料1的使用

        for i in range(start_level, target_level):
            data = REFINING_DATA[i]
            total_mat1_lowest += _REFINING_LOWEST[i]
            total_mat2 += data["mat2Count"]

            t = data["mat1Type"]
            mat1_type_usage[t] = mat1_type_usage.get(t, 0) + data["mat1Count"]

        # 找出最高级别的材料1类型
        highest_mat1_type = max(mat1_type_usage.keys()) if mat1_type_usage else 0

        # 将总材料1转换为最高级别的数量
        total_mat1_highest = from_lowest_material(total_mat1_lowest, highest_mat1_type)

        # 构建结果文本
        lines = []
        lines.append(f"从 {start_level} 级 → {target_level} 级")
        lines.append(f"需要提升 {target_level - start_level} 级")
        lines.append("━" * 36)
        lines.append(f"所需材料1：{format_number(total_mat1_highest)} {MATERIAL_NAMES[highest_mat1_type]}")
        lines.append(f"所需材料2：{format_number(total_mat2)} {MATERIAL2_NAME}")

        # 显示各类型材料1的总量
        if len(mat1_type_usage) > 1:
            lines.append("")
            lines.append("材料1各类型需求：")
            for t in range(4):
                if mat1_type_usage.get(t, 0) > 0.0001:
                    lines.append(f"  {MATERIAL_NAMES[t]}：{format_number(mat1_type_usage[t])}")

        # 显示材料1的低级换算
        if highest_mat1_type > 0:
            lines.append("")
            lines.append("低级换算：")
            for t in range(highest_mat1_type - 1, -1, -1):
                lower_count = from_lowest_material(total_mat1_lowest, t)
                lines.append(f"  或需 {MATERIAL_NAMES[t]}：{format_number(lower_count)}")

        # 显示各级别消耗详情
        lines.append("")
        lines.append("各级别详细消耗：")
        for i in range(start_level, target_level):
            data = REFINING_DATA[i]
            lines.append(
                f"  {data['level']}级：{MATERIAL_NAMES[data['mat1Type']]}×{format_number(data['mat1Count'])}，"
                f"{MATERIAL2_NAME}×{format_number(data['mat2Count'])}"
            )

        self._show_result(self.calc2_result, "\n".join(lines) + "\n")
