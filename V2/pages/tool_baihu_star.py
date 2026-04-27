"""
白虎星图锤炼计算器
支持两种计算模式：
  模式一：根据目标计算消耗 — 输入当前/目标状态 → 计算所需锤炼材料和保底材料
  模式二：根据材料反推等级 — 输入持有材料数量 → 计算可达到的最高重数和等级
"""

import math
import customtkinter as ctk
from pages.base_tool import BaseToolPage
from calculators.calc_baihu_star import (
    MAX_WEIGHT, MAX_LEVEL, GUARANTEE_MAT,
    get_official_names, find_official,
    calc_material_cost, calc_max_reachable,
)


class ToolBaihuStar(BaseToolPage):
    """白虎星图锤炼计算器"""

    def __init__(self, parent, colors: dict = None):
        super().__init__(parent, colors)
        self._build_ui()

    # ================================================================
    #  UI 构建
    # ================================================================
    def _build_ui(self):
        scroll = self._create_scroll_container()

        # 标题
        self._create_title(
            scroll,
            "🐯 白虎星图锤炼计算器",
            "奎木狼 / 胃土雉 / 娄金星官 · 锤炼期望消耗 · 默认使用保底材料",
            row=0,
        )

        # Tab 切换
        self.tab_seg = self._create_tab_switcher(
            scroll,
            ["🎯 根据目标计算消耗", "📦 根据材料反推等级"],
            row=2,
        )

        # Tab 1: 目标消耗
        self.tab1 = self._create_tab_frame(scroll, row=3, visible=True)
        self._build_tab1()

        # Tab 2: 材料反推
        self.tab2 = self._create_tab_frame(scroll, row=3, visible=False)
        self._build_tab2()

        # 说明区域
        self._create_info_section(scroll, "锤炼说明", [
            "• 白虎星图分为奎木狼、胃土雉、娄金星官三个星官",
            "• 每个星官 10 重 × 6 级，锤炼为概率事件",
            "• 每次锤炼消耗锤炼材料（各星官不同）+ 保底材料（白虎之灵，通用）",
            "• 保底材料可保证锤炼失败时不降级，计算时默认使用",
            "• 计算结果为期望值（基于保底期望次数），实际消耗可能有偏差",
            "",
            "材料对应：",
            "  - 奎木狼：奎木星砂 + 白虎之灵",
            "  - 胃土雉：胃土星砂 + 白虎之灵",
            "  - 娄金星官：娄金星砂 + 白虎之灵",
        ], row=4)

    # ────────────────────────────────────────────
    #  Tab 1 : 根据目标计算消耗
    # ────────────────────────────────────────────
    def _build_tab1(self):
        inner = self._create_tab_inner(self.tab1, columns=2)
        row = 0

        # 选择星官
        self._create_section_title(inner, "选择星官", row=row)
        row += 1

        official_names = get_official_names()
        self.t1_official = self._create_input_option(
            inner, row=row, column=0, values=official_names,
            padx=(0, 10), columnspan=2,
        )
        self.t1_official.set(official_names[0])
        row += 1

        # 当前状态
        self._create_section_title(inner, "当前状态", row=row)
        row += 1

        self._create_input_label(inner, f"当前重数（0=未开始, 0~{MAX_WEIGHT}）",
                                 row=row, column=0, padx=(0, 10))
        self._create_input_label(inner, f"当前等级（0=未开始, 0~{MAX_LEVEL}）",
                                 row=row, column=1, padx=(10, 0))
        row += 1

        self.t1_cur_w = self._create_input_entry(
            inner, row=row, column=0, placeholder="0", default="0", padx=(0, 10))
        self.t1_cur_l = self._create_input_entry(
            inner, row=row, column=1, placeholder="0", default="0", padx=(10, 0))
        row += 1

        # 目标状态
        self._create_section_title(inner, "目标状态", row=row)
        row += 1

        self._create_input_label(inner, f"目标重数（1~{MAX_WEIGHT}）",
                                 row=row, column=0, padx=(0, 10))
        self._create_input_label(inner, f"目标等级（1~{MAX_LEVEL}）",
                                 row=row, column=1, padx=(10, 0))
        row += 1

        self.t1_tgt_w = self._create_input_entry(
            inner, row=row, column=0, placeholder="10", default="10", padx=(0, 10))
        self.t1_tgt_l = self._create_input_entry(
            inner, row=row, column=1, placeholder="6", default="6", padx=(10, 0))
        row += 1

        # 计算按钮
        self._create_calc_button(inner, text="▶  计算材料消耗",
                                 command=self._calc_cost, row=row)
        row += 1

        # 结果区域
        self.t1_result = self._create_result_box(inner, row=row, height=350)

    # ────────────────────────────────────────────
    #  Tab 2 : 根据材料反推等级
    # ────────────────────────────────────────────
    def _build_tab2(self):
        inner = self._create_tab_inner(self.tab2, columns=2)
        row = 0

        # 选择星官
        self._create_section_title(inner, "选择星官", row=row)
        row += 1

        official_names = get_official_names()
        self.t2_official = self._create_input_option(
            inner, row=row, column=0, values=official_names,
            padx=(0, 10), columnspan=2,
        )
        self.t2_official.set(official_names[0])
        row += 1

        # 当前状态
        self._create_section_title(inner, "当前状态", row=row)
        row += 1

        self._create_input_label(inner, f"当前重数（0=未开始, 0~{MAX_WEIGHT}）",
                                 row=row, column=0, padx=(0, 10))
        self._create_input_label(inner, f"当前等级（0=未开始, 0~{MAX_LEVEL}）",
                                 row=row, column=1, padx=(10, 0))
        row += 1

        self.t2_cur_w = self._create_input_entry(
            inner, row=row, column=0, placeholder="0", default="0", padx=(0, 10))
        self.t2_cur_l = self._create_input_entry(
            inner, row=row, column=1, placeholder="0", default="0", padx=(10, 0))
        row += 1

        # 持有材料
        self._create_section_title(inner, "持有材料", row=row)
        row += 1

        self._create_input_label(inner, "锤炼材料数量（星砂）",
                                 row=row, column=0, padx=(0, 10))
        self._create_input_label(inner, f"保底材料数量（{GUARANTEE_MAT}）",
                                 row=row, column=1, padx=(10, 0))
        row += 1

        self.t2_hammer = self._create_input_entry(
            inner, row=row, column=0, placeholder="10000", default="10000", padx=(0, 10))
        self.t2_guarantee = self._create_input_entry(
            inner, row=row, column=1, placeholder="5000", default="5000", padx=(10, 0))
        row += 1

        # 计算按钮
        self._create_calc_button(inner, text="▶  计算可达等级",
                                 command=self._calc_reachable, row=row)
        row += 1

        # 结果区域
        self.t2_result = self._create_result_box(inner, row=row, height=350)

    # ================================================================
    #  Tab 1 计算：目标消耗
    # ================================================================
    def _calc_cost(self):
        official = self.t1_official.get()

        try:
            cur_w = self._parse_int(self.t1_cur_w.get(), 0)
            cur_l = self._parse_int(self.t1_cur_l.get(), 0)
            tgt_w = self._parse_int(self.t1_tgt_w.get(), 10)
            tgt_l = self._parse_int(self.t1_tgt_l.get(), 6)
        except Exception:
            self._show_error(self.t1_result, "请输入有效数字")
            return

        # 输入校验
        if cur_w == 0 and cur_l == 0:
            pass  # 未开始状态，合法
        elif not (1 <= cur_w <= MAX_WEIGHT and 1 <= cur_l <= MAX_LEVEL):
            self._show_error(self.t1_result,
                             f"当前状态无效：重数 1~{MAX_WEIGHT}，等级 1~{MAX_LEVEL}（或 0重0级表示未开始）")
            return

        if not (1 <= tgt_w <= MAX_WEIGHT and 1 <= tgt_l <= MAX_LEVEL):
            self._show_error(self.t1_result,
                             f"目标状态无效：重数 1~{MAX_WEIGHT}，等级 1~{MAX_LEVEL}")
            return

        result = calc_material_cost(official, cur_w, cur_l, tgt_w, tgt_l)

        if result.get("error"):
            self._show_error(self.t1_result, result["error"])
            return

        output = self._format_cost_result(result)
        self._show_result(self.t1_result, output)

    def _format_cost_result(self, r: dict) -> str:
        """格式化目标消耗计算结果"""
        cw, cl = r["cur_state"]
        tw, tl = r["tgt_state"]
        cur_str = f"{cw}重{cl}级" if cw > 0 else "未开始"

        lines = [
            f"━━━ 白虎星图锤炼消耗 ━━━",
            f"",
            f"星官：{r['official_name']}",
            f"从 {cur_str} → {tw}重{tl}级",
            f"",
            f"┌─────────────────────────────────┐",
            f"│ 锤炼材料（{r['hammer_material']}）",
            f"│   期望消耗：{r['total_hammer']:,.1f} 个",
            f"│   （向上取整：{math.ceil(r['total_hammer']):,} 个）",
            f"│",
            f"│ 保底材料（{r['guarantee_material']}）",
            f"│   期望消耗：{r['total_guarantee']:,.1f} 个",
            f"│   （向上取整：{math.ceil(r['total_guarantee']):,} 个）",
            f"└─────────────────────────────────┘",
            f"",
        ]

        # 按重数汇总
        weight_summary = {}
        for d in r["details"]:
            w = d["weight"]
            if w not in weight_summary:
                weight_summary[w] = {"hammer": 0.0, "guarantee": 0.0, "levels": 0}
            weight_summary[w]["hammer"] += d["hammer_total"]
            weight_summary[w]["guarantee"] += d["guarantee_total"]
            weight_summary[w]["levels"] += 1

        lines.append("各重消耗汇总：")
        for w in sorted(weight_summary.keys()):
            s = weight_summary[w]
            lines.append(
                f"  {w}重（{s['levels']}级）：{r['hammer_material']} {s['hammer']:,.1f}"
                f" + {r['guarantee_material']} {s['guarantee']:,.1f}"
            )

        return "\n".join(lines)

    # ================================================================
    #  Tab 2 计算：材料反推等级
    # ================================================================
    def _calc_reachable(self):
        official = self.t2_official.get()

        try:
            cur_w = self._parse_int(self.t2_cur_w.get(), 0)
            cur_l = self._parse_int(self.t2_cur_l.get(), 0)
            held_h = float(self.t2_hammer.get() or "0")
            held_g = float(self.t2_guarantee.get() or "0")
        except Exception:
            self._show_error(self.t2_result, "请输入有效数字")
            return

        # 输入校验
        if cur_w == 0 and cur_l == 0:
            pass
        elif not (1 <= cur_w <= MAX_WEIGHT and 1 <= cur_l <= MAX_LEVEL):
            self._show_error(self.t2_result,
                             f"当前状态无效：重数 1~{MAX_WEIGHT}，等级 1~{MAX_LEVEL}（或 0重0级表示未开始）")
            return

        if held_h < 0 or held_g < 0:
            self._show_error(self.t2_result, "材料数量不能为负数")
            return

        result = calc_max_reachable(official, cur_w, cur_l, held_h, held_g)

        if result.get("error"):
            self._show_error(self.t2_result, result["error"])
            return

        output = self._format_reachable_result(result)
        self._show_result(self.t2_result, output)

    def _format_reachable_result(self, r: dict) -> str:
        """格式化材料反推结果"""
        cw, cl = r["cur_state"]
        mw, ml = r["max_state"]
        cur_str = f"{cw}重{cl}级" if cw > 0 else "未开始"
        max_str = f"{mw}重{ml}级" if mw > 0 else "未开始"

        lines = [
            f"━━━ 白虎星图材料反推 ━━━",
            f"",
            f"星官：{r['official_name']}",
            f"当前状态：{cur_str}",
            f"",
            f"┌─────────────────────────────────┐",
            f"│ 🎯 可达到最高等级：{max_str}",
            f"│    共提升 {r['levels_gained']} 级",
            f"│",
            f"│ 消耗 {r['hammer_material']}：{r['used_hammer']:,.1f} 个",
            f"│ 消耗 {r['guarantee_material']}：{r['used_guarantee']:,.1f} 个",
            f"│",
            f"│ 剩余 {r['hammer_material']}：{r['remaining_hammer']:,.1f} 个",
            f"│ 剩余 {r['guarantee_material']}：{r['remaining_guarantee']:,.1f} 个",
            f"│",
            f"│ 瓶颈：{r['limiting_factor']}",
            f"└─────────────────────────────────┘",
        ]

        if r["details"]:
            lines.append("")
            lines.append("逐级消耗明细（最后10级）：")
            show_details = r["details"][-10:]
            for d in show_details:
                lines.append(
                    f"  {d['weight']}重{d['level']}级："
                    f" 星砂 {d['hammer_total']:,.1f}"
                    f" + 白虎之灵 {d['guarantee_total']:,.1f}"
                    f" （概率{d.get('base_rate', 0):.0%}, 期望{d['tries']}次）"
                )
            if len(r["details"]) > 10:
                lines.insert(-10, f"  ... 前 {len(r['details'])-10} 级已省略 ...")

        return "\n".join(lines)
