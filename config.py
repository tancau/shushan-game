#!/usr/bin/env python3
"""
蜀山剑侠传 - 游戏配置
"""

# 游戏信息
GAME_NAME = "蜀山剑侠传"
VERSION = "0.1.0"
AUTHOR = "初初 💎"

# 修炼境界配置
REALMS = {
    "练气期": {
        "level": 1,
        "cultivation_required": 0,
        "description": "感应天地灵气，初入修真",
        "unlock_features": ["基础法术"]
    },
    "筑基期": {
        "level": 2,
        "cultivation_required": 1000,
        "description": "铸就道基，稳固根基",
        "unlock_features": ["飞剑", "二级法宝"]
    },
    "金丹期": {
        "level": 3,
        "cultivation_required": 10000,
        "description": "凝聚金丹，法力大增",
        "unlock_features": ["剑光分化", "三级法宝"]
    },
    "元婴期": {
        "level": 4,
        "cultivation_required": 100000,
        "description": "元婴出窍，神识外放",
        "unlock_features": ["神识外放", "四级法宝"]
    },
    "化神期": {
        "level": 5,
        "cultivation_required": 1000000,
        "description": "元神化形，法宝炼化",
        "unlock_features": ["法宝炼化", "五级法宝"]
    },
    "合体期": {
        "level": 6,
        "cultivation_required": 10000000,
        "description": "身神合一，准备飞升",
        "unlock_features": ["破界准备"]
    },
    "渡劫期": {
        "level": 7,
        "cultivation_required": 100000000,
        "description": "渡天劫，飞升成仙",
        "unlock_features": ["飞升"]
    }
}

# 五行配置
ELEMENTS = {
    "金": {"克制": "木", "被克": "火", "特性": "锐利、穿透"},
    "木": {"克制": "土", "被克": "金", "特性": "生机、缠绕"},
    "水": {"克制": "火", "被克": "土", "特性": "柔韧、侵蚀"},
    "火": {"克制": "金", "被克": "水", "特性": "爆裂、灼烧"},
    "土": {"克制": "水", "被克": "木", "特性": "厚重、防御"}
}

# 门派配置
SECTS = {
    "峨眉派": {
        "type": "正道",
        "description": "正道领袖，飞剑第一",
        "bonus": {"飞剑威力": 1.2, "修炼速度": 1.1},
        "location": "峨眉山"
    },
    "青城派": {
        "type": "正道",
        "description": "剑术精妙，防御见长",
        "bonus": {"防御": 1.2, "剑术": 1.1},
        "location": "青城山"
    },
    "昆仑派": {
        "type": "正道",
        "description": "炼器圣地，法宝众多",
        "bonus": {"炼器": 1.3, "法宝契合": 1.1},
        "location": "昆仑山"
    },
    "血河教": {
        "type": "邪道",
        "description": "血河大法，速成但危险",
        "bonus": {"修炼速度": 1.5, "渡劫难度": 2.0},
        "location": "西域"
    }
}

# 初始属性
INITIAL_STATS = {
    "生命": 100,
    "真元": 100,
    "攻击": 10,
    "防御": 5,
    "速度": 10,
    "悟性": 50,  # 影响修炼和领悟
    "幸运": 50   # 影响奇遇和掉落
}

# 文件路径
SAVE_DIR = "save"
DATA_DIR = "data"

# 显示设置
DISPLAY_WIDTH = 60
