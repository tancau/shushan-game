from .player import Player
from .enemy import Enemy
import random

class Combat:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.combat_log = []
        self.turn_order = []
        self.current_turn = 0
        self.combo = 0
        self.initialize_turn_order()
    
    def initialize_turn_order(self):
        # 初始化回合顺序，根据速度排序
        all_characters = [self.player] + self.enemies
        self.turn_order = sorted(all_characters, key=lambda x: x.speed, reverse=True)
    
    def start_combat(self):
        self.combat_log.append("战斗开始！")
        return self.get_combat_state()
    
    def player_action(self, action, target_index, skill_name=None):
        if action == "attack":
            target = self.enemies[target_index]
            damage = self.player.attack_enemy(target)
            self.combo += 1
            log = f"{self.player.name}使用普通攻击，造成{damage}点伤害！"
            self.combat_log.append(log)
            return {
                "damage": damage,
                "critical": False,
                "enemy_hp": target.hp,
                "combo": self.combo,
                "log": log
            }
        elif action == "skill":
            target = self.enemies[target_index]
            damage = self.player.use_skill(skill_name, target)
            if damage > 0:
                self.combo += 1
                log = f"{self.player.name}使用{skill_name}，造成{damage}点伤害！"
            else:
                log = f"{self.player.name}使用{skill_name}失败，法力不足！"
            self.combat_log.append(log)
            return {
                "damage": damage,
                "critical": False,
                "enemy_hp": target.hp if damage > 0 else target.hp,
                "combo": self.combo if damage > 0 else 0,
                "log": log
            }
        return {}
    
    def enemy_action(self, enemy):
        damage = enemy.attack_player(self.player)
        log = f"{enemy.name}攻击{self.player.name}，造成{damage}点伤害！"
        self.combat_log.append(log)
        return {
            "damage": damage,
            "player_hp": self.player.hp,
            "log": log
        }
    
    def check_combat_end(self):
        # 检查战斗是否结束
        if self.player.hp <= 0:
            return "player_defeated"
        for enemy in self.enemies:
            if enemy.hp > 0:
                return None
        return "enemies_defeated"
    
    def get_combat_state(self):
        return {
            "player": self.player.to_dict(),
            "enemies": [enemy.to_dict() for enemy in self.enemies],
            "combat_log": self.combat_log,
            "combo": self.combo
        }
