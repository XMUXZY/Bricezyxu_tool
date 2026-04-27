"""
游戏运营小工具合集 - 主程序
基于 CustomTkinter 的模块化桌面应用框架
"""

import customtkinter as ctk
from typing import Dict, Type, Optional
import threading
import os
from updater import check_update, VersionInfo

# ============================================================
# 导入各页面模块
# 如需添加新工具，只需：
#   1. 在 pages/ 目录下创建新的页面文件（参考现有模块）
#   2. 在下方导入该模块
#   3. 在 NAV_ITEMS 列表中添加对应条目
# ============================================================
from pages.home import HomePage
from pages.tool_a import ToolAPage
from pages.tool_b import ToolBPage
from pages.tool_c import ToolCPage
from pages.tool_d import ToolDPage
from pages.tool_e import ToolEPage
from pages.tool_star_map import ToolStarMapPage
from pages.tool_feng_shui import ToolFengShuiPage
from pages.tool_gem_grind import ToolGemGrindPage
from pages.tool_zhu_ling import ToolZhuLingPage
from pages.tool_dunjia import ToolDunJia
from pages.tool_guardian import ToolGuardian
from pages.tool_zhance import ToolZhanCe
from pages.tool_fabao import ToolFaBao
from pages.table_demo import TableDemoPage
from pages.settings import SettingsPage


# 导航配置：(显示名称, 图标符号, 页面类)
# 添加新工具时，在此列表中追加一项即可
NAV_ITEMS = [
    ("首  页", "🏠", HomePage),
    ("颜色解析", "🎨", ToolAPage),
    ("淬炼计算器", "⚙️", ToolBPage),
    ("重铸计算器", "⚔️", ToolCPage),
    ("星录养成", "⭐", ToolDPage),
    ("圣石养成", "💎", ToolEPage),
    ("星图养成", "☪️", ToolStarMapPage),
    ("风水录养成", "🏔", ToolFengShuiPage),
    ("磨砺养成", "⚒️", ToolGemGrindPage),
    ("注灵养成", "⚔️", ToolZhuLingPage),
    ("遁甲养成", "🔮", ToolDunJia),
    ("守护神养成", "🛡️", ToolGuardian),
    ("占测养成", "📜", ToolZhanCe),
    ("法宝升阶", "🏺", ToolFaBao),
    ("表格演示", "📊", TableDemoPage),  # 新增：表格展示功能演示
    ("设  置", "⚡", SettingsPage),
]

# 预建名称→类的查找字典，避免每次切换时线性遍历
_NAV_CLASS_MAP: Dict[str, Type[ctk.CTkFrame]] = {name: cls for name, _, cls in NAV_ITEMS}


