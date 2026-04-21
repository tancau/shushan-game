#!/usr/bin/env python3
"""
蜀山剑侠传 - 快速功能测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("《蜀山剑侠传》功能测试")
print("=" * 60)

# 1. 测试功法系统
print("\n【1. 功法系统】")
try:
    from game.skills import SkillManager
    manager = SkillManager()
    manager.load_skills()
    print(f"✅ 功法加载成功")
    
    # 获取功法数量
    import json
    with open("data/skills.json", "r", encoding="utf-8") as f:
        skills_data = json.load(f)
    print(f"   功法数量：{len(skills_data)} 种")
except Exception as e:
    print(f"❌ 失败：{e}")

# 2. 测试地图系统
print("\n【2. 地图探索系统】")
try:
    from game.world import WorldMap
    world = WorldMap()
    locations = world.get_all_locations()
    print(f"✅ 地图加载成功")
    print(f"   地点数量：{len(locations)} 个")
except Exception as e:
    print(f"❌ 失败：{e}")

# 3. 测试任务系统
print("\n【3. 任务系统】")
try:
    from game.quest import QuestManager
    qm = QuestManager()
    quests = qm.get_all_quests()
    print(f"✅ 任务加载成功")
    print(f"   任务数量：{len(quests)} 个")
except Exception as e:
    print(f"❌ 失败：{e}")

# 4. 测试炼丹炼器系统
print("\n【4. 炼丹炼器系统】")
try:
    from game.crafting import CraftingManager
    cm = CraftingManager()
    recipes = cm.get_all_recipes()
    materials = cm.get_all_materials()
    print(f"✅ 炼丹炼器加载成功")
    print(f"   配方数量：{len(recipes)} 种")
    print(f"   材料数量：{len(materials)} 种")
except Exception as e:
    print(f"❌ 失败：{e}")

# 5. 测试玩家系统整合
print("\n【5. 玩家系统整合】")
try:
    from game.player import Player
    player = Player("测试")
    
    # 测试修炼
    result = player.cultivate("吐纳")
    print(f"✅ 修炼系统：{result['message']}")
    
    # 测试存档
    player.save()
    loaded = Player.load()
    print(f"✅ 存档系统：角色 {loaded.name} 已保存和加载")
except Exception as e:
    print(f"❌ 失败：{e}")

print("\n" + "=" * 60)
print("功能测试完成！")
print("=" * 60)
