"""
新工具页面模板
复制此文件并修改即可快速创建新工具页面
"""

import customtkinter as ctk
from pages.base_tool import BaseToolPage


class ToolTemplatePage(BaseToolPage):
    """工具页面模板（继承自 BaseToolPage）"""
    
    def __init__(self, parent, colors: dict = None):
        """初始化页面
        
        Args:
            parent: 父容器
            colors: 颜色配置字典
        """
        super().__init__(parent, colors)
        # 在这里初始化页面特有的属性
        # 例如：self.data = self._load_data()
        self._build_ui()
    
    def _build_ui(self):
        """构建页面界面（必须实现）"""
        # 创建主滚动容器
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)
        
        # ---- 页面标题 ----
        ctk.CTkLabel(
            scroll,
            text="🔧 新工具页面标题",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        ctk.CTkLabel(
            scroll,
            text="工具描述和简要说明",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))
        
        # ---- 主要功能区 ----
        main_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        main_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        inner = ctk.CTkFrame(main_frame, fg_color="transparent")
        inner.pack(fill="both", padx=20, pady=18)
        inner.grid_columnconfigure(0, weight=1)
        
        # 在这里添加输入控件
        ctk.CTkLabel(
            inner, text="输入项1",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"], anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 3))
        
        self.input1 = ctk.CTkEntry(inner, placeholder_text="请输入...", height=32, corner_radius=6)
        self.input1.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        
        # 计算按钮
        ctk.CTkButton(
            inner,
            text="▶  开始计算",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#0f3460", hover_color="#16213e",
            command=self._calculate,
        ).grid(row=2, column=0, sticky="ew", pady=(8, 8))
        
        # 结果显示区
        self.result_box = ctk.CTkTextbox(
            inner, height=200, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(family="Microsoft YaHei UI", size=12),
        )
        self.result_box.grid(row=3, column=0, sticky="ew", pady=(0, 0))
        self.result_box.insert("1.0", "等待计算...\n")
        self.result_box.configure(state="disabled")
        # 阻止滚轮事件冒泡（使用基类方法）
        self._bind_mousewheel(self.result_box)
        
        # ---- 使用说明卡片 ----
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            info_inner,
            text="📖 使用说明",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).pack(fill="x", pady=(0, 8))
        
        rules = [
            "• 说明条目1",
            "• 说明条目2",
            "• 说明条目3",
        ]
        for rule in rules:
            ctk.CTkLabel(
                info_inner, text=rule,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"], anchor="w",
            ).pack(fill="x", pady=1)
    
    def _calculate(self):
        """计算逻辑（在这里实现具体功能）"""
        try:
            # 获取输入
            input_val = self.input1.get().strip()
            if not input_val:
                self._show_error(self.result_box, "请输入有效内容")
                return
            
            # 执行计算
            result = self._do_calculation(input_val)
            
            # 显示结果（使用基类方法）
            output = "✅ 计算完成\n\n"
            output += f"输入: {input_val}\n"
            output += f"结果: {result}\n"
            self._show_result(self.result_box, output)
            
        except Exception as e:
            self._show_error(self.result_box, f"计算出错: {str(e)}")
    
    def _do_calculation(self, input_val: str):
        """实际的计算逻辑"""
        # 在这里实现具体的计算
        return f"处理后的结果: {input_val}"


# ============================================================
# 如何使用此模板创建新工具：
# 
# 1. 复制此文件到 pages/ 目录，重命名为 tool_xxx.py
# 2. 将类名改为 ToolXxxPage
# 3. 修改 _build_ui() 和 _calculate() 方法
# 4. 在 main.py 中导入并添加到 NAV_ITEMS:
#    from pages.tool_xxx import ToolXxxPage
#    NAV_ITEMS.append(("工具名", "🔧", ToolXxxPage))
# 5. 运行 python main.py 查看效果
# ============================================================
