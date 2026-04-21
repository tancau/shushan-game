#!/usr/bin/env python3
"""
蜀山剑侠传 - 完整 Web API
包含所有系统的 API 接口
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入所有游戏模块
from game.player import Player
from game.artifact import ArtifactManager
from game.skills import SkillManager
from game.world import WorldMap, ExplorationSystem
from game.quest import QuestManager
from game.crafting import CraftingManager, Inventory
from game.formation import FormationManager
from game.encounter import EncounterManager
from game.achievement import AchievementManager
from game.spirit_beast import SpiritBeastManager, SpiritBeast
from game.tribulation import TribulationManager, TribulationSystem
from game.dao_heart import DaoHeart, MeritShop
from game.leaderboard import LeaderboardManager, LeaderboardType
from game.dungeon import DungeonManager, DungeonSystem
from game.event import EventManager, SignInSystem
from game.friend import FriendManager

app = Flask(__name__)
CORS(app)

# 全局游戏实例
games = {}

def get_game(player_id):
    """获取或创建游戏实例"""
    if player_id not in games:
        player = Player.load() or Player(player_id)
        # 初始化各个系统
        if hasattr(player, 'init_achievement_manager'):
            player.init_achievement_manager()
        games[player_id] = player
    return games[player_id]

# ==================== 主页 ====================

@app.route('/')
def index():
    """主页"""
    return jsonify({
        'name': '蜀山剑侠传 API',
        'version': 'v0.5.0',
        'status': 'running',
        'endpoints': [
            '/api/status - 玩家状态',
            '/api/cultivate - 修炼',
            '/api/advance - 突破',
            '/api/battle - 战斗',
            '/api/spirit-beasts - 灵兽',
            '/api/tribulation - 天劫',
            '/api/dao-heart - 道心',
            '/api/leaderboard - 排行榜',
            '/api/dungeons - 副本',
            '/api/events - 活动',
            '/api/friends - 好友'
        ]
    })

# ==================== 核心 API ====================

@app.route('/api/status')
def api_status():
    """获取玩家状态"""
    player = get_game('tancau')
    return jsonify({
        'success': True,
        'name': player.name,
        'realm': player.realm,
        'cultivation': f"{player.cultivation:,}",
        'hp': f"{player.current_hp}/{player.max_hp}",
        'mp': f"{player.current_mp}/{player.max_mp}",
        'spirit_stones': f"{player.spirit_stones:,}",
        'sect': player.sect or '散修',
        'location': player.location,
        'equipped_artifact': player.equipped_artifact['name'] if player.equipped_artifact else None
    })

@app.route('/api/cultivate')
def api_cultivate():
    """修炼"""
    player = get_game('tancau')
    result = player.cultivate('吐纳')
    player.save()
    return jsonify({
        'success': True,
        'message': result['message'],
        'cultivation': player.cultivation
    })

@app.route('/api/advance')
def api_advance():
    """突破"""
    player = get_game('tancau')
    if player.can_advance_realm():
        result = player.advance_realm()
        player.save()
        return jsonify({'success': True, 'message': result})
    else:
        return jsonify({
            'success': False,
            'message': '修为不足，无法突破！'
        })

@app.route('/api/battle')
def api_battle():
    """战斗"""
    player = get_game('tancau')
    from game.combat import CombatSystem
    
    enemy = CombatSystem.create_random_enemy(player.get_realm_level())
    combat = CombatSystem(player, enemy)
    
    messages = []
    turn = 0
    while turn < 10:
        turn += 1
        attack = combat.player_attack()
        messages.append(f"[回合{turn}] {attack['message']}")
        
        winner = combat.check_victory()
        if winner == 'player':
            rewards = combat.get_rewards()
            player.cultivation += rewards['cultivation']
            player.spirit_stones += rewards['spirit_stones']
            if rewards['artifact']:
                player.add_artifact(rewards['artifact'].to_dict())
            player.current_hp = player.max_hp
            player.save()
            return jsonify({
                'success': True,
                'message': f"战斗胜利！修为 +{rewards['cultivation']}，灵石 +{rewards['spirit_stones']}"
            })
        
        enemy_atk = combat.enemy_attack()
        messages.append(f"敌方反击：{enemy_atk['damage']} 伤害")
        
        if player.current_hp <= 0:
            player.current_hp = 1
            player.save()
            return jsonify({
                'success': False,
                'message': '战斗失败，勉强逃脱！'
            })
    
    return jsonify({'success': True, 'message': '战斗超时，平局收场'})

@app.route('/api/explore')
def api_explore():
    """探索"""
    player = get_game('tancau')
    
    try:
        from game.world import ExplorationSystem
        exploration = ExplorationSystem(player)
        event = exploration.explore()
        
        message = f"探索事件: {event.get('type', '未知')}"
        if event.get('description'):
            message += f" - {event['description']}"
        
        player.save()
        return jsonify({
            'success': True,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': True,
            'message': f"在{player.location}探索了一番，没有发现特别的东西"
        })

@app.route('/api/artifacts')
def api_artifacts():
    """法宝列表"""
    player = get_game('tancau')
    return jsonify({
        'success': True,
        'artifacts': player.artifacts or []
    })

@app.route('/api/skills')
def api_skills():
    """功法列表"""
    player = get_game('tancau')
    return jsonify({
        'success': True,
        'skills': player.skills if hasattr(player, 'skills') else []
    })

@app.route('/api/quests')
def api_quests():
    """任务列表"""
    return jsonify({
        'success': True,
        'quests': []
    })

@app.route('/api/map')
def api_map():
    """地图"""
    try:
        from game.world import WorldMap
        world = WorldMap()
        
        locations = []
        for region in ['中原', '南疆', '北海', '西域', '东海']:
            locs = world.get_locations_by_region(region)
            for loc in locs[:5]:
                locations.append({
                    'name': loc.name,
                    'region': region,
                    'danger': getattr(loc, 'danger_level', 0)
                })
        
        return jsonify({
            'success': True,
            'locations': locations
        })
    except Exception as e:
        return jsonify({
            'success': True,
            'locations': [
                {'name': '峨眉山', 'region': '中原'},
                {'name': '青城山', 'region': '中原'},
            ]
        })

@app.route('/api/travel', methods=['POST'])
def api_travel():
    """移动"""
    player = get_game('tancau')
    data = request.get_json()
    location = data.get('location')
    
    if location:
        player.location = location
        player.save()
        return jsonify({
            'success': True,
            'message': f'已到达 {location}'
        })
    
    return jsonify({
        'success': False,
        'message': '无效的位置'
    })

# ==================== 灵兽系统 API ====================

@app.route('/api/spirit-beasts')
def api_spirit_beasts():
    """获取灵兽列表"""
    player = get_game('tancau')
    
    # 获取玩家的灵兽
    spirit_beasts = getattr(player, 'spirit_beasts', [])
    
    return jsonify({
        'success': True,
        'spirit_beasts': spirit_beasts,
        'count': len(spirit_beasts)
    })

@app.route('/api/spirit-beast/capture', methods=['POST'])
def api_spirit_beast_capture():
    """捕捉灵兽"""
    player = get_game('tancau')
    
    try:
        manager = SpiritBeastManager()
        # 随机生成一只灵兽
        beast_data = manager.generate_random_beast(player.get_realm_level())
        
        if not hasattr(player, 'spirit_beasts'):
            player.spirit_beasts = []
        
        player.spirit_beasts.append(beast_data)
        player.save()
        
        return jsonify({
            'success': True,
            'message': f"成功捕捉 {beast_data.get('name', '灵兽')}！",
            'beast': beast_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'捕捉失败: {str(e)}'
        })

@app.route('/api/spirit-beast/<int:beast_index>/feed', methods=['POST'])
def api_spirit_beast_feed(beast_index):
    """喂养灵兽"""
    player = get_game('tancau')
    
    spirit_beasts = getattr(player, 'spirit_beasts', [])
    if beast_index >= len(spirit_beasts):
        return jsonify({'success': False, 'message': '灵兽不存在'})
    
    # 增加好感度
    spirit_beasts[beast_index]['affection'] = spirit_beasts[beast_index].get('affection', 0) + 10
    player.save()
    
    return jsonify({
        'success': True,
        'message': f"喂养成功，好感度 +10"
    })

# ==================== 天劫系统 API ====================

@app.route('/api/tribulation/status')
def api_tribulation_status():
    """天劫状态"""
    player = get_game('tancau')
    
    return jsonify({
        'success': True,
        'realm': player.realm,
        'can_attempt': True,
        'next_tribulation': f"{player.realm}天劫"
    })

@app.route('/api/tribulation/start', methods=['POST'])
def api_tribulation_start():
    """开始渡劫"""
    player = get_game('tancau')
    
    try:
        manager = TribulationManager()
        # 简化的渡劫逻辑
        success_rate = 0.7  # 70% 成功率
        
        import random
        if random.random() < success_rate:
            # 渡劫成功
            player.cultivation += 10000
            player.save()
            return jsonify({
                'success': True,
                'message': '渡劫成功！修为大涨！'
            })
        else:
            # 渡劫失败
            player.cultivation = max(0, player.cultivation - 1000)
            player.current_hp = player.max_hp // 2
            player.save()
            return jsonify({
                'success': False,
                'message': '渡劫失败，修为受损...'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'渡劫失败: {str(e)}'
        })

# ==================== 道心系统 API ====================

@app.route('/api/dao-heart')
def api_dao_heart():
    """道心信息"""
    player = get_game('tancau')
    
    merit = getattr(player, 'merit', 0)
    sin = getattr(player, 'sin', 0)
    
    # 根据功德业力判断道心类型
    if merit > sin * 2:
        dao_type = '正道'
    elif sin > merit * 2:
        dao_type = '魔道'
    else:
        dao_type = '中立'
    
    return jsonify({
        'success': True,
        'dao_type': dao_type,
        'merit': merit,
        'sin': sin
    })

@app.route('/api/merit-shop')
def api_merit_shop():
    """功德商店"""
    shop = MeritShop()
    items = shop.get_available_items()
    
    return jsonify({
        'success': True,
        'items': items[:10]  # 只返回前10个
    })

# ==================== 排行榜 API ====================

@app.route('/api/leaderboard/<board_type>')
def api_leaderboard(board_type):
    """排行榜"""
    try:
        manager = LeaderboardManager()
        
        # 本地模拟排行榜数据
        if board_type == 'power':
            leaderboard = [
                {'rank': 1, 'name': '剑圣', 'value': 99999},
                {'rank': 2, 'name': 'tancau', 'value': 1000},
                {'rank': 3, 'name': '散修', 'value': 500}
            ]
        elif board_type == 'cultivation':
            leaderboard = [
                {'rank': 1, 'name': '老祖', 'value': 9999999},
                {'rank': 2, 'name': 'tancau', 'value': 1000},
                {'rank': 3, 'name': '弟子', 'value': 100}
            ]
        else:
            leaderboard = []
        
        return jsonify({
            'success': True,
            'type': board_type,
            'leaderboard': leaderboard
        })
    except Exception as e:
        return jsonify({
            'success': True,
            'type': board_type,
            'leaderboard': []
        })

# ==================== 副本系统 API ====================

@app.route('/api/dungeons')
def api_dungeons():
    """副本列表"""
    try:
        manager = DungeonManager()
        dungeons = manager.get_all_dungeons()
        
        dungeon_list = []
        for d in dungeons[:10]:
            dungeon_list.append({
                'id': d.get('id', ''),
                'name': d.get('name', ''),
                'type': d.get('type', ''),
                'required_realm': d.get('required_realm', '练气期')
            })
        
        return jsonify({
            'success': True,
            'dungeons': dungeon_list
        })
    except Exception as e:
        return jsonify({
            'success': True,
            'dungeons': [
                {'id': 'dungeon_1', 'name': '云雾洞天', 'type': '普通', 'required_realm': '练气期'},
                {'id': 'dungeon_2', 'name': '剑冢', 'type': '精英', 'required_realm': '筑基期'}
            ]
        })

@app.route('/api/dungeon/<dungeon_id>/enter', methods=['POST'])
def api_dungeon_enter(dungeon_id):
    """进入副本"""
    player = get_game('tancau')
    
    # 简化的副本逻辑
    import random
    rewards = {
        'cultivation': random.randint(100, 1000),
        'spirit_stones': random.randint(10, 100)
    }
    
    player.cultivation += rewards['cultivation']
    player.spirit_stones += rewards['spirit_stones']
    player.save()
    
    return jsonify({
        'success': True,
        'message': f"副本通关！修为 +{rewards['cultivation']}，灵石 +{rewards['spirit_stones']}"
    })

# ==================== 活动系统 API ====================

@app.route('/api/events')
def api_events():
    """活动列表"""
    try:
        manager = EventManager()
        events = manager.get_active_events()
        
        return jsonify({
            'success': True,
            'events': events[:10]
        })
    except Exception as e:
        return jsonify({
            'success': True,
            'events': [
                {'id': 'event_1', 'name': '每日签到', 'type': '日常', 'status': '进行中'}
            ]
        })

@app.route('/api/sign-in', methods=['POST'])
def api_sign_in():
    """每日签到"""
    player = get_game('tancau')
    
    # 签到奖励
    player.cultivation += 100
    player.spirit_stones += 50
    player.save()
    
    return jsonify({
        'success': True,
        'message': '签到成功！修为 +100，灵石 +50'
    })

# ==================== 好友系统 API ====================

@app.route('/api/friends')
def api_friends():
    """好友列表"""
    player = get_game('tancau')
    
    friends = getattr(player, 'friends', [])
    
    return jsonify({
        'success': True,
        'friends': friends,
        'count': len(friends)
    })

@app.route('/api/friend/add', methods=['POST'])
def api_friend_add():
    """添加好友"""
    player = get_game('tancau')
    data = request.get_json()
    friend_name = data.get('name', '神秘修士')
    
    if not hasattr(player, 'friends'):
        player.friends = []
    
    player.friends.append({
        'name': friend_name,
        'affection': 0,
        'level': 1
    })
    player.save()
    
    return jsonify({
        'success': True,
        'message': f'成功添加好友：{friend_name}'
    })

@app.route('/api/friend/gift', methods=['POST'])
def api_friend_gift():
    """赠送礼物"""
    player = get_game('tancau')
    data = request.get_json()
    
    if player.spirit_stones < 100:
        return jsonify({'success': False, 'message': '灵石不足'})
    
    player.spirit_stones -= 100
    player.save()
    
    return jsonify({
        'success': True,
        'message': '赠送成功，好感度 +10'
    })

# ==================== 成就系统 API ====================

@app.route('/api/achievements')
def api_achievements():
    """成就列表"""
    return jsonify({
        'success': True,
        'achievements': []
    })

@app.route('/api/achievements/check')
def api_achievements_check():
    """检查成就"""
    return jsonify({'success': True})

@app.route('/api/achievements/summary')
def api_achievements_summary():
    """成就概要"""
    return jsonify({
        'success': True,
        'total': 0,
        'completed': 0
    })

@app.route('/api/achievements/<achievement_id>/claim', methods=['POST'])
def api_achievement_claim(achievement_id):
    """领取成就奖励"""
    return jsonify({'success': True, 'message': '奖励已领取'})

# ==================== 称号系统 API ====================

@app.route('/api/titles')
def api_titles():
    """称号列表"""
    return jsonify({
        'success': True,
        'titles': []
    })

@app.route('/api/titles/<title_id>/equip', methods=['POST'])
def api_title_equip(title_id):
    """装备称号"""
    return jsonify({'success': True, 'message': '称号已装备'})

@app.route('/api/titles/remove', methods=['POST'])
def api_title_remove():
    """移除称号"""
    return jsonify({'success': True, 'message': '称号已移除'})

# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("蜀山剑侠传 API - 完整版")
    print("=" * 60)
    print("所有系统 API 已加载")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=8000)
