"""
星录养成计算器模块
QQ华夏手游经典区 · 星录养成系统（太微/紫微/天市/启明）

支持两种计算模式：
  模式一：根据已有材料计算可达到的等级（重数+星级）
  模式二：根据目标等级计算所需材料

仅计算锤炼材料和保级材料的期望消耗，不含升重石。
数据来源：星录养成数据_AI版v2.xlsx（经典区配置表 release6.3）
"""

import customtkinter as ctk
from pages.base_tool import BaseToolPage

from calculators.calc_d import (
    XINLU_CONFIG, XINLU_NAMES, FORGE_DATA,
    get_mat_tier, get_mat_name, get_guard_exp, get_forge_exp_mat,
    calc_by_materials, calc_for_target,
)


class ToolDPage(BaseToolPage):
    """星录养成计算器界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, colors)
        self._build_ui()

    # ------------------------------------------------------------------
    # UI 构建
    # ------------------------------------------------------------------

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # 标题
        ctk.CTkLabel(scroll, text="⭐ 星录养成计算器",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(scroll, text="QQ华夏手游 · 4部星录 × 8星官 · 概率期望计算",
                     font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"], anchor="w"
                     ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # 标签页切换
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

        # Tab 1
        self.tab1 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self._build_tab1()

        # Tab 2
        self.tab2 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self._build_tab2()

        # 说明区域
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(info_inner, text="📖 养成说明", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").pack(fill="x", pady=(0, 8))

        rules = [
            "· 4部星录：太微→紫微→天市→启明，按解锁顺序依次开放",
            "· 每部星录下设8个星官，各星官独立养成",
            "· 每重有6个星级（1→6星），全部打通后可升重",
            "· 锤炼为概率制：结果为期望消耗（≈实际平均）",
            "· 本计算器关注锤炼材料和保级材料，不计算升重石",
            "· 天市最高22重，21-22重概率仅5%、消耗极高",
            "· 启明17-20重保级消耗急增（17:12→20:49/次）",
            "· 建议在期望值基础上备20-30%冗余",
        ]
        for r in rules:
            ctk.CTkLabel(info_inner, text=r, font=ctk.CTkFont(size=12),
                         text_color=self.colors["text_dim"], anchor="w").pack(fill="x", pady=1)

    # ------------------------------------------------------------------
    # Tab 1: 根据材料算可达等级
    # ------------------------------------------------------------------

    def _build_tab1(self):
        inner = ctk.CTkFrame(self.tab1, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        row = 0

        # 星录选择
        ctk.CTkLabel(inner, text="选择星录", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 6))
        row += 1

        self.t1_xinlu = ctk.CTkOptionMenu(
            inner, values=XINLU_NAMES,
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_xinlu_change_t1,
        )
        self.t1_xinlu.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t1_xinlu.set("太微")
        row += 1

        # 材料信息提示
        self.t1_mat_info = ctk.CTkLabel(inner, text="",
                                        font=ctk.CTkFont(size=11),
                                        text_color="#e94560", anchor="w")
        self.t1_mat_info.grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 8))
        row += 1

        # 当前状态
        ctk.CTkLabel(inner, text="当前状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(6, 6))
        row += 1

        ctk.CTkLabel(inner, text="当前重数", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=0, sticky="w", padx=(0, 8))
        ctk.CTkLabel(inner, text="当前星级 (0=未开始)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=1, sticky="w", padx=(8, 0))
        row += 1
        self.t1_cur_chong = ctk.CTkEntry(inner, placeholder_text="1", height=32, corner_radius=6)
        self.t1_cur_chong.grid(row=row, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t1_cur_chong.insert(0, "1")
        self.t1_cur_star = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_cur_star.grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t1_cur_star.insert(0, "0")
        row += 1

        # 拥有材料
        ctk.CTkLabel(inner, text="拥有材料（留空=无限）", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 6))
        row += 1

        # 低阶材料
        self.t1_low_label = ctk.CTkLabel(inner, text="低阶材料(南明离火):", font=ctk.CTkFont(size=12),
                                         text_color=self.colors["text_dim"])
        self.t1_low_label.grid(row=row, column=0, sticky="w", padx=(0, 8), pady=(3, 2))
        self.t1_mid_label = ctk.CTkLabel(inner, text="中阶材料(九幽玄火):", font=ctk.CTkFont(size=12),
                                         text_color=self.colors["text_dim"])
        self.t1_mid_label.grid(row=row, column=1, sticky="w", padx=(8, 0), pady=(3, 2))
        row += 1
        self.t1_low_entry = ctk.CTkEntry(inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_low_entry.grid(row=row, column=0, sticky="ew", padx=(0, 8), pady=(0, 4))
        self.t1_mid_entry = ctk.CTkEntry(inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_mid_entry.grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=(0, 4))
        row += 1

        self.t1_high_label = ctk.CTkLabel(inner, text="高阶材料(红莲业火):", font=ctk.CTkFont(size=12),
                                          text_color=self.colors["text_dim"])
        self.t1_high_label.grid(row=row, column=0, sticky="w", padx=(0, 8), pady=(3, 2))
        self.t1_guard_label = ctk.CTkLabel(inner, text="保级道具(灵运石):", font=ctk.CTkFont(size=12),
                                           text_color=self.colors["text_dim"])
        self.t1_guard_label.grid(row=row, column=1, sticky="w", padx=(8, 0), pady=(3, 2))
        row += 1
        self.t1_high_entry = ctk.CTkEntry(inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_high_entry.grid(row=row, column=0, sticky="ew", padx=(0, 8), pady=(0, 4))
        self.t1_guard_entry = ctk.CTkEntry(inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_guard_entry.grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=(0, 4))
        row += 1

        # 星官数量
        ctk.CTkLabel(inner, text="计算星官数量", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=0, sticky="w", pady=(3, 2))
        row += 1
        self.t1_officer_count = ctk.CTkOptionMenu(
            inner, values=["1个星官", "8个星官(全部)"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t1_officer_count.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t1_officer_count.set("1个星官")
        row += 1

        # 计算按钮
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(12, 8))
        row += 1
        ctk.CTkButton(btn_row, text="▶ 计算可达到的等级",
                      font=ctk.CTkFont(size=14, weight="bold"), height=38,
                      fg_color="#e94560", hover_color="#c73650",
                      command=self._calc_by_materials).pack(fill="x")

        # 结果区
        self.t1_result = ctk.CTkTextbox(inner, height=300, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
                                        wrap="word")
        self.t1_result.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.t1_result.insert("1.0", "请输入参数后点击计算...\n")
        self.t1_result.configure(state="disabled")

        # 初始更新材料名
        self._update_mat_labels_t1()

    # ------------------------------------------------------------------
    # Tab 2: 根据目标算所需材料
    # ------------------------------------------------------------------

    def _build_tab2(self):
        inner = ctk.CTkFrame(self.tab2, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        row = 0

        # 星录选择
        ctk.CTkLabel(inner, text="选择星录", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 6))
        row += 1
        self.t2_xinlu = ctk.CTkOptionMenu(
            inner, values=XINLU_NAMES, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_xinlu_change_t2,
        )
        self.t2_xinlu.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t2_xinlu.set("太微")
        row += 1

        # 材料信息提示
        self.t2_mat_info = ctk.CTkLabel(inner, text="",
                                        font=ctk.CTkFont(size=11),
                                        text_color="#e94560", anchor="w")
        self.t2_mat_info.grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 8))
        row += 1

        # 起始状态
        ctk.CTkLabel(inner, text="起始状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(6, 6))
        row += 1

        ctk.CTkLabel(inner, text="起始重数", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=0, sticky="w", padx=(0, 8))
        ctk.CTkLabel(inner, text="起始星级 (0=未开始)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=1, sticky="w", padx=(8, 0))
        row += 1
        self.t2_start_chong = ctk.CTkEntry(inner, placeholder_text="1", height=32, corner_radius=6)
        self.t2_start_chong.grid(row=row, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t2_start_chong.insert(0, "1")
        self.t2_start_star = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_start_star.grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t2_start_star.insert(0, "0")
        row += 1

        # 目标状态
        ctk.CTkLabel(inner, text="目标状态", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(6, 6))
        row += 1

        ctk.CTkLabel(inner, text="目标重数", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=0, sticky="w", padx=(0, 8))
        ctk.CTkLabel(inner, text="目标星级 (0=刚升重/6=满)", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=1, sticky="w", padx=(8, 0))
        row += 1
        self.t2_target_chong = ctk.CTkEntry(inner, placeholder_text="20", height=32, corner_radius=6)
        self.t2_target_chong.grid(row=row, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t2_target_chong.insert(0, "20")
        self.t2_target_star = ctk.CTkEntry(inner, placeholder_text="6", height=32, corner_radius=6)
        self.t2_target_star.grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t2_target_star.insert(0, "6")
        row += 1

        # 星官数量
        ctk.CTkLabel(inner, text="计算星官数量", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=0, sticky="w", pady=(3, 2))
        row += 1
        self.t2_officer_count = ctk.CTkOptionMenu(
            inner, values=["1个星官", "8个星官(全部)"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
        )
        self.t2_officer_count.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t2_officer_count.set("1个星官")
        row += 1

        # 计算按钮
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(12, 8))
        row += 1
        ctk.CTkButton(btn_row, text="▶ 计算所需材料",
                      font=ctk.CTkFont(size=14, weight="bold"), height=38,
                      fg_color="#e94560", hover_color="#c73650",
                      command=self._calc_for_target).pack(fill="x")

        # 结果区
        self.t2_result = ctk.CTkTextbox(inner, height=350, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
                                        wrap="word")
        self.t2_result.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.t2_result.insert("1.0", "请输入参数后点击计算...\n")
        self.t2_result.configure(state="disabled")

        # 初始更新材料名
        self._update_mat_info_t2()

    # ------------------------------------------------------------------
    # 交互回调
    # ------------------------------------------------------------------

    def _on_tab_change(self, val):
        if "根据材料" in str(val):
            self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            try:
                self.tab2.grid_forget()
            except Exception:
                pass
        else:
            self.tab2.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            try:
                self.tab1.grid_forget()
            except Exception:
                pass

    def _on_xinlu_change_t1(self, val):
        self._update_mat_labels_t1()

    def _on_xinlu_change_t2(self, val):
        self._update_mat_info_t2()

    def _update_mat_labels_t1(self):
        xinlu = self.t1_xinlu.get()
        cfg = XINLU_CONFIG[xinlu]
        self.t1_low_label.configure(text=f"低阶材料({cfg['low_mat']}):")
        self.t1_mid_label.configure(text=f"中阶材料({cfg['mid_mat']}):")
        self.t1_high_label.configure(text=f"高阶材料({cfg['high_mat']}):")
        self.t1_guard_label.configure(text=f"保级道具({cfg['guard']}):")
        max_c = cfg["max_chong"]
        self.t1_mat_info.configure(
            text=f"最高{max_c}重 | 解锁等级:{cfg['unlock_lv']} | 前置:{cfg['pre_req']}"
        )

    def _update_mat_info_t2(self):
        xinlu = self.t2_xinlu.get()
        cfg = XINLU_CONFIG[xinlu]
        max_c = cfg["max_chong"]
        self.t2_mat_info.configure(
            text=f"最高{max_c}重 | 低阶:{cfg['low_mat']} | 中阶:{cfg['mid_mat']} | 高阶:{cfg['high_mat']}"
        )

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _parse_int(self, val, default):
        try:
            return int((val or "").strip() or str(default))
        except (ValueError, AttributeError):
            return default

    def _parse_float_or_inf(self, val):
        v = (val or "").strip()
        if not v:
            return float("inf")
        try:
            return float(v)
        except (ValueError, AttributeError):
            return float("inf")

    def _fmt(self, v):
        if isinstance(v, float) and v == float("inf"):
            return "∞"
        if isinstance(v, float):
            if v >= 10000:
                return f"{v:,.0f}"
            return f"{v:,.1f}"
        return f"{v:,}"

    def _get_officer_mult(self, option_val):
        return 8 if "8" in option_val else 1

    # ------------------------------------------------------------------
    # 模式一：根据材料计算可达等级
    # ------------------------------------------------------------------

    def _calc_by_materials(self):
        try:
            xinlu = self.t1_xinlu.get()
            cfg = XINLU_CONFIG[xinlu]
            max_chong = cfg["max_chong"]
            mult = self._get_officer_mult(self.t1_officer_count.get())

            cur_chong = self._parse_int(self.t1_cur_chong.get(), 1)
            cur_star = self._parse_int(self.t1_cur_star.get(), 0)

            if cur_chong < 1 or cur_chong > max_chong:
                self._show_error(self.t1_result, f"当前重数需在 1 ~ {max_chong} 之间")
                return
            if cur_star < 0 or cur_star > 6:
                self._show_error(self.t1_result, "当前星级需在 0 ~ 6 之间")
                return

            # 解析材料
            low_mat = self._parse_float_or_inf(self.t1_low_entry.get())
            mid_mat = self._parse_float_or_inf(self.t1_mid_entry.get())
            high_mat = self._parse_float_or_inf(self.t1_high_entry.get())
            guard = self._parse_float_or_inf(self.t1_guard_entry.get())

            # 按倍数除以星官数（材料总量分给N个星官）
            if mult > 1:
                if low_mat != float("inf"):
                    low_mat /= mult
                if mid_mat != float("inf"):
                    mid_mat /= mult
                if high_mat != float("inf"):
                    high_mat /= mult
                if guard != float("inf"):
                    guard /= mult

            # 调用计算引擎
            result = calc_by_materials(xinlu, cur_chong, cur_star,
                                       low_mat, mid_mat, high_mat, guard)
            chong = result["chong"]
            star = result["star"]
            used = result["used"]

            # 输出结果
            lines = []
            lines.append(f"━━━ 星录养成模拟结果 ━━━\n")
            lines.append(f"星录：{xinlu} | 最高{max_chong}重")
            lines.append(f"计算方式：{'8个星官(材料平分)' if mult > 1 else '单个星官'}\n")
            lines.append(f"▸ 可达等级：{chong}重{star}星")
            lines.append(f"  从 {cur_chong}重{self._parse_int(self.t1_cur_star.get(), 0)}星 出发\n")

            lines.append("━ 单官期望消耗 ━")
            if used["low"] > 0:
                lines.append(f"  {cfg['low_mat']}(低阶): {self._fmt(used['low'])}")
            if used["mid"] > 0:
                lines.append(f"  {cfg['mid_mat']}(中阶): {self._fmt(used['mid'])}")
            if used["high"] > 0:
                lines.append(f"  {cfg['high_mat']}(高阶): {self._fmt(used['high'])}")
            if used["guard"] > 0:
                lines.append(f"  {cfg['guard']}(保级): {self._fmt(used['guard'])}")

            if mult > 1:
                lines.append(f"\n━ 8官总消耗 ━")
                if used["low"] > 0:
                    lines.append(f"  {cfg['low_mat']}: {self._fmt(used['low'] * 8)}")
                if used["mid"] > 0:
                    lines.append(f"  {cfg['mid_mat']}: {self._fmt(used['mid'] * 8)}")
                if used["high"] > 0:
                    lines.append(f"  {cfg['high_mat']}: {self._fmt(used['high'] * 8)}")
                if used["guard"] > 0:
                    lines.append(f"  {cfg['guard']}: {self._fmt(used['guard'] * 8)}")

            self._show_result(self.t1_result, "\n".join(lines) + "\n")

        except Exception as ex:
            self._show_error(self.t1_result, f"计算出错: {ex}")

    # ------------------------------------------------------------------
    # 模式二：根据目标计算所需材料
    # ------------------------------------------------------------------

    def _calc_for_target(self):
        try:
            xinlu = self.t2_xinlu.get()
            cfg = XINLU_CONFIG[xinlu]
            max_chong = cfg["max_chong"]
            mult = self._get_officer_mult(self.t2_officer_count.get())

            start_chong = self._parse_int(self.t2_start_chong.get(), 1)
            start_star = self._parse_int(self.t2_start_star.get(), 0)
            target_chong = self._parse_int(self.t2_target_chong.get(), max_chong)
            target_star = self._parse_int(self.t2_target_star.get(), 6)

            # 校验
            if start_chong < 1 or start_chong > max_chong:
                self._show_error(self.t2_result, f"起始重数需在 1 ~ {max_chong}")
                return
            if target_chong < 1 or target_chong > max_chong:
                self._show_error(self.t2_result, f"目标重数需在 1 ~ {max_chong}")
                return
            if start_star < 0 or start_star > 6:
                self._show_error(self.t2_result, "起始星级需在 0 ~ 6")
                return
            if target_star < 0 or target_star > 6:
                self._show_error(self.t2_result, "目标星级需在 0 ~ 6")
                return
            if target_chong < start_chong or (target_chong == start_chong and target_star <= start_star):
                self._show_error(self.t2_result, "目标必须大于起始状态")
                return

            # 调用计算引擎
            result = calc_for_target(xinlu, start_chong, start_star,
                                     target_chong, target_star)
            if result.get("error"):
                self._show_error(self.t2_result, result["error"])
                return
            used = result["used"]

            # 输出
            lines = []
            lines.append(f"━━━ 星录材料需求汇总 ━━━\n")
            lines.append(f"星录：{xinlu} | 最高{max_chong}重")
            lines.append(f"范围：{start_chong}重{start_star}星 → {target_chong}重{target_star}星")
            lines.append(f"计算方式：{'8个星官' if mult > 1 else '单个星官'}\n")

            lines.append("━ 单官期望消耗 ━")
            total_items = []
            if used["low"] > 0:
                total_items.append((cfg['low_mat'], "低阶", used["low"]))
                lines.append(f"  {cfg['low_mat']}(低阶): {self._fmt(used['low'])}")
            if used["mid"] > 0:
                total_items.append((cfg['mid_mat'], "中阶", used["mid"]))
                lines.append(f"  {cfg['mid_mat']}(中阶): {self._fmt(used['mid'])}")
            if used["high"] > 0:
                total_items.append((cfg['high_mat'], "高阶", used["high"]))
                lines.append(f"  {cfg['high_mat']}(高阶): {self._fmt(used['high'])}")
            if used["guard"] > 0:
                total_items.append((cfg['guard'], "保级", used["guard"]))
                lines.append(f"  {cfg['guard']}(保级): {self._fmt(used['guard'])}")

            if mult > 1:
                lines.append(f"\n━ 8官总消耗 ━")
                for name, tier_name, amount in total_items:
                    lines.append(f"  {name}({tier_name}): {self._fmt(amount * 8)}")

            # 重段消耗明细
            lines.append(f"\n━ 各重段消耗明细(单官) ━")
            if used["low"] > 0:
                lines.append(f"  1-10重 {cfg['low_mat']}: {self._fmt(used['low'])}")
            if used["mid"] > 0:
                lines.append(f"  11-15重 {cfg['mid_mat']}: {self._fmt(used['mid'])}")
            if used["high"] > 0:
                high_desc = "16-20重" if xinlu != "天市" else f"16-{max_chong}重"
                lines.append(f"  {high_desc} {cfg['high_mat']}: {self._fmt(used['high'])}")

            lines.append(f"\n💡 以上为期望值（锤炼为概率制），建议备20-30%冗余")

            self._show_result(self.t2_result, "\n".join(lines) + "\n")

        except Exception as ex:
            self._show_error(self.t2_result, f"计算出错: {ex}")
