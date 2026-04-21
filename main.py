#!/usr/bin/env python3
"""
蜀山剑侠传 - 游戏主程序
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.player import Player
from game.artifact import ArtifactManager
from game.combat import CombatSystem, Enemy
from config import GAME_NAME, VERSION, SECTS, ELEMENTS


class ShushanGame:
    """蜀山剑侠传游戏主类"""
    
    def __init__(self):
        self.player = None
        self.running = False
    
    def show_title(self):
        """显示标题"""
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              ⚔️  {GAME_NAME}  ⚔️                       ║
║                                                           ║
║                  版本：{VERSION}                          ║
║                                                           ║
║           "蜀山万载，剑气纵横三万里"                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """)
    
    def show_main_menu(self):
        """显示主菜单"""
        print("""
【主菜单】
1. 开始新游戏
2. 继续游戏
3. 游戏说明
4. 退出
        """)
    
    def create_character(self):
        """创建角色"""
        print("\n【角色创建】")
        print("=" * 50)
        
        name = input("请输入你的名字：").strip()
        
        if not name:
            print("名字不能为空！")
            return False
        
        # 选择门派
        print("\n请选择门派：")
        print("-" * 50)
        for sect_name, sect_info in SECTS.items():
            print(f"  {sect_name}：{sect_info['description']}")
            print(f"    加成：{sect_info['bonus']}")
            print(f"    位置：{sect_info['location']}")
            print()
        
        sect = input("输入门派名称（或回车选择散修）：").strip()
        
        # 创建玩家
        self.player = Player(name)
        
        if sect in SECTS:
            self.player.join_sect(sect)
            print(f"\n你拜入 {sect}，开始修真之旅...")
        else:
            print("\n你选择成为一名散修，独自踏上修真之路...")
        
        # 给予初始法宝
        initial_artifact = ArtifactManager.get_artifact("青竹剑")
        if initial_artifact:
            self.player.add_artifact(initial_artifact.to_dict())
            self.player.equip_artifact("青竹剑")
            print(f"获得初始法宝：{initial_artifact.name}")
        
        # 保存
        self.player.save()
        print("\n角色创建完成！存档已保存。")
        
        return True
    
    def load_game(self) -> bool:
        """读取存档"""
        self.player = Player.load()
        
        if self.player:
            print(f"\n读取存档成功！")
            print(f"欢迎回来，{self.player.name}！")
            return True
        else:
            print("\n没有找到存档，请开始新游戏。")
            return False
    
    def show_game_menu(self):
        """显示游戏菜单"""
        print(f"""
{self.player}
─────────────────────────────────────────────────────────
【行动】
  1. 修炼    2. 炼丹    3. 探索
  4. 战斗    5. 法宝    6. 状态
  7. 存档    8. 返回主菜单
─────────────────────────────────────────────────────────
        """)
    
    def do_cultivate(self):
        """修炼"""
        print("\n【修炼】")
        print("=" * 50)
        print("1. 打坐（获得 10 修为，无消耗）")
        print("2. 吐纳（获得 20 修为，消耗 5 真元）")
        print("3. 悟道（获得 50 修为，消耗 20 真元）")
        print("4. 尝试突破境界")
        print("0. 返回")
        
        choice = input("\n选择修炼方式：").strip()
        
        if choice == "0":
            return
        
        if choice == "4":
            if self.player.can_advance_realm():
                confirm = input("确认突破？(y/n)：").strip().lower()
                if confirm == 'y':
                    result = self.player.advance_realm()
                    print(f"\n{result}")
            else:
                print("\n修为不足，无法突破！")
            return
        
        methods = {"1": "打坐", "2": "吐纳", "3": "悟道"}
        
        if choice in methods:
            result = self.player.cultivate(methods[choice])
            print(f"\n{result['message']}")
            
            if result.get("can_advance"):
                print(f"\n🌟 {result['advance_message']}")
        else:
            print("无效选择！")
    
    def do_combat(self):
        """战斗"""
        print("\n【战斗】")
        print("=" * 50)
        print("遭遇敌人！")
        
        # 创建敌人
        enemy = CombatSystem.create_random_enemy(self.player.get_realm_level())
        combat = CombatSystem(self.player, enemy)
        
        print(f"敌人：{enemy}")
        
        # 战斗循环
        while True:
            print(combat.get_status())
            
            print("\n【战斗指令】")
            print("1. 攻击  2. 防御  3. 逃跑")
            
            choice = input("选择指令：").strip()
            
            if choice == "1":
                result = combat.player_attack()
                print(f"\n{result['message']}")
                
                # 检查胜利
                winner = combat.check_victory()
                if winner == "player":
                    print("\n🎉 战斗胜利！")
                    rewards = combat.get_rewards()
                    print(f"获得修为：+{rewards['cultivation']}")
                    print(f"获得灵石：+{rewards['spirit_stones']}")
                    
                    self.player.cultivation += rewards["cultivation"]
                    self.player.spirit_stones += rewards["spirit_stones"]
                    
                    if rewards["artifact"]:
                        print(f"🎊 获得法宝：{rewards['artifact'].name}！")
                        self.player.add_artifact(rewards["artifact"].to_dict())
                    
                    break
                elif winner == "enemy":
                    print("\n💀 战斗失败...")
                    self.player.current_hp = 1
                    print("你勉强逃脱，生命值降至 1")
                    break
                
                # 敌人攻击
                enemy_result = combat.enemy_attack()
                print(f"\n{enemy_result['message']}")
                
                if self.player.current_hp <= 0:
                    print("\n💀 战斗失败...")
                    self.player.current_hp = 1
                    break
            
            elif choice == "2":
                result = combat.player_defend()
                print(f"\n{result['message']}")
                
                # 敌人攻击（伤害减半）
                enemy_result = combat.enemy_attack()
                print(f"\n{enemy_result['message']}")
            
            elif choice == "3":
                print("\n逃跑成功！")
                break
            
            combat.turn += 1
    
    def do_artifacts(self):
        """法宝管理"""
        print("\n【法宝】")
        print("=" * 50)
        
        if not self.player.artifacts:
            print("你还没有任何法宝。")
            return
        
        print("你拥有的法宝：")
        for i, artifact in enumerate(self.player.artifacts, 1):
            equipped = "（装备中）" if (self.player.equipped_artifact and 
                                       self.player.equipped_artifact["name"] == artifact["name"]) else ""
            print(f"  {i}. {artifact['name']}{equipped}")
            print(f"     类型：{artifact['artifact_type']}  五行：{artifact['element']}")
            print(f"     威力：{artifact['power']}  速度：{artifact['speed']}")
            print(f"     {artifact['description']}")
            print()
        
        choice = input("输入编号装备法宝（0返回）：").strip()
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.artifacts):
                artifact_name = self.player.artifacts[idx]["name"]
                if self.player.equip_artifact(artifact_name):
                    print(f"\n已装备 {artifact_name}！")
            else:
                print("无效编号！")
        except ValueError:
            print("请输入数字！")
    
    def show_status(self):
        """显示详细状态"""
        print(f"""
═══════════════════════════════════════════════════════════
【角色状态】
═══════════════════════════════════════════════════════════
{self.player}

【功法】
主修：{self.player.main_skill}
已学：{', '.join(self.player.skills)}

【功德/业力】：{self.player.karma}
【游戏时长】：{self.player.play_time} 分钟
═══════════════════════════════════════════════════════════
        """)
    
    def run(self):
        """运行游戏"""
        self.show_title()
        
        while True:
            if not self.player:
                self.show_main_menu()
                choice = input("请选择：").strip()
                
                if choice == "1":
                    if self.create_character():
                        self.game_loop()
                elif choice == "2":
                    if self.load_game():
                        self.game_loop()
                elif choice == "3":
                    self.show_help()
                elif choice == "4":
                    print("\n感谢游玩！再见！")
                    break
                else:
                    print("无效选择！")
            else:
                self.game_loop()
    
    def game_loop(self):
        """游戏主循环"""
        self.running = True
        
        while self.running:
            self.show_game_menu()
            choice = input("请选择：").strip()
            
            if choice == "1":
                self.do_cultivate()
            elif choice == "2":
                print("\n炼丹功能开发中...")
            elif choice == "3":
                print("\n探索功能开发中...")
            elif choice == "4":
                self.do_combat()
            elif choice == "5":
                self.do_artifacts()
            elif choice == "6":
                self.show_status()
            elif choice == "7":
                self.player.save()
                print("\n存档成功！")
            elif choice == "8":
                self.player = None
                self.running = False
            else:
                print("无效选择！")
            
            # 恢复真元
            if self.player and self.player.current_mp < self.player.max_mp:
                self.player.current_mp = min(
                    self.player.max_mp,
                    self.player.current_mp + 5
                )
    
    def show_help(self):
        """显示帮助"""
        print(f"""
═══════════════════════════════════════════════════════════
【游戏说明】
═══════════════════════════════════════════════════════════

《蜀山剑侠传》是一款文字修仙游戏，基于还珠楼主的经典小说改编。

【游戏目标】
修炼提升境界，收集法宝，探索蜀山世界，最终飞升成仙。

【修炼系统】
- 境界：练气 → 筑基 → 金丹 → 元婴 → 化神 → 合体 → 渡劫
- 每个境界需要足够的修为才能突破

【法宝系统】
- 五行：金木水火土，相生相克
- 类型：飞剑、防御、攻击、辅助、特殊
- 品阶：1-5级，越高越强

【战斗系统】
- 回合制策略战斗
- 法宝克制、五行相克
- 境界压制

【五行相克】
{chr(10).join([f"  {k} 克制 {v['克制']}，被 {v['被克']} 克制" for k, v in ELEMENTS.items()])}

═══════════════════════════════════════════════════════════
        """)


def main():
    """主函数"""
    game = ShushanGame()
    game.run()


if __name__ == "__main__":
    main()
