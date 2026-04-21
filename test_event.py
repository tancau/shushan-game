#!/usr/bin/env python3
"""
蜀山剑侠传 - 活动系统测试
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from game.event import (
    EventManager, Event, EventType, EventStatus, EventTask, EventTaskType,
    EventReward, SignInSystem
)


def test_event_manager():
    """测试活动管理器"""
    print("=" * 50)
    print("测试活动管理器")
    print("=" * 50)
    
    manager = EventManager()
    
    # 测试加载活动
    print(f"\n加载的活动数量: {len(manager.events)}")
    
    # 显示所有活动
    for event_id, event in manager.events.items():
        print(f"\n活动ID: {event_id}")
        print(f"  名称: {event.name}")
        print(f"  类型: {event.event_type.value}")
        print(f"  状态: {event.status.value}")
        print(f"  任务数: {len(event.tasks)}")
        print(f"  剩余时间: {event.get_remaining_time()}")
    
    # 测试获取进行中的活动
    active_events = manager.get_active_events()
    print(f"\n进行中的活动数量: {len(active_events)}")
    
    # 测试按类型获取
    daily_events = manager.get_events_by_type(EventType.DAILY)
    print(f"日常活动数量: {len(daily_events)}")
    
    weekly_events = manager.get_events_by_type(EventType.WEEKLY)
    print(f"周常活动数量: {len(weekly_events)}")
    
    festival_events = manager.get_events_by_type(EventType.FESTIVAL)
    print(f"节日活动数量: {len(festival_events)}")
    
    special_events = manager.get_events_by_type(EventType.SPECIAL)
    print(f"特殊活动数量: {len(special_events)}")
    
    return manager


def test_sign_in_system():
    """测试签到系统"""
    print("\n" + "=" * 50)
    print("测试签到系统")
    print("=" * 50)
    
    sign_in = SignInSystem()
    player_id = "test_player_001"
    
    # 获取签到状态
    status = sign_in.get_sign_in_status(player_id)
    print(f"\n初始签到状态:")
    print(f"  连续签到: {status['consecutive_days']}天")
    print(f"  累计签到: {status['total_days']}天")
    print(f"  今日已签到: {status['today_signed']}")
    
    # 进行签到
    print(f"\n进行签到...")
    result = sign_in.sign_in(player_id)
    print(f"签到结果: {result['message']}")
    print(f"连续签到: {result['consecutive_days']}天")
    
    if result['success'] and result['rewards']:
        print(f"获得奖励:")
        for reward in result['rewards']:
            print(f"  {reward['name']}: {reward['reward']}")
    
    # 再次签到（应该失败）
    print(f"\n再次尝试签到...")
    result = sign_in.sign_in(player_id)
    print(f"签到结果: {result['message']}")
    
    # 获取更新后的状态
    status = sign_in.get_sign_in_status(player_id)
    print(f"\n更新后签到状态:")
    print(f"  连续签到: {status['consecutive_days']}天")
    print(f"  累计签到: {status['total_days']}天")
    print(f"  今日已签到: {status['today_signed']}")
    
    return sign_in


def test_event_participation():
    """测试活动参与"""
    print("\n" + "=" * 50)
    print("测试活动参与")
    print("=" * 50)
    
    manager = EventManager()
    player_id = "test_player_001"
    
    # 参加活动
    event_id = "daily_cultivation"
    print(f"\n参加活动: {event_id}")
    result = manager.join_event(player_id, event_id)
    print(f"结果: {result['message']}")
    
    # 更新任务进度
    print(f"\n更新任务进度...")
    task_result = manager.update_task_progress(player_id, event_id, "cultivation_1", 5)
    print(f"任务进度: {task_result.get('current', 0)}/{task_result.get('required', 0)}")
    
    # 再次更新
    task_result = manager.update_task_progress(player_id, event_id, "cultivation_1", 5)
    print(f"任务进度: {task_result.get('current', 0)}/{task_result.get('required', 0)}")
    if task_result.get('completed'):
        print(f"任务完成！")
        if task_result.get('reward'):
            print(f"获得奖励: {task_result['reward']}")
    
    # 查看玩家活动数据
    data = manager.get_player_event_data(player_id, event_id)
    if data:
        print(f"\n玩家活动数据:")
        print(f"  积分: {data['points']}")
        print(f"  任务进度: {data['task_progress']}")


def test_point_exchange():
    """测试积分兑换"""
    print("\n" + "=" * 50)
    print("测试积分兑换")
    print("=" * 50)
    
    manager = EventManager()
    player_id = "test_player_002"
    event_id = "special_server_launch"
    
    # 参加活动
    result = manager.join_event(player_id, event_id)
    print(f"参加活动: {result['message']}")
    
    # 检查是否成功参加
    if event_id not in manager.player_event_data.get(player_id, {}):
        print("参加活动失败，跳过积分兑换测试")
        return
    
    # 模拟获得积分
    manager.player_event_data[player_id][event_id]["points"] = 500
    print(f"当前积分: 500")
    
    # 尝试兑换
    print(f"\n尝试兑换: 开服限定时装")
    result = manager.exchange_points(player_id, event_id, "launch_skin")
    print(f"兑换结果: {result['message']}")
    if result['success']:
        print(f"剩余积分: {result['remaining_points']}")
    
    # 再次兑换（应该失败，限制1次）
    print(f"\n再次尝试兑换...")
    result = manager.exchange_points(player_id, event_id, "launch_skin")
    print(f"兑换结果: {result['message']}")


def test_rank_rewards():
    """测试排行奖励"""
    print("\n" + "=" * 50)
    print("测试排行奖励")
    print("=" * 50)
    
    manager = EventManager()
    
    # 模拟多个玩家参与
    event_id = "special_server_launch"
    for i in range(5):
        player_id = f"player_{i}"
        manager.join_event(player_id, event_id)
        manager.player_event_data[player_id][event_id]["points"] = (5 - i) * 100
    
    # 获取排行榜
    rankings = manager.get_event_rank(event_id)
    print(f"\n排行榜:")
    for r in rankings:
        print(f"  第{r['rank']}名: {r['player_id']} - {r['points']}积分")
    
    # 显示奖励信息
    event = manager.get_event(event_id)
    if event and event.rank_rewards:
        print(f"\n排行奖励:")
        for reward in event.rank_rewards:
            print(f"  第{reward.min_rank}-{reward.max_rank}名:")
            print(f"    修为: {reward.reward.cultivation}")
            print(f"    灵石: {reward.reward.spirit_stones}")
            if reward.title:
                print(f"    称号: {reward.title}")


def main():
    """运行所有测试"""
    print("\n🎮 蜀山剑侠传 - 活动系统测试 🎮\n")
    
    test_event_manager()
    test_sign_in_system()
    test_event_participation()
    test_point_exchange()
    test_rank_rewards()
    
    print("\n" + "=" * 50)
    print("✅ 所有测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
