#!/usr/bin/env python3
"""
蜀山剑侠传 - 灵兽系统完整测试
"""

from game.spirit_beast import (
    SpiritBeast, SpiritBeastType, SpiritBeastElement, SpiritBeastSkill,
    SpiritBeastManager, CaptureSystem, TrainingSystem, SpiritBeastCombatSystem
)


def test_spirit_beast_system():
    """测试灵兽系统"""
    print("=" * 60)
    print("蜀山剑侠传 - 灵兽系统测试")
    print("=" * 60)
    
    # 初始化管理器
    manager = SpiritBeastManager()
    print(f"\n✅ 加载了 {len(manager.beast_templates)} 种灵兽模板")
    
    # 测试1: 创建各类灵兽
    print("\n" + "=" * 60)
    print("【测试1】创建各类灵兽")
    print("=" * 60)
    
    test_beasts = [
        ("qinglong", "神兽 - 青龙", 10),
        ("baihu", "神兽 - 白虎", 10),
        ("jianling", "灵兽 - 剑灵", 5),
        ("linghu", "灵兽 - 灵狐", 5),
        ("yinlang", "妖兽 - 银狼", 3),
    ]
    
    beasts = []
    for beast_id, desc, level in test_beasts:
        beast = manager.create_beast(beast_id, level)
        if beast:
            beasts.append(beast)
            print(f"\n{desc}:")
            print(f"  {beast}")
            print(f"  攻击:{beast.attack} 防御:{beast.defense} 速度:{beast.speed}")
            print(f"  血脉:{beast.bloodline} 资质:{beast.aptitude}")
            print(f"  技能: {[s.name for s in beast.skills]}")
    
    # 测试2: 捕捉系统
    print("\n" + "=" * 60)
    print("【测试2】捕捉系统")
    print("=" * 60)
    
    capture_sys = CaptureSystem(manager)
    test_beast = manager.create_beast("lingyuan", level=5)
    
    print(f"\n目标灵兽: {test_beast.name}")
    print(f"捕捉难度: {test_beast.capture_difficulty}")
    
    # 先喂养提升好感度
    print("\n喂养灵兽...")
    for _ in range(3):
        gain, msg = capture_sys.feed_beast(test_beast, "高级灵食")
        print(f"  {msg}")
    
    # 尝试捕捉
    print("\n尝试驯服...")
    for i in range(3):
        success, msg = capture_sys.attempt_capture(test_beast, player_cultivation=30)
        print(f"  第{i+1}次: {msg}")
        if success:
            break
    
    # 签订契约
    if test_beast.affection >= 30:
        success, msg = capture_sys.sign_contract(test_beast, "测试玩家")
        print(f"\n签订契约: {msg}")
    
    # 测试3: 培养系统
    print("\n" + "=" * 60)
    print("【测试3】培养系统")
    print("=" * 60)
    
    training_sys = TrainingSystem(manager)
    training_beast = manager.create_beast("huolongzai", level=1)
    
    print(f"\n培养目标: {training_beast.name} Lv.{training_beast.level}")
    
    # 获取经验升级
    print("\n获取经验...")
    for _ in range(5):
        result = training_sys.gain_exp(training_beast, 200)
        print(f"  {result['message']}")
    
    # 培养属性
    print("\n培养血脉...")
    success, msg = training_sys.train_stat(training_beast, "bloodline", 100)
    print(f"  {msg}")
    
    print("\n培养资质...")
    success, msg = training_sys.train_stat(training_beast, "aptitude", 100)
    print(f"  {msg}")
    
    # 学习技能
    print("\n学习技能...")
    success, msg = training_sys.learn_skill_from_scroll(training_beast, "thunder_strike")
    print(f"  {msg}")
    
    print(f"\n培养结果: {training_beast}")
    print(f"技能列表: {[s.name for s in training_beast.skills]}")
    
    # 测试4: 战斗系统
    print("\n" + "=" * 60)
    print("【测试4】战斗系统")
    print("=" * 60)
    
    combat_sys = SpiritBeastCombatSystem(manager)
    attacker = manager.create_beast("leishou", level=8)
    defender = manager.create_beast("xuantiegui", level=8)
    
    print(f"\n攻击方: {attacker.name} (攻击:{attacker.attack})")
    print(f"防御方: {defender.name} (防御:{defender.defense})")
    
    # 获取战斗属性
    print("\n攻击方战斗属性:")
    stats = combat_sys.get_combat_stats(attacker)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 模拟战斗
    print("\n战斗模拟:")
    for i in range(3):
        # 选择技能
        available_skills = attacker.get_available_skills()
        skill_id = available_skills[0].id if available_skills else None
        
        result = combat_sys.beast_attack(attacker, defender, skill_id)
        print(f"\n  回合 {i+1}:")
        print(f"    {result['message']}")
        if result['effect_applied']:
            print(f"    效果: {result['effect_applied']}")
        print(f"    防御方HP: {defender.current_hp}/{defender.max_hp}")
        
        if not defender.is_alive:
            print(f"    {defender.name} 已被击败!")
            break
    
    # 测试5: 复活系统
    print("\n" + "=" * 60)
    print("【测试5】复活系统")
    print("=" * 60)
    
    dead_beast = manager.create_beast("yinlang", level=5)
    dead_beast.current_hp = 0
    
    print(f"\n灵兽状态: {dead_beast.name} HP:{dead_beast.current_hp}/{dead_beast.max_hp}")
    print(f"是否存活: {'是' if dead_beast.is_alive else '否'}")
    
    success, msg = combat_sys.revive_beast(dead_beast)
    print(f"\n复活结果: {msg}")
    print(f"复活后HP: {dead_beast.current_hp}/{dead_beast.max_hp}")
    
    # 测试6: 灵兽类型统计
    print("\n" + "=" * 60)
    print("【测试6】灵兽统计")
    print("=" * 60)
    
    divine_count = len(manager.get_beasts_by_type(SpiritBeastType.DIVINE))
    spirit_count = len(manager.get_beasts_by_type(SpiritBeastType.SPIRIT))
    demon_count = len(manager.get_beasts_by_type(SpiritBeastType.DEMON))
    
    print(f"\n神兽数量: {divine_count}")
    print(f"灵兽数量: {spirit_count}")
    print(f"妖兽数量: {demon_count}")
    print(f"总计: {divine_count + spirit_count + demon_count}")
    
    # 测试7: 随机生成灵兽
    print("\n" + "=" * 60)
    print("【测试7】随机生成灵兽")
    print("=" * 60)
    
    random_beast = manager.get_random_beast(level_range=(5, 15))
    if random_beast:
        print(f"\n随机灵兽: {random_beast}")
        print(f"类型: {random_beast.beast_type.value}")
        print(f"属性: {random_beast.element.value}")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    test_spirit_beast_system()
