#!/usr/bin/env python3
"""
蜀山剑侠传 - 活动系统
包含活动类型、限时活动、签到系统、积分兑换、排行奖励
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from pathlib import Path


class EventType(Enum):
    """活动类型"""
    DAILY = "日常"       # 日常活动
    WEEKLY = "周常"      # 周常活动
    FESTIVAL = "节日"    # 节日活动
    SPECIAL = "特殊"     # 特殊活动


class EventStatus(Enum):
    """活动状态"""
    UPCOMING = "即将开始"   # 未开始
    ACTIVE = "进行中"       # 进行中
    ENDED = "已结束"        # 已结束


class EventTaskType(Enum):
    """活动任务类型"""
    KILL = "击杀"           # 击杀怪物
    COLLECT = "收集"        # 收集物品
    EXPLORE = "探索"        # 探索地点
    CULTIVATE = "修炼"      # 修炼次数
    COMBAT = "战斗"         # 战斗次数
    SIGN_IN = "签到"        # 签到
    CONSUME = "消耗"        # 消耗灵石
    BREAKTHROUGH = "突破"   # 突破境界
    TALK = "对话"           # 对话NPC
    SOCIAL = "社交"         # 社交分享


@dataclass
class EventReward:
    """活动奖励"""
    cultivation: int = 0           # 修为
    spirit_stones: int = 0         # 灵石
    karma: int = 0                 # 功德
    points: int = 0                # 活动积分
    artifacts: List[str] = field(default_factory=list)     # 法宝奖励
    skills: List[str] = field(default_factory=list)        # 功法奖励
    materials: Dict[str, int] = field(default_factory=dict) # 材料奖励
    titles: List[str] = field(default_factory=list)        # 称号奖励
    
    def to_dict(self) -> dict:
        return {
            "cultivation": self.cultivation,
            "spirit_stones": self.spirit_stones,
            "karma": self.karma,
            "points": self.points,
            "artifacts": self.artifacts,
            "skills": self.skills,
            "materials": self.materials,
            "titles": self.titles
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "EventReward":
        return cls(
            cultivation=data.get("cultivation", 0),
            spirit_stones=data.get("spirit_stones", 0),
            karma=data.get("karma", 0),
            points=data.get("points", 0),
            artifacts=data.get("artifacts", []),
            skills=data.get("skills", []),
            materials=data.get("materials", {}),
            titles=data.get("titles", [])
        )


@dataclass
class EventTask:
    """活动任务"""
    task_id: str
    task_type: EventTaskType
    target: str                 # 目标名称
    required: int = 1           # 需求数量
    description: str = ""       # 任务描述
    reward: Optional[EventReward] = None  # 完成奖励
    
    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "target": self.target,
            "required": self.required,
            "description": self.description,
            "reward": self.reward.to_dict() if self.reward else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "EventTask":
        return cls(
            task_id=data["task_id"],
            task_type=EventTaskType(data["task_type"]),
            target=data["target"],
            required=data.get("required", 1),
            description=data.get("description", ""),
            reward=EventReward.from_dict(data["reward"]) if data.get("reward") else None
        )


@dataclass
class RankReward:
    """排行奖励"""
    min_rank: int                # 最低排名
    max_rank: int                # 最高排名
    reward: EventReward          # 奖励
    title: Optional[str] = None  # 称号
    
    def to_dict(self) -> dict:
        return {
            "min_rank": self.min_rank,
            "max_rank": self.max_rank,
            "reward": self.reward.to_dict(),
            "title": self.title
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "RankReward":
        return cls(
            min_rank=data["min_rank"],
            max_rank=data["max_rank"],
            reward=EventReward.from_dict(data["reward"]),
            title=data.get("title")
        )


@dataclass
class PointExchange:
    """积分兑换项"""
    exchange_id: str
    name: str                           # 兑换物品名称
    description: str = ""               # 描述
    points_cost: int = 0                # 消耗积分
    reward: Optional[EventReward] = None # 获得奖励
    limit: int = 0                      # 兑换限制(0=无限)
    exchanged_count: int = 0            # 已兑换次数
    
    def to_dict(self) -> dict:
        return {
            "exchange_id": self.exchange_id,
            "name": self.name,
            "description": self.description,
            "points_cost": self.points_cost,
            "reward": self.reward.to_dict() if self.reward else None,
            "limit": self.limit,
            "exchanged_count": self.exchanged_count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PointExchange":
        return cls(
            exchange_id=data["exchange_id"],
            name=data["name"],
            description=data.get("description", ""),
            points_cost=data.get("points_cost", 0),
            reward=EventReward.from_dict(data["reward"]) if data.get("reward") else None,
            limit=data.get("limit", 0),
            exchanged_count=data.get("exchanged_count", 0)
        )


@dataclass
class Event:
    """活动"""
    event_id: str
    name: str
    description: str
    event_type: EventType
    start_time: str               # 开始时间 (ISO格式或相对时间)
    end_time: str                 # 结束时间
    status: EventStatus = EventStatus.UPCOMING
    tasks: List[EventTask] = field(default_factory=list)
    rewards: List[EventReward] = field(default_factory=list)     # 阶段奖励
    rank_rewards: List[RankReward] = field(default_factory=list) # 排行奖励
    point_exchanges: List[PointExchange] = field(default_factory=list) # 积分兑换
    prerequisites: List[str] = field(default_factory=list)       # 前置条件
    icon: str = ""                # 活动图标
    banner: str = ""              # 活动横幅
    
    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "name": self.name,
            "description": self.description,
            "event_type": self.event_type.value,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status.value,
            "tasks": [t.to_dict() for t in self.tasks],
            "rewards": [r.to_dict() for r in self.rewards],
            "rank_rewards": [r.to_dict() for r in self.rank_rewards],
            "point_exchanges": [e.to_dict() for e in self.point_exchanges],
            "prerequisites": self.prerequisites,
            "icon": self.icon,
            "banner": self.banner
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        return cls(
            event_id=data["event_id"],
            name=data["name"],
            description=data["description"],
            event_type=EventType(data["event_type"]),
            start_time=data["start_time"],
            end_time=data["end_time"],
            status=EventStatus(data.get("status", "即将开始")),
            tasks=[EventTask.from_dict(t) for t in data.get("tasks", [])],
            rewards=[EventReward.from_dict(r) for r in data.get("rewards", [])],
            rank_rewards=[RankReward.from_dict(r) for r in data.get("rank_rewards", [])],
            point_exchanges=[PointExchange.from_dict(e) for e in data.get("point_exchanges", [])],
            prerequisites=data.get("prerequisites", []),
            icon=data.get("icon", ""),
            banner=data.get("banner", "")
        )
    
    def is_active(self) -> bool:
        """检查活动是否进行中"""
        now = datetime.now()
        try:
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            return start <= now <= end
        except:
            return self.status == EventStatus.ACTIVE
    
    def get_remaining_time(self) -> str:
        """获取剩余时间描述"""
        now = datetime.now()
        try:
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            
            if now < start:
                delta = start - now
                return f"距离开始: {self._format_delta(delta)}"
            elif now > end:
                return "已结束"
            else:
                delta = end - now
                return f"剩余: {self._format_delta(delta)}"
        except:
            return "时间未知"
    
    def _format_delta(self, delta: timedelta) -> str:
        """格式化时间差"""
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}天{hours}小时"
        elif hours > 0:
            return f"{hours}小时{minutes}分钟"
        elif minutes > 0:
            return f"{minutes}分钟"
        else:
            return f"{seconds}秒"


# ==================== 签到系统 ====================

@dataclass
class SignInReward:
    """签到奖励"""
    day: int                      # 第几天
    reward: EventReward           # 奖励
    is_special: bool = False      # 是否特殊奖励(连续签到)
    
    def to_dict(self) -> dict:
        return {
            "day": self.day,
            "reward": self.reward.to_dict(),
            "is_special": self.is_special
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SignInReward":
        return cls(
            day=data["day"],
            reward=EventReward.from_dict(data["reward"]),
            is_special=data.get("is_special", False)
        )


class SignInSystem:
    """签到系统"""
    
    def __init__(self):
        self.daily_rewards: List[SignInReward] = []      # 每日签到奖励
        self.consecutive_rewards: Dict[int, EventReward] = {}  # 连续签到奖励
        self.monthly_rewards: Dict[int, EventReward] = {}      # 月度签到奖励
        self.player_sign_data: Dict[str, Dict] = {}    # 玩家签到数据
        
        self._init_default_rewards()
    
    def _init_default_rewards(self):
        """初始化默认签到奖励"""
        # 每日签到奖励 (7天循环)
        daily_rewards = [
            (1, 50, 100, 5),    # 第1天: 50修为, 100灵石, 5功德
            (2, 60, 120, 5),
            (3, 70, 140, 5),
            (4, 80, 160, 10),
            (5, 90, 180, 10),
            (6, 100, 200, 10),
            (7, 150, 300, 20),  # 第7天: 豪华奖励
        ]
        
        for day, cult, stones, karma in daily_rewards:
            self.daily_rewards.append(SignInReward(
                day=day,
                reward=EventReward(cultivation=cult, spirit_stones=stones, karma=karma),
                is_special=(day == 7)
            ))
        
        # 连续签到奖励
        self.consecutive_rewards = {
            7: EventReward(cultivation=500, spirit_stones=500, karma=50, materials={"灵石矿": 5}),
            14: EventReward(cultivation=1000, spirit_stones=1000, karma=100, materials={"玄铁": 3}),
            21: EventReward(cultivation=2000, spirit_stones=1500, karma=150, materials={"天雷石": 2}),
            30: EventReward(cultivation=5000, spirit_stones=3000, karma=300, artifacts=["签到法宝·七星剑"]),
        }
        
        # 月度签到奖励 (全勤)
        self.monthly_rewards = {
            28: EventReward(cultivation=10000, spirit_stones=5000, karma=500, titles=["勤奋修士"]),
        }
    
    def sign_in(self, player_id: str) -> Dict[str, Any]:
        """
        玩家签到
        返回: {success, message, rewards, consecutive_days, total_days}
        """
        now = datetime.now()
        today = now.date()
        
        # 初始化玩家数据
        if player_id not in self.player_sign_data:
            self.player_sign_data[player_id] = {
                "last_sign_date": None,
                "consecutive_days": 0,
                "total_days": 0,
                "month_days": 0,
                "last_month": now.month,
                "claimed_consecutive": [],  # 已领取的连续签到奖励
                "claimed_monthly": []       # 已领取的月度奖励
            }
        
        data = self.player_sign_data[player_id]
        last_sign = data["last_sign_date"]
        
        # 检查是否已签到
        if last_sign and datetime.fromisoformat(last_sign).date() == today:
            return {
                "success": False,
                "message": "今日已签到，请明天再来~",
                "consecutive_days": data["consecutive_days"],
                "total_days": data["total_days"]
            }
        
        # 更新连续签到天数
        if last_sign:
            last_date = datetime.fromisoformat(last_sign).date()
            if (today - last_date).days == 1:
                data["consecutive_days"] += 1
            else:
                data["consecutive_days"] = 1  # 中断，重新开始
        else:
            data["consecutive_days"] = 1
        
        # 检查月份变化
        if data["last_month"] != now.month:
            data["month_days"] = 0
            data["last_month"] = now.month
            data["claimed_monthly"] = []
        
        data["month_days"] += 1
        data["total_days"] += 1
        data["last_sign_date"] = now.isoformat()
        
        # 计算奖励
        rewards = []
        day_in_cycle = ((data["consecutive_days"] - 1) % 7) + 1
        
        # 基础签到奖励
        daily_reward = self.daily_rewards[day_in_cycle - 1]
        rewards.append({
            "type": "daily",
            "name": f"第{day_in_cycle}天签到奖励",
            "reward": daily_reward.reward.to_dict()
        })
        
        # 连续签到奖励
        if data["consecutive_days"] in self.consecutive_rewards:
            if data["consecutive_days"] not in data["claimed_consecutive"]:
                rewards.append({
                    "type": "consecutive",
                    "name": f"连续签到{data['consecutive_days']}天奖励",
                    "reward": self.consecutive_rewards[data["consecutive_days"]].to_dict()
                })
                data["claimed_consecutive"].append(data["consecutive_days"])
        
        # 月度全勤奖励
        if data["month_days"] in self.monthly_rewards:
            if data["month_days"] not in data["claimed_monthly"]:
                rewards.append({
                    "type": "monthly",
                    "name": f"本月签到{data['month_days']}天奖励",
                    "reward": self.monthly_rewards[data["month_days"]].to_dict()
                })
                data["claimed_monthly"].append(data["month_days"])
        
        return {
            "success": True,
            "message": f"签到成功！已连续签到{data['consecutive_days']}天",
            "rewards": rewards,
            "consecutive_days": data["consecutive_days"],
            "total_days": data["total_days"],
            "month_days": data["month_days"]
        }
    
    def get_sign_in_status(self, player_id: str) -> Dict[str, Any]:
        """获取玩家签到状态"""
        if player_id not in self.player_sign_data:
            return {
                "consecutive_days": 0,
                "total_days": 0,
                "month_days": 0,
                "today_signed": False
            }
        
        data = self.player_sign_data[player_id]
        today = datetime.now().date()
        last_sign = data["last_sign_date"]
        today_signed = last_sign and datetime.fromisoformat(last_sign).date() == today
        
        return {
            "consecutive_days": data["consecutive_days"],
            "total_days": data["total_days"],
            "month_days": data["month_days"],
            "today_signed": today_signed,
            "next_consecutive_reward": self._get_next_consecutive_reward(data["consecutive_days"])
        }
    
    def _get_next_consecutive_reward(self, current_days: int) -> Optional[int]:
        """获取下一个连续签到奖励天数"""
        for days in sorted(self.consecutive_rewards.keys()):
            if days > current_days:
                return days
        return None


# ==================== 活动管理器 ====================

class EventManager:
    """活动管理器"""
    
    def __init__(self):
        self.events: Dict[str, Event] = {}           # 所有活动
        self.player_event_data: Dict[str, Dict] = {} # 玩家活动数据
        self.sign_in_system = SignInSystem()         # 签到系统
        self._load_events()
    
    def _load_events(self):
        """从JSON加载活动数据"""
        data_path = Path(__file__).parent.parent / "data" / "events.json"
        if data_path.exists():
            try:
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for event_data in data.get("events", []):
                        event = Event.from_dict(event_data)
                        self.events[event.event_id] = event
            except Exception as e:
                print(f"加载活动数据失败: {e}")
    
    def get_active_events(self) -> List[Event]:
        """获取所有进行中的活动"""
        return [e for e in self.events.values() if e.is_active()]
    
    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        """按类型获取活动"""
        return [e for e in self.events.values() if e.event_type == event_type]
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """获取指定活动"""
        return self.events.get(event_id)
    
    def join_event(self, player_id: str, event_id: str) -> Dict[str, Any]:
        """玩家参加活动"""
        event = self.events.get(event_id)
        if not event:
            return {"success": False, "message": "活动不存在"}
        
        if not event.is_active():
            return {"success": False, "message": "活动未开启或已结束"}
        
        # 初始化玩家活动数据
        if player_id not in self.player_event_data:
            self.player_event_data[player_id] = {}
        
        if event_id not in self.player_event_data[player_id]:
            self.player_event_data[player_id][event_id] = {
                "joined": True,
                "join_time": datetime.now().isoformat(),
                "points": 0,
                "task_progress": {},
                "claimed_rewards": [],
                "rank": 0
            }
        else:
            return {"success": True, "message": "已参加该活动", "data": self.player_event_data[player_id][event_id]}
        
        return {
            "success": True,
            "message": f"成功参加【{event.name}】活动！",
            "data": self.player_event_data[player_id][event_id]
        }
    
    def update_task_progress(self, player_id: str, event_id: str, task_id: str, 
                            progress: int = 1) -> Dict[str, Any]:
        """更新活动任务进度"""
        if player_id not in self.player_event_data:
            return {"success": False, "message": "未参加该活动"}
        
        if event_id not in self.player_event_data[player_id]:
            return {"success": False, "message": "未参加该活动"}
        
        event = self.events.get(event_id)
        if not event:
            return {"success": False, "message": "活动不存在"}
        
        data = self.player_event_data[player_id][event_id]
        
        # 更新任务进度
        if task_id not in data["task_progress"]:
            data["task_progress"][task_id] = 0
        data["task_progress"][task_id] += progress
        
        # 查找任务
        task = None
        for t in event.tasks:
            if t.task_id == task_id:
                task = t
                break
        
        if not task:
            return {"success": False, "message": "任务不存在"}
        
        result = {
            "success": True,
            "task_id": task_id,
            "current": data["task_progress"][task_id],
            "required": task.required,
            "completed": data["task_progress"][task_id] >= task.required
        }
        
        # 任务完成奖励
        if result["completed"] and task.reward and task_id not in data.get("completed_tasks", []):
            if "completed_tasks" not in data:
                data["completed_tasks"] = []
            data["completed_tasks"].append(task_id)
            data["points"] += task.reward.points
            result["reward"] = task.reward.to_dict()
        
        return result
    
    def claim_reward(self, player_id: str, event_id: str, reward_index: int) -> Dict[str, Any]:
        """领取活动奖励"""
        if player_id not in self.player_event_data:
            return {"success": False, "message": "未参加该活动"}
        
        if event_id not in self.player_event_data[player_id]:
            return {"success": False, "message": "未参加该活动"}
        
        event = self.events.get(event_id)
        if not event:
            return {"success": False, "message": "活动不存在"}
        
        if reward_index >= len(event.rewards):
            return {"success": False, "message": "奖励不存在"}
        
        data = self.player_event_data[player_id][event_id]
        
        if reward_index in data["claimed_rewards"]:
            return {"success": False, "message": "奖励已领取"}
        
        reward = event.rewards[reward_index]
        
        # 检查积分是否足够
        if data["points"] < reward.points:
            return {"success": False, "message": f"积分不足，需要{reward.points}积分"}
        
        data["claimed_rewards"].append(reward_index)
        
        return {
            "success": True,
            "message": "奖励领取成功！",
            "reward": reward.to_dict()
        }
    
    def exchange_points(self, player_id: str, event_id: str, 
                       exchange_id: str) -> Dict[str, Any]:
        """积分兑换"""
        if player_id not in self.player_event_data:
            return {"success": False, "message": "未参加该活动"}
        
        if event_id not in self.player_event_data[player_id]:
            return {"success": False, "message": "未参加该活动"}
        
        event = self.events.get(event_id)
        if not event:
            return {"success": False, "message": "活动不存在"}
        
        # 查找兑换项
        exchange = None
        for e in event.point_exchanges:
            if e.exchange_id == exchange_id:
                exchange = e
                break
        
        if not exchange:
            return {"success": False, "message": "兑换项不存在"}
        
        data = self.player_event_data[player_id][event_id]
        
        # 检查积分
        if data["points"] < exchange.points_cost:
            return {"success": False, "message": f"积分不足，需要{exchange.points_cost}积分"}
        
        # 检查兑换次数
        if exchange.limit > 0:
            exchanged = data.get("exchanges", {}).get(exchange_id, 0)
            if exchanged >= exchange.limit:
                return {"success": False, "message": "兑换次数已达上限"}
        
        # 扣除积分
        data["points"] -= exchange.points_cost
        
        # 记录兑换
        if "exchanges" not in data:
            data["exchanges"] = {}
        data["exchanges"][exchange_id] = data["exchanges"].get(exchange_id, 0) + 1
        
        return {
            "success": True,
            "message": f"兑换成功！获得【{exchange.name}】",
            "reward": exchange.reward.to_dict() if exchange.reward else None,
            "remaining_points": data["points"]
        }
    
    def get_player_event_data(self, player_id: str, event_id: str) -> Optional[Dict]:
        """获取玩家活动数据"""
        if player_id not in self.player_event_data:
            return None
        return self.player_event_data[player_id].get(event_id)
    
    def get_event_rank(self, event_id: str) -> List[Dict[str, Any]]:
        """获取活动排行榜"""
        event = self.events.get(event_id)
        if not event or not event.rank_rewards:
            return []
        
        # 收集所有参与玩家的积分
        rankings = []
        for player_id, events in self.player_event_data.items():
            if event_id in events:
                rankings.append({
                    "player_id": player_id,
                    "points": events[event_id]["points"]
                })
        
        # 按积分排序
        rankings.sort(key=lambda x: x["points"], reverse=True)
        
        # 添加排名
        for i, r in enumerate(rankings):
            r["rank"] = i + 1
        
        return rankings[:100]  # 返回前100名


# 导出
__all__ = [
    'EventType', 'EventStatus', 'EventTaskType',
    'EventReward', 'EventTask', 'RankReward', 'PointExchange', 'Event',
    'SignInReward', 'SignInSystem',
    'EventManager'
]
