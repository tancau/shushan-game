#!/usr/bin/env python3
"""
蜀山剑侠传 - 玩家类
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from config import REALMS, INITIAL_STATS, SAVE_DIR
from game.skills import Skill, SkillManager, SkillType, SkillQuality, SkillEffect

# 任务系统类型提示（避免循环导入）
try:
    from game.quest import Quest, QuestManager, QuestStatus, ObjectiveType
except ImportError:
    Quest = None
    QuestManager = None
    QuestStatus = None
    ObjectiveType = None

# 成就系统类型提示（避免循环导入）
try:
    from game.achievement import AchievementManager, Achievement, Title
except ImportError:
    AchievementManager = None
    Achievement = None
    Title = None

# 道心系统
try:
    from game.dao_heart import DaoHeart, DaoHeartType, ActionType, KarmaType
except ImportError:
    DaoHeart = None
    DaoHeartType = None
    ActionType = None
    KarmaType = None


class Player:
    """玩家类 - 修仙者"""
    
    def __init__(self, name: str):
        # 基本信息
        self.name = name
        self.realm = "练气期"
        self.cultivation = 0
        self.spirit_stones = 100  # 灵石
        
        # 属性
        self.stats = INITIAL_STATS.copy()
        self.max_hp = self.stats["生命"]
        self.max_mp = self.stats["真元"]
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp
        
        # 门派
        self.sect = None
        self.sect_contribution = 0
        
        # 法宝
        self.artifacts = []  # 已拥有法宝
        self.equipped_artifact = None  # 装备的法宝
        
        # 功法系统
        self.skill_manager = SkillManager()
        self.learned_skills: Dict[str, int] = {}  # 已学功法ID -> 等级
        self.main_skill_id: Optional[str] = "basic_qigong"  # 主修功法ID
        
        # 初始功法
        self.learned_skills["basic_qigong"] = 1
        
        # 任务系统
        self.quest_manager: Optional[QuestManager] = None  # 任务管理器
        self.active_quests: List[str] = []  # 进行中的任务ID
        self.completed_quests: List[str] = []  # 已完成的任务ID
        self.quest_kills: Dict[str, int] = {}  # 任务击杀计数
        self.quest_collections: Dict[str, int] = {}  # 任务收集计数
        
        # 成就系统
        self.achievement_manager: Optional[AchievementManager] = None  # 成就管理器
        self.completed_achievements: List[str] = []  # 已完成的成就ID
        self.claimed_achievements: List[str] = []  # 已领取的成就ID
        self.unlocked_titles: List[str] = []  # 已解锁的称号ID
        self.current_title_id: Optional[str] = None  # 当前称号ID
        self.total_achievement_points: int = 0  # 成就点数
        
        # 探索记录
        self.explored_locations: List[str] = []  # 已探索的地点
        
        # 战斗统计
        self.battles_total: int = 0  # 总战斗次数
        self.battles_won: int = 0  # 胜利次数
        
        # 位置
        self.location = "峨眉山脚"
        
        # 道心系统
        self.dao_heart: Optional[DaoHeart] = DaoHeart() if DaoHeart else None
        
        # 其他
        self.karma = 0  # 功德/业力（兼容旧版本）
        self.play_time = 0  # 游戏时长（分钟）
        self.created_at = datetime.now().isoformat()
    
    def get_realm_level(self) -> int:
        """获取当前境界等级"""
        return REALMS[self.realm]["level"]
    
    def can_advance_realm(self) -> bool:
        """检查是否可以突破境界"""
        current_level = self.get_realm_level()
        if current_level >= len(REALMS):
            return False
        
        # 找到下一个境界
        for realm_name, realm_info in REALMS.items():
            if realm_info["level"] == current_level + 1:
                return self.cultivation >= realm_info["cultivation_required"]
        
        return False
    
    def advance_realm(self) -> str:
        """突破境界"""
        if not self.can_advance_realm():
            return "修为不足，无法突破"
        
        current_level = self.get_realm_level()
        
        # 找到下一个境界
        for realm_name, realm_info in REALMS.items():
            if realm_info["level"] == current_level + 1:
                self.realm = realm_name
                # 提升属性
                self.stats["生命"] = int(self.stats["生命"] * 1.5)
                self.stats["真元"] = int(self.stats["真元"] * 1.5)
                self.stats["攻击"] = int(self.stats["攻击"] * 1.3)
                self.max_hp = self.stats["生命"]
                self.max_mp = self.stats["真元"]
                self.current_hp = self.max_hp
                self.current_mp = self.max_mp
                
                return f"🎉 恭喜突破至 {realm_name}！{realm_info['description']}"
        
        return "已至最高境界"
    
    # ==================== 功法系统 ====================
    
    def get_main_skill(self) -> Optional[Skill]:
        """获取主修功法对象"""
        if not self.main_skill_id:
            return None
        return self.skill_manager.get_skill(self.main_skill_id)
    
    def get_learned_skill(self, skill_id: str) -> Optional[Skill]:
        """获取已学功法对象"""
        if skill_id not in self.learned_skills:
            return None
        
        skill = self.skill_manager.get_skill(skill_id)
        if skill:
            skill.current_level = self.learned_skills[skill_id]
        return skill
    
    def get_all_learned_skills(self) -> List[Skill]:
        """获取所有已学功法"""
        skills = []
        for skill_id, level in self.learned_skills.items():
            skill = self.skill_manager.get_skill(skill_id)
            if skill:
                skill.current_level = level
                skills.append(skill)
        return skills
    
    def learn_skill(self, skill_id: str) -> dict:
        """学习功法"""
        skill = self.skill_manager.get_skill(skill_id)
        if not skill:
            return {"success": False, "message": f"未知的功法：{skill_id}"}
        
        if skill_id in self.learned_skills:
            return {"success": False, "message": f"已学过此功法"}
        
        current_level = self.get_realm_level()
        required_level = REALMS.get(skill.realm_required, {}).get("level", 1)
        if current_level < required_level:
            return {"success": False, "message": f"境界不足，需要 {skill.realm_required}"}
        
        if skill.prerequisites:
            for prereq in skill.prerequisites:
                if prereq not in self.learned_skills:
                    prereq_skill = self.skill_manager.get_skill(prereq)
                    prereq_name = prereq_skill.name if prereq_skill else prereq
                    return {"success": False, "message": f"需要先学习 {prereq_name}"}
        
        if skill.is_secret and skill.sect != self.sect:
            return {"success": False, "message": "此功法为门派秘传，无法学习"}
        
        self.learned_skills[skill_id] = 1
        
        if skill.skill_type == SkillType.MAIN and not self.main_skill_id:
            self.main_skill_id = skill_id
        
        return {
            "success": True,
            "message": f"习得功法【{skill.name}】！",
            "skill": skill
        }
    
    def set_main_skill(self, skill_id: str) -> dict:
        """设置主修功法"""
        if skill_id not in self.learned_skills:
            return {"success": False, "message": "未学习此功法"}
        
        skill = self.skill_manager.get_skill(skill_id)
        if not skill:
            return {"success": False, "message": "功法不存在"}
        
        if skill.skill_type != SkillType.MAIN:
            return {"success": False, "message": "只能设置主修类功法为主修功法"}
        
        self.main_skill_id = skill_id
        return {
            "success": True,
            "message": f"主修功法已切换为【{skill.name}】"
        }
    
    def upgrade_skill(self, skill_id: str) -> dict:
        """升级功法"""
        if skill_id not in self.learned_skills:
            return {"success": False, "message": "未学习此功法"}
        
        skill = self.skill_manager.get_skill(skill_id)
        if not skill:
            return {"success": False, "message": "功法不存在"}
        
        current_level = self.learned_skills[skill_id]
        if current_level >= skill.max_level:
            return {"success": False, "message": "功法已达到最高等级"}
        
        cost = skill.get_level_up_cost()
        
        if self.spirit_stones < cost["spirit_stones"]:
            return {"success": False, "message": f"灵石不足，需要 {cost['spirit_stones']} 灵石"}
        
        if self.cultivation < cost["cultivation"]:
            return {"success": False, "message": f"修为不足，需要 {cost['cultivation']} 修为"}
        
        self.spirit_stones -= cost["spirit_stones"]
        self.cultivation -= cost["cultivation"]
        self.learned_skills[skill_id] = current_level + 1
        
        return {
            "success": True,
            "message": f"功法【{skill.name}】升至 Lv.{current_level + 1}！",
            "cost": cost,
            "new_level": current_level + 1
        }
    
    def get_skill_bonuses(self) -> Dict[str, float]:
        """获取所有功法的被动加成"""
        bonuses = {}
        
        for skill_id, level in self.learned_skills.items():
            skill = self.skill_manager.get_skill(skill_id)
            if skill:
                skill.current_level = level
                skill_bonuses = skill.get_passive_bonuses()
                
                for name, value in skill_bonuses.items():
                    if name in bonuses:
                        bonuses[name] += value
                    else:
                        bonuses[name] = value
        
        return bonuses
    
    def get_active_skills(self) -> List[Dict]:
        """获取所有可用的主动技能"""
        active_skills = []
        
        for skill_id, level in self.learned_skills.items():
            skill = self.skill_manager.get_skill(skill_id)
            if skill:
                skill.current_level = level
                for effect in skill.get_active_skills():
                    active_skills.append({
                        "skill_name": skill.name,
                        "effect": effect,
                        "level": level
                    })
        
        return active_skills
    
    def get_available_skills(self) -> List[Skill]:
        """获取可学习的功法列表"""
        return self.skill_manager.get_available_skills(
            self.realm,
            list(self.learned_skills.keys()),
            self.sect
        )
    
    # ==================== 修炼系统 ====================
    
    def cultivate(self, method: str = "打坐") -> dict:
        """修炼获取修为"""
        methods = {
            "打坐": {"修为": 10, "真元消耗": 0, "描述": "静心打坐"},
            "吐纳": {"修为": 20, "真元消耗": 5, "描述": "吐纳天地灵气"},
            "悟道": {"修为": 50, "真元消耗": 20, "描述": "参悟天地大道"}
        }
        
        if method not in methods:
            return {"success": False, "message": f"未知的修炼方式：{method}"}
        
        m = methods[method]
        
        if self.current_mp < m["真元消耗"]:
            return {"success": False, "message": "真元不足"}
        
        self.current_mp -= m["真元消耗"]
        
        base_cultivation = m["修为"]
        
        main_skill = self.get_main_skill()
        if main_skill:
            bonus = main_skill.get_cultivation_bonus()
            base_cultivation = int(base_cultivation * bonus)
        
        if self.sect:
            sect_bonus = REALMS.get(self.sect, {}).get("bonus", {}).get("修炼速度", 1.0)
            base_cultivation = int(base_cultivation * sect_bonus)
        
        self.cultivation += base_cultivation
        
        # 记录修炼（用于任务进度）
        self.record_cultivate(method)
        
        result = {
            "success": True,
            "cultivation": base_cultivation,
            "total_cultivation": self.cultivation,
            "message": f"{m['描述']}，获得修为 +{base_cultivation}"
        }
        
        if self.can_advance_realm():
            result["can_advance"] = True
            result["advance_message"] = "修为已足，可以尝试突破境界！"
        
        return result
    
    # ==================== 任务系统 ====================
    
    def init_quest_manager(self, data_path: str = "data/quests.json"):
        """初始化任务管理器"""
        if QuestManager:
            self.quest_manager = QuestManager(data_path)
            self.quest_manager.completed_quests = self.completed_quests.copy()
            for quest_id in self.active_quests:
                if quest_id in self.quest_manager.quests:
                    self.quest_manager.active_quests[quest_id] = self.quest_manager.quests[quest_id]
    
    def accept_quest(self, quest_id: str) -> dict:
        """接取任务"""
        if not self.quest_manager:
            return {"success": False, "message": "任务系统未初始化"}
        
        result = self.quest_manager.accept_quest(quest_id)
        
        if result.get("success"):
            if quest_id not in self.active_quests:
                self.active_quests.append(quest_id)
        
        return result
    
    def complete_quest(self, quest_id: str) -> dict:
        """完成任务"""
        if not self.quest_manager:
            return {"success": False, "message": "任务系统未初始化"}
        
        result = self.quest_manager.complete_quest(quest_id, self)
        
        if result.get("success"):
            if quest_id not in self.completed_quests:
                self.completed_quests.append(quest_id)
            if quest_id in self.active_quests:
                self.active_quests.remove(quest_id)
        
        return result
    
    def abandon_quest(self, quest_id: str) -> dict:
        """放弃任务"""
        if not self.quest_manager:
            return {"success": False, "message": "任务系统未初始化"}
        
        result = self.quest_manager.abandon_quest(quest_id)
        
        if result.get("success"):
            if quest_id in self.active_quests:
                self.active_quests.remove(quest_id)
        
        return result
    
    def get_active_quests(self) -> List[dict]:
        """获取进行中的任务列表"""
        if not self.quest_manager:
            return []
        
        quests = []
        for quest in self.quest_manager.get_active_quests():
            quests.append({
                "id": quest.quest_id,
                "name": quest.name,
                "type": quest.quest_type.value,
                "description": quest.description,
                "progress": quest.get_progress(),
                "is_complete": quest.is_complete()
            })
        
        return quests
    
    def get_available_quests(self) -> List[dict]:
        """获取可接取的任务列表"""
        if not self.quest_manager:
            return []
        
        quests = []
        for quest in self.quest_manager.get_available_quests():
            quests.append({
                "id": quest.quest_id,
                "name": quest.name,
                "type": quest.quest_type.value,
                "description": quest.description,
                "giver": quest.giver_npc
            })
        
        return quests
    
    def record_kill(self, enemy_name: str, count: int = 1):
        """记录击杀（用于任务进度）"""
        if enemy_name not in self.quest_kills:
            self.quest_kills[enemy_name] = 0
        self.quest_kills[enemy_name] += count
        
        if self.quest_manager and ObjectiveType:
            self.quest_manager.update_objective(ObjectiveType.KILL, enemy_name, count)
    
    def record_collection(self, item_name: str, count: int = 1):
        """记录收集（用于任务进度）"""
        if item_name not in self.quest_collections:
            self.quest_collections[item_name] = 0
        self.quest_collections[item_name] += count
        
        if self.quest_manager and ObjectiveType:
            self.quest_manager.update_objective(ObjectiveType.COLLECT, item_name, count)
    
    def record_explore(self, location_name: str):
        """记录探索（用于任务进度）"""
        if self.quest_manager and ObjectiveType:
            self.quest_manager.update_objective(ObjectiveType.EXPLORE, location_name, 1)
    
    def record_dialogue(self, npc_name: str):
        """记录对话（用于任务进度）"""
        if self.quest_manager and ObjectiveType:
            self.quest_manager.update_objective(ObjectiveType.TALK, npc_name, 1)
    
    def record_cultivate(self, method: str):
        """记录修炼（用于任务进度）"""
        if self.quest_manager and ObjectiveType:
            self.quest_manager.update_objective(ObjectiveType.CULTIVATE, method, 1)
    
    # ==================== 成就系统 ====================
    
    def init_achievement_manager(self, data_path: str = "data/achievements.json"):
        """初始化成就管理器"""
        if AchievementManager:
            self.achievement_manager = AchievementManager(data_path)
            # 加载玩家成就状态
            self.achievement_manager.load_state({
                "completed_achievements": self.completed_achievements,
                "claimed_achievements": self.claimed_achievements,
                "unlocked_titles": self.unlocked_titles,
                "current_title": self.current_title_id,
                "total_achievement_points": self.total_achievement_points
            })
    
    def check_achievements(self) -> List[dict]:
        """检查成就进度"""
        if not self.achievement_manager:
            return []
        return self.achievement_manager.check_achievements(self)
    
    def claim_achievement_reward(self, achievement_id: str) -> dict:
        """领取成就奖励"""
        if not self.achievement_manager:
            return {"success": False, "message": "成就系统未初始化"}
        return self.achievement_manager.claim_reward(achievement_id, self)
    
    def get_achievement_summary(self) -> str:
        """获取成就概要"""
        if not self.achievement_manager:
            return "成就系统未初始化"
        return self.achievement_manager.get_achievement_summary_text(self)
    
    def get_completed_achievements(self) -> List[dict]:
        """获取已完成的成就列表"""
        if not self.achievement_manager:
            return []
        achievements = self.achievement_manager.get_completed_achievements()
        return [
            {
                "id": ach.achievement_id,
                "name": ach.name,
                "description": ach.description,
                "rarity": ach.rarity.value,
                "completed_at": ach.completed_at
            }
            for ach in achievements
        ]
    
    def get_unclaimed_achievements(self) -> List[dict]:
        """获取待领取的成就"""
        if not self.achievement_manager:
            return []
        achievements = self.achievement_manager.get_unclaimed_achievements()
        return [
            {
                "id": ach.achievement_id,
                "name": ach.name,
                "rarity": ach.rarity.value
            }
            for ach in achievements
        ]
    
    def set_title(self, title_id: str) -> dict:
        """设置当前称号"""
        if not self.achievement_manager:
            return {"success": False, "message": "成就系统未初始化"}
        result = self.achievement_manager.set_title(title_id)
        if result.get("success"):
            self.current_title_id = title_id
        return result
    
    def remove_title(self) -> dict:
        """取消当前称号"""
        if not self.achievement_manager:
            return {"success": False, "message": "成就系统未初始化"}
        result = self.achievement_manager.remove_title()
        if result.get("success"):
            self.current_title_id = None
        return result
    
    def get_current_title(self) -> Optional[dict]:
        """获取当前称号"""
        if not self.achievement_manager:
            return None
        title = self.achievement_manager.get_current_title()
        if title:
            return {
                "id": title.title_id,
                "name": title.name,
                "description": title.description,
                "bonuses": title.get_bonus_text()
            }
        return None
    
    def get_unlocked_titles(self) -> List[dict]:
        """获取已解锁的称号列表"""
        if not self.achievement_manager:
            return []
        titles = self.achievement_manager.get_unlocked_titles()
        return [
            {
                "id": title.title_id,
                "name": title.name,
                "description": title.description,
                "bonuses": title.get_bonus_text(),
                "rarity": title.rarity.value
            }
            for title in titles
        ]
    
    def get_title_bonuses(self) -> Dict[str, float]:
        """获取当前称号的属性加成"""
        if not self.achievement_manager:
            return {}
        return self.achievement_manager.get_title_bonuses()
    
    def check_quest_completion(self) -> List[dict]:
        """检查任务完成状态"""
        if not self.quest_manager:
            return []
        
        completable = []
        for quest in self.quest_manager.get_active_quests():
            if quest.is_complete():
                completable.append({
                    "id": quest.quest_id,
                    "name": quest.name,
                    "completer_npc": quest.completer_npc
                })
        
        return completable
    
    def get_quest_info(self, quest_id: str) -> Optional[dict]:
        """获取任务详情"""
        if not self.quest_manager:
            return None
        
        quest = self.quest_manager.get_quest_info(quest_id)
        if not quest:
            return None
        
        return {
            "id": quest.quest_id,
            "name": quest.name,
            "type": quest.quest_type.value,
            "description": quest.description,
            "objectives": [
                {
                    "type": obj.objective_type.value,
                    "target": obj.target,
                    "current": obj.current,
                    "required": obj.required,
                    "description": obj.description,
                    "complete": obj.is_complete()
                }
                for obj in quest.objectives
            ],
            "rewards": quest.rewards.to_dict(),
            "progress": quest.get_progress(),
            "status": quest.status.value
        }
    
    # ==================== 道心系统 ====================
    
    def get_dao_heart_info(self) -> dict:
        """获取道心信息"""
        if not self.dao_heart:
            return {"available": False}
        return {
            "available": True,
            **self.dao_heart.get_dao_heart_info()
        }
    
    def add_karma_action(self, action_type: ActionType, description: str = "") -> dict:
        """添加因果行为"""
        if not self.dao_heart or not ActionType:
            return {"success": False, "message": "道心系统未初始化"}
        
        result = self.dao_heart.add_karma(action_type, description)
        
        # 更新兼容性 karma 值
        self.karma = self.dao_heart.merit - self.dao_heart.sin
        
        return result
    
    def get_dao_heart_bonuses(self) -> Dict[str, float]:
        """获取道心系统加成"""
        if not self.dao_heart:
            return {}
        return self.dao_heart.get_merit_bonuses()
    
    def get_dao_heart_penalties(self) -> List[dict]:
        """获取道心系统惩罚"""
        if not self.dao_heart:
            return []
        return self.dao_heart.get_active_penalties()
    
    def get_npc_relation_modifier(self, npc_faction: str) -> int:
        """获取NPC好感度修正"""
        if not self.dao_heart:
            return 0
        return self.dao_heart.get_npc_relation_modifier(npc_faction)
    
    def get_encounter_modifier(self) -> float:
        """获取奇遇概率修正"""
        if not self.dao_heart:
            return 0.0
        return self.dao_heart.get_encounter_modifier()
    
    def get_tribulation_modifier(self) -> dict:
        """获取渡劫修正"""
        if not self.dao_heart:
            return {"success_rate": 0, "difficulty": 0, "heart_demon_strength": 0}
        return self.dao_heart.get_tribulation_modifier()
    
    def get_combat_modifier(self, enemy_type: str) -> dict:
        """获取战斗修正"""
        if not self.dao_heart:
            return {"damage_bonus": 0, "defense_bonus": 0}
        return self.dao_heart.get_combat_modifier(enemy_type)
    
    def get_merit_shop_items(self) -> List[dict]:
        """获取功德商店物品"""
        if not self.dao_heart:
            return []
        return self.dao_heart.get_merit_shop()
    
    def purchase_merit_item(self, item_name: str) -> dict:
        """购买功德物品"""
        if not self.dao_heart:
            return {"success": False, "message": "道心系统未初始化"}
        
        success, message = self.dao_heart.purchase_merit_item(item_name)
        return {"success": success, "message": message}
    
    def reduce_sin(self, amount: int, reason: str = "") -> bool:
        """消除业力"""
        if not self.dao_heart:
            return False
        
        result = self.dao_heart.reduce_sin(amount, reason)
        if result:
            self.karma = self.dao_heart.merit - self.dao_heart.sin
        return result
    
    def get_sin_reduction_methods(self) -> dict:
        """获取消业方式"""
        if not self.dao_heart:
            return {"methods": []}
        return self.dao_heart.can_reduce_sin()
    
    # ==================== 其他系统 ====================
    
    def add_artifact(self, artifact: dict):
        """添加法宝"""
        self.artifacts.append(artifact)
    
    def equip_artifact(self, artifact_name: str) -> bool:
        """装备法宝"""
        for artifact in self.artifacts:
            if artifact["name"] == artifact_name:
                self.equipped_artifact = artifact
                return True
        return False
    
    def join_sect(self, sect_name: str):
        """加入门派"""
        if sect_name in ["峨眉派", "青城派", "昆仑派", "血河教"]:
            self.sect = sect_name
            return True
        return False
    
    def restore(self):
        """恢复生命和真元"""
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp
    
    def to_dict(self) -> dict:
        """转换为字典（用于存档）"""
        return {
            "name": self.name,
            "realm": self.realm,
            "cultivation": self.cultivation,
            "spirit_stones": self.spirit_stones,
            "stats": self.stats,
            "current_hp": self.current_hp,
            "current_mp": self.current_mp,
            "sect": self.sect,
            "sect_contribution": self.sect_contribution,
            "artifacts": self.artifacts,
            "equipped_artifact": self.equipped_artifact,
            "learned_skills": self.learned_skills,
            "main_skill_id": self.main_skill_id,
            "location": self.location,
            "karma": self.karma,
            "play_time": self.play_time,
            "created_at": self.created_at,
            # 任务系统
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests,
            "quest_kills": self.quest_kills,
            "quest_collections": self.quest_collections,
            # 成就系统
            "completed_achievements": self.completed_achievements,
            "claimed_achievements": self.claimed_achievements,
            "unlocked_titles": self.unlocked_titles,
            "current_title_id": self.current_title_id,
            "total_achievement_points": self.total_achievement_points,
            # 探索记录
            "explored_locations": self.explored_locations,
            # 战斗统计
            "battles_total": self.battles_total,
            "battles_won": self.battles_won,
            # 道心系统
            "dao_heart": self.dao_heart.to_dict() if self.dao_heart else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """从字典创建玩家（用于读档）"""
        player = cls(data["name"])
        player.realm = data["realm"]
        player.cultivation = data["cultivation"]
        player.spirit_stones = data["spirit_stones"]
        player.stats = data["stats"]
        player.max_hp = player.stats["生命"]
        player.max_mp = player.stats["真元"]
        player.current_hp = data["current_hp"]
        player.current_mp = data["current_mp"]
        player.sect = data["sect"]
        player.sect_contribution = data["sect_contribution"]
        player.artifacts = data["artifacts"]
        player.equipped_artifact = data["equipped_artifact"]
        
        # 功法系统（兼容旧存档）
        if "learned_skills" in data:
            player.learned_skills = data["learned_skills"]
        else:
            old_skills = data.get("skills", ["基础吐纳法"])
            player.learned_skills = {}
            for skill_name in old_skills:
                skill = player.skill_manager.get_skill_by_name(skill_name)
                if skill:
                    player.learned_skills[skill.id] = 1
        
        if "main_skill_id" in data:
            player.main_skill_id = data["main_skill_id"]
        else:
            old_main = data.get("main_skill", "基础吐纳法")
            skill = player.skill_manager.get_skill_by_name(old_main)
            player.main_skill_id = skill.id if skill else "basic_qigong"
        
        player.location = data["location"]
        player.karma = data["karma"]
        player.play_time = data["play_time"]
        player.created_at = data["created_at"]
        
        # 任务系统（兼容旧存档）
        player.active_quests = data.get("active_quests", [])
        player.completed_quests = data.get("completed_quests", [])
        player.quest_kills = data.get("quest_kills", {})
        player.quest_collections = data.get("quest_collections", {})
        
        # 成就系统（兼容旧存档）
        player.completed_achievements = data.get("completed_achievements", [])
        player.claimed_achievements = data.get("claimed_achievements", [])
        player.unlocked_titles = data.get("unlocked_titles", [])
        player.current_title_id = data.get("current_title_id")
        player.total_achievement_points = data.get("total_achievement_points", 0)
        
        # 探索记录（兼容旧存档）
        player.explored_locations = data.get("explored_locations", [])
        
        # 战斗统计（兼容旧存档）
        player.battles_total = data.get("battles_total", 0)
        player.battles_won = data.get("battles_won", 0)
        
        # 道心系统（兼容旧存档）
        if DaoHeart and "dao_heart" in data and data["dao_heart"]:
            player.dao_heart = DaoHeart.from_dict(data["dao_heart"])
        elif DaoHeart:
            # 旧版本兼容：用 karma 初始化
            player.dao_heart = DaoHeart()
            player.dao_heart.merit = max(0, data.get("karma", 0))
            player.dao_heart.sin = max(0, -data.get("karma", 0))
            player.dao_heart._update_dao_heart_type()
        
        return player
    
    def save(self, slot: int = 1):
        """保存游戏"""
        save_dir = Path(SAVE_DIR)
        save_dir.mkdir(exist_ok=True)
        
        save_file = save_dir / f"save_{slot}.json"
        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, slot: int = 1) -> "Player":
        """读取存档"""
        save_file = Path(SAVE_DIR) / f"save_{slot}.json"
        
        if not save_file.exists():
            return None
        
        with open(save_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def __str__(self) -> str:
        """玩家信息字符串"""
        main_skill_name = "无"
        if self.main_skill_id:
            main_skill = self.get_main_skill()
            if main_skill:
                main_skill_name = f"{main_skill.name} Lv.{self.learned_skills.get(self.main_skill_id, 1)}"
        
        # 道心信息
        dao_heart_str = ""
        if self.dao_heart:
            dao_heart_str = f"\n道心：{self.dao_heart.dao_heart_type.value}（功德:{self.dao_heart.merit} 业力:{self.dao_heart.sin}）"
        
        return f"""
