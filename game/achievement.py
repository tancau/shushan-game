#!/usr/bin/env python3
"""
蜀山剑侠传 - 成就系统
包含成就类、成就管理器、称号系统、奖励发放
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
import json
from pathlib import Path


class AchievementCategory(Enum):
    """成就分类"""
    CULTIVATION = "修炼"      # 修炼相关
    COMBAT = "战斗"          # 战斗相关
    EXPLORATION = "探索"     # 探索相关
    COLLECTION = "收集"      # 收集相关
    SOCIAL = "社交"         # 社交相关
    SPECIAL = "特殊"        # 特殊成就


class AchievementRarity(Enum):
    """成就稀有度"""
    COMMON = "普通"
    RARE = "稀有"
    EPIC = "史诗"
    LEGENDARY = "传说"


class AchievementStatus(Enum):
    """成就状态"""
    LOCKED = "未解锁"       # 条件未满足
    IN_PROGRESS = "进行中"  # 已触发但未完成
    COMPLETED = "已完成"    # 已完成
    CLAIMED = "已领取"      # 已领取奖励


@dataclass
class AchievementReward:
    """成就奖励"""
    achievement_points: int = 0           # 成就点数
    spirit_stones: int = 0                # 灵石
    cultivation: int = 0                  # 修为
    title: Optional[str] = None           # 称号
    artifacts: List[str] = field(default_factory=list)  # 法宝
    skills: List[str] = field(default_factory=list)     # 功法
    stat_bonuses: Dict[str, float] = field(default_factory=dict)  # 属性加成
    
    def to_dict(self) -> dict:
        return {
            "achievement_points": self.achievement_points,
            "spirit_stones": self.spirit_stones,
            "cultivation": self.cultivation,
            "title": self.title,
            "artifacts": self.artifacts,
            "skills": self.skills,
            "stat_bonuses": self.stat_bonuses
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AchievementReward":
        return cls(
            achievement_points=data.get("achievement_points", 0),
            spirit_stones=data.get("spirit_stones", 0),
            cultivation=data.get("cultivation", 0),
            title=data.get("title"),
            artifacts=data.get("artifacts", []),
            skills=data.get("skills", []),
            stat_bonuses=data.get("stat_bonuses", {})
        )


@dataclass
class AchievementCondition:
    """成就条件"""
    condition_type: str      # 条件类型：realm_reach, kill_count, explore, collect, etc.
    target: str              # 目标名称
    required: int = 1        # 需求数量
    description: str = ""    # 条件描述
    
    def check(self, player_data: dict) -> bool:
        """检查条件是否满足"""
        if self.condition_type == "realm_reach":
            realm_levels = {
                "练气期": 1, "筑基期": 2, "金丹期": 3, "元婴期": 4,
                "化神期": 5, "合体期": 6, "渡劫期": 7
            }
            player_level = realm_levels.get(player_data.get("realm", "练气期"), 1)
            return player_level >= self.required
        
        elif self.condition_type == "cultivation_reach":
            return player_data.get("cultivation", 0) >= self.required
        
        elif self.condition_type == "spirit_stones_reach":
            return player_data.get("spirit_stones", 0) >= self.required
        
        elif self.condition_type == "kill_count":
            kills = player_data.get("quest_kills", {})
            return kills.get(self.target, 0) >= self.required
        
        elif self.condition_type == "explore":
            explored = player_data.get("explored_locations", [])
            return self.target in explored
        
        elif self.condition_type == "artifact_count":
            return len(player_data.get("artifacts", [])) >= self.required
        
        elif self.condition_type == "skill_count":
            return len(player_data.get("learned_skills", [])) >= self.required
        
        elif self.condition_type == "quest_complete":
            completed = player_data.get("completed_quests", [])
            return len(completed) >= self.required
        
        elif self.condition_type == "sect_join":
            return player_data.get("sect") == self.target
        
        elif self.condition_type == "karma_reach":
            karma = player_data.get("karma", 0)
            if self.required > 0:
                return karma >= self.required
            else:
                return karma <= self.required
        
        elif self.condition_type == "play_time":
            return player_data.get("play_time", 0) >= self.required
        
        elif self.condition_type == "win_rate":
            battles = player_data.get("battles_total", 0)
            wins = player_data.get("battles_won", 0)
            if battles == 0:
                return False
            return (wins / battles) >= (self.required / 100)
        
        return False
    
    def get_progress(self, player_data: dict) -> tuple:
        """获取进度 (当前, 目标)"""
        if self.condition_type == "realm_reach":
            realm_levels = {
                "练气期": 1, "筑基期": 2, "金丹期": 3, "元婴期": 4,
                "化神期": 5, "合体期": 6, "渡劫期": 7
            }
            current = realm_levels.get(player_data.get("realm", "练气期"), 1)
            return (current, self.required)
        
        elif self.condition_type == "cultivation_reach":
            return (player_data.get("cultivation", 0), self.required)
        
        elif self.condition_type == "spirit_stones_reach":
            return (player_data.get("spirit_stones", 0), self.required)
        
        elif self.condition_type == "kill_count":
            kills = player_data.get("quest_kills", {})
            return (kills.get(self.target, 0), self.required)
        
        elif self.condition_type == "artifact_count":
            return (len(player_data.get("artifacts", [])), self.required)
        
        elif self.condition_type == "skill_count":
            return (len(player_data.get("learned_skills", [])), self.required)
        
        elif self.condition_type == "quest_complete":
            return (len(player_data.get("completed_quests", [])), self.required)
        
        elif self.condition_type == "karma_reach":
            return (abs(player_data.get("karma", 0)), abs(self.required))
        
        elif self.condition_type == "play_time":
            return (player_data.get("play_time", 0), self.required)
        
        return (0, self.required)
    
    def to_dict(self) -> dict:
        return {
            "condition_type": self.condition_type,
            "target": self.target,
            "required": self.required,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AchievementCondition":
        return cls(
            condition_type=data["condition_type"],
            target=data.get("target", ""),
            required=data.get("required", 1),
            description=data.get("description", "")
        )


@dataclass
class Achievement:
    """成就"""
    achievement_id: str
    name: str
    description: str
    category: AchievementCategory
    rarity: AchievementRarity
    conditions: List[AchievementCondition]
    rewards: AchievementReward
    prerequisites: List[str] = field(default_factory=list)  # 前置成就ID
    status: AchievementStatus = AchievementStatus.LOCKED
    progress: int = 0           # 当前进度
    completed_at: Optional[str] = None  # 完成时间
    hidden: bool = False        # 是否隐藏（未完成前不显示详情）
    
    def is_available(self, completed_achievements: List[str]) -> bool:
        """检查成就是否可触发"""
        return all(pre in completed_achievements for pre in self.prerequisites)
    
    def check_completion(self, player_data: dict) -> bool:
        """检查成就是否完成"""
        return all(cond.check(player_data) for cond in self.conditions)
    
    def update_progress(self, player_data: dict) -> int:
        """更新进度并返回完成百分比"""
        if len(self.conditions) == 0:
            return 0
        
        total_progress = 0
        for cond in self.conditions:
            current, required = cond.get_progress(player_data)
            if required > 0:
                total_progress += min(100, int(current / required * 100))
        
        self.progress = total_progress // len(self.conditions)
        return self.progress
    
    def get_progress_text(self, player_data: dict) -> str:
        """获取进度描述"""
        lines = []
        for cond in self.conditions:
            current, required = cond.get_progress(player_data)
            desc = cond.description or f"{cond.condition_type}: {cond.target}"
            status = "✓" if cond.check(player_data) else "○"
            lines.append(f"  {status} {desc}: {current}/{required}")
        return "\n".join(lines)
    
    def to_dict(self) -> dict:
        return {
            "achievement_id": self.achievement_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "rarity": self.rarity.value,
            "conditions": [c.to_dict() for c in self.conditions],
            "rewards": self.rewards.to_dict(),
            "prerequisites": self.prerequisites,
            "status": self.status.value,
            "progress": self.progress,
            "completed_at": self.completed_at,
            "hidden": self.hidden
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Achievement":
        return cls(
            achievement_id=data["achievement_id"],
            name=data["name"],
            description=data["description"],
            category=AchievementCategory(data["category"]),
            rarity=AchievementRarity(data["rarity"]),
            conditions=[AchievementCondition.from_dict(c) for c in data["conditions"]],
            rewards=AchievementReward.from_dict(data["rewards"]),
            prerequisites=data.get("prerequisites", []),
            status=AchievementStatus(data.get("status", "未解锁")),
            progress=data.get("progress", 0),
            completed_at=data.get("completed_at"),
            hidden=data.get("hidden", False)
        )


@dataclass
class Title:
    """称号"""
    title_id: str
    name: str
    description: str
    source: str                         # 来源（成就ID或特殊事件）
    stat_bonuses: Dict[str, float] = field(default_factory=dict)  # 属性加成
    special_effects: List[str] = field(default_factory=list)      # 特殊效果
    rarity: AchievementRarity = AchievementRarity.COMMON
    unlocked: bool = False
    unlocked_at: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "title_id": self.title_id,
            "name": self.name,
            "description": self.description,
            "source": self.source,
            "stat_bonuses": self.stat_bonuses,
            "special_effects": self.special_effects,
            "rarity": self.rarity.value,
            "unlocked": self.unlocked,
            "unlocked_at": self.unlocked_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Title":
        return cls(
            title_id=data["title_id"],
            name=data["name"],
            description=data["description"],
            source=data["source"],
            stat_bonuses=data.get("stat_bonuses", {}),
            special_effects=data.get("special_effects", []),
            rarity=AchievementRarity(data.get("rarity", "普通")),
            unlocked=data.get("unlocked", False),
            unlocked_at=data.get("unlocked_at")
        )
    
    def get_bonus_text(self) -> str:
        """获取加成描述"""
        lines = []
        for stat, bonus in self.stat_bonuses.items():
            if bonus >= 1:
                lines.append(f"{stat} +{int(bonus)}")
            else:
                lines.append(f"{stat} +{int(bonus * 100)}%")
        for effect in self.special_effects:
            lines.append(effect)
        return " | ".join(lines) if lines else "无加成"


class AchievementManager:
    """成就管理器"""
    
    def __init__(self, data_path: str = None):
        self.achievements: Dict[str, Achievement] = {}
        self.titles: Dict[str, Title] = {}
        self.completed_achievements: List[str] = []
        self.claimed_achievements: List[str] = []
        self.unlocked_titles: List[str] = []
        self.current_title: Optional[str] = None
        self.total_achievement_points: int = 0
        self.data_path = data_path or "data/achievements.json"
        
        # 成就完成回调
        self.on_achievement_complete: Optional[Callable] = None
        self.on_title_unlock: Optional[Callable] = None
        
        # 加载数据
        self.load_data()
    
    def load_data(self):
        """从JSON加载成就数据"""
        data_file = Path(self.data_path)
        if not data_file.exists():
            return
        
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 加载成就
        for ach_data in data.get("achievements", []):
            achievement = Achievement.from_dict(ach_data)
            self.achievements[achievement.achievement_id] = achievement
        
        # 加载称号
        for title_data in data.get("titles", []):
            title = Title.from_dict(title_data)
            self.titles[title.title_id] = title
    
    def save_state(self) -> dict:
        """保存状态（用于存档）"""
        return {
            "completed_achievements": self.completed_achievements,
            "claimed_achievements": self.claimed_achievements,
            "unlocked_titles": self.unlocked_titles,
            "current_title": self.current_title,
            "total_achievement_points": self.total_achievement_points
        }
    
    def load_state(self, data: dict):
        """加载状态（用于读档）"""
        self.completed_achievements = data.get("completed_achievements", [])
        self.claimed_achievements = data.get("claimed_achievements", [])
        self.unlocked_titles = data.get("unlocked_titles", [])
        self.current_title = data.get("current_title")
        self.total_achievement_points = data.get("total_achievement_points", 0)
        
        # 更新成就和称号状态
        for ach_id in self.completed_achievements:
            if ach_id in self.achievements:
                self.achievements[ach_id].status = AchievementStatus.COMPLETED
        
        for ach_id in self.claimed_achievements:
            if ach_id in self.achievements:
                self.achievements[ach_id].status = AchievementStatus.CLAIMED
        
        for title_id in self.unlocked_titles:
            if title_id in self.titles:
                self.titles[title_id].unlocked = True
    
    def get_player_data(self, player) -> dict:
        """从玩家对象提取数据用于成就检查"""
        return {
            "name": player.name,
            "realm": player.realm,
            "cultivation": player.cultivation,
            "spirit_stones": player.spirit_stones,
            "sect": player.sect,
            "karma": player.karma,
            "play_time": player.play_time,
            "artifacts": player.artifacts,
            "learned_skills": list(player.learned_skills.keys()) if hasattr(player, 'learned_skills') else [],
            "completed_quests": player.completed_quests,
            "quest_kills": player.quest_kills,
            "explored_locations": getattr(player, 'explored_locations', []),
            "battles_total": getattr(player, 'battles_total', 0),
            "battles_won": getattr(player, 'battles_won', 0)
        }
    
    def check_achievements(self, player) -> List[dict]:
        """检查所有成就进度，返回新完成的成就"""
        player_data = self.get_player_data(player)
        newly_completed = []
        
        for ach_id, achievement in self.achievements.items():
            if ach_id in self.completed_achievements:
                continue
            
            # 检查是否可触发
            if not achievement.is_available(self.completed_achievements):
                continue
            
            # 更新状态
            if achievement.status == AchievementStatus.LOCKED:
                achievement.status = AchievementStatus.IN_PROGRESS
            
            # 更新进度
            achievement.update_progress(player_data)
            
            # 检查是否完成
            if achievement.check_completion(player_data):
                achievement.status = AchievementStatus.COMPLETED
                achievement.completed_at = datetime.now().isoformat()
                self.completed_achievements.append(ach_id)
                
                newly_completed.append({
                    "achievement_id": ach_id,
                    "name": achievement.name,
                    "description": achievement.description,
                    "rarity": achievement.rarity.value,
                    "rewards": achievement.rewards.to_dict()
                })
                
                # 解锁称号
                if achievement.rewards.title:
                    self._unlock_title(achievement.rewards.title)
                
                # 回调
                if self.on_achievement_complete:
                    self.on_achievement_complete(achievement, player)
        
        return newly_completed
    
    def claim_reward(self, achievement_id: str, player) -> dict:
        """领取成就奖励"""
        if achievement_id not in self.completed_achievements:
            return {"success": False, "message": "成就未完成"}
        
        if achievement_id in self.claimed_achievements:
            return {"success": False, "message": "奖励已领取"}
        
        achievement = self.achievements.get(achievement_id)
        if not achievement:
            return {"success": False, "message": "成就不存在"}
        
        rewards = achievement.rewards
        reward_text = []
        
        # 发放奖励
        if rewards.achievement_points > 0:
            self.total_achievement_points += rewards.achievement_points
            reward_text.append(f"成就点数 +{rewards.achievement_points}")
        
        if rewards.spirit_stones > 0:
            player.spirit_stones += rewards.spirit_stones
            reward_text.append(f"灵石 +{rewards.spirit_stones}")
        
        if rewards.cultivation > 0:
            player.cultivation += rewards.cultivation
            reward_text.append(f"修为 +{rewards.cultivation}")
        
        for artifact_name in rewards.artifacts:
            player.artifacts.append({"name": artifact_name, "level": 1, "type": "法宝"})
            reward_text.append(f"获得法宝「{artifact_name}」")
        
        for skill_name in rewards.skills:
            if hasattr(player, 'learned_skills'):
                if skill_name not in player.learned_skills:
                    player.learned_skills[skill_name] = 1
                    reward_text.append(f"学会功法「{skill_name}」")
        
        # 属性加成记录到玩家
        if rewards.stat_bonuses:
            for stat, bonus in rewards.stat_bonuses.items():
                if stat in player.stats:
                    player.stats[stat] = int(player.stats[stat] * (1 + bonus))
            reward_text.append("获得属性加成")
        
        # 更新状态
        achievement.status = AchievementStatus.CLAIMED
        self.claimed_achievements.append(achievement_id)
        
        return {
            "success": True,
            "message": f"领取成就「{achievement.name}」奖励！",
            "rewards": reward_text
        }
    
    def _unlock_title(self, title_name: str):
        """解锁称号"""
        for title_id, title in self.titles.items():
            if title.name == title_name and not title.unlocked:
                title.unlocked = True
                title.unlocked_at = datetime.now().isoformat()
                self.unlocked_titles.append(title_id)
                
                if self.on_title_unlock:
                    self.on_title_unlock(title)
                break
    
    def set_title(self, title_id: str) -> dict:
        """设置当前展示称号"""
        if title_id not in self.unlocked_titles:
            return {"success": False, "message": "未解锁此称号"}
        
        if title_id not in self.titles:
            return {"success": False, "message": "称号不存在"}
        
        self.current_title = title_id
        title = self.titles[title_id]
        
        return {
            "success": True,
            "message": f"已佩戴称号「{title.name}」",
            "bonuses": title.get_bonus_text()
        }
    
    def remove_title(self) -> dict:
        """取消当前称号"""
        if not self.current_title:
            return {"success": False, "message": "当前未佩戴称号"}
        
        old_title = self.titles.get(self.current_title)
        self.current_title = None
        
        return {
            "success": True,
            "message": f"已取消称号「{old_title.name}」" if old_title else "已取消称号"
        }
    
    def get_current_title(self) -> Optional[Title]:
        """获取当前称号"""
        if self.current_title and self.current_title in self.titles:
            return self.titles[self.current_title]
        return None
    
    def get_title_bonuses(self) -> Dict[str, float]:
        """获取当前称号的属性加成"""
        title = self.get_current_title()
        if title:
            return title.stat_bonuses
        return {}
    
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """获取成就详情"""
        return self.achievements.get(achievement_id)
    
    def get_achievements_by_category(self, category: AchievementCategory) -> List[Achievement]:
        """按分类获取成就"""
        return [
            ach for ach in self.achievements.values()
            if ach.category == category
        ]
    
    def get_achievements_by_rarity(self, rarity: AchievementRarity) -> List[Achievement]:
        """按稀有度获取成就"""
        return [
            ach for ach in self.achievements.values()
            if ach.rarity == rarity
        ]
    
    def get_completed_achievements(self) -> List[Achievement]:
        """获取已完成的成就"""
        return [
            self.achievements[ach_id] 
            for ach_id in self.completed_achievements 
            if ach_id in self.achievements
        ]
    
    def get_unclaimed_achievements(self) -> List[Achievement]:
        """获取已完成但未领取奖励的成就"""
        return [
            self.achievements[ach_id]
            for ach_id in self.completed_achievements
            if ach_id in self.achievements 
            and ach_id not in self.claimed_achievements
        ]
    
    def get_unlocked_titles(self) -> List[Title]:
        """获取已解锁的称号"""
        return [
            self.titles[title_id]
            for title_id in self.unlocked_titles
            if title_id in self.titles
        ]
    
    def get_progress_summary(self, player) -> dict:
        """获取成就进度概要"""
        player_data = self.get_player_data(player)
        
        total = len(self.achievements)
        completed = len(self.completed_achievements)
        claimed = len(self.claimed_achievements)
        
        # 按分类统计
        by_category = {}
        for category in AchievementCategory:
            cat_achievements = self.get_achievements_by_category(category)
            cat_completed = sum(1 for a in cat_achievements if a.achievement_id in self.completed_achievements)
            by_category[category.value] = {
                "total": len(cat_achievements),
                "completed": cat_completed
            }
        
        # 按稀有度统计
        by_rarity = {}
        for rarity in AchievementRarity:
            rar_achievements = self.get_achievements_by_rarity(rarity)
            rar_completed = sum(1 for a in rar_achievements if a.achievement_id in self.completed_achievements)
            by_rarity[rarity.value] = {
                "total": len(rar_achievements),
                "completed": rar_completed
            }
        
        return {
            "total": total,
            "completed": completed,
            "claimed": claimed,
            "unclaimed": completed - claimed,
            "achievement_points": self.total_achievement_points,
            "by_category": by_category,
            "by_rarity": by_rarity,
            "titles_unlocked": len(self.unlocked_titles),
            "titles_total": len(self.titles)
        }
    
    def get_display_achievements(self, player, category: str = None, show_hidden: bool = False) -> List[dict]:
        """获取用于显示的成就列表"""
        player_data = self.get_player_data(player)
        achievements = []
        
        for ach in self.achievements.values():
            # 过滤分类
            if category and ach.category.value != category:
                continue
            
            # 隐藏成就处理
            if ach.hidden and ach.achievement_id not in self.completed_achievements and not show_hidden:
                continue
            
            # 更新进度
            ach.update_progress(player_data)
            
            # 构建显示数据
            display = {
                "id": ach.achievement_id,
                "name": ach.name if not ach.hidden or ach.achievement_id in self.completed_achievements else "???",
                "description": ach.description if not ach.hidden or ach.achievement_id in self.completed_achievements else "完成特定条件后解锁",
                "category": ach.category.value,
                "rarity": ach.rarity.value,
                "status": ach.status.value,
                "progress": ach.progress,
                "progress_text": ach.get_progress_text(player_data) if ach.achievement_id in self.completed_achievements or not ach.hidden else "",
                "rewards": ach.rewards.to_dict() if ach.achievement_id in self.completed_achievements or not ach.hidden else {},
                "completed_at": ach.completed_at
            }
            
            achievements.append(display)
        
        return achievements
    
    def get_achievement_info(self, achievement_id: str, player) -> Optional[dict]:
        """获取成就详细信息"""
        ach = self.achievements.get(achievement_id)
        if not ach:
            return None
        
        player_data = self.get_player_data(player)
        ach.update_progress(player_data)
        
        return {
            "id": ach.achievement_id,
            "name": ach.name,
            "description": ach.description,
            "category": ach.category.value,
            "rarity": ach.rarity.value,
            "conditions": [c.to_dict() for c in ach.conditions],
            "progress_text": ach.get_progress_text(player_data),
            "progress": ach.progress,
            "status": ach.status.value,
            "rewards": ach.rewards.to_dict(),
            "prerequisites": ach.prerequisites,
            "completed_at": ach.completed_at,
            "hidden": ach.hidden
        }
    
    def get_recent_achievements(self, limit: int = 5) -> List[dict]:
        """获取最近完成的成就"""
        recent = []
        
        for ach_id in reversed(self.completed_achievements[-limit:]):
            ach = self.achievements.get(ach_id)
            if ach:
                recent.append({
                    "id": ach_id,
                    "name": ach.name,
                    "rarity": ach.rarity.value,
                    "completed_at": ach.completed_at
                })
        
        return recent
    
    def get_achievement_summary_text(self, player) -> str:
        """获取成就概要文本"""
        summary = self.get_progress_summary(player)
        
        text = "【成就系统】\n"
        text += "─" * 30 + "\n"
        text += f"总进度：{summary['completed']}/{summary['total']}\n"
        text += f"成就点数：{summary['achievement_points']}\n"
        text += f"待领取：{summary['unclaimed']}\n"
        text += f"称号：{summary['titles_unlocked']}/{summary['titles_total']}\n\n"
        
        # 当前称号
        current = self.get_current_title()
        if current:
            text += f"当前称号：{current.name}\n"
            text += f"  {current.get_bonus_text()}\n\n"
        
        # 分类进度
        text += "【分类进度】\n"
        for cat, data in summary['by_category'].items():
            if data['total'] > 0:
                text += f"  {cat}：{data['completed']}/{data['total']}\n"
        
        # 最近完成
        recent = self.get_recent_achievements(3)
        if recent:
            text += "\n【最近完成】\n"
            for ach in recent:
                text += f"  • {ach['name']} [{ach['rarity']}]\n"
        
        return text
