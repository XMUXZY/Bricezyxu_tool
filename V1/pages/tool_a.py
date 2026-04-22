"""
文字颜色解析工具
解析包含 <color=xxx>文本</color> 格式的文本，实时预览带颜色的效果。
支持十六进制、RGB、RGBA、HSL、颜色名称等多种格式。
"""

import customtkinter as ctk
import re
import tkinter as tk
from tkinter import colorchooser


# ============================================================
# 颜色名称映射表（CSS 常用颜色名称 -> 十六进制）
# ============================================================
COLOR_NAMES = {
    "red": "#ff0000", "green": "#008000", "blue": "#0000ff",
    "white": "#ffffff", "black": "#000000", "yellow": "#ffff00",
    "cyan": "#00ffff", "magenta": "#ff00ff", "orange": "#ffa500",
    "purple": "#800080", "pink": "#ffc0cb", "brown": "#a52a2a",
    "gray": "#808080", "grey": "#808080", "gold": "#ffd700",
    "silver": "#c0c0c0", "navy": "#000080", "teal": "#008080",
    "maroon": "#800000", "olive": "#808000", "lime": "#00ff00",
    "aqua": "#00ffff", "fuchsia": "#ff00ff", "coral": "#ff7f50",
    "salmon": "#fa8072", "tomato": "#ff6347", "crimson": "#dc143c",
    "violet": "#ee82ee", "indigo": "#4b0082", "turquoise": "#40e0d0",
    "tan": "#d2b48c", "khaki": "#f0e68c", "orchid": "#da70d6",
    "plum": "#dda0dd", "sienna": "#a0522d", "peru": "#cd853f",
    "chocolate": "#d2691e", "firebrick": "#b22222",
}

# 常用预设颜色（游戏色表）
PRESET_COLORS = [
    "#f2e37c", "#a6872c", "#ffcf2f", "#c0aa85",
    "#f2e2c7", "#524c42", "#463823", "#bdf3fe",
    "#c6febd", "#ffe4d8", "#c67b79", "#8bb6c4",
    "#bdf3fe", "#d17702", "#05c30e", "#007fff",
    "#c30505", "#05b8c3", "#c305aa", "#7e05c3",
    "#d0c9d2", "#831717",
]

# 示例文本
EXAMPLES = {
    "游戏道具": (
        "游戏道具示例：<color=#ff9900>传说级装备</color>、"
        "<color=#9b59b6>史诗级材料</color>、"
        "<color=#3498db>稀有级消耗品</color>"
    ),
    "系统公告": (
        "系统公告：<color=#e74c3c>紧急维护通知</color>，"
        "服务器将于<color=#f39c12>今晚22:00-24:00</color>进行维护。"
    ),
    "多彩文本": (
        "多彩文本：<color=#e74c3c>红色文字</color>、"
        "<color=#2ecc71>绿色文字</color>、"
        "<color=#3498db>蓝色文字</color>、"
        "<color=#9b59b6>紫色文字</color>"
    ),
    "游戏邮件": (
        "<color=#e8c84a>全新百级区二服已正式开启！版本亮点速览！</color>\n\n"
        "亲爱的英雄：\n"
        "百级区二服目前已正式开启！在这片大陆上，您可以感受到更精简、"
        "更心跳、更平衡、更耐玩的全新体验！\n\n"
        "<color=#e8c84a>【开服狂欢好礼不断】</color>\n"
        "－<color=#e8a030>登录即可领取<华夏同行礼包>！</color>"
        "达到特定等级即可领取强力战魂、天地宝图、永久限定称号等诸多好礼！\n\n"
        "－<color=#e8a030>首充就能骑犀牛！</color>"
        "首充即可获得传说焚天犀、极品天尊魂珠、极品武器等价值8888元宝好礼！\n\n"
        "<color=#e8c84a>【百级服五大全新特色】</color>\n"
        "◆<color=#05b8c3>随时上线随时PK</color>\n"
        "－新增特色精英怪玩法，全天持续刷新，随时上线PK争夺丰富资源！\n"
        "◆<color=#05b8c3>玩法省时又省力</color>\n"
        "－新增主线任务一键跳过，周边玩法减负超50%，活跃还可兑换扫荡令！\n"
        "◆<color=#05b8c3>三五好友可开团</color>\n"
        "－参团选择更灵活，小队也能抢BOSS，集结拉人更轻松！\n"
        "◆<color=#05b8c3>人人轻松合劫七</color>\n"
        "－合魂玩法更亲民，极品战魂轻松合劫七！\n"
        "◆<color=#05b8c3>爽快畅玩还能赚</color>"
    ),
}


