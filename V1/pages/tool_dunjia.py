"""
遁甲（强运）养成计算器
支持两种计算模式：
1. 已知材料 → 计算可达等级
2. 已知目标 → 计算所需材料
"""

import customtkinter as ctk


class ToolDunJia(ctk.CTkFrame):
    """遁甲（强运）养成计算器"""
    
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
        """加载遁甲养成数据"""
        # 品阶配置
        self.GRADES = {
            '黄阶': {'max_level': 36, 'material': '古迹灵石', 'material_id': 59011243},
            '玄阶': {'max_level': 49, 'material': '古迹灵石·玄', 'material_id': 59011248},
            '地阶': {'max_level': 64, 'material': '古迹灵石·地', 'material_id': 59011249},
            '天阶': {'max_level': 100, 'material': '古迹灵石·天', 'material_id': 59011250},
        }
        
        self.GRADE_ORDER = ['黄阶', '玄阶', '地阶', '天阶']
        
        # 逐级明细数据（品阶、等级、能力值、消耗数量、累计材料）
        self.LEVEL_DATA = self._build_level_data()
    
    def _build_level_data(self):
        """构建逐级数据（优化版：使用字典索引）"""
        # 数据字典：(品阶, 等级) -> (能力值, 单级消耗, 累计消耗)
        data_dict = {}
        
        # 黄阶 1-36级，每级消耗1个
        ability = 55
        for lv in range(1, 37):
            data_dict[('黄阶', lv)] = (ability, 1, lv)
            ability += 110
        
        # 玄阶 1-49级，每级消耗1个
        ability = 40
        for lv in range(1, 50):
            data_dict[('玄阶', lv)] = (ability, 1, lv)
            ability += 60 + (lv - 1) * 30
        
        # 地阶 1-64级，每级消耗1个
        ability = 28
        for lv in range(1, 65):
            data_dict[('地阶', lv)] = (ability, 1, lv)
            ability += 14 + (lv - 1) * 36
        
        # 天阶 1-100级，消耗量递增
        ability = 1590
        cumulative = 0
        for lv in range(1, 101):
            # 根据等级确定消耗量
            if lv <= 81:
                cost = 1
            elif lv <= 83:
                cost = 2
            elif lv <= 85:
                cost = 3
            elif lv <= 87:
                cost = 4
            elif lv <= 89:
                cost = 6
            elif lv <= 91:
                cost = 8
            elif lv <= 93:
                cost = 10
            elif lv <= 95:
                cost = 12
            elif lv <= 97:
                cost = 14
            elif lv <= 99:
                cost = 16
            else:  # 100
                cost = 18
            
            cumulative += cost
            data_dict[('天阶', lv)] = (ability, cost, cumulative)
            ability += 9222
        
        return data_dict
    
    def _build_ui(self):
        """创建界面（参考注灵工具）"""
        # 主滚动容器
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)
        
        # ---- 页面标题 ----
        ctk.CTkLabel(
            scroll,
            text="🔮 遁甲（强运）养成计算器",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        ctk.CTkLabel(
            scroll,
            text="4个品阶体系 · 黄阶→玄阶→地阶→天阶 · 共398个材料满级",
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
            selected_color=self.colors.get("nav_active", "#0f3460"),
            unselected_color="#0f0f1a",
            selected_hover_color="#164080",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("📊 根据材料计算等级")
        
        # ============================================================
        # Tab 1：根据持有材料计算可达等级
        # ============================================================
        self.tab1_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        tab1_inner = ctk.CTkFrame(self.tab1_frame, fg_color="transparent")
        tab1_inner.pack(fill="x", padx=20, pady=18)
        tab1_inner.grid_columnconfigure((0, 1), weight=1)
        
        # 初始状态标题
        ctk.CTkLabel(
            tab1_inner, text="初始遁甲状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        
        # 当前品阶
        ctk.CTkLabel(tab1_inner, text="当前品阶",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t1_grade_var = ctk.StringVar(value="黄阶")
        self.t1_grade_menu = ctk.CTkOptionMenu(
            tab1_inner, variable=self.t1_grade_var,
            values=self.GRADE_ORDER, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t1_grade_menu.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        
        # 当前等级
        ctk.CTkLabel(tab1_inner, text="当前等级",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t1_level_entry = ctk.CTkEntry(tab1_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_level_entry.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.t1_level_entry.insert(0, "0")
        
        # ---- 材料输入 ----
        ctk.CTkLabel(tab1_inner, text="持有材料数量",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(6, 3))
        
        # 创建材料输入框
        self.t1_mat_entries = {}
        row_idx = 4
        for grade_name, grade_info in self.GRADES.items():
            mat_name = grade_info['material']
            
            ctk.CTkLabel(tab1_inner, text=mat_name,
                         font=ctk.CTkFont(size=12),
                         text_color=self.colors["text"], anchor="w").grid(
                row=row_idx, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
            
            entry = ctk.CTkEntry(tab1_inner, placeholder_text="数量", height=30, corner_radius=6, fg_color="#0f0f1a")
            entry.insert(0, "0")
            entry.grid(row=row_idx + 1, column=0, sticky="ew", padx=(0, 10), pady=(0, 6))
            self.t1_mat_entries[grade_name] = entry
            row_idx += 2
        
        # 计算按钮
        ctk.CTkButton(
            tab1_inner,
            text="▶  计算可达到的遁甲等级",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#0f3460", hover_color="#16213e",
            command=self._calc_by_materials,
        ).grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(8, 8))
        
        # 结果区域
        self.t1_result = ctk.CTkTextbox(
            tab1_inner, height=180, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(family="Microsoft YaHei UI", size=12),
        )
        self.t1_result.grid(row=row_idx+1, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")
        # 阻止滚轮事件冒泡
        self._bind_mousewheel(self.t1_result)
        
        # ============================================================
        # Tab 2：根据目标等级计算所需材料
        # ============================================================
        self.tab2_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        # 不立即 grid，由标签页切换控制
        
        tab2_inner = ctk.CTkFrame(self.tab2_frame, fg_color="transparent")
        tab2_inner.pack(fill="x", padx=20, pady=18)
        tab2_inner.grid_columnconfigure((0, 1), weight=1)
        
        # 初始状态
        ctk.CTkLabel(
            tab2_inner, text="初始遁甲状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        
        ctk.CTkLabel(tab2_inner, text="当前品阶",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t2_start_grade_var = ctk.StringVar(value="黄阶")
        self.t2_start_grade_menu = ctk.CTkOptionMenu(
            tab2_inner, variable=self.t2_start_grade_var,
            values=self.GRADE_ORDER, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t2_start_grade_menu.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        
        ctk.CTkLabel(tab2_inner, text="当前等级",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t2_start_level_entry = ctk.CTkEntry(tab2_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_start_level_entry.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.t2_start_level_entry.insert(0, "0")
        
        # 目标状态
        ctk.CTkLabel(
            tab2_inner, text="目标遁甲状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 8))
        
        ctk.CTkLabel(tab2_inner, text="目标品阶",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=4, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t2_target_grade_var = ctk.StringVar(value="天阶")
        self.t2_target_grade_menu = ctk.CTkOptionMenu(
            tab2_inner, variable=self.t2_target_grade_var,
            values=self.GRADE_ORDER, height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t2_target_grade_menu.grid(row=5, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        
        ctk.CTkLabel(tab2_inner, text="目标等级",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=4, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t2_target_level_entry = ctk.CTkEntry(tab2_inner, placeholder_text="100", height=32, corner_radius=6)
        self.t2_target_level_entry.grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.t2_target_level_entry.insert(0, "100")
        
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
            tab2_inner, height=240, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(family="Microsoft YaHei UI", size=12),
        )
        self.t2_result.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.t2_result.insert("1.0", "等待计算...\n")
        self.t2_result.configure(state="disabled")
        # 阻止滚轮事件冒泡
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
            "• 功能一：输入持有的各材料数量 + 当前状态 → 算最多能升到几级",
            "• 功能二：设定起始/目标状态 → 算所需材料明细和汇总",
            "",
            "4个品阶体系：黄阶(36级) → 玄阶(49级) → 地阶(64级) → 天阶(100级)",
            "4种材料独立：古迹灵石、古迹灵石·玄、古迹灵石·地、古迹灵石·天",
            "天阶后期递增：81级后每级消耗逐步增加到18个",
            "满级总计：从黄阶1级到天阶100级共需398个材料",
        ]
        for rule in rules:
            ctk.CTkLabel(
                info_inner, text=rule,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"], anchor="w",
            ).pack(fill="x", pady=1)
    
    def _on_tab_change(self, value):
        """切换标签页"""
        if value == "📊 根据材料计算等级":
            self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2_frame.grid_forget()
        else:
            self.tab2_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1_frame.grid_forget()
    
    def _show_result(self, textbox: ctk.CTkTextbox, text: str):
        """显示结果"""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
    
    def _show_error(self, textbox: ctk.CTkTextbox, msg: str):
        """显示错误"""
        self._show_result(textbox, f"⚠️ {msg}\n")
    
    def _bind_mousewheel(self, widget):
        """绑定滚轮事件，阻止事件冒泡"""
        def on_mousewheel(event):
            # 只在widget内部处理滚轮事件，不让事件继续传播
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"  # 阻止事件冒泡
        
        # 绑定Windows/MacOS的滚轮事件
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        # 绑定Linux的滚轮事件
        widget.bind("<Button-4>", lambda e: (widget._parent_canvas.yview_scroll(-1, "units"), "break")[1], add="+")
        widget.bind("<Button-5>", lambda e: (widget._parent_canvas.yview_scroll(1, "units"), "break")[1], add="+")
    
    def _get_level_cost(self, grade, level):
        """获取指定品阶等级的升级消耗 (O(1)优化)"""
        data = self.LEVEL_DATA.get((grade, level))
        return data[1] if data else 0
    
    def _get_cumulative_cost(self, grade, level):
        """获取品阶内累计消耗 (O(1)优化)"""
        data = self.LEVEL_DATA.get((grade, level))
        return data[2] if data else 0
    
    def _get_ability(self, grade, level):
        """获取能力值 (O(1)优化)"""
        data = self.LEVEL_DATA.get((grade, level))
        return data[0] if data else 0
    
    def _calc_by_materials(self):
        """模式1：根据材料计算可达等级"""
        try:
            current_grade = self.t1_grade_var.get()
            current_level = int(self.t1_level_entry.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "当前等级请输入有效数字！")
            return
        
        # 验证当前等级
        max_level = self.GRADES[current_grade]['max_level']
        if current_level < 0 or current_level > max_level:
            self._show_error(self.t1_result, f"{current_grade}等级范围为0-{max_level}")
            return
        
        # 读取持有材料
        materials = {}
        for grade_name, entry in self.t1_mat_entries.items():
            txt = entry.get().strip()
            materials[grade_name] = int(txt) if txt else 0
        
        # 如果所有材料都是0
        if all(v == 0 for v in materials.values()):
            self._show_error(self.t1_result, "请输入至少一种材料的数量")
            return
        
        # 计算可达等级
        result = self._calc_reachable_level(current_grade, current_level, materials)
        
        # 在文本框中显示详细结果
        output = f"✅ 计算完成\n\n"
        output += f"{'='*50}\n"
        output += f"起始状态: {current_grade} Lv.{current_level}\n"
        output += f"可达状态: {result['final_grade']} Lv.{result['final_level']}\n"
        output += f"{'='*50}\n\n"
        
        # 材料使用汇总
        output += "【材料使用汇总】\n"
        for grade_name in self.GRADE_ORDER:
            used = result['used_materials'][grade_name]
            if used > 0:
                material_name = self.GRADES[grade_name]['material']
                available = materials[grade_name]
                output += f"  {material_name}: 使用 {used}/{available} 个\n"
        output += f"\n{'='*50}\n\n"
        
        # 详细升级路径（只显示关键节点）
        output += "【升级路径】\n"
        path_lines = []
        for item in result['path']:
            if "满级" in item[0]:
                # 进阶节点
                path_lines.append(f"\n>>> {item[0]} {item[1]} {item[2]} <<<\n")
            else:
                # 只显示每5级或最后一级
                lv = int(item[1].replace("Lv.", ""))
                if lv % 5 == 0 or lv == result['final_level'] or lv == 1:
                    path_lines.append(
                        f"  {item[0]} {item[1]}: 能力值 {item[2]}, "
                        f"消耗 {item[3]}, 累计已用 {item[5]} 个"
                    )
        
        output += "\n".join(path_lines[:50])  # 限制显示行数
        if len(path_lines) > 50:
            output += f"\n\n... (共{len(result['path'])}级，仅显示关键节点) ...\n"
        
        self._show_result(self.t1_result, output)
    
    def _calc_reachable_level(self, start_grade, start_level, materials):
        """计算可达等级"""
        start_idx = self.GRADE_ORDER.index(start_grade)
        current_level = start_level
        
        path = []
        used_materials = {grade: 0 for grade in self.GRADES.keys()}
        
        for grade_idx in range(start_idx, len(self.GRADE_ORDER)):
            grade_name = self.GRADE_ORDER[grade_idx]
            max_level = self.GRADES[grade_name]['max_level']
            material_name = self.GRADES[grade_name]['material']
            available = materials[grade_name]
            
            # 如果是当前品阶，从当前等级开始；否则从1级开始
            if grade_idx == start_idx:
                start_lv = current_level
            else:
                start_lv = 0
            
            # 逐级累加消耗
            for lv in range(start_lv + 1, max_level + 1):
                # 查询该等级的消耗
                cost = self._get_level_cost(grade_name, lv)
                
                if used_materials[grade_name] + cost <= available:
                    used_materials[grade_name] += cost
                    current_level = lv
                    
                    # 记录路径
                    cumulative = self._get_cumulative_cost(grade_name, lv)
                    ability = self._get_ability(grade_name, lv)
                    path.append([
                        grade_name,
                        f"Lv.{lv}",
                        ability,
                        f"{material_name} ×{cost}",
                        cumulative,
                        used_materials[grade_name]
                    ])
                else:
                    # 材料不足，停止
                    break
            
            # 如果没有升到满级，停止进阶
            if current_level < max_level:
                break
            
            # 重置等级计数，准备进阶
            if grade_idx < len(self.GRADE_ORDER) - 1:
                current_level = 0
                # 记录进阶节点
                path.append([
                    f"【{grade_name}满级】",
                    "→",
                    f"进阶到{self.GRADE_ORDER[grade_idx + 1]}",
                    "无额外消耗",
                    "-",
                    "-"
                ])
        
        # 确定最终品阶
        final_grade = grade_name
        final_level = current_level
        
        return {
            'final_grade': final_grade,
            'final_level': final_level,
            'used_materials': used_materials,
            'path': path
        }
    
    def _calc_by_target(self):
        """模式2：根据目标计算材料需求"""
        try:
            start_grade = self.t2_start_grade_var.get()
            start_level = int(self.t2_start_level_entry.get() or "0")
            target_grade = self.t2_target_grade_var.get()
            target_level = int(self.t2_target_level_entry.get() or "100")
        except ValueError:
            self._show_error(self.t2_result, "等级请输入有效数字！")
            return
        
        # 验证等级范围
        start_max = self.GRADES[start_grade]['max_level']
        if start_level < 0 or start_level > start_max:
            self._show_error(self.t2_result, f"{start_grade}等级范围为0-{start_max}")
            return
        
        target_max = self.GRADES[target_grade]['max_level']
        if target_level < 1 or target_level > target_max:
            self._show_error(self.t2_result, f"{target_grade}等级范围为1-{target_max}")
            return
        
        # 验证目标必须大于当前
        start_idx = self.GRADE_ORDER.index(start_grade)
        target_idx = self.GRADE_ORDER.index(target_grade)
        
        if target_idx < start_idx or (target_idx == start_idx and target_level <= start_level):
            self._show_error(self.t2_result, "目标等级必须高于当前等级")
            return
        
        # 计算所需材料
        result = self._calc_required_materials(start_grade, start_level, target_grade, target_level)
        
        # 在文本框中显示详细结果
        output = f"✅ 计算完成\n\n"
        output += f"{'='*50}\n"
        output += f"起始状态: {start_grade} Lv.{start_level}\n"
        output += f"目标状态: {target_grade} Lv.{target_level}\n"
        output += f"{'='*50}\n\n"
        
        # 材料需求汇总
        output += "【材料需求汇总】\n"
        total_cost = 0
        for grade_name in self.GRADE_ORDER:
            needed = result['required'][grade_name]
            if needed > 0:
                material_name = self.GRADES[grade_name]['material']
                output += f"  {material_name}: {needed} 个\n"
                total_cost += needed
        output += f"\n  总计: {total_cost} 个材料\n"
        output += f"\n{'='*50}\n\n"
        
        # 详细升级路径（按品阶分组显示）
        output += "【升级路径详情】\n"
        current_display_grade = None
        line_count = 0
        max_lines = 40
        
        for item in result['path']:
            if "满级" in item[0]:
                # 进阶节点
                output += f"\n>>> {item[0]} {item[1]} {item[2]} <<<\n\n"
                current_display_grade = None
            else:
                grade = item[0]
                lv_str = item[1]
                lv = int(lv_str.replace("Lv.", ""))
                
                # 品阶开始时显示标题
                if grade != current_display_grade:
                    output += f"\n【{grade}】\n"
                    current_display_grade = grade
                
                # 只显示每5级或最后关键节点
                if lv % 10 == 0 or lv == int(target_level) or line_count < 10:
                    output += f"  {lv_str}: 能力值 {item[2]}, 消耗 {item[3]}\n"
                    line_count += 1
                    
                if line_count >= max_lines:
                    output += f"\n... (共{len(result['path'])}条，仅显示关键节点) ...\n"
                    break
        
        self._show_result(self.t2_result, output)
    
    def _calc_required_materials(self, start_grade, start_level, end_grade, end_level):
        """计算所需材料"""
        start_idx = self.GRADE_ORDER.index(start_grade)
        end_idx = self.GRADE_ORDER.index(end_grade)
        
        required = {grade: 0 for grade in self.GRADES.keys()}
        path = []
        
        for grade_idx in range(start_idx, end_idx + 1):
            grade_name = self.GRADE_ORDER[grade_idx]
            max_level = self.GRADES[grade_name]['max_level']
            material_name = self.GRADES[grade_name]['material']
            
            # 确定起始和结束等级
            if grade_idx == start_idx:
                from_lv = start_level
            else:
                from_lv = 0
            
            if grade_idx == end_idx:
                to_lv = end_level
            else:
                to_lv = max_level
            
            # 累加该品阶的消耗
            for lv in range(from_lv + 1, to_lv + 1):
                cost = self._get_level_cost(grade_name, lv)
                required[grade_name] += cost
                
                # 记录路径
                cumulative = self._get_cumulative_cost(grade_name, lv)
                ability = self._get_ability(grade_name, lv)
                path.append([
                    grade_name,
                    f"Lv.{lv}",
                    ability,
                    f"{material_name} ×{cost}",
                    cumulative,
                    required[grade_name]
                ])
            
            # 记录进阶节点
            if grade_idx < end_idx:
                path.append([
                    f"【{grade_name}满级】",
                    "→",
                    f"进阶到{self.GRADE_ORDER[grade_idx + 1]}",
                    "无额外消耗",
                    "-",
                    "-"
                ])
        
        return {
            'start_grade': start_grade,
            'start_level': start_level,
            'end_grade': end_grade,
            'end_level': end_level,
            'required': required,
            'path': path
        }




