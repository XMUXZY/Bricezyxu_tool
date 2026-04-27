"""
法宝升阶养成计算器
支持两种模式：
1. 材料→进度：输入当前阶数 + 持有碎片/第二材料 → 可达阶数及剩余
2. 目标→材料：输入当前阶数 + 目标阶数 → 所需碎片 + 所需第二材料
"""

import customtkinter as ctk
from pages.base_tool import BaseToolPage
from calculators.calc_fabao import (
    FABAO_LIST, FORMATION_TYPES, FORMATION_COLORS,
    has_mat2, get_fabao_display_name, get_fabao_by_formation,
    calc_by_materials, calc_for_target,
)


class ToolFaBao(BaseToolPage):
    """法宝升阶养成计算器"""

    def __init__(self, parent, colors=None):
        super().__init__(parent, colors)
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
        first_fabaos = get_fabao_by_formation("四象阵")
        fabao_names = [get_fabao_display_name(f) for f in first_fabaos]
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

        first_fabaos = get_fabao_by_formation("四象阵")
        fabao_names = [get_fabao_display_name(f) for f in first_fabaos]
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
        fabaos = get_fabao_by_formation(formation)
        names = [get_fabao_display_name(f) for f in fabaos]
        self.t1_fabao_menu.configure(values=names)
        self.t1_fabao_var.set(names[0])
        self._update_mat2_visibility_t1()

    def _on_formation_change_t2(self, _value):
        formation = self.t2_formation_var.get()
        fabaos = get_fabao_by_formation(formation)
        names = [get_fabao_display_name(f) for f in fabaos]
        self.t2_fabao_menu.configure(values=names)
        self.t2_fabao_var.set(names[0])

    def _update_mat2_visibility_t1(self):
        """更新Tab1第二材料输入的可见性提示"""
        formation = self.t1_formation_var.get()
        if has_mat2(formation):
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
        for f in get_fabao_by_formation(formation):
            if get_fabao_display_name(f) == display_name:
                return f
        return None

    def _find_fabao_t2(self):
        """查找Tab2当前选中的法宝数据"""
        formation = self.t2_formation_var.get()
        display_name = self.t2_fabao_var.get()
        for f in get_fabao_by_formation(formation):
            if get_fabao_display_name(f) == display_name:
                return f
        return None

    # ================================================================
    #  工具方法
    # ================================================================
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

        try:
            owned_chips = int(self.t1_chip_entry.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的碎片数量")
            return

        try:
            owned_mat2 = int(self.t1_mat2_entry.get() or "0")
        except ValueError:
            owned_mat2 = 0

        # 调用 calculator 计算
        result = calc_by_materials(fabao, cur_level, owned_chips, owned_mat2)
        if result.get("error"):
            self._show_error(self.t1_result, result["error"])
            return

        reach_level = result["reach_level"]
        remaining_chips = result["remaining_chips"]
        remaining_mat2 = result["remaining_mat2"]
        stop_reason = result["stop_reason"]
        has_m2 = result["has_mat2"]
        next_info = result["next_info"]
        display_name = get_fabao_display_name(fabao)

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
        elif next_info:
            output += f"\n⏸ 停止原因: {stop_reason}\n"
            output += f"\n📋 下一阶({reach_level}→{reach_level+1}): 需碎片 {next_info['next_chip']}"
            if next_info['chip_gap'] > 0:
                output += f"（还差 {next_info['chip_gap']}）"
            if has_m2 and next_info['next_mat2'] > 0:
                output += f"，需{mat2_name} {next_info['next_mat2']}"
                if next_info['mat2_gap'] > 0:
                    output += f"（还差 {next_info['mat2_gap']}）"
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

        # 调用 calculator 计算
        result = calc_for_target(fabao, cur_level, tgt_level)
        if result.get("error"):
            self._show_error(self.t2_result, result["error"])
            return

        total_chips = result["total_chips"]
        total_mat2 = result["total_mat2"]
        has_m2 = result["has_mat2"]
        segments = result["segments"]
        display_name = get_fabao_display_name(fabao)

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
        for seg in segments:
            line = f"  {seg['from']}~{seg['to']}阶: 碎片 {seg['chips']}"
            if has_m2 and seg['mat2'] > 0:
                line += f" + {mat2_name} {seg['mat2']}"
            output += line + "\n"

        output += f"\n{'='*50}\n"
        output += f"🏆 所需材料总计:\n"
        output += f"  💎 {chip_name}: {total_chips:,} 个\n"
        if has_m2:
            output += f"  💎 {mat2_name}: {total_mat2:,} 个\n"
            if total_mat2 == 0:
                output += f"  ℹ️ 该阶数段不消耗第二材料\n"

        self._show_result(self.t2_result, output)
