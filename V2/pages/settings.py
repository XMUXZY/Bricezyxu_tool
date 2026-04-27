"""
设置模块
提供应用配置选项，如主题切换、关于信息、在线更新等
"""

import customtkinter as ctk
import threading
from updater import (
    get_local_version, check_update, do_update, restart_app,
    VersionInfo, compare_versions, is_frozen
)


class SettingsPage(ctk.CTkFrame):
    """设置界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self.remote_version = None  # 远程版本缓存
        self._build_ui()

    def _build_ui(self):
        """构建设置界面"""
        scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # ---- 页面标题 ----
        ctk.CTkLabel(
            scroll,
            text="⚡ 设置",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 20))

        # ---- 外观设置 ----
        self._create_section(scroll, "🎨 外观设置", row=1)

        appearance_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        appearance_card.grid(row=2, column=0, sticky="ew", pady=(0, 20))

        appearance_inner = ctk.CTkFrame(appearance_card, fg_color="transparent")
        appearance_inner.pack(fill="x", padx=20, pady=15)

        # 主题模式
        theme_row = ctk.CTkFrame(appearance_inner, fg_color="transparent")
        theme_row.pack(fill="x", pady=5)

        ctk.CTkLabel(
            theme_row,
            text="主题模式",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text"],
            width=120,
            anchor="w",
        ).pack(side="left")

        self.theme_var = ctk.StringVar(value="深色")
        theme_menu = ctk.CTkOptionMenu(
            theme_row,
            values=["深色", "浅色", "跟随系统"],
            variable=self.theme_var,
            width=160,
            height=32,
            corner_radius=8,
            fg_color="#0f3460",
            button_color="#0f3460",
            button_hover_color="#16213e",
            command=self._on_theme_change,
        )
        theme_menu.pack(side="right")

        # 缩放比例
        scale_row = ctk.CTkFrame(appearance_inner, fg_color="transparent")
        scale_row.pack(fill="x", pady=10)

        ctk.CTkLabel(
            scale_row,
            text="界面缩放",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text"],
            width=120,
            anchor="w",
        ).pack(side="left")

        self.scale_var = ctk.StringVar(value="100%")
        scale_menu = ctk.CTkOptionMenu(
            scale_row,
            values=["80%", "90%", "100%", "110%", "120%"],
            variable=self.scale_var,
            width=160,
            height=32,
            corner_radius=8,
            fg_color="#0f3460",
            button_color="#0f3460",
            button_hover_color="#16213e",
            command=self._on_scale_change,
        )
        scale_menu.pack(side="right")

        # ---- 通用设置 ----
        self._create_section(scroll, "🔔 通用设置", row=3)

        general_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        general_card.grid(row=4, column=0, sticky="ew", pady=(0, 20))

        general_inner = ctk.CTkFrame(general_card, fg_color="transparent")
        general_inner.pack(fill="x", padx=20, pady=15)

        # 启动时检查更新
        update_row = ctk.CTkFrame(general_inner, fg_color="transparent")
        update_row.pack(fill="x", pady=5)

        ctk.CTkLabel(
            update_row,
            text="启动时检查更新",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text"],
            anchor="w",
        ).pack(side="left")

        self.update_switch = ctk.CTkSwitch(
            update_row,
            text="",
            onvalue=True,
            offvalue=False,
            width=46,
        )
        self.update_switch.pack(side="right")
        self.update_switch.select()

        # 记住窗口位置
        position_row = ctk.CTkFrame(general_inner, fg_color="transparent")
        position_row.pack(fill="x", pady=10)

        ctk.CTkLabel(
            position_row,
            text="记住窗口位置",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text"],
            anchor="w",
        ).pack(side="left")

        self.position_switch = ctk.CTkSwitch(
            position_row,
            text="",
            onvalue=True,
            offvalue=False,
            width=46,
        )
        self.position_switch.pack(side="right")

        # ---- 在线更新 ----
        self._create_section(scroll, "🔄 在线更新", row=5)

        update_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        update_card.grid(row=6, column=0, sticky="ew", pady=(0, 20))

        update_inner = ctk.CTkFrame(update_card, fg_color="transparent")
        update_inner.pack(fill="x", padx=20, pady=15)

        # 当前版本 + 检查按钮行
        version_row = ctk.CTkFrame(update_inner, fg_color="transparent")
        version_row.pack(fill="x", pady=5)

        ctk.CTkLabel(
            version_row,
            text=f"当前版本：v{get_local_version()}",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text"],
            anchor="w",
        ).pack(side="left")

        self.check_btn = ctk.CTkButton(
            version_row,
            text="检查更新",
            width=100,
            height=30,
            corner_radius=8,
            fg_color="#0f3460",
            hover_color="#16213e",
            command=self._on_check_update,
        )
        self.check_btn.pack(side="right")

        # 更新状态标签（动态显示结果）
        self.update_status_label = ctk.CTkLabel(
            update_inner,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_dim"],
            anchor="w",
            justify="left",
        )
        self.update_status_label.pack(fill="x", pady=(5, 0))
        self.update_status_label.grid_forget()  # 默认隐藏

        # 更新日志显示区（有新版本时显示）
        self.changelog_textbox = None

        # ---- 关于 ----
        self._create_section(scroll, "💡 关于", row=7)

        about_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        about_card.grid(row=8, column=0, sticky="ew", pady=(0, 20))

        about_inner = ctk.CTkFrame(about_card, fg_color="transparent")
        about_inner.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            about_inner,
            text="🎮 游戏运营工具合集",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff",
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            about_inner,
            text=f"版本 {get_local_version()}",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_dim"],
        ).pack()

        ctk.CTkLabel(
            about_inner,
            text="基于 CustomTkinter 构建的模块化桌面工具集\n可随时扩展新的运营工具模块",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
            justify="center",
        ).pack(pady=(10, 0))

    def _on_check_update(self):
        """检查更新按钮回调"""
        self.check_btn.configure(state="disabled", text="检查中...")
        self.update_status_label.configure(text="正在连接服务器...", text_color="#e94560")
        self.update_status_label.pack(fill="x", pady=(5, 0))
        threading.Thread(target=self._do_check_update, daemon=True).start()

    def _do_check_update(self):
        """后台线程执行版本检查"""
        try:
            remote = check_update()
        except Exception:
            remote = None
        self.after(0, lambda: self._on_check_result(remote))

    def _on_check_result(self, remote):
        """主线程处理检查结果"""
        self.remote_version = remote
        self.check_btn.configure(state="normal", text="检查更新")

        if remote is None:
            self.update_status_label.configure(
                text="✅ 已是最新版本",
                text_color="#4ecca3"
            )
            return

        # 发现新版本
        status_text = f"🔔 发现新版本 v{remote.version}"
        if remote.force_update:
            status_text += "（强制更新）"
        self.update_status_label.configure(text=status_text, text_color="#f0a500")
        self._show_update_dialog(remote)

    def _show_update_dialog(self, remote: VersionInfo):
        """弹出更新确认对话框（内嵌在设置页中）"""
        # 创建一个顶层弹窗
        dialog = ctk.CTkToplevel(self)
        dialog.title("发现新版本")
        dialog.geometry("480x420")
        dialog.resizable(False, False)
        dialog.grab_set()  # 模态

        # 居中显示
        dialog.transient(self.winfo_toplevel())
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 480) // 2
        y = (dialog.winfo_screenheight() - 420) // 2
        dialog.geometry(f"+{x}+{y}")

        # 内容
        main_frame = ctk.CTkFrame(dialog, fg_color="#0f0f1a", corner_radius=0)
        main_frame.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 5))

        ctk.CTkLabel(
            header_frame,
            text=f"🔄 新版本 v{remote.version} 可用",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff",
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text=f"当前版本：v{get_local_version()}  |  发布日期：{remote.release_date}",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_dim"],
        ).pack(anchor="w", pady=(3, 0))

        # 更新日志
        log_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a2e", corner_radius=10)
        log_frame.pack(fill="both", expand=True, padx=25, pady=15)

        ctk.CTkLabel(
            log_frame,
            text="📋 更新内容",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors["text"],
            anchor="w",
        ).pack(anchor="w", padx=15, pady=(12, 8))

        changelog_text = "\n".join(f"  • {line}" for line in remote.changelog)
        ctk.CTkLabel(
            log_frame,
            text=changelog_text if changelog_text else "  （暂无详细日志）",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
            justify="left",
            anchor="nw",
        ).pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # 进度条（默认隐藏）
        progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        progress_frame.pack(fill="x", padx=25)

        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=430)
        self.progress_bar.set(0)
        # 默认隐藏进度条

        self.progress_label = ctk.CTkLabel(
            progress_frame, text="", font=ctk.CTkFont(size=11),
            text_color=self.colors["text_dim"]
        )
        # 默认隐藏

        # 按钮区
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=(5, 20))

        def on_update():
            """点击立即更新按钮"""
            # 隐藏按钮，显示进度
            for w in btn_frame.winfo_children():
                w.pack_forget()
            self.progress_bar.pack(pady=(0, 3))
            self.progress_label.pack()
            self.progress_bar.set(0.1)
            self.progress_label.configure(text="正在准备下载...")

            # 在后台执行下载
            self._do_download(dialog, remote)

        def on_skip():
            dialog.destroy()

        # 跳过按钮
        if not remote.force_update:
            ctk.CTkButton(
                btn_frame, text="跳过此版本", width=130, height=34,
                corner_radius=8, fg_color="#333344", hover_color="#444455",
                text_color=self.colors["text_dim"],
                command=on_skip,
            ).pack(side="right", padx=(10, 0))

        # 立即更新按钮
        ctk.CTkButton(
            btn_frame, text="⬇️ 立即更新", width=150, height=34,
            corner_radius=8, fg_color="#e94560", hover_color="#c73e54",
            text_color="#ffffff", font=ctk.CTkFont(size=13, weight="bold"),
            command=on_update,
        ).pack(side="right")

    def _do_download(self, dialog, remote: VersionInfo):
        """执行下载和安装流程"""

        def on_progress(msg: str, current: int = 0, total: int = 0):
            def ui_update():
                self.progress_label.configure(text=msg)
                if total > 0:
                    self.progress_bar.set(current / total)
                else:
                    self.progress_bar.set(0)  # 不确定模式
            self.after(0, ui_update)

        def on_error(msg: str):
            def ui_show_err():
                self.progress_label.configure(text=msg, text_color="#e94560")
            self.after(0, ui_show_err)

        def run_update():
            success = do_update(on_progress=on_progress, on_error=on_error)
            if success:
                def ui_complete():
                    self.progress_bar.set(1.0)
                    if is_frozen():
                        # EXE 模式：bat 脚本已启动，直接退出当前程序即可
                        self.progress_label.configure(
                            text="✅ 更新完成！程序即将关闭并自动重启...",
                            text_color="#4ecca3"
                        )
                        import os
                        self.after(1500, lambda: os._exit(0))
                    else:
                        # 源码模式：手动重启
                        self.progress_label.configure(
                            text="✅ 更新完成！即将重启...",
                            text_color="#4ecca3"
                        )
                        self.after(1200, lambda: (dialog.destroy(), restart_app()))
                self.after(0, ui_complete)
            else:
                # 失败时显示重试按钮
                def ui_fail():
                    self.progress_label.configure(text="❌ 更新失败，请重试", text_color="#e94560")
                    retry_btn = ctk.CTkButton(
                        dialog, text="🔙 返回", width=100, height=32,
                        command=dialog.destroy
                    )
                    retry_btn.place(relx=0.5, rely=0.92, anchor="center")
                self.after(0, ui_fail)

        t = threading.Thread(target=run_update, daemon=True)
        t.start()

    def _create_section(self, parent, title: str, row: int):
        """创建设置分区标题"""
        ctk.CTkLabel(
            parent,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors["text"],
            anchor="w",
        ).grid(row=row, column=0, sticky="w", pady=(5, 8))

    def _on_theme_change(self, value: str):
        """主题切换回调"""
        theme_map = {
            "深色": "dark",
            "浅色": "light",
            "跟随系统": "system",
        }
        ctk.set_appearance_mode(theme_map.get(value, "dark"))

    def _on_scale_change(self, value: str):
        """缩放比例切换回调"""
        scale_map = {
            "80%": 0.8,
            "90%": 0.9,
            "100%": 1.0,
            "110%": 1.1,
            "120%": 1.2,
        }
        scale = scale_map.get(value, 1.0)
        ctk.set_widget_scaling(scale)
