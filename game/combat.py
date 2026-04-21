#!/usr/bin/env python3
"""
蜀山剑侠传 - 战斗系统（含阵法）
"""

from typing import List, Dict, Optional
import random
from game.player import Player
from game.artifact import Artifact, ArtifactManager
from game.formation import (
    Formation, FormationManager, FormationType, 
    FormationCombatSystem, ActiveFormation
)


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
        
        # 状态效果
        self.status_effects: Dict[str, Dict] = {}
    
    def take_damage(self, damage: int) -> int:
        """受到伤害"""
        actual_damage = max(1, damage - self.defense)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage
    
    def apply_status(self, status_type: str, value: float, duration: int) -> None:
        """应用状态效果"""
        self.status_effects[status_type] = {
            "value": value,
            "duration": duration
        }
    
    def process_status_effects(self) -> List[Dict]:
        """处理状态效果"""
        results = []
        to_remove = []
        
        for status_type, data in self.status_effects.items():
            result = {
                "type": status_type,
                "value": data["value"],
                "duration": data["duration"]
            }
            
            if status_type == "dot":
                damage = int(data["value"])
                self.current_hp = max(0, self.current_hp - damage)
                result["damage"] = damage
            
            elif status_type == "slow":
                result["effect"] = f"行动速度降低 {int(data['value']*100)}%"
            
            elif status_type == "freeze":
                result["effect"] = "被冰封，无法行动"
            
            elif status_type == "paralyze":
                result["effect"] = "被麻痹，无法行动"
            
            elif status_type == "confuse":
                result["effect"] = "陷入混乱"
            
            results.append(result)
            
            data["duration"] -= 1
            if data["duration"] <= 0:
                to_remove.append(status_type)
        
        for status in to_remove:
            del self.status_effects[status]
        
        return results
    
    def is_stunned(self) -> bool:
        """检查是否被控制"""
        return any(
            s in self.status_effects 
            for s in ["freeze", "paralyze", "confuse"]
        )
    
    def is_alive(self) -> bool:
        return self.current_hp > 0
    
    def __str__(self):
        status_str = ""
        if self.status_effects:
            status_str = f" [{', '.join(self.status_effects.keys())}]"
        return f"{self.name}（{self.realm}） HP: {self.current_hp}/{self.max_hp}{status_str}"


