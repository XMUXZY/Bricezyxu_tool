"""
表格展示功能测试页面
演示如何使用 TableResultWindow 组件
"""

import customtkinter as ctk
from tkinter import messagebox
from utils.table_result import show_table_result


class TableDemoPage(ctk.CTkFrame):
    """表格展示演示页面"""
    
    def __init__(self, parent, colors=None):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors or {}
        self._create_ui()
    
    def _create_ui(self):
        """创建UI"""
        # 标题
        title_label = ctk.CTkLabel(
            self,
            text="📊 表格展示功能演示",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.pack(pady=(30, 10))
        
        desc_label = ctk.CTkLabel(
            self,
            text="点击下方按钮查看不同类型的表格展示效果",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        )
        desc_label.pack(pady=(0, 30))
        
        # 示例按钮区域
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="both", expand=True, padx=50)
        
        # 示例1：注灵养成计算结果
        self._create_demo_card(
            btn_frame,
            "示例1：注灵养成计算",
            "模拟注灵等级计算结果展示",
            self._demo_zhuling,
            row=0,
        )
        
        # 示例2：材料需求汇总
        self._create_demo_card(
            btn_frame,
            "示例2：材料需求汇总",
            "展示各等级所需材料统计",
            self._demo_materials,
            row=1,
        )
        
        # 示例3：字典格式数据
        self._create_demo_card(
            btn_frame,
            "示例3：字典数据展示",
            "使用字典列表自动生成表格",
            self._demo_dict_data,
            row=2,
        )
        
        # 示例4：大数据量测试
        self._create_demo_card(
            btn_frame,
            "示例4：大数据量测试",
            "测试100行数据的展示性能",
            self._demo_large_data,
            row=3,
        )
    
    def _create_demo_card(self, parent, title, desc, command, row):
        """创建演示卡片"""
        card = ctk.CTkFrame(parent)
        card.grid(row=row, column=0, sticky="ew", pady=10)
        parent.grid_columnconfigure(0, weight=1)
        
        # 左侧文字
        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        
        ctk.CTkLabel(
            text_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame,
            text=desc,
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w",
        ).pack(anchor="w", pady=(5, 0))
        
        # 右侧按钮
        ctk.CTkButton(
            card,
            text="查看示例",
            command=command,
            width=120,
            height=36,
        ).pack(side="right", padx=20, pady=15)
    
    def _demo_zhuling(self):
        """示例1：注灵养成计算"""
        data = [
            ["Lv.1", "天罡石 × 100", "地煞符 × 50", "灵元宝 × 20", "✅ 已达成"],
            ["Lv.2", "天罡石 × 200", "地煞符 × 100", "灵元宝 × 40", "✅ 已达成"],
            ["Lv.3", "玄铁石 × 300", "地煞符 × 150", "灵元宝 × 60", "✅ 已达成"],
            ["Lv.4", "玄铁石 × 400", "天罡符 × 200", "灵元宝 × 80", "✅ 已达成"],
            ["Lv.5", "寒冰石 × 500", "天罡符 × 250", "灵元宝 × 100", "❌ 材料不足 (差150)"],
            ["", "", "", "", ""],
            ["汇总", "可达最高等级: Lv.4", "共提升 4 级", "", ""],
        ]
        headers = ["等级", "开启消耗", "刷新主材料", "刷新保底", "状态"]
        
        show_table_result(self, "注灵养成计算结果", data, headers)
    
    def _demo_materials(self):
        """示例2：材料需求汇总"""
        data = [
            ["天罡石", "1000", "500", "500", "充足 ✅"],
            ["玄铁石", "1500", "1200", "300", "充足 ✅"],
            ["寒冰石", "800", "900", "-100", "不足 ❌"],
            ["地煞符", "600", "450", "150", "充足 ✅"],
            ["天罡符", "400", "600", "-200", "不足 ❌"],
            ["灵元宝", "200", "150", "50", "充足 ✅"],
        ]
        headers = ["材料名称", "需求数量", "持有数量", "剩余/缺少", "状态"]
        
        show_table_result(self, "材料需求汇总表", data, headers)
    
    def _demo_dict_data(self):
        """示例3：字典格式数据"""
        data = [
            {
                "装备部位": "武器",
                "当前等级": "Lv.10",
                "目标等级": "Lv.15",
                "所需金币": "50,000",
                "所需材料": "精铁 × 200",
                "预计战力": "+1,500",
            },
            {
                "装备部位": "头盔",
                "当前等级": "Lv.8",
                "目标等级": "Lv.15",
                "所需金币": "40,000",
                "所需材料": "精铁 × 150",
                "预计战力": "+1,200",
            },
            {
                "装备部位": "护甲",
                "当前等级": "Lv.12",
                "目标等级": "Lv.15",
                "所需金币": "30,000",
                "所需材料": "精铁 × 100",
                "预计战力": "+800",
            },
            {
                "装备部位": "裤子",
                "当前等级": "Lv.9",
                "目标等级": "Lv.15",
                "所需金币": "35,000",
                "所需材料": "精铁 × 120",
                "预计战力": "+1,000",
            },
        ]
        # 注意：使用字典列表时，headers会自动从字典的键提取
        show_table_result(self, "装备强化计划", data)
    
    def _demo_large_data(self):
        """示例4：大数据量测试"""
        data = []
        for i in range(1, 101):
            status = "✅" if i % 3 != 0 else "❌"
            data.append([
                f"第 {i} 项",
                f"数值 {i * 100}",
                f"金币 {i * 1000:,}",
                f"材料 × {i * 10}",
                status,
            ])
        
        headers = ["序号", "数值", "消耗金币", "消耗材料", "状态"]
        show_table_result(self, "大数据量测试 (100行)", data, headers)


# 如果需要在主程序中注册这个演示页面，在 main.py 中添加：
# from pages.table_demo import TableDemoPage
# 然后在导航菜单中添加对应的按钮
