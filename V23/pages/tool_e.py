"""
圣石养成计算器模块
QQ华夏手游经典区 · 圣石/玄石/罡石镶嵌养成系统

支持两种计算模式：
  模式一：根据已有材料计算可达到的等级
  模式二：根据目标等级计算所需材料

数据来源：圣石养成数据_AI版.xlsx（圣石120级 / 玄石360级 / 罡石150级）
"""

import customtkinter as ctk
from pages.base_tool import BaseToolPage

from calculators.calc_e import (
    PART_CONFIG, SLOT_LIMITS, SLOT_ITEM_NAMES,
    STONE_DATA, XUAN_DATA, GANG_DATA,
    STONE_BY_LVL, XUAN_BY_LVL, GANG_BY_LVL,
    get_data_list, get_data_map, has_items, resolve_attr,
    calc_by_materials, calc_for_target,
)


# ============================================================
# 三、工具页面
# ============================================================

class ToolEPage(BaseToolPage):
    """圣石养成计算器界面"""

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
        ctk.CTkLabel(scroll, text="💎 圣石养成计算器",
                    font=ctk.CTkFont(size=22, weight="bold"),
                    text_color="#ffffff", anchor="w"
                    ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(scroll, text="QQ华夏手游 · 11件装备 × 3槽位 · 精确计算无随机",
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

        # Tab 2（不 grid）
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
            "· 11件装备(10种部位)，每件3个槽位：圣石/玄石/罡石",
            "· 圣石最高120级 | 玄石最高360级 | 罡石最高150级",
            "· 升级完全确定性：每级消耗积分 + 可能的道具",
            "· 升阶卡口：到特定等级需先消耗升阶材料才能继续",
            "· 玄石升级需消耗同系圣石道具；腕部栏3为气海系(渊泽罡石)",
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

        # 部位选择
        ctk.CTkLabel(inner, text="选择部位", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 6))
        row += 1

        self.t1_part = ctk.CTkOptionMenu(
            inner, values=list(PART_CONFIG.keys()),
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_part_change_t1,
        )
        self.t1_part.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t1_part.set("背部")
        row += 1

        # 属性系选择（头部/胸部/颈部显示）
        self.t1_attr_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t1_attr_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        row += 1
        ctk.CTkLabel(self.t1_attr_frame, text="属性系选择",
                     font=ctk.CTkFont(size=13), text_color=self.colors["text_dim"],
                     anchor="w").pack(side="left", padx=(0, 8))
        self.t1_attr_btns = {}
        for attr in ["金刚系", "灵柔系"]:
            btn = ctk.CTkRadioButton(self.t1_attr_frame, text=attr, value=False,
                                     font=ctk.CTkFont(size=12),
                                     command=lambda a=attr: self._set_attr_t1(a))
            btn.pack(side="left", padx=(0, 12))
            self.t1_attr_btns[attr] = btn
        self.t1_selected_attr = "金刚系"  # 默认
        self._hide_attr_t1()  # 背部固定气海，隐藏选择
        row += 1

        # 槽位选择
        ctk.CTkLabel(inner, text="槽位类型", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(6, 6))
        row += 1
        self.t1_slot = ctk.CTkOptionMenu(
            inner, values=["圣石(栏位1)", "玄石(栏位2)", "罡石(栏位3)"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_slot_change_t1,
        )
        self.t1_slot.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t1_slot.set("圣石(栏位1)")
        row += 1

        # 当前等级
        ctk.CTkLabel(inner, text="当前等级", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(6, 6))
        row += 1
        ctk.CTkLabel(inner, text=f"(上限{SLOT_LIMITS['圣石(栏位1)']}级)",
                     font=ctk.CTkFont(size=11), text_color=self.colors["text_dim"]).grid(
            row=row, column=0, columnspan=2, sticky="w")
        row += 1
        self.t1_cur_lv = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_cur_lv.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t1_cur_lv.insert(0, "0")
        row += 1

        # 拥有材料
        ctk.CTkLabel(inner, text="拥有材料", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 6))
        row += 1

        self.t1_mat_jf_label = ctk.CTkLabel(inner, text="积分:", font=ctk.CTkFont(size=12),
                                            text_color=self.colors["text_dim"])
        self.t1_mat_jf_label.grid(row=row, column=0, sticky="w", padx=(0, 8), pady=(3, 2))
        self.t1_jf_entry = ctk.CTkEntry(inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_jf_entry.grid(row=row+1, column=0, sticky="ew", padx=(0, 8), pady=(0, 4))
        row += 2

        # 道具输入（动态标签）
        self.t1_item_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t1_item_frame.grid(row=row, column=0, columnspan=2, sticky="ew")
        self.t1_item_label = ctk.CTkLabel(self.t1_item_frame, text="道具:", font=ctk.CTkFont(size=12),
                                          text_color=self.colors["text_dim"])
        self.t1_item_label.pack(side="left", padx=(0, 8))
        self.t1_item_entry = ctk.CTkEntry(self.t1_item_frame, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_item_entry.pack(side="left", fill="x", expand=True)
        self._update_item_name_t1()
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
        self.t1_result = ctk.CTkTextbox(inner, height=240, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
                                        wrap="word")
        self.t1_result.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.t1_result.insert("1.0", "请输入参数后点击计算...")
        self.t1_result.configure(state="disabled")

    # ------------------------------------------------------------------
    # Tab 2: 根据目标算所需材料
    # ------------------------------------------------------------------

    def _build_tab2(self):
        inner = ctk.CTkFrame(self.tab2, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        row = 0

        # 部位选择
        ctk.CTkLabel(inner, text="选择部位", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(0, 6)); row+=1
        self.t2_part = ctk.CTkOptionMenu(
            inner, values=list(PART_CONFIG.keys()), height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_part_change_t2,
        )
        self.t2_part.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t2_part.set("背部"); row+=1

        # 属性系选择
        self.t2_attr_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t2_attr_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8)); row+=1
        ctk.CTkLabel(self.t2_attr_frame, text="属性系选择", font=ctk.CTkFont(size=13),
                     text_color=self.colors["text_dim"], anchor="w").pack(side="left", padx=(0, 8))
        self.t2_attr_btns = {}
        for attr in ["金刚系", "灵柔系"]:
            btn = ctk.CTkRadioButton(self.t2_attr_frame, text=attr, value=False,
                                     font=ctk.CTkFont(size=12),
                                     command=lambda a=attr: self._set_attr_t2(a))
            btn.pack(side="left", padx=(0, 12))
            self.t2_attr_btns[attr] = btn
        self.t2_selected_attr = "金刚系"
        self._hide_attr_t2(); row+=1

        # 槽位选择
        ctk.CTkLabel(inner, text="槽位类型", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(6, 6)); row+=1
        self.t2_slot = ctk.CTkOptionMenu(
            inner, values=["圣石(栏位1)", "玄石(栏位2)", "罡石(栏位3)"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_slot_change_t2,
        )
        self.t2_slot.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t2_slot.set("圣石(栏位1)"); row+=1

        # 起始/目标等级
        ctk.CTkLabel(inner, text="等级范围", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(6, 6)); row+=1

        ctk.CTkLabel(inner, text="起始等级", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=0, sticky="w", padx=(0, 8))
        ctk.CTkLabel(inner, text="目标等级", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=1, sticky="w", padx=(8, 0)); row+=1
        self.t2_start_lv = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_target_lv = ctk.CTkEntry(inner, placeholder_text="120", height=32, corner_radius=6)
        self.t2_start_lv.grid(row=row, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t2_target_lv.grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t2_start_lv.insert(0, "0")
        self.t2_target_lv.insert(0, "120"); row+=1

        # 计算按钮
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(12, 8)); row+=1
        ctk.CTkButton(btn_row, text="▶ 计算所需材料",
                      font=ctk.CTkFont(size=14, weight="bold"), height=38,
                      fg_color="#e94560", hover_color="#c73650",
                      command=self._calc_for_target).pack(fill="x")

        # 结果区
        self.t2_result = ctk.CTkTextbox(inner, height=300, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
                                        wrap="word")
        self.t2_result.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.t2_result.insert("1.0", "请输入参数后点击计算...")
        self.t2_result.configure(state="disabled")

    # ------------------------------------------------------------------
    # 交互回调
    # ------------------------------------------------------------------

    def _on_tab_change(self, val):
        if "根据材料" in str(val):
            self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            try: self.tab2.grid_forget()
            except: pass
        else:
            self.tab2.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            try: self.tab1.grid_forget()
            except: pass

    def _on_part_change_t1(self, val):
        part = str(val)
        cfg = PART_CONFIG.get(part, {})
        slot1 = cfg.get("slot1系", "")
        if "可选" in slot1:
            self._show_attr_t1()
        else:
            self._hide_attr_t1()
        self._update_item_name_t1()
        self._update_limit_label_t1()

    def _on_part_change_t2(self, val):
        part = str(val)
        cfg = PART_CONFIG.get(part, {})
        slot1 = cfg.get("slot1系", "")
        if "可选" in slot1:
            self._show_attr_t2()
        else:
            self._hide_attr_t2()
        self._update_limit_label_t2()

    def _on_slot_change_t1(self, val):
        self._update_item_name_t1()
        self._update_limit_label_t1()

    def _on_slot_change_t2(self, val):
        self._update_limit_label_t2()

    def _set_attr_t1(self, attr):
        self.t1_selected_attr = attr
        self.t1_attr_btns[attr].configure(value=True)
        for k, v in self.t1_attr_btns.items():
            if k != attr:
                v.configure(value=False)

    def _set_attr_t2(self, attr):
        self.t2_selected_attr = attr
        self.t2_attr_btns[attr].configure(value=True)
        for k, v in self.t2_attr_btns.items():
            if k != attr:
                v.configure(value=False)

    def _show_attr_t1(self):
        self.t1_attr_frame.pack_configure(pady=(0, 8))
        self.t1_attr_frame.grid()

    def _hide_attr_t1(self):
        try:
            self.t1_attr_frame.grid_forget()
        except Exception:
            pass

    def _show_attr_t2(self):
        self.t2_attr_frame.pack_configure(pady=(0, 8))
        self.t2_attr_frame.grid()

    def _hide_attr_t2(self):
        try:
            self.t2_attr_frame.grid_forget()
        except Exception:
            pass

    def _resolve_attr(self, part, slot_key):
        """解析当前部位的属性系"""
        return resolve_attr(part, slot_key, self.t1_selected_attr)

    def _update_item_name_t1(self):
        part = self.t1_part.get()
        slot = self.t1_slot.get()
        attr = self._resolve_attr(part, "slot1系" if "栏位1" in slot else "slot3系")
        item_name = SLOT_ITEM_NAMES.get((slot, attr), None)
        if item_name:
            self.t1_item_label.configure(text=f"{item_name}:")
            self.t1_item_frame.pack_configure(pady=(4, 0))
            self.t1_item_frame.grid()
        else:
            try: self.t1_item_frame.grid_forget()
            except: pass

    def _update_limit_label_t1(self):
        slot = self.t1_slot.get()
        limit = SLOT_LIMITS.get(slot, 99)
        # 更新当前等级提示（通过重新查找label）
        pass  # 静态显示即可，用户可看上方说明

    def _update_limit_label_t2(self):
        pass

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _parse_int(self, val: str, default: int) -> int:
        try: return int((val or "").strip() or str(default))
        except: return default

    def _parse_float_or_inf(self, val: str) -> float:
        v = (val or "").strip()
        if not v: return float("inf")
        try: return float(v)
        except: return float("inf")

    @staticmethod
    def _get_data_list(slot: str):
        return get_data_list(slot)

    def _fmt(self, v) -> str:
        if isinstance(v, float) and v == float("inf"): return "∞"
        if isinstance(v, float): return f"{v:,.1f}"
        return f"{v:,}"

    # ------------------------------------------------------------------
    # 模式一：根据材料计算可达等级
    # ------------------------------------------------------------------

    def _calc_by_materials(self):
        try:
            part = self.t1_part.get()
            slot = self.t1_slot.get()
            cur_lv = self._parse_int(self.t1_cur_lv.get(), 0)
            jf = self._parse_float_or_inf(self.t1_jf_entry.get())
            item_val = self._parse_float_or_inf(self.t1_item_entry.get()) if self._has_items(slot) else float("inf")

            max_lv = SLOT_LIMITS[slot]
            if cur_lv < 0 or cur_lv > max_lv:
                self._show_error(self.t1_result, f"当前等级需在 0 ~ {max_lv} 之间")
                return

            # 调用计算引擎
            result = calc_by_materials(slot, cur_lv, jf, item_val)
            lv = result["level"]
            total_jf = result["total_jf"]
            total_item = result["total_item"]
            steps = result["steps"]
            remaining_jf = result["remaining_jf"]
            remaining_item = result["remaining_item"]

            # 输出结果
            attr = self._resolve_attr(part, "slot1系" if "栏位1" in slot else "slot3系")
            lines = []
            lines.append(f"━━━ 养成模拟结果 ━━━\n")
            lines.append(f"部位：{part} | 槽位：{slot}")
            if "可选" in PART_CONFIG.get(part, {}).get("slot1系", ""):
                lines.append(f"属性系：{self.t1_selected_attr.replace('系','')}系\n")
            else:
                lines.append(f"属性系：{attr}系\n")
            lines.append(f"▸ 可达等级：{lv}级 (上限 {max_lv})")
            lines.append(f"  从 {cur_lv}级 出发，共推进 {steps} 个等级\n")

            lines.append("━ 累计材料消耗 ━")
            lines.append(f"  积分: {self._fmt(total_jf)}")
            if self._has_items(slot):
                item_name = SLOT_ITEM_NAMES.get((slot, attr), "道具")
                lines.append(f"  {item_name}: {self._fmt(total_item)}")

            equip_count = PART_CONFIG.get(part, {}).get("count", 1)
            lines.append(f"\n(以上为单槽位值 × {equip_count}件装备)")

            # 剩余提示
            remain_lines = []
            if remaining_jf != float("inf") and remaining_jf > 0:
                remain_lines.append(f"  剩余积分: {self._fmt(remaining_jf)}")
            if remaining_item != float("inf") and remaining_item > 0 and self._has_items(slot):
                remain_lines.append(f"  剩余道具: {self._fmt(remaining_item)}")
            if remain_lines:
                old_text = "\n".join(lines) + "\n"
                lines_str = old_text + "\n" + "\n".join(remain_lines) + "\n"
            else:
                lines_str = "\n".join(lines) + "\n"

            self._show_result(self.t1_result, lines_str)

        except Exception as ex:
            self._show_error(self.t1_result, f"计算出错: {ex}")

    # ------------------------------------------------------------------
    # 模式二：根据目标计算所需材料
    # ------------------------------------------------------------------

    def _calc_for_target(self):
        try:
            part = self.t2_part.get()
            slot = self.t2_slot.get()
            start_lv = self._parse_int(self.t2_start_lv.get(), 0)
            target_lv = self._parse_int(self.t2_target_lv.get(),
                                         SLOT_LIMITS[slot])

            max_lv = SLOT_LIMITS[slot]
            if start_lv < 0 or start_lv > max_lv:
                self._show_error(self.t2_result, f"起始等级需在 0 ~ {max_lv}"); return
            if target_lv < 0 or target_lv > max_lv:
                self._show_error(self.t2_result, f"目标等级需在 0 ~ {max_lv}"); return
            if target_lv <= start_lv:
                self._show_error(self.t2_result, "目标必须大于起始等级"); return

            # 调用计算引擎
            result = calc_for_target(slot, start_lv, target_lv)
            total_jf = result["total_jf"]
            total_item = result["total_item"]
            stages_hit = result["stages_hit"]

            attr = self._resolve_attr(part, "slot1系" if "栏位1" in slot else "slot3系")
            equip_count = PART_CONFIG.get(part, {}).get("count", 1)

            lines = []
            lines.append(f"━━━ 材料需求汇总 ━━━\n")
            lines.append(f"部位：{part} | 槽位：{slot}")
            if "可选" in PART_CONFIG.get(part, {}).get("slot1系", ""):
                lines.append(f"属性系：{self.t1_selected_attr.replace('系','')}系\n")
            else:
                lines.append(f"属性系：{attr}系\n")
            lines.append(f"范围：{start_lv}级 → {target_lv}级 (跨{target_lv-start_lv}级)\n")

            lines.append("━ 所需材料 ━")
            lines.append(f"  积分总计: {total_jf:,}")
            if self._has_items(slot):
                item_name = SLOT_ITEM_NAMES.get((slot, attr), "道具")
                lines.append(f"  {item_name}总计: {total_item:,}")

            lines.append(f"\n━ 升阶节点 ━")
            data_map = get_data_map(slot)
            if stages_hit:
                for sv in stages_hit:
                    e = data_map[sv]
                    sj = e.get("stage_jf", 0)
                    si = e.get("stage_item", 0)
                    detail = f"  Lv.{sv}: "
                    parts = []
                    if sj > 0:
                        parts.append(f"+{sj}积分")
                    if si > 0:
                        parts.append(f"+{si}{item_name if self._has_items(slot) else '道具'}")
                    detail += " & ".join(parts)
                    lines.append(detail)
            else:
                lines.append("  无升阶节点")

            lines.append(f"\n(以上为单槽位值 × {equip_count}件装备)")

            self._show_result(self.t2_result, "\n".join(lines) + "\n")

        except Exception as ex:
            self._show_error(self.t2_result, f"计算出错: {ex}")

    @staticmethod
    def _has_items(slot: str) -> bool:
        """该槽位是否消耗道具"""
        return has_items(slot)

    @staticmethod
    def _get_data_map(slot: str):
        return get_data_map(slot)
