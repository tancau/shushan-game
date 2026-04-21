#!/usr/bin/env python3
"""
蜀山剑侠传 - 成就系统测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.player import Player
from game.achievement import AchievementManager, AchievementCategory, AchievementRarity

def test_achievement_data():
    """测试成就数据加载"""
    print("\n=== 测试成就数据 ===")
    
    # 使用绝对路径
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'achievements.json')
    am = AchievementManager(data_path)
    
    # 检查成就数量
    assert len(am.achievements) >= 50, f"成就数量不足: {len(am.achievements)}"
    assert len(am.titles) >= 30, f"称号数量不足: {len(am.titles)}"
    
    print(f"✓ 总成就数: {len(am.achievements)}")
    print(f"✓ 总称号数: {len(am.titles)}")
    
    # 检查分类
    for cat in AchievementCategory:
        count = len(am.get_achievements_by_category(cat))
        print(f"✓ {cat.value}: {count} 个成就")
    
    # 检查稀有度
    for rar in AchievementRarity:
        count = len(am.get_achievements_by_rarity(rar))
        print(f"✓ {rar.value}: {count} 个成就")
    
    return True

def test_achievement_conditions():
    """测试成就条件检查"""
    print("\n=== 测试成就条件 ===")
    
    am = AchievementManager('data/achievements.json')
    
    # 测试境界条件
    player_data = {"realm": "金丹期", "cultivation": 10000, "spirit_stones": 1000}
    
    # 检查各个成就条件类型
    from game.achievement import AchievementCondition
    
    cond = AchievementCondition("realm_reach", "", 3, "达到金丹期")
    assert cond.check(player_data), "境界条件检查失败"
    print("✓ 境界条件检查通过")
    
    cond = AchievementCondition("cultivation_reach", "", 10000, "修为达到10000")
    assert cond.check(player_data), "修为条件检查失败"
    print("✓ 修为条件检查通过")
    
    cond = AchievementCondition("spirit_stones_reach", "", 1000, "灵石达到1000")
    assert cond.check(player_data), "灵石条件检查失败"
    print("✓ 灵石条件检查通过")
    
    return True

def test_player_integration():
    """测试玩家集成"""
    print("\n=== 测试玩家集成 ===")
    
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'achievements.json')
    
    # 创建玩家
    player = Player("测试玩家")
    player.init_achievement_manager(data_path)
    
    assert player.achievement_manager is not None, "成就管理器未初始化"
    print("✓ 成就管理器初始化成功")
    
    # 模拟玩家进度
    player.cultivation = 100000
    player.spirit_stones = 50000
    player.quest_kills['any'] = 100
    player.join_sect("峨眉派")
    
    # 检查成就
    newly_completed = player.check_achievements()
    print(f"✓ 检查成就: 完成 {len(newly_completed)} 个")
    
    # 获取概要
    summary = player.achievement_manager.get_progress_summary(player)
    print(f"✓ 成就进度: {summary['completed']}/{summary['total']}")
    
    # 领取奖励
    if newly_completed:
        ach_id = newly_completed[0]['achievement_id']
        result = player.claim_achievement_reward(ach_id)
        print(f"✓ 领取奖励: {result.get('message', '成功')}")
    
    # 测试称号
    unlocked_titles = player.get_unlocked_titles()
    print(f"✓ 已解锁称号: {len(unlocked_titles)} 个")
    
    if unlocked_titles:
        title_id = unlocked_titles[0]['id']
        result = player.set_title(title_id)
        print(f"✓ 设置称号: {result.get('message', '成功')}")
    
    return True

def test_save_load():
    """测试保存/加载"""
    print("\n=== 测试保存/加载 ===")
    
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'achievements.json')
    
    # 创建并保存
    player = Player("存档测试")
    player.init_achievement_manager(data_path)
    player.cultivation = 50000
    player.quest_kills['any'] = 50
    player.check_achievements()
    
    # 保存
    player.save(99)
    print("✓ 存档保存成功")
    
    # 加载
    loaded = Player.load(99)
    loaded.init_achievement_manager('data/achievements.json')
    
    assert len(loaded.completed_achievements) == len(player.completed_achievements), "成就数据丢失"
    print(f"✓ 存档加载成功: {len(loaded.completed_achievements)} 个成就")
    
    # 清理
    save_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'save', 'save_99.json')
    if os.path.exists(save_file):
        os.remove(save_file)
        print("✓ 测试存档已清理")
    
    return True

def test_title_system():
    """测试称号系统"""
    print("\n=== 测试称号系统 ===")
    
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'achievements.json')
    am = AchievementManager(data_path)
    
    # 检查称号加成
    for title_id, title in list(am.titles.items())[:5]:
        bonus = title.get_bonus_text()
        print(f"✓ {title.name}: {bonus}")
    
    return True

def main():
    """运行所有测试"""
    print("=" * 50)
    print("蜀山剑侠传 - 成就系统测试")
    print("=" * 50)
    
    tests = [
        ("成就数据", test_achievement_data),
        ("成就条件", test_achievement_conditions),
        ("玩家集成", test_player_integration),
        ("保存/加载", test_save_load),
        ("称号系统", test_title_system),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✓ {name}测试通过")
        except Exception as e:
            failed += 1
            print(f"\n✗ {name}测试失败: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
