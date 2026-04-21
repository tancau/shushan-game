#!/usr/bin/env python3
"""
蜀山剑侠传 - 排行榜系统

排行榜类型：
- 战力榜：综合战斗力排名
- 修为榜：修为值排名
- 境界榜：境界等级排名
- 财富榜：灵石总数排名
- 成就榜：成就点数排名
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid


class LeaderboardType(Enum):
    """排行榜类型"""
    POWER = "战力榜"        # 综合战斗力
    CULTIVATION = "修为榜"  # 修为值
    REALM = "境界榜"        # 境界等级
    WEALTH = "财富榜"       # 灵石总数
    ACHIEVEMENT = "成就榜"  # 成就点数


class RewardType(Enum):
    """奖励类型"""
    SPIRIT_STONES = "灵石"
    CULTIVATION = "修为"
    TITLE = "称号"
    ITEM = "物品"
    REPUTATION = "声望"


@dataclass
class LeaderboardReward:
    """排行奖励"""
    reward_id: str
    name: str
    reward_type: RewardType
    value: int
    description: str = ""
    
    def to_dict(self) -> dict:
        return {
            "reward_id": self.reward_id,
            "name": self.name,
            "reward_type": self.reward_type.value,
            "value": self.value,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LeaderboardReward":
        return cls(
            reward_id=data["reward_id"],
            name=data["name"],
            reward_type=RewardType(data["reward_type"]),
            value=data["value"],
            description=data.get("description", "")
        )


@dataclass
class LeaderboardEntry:
    """排行榜条目"""
    player_name: str
    player_id: str  # 用于区分同名玩家
    value: int  # 排名数值
    rank: int = 0  # 排名
    realm: str = "练气期"  # 玩家境界
    sect: Optional[str] = None  # 门派
    title: Optional[str] = None  # 当前称号
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        return {
            "player_name": self.player_name,
            "player_id": self.player_id,
            "value": self.value,
            "rank": self.rank,
            "realm": self.realm,
            "sect": self.sect,
            "title": self.title,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LeaderboardEntry":
        return cls(
            player_name=data["player_name"],
            player_id=data["player_id"],
            value=data["value"],
            rank=data["rank"],
            realm=data.get("realm", "练气期"),
            sect=data.get("sect"),
            title=data.get("title"),
            updated_at=data.get("updated_at", datetime.now().isoformat())
        )


@dataclass
class RankingTitle:
    """排名称号"""
    title_id: str
    name: str
    description: str
    leaderboard_type: LeaderboardType
    rank_requirement: int  # 需要的排名 (1, 2, 3)
    bonuses: Dict[str, float] = field(default_factory=dict)
    duration_days: int = 7  # 称号持续时间（天）
    
    def to_dict(self) -> dict:
        return {
            "title_id": self.title_id,
            "name": self.name,
            "description": self.description,
            "leaderboard_type": self.leaderboard_type.value,
            "rank_requirement": self.rank_requirement,
            "bonuses": self.bonuses,
            "duration_days": self.duration_days
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "RankingTitle":
        return cls(
            title_id=data["title_id"],
            name=data["name"],
            description=data["description"],
            leaderboard_type=LeaderboardType(data["leaderboard_type"]),
            rank_requirement=data["rank_requirement"],
            bonuses=data.get("bonuses", {}),
            duration_days=data.get("duration_days", 7)
        )
    
    def get_bonus_text(self) -> str:
        """获取加成描述"""
        if not self.bonuses:
            return "无加成"
        
        bonus_texts = []
        for stat, value in self.bonuses.items():
            if value >= 1:
                bonus_texts.append(f"{stat}+{int(value)}")
            else:
                bonus_texts.append(f"{stat}+{int(value*100)}%")
        
        return "，".join(bonus_texts)


class Leaderboard:
    """单个排行榜"""
    
    def __init__(self, leaderboard_type: LeaderboardType, max_entries: int = 100):
        self.leaderboard_type = leaderboard_type
        self.max_entries = max_entries
        self.entries: Dict[str, LeaderboardEntry] = {}  # player_id -> entry
        self.last_reset: Optional[str] = None
        self.last_weekly_reset: Optional[str] = None
        
    def update_entry(self, player_name: str, player_id: str, value: int,
                     realm: str = "练气期", sect: Optional[str] = None,
                     title: Optional[str] = None) -> LeaderboardEntry:
        """更新玩家排名数据"""
        entry = LeaderboardEntry(
            player_name=player_name,
            player_id=player_id,
            value=value,
            realm=realm,
            sect=sect,
            title=title,
            updated_at=datetime.now().isoformat()
        )
        
        self.entries[player_id] = entry
        self._recalculate_ranks()
        
        return self.entries[player_id]
    
    def remove_entry(self, player_id: str) -> bool:
        """移除玩家排名"""
        if player_id in self.entries:
            del self.entries[player_id]
            self._recalculate_ranks()
            return True
        return False
    
    def get_entry(self, player_id: str) -> Optional[LeaderboardEntry]:
        """获取玩家排名信息"""
        return self.entries.get(player_id)
    
    def get_rank(self, player_id: str) -> int:
        """获取玩家排名"""
        entry = self.entries.get(player_id)
        return entry.rank if entry else 0
    
    def get_top_entries(self, count: int = 10) -> List[LeaderboardEntry]:
        """获取前N名"""
        sorted_entries = sorted(
            self.entries.values(),
            key=lambda e: (-e.value, e.player_name)
        )
        return sorted_entries[:count]
    
    def get_entries_around(self, player_id: str, range_count: int = 5) -> List[LeaderboardEntry]:
        """获取玩家周围的排名"""
        sorted_entries = sorted(
            self.entries.values(),
            key=lambda e: (-e.value, e.player_name)
        )
        
        # 找到玩家的位置
        player_index = -1
        for i, entry in enumerate(sorted_entries):
            if entry.player_id == player_id:
                player_index = i
                break
        
        if player_index == -1:
            return []
        
        # 获取周围的条目
        start = max(0, player_index - range_count)
        end = min(len(sorted_entries), player_index + range_count + 1)
        
        return sorted_entries[start:end]
    
    def _recalculate_ranks(self):
        """重新计算排名"""
        sorted_entries = sorted(
            self.entries.values(),
            key=lambda e: (-e.value, e.player_name)
        )
        
        for i, entry in enumerate(sorted_entries):
            entry.rank = i + 1
    
    def clear(self):
        """清空排行榜"""
        self.entries.clear()
        self.last_reset = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "leaderboard_type": self.leaderboard_type.value,
            "max_entries": self.max_entries,
            "entries": {
                pid: entry.to_dict() 
                for pid, entry in self.entries.items()
            },
            "last_reset": self.last_reset,
            "last_weekly_reset": self.last_weekly_reset
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Leaderboard":
        """从字典创建"""
        leaderboard_type = LeaderboardType(data["leaderboard_type"])
        leaderboard = cls(leaderboard_type, data.get("max_entries", 100))
        
        leaderboard.entries = {
            pid: LeaderboardEntry.from_dict(entry_data)
            for pid, entry_data in data.get("entries", {}).items()
        }
        
        leaderboard.last_reset = data.get("last_reset")
        leaderboard.last_weekly_reset = data.get("last_weekly_reset")
        
        # 重新计算排名
        leaderboard._recalculate_ranks()
        
        return leaderboard


class LeaderboardManager:
    """排行榜管理器"""
    
    # 排名称号配置
    RANKING_TITLES = {
        (LeaderboardType.POWER, 1): RankingTitle(
            title_id="power_champion",
            name="战神",
            description="战力榜第一名",
            leaderboard_type=LeaderboardType.POWER,
            rank_requirement=1,
            bonuses={"攻击": 50, "防御": 30},
            duration_days=7
        ),
        (LeaderboardType.POWER, 2): RankingTitle(
            title_id="power_runner_up",
            name="武圣",
            description="战力榜第二名",
            leaderboard_type=LeaderboardType.POWER,
            rank_requirement=2,
            bonuses={"攻击": 30, "防御": 20},
            duration_days=7
        ),
        (LeaderboardType.POWER, 3): RankingTitle(
            title_id="power_third",
            name="武宗",
            description="战力榜第三名",
            leaderboard_type=LeaderboardType.POWER,
            rank_requirement=3,
            bonuses={"攻击": 20, "防御": 10},
            duration_days=7
        ),
        (LeaderboardType.CULTIVATION, 1): RankingTitle(
            title_id="cultivation_champion",
            name="修真第一人",
            description="修为榜第一名",
            leaderboard_type=LeaderboardType.CULTIVATION,
            rank_requirement=1,
            bonuses={"修炼速度": 0.2},
            duration_days=7
        ),
        (LeaderboardType.CULTIVATION, 2): RankingTitle(
            title_id="cultivation_runner_up",
            name="大道修士",
            description="修为榜第二名",
            leaderboard_type=LeaderboardType.CULTIVATION,
            rank_requirement=2,
            bonuses={"修炼速度": 0.15},
            duration_days=7
        ),
        (LeaderboardType.CULTIVATION, 3): RankingTitle(
            title_id="cultivation_third",
            name="苦修之士",
            description="修为榜第三名",
            leaderboard_type=LeaderboardType.CULTIVATION,
            rank_requirement=3,
            bonuses={"修炼速度": 0.1},
            duration_days=7
        ),
        (LeaderboardType.REALM, 1): RankingTitle(
            title_id="realm_champion",
            name="境界至尊",
            description="境界榜第一名",
            leaderboard_type=LeaderboardType.REALM,
            rank_requirement=1,
            bonuses={"突破成功率": 0.2},
            duration_days=7
        ),
        (LeaderboardType.REALM, 2): RankingTitle(
            title_id="realm_runner_up",
            name="境界大师",
            description="境界榜第二名",
            leaderboard_type=LeaderboardType.REALM,
            rank_requirement=2,
            bonuses={"突破成功率": 0.15},
            duration_days=7
        ),
        (LeaderboardType.REALM, 3): RankingTitle(
            title_id="realm_third",
            name="境界高人",
            description="境界榜第三名",
            leaderboard_type=LeaderboardType.REALM,
            rank_requirement=3,
            bonuses={"突破成功率": 0.1},
            duration_days=7
        ),
        (LeaderboardType.WEALTH, 1): RankingTitle(
            title_id="wealth_champion",
            name="灵石大亨",
            description="财富榜第一名",
            leaderboard_type=LeaderboardType.WEALTH,
            rank_requirement=1,
            bonuses={"灵石掉落": 0.2},
            duration_days=7
        ),
        (LeaderboardType.WEALTH, 2): RankingTitle(
            title_id="wealth_runner_up",
            name="富甲一方",
            description="财富榜第二名",
            leaderboard_type=LeaderboardType.WEALTH,
            rank_requirement=2,
            bonuses={"灵石掉落": 0.15},
            duration_days=7
        ),
        (LeaderboardType.WEALTH, 3): RankingTitle(
            title_id="wealth_third",
            name="财运亨通",
            description="财富榜第三名",
            leaderboard_type=LeaderboardType.WEALTH,
            rank_requirement=3,
            bonuses={"灵石掉落": 0.1},
            duration_days=7
        ),
        (LeaderboardType.ACHIEVEMENT, 1): RankingTitle(
            title_id="achievement_champion",
            name="成就之王",
            description="成就榜第一名",
            leaderboard_type=LeaderboardType.ACHIEVEMENT,
            rank_requirement=1,
            bonuses={"声望": 100},
            duration_days=7
        ),
        (LeaderboardType.ACHIEVEMENT, 2): RankingTitle(
            title_id="achievement_runner_up",
            name="成就大师",
            description="成就榜第二名",
            leaderboard_type=LeaderboardType.ACHIEVEMENT,
            rank_requirement=2,
            bonuses={"声望": 50},
            duration_days=7
        ),
        (LeaderboardType.ACHIEVEMENT, 3): RankingTitle(
            title_id="achievement_third",
            name="成就达人",
            description="成就榜第三名",
            leaderboard_type=LeaderboardType.ACHIEVEMENT,
            rank_requirement=3,
            bonuses={"声望": 30},
            duration_days=7
        ),
    }
    
    # 每日奖励配置
    DAILY_REWARDS = {
        1: [  # 第一名
            LeaderboardReward("daily_1_stones", "灵石礼包", RewardType.SPIRIT_STONES, 1000, "第一名每日奖励"),
            LeaderboardReward("daily_1_cultivation", "修为丹", RewardType.CULTIVATION, 500, "第一名每日奖励"),
        ],
        2: [  # 第二名
            LeaderboardReward("daily_2_stones", "灵石袋", RewardType.SPIRIT_STONES, 500, "第二名每日奖励"),
            LeaderboardReward("daily_2_cultivation", "修为丸", RewardType.CULTIVATION, 250, "第二名每日奖励"),
        ],
        3: [  # 第三名
            LeaderboardReward("daily_3_stones", "灵石包", RewardType.SPIRIT_STONES, 300, "第三名每日奖励"),
            LeaderboardReward("daily_3_cultivation", "修为散", RewardType.CULTIVATION, 150, "第三名每日奖励"),
        ],
        4: [  # 第四到十名
            LeaderboardReward("daily_4_stones", "灵石", RewardType.SPIRIT_STONES, 100, "前十每日奖励"),
        ],
        10: [  # 前十名
            LeaderboardReward("daily_10_stones", "灵石", RewardType.SPIRIT_STONES, 50, "前十每日奖励"),
        ],
    }
    
    # 每周奖励配置
    WEEKLY_REWARDS = {
        1: [  # 第一名
            LeaderboardReward("weekly_1_stones", "巨额灵石", RewardType.SPIRIT_STONES, 10000, "第一名周奖励"),
            LeaderboardReward("weekly_1_cultivation", "修为大丹", RewardType.CULTIVATION, 5000, "第一名周奖励"),
        ],
        2: [  # 第二名
            LeaderboardReward("weekly_2_stones", "大量灵石", RewardType.SPIRIT_STONES, 5000, "第二名周奖励"),
            LeaderboardReward("weekly_2_cultivation", "修为丹", RewardType.CULTIVATION, 2500, "第二名周奖励"),
        ],
        3: [  # 第三名
            LeaderboardReward("weekly_3_stones", "中量灵石", RewardType.SPIRIT_STONES, 3000, "第三名周奖励"),
            LeaderboardReward("weekly_3_cultivation", "修为丸", RewardType.CULTIVATION, 1500, "第三名周奖励"),
        ],
        10: [  # 前十名
            LeaderboardReward("weekly_10_stones", "灵石", RewardType.SPIRIT_STONES, 500, "前十周奖励"),
        ],
        50: [  # 前五十名
            LeaderboardReward("weekly_50_stones", "灵石", RewardType.SPIRIT_STONES, 200, "前五十周奖励"),
        ],
    }
    
    def __init__(self, data_path: str = "data/leaderboards.json"):
        self.data_path = Path(data_path)
        self.leaderboards: Dict[LeaderboardType, Leaderboard] = {}
        self.claimed_daily_rewards: Dict[str, List[str]] = {}  # player_id -> [claimed_date]
        self.claimed_weekly_rewards: Dict[str, List[str]] = {}  # player_id -> [claimed_week]
        self.awarded_titles: Dict[str, Dict[str, str]] = {}  # player_id -> {title_id: expiry_date}
        
        # 初始化所有排行榜
        for lb_type in LeaderboardType:
            self.leaderboards[lb_type] = Leaderboard(lb_type)
        
        # 加载数据
        self._load_data()
    
    def _load_data(self):
        """加载排行榜数据"""
        if not self.data_path.exists():
            self._save_data()
            return
        
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 加载排行榜
            for lb_type in LeaderboardType:
                lb_key = lb_type.value
                if lb_key in data.get("leaderboards", {}):
                    self.leaderboards[lb_type] = Leaderboard.from_dict(data["leaderboards"][lb_key])
            
            # 加载已领取奖励记录
            self.claimed_daily_rewards = data.get("claimed_daily_rewards", {})
            self.claimed_weekly_rewards = data.get("claimed_weekly_rewards", {})
            self.awarded_titles = data.get("awarded_titles", {})
            
        except Exception as e:
            print(f"加载排行榜数据失败: {e}")
            self._save_data()
    
    def _save_data(self):
        """保存排行榜数据"""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "leaderboards": {
                lb_type.value: lb.to_dict()
                for lb_type, lb in self.leaderboards.items()
            },
            "claimed_daily_rewards": self.claimed_daily_rewards,
            "claimed_weekly_rewards": self.claimed_weekly_rewards,
            "awarded_titles": self.awarded_titles
        }
        
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ==================== 更新排行榜 ====================
    
    def update_player(self, player) -> Dict[str, int]:
        """
        更新玩家所有排行榜数据
        
        Args:
            player: Player 对象
            
        Returns:
            dict: 各排行榜的排名 {排行榜类型: 排名}
        """
        player_id = self._get_player_id(player)
        player_name = player.name
        realm = player.realm
        sect = player.sect
        title = player.current_title_id
        
        rankings = {}
        
        # 战力榜 - 综合战斗力
        power = self._calculate_power(player)
        self.leaderboards[LeaderboardType.POWER].update_entry(
            player_name, player_id, power, realm, sect, title
        )
        rankings[LeaderboardType.POWER.value] = self.leaderboards[LeaderboardType.POWER].get_rank(player_id)
        
        # 修为榜
        self.leaderboards[LeaderboardType.CULTIVATION].update_entry(
            player_name, player_id, player.cultivation, realm, sect, title
        )
        rankings[LeaderboardType.CULTIVATION.value] = self.leaderboards[LeaderboardType.CULTIVATION].get_rank(player_id)
        
        # 境界榜 - 用境界等级数值
        realm_level = player.get_realm_level() if hasattr(player, 'get_realm_level') else 1
        self.leaderboards[LeaderboardType.REALM].update_entry(
            player_name, player_id, realm_level, realm, sect, title
        )
        rankings[LeaderboardType.REALM.value] = self.leaderboards[LeaderboardType.REALM].get_rank(player_id)
        
        # 财富榜
        self.leaderboards[LeaderboardType.WEALTH].update_entry(
            player_name, player_id, player.spirit_stones, realm, sect, title
        )
        rankings[LeaderboardType.WEALTH.value] = self.leaderboards[LeaderboardType.WEALTH].get_rank(player_id)
        
        # 成就榜
        achievement_points = player.total_achievement_points if hasattr(player, 'total_achievement_points') else 0
        self.leaderboards[LeaderboardType.ACHIEVEMENT].update_entry(
            player_name, player_id, achievement_points, realm, sect, title
        )
        rankings[LeaderboardType.ACHIEVEMENT.value] = self.leaderboards[LeaderboardType.ACHIEVEMENT].get_rank(player_id)
        
        self._save_data()
        
        return rankings
    
    def _get_player_id(self, player) -> str:
        """获取玩家唯一ID"""
        # 使用玩家名作为ID（单机模式）
        # 如果需要支持多存档，可以使用存档ID+玩家名
        return player.name
    
    def _calculate_power(self, player) -> int:
        """
        计算玩家综合战斗力
        
        战力 = 基础属性 + 功法加成 + 法宝加成 + 称号加成
        """
        power = 0
        
        # 基础属性
        power += player.stats.get("生命", 0) * 1
        power += player.stats.get("真元", 0) * 1
        power += player.stats.get("攻击", 0) * 5
        power += player.stats.get("防御", 0) * 3
        power += player.stats.get("速度", 0) * 2
        
        # 修为加成
        power += player.cultivation // 100
        
        # 境界加成
        realm_level = player.get_realm_level() if hasattr(player, 'get_realm_level') else 1
        power += realm_level * 1000
        
        # 功法加成
        if hasattr(player, 'learned_skills'):
            for skill_id, level in player.learned_skills.items():
                power += level * 50
        
        # 法宝加成
        if hasattr(player, 'artifacts'):
            power += len(player.artifacts) * 200
        
        return power
    
    # ==================== 查询排行榜 ====================
    
    def get_leaderboard(self, leaderboard_type: LeaderboardType) -> Leaderboard:
        """获取指定排行榜"""
        return self.leaderboards.get(leaderboard_type)
    
    def get_top_players(self, leaderboard_type: LeaderboardType, count: int = 10) -> List[LeaderboardEntry]:
        """获取排行榜前N名"""
        lb = self.leaderboards.get(leaderboard_type)
        if lb:
            return lb.get_top_entries(count)
        return []
    
    def get_player_rank(self, leaderboard_type: LeaderboardType, player_id: str) -> int:
        """获取玩家在指定排行榜的排名"""
        lb = self.leaderboards.get(leaderboard_type)
        if lb:
            return lb.get_rank(player_id)
        return 0
    
    def get_player_entry(self, leaderboard_type: LeaderboardType, player_id: str) -> Optional[LeaderboardEntry]:
        """获取玩家排行榜信息"""
        lb = self.leaderboards.get(leaderboard_type)
        if lb:
            return lb.get_entry(player_id)
        return None
    
    def get_all_player_ranks(self, player_id: str) -> Dict[str, dict]:
        """获取玩家所有排行榜排名"""
        ranks = {}
        for lb_type in LeaderboardType:
            entry = self.get_player_entry(lb_type, player_id)
            if entry:
                ranks[lb_type.value] = {
                    "rank": entry.rank,
                    "value": entry.value
                }
        return ranks
    
    # ==================== 奖励系统 ====================
    
    def get_daily_rewards(self, rank: int) -> List[LeaderboardReward]:
        """获取指定排名的每日奖励"""
        rewards = []
        
        # 第一名
        if rank == 1:
            rewards.extend(self.DAILY_REWARDS.get(1, []))
        # 第二名
        elif rank == 2:
            rewards.extend(self.DAILY_REWARDS.get(2, []))
        # 第三名
        elif rank == 3:
            rewards.extend(self.DAILY_REWARDS.get(3, []))
        
        # 前十都有奖励
        if rank <= 10:
            rewards.extend(self.DAILY_REWARDS.get(10, []))
        
        return rewards
    
    def get_weekly_rewards(self, rank: int) -> List[LeaderboardReward]:
        """获取指定排名的每周奖励"""
        rewards = []
        
        # 第一名
        if rank == 1:
            rewards.extend(self.WEEKLY_REWARDS.get(1, []))
        # 第二名
        elif rank == 2:
            rewards.extend(self.WEEKLY_REWARDS.get(2, []))
        # 第三名
        elif rank == 3:
            rewards.extend(self.WEEKLY_REWARDS.get(3, []))
        
        # 前十
        if rank <= 10:
            rewards.extend(self.WEEKLY_REWARDS.get(10, []))
        
        # 前五十
        if rank <= 50:
            rewards.extend(self.WEEKLY_REWARDS.get(50, []))
        
        return rewards
    
    def can_claim_daily_reward(self, player_id: str) -> bool:
        """检查是否可以领取每日奖励"""
        today = datetime.now().strftime("%Y-%m-%d")
        claimed = self.claimed_daily_rewards.get(player_id, [])
        return today not in claimed
    
    def can_claim_weekly_reward(self, player_id: str) -> bool:
        """检查是否可以领取每周奖励"""
        week = datetime.now().strftime("%Y-W%W")
        claimed = self.claimed_weekly_rewards.get(player_id, [])
        return week not in claimed
    
    def claim_daily_reward(self, player) -> dict:
        """
        领取每日排名奖励
        
        Returns:
            dict: {
                success: bool,
                message: str,
                rewards: List[LeaderboardReward]
            }
        """
        player_id = self._get_player_id(player)
        
        if not self.can_claim_daily_reward(player_id):
            return {
                "success": False,
                "message": "今日已领取过奖励",
                "rewards": []
            }
        
        # 获取玩家在各排行榜的排名，取最高排名
        best_rank = float('inf')
        best_leaderboard = None
        
        for lb_type in LeaderboardType:
            rank = self.get_player_rank(lb_type, player_id)
            if rank > 0 and rank < best_rank:
                best_rank = rank
                best_leaderboard = lb_type
        
        if best_rank == float('inf'):
            return {
                "success": False,
                "message": "未上榜，无法领取奖励",
                "rewards": []
            }
        
        # 获取奖励
        rewards = self.get_daily_rewards(best_rank)
        
        if not rewards:
            return {
                "success": False,
                "message": "排名过低，无奖励可领",
                "rewards": []
            }
        
        # 记录领取
        today = datetime.now().strftime("%Y-%m-%d")
        if player_id not in self.claimed_daily_rewards:
            self.claimed_daily_rewards[player_id] = []
        self.claimed_daily_rewards[player_id].append(today)
        
        # 发放奖励
        self._grant_rewards(player, rewards)
        
        self._save_data()
        
        return {
            "success": True,
            "message": f"领取每日奖励成功！最高排名：{best_leaderboard.value} 第{best_rank}名",
            "rewards": rewards,
            "best_rank": best_rank
        }
    
    def claim_weekly_reward(self, player) -> dict:
        """
        领取每周排名奖励
        
        Returns:
            dict: {
                success: bool,
                message: str,
                rewards: List[LeaderboardReward]
            }
        """
        player_id = self._get_player_id(player)
        
        if not self.can_claim_weekly_reward(player_id):
            return {
                "success": False,
                "message": "本周已领取过奖励",
                "rewards": []
            }
        
        # 获取玩家在各排行榜的排名，取最高排名
        best_rank = float('inf')
        best_leaderboard = None
        
        for lb_type in LeaderboardType:
            rank = self.get_player_rank(lb_type, player_id)
            if rank > 0 and rank < best_rank:
                best_rank = rank
                best_leaderboard = lb_type
        
        if best_rank == float('inf'):
            return {
                "success": False,
                "message": "未上榜，无法领取奖励",
                "rewards": []
            }
        
        # 获取奖励
        rewards = self.get_weekly_rewards(best_rank)
        
        if not rewards:
            return {
                "success": False,
                "message": "排名过低，无奖励可领",
                "rewards": []
            }
        
        # 记录领取
        week = datetime.now().strftime("%Y-W%W")
        if player_id not in self.claimed_weekly_rewards:
            self.claimed_weekly_rewards[player_id] = []
        self.claimed_weekly_rewards[player_id].append(week)
        
        # 发放奖励
        self._grant_rewards(player, rewards)
        
        self._save_data()
        
        return {
            "success": True,
            "message": f"领取每周奖励成功！最高排名：{best_leaderboard.value} 第{best_rank}名",
            "rewards": rewards,
            "best_rank": best_rank
        }
    
    def _grant_rewards(self, player, rewards: List[LeaderboardReward]):
        """发放奖励"""
        for reward in rewards:
            if reward.reward_type == RewardType.SPIRIT_STONES:
                player.spirit_stones += reward.value
            elif reward.reward_type == RewardType.CULTIVATION:
                player.cultivation += reward.value
            elif reward.reward_type == RewardType.REPUTATION:
                if hasattr(player, 'sect_contribution'):
                    player.sect_contribution += reward.value
    
    # ==================== 称号系统 ====================
    
    def get_ranking_title(self, leaderboard_type: LeaderboardType, rank: int) -> Optional[RankingTitle]:
        """获取指定排名的称号"""
        return self.RANKING_TITLES.get((leaderboard_type, rank))
    
    def check_and_award_titles(self, player) -> List[dict]:
        """
        检查并发放排名称号
        
        Returns:
            List[dict]: 获得的称号列表
        """
        player_id = self._get_player_id(player)
        awarded = []
        
        for lb_type in LeaderboardType:
            rank = self.get_player_rank(lb_type, player_id)
            
            if rank in [1, 2, 3]:
                title = self.get_ranking_title(lb_type, rank)
                if title:
                    # 检查是否已有此称号
                    existing = self.awarded_titles.get(player_id, {})
                    title_key = title.title_id
                    
                    # 计算过期时间
                    expiry = (datetime.now() + timedelta(days=title.duration_days)).isoformat()
                    
                    # 记录称号
                    if player_id not in self.awarded_titles:
                        self.awarded_titles[player_id] = {}
                    self.awarded_titles[player_id][title_key] = expiry
                    
                    awarded.append({
                        "title": title,
                        "expiry": expiry
                    })
        
        if awarded:
            self._save_data()
        
        return awarded
    
    def get_player_active_titles(self, player_id: str) -> List[dict]:
        """获取玩家当前有效的排名称号"""
        active = []
        now = datetime.now()
        
        player_titles = self.awarded_titles.get(player_id, {})
        
        for title_id, expiry in player_titles.items():
            expiry_date = datetime.fromisoformat(expiry)
            if expiry_date > now:
                # 找到称号详情
                for (lb_type, rank), title in self.RANKING_TITLES.items():
                    if title.title_id == title_id:
                        active.append({
                            "title": title,
                            "expiry": expiry,
                            "days_remaining": (expiry_date - now).days
                        })
                        break
        
        return active
    
    def is_title_expired(self, player_id: str, title_id: str) -> bool:
        """检查称号是否已过期"""
        player_titles = self.awarded_titles.get(player_id, {})
        expiry = player_titles.get(title_id)
        
        if not expiry:
            return True
        
        return datetime.fromisoformat(expiry) <= datetime.now()
    
    def cleanup_expired_titles(self):
        """清理过期的称号"""
        now = datetime.now()
        cleaned = 0
        
        for player_id in list(self.awarded_titles.keys()):
            expired_titles = []
            
            for title_id, expiry in self.awarded_titles[player_id].items():
                if datetime.fromisoformat(expiry) <= now:
                    expired_titles.append(title_id)
            
            for title_id in expired_titles:
                del self.awarded_titles[player_id][title_id]
                cleaned += 1
            
            if not self.awarded_titles[player_id]:
                del self.awarded_titles[player_id]
        
        if cleaned > 0:
            self._save_data()
        
        return cleaned
    
    # ==================== 排行榜显示 ====================
    
    def get_leaderboard_display(self, leaderboard_type: LeaderboardType, count: int = 10) -> str:
        """获取排行榜显示文本"""
        lb = self.leaderboards.get(leaderboard_type)
        if not lb:
            return "排行榜不存在"
        
        entries = lb.get_top_entries(count)
        
        lines = []
        lines.append(f"【{leaderboard_type.value}】")
        lines.append("═" * 40)
        
        # 值标签
        value_labels = {
            LeaderboardType.POWER: "战力",
            LeaderboardType.CULTIVATION: "修为",
            LeaderboardType.REALM: "境界",
            LeaderboardType.WEALTH: "灵石",
            LeaderboardType.ACHIEVEMENT: "成就点"
        }
        value_label = value_labels.get(leaderboard_type, "数值")
        
        for entry in entries:
            # 排名图标
            if entry.rank == 1:
                rank_icon = "🥇"
            elif entry.rank == 2:
                rank_icon = "🥈"
            elif entry.rank == 3:
                rank_icon = "🥉"
            else:
                rank_icon = f"{entry.rank}."
            
            # 门派信息
            sect_str = f"[{entry.sect}]" if entry.sect else ""
            
            # 称号信息
            title_str = f"<{entry.title}>" if entry.title else ""
            
            # 格式化数值
            if leaderboard_type == LeaderboardType.REALM:
                from config import REALMS
                realm_names = {info["level"]: name for name, info in REALMS.items()}
                value_str = realm_names.get(entry.value, "练气期")
            else:
                value_str = f"{entry.value:,}"
            
            lines.append(
                f"{rank_icon} {entry.player_name} {sect_str}{title_str}"
            )
            lines.append(f"   {value_label}: {value_str}")
        
        if not entries:
            lines.append("暂无排名数据")
        
        return "\n".join(lines)
    
    def get_all_leaderboards_summary(self, player_id: str = None, count: int = 5) -> str:
        """获取所有排行榜概要"""
        lines = []
        lines.append("【蜀山风云榜】")
        lines.append("═" * 50)
        
        for lb_type in LeaderboardType:
            entries = self.get_top_players(lb_type, count)
            
            lines.append(f"\n▸ {lb_type.value}")
            
            if entries:
                for entry in entries[:3]:
                    rank_icon = ["🥇", "🥈", "🥉"][entry.rank - 1] if entry.rank <= 3 else f"{entry.rank}."
                    lines.append(f"  {rank_icon} {entry.player_name} ({entry.value:,})")
            else:
                lines.append("  暂无数据")
            
            # 如果指定了玩家，显示其排名
            if player_id:
                player_entry = self.get_player_entry(lb_type, player_id)
                if player_entry:
                    lines.append(f"  ── 我的排名: 第{player_entry.rank}名")
        
        return "\n".join(lines)
    
    def get_player_rank_card(self, player) -> str:
        """获取玩家排名卡片"""
        player_id = self._get_player_id(player)
        
        lines = []
        lines.append(f"【{player.name} 的排名】")
        lines.append("═" * 30)
        
        for lb_type in LeaderboardType:
            entry = self.get_player_entry(lb_type, player_id)
            if entry:
                # 排名变化标记（可以用不同颜色表示）
                rank_str = f"第{entry.rank}名"
                value_str = f"{entry.value:,}"
                
                lines.append(f"▸ {lb_type.value}: {rank_str} ({value_str})")
            else:
                lines.append(f"▸ {lb_type.value}: 未上榜")
        
        # 显示有效称号
        active_titles = self.get_player_active_titles(player_id)
        if active_titles:
            lines.append("\n【排名称号】")
            for title_info in active_titles:
                title = title_info["title"]
                lines.append(f"  • {title.name} ({title_info['days_remaining']}天后过期)")
        
        # 显示可领取奖励
        can_daily = self.can_claim_daily_reward(player_id)
        can_weekly = self.can_claim_weekly_reward(player_id)
        
        if can_daily or can_weekly:
            lines.append("\n【待领取奖励】")
            if can_daily:
                lines.append("  • 每日奖励可领取")
            if can_weekly:
                lines.append("  • 每周奖励可领取")
        
        return "\n".join(lines)


# ==================== 工具函数 ====================

def create_sample_leaderboard_data() -> dict:
    """创建示例排行榜数据"""
    return {
        "leaderboards": {
            lb_type.value: Leaderboard(lb_type).to_dict()
            for lb_type in LeaderboardType
        },
        "claimed_daily_rewards": {},
        "claimed_weekly_rewards": {},
        "awarded_titles": {}
    }


def init_leaderboard_system(data_path: str = "data/leaderboards.json") -> LeaderboardManager:
    """初始化排行榜系统"""
    return LeaderboardManager(data_path)


# 测试代码
if __name__ == "__main__":
    # 创建排行榜管理器
    manager = LeaderboardManager("data/leaderboards.json")
    
    # 测试显示
    print("排行榜系统测试")
    print("=" * 50)
    
    for lb_type in LeaderboardType:
        print(manager.get_leaderboard_display(lb_type, 5))
        print()
