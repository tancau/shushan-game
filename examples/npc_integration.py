#!/usr/bin/env python3
"""
蜀山剑侠传 - NPC 系统集成示例

展示如何将 NPC 系统集成到游戏主系统中
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.npc import NPCManager
from game.player import Player
from typing import Dict, Optional


class GameNPCIntegration:
    """游戏 NPC 集成类"""
    
    def __init__(self, game):
        """初始化
        
        Args:
            game: 游戏主实例
        """
        self.game = game
        
        # 使用绝对路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        npc_path = os.path.join(base_dir, 'data/npcs.json')
        shop_path = os.path.join(base_dir, 'data/shops.json')
        self.npc_manager = NPCManager(npc_path, shop_path)
    
    def interact_with_npc(self, player: Player, npc_id: str) -> Dict:
        """与 NPC 交互
        
        Args:
            player: 玩家实例
            npc_id: NPC ID
            
        Returns:
            交互结果
        """
        # 转换玩家数据
        player_data = self._player_to_dict(player)
        
        # 与 NPC 对话
        result = self.npc_manager.talk_to_npc(npc_id, player_data)
        
        if not result['success']:
            return result
        
        # 记录对话（用于任务进度）
        npc = self.npc_manager.get_npc(npc_id)
        if npc:
            player.record_dialogue(npc.name)
        
        return result
    
    def open_npc_shop(self, player: Player, npc_id: str) -> Dict:
        """打开 NPC 商店
        
        Args:
            player: 玩家实例
            npc_id: NPC ID
            
        Returns:
            商店数据
        """
        player_data = self._player_to_dict(player)
        return self.npc_manager.open_shop(npc_id, player_data)
    
    def buy_item_from_npc(self, player: Player, npc_id: str, 
                          item_id: str, quantity: int = 1) -> Dict:
        """从 NPC 购买物品
        
        Args:
            player: 玩家实例
            npc_id: NPC ID
            item_id: 物品 ID
            quantity: 数量
            
        Returns:
            购买结果
        """
        player_data = self._player_to_dict(player)
        result = self.npc_manager.buy_item(npc_id, item_id, quantity, player_data)
        
        if result['success']:
            # 扣除灵石
            player.spirit_stones -= result['cost']
            
            # 添加物品到玩家背包（需要在主游戏中实现）
            # self.game.add_item_to_inventory(player, item_id, quantity)
            
            # 记录交易（用于任务进度）
            npc = self.npc_manager.get_npc(npc_id)
            if npc:
                player.record_dialogue(npc.name)
        
        return result
    
    def learn_skill_from_npc(self, player: Player, npc_id: str, skill_id: str) -> Dict:
        """从 NPC 学习功法
        
        Args:
            player: 玩家实例
            npc_id: NPC ID
            skill_id: 功法 ID
            
        Returns:
            学习结果
        """
        player_data = self._player_to_dict(player)
        result = self.npc_manager.learn_skill(npc_id, skill_id, player_data)
        
        if result['success']:
            # 执行学习逻辑
            learn_result = player.learn_skill(skill_id)
            
            if learn_result['success']:
                return {
                    'success': True,
                    'message': f"成功向 {result['npc_name']} 学习了 {learn_result['skill'].name}！",
                    'skill': learn_result['skill']
                }
            else:
                return {
                    'success': False,
                    'message': learn_result['message']
                }
        
        return result
    
    def exchange_with_npc(self, player: Player, npc_id: str, exchange_id: str) -> Dict:
        """与 NPC 兑换门派贡献
        
        Args:
            player: 玩家实例
            npc_id: NPC ID
            exchange_id: 兑换项 ID
            
        Returns:
            兑换结果
        """
        player_data = self._player_to_dict(player)
        result = self.npc_manager.exchange_contribution(npc_id, exchange_id, player_data)
        
        if result['success']:
            # 扣除贡献
            player.sect_contribution -= result['contribution_cost']
            
            # 添加物品到玩家背包（需要在主游戏中实现）
            # self.game.add_item_to_inventory(player, result['item_id'], 1)
        
        return result
    
    def get_available_quests(self, player: Player, npc_id: str) -> list:
        """获取 NPC 可接取的任务
        
        Args:
            player: 玩家实例
            npc_id: NPC ID
            
        Returns:
            可接任务列表
        """
        player_data = self._player_to_dict(player)
        return self.npc_manager.get_available_quests_from_npc(npc_id, player_data)
    
    def get_npcs_at_current_location(self, player: Player) -> list:
        """获取玩家当前位置的所有 NPC
        
        Args:
            player: 玩家实例
            
        Returns:
            NPC 列表
        """
        npcs = self.npc_manager.get_npcs_at_location(player.location)
        
        result = []
        for npc in npcs:
            player_data = self._player_to_dict(player)
            can_interact, _ = npc.can_interact(player_data)
            
            result.append({
                'npc_id': npc.npc_id,
                'name': npc.name,
                'type': npc.npc_type.value,
                'description': npc.description,
                'can_interact': can_interact
            })
        
        return result
    
    def _player_to_dict(self, player: Player) -> dict:
        """将玩家实例转换为字典
        
        Args:
            player: 玩家实例
            
        Returns:
            玩家数据字典
        """
        return {
            'name': player.name,
            'level': player.get_realm_level(),
            'realm': player.realm,
            'spirit_stones': player.spirit_stones,
            'sect': player.sect,
            'sect_contribution': player.sect_contribution,
            'location': player.location,
            'completed_quests': player.completed_quests,
            'active_quests': player.active_quests,
            'learned_skills': list(player.learned_skills.keys()),
            'reputation': getattr(player, 'reputation', 0)
        }


# ==================== 使用示例 ====================

def example_usage():
    """使用示例"""
    from game.player import Player
    
    # 创建玩家
    player = Player("测试玩家")
    player.realm = "筑基期"
    player.cultivation = 5000
    player.spirit_stones = 3000
    player.sect = "峨眉派"
    player.sect_contribution = 500
    player.location = "峨眉山"
    
    # 初始化集成
    integration = GameNPCIntegration(None)
    
    print("=" * 60)
    print("NPC 系统集成示例")
    print("=" * 60)
    
    # 1. 查看当前位置的 NPC
    print("\n【当前位置的 NPC】")
    npcs = integration.get_npcs_at_current_location(player)
    for npc in npcs:
        status = "✓" if npc['can_interact'] else "✗"
        print(f"  {status} {npc['name']} ({npc['type']}) - {npc['description'][:30]}...")
    
    # 2. 与妙一真人对话
    print("\n【与妙一真人对话】")
    result = integration.interact_with_npc(player, 'miaoyi_zhenren')
    print(f"  {result['npc_name']}: {result['dialogue']}")
    
    # 3. 学习功法
    print("\n【学习峨眉剑术】")
    result = integration.learn_skill_from_npc(player, 'miaoyi_zhenren', 'emei_sword_art')
    print(f"  结果: {result.get('message', '学习成功')}")
    
    # 4. 门派兑换
    print("\n【门派贡献兑换】")
    result = integration.exchange_with_npc(player, 'emei_steward', 'emei_pill')
    print(f"  结果: {result['message']}")
    
    # 5. 去成都府买丹药
    print("\n【前往成都府】")
    player.location = "成都府"
    
    # 打开灵药铺
    print("\n【打开灵药铺】")
    shop_result = integration.open_npc_shop(player, 'medicine_merchant')
    if shop_result['success']:
        print(f"  商店: {shop_result['shop_name']}")
        print(f"  灵石: {shop_result['player_spirit_stones']}")
        print(f"  商品:")
        for item in shop_result['items'][:5]:
            rare_mark = " [稀有]" if item['is_rare'] else ""
            print(f"    - {item['name']}: {item['price']} 灵石{rare_mark}")
    
    # 购买回春丹
    print("\n【购买回春丹 x10】")
    buy_result = integration.buy_item_from_npc(player, 'medicine_merchant', 'hunchun_pill', 10)
    print(f"  结果: {buy_result['message']}")
    if buy_result['success']:
        print(f"  剩余灵石: {player.spirit_stones}")
    
    print("\n" + "=" * 60)
    print("✅ 示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()