class App(ctk.CTk):
    """主应用窗口"""

    def __init__(self):
        super().__init__()

        # ---- 窗口基础配置 ----
        self.title("🎮 游戏运营工具合集")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # 深色主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ---- 颜色配置 ----
        self.colors = {
            "nav_bg": "#1a1a2e",        # 导航栏背景
            "nav_hover": "#16213e",     # 导航按钮悬停
            "nav_active": "#0f3460",    # 导航按钮激活
            "accent": "#e94560",        # 强调色
            "content_bg": "#0f0f1a",    # 内容区背景
            "text": "#e0e0e0",          # 主文字颜色
            "text_dim": "#888888",      # 次要文字颜色
        }

        # ---- 页面缓存（预加载） ----
        self.pages: Dict[str, ctk.CTkFrame] = {}
        self.current_page: Optional[ctk.CTkFrame] = None
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        self._loading_frame: Optional[ctk.CTkFrame] = None
        self._loading_icon: Optional[ctk.CTkLabel] = None
        self._loading_text: Optional[ctk.CTkLabel] = None
        self._closing = False  # 标记是否正在关闭
        self._preload_overlay: Optional[ctk.CTkFrame] = None  # 预加载遮罩层
        self._preload_progress_label: Optional[ctk.CTkLabel] = None  # 进度文字
        self._preload_progress_bar: Optional[ctk.CTkProgressBar] = None  # 进度条

        # ---- 注册窗口关闭事件 ----
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # ---- 构建界面 ----
        self._build_layout()
        self._build_nav()

        # 默认显示首页
        if NAV_ITEMS:
            self._switch_page(NAV_ITEMS[0][0])

        # 首页显示后，空闲时逐个预加载其他页面（消除首次点击卡顿）
        self._preload_remaining_pages()

    def _build_layout(self):
        """构建主布局：左侧导航 + 右侧内容"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 左侧导航栏容器
        self.nav_frame = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=self.colors["nav_bg"],
        )
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_propagate(False)

        # 右侧内容区容器
        self.content_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.colors["content_bg"],
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def _build_nav(self):
        """构建左侧导航栏（支持滚动）"""
        # 使用 grid 布局让导航栏分为三部分：顶部Logo、中间可滚动按钮区、底部设置+版本
        self.nav_frame.grid_rowconfigure(2, weight=1)  # 中间按钮区可伸缩
        self.nav_frame.grid_columnconfigure(0, weight=1)

        # ======== 顶部区域：Logo + 标题（固定） ========
        top_section = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        top_section.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        logo_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        logo_frame.pack(fill="x", padx=15, pady=(20, 5))

        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🎮",
            font=ctk.CTkFont(size=32),
        )
        logo_label.pack()

        title_label = ctk.CTkLabel(
            logo_frame,
            text="运营工具合集",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text"],
        )
        title_label.pack(pady=(3, 0))

        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="Game Ops Toolkit",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_dim"],
        )
        subtitle_label.pack()

        # 分隔线
        separator = ctk.CTkFrame(top_section, height=1, fg_color="#2a2a4a")
        separator.pack(fill="x", padx=20, pady=(12, 5))

        # ======== 中间区域：可滚动的导航按钮列表 ========
        # 将"设置"放在底部，其余放在可滚动区
        top_items = NAV_ITEMS[:-1]
        bottom_items = NAV_ITEMS[-1:]

        self.nav_scroll = ctk.CTkScrollableFrame(
            self.nav_frame,
            fg_color="transparent",
            scrollbar_button_color="#2a2a4a",
            scrollbar_button_hover_color="#3a3a5a",
        )
        self.nav_scroll.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        self.nav_scroll.grid_columnconfigure(0, weight=1)

        for name, icon, _ in top_items:
            btn = self._create_nav_button(name, icon, parent=self.nav_scroll)
            btn.pack(fill="x", padx=12, pady=2)

        # ======== 底部区域：分隔线 + 设置按钮 + 版本号（固定） ========
        bottom_section = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        bottom_section.grid(row=3, column=0, sticky="ew", padx=0, pady=0)

        separator_bottom = ctk.CTkFrame(
            bottom_section, height=1, fg_color="#2a2a4a"
        )
        separator_bottom.pack(fill="x", padx=20, pady=(5, 8))

        for name, icon, _ in bottom_items:
            btn = self._create_nav_button(name, icon, parent=bottom_section)
            btn.pack(fill="x", padx=12, pady=2)

        from updater import get_local_version
        version_label = ctk.CTkLabel(
            bottom_section,
            text=f"v{get_local_version()}",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_dim"],
        )
        version_label.pack(pady=(3, 10))

    def _create_nav_button(self, name: str, icon: str, parent=None) -> ctk.CTkButton:
        """创建单个导航按钮"""
        btn = ctk.CTkButton(
            parent or self.nav_frame,
            text=f"  {icon}  {name}",
            font=ctk.CTkFont(size=13),
            height=36,
            anchor="w",
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.colors["nav_hover"],
            text_color=self.colors["text"],
            command=lambda n=name: self._switch_page(n),
        )
        self.nav_buttons[name] = btn
        return btn

    def _create_loading_layer(self):
        """创建 Loading 过渡层（首次加载页面时显示）"""
        self._loading_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["content_bg"],
        )
        self._loading_frame.grid(row=0, column=0, sticky="nsew")

        inner = ctk.CTkFrame(self._loading_frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.45, anchor="center")

        self._loading_icon = ctk.CTkLabel(
            inner, text="⏳", font=ctk.CTkFont(size=36),
        )
        self._loading_icon.pack()
        self._loading_text = ctk.CTkLabel(
            inner, text="加载中…",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_dim"],
        )
        self._loading_text.pack(pady=(8, 0))

    def _show_loading(self):
        """显示 Loading 层"""
        if self._loading_frame is None:
            self._create_loading_layer()
        self._loading_frame.lift()

    def _hide_loading(self):
        """隐藏 Loading 层"""
        if self._loading_frame is not None:
            self._loading_frame.lower()

    def _get_or_create_page(self, page_name: str, page_class: Type[ctk.CTkFrame]) -> ctk.CTkFrame:
        """获取已缓存的页面实例，不存在则创建"""
        if page_name not in self.pages:
            page = page_class(self.content_frame, self.colors)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[page_name] = page
        return self.pages[page_name]

    def _switch_page(self, page_name: str):
        """切换到指定页面"""
        target_class = _NAV_CLASS_MAP.get(page_name)
        if target_class is None:
            return

        # 更新导航按钮样式（立即响应点击）
        self._update_nav_style(page_name)

        if page_name in self.pages:
            # 页面已缓存，直接切换
            self.pages[page_name].lift()
            self.current_page = self.pages[page_name]
            # 如果预加载遮罩还在，保持遮罩在最上层
            if self._preload_overlay is not None:
                self._preload_overlay.lift()
        else:
            # 首次加载：先显示 Loading，再异步创建页面
            self._show_loading()
            self.update_idletasks()
            self.after(10, lambda: self._deferred_create_page(page_name, target_class))

    def _deferred_create_page(self, page_name: str, page_class: Type[ctk.CTkFrame]):
        """延迟创建页面（让 Loading 动画先显示）"""
        target_page = self._get_or_create_page(page_name, page_class)
        target_page.lift()
        self.current_page = target_page
        self._hide_loading()

    def _preload_remaining_pages(self):
        """空闲时逐个预加载剩余页面，消除后续首次点击的卡顿"""
        # 收集尚未创建的页面
        pending = [
            (name, cls) for name, _, cls in NAV_ITEMS
            if name not in self.pages
        ]
        if not pending:
            return

        total = len(pending)

        # 创建预加载遮罩层，覆盖整个内容区
        self._preload_overlay = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["content_bg"],
        )
        self._preload_overlay.grid(row=0, column=0, sticky="nsew")
        self._preload_overlay.lift()  # 置顶遮挡一切

        # 遮罩层内容：居中的加载提示
        center = ctk.CTkFrame(self._preload_overlay, fg_color="transparent")
        center.place(relx=0.5, rely=0.45, anchor="center")

        icon_lbl = ctk.CTkLabel(
            center, text="⚡", font=ctk.CTkFont(size=40),
        )
        icon_lbl.pack()

        tip_lbl = ctk.CTkLabel(
            center, text="正在初始化工具模块…",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_dim"],
        )
        tip_lbl.pack(pady=(8, 10))

        # 进度条
        self._preload_progress_bar = ctk.CTkProgressBar(
            center, width=260, height=6,
            progress_color="#e94560",
            fg_color="#2a2a4a",
        )
        self._preload_progress_bar.set(0)
        self._preload_progress_bar.pack(pady=(0, 6))

        # 进度文字
        self._preload_progress_label = ctk.CTkLabel(
            center, text=f"0 / {total}",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_dim"],
        )
        self._preload_progress_label.pack()

        # 确保遮罩渲染出来后再开始创建页面
        self.update_idletasks()

        def _preload_next(idx=0):
            # 如果正在关闭，立即停止预加载
            if self._closing:
                return
            if idx >= len(pending):
                # 全部预加载完成，移除遮罩
                self._remove_preload_overlay()
                return
            name, cls = pending[idx]
            if name not in self.pages:
                self._get_or_create_page(name, cls)
            # 更新进度
            done = idx + 1
            if self._preload_progress_bar is not None:
                self._preload_progress_bar.set(done / total)
            if self._preload_progress_label is not None:
                self._preload_progress_label.configure(text=f"{done} / {total}")
            # 确保当前页面在遮罩下面（不会被新建的页面挡住遮罩）
            if self._preload_overlay is not None:
                self._preload_overlay.lift()
            # 让出主线程 30ms 再创建下一个
            self.after(30, lambda: _preload_next(idx + 1))

        # 首页渲染完成后 200ms 开始预加载
        self.after(200, _preload_next)

    def _remove_preload_overlay(self):
        """移除预加载遮罩层，露出当前页面"""
        if self._preload_overlay is not None:
            self._preload_overlay.destroy()
            self._preload_overlay = None
            self._preload_progress_bar = None
            self._preload_progress_label = None
        # 确保当前页面在最上层
        if self.current_page is not None:
            self.current_page.lift()

    def _on_close(self):
        """窗口关闭事件：瞬间关闭，不卡顿"""
        # 1. 标记关闭，停止所有 after 回调
        self._closing = True
        # 2. 立即隐藏窗口（视觉上瞬间消失）
        try:
            self.withdraw()
        except Exception:
            pass
        # 3. 强制退出进程，跳过 destroy() 的逐控件销毁（这是卡顿根源）
        os._exit(0)

    def _update_nav_style(self, active_name: str):
        """更新导航按钮的激活状态样式"""
        for name, btn in self.nav_buttons.items():
            if name == active_name:
                btn.configure(
                    fg_color=self.colors["nav_active"],
                    text_color="#ffffff",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=self.colors["text"],
                )

    def _startup_check_update(self):
        """启动时后台检查更新，发现新版本后弹窗提示"""
        def do_check():
            try:
                remote = check_update()
                if remote is not None:
                    self.after(0, lambda: self._show_update_notification(remote))
            except Exception:
                pass

        t = threading.Thread(target=do_check, daemon=True)
        t.start()

    def _show_update_notification(self, remote: VersionInfo):
        """显示更新通知（右下角浮动提示）"""
        # 创建一个悬浮提示窗口
        notify = ctk.CTkToplevel(self)
        notify.overrideredirect(True)  # 无边框
        notify.geometry("320x90")
        notify.attributes("-topmost", True)
        notify.lift()

        # 定位到右下角
        self.update_idletasks()
        x = self.winfo_x() + self.winfo_width() - 340
        y = self.winfo_y() + self.winfo_height() - 120
        notify.geometry(f"+{x}+{y}")

        frame = ctk.CTkFrame(notify, fg_color="#16213e", corner_radius=10,
                             border_width=1, border_color="#e94560")
        frame.pack(fill="both", expand=True, padx=2, pady=2)

        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=15, pady=12)

        ctk.CTkLabel(
            inner, text=f"🔄 发现新版本 v{remote.version}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff", anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            inner, text="点击查看详情并更新",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_dim"], anchor="w"
        ).pack(fill="x", pady=(2, 8))

        # 关闭和前往按钮
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x")

        ctk.CTkButton(
            btn_row, text="稍后", width=80, height=26,
            corner_radius=6, fg_color="#333344", hover_color="#444455",
            text_color=self.colors["text_dim"], font=ctk.CTkFont(size=11),
            command=notify.destroy
        ).pack(side="left")

        ctk.CTkButton(
            btn_row, text="去更新", width=100, height=26,
            corner_radius=6, fg_color="#e94560", hover_color="#c73e54",
            text_color="#ffffff", font=ctk.CTkFont(size=11),
            command=lambda: (notify.destroy(), self._switch_page("设  置"))
        ).pack(side="right")

        # 15秒后自动消失
        self.after(15000, lambda: (
            notify.destroy() if notify.winfo_exists() else None
        ))


if __name__ == "__main__":
    app = App()
    app.mainloop()
