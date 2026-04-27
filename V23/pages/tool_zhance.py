"""
占测养成计算器（经典区）
支持两种计算模式：
1. 已知材料 → 计算可达阶数与重数
2. 已知目标 → 计算所需材料数量
"""

import customtkinter as ctk
from pages.base_tool import BaseToolPage

from calculators.calc_zhance import (
    SERIES_CONFIG, SERIES_ORDER, TIER_MAX_LEVELS,
    ALL_TIERS, TIER_SERIES, LEVEL_DATA, CUM_DATA,
    pos_to_index, format_number,
    calc_by_materials, calc_by_target,
)


class ToolZhanCe(BaseToolPage):
    """占测养成计算器（经典区）"""
    
    def __init__(self, parent, colors=None):
        super().__init__(parent, colors)
        # 界面布局
        self._build_ui()
    
    def _get_tier_level_label(self, tier, level):
        """获取阶重的显示文本"""
        return f"{tier}阶{level}重"
    
    def _build_all_positions(self):
        """构建全部有效的(阶, 重)位置列表，按顺序排列"""
        positions = [(0, 0)]  # 0阶0重 = 起点
        for tier in ALL_TIERS:
            max_lv = TIER_MAX_LEVELS[tier]
            for lv in range(1, max_lv + 1):
                positions.append((tier, lv))
        return positions
    
    # ============================================================
    # UI 构建
    # ============================================================
    
    def _build_ui(self):
        """创建界面（参考遁甲工具）"""
        # 主滚动容器
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)
        
        # ---- 页面标题 ----
        ctk.CTkLabel(
            scroll,
            text="📜 占测养成计算器（经典区）",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        ctk.CTkLabel(
            scroll,
            text="3种品质体系 · 普通(1-8阶) → 玄(9-12阶) → 地(13-17阶) · 17阶4重满级",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))
        
        # ---- 标签页切换 ----
        tab_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        
        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["📊 材料 → 可达等级", "🎯 目标 → 所需材料"],
            height=34,
            font=ctk.CTkFont(size=13),
            selected_color=self.colors.get("nav_active", "#0f3460"),
            unselected_color="#0f0f1a",
            selected_hover_color="#164080",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("📊 材料 → 可达等级")
        
        # ============================================================
        # Tab 1：根据持有材料计算可达等级
        # ============================================================
        self.tab1_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        tab1_inner = ctk.CTkFrame(self.tab1_frame, fg_color="transparent")
        tab1_inner.pack(fill="x", padx=20, pady=18)
        tab1_inner.grid_columnconfigure((0, 1), weight=1)
        
        # -- 初始状态 --
        ctk.CTkLabel(
            tab1_inner, text="当前占测状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        
        # 当前阶数
        ctk.CTkLabel(tab1_inner, text="当前阶数",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t1_tier_var = ctk.StringVar(value="1")
        tier_values = [str(t) for t in ALL_TIERS]
        self.t1_tier_menu = ctk.CTkOptionMenu(
            tab1_inner, variable=self.t1_tier_var,
            values=tier_values, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
            command=self._on_t1_tier_change,
        )
        self.t1_tier_menu.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        
        # 当前重数
        ctk.CTkLabel(tab1_inner, text="当前重数",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t1_level_var = ctk.StringVar(value="0")
        self.t1_level_menu = ctk.CTkOptionMenu(
            tab1_inner, variable=self.t1_level_var,
            values=["0"] + [str(i) for i in range(1, TIER_MAX_LEVELS[1] + 1)],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t1_level_menu.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        
        # -- 材料输入 --
        ctk.CTkLabel(tab1_inner, text="持有材料数量",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(10, 8))
        
        self.t1_mat_entries = {}
        row_idx = 4
        
        for series_name in SERIES_ORDER:
            cfg = SERIES_CONFIG[series_name]
            
            # 主材料
            mat1_label = f"{cfg['mat1_name']}（{cfg['tiers'][0]}-{cfg['tiers'][-1]}阶主材）"
            ctk.CTkLabel(tab1_inner, text=mat1_label,
                         font=ctk.CTkFont(size=12),
                         text_color=self.colors["text"], anchor="w").grid(
                row=row_idx, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
            
            entry_mat1 = ctk.CTkEntry(tab1_inner, placeholder_text="数量", height=30,
                                       corner_radius=6, fg_color="#0f0f1a")
            entry_mat1.insert(0, "0")
            entry_mat1.grid(row=row_idx + 1, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
            self.t1_mat_entries[(series_name, 'mat1')] = entry_mat1
            
            # 副材料
            mat2_label = f"{cfg['mat2_name']}（进阶副材）"
            ctk.CTkLabel(tab1_inner, text=mat2_label,
                         font=ctk.CTkFont(size=12),
                         text_color=self.colors["text"], anchor="w").grid(
                row=row_idx, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
            
            entry_mat2 = ctk.CTkEntry(tab1_inner, placeholder_text="数量", height=30,
                                       corner_radius=6, fg_color="#0f0f1a")
            entry_mat2.insert(0, "0")
            entry_mat2.grid(row=row_idx + 1, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
            self.t1_mat_entries[(series_name, 'mat2')] = entry_mat2
            
            row_idx += 2
        
        # 铜钱输入
        ctk.CTkLabel(tab1_inner, text="💰 铜钱",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text"], anchor="w").grid(
            row=row_idx, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t1_copper_entry = ctk.CTkEntry(tab1_inner, placeholder_text="铜钱数量",
                                             height=30, corner_radius=6, fg_color="#0f0f1a")
        self.t1_copper_entry.insert(0, "99999999")
        self.t1_copper_entry.grid(row=row_idx + 1, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        
        ctk.CTkLabel(tab1_inner, text="（默认不限制）",
                     font=ctk.CTkFont(size=11),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=row_idx + 1, column=1, sticky="w", padx=(10, 0), pady=(0, 8))
        
        row_idx += 2
        
        # 计算按钮
        ctk.CTkButton(
            tab1_inner,
            text="▶  计算可达到的阶数与重数",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#0f3460", hover_color="#16213e",
            command=self._calc_by_materials,
        ).grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(8, 8))
        
        # 结果区域
        self.t1_result = ctk.CTkTextbox(
            tab1_inner, height=260, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(family="Microsoft YaHei UI", size=12),
        )
        self.t1_result.grid(row=row_idx + 1, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")
        self._bind_mousewheel(self.t1_result)
        
        # ============================================================
        # Tab 2：根据目标等级计算所需材料
        # ============================================================
        self.tab2_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        # 不立即 grid，由标签页切换控制
        
        tab2_inner = ctk.CTkFrame(self.tab2_frame, fg_color="transparent")
        tab2_inner.pack(fill="x", padx=20, pady=18)
        tab2_inner.grid_columnconfigure((0, 1), weight=1)
        
        # -- 初始状态 --
        ctk.CTkLabel(
            tab2_inner, text="当前占测状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        
        ctk.CTkLabel(tab2_inner, text="当前阶数",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t2_start_tier_var = ctk.StringVar(value="1")
        self.t2_start_tier_menu = ctk.CTkOptionMenu(
            tab2_inner, variable=self.t2_start_tier_var,
            values=tier_values, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
            command=self._on_t2_start_tier_change,
        )
        self.t2_start_tier_menu.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        
        ctk.CTkLabel(tab2_inner, text="当前重数",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t2_start_level_var = ctk.StringVar(value="0")
        self.t2_start_level_menu = ctk.CTkOptionMenu(
            tab2_inner, variable=self.t2_start_level_var,
            values=["0"] + [str(i) for i in range(1, TIER_MAX_LEVELS[1] + 1)],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t2_start_level_menu.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        
        # -- 目标状态 --
        ctk.CTkLabel(
            tab2_inner, text="目标占测状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 8))
        
        ctk.CTkLabel(tab2_inner, text="目标阶数",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=4, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t2_target_tier_var = ctk.StringVar(value="17")
        self.t2_target_tier_menu = ctk.CTkOptionMenu(
            tab2_inner, variable=self.t2_target_tier_var,
            values=tier_values, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
            command=self._on_t2_target_tier_change,
        )
        self.t2_target_tier_menu.grid(row=5, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        
        ctk.CTkLabel(tab2_inner, text="目标重数",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=4, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t2_target_level_var = ctk.StringVar(value="4")
        self.t2_target_level_menu = ctk.CTkOptionMenu(
            tab2_inner, variable=self.t2_target_level_var,
            values=[str(i) for i in range(1, TIER_MAX_LEVELS[17] + 1)],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t2_target_level_menu.grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        
        # 计算按钮
        ctk.CTkButton(
            tab2_inner,
            text="▶  计算所需材料",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#2e7d32", hover_color="#1b5e20",
            command=self._calc_by_target,
        ).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(8, 8))
        
        # 结果区域
        self.t2_result = ctk.CTkTextbox(
            tab2_inner, height=300, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(family="Microsoft YaHei UI", size=12),
        )
        self.t2_result.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.t2_result.insert("1.0", "等待计算...\n")
        self.t2_result.configure(state="disabled")
        self._bind_mousewheel(self.t2_result)
        
        # ---- 说明卡片 ----
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            info_inner,
            text="📖 使用说明",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).pack(fill="x", pady=(0, 8))
        
        rules = [
            "• 功能一：输入持有的各材料数量 + 当前状态 → 计算最多能升到几阶几重",
            "• 功能二：设定起始/目标状态 → 计算所需材料明细和铜钱",
            "",
            "【3种品质体系】",
            "  普通(1-8阶): 火灼兽骨 + 无极灵石",
            "  玄 (9-12阶): 火灼兽骨·玄 + 无极灵石·玄",
            "  地(13-17阶): 火灼兽骨·地 + 无极灵石·地",
            "",
            "【阶重规则】",
            "  每4阶为一个循环: 4重→5重→5重→7重",
            "  副材料(无极灵石)仅在每阶最后一重的进阶步骤消耗1个",
            "",
            "【数据说明】",
            "  数据来源：经典区占测养成表，当前数据到17阶4重",
            f"  满级总材料: 火灼兽骨×5440 + 无极灵石×8 + 火灼兽骨·玄×2725 + 无极灵石·玄×4",
            f"              + 火灼兽骨·地×3031 + 无极灵石·地×4 + 铜钱789万",
        ]
        for rule in rules:
            ctk.CTkLabel(
                info_inner, text=rule,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"], anchor="w",
            ).pack(fill="x", pady=1)
    
    # ============================================================
    # 事件处理
    # ============================================================
    
    def _on_tab_change(self, value):
        """切换标签页"""
        if value == "📊 材料 → 可达等级":
            self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2_frame.grid_forget()
        else:
            self.tab2_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1_frame.grid_forget()
    
    def _on_t1_tier_change(self, value):
        """Tab1阶数变更 → 更新重数选项"""
        tier = int(value)
        max_lv = TIER_MAX_LEVELS.get(tier, 4)
        new_values = ["0"] + [str(i) for i in range(1, max_lv + 1)]
        self.t1_level_menu.configure(values=new_values)
        self.t1_level_var.set("0")
    
    def _on_t2_start_tier_change(self, value):
        """Tab2起始阶数变更"""
        tier = int(value)
        max_lv = TIER_MAX_LEVELS.get(tier, 4)
        new_values = ["0"] + [str(i) for i in range(1, max_lv + 1)]
        self.t2_start_level_menu.configure(values=new_values)
        self.t2_start_level_var.set("0")
    
    def _on_t2_target_tier_change(self, value):
        """Tab2目标阶数变更"""
        tier = int(value)
        max_lv = TIER_MAX_LEVELS.get(tier, 4)
        new_values = [str(i) for i in range(1, max_lv + 1)]
        self.t2_target_level_menu.configure(values=new_values)
        self.t2_target_level_var.set(str(max_lv))
    
    # ============================================================
    # 模式1：根据材料计算可达等级
    # ============================================================
    
    def _calc_by_materials(self):
        """模式1：根据持有材料计算可达等级"""
        try:
            start_tier = int(self.t1_tier_var.get())
            start_level = int(self.t1_level_var.get())
        except ValueError:
            self._show_error(self.t1_result, "请输入有效数字！")
            return
        
        # 读取持有材料
        materials = {}
        for series_name in SERIES_ORDER:
            mat1_txt = self.t1_mat_entries[(series_name, 'mat1')].get().strip()
            mat2_txt = self.t1_mat_entries[(series_name, 'mat2')].get().strip()
            materials[(series_name, 'mat1')] = int(mat1_txt) if mat1_txt else 0
            materials[(series_name, 'mat2')] = int(mat2_txt) if mat2_txt else 0
        
        try:
            copper_available = int(self.t1_copper_entry.get().strip() or "99999999")
        except ValueError:
            copper_available = 99999999
        
        # 调用计算器
        result = calc_by_materials(start_tier, start_level, materials, copper_available)
        
        if result.get("error"):
            self._show_error(self.t1_result, result["error"])
            return
        
        # 格式化输出
        output = self._format_material_result(start_tier, start_level, result)
        self._show_result(self.t1_result, output)
    
    def _format_material_result(self, start_tier, start_level, result):
        """格式化模式1的计算结果"""
        ft = result['final_tier']
        fl = result['final_level']
        
        out = f"✅ 计算完成\n\n"
        out += f"{'═' * 45}\n"
        out += f"  起始状态: {start_tier}阶{start_level}重\n"
        out += f"  可达状态: {ft}阶{fl}重\n"
        out += f"{'═' * 45}\n\n"
        
        # 材料使用汇总
        out += "【材料使用汇总】\n"
        for series in SERIES_ORDER:
            cfg = SERIES_CONFIG[series]
            m1_used = result['used'][(series, 'mat1')]
            m2_used = result['used'][(series, 'mat2')]
            if m1_used > 0 or m2_used > 0:
                out += f"  {cfg['mat1_name']}: {format_number(m1_used)} 个\n"
                if m2_used > 0:
                    out += f"  {cfg['mat2_name']}: {m2_used} 个\n"
        
        out += f"  💰 铜钱: {format_number(result['used_copper'])}\n"
        out += f"\n{'─' * 45}\n\n"
        
        # 升级路径概要（按阶分组）
        out += "【升级路径】\n"
        current_display_tier = None
        for step in result['path']:
            tier = step['tier']
            lv = step['level']
            
            if tier != current_display_tier:
                series = step['series']
                out += f"\n  ▸ {tier}阶 [{series}系列]\n"
                current_display_tier = tier
            
            mat_info = f"{step['mat1_name']}×{step['mat1']}"
            if step['mat2'] > 0:
                mat_info += f" + {step['mat2_name']}×{step['mat2']}"
            out += f"    {lv}重: {mat_info}, 铜钱{format_number(step['copper'])}\n"
        
        out += f"\n{'─' * 45}\n"
        out += f"⏹ 停止原因: {result['stopped_reason']}\n"
        
        return out
    
    # ============================================================
    # 模式2：根据目标计算所需材料
    # ============================================================
    
    def _calc_by_target(self):
        """模式2：根据目标等级计算所需材料"""
        try:
            start_tier = int(self.t2_start_tier_var.get())
            start_level = int(self.t2_start_level_var.get())
            target_tier = int(self.t2_target_tier_var.get())
            target_level = int(self.t2_target_level_var.get())
        except ValueError:
            self._show_error(self.t2_result, "请输入有效数字！")
            return
        
        # 调用计算器
        result = calc_by_target(start_tier, start_level, target_tier, target_level)
        
        if result.get("error"):
            self._show_error(self.t2_result, result["error"])
            return
        
        # 格式化输出
        output = self._format_target_result(start_tier, start_level, target_tier, target_level, result)
        self._show_result(self.t2_result, output)
    
    def _format_target_result(self, st, sl, tt, tl, result):
        """格式化模式2的计算结果"""
        out = f"✅ 计算完成\n\n"
        out += f"{'═' * 45}\n"
        out += f"  起始状态: {st}阶{sl}重\n"
        out += f"  目标状态: {tt}阶{tl}重\n"
        out += f"{'═' * 45}\n\n"
        
        # 材料需求汇总
        out += "【材料需求汇总】\n"
        total_items = 0
        for series in SERIES_ORDER:
            cfg = SERIES_CONFIG[series]
            m1 = result['required'][(series, 'mat1')]
            m2 = result['required'][(series, 'mat2')]
            if m1 > 0 or m2 > 0:
                out += f"  {cfg['mat1_name']}: {format_number(m1)} 个\n"
                total_items += m1
                if m2 > 0:
                    out += f"  {cfg['mat2_name']}: {m2} 个\n"
                    total_items += m2
        
        out += f"  💰 铜钱: {format_number(result['required_copper'])}\n"
        out += f"\n  📦 材料总计: {format_number(total_items)} 个\n"
        out += f"\n{'─' * 45}\n\n"
        
        # 按阶分组的升级路径
        out += "【逐阶升级明细】\n"
        current_display_tier = None
        tier_mat1_sum = 0
        tier_mat2_sum = 0
        tier_copper_sum = 0
        
        for i, step in enumerate(result['path']):
            tier = step['tier']
            lv = step['level']
            
            # 新阶开始
            if tier != current_display_tier:
                # 输出上一阶的汇总
                if current_display_tier is not None:
                    out += f"    ── 小计: 主材×{format_number(tier_mat1_sum)}"
                    if tier_mat2_sum > 0:
                        out += f" + 副材×{tier_mat2_sum}"
                    out += f" + 铜钱{format_number(tier_copper_sum)}\n"
                
                series = step['series']
                out += f"\n  ▸ {tier}阶 [{series}系列] ({step['mat1_name']})\n"
                current_display_tier = tier
                tier_mat1_sum = 0
                tier_mat2_sum = 0
                tier_copper_sum = 0
            
            tier_mat1_sum += step['mat1']
            tier_mat2_sum += step['mat2']
            tier_copper_sum += step['copper']
            
            mat_info = f"主材×{step['mat1']}"
            if step['mat2'] > 0:
                mat_info += f" + 副材×{step['mat2']}"
            out += f"    {lv}重: {mat_info}, 铜钱{format_number(step['copper'])}\n"
        
        # 最后一阶的汇总
        if current_display_tier is not None:
            out += f"    ── 小计: 主材×{format_number(tier_mat1_sum)}"
            if tier_mat2_sum > 0:
                out += f" + 副材×{tier_mat2_sum}"
            out += f" + 铜钱{format_number(tier_copper_sum)}\n"
        
        return out
