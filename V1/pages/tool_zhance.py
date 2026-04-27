"""
占测养成计算器（经典区）
支持两种计算模式：
1. 已知材料 → 计算可达阶数与重数
2. 已知目标 → 计算所需材料数量
"""

import customtkinter as ctk


class ToolZhanCe(ctk.CTkFrame):
    """占测养成计算器（经典区）"""
    
    def __init__(self, parent, colors=None):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors or {
            "text": "#ffffff",
            "text_dim": "#888888",
            "nav_active": "#0f3460"
        }
        
        # 加载数据
        self._load_data()
        
        # 界面布局
        self._build_ui()
    
    def _load_data(self):
        """加载占测养成数据"""
        # ============================================================
        # 系列配置：3种品质体系
        # ============================================================
        self.SERIES_CONFIG = {
            '普通': {
                'tiers': [1, 2, 3, 4, 5, 6, 7, 8],
                'mat1_name': '火灼兽骨',
                'mat1_id': '59401131',
                'mat2_name': '无极灵石',
                'mat2_id': '59401171',
            },
            '玄': {
                'tiers': [9, 10, 11, 12],
                'mat1_name': '火灼兽骨·玄',
                'mat1_id': '59401132',
                'mat2_name': '无极灵石·玄',
                'mat2_id': '59401172',
            },
            '地': {
                'tiers': [13, 14, 15, 16, 17],
                'mat1_name': '火灼兽骨·地',
                'mat1_id': '59401133',
                'mat2_name': '无极灵石·地',
                'mat2_id': '59401173',
            },
        }
        
        self.SERIES_ORDER = ['普通', '玄', '地']
        
        # ============================================================
        # 每阶最大重数
        # ============================================================
        self.TIER_MAX_LEVELS = {
            1: 4, 2: 5, 3: 5, 4: 7,
            5: 4, 6: 5, 7: 5, 8: 7,
            9: 4, 10: 5, 11: 5, 12: 7,
            13: 4, 14: 5, 15: 5, 16: 7,
            17: 4,  # 数据到此为止
        }
        
        # 所有阶的顺序
        self.ALL_TIERS = list(range(1, 18))
        
        # 获取阶对应的系列
        self.TIER_SERIES = {}
        for series, cfg in self.SERIES_CONFIG.items():
            for t in cfg['tiers']:
                self.TIER_SERIES[t] = series
        
        # ============================================================
        # 逐级明细数据：每个(阶,重)需要的材料汇总
        # 数据格式：(阶, 重) -> {mat1_qty, mat2_qty, copper, steps_detail}
        # ============================================================
        self.LEVEL_DATA = self._build_level_data()
        
        # 构建累计数据：从(1,0) -> (tier,level) 的累计消耗
        self._build_cumulative_data()
    
    def _build_level_data(self):
        """构建逐级数据"""
        data = {}
        
        # ---- 1阶 (4重, 普通) ----
        data[(1, 1)] = {'mat1': 65, 'mat2': 0, 'copper': 30000}
        data[(1, 2)] = {'mat1': 75, 'mat2': 0, 'copper': 40000}
        data[(1, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(1, 4)] = {'mat1': 290, 'mat2': 1, 'copper': 60000}
        
        # ---- 2阶 (5重, 普通) ----
        data[(2, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 40000}
        data[(2, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(2, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(2, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(2, 5)] = {'mat1': 300, 'mat2': 1, 'copper': 70000}
        
        # ---- 3阶 (5重, 普通) ----
        data[(3, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 40000}
        data[(3, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(3, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(3, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(3, 5)] = {'mat1': 300, 'mat2': 1, 'copper': 70000}
        
        # ---- 4阶 (7重, 普通) ----
        data[(4, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 40000}
        data[(4, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(4, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(4, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(4, 5)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(4, 6)] = {'mat1': 105, 'mat2': 0, 'copper': 70000}
        data[(4, 7)] = {'mat1': 310, 'mat2': 1, 'copper': 80000}
        
        # ---- 5阶 (4重, 普通) ----
        data[(5, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 40000}
        data[(5, 2)] = {'mat1': 75, 'mat2': 0, 'copper': 40000}
        data[(5, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(5, 4)] = {'mat1': 290, 'mat2': 1, 'copper': 60000}
        
        # ---- 6阶 (5重, 普通) ----
        data[(6, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 40000}
        data[(6, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(6, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(6, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(6, 5)] = {'mat1': 300, 'mat2': 1, 'copper': 70000}
        
        # ---- 7阶 (5重, 普通) ----
        data[(7, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 40000}
        data[(7, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(7, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(7, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(7, 5)] = {'mat1': 300, 'mat2': 1, 'copper': 70000}
        
        # ---- 8阶 (7重, 普通) ----
        data[(8, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 40000}
        data[(8, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(8, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(8, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(8, 5)] = {'mat1': 95, 'mat2': 0, 'copper': 60000}
        data[(8, 6)] = {'mat1': 105, 'mat2': 0, 'copper': 70000}
        data[(8, 7)] = {'mat1': 310, 'mat2': 1, 'copper': 80000}
        
        # ---- 9阶 (4重, 玄) ----
        data[(9, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(9, 2)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(9, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(9, 4)] = {'mat1': 290, 'mat2': 1, 'copper': 120000}
        
        # ---- 10阶 (5重, 玄) ----
        data[(10, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(10, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(10, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(10, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(10, 5)] = {'mat1': 300, 'mat2': 1, 'copper': 140000}
        
        # ---- 11阶 (5重, 玄) ----
        data[(11, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(11, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(11, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(11, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(11, 5)] = {'mat1': 300, 'mat2': 1, 'copper': 140000}
        
        # ---- 12阶 (7重, 玄) ----
        data[(12, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(12, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(12, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(12, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(12, 5)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(12, 6)] = {'mat1': 105, 'mat2': 0, 'copper': 140000}
        data[(12, 7)] = {'mat1': 310, 'mat2': 1, 'copper': 160000}
        
        # ---- 13阶 (4重, 地) ----
        data[(13, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(13, 2)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(13, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(13, 4)] = {'mat1': 290, 'mat2': 1, 'copper': 120000}
        
        # ---- 14阶 (5重, 地) ----
        data[(14, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(14, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(14, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(14, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(14, 5)] = {'mat1': 300, 'mat2': 1, 'copper': 140000}
        
        # ---- 15阶 (5重, 地) ----
        data[(15, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(15, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(15, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(15, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(15, 5)] = {'mat1': 300, 'mat2': 1, 'copper': 140000}
        
        # ---- 16阶 (7重, 地) ----
        data[(16, 1)] = {'mat1': 75, 'mat2': 0, 'copper': 80000}
        data[(16, 2)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(16, 3)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(16, 4)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(16, 5)] = {'mat1': 95, 'mat2': 0, 'copper': 120000}
        data[(16, 6)] = {'mat1': 105, 'mat2': 0, 'copper': 140000}
        data[(16, 7)] = {'mat1': 310, 'mat2': 1, 'copper': 160000}
        
        # ---- 17阶 (4重, 地, 数据不完整) ----
        data[(17, 1)] = {'mat1': 86, 'mat2': 0, 'copper': 160000}
        data[(17, 2)] = {'mat1': 86, 'mat2': 0, 'copper': 160000}
        data[(17, 3)] = {'mat1': 110, 'mat2': 0, 'copper': 240000}
        data[(17, 4)] = {'mat1': 24, 'mat2': 0, 'copper': 80000}
        
        return data
    
    def _build_cumulative_data(self):
        """构建全局累计消耗数据"""
        # cum_data[(tier, level)] = {cum_mat1_普通, cum_mat2_普通, cum_mat1_玄, ...}
        # 简化为按系列统计
        self.CUM_DATA = {}
        
        cum = {'普通': {'mat1': 0, 'mat2': 0, 'copper': 0},
               '玄': {'mat1': 0, 'mat2': 0, 'copper': 0},
               '地': {'mat1': 0, 'mat2': 0, 'copper': 0}}
        
        for tier in self.ALL_TIERS:
            max_lv = self.TIER_MAX_LEVELS[tier]
            series = self.TIER_SERIES[tier]
            for lv in range(1, max_lv + 1):
                key = (tier, lv)
                info = self.LEVEL_DATA.get(key, {'mat1': 0, 'mat2': 0, 'copper': 0})
                cum[series]['mat1'] += info['mat1']
                cum[series]['mat2'] += info['mat2']
                cum[series]['copper'] += info['copper']
                # 保存快照
                self.CUM_DATA[key] = {
                    s: {'mat1': cum[s]['mat1'], 'mat2': cum[s]['mat2'], 'copper': cum[s]['copper']}
                    for s in self.SERIES_ORDER
                }
    
    def _get_tier_level_label(self, tier, level):
        """获取阶重的显示文本"""
        return f"{tier}阶{level}重"
    
    def _build_all_positions(self):
        """构建全部有效的(阶, 重)位置列表，按顺序排列"""
        positions = [(0, 0)]  # 0阶0重 = 起点
        for tier in self.ALL_TIERS:
            max_lv = self.TIER_MAX_LEVELS[tier]
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
        tier_values = [str(t) for t in self.ALL_TIERS]
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
            values=["0"] + [str(i) for i in range(1, self.TIER_MAX_LEVELS[1] + 1)],
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
        
        for series_name in self.SERIES_ORDER:
            cfg = self.SERIES_CONFIG[series_name]
            
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
            values=["0"] + [str(i) for i in range(1, self.TIER_MAX_LEVELS[1] + 1)],
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
            values=[str(i) for i in range(1, self.TIER_MAX_LEVELS[17] + 1)],
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
        max_lv = self.TIER_MAX_LEVELS.get(tier, 4)
        new_values = ["0"] + [str(i) for i in range(1, max_lv + 1)]
        self.t1_level_menu.configure(values=new_values)
        self.t1_level_var.set("0")
    
    def _on_t2_start_tier_change(self, value):
        """Tab2起始阶数变更"""
        tier = int(value)
        max_lv = self.TIER_MAX_LEVELS.get(tier, 4)
        new_values = ["0"] + [str(i) for i in range(1, max_lv + 1)]
        self.t2_start_level_menu.configure(values=new_values)
        self.t2_start_level_var.set("0")
    
    def _on_t2_target_tier_change(self, value):
        """Tab2目标阶数变更"""
        tier = int(value)
        max_lv = self.TIER_MAX_LEVELS.get(tier, 4)
        new_values = [str(i) for i in range(1, max_lv + 1)]
        self.t2_target_level_menu.configure(values=new_values)
        self.t2_target_level_var.set(str(max_lv))
    
    def _show_result(self, textbox, text):
        """显示结果"""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
    
    def _show_error(self, textbox, msg):
        """显示错误"""
        self._show_result(textbox, f"⚠️ {msg}\n")
    
    def _bind_mousewheel(self, widget):
        """绑定滚轮事件，阻止事件冒泡"""
        def on_mousewheel(event):
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        widget.bind("<Button-4>", lambda e: (widget._parent_canvas.yview_scroll(-1, "units"), "break")[1], add="+")
        widget.bind("<Button-5>", lambda e: (widget._parent_canvas.yview_scroll(1, "units"), "break")[1], add="+")
    
    def _format_number(self, num):
        """格式化数字（加千分位）"""
        if isinstance(num, int):
            return f"{num:,}"
        return str(num)
    
    def _pos_to_index(self, tier, level):
        """将(阶,重)转为全局序号，用于比较先后"""
        idx = 0
        for t in self.ALL_TIERS:
            if t < tier:
                idx += self.TIER_MAX_LEVELS[t]
            elif t == tier:
                idx += level
                break
        return idx
    
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
        
        # 验证
        max_lv = self.TIER_MAX_LEVELS.get(start_tier, 0)
        if start_level > max_lv:
            self._show_error(self.t1_result, f"{start_tier}阶最大{max_lv}重")
            return
        
        # 读取持有材料
        materials = {}
        for series_name in self.SERIES_ORDER:
            mat1_txt = self.t1_mat_entries[(series_name, 'mat1')].get().strip()
            mat2_txt = self.t1_mat_entries[(series_name, 'mat2')].get().strip()
            materials[(series_name, 'mat1')] = int(mat1_txt) if mat1_txt else 0
            materials[(series_name, 'mat2')] = int(mat2_txt) if mat2_txt else 0
        
        try:
            copper_available = int(self.t1_copper_entry.get().strip() or "99999999")
        except ValueError:
            copper_available = 99999999
        
        # 检查是否所有材料都是0
        all_zero = all(v == 0 for v in materials.values()) and copper_available == 0
        if all_zero:
            self._show_error(self.t1_result, "请输入至少一种材料的数量")
            return
        
        # 执行计算
        result = self._do_calc_by_materials(start_tier, start_level, materials, copper_available)
        
        # 格式化输出
        output = self._format_material_result(start_tier, start_level, result)
        self._show_result(self.t1_result, output)
    
    def _do_calc_by_materials(self, start_tier, start_level, materials, copper_available):
        """执行材料→等级计算"""
        # 跟踪消耗
        used = {(s, t): 0 for s in self.SERIES_ORDER for t in ('mat1', 'mat2')}
        used_copper = 0
        
        path = []  # 记录升级路径
        
        current_tier = start_tier
        current_level = start_level
        
        # 从当前位置开始，逐级升级
        for tier in self.ALL_TIERS:
            if tier < start_tier:
                continue
            
            series = self.TIER_SERIES[tier]
            max_lv = self.TIER_MAX_LEVELS[tier]
            cfg = self.SERIES_CONFIG[series]
            
            # 确定起始重数
            if tier == start_tier:
                from_lv = start_level + 1
            else:
                from_lv = 1
            
            for lv in range(from_lv, max_lv + 1):
                key = (tier, lv)
                info = self.LEVEL_DATA.get(key)
                if not info:
                    continue
                
                mat1_need = info['mat1']
                mat2_need = info['mat2']
                copper_need = info['copper']
                
                # 检查材料是否充足
                mat1_avail = materials.get((series, 'mat1'), 0) - used[(series, 'mat1')]
                mat2_avail = materials.get((series, 'mat2'), 0) - used[(series, 'mat2')]
                copper_avail = copper_available - used_copper
                
                if mat1_avail >= mat1_need and mat2_avail >= mat2_need and copper_avail >= copper_need:
                    used[(series, 'mat1')] += mat1_need
                    used[(series, 'mat2')] += mat2_need
                    used_copper += copper_need
                    
                    current_tier = tier
                    current_level = lv
                    
                    path.append({
                        'tier': tier, 'level': lv,
                        'mat1': mat1_need, 'mat2': mat2_need, 'copper': copper_need,
                        'mat1_name': cfg['mat1_name'],
                        'mat2_name': cfg['mat2_name'],
                        'series': series,
                    })
                else:
                    # 材料不足，停在这里
                    return {
                        'final_tier': current_tier,
                        'final_level': current_level,
                        'used': used,
                        'used_copper': used_copper,
                        'path': path,
                        'stopped_reason': self._get_stop_reason(
                            mat1_avail, mat1_need, mat2_avail, mat2_need,
                            copper_avail, copper_need, cfg, tier, lv
                        )
                    }
        
        return {
            'final_tier': current_tier,
            'final_level': current_level,
            'used': used,
            'used_copper': used_copper,
            'path': path,
            'stopped_reason': '已达当前数据最高等级（17阶4重）'
        }
    
    def _get_stop_reason(self, m1_avail, m1_need, m2_avail, m2_need, c_avail, c_need, cfg, tier, lv):
        """获取停止升级的原因"""
        reasons = []
        if m1_avail < m1_need:
            reasons.append(f"{cfg['mat1_name']}不足（需{m1_need}，剩{max(0, m1_avail)}）")
        if m2_avail < m2_need:
            reasons.append(f"{cfg['mat2_name']}不足（需{m2_need}，剩{max(0, m2_avail)}）")
        if c_avail < c_need:
            reasons.append(f"铜钱不足（需{self._format_number(c_need)}，剩{self._format_number(max(0, c_avail))}）")
        return f"升{tier}阶{lv}重时: " + "、".join(reasons)
    
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
        for series in self.SERIES_ORDER:
            cfg = self.SERIES_CONFIG[series]
            m1_used = result['used'][(series, 'mat1')]
            m2_used = result['used'][(series, 'mat2')]
            if m1_used > 0 or m2_used > 0:
                out += f"  {cfg['mat1_name']}: {self._format_number(m1_used)} 个\n"
                if m2_used > 0:
                    out += f"  {cfg['mat2_name']}: {m2_used} 个\n"
        
        out += f"  💰 铜钱: {self._format_number(result['used_copper'])}\n"
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
            out += f"    {lv}重: {mat_info}, 铜钱{self._format_number(step['copper'])}\n"
        
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
        
        # 验证
        s_max = self.TIER_MAX_LEVELS.get(start_tier, 0)
        if start_level > s_max:
            self._show_error(self.t2_result, f"{start_tier}阶最大{s_max}重")
            return
        
        t_max = self.TIER_MAX_LEVELS.get(target_tier, 0)
        if target_level < 1 or target_level > t_max:
            self._show_error(self.t2_result, f"{target_tier}阶重数范围为1-{t_max}")
            return
        
        # 比较起点和终点
        start_idx = self._pos_to_index(start_tier, start_level)
        target_idx = self._pos_to_index(target_tier, target_level)
        
        if target_idx <= start_idx:
            self._show_error(self.t2_result, "目标等级必须高于当前等级")
            return
        
        # 执行计算
        result = self._do_calc_by_target(start_tier, start_level, target_tier, target_level)
        
        # 格式化输出
        output = self._format_target_result(start_tier, start_level, target_tier, target_level, result)
        self._show_result(self.t2_result, output)
    
    def _do_calc_by_target(self, start_tier, start_level, target_tier, target_level):
        """执行目标→材料计算"""
        required = {(s, t): 0 for s in self.SERIES_ORDER for t in ('mat1', 'mat2')}
        required_copper = 0
        path = []
        
        for tier in self.ALL_TIERS:
            if tier < start_tier or tier > target_tier:
                continue
            
            series = self.TIER_SERIES[tier]
            max_lv = self.TIER_MAX_LEVELS[tier]
            cfg = self.SERIES_CONFIG[series]
            
            # 确定起始和结束重数
            if tier == start_tier:
                from_lv = start_level + 1
            else:
                from_lv = 1
            
            if tier == target_tier:
                to_lv = target_level
            else:
                to_lv = max_lv
            
            for lv in range(from_lv, to_lv + 1):
                key = (tier, lv)
                info = self.LEVEL_DATA.get(key)
                if not info:
                    continue
                
                required[(series, 'mat1')] += info['mat1']
                required[(series, 'mat2')] += info['mat2']
                required_copper += info['copper']
                
                path.append({
                    'tier': tier, 'level': lv,
                    'mat1': info['mat1'], 'mat2': info['mat2'], 'copper': info['copper'],
                    'mat1_name': cfg['mat1_name'],
                    'mat2_name': cfg['mat2_name'],
                    'series': series,
                })
        
        return {
            'required': required,
            'required_copper': required_copper,
            'path': path,
        }
    
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
        for series in self.SERIES_ORDER:
            cfg = self.SERIES_CONFIG[series]
            m1 = result['required'][(series, 'mat1')]
            m2 = result['required'][(series, 'mat2')]
            if m1 > 0 or m2 > 0:
                out += f"  {cfg['mat1_name']}: {self._format_number(m1)} 个\n"
                total_items += m1
                if m2 > 0:
                    out += f"  {cfg['mat2_name']}: {m2} 个\n"
                    total_items += m2
        
        out += f"  💰 铜钱: {self._format_number(result['required_copper'])}\n"
        out += f"\n  📦 材料总计: {self._format_number(total_items)} 个\n"
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
                    out += f"    ── 小计: 主材×{self._format_number(tier_mat1_sum)}"
                    if tier_mat2_sum > 0:
                        out += f" + 副材×{tier_mat2_sum}"
                    out += f" + 铜钱{self._format_number(tier_copper_sum)}\n"
                
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
            out += f"    {lv}重: {mat_info}, 铜钱{self._format_number(step['copper'])}\n"
        
        # 最后一阶的汇总
        if current_display_tier is not None:
            out += f"    ── 小计: 主材×{self._format_number(tier_mat1_sum)}"
            if tier_mat2_sum > 0:
                out += f" + 副材×{tier_mat2_sum}"
            out += f" + 铜钱{self._format_number(tier_copper_sum)}\n"
        
        return out
