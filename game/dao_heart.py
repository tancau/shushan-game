#!/usr/bin/env python3
"""
蜀山剑侠传 - 道心系统
正邪选择、功德业力系统
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import random


class DaoHeartType(Enum):
    """道心类型"""
    RIGHTEOUS = "正道"      # 正道 - 功德高
    DEMONIC = "魔道"        # 魔道 - 业力高
    EVIL = "邪道"           # 邪道 - 极端业力
    CHAOS = "混沌"          # 混沌 - 功德业力平衡


class KarmaType(Enum):
    """因果类型"""
    MERIT = "功德"          # 正面因果
    SIN = "业力"            # 负面因果


class ActionType(Enum):
    """行为类型"""
    # 正道行为
    SAVE_LIFE = ("救人性命", 50, KarmaType.MERIT)
    EXORCISE_DEMON = ("斩妖除魔", 30, KarmaType.MERIT)
    HELP_WEAK = "扶弱济贫", 10, KarmaType.MERIT
    PROTECT_INNOCENT = ("护佑平民", 20, KarmaType.MERIT)
    MERCY = ("宽恕敌人", 15, KarmaType.MERIT)
    TEACH_DAO = ("传道授业", 25, KarmaType.MERIT)
    DONATE = ("布施财物", 5, KarmaType.MERIT)
    GUARD_SEAL = ("守护封印", 40, KarmaType.MERIT)
    PURIFY_EVIL = ("净化邪气", 35, KarmaType.MERIT)
    UPHOLD_JUSTICE = ("主持公道", 20, KarmaType.MERIT)
    
    # 邪道行为
    KILL_INNOCENT = ("滥杀无辜", 100, KarmaType.SIN)
    CULTIVATE_BLOOD = ("血祭修炼", 80, KarmaType.SIN)
    BETRAY_SECT = ("背叛师门", 60, KarmaType.SIN)
    STEAL_TREASURE = ("盗取宝物", 30, KarmaType.SIN)
    HARM_WEAK = ("欺凌弱小", 40, KarmaType.SIN)
    CORRUPT_SOUL = ("炼化生魂", 90, KarmaType.SIN)
    BREAK_SEAL = ("破坏封印", 50, KarmaType.SIN)
    SPREAD_EVIL = ("散布邪气", 45, KarmaType.SIN)
    DECEIVE = ("欺瞒师长", 25, KarmaType.SIN)
    MURDER_FOR_GAIN = ("杀人夺宝", 70, KarmaType.SIN)
    
    # 中性行为
    NEUTRAL_KILL = ("斩杀敌人", 5, KarmaType.SIN)  # 战斗击杀，业力较少
    SELF_DEFENSE = ("正当防卫", 0, None)          # 无因果
    
    # 渡劫行为
    TRIBULATION_SUCCESS = ("渡劫成功", 100, KarmaType.MERIT)  # 渡劫成功，功德大增
    TRIBULATION_FAILURE = ("渡劫失败", 20, KarmaType.SIN)     # 渡劫失败，业力增加
    
    def __new__(cls, display_name: str, value: int, karma_type: Optional[KarmaType]):
        obj = object.__new__(cls)
        obj._value_ = display_name
        obj.display_name = display_name
        obj.karma_value = value
        obj.karma_type = karma_type
        return obj


@dataclass
class KarmaRecord:
    """因果记录"""
    action_type: ActionType
    karma_type: Optional[KarmaType]
    value: int
    description: str
    timestamp: str = ""  # 游戏时间


@dataclass
class MeritReward:
    """功德奖励"""
    name: str
    description: str
    merit_cost: int
    effect_type: str  # "buff", "item", "skill", "chance"
    effect_value: Dict
    duration: int = 0  # 持续时间（游戏天数），0表示永久


@dataclass
class SinPenalty:
    """业力惩罚"""
    name: str
    description: str
    sin_threshold: int  # 触发业力阈值
    penalty_type: str   # "debuff", "event", "difficulty"
    penalty_value: Dict
    severity: int = 1   # 严重程度 1-5


class MeritShop:
    """功德商店"""
    
    def __init__(self):
        self.items = self._init_shop_items()
    
    def _init_shop_items(self) -> List[MeritReward]:
        """初始化功德商店物品"""
        return [
            # 永久增益
            MeritReward(
                name="天道庇佑",
                description="渡劫成功率 +10%",
                merit_cost=500,
                effect_type="buff",
                effect_value={"tribulation_success_rate": 0.1},
                duration=0
            ),
            MeritReward(
                name="福缘深厚",
                description="奇遇概率 +5%",
                merit_cost=300,
                effect_type="buff",
                effect_value={"encounter_chance": 0.05},
                duration=0
            ),
            MeritReward(
                name="正气护体",
                description="对邪魔伤害 +20%",
                merit_cost=400,
                effect_type="buff",
                effect_value={"damage_vs_evil": 0.2},
                duration=0
            ),
            MeritReward(
                name="道心稳固",
                description="心魔强度 -20%",
                merit_cost=600,
                effect_type="buff",
                effect_value={"heart_demon_reduction": 0.2},
                duration=0
            ),
            
            # 临时增益
            MeritReward(
                name="天赐灵丹",
                description="恢复全部生命和真元",
                merit_cost=50,
                effect_type="item",
                effect_value={"heal_all": True},
                duration=0
            ),
            MeritReward(
                name="悟道机缘",
                description="修炼速度 +50%（持续7天）",
                merit_cost=200,
                effect_type="buff",
                effect_value={"cultivation_speed": 0.5},
                duration=7
            ),
            
            # 特殊能力
            MeritReward(
                name="因果之眼",
                description="可查看NPC善恶值",
                merit_cost=1000,
                effect_type="skill",
                effect_value={"see_karma": True},
                duration=0
            ),
            MeritReward(
                name="天命护符",
                description="死亡时免死一次（消耗护符）",
                merit_cost=800,
                effect_type="item",
                effect_value={"death_ward": True},
                duration=0
            ),
        ]
    
    def get_available_items(self, current_merit: int) -> List[Dict]:
        """获取可购买的物品"""
        items = []
        for item in self.items:
            items.append({
                "name": item.name,
                "description": item.description,
                "merit_cost": item.merit_cost,
                "can_afford": current_merit >= item.merit_cost,
                "effect_type": item.effect_type,
                "duration": item.duration
            })
        return items
    
    def purchase(self, item_name: str, current_merit: int) -> Tuple[bool, str, Optional[MeritReward]]:
        """购买功德物品"""
        for item in self.items:
            if item.name == item_name:
                if current_merit < item.merit_cost:
                    return False, f"功德不足，需要 {item.merit_cost} 功德", None
                return True, f"成功兑换【{item.name}】", item
        return False, "未找到该物品", None


class SinPenaltySystem:
    """业力惩罚系统"""
    
    def __init__(self):
        self.penalties = self._init_penalties()
    
    def _init_penalties(self) -> List[SinPenalty]:
        """初始化业力惩罚"""
        return [
            SinPenalty(
                name="心魔初现",
                description="心魔强度 +10%",
                sin_threshold=50,
                penalty_type="debuff",
                penalty_value={"heart_demon_strength": 0.1},
                severity=1
            ),
            SinPenalty(
                name="业障缠身",
                description="修炼速度 -10%",
                sin_threshold=100,
                penalty_type="debuff",
                penalty_value={"cultivation_speed": -0.1},
                severity=2
            ),
            SinPenalty(
                name="天罚预警",
                description="渡劫难度 +20%",
                sin_threshold=200,
                penalty_type="difficulty",
                penalty_value={"tribulation_difficulty": 0.2},
                severity=3
            ),
            SinPenalty(
                name="正道排斥",
                description="正道NPC好感度 -20",
                sin_threshold=300,
                penalty_type="debuff",
                penalty_value={"righteous_faction_penalty": -20},
                severity=3
            ),
            SinPenalty(
                name="心魔深重",
                description="心魔强度 +30%，渡劫难度 +30%",
                sin_threshold=500,
                penalty_type="debuff",
                penalty_value={
                    "heart_demon_strength": 0.3,
                    "tribulation_difficulty": 0.3
                },
                severity=4
            ),
            SinPenalty(
                name="天劫将至",
                description="随机触发天劫，渡劫失败几率大增",
                sin_threshold=800,
                penalty_type="event",
                penalty_value={"random_tribulation": True},
                severity=5
            ),
            SinPenalty(
                name="万劫不复",
                description="道心崩塌，陷入魔道深渊",
                sin_threshold=1000,
                penalty_type="debuff",
                penalty_value={
                    "dao_heart_collapse": True,
                    "all_stats_penalty": -0.3
                },
                severity=5
            ),
        ]
    
    def get_active_penalties(self, current_sin: int) -> List[Dict]:
        """获取当前生效的惩罚"""
        active = []
        for penalty in self.penalties:
            if current_sin >= penalty.sin_threshold:
                active.append({
                    "name": penalty.name,
                    "description": penalty.description,
                    "severity": penalty.severity,
                    "penalty_type": penalty.penalty_type,
                    "penalty_value": penalty.penalty_value
                })
        return active
    
    def get_next_penalty(self, current_sin: int) -> Optional[Dict]:
        """获取下一个惩罚阈值"""
        for penalty in self.penalties:
            if current_sin < penalty.sin_threshold:
                return {
                    "name": penalty.name,
                    "description": penalty.description,
                    "threshold": penalty.sin_threshold,
                    "sin_needed": penalty.sin_threshold - current_sin
                }
        return None


class DaoHeart:
    """道心系统核心类"""
    
    def __init__(self):
        self.merit: int = 0           # 功德值
        self.sin: int = 0             # 业力值
        self.dao_heart_type: DaoHeartType = DaoHeartType.CHAOS  # 初始为混沌
        
        self.karma_records: List[KarmaRecord] = []  # 因果记录
        self.merit_shop = MeritShop()               # 功德商店
        self.sin_penalty = SinPenaltySystem()       # 业力惩罚系统
        
        # 已购买的功德效果
        self.active_merit_effects: Dict[str, Dict] = {}  # name -> {effect, expire_time}
        self.permanent_buffs: Dict[str, float] = {}      # 永久增益
    
    def add_karma(self, action_type: ActionType, description: str = "") -> Dict:
        """添加因果记录"""
        record = KarmaRecord(
            action_type=action_type,
            karma_type=action_type.karma_type,
            value=action_type.karma_value,
            description=description or action_type.display_name
        )
        
        self.karma_records.append(record)
        
        if action_type.karma_type == KarmaType.MERIT:
            self.merit += action_type.karma_value
        elif action_type.karma_type == KarmaType.SIN:
            self.sin += action_type.karma_value
        
        # 更新道心类型
        old_type = self.dao_heart_type
        self._update_dao_heart_type()
        
        result = {
            "action": action_type.display_name,
            "karma_type": action_type.karma_type.value if action_type.karma_type else "无",
            "value": action_type.karma_value,
            "total_merit": self.merit,
            "total_sin": self.sin,
            "dao_heart_changed": old_type != self.dao_heart_type
        }
        
        if result["dao_heart_changed"]:
            result["new_dao_heart"] = self.dao_heart_type.value
        
        return result
    
    def _update_dao_heart_type(self):
        """更新道心类型"""
        diff = self.merit - self.sin
        
        if diff > 500:
            self.dao_heart_type = DaoHeartType.RIGHTEOUS
        elif self.sin > 500 and self.sin > self.merit * 2:
            self.dao_heart_type = DaoHeartType.EVIL
        elif self.sin > 200 and self.sin > self.merit:
            self.dao_heart_type = DaoHeartType.DEMONIC
        else:
            self.dao_heart_type = DaoHeartType.CHAOS
    
    def get_dao_heart_info(self) -> Dict:
        """获取道心信息"""
        return {
            "type": self.dao_heart_type.value,
            "merit": self.merit,
            "sin": self.sin,
            "balance": self.merit - self.sin,
            "description": self._get_dao_heart_description()
        }
    
    def _get_dao_heart_description(self) -> str:
        """获取道心描述"""
        descriptions = {
            DaoHeartType.RIGHTEOUS: "正气凛然，天命所归。正道人士敬仰，邪魔畏惧。",
            DaoHeartType.DEMONIC: "魔心深种，正邪难辨。行事诡谲，独断独行。",
            DaoHeartType.EVIL: "堕入魔道，为正道所不容。心魔缠身，渡劫艰难。",
            DaoHeartType.CHAOS: "道心混沌，正邪未分。未来何去何从，全在一念之间。"
        }
        return descriptions[self.dao_heart_type]
    
    # ==================== 功德系统 ====================
    
    def get_merit_shop(self) -> List[Dict]:
        """获取功德商店物品"""
        return self.merit_shop.get_available_items(self.merit)
    
    def purchase_merit_item(self, item_name: str) -> Tuple[bool, str]:
        """购买功德物品"""
        success, message, item = self.merit_shop.purchase(item_name, self.merit)
        
        if success and item:
            self.merit -= item.merit_cost
            
            # 应用效果
            if item.duration == 0:
                # 永久效果
                for key, value in item.effect_value.items():
                    if key in self.permanent_buffs:
                        self.permanent_buffs[key] += value
                    else:
                        self.permanent_buffs[key] = value
            else:
                # 临时效果（需要外部系统处理过期）
                self.active_merit_effects[item.name] = {
                    "effect": item.effect_value,
                    "duration": item.duration
                }
            
            return True, f"消耗 {item.merit_cost} 功德，{message}"
        
        return False, message
    
    def get_merit_bonuses(self) -> Dict[str, float]:
        """获取功德加成"""
        bonuses = self.permanent_buffs.copy()
        
        # 添加临时效果
        for effect_data in self.active_merit_effects.values():
            for key, value in effect_data["effect"].items():
                if key in bonuses:
                    bonuses[key] += value
                else:
                    bonuses[key] = value
        
        return bonuses
    
    def reduce_merit(self, amount: int, reason: str = "") -> bool:
        """消耗功德"""
        if self.merit < amount:
            return False
        self.merit -= amount
        return True
    
    # ==================== 业力系统 ====================
    
    def get_active_penalties(self) -> List[Dict]:
        """获取当前生效的业力惩罚"""
        return self.sin_penalty.get_active_penalties(self.sin)
    
    def get_sin_effects(self) -> Dict[str, float]:
        """获取业力效果（负面增益）"""
        effects = {}
        for penalty in self.get_active_penalties():
            if penalty["penalty_type"] == "debuff":
                for key, value in penalty["penalty_value"].items():
                    if key in effects:
                        effects[key] += value
                    else:
                        effects[key] = value
        return effects
    
    def reduce_sin(self, amount: int, reason: str = "") -> bool:
        """消除业力"""
        actual_reduction = min(amount, self.sin)
        self.sin -= actual_reduction
        self._update_dao_heart_type()
        return actual_reduction > 0
    
    def can_reduce_sin(self) -> Dict:
        """获取消业方式"""
        methods = [
            {
                "method": "闭关忏悔",
                "sin_reduction": 10,
                "cost": {"time": 1, "spirit_stones": 100},
                "description": "闭关一天，反省己过，消除10点业力"
            },
            {
                "method": "行善积德",
                "sin_reduction": 20,
                "cost": {"merit": 100},
                "description": "以功德抵消业力，100功德消除20业力"
            },
            {
                "method": "斩妖除魔",
                "sin_reduction": 30,
                "cost": {"kills": 10, "targets": ["妖魔", "邪修"]},
                "description": "斩杀10只妖魔或邪修，消除30点业力"
            },
            {
                "method": "护佑凡人",
                "sin_reduction": 50,
                "cost": {"time": 7, "merit": 200},
                "description": "花费7天护佑凡人村落，消耗200功德，消除50业力"
            },
            {
                "method": "天劫洗礼",
                "sin_reduction": 100,
                "cost": {"tribulation": True},
                "description": "主动引发天劫，渡劫成功消除100业力（失败则...）"
            }
        ]
        return {"methods": methods}
    
    # ==================== 特殊效果 ====================
    
    def get_npc_relation_modifier(self, npc_faction: str) -> int:
        """获取NPC好感度修正"""
        modifiers = {
            DaoHeartType.RIGHTEOUS: {
                "正道": 20,
                "中立": 0,
                "邪道": -20
            },
            DaoHeartType.DEMONIC: {
                "正道": -10,
                "中立": 0,
                "邪道": 10
            },
            DaoHeartType.EVIL: {
                "正道": -30,
                "中立": -10,
                "邪道": 20
            },
            DaoHeartType.CHAOS: {
                "正道": 0,
                "中立": 0,
                "邪道": 0
            }
        }
        return modifiers[self.dao_heart_type].get(npc_faction, 0)
    
    def get_encounter_modifier(self) -> float:
        """获取奇遇概率修正"""
        base = 0.0
        
        # 正道功德加成
        if self.dao_heart_type == DaoHeartType.RIGHTEOUS:
            base += min(0.1, self.merit / 5000)  # 最多+10%
        
        # 业力惩罚
        penalties = self.get_active_penalties()
        for p in penalties:
            if p["penalty_type"] == "debuff" and "encounter_chance" in p["penalty_value"]:
                base += p["penalty_value"]["encounter_chance"]
        
        return base
    
    def get_tribulation_modifier(self) -> Dict:
        """获取渡劫修正"""
        modifier = {
            "success_rate": 0.0,
            "difficulty": 0.0,
            "heart_demon_strength": 0.0
        }
        
        # 功德加成
        if self.merit > 0:
            modifier["success_rate"] += min(0.2, self.merit / 2000)
        
        # 正道额外加成
        if self.dao_heart_type == DaoHeartType.RIGHTEOUS:
            modifier["success_rate"] += 0.1
        
        # 业力惩罚
        penalties = self.get_active_penalties()
        for p in penalties:
            if p["penalty_type"] == "debuff":
                pv = p["penalty_value"]
                modifier["difficulty"] += pv.get("tribulation_difficulty", 0)
                modifier["heart_demon_strength"] += pv.get("heart_demon_strength", 0)
        
        return modifier
    
    def get_combat_modifier(self, enemy_type: str) -> Dict:
        """获取战斗修正"""
        modifier = {"damage_bonus": 0.0, "defense_bonus": 0.0}
        
        bonuses = self.get_merit_bonuses()
        
        # 对邪魔伤害加成
        if enemy_type in ["妖魔", "邪修", "魔物"]:
            modifier["damage_bonus"] += bonuses.get("damage_vs_evil", 0)
        
        return modifier
    
    # ==================== 存档 ====================
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "merit": self.merit,
            "sin": self.sin,
            "dao_heart_type": self.dao_heart_type.value,
            "karma_records": [
                {
                    "action": r.action_type.display_name,
                    "karma_type": r.karma_type.value if r.karma_type else None,
                    "value": r.value,
                    "description": r.description
                }
                for r in self.karma_records[-100:]  # 只保留最近100条
            ],
            "permanent_buffs": self.permanent_buffs,
            "active_merit_effects": self.active_merit_effects
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DaoHeart":
        """从字典创建"""
        dao_heart = cls()
        dao_heart.merit = data.get("merit", 0)
        dao_heart.sin = data.get("sin", 0)
        
        # 恢复道心类型
        type_str = data.get("dao_heart_type", "混沌")
        for t in DaoHeartType:
            if t.value == type_str:
                dao_heart.dao_heart_type = t
                break
        
        dao_heart.permanent_buffs = data.get("permanent_buffs", {})
        dao_heart.active_merit_effects = data.get("active_merit_effects", {})
        
        return dao_heart
    
    def __str__(self) -> str:
        """道心信息"""
        info = f"""
【道心系统】
━━━━━━━━━━━━━━━━━━━━━━
道心类型：{self.dao_heart_type.value}
功德值：{self.merit:,}
业力值：{self.sin:,}
平衡：{self.merit - self.sin:+,}

{self._get_dao_heart_description()}
"""
        
        # 显示惩罚
        penalties = self.get_active_penalties()
        if penalties:
            info += "\n【业力惩罚】\n"
            for p in penalties:
                info += f"  ⚠ {p['name']}：{p['description']}\n"
        
        # 显示增益
        bonuses = self.get_merit_bonuses()
        if bonuses:
            info += "\n【功德加成】\n"
            for name, value in bonuses.items():
                if value > 0:
                    info += f"  ✓ {name}：+{value:.0%}\n"
                else:
                    info += f"  ✗ {name}：{value:.0%}\n"
        
        return info
