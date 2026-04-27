"""
新工具页面模板（双 Tab 计算器版）
复制此文件并修改即可快速创建新工具页面

演示了增强版 BaseToolPage 的全部骨架方法：
  _create_scroll_container / _create_title / _create_tab_switcher
  _create_tab_frame / _create_tab_inner / _create_result_box
  _create_calc_button / _create_info_section
  _create_section_title / _create_input_label / _create_input_entry
  _create_input_option

比起直接写 CTkLabel/CTkEntry/CTkFrame，可减少约 80% 的 UI 样板代码。
"""

import customtkinter as ctk
from pages.base_tool import BaseToolPage


class ToolTemplatePage(BaseToolPage):
    """工具页面模板（继承自 BaseToolPage）"""

    def __init__(self, parent, colors: dict = None):
        super().__init__(parent, colors)
        self._build_ui()

    # ================================================================
    #  界面构建
    # ================================================================
    def _build_ui(self):
        # 1. 主滚动容器
        scroll = self._create_scroll_container()

        # 2. 页面标题 + 副标题（row 0-1）
        self._create_title(scroll, "🔧 新工具页面标题", "工具描述和简要说明")

        # 3. Tab 切换器（row 2）
        self.tab_seg = self._create_tab_switcher(
            scroll,
            tab_labels=["📊 根据材料计算等级", "🎯 根据目标计算材料"],
        )

        # 4. Tab 1 内容区（row 3）
        self.tab1 = self._create_tab_frame(scroll, row=3, visible=True)
        self._build_tab1()

        # 5. Tab 2 内容区（row 3，初始隐藏）
        self.tab2 = self._create_tab_frame(scroll, row=3, visible=False)
        self._build_tab2()

        # 6. 底部说明卡片（row 4）
        self._create_info_section(scroll, "使用说明", [
            "• 说明条目1：在左侧 Tab 输入持有材料，计算可达等级",
            "• 说明条目2：在右侧 Tab 输入目标等级，计算所需材料",
            "• 说明条目3：其他注意事项",
        ], row=4)

    # ---- Tab 1：根据材料计算等级 ----
    def _build_tab1(self):
        inner = self._create_tab_inner(self.tab1, columns=2)

        # 分区标题
        self._create_section_title(inner, "初始状态", row=0)

        # 输入项
        self._create_input_label(inner, "初始等级 (0-30)", row=1, column=0, padx=(0, 10))
        self.t1_init_level = self._create_input_entry(inner, row=2, column=0, padx=(0, 10))

        self._create_input_label(inner, "持有材料数量", row=1, column=1, padx=(10, 0))
        self.t1_material = self._create_input_entry(inner, row=2, column=1, padx=(10, 0))

        # 计算按钮
        self._create_calc_button(inner, command=self._calc_tab1, row=3)

        # 结果展示
        self.t1_result = self._create_result_box(inner, row=4)

    # ---- Tab 2：根据目标计算材料 ----
    def _build_tab2(self):
        inner = self._create_tab_inner(self.tab2, columns=2)

        self._create_section_title(inner, "目标设置", row=0)

        self._create_input_label(inner, "当前等级", row=1, column=0, padx=(0, 10))
        self.t2_cur = self._create_input_entry(inner, row=2, column=0, padx=(0, 10))

        self._create_input_label(inner, "目标等级", row=1, column=1, padx=(10, 0))
        self.t2_tgt = self._create_input_entry(inner, row=2, column=1, default="30", padx=(10, 0))

        self._create_calc_button(inner, command=self._calc_tab2, row=3)

        self.t2_result = self._create_result_box(inner, row=4)

    # ================================================================
    #  计算逻辑
    # ================================================================
    def _calc_tab1(self):
        try:
            level = self._parse_int(self.t1_init_level.get(), 0)
            material = self._parse_int(self.t1_material.get(), 0)
            output = f"✅ Tab1 计算完成\n\n初始等级: {level}\n持有材料: {self._fmt(material)}\n"
            self._show_result(self.t1_result, output)
        except Exception as e:
            self._show_error(self.t1_result, f"计算出错: {e}")

    def _calc_tab2(self):
        try:
            cur = self._parse_int(self.t2_cur.get(), 0)
            tgt = self._parse_int(self.t2_tgt.get(), 30)
            output = f"✅ Tab2 计算完成\n\n当前等级: {cur}\n目标等级: {tgt}\n"
            self._show_result(self.t2_result, output)
        except Exception as e:
            self._show_error(self.t2_result, f"计算出错: {e}")


# ============================================================
# 如何使用此模板创建新工具：
#
# 1. 复制此文件到 pages/ 目录，重命名为 tool_xxx.py
# 2. 将类名改为 ToolXxxPage
# 3. 修改 _build_ui() 中的标题/Tab 文本/说明内容
# 4. 修改 _build_tab1() / _build_tab2() 中的输入控件
# 5. 实现 _calc_tab1() / _calc_tab2() 中的计算逻辑
# 6. 在 main.py 中导入并添加到 NAV_ITEMS:
#    from pages.tool_xxx import ToolXxxPage
#    NAV_ITEMS.append(("工具名", "🔧", ToolXxxPage))
# 7. 运行 python main.py 查看效果
#
# 对比旧模板：
#   旧：手动创建 CTkScrollableFrame + CTkLabel + CTkSegmentedButton + ... ≈ 100 行
#   新：调用基类骨架方法 ≈ 20 行，仅关注输入控件和计算逻辑
# ============================================================
