#!/usr/bin/env python3
"""
蜀山剑侠传 - 交互式游戏
"""

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.player import Player
from game.artifact import ArtifactManager
from game.combat import CombatSystem, Enemy
from config import REALMS


class InteractiveGame:
    """交互式游戏"""
    
    def __init__(self):
        self.player = None
        self.load()
    
    def load(self):
        """加载游戏"""
        self.player = Player.load()
        if not self.player:
            # 创建新角色
            self.player = Player("tancau")
            self.player.join_sect("峨眉派")
            
            artifact = ArtifactManager.get_artifact("青竹剑")
            if artifact:
                self.player.add_artifact(artifact.to_dict())
                self.player.equip_artifact("青竹剑")
            
            self.player.save()
    
    def save(self):
        """保存游戏"""
        self.player.save()
    
    def status(self):
        """状态"""
        next_realm = None
        for realm_name, realm_info in REALMS.items():
            if realm_info["level"] == self.player.get_realm_level() + 1:
                next_realm = realm_name
                next_required = realm_info["cultivation_required"]
                break
        
        progress = ""
        if next_realm:
            progress = f" (下一境界：{next_realm}，需要 {next_required:,} 修为)"
        
        return f"""
═══════════════════════════════════════
【{self.player.name}】{progress}
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
    
    def cultivate(self, method="吐纳", times=1):
        """修炼"""
        results = []
        
        for i in range(times):
            result = self.player.cultivate(method)
            results.append(result['message'])
            
            if result.get('can_advance'):
                results.append(f"🌟 {result['advance_message']}")
        
        # 恢复真元
        if self.player.current_mp < self.player.max_mp:
            self.player.current_mp = min(
                self.player.max_mp,
                self.player.current_mp + 10 * times
            )
        
        self.save()
        
        return "\n".join(results)
    
    def advance(self):
        """突破"""
        if self.player.can_advance_realm():
            result = self.player.advance_realm()
            self.save()
            return f"🎉 {result}"
        else:
            # 计算需要多少修为
            next_required = 0
            next_realm = ""
            
            realm_list = list(REALMS.items())
            for i, (realm_name, realm_info) in enumerate(realm_list):
                if realm_name == self.player.realm and i + 1 < len(realm_list):
                    next_realm = realm_list[i + 1][0]
                    next_required = realm_list[i + 1][1]["cultivation_required"]
                    break
            
            if next_required > 0:
                need = next_required - self.player.cultivation
                return f"❌ 修为不足！还需要 {need:,} 修为才能突破到 {next_realm}"
            else:
                return "✅ 已达最高境界！"
    
    def battle(self):
        """战斗"""
        enemy = CombatSystem.create_random_enemy(self.player.get_realm_level())
        combat = CombatSystem(self.player, enemy)
        
        result = f"⚔️ 遭遇 {enemy.name}（{enemy.realm}）！\n"
        result += "═" * 40 + "\n"
        
        turn = 0
        while turn < 20:
            turn += 1
            
            # 玩家攻击
            attack = combat.player_attack()
            result += f"[{turn}] {attack['message']}\n"
            
            # 检查胜负
            winner = combat.check_victory()
            if winner == "player":
                rewards = combat.get_rewards()
                result += "\n🎉 胜利！\n"
                result += f"  修为 +{rewards['cultivation']}\n"
                result += f"  灵石 +{rewards['spirit_stones']}\n"
                
                self.player.cultivation += rewards["cultivation"]
                self.player.spirit_stones += rewards["spirit_stones"]
                
                if rewards["artifact"]:
                    result += f"  🎊 获得法宝：{rewards['artifact'].name}！\n"
                    self.player.add_artifact(rewards["artifact"].to_dict())
                
                # 恢复生命
                self.player.current_hp = self.player.max_hp
                self.save()
                return result
            
            # 敌人攻击
            enemy_atk = combat.enemy_attack()
            result += f"  敌方反击：{enemy_atk['damage']} 伤害\n"
            
            if self.player.current_hp <= 0:
                self.player.current_hp = 1
                result += "\n💀 战败逃脱\n"
                self.save()
                return result
        
        result += "\n战斗超时\n"
        self.save()
        return result
    
    def artifacts(self):
        """法宝列表"""
        if not self.player.artifacts:
            return "暂无法宝"
        
        result = "【法宝列表】\n" + "─" * 40 + "\n"
        
        for i, art in enumerate(self.player.artifacts, 1):
            equipped = " ⚔️" if (self.player.equipped_artifact and 
                                self.player.equipped_artifact["name"] == art["name"]) else ""
            result += f"{i}. {art['name']}{equipped}\n"
            result += f"   威力:{art['power']} 五行:{art['element']}\n"
        
        return result
    
    def equip(self, index):
        """装备法宝"""
        if 1 <= index <= len(self.player.artifacts):
            artifact_name = self.player.artifacts[index - 1]["name"]
            if self.player.equip_artifact(artifact_name):
                self.save()
                return f"✅ 已装备 {artifact_name}"
        return "❌ 无效编号"


def execute_command(command):
    """执行游戏命令"""
    game = InteractiveGame()
    
    parts = command.split()
    cmd = parts[0].lower() if parts else ""
    
    if cmd == "状态":
        return game.status()
    
    elif cmd == "修炼":
        times = int(parts[1]) if len(parts) > 1 else 1
        times = min(times, 100)  # 最多100次
        return game.cultivate("吐纳", times)
    
    elif cmd == "突破":
        return game.advance()
    
    elif cmd == "战斗":
        return game.battle()
    
    elif cmd == "法宝":
        return game.artifacts()
    
    elif cmd == "装备":
        if len(parts) > 1:
            index = int(parts[1])
            return game.equip(index)
        return "用法：装备 <编号>"
    
    elif cmd == "恢复":
        game.player.current_hp = game.player.max_hp
        game.player.current_mp = game.player.max_mp
        game.save()
        return "✅ 生命和真元已恢复"
    
    else:
        return """
可用命令：
  状态 - 查看角色状态
  修炼 [次数] - 修炼获得修为（默认1次）
  突破 - 突破境界
  战斗 - 与敌人战斗
  法宝 - 查看法宝列表
  装备 <编号> - 装备法宝
  恢复 - 恢复生命和真元
        """.strip()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        print(execute_command(command))
    else:
        print(execute_command("状态"))
