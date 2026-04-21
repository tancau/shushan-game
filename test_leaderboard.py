#!/usr/bin/env python3
"""
排行榜系统测试
"""

import sys
sys.path.insert(0, "/home/tancau/.openclaw/workspace/shushan-game")

from game.player import Player
from game.leaderboard import (
    LeaderboardManager, LeaderboardType, RewardType,
    LeaderboardEntry, RankingTitle
)


def test_leaderboard_basic():
    """测试基础功能"""
    print("=" * 50)
    print("【测试1：基础功能】")
    print("=" * 50)
    
    # 创建排行榜管理器
    manager = LeaderboardManager("data/leaderboards.json")
    
    # 创建测试玩家
    players = []
    for i, name in enumerate(["张三", "李四", "王五", "赵六", "钱七"]):
        player = Player(name)
        player.cultivation = 1000 * (5 - i)
        player.spirit_stones = 500 * (5 - i)
        player.spirit_stones += i * 100
        player.realm = ["筑基期", "金丹期", "练气期", "元婴期", "筑基期"][i]
        player.sect = ["峨眉派", "青城派", "昆仑派", "血河教", None][i]
        players.append(player)
    
    # 更新排行榜
    for player in players:
        rankings = manager.update_player(player)
        print(f"\n{player.name} 排名更新:")
        for lb_name, rank in rankings.items():
            print(f"  {lb_name}: 第{rank}名")
    
    # 显示排行榜
    print("\n" + "=" * 50)
    print("【战力榜】")
    print(manager.get_leaderboard_display(LeaderboardType.POWER))
    
    print("\n【修为榜】")
    print(manager.get_leaderboard_display(LeaderboardType.CULTIVATION))
    
    print("\n【境界榜】")
    print(manager.get_leaderboard_display(LeaderboardType.REALM))
    
    return manager, players


def test_ranking_titles(manager: LeaderboardManager, players):
    """测试排名称号"""
    print("\n" + "=" * 50)
    print("【测试2：排名称号】")
    print("=" * 50)
    
    # 检查并发放称号
    for player in players:
        awarded = manager.check_and_award_titles(player)
        if awarded:
            print(f"\n{player.name} 获得称号:")
            for title_info in awarded:
                title = title_info["title"]
                print(f"  🏆 {title.name} - {title.description}")
                print(f"     加成: {title.get_bonus_text()}")
    
    # 显示玩家有效称号
    print("\n【玩家有效称号】")
    for player in players:
        active_titles = manager.get_player_active_titles(player.name)
        if active_titles:
            print(f"\n{player.name}:")
            for title_info in active_titles:
                title = title_info["title"]
                print(f"  • {title.name} ({title_info['days_remaining']}天后过期)")


def test_rewards(manager: LeaderboardManager, players):
    """测试奖励系统"""
    print("\n" + "=" * 50)
    print("【测试3：奖励系统】")
    print("=" * 50)
    
    # 显示每日奖励配置
    print("\n【每日奖励配置】")
    for rank in [1, 2, 3]:
        rewards = manager.get_daily_rewards(rank)
        print(f"第{rank}名奖励:")
        for reward in rewards:
            print(f"  • {reward.name}: {reward.value} {reward.reward_type.value}")
    
    # 显示每周奖励配置
    print("\n【每周奖励配置】")
    for rank in [1, 2, 3]:
        rewards = manager.get_weekly_rewards(rank)
        print(f"第{rank}名奖励:")
        for reward in rewards:
            print(f"  • {reward.name}: {reward.value} {reward.reward_type.value}")
    
    # 测试领取奖励
    print("\n【领取每日奖励】")
    for player in players[:3]:  # 只测试前三名
        result = manager.claim_daily_reward(player)
        print(f"\n{player.name}: {result['message']}")
        if result['success']:
            for reward in result['rewards']:
                print(f"  ✓ 获得 {reward.name} x{reward.value}")
    
    # 再次领取（应该失败）
    print("\n【重复领取测试】")
    result = manager.claim_daily_reward(players[0])
    print(f"{players[0].name}: {result['message']}")


def test_player_rank_card(manager: LeaderboardManager, players):
    """测试玩家排名卡片"""
    print("\n" + "=" * 50)
    print("【测试4：玩家排名卡片】")
    print("=" * 50)
    
    for player in players[:2]:
        print(manager.get_player_rank_card(player))
        print()


def test_leaderboard_summary(manager: LeaderboardManager, players):
    """测试排行榜概要"""
    print("\n" + "=" * 50)
    print("【测试5：排行榜概要】")
    print("=" * 50)
    
    print(manager.get_all_leaderboards_summary(players[0].name))


def main():
    """主测试函数"""
    print("╔════════════════════════════════════════════╗")
    print("║       蜀山剑侠传 - 排行榜系统测试          ║")
    print("╚════════════════════════════════════════════╝")
    
    # 基础功能测试
    manager, players = test_leaderboard_basic()
    
    # 称号测试
    test_ranking_titles(manager, players)
    
    # 奖励测试
    test_rewards(manager, players)
    
    # 玩家卡片测试
    test_player_rank_card(manager, players)
    
    # 概要测试
    test_leaderboard_summary(manager, players)
    
    print("\n" + "=" * 50)
    print("✅ 所有测试完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
