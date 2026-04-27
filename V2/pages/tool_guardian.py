"""
守护神养成计算器 v4
支持两种模式：
1. 简单模式：输入平均星级 → 消耗最少/最常见方案
2. 精确模式：输入各守护神星级 → 精确消耗
"""

import customtkinter as ctk
from pages.base_tool import BaseToolPage
from calculators.calc_guardian import (
    GROUPS, QUALITY_COLORS, STAR_CUM,
    get_group_names, get_group_guardians, get_group_ticket, get_exp_per_ticket,
    calc_simple, calc_precise,
)


class ToolGuardian(BaseToolPage):
    """守护神养成计算器"""

    def __init__(self, parent, colors=None):
        super().__init__(parent, colors)
        self._precise_entries = {}  # 精确模式的输入框
        self._build_ui()

    # ================================================================
    #  UI 构建
    # ================================================================
    def _build_ui(self):
        scroll = self._create_scroll_container()

        # 标题
        self._create_title(
            scroll,
            "🛡️ 守护神养成计算器",
            "基于真实出货概率 + 幸运值保底 + 次数保底，计算各守护神所需请神符（期望值）",
            row=0,
        )

        # 标签页切换
        self.tab_seg = self._create_tab_switcher(
            scroll,
            ["📊 简单模式（平均星级）", "🎯 精确模式（各守护神星级）"],
            row=2,
        )

        # Tab 1: 简单模式
        self.tab1 = self._create_tab_frame(scroll, row=3, visible=True)
        self._build_tab_simple()

        # Tab 2: 精确模式
        self.tab2 = self._create_tab_frame(scroll, row=3, visible=False)
        self._build_tab_precise()

        # 使用说明
        self._create_info_section(scroll, "养成说明", [
            "• 简单模式：输入当前/目标平均星级，AI展开为两种分布方案",
            "  → 消耗最少方案 = 当前最乐观 + 目标最悲观（缺口最小）",
            "  → 最常见方案 = 按期望残念速率比例加权分配（最贴近实际情况）",
            "",
            "• 精确模式：精确输入各守护神当前和目标星级，获得精确消耗",
            "",
            "核心机制：",
            "  - 总消耗 = 最慢到位守护神的独立需求（并行模型，非各守护神求和）",
            "  - 升星消耗残念：0→1星(20) / 1→2星(40) / 2→3星(80) / 3→4星(160) / 4→5星(供奉解锁,0)",
            "  - 每次请神若抽到已有守护神，获得 10 个残念",
            "  - 请神符基于【真实出货概率 + 幸运值保底 + 次数保底】计算期望值",
            "  - 紫/金品质守护神出货概率极低，建议配合精华路径",
            "",
            "精华流转：",
            "  - 满5星后多余残念可分解为精华（残念数 × 精华单价）",
            "  - 精华只在同组内流转，优先补贴精华单价最高的守护神",
        ], row=4)

    # ────────────────────────────────────────────────
    #  Tab 1 : 简单模式
    # ────────────────────────────────────────────────
    def _build_tab_simple(self):
        inner = self._create_tab_inner(self.tab1, columns=2)
        row = 0

        # 选择神仙谱组
        self._create_section_title(inner, "选择神仙谱组", row=row)
        row += 1

        self._create_input_label(inner, "神仙谱组", row=row, column=0, padx=(0, 10))
        row += 1

        group_names = get_group_names()
        self.t1_group_menu = self._create_input_option(
            inner, row=row, column=0, values=group_names,
            padx=(0, 10), columnspan=2,
            command=self._on_group_change_t1,
        )
        self.t1_group_menu.set(group_names[0])
        row += 1

        # 星级设置
        self._create_section_title(inner, "星级设置", row=row)
        row += 1

        self._create_input_label(inner, "当前平均星级（0.0 ~ 5.0）",
                                 row=row, column=0, padx=(0, 10))
        self._create_input_label(inner, "目标平均星级（0.0 ~ 5.0）",
                                 row=row, column=1, padx=(10, 0))
        row += 1

        self.t1_cur_avg = self._create_input_entry(
            inner, row=row, column=0, placeholder="0.0", default="0",
            padx=(0, 10))
        self.t1_tgt_avg = self._create_input_entry(
            inner, row=row, column=1, placeholder="5.0", default="5",
            padx=(10, 0))
        row += 1

        # 可选：持有精华
        self._create_section_title(inner, "已有资源（可选）", row=row)
        row += 1

        self._create_input_label(inner, "持有精华数量", row=row, column=0, padx=(0, 10))
        row += 1

        self.t1_essence = self._create_input_entry(
            inner, row=row, column=0, placeholder="0（不填默认0）", default="0",
            padx=(0, 10), columnspan=2)
        row += 1

        # 计算按钮
        self._create_calc_button(inner, text="▶  计算请神符消耗",
                                 command=self._calc_simple, row=row)
        row += 1

        # 结果区域
        self.t1_result = self._create_result_box(inner, row=row, height=350)

    # ────────────────────────────────────────────────
    #  Tab 2 : 精确模式
    # ────────────────────────────────────────────────
    def _build_tab_precise(self):
        inner = self._create_tab_inner(self.tab2, columns=2)
        row = 0

        # 选择神仙谱组
        self._create_section_title(inner, "选择神仙谱组", row=row)
        row += 1

        self._create_input_label(inner, "神仙谱组", row=row, column=0, padx=(0, 10))
        row += 1

        group_names = get_group_names()
        self.t2_group_menu = self._create_input_option(
            inner, row=row, column=0, values=group_names,
            padx=(0, 10), columnspan=2,
            command=self._on_group_change_t2,
        )
        self.t2_group_menu.set(group_names[0])
        row += 1

        # 各守护神星级输入区域
        self._create_section_title(inner, "各守护神星级", row=row)
        row += 1

        self.t2_guardian_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t2_guardian_frame.grid(row=row, column=0, columnspan=2,
                                    sticky="ew", pady=(0, 8))
        self._t2_guardian_row = row
        row += 1

        # 初始化守护神输入
        self._rebuild_precise_inputs(group_names[0])

        # 可选：持有精华
        self._create_section_title(inner, "已有资源（可选）", row=row)
        row += 1

        self._create_input_label(inner, "持有精华数量", row=row, column=0, padx=(0, 10))
        row += 1

        self.t2_essence = self._create_input_entry(
            inner, row=row, column=0, placeholder="0", default="0",
            padx=(0, 10), columnspan=2)
        row += 1

        # 计算按钮
        self._create_calc_button(inner, text="▶  精确计算请神符消耗",
                                 command=self._calc_precise, row=row)
        row += 1

        # 结果区域
        self.t2_result = self._create_result_box(inner, row=row, height=350)

    def _rebuild_precise_inputs(self, group_name: str):
        """重建精确模式的守护神星级输入控件"""
        # 清除旧控件
        for widget in self.t2_guardian_frame.winfo_children():
            widget.destroy()
        self._precise_entries = {}

        guardians = get_group_guardians(group_name)
        # 4列：名称、品质、当前星级、目标星级
        self.t2_guardian_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # 表头
        headers = ["守护神", "品质", "当前星级", "目标星级"]
        for j, h in enumerate(headers):
            ctk.CTkLabel(
                self.t2_guardian_frame, text=h,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=self.colors["text_dim"],
            ).grid(row=0, column=j, sticky="w", padx=5, pady=(0, 5))

        star_values = ["0", "1", "2", "3", "4", "5"]
        for i, g in enumerate(guardians):
            r = i + 1
            color = QUALITY_COLORS.get(g["quality"], "#ffffff")

            ctk.CTkLabel(
                self.t2_guardian_frame, text=g["name"],
                font=ctk.CTkFont(size=12),
                text_color=color,
            ).grid(row=r, column=0, sticky="w", padx=5, pady=2)

            ctk.CTkLabel(
                self.t2_guardian_frame, text=g["quality"],
                font=ctk.CTkFont(size=11),
                text_color=color,
            ).grid(row=r, column=1, sticky="w", padx=5, pady=2)

            cur_var = ctk.StringVar(value="0")
            cur_menu = ctk.CTkOptionMenu(
                self.t2_guardian_frame, variable=cur_var,
                values=star_values, width=70, height=28,
                fg_color=self.BTN_PRIMARY,
                button_color=self.BTN_PRIMARY,
                button_hover_color=self.BTN_PRIMARY_HOVER,
            )
            cur_menu.grid(row=r, column=2, padx=5, pady=2)

            tgt_var = ctk.StringVar(value="5")
            tgt_menu = ctk.CTkOptionMenu(
                self.t2_guardian_frame, variable=tgt_var,
                values=star_values, width=70, height=28,
                fg_color=self.BTN_PRIMARY,
                button_color=self.BTN_PRIMARY,
                button_hover_color=self.BTN_PRIMARY_HOVER,
            )
            tgt_menu.grid(row=r, column=3, padx=5, pady=2)

            self._precise_entries[g["name"]] = {
                "cur_var": cur_var,
                "tgt_var": tgt_var,
            }

    # ================================================================
    #  事件回调
    # ================================================================
    def _on_group_change_t1(self, _value):
        """简单模式切换组"""
        pass  # 无需额外操作

    def _on_group_change_t2(self, _value):
        """精确模式切换组：重建输入控件"""
        group_name = self.t2_group_menu.get()
        self._rebuild_precise_inputs(group_name)

    # ================================================================
    #  简单模式计算
    # ================================================================
    def _calc_simple(self):
        group_name = self.t1_group_menu.get()

        try:
            cur_avg = float(self.t1_cur_avg.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的当前平均星级")
            return

        try:
            tgt_avg = float(self.t1_tgt_avg.get() or "5")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的目标平均星级")
            return

        try:
            held_essence = int(self.t1_essence.get() or "0")
        except ValueError:
            held_essence = 0

        result = calc_simple(group_name, cur_avg, tgt_avg,
                             held_essence=held_essence)

        if result.get("error"):
            self._show_error(self.t1_result, result["error"])
            return

        output = self._format_simple_result(result)
        self._show_result(self.t1_result, output)

    def _format_simple_result(self, result: dict) -> str:
        """格式化简单模式结果"""
        gn = result["group_name"]
        cur_avg = result["cur_avg"]
        tgt_avg = result["tgt_avg"]
        guardians = get_group_guardians(gn)
        ticket_name = get_group_ticket(gn)

        lines = []
        lines.append(f"【{gn}组 养成计算】")
        lines.append(f"")
        lines.append(f"当前平均星级：{cur_avg}星 → 目标平均星级：{tgt_avg}星")
        lines.append(f"使用道具：{ticket_name}")
        lines.append("")

        # ---- 消耗最少方案 ----
        plan_min = result["plan_min"]
        lines.append("━━━ 消耗最少方案 ━━━")
        lines.append(self._format_plan(gn, plan_min))
        lines.append("")

        # ---- 最常见方案 ----
        plan_typical = result["plan_typical"]
        lines.append("━━━ 最常见方案 ━━━")
        lines.append(self._format_plan(gn, plan_typical))
        lines.append("")

        # 消耗区间
        t_min, t_max = result["ticket_range"]
        t_typical = result["plan_typical"]["total_tickets"]
        lines.append("━━━━━━━━━━━━━━━━━━")
        lines.append(f"📊 消耗参考：最少 {t_min:,} 张{ticket_name} | 常见 {t_typical:,} 张{ticket_name}")

        return "\n".join(lines)

    def _format_plan(self, group_name: str, plan: dict) -> str:
        """格式化一个方案的显示"""
        guardians = get_group_guardians(group_name)
        ticket_name = get_group_ticket(group_name)
        details = plan["details"]
        cur_dist = plan.get("cur_distribution", [])
        tgt_dist = plan.get("tgt_distribution", [])

        lines = []

        # 分布展示
        if cur_dist:
            cur_parts = [f"{guardians[i]['name']}: {cur_dist[i]}星"
                         for i in range(len(guardians))]
            lines.append(f"当前分布：{' / '.join(cur_parts)}")

        if tgt_dist:
            tgt_parts = [f"{guardians[i]['name']}: {tgt_dist[i]}星"
                         for i in range(len(guardians))]
            lines.append(f"目标分布：{' / '.join(tgt_parts)}")

        lines.append("")
        lines.append("各守护神消耗：")

        for d in details:
            name = d["name"]
            quality = d["quality"]
            exp = d["exp_per_ticket"]
            cur = d["cur_star"]
            tgt = d["tgt_star"]
            gap = d["gap"]
            subsidy = d.get("essence_subsidy", 0)
            tickets = d["tickets"]

            if gap == 0 and d["need"] <= 0:
                lines.append(f"  {name}({quality}, {exp}残念/张)："
                             f"已达目标，消耗0张")
            elif tickets == 0 and subsidy > 0:
                lines.append(f"  {name}({quality}, {exp}残念/张)："
                             f"残念缺口{d['need']}，精华补贴{subsidy}残念，消耗0张")
            else:
                extra = ""
                if subsidy > 0:
                    extra = f"（精华补贴{subsidy}残念）"
                lines.append(f"  {name}({quality}, {exp}残念/张)："
                             f"残念缺口{d['need']}，需{ticket_name}{tickets:,}张{extra}")

        total = plan["total_tickets"]
        lines.append(f"\n合计{ticket_name}：约 {total:,} 张")

        # 精华流转说明
        ef = plan.get("essence_flow", {})
        if ef.get("beneficiaries"):
            lines.append("")
            lines.append("精华流转：")
            for b in ef["beneficiaries"]:
                lines.append(f"  精华购买 {b['name']} 残念 {b['bought_remnant']} 个"
                             f"（消耗精华 {b['cost_essence']:,}）")

        return "\n".join(lines)

    # ================================================================
    #  精确模式计算
    # ================================================================
    def _calc_precise(self):
        group_name = self.t2_group_menu.get()
        guardians = get_group_guardians(group_name)

        cur_stars = []
        tgt_stars = []
        for g in guardians:
            entry = self._precise_entries.get(g["name"])
            if not entry:
                self._show_error(self.t2_result, f"找不到 {g['name']} 的输入")
                return
            try:
                cur_stars.append(int(entry["cur_var"].get()))
                tgt_stars.append(int(entry["tgt_var"].get()))
            except ValueError:
                self._show_error(self.t2_result, f"{g['name']} 星级必须是整数")
                return

        try:
            held_essence = int(self.t2_essence.get() or "0")
        except ValueError:
            held_essence = 0

        result = calc_precise(group_name, cur_stars, tgt_stars,
                              held_essence=held_essence)

        if result.get("error"):
            self._show_error(self.t2_result, result["error"])
            return

        output = self._format_precise_result(group_name, result)
        self._show_result(self.t2_result, output)

    def _format_precise_result(self, group_name: str, result: dict) -> str:
        """格式化精确模式结果"""
        guardians = get_group_guardians(group_name)
        ticket_name = get_group_ticket(group_name)
        details = result["details"]

        lines = []
        lines.append(f"【精确计算：{group_name}组】")
        lines.append("")

        # 当前/目标状态
        cur_parts = [f"{d['name']}{d['cur_star']}星" for d in details]
        tgt_parts = [f"{d['name']}{d['tgt_star']}星" for d in details]
        lines.append(f"当前：{' / '.join(cur_parts)}")
        lines.append(f"目标：{' / '.join(tgt_parts)}")
        lines.append(f"使用道具：{ticket_name}")
        lines.append("")

        lines.append("各守护神消耗（基于真实概率+保底）：")
        for d in details:
            name = d["name"]
            gap = d["gap"]
            tickets = d["tickets"]
            exp = d["exp_per_ticket"]
            subsidy = d.get("essence_subsidy", 0)

            if gap == 0 and d["need"] <= 0:
                lines.append(f"  {name}：已达目标，消耗0张")
            else:
                extra = ""
                if subsidy > 0:
                    extra = f"（精华补贴{subsidy}残念）"
                lines.append(f"  {name}：缺口{d['need']}，"
                             f"期望{tickets:,}张（{exp}残念/张）{extra}")

        total = result["total_tickets"]
        lines.append(f"\n合计{ticket_name}：精确 {total:,} 张（期望值）")

        # 精华流转说明
        ef = result.get("essence_flow", {})
        if ef.get("beneficiaries"):
            lines.append("")
            lines.append("精华流转：")
            for b in ef["beneficiaries"]:
                lines.append(f"  精华购买 {b['name']} 残念 {b['bought_remnant']} 个"
                             f"（消耗精华 {b['cost_essence']:,}）")

        return "\n".join(lines)
