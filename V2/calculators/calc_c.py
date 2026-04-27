"""
装备重铸计算引擎
纯数据 + 纯计算函数，不依赖任何 UI 框架。
"""

# ============================================================
# 数据常量
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


# ============================================================
# 纯函数
# ============================================================

def find_data_index(level: int, stage: int) -> int:
    """在 REFORGE_DATA 中查找指定等级和阶段的索引（O(1) 字典查找）"""
    return _REFORGE_INDEX.get((level, stage), -1)


def format_num(num: float) -> str:
    """格式化数字显示"""
    if num >= 10000:
        return f"{num:,.1f}"
    if num >= 100:
        return f"{num:,.2f}"
    if num >= 1:
        return f"{num:,.3f}"
    return f"{num:.4f}"


# ============================================================
# 计算函数
# ============================================================

def calc_reforge_by_materials(init_level: int, init_stage: int,
                              mat_type: str, remaining_a: float,
                              remaining_b: float) -> dict:
    """
    根据拥有的材料量计算可达到的最高重铸等级/阶段。

    参数:
        init_level: 初始等级 (0-30)
        init_stage: 初始阶段 (0-5)
        mat_type: 材料A类型名称
        remaining_a: 材料A数量 (float('inf') 表示无限)
        remaining_b: 材料B数量 (float('inf') 表示无限)

    返回:
        dict: 包含 current_level, current_stage, total_used_a, total_used_b, error
    """
    start_index = find_data_index(init_level, init_stage)
    if start_index < 0:
        return {"error": "无效的初始等级和阶段"}

    current_level = init_level
    current_stage = init_stage
    total_used_a = 0.0
    total_used_b = 0.0

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
                break

        # 检查是否足够
        if remaining_a >= required_a and remaining_b >= required_b:
            if remaining_a != float("inf"):
                remaining_a -= required_a
            if remaining_b != float("inf"):
                remaining_b -= required_b

            total_used_a += required_a
            total_used_b += required_b
            current_level = stage_data["level"]
            current_stage = stage_data["stage"]

            if stage_data["stage"] == 5:
                current_level = stage_data["level"] + 1
                current_stage = 0
            else:
                current_stage = stage_data["stage"] + 1
        else:
            break

    return {
        "current_level": current_level,
        "current_stage": current_stage,
        "total_used_a": total_used_a,
        "total_used_b": total_used_b,
        "remaining_a": remaining_a,
        "remaining_b": remaining_b,
        "error": None,
    }


def calc_materials_for_target(start_level: int, start_stage: int,
                              target_level: int, target_stage: int,
                              target_mat_type: str) -> dict:
    """
    计算从初始状态升级到目标状态所需的各种材料量。

    返回:
        dict: 包含 total_materials, converted_total, start_idx, end_idx, error
    """
    start_idx = find_data_index(start_level, start_stage)
    end_idx = find_data_index(target_level, target_stage)

    if start_idx < 0:
        return {"error": "无效的初始等级和阶段"}
    if end_idx < 0:
        return {"error": "无效的目标等级和阶段"}
    if start_idx >= end_idx:
        return {"error": "目标等级/阶段必须大于初始等级/阶段"}

    total_materials = {
        "不灭离炎": 0.0, "青璃焰光": 0.0, "冥雷寒铁": 0.0,
        "辉光玄铁": 0.0, "坠影紫晶": 0.0, "绯云玄晶": 0.0,
        MATERIAL_B_NAME: 0.0,
    }

    for i in range(start_idx, end_idx):
        sd = REFORGE_DATA[i]
        req_a = sd["materialARequired"] * EQUIPMENT_COUNT
        req_b = sd["materialBRequired"] * EQUIPMENT_COUNT
        total_materials[sd["materialA"]] += req_a
        total_materials[MATERIAL_B_NAME] += req_b

    # 计算转换为基准材料的总需求
    converted_total = 0.0
    for material_name, amount in total_materials.items():
        if material_name == MATERIAL_B_NAME:
            continue
        if amount > 0:
            if material_name in MATERIAL_CONVERSION and target_mat_type in MATERIAL_CONVERSION:
                converted_total += amount * MATERIAL_CONVERSION[material_name] / MATERIAL_CONVERSION[target_mat_type]
            elif material_name == target_mat_type:
                converted_total += amount

    return {
        "total_materials": total_materials,
        "converted_total": converted_total,
        "stages_count": end_idx - start_idx,
        "error": None,
    }
