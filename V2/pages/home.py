"""
首页模块
展示欢迎信息、工具概览和快捷入口
"""

import customtkinter as ctk
from datetime import datetime
import threading

from updater import get_local_version, check_update, do_update, VersionInfo, restart_app


class HomePage(ctk.CTkFrame):
    """首页界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self._build_ui()

    def _build_ui(self):
        """构建首页界面"""
        # 滚动容器
        scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # ---- 欢迎横幅 ----
        banner = ctk.CTkFrame(scroll, fg_color="#0f3460", corner_radius=16)
        banner.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        banner_inner = ctk.CTkFrame(banner, fg_color="transparent")
        banner_inner.pack(fill="x", padx=30, pady=25)

        greeting = self._get_greeting()
        ctk.CTkLabel(
            banner_inner,
            text=f"{greeting}，欢迎使用游戏运营工具合集 👋",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            banner_inner,
            text="这里集成了日常运营所需的各类实用工具，助你高效完成工作。",
            font=ctk.CTkFont(size=13),
            text_color="#b0c4de",
            anchor="w",
        ).pack(fill="x", pady=(8, 0))

        # ---- 系统信息区 ----
        ctk.CTkLabel(
            scroll,
            text="ℹ️ 系统信息",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text"],
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(10, 10))

        info_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_frame.grid(row=2, column=0, sticky="ew")

        # 基础信息
        self._version_label = ctk.CTkLabel(
            info_frame,
            text=f"v{get_local_version()}",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text"],
            anchor="w",
        )

        info_items = [
            ("应用版本", self._version_label),
            ("框架", "CustomTkinter"),
            ("主题", "深色模式"),
            ("当前时间", datetime.now().strftime("%Y-%m-%d %H:%M")),
        ]

        for i, (key, value) in enumerate(info_items):
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(
                row_frame,
                text=key,
                font=ctk.CTkFont(size=13),
                text_color=self.colors["text_dim"],
                width=120,
                anchor="w",
            ).pack(side="left")

            if isinstance(value, str):
                ctk.CTkLabel(
                    row_frame,
                    text=value,
                    font=ctk.CTkFont(size=13),
                    text_color=self.colors["text"],
                    anchor="w",
                ).pack(side="left")
            else:
                value.pack(side="left")

        # 分隔线
        sep = ctk.CTkFrame(info_frame, height=1, fg_color="#333355")
        sep.pack(fill="x", padx=20, pady=(8, 12))

        # 在线更新区域
        update_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        update_row.pack(fill="x", padx=20, pady=(0, 18))

        ctk.CTkLabel(
            update_row,
            text="在线更新",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_dim"],
            width=120,
            anchor="w",
        ).pack(side="left")

        btn_frame = ctk.CTkFrame(update_row, fg_color="transparent")
        btn_frame.pack(side="left", fill="x", expand=True)

        self._check_btn = ctk.CTkButton(
            btn_frame,
            text="检查更新",
            width=100,
            height=28,
            command=self._on_check_update,
        )
        self._check_btn.pack(side="left", padx=(0, 8))

        self._update_btn = ctk.CTkButton(
            btn_frame,
            text="立即更新",
            width=100,
            height=28,
            fg_color="#e94560",
            hover_color="#ff6b6b",
            command=self._on_do_update,
            state="disabled",
        )
        self._update_btn.pack(side="left")

        # 更新状态标签（初始隐藏）
        self._update_status = ctk.CTkLabel(
            info_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#4ade80",
            anchor="w",
        )
        self._update_status.pack(fill="x", padx=20, pady=(0, 14))

        # 存储远程版本信息，供更新按钮使用
        self._remote_version: VersionInfo = None

    @staticmethod
    def _get_greeting() -> str:
        """根据当前时间返回问候语"""
        hour = datetime.now().hour
        if hour < 6:
            return "夜深了"
        elif hour < 12:
            return "上午好"
        elif hour < 14:
            return "中午好"
        elif hour < 18:
            return "下午好"
        else:
            return "晚上好"

    # ---- 在线更新功能 ----

    def _on_check_update(self):
        """点击'检查更新'按钮的回调"""
        self._check_btn.configure(state="disabled", text="检查中...")
        self._update_status.configure(text="正在连接服务器...", text_color="#fbbf24")

        threading.Thread(target=self._check_update_thread, daemon=True).start()

    def _check_update_thread(self):
        """后台线程执行版本检测"""
        try:
            remote = check_update()
            if remote is None:
                # 检查是否是网络错误还是确实无更新
                from updater import fetch_remote_version
                raw = fetch_remote_version()
                if raw is None:
                    self.after(0, lambda: self._show_status("无法连接更新服务器，请检查网络", "#ef4444"))
                else:
                    self.after(0, lambda: self._show_status(f"当前已是最新版本 v{get_local_version()}", "#4ade80"))
                self.after(0, lambda: self._update_btn.configure(state="disabled"))
            else:
                changelog_str = "\n".join([f"  · {item}" for item in remote.changelog])
                msg = f"发现新版本 v{remote.version}（{remote.release_date}）\n{changelog_str}"
                self.after(0, lambda m=msg: self._show_status(m, "#4ade80"))
                self.after(0, lambda: self._update_btn.configure(state="normal"))
                self._remote_version = remote
        except Exception as e:
            self.after(0, lambda e=e: self._show_status(f"检查失败: {e}", "#ef4444"))
            self.after(0, lambda: self._update_btn.configure(state="disabled"))
        finally:
            self.after(0, lambda: self._check_btn.configure(state="normal", text="检查更新"))

    def _on_do_update(self):
        """点击'立即更新'按钮的回调"""
        self._update_btn.configure(state="disabled", text="更新中...")
        self._check_btn.configure(state="disabled")
        self._show_status("正在下载并安装更新，请勿关闭程序...", "#fbbf24")

        threading.Thread(target=self._do_update_thread, daemon=True).start()

    def _do_update_thread(self):
        """后台线程执行完整更新流程"""
        def on_progress(msg, current=0, total=0):
            self.after(0, lambda m=msg: self._show_status(m, "#fbbf24"))

        def on_error(err_msg):
            self.after(0, lambda m=err_msg: self._show_status(m, "#ef4444"))
            self.after(0, lambda: self._update_btn.configure(
                state="normal" if self._remote_version else "disabled",
                text="立即更新",
            ))
            self.after(0, lambda: self._check_btn.configure(state="normal"))

        success = do_update(on_progress=on_progress, on_error=on_error)
        if success:
            self.after(0, lambda: self._show_status("更新完成，即将重启应用...", "#4ade80"))
            # 延迟1秒后重启
            self.after(1000, restart_app)
        # do_update 失败时由 on_error 回调恢复状态

    def _show_status(self, text: str, color: str):
        """显示更新状态文本"""
        self._update_status.configure(text=text, text_color=color)
