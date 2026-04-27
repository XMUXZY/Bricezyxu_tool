"""
装备重铸计算器模块
根据材料量计算可达到的重铸等级，或根据目标等级计算所需材料。
支持6种材料类型，按等级0-30、阶段0-5的完整消耗表。
所有材料消耗量已乘以11（11件装备）。
"""

import customtkinter as ctk
from pages.base_tool import BaseToolPage
from calculators.calc_c import (
    REFORGE_DATA, MATERIAL_CONVERSION, MATERIAL_B_NAME, EQUIPMENT_COUNT,
    find_data_index, format_num,
    calc_reforge_by_materials, calc_materials_for_target,
)


class ToolCPage(BaseToolPage):
    """装备重铸计算器界面（11件装备）"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, colors)
        self._build_ui()

    def _build_ui(self):
        """构建重铸计算器界面"""
        # 主滚动容器
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # ---- 页面标题 ----
        ctk.CTkLabel(
            scroll,
            text="⚔️ 装备重铸计算器",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        ctk.CTkLabel(
            scroll,
            text=f"支持 11 件装备同时重铸 · 等级 0-30 · 阶段 0-5",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # ---- 标签页切换 ----
        tab_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["📊 根据材料计算等级", "🎯 根据目标计算材料"],
            height=34,
            font=ctk.CTkFont(size=13),
            selected_color=self.colors["nav_active"],
            unselected_color="#0f0f1a",
            selected_hover_color="#164080",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("📊 根据材料计算等级")

        # ---- Tab 1：根据材料计算等级 ----
        self.tab1_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        tab1_inner = ctk.CTkFrame(self.tab1_frame, fg_color="transparent")
        tab1_inner.pack(fill="x", padx=20, pady=18)
        tab1_inner.grid_columnconfigure((0, 1), weight=1)

        # 初始状态标题
        ctk.CTkLabel(
            tab1_inner, text="初始重铸状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        # 初始等级
        ctk.CTkLabel(tab1_inner, text="初始等级 (0-30)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t1_initial_level = ctk.CTkEntry(tab1_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_initial_level.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        self.t1_initial_level.insert(0, "0")

        # 初始阶段
        ctk.CTkLabel(tab1_inner, text="初始阶段 (0-5)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t1_initial_stage = ctk.CTkEntry(tab1_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_initial_stage.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.t1_initial_stage.insert(0, "0")

        # 材料类型
        ctk.CTkLabel(tab1_inner, text="重铸材料A类型",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(6, 3))

        self.t1_mat_type = ctk.CTkOptionMenu(
            tab1_inner,
            values=[
                "不灭离炎",
                "青璃焰光",
                "冥雷寒铁",
                "辉光玄铁",
                "坠影紫晶",
                "绯云玄晶",
            ],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t1_mat_type.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # 材料数量
        ctk.CTkLabel(tab1_inner, text="重铸A材料数量",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=5, column=0, sticky="w", padx=(0, 10), pady=(6, 3))
        self.t1_material_a = ctk.CTkEntry(tab1_inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_material_a.grid(row=6, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

        ctk.CTkLabel(tab1_inner, text="保底材料B数量",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=5, column=1, sticky="w", padx=(10, 0), pady=(6, 3))
        self.t1_material_b = ctk.CTkEntry(tab1_inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_material_b.grid(row=6, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))

        # 计算按钮
        ctk.CTkButton(
            tab1_inner,
            text="▶  计算可达到的重铸等级",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#0f3460", hover_color="#16213e",
            command=self._calc_reforge_by_materials,
        ).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(8, 8))

        # 结果区域
        self.t1_result = ctk.CTkTextbox(
            tab1_inner, height=160, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
        )
        self.t1_result.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")

        # ---- Tab 2：根据目标计算材料 ----
        self.tab2_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        # 不立即 grid，由标签页切换控制

        tab2_inner = ctk.CTkFrame(self.tab2_frame, fg_color="transparent")
        tab2_inner.pack(fill="x", padx=20, pady=18)
        tab2_inner.grid_columnconfigure((0, 1), weight=1)

        # 初始状态
        ctk.CTkLabel(
            tab2_inner, text="初始重铸状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ctk.CTkLabel(tab2_inner, text="初始等级 (0-30)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t2_start_level = ctk.CTkEntry(tab2_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_start_level.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        self.t2_start_level.insert(0, "0")

        ctk.CTkLabel(tab2_inner, text="初始阶段 (0-5)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t2_start_stage = ctk.CTkEntry(tab2_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_start_stage.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.t2_start_stage.insert(0, "0")

        # 目标状态
        ctk.CTkLabel(
            tab2_inner, text="目标重铸状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 8))

        ctk.CTkLabel(tab2_inner, text="目标等级 (0-30)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=4, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t2_target_level = ctk.CTkEntry(tab2_inner, placeholder_text="30", height=32, corner_radius=6)
        self.t2_target_level.grid(row=5, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        self.t2_target_level.insert(0, "30")

        ctk.CTkLabel(tab2_inner, text="目标阶段 (0-5)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=4, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t2_target_stage = ctk.CTkEntry(tab2_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_target_stage.grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.t2_target_stage.insert(0, "0")

        # 基准材料类型
        ctk.CTkLabel(tab2_inner, text="基准材料类型",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(6, 3))

        self.t2_mat_type = ctk.CTkOptionMenu(
            tab2_inner,
            values=[
                "不灭离炎",
                "青璃焰光",
                "冥雷寒铁",
                "辉光玄铁",
                "坠影紫晶",
                "绯云玄晶",
            ],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t2_mat_type.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # 计算按钮
        ctk.CTkButton(
            tab2_inner,
            text="▶  计算所需材料",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#2e7d32", hover_color="#1b5e20",
            command=self._calc_materials_for_target,
        ).grid(row=8, column=0, columnspan=2, sticky="ew", pady=(8, 8))

        # 结果区域
        self.t2_result = ctk.CTkTextbox(
            tab2_inner, height=220, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
        )
        self.t2_result.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.t2_result.insert("1.0", "等待计算...\n")
        self.t2_result.configure(state="disabled")

        # ---- 材料转换说明 ----
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            info_inner,
            text="📖 材料转换关系",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).pack(fill="x", pady=(0, 8))

        rules = [
            "· 青璃焰光 = 不灭离炎 × 3",
            "· 冥雷寒铁 = 不灭离炎 × 9",
            "· 辉光玄铁 = 不灭离炎 × 27",
            "· 坠影紫晶和绯云玄晶不可转换",
            "",
            f"⚠ 所有消耗量已 × {EQUIPMENT_COUNT}（{EQUIPMENT_COUNT} 件装备）",
        ]
        for rule in rules:
            ctk.CTkLabel(
                info_inner, text=rule,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"], anchor="w",
            ).pack(fill="x", pady=1)

    # ================================================================
    # 标签页切换
    # ================================================================

    def _on_tab_change(self, value):
        """切换标签页"""
        if value == "📊 根据材料计算等级":
            self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2_frame.grid_forget()
        else:
            self.tab2_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1_frame.grid_forget()

    # ================================================================
    # 辅助方法
    # ================================================================

    @staticmethod
    def _find_data_index(level: int, stage: int) -> int:
        """在 REFORGE_DATA 中查找指定等级和阶段的索引（O(1) 字典查找）"""
        return find_data_index(level, stage)

    @staticmethod
    def _format_num(num: float) -> str:
        """格式化数字显示"""
        return format_num(num)

    # ================================================================
    # 功能一：根据材料量计算可达到的重铸等级
    # ================================================================

    def _calc_reforge_by_materials(self):
        """根据拥有的材料量计算可达到的最高重铸等级/阶段"""
        # --- 获取输入 ---
        try:
            init_level = int(self.t1_initial_level.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的初始等级 (0-30)")
            return

        try:
            init_stage = int(self.t1_initial_stage.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的初始阶段 (0-5)")
            return

        mat_type = self.t1_mat_type.get()
        if not mat_type:
            self._show_error(self.t1_result, "请选择重铸材料A类型")
            return

        mat_a_input = self.t1_material_a.get().strip()
        mat_b_input = self.t1_material_b.get().strip()

        has_mat_a = mat_a_input != ""
        has_mat_b = mat_b_input != ""

        if not has_mat_a and not has_mat_b:
            self._show_error(self.t1_result, "材料A数量和保底材料B不能同时为空")
            return

        try:
            remaining_a = float(mat_a_input) if has_mat_a else float("inf")
            remaining_b = float(mat_b_input) if has_mat_b else float("inf")
        except ValueError:
            self._show_error(self.t1_result, "材料数量请输入有效数字")
            return

        # 校验范围
        if not (0 <= init_level <= 30):
            self._show_error(self.t1_result, "初始等级必须在 0-30 之间")
            return
        if not (0 <= init_stage <= 5):
            self._show_error(self.t1_result, "初始阶段必须在 0-5 之间")
            return

        # --- 调用计算引擎 ---
        result = calc_reforge_by_materials(init_level, init_stage, mat_type, remaining_a, remaining_b)
        if result["error"]:
            self._show_error(self.t1_result, result["error"])
            return

        current_level = result["current_level"]
        current_stage = result["current_stage"]
        total_used_a = result["total_used_a"]
        total_used_b = result["total_used_b"]
        rem_a = result["remaining_a"]
        rem_b = result["remaining_b"]

        # --- 构建结果文本 ---
        lines = []
        lines.append(f"━━━ 重铸结果 ━━━")
        lines.append(f"\n最高可达到：{current_level} 级 {current_stage} 阶段")
        lines.append(f"(从 {init_level} 级 {init_stage} 阶段出发)")
        lines.append(f"\n━━━ 累计消耗 ━━━")
        lines.append(f"材料A ({mat_type}): {self._format_num(total_used_a)}")
        lines.append(f"材料B ({MATERIAL_B_NAME}): {self._format_num(total_used_b)}")

        if rem_a != float("inf") and rem_a > 0.0001:
            lines.append(f"\n剩余材料A: {self._format_num(rem_a)}")
        if rem_b != float("inf") and rem_b > 0.0001:
            lines.append(f"剩余材料B: {self._format_num(rem_b)}")

        lines.append(f"\n(以上为 {EQUIPMENT_COUNT} 件装备的总消耗)")

        self._show_result(self.t1_result, "\n".join(lines) + "\n")

    # ================================================================
    # 功能二：根据目标等级计算所需材料
    # ================================================================

    def _calc_materials_for_target(self):
        """计算从初始状态升级到目标状态所需的各种材料量"""
        # --- 获取输入 ---
        try:
            start_level = int(self.t2_start_level.get() or "0")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的初始等级 (0-30)")
            return

        try:
            start_stage = int(self.t2_start_stage.get() or "0")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的初始阶段 (0-5)")
            return

        try:
            target_level = int(self.t2_target_level.get() or "30")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的目标等级 (0-30)")
            return

        try:
            target_stage = int(self.t2_target_stage.get() or "0")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的目标阶段 (0-5)")
            return

        target_mat_type = self.t2_mat_type.get()

        # 校验范围
        if not (0 <= start_level <= 30):
            self._show_error(self.t2_result, "初始等级必须在 0-30 之间")
            return
        if not (0 <= start_stage <= 5):
            self._show_error(self.t2_result, "初始阶段必须在 0-5 之间")
            return
        if not (0 <= target_level <= 30):
            self._show_error(self.t2_result, "目标等级必须在 0-30 之间")
            return
        if not (0 <= target_stage <= 5):
            self._show_error(self.t2_result, "目标阶段必须在 0-5 之间")
            return

        if (target_level < start_level) or (target_level == start_level and target_stage <= start_stage):
            self._show_error(self.t2_result, "目标等级/阶段必须大于初始等级/阶段")
            return

        # --- 调用计算引擎 ---
        result = calc_materials_for_target(start_level, start_stage, target_level, target_stage, target_mat_type)
        if result["error"]:
            self._show_error(self.t2_result, result["error"])
            return

        total_materials = result["total_materials"]
        converted_total = result["converted_total"]
        stages_count = result["stages_count"]

        # --- 构建结果文本 ---
        lines = []
        lines.append(f"━━━ 材料需求 ━━━")
        lines.append(f"\n从 {start_level} 级 {start_stage} 阶段 → {target_level} 级 {target_stage} 阶段")
        lines.append(f"共需提升 {stages_count} 个阶段\n")

        lines.append("┌─────────────────────────────┐")
        lines.append("│ 各材料原始需求 (×11件)       │")
        lines.append("├─────────────────────────────┤")

        has_materials = False
        for mname, amt in total_materials.items():
            if amt > 0.0001:
                has_materials = True
                lines.append(f"│ {mname:<12}{self._format_num(amt):>15} │")

        if not has_materials:
            lines.append("│ 无需升级                      │")

        lines.append("└─────────────────────────────┘")

        if converted_total > 0.0001:
            lines.append(f"\n▸ 转换为 [{target_mat_type}] 总计: {self._format_num(converted_total)}")

        lines.append(f"\n(以上为 {EQUIPMENT_COUNT} 件装备的总消耗)")

        self._show_result(self.t2_result, "\n".join(lines) + "\n")