def validate_color(color_str: str) -> str | None:
    """
    验证并标准化颜色值，返回十六进制颜色或 None。
    支持：#RRGGBB, #RGB, rgb(), rgba(), hsl(), 颜色名称
    """
    color_str = color_str.strip().lower()

    # 十六进制 #RRGGBB
    if re.match(r'^#[0-9a-f]{6}$', color_str):
        return color_str

    # 十六进制 #RGB -> #RRGGBB
    m = re.match(r'^#([0-9a-f])([0-9a-f])([0-9a-f])$', color_str)
    if m:
        return f"#{m.group(1)*2}{m.group(2)*2}{m.group(3)*2}"

    # rgb(r, g, b)
    m = re.match(r'^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$', color_str)
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if all(0 <= v <= 255 for v in (r, g, b)):
            return f"#{r:02x}{g:02x}{b:02x}"

    # rgba(r, g, b, a) — 忽略 alpha，仅取 RGB
    m = re.match(
        r'^rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*[\d.]+\s*\)$',
        color_str,
    )
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if all(0 <= v <= 255 for v in (r, g, b)):
            return f"#{r:02x}{g:02x}{b:02x}"

    # hsl(h, s%, l%)
    m = re.match(
        r'^hsl\(\s*(\d{1,3})\s*,\s*(\d{1,3})%\s*,\s*(\d{1,3})%\s*\)$',
        color_str,
    )
    if m:
        h, s, l = int(m.group(1)), int(m.group(2)) / 100, int(m.group(3)) / 100
        if 0 <= h <= 360 and 0 <= s <= 1 and 0 <= l <= 1:
            return _hsl_to_hex(h, s, l)

    # 颜色名称
    if color_str in COLOR_NAMES:
        return COLOR_NAMES[color_str]

    return None


def _hsl_to_hex(h: int, s: float, l: float) -> str:
    """HSL 转十六进制颜色"""
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    if h < 60:
        r1, g1, b1 = c, x, 0
    elif h < 120:
        r1, g1, b1 = x, c, 0
    elif h < 180:
        r1, g1, b1 = 0, c, x
    elif h < 240:
        r1, g1, b1 = 0, x, c
    elif h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x
    r = int((r1 + m) * 255)
    g = int((g1 + m) * 255)
    b = int((b1 + m) * 255)
    return f"#{r:02x}{g:02x}{b:02x}"


def parse_color_tags(text: str):
    """
    解析文本中的 <color=xxx>...</color> 标签。
    返回 (segments, unique_colors, tag_count, errors)
    segments: [(text, color_or_None), ...]
    """
    pattern = re.compile(
        r'<color=(#[0-9a-fA-F]{3,6}|rgb\([^)]+\)|rgba\([^)]+\)|hsl\([^)]+\)|[a-zA-Z]+)>'
        r'(.*?)</color>',
        re.DOTALL,
    )

    segments = []
    colors_set = set()
    tag_count = 0
    errors = []
    last_end = 0

    for match in pattern.finditer(text):
        # 匹配前的普通文本
        if match.start() > last_end:
            segments.append((text[last_end:match.start()], None))

        color_raw = match.group(1)
        inner_text = match.group(2)
        tag_count += 1

        validated = validate_color(color_raw)
        if validated:
            colors_set.add(validated)
            segments.append((inner_text, validated))
        else:
            errors.append(f"无效颜色: {color_raw}")
            segments.append((inner_text, "#ff0000"))
            colors_set.add("#ff0000")

        last_end = match.end()

    # 剩余文本
    if last_end < len(text):
        segments.append((text[last_end:], None))

    return segments, list(colors_set), tag_count, errors


