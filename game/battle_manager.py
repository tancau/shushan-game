from .combat import Combat
from .enemy import Enemy

class BattleManager:
    def __init__(self):
        self.current_combat = None
    
    def start_battle(self, player, enemy_configs):
        enemies = []
        for config in enemy_configs:
            enemy = Enemy(
                name=config["name"],
                level=config["level"],
                hp=config["hp"],
                attack=config["attack"],
                defense=config["defense"],
                speed=config["speed"]
            )
            enemies.append(enemy)
        self.current_combat = Combat(player, enemies)
        return self.current_combat.start_combat()
    
    def process_action(self, action, target_index, skill_name=None):
        if not self.current_combat:
            return {"error": "No active combat"}
        
        # 处理玩家行动
        player_result = self.current_combat.player_action(action, target_index, skill_name)
        
        # 检查战斗是否结束
        combat_end = self.current_combat.check_combat_end()
        if combat_end:
            return {
                **player_result,
                "combat_end": combat_end
            }
        
        # 处理敌人行动
        enemy_results = []
        for enemy in self.current_combat.enemies:
            if enemy.hp > 0:
                enemy_result = self.current_combat.enemy_action(enemy)
                enemy_results.append(enemy_result)
                
                # 检查战斗是否结束
                combat_end = self.current_combat.check_combat_end()
                if combat_end:
                    return {
                        **player_result,
                        "enemy_results": enemy_results,
                        "combat_end": combat_end
                    }
        
        return {
            **player_result,
            "enemy_results": enemy_results
        }
    
    def get_combat_state(self):
        if not self.current_combat:
            return {"error": "No active combat"}
        return self.current_combat.get_combat_state()
