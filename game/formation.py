#!/usr/bin/env python3
"""
蜀山剑侠传 - 阵法系统
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field


class FormationType(Enum):
    """阵法类型"""
    ATTACK = "攻击阵"
    DEFENSE = "防御阵"
    TRAP = "困敌阵"
    SUPPORT = "辅助阵"


class FormationQuality(Enum):
    """阵法品质"""
    MORTAL = ("凡", 1)
    SPIRIT = ("灵", 2)
    IMMORTAL = ("仙", 3)
    DIVINE = ("神", 4)
    SAINT = ("圣", 5)
    
    def __init__(self, chinese: str, level: int):
        self.chinese = chinese
        self.level = level


class FormationPosition(Enum):
    """阵位类型"""
    CORE = "阵眼"      # 核心
    CORNER = "阵角"    # 支撑
    GATE = "阵门"      # 出入口


# 五行相克关系
ELEMENT_COUNTER = {
    "金": {"克": "木", "被克": "火"},
    "木": {"克": "土", "被克": "金"},
    "水": {"克": "火", "被克": "土"},
    "火": {"克": "金", "被克": "水"},
    "土": {"克": "水", "被克": "木"},
}


@dataclass
class FormationEffect:
    """阵法效果"""
    name: str
    effect_type: str
    value: float = 0
    duration: int = 1
    element: str = None
    chance: float = 1.0
    targets: int = 1
    stat: str = None


@dataclass
class FormationMaterial:
    """阵法材料需求"""
    materials: Dict[str, int]
    upgrade_materials: Dict[str, int]


@dataclass
class Formation:
    """阵法类"""
    id: str
    name: str
    type: FormationType
    quality: FormationQuality
    element: str
    description: str
    realm_required: str
    
    # 阵法结构
    formation_size: int
    positions: Dict[str, Dict]
    
    # 效果
    effects: List[FormationEffect]
    
    # 基础属性
    base_damage: int
    base_defense: int
    
    # 消耗
    mp_cost_per_turn: int
    setup_mp_cost: int
    
    # 材料
    materials: Dict[str, int]
    upgrade_materials: Dict[str, int]
    
    # 等级
    max_level: int
    prerequisites: List[str] = field(default_factory=list)
    
    def get_damage(self, level: int = 1, realm_level: int = 1) -> int:
        """计算阵法伤害"""
        base = self.base_damage
        level_bonus = base * 0.1 * (level - 1)
        realm_bonus = base * 0.15 * (realm_level - 1)
        return int(base + level_bonus + realm_bonus)
    
    def get_defense(self, level: int = 1, realm_level: int = 1) -> int:
        """计算阵法防御"""
        base = self.base_defense
        level_bonus = base * 0.1 * (level - 1)
        realm_bonus = base * 0.15 * (realm_level - 1)
        return int(base + level_bonus + realm_bonus)
    
    def get_mp_cost(self, level: int = 1) -> Tuple[int, int]:
        """获取真元消耗（布置消耗，每回合消耗）"""
        # 等级越高，效率越高
        reduction = 1 - (level - 1) * 0.03
        setup_cost = int(self.setup_mp_cost * max(0.7, reduction))
        turn_cost = int(self.mp_cost_per_turn * max(0.7, reduction))
        return setup_cost, turn_cost
    
    def get_element_damage_multiplier(self, target_element: str) -> float:
        """计算五行相克伤害倍率"""
        if not self.element or not target_element:
            return 1.0
        
        if self.element in ELEMENT_COUNTER:
            if ELEMENT_COUNTER[self.element]["克"] == target_element:
                return 1.5  # 克制敌人，伤害+50%
            elif ELEMENT_COUNTER[self.element]["被克"] == target_element:
                return 0.7  # 被克制，伤害-30%
        
        return 1.0
    
    def can_learn(self, learned_formations: Dict[str, int]) -> bool:
        """检查是否可以学习"""
        if not self.prerequisites:
            return True
        return all(pre in learned_formations for pre in self.prerequisites)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "quality": self.quality.chinese,
            "element": self.element,
            "description": self.description,
            "realm_required": self.realm_required,
            "formation_size": self.formation_size,
            "positions": self.positions,
            "effects": [
                {
                    "name": e.name,
                    "type": e.effect_type,
                    "value": e.value,
                    "duration": e.duration,
                    "element": e.element,
                    "chance": e.chance,
                    "targets": e.targets,
                    "stat": e.stat
                }
                for e in self.effects
            ],
            "base_damage": self.base_damage,
            "base_defense": self.base_defense,
            "mp_cost_per_turn": self.mp_cost_per_turn,
            "setup_mp_cost": self.setup_mp_cost,
            "materials": self.materials,
            "upgrade_materials": self.upgrade_materials,
            "max_level": self.max_level,
            "prerequisites": self.prerequisites
        }


@dataclass
class ActiveFormation:
    """激活的阵法（战斗中使用）"""
    formation: Formation
    level: int
    owner_realm_level: int
    turns_remaining: int
    current_hp: int = 0
    shield_hp: int = 0
    
    def __post_init__(self):
        """初始化阵法护盾"""
        if self.formation.type == FormationType.DEFENSE:
            self.shield_hp = self.formation.get_defense(
                self.level, self.owner_realm_level
            )
    
    def get_damage(self) -> int:
        """获取当前伤害"""
        return self.formation.get_damage(self.level, self.owner_realm_level)
    
    def get_defense(self) -> int:
        """获取当前防御"""
        return self.formation.get_defense(self.level, self.owner_realm_level)
    
    def take_damage(self, damage: int) -> int:
        """阵法承受伤害"""
        if self.shield_hp > 0:
            absorbed = min(self.shield_hp, damage)
            self.shield_hp -= absorbed
            return absorbed
        return 0
    
    def is_destroyed(self) -> bool:
        """检查阵法是否被破坏"""
        return self.shield_hp <= 0 and self.formation.type == FormationType.DEFENSE
    
    def process_turn(self) -> Dict:
        """处理回合结束效果"""
        self.turns_remaining -= 1
        
        result = {
            "still_active": self.turns_remaining > 0,
            "effects": []
        }
        
        # 处理持续效果
        for effect in self.formation.effects:
            if effect.effect_type in ["dot", "mp_regen", "mp_drain"]:
                result["effects"].append({
                    "name": effect.name,
                    "type": effect.effect_type,
                    "value": int(effect.value * (1 + (self.level - 1) * 0.1))
                })
        
        return result
    
    def get_mp_cost_per_turn(self) -> int:
        """获取每回合真元消耗"""
        _, turn_cost = self.formation.get_mp_cost(self.level)
        return turn_cost


class FormationManager:
    """阵法管理器"""
    
    _instance = None
    _formations: Dict[str, Formation] = {}
    _loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def load_formations(cls):
        """加载阵法数据"""
        if cls._loaded:
            return
        
        data_path = Path(__file__).parent.parent / "data" / "formations.json"
        
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"阵法数据文件不存在: {data_path}")
            return
        except json.JSONDecodeError as e:
            print(f"阵法数据解析错误: {e}")
            return
        
        cls._formations = {}
        
        for formation_id, formation_data in data.get("formations", {}).items():
            formation = cls._parse_formation(formation_data)
            if formation:
                cls._formations[formation_id] = formation
        
        cls._loaded = True
        print(f"加载了 {len(cls._formations)} 个阵法")
    
    @classmethod
    def _parse_formation(cls, data: Dict) -> Optional[Formation]:
        """解析阵法数据"""
        try:
            # 解析类型
            type_map = {
                "攻击阵": FormationType.ATTACK,
                "防御阵": FormationType.DEFENSE,
                "困敌阵": FormationType.TRAP,
                "辅助阵": FormationType.SUPPORT
            }
            formation_type = type_map.get(data["type"], FormationType.ATTACK)
            
            # 解析品质
            quality_map = {
                "凡": FormationQuality.MORTAL,
                "灵": FormationQuality.SPIRIT,
                "仙": FormationQuality.IMMORTAL,
                "神": FormationQuality.DIVINE,
                "圣": FormationQuality.SAINT
            }
            quality = quality_map.get(data["quality"], FormationQuality.MORTAL)
            
            # 解析效果
            effects = []
            for effect_data in data.get("effects", []):
                effect = FormationEffect(
                    name=effect_data.get("name", ""),
                    effect_type=effect_data.get("type", ""),
                    value=effect_data.get("value", 0),
                    duration=effect_data.get("duration", 1),
                    element=effect_data.get("element"),
                    chance=effect_data.get("chance", 1.0),
                    targets=effect_data.get("targets", 1),
                    stat=effect_data.get("stat")
                )
                effects.append(effect)
            
            # 创建阵法
            return Formation(
                id=data["id"],
                name=data["name"],
                type=formation_type,
                quality=quality,
                element=data.get("element", "无"),
                description=data["description"],
                realm_required=data["realm_required"],
                formation_size=data["formation_size"],
                positions=data["positions"],
                effects=effects,
                base_damage=data["base_damage"],
                base_defense=data["base_defense"],
                mp_cost_per_turn=data["mp_cost_per_turn"],
                setup_mp_cost=data["setup_mp_cost"],
                materials=data["materials"],
                upgrade_materials=data["upgrade_materials"],
                max_level=data["max_level"],
                prerequisites=data.get("prerequisites", [])
            )
        except Exception as e:
            print(f"解析阵法 {data.get('id', 'unknown')} 失败: {e}")
            return None
    
    @classmethod
    def get_formation(cls, formation_id: str) -> Optional[Formation]:
        """获取阵法"""
        if not cls._loaded:
            cls.load_formations()
        return cls._formations.get(formation_id)
    
    @classmethod
    def get_all_formations(cls) -> Dict[str, Formation]:
        """获取所有阵法"""
        if not cls._loaded:
            cls.load_formations()
        return cls._formations
    
    @classmethod
    def get_formations_by_type(cls, formation_type: FormationType) -> List[Formation]:
        """按类型获取阵法"""
        if not cls._loaded:
            cls.load_formations()
        return [f for f in cls._formations.values() if f.type == formation_type]
    
    @classmethod
    def get_formations_by_quality(cls, quality: FormationQuality) -> List[Formation]:
        """按品质获取阵法"""
        if not cls._loaded:
            cls.load_formations()
        return [f for f in cls._formations.values() if f.quality == quality]
    
    @classmethod
    def get_formations_by_element(cls, element: str) -> List[Formation]:
        """按五行属性获取阵法"""
        if not cls._loaded:
            cls.load_formations()
        return [f for f in cls._formations.values() if f.element == element]
    
    @classmethod
    def can_setup_formation(
        cls,
        formation_id: str,
        player_mp: int,
        player_realm: str,
        player_materials: Dict[str, int],
        learned_formations: Dict[str, int]
    ) -> Tuple[bool, str]:
        """
        检查是否可以布设阵法
        
        Returns:
            (是否可以, 原因说明)
        """
        formation = cls.get_formation(formation_id)
        if not formation:
            return False, "阵法不存在"
        
        # 检查境界
        from config import REALMS
        player_level = REALMS.get(player_realm, {}).get("level", 0)
        required_level = REALMS.get(formation.realm_required, {}).get("level", 0)
        
        if player_level < required_level:
            return False, f"境界不足，需要 {formation.realm_required}"
        
        # 检查是否已学习
        if formation_id not in learned_formations:
            return False, "尚未学习此阵法"
        
        # 检查前置阵法
        if not formation.can_learn(learned_formations):
            return False, f"需要先学习: {', '.join(formation.prerequisites)}"
        
        # 检查真元
        setup_cost, _ = formation.get_mp_cost(learned_formations[formation_id])
        if player_mp < setup_cost:
            return False, f"真元不足，需要 {setup_cost} 点真元"
        
        # 检查材料
        for material, count in formation.materials.items():
            if player_materials.get(material, 0) < count:
                return False, f"材料不足，需要 {material} x{count}"
        
        return True, "可以布设"
    
    @classmethod
    def calculate_formation_damage(
        cls,
        formation: Formation,
        formation_level: int,
        attacker_realm_level: int,
        defender_element: str = None,
        defender_defense: int = 0
    ) -> Dict:
        """
        计算阵法伤害
        
        Returns:
            伤害结果详情
        """
        result = {
            "base_damage": formation.get_damage(formation_level, attacker_realm_level),
            "element_multiplier": 1.0,
            "final_damage": 0,
            "effects": []
        }
        
        # 五行相克
        if defender_element:
            result["element_multiplier"] = formation.get_element_damage_multiplier(defender_element)
        
        # 计算最终伤害
        damage = result["base_damage"] * result["element_multiplier"]
        damage = max(1, damage - defender_defense * 0.5)
        result["final_damage"] = int(damage)
        
        # 处理效果
        for effect in formation.effects:
            if effect.effect_type in ["damage", "dot", "aoe_damage"]:
                effect_value = effect.value * (1 + (formation_level - 1) * 0.1)
                effect_value *= result["element_multiplier"]
                
                result["effects"].append({
                    "name": effect.name,
                    "type": effect.effect_type,
                    "value": int(effect_value),
                    "duration": effect.duration,
                    "chance": effect.chance
                })
        
        return result
    
    @classmethod
    def break_formation(
        cls,
        active_formation: ActiveFormation,
        attack_damage: int,
        attacker_element: str = None
    ) -> Dict:
        """
        破阵计算
        
        Returns:
            破阵结果
        """
        result = {
            "damage_absorbed": 0,
            "shield_remaining": active_formation.shield_hp,
            "formation_broken": False,
            "counter_damage": 0
        }
        
        # 五行克制对破阵的影响
        element_multiplier = 1.0
        if attacker_element and active_formation.formation.element:
            if active_formation.formation.element in ELEMENT_COUNTER:
                if ELEMENT_COUNTER[active_formation.formation.element]["被克"] == attacker_element:
                    element_multiplier = 1.5  # 克制阵法，破阵效率+50%
        
        # 计算伤害
        effective_damage = int(attack_damage * element_multiplier)
        result["damage_absorbed"] = active_formation.take_damage(effective_damage)
        result["shield_remaining"] = active_formation.shield_hp
        
        # 检查是否破阵
        if active_formation.is_destroyed():
            result["formation_broken"] = True
            # 破阵反噬
            result["counter_damage"] = int(active_formation.get_damage() * 0.3)
        
        return result


class FormationCombatSystem:
    """阵法战斗系统"""
    
    def __init__(self, combat_system):
        """
        初始化阵法战斗系统
        
        Args:
            combat_system: 战斗系统实例
        """
        self.combat = combat_system
        self.active_formations: List[ActiveFormation] = []
        self.formation_cooldowns: Dict[str, int] = {}
    
    def setup_formation(
        self,
        formation_id: str,
        formation_level: int,
        player_mp: int,
        player_realm_level: int
    ) -> Dict:
        """
        布设阵法
        
        Returns:
            布设结果
        """
        formation = FormationManager.get_formation(formation_id)
        if not formation:
            return {"success": False, "message": "阵法不存在"}
        
        # 检查冷却
        if formation_id in self.formation_cooldowns and self.formation_cooldowns[formation_id] > 0:
            return {"success": False, "message": f"阵法冷却中，还需 {self.formation_cooldowns[formation_id]} 回合"}
        
        # 检查真元
        setup_cost, turn_cost = formation.get_mp_cost(formation_level)
        if player_mp < setup_cost:
            return {"success": False, "message": f"真元不足，需要 {setup_cost} 点真元"}
        
        # 创建激活阵法
        active = ActiveFormation(
            formation=formation,
            level=formation_level,
            owner_realm_level=player_realm_level,
            turns_remaining=formation.effects[0].duration if formation.effects else 5
        )
        
        self.active_formations.append(active)
        
        # 设置冷却
        self.formation_cooldowns[formation_id] = formation.formation_size
        
        return {
            "success": True,
            "message": f"{formation.name} 已布设！",
            "mp_cost": setup_cost,
            "turn_cost": turn_cost,
            "formation": active
        }
    
    def process_formations_turn(self) -> List[Dict]:
        """
        处理所有阵法的回合效果
        
        Returns:
            效果列表
        """
        results = []
        to_remove = []
        
        for i, active in enumerate(self.active_formations):
            # 处理回合
            turn_result = active.process_turn()
            
            # 收集效果
            result = {
                "formation_name": active.formation.name,
                "turns_remaining": active.turns_remaining,
                "effects": turn_result["effects"],
                "mp_cost": active.get_mp_cost_per_turn(),
                "still_active": turn_result["still_active"]
            }
            
            results.append(result)
            
            if not turn_result["still_active"]:
                to_remove.append(i)
        
        # 移除结束的阵法
        for i in reversed(to_remove):
            self.active_formations.pop(i)
        
        # 减少冷却
        for formation_id in self.formation_cooldowns:
            if self.formation_cooldowns[formation_id] > 0:
                self.formation_cooldowns[formation_id] -= 1
        
        return results
    
    def get_formation_attack_damage(self, target_element: str = None) -> int:
        """获取阵法攻击伤害总和"""
        total_damage = 0
        
        for active in self.active_formations:
            if active.formation.type == FormationType.ATTACK:
                damage = active.get_damage()
                if target_element:
                    damage *= active.formation.get_element_damage_multiplier(target_element)
                total_damage += int(damage)
        
        return total_damage
    
    def get_formation_defense(self) -> int:
        """获取阵法防御总和"""
        total_defense = 0
        
        for active in self.active_formations:
            if active.formation.type == FormationType.DEFENSE:
                total_defense += active.shield_hp
        
        return total_defense
    
    def has_trap_formation(self) -> bool:
        """是否有困敌阵"""
        return any(a.formation.type == FormationType.TRAP for a in self.active_formations)
    
    def get_trap_effects(self) -> List[Dict]:
        """获取困敌阵效果"""
        effects = []
        
        for active in self.active_formations:
            if active.formation.type == FormationType.TRAP:
                for effect in active.formation.effects:
                    if effect.effect_type in ["freeze", "slow", "confuse", "paralyze"]:
                        effects.append({
                            "name": effect.name,
                            "type": effect.effect_type,
                            "chance": effect.chance * (1 + (active.level - 1) * 0.05),
                            "duration": effect.duration
                        })
        
        return effects
    
    def get_support_effects(self) -> List[Dict]:
        """获取辅助阵效果"""
        effects = []
        
        for active in self.active_formations:
            if active.formation.type == FormationType.SUPPORT:
                for effect in active.formation.effects:
                    if effect.effect_type in ["mp_regen", "cultivation_boost", "stealth"]:
                        effects.append({
                            "name": effect.name,
                            "type": effect.effect_type,
                            "value": int(effect.value * (1 + (active.level - 1) * 0.1)),
                            "duration": effect.duration
                        })
        
        return effects
    
    def attack_formation(self, damage: int, attacker_element: str = None) -> Dict:
        """
        攻击阵法（破阵）
        
        Returns:
            破阵结果
        """
        result = {
            "damage_absorbed": 0,
            "formations_broken": [],
            "counter_damage": 0
        }
        
        for active in self.active_formations[:]:  # 使用切片避免修改时出问题
            if active.formation.type == FormationType.DEFENSE and active.shield_hp > 0:
                break_result = FormationManager.break_formation(
                    active, damage, attacker_element
                )
                
                result["damage_absorbed"] += break_result["damage_absorbed"]
                result["counter_damage"] += break_result["counter_damage"]
                
                if break_result["formation_broken"]:
                    result["formations_broken"].append(active.formation.name)
                    self.active_formations.remove(active)
        
        return result
    
    def get_status_text(self) -> str:
        """获取阵法状态文本"""
        if not self.active_formations:
            return "无激活阵法"
        
        lines = ["【激活阵法】"]
        
        for active in self.active_formations:
            status = f"  • {active.formation.name} (Lv.{active.level})"
            if active.formation.type == FormationType.DEFENSE:
                status += f" 护盾: {active.shield_hp}"
            status += f" 剩余: {active.turns_remaining}回合"
            lines.append(status)
        
        return "\n".join(lines)


# 初始化加载
FormationManager.load_formations()
