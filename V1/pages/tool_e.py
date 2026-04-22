"""
圣石养成计算器模块
QQ华夏手游经典区 · 圣石/玄石/罡石镶嵌养成系统

支持两种计算模式：
  模式一：根据已有材料计算可达到的等级
  模式二：根据目标等级计算所需材料

数据来源：圣石养成数据_AI版.xlsx（圣石120级 / 玄石360级 / 罡石150级）
"""

import customtkinter as ctk


# ============================================================
# 一、部位配置
# ============================================================
PART_CONFIG = {
    "背部":   {"slot1系": "气海", "slot2系": "气海", "slot3系": "气海", "count": 1},
    "腰部":   {"slot1系": "气海", "slot2系": "气海", "slot3系": "气海", "count": 1},
    "脚部":   {"slot1系": "气海", "slot2系": "气海", "slot3系": "气海", "count": 1},
    "腿部":   {"slot1系": "气海", "slot2系": "气海", "slot3系": "气海", "count": 1},
    "右手武器":{"slot1系": "极意", "slot2系": "极意", "slot3系": "极意(威霆)", "count": 1},
    "手指×2": {"slot1系": "极意", "slot2系": "极意", "slot3系": "极意",     "count": 2},
    "腕部":   {"slot1系": "极意", "slot2系": "极意", "slot3系": "气海(渊泽)", "count": 1},
    "头部":   {"slot1系": "可选", "slot2系": "可选", "slot3系": "可选",       "count": 1},
    "胸部":   {"slot1系": "可选", "slot2系": "可选", "slot3系": "可选",       "count": 1},
    "颈部":   {"slot1系": "可选", "slot2系": "可选", "slot3系": "可选",       "count": 1},
}

# 槽位类型上限
SLOT_LIMITS = {
    "圣石(栏位1)": 120,
    "玄石(栏位2)": 360,
    "罡石(栏位3)": 150,
}

# 槽位道具名称映射
SLOT_ITEM_NAMES = {
    ("圣石(栏位1)", "气海"): None,          # 圣石只消耗积分，无额外道具
    ("圣石(栏位1)", "极意"): None,
    ("圣石(栏位1)", "金刚"): None,
    ("圣石(栏位1)", "灵柔"): None,
    ("玄石(栏位2)", "气海"): "气海圣石",
    ("玄石(栏位2)", "极意"): "极意圣石",
    ("玄石(栏位2)", "金刚"): "金刚圣石",
    ("玄石(栏位2)", "灵柔"): "灵柔圣石",
    ("罡石(栏位3)", "气海"): "气海罡石",
    ("罡石(栏位3)", "极意"): "威霆罡石",
    ("罡石(栏位3)", "金刚"): "金刚罡石",
    ("罡石(栏位3)", "灵柔"): "灵柔罡石",
}


# ============================================================
# 二、逐级消耗数据（从Excel提取，已内嵌为字面量）
# 数据来源：圣石养成数据_AI版.xlsx
#   圣石: 120级(栏位1)  玄石: 360级(栏位2)  罡石: 150级(栏位3)
# ============================================================

# 原始元组: 圣石(lv, jf, stage_jf), 玄石(lv, jf, item, stage_jf), 罡石(lv, jf, item, stage_jf, stage_ITEM)
_STONE_RAW = [
    (1, 5, 0),(2, 5, 0),(3, 5, 0),(4, 5, 0),(5, 5, 0),
    (6, 5, 0),(7, 5, 0),(8, 5, 0),(9, 5, 0),(10, 5, 0),
    (11, 5, 0),(12, 5, 0),(13, 5, 0),(14, 5, 0),(15, 5, 0),
    (16, 5, 0),(17, 5, 0),(18, 5, 0),(19, 5, 0),(20, 5, 500),
    (21, 5, 0),(22, 5, 0),(23, 5, 0),(24, 5, 0),(25, 5, 0),
    (26, 25, 0),(27, 25, 0),(28, 25, 0),(29, 25, 0),(30, 25, 0),
    (31, 25, 0),(32, 25, 0),(33, 25, 0),(34, 25, 0),(35, 25, 0),
    (36, 25, 0),(37, 25, 0),(38, 25, 0),(39, 25, 0),(40, 25, 1500),
    (41, 25, 0),(42, 25, 0),(43, 25, 0),(44, 25, 0),(45, 25, 0),
    (46, 25, 0),(47, 25, 0),(48, 25, 0),(49, 50, 0),(50, 50, 0),
    (51, 50, 0),(52, 50, 0),(53, 50, 0),(54, 50, 0),(55, 50, 0),
    (56, 50, 0),(57, 50, 0),(58, 50, 0),(59, 50, 0),(60, 50, 2000),
    (61, 50, 0),(62, 50, 0),(63, 50, 0),(64, 50, 0),(65, 50, 0),
    (66, 50, 0),(67, 50, 0),(68, 50, 0),(69, 50, 0),(70, 50, 0),
    (71, 50, 0),(72, 50, 0),(73, 50, 0),(74, 50, 0),(75, 50, 0),
    (76, 50, 0),(77, 50, 0),(78, 50, 0),(79, 50, 0),(80, 50, 4000),
    (81, 60, 0),(82, 60, 0),(83, 60, 0),(84, 60, 0),(85, 60, 0),
    (86, 60, 0),(87, 60, 0),(88, 60, 0),(89, 60, 0),(90, 60, 0),
    (91, 60, 0),(92, 60, 0),(93, 60, 0),(94, 60, 0),(95, 60, 0),
    (96, 60, 0),(97, 60, 0),(98, 60, 0),(99, 60, 0),(100, 100, 8000),
    (101, 100, 0),(102, 100, 0),(103, 100, 0),(104, 100, 0),(105, 100, 0),
    (106, 100, 0),(107, 100, 0),(108, 100, 0),(109, 100, 0),(110, 100, 0),
    (111, 100, 0),(112, 100, 0),(113, 100, 0),(114, 100, 0),(115, 100, 0),
    (116, 100, 0),(117, 100, 0),(118, 100, 0),(119, 100, 0),(120, 0, 0),
]

