#!/usr/bin/env python3
"""
蜀山剑侠传 - 秘境副本系统
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
from datetime import datetime


class DungeonType(Enum):
    """副本类型"""
    NORMAL = "普通"      # 普通副本，日常挑战
    ELITE = "精英"       # 精英副本，难度较高
    LEGENDARY = "传说"   # 传说副本，极高难度


class DungeonStatus(Enum):
    """副本状态"""
    LOCKED = "未解锁"
    AVAILABLE = "可进入"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    COOLDOWN = "冷却中"


class FloorStatus(Enum):
    """层数状态"""
    LOCKED = "未解锁"
    AVAILABLE = "可挑战"
    COMPLETED = "已通关"
    FAILED = "挑战失败"


@dataclass
class DungeonReward:
    """副本奖励"""
    spirit_stones: int = 0                    # 灵石
    cultivation: int = 0                      # 修为
    artifacts: List[str] = field(default_factory=list)  # 法宝ID列表
    skills: List[str] = field(default_factory=list)     # 功法ID列表
    materials: Dict[str, int] = field(default_factory=dict)  # 材料名称 -> 数量
    exp: int = 0                              # 经验值
    
    def to_dict(self) -> dict:
        return {
            "spirit_stones": self.spirit_stones,
            "cultivation": self.cultivation,
            "artifacts": self.artifacts,
            "skills": self.skills,
            "materials": self.materials,
            "exp": self.exp
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DungeonReward":
        return cls(
            spirit_stones=data.get("spirit_stones", 0),
            cultivation=data.get("cultivation", 0),
            artifacts=data.get("artifacts", []),
            skills=data.get("skills", []),
            materials=data.get("materials", {}),
            exp=data.get("exp", 0)
        )


@dataclass
class BossData:
    """Boss数据"""
    name: str
    realm: str
    hp: int
    attack: int
    defense: int
    element: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    special_ability: Optional[str] = None
    lore: str = ""
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "realm": self.realm,
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "element": self.element,
            "skills": self.skills,
            "special_ability": self.special_ability,
            "lore": self.lore
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "BossData":
        return cls(
            name=data["name"],
            realm=data["realm"],
            hp=data["hp"],
            attack=data["attack"],
            defense=data["defense"],
            element=data.get("element"),
            skills=data.get("skills", []),
            special_ability=data.get("special_ability"),
            lore=data.get("lore", "")
        )


@dataclass
class FloorData:
    """副本层数据"""
    floor_number: int
    name: str
    description: str
    enemies: List[Dict] = field(default_factory=list)  # 小怪列表
    boss: Optional[BossData] = None                      # Boss数据
    reward: Optional[DungeonReward] = None               # 通关奖励
    special_rules: List[str] = field(default_factory=list)  # 特殊规则
    
    def to_dict(self) -> dict:
        return {
            "floor_number": self.floor_number,
            "name": self.name,
            "description": self.description,
            "enemies": self.enemies,
            "boss": self.boss.to_dict() if self.boss else None,
            "reward": self.reward.to_dict() if self.reward else None,
            "special_rules": self.special_rules
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FloorData":
        boss = BossData.from_dict(data["boss"]) if data.get("boss") else None
        reward = DungeonReward.from_dict(data["reward"]) if data.get("reward") else None
        
        return cls(
            floor_number=data["floor_number"],
            name=data["name"],
            description=data["description"],
            enemies=data.get("enemies", []),
            boss=boss,
            reward=reward,
            special_rules=data.get("special_rules", [])
        )


@dataclass
class DungeonData:
    """副本数据"""
    dungeon_id: str
    name: str
    dungeon_type: DungeonType
    description: str
    lore: str                                          # 背景故事
    location: str                                      # 地点
    required_realm: str                                # 需要境界
    required_item: Optional[str] = None                # 进入门票
    floors: List[FloorData] = field(default_factory=list)
    first_clear_reward: Optional[DungeonReward] = None # 首通奖励
    daily_reward: Optional[DungeonReward] = None       # 每日通关奖励
    cooldown_hours: int = 24                           # 冷却时间（小时）
    max_attempts_daily: int = 3                        # 每日最大尝试次数
    recommended_power: int = 0                         # 推荐战力
    
    def to_dict(self) -> dict:
        return {
            "dungeon_id": self.dungeon_id,
            "name": self.name,
            "dungeon_type": self.dungeon_type.value,
            "description": self.description,
            "lore": self.lore,
            "location": self.location,
            "required_realm": self.required_realm,
            "required_item": self.required_item,
            "floors": [f.to_dict() for f in self.floors],
            "first_clear_reward": self.first_clear_reward.to_dict() if self.first_clear_reward else None,
            "daily_reward": self.daily_reward.to_dict() if self.daily_reward else None,
            "cooldown_hours": self.cooldown_hours,
            "max_attempts_daily": self.max_attempts_daily,
            "recommended_power": self.recommended_power
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DungeonData":
        dungeon_type = DungeonType(data["dungeon_type"])
        floors = [FloorData.from_dict(f) for f in data.get("floors", [])]
        first_clear = DungeonReward.from_dict(data["first_clear_reward"]) if data.get("first_clear_reward") else None
        daily_reward = DungeonReward.from_dict(data["daily_reward"]) if data.get("daily_reward") else None
        
        return cls(
            dungeon_id=data["dungeon_id"],
            name=data["name"],
            dungeon_type=dungeon_type,
            description=data["description"],
            lore=data.get("lore", ""),
            location=data.get("location", "未知"),
            required_realm=data["required_realm"],
            required_item=data.get("required_item"),
            floors=floors,
            first_clear_reward=first_clear,
            daily_reward=daily_reward,
            cooldown_hours=data.get("cooldown_hours", 24),
            max_attempts_daily=data.get("max_attempts_daily", 3),
            recommended_power=data.get("recommended_power", 0)
        )


class DungeonRun:
    """副本运行实例"""
    
    def __init__(self, dungeon: DungeonData, player_name: str):
        self.dungeon = dungeon
        self.player_name = player_name
        self.current_floor = 0
        self.start_time = datetime.now()
        self.enemies_defeated = 0
        self.bosses_defeated = 0
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        self.items_collected: List[str] = []
        self.is_completed = False
        self.is_failed = False
    
    def get_current_floor(self) -> Optional[FloorData]:
        """获取当前层数据"""
        if 0 <= self.current_floor < len(self.dungeon.floors):
            return self.dungeon.floors[self.current_floor]
        return None
    
    def advance_floor(self) -> bool:
        """进入下一层"""
        if self.current_floor < len(self.dungeon.floors) - 1:
            self.current_floor += 1
            return True
        else:
            self.is_completed = True
            return False
    
    def get_progress(self) -> Dict:
        """获取进度"""
        return {
            "current_floor": self.current_floor + 1,
            "total_floors": len(self.dungeon.floors),
            "enemies_defeated": self.enemies_defeated,
            "bosses_defeated": self.bosses_defeated,
            "is_completed": self.is_completed,
            "is_failed": self.is_failed
        }
    
    def to_dict(self) -> dict:
        return {
            "dungeon_id": self.dungeon.dungeon_id,
            "player_name": self.player_name,
            "current_floor": self.current_floor,
            "start_time": self.start_time.isoformat(),
            "enemies_defeated": self.enemies_defeated,
            "bosses_defeated": self.bosses_defeated,
            "total_damage_dealt": self.total_damage_dealt,
            "total_damage_taken": self.total_damage_taken,
            "items_collected": self.items_collected,
            "is_completed": self.is_completed,
            "is_failed": self.is_failed
        }


class PlayerDungeonProgress:
    """玩家副本进度"""
    
    def __init__(self, dungeon_id: str):
        self.dungeon_id = dungeon_id
        self.highest_floor = 0                    # 最高通关层数
        self.total_clears = 0                      # 总通关次数
        self.first_clear_date: Optional[datetime] = None  # 首通时间
        self.fastest_clear_time: Optional[float] = None   # 最快通关时间（秒）
        self.attempts_today = 0                    # 今日尝试次数
        self.last_attempt_date: Optional[str] = None      # 上次尝试日期
        self.claimed_first_clear = False           # 是否已领取首通奖励
        self.claimed_today = False                 # 今日是否已领取奖励
    
    def can_attempt(self, max_attempts: int, today: str) -> Tuple[bool, str]:
        """检查是否可以尝试"""
        if self.last_attempt_date != today:
            self.attempts_today = 0
            self.claimed_today = False
            self.last_attempt_date = today
        
        if self.attempts_today >= max_attempts:
            return False, f"今日尝试次数已达上限 ({max_attempts}次)"
        
        return True, "可以进入"
    
    def record_attempt(self, today: str):
        """记录尝试"""
        if self.last_attempt_date != today:
            self.attempts_today = 0
            self.claimed_today = False
        self.attempts_today += 1
        self.last_attempt_date = today
    
    def record_clear(self, clear_time: float):
        """记录通关"""
        self.total_clears += 1
        
        if self.first_clear_date is None:
            self.first_clear_date = datetime.now()
        
        if self.fastest_clear_time is None or clear_time < self.fastest_clear_time:
            self.fastest_clear_time = clear_time
    
    def to_dict(self) -> dict:
        return {
            "dungeon_id": self.dungeon_id,
            "highest_floor": self.highest_floor,
            "total_clears": self.total_clears,
            "first_clear_date": self.first_clear_date.isoformat() if self.first_clear_date else None,
            "fastest_clear_time": self.fastest_clear_time,
            "attempts_today": self.attempts_today,
            "last_attempt_date": self.last_attempt_date,
            "claimed_first_clear": self.claimed_first_clear,
            "claimed_today": self.claimed_today
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PlayerDungeonProgress":
        progress = cls(data["dungeon_id"])
        progress.highest_floor = data.get("highest_floor", 0)
        progress.total_clears = data.get("total_clears", 0)
        
        if data.get("first_clear_date"):
            progress.first_clear_date = datetime.fromisoformat(data["first_clear_date"])
        
        progress.fastest_clear_time = data.get("fastest_clear_time")
        progress.attempts_today = data.get("attempts_today", 0)
        progress.last_attempt_date = data.get("last_attempt_date")
        progress.claimed_first_clear = data.get("claimed_first_clear", False)
        progress.claimed_today = data.get("claimed_today", False)
        
        return progress


class DungeonManager:
    """副本管理器"""
    
    def __init__(self, data_path: str = "data/dungeons.json"):
        self.data_path = data_path
        self.dungeons: Dict[str, DungeonData] = {}
        self.load_dungeons()
    
    def load_dungeons(self):
        """加载副本数据"""
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for dungeon_id, dungeon_data in data.get("dungeons", {}).items():
                self.dungeons[dungeon_id] = DungeonData.from_dict(dungeon_data)
        except FileNotFoundError:
            print(f"警告：副本数据文件 {self.data_path} 不存在")
        except json.JSONDecodeError as e:
            print(f"错误：副本数据格式错误 - {e}")
    
    def get_dungeon(self, dungeon_id: str) -> Optional[DungeonData]:
        """获取副本"""
        return self.dungeons.get(dungeon_id)
    
    def get_all_dungeons(self) -> List[DungeonData]:
        """获取所有副本"""
        return list(self.dungeons.values())
    
    def get_dungeons_by_type(self, dungeon_type: DungeonType) -> List[DungeonData]:
        """按类型获取副本"""
        return [d for d in self.dungeons.values() if d.dungeon_type == dungeon_type]
    
    def get_available_dungeons(self, player_realm: str, 
                               player_progress: Dict[str, PlayerDungeonProgress],
                               inventory: Dict[str, int] = None) -> List[Dict]:
        """获取玩家可进入的副本"""
        from config import REALMS
        
        available = []
        player_realm_level = REALMS.get(player_realm, {}).get("level", 1)
        
        for dungeon in self.dungeons.values():
            required_level = REALMS.get(dungeon.required_realm, {}).get("level", 1)
            progress = player_progress.get(dungeon.dungeon_id)
            
            status = DungeonStatus.AVAILABLE
            reason = ""
            
            # 检查境界
            if player_realm_level < required_level:
                status = DungeonStatus.LOCKED
                reason = f"需要境界 {dungeon.required_realm}"
            
            # 检查门票
            elif dungeon.required_item:
                if inventory is None or inventory.get(dungeon.required_item, 0) <= 0:
                    status = DungeonStatus.LOCKED
                    reason = f"需要道具 {dungeon.required_item}"
            
            # 检查冷却
            elif progress:
                today = datetime.now().strftime("%Y-%m-%d")
                can_attempt, _ = progress.can_attempt(dungeon.max_attempts_daily, today)
                if not can_attempt:
                    status = DungeonStatus.COOLDOWN
                    reason = "今日次数已用尽"
            
            available.append({
                "dungeon": dungeon,
                "status": status,
                "reason": reason,
                "progress": progress
            })
        
        return available
    
    def can_enter(self, dungeon_id: str, player, 
                  player_progress: Dict[str, PlayerDungeonProgress]) -> Tuple[bool, str]:
        """检查是否可以进入副本"""
        from config import REALMS
        
        dungeon = self.get_dungeon(dungeon_id)
        if not dungeon:
            return False, "副本不存在"
        
        # 检查境界
        player_realm_level = REALMS.get(player.realm, {}).get("level", 1)
        required_level = REALMS.get(dungeon.required_realm, {}).get("level", 1)
        
        if player_realm_level < required_level:
            return False, f"境界不足，需要 {dungeon.required_realm}"
        
        # 检查门票
        if dungeon.required_item:
            has_item = False
            # 检查玩家物品栏
            if hasattr(player, 'materials'):
                if dungeon.required_item in player.materials:
                    has_item = player.materials[dungeon.required_item] > 0
            if not has_item:
                return False, f"缺少进入道具：{dungeon.required_item}"
        
        # 检查次数
        progress = player_progress.get(dungeon_id)
        if progress:
            today = datetime.now().strftime("%Y-%m-%d")
            can_attempt, msg = progress.can_attempt(dungeon.max_attempts_daily, today)
            if not can_attempt:
                return False, msg
        
        return True, "可以进入"
    
    def start_dungeon(self, dungeon_id: str, player) -> Tuple[Optional[DungeonRun], str]:
        """开始副本"""
        dungeon = self.get_dungeon(dungeon_id)
        if not dungeon:
            return None, "副本不存在"
        
        run = DungeonRun(dungeon, player.name)
        return run, f"进入【{dungeon.name}】，当前第 1 层"
    
    def get_dungeon_info(self, dungeon_id: str) -> Optional[Dict]:
        """获取副本详情"""
        dungeon = self.get_dungeon(dungeon_id)
        if not dungeon:
            return None
        
        return {
            "id": dungeon.dungeon_id,
            "name": dungeon.name,
            "type": dungeon.dungeon_type.value,
            "description": dungeon.description,
            "lore": dungeon.lore,
            "location": dungeon.location,
            "required_realm": dungeon.required_realm,
            "required_item": dungeon.required_item,
            "floors": len(dungeon.floors),
            "recommended_power": dungeon.recommended_power,
            "cooldown_hours": dungeon.cooldown_hours,
            "max_attempts_daily": dungeon.max_attempts_daily,
            "first_clear_reward": dungeon.first_clear_reward.to_dict() if dungeon.first_clear_reward else None,
            "daily_reward": dungeon.daily_reward.to_dict() if dungeon.daily_reward else None
        }
    
    def get_floor_info(self, dungeon_id: str, floor_number: int) -> Optional[Dict]:
        """获取副本层数信息"""
        dungeon = self.get_dungeon(dungeon_id)
        if not dungeon:
            return None
        
        if floor_number < 1 or floor_number > len(dungeon.floors):
            return None
        
        floor = dungeon.floors[floor_number - 1]
        
        return {
            "floor_number": floor.floor_number,
            "name": floor.name,
            "description": floor.description,
            "enemy_count": len(floor.enemies),
            "has_boss": floor.boss is not None,
            "boss_name": floor.boss.name if floor.boss else None,
            "special_rules": floor.special_rules,
            "reward": floor.reward.to_dict() if floor.reward else None
        }


class DungeonRewardSystem:
    """副本奖励系统"""
    
    @staticmethod
    def calculate_floor_reward(floor: FloorData, player_level: int) -> DungeonReward:
        """计算层数奖励"""
        base_reward = floor.reward or DungeonReward()
        
        # 根据玩家等级调整
        multiplier = 1 + (player_level - 1) * 0.1
        
        reward = DungeonReward(
            spirit_stones=int(base_reward.spirit_stones * multiplier),
            cultivation=int(base_reward.cultivation * multiplier),
            artifacts=base_reward.artifacts.copy(),
            skills=base_reward.skills.copy(),
            materials=base_reward.materials.copy(),
            exp=int(base_reward.exp * multiplier)
        )
        
        return reward
    
    @staticmethod
    def calculate_first_clear_reward(dungeon: DungeonData, player_level: int) -> DungeonReward:
        """计算首通奖励"""
        if not dungeon.first_clear_reward:
            return DungeonReward()
        
        base = dungeon.first_clear_reward
        multiplier = 1 + (player_level - 1) * 0.15
        
        return DungeonReward(
            spirit_stones=int(base.spirit_stones * multiplier),
            cultivation=int(base.cultivation * multiplier),
            artifacts=base.artifacts.copy(),
            skills=base.skills.copy(),
            materials=base.materials.copy(),
            exp=int(base.exp * multiplier)
        )
    
    @staticmethod
    def calculate_completion_reward(dungeon: DungeonData, run: DungeonRun, 
                                    player_level: int) -> Dict:
        """计算通关总奖励"""
        total_reward = DungeonReward()
        
        # 累加所有层数奖励
        for floor in dungeon.floors[:run.current_floor + 1]:
            floor_reward = DungeonRewardSystem.calculate_floor_reward(floor, player_level)
            total_reward.spirit_stones += floor_reward.spirit_stones
            total_reward.cultivation += floor_reward.cultivation
            total_reward.exp += floor_reward.exp
            
            for artifact in floor_reward.artifacts:
                if artifact not in total_reward.artifacts:
                    total_reward.artifacts.append(artifact)
            
            for skill in floor_reward.skills:
                if skill not in total_reward.skills:
                    total_reward.skills.append(skill)
            
            for mat, count in floor_reward.materials.items():
                total_reward.materials[mat] = total_reward.materials.get(mat, 0) + count
        
        # 每日通关奖励
        if dungeon.daily_reward:
            total_reward.spirit_stones += dungeon.daily_reward.spirit_stones
            total_reward.cultivation += dungeon.daily_reward.cultivation
        
        # 计算评分加成
        score = DungeonRewardSystem.calculate_score(run)
        if score >= 90:
            total_reward.spirit_stones = int(total_reward.spirit_stones * 1.5)
            total_reward.cultivation = int(total_reward.cultivation * 1.5)
        elif score >= 70:
            total_reward.spirit_stones = int(total_reward.spirit_stones * 1.2)
            total_reward.cultivation = int(total_reward.cultivation * 1.2)
        
        return {
            "reward": total_reward,
            "score": score,
            "is_first_clear": run.enemies_defeated == len(dungeon.floors)  # 简化判断
        }
    
    @staticmethod
    def calculate_score(run: DungeonRun) -> int:
        """计算副本评分"""
        base_score = 100
        
        # 根据伤害承受扣分
        if run.total_damage_taken > 0:
            damage_ratio = run.total_damage_taken / (run.total_damage_dealt + 1)
            base_score -= int(damage_ratio * 20)
        
        # 根据时间加成
        elapsed = (datetime.now() - run.start_time).total_seconds()
        if elapsed < 300:  # 5分钟内
            base_score += 10
        elif elapsed < 600:  # 10分钟内
            base_score += 5
        elif elapsed > 1800:  # 超过30分钟
            base_score -= 10
        
        return max(0, min(100, base_score))
    
    @staticmethod
    def grant_reward(player, reward: DungeonReward) -> Dict:
        """发放奖励"""
        result = {
            "success": True,
            "granted": {}
        }
        
        # 灵石
        if reward.spirit_stones > 0:
            player.spirit_stones += reward.spirit_stones
            result["granted"]["spirit_stones"] = reward.spirit_stones
        
        # 修为
        if reward.cultivation > 0:
            player.cultivation += reward.cultivation
            result["granted"]["cultivation"] = reward.cultivation
        
        # 法宝
        if reward.artifacts:
            for artifact_id in reward.artifacts:
                # 简化处理，实际应调用法宝系统
                player.artifacts.append({"id": artifact_id, "name": artifact_id})
            result["granted"]["artifacts"] = reward.artifacts
        
        # 功法
        if reward.skills:
            for skill_id in reward.skills:
                if skill_id not in player.learned_skills:
                    player.learned_skills[skill_id] = 1
            result["granted"]["skills"] = reward.skills
        
        # 材料
        if reward.materials:
            if not hasattr(player, 'materials'):
                player.materials = {}
            for mat, count in reward.materials.items():
                player.materials[mat] = player.materials.get(mat, 0) + count
            result["granted"]["materials"] = reward.materials
        
        return result


class DungeonRanking:
    """副本排行榜"""
    
    def __init__(self):
        self.rankings: Dict[str, List[Dict]] = {}  # dungeon_id -> rankings
    
    def add_entry(self, dungeon_id: str, player_name: str, 
                  clear_time: float, score: int):
        """添加排行榜条目"""
        if dungeon_id not in self.rankings:
            self.rankings[dungeon_id] = []
        
        entry = {
            "player_name": player_name,
            "clear_time": clear_time,
            "score": score,
            "date": datetime.now().isoformat()
        }
        
        self.rankings[dungeon_id].append(entry)
        
        # 按时间排序
        self.rankings[dungeon_id].sort(key=lambda x: x["clear_time"])
        
        # 只保留前100名
        self.rankings[dungeon_id] = self.rankings[dungeon_id][:100]
    
    def get_ranking(self, dungeon_id: str, limit: int = 10) -> List[Dict]:
        """获取排行榜"""
        if dungeon_id not in self.rankings:
            return []
        
        rankings = self.rankings[dungeon_id][:limit]
        
        for i, entry in enumerate(rankings):
            entry["rank"] = i + 1
        
        return rankings
    
    def get_player_rank(self, dungeon_id: str, player_name: str) -> Optional[int]:
        """获取玩家排名"""
        if dungeon_id not in self.rankings:
            return None
        
        for i, entry in enumerate(self.rankings[dungeon_id]):
            if entry["player_name"] == player_name:
                return i + 1
        
        return None


# ==================== 便捷函数 ====================

def create_dungeon_enemy(floor: FloorData, enemy_index: int = 0) -> Optional[Dict]:
    """创建副本敌人"""
    from game.combat import Enemy
    
    if enemy_index < len(floor.enemies):
        enemy_data = floor.enemies[enemy_index]
        return enemy_data
    
    return None


def create_dungeon_boss(floor: FloorData) -> Optional["Enemy"]:
    """创建副本Boss"""
    from game.combat import Enemy
    
    if floor.boss:
        boss = floor.boss
        return Enemy(
            name=boss.name,
            realm=boss.realm,
            hp=boss.hp,
            attack=boss.attack,
            defense=boss.defense,
            element=boss.element
        )
    
    return None


def get_dungeon_status_text(dungeon: DungeonData, 
                            progress: Optional[PlayerDungeonProgress] = None) -> str:
    """获取副本状态文本"""
    lines = [
        f"【{dungeon.name}】",
        f"类型：{dungeon.dungeon_type.value}副本",
        f"地点：{dungeon.location}",
        f"要求境界：{dungeon.required_realm}",
        f"层数：{len(dungeon.floors)} 层",
        f"推荐战力：{dungeon.recommended_power}",
        "",
        f"描述：{dungeon.description}",
    ]
    
    if progress:
        lines.append("")
        lines.append("【进度】")
        lines.append(f"最高层数：{progress.highest_floor + 1}/{len(dungeon.floors)}")
        lines.append(f"通关次数：{progress.total_clears}")
        
        if progress.first_clear_date:
            lines.append(f"首通时间：{progress.first_clear_date.strftime('%Y-%m-%d %H:%M')}")
        
        if progress.fastest_clear_time:
            minutes = int(progress.fastest_clear_time // 60)
            seconds = int(progress.fastest_clear_time % 60)
            lines.append(f"最快通关：{minutes}分{seconds}秒")
        
        lines.append(f"今日尝试：{progress.attempts_today}/{dungeon.max_attempts_daily}")
    
    if dungeon.first_clear_reward:
        lines.append("")
        lines.append("【首通奖励】")
        lines.append(f"灵石：{dungeon.first_clear_reward.spirit_stones}")
        lines.append(f"修为：{dungeon.first_clear_reward.cultivation}")
    
    return "\n".join(lines)


# ==================== 测试代码 ====================

def test_dungeon_system():
    """测试副本系统"""
    print("=" * 50)
    print("副本系统测试")
    print("=" * 50)
    
    # 创建副本管理器
    manager = DungeonManager("data/dungeons.json")
    
    print(f"\n已加载 {len(manager.dungeons)} 个副本")
    
    # 显示所有副本
    for dungeon in manager.get_all_dungeons():
        print(f"\n{dungeon.name} ({dungeon.dungeon_type.value})")
        print(f"  境界要求：{dungeon.required_realm}")
        print(f"  层数：{len(dungeon.floors)}")
        
        if dungeon.floors:
            print(f"  首层Boss：{dungeon.floors[0].boss.name if dungeon.floors[0].boss else '无'}")
    
    # 模拟进入副本
    print("\n" + "=" * 50)
    print("模拟进入副本")
    print("=" * 50)
    
    # 创建模拟玩家
    class MockPlayer:
        def __init__(self):
            self.name = "测试玩家"
            self.realm = "筑基期"
            self.spirit_stones = 1000
            self.cultivation = 5000
            self.artifacts = []
            self.learned_skills = {}
            self.materials = {}
    
    player = MockPlayer()
    progress = {}
    
    # 尝试进入第一个副本
    dungeon_id = list(manager.dungeons.keys())[0] if manager.dungeons else None
    
    if dungeon_id:
        can_enter, msg = manager.can_enter(dungeon_id, player, progress)
        print(f"\n进入 {dungeon_id}：{msg}")
        
        if can_enter:
            run, msg = manager.start_dungeon(dungeon_id, player)
            print(msg)
            
            if run:
                floor = run.get_current_floor()
                if floor:
                    print(f"\n当前层：{floor.name}")
                    print(f"描述：{floor.description}")
                    if floor.boss:
                        print(f"Boss：{floor.boss.name} ({floor.boss.realm})")


if __name__ == "__main__":
    test_dungeon_system()
