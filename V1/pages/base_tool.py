"""
页面基类 - 统一公共方法
所有工具页面都应继承此基类，以复用通用功能
"""

import customtkinter as ctk


class BaseToolPage(ctk.CTkFrame):
    """工具页面基类
    
    提供所有工具页面通用的方法：
    - _show_result: 在 CTkTextbox 中显示结果
    - _show_error: 在 CTkTextbox 中显示错误信息
    - _bind_mousewheel: 阻止嵌套滚动区的滚轮事件冒泡
    - _parse_int: 安全解析整数
    - _parse_float_or_inf: 解析浮点数或无穷大
    
    子类可覆盖 _error_prefix 属性来自定义错误提示前缀。
    """
    
    # 错误提示前缀，子类可覆盖
    _error_prefix = "⚠"
    
    def __init__(self, parent, colors: dict = None):
        """初始化基类
        
        Args:
            parent: 父容器
            colors: 颜色配置字典，如果为None则使用默认配置
        """
        super().__init__(parent, fg_color="transparent")
        self.colors = colors or {
            "text": "#e0e0e0",
            "text_dim": "#888888",
            "nav_active": "#0f3460"
        }
        # 子类应在 __init__ 末尾调用 self._build_ui()
    
    def _build_ui(self):
        """构建界面（子类必须实现）"""
        raise NotImplementedError("子类必须实现 _build_ui 方法")
    
    # ================================================================
    # 结果显示方法
    # ================================================================
    
    def _show_result(self, textbox: ctk.CTkTextbox, text: str):
        """在结果文本框中显示内容
        
        Args:
            textbox: CTkTextbox 控件
            text: 要显示的文本内容
        """
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
    
    def _show_error(self, textbox: ctk.CTkTextbox, msg: str):
        """在结果文本框中显示错误信息
        
        Args:
            textbox: CTkTextbox 控件
            msg: 错误消息
        """
        self._show_result(textbox, f"{self._error_prefix} {msg}\n")
    
    # ================================================================
    # 滚轮事件处理
    # ================================================================
    
    def _bind_mousewheel(self, widget):
        """绑定滚轮事件，阻止事件冒泡到父容器
        
        用于嵌套的 CTkScrollableFrame 和 CTkTextbox，
        防止滚轮事件传播到外层滚动区域。
        
        Args:
            widget: CTkTextbox 或其他支持 _parent_canvas 的控件
        """
        def on_mousewheel(event):
            # 只在 widget 内部处理滚轮事件，不让事件继续传播
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"  # 阻止事件冒泡
        
        # 绑定 Windows/MacOS 的滚轮事件
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        # 绑定 Linux 的滚轮事件
        widget.bind("<Button-4>", lambda e: (widget._parent_canvas.yview_scroll(-1, "units"), "break")[1], add="+")
        widget.bind("<Button-5>", lambda e: (widget._parent_canvas.yview_scroll(1, "units"), "break")[1], add="+")
    
    # ================================================================
    # 数据解析工具方法
    # ================================================================
    
    @staticmethod
    def _parse_int(val: str, default: int) -> int:
        """安全解析整数，解析失败时返回默认值
        
        Args:
            val: 要解析的字符串
            default: 解析失败时的默认值
        
        Returns:
            解析结果或默认值
        """
        try:
            return int((val or "").strip() or str(default))
        except (ValueError, AttributeError):
            return default
    
    @staticmethod
    def _parse_float_or_inf(val: str) -> float:
        """解析浮点数，空值或解析失败时返回无穷大
        
        用于"材料不限"的场景。
        
        Args:
            val: 要解析的字符串
        
        Returns:
            解析结果或 float('inf')
        """
        v = (val or "").strip()
        if not v:
            return float("inf")
        try:
            return float(v)
        except (ValueError, AttributeError):
            return float("inf")
    
    # ================================================================
    # 数字格式化（可选，子类可覆盖或不使用）
    # ================================================================
    
    @staticmethod
    def _fmt(num) -> str:
        """格式化数字显示（通用版本）
        
        子类如有特殊格式化需求可覆盖此方法。
        
        Args:
            num: 数字（int/float）
        
        Returns:
            格式化后的字符串
        """
        if isinstance(num, float) and num == float("inf"):
            return "∞"
        if isinstance(num, float):
            if num >= 10000:
                return f"{num:,.0f}"
            if num >= 100:
                return f"{num:,.1f}"
            return f"{num:.1f}"
        # int
        return f"{num:,}"
