"""
装备重铸计算器模块
根据材料量计算可达到的重铸等级，或根据目标等级计算所需材料。
支持6种材料类型，按等级0-30、阶段0-5的完整消耗表。
所有材料消耗量已乘以11（11件装备）。
"""

import customtkinter as ctk


# ============================================================
# 重铸材料消耗表数据（单件装备）
# 每个条目：{level: 等级, stage: 阶段, materialA: 材料A类型,
#            materialARequired: 材料A需求量, materialBRequired: 材料B(保底)需求量}
# ============================================================
REFORGE_DATA = [
    {"level": 0, "stage": 0, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 1, "stage": 0, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 1, "stage": 1, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 1, "stage": 2, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 1, "stage": 3, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 1, "stage": 4, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 1, "stage": 5, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 2, "stage": 0, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 2, "stage": 1, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 2, "stage": 2, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 2, "stage": 3, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 2, "stage": 4, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 2, "stage": 5, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 3, "stage": 0, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 3, "stage": 1, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 3, "stage": 2, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 3, "stage": 3, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 3, "stage": 4, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 3, "stage": 5, "materialA": "不灭离炎", "materialARequired": 1, "materialBRequired": 0},
    {"level": 4, "stage": 0, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 4, "stage": 1, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 4, "stage": 2, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 4, "stage": 3, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 4, "stage": 4, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 4, "stage": 5, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 5, "stage": 0, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 5, "stage": 1, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 5, "stage": 2, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 5, "stage": 3, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 5, "stage": 4, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 5, "stage": 5, "materialA": "不灭离炎", "materialARequired": 2, "materialBRequired": 1},
    {"level": 6, "stage": 0, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 6, "stage": 1, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 6, "stage": 2, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 6, "stage": 3, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 6, "stage": 4, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 6, "stage": 5, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 7, "stage": 0, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 7, "stage": 1, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 7, "stage": 2, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 7, "stage": 3, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 7, "stage": 4, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 7, "stage": 5, "materialA": "青璃焰光", "materialARequired": 2, "materialBRequired": 1},
    {"level": 8, "stage": 0, "materialA": "青璃焰光", "materialARequired": 2.10526315789474, "materialBRequired": 1.05263157894737},
    {"level": 8, "stage": 1, "materialA": "青璃焰光", "materialARequired": 2.10526315789474, "materialBRequired": 1.05263157894737},
    {"level": 8, "stage": 2, "materialA": "青璃焰光", "materialARequired": 3.15789473684211, "materialBRequired": 1.05263157894737},
    {"level": 8, "stage": 3, "materialA": "青璃焰光", "materialARequired": 3.15789473684211, "materialBRequired": 1.05263157894737},
    {"level": 8, "stage": 4, "materialA": "青璃焰光", "materialARequired": 4.21052631578947, "materialBRequired": 1.05263157894737},
    {"level": 8, "stage": 5, "materialA": "青璃焰光", "materialARequired": 4.21052631578947, "materialBRequired": 1.05263157894737},
    {"level": 9, "stage": 0, "materialA": "青璃焰光", "materialARequired": 2.35294117647059, "materialBRequired": 1.17647058823529},
    {"level": 9, "stage": 1, "materialA": "青璃焰光", "materialARequired": 2.35294117647059, "materialBRequired": 1.17647058823529},
    {"level": 9, "stage": 2, "materialA": "青璃焰光", "materialARequired": 3.52941176470588, "materialBRequired": 1.17647058823529},
    {"level": 9, "stage": 3, "materialA": "青璃焰光", "materialARequired": 3.52941176470588, "materialBRequired": 1.17647058823529},
    {"level": 9, "stage": 4, "materialA": "青璃焰光", "materialARequired": 4.70588235294118, "materialBRequired": 1.17647058823529},
    {"level": 9, "stage": 5, "materialA": "青璃焰光", "materialARequired": 4.70588235294118, "materialBRequired": 1.17647058823529},
    {"level": 10, "stage": 0, "materialA": "青璃焰光", "materialARequired": 5.33333333333333, "materialBRequired": 1.33333333333333},
    {"level": 10, "stage": 1, "materialA": "青璃焰光", "materialARequired": 5.33333333333333, "materialBRequired": 1.33333333333333},
    {"level": 10, "stage": 2, "materialA": "青璃焰光", "materialARequired": 6.66666666666667, "materialBRequired": 1.33333333333333},
    {"level": 10, "stage": 3, "materialA": "青璃焰光", "materialARequired": 6.66666666666667, "materialBRequired": 1.33333333333333},
    {"level": 10, "stage": 4, "materialA": "青璃焰光", "materialARequired": 8, "materialBRequired": 1.33333333333333},
    {"level": 10, "stage": 5, "materialA": "青璃焰光", "materialARequired": 8, "materialBRequired": 1.33333333333333},
    {"level": 11, "stage": 0, "materialA": "冥雷寒铁", "materialARequired": 12, "materialBRequired": 2.66666666666667},
    {"level": 11, "stage": 1, "materialA": "冥雷寒铁", "materialARequired": 12, "materialBRequired": 2.66666666666667},
    {"level": 11, "stage": 2, "materialA": "冥雷寒铁", "materialARequired": 16, "materialBRequired": 2.66666666666667},
    {"level": 11, "stage": 3, "materialA": "冥雷寒铁", "materialARequired": 16, "materialBRequired": 2.66666666666667},
    {"level": 11, "stage": 4, "materialA": "冥雷寒铁", "materialARequired": 20, "materialBRequired": 2.66666666666667},
    {"level": 11, "stage": 5, "materialA": "冥雷寒铁", "materialARequired": 20, "materialBRequired": 2.66666666666667},
    {"level": 12, "stage": 0, "materialA": "冥雷寒铁", "materialARequired": 12.8571428571429, "materialBRequired": 2.85714285714286},
    {"level": 12, "stage": 1, "materialA": "冥雷寒铁", "materialARequired": 12.8571428571429, "materialBRequired": 2.85714285714286},
    {"level": 12, "stage": 2, "materialA": "冥雷寒铁", "materialARequired": 17.1428571428571, "materialBRequired": 2.85714285714286},
    {"level": 12, "stage": 3, "materialA": "冥雷寒铁", "materialARequired": 17.1428571428571, "materialBRequired": 2.85714285714286},
    {"level": 12, "stage": 4, "materialA": "冥雷寒铁", "materialARequired": 21.4285714285714, "materialBRequired": 2.85714285714286},
    {"level": 12, "stage": 5, "materialA": "冥雷寒铁", "materialARequired": 21.4285714285714, "materialBRequired": 2.85714285714286},
    {"level": 13, "stage": 0, "materialA": "冥雷寒铁", "materialARequired": 12.8571428571429, "materialBRequired": 2.85714285714286},
    {"level": 13, "stage": 1, "materialA": "冥雷寒铁", "materialARequired": 12.8571428571429, "materialBRequired": 2.85714285714286},
    {"level": 13, "stage": 2, "materialA": "冥雷寒铁", "materialARequired": 17.1428571428571, "materialBRequired": 2.85714285714286},
    {"level": 13, "stage": 3, "materialA": "冥雷寒铁", "materialARequired": 17.1428571428571, "materialBRequired": 2.85714285714286},
    {"level": 13, "stage": 4, "materialA": "冥雷寒铁", "materialARequired": 21.4285714285714, "materialBRequired": 2.85714285714286},
    {"level": 13, "stage": 5, "materialA": "冥雷寒铁", "materialARequired": 21.4285714285714, "materialBRequired": 2.85714285714286},
    {"level": 14, "stage": 0, "materialA": "冥雷寒铁", "materialARequired": 18.3333333333333, "materialBRequired": 5},
    {"level": 14, "stage": 1, "materialA": "冥雷寒铁", "materialARequired": 18.3333333333333, "materialBRequired": 5},
    {"level": 14, "stage": 2, "materialA": "冥雷寒铁", "materialARequired": 23.3333333333333, "materialBRequired": 5},
    {"level": 14, "stage": 3, "materialA": "冥雷寒铁", "materialARequired": 23.3333333333333, "materialBRequired": 5},
    {"level": 14, "stage": 4, "materialA": "冥雷寒铁", "materialARequired": 28.3333333333333, "materialBRequired": 5},
    {"level": 14, "stage": 5, "materialA": "冥雷寒铁", "materialARequired": 28.3333333333333, "materialBRequired": 5},
    {"level": 15, "stage": 0, "materialA": "冥雷寒铁", "materialARequired": 18.3333333333333, "materialBRequired": 5},
    {"level": 15, "stage": 1, "materialA": "冥雷寒铁", "materialARequired": 18.3333333333333, "materialBRequired": 5},
    {"level": 15, "stage": 2, "materialA": "冥雷寒铁", "materialARequired": 23.3333333333333, "materialBRequired": 5},
    {"level": 15, "stage": 3, "materialA": "冥雷寒铁", "materialARequired": 23.3333333333333, "materialBRequired": 5},
    {"level": 15, "stage": 4, "materialA": "冥雷寒铁", "materialARequired": 28.3333333333333, "materialBRequired": 5},
    {"level": 15, "stage": 5, "materialA": "冥雷寒铁", "materialARequired": 28.3333333333333, "materialBRequired": 5},
    {"level": 16, "stage": 0, "materialA": "辉光玄铁", "materialARequired": 20, "materialBRequired": 5.45454545454545},
    {"level": 16, "stage": 1, "materialA": "辉光玄铁", "materialARequired": 20, "materialBRequired": 5.45454545454545},
    {"level": 16, "stage": 2, "materialA": "辉光玄铁", "materialARequired": 25.4545454545455, "materialBRequired": 5.45454545454545},
    {"level": 16, "stage": 3, "materialA": "辉光玄铁", "materialARequired": 25.4545454545455, "materialBRequired": 5.45454545454545},
    {"level": 16, "stage": 4, "materialA": "辉光玄铁", "materialARequired": 30.9090909090909, "materialBRequired": 5.45454545454545},
    {"level": 16, "stage": 5, "materialA": "辉光玄铁", "materialARequired": 30.9090909090909, "materialBRequired": 5.45454545454545},
    {"level": 17, "stage": 0, "materialA": "辉光玄铁", "materialARequired": 26, "materialBRequired": 10},
    {"level": 17, "stage": 1, "materialA": "辉光玄铁", "materialARequired": 26, "materialBRequired": 10},
    {"level": 17, "stage": 2, "materialA": "辉光玄铁", "materialARequired": 32, "materialBRequired": 10},
    {"level": 17, "stage": 3, "materialA": "辉光玄铁", "materialARequired": 32, "materialBRequired": 10},
    {"level": 17, "stage": 4, "materialA": "辉光玄铁", "materialARequired": 38, "materialBRequired": 10},
    {"level": 17, "stage": 5, "materialA": "辉光玄铁", "materialARequired": 38, "materialBRequired": 10},
    {"level": 18, "stage": 0, "materialA": "辉光玄铁", "materialARequired": 26, "materialBRequired": 10},
    {"level": 18, "stage": 1, "materialA": "辉光玄铁", "materialARequired": 26, "materialBRequired": 10},
    {"level": 18, "stage": 2, "materialA": "辉光玄铁", "materialARequired": 32, "materialBRequired": 10},
    {"level": 18, "stage": 3, "materialA": "辉光玄铁", "materialARequired": 32, "materialBRequired": 10},
    {"level": 18, "stage": 4, "materialA": "辉光玄铁", "materialARequired": 38, "materialBRequired": 10},
    {"level": 18, "stage": 5, "materialA": "辉光玄铁", "materialARequired": 38, "materialBRequired": 10},
    {"level": 19, "stage": 0, "materialA": "辉光玄铁", "materialARequired": 28.8888888888889, "materialBRequired": 11.1111111111111},
    {"level": 19, "stage": 1, "materialA": "辉光玄铁", "materialARequired": 28.8888888888889, "materialBRequired": 11.1111111111111},
    {"level": 19, "stage": 2, "materialA": "辉光玄铁", "materialARequired": 35.5555555555556, "materialBRequired": 11.1111111111111},
    {"level": 19, "stage": 3, "materialA": "辉光玄铁", "materialARequired": 35.5555555555556, "materialBRequired": 11.1111111111111},
    {"level": 19, "stage": 4, "materialA": "辉光玄铁", "materialARequired": 42.2222222222222, "materialBRequired": 11.1111111111111},
    {"level": 19, "stage": 5, "materialA": "辉光玄铁", "materialARequired": 42.2222222222222, "materialBRequired": 11.1111111111111},
    {"level": 20, "stage": 0, "materialA": "辉光玄铁", "materialARequired": 35.7142857142857, "materialBRequired": 19.047619047619},
    {"level": 20, "stage": 1, "materialA": "辉光玄铁", "materialARequired": 35.7142857142857, "materialBRequired": 19.047619047619},
    {"level": 20, "stage": 2, "materialA": "辉光玄铁", "materialARequired": 42.8571428571429, "materialBRequired": 19.047619047619},
    {"level": 20, "stage": 3, "materialA": "辉光玄铁", "materialARequired": 42.8571428571429, "materialBRequired": 19.047619047619},
    {"level": 20, "stage": 4, "materialA": "辉光玄铁", "materialARequired": 50, "materialBRequired": 19.047619047619},
    {"level": 20, "stage": 5, "materialA": "辉光玄铁", "materialARequired": 50, "materialBRequired": 19.047619047619},
    {"level": 21, "stage": 0, "materialA": "坠影紫晶", "materialARequired": 37.5, "materialBRequired": 20},
    {"level": 21, "stage": 1, "materialA": "坠影紫晶", "materialARequired": 37.5, "materialBRequired": 20},
    {"level": 21, "stage": 2, "materialA": "坠影紫晶", "materialARequired": 45, "materialBRequired": 20},
    {"level": 21, "stage": 3, "materialA": "坠影紫晶", "materialARequired": 45, "materialBRequired": 20},
    {"level": 21, "stage": 4, "materialA": "坠影紫晶", "materialARequired": 52.5, "materialBRequired": 20},
    {"level": 21, "stage": 5, "materialA": "坠影紫晶", "materialARequired": 52.5, "materialBRequired": 20},
    {"level": 22, "stage": 0, "materialA": "坠影紫晶", "materialARequired": 39.4736842105263, "materialBRequired": 21.0526315789474},
    {"level": 22, "stage": 1, "materialA": "坠影紫晶", "materialARequired": 39.4736842105263, "materialBRequired": 21.0526315789474},
    {"level": 22, "stage": 2, "materialA": "坠影紫晶", "materialARequired": 47.3684210526316, "materialBRequired": 21.0526315789474},
    {"level": 22, "stage": 3, "materialA": "坠影紫晶", "materialARequired": 47.3684210526316, "materialBRequired": 21.0526315789474},
    {"level": 22, "stage": 4, "materialA": "坠影紫晶", "materialARequired": 55.2631578947368, "materialBRequired": 21.0526315789474},
    {"level": 22, "stage": 5, "materialA": "坠影紫晶", "materialARequired": 55.2631578947368, "materialBRequired": 21.0526315789474},
    {"level": 23, "stage": 0, "materialA": "坠影紫晶", "materialARequired": 44.4444444444444, "materialBRequired": 27.7777777777778},
    {"level": 23, "stage": 1, "materialA": "坠影紫晶", "materialARequired": 44.4444444444444, "materialBRequired": 27.7777777777778},
    {"level": 23, "stage": 2, "materialA": "坠影紫晶", "materialARequired": 55.5555555555556, "materialBRequired": 27.7777777777778},
    {"level": 23, "stage": 3, "materialA": "坠影紫晶", "materialARequired": 55.5555555555556, "materialBRequired": 27.7777777777778},
    {"level": 23, "stage": 4, "materialA": "坠影紫晶", "materialARequired": 66.6666666666667, "materialBRequired": 27.7777777777778},
    {"level": 23, "stage": 5, "materialA": "坠影紫晶", "materialARequired": 66.6666666666667, "materialBRequired": 27.7777777777778},
    {"level": 24, "stage": 0, "materialA": "坠影紫晶", "materialARequired": 47.0588235294118, "materialBRequired": 29.4117647058824},
    {"level": 24, "stage": 1, "materialA": "坠影紫晶", "materialARequired": 47.0588235294118, "materialBRequired": 29.4117647058824},
    {"level": 24, "stage": 2, "materialA": "坠影紫晶", "materialARequired": 58.8235294117647, "materialBRequired": 29.4117647058824},
    {"level": 24, "stage": 3, "materialA": "坠影紫晶", "materialARequired": 58.8235294117647, "materialBRequired": 29.4117647058824},
    {"level": 24, "stage": 4, "materialA": "坠影紫晶", "materialARequired": 70.5882352941177, "materialBRequired": 29.4117647058824},
    {"level": 24, "stage": 5, "materialA": "坠影紫晶", "materialARequired": 70.5882352941177, "materialBRequired": 29.4117647058824},
    {"level": 25, "stage": 0, "materialA": "坠影紫晶", "materialARequired": 48.4848484848485, "materialBRequired": 30.3030303030303},
    {"level": 25, "stage": 1, "materialA": "坠影紫晶", "materialARequired": 51.6129032258064, "materialBRequired": 32.258064516129},
    {"level": 25, "stage": 2, "materialA": "坠影紫晶", "materialARequired": 68.9655172413793, "materialBRequired": 34.4827586206897},
    {"level": 25, "stage": 3, "materialA": "坠影紫晶", "materialARequired": 74.0740740740741, "materialBRequired": 37.037037037037},
    {"level": 25, "stage": 4, "materialA": "坠影紫晶", "materialARequired": 92.3076923076923, "materialBRequired": 38.4615384615385},
    {"level": 25, "stage": 5, "materialA": "坠影紫晶", "materialARequired": 96, "materialBRequired": 40},
    {"level": 26, "stage": 0, "materialA": "绯云玄晶", "materialARequired": 72, "materialBRequired": 48},
    {"level": 26, "stage": 1, "materialA": "绯云玄晶", "materialARequired": 72, "materialBRequired": 48},
    {"level": 26, "stage": 2, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 48},
    {"level": 26, "stage": 3, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 48},
    {"level": 26, "stage": 4, "materialA": "绯云玄晶", "materialARequired": 104, "materialBRequired": 48},
    {"level": 26, "stage": 5, "materialA": "绯云玄晶", "materialARequired": 104, "materialBRequired": 48},
    {"level": 27, "stage": 0, "materialA": "绯云玄晶", "materialARequired": 72, "materialBRequired": 48},
    {"level": 27, "stage": 1, "materialA": "绯云玄晶", "materialARequired": 72, "materialBRequired": 48},
    {"level": 27, "stage": 2, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 48},
    {"level": 27, "stage": 3, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 48},
    {"level": 27, "stage": 4, "materialA": "绯云玄晶", "materialARequired": 104, "materialBRequired": 48},
    {"level": 27, "stage": 5, "materialA": "绯云玄晶", "materialARequired": 104, "materialBRequired": 48},
    {"level": 28, "stage": 0, "materialA": "绯云玄晶", "materialARequired": 72, "materialBRequired": 48},
    {"level": 28, "stage": 1, "materialA": "绯云玄晶", "materialARequired": 72, "materialBRequired": 48},
    {"level": 28, "stage": 2, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 48},
    {"level": 28, "stage": 3, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 48},
    {"level": 28, "stage": 4, "materialA": "绯云玄晶", "materialARequired": 104, "materialBRequired": 48},
    {"level": 28, "stage": 5, "materialA": "绯云玄晶", "materialARequired": 104, "materialBRequired": 48},
    {"level": 29, "stage": 0, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 60},
    {"level": 29, "stage": 1, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 60},
    {"level": 29, "stage": 2, "materialA": "绯云玄晶", "materialARequired": 100, "materialBRequired": 60},
    {"level": 29, "stage": 3, "materialA": "绯云玄晶", "materialARequired": 100, "materialBRequired": 60},
    {"level": 29, "stage": 4, "materialA": "绯云玄晶", "materialARequired": 112, "materialBRequired": 60},
    {"level": 29, "stage": 5, "materialA": "绯云玄晶", "materialARequired": 112, "materialBRequired": 60},
    {"level": 30, "stage": 0, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 60},
    {"level": 30, "stage": 1, "materialA": "绯云玄晶", "materialARequired": 88, "materialBRequired": 60},
    {"level": 30, "stage": 2, "materialA": "绯云玄晶", "materialARequired": 100, "materialBRequired": 60},
    {"level": 30, "stage": 3, "materialA": "绯云玄晶", "materialARequired": 100, "materialBRequired": 60},
    {"level": 30, "stage": 4, "materialA": "绯云玄晶", "materialARequired": 112, "materialBRequired": 60},
    {"level": 30, "stage": 5, "materialA": "绯云玄晶", "materialARequired": 112, "materialBRequired": 60},
]