class CombatSystem:
    """战斗系统（含阵法）"""
    
    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 0
        self.combat_log = []
        self.is_player_turn = True
        
        # 阵法系统
        self.formation_system = FormationCombatSystem(self)
        self.player_defending = False
        
        # 玩家学习过的阵法 {阵法ID: 等级}
        self.player_formations: Dict[str, int] = getattr(player, 'learned_formations', {})
    
    def setup_formation(self, formation_id: str) -> Dict:
        """
        布设阵法
        
        Args:
            formation_id: 阵法ID
        
        Returns:
            布设结果
        """
        # 检查是否学过此阵法
        formation_level = self.player_formations.get(formation_id, 0)
        if formation_level == 0:
            return {"success": False, "message": "尚未学习此阵法"}
        
        result = self.formation_system.setup_formation(
            formation_id=formation_id,
            formation_level=formation_level,
            player_mp=self.player.current_mp,
            player_realm_level=self.player.get_realm_level()
        )
        
        if result["success"]:
            # 扣除真元
            self.player.current_mp -= result["mp_cost"]
        
        return result
    
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
            "message": "",
            "formation_damage": 0
        }
        
        # 阵法伤害
        formation_damage = self.formation_system.get_formation_attack_damage(self.enemy.element)
        if formation_damage > 0:
            result["formation_damage"] = formation_damage
            actual_formation_damage = self.enemy.take_damage(formation_damage)
            result["message"] += f"阵法造成 {actual_formation_damage} 点伤害！\n"
        
        # 困敌阵效果
        if self.formation_system.has_trap_formation():
            trap_effects = self.formation_system.get_trap_effects()
            for effect in trap_effects:
                if random.random() < effect["chance"]:
                    self.enemy.apply_status(effect["type"], effect.get("value", 0), effect["duration"])
                    result["message"] += f"阵法效果【{effect['name']}】生效！\n"
        
        # 计算法宝/普通伤害
        if use_artifact and self.player.equipped_artifact:
            artifact = ArtifactManager.get_artifact(self.player.equipped_artifact["name"])
            if artifact:
                damage = ArtifactManager.calculate_damage(
                    attacker_artifact=artifact,
                    defender_element=self.enemy.element,
                    attacker_realm_level=self.player.get_realm_level()
                )
                result["message"] += f"祭出 {artifact.name}，剑光一闪！"
            else:
                damage = self.player.stats["攻击"]
                result["message"] += "一剑刺出！"
        else:
            damage = self.player.stats["攻击"]
            result["message"] += "一剑刺出！"
        
        # 造成伤害
        actual_damage = self.enemy.take_damage(damage)
        result["damage"] = actual_damage
        result["message"] += f" 造成 {actual_damage} 点伤害！"
        
        self.combat_log.append(result)
        self.player_defending = False
        
        return result
    
    def player_defend(self) -> Dict:
        """玩家防御"""
        result = {
            "action": "防御",
            "message": "运转真元，形成护盾，防御提升 50%！",
            "defense_bonus": 0.5
        }
        
        self.combat_log.append(result)
        self.player_defending = True
        
        return result
    
    def enemy_attack(self) -> Dict:
        """敌人攻击"""
        result = {
            "action": "攻击",
            "damage": 0,
            "message": "",
            "formation_absorbed": 0
        }
        
        # 检查敌人是否被控制
        if self.enemy.is_stunned():
            status = self.enemy.status_effects
            stun_type = next(s for s in ["freeze", "paralyze", "confuse"] if s in status)
            result["message"] = f"{self.enemy.name} 被【{stun_type}】控制，无法行动！"
            self.combat_log.append(result)
            return result
        
        # 处理敌人状态效果
        status_results = self.enemy.process_status_effects()
        for sr in status_results:
            if sr["type"] == "dot":
                result["message"] += f"{self.enemy.name} 受到灼烧伤害 {sr['damage']} 点！\n"
        
        # 基础伤害
        base_damage = self.enemy.attack
        
        # 检查减速效果
        if "slow" in self.enemy.status_effects:
            base_damage = int(base_damage * (1 - self.enemy.status_effects["slow"]["value"]))
        
        # 如果玩家有防御法宝
        if self.player.equipped_artifact:
            artifact = ArtifactManager.get_artifact(self.player.equipped_artifact["name"])
            if artifact and artifact.artifact_type == "防御":
                base_damage = int(base_damage * 0.7)
        
        # 阵法护盾吸收
        formation_defense = self.formation_system.get_formation_defense()
        if formation_defense > 0:
            break_result = self.formation_system.attack_formation(base_damage, None)
            result["formation_absorbed"] = break_result["damage_absorbed"]
            base_damage -= break_result["damage_absorbed"]
            
            if break_result["formations_broken"]:
                result["message"] += f"阵法【{', '.join(break_result['formations_broken'])}】被击破！\n"
            
            if break_result["counter_damage"] > 0:
                counter = self.enemy.take_damage(break_result["counter_damage"])
                result["message"] += f"破阵反噬，敌人受到 {counter} 点伤害！\n"
        
        # 应用防御
        actual_damage = max(1, base_damage - self.player.stats["防御"])
        
        # 检查是否防御中
        if self.player_defending:
            actual_damage = int(actual_damage * 0.5)
        
        self.player.current_hp = max(0, self.player.current_hp - actual_damage)
        
        result["damage"] = actual_damage
        result["message"] += f"{self.enemy.name} 攻击！造成 {actual_damage} 点伤害！"
        
        self.combat_log.append(result)
        
        return result
    
    def process_turn_end(self) -> Dict:
        """
        处理回合结束效果
        
        Returns:
            回合结束效果
        """
        result = {
            "formation_effects": [],
            "mp_cost": 0,
            "mp_regen": 0
        }
        
        # 处理阵法回合效果
        formation_results = self.formation_system.process_formations_turn()
        
        for fr in formation_results:
            result["mp_cost"] += fr.get("mp_cost", 0)
            
            for effect in fr.get("effects", []):
                result["formation_effects"].append(effect)
                
                if effect["type"] == "mp_drain":
                    self.player.current_mp = max(0, self.player.current_mp - effect["value"])
                elif effect["type"] == "mp_regen":
                    result["mp_regen"] += effect["value"]
        
        # 应用真元恢复
        if result["mp_regen"] > 0:
            self.player.current_mp = min(
                self.player.max_mp, 
                self.player.current_mp + result["mp_regen"]
            )
        
        # 扣除阵法维持真元
        if result["mp_cost"] > 0:
            self.player.current_mp = max(0, self.player.current_mp - result["mp_cost"])
        
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
        rewards = {
            "cultivation": 0,
            "spirit_stones": 0,
            "artifact": None,
            "formation_exp": {}
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
        
        # 阵法经验
        for formation_id in self.player_formations:
            rewards["formation_exp"][formation_id] = random.randint(5, 15)
        
        return rewards
    
    def get_status(self) -> str:
        """获取战斗状态"""
        status_lines = [
            "═══════════════════════════════════════",
            f"【战斗状态】第 {self.turn} 回合",
            "═══════════════════════════════════════",
            f"敌方：{self.enemy}",
            "───────────────────────────────────────",
            f"我方：{self.player.name}",
            f"境界：{self.player.realm}",
            f"生命：{self.player.current_hp}/{self.player.max_hp}",
            f"真元：{self.player.current_mp}/{self.player.max_mp}",
            f"法宝：{self.player.equipped_artifact['name'] if self.player.equipped_artifact else '无'}",
        ]
        
        # 阵法状态
        formation_status = self.formation_system.get_status_text()
        if formation_status != "无激活阵法":
            status_lines.append("───────────────────────────────────────")
            status_lines.append(formation_status)
        
        status_lines.append("═══════════════════════════════════════")
        
        return "\n".join(status_lines)
    
    def get_available_formations(self) -> List[Dict]:
        """获取可用阵法列表"""
        formations = []
        
        for formation_id, level in self.player_formations.items():
            formation = FormationManager.get_formation(formation_id)
            if formation:
                setup_cost, turn_cost = formation.get_mp_cost(level)
                formations.append({
                    "id": formation_id,
                    "name": formation.name,
                    "type": formation.type.value,
                    "level": level,
                    "setup_cost": setup_cost,
                    "turn_cost": turn_cost,
                    "can_use": self.player.current_mp >= setup_cost
                })
        
        return formations
    
    @staticmethod
    def create_random_enemy(player_level: int) -> Enemy:
        """创建随机敌人"""
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


def demo_formation_combat():
    """演示阵法战斗"""
    from game.player import Player
    
    # 创建玩家
    player = Player("剑心")
    player.learned_formations = {
        "jinguang_zhen": 3,
        "liehuo_zhen": 2,
        "hushen_zhen": 1
    }
    
    # 创建敌人
    enemy = Enemy(
        name="山中妖兽",
        realm="练气期",
        hp=200,
        attack=25,
        defense=10,
        element="木"
    )
    
    # 创建战斗系统
    combat = CombatSystem(player, enemy)
    
    print("=" * 50)
    print("阵法战斗演示")
    print("=" * 50)
    print(combat.get_status())
    
    # 显示可用阵法
    print("\n可用阵法:")
    for f in combat.get_available_formations():
        print(f"  - {f['name']} Lv.{f['level']} | 布设: {f['setup_cost']}真元 | 维持: {f['turn_cost']}/回合")
    
    # 布设阵法
    print("\n布设【金光阵】...")
    result = combat.setup_formation("jinguang_zhen")
    print(result["message"])
    
    # 布设攻击阵
    print("\n布设【烈火阵】...")
    result = combat.setup_formation("liehuo_zhen")
    print(result["message"])
    
    print("\n" + combat.get_status())
    
    # 战斗
    print("\n【第1回合】")
    combat.turn = 1
    attack_result = combat.player_attack()
    print(attack_result["message"])
    
    # 敌人攻击
    enemy_result = combat.enemy_attack()
    print(enemy_result["message"])
    
    # 回合结束
    turn_result = combat.process_turn_end()
    if turn_result["mp_cost"] > 0:
        print(f"阵法维持消耗 {turn_result['mp_cost']} 点真元")
    
    print("\n" + combat.get_status())


if __name__ == "__main__":
    demo_formation_combat()
