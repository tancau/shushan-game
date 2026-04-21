#!/usr/bin/env python3
"""
蜀山剑侠传 - 快速游戏启动器
适合在聊天界面使用
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.player import Player
from game.artifact import ArtifactManager
from game.combat import CombatSystem


class QuickGame:
    """快速游戏启动器"""
    
    def __init__(self):
        self.player = None
    
    def start(self):
        """开始游戏"""
        # 尝试读取存档
        self.player = Player.load()
        
        if self.player:
            print(f"欢迎回来，{self.player.name}！\n")
        else:
            # 创建新角色
            print("【创建角色】\n")
            name = "tancau"  # 使用用户名
            
            self.player = Player(name)
            self.player.join_sect("峨眉派")
            
            # 给予初始法宝
            artifact = ArtifactManager.get_artifact("青竹剑")
            if artifact:
                self.player.add_artifact(artifact.to_dict())
                self.player.equip_artifact("青竹剑")
            
            print(f"你叫{name}，拜入峨眉派，开始修真之旅...\n")
            print(f"获得初始法宝：青竹剑\n")
            
            self.player.save()
        
        return self.show_status()
    
    def show_status(self):
        """显示状态"""
        status = f"""
═══════════════════════════════════════
【{self.player.name}】
═══════════════════════════════════════
境界：{self.player.realm}
修为：{self.player.cultivation:,}
灵石：{self.player.spirit_stones:,}
生命：{self.player.current_hp}/{self.player.max_hp}
真元：{self.player.current_mp}/{self.player.max_mp}
门派：{self.player.sect}
位置：{self.player.location}
法宝：{len(self.player.artifacts)} 件
───────────────────────────────────────
装备：{self.player.equipped_artifact['name'] if self.player.equipped_artifact else '无'}
═══════════════════════════════════════
        """.strip()
        
        return status
    
    def cultivate(self, times=1):
        """修炼"""
        results = []
        
        for _ in range(times):
            result = self.player.cultivate("吐纳")
            results.append(result['message'])
            
            if result.get('can_advance'):
                results.append(f"🌟 {result['advance_message']}")
        
        # 恢复真元
        if self.player.current_mp < self.player.max_mp:
            self.player.current_mp = min(
                self.player.max_mp,
                self.player.current_mp + 10
            )
        
        self.player.save()
        
        return "\n".join(results)
    
    def advance(self):
        """突破境界"""
        if self.player.can_advance_realm():
            result = self.player.advance_realm()
            self.player.save()
            return result
        else:
            required = 0
            for realm_name, realm_info in {
                "筑基期": {"cultivation_required": 1000},
                "金丹期": {"cultivation_required": 10000},
                "元婴期": {"cultivation_required": 100000},
                "化神期": {"cultivation_required": 1000000},
            }.items():
                if realm_name not in ["练气期", self.player.realm]:
                    if self.player.get_realm_level() < {
                        "筑基期": 2, "金丹期": 3, "元婴期": 4, "化神期": 5
                    }.get(realm_name, 1):
                        required = realm_info["cultivation_required"]
                        break
            
            return f"修为不足！需要 {required:,} 修为才能突破"
    
    def battle(self):
        """战斗"""
        enemy = CombatSystem.create_random_enemy(self.player.get_realm_level())
        combat = CombatSystem(self.player, enemy)
        
        result = f"\n遭遇 {enemy.name}（{enemy.realm}）！\n"
        result += "=" * 40 + "\n"
        
        # 自动战斗
        turn = 0
        while turn < 20:  # 最多20回合
            turn += 1
            
            # 玩家攻击
            attack_result = combat.player_attack()
            result += f"[回合{turn}] {attack_result['message']}\n"
            
            winner = combat.check_victory()
            if winner == "player":
                rewards = combat.get_rewards()
                result += "\n🎉 战斗胜利！\n"
                result += f"修为 +{rewards['cultivation']}\n"
                result += f"灵石 +{rewards['spirit_stones']}\n"
                
                self.player.cultivation += rewards["cultivation"]
                self.player.spirit_stones += rewards["spirit_stones"]
                
                if rewards["artifact"]:
                    result += f"🎊 获得法宝：{rewards['artifact'].name}！\n"
                    self.player.add_artifact(rewards["artifact"].to_dict())
                
                self.player.save()
                return result
            
            # 敌人攻击
            enemy_result = combat.enemy_attack()
            result += f"  敌方攻击：{enemy_result['damage']} 伤害\n"
            
            if self.player.current_hp <= 0:
                self.player.current_hp = 1
                result += "\n💀 战斗失败，勉强逃脱\n"
                self.player.save()
                return result
        
        result += "\n战斗超时，平局收场\n"
        return result
    
    def show_artifacts(self):
        """显示法宝"""
        if not self.player.artifacts:
            return "你还没有任何法宝"
        
        result = "【我的法宝】\n" + "=" * 40 + "\n"
        
        for i, artifact in enumerate(self.player.artifacts, 1):
            equipped = " ⚔️" if (self.player.equipped_artifact and 
                                self.player.equipped_artifact["name"] == artifact["name"]) else ""
            result += f"{i}. {artifact['name']}{equipped}\n"
            result += f"   {artifact['description']}\n"
        
        return result


if __name__ == "__main__":
    game = QuickGame()
    
    # 快速开始
    print(game.start())
    print("\n修炼中...")
    print(game.cultivate(5))
    print("\n" + game.show_status())