# 材料转换系数（相对于"不灭离炎"的倍数）
MATERIAL_CONVERSION = {
    "不灭离炎": 1,
    "青璃焰光": 3,
    "冥雷寒铁": 9,
    "辉光玄铁": 27,
}

MATERIAL_B_NAME = "忘川冥息"

EQUIPMENT_COUNT = 11  # 装备数量

# 预建 (level, stage) -> index 查找字典，消除线性搜索
_REFORGE_INDEX: dict = {(d["level"], d["stage"]): i for i, d in enumerate(REFORGE_DATA)}


class ToolCPage(ctk.CTkFrame):
    """装备重铸计算器界面（11件装备）"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self._build_ui()

    def _build_ui(self):
        """构建重铸计算器界面"""
        # 主滚动容器
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # ---- 页面标题 ----
        ctk.CTkLabel(
            scroll,
            text="⚔️ 装备重铸计算器",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        ctk.CTkLabel(
            scroll,
            text=f"支持 11 件装备同时重铸 · 等级 0-30 · 阶段 0-5",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_dim"],
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # ---- 标签页切换 ----
        tab_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["📊 根据材料计算等级", "🎯 根据目标计算材料"],
            height=34,
            font=ctk.CTkFont(size=13),
            selected_color=self.colors["nav_active"],
            unselected_color="#0f0f1a",
            selected_hover_color="#164080",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("📊 根据材料计算等级")

        # ---- Tab 1：根据材料计算等级 ----
        self.tab1_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        tab1_inner = ctk.CTkFrame(self.tab1_frame, fg_color="transparent")
        tab1_inner.pack(fill="x", padx=20, pady=18)
        tab1_inner.grid_columnconfigure((0, 1), weight=1)

        # 初始状态标题
        ctk.CTkLabel(
            tab1_inner, text="初始重铸状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        # 初始等级
        ctk.CTkLabel(tab1_inner, text="初始等级 (0-30)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t1_initial_level = ctk.CTkEntry(tab1_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_initial_level.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        self.t1_initial_level.insert(0, "0")

        # 初始阶段
        ctk.CTkLabel(tab1_inner, text="初始阶段 (0-5)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t1_initial_stage = ctk.CTkEntry(tab1_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_initial_stage.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.t1_initial_stage.insert(0, "0")

        # 材料类型
        ctk.CTkLabel(tab1_inner, text="重铸材料A类型",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(6, 3))

        self.t1_mat_type = ctk.CTkOptionMenu(
            tab1_inner,
            values=[
                "不灭离炎",
                "青璃焰光",
                "冥雷寒铁",
                "辉光玄铁",
                "坠影紫晶",
                "绯云玄晶",
            ],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t1_mat_type.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # 材料数量
        ctk.CTkLabel(tab1_inner, text="重铸A材料数量",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=5, column=0, sticky="w", padx=(0, 10), pady=(6, 3))
        self.t1_material_a = ctk.CTkEntry(tab1_inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_material_a.grid(row=6, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

        ctk.CTkLabel(tab1_inner, text="保底材料B数量",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=5, column=1, sticky="w", padx=(10, 0), pady=(6, 3))
        self.t1_material_b = ctk.CTkEntry(tab1_inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_material_b.grid(row=6, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))

        # 计算按钮
        ctk.CTkButton(
            tab1_inner,
            text="▶  计算可达到的重铸等级",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#0f3460", hover_color="#16213e",
            command=self._calc_reforge_by_materials,
        ).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(8, 8))

        # 结果区域
        self.t1_result = ctk.CTkTextbox(
            tab1_inner, height=160, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
        )
        self.t1_result.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.t1_result.insert("1.0", "等待计算...\n")
        self.t1_result.configure(state="disabled")

        # ---- Tab 2：根据目标计算材料 ----
        self.tab2_frame = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        # 不立即 grid，由标签页切换控制

        tab2_inner = ctk.CTkFrame(self.tab2_frame, fg_color="transparent")
        tab2_inner.pack(fill="x", padx=20, pady=18)
        tab2_inner.grid_columnconfigure((0, 1), weight=1)

        # 初始状态
        ctk.CTkLabel(
            tab2_inner, text="初始重铸状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ctk.CTkLabel(tab2_inner, text="初始等级 (0-30)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t2_start_level = ctk.CTkEntry(tab2_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_start_level.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        self.t2_start_level.insert(0, "0")

        ctk.CTkLabel(tab2_inner, text="初始阶段 (0-5)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t2_start_stage = ctk.CTkEntry(tab2_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_start_stage.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.t2_start_stage.insert(0, "0")

        # 目标状态
        ctk.CTkLabel(
            tab2_inner, text="目标重铸状态",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 8))

        ctk.CTkLabel(tab2_inner, text="目标等级 (0-30)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=4, column=0, sticky="w", padx=(0, 10), pady=(0, 3))
        self.t2_target_level = ctk.CTkEntry(tab2_inner, placeholder_text="30", height=32, corner_radius=6)
        self.t2_target_level.grid(row=5, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))
        self.t2_target_level.insert(0, "30")

        ctk.CTkLabel(tab2_inner, text="目标阶段 (0-5)",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=4, column=1, sticky="w", padx=(10, 0), pady=(0, 3))
        self.t2_target_stage = ctk.CTkEntry(tab2_inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_target_stage.grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=(0, 8))
        self.t2_target_stage.insert(0, "0")

        # 基准材料类型
        ctk.CTkLabel(tab2_inner, text="基准材料类型",
                     font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"], anchor="w").grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(6, 3))

        self.t2_mat_type = ctk.CTkOptionMenu(
            tab2_inner,
            values=[
                "不灭离炎",
                "青璃焰光",
                "冥雷寒铁",
                "辉光玄铁",
                "坠影紫晶",
                "绯云玄晶",
            ],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460",
            button_hover_color="#16213e",
        )
        self.t2_mat_type.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # 计算按钮
        ctk.CTkButton(
            tab2_inner,
            text="▶  计算所需材料",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=8,
            fg_color="#2e7d32", hover_color="#1b5e20",
            command=self._calc_materials_for_target,
        ).grid(row=8, column=0, columnspan=2, sticky="ew", pady=(8, 8))

        # 结果区域
        self.t2_result = ctk.CTkTextbox(
            tab2_inner, height=220, corner_radius=8,
            fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
        )
        self.t2_result.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.t2_result.insert("1.0", "等待计算...\n")
        self.t2_result.configure(state="disabled")

        # ---- 材料转换说明 ----
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            info_inner,
            text="📖 材料转换关系",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).pack(fill="x", pady=(0, 8))

        rules = [
            "· 青璃焰光 = 不灭离炎 × 3",
            "· 冥雷寒铁 = 不灭离炎 × 9",
            "· 辉光玄铁 = 不灭离炎 × 27",
            "· 坠影紫晶和绯云玄晶不可转换",
            "",
            f"⚠ 所有消耗量已 × {EQUIPMENT_COUNT}（{EQUIPMENT_COUNT} 件装备）",
        ]
        for rule in rules:
            ctk.CTkLabel(
                info_inner, text=rule,
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_dim"], anchor="w",
            ).pack(fill="x", pady=1)

    # ================================================================
    # 标签页切换
    # ================================================================

    def _on_tab_change(self, value):
        """切换标签页"""
        if value == "📊 根据材料计算等级":
            self.tab1_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab2_frame.grid_forget()
        else:
            self.tab2_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            self.tab1_frame.grid_forget()

    # ================================================================
    # 辅助方法
    # ================================================================

    def _show_result(self, textbox: ctk.CTkTextbox, text: str):
        """在结果区域显示文本"""
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")

    def _show_error(self, textbox: ctk.CTkTextbox, msg: str):
        """显示错误信息"""
        self._show_result(textbox, f"⚠ {msg}\n")

    def _find_data_index(self, level: int, stage: int) -> int:
        """在 REFORGE_DATA 中查找指定等级和阶段的索引（O(1) 字典查找）"""
        return _REFORGE_INDEX.get((level, stage), -1)

    def _format_num(self, num: float) -> str:
        """格式化数字显示"""
        if num >= 10000:
            return f"{num:,.1f}"
        if num >= 100:
            return f"{num:,.2f}"
        if num >= 1:
            return f"{num:,.3f}"
        return f"{num:.4f}"

    # ================================================================
    # 功能一：根据材料量计算可达到的重铸等级
    # ================================================================

    def _calc_reforge_by_materials(self):
        """根据拥有的材料量计算可达到的最高重铸等级/阶段"""
        # --- 获取输入 ---
        try:
            init_level = int(self.t1_initial_level.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的初始等级 (0-30)")
            return

        try:
            init_stage = int(self.t1_initial_stage.get() or "0")
        except ValueError:
            self._show_error(self.t1_result, "请输入有效的初始阶段 (0-5)")
            return

        mat_type = self.t1_mat_type.get()
        if not mat_type:
            self._show_error(self.t1_result, "请选择重铸材料A类型")
            return

        mat_a_input = self.t1_material_a.get().strip()
        mat_b_input = self.t1_material_b.get().strip()

        has_mat_a = mat_a_input != ""
        has_mat_b = mat_b_input != ""

        if not has_mat_a and not has_mat_b:
            self._show_error(self.t1_result, "材料A数量和保底材料B不能同时为空")
            return

        try:
            remaining_a = float(mat_a_input) if has_mat_a else float("inf")
            remaining_b = float(mat_b_input) if has_mat_b else float("inf")
        except ValueError:
            self._show_error(self.t1_result, "材料数量请输入有效数字")
            return

        # 校验范围
        if not (0 <= init_level <= 30):
            self._show_error(self.t1_result, "初始等级必须在 0-30 之间")
            return
        if not (0 <= init_stage <= 5):
            self._show_error(self.t1_result, "初始阶段必须在 0-5 之间")
            return

        # --- 开始计算 ---
        current_level = init_level
        current_stage = init_stage
        total_used_a = 0.0
        total_used_b = 0.0

        start_index = self._find_data_index(init_level, init_stage)
        if start_index < 0:
            self._show_error(self.t1_result, "无效的初始等级和阶段")
            return

        for i in range(start_index, len(REFORGE_DATA)):
            stage_data = REFORGE_DATA[i]
            required_a = stage_data["materialARequired"] * EQUIPMENT_COUNT
            required_b = stage_data["materialBRequired"] * EQUIPMENT_COUNT

            # 材料类型不同时进行转换
            if stage_data["materialA"] != mat_type:
                if (stage_data["materialA"] in MATERIAL_CONVERSION
                        and mat_type in MATERIAL_CONVERSION):
                    required_a = required_a * MATERIAL_CONVERSION[stage_data["materialA"]] / MATERIAL_CONVERSION[mat_type]
                elif stage_data["materialA"] != mat_type:
                    # 不可转换的材料类型（坠影紫晶/绯云玄晶），无法继续
                    break

            # 检查是否足够
            if (remaining_a is None or remaining_a >= required_a) and \
               (remaining_b is None or remaining_b >= required_b):
                if remaining_a != float("inf"):
                    remaining_a -= required_a
                if remaining_b != float("inf"):
                    remaining_b -= required_b

                total_used_a += required_a
                total_used_b += required_b
                current_level = stage_data["level"]
                current_stage = stage_data["stage"]

                # 更新到下一阶段
                if stage_data["stage"] == 5:
                    current_level = stage_data["level"] + 1
                    current_stage = 0
                else:
                    current_stage = stage_data["stage"] + 1
            else:
                break

        # --- 构建结果文本 ---
        lines = []
        lines.append(f"━━━ 重铸结果 ━━━")
        lines.append(f"\n最高可达到：{current_level} 级 {current_stage} 阶段")
        lines.append(f"(从 {init_level} 级 {init_stage} 阶段出发)")
        lines.append(f"\n━━━ 累计消耗 ━━━")
        lines.append(f"材料A ({mat_type}): {self._format_num(total_used_a)}")
        lines.append(f"材料B ({MATERIAL_B_NAME}): {self._format_num(total_used_b)}")

        if remaining_a != float("inf") and remaining_a > 0.0001:
            lines.append(f"\n剩余材料A: {self._format_num(remaining_a)}")
        if remaining_b != float("inf") and remaining_b > 0.0001:
            lines.append(f"剩余材料B: {self._format_num(remaining_b)}")

        lines.append(f"\n(以上为 {EQUIPMENT_COUNT} 件装备的总消耗)")

        self._show_result(self.t1_result, "\n".join(lines) + "\n")

    # ================================================================
    # 功能二：根据目标等级计算所需材料
    # ================================================================

    def _calc_materials_for_target(self):
        """计算从初始状态升级到目标状态所需的各种材料量"""
        # --- 获取输入 ---
        try:
            start_level = int(self.t2_start_level.get() or "0")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的初始等级 (0-30)")
            return

        try:
            start_stage = int(self.t2_start_stage.get() or "0")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的初始阶段 (0-5)")
            return

        try:
            target_level = int(self.t2_target_level.get() or "30")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的目标等级 (0-30)")
            return

        try:
            target_stage = int(self.t2_target_stage.get() or "0")
        except ValueError:
            self._show_error(self.t2_result, "请输入有效的目标阶段 (0-5)")
            return

        target_mat_type = self.t2_mat_type.get()

        # 校验范围
        if not (0 <= start_level <= 30):
            self._show_error(self.t2_result, "初始等级必须在 0-30 之间")
            return
        if not (0 <= start_stage <= 5):
            self._show_error(self.t2_result, "初始阶段必须在 0-5 之间")
            return
        if not (0 <= target_level <= 30):
            self._show_error(self.t2_result, "目标等级必须在 0-30 之间")
            return
        if not (0 <= target_stage <= 5):
            self._show_error(self.t2_result, "目标阶段必须在 0-5 之间")
            return

        if (target_level < start_level) or (target_level == start_level and target_stage <= start_stage):
            self._show_error(self.t2_result, "目标等级/阶段必须大于初始等级/阶段")
            return

        # --- 计算各材料总需求 ---
        total_materials = {
            "不灭离炎": 0.0,
            "青璃焰光": 0.0,
            "冥雷寒铁": 0.0,
            "辉光玄铁": 0.0,
            "坠影紫晶": 0.0,
            "绯云玄晶": 0.0,
            MATERIAL_B_NAME: 0.0,
        }

        start_idx = self._find_data_index(start_level, start_stage)
        end_idx = self._find_data_index(target_level, target_stage)

        if start_idx < 0:
            self._show_error(self.t2_result, "无效的初始等级和阶段")
            return
        if end_idx < 0:
            self._show_error(self.t2_result, "无效的目标等级和阶段")
            return
        if start_idx >= end_idx:
            self._show_error(self.t2_result, "目标等级/阶段必须大于初始等级/阶段")
            return

        for i in range(start_idx, end_idx):
            sd = REFORGE_DATA[i]
            req_a = sd["materialARequired"] * EQUIPMENT_COUNT
            req_b = sd["materialBRequired"] * EQUIPMENT_COUNT
            total_materials[sd["materialA"]] += req_a
            total_materials[MATERIAL_B_NAME] += req_b

        # --- 计算转换为基准材料的总需求 ---
        converted_total = 0.0
        for material_name, amount in total_materials.items():
            if material_name == MATERIAL_B_NAME:
                continue
            if amount > 0:
                if material_name in MATERIAL_CONVERSION and target_mat_type in MATERIAL_CONVERSION:
                    converted_total += amount * MATERIAL_CONVERSION[material_name] / MATERIAL_CONVERSION[target_mat_type]
                elif material_name == target_mat_type:
                    converted_total += amount

        # --- 构建结果文本 ---
        lines = []
        lines.append(f"━━━ 材料需求 ━━━")
        lines.append(f"\n从 {start_level} 级 {start_stage} 阶段 → {target_level} 级 {target_stage} 阶段")
        lines.append(f"共需提升 {end_idx - start_idx} 个阶段\n")

        lines.append("┌─────────────────────────────┐")
        lines.append("│ 各材料原始需求 (×11件)       │")
        lines.append("├─────────────────────────────┤")

        has_materials = False
        for mname, amt in total_materials.items():
            if amt > 0.0001:
                has_materials = True
                lines.append(f"│ {mname:<12}{self._format_num(amt):>15} │")

        if not has_materials:
            lines.append("│ 无需升级                      │")

        lines.append("└─────────────────────────────┘")

        if converted_total > 0.0001:
            lines.append(f"\n▸ 转换为 [{target_mat_type}] 总计: {self._format_num(converted_total)}")

        lines.append(f"\n(以上为 {EQUIPMENT_COUNT} 件装备的总消耗)")

        self._show_result(self.t2_result, "\n".join(lines) + "\n")
