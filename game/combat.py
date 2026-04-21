#!/usr/bin/env python3
"""
蜀山剑侠传 - 战斗系统
"""

from typing import List, Dict, Optional
from game.player import Player
from game.artifact import Artifact, ArtifactManager


class Enemy:
    """敌人类"""
    
    def __init__(self, name: str, realm: str, hp: int, attack: int, 
                 defense: int, element: str = None, artifact: Artifact = None):
        self.name = name
        self.realm = realm
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.element = element
        self.artifact = artifact
    
    def take_damage(self, damage: int) -> int:
        """受到伤害"""
        actual_damage = max(1, damage - self.defense)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage
    
    def is_alive(self) -> bool:
        return self.current_hp > 0
    
    def __str__(self):
        return f"{self.name}（{self.realm}） HP: {self.current_hp}/{self.max_hp}"


class CombatSystem:
    """战斗系统"""
    
    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 0
        self.combat_log = []
        self.is_player_turn = True
    
    def player_attack(self, use_artifact: bool = True) -> Dict:
        """
        玩家攻击
        
        Args:
            use_artifact: 是否使用法宝
        
        Returns:
            攻击结果
        """
        result = {
            "action": "攻击",
            "damage": 0,
            "message": ""
        }
        
        # 计算伤害
        if use_artifact and self.player.equipped_artifact:
            artifact = ArtifactManager.get_artifact(self.player.equipped_artifact["name"])
            if artifact:
                damage = ArtifactManager.calculate_damage(
                    attacker_artifact=artifact,
                    defender_element=self.enemy.element,
                    attacker_realm_level=self.player.get_realm_level()
                )
                result["message"] = f"祭出 {artifact.name}，剑光一闪！"
            else:
                damage = self.player.stats["攻击"]
                result["message"] = "一剑刺出！"
        else:
            damage = self.player.stats["攻击"]
            result["message"] = "一剑刺出！"
        
        # 造成伤害
        actual_damage = self.enemy.take_damage(damage)
        result["damage"] = actual_damage
        result["message"] += f" 造成 {actual_damage} 点伤害！"
        
        self.combat_log.append(result)
        
        return result
    
    def player_defend(self) -> Dict:
        """玩家防御"""
        result = {
            "action": "防御",
            "message": "运转真元，形成护盾，防御提升 50%！",
            "defense_bonus": 0.5
        }
        
        self.combat_log.append(result)
        
        return result
    
    def enemy_attack(self) -> Dict:
        """敌人攻击"""
        result = {
            "action": "攻击",
            "damage": 0,
            "message": ""
        }
        
        # 基础伤害
        base_damage = self.enemy.attack
        
        # 如果玩家有法宝
        if self.player.equipped_artifact:
            artifact = ArtifactManager.get_artifact(self.player.equipped_artifact["name"])
            if artifact and artifact.artifact_type == "防御":
                base_damage = int(base_damage * 0.7)
        
        # 应用防御
        actual_damage = max(1, base_damage - self.player.stats["防御"])
        
        # 检查是否防御中
        if self.combat_log and self.combat_log[-1].get("action") == "防御":
            actual_damage = int(actual_damage * 0.5)
        
        self.player.current_hp = max(0, self.player.current_hp - actual_damage)
        
        result["damage"] = actual_damage
        result["message"] = f"{self.enemy.name} 攻击！造成 {actual_damage} 点伤害！"
        
        self.combat_log.append(result)
        
        return result
    
    def check_victory(self) -> Optional[str]:
        """检查战斗结果"""
        if not self.enemy.is_alive():
            return "player"
        if self.player.current_hp <= 0:
            return "enemy"
        return None
    
    def get_rewards(self) -> Dict:
        """获取胜利奖励"""
        import random
        
        rewards = {
            "cultivation": 0,
            "spirit_stones": 0,
            "artifact": None
        }
        
        # 基础奖励
        realm_multiplier = self.player.get_realm_level()
        rewards["cultivation"] = random.randint(50, 150) * realm_multiplier
        rewards["spirit_stones"] = random.randint(10, 50) * realm_multiplier
        
        # 小概率掉落法宝
        if random.random() < 0.1:  # 10% 概率
            artifact_tier = min(self.player.get_realm_level(), 3)
            artifact = ArtifactManager.create_random_artifact(artifact_tier)
            if artifact:
                rewards["artifact"] = artifact
        
        return rewards
    
    def get_status(self) -> str:
        """获取战斗状态"""
        status = f"""
═══════════════════════════════════════
【战斗状态】第 {self.turn} 回合
═══════════════════════════════════════
敌方：{self.enemy}
───────────────────────────────────────
我方：{self.player.name}
境界：{self.player.realm}
生命：{self.player.current_hp}/{self.player.max_hp}
真元：{self.player.current_mp}/{self.player.max_mp}
法宝：{self.player.equipped_artifact['name'] if self.player.equipped_artifact else '无'}
═══════════════════════════════════════
        """.strip()
        
        return status
    
    @staticmethod
    def create_random_enemy(player_level: int) -> Enemy:
        """创建随机敌人"""
        import random
        
        enemies = [
            {
                "name": "山中妖兽",
                "realm": "练气期",
                "hp": 100 + player_level * 20,
                "attack": 10 + player_level * 3,
                "defense": 5 + player_level,
                "element": random.choice(["金", "木", "水", "火", "土"])
            },
            {
                "name": "邪道修士",
                "realm": "筑基期",
                "hp": 300 + player_level * 50,
                "attack": 30 + player_level * 5,
                "defense": 15 + player_level * 2,
                "element": random.choice(["金", "木", "水", "火", "土"])
            },
            {
                "name": "血河教徒",
                "realm": "金丹期",
                "hp": 800 + player_level * 100,
                "attack": 60 + player_level * 8,
                "defense": 30 + player_level * 3,
                "element": "火"
            }
        ]
        
        # 根据玩家境界选择敌人
        enemy_data = random.choice(enemies)
        
        return Enemy(
            name=enemy_data["name"],
            realm=enemy_data["realm"],
            hp=enemy_data["hp"],
            attack=enemy_data["attack"],
            defense=enemy_data["defense"],
            element=enemy_data.get("element")
        )
