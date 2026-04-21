#!/usr/bin/env python3
"""
蜀山剑侠传 - 灵兽系统
包含灵兽捕捉、培养、战斗系统
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SpiritBeastType(Enum):
    """灵兽类型"""
    DIVINE = "神兽"      # 神兽 - 最稀有
    SPIRIT = "灵兽"      # 灵兽 - 较稀有
    DEMON = "妖兽"       # 妖兽 - 普通


class SpiritBeastElement(Enum):
    """灵兽属性"""
    METAL = "金"
    WOOD = "木"
    WATER = "水"
    FIRE = "火"
    EARTH = "土"
    THUNDER = "雷"
    WIND = "风"
    ICE = "冰"
    LIGHT = "光"
    DARK = "暗"


@dataclass
class SpiritBeastSkill:
    """灵兽技能"""
    id: str
    name: str
    description: str
    damage_multiplier: float = 1.0  # 伤害倍率
    mp_cost: int = 10  # 消耗真元
    cooldown: int = 0  # 冷却回合
    element: Optional[str] = None  # 属性
    effect_type: Optional[str] = None  # 效果类型：dot, heal, buff, debuff
    effect_value: float = 0  # 效果值
    effect_duration: int = 0  # 效果持续回合


@dataclass
class SpiritBeast:
    """灵兽类"""
    # 基础信息
    id: str
    name: str
    beast_type: SpiritBeastType
    element: SpiritBeastElement
    
    # 基础属性
    base_hp: int
    base_attack: int
    base_defense: int
    base_speed: int
    
    # 成长属性
    bloodline: int = 50  # 血脉纯度 (1-100)
    aptitude: int = 50   # 资质 (1-100)
    
    # 状态
    level: int = 1
    exp: int = 0
    affection: int = 0  # 好感度 (0-100)
    
    # 当前状态
    current_hp: int = 0
    current_mp: int = 0
    max_mp: int = 50
    
    # 技能
    skills: List[SpiritBeastSkill] = field(default_factory=list)
    skill_cooldowns: Dict[str, int] = field(default_factory=dict)
    
    # 契约
    is_contracted: bool = False
    owner_name: str = ""
    
    # 进化
    evolution_stage: int = 1  # 进化阶段 1-3
    evolution_id: Optional[str] = None  # 进化后的灵兽ID
    
    # 复活
    revive_cost: int = 100  # 复活所需灵石
    
    # 描述
    description: str = ""
    habitat: str = ""  # 栖息地
    rarity: str = "普通"  # 稀有度
    
    def __post_init__(self):
        """初始化后计算属性"""
        if self.current_hp == 0:
            self.current_hp = self.max_hp
        if self.current_mp == 0:
            self.current_mp = self.max_mp
    
    @property
    def max_hp(self) -> int:
        """计算最大生命值"""
        base = self.base_hp + self.level * 10
        aptitude_bonus = 1 + (self.aptitude - 50) * 0.01
        bloodline_bonus = 1 + (self.bloodline - 50) * 0.005
        return int(base * aptitude_bonus * bloodline_bonus)
    
    @property
    def attack(self) -> int:
        """计算攻击力"""
        base = self.base_attack + self.level * 2
        aptitude_bonus = 1 + (self.aptitude - 50) * 0.015
        bloodline_bonus = 1 + (self.bloodline - 50) * 0.008
        return int(base * aptitude_bonus * bloodline_bonus)
    
    @property
    def defense(self) -> int:
        """计算防御力"""
        base = self.base_defense + self.level * 1
        aptitude_bonus = 1 + (self.aptitude - 50) * 0.01
        bloodline_bonus = 1 + (self.bloodline - 50) * 0.005
        return int(base * aptitude_bonus * bloodline_bonus)
    
    @property
    def speed(self) -> int:
        """计算速度"""
        base = self.base_speed + self.level * 0.5
        return int(base)
    
    @property
    def exp_to_next_level(self) -> int:
        """升到下一级所需经验"""
        return int(100 * (self.level ** 1.5))
    
    @property
    def capture_difficulty(self) -> int:
        """捕捉难度"""
        type_modifier = {
            SpiritBeastType.DIVINE: 3.0,
            SpiritBeastType.SPIRIT: 2.0,
            SpiritBeastType.DEMON: 1.0
        }
        return int(50 * type_modifier[self.beast_type] * (self.level / 10 + 1))
    
    @property
    def is_alive(self) -> bool:
        """是否存活"""
        return self.current_hp > 0
    
    def take_damage(self, damage: int) -> int:
        """受到伤害"""
        actual_damage = max(1, damage - self.defense)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """恢复生命"""
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp
    
    def use_mp(self, amount: int) -> bool:
        """使用真元"""
        if self.current_mp >= amount:
            self.current_mp -= amount
            return True
        return False
    
    def restore_mp(self, amount: int) -> int:
        """恢复真元"""
        old_mp = self.current_mp
        self.current_mp = min(self.max_mp, self.current_mp + amount)
        return self.current_mp - old_mp
    
    def add_exp(self, amount: int) -> Tuple[bool, int]:
        """增加经验，返回 (是否升级, 升级次数)"""
        self.exp += amount
        level_ups = 0
        
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1
            level_ups += 1
            # 升级恢复
            self.current_hp = self.max_hp
            self.current_mp = self.max_mp
        
        return level_ups > 0, level_ups
    
    def add_affection(self, amount: int) -> int:
        """增加好感度"""
        old_affection = self.affection
        self.affection = min(100, self.affection + amount)
        return self.affection - old_affection
    
    def learn_skill(self, skill: SpiritBeastSkill) -> bool:
        """学习技能"""
        if len(self.skills) >= 5:  # 最多5个技能
            return False
        if any(s.id == skill.id for s in self.skills):
            return False
        self.skills.append(skill)
        return True
    
    def can_evolve(self) -> bool:
        """是否可以进化"""
        if self.evolution_stage >= 3:
            return False
        if not self.evolution_id:
            return False
        return self.level >= self.evolution_stage * 20 and self.affection >= 50
    
    def evolve(self) -> Optional['SpiritBeast']:
        """进化，返回进化后的灵兽"""
        if not self.can_evolve():
            return None
        
        # 进化时保留部分属性
        evolved = SpiritBeast(
            id=self.evolution_id,
            name=self.name,
            beast_type=self.beast_type,
            element=self.element,
            base_hp=self.base_hp + 20,
            base_attack=self.base_attack + 10,
            base_defense=self.base_defense + 5,
            base_speed=self.base_speed + 5,
            bloodline=min(100, self.bloodline + 10),
            aptitude=self.aptitude,
            level=self.level,
            affection=self.affection,
            evolution_stage=self.evolution_stage + 1,
        )
        evolved.current_hp = evolved.max_hp
        evolved.current_mp = evolved.max_mp
        evolved.skills = self.skills.copy()
        evolved.owner_name = self.owner_name
        evolved.is_contracted = self.is_contracted
        
        return evolved
    
    def process_cooldowns(self):
        """处理技能冷却"""
        to_remove = []
        for skill_id, cooldown in self.skill_cooldowns.items():
            self.skill_cooldowns[skill_id] = cooldown - 1
            if self.skill_cooldowns[skill_id] <= 0:
                to_remove.append(skill_id)
        for skill_id in to_remove:
            del self.skill_cooldowns[skill_id]
    
    def get_available_skills(self) -> List[SpiritBeastSkill]:
        """获取可用技能"""
        return [s for s in self.skills if s.id not in self.skill_cooldowns]
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "beast_type": self.beast_type.value,
            "element": self.element.value,
            "base_hp": self.base_hp,
            "base_attack": self.base_attack,
            "base_defense": self.base_defense,
            "base_speed": self.base_speed,
            "bloodline": self.bloodline,
            "aptitude": self.aptitude,
            "level": self.level,
            "exp": self.exp,
            "affection": self.affection,
            "current_hp": self.current_hp,
            "current_mp": self.current_mp,
            "max_mp": self.max_mp,
            "skills": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "damage_multiplier": s.damage_multiplier,
                    "mp_cost": s.mp_cost,
                    "cooldown": s.cooldown,
                    "element": s.element,
                    "effect_type": s.effect_type,
                    "effect_value": s.effect_value,
                    "effect_duration": s.effect_duration
                }
                for s in self.skills
            ],
            "is_contracted": self.is_contracted,
            "owner_name": self.owner_name,
            "evolution_stage": self.evolution_stage,
            "evolution_id": self.evolution_id,
            "revive_cost": self.revive_cost,
            "description": self.description,
            "habitat": self.habitat,
            "rarity": self.rarity
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SpiritBeast':
        """从字典创建"""
        beast = cls(
            id=data["id"],
            name=data["name"],
            beast_type=SpiritBeastType(data["beast_type"]),
            element=SpiritBeastElement(data["element"]),
            base_hp=data["base_hp"],
            base_attack=data["base_attack"],
            base_defense=data["base_defense"],
            base_speed=data["base_speed"],
            bloodline=data.get("bloodline", 50),
            aptitude=data.get("aptitude", 50),
            level=data.get("level", 1),
            exp=data.get("exp", 0),
            affection=data.get("affection", 0),
            current_hp=data.get("current_hp", 0),
            current_mp=data.get("current_mp", 0),
            max_mp=data.get("max_mp", 50),
            is_contracted=data.get("is_contracted", False),
            owner_name=data.get("owner_name", ""),
            evolution_stage=data.get("evolution_stage", 1),
            evolution_id=data.get("evolution_id"),
            revive_cost=data.get("revive_cost", 100),
            description=data.get("description", ""),
            habitat=data.get("habitat", ""),
            rarity=data.get("rarity", "普通")
        )
        
        # 加载技能
        for skill_data in data.get("skills", []):
            skill = SpiritBeastSkill(
                id=skill_data["id"],
                name=skill_data["name"],
                description=skill_data.get("description", ""),
                damage_multiplier=skill_data.get("damage_multiplier", 1.0),
                mp_cost=skill_data.get("mp_cost", 10),
                cooldown=skill_data.get("cooldown", 0),
                element=skill_data.get("element"),
                effect_type=skill_data.get("effect_type"),
                effect_value=skill_data.get("effect_value", 0),
                effect_duration=skill_data.get("effect_duration", 0)
            )
            beast.skills.append(skill)
        
        return beast
    
    def __str__(self):
        status = "存活" if self.is_alive else "阵亡"
        return (f"【{self.beast_type.value}】{self.name} Lv.{self.level} "
                f"HP:{self.current_hp}/{self.max_hp} MP:{self.current_mp}/{self.max_mp} "
                f"血脉:{self.bloodline} 资质:{self.aptitude} 好感:{self.affection} [{status}]")


class SpiritBeastManager:
    """灵兽管理器"""
    
    def __init__(self, data_path: str = None):
        if data_path:
            self.data_path = Path(data_path)
        else:
            # 尝试多个可能的路径
            possible_paths = [
                Path("data/spirit_beasts.json"),
                Path(__file__).parent.parent / "data" / "spirit_beasts.json",
            ]
            self.data_path = None
            for path in possible_paths:
                if path.exists():
                    self.data_path = path
                    break
            if not self.data_path:
                self.data_path = possible_paths[0]  # 使用默认路径
        
        self.beast_templates: Dict[str, Dict] = {}
        self.load_templates()
    
    def load_templates(self):
        """加载灵兽模板"""
        if self.data_path.exists():
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.beast_templates = {b["id"]: b for b in data.get("spirit_beasts", [])}
    
    def get_template(self, beast_id: str) -> Optional[Dict]:
        """获取灵兽模板"""
        return self.beast_templates.get(beast_id)
    
    def create_beast(self, beast_id: str, level: int = 1) -> Optional[SpiritBeast]:
        """创建灵兽实例"""
        template = self.get_template(beast_id)
        if not template:
            return None
        
        beast = SpiritBeast(
            id=beast_id,
            name=template["name"],
            beast_type=SpiritBeastType(template["beast_type"]),
            element=SpiritBeastElement(template["element"]),
            base_hp=template["base_hp"],
            base_attack=template["base_attack"],
            base_defense=template["base_defense"],
            base_speed=template["base_speed"],
            bloodline=random.randint(
                template.get("bloodline_min", 40),
                template.get("bloodline_max", 80)
            ),
            aptitude=random.randint(
                template.get("aptitude_min", 40),
                template.get("aptitude_max", 80)
            ),
            level=level,
            description=template.get("description", ""),
            habitat=template.get("habitat", ""),
            rarity=template.get("rarity", "普通"),
            evolution_id=template.get("evolution_id"),
            max_mp=template.get("max_mp", 50),
            revive_cost=template.get("revive_cost", 100)
        )
        
        # 初始化HP和MP
        beast.current_hp = beast.max_hp
        beast.current_mp = beast.max_mp
        
        # 加载初始技能
        for skill_id in template.get("initial_skills", []):
            skill_template = self.get_skill_template(skill_id)
            if skill_template:
                skill = SpiritBeastSkill(
                    id=skill_id,
                    name=skill_template["name"],
                    description=skill_template.get("description", ""),
                    damage_multiplier=skill_template.get("damage_multiplier", 1.0),
                    mp_cost=skill_template.get("mp_cost", 10),
                    cooldown=skill_template.get("cooldown", 0),
                    element=skill_template.get("element"),
                    effect_type=skill_template.get("effect_type"),
                    effect_value=skill_template.get("effect_value", 0),
                    effect_duration=skill_template.get("effect_duration", 0)
                )
                beast.skills.append(skill)
        
        return beast
    
    def get_skill_template(self, skill_id: str) -> Optional[Dict]:
        """获取技能模板"""
        # 从配置文件或数据库获取
        # 这里简单返回一个默认模板
        skill_templates = {
            "fire_breath": {
                "id": "fire_breath",
                "name": "烈焰吐息",
                "description": "喷吐烈焰攻击敌人",
                "damage_multiplier": 1.5,
                "mp_cost": 15,
                "cooldown": 2,
                "element": "火"
            },
            "ice_claw": {
                "id": "ice_claw",
                "name": "寒冰利爪",
                "description": "带有寒冰之力的爪击",
                "damage_multiplier": 1.3,
                "mp_cost": 10,
                "cooldown": 1,
                "element": "冰",
                "effect_type": "slow",
                "effect_value": 0.3,
                "effect_duration": 2
            },
            "thunder_strike": {
                "id": "thunder_strike",
                "name": "雷霆一击",
                "description": "召唤雷电攻击",
                "damage_multiplier": 2.0,
                "mp_cost": 25,
                "cooldown": 3,
                "element": "雷"
            },
            "healing_light": {
                "id": "healing_light",
                "name": "治愈之光",
                "description": "恢复主人生命",
                "damage_multiplier": 0,
                "mp_cost": 20,
                "cooldown": 4,
                "element": "光",
                "effect_type": "heal",
                "effect_value": 0.3,
                "effect_duration": 0
            },
            "wind_slash": {
                "id": "wind_slash",
                "name": "风刃斩",
                "description": "斩出风刃攻击",
                "damage_multiplier": 1.2,
                "mp_cost": 8,
                "cooldown": 0,
                "element": "风"
            },
            "earth_shield": {
                "id": "earth_shield",
                "name": "大地护盾",
                "description": "召唤大地护盾保护主人",
                "damage_multiplier": 0,
                "mp_cost": 15,
                "cooldown": 3,
                "element": "土",
                "effect_type": "buff",
                "effect_value": 0.5,
                "effect_duration": 3
            }
        }
        return skill_templates.get(skill_id)
    
    def get_beasts_by_type(self, beast_type: SpiritBeastType) -> List[str]:
        """获取指定类型的灵兽ID列表"""
        return [
            beast_id for beast_id, template in self.beast_templates.items()
            if template["beast_type"] == beast_type.value
        ]
    
    def get_beasts_by_habitat(self, habitat: str) -> List[str]:
        """获取指定栖息地的灵兽ID列表"""
        return [
            beast_id for beast_id, template in self.beast_templates.items()
            if template.get("habitat") == habitat
        ]
    
    def get_random_beast(self, level_range: Tuple[int, int] = (1, 10), 
                         beast_type: Optional[SpiritBeastType] = None) -> Optional[SpiritBeast]:
        """获取随机灵兽"""
        candidates = []
        for beast_id, template in self.beast_templates.items():
            if beast_type and template["beast_type"] != beast_type.value:
                continue
            candidates.append(beast_id)
        
        if not candidates:
            return None
        
        beast_id = random.choice(candidates)
        level = random.randint(level_range[0], level_range[1])
        return self.create_beast(beast_id, level)


class CaptureSystem:
    """灵兽捕捉系统"""
    
    def __init__(self, manager: SpiritBeastManager):
        self.manager = manager
    
    def calculate_capture_rate(self, beast: SpiritBeast, 
                                player_cultivation: int = 0,
                                items_bonus: float = 0) -> float:
        """
        计算捕捉成功率
        
        基础公式：
        成功率 = (玩家修为 / 灵兽难度) × 资质修正 × 好感度修正 × 道具加成
        
        参数：
        - beast: 目标灵兽
        - player_cultivation: 玩家修为等级
        - items_bonus: 道具加成 (0-1)
        """
        # 基础成功率
        base_rate = min(0.9, player_cultivation / (beast.capture_difficulty + 1))
        
        # 灵兽类型修正
        type_modifier = {
            SpiritBeastType.DIVINE: 0.5,
            SpiritBeastType.SPIRIT: 0.7,
            SpiritBeastType.DEMON: 0.9
        }
        
        # 血脉修正（血脉越高越难捕捉）
        bloodline_modifier = 1 - (beast.bloodline - 50) * 0.005
        
        # 好感度修正
        affection_modifier = 1 + beast.affection * 0.005
        
        # 计算最终成功率
        final_rate = (base_rate * type_modifier[beast.beast_type] * 
                      bloodline_modifier * affection_modifier + items_bonus)
        
        return max(0.05, min(0.95, final_rate))
    
    def attempt_capture(self, beast: SpiritBeast, 
                        player_cultivation: int = 0,
                        items_bonus: float = 0) -> Tuple[bool, str]:
        """
        尝试捕捉灵兽
        
        返回：(是否成功, 结果描述)
        """
        rate = self.calculate_capture_rate(beast, player_cultivation, items_bonus)
        
        # 随机判定
        roll = random.random()
        
        if roll < rate:
            beast.is_contracted = True
            return True, f"成功驯服了 {beast.name}！好感度 +{random.randint(5, 15)}"
        else:
            # 失败时可能增加少量好感度
            affection_gain = random.randint(1, 3)
            beast.add_affection(affection_gain)
            return False, f"驯服失败...{beast.name}对你的好感度略微提升 (+{affection_gain})"
    
    def feed_beast(self, beast: SpiritBeast, food_type: str = "普通灵食") -> Tuple[int, str]:
        """
        喂养灵兽，提升好感度
        
        食物类型：
        - 普通灵食: +5 好感度
        - 高级灵食: +10 好感度
        - 灵丹: +20 好感度
        - 神品灵丹: +50 好感度
        """
        food_values = {
            "普通灵食": 5,
            "高级灵食": 10,
            "灵丹": 20,
            "神品灵丹": 50
        }
        
        gain = food_values.get(food_type, 5)
        actual_gain = beast.add_affection(gain)
        
        # 好感度等级描述
        if beast.affection >= 80:
            desc = f"{beast.name}非常喜欢你！"
        elif beast.affection >= 50:
            desc = f"{beast.name}对你产生了好感。"
        elif beast.affection >= 20:
            desc = f"{beast.name}开始亲近你了。"
        else:
            desc = f"{beast.name}吃了食物，似乎对你不那么警惕了。"
        
        return actual_gain, desc
    
    def sign_contract(self, beast: SpiritBeast, owner_name: str) -> Tuple[bool, str]:
        """
        签订契约
        
        条件：好感度 >= 30
        """
        if beast.is_contracted:
            return False, f"{beast.name}已经与你签订了契约。"
        
        if beast.affection < 30:
            return False, f"{beast.name}对你的好感度不足，还需要培养感情..."
        
        if beast.add_affection(10):
            beast.is_contracted = True
            beast.owner_name = owner_name
            return True, f"契约签订成功！{beast.name}正式成为你的契约灵兽！"
        
        return False, "契约签订失败..."
    
    def release_beast(self, beast: SpiritBeast) -> Tuple[bool, str]:
        """解除契约，放生灵兽"""
        if not beast.is_contracted:
            return False, f"{beast.name}并未与你签订契约。"
        
        beast.is_contracted = False
        beast.owner_name = ""
        beast.affection = max(0, beast.affection - 20)
        
        return True, f"解除了与{beast.name}的契约，它离开了..."


class TrainingSystem:
    """灵兽培养系统"""
    
    def __init__(self, manager: SpiritBeastManager):
        self.manager = manager
    
    def gain_exp(self, beast: SpiritBeast, amount: int) -> Dict:
        """
        灵兽获得经验
        
        返回：{
            "exp_gained": 获得的经验,
            "level_up": 是否升级,
            "new_level": 新等级,
            "level_ups": 升级次数
        }
        """
        old_level = beast.level
        leveled_up, level_ups = beast.add_exp(amount)
        
        return {
            "exp_gained": amount,
            "level_up": leveled_up,
            "new_level": beast.level,
            "level_ups": level_ups,
            "message": f"{beast.name}获得 {amount} 经验" + 
                       (f"，升到了 Lv.{beast.level}！" if leveled_up else "")
        }
    
    def train_stat(self, beast: SpiritBeast, stat: str, 
                   cost: int = 100) -> Tuple[bool, str]:
        """
        培养属性
        
        stat: "bloodline" 或 "aptitude"
        cost: 消耗灵石
        """
        if stat == "bloodline":
            if beast.bloodline >= 100:
                return False, f"{beast.name}的血脉已达完美境界！"
            increase = random.randint(1, 5)
            beast.bloodline = min(100, beast.bloodline + increase)
            return True, f"{beast.name}的血脉提升了 {increase} 点！(当前: {beast.bloodline})"
        
        elif stat == "aptitude":
            if beast.aptitude >= 100:
                return False, f"{beast.name}的资质已达巅峰！"
            increase = random.randint(1, 3)
            beast.aptitude = min(100, beast.aptitude + increase)
            return True, f"{beast.name}的资质提升了 {increase} 点！(当前: {beast.aptitude})"
        
        return False, "无效的培养项目"
    
    def learn_skill_from_scroll(self, beast: SpiritBeast, 
                                 skill_id: str) -> Tuple[bool, str]:
        """
        通过技能书学习技能
        
        返回：(是否成功, 结果描述)
        """
        if len(beast.skills) >= 5:
            return False, f"{beast.name}已学会了5个技能，无法再学习更多。"
        
        skill_template = self.manager.get_skill_template(skill_id)
        if not skill_template:
            return False, "技能书无效。"
        
        if any(s.id == skill_id for s in beast.skills):
            return False, f"{beast.name}已经学会了这个技能。"
        
        # 学习成功率基于好感度和资质
        success_rate = 0.5 + beast.affection * 0.003 + beast.aptitude * 0.002
        
        if random.random() < success_rate:
            skill = SpiritBeastSkill(
                id=skill_id,
                name=skill_template["name"],
                description=skill_template.get("description", ""),
                damage_multiplier=skill_template.get("damage_multiplier", 1.0),
                mp_cost=skill_template.get("mp_cost", 10),
                cooldown=skill_template.get("cooldown", 0),
                element=skill_template.get("element"),
                effect_type=skill_template.get("effect_type"),
                effect_value=skill_template.get("effect_value", 0),
                effect_duration=skill_template.get("effect_duration", 0)
            )
            beast.skills.append(skill)
            return True, f"{beast.name}学会了【{skill.name}】！"
        else:
            return False, f"学习失败，{beast.name}似乎无法领悟这个技能..."
    
    def evolve_beast(self, beast: SpiritBeast) -> Tuple[bool, str, Optional[SpiritBeast]]:
        """
        进化灵兽
        
        返回：(是否成功, 结果描述, 进化后的灵兽)
        """
        if not beast.can_evolve():
            if beast.evolution_stage >= 3:
                return False, f"{beast.name}已达最终形态！", None
            if beast.level < beast.evolution_stage * 20:
                return False, f"{beast.name}等级不足，需要 Lv.{beast.evolution_stage * 20} 才能进化。", None
            if beast.affection < 50:
                return False, f"{beast.name}好感度不足，需要达到 50 才能进化。", None
            return False, f"{beast.name}无法进化。", None
        
        evolved = beast.evolve()
        if evolved:
            return True, f"{beast.name}成功进化！力量大增！", evolved
        
        return False, "进化失败...", None


class SpiritBeastCombatSystem:
    """灵兽战斗系统"""
    
    def __init__(self, manager: SpiritBeastManager):
        self.manager = manager
    
    def calculate_damage(self, attacker: SpiritBeast, 
                         target, skill: Optional[SpiritBeastSkill] = None) -> int:
        """
        计算伤害
        
        基础伤害 = 攻击力 × 技能倍率 - 目标防御
        属性克制加成
        """
        base_damage = attacker.attack
        
        if skill:
            base_damage = int(base_damage * skill.damage_multiplier)
            # MP消耗
            if not attacker.use_mp(skill.mp_cost):
                # MP不足，使用普通攻击
                base_damage = attacker.attack
        
        # 属性克制
        if skill and skill.element:
            element_advantage = self.get_element_advantage(skill.element, getattr(target, 'element', None))
            base_damage = int(base_damage * element_advantage)
        
        # 防御减免
        target_defense = getattr(target, 'defense', 0)
        final_damage = max(1, base_damage - target_defense)
        
        # 冷却处理
        if skill and skill.cooldown > 0:
            attacker.skill_cooldowns[skill.id] = skill.cooldown
        
        return final_damage
    
    def get_element_advantage(self, attack_element: str, 
                               defense_element: Optional[str]) -> float:
        """
        获取属性克制倍率
        
        金克木、木克土、土克水、水克火、火克金
        雷克水、风克土
        光暗互克
        """
        if not defense_element:
            return 1.0
        
        advantages = {
            "金": {"木": 1.3},
            "木": {"土": 1.3},
            "土": {"水": 1.3},
            "水": {"火": 1.3},
            "火": {"金": 1.3},
            "雷": {"水": 1.2},
            "风": {"土": 1.2},
            "光": {"暗": 1.5},
            "暗": {"光": 1.5}
        }
        
        return advantages.get(attack_element, {}).get(defense_element, 1.0)
    
    def beast_attack(self, beast: SpiritBeast, target, 
                     skill_id: Optional[str] = None) -> Dict:
        """
        灵兽攻击
        
        返回：{
            "success": 是否成功,
            "damage": 伤害值,
            "skill_used": 使用的技能,
            "effect_applied": 应用的效果,
            "message": 战斗描述
        }
        """
        result = {
            "success": True,
            "damage": 0,
            "skill_used": None,
            "effect_applied": None,
            "message": ""
        }
        
        skill = None
        if skill_id:
            # 查找技能
            for s in beast.skills:
                if s.id == skill_id and skill_id not in beast.skill_cooldowns:
                    skill = s
                    break
        
        if skill:
            result["damage"] = self.calculate_damage(beast, target, skill)
            result["skill_used"] = skill.name
            
            # 应用技能效果
            if skill.effect_type:
                result["effect_applied"] = {
                    "type": skill.effect_type,
                    "value": skill.effect_value,
                    "duration": skill.effect_duration
                }
                
                # 对于治疗技能
                if skill.effect_type == "heal":
                    heal_amount = int(beast.max_hp * skill.effect_value)
                    beast.heal(heal_amount)
                    result["message"] = f"{beast.name}使用【{skill.name}】，恢复了 {heal_amount} 生命！"
                else:
                    result["message"] = f"{beast.name}使用【{skill.name}】，造成 {result['damage']} 伤害！"
            else:
                result["message"] = f"{beast.name}使用【{skill.name}】，造成 {result['damage']} 伤害！"
        else:
            # 普通攻击
            result["damage"] = self.calculate_damage(beast, target)
            result["message"] = f"{beast.name}发起攻击，造成 {result['damage']} 伤害！"
        
        # 对目标造成伤害
        if hasattr(target, 'take_damage'):
            target.take_damage(result["damage"])
        
        # 处理冷却
        beast.process_cooldowns()
        
        return result
    
    def revive_beast(self, beast: SpiritBeast, cost: int = None) -> Tuple[bool, str]:
        """
        复活灵兽
        
        返回：(是否成功, 结果描述)
        """
        if beast.is_alive:
            return False, f"{beast.name}尚在战斗，无需复活。"
        
        revive_cost = cost if cost else beast.revive_cost
        
        # 假设调用者会扣除灵石
        beast.current_hp = int(beast.max_hp * 0.5)  # 复活后恢复50%生命
        beast.current_mp = int(beast.max_mp * 0.5)
        
        return True, f"{beast.name}成功复活！消耗 {revive_cost} 灵石。"
    
    def get_combat_stats(self, beast: SpiritBeast) -> Dict:
        """
        获取灵兽战斗属性
        
        返回：属性字典
        """
        return {
            "name": beast.name,
            "level": beast.level,
            "hp": f"{beast.current_hp}/{beast.max_hp}",
            "mp": f"{beast.current_mp}/{beast.max_mp}",
            "attack": beast.attack,
            "defense": beast.defense,
            "speed": beast.speed,
            "element": beast.element.value,
            "available_skills": [s.name for s in beast.get_available_skills()],
            "is_alive": beast.is_alive
        }


# 便捷函数
def create_random_beast(level_range: Tuple[int, int] = (1, 10)) -> Optional[SpiritBeast]:
    """创建随机灵兽"""
    manager = SpiritBeastManager()
    return manager.get_random_beast(level_range)


if __name__ == "__main__":
    # 测试代码
    print("=== 灵兽系统测试 ===\n")
    
    # 初始化管理器
    manager = SpiritBeastManager()
    
    # 创建一只灵兽
    beast = manager.create_beast("qinglong", level=10)
    if beast:
        print(f"创建灵兽: {beast}")
        print(f"攻击力: {beast.attack}")
        print(f"防御力: {beast.defense}")
        print(f"生命值: {beast.max_hp}")
        print(f"捕捉难度: {beast.capture_difficulty}")
        
        # 测试捕捉系统
        print("\n--- 捕捉测试 ---")
        capture_sys = CaptureSystem(manager)
        success, msg = capture_sys.attempt_capture(beast, player_cultivation=50)
        print(msg)
        
        # 测试培养系统
        print("\n--- 培养测试 ---")
        training_sys = TrainingSystem(manager)
        result = training_sys.gain_exp(beast, 500)
        print(result["message"])
        
        # 测试战斗系统
        print("\n--- 战斗测试 ---")
        combat_sys = SpiritBeastCombatSystem(manager)
        stats = combat_sys.get_combat_stats(beast)
        print(f"战斗属性: {stats}")
