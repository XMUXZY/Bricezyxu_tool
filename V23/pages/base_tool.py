"""
页面基类 - 统一公共方法与 UI 骨架
所有工具页面都应继承此基类，以复用通用功能和统一布局风格
"""

import customtkinter as ctk
from typing import List, Optional, Tuple


class BaseToolPage(ctk.CTkFrame):
    """工具页面基类

    提供两大类能力：

    A) 通用工具方法（原有）：
        - _show_result: 在 CTkTextbox 中显示结果
        - _show_error: 在 CTkTextbox 中显示错误信息
        - _bind_mousewheel: 阻止嵌套滚动区的滚轮事件冒泡
        - _parse_int: 安全解析整数
        - _parse_float_or_inf: 解析浮点数或无穷大
        - _fmt: 数字格式化

    B) UI 骨架构建器（新增）：
        - _create_scroll_container: 创建主滚动容器
        - _create_title: 创建标题 + 副标题
        - _create_tab_switcher: 创建 SegmentedButton 双 Tab 切换器
        - _create_tab_frame: 创建 Tab 内容卡片容器
        - _create_result_box: 创建结果展示文本框
        - _create_calc_button: 创建计算按钮
        - _create_info_section: 创建底部说明卡片
        - _on_tab_change: 通用 Tab 切换逻辑

    典型用法（双 Tab 计算器）：
        scroll = self._create_scroll_container()
        self._create_title(scroll, "⚔️ XX计算器", "描述信息", row=0)
        self.tab_seg = self._create_tab_switcher(scroll, ["Tab1", "Tab2"], row=2)
        self.tab1 = self._create_tab_frame(scroll, row=3, visible=True)
        self.tab2 = self._create_tab_frame(scroll, row=3, visible=False)
        ...
        self._create_info_section(scroll, "使用说明", [...], row=4)
    """

    # 错误提示前缀，子类可覆盖
    _error_prefix = "⚠️"

    # ================================================================
    # 标准颜色常量（子类可直接引用）
    # ================================================================
    CARD_BG = "#1a1a2e"         # 卡片/Tab 内容区背景色
    INPUT_BG = "#0f0f1a"        # 输入框/结果框背景色
    BTN_PRIMARY = "#0f3460"     # 主按钮颜色
    BTN_PRIMARY_HOVER = "#16213e"
    BTN_SECONDARY = "#2a2a4a"   # 次按钮颜色
    BTN_SECONDARY_HOVER = "#3a3a5a"
    SEPARATOR_COLOR = "#2a2a4a"
    TAB_UNSELECTED_BG = "#0f0f1a"
    TAB_HOVER = "#164080"

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
        # Tab 框架引用（由 _create_tab_switcher 自动管理）
        self._tab_frames: List[ctk.CTkFrame] = []
        self._tab_labels: List[str] = []
        # 子类应在 __init__ 末尾调用 self._build_ui()

    def _build_ui(self):
        """构建界面（子类必须实现）"""
        raise NotImplementedError("子类必须实现 _build_ui 方法")

    # ================================================================
    # A) UI 骨架构建器
    # ================================================================

    def _create_scroll_container(self, padx: int = 30, pady: int = 20) -> ctk.CTkScrollableFrame:
        """创建主滚动容器

        几乎所有工具页面的顶层布局都是一个带透明背景的 CTkScrollableFrame。
        返回该容器，子类在其上用 grid 布局放置子控件。

        Args:
            padx: 水平内边距（默认30）
            pady: 垂直内边距（默认20）

        Returns:
            CTkScrollableFrame 实例
        """
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=padx, pady=pady)
        scroll.grid_columnconfigure(0, weight=1)
        return scroll

    def _create_title(self, parent, title: str, subtitle: str = "",
                      row: int = 0) -> None:
        """创建标题 + 副标题行

        在 parent 容器内以 grid 方式放置标题（row）和副标题（row+1）。

        Args:
            parent: 父容器（通常是 scroll）
            title: 主标题文本（含 emoji，如 "⚔️ XX计算器"）
            subtitle: 副标题文本（功能简述）
            row: 标题所在的 grid 行号（副标题自动占 row+1）
        """
        ctk.CTkLabel(
            parent,
            text=title,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=row, column=0, sticky="w", pady=(0, 5 if subtitle else 15))

        if subtitle:
            ctk.CTkLabel(
                parent,
                text=subtitle,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"],
                anchor="w",
            ).grid(row=row + 1, column=0, sticky="w", pady=(0, 15))

    def _create_tab_switcher(self, parent, tab_labels: List[str],
                             row: int = 2,
                             default: int = 0) -> ctk.CTkSegmentedButton:
        """创建 SegmentedButton Tab 切换器

        自动绑定 _on_tab_change 回调。子类应配合 _create_tab_frame
        创建对应的 tab 内容区，它们会被自动切换显示/隐藏。

        Args:
            parent: 父容器（通常是 scroll）
            tab_labels: Tab 标签文本列表，如 ["📊 根据材料计算等级", "🎯 根据目标计算材料"]
            row: 所在的 grid 行号
            default: 默认选中的 Tab 索引（默认0）

        Returns:
            CTkSegmentedButton 实例
        """
        self._tab_labels = tab_labels
        self._tab_frames = []  # 重置，等 _create_tab_frame 填充

        tab_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tab_frame.grid(row=row, column=0, sticky="ew", pady=(0, 12))

        seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=tab_labels,
            height=34,
            font=ctk.CTkFont(size=13),
            selected_color=self.colors.get("nav_active", self.BTN_PRIMARY),
            unselected_color=self.TAB_UNSELECTED_BG,
            selected_hover_color=self.TAB_HOVER,
            command=self._on_tab_change,
        )
        seg.pack(fill="x")
        seg.set(tab_labels[default])
        return seg

    def _create_tab_frame(self, parent, row: int = 3,
                          visible: bool = True) -> ctk.CTkFrame:
        """创建 Tab 内容卡片容器

        每次调用会创建一个深色圆角卡片框，并自动注册到内部 _tab_frames 列表。
        第一个 visible=True 的 Tab 会显示，其余隐藏。

        Args:
            parent: 父容器（通常是 scroll）
            row: 所在的 grid 行号（通常所有 Tab 共用同一 row）
            visible: 是否初始可见

        Returns:
            CTkFrame 实例（子类在其中 pack/grid 输入控件）
        """
        frame = ctk.CTkFrame(parent, fg_color=self.CARD_BG, corner_radius=12)
        if visible:
            frame.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        self._tab_frames.append(frame)
        return frame

    def _on_tab_change(self, value: str):
        """通用 Tab 切换逻辑

        根据当前选中的 tab_label，显示对应的 tab_frame，隐藏其余。
        子类如需额外处理，可覆盖此方法（记得先调 super）。

        Args:
            value: 被选中的 Tab 标签文本
        """
        if not self._tab_labels or not self._tab_frames:
            return

        try:
            idx = self._tab_labels.index(value)
        except ValueError:
            return

        for i, frame in enumerate(self._tab_frames):
            if i == idx:
                frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            else:
                frame.grid_forget()

    def _create_tab_inner(self, tab_frame: ctk.CTkFrame,
                          columns: int = 2) -> ctk.CTkFrame:
        """在 Tab 卡片内创建标准内容区（带内边距和多列网格）

        Args:
            tab_frame: 由 _create_tab_frame 创建的卡片容器
            columns: 网格列数（默认2列，用于左右并排输入控件）

        Returns:
            CTkFrame 实例（在其中 grid 输入控件）
        """
        inner = ctk.CTkFrame(tab_frame, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        if columns > 1:
            inner.grid_columnconfigure(tuple(range(columns)), weight=1)
        else:
            inner.grid_columnconfigure(0, weight=1)
        return inner

    def _create_result_box(self, parent, row: int,
                           height: int = 200,
                           placeholder: str = "等待计算…\n",
                           columnspan: int = 2,
                           font_size: int = 12) -> ctk.CTkTextbox:
        """创建结果展示文本框

        创建一个只读的 CTkTextbox，自动绑定滚轮事件防冒泡。

        Args:
            parent: 父容器（通常是 tab 内的 inner frame）
            row: grid 行号
            height: 文本框高度
            placeholder: 初始占位文本
            columnspan: 跨列数
            font_size: 字体大小

        Returns:
            CTkTextbox 实例
        """
        tb = ctk.CTkTextbox(
            parent, height=height, corner_radius=8,
            fg_color=self.INPUT_BG,
            font=ctk.CTkFont(family="Microsoft YaHei UI", size=font_size),
        )
        tb.grid(row=row, column=0, columnspan=columnspan, sticky="ew", pady=(0, 0))
        if placeholder:
            tb.insert("1.0", placeholder)
        tb.configure(state="disabled")
        self._bind_mousewheel(tb)
        return tb

    def _create_calc_button(self, parent, text: str = "▶  开始计算",
                            command=None, row: int = 0,
                            columnspan: int = 2) -> ctk.CTkButton:
        """创建标准计算按钮

        Args:
            parent: 父容器
            text: 按钮文本
            command: 点击回调
            row: grid 行号
            columnspan: 跨列数

        Returns:
            CTkButton 实例
        """
        btn = ctk.CTkButton(
            parent,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color=self.BTN_PRIMARY,
            hover_color=self.BTN_PRIMARY_HOVER,
            command=command,
        )
        btn.grid(row=row, column=0, columnspan=columnspan, sticky="ew", pady=(8, 8))
        return btn

    def _create_input_label(self, parent, text: str, row: int,
                            column: int = 0, columnspan: int = 1,
                            padx: Tuple[int, int] = (0, 0)) -> ctk.CTkLabel:
        """创建输入项标签

        Args:
            parent: 父容器
            text: 标签文本
            row: grid 行号
            column: grid 列号
            columnspan: 跨列数
            padx: 水平内边距

        Returns:
            CTkLabel 实例
        """
        lbl = ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"], anchor="w",
        )
        lbl.grid(row=row, column=column, columnspan=columnspan,
                 sticky="w", padx=padx, pady=(0, 3))
        return lbl

    def _create_input_entry(self, parent, row: int, column: int = 0,
                            placeholder: str = "0",
                            default: str = "0",
                            padx: Tuple[int, int] = (0, 0),
                            columnspan: int = 1) -> ctk.CTkEntry:
        """创建标准输入框

        Args:
            parent: 父容器
            row: grid 行号
            column: grid 列号
            placeholder: 占位文本
            default: 默认值
            padx: 水平内边距
            columnspan: 跨列数

        Returns:
            CTkEntry 实例
        """
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder,
            height=32, corner_radius=6,
        )
        entry.grid(row=row, column=column, columnspan=columnspan,
                   sticky="ew", padx=padx, pady=(0, 8))
        if default:
            entry.insert(0, default)
        return entry

    def _create_input_option(self, parent, row: int, column: int = 0,
                             values: List[str] = None,
                             padx: Tuple[int, int] = (0, 0),
                             columnspan: int = 1,
                             command=None) -> ctk.CTkOptionMenu:
        """创建标准下拉选择框

        Args:
            parent: 父容器
            row: grid 行号
            column: grid 列号
            values: 选项列表
            padx: 水平内边距
            columnspan: 跨列数
            command: 选择变化回调

        Returns:
            CTkOptionMenu 实例
        """
        opt = ctk.CTkOptionMenu(
            parent, values=values or [],
            height=32, corner_radius=6,
            fg_color=self.BTN_PRIMARY,
            button_color=self.BTN_PRIMARY,
            button_hover_color=self.BTN_PRIMARY_HOVER,
            command=command,
        )
        opt.grid(row=row, column=column, columnspan=columnspan,
                 sticky="ew", padx=padx, pady=(0, 8))
        return opt

    def _create_section_title(self, parent, text: str, row: int,
                              column: int = 0, columnspan: int = 2) -> ctk.CTkLabel:
        """创建分区小标题（如 "初始状态"、"目标设置"）

        Args:
            parent: 父容器
            text: 小标题文本
            row: grid 行号
            column: grid 列号
            columnspan: 跨列数

        Returns:
            CTkLabel 实例
        """
        lbl = ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        )
        lbl.grid(row=row, column=column, columnspan=columnspan,
                 sticky="w", pady=(0, 6))
        return lbl

    def _create_info_section(self, parent, title: str,
                             rules: List[str], row: int = 4) -> ctk.CTkFrame:
        """创建底部说明信息卡片

        包含一个带 📖 图标的标题和多条说明文本。

        Args:
            parent: 父容器（通常是 scroll）
            title: 说明标题（如 "养成说明"、"使用说明"）
            rules: 说明条目列表（每条一行文本，建议以 "·" 或 "•" 开头）
            row: 所在的 grid 行号

        Returns:
            CTkFrame 卡片容器
        """
        info_card = ctk.CTkFrame(parent, fg_color=self.CARD_BG, corner_radius=12)
        info_card.grid(row=row, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            info_inner,
            text=f"📖 {title}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).pack(fill="x", pady=(0, 8))

        for rule in rules:
            ctk.CTkLabel(
                info_inner, text=rule,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"], anchor="w",
            ).pack(fill="x", pady=1)

        return info_card

    # ================================================================
    # B) 结果显示方法（原有）
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
    # C) 滚轮事件处理（原有）
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
    # D) 数据解析工具方法（原有）
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
    # E) 数字格式化（原有，子类可覆盖）
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
