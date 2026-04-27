"""
装备淬炼计算器模块
根据材料量计算可达成淬炼等级，或根据目标等级计算所需材料。
"""

import customtkinter as ctk
from pages.base_tool import BaseToolPage
from calculators.calc_b import (
    MATERIAL_NAMES, MATERIAL2_NAME, REFINING_DATA,
    to_lowest_material, from_lowest_material, format_number,
    calc_max_level, calc_materials_for_target,
)


class ToolBPage(BaseToolPage):
    """装备淬炼计算器界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, colors)
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

        # 调用计算引擎
        result = calc_max_level(start_level, mat1_type, mat1_lowest, mat2_count)
        current_level = result["current_level"]
        used_mat1_lowest = result["used_mat1_lowest"]
        used_mat2 = result["used_mat2"]
        details = result["details"]

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

        # 调用计算引擎
        result = calc_materials_for_target(start_level, target_level)
        total_mat1_lowest = result["total_mat1_lowest"]
        total_mat2 = result["total_mat2"]
        mat1_type_usage = result["mat1_type_usage"]
        highest_mat1_type = result["highest_mat1_type"]

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