_XUAN_RAW = [
    (1, 5, 1, 0),(2, 5, 1, 0),(3, 5, 1, 0),(4, 5, 1, 0),(5, 5, 1, 0),
    (6, 5, 1, 0),(7, 5, 1, 0),(8, 5, 1, 0),(9, 5, 1, 0),(10, 5, 1, 0),
    (11, 5, 1, 0),(12, 5, 1, 0),(13, 5, 1, 0),(14, 5, 1, 0),(15, 5, 1, 0),
    (16, 5, 1, 0),(17, 5, 1, 0),(18, 5, 1, 0),(19, 5, 1, 0),(20, 5, 1, 0),
    (21, 5, 1, 0),(22, 5, 1, 0),(23, 5, 1, 0),(24, 5, 1, 0),(25, 5, 1, 0),
    (26, 5, 1, 0),(27, 5, 1, 0),(28, 5, 1, 0),(29, 5, 1, 0),(30, 5, 1, 0),
    (31, 5, 1, 0),(32, 5, 1, 0),(33, 5, 1, 0),(34, 5, 1, 0),(35, 5, 1, 0),
    (36, 5, 1, 0),(37, 5, 1, 0),(38, 5, 1, 0),(39, 5, 1, 0),(40, 5, 1, 0),
    (41, 5, 1, 0),(42, 5, 1, 0),(43, 5, 1, 0),(44, 5, 1, 0),(45, 5, 1, 0),
    (46, 5, 1, 0),(47, 5, 1, 0),(48, 5, 1, 0),(49, 5, 1, 0),(50, 5, 1, 0),
    (51, 5, 1, 0),(52, 5, 1, 0),(53, 5, 1, 0),(54, 5, 1, 0),(55, 5, 1, 0),
    (56, 5, 1, 0),(57, 5, 1, 0),(58, 5, 1, 0),(59, 5, 1, 0),(60, 5, 1, 1500),
    (61, 5, 1, 0),(62, 5, 1, 0),(63, 5, 1, 0),(64, 5, 1, 0),(65, 5, 1, 0),
    (66, 5, 1, 0),(67, 5, 1, 0),(68, 5, 1, 0),(69, 5, 1, 0),(70, 5, 1, 0),
    (71, 5, 1, 0),(72, 5, 1, 0),(73, 5, 1, 0),(74, 5, 1, 0),(75, 5, 1, 0),
    (76, 25, 5, 0),(77, 25, 5, 0),(78, 25, 5, 0),(79, 25, 5, 0),(80, 25, 5, 0),
    (81, 25, 5, 0),(82, 25, 5, 0),(83, 25, 5, 0),(84, 25, 5, 0),(85, 25, 5, 0),
    (86, 25, 5, 0),(87, 25, 5, 0),(88, 25, 5, 0),(89, 25, 5, 0),(90, 25, 5, 0),
    (91, 25, 5, 0),(92, 25, 5, 0),(93, 25, 5, 0),(94, 25, 5, 0),(95, 25, 5, 0),
    (96, 25, 5, 0),(97, 25, 5, 0),(98, 25, 5, 0),(99, 25, 5, 0),(100, 25, 5, 0),
    (101, 25, 5, 0),(102, 25, 5, 0),(103, 25, 5, 0),(104, 25, 5, 0),(105, 25, 5, 0),
    (106, 25, 5, 0),(107, 25, 5, 0),(108, 25, 5, 0),(109, 25, 5, 0),(110, 25, 5, 0),
    (111, 25, 5, 0),(112, 25, 5, 0),(113, 25, 5, 0),(114, 25, 5, 0),(115, 25, 5, 0),
    (116, 25, 5, 0),(117, 25, 5, 0),(118, 25, 5, 0),(119, 25, 5, 0),(120, 25, 5, 1500),
    (121, 25, 5, 0),(122, 25, 5, 0),(123, 25, 5, 0),(124, 25, 5, 0),(125, 25, 5, 0),
    (126, 25, 5, 0),(127, 25, 5, 0),(128, 25, 5, 0),(129, 25, 5, 0),(130, 25, 5, 0),
    (131, 25, 5, 0),(132, 25, 5, 0),(133, 25, 5, 0),(134, 25, 5, 0),(135, 25, 5, 0),
    (136, 25, 5, 0),(137, 25, 5, 0),(138, 25, 5, 0),(139, 25, 5, 0),(140, 25, 5, 0),
    (141, 25, 5, 0),(142, 25, 5, 0),(143, 25, 5, 0),(144, 25, 5, 0),(145, 50, 10, 0),
    (146, 50, 10, 0),(147, 50, 10, 0),(148, 50, 10, 0),(149, 50, 10, 0),
    (150, 50, 10, 0),(151, 50, 10, 0),(152, 50, 10, 0),(153, 50, 10, 0),(154, 50, 10, 0),
    (155, 50, 10, 0),(156, 50, 10, 0),(157, 50, 10, 0),(158, 50, 10, 0),(159, 50, 10, 0),
    (160, 50, 10, 0),(161, 50, 10, 0),(162, 50, 10, 0),(163, 50, 10, 0),(164, 50, 10, 0),
    (165, 50, 10, 0),(166, 50, 10, 0),(167, 50, 10, 0),(168, 50, 10, 0),(169, 50, 10, 0),
    (170, 50, 10, 0),(171, 50, 10, 0),(172, 50, 10, 0),(173, 50, 10, 0),(174, 50, 10, 0),
    (175, 50, 10, 0),(176, 50, 10, 0),(177, 50, 10, 0),(178, 50, 10, 0),(179, 50, 10, 0),
    (180, 50, 10, 2000),(181, 50, 10, 0),(182, 50, 10, 0),(183, 50, 10, 0),(184, 50, 10, 0),
    (185, 50, 10, 0),(186, 50, 10, 0),(187, 50, 10, 0),(188, 50, 10, 0),(189, 50, 10, 0),
    (190, 50, 10, 0),(191, 50, 10, 0),(192, 50, 10, 0),(193, 50, 10, 0),(194, 50, 10, 0),
    (195, 50, 10, 0),(196, 50, 10, 0),(197, 50, 10, 0),(198, 50, 10, 0),(199, 50, 10, 0),
    (200, 50, 10, 0),(201, 50, 10, 0),(202, 50, 10, 0),(203, 50, 10, 0),(204, 50, 10, 0),
    (205, 50, 10, 0),(206, 50, 10, 0),(207, 50, 10, 0),(208, 50, 10, 0),(209, 50, 10, 0),
    (210, 50, 10, 0),(211, 50, 10, 0),(212, 50, 10, 0),(213, 50, 10, 0),(214, 50, 10, 0),
    (215, 50, 10, 0),(216, 50, 10, 0),(217, 50, 10, 0),(218, 50, 10, 0),(219, 50, 10, 0),
    (220, 50, 10, 0),(221, 50, 10, 0),(222, 50, 10, 0),(223, 50, 10, 0),(224, 50, 10, 0),
    (225, 50, 10, 0),(226, 50, 10, 0),(227, 50, 10, 0),(228, 50, 10, 0),(229, 50, 10, 0),
    (230, 50, 10, 0),(231, 50, 10, 0),(232, 50, 10, 0),(233, 50, 10, 0),(234, 50, 10, 0),
    (235, 50, 10, 0),(236, 50, 10, 0),(237, 50, 10, 0),(238, 50, 10, 0),(239, 50, 10, 0),
    (240, 50, 10, 4000),(241, 60, 15, 0),(242, 60, 15, 0),(243, 60, 15, 0),(244, 60, 15, 0),
    (245, 60, 15, 0),(246, 60, 15, 0),(247, 60, 15, 0),(248, 60, 15, 0),(249, 60, 15, 0),
    (250, 60, 15, 0),(251, 60, 15, 0),(252, 60, 15, 0),(253, 60, 15, 0),(254, 60, 15, 0),
    (255, 60, 15, 0),(256, 60, 15, 0),(257, 60, 15, 0),(258, 60, 15, 0),(259, 60, 15, 0),
    (260, 60, 15, 0),(261, 60, 15, 0),(262, 60, 15, 0),(263, 60, 15, 0),(264, 60, 15, 0),
    (265, 60, 15, 0),(266, 60, 15, 0),(267, 60, 15, 0),(268, 60, 15, 0),(269, 60, 15, 0),
    (270, 60, 15, 0),(271, 80, 15, 0),(272, 80, 15, 0),(273, 80, 15, 0),(274, 80, 15, 0),
    (275, 80, 15, 0),(276, 80, 15, 0),(277, 80, 15, 0),(278, 80, 15, 0),(279, 80, 15, 0),
    (280, 80, 15, 0),(281, 80, 15, 0),(282, 80, 15, 0),(283, 80, 15, 0),(284, 80, 15, 0),
    (285, 80, 15, 0),(286, 80, 15, 0),(287, 80, 15, 0),(288, 80, 15, 0),(289, 80, 15, 0),
    (290, 80, 15, 0),(291, 80, 15, 0),(292, 80, 15, 0),(293, 80, 15, 0),(294, 80, 15, 0),
    (295, 80, 15, 0),(296, 80, 15, 0),(297, 80, 15, 0),(298, 80, 15, 0),(299, 80, 15, 0),
    (300, 80, 15, 8000),(301, 100, 25, 0),(302, 100, 25, 0),(303, 100, 25, 0),(304, 100, 25, 0),
    (305, 100, 25, 0),(306, 100, 25, 0),(307, 100, 25, 0),(308, 100, 25, 0),(309, 100, 25, 0),
    (310, 100, 25, 0),(311, 100, 25, 0),(312, 100, 25, 0),(313, 100, 25, 0),(314, 100, 25, 0),
    (315, 100, 25, 0),(316, 100, 25, 0),(317, 100, 25, 0),(318, 100, 25, 0),(319, 100, 25, 0),
    (320, 100, 25, 0),(321, 100, 25, 0),(322, 100, 25, 0),(323, 100, 25, 0),(324, 100, 25, 0),
    (325, 100, 25, 0),(326, 100, 25, 0),(327, 100, 25, 0),(328, 100, 25, 0),(329, 100, 25, 0),
    (330, 100, 25, 0),(331, 100, 30, 0),(332, 100, 30, 0),(333, 100, 30, 0),(334, 100, 30, 0),
    (335, 100, 30, 0),(336, 100, 30, 0),(337, 100, 30, 0),(338, 100, 30, 0),(339, 100, 30, 0),
    (340, 100, 30, 0),(341, 100, 35, 0),(342, 100, 35, 0),(343, 100, 35, 0),(344, 100, 35, 0),
    (345, 100, 35, 0),(346, 100, 35, 0),(347, 100, 35, 0),(348, 100, 35, 0),(349, 100, 35, 0),
    (350, 100, 35, 0),(351, 100, 40, 0),(352, 100, 40, 0),(353, 100, 40, 0),(354, 100, 40, 0),
    (355, 100, 40, 0),(356, 100, 40, 0),(357, 100, 40, 0),(358, 100, 40, 0),(359, 100, 40, 0),
    (360, 0, 0, 0),
]

