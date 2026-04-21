#!/usr/bin/env python3
"""
蜀山剑侠传 - 功能测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.player import Player
from game.artifact import ArtifactManager
from game.skills import SkillManager
from game.world import WorldMap, ExplorationSystem
from game.quest import QuestManager
from game.crafting import CraftingManager, Inventory

def test_all():
    """测试所有系统"""
    
    print("=" * 60)
    print("《蜀山剑侠传》功能测试")
    print("=" * 60)
    
    # 1. 测试功法系统
    print("\n【1. 功法系统测试】")
    print("-" * 60)
    
    skills = SkillManager.list_all()
    print(f"✅ 加载功法：{len(skills)} 种")
    
    # 显示几个功法
    for i, (name, skill) in enumerate(list(skills.items())[:3]):
        print(f"   - {name}（{skill['type']}，{skill['quality']}）")
    
    # 创建玩家并学习功法
    player = Player("测试角色")
    
    # 学习功法
    result = player.learn_skill("峨眉剑法")
    print(f"\n学习功法：{result}")
    
    result = player.learn_skill("太清一气诀")
    print(f"设置主修：{result}")
    
    # 测试修炼加成
    base_result = player.cultivate("打坐")
    print(f"修炼效果：{base_result['message']}")
    print(f"功法加成：{player.get_cultivation_bonus():.1%}")
    
    # 2. 测试地图探索系统
    print("\n【2. 地图探索系统测试】")
    print("-" * 60)
    
    world_map = WorldMap()
    locations = world_map.get_all_locations()
    print(f"✅ 加载地图：{len(locations)} 个地点")
    
    # 显示区域
    regions = world_map.get_regions()
    for region, locs in regions.items():
        print(f"   - {region}：{len(locs)} 个地点")
    
    # 测试移动
    current = player.location
    print(f"\n当前位置：{current}")
    
    # 探索当前地点
    exploration = ExplorationSystem(player)
    event = exploration.explore()
    print(f"探索事件：{event['type']}")
    if event.get('description'):
        print(f"   描述：{event['description']}")
    
    # 3. 测试任务系统
    print("\n【3. 任务系统测试】")
    print("-" * 60)
    
    quest_manager = QuestManager()
    quests = quest_manager.get_all_quests()
    print(f"✅ 加载任务：{len(quests)} 个")
    
    # 显示任务类型
    quest_types = {}
    for q in quests.values():
        t = q['type']
        quest_types[t] = quest_types.get(t, 0) + 1
    
    for t, count in quest_types.items():
        print(f"   - {t}：{count} 个")
    
    # 接取任务
    player.init_quest_manager()
    result = player.accept_quest("初入蜀山")
    print(f"\n接取任务：{result}")
    
    # 显示进行中任务
    active = player.get_active_quests()
    if active:
        print(f"进行中任务：{len(active)} 个")
    
    # 4. 测试炼丹炼器系统
    print("\n【4. 炼丹炼器系统测试】")
    print("-" * 60)
    
    crafting = CraftingManager()
    recipes = crafting.get_all_recipes()
    materials = crafting.get_all_materials()
    
    print(f"✅ 加载配方：{len(recipes)} 种")
    print(f"✅ 加载材料：{len(materials)} 种")
    
    # 显示配方类型
    pill_recipes = [r for r in recipes.values() if r['type'] == '丹药']
    artifact_recipes = [r for r in recipes.values() if r['type'] == '法宝']
    print(f"   - 丹药配方：{len(pill_recipes)} 种")
    print(f"   - 法宝配方：{len(artifact_recipes)} 种")
    
    # 测试背包
    inventory = Inventory()
    inventory.add_material("玄铁", 10)
    inventory.add_material("灵参", 5)
    print(f"\n添加材料：玄铁 x10，灵参 x5")
    print(f"背包材料：{len(inventory.materials)} 种")
    
    # 测试炼丹
    player.inventory = inventory
    player.realm = "筑基期"
    player.cultivation = 10000
    
    result = crafting.craft_pill(player, "疗伤丹")
    print(f"炼制丹药：{result['message']}")
    
    # 5. 整合测试
    print("\n【5. 整合测试】")
    print("-" * 60)
    
    # 保存角色
    player.save()
    print("✅ 存档保存成功")
    
    # 读取角色
    loaded = Player.load()
    print(f"✅ 存档读取成功：{loaded.name}")
    
    print("\n" + "=" * 60)
    print("所有功能测试完成！")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        test_all()
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
