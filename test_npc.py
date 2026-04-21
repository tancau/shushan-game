#!/usr/bin/env python3
"""
蜀山剑侠传 - NPC 系统测试
"""

from game.npc import NPCManager, NPCType

def test_npc_system():
    """测试 NPC 系统"""
    print("=" * 60)
    print("蜀山剑侠传 - NPC 系统测试")
    print("=" * 60)
    
    # 初始化管理器（使用绝对路径）
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    npc_path = os.path.join(base_dir, 'data/npcs.json')
    shop_path = os.path.join(base_dir, 'data/shops.json')
    manager = NPCManager(npc_path, shop_path)
    
    # 1. 统计 NPC
    print("\n【NPC 统计】")
    print(f"总 NPC 数量: {len(manager.npcs)}")
    print(f"总商店数量: {len(manager.shops)}")
    
    # 按类型统计
    type_counts = {}
    for npc in manager.npcs.values():
        npc_type = npc.npc_type.value
        type_counts[npc_type] = type_counts.get(npc_type, 0) + 1
    
    print("\n按类型统计:")
    for npc_type, count in type_counts.items():
        print(f"  {npc_type}: {count} 个")
    
    # 2. 测试 NPC 查询
    print("\n【NPC 查询测试】")
    
    # 获取峨眉山的 NPC
    emei_npcs = manager.get_npcs_at_location("峨眉山")
    print(f"\n峨眉山的 NPC ({len(emei_npcs)} 个):")
    for npc in emei_npcs:
        print(f"  - {npc.name} ({npc.npc_type.value})")
    
    # 获取所有师傅
    masters = manager.get_masters()
    print(f"\n所有师傅 ({len(masters)} 个):")
    for master in masters[:5]:
        print(f"  - {master.name} @ {master.location} ({master.sect or '无门派'})")
    
    # 3. 测试对话系统
    print("\n【对话系统测试】")
    
    player_data = {
        'level': 25,
        'spirit_stones': 5000,
        'sect': '峨眉派',
        'sect_contribution': 300,
        'completed_quests': [],
        'active_quests': [],
        'learned_skills': {}
    }
    
    # 与妙一真人对话
    print("\n与妙一真人对话:")
    result = manager.talk_to_npc('miaoyi_zhenren', player_data)
    print(f"  NPC: {result['npc_name']}")
    print(f"  类型: {result['npc_type']}")
    print(f"  对话: {result['dialogue']}")
    if result.get('has_skills'):
        print(f"  可学功法: {result['skill_ids']}")
    if result.get('can_exchange'):
        print(f"  可兑换物品")
    
    # 与村长对话
    print("\n与村长对话:")
    result = manager.talk_to_npc('village_elder', player_data)
    print(f"  对话: {result['dialogue']}")
    if result.get('has_quests'):
        print(f"  可接任务: {result['quest_ids']}")
    
    # 4. 测试商店系统
    print("\n【商店系统测试】")
    
    # 灵药店
    print("\n打开灵药铺:")
    shop_result = manager.open_shop('medicine_merchant', player_data)
    if shop_result['success']:
        print(f"  商店名: {shop_result['shop_name']}")
        print(f"  商品数量: {len(shop_result['items'])}")
        print(f"  部分商品:")
        for item in shop_result['items'][:3]:
            rare_mark = " [稀有]" if item['is_rare'] else ""
            print(f"    - {item['name']}: {item['price']} 灵石{rare_mark}")
    
    # 黑市（需要等级20）
    print("\n尝试打开黑市:")
    shop_result = manager.open_shop('black_market_merchant', player_data)
    if shop_result['success']:
        print(f"  商店名: {shop_result['shop_name']}")
        print(f"  商品数量: {len(shop_result['items'])}")
        print(f"  稀有商品:")
        for item in shop_result['items']:
            print(f"    - {item['name']}: {item['price']} 灵石")
    
    # 5. 测试购买系统
    print("\n【购买系统测试】")
    
    # 购买回春丹
    print("\n购买回春丹 x5:")
    buy_result = manager.buy_item('medicine_merchant', 'hunchun_pill', 5, player_data)
    print(f"  结果: {buy_result['message']}")
    if buy_result['success']:
        print(f"  花费: {buy_result['cost']} 灵石")
    
    # 尝试购买稀有商品
    print("\n购买筑基丹 x1:")
    buy_result = manager.buy_item('medicine_merchant', 'zhujidan', 1, player_data)
    print(f"  结果: {buy_result['message']}")
    if buy_result['success']:
        print(f"  花费: {buy_result['cost']} 灵石")
    
    # 6. 测试门派系统
    print("\n【门派系统测试】")
    
    # 学习功法
    print("\n尝试向妙一真人学习峨眉剑术:")
    learn_result = manager.learn_skill('miaoyi_zhenren', 'emei_sword_art', player_data)
    print(f"  结果: {learn_result['message']}")
    
    # 门派兑换
    print("\n峨眉派贡献兑换:")
    player_data['sect_contribution'] = 500
    exchange_result = manager.exchange_contribution('emei_steward', 'emei_pill', player_data)
    print(f"  结果: {exchange_result['message']}")
    if exchange_result['success']:
        print(f"  花费贡献: {exchange_result['contribution_cost']} 点")
    
    # 7. 测试隐藏 NPC
    print("\n【隐藏 NPC 测试】")
    
    # 低等级玩家无法看到隐世高人
    print("\n低等级玩家尝试与隐世高人对话:")
    low_level_player = {'level': 10, 'spirit_stones': 0, 'sect': None}
    result = manager.talk_to_npc('hidden_master', low_level_player)
    print(f"  结果: {result['message']}")
    
    # 高等级玩家可以看到
    print("\n高等级玩家与隐世高人对话:")
    high_level_player = {'level': 55, 'spirit_stones': 0, 'sect': None}
    result = manager.talk_to_npc('hidden_master', high_level_player)
    if result['success']:
        print(f"  对话: {result['dialogue']}")
    else:
        print(f"  结果: {result['message']}")
    
    # 8. 测试任务系统
    print("\n【任务系统测试】")
    
    # 获取村长的可接任务
    print("\n村长可接任务:")
    available_quests = manager.get_available_quests_from_npc('village_elder', player_data)
    print(f"  可接任务: {available_quests}")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_npc_system()