_GANG_RAW = [
    (1, 5, 10, 0, 0),(2, 5, 10, 0, 0),(3, 5, 10, 0, 0),(4, 5, 10, 0, 0),(5, 5, 10, 0, 0),
    (6, 5, 10, 0, 0),(7, 5, 10, 0, 0),(8, 5, 10, 0, 0),(9, 5, 10, 0, 0),(10, 5, 10, 0, 0),
    (11, 5, 10, 0, 0),(12, 5, 10, 0, 0),(13, 5, 10, 0, 0),(14, 5, 10, 0, 0),(15, 5, 10, 0, 0),
    (16, 5, 10, 0, 0),(17, 5, 10, 0, 0),(18, 5, 10, 0, 0),(19, 5, 10, 0, 0),(20, 7, 14, 0, 0),
    (21, 7, 14, 0, 0),(22, 7, 14, 0, 0),(23, 7, 14, 0, 0),(24, 7, 14, 0, 0),(25, 7, 14, 0, 0),
    (26, 7, 14, 0, 0),(27, 7, 14, 0, 0),(28, 7, 14, 0, 0),(29, 7, 14, 0, 0),(30, 7, 14, 0, 0),
    (31, 7, 14, 0, 0),(32, 7, 14, 0, 0),(33, 7, 14, 0, 0),(34, 7, 14, 0, 0),(35, 7, 14, 0, 0),
    (36, 7, 14, 0, 0),(37, 7, 14, 0, 0),(38, 7, 14, 0, 0),(39, 9, 18, 0, 0),(40, 9, 18, 0, 0),
    (41, 9, 18, 0, 0),(42, 9, 18, 0, 0),(43, 9, 18, 0, 0),(44, 9, 18, 0, 0),(45, 9, 18, 0, 0),
    (46, 9, 18, 0, 0),(47, 9, 18, 0, 0),(48, 9, 18, 0, 0),(49, 9, 18, 0, 0),(50, 9, 18, 0, 0),
    (51, 9, 18, 0, 0),(52, 9, 18, 0, 0),(53, 9, 18, 0, 0),(54, 9, 18, 0, 0),(55, 9, 18, 0, 0),
    (56, 9, 18, 0, 0),(57, 9, 18, 0, 0),(58, 11, 22, 0, 0),(59, 11, 22, 0, 0),(60, 11, 22, 140, 140),
    (61, 11, 22, 0, 0),(62, 11, 22, 0, 0),(63, 11, 22, 0, 0),(64, 11, 22, 0, 0),(65, 11, 22, 0, 0),
    (66, 11, 22, 0, 0),(67, 11, 22, 0, 0),(68, 11, 22, 0, 0),(69, 11, 22, 0, 0),(70, 11, 22, 0, 0),
    (71, 11, 22, 0, 0),(72, 11, 22, 0, 0),(73, 11, 22, 0, 0),(74, 11, 22, 0, 0),(75, 11, 22, 0, 0),
    (76, 11, 22, 0, 0),(77, 13, 26, 0, 0),(78, 13, 26, 0, 0),(79, 13, 26, 0, 0),(80, 13, 26, 0, 0),
    (81, 13, 26, 0, 0),(82, 13, 26, 0, 0),(83, 13, 26, 0, 0),(84, 13, 26, 0, 0),(85, 13, 26, 0, 0),
    (86, 13, 26, 0, 0),(87, 13, 26, 0, 0),(88, 13, 26, 0, 0),(89, 13, 26, 0, 0),(90, 13, 26, 0, 0),
    (91, 13, 26, 0, 0),(92, 13, 26, 0, 0),(93, 13, 26, 0, 0),(94, 13, 26, 0, 0),(95, 13, 26, 0, 0),
    (96, 15, 30, 0, 0),(97, 15, 30, 0, 0),(98, 15, 30, 0, 0),(99, 15, 30, 0, 0),(100, 15, 30, 0, 0),
    (101, 15, 30, 0, 0),(102, 15, 30, 0, 0),(103, 15, 30, 0, 0),(104, 15, 30, 0, 0),(105, 15, 30, 0, 0),
    (106, 15, 30, 0, 0),(107, 15, 30, 0, 0),(108, 15, 30, 0, 0),(109, 15, 30, 0, 0),(110, 15, 30, 0, 0),
    (111, 15, 30, 0, 0),(112, 15, 30, 0, 0),(113, 15, 30, 0, 0),(114, 15, 30, 0, 0),(115, 17, 34, 0, 0),
    (116, 17, 34, 0, 0),(117, 17, 34, 0, 0),(118, 17, 34, 0, 0),(119, 17, 34, 0, 0),(120, 17, 34, 280, 280),
    (121, 20, 40, 0, 0),(122, 20, 40, 0, 0),(123, 20, 40, 0, 0),(124, 20, 40, 0, 0),(125, 20, 40, 0, 0),
    (126, 20, 40, 0, 0),(127, 20, 40, 0, 0),(128, 20, 40, 0, 0),(129, 20, 40, 0, 0),(130, 20, 40, 0, 0),
    (131, 20, 50, 0, 0),(132, 20, 50, 0, 0),(133, 20, 50, 0, 0),(134, 20, 50, 0, 0),(135, 20, 50, 0, 0),
    (136, 20, 50, 0, 0),(137, 20, 50, 0, 0),(138, 20, 50, 0, 0),(139, 20, 50, 0, 0),(140, 20, 60, 0, 0),
    (141, 20, 60, 0, 0),(142, 20, 60, 0, 0),(143, 20, 60, 0, 0),(144, 20, 60, 0, 0),(145, 20, 60, 0, 0),
    (146, 20, 60, 0, 0),(147, 20, 60, 0, 0),(148, 20, 60, 0, 0),(149, 20, 60, 0, 0),(150, 0, 0, 0, 0),
]

