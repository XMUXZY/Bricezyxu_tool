"""
游戏运营小工具合集 - 主程序
基于 CustomTkinter 的模块化桌面应用框架
"""

import customtkinter as ctk
from typing import Dict, Type, Optional
import threading
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

        # ---- 构建界面 ----
        self._build_layout()
        self._build_nav()

        # 默认显示首页（懒加载：仅创建当前需要的页面）
        if NAV_ITEMS:
            self._switch_page(NAV_ITEMS[0][0])

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
        """构建左侧导航栏"""
        # ---- Logo / 标题区域 ----
        logo_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        logo_frame.pack(fill="x", padx=15, pady=(25, 5))

        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🎮",
            font=ctk.CTkFont(size=36),
        )
        logo_label.pack()

        title_label = ctk.CTkLabel(
            logo_frame,
            text="运营工具合集",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors["text"],
        )
        title_label.pack(pady=(5, 0))

        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="Game Ops Toolkit",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_dim"],
        )
        subtitle_label.pack()

        # ---- 分隔线 ----
        separator = ctk.CTkFrame(
            self.nav_frame, height=1, fg_color="#2a2a4a"
        )
        separator.pack(fill="x", padx=20, pady=(20, 15))

        # ---- 导航按钮 ----
        # 将"设置"放在底部，其余放在顶部
        top_items = NAV_ITEMS[:-1]  # 除最后一项外
        bottom_items = NAV_ITEMS[-1:]  # 最后一项（设置）

        for name, icon, _ in top_items:
            btn = self._create_nav_button(name, icon)
            btn.pack(fill="x", padx=12, pady=3)

        # 弹性空间，将"设置"推到底部
        spacer = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        # 底部分隔线
        separator_bottom = ctk.CTkFrame(
            self.nav_frame, height=1, fg_color="#2a2a4a"
        )
        separator_bottom.pack(fill="x", padx=20, pady=(5, 10))

        for name, icon, _ in bottom_items:
            btn = self._create_nav_button(name, icon)
            btn.pack(fill="x", padx=12, pady=3)

        # ---- 版本信息 ----
        version_label = ctk.CTkLabel(
            self.nav_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_dim"],
        )
        version_label.pack(pady=(5, 15))

    def _create_nav_button(self, name: str, icon: str) -> ctk.CTkButton:
        """创建单个导航按钮"""
        btn = ctk.CTkButton(
            self.nav_frame,
            text=f"  {icon}  {name}",
            font=ctk.CTkFont(size=14),
            height=42,
            anchor="w",
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.colors["nav_hover"],
            text_color=self.colors["text"],
            command=lambda n=name: self._switch_page(n),
        )
        self.nav_buttons[name] = btn
        return btn

    def _get_or_create_page(self, page_name: str, page_class: Type[ctk.CTkFrame]) -> ctk.CTkFrame:
        """获取已缓存的页面实例，不存在则创建"""
        if page_name not in self.pages:
            page = page_class(self.content_frame, self.colors)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[page_name] = page
            # 触发布局计算，避免首次显示时闪烁
            self.update_idletasks()
        return self.pages[page_name]

    def _switch_page(self, page_name: str):
        """切换到指定页面（懒加载 + lift 优化）"""
        target_class = _NAV_CLASS_MAP.get(page_name)
        if target_class is None:
            return

        # 懒加载：首次切换时才创建页面
        target_page = self._get_or_create_page(page_name, target_class)

        # 使用 lift() 将目标页面提升到最前，避免 destroy/recreate
        target_page.lift()
        self.current_page = target_page

        # 更新导航按钮样式
        self._update_nav_style(page_name)

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