【{self.name}】
境界：{self.realm}
修为：{self.cultivation:,}
灵石：{self.spirit_stones:,}
生命：{self.current_hp}/{self.max_hp}
真元：{self.current_mp}/{self.max_mp}
门派：{self.sect or '散修'}
主修：{main_skill_name}
位置：{self.location}
法宝：{len(self.artifacts)} 件
功法：{len(self.learned_skills)} 种
任务：{len(self.active_quests)} 进行中 / {len(self.completed_quests)} 已完成{dao_heart_str}
        """.strip()
    
    def get_skill_info(self) -> str:
        """获取功法信息"""
        info = "【已学功法】\n"
        info += "─" * 30 + "\n"
        
        if self.main_skill_id:
            main_skill = self.get_main_skill()
            if main_skill:
                level = self.learned_skills.get(self.main_skill_id, 1)
                info += f"主修：{main_skill.name} Lv.{level}\n"
                info += f"      {main_skill.description}\n\n"
        
        info += "已学功法：\n"
        for skill_id, level in self.learned_skills.items():
            if skill_id == self.main_skill_id:
                continue
            skill = self.skill_manager.get_skill(skill_id)
            if skill:
                info += f"  • {skill.name} Lv.{level} [{skill.skill_type.value}]\n"
        
        bonuses = self.get_skill_bonuses()
        if bonuses:
            info += "\n【功法加成】\n"
            info += "─" * 30 + "\n"
            for name, value in bonuses.items():
                info += f"  {name}: +{value:.0%}\n"
        
        return info
    
    def get_quest_summary(self) -> str:
        """获取任务概要"""
        info = "【任务概要】\n"
        info += "─" * 30 + "\n"
        
        if not self.quest_manager:
            info += "任务系统未初始化\n"
            return info
        
        # 进行中的任务
        active = self.get_active_quests()
        if active:
            info += f"进行中 ({len(active)})：\n"
            for quest in active[:5]:  # 最多显示5个
                status = "✓" if quest["is_complete"] else "○"
                info += f"  {status} {quest['name']}\n"
        else:
            info += "暂无进行中的任务\n"
        
        # 可接取的任务
        available = self.get_available_quests()
        if available:
            info += f"\n可接取 ({len(available)})：\n"
            for quest in available[:3]:
                info += f"  • {quest['name']} [{quest['type']}]\n"
        
        # 剧情进度
        progress = self.quest_manager.get_story_progress()
        info += f"\n剧情进度：{progress['completed_main_quests']}/{progress['total_main_quests']} 主线\n"
        
        return info