# 转换为统一字典格式（与原 _build_data 输出一致）
STONE_DATA = [{"lv": r[0], "jf": r[1], "stage": bool(r[2] > 0), "stage_jf": r[2]} for r in _STONE_RAW]
XUAN_DATA = [{"lv": r[0], "jf": r[1], "item": r[2], "stage": bool(r[3] > 0), "stage_jf": r[3]} for r in _XUAN_RAW]
GANG_DATA = [{"lv": r[0], "jf": r[1], "item": r[2], "stage": bool(r[3] > 0), "stage_jf": r[3], "stage_item": r[4]} for r in _GANG_RAW]
del _STONE_RAW, _XUAN_RAW, _GANG_RAW

# 数据字典索引: lv -> data dict
STONE_BY_LVL = {d["lv"]: d for d in STONE_DATA}
XUAN_BY_LVL = {d["lv"]: d for d in XUAN_DATA}
GANG_BY_LVL = {d["lv"]: d for d in GANG_DATA}


# ============================================================
# 三、工具页面
# ============================================================

class ToolEPage(ctk.CTkFrame):
    """圣石养成计算器界面"""

    def __init__(self, parent, colors: dict):
        super().__init__(parent, fg_color="transparent")
        self.colors = colors
        self._build_ui()

    # ------------------------------------------------------------------
    # UI 构建
    # ------------------------------------------------------------------

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        # 标题
        ctk.CTkLabel(scroll, text="💎 圣石养成计算器",
                    font=ctk.CTkFont(size=22, weight="bold"),
                    text_color="#ffffff", anchor="w"
                    ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(scroll, text="QQ华夏手游 · 11件装备 × 3槽位 · 精确计算无随机",
                    font=ctk.CTkFont(size=12), text_color=self.colors["text_dim"], anchor="w"
                    ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # 标签页切换
        tab_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["📊 根据材料算可达等级", "🎯 根据目标算所需材料"],
            height=34, font=ctk.CTkFont(size=13),
            selected_color=self.colors["nav_active"],
            unselected_color="#0f0f1a",
            command=self._on_tab_change,
        )
        self.tab_seg.pack(fill="x")
        self.tab_seg.set("📊 根据材料算可达等级")

        # Tab 1
        self.tab1 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self._build_tab1()

        # Tab 2（不 grid）
        self.tab2 = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        self._build_tab2()

        # 说明区域
        info_card = ctk.CTkFrame(scroll, fg_color="#1a1a2e", corner_radius=12)
        info_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(info_inner, text="📖 养成说明", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").pack(fill="x", pady=(0, 8))

        rules = [
            "· 11件装备(10种部位)，每件3个槽位：圣石/玄石/罡石",
            "· 圣石最高120级 | 玄石最高360级 | 罡石最高150级",
            "· 升级完全确定性：每级消耗积分 + 可能的道具",
            "· 升阶卡口：到特定等级需先消耗升阶材料才能继续",
            "· 玄石升级需消耗同系圣石道具；腕部栏3为气海系(渊泽罡石)",
        ]
        for r in rules:
            ctk.CTkLabel(info_inner, text=r, font=ctk.CTkFont(size=12),
                         text_color=self.colors["text_dim"], anchor="w").pack(fill="x", pady=1)

    # ------------------------------------------------------------------
    # Tab 1: 根据材料算可达等级
    # ------------------------------------------------------------------

    def _build_tab1(self):
        inner = ctk.CTkFrame(self.tab1, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        row = 0

        # 部位选择
        ctk.CTkLabel(inner, text="选择部位", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 6))
        row += 1

        self.t1_part = ctk.CTkOptionMenu(
            inner, values=list(PART_CONFIG.keys()),
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_part_change_t1,
        )
        self.t1_part.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t1_part.set("背部")
        row += 1

        # 属性系选择（头部/胸部/颈部显示）
        self.t1_attr_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t1_attr_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        row += 1
        ctk.CTkLabel(self.t1_attr_frame, text="属性系选择",
                     font=ctk.CTkFont(size=13), text_color=self.colors["text_dim"],
                     anchor="w").pack(side="left", padx=(0, 8))
        self.t1_attr_btns = {}
        for attr in ["金刚系", "灵柔系"]:
            btn = ctk.CTkRadioButton(self.t1_attr_frame, text=attr, value=False,
                                     font=ctk.CTkFont(size=12),
                                     command=lambda a=attr: self._set_attr_t1(a))
            btn.pack(side="left", padx=(0, 12))
            self.t1_attr_btns[attr] = btn
        self.t1_selected_attr = "金刚系"  # 默认
        self._hide_attr_t1()  # 背部固定气海，隐藏选择
        row += 1

        # 槽位选择
        ctk.CTkLabel(inner, text="槽位类型", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(6, 6))
        row += 1
        self.t1_slot = ctk.CTkOptionMenu(
            inner, values=["圣石(栏位1)", "玄石(栏位2)", "罡石(栏位3)"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_slot_change_t1,
        )
        self.t1_slot.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t1_slot.set("圣石(栏位1)")
        row += 1

        # 当前等级
        ctk.CTkLabel(inner, text="当前等级", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(6, 6))
        row += 1
        ctk.CTkLabel(inner, text=f"(上限{SLOT_LIMITS['圣石(栏位1)']}级)",
                     font=ctk.CTkFont(size=11), text_color=self.colors["text_dim"]).grid(
            row=row, column=0, columnspan=2, sticky="w")
        row += 1
        self.t1_cur_lv = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t1_cur_lv.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t1_cur_lv.insert(0, "0")
        row += 1

        # 拥有材料
        ctk.CTkLabel(inner, text="拥有材料", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w"
                     ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 6))
        row += 1

        self.t1_mat_jf_label = ctk.CTkLabel(inner, text="积分:", font=ctk.CTkFont(size=12),
                                            text_color=self.colors["text_dim"])
        self.t1_mat_jf_label.grid(row=row, column=0, sticky="w", padx=(0, 8), pady=(3, 2))
        self.t1_jf_entry = ctk.CTkEntry(inner, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_jf_entry.grid(row=row+1, column=0, sticky="ew", padx=(0, 8), pady=(0, 4))
        row += 2

        # 道具输入（动态标签）
        self.t1_item_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t1_item_frame.grid(row=row, column=0, columnspan=2, sticky="ew")
        self.t1_item_label = ctk.CTkLabel(self.t1_item_frame, text="道具:", font=ctk.CTkFont(size=12),
                                          text_color=self.colors["text_dim"])
        self.t1_item_label.pack(side="left", padx=(0, 8))
        self.t1_item_entry = ctk.CTkEntry(self.t1_item_frame, placeholder_text="留空=无限", height=32, corner_radius=6)
        self.t1_item_entry.pack(side="left", fill="x", expand=True)
        self._update_item_name_t1()
        row += 1

        # 计算按钮
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(12, 8))
        row += 1
        ctk.CTkButton(btn_row, text="▶ 计算可达到的等级",
                      font=ctk.CTkFont(size=14, weight="bold"), height=38,
                      fg_color="#e94560", hover_color="#c73650",
                      command=self._calc_by_materials).pack(fill="x")

        # 结果区
        self.t1_result = ctk.CTkTextbox(inner, height=240, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
                                        wrap="word")
        self.t1_result.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.t1_result.insert("1.0", "请输入参数后点击计算...")
        self.t1_result.configure(state="disabled")

    # ------------------------------------------------------------------
    # Tab 2: 根据目标算所需材料
    # ------------------------------------------------------------------

    def _build_tab2(self):
        inner = ctk.CTkFrame(self.tab2, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=18)
        inner.grid_columnconfigure((0, 1), weight=1)

        row = 0

        # 部位选择
        ctk.CTkLabel(inner, text="选择部位", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(0, 6)); row+=1
        self.t2_part = ctk.CTkOptionMenu(
            inner, values=list(PART_CONFIG.keys()), height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_part_change_t2,
        )
        self.t2_part.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.t2_part.set("背部"); row+=1

        # 属性系选择
        self.t2_attr_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.t2_attr_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8)); row+=1
        ctk.CTkLabel(self.t2_attr_frame, text="属性系选择", font=ctk.CTkFont(size=13),
                     text_color=self.colors["text_dim"], anchor="w").pack(side="left", padx=(0, 8))
        self.t2_attr_btns = {}
        for attr in ["金刚系", "灵柔系"]:
            btn = ctk.CTkRadioButton(self.t2_attr_frame, text=attr, value=False,
                                     font=ctk.CTkFont(size=12),
                                     command=lambda a=attr: self._set_attr_t2(a))
            btn.pack(side="left", padx=(0, 12))
            self.t2_attr_btns[attr] = btn
        self.t2_selected_attr = "金刚系"
        self._hide_attr_t2(); row+=1

        # 槽位选择
        ctk.CTkLabel(inner, text="槽位类型", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(6, 6)); row+=1
        self.t2_slot = ctk.CTkOptionMenu(
            inner, values=["圣石(栏位1)", "玄石(栏位2)", "罡石(栏位3)"],
            height=32, corner_radius=6,
            fg_color="#0f3460", button_color="#0f3460", button_hover_color="#16213e",
            command=self._on_slot_change_t2,
        )
        self.t2_slot.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.t2_slot.set("圣石(栏位1)"); row+=1

        # 起始/目标等级
        ctk.CTkLabel(inner, text="等级范围", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff", anchor="w").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(6, 6)); row+=1

        ctk.CTkLabel(inner, text="起始等级", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=0, sticky="w", padx=(0, 8))
        ctk.CTkLabel(inner, text="目标等级", font=ctk.CTkFont(size=12),
                     text_color=self.colors["text_dim"]).grid(row=row, column=1, sticky="w", padx=(8, 0)); row+=1
        self.t2_start_lv = ctk.CTkEntry(inner, placeholder_text="0", height=32, corner_radius=6)
        self.t2_target_lv = ctk.CTkEntry(inner, placeholder_text="120", height=32, corner_radius=6)
        self.t2_start_lv.grid(row=row, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.t2_target_lv.grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.t2_start_lv.insert(0, "0")
        self.t2_target_lv.insert(0, "120"); row+=1

        # 计算按钮
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(12, 8)); row+=1
        ctk.CTkButton(btn_row, text="▶ 计算所需材料",
                      font=ctk.CTkFont(size=14, weight="bold"), height=38,
                      fg_color="#e94560", hover_color="#c73650",
                      command=self._calc_for_target).pack(fill="x")

        # 结果区
        self.t2_result = ctk.CTkTextbox(inner, height=300, corner_radius=8,
                                        fg_color="#0f0f1a", font=ctk.CTkFont(size=13),
                                        wrap="word")
        self.t2_result.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.t2_result.insert("1.0", "请输入参数后点击计算...")
        self.t2_result.configure(state="disabled")

    # ------------------------------------------------------------------
    # 交互回调
    # ------------------------------------------------------------------

    def _on_tab_change(self, val):
        if "根据材料" in str(val):
            self.tab1.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            try: self.tab2.grid_forget()
            except: pass
        else:
            self.tab2.grid(row=3, column=0, sticky="ew", pady=(0, 15))
            try: self.tab1.grid_forget()
            except: pass

    def _on_part_change_t1(self, val):
        part = str(val)
        cfg = PART_CONFIG.get(part, {})
        slot1 = cfg.get("slot1系", "")
        if "可选" in slot1:
            self._show_attr_t1()
        else:
            self._hide_attr_t1()
        self._update_item_name_t1()
        self._update_limit_label_t1()

    def _on_part_change_t2(self, val):
        part = str(val)
        cfg = PART_CONFIG.get(part, {})
        slot1 = cfg.get("slot1系", "")
        if "可选" in slot1:
            self._show_attr_t2()
        else:
            self._hide_attr_t2()
        self._update_limit_label_t2()

    def _on_slot_change_t1(self, val):
        self._update_item_name_t1()
        self._update_limit_label_t1()

    def _on_slot_change_t2(self, val):
        self._update_limit_label_t2()

    def _set_attr_t1(self, attr):
        self.t1_selected_attr = attr
        self.t1_attr_btns[attr].configure(value=True)
        for k, v in self.t1_attr_btns.items():
            if k != attr:
                v.configure(value=False)

    def _set_attr_t2(self, attr):
        self.t2_selected_attr = attr
        self.t2_attr_btns[attr].configure(value=True)
        for k, v in self.t2_attr_btns.items():
            if k != attr:
                v.configure(value=False)

    def _show_attr_t1(self):
        self.t1_attr_frame.pack_configure(pady=(0, 8))
        self.t1_attr_frame.grid()

    def _hide_attr_t1(self):
        try:
            self.t1_attr_frame.grid_forget()
        except Exception:
            pass

    def _show_attr_t2(self):
        self.t2_attr_frame.pack_configure(pady=(0, 8))
        self.t2_attr_frame.grid()

    def _hide_attr_t2(self):
        try:
            self.t2_attr_frame.grid_forget()
        except Exception:
            pass

    def _resolve_attr(self, part, slot_key):
        """解析当前部位的属性系"""
        cfg = PART_CONFIG.get(part, {})
        series = cfg.get(slot_key, "")
        if "可选" in series:
            return "金刚" if "金" in self.t1_selected_attr else "灵柔"
        elif "极意" in series or "(威霆)" in series:
            return "极意"
        elif "气海" in series or "(渊泽)" in series:
            return "气海"
        return "气海"

    def _update_item_name_t1(self):
        part = self.t1_part.get()
        slot = self.t1_slot.get()
        attr = self._resolve_attr(part, "slot1系" if "栏位1" in slot else "slot3系")
        item_name = SLOT_ITEM_NAMES.get((slot, attr), None)
        if item_name:
            self.t1_item_label.configure(text=f"{item_name}:")
            self.t1_item_frame.pack_configure(pady=(4, 0))
            self.t1_item_frame.grid()
        else:
            try: self.t1_item_frame.grid_forget()
            except: pass

    def _update_limit_label_t1(self):
        slot = self.t1_slot.get()
        limit = SLOT_LIMITS.get(slot, 99)
        # 更新当前等级提示（通过重新查找label）
        pass  # 静态显示即可，用户可看上方说明

    def _update_limit_label_t2(self):
        pass

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _parse_int(self, val: str, default: int) -> int:
        try: return int((val or "").strip() or str(default))
        except: return default

    def _parse_float_or_inf(self, val: str) -> float:
        v = (val or "").strip()
        if not v: return float("inf")
        try: return float(v)
        except: return float("inf")

    def _get_data_list(self, slot: str):
        if "圣石" in slot: return STONE_DATA
        if "玄石" in slot: return XUAN_DATA
        return GANG_DATA

    def _fmt(self, v) -> str:
        if isinstance(v, float) and v == float("inf"): return "∞"
        if isinstance(v, float): return f"{v:,.1f}"
        return f"{v:,}"

    def _show_result(self, tb: ctk.CTkTextbox, text: str):
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.insert("1.0", text)
        tb.configure(state="disabled")

    def _show_error(self, tb: ctk.CTkTextbox, msg: str):
        self._show_result(tb, f"⚠ {msg}")

    # ------------------------------------------------------------------
    # 模式一：根据材料计算可达等级
    # ------------------------------------------------------------------

    def _calc_by_materials(self):
        try:
            part = self.t1_part.get()
            slot = self.t1_slot.get()
            cur_lv = self._parse_int(self.t1_cur_lv.get(), 0)
            jf = self._parse_float_or_inf(self.t1_jf_entry.get())
            item_val = self._parse_float_or_inf(self.t1_item_entry.get()) if self._has_items(slot) else float("inf")

            max_lv = SLOT_LIMITS[slot]
            if cur_lv < 0 or cur_lv > max_lv:
                self._show_error(self.t1_result, f"当前等级需在 0 ~ {max_lv} 之间")
                return

            data_list = self._get_data_list(slot)
            data_map = self._get_data_map(slot)
            lv = cur_lv
            total_jf = 0.0
            total_item = 0.0
            steps = 0

            while lv < max_lv:
                next_lv = lv + 1
                entry = data_map.get(next_lv)
                if not entry:
                    break

                need_jf = entry.get("jf", 0)
                need_item = entry.get("item", 0)
                stage_jf = entry.get("stage_jf", 0)
                stage_item = entry.get("stage_item", 0)

                # 检查升阶
                if entry.get("stage") and stage_jf > 0:
                    if jf != float("inf") and jf < stage_jf:
                        break
                    if jf != float("inf"):
                        jf -= stage_jf
                        total_jf += stage_jf
                    if item_val != float("inf") and stage_item > 0 and item_val < stage_item:
                        break
                    if item_val != float("inf"):
                        item_val -= stage_item
                        total_item += stage_item

                # 正常升级
                cost_ok = True
                if need_jf > 0:
                    if jf != float("inf") and jf < need_jf:
                        cost_ok = False
                    elif jf != float("inf"):
                        jf -= need_jf
                        total_jf += need_jf

                if need_item > 0 and self._has_items(slot):
                    if item_val != float("inf") and item_val < need_item:
                        cost_ok = False
                    elif item_val != float("inf"):
                        item_val -= need_item
                        total_item += need_item

                if not cost_ok:
                    break

                lv = next_lv
                steps += 1

            # 输出结果
            attr = self._resolve_attr(part, "slot1系" if "栏位1" in slot else "slot3系")
            lines = []
            lines.append(f"━━━ 养成模拟结果 ━━━\n")
            lines.append(f"部位：{part} | 槽位：{slot}")
            if "可选" in PART_CONFIG.get(part, {}).get("slot1系", ""):
                lines.append(f"属性系：{self.t1_selected_attr.replace('系','')}系\n")
            else:
                lines.append(f"属性系：{attr}系\n")
            lines.append(f"▸ 可达等级：{lv}级 (上限 {max_lv})")
            lines.append(f"  从 {cur_lv}级 出发，共推进 {steps} 个等级\n")

            lines.append("━ 累计材料消耗 ━")
            lines.append(f"  积分: {self._fmt(total_jf)}")
            if self._has_items(slot):
                item_name = SLOT_ITEM_NAMES.get((slot, attr), "道具")
                lines.append(f"  {item_name}: {self._fmt(total_item)}")

            equip_count = PART_CONFIG.get(part, {}).get("count", 1)
            lines.append(f"\n(以上为单槽位值 × {equip_count}件装备)")

            # 剩余提示
            remain_lines = []
            if jf != float("inf") and jf > 0:
                remain_lines.append(f"  剩余积分: {self._fmt(jf)}")
            if item_val != float("inf") and item_val > 0 and self._has_items(slot):
                remain_lines.append(f"  剩余道具: {self._fmt(item_val)}")
            if remain_lines:
                old_text = "\n".join(lines) + "\n"
                lines_str = old_text + "\n" + "\n".join(remain_lines) + "\n"
            else:
                lines_str = "\n".join(lines) + "\n"

            self._show_result(self.t1_result, lines_str)

        except Exception as ex:
            self._show_error(self.t1_result, f"计算出错: {ex}")

    # ------------------------------------------------------------------
    # 模式二：根据目标计算所需材料
    # ------------------------------------------------------------------

    def _calc_for_target(self):
        try:
            part = self.t2_part.get()
            slot = self.t2_slot.get()
            start_lv = self._parse_int(self.t2_start_lv.get(), 0)
            target_lv = self._parse_int(self.t2_target_lv.get(),
                                         SLOT_LIMITS[slot])

            max_lv = SLOT_LIMITS[slot]
            if start_lv < 0 or start_lv > max_lv:
                self._show_error(self.t2_result, f"起始等级需在 0 ~ {max_lv}"); return
            if target_lv < 0 or target_lv > max_lv:
                self._show_error(self.t2_result, f"目标等级需在 0 ~ {max_lv}"); return
            if target_lv <= start_lv:
                self._show_error(self.t2_result, "目标必须大于起始等级"); return

            data_map = self._get_data_map(slot)
            total_jf = 0
            total_item = 0
            stages_hit = []

            for lv in range(start_lv + 1, target_lv + 1):
                entry = data_map.get(lv)
                if not entry:
                    continue
                total_jf += entry.get("jf", 0)
                total_item += entry.get("item", 0)
                if entry.get("stage"):
                    sj = entry.get("stage_jf", 0)
                    si = entry.get("stage_item", 0)
                    total_jf += sj
                    total_item += si
                    stages_hit.append(lv)

            attr = self._resolve_attr(part, "slot1系" if "栏位1" in slot else "slot3系")
            equip_count = PART_CONFIG.get(part, {}).get("count", 1)

            lines = []
            lines.append(f"━━━ 材料需求汇总 ━━━\n")
            lines.append(f"部位：{part} | 槽位：{slot}")
            if "可选" in PART_CONFIG.get(part, {}).get("slot1系", ""):
                lines.append(f"属性系：{self.t1_selected_attr.replace('系','')}系\n")
            else:
                lines.append(f"属性系：{attr}系\n")
            lines.append(f"范围：{start_lv}级 → {target_lv}级 (跨{target_lv-start_lv}级)\n")

            lines.append("━ 所需材料 ━")
            lines.append(f"  积分总计: {total_jf:,}")
            if self._has_items(slot):
                item_name = SLOT_ITEM_NAMES.get((slot, attr), "道具")
                lines.append(f"  {item_name}总计: {total_item:,}")

            lines.append(f"\n━ 升阶节点 ━")
            if stages_hit:
                for sv in stages_hit:
                    e = data_map[sv]
                    sj = e.get("stage_jf", 0)
                    si = e.get("stage_item", 0)
                    detail = f"  Lv.{sv}: "
                    parts = []
                    if sj > 0:
                        parts.append(f"+{sj}积分")
                    if si > 0:
                        parts.append(f"+{si}{item_name if self._has_items(slot) else '道具'}")
                    detail += " & ".join(parts)
                    lines.append(detail)
            else:
                lines.append("  无升阶节点")

            lines.append(f"\n(以上为单槽位值 × {equip_count}件装备)")

            self._show_result(self.t2_result, "\n".join(lines) + "\n")

        except Exception as ex:
            self._show_error(self.t2_result, f"计算出错: {ex}")

    def _has_items(self, slot: str) -> bool:
        """该槽位是否消耗道具"""
        return "圣石" not in slot

    def _get_data_map(self, slot: str):
        if "圣石" in slot: return STONE_BY_LVL
        if "玄石" in slot: return XUAN_BY_LVL
        return GANG_BY_LVL