class ToolAPage(ctk.CTkFrame):
    """文字颜色解析工具界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self._current_color = "#e74c3c"  # 当前选中的颜色
        self._build_ui()

    # ================================================================
    #  界面构建
    # ================================================================
    def _build_ui(self):
        """构建主界面"""
        # 主容器
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=15, pady=10)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(1, weight=1)

        # ---- 页面标题 ----
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            header,
            text="🎨 文字颜色解析工具",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="输入含颜色代码的文本，实时预览带颜色的效果",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
            anchor="w",
        ).pack(side="left", padx=(15, 0))

        # ---- 左侧：输入区 ----
        left_panel = ctk.CTkFrame(container, fg_color="#1a1a2e", corner_radius=12)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 6))

        self._build_input_panel(left_panel)

        # ---- 右侧：预览区 ----
        right_panel = ctk.CTkFrame(container, fg_color="#1a1a2e", corner_radius=12)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(6, 0))

        self._build_preview_panel(right_panel)

    # ----------------------------------------------------------------
    #  左侧输入面板
    # ----------------------------------------------------------------
    def _build_input_panel(self, parent):
        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=15, pady=12)
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_rowconfigure(1, weight=1)

        # 标题行
        title_row = ctk.CTkFrame(inner, fg_color="transparent")
        title_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkLabel(
            title_row,
            text="📝 输入文本",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#ffffff",
        ).pack(side="left")

        self.char_count_label = ctk.CTkLabel(
            title_row,
            text="字数: 0",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
        )
        self.char_count_label.pack(side="right")

        # 文本输入框
        self.text_input = ctk.CTkTextbox(
            inner,
            corner_radius=8,
            fg_color="#0f0f1a",
            font=ctk.CTkFont(size=13),
            wrap="word",
        )
        self.text_input.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.text_input.bind("<KeyRelease>", lambda e: self._on_text_changed())
        self._debounce_id = None  # 防抖定时器 ID

        # ---- 颜色工具栏 ----
        toolbar = ctk.CTkFrame(inner, fg_color="transparent")
        toolbar.grid(row=2, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkLabel(
            toolbar,
            text="快速插入：",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
        ).pack(side="left")

        # 颜色选择按钮（点击弹出预设色板）
        self.color_display = ctk.CTkButton(
            toolbar,
            text="",
            width=30,
            height=30,
            corner_radius=6,
            fg_color=self._current_color,
            hover_color=self._current_color,
            command=self._show_color_palette,
        )
        self.color_display.pack(side="left", padx=(5, 3))

        ctk.CTkButton(
            toolbar,
            text="插入标签",
            width=80,
            height=30,
            corner_radius=6,
            fg_color="#0f3460",
            hover_color="#16213e",
            font=ctk.CTkFont(size=12),
            command=self._insert_color_tag,
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            toolbar,
            text="清空",
            width=60,
            height=30,
            corner_radius=6,
            fg_color="#2a2a4a",
            hover_color="#3a3a5a",
            font=ctk.CTkFont(size=12),
            command=self._clear_text,
        ).pack(side="left", padx=3)

        # ---- 示例文本 ----
        example_frame = ctk.CTkFrame(inner, fg_color="transparent")
        example_frame.grid(row=3, column=0, sticky="ew")

        ctk.CTkLabel(
            example_frame,
            text="示例文本：",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
        ).pack(side="left")

        for name in EXAMPLES:
            ctk.CTkButton(
                example_frame,
                text=name,
                width=70,
                height=26,
                corner_radius=6,
                fg_color="#2a2a4a",
                hover_color="#3a3a5a",
                font=ctk.CTkFont(size=11),
                command=lambda n=name: self._load_example(n),
            ).pack(side="left", padx=2)

    # ----------------------------------------------------------------
    #  右侧预览面板
    # ----------------------------------------------------------------
    def _build_preview_panel(self, parent):
        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=15, pady=12)
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_rowconfigure(1, weight=1)

        # 标题行
        title_row = ctk.CTkFrame(inner, fg_color="transparent")
        title_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkLabel(
            title_row,
            text="👁️ 游戏邮件预览",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#ffffff",
        ).pack(side="left")

        # ---- 游戏邮件风格预览框 ----
        mail_container = ctk.CTkFrame(
            inner, fg_color="#2e2218", corner_radius=10,
            border_width=2, border_color="#5a4530",
        )
        mail_container.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        mail_container.grid_columnconfigure(0, weight=1)
        mail_container.grid_rowconfigure(2, weight=1)

        # 邮件标题栏
        mail_header = ctk.CTkFrame(mail_container, fg_color="#3c2d1e", corner_radius=0)
        mail_header.grid(row=0, column=0, sticky="ew")

        self.mail_title_label = ctk.CTkLabel(
            mail_header,
            text="邮件预览",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#e8c84a",
        )
        self.mail_title_label.pack(pady=10)

        # 过期时间
        self.mail_expire_label = ctk.CTkLabel(
            mail_container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#e8a030",
            anchor="e",
        )
        self.mail_expire_label.grid(row=1, column=0, sticky="e", padx=15, pady=(4, 0))

        # 邮件正文（使用 tk.Text 以支持多颜色标签）
        text_frame = ctk.CTkFrame(mail_container, fg_color="transparent")
        text_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=(4, 12))
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)

        self.preview_text = tk.Text(
            text_frame,
            bg="#261c12",
            fg="#d4d0c8",
            font=("Microsoft YaHei UI", 12),
            wrap="word",
            relief="flat",
            padx=10,
            pady=8,
            insertbackground="#d4d0c8",
            selectbackground="#5a4530",
            borderwidth=0,
            highlightthickness=0,
            state="disabled",
        )
        self.preview_text.grid(row=0, column=0, sticky="nsew")

        # 滚动条
        scrollbar = ctk.CTkScrollbar(text_frame, command=self.preview_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.preview_text.configure(yscrollcommand=scrollbar.set)

        # 初始占位文字
        self.preview_text.configure(state="normal")
        self.preview_text.insert("1.0", "输入文本后，此处将以游戏邮件风格显示带颜色的预览效果...")
        self.preview_text.configure(state="disabled")

        # ---- 已解析颜色列表 ----
        color_section = ctk.CTkFrame(inner, fg_color="#0f0f1a", corner_radius=8)
        color_section.grid(row=2, column=0, sticky="ew", pady=(0, 8))

        color_header = ctk.CTkFrame(color_section, fg_color="transparent")
        color_header.pack(fill="x", padx=12, pady=(8, 4))

        ctk.CTkLabel(
            color_header,
            text="🎨 已解析的颜色",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors["text"],
        ).pack(side="left")

        self.color_list_frame = ctk.CTkFrame(color_section, fg_color="transparent")
        self.color_list_frame.pack(fill="x", padx=12, pady=(0, 8))

        self.no_color_label = ctk.CTkLabel(
            self.color_list_frame,
            text="尚未检测到颜色代码",
            font=ctk.CTkFont(size=11),
            text_color="#666666",
        )
        self.no_color_label.pack(anchor="w")

        # ---- 统计信息 ----
        stats_frame = ctk.CTkFrame(inner, fg_color="transparent")
        stats_frame.grid(row=3, column=0, sticky="ew")
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.stat_colors = self._create_stat_card(stats_frame, "颜色数量", "0", "#0f3460", 0)
        self.stat_tags = self._create_stat_card(stats_frame, "标签数量", "0", "#1a5c3a", 1)
        self.stat_chars = self._create_stat_card(stats_frame, "字符数", "0", "#4a2060", 2)

    def _create_stat_card(self, parent, label, value, bg_color, col):
        """创建统计卡片，返回值 Label"""
        card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=8)
        card.grid(row=0, column=col, sticky="ew", padx=3)

        val_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff",
        )
        val_label.pack(pady=(8, 0))

        ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=10),
            text_color="#aaaaaa",
        ).pack(pady=(0, 8))

        return val_label

    # ================================================================
    #  事件处理
    # ================================================================
    def _on_text_changed(self):
        """文本变化时触发（带 80ms 防抖）"""
        if self._debounce_id is not None:
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(80, self._do_parse)

    def _do_parse(self):
        """实际执行解析和预览（由防抖定时器调用）"""
        self._debounce_id = None
        text = self.text_input.get("1.0", "end").rstrip("\n")

        # 更新字符计数
        char_len = len(text)
        self.char_count_label.configure(text=f"字数: {char_len}")

        if not text.strip():
            self._reset_preview()
            return

        # 解析
        segments, unique_colors, tag_count, errors = parse_color_tags(text)

        # 更新邮件标题
        title = self._extract_title(text)
        self.mail_title_label.configure(text=title)

        # 更新过期时间
        expire = self._extract_expire(text)
        self.mail_expire_label.configure(text=expire)

        # 更新预览
        self._render_preview(segments)

        # 更新颜色列表
        self._render_color_list(unique_colors)

        # 更新统计
        self.stat_colors.configure(text=str(len(unique_colors)))
        self.stat_tags.configure(text=str(tag_count))
        self.stat_chars.configure(text=str(char_len))

    def _reset_preview(self):
        """重置预览区域"""
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", "输入文本后，此处将以游戏邮件风格显示带颜色的预览效果...")
        self.preview_text.configure(state="disabled")
        self.mail_title_label.configure(text="邮件预览")
        self.mail_expire_label.configure(text="")
        self.stat_colors.configure(text="0")
        self.stat_tags.configure(text="0")
        self.stat_chars.configure(text="0")
        self._render_color_list([])

    def _render_preview(self, segments):
        """在预览区域渲染带颜色的文本"""
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")

        # 清除旧的颜色标签
        for tag in self.preview_text.tag_names():
            if tag.startswith("color_"):
                self.preview_text.tag_delete(tag)

        tag_counter = 0
        for text, color in segments:
            if color:
                tag_name = f"color_{tag_counter}"
                tag_counter += 1
                self.preview_text.tag_configure(tag_name, foreground=color)
                self.preview_text.insert("end", text, tag_name)
            else:
                self.preview_text.insert("end", text)

        self.preview_text.configure(state="disabled")

    def _render_color_list(self, colors):
        """渲染已解析的颜色列表"""
        for widget in self.color_list_frame.winfo_children():
            widget.destroy()

        if not colors:
            self.no_color_label = ctk.CTkLabel(
                self.color_list_frame,
                text="尚未检测到颜色代码",
                font=ctk.CTkFont(size=11),
                text_color="#666666",
            )
            self.no_color_label.pack(anchor="w")
            return

        for color in colors:
            item = ctk.CTkFrame(self.color_list_frame, fg_color="transparent")
            item.pack(side="left", padx=(0, 8), pady=2)

            # 颜色方块
            ctk.CTkButton(
                item,
                text="",
                width=18,
                height=18,
                corner_radius=9,
                fg_color=color,
                hover_color=color,
                border_width=1,
                border_color="#555555",
                command=lambda c=color: self._copy_to_clipboard(c),
            ).pack(side="left", padx=(0, 4))

            ctk.CTkLabel(
                item,
                text=color,
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=self.colors["text_dim"],
            ).pack(side="left")

    def _extract_title(self, text: str) -> str:
        """从文本中提取标题"""
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            m = re.search(r'<color=[^>]+>([^<]+)</color>', line)
            if m:
                return m.group(1).strip()
            plain = re.sub(r'</?color[^>]*>', '', line)
            if 0 < len(plain) <= 40:
                return plain
            break
        return "邮件预览"

    def _extract_expire(self, text: str) -> str:
        """从文本中提取过期时间"""
        m = re.search(r'(\d+时后过期|\d+天后过期|\d+小时后过期|永久有效)', text)
        return m.group(1) if m else ""

    def _show_color_palette(self):
        """弹出预设色板菜单（22个游戏色表 + 自定义选项）"""
        menu = tk.Menu(self, tearoff=0, bg="#2a2a3a", fg="#dddddd",
                       activebackground="#3a3a5a", activeforeground="#ffffff",
                       borderwidth=1, relief="flat")

        # 按每行最多11个色块分组展示
        cols = 11
        for i in range(0, len(PRESET_COLORS), cols):
            row_colors = PRESET_COLORS[i:i + cols]
            for c in row_colors:
                # 用小图标模拟色块：创建一个带背景色的 Label 作为 image
                # 由于 Menu 不支持自定义 widget，改用带色块前缀的文本
                hex_short = c.lstrip("#").upper()
                menu.add_command(
                    label=f"  {hex_short}  ",
                    command=lambda color=c: self._select_preset_color(color),
                    background=c,
                    foreground=self._get_contrast_text(c),
                    activebackground=c,
                    activeforeground=self._get_contrast_text(c),
                    font=("Consolas", 10, "bold"),
                    columnbreak=False,
                )

        menu.add_separator()
        menu.add_command(label="🎨 自定义颜色...", command=self._pick_color)

        # 在按钮位置弹出
        try:
            menu.tk_popup(
                self.winfo_pointerx(),
                self.winfo_pointery(),
            )
        finally:
            menu.grab_release()

    @staticmethod
    def _get_contrast_text(hex_color: str) -> str:
        """根据背景亮度返回对比文字颜色"""
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "#000000" if luminance > 0.55 else "#ffffff"

    def _pick_color(self):
        """打开颜色选择器"""
        result = colorchooser.askcolor(
            initialcolor=self._current_color,
            title="选择颜色",
        )
        if result and result[1]:
            self._current_color = result[1]
            self.color_display.configure(
                fg_color=self._current_color,
                hover_color=self._current_color,
            )

    def _select_preset_color(self, color: str):
        """选择预设颜色"""
        self._current_color = color
        self.color_display.configure(
            fg_color=color,
            hover_color=color,
        )

    def _insert_color_tag(self):
        """在输入框中插入颜色标签"""
        try:
            sel_start = self.text_input.index("sel.first")
            sel_end = self.text_input.index("sel.last")
            selected = self.text_input.get(sel_start, sel_end)
            self.text_input.delete(sel_start, sel_end)
            tag = f"<color={self._current_color}>{selected}</color>"
            self.text_input.insert(sel_start, tag)
        except tk.TclError:
            # 没有选中文本
            tag = f"<color={self._current_color}>带颜色的文字</color>"
            self.text_input.insert("insert", tag)

        self._on_text_changed()

    def _clear_text(self):
        """清空输入框"""
        self.text_input.delete("1.0", "end")
        self._on_text_changed()

    def _load_example(self, name: str):
        """加载示例文本"""
        if name in EXAMPLES:
            self.text_input.delete("1.0", "end")
            self.text_input.insert("1.0", EXAMPLES[name])
            self._on_text_changed()

    def _copy_to_clipboard(self, text: str):
        """复制文本到剪贴板"""
        self.clipboard_clear()
        self.clipboard_append(text)
        # 简单的视觉反馈：临时改变标题
        original = self.mail_title_label.cget("text")
        self.mail_title_label.configure(text=f"✅ 已复制: {text}")
        self.after(1500, lambda: self.mail_title_label.configure(text=original))
