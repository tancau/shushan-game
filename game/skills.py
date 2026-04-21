#!/usr/bin/env python3
"""
蜀山剑侠传 - 功法系统

功法类型：
- 主修：影响修炼速度，只能有一个
- 辅修：提供辅助能力，可学习多个
- 秘术：特殊技能，有使用限制

功法品质：
- 凡：普通功法
- 灵：灵级功法
- 仙：仙级功法
- 神：神级功法
- 圣：圣级功法（传说级）
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, field


class SkillType(Enum):
    """功法类型"""
    MAIN = "主修"      # 主修功法
    AUXILIARY = "辅修" # 辅修功法
    SECRET = "秘术"    # 秘术


class SkillQuality(Enum):
    """功法品质"""
    MORTAL = "凡"      # 凡品
    SPIRIT = "灵"      # 灵品
    IMMORTAL = "仙"    # 仙品
    DIVINE = "神"      # 神品
    HOLY = "圣"        # 圣品


@dataclass
class SkillEffect:
    """功法效果"""
    name: str
    description: str
    effect_type: str  # passive, active, special
    value: float = 0.0
    duration: int = 0  # 持续回合（战斗技能）
    cooldown: int = 0  # 冷却回合
    mp_cost: int = 0   # 真元消耗
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "effect_type": self.effect_type,
            "value": self.value,
            "duration": self.duration,
            "cooldown": self.cooldown,
            "mp_cost": self.mp_cost
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SkillEffect":
        return cls(
            name=data["name"],
            description=data["description"],
            effect_type=data.get("effect_type", "passive"),
            value=data.get("value", 0.0),
            duration=data.get("duration", 0),
            cooldown=data.get("cooldown", 0),
            mp_cost=data.get("mp_cost", 0)
        )


@dataclass
class Skill:
    """功法类"""
    id: str
    name: str
    skill_type: SkillType
    quality: SkillQuality
    description: str
    sect: Optional[str] = None  # 所属门派
    
    # 学习要求
    realm_required: str = "练气期"
    prerequisites: List[str] = field(default_factory=list)
    
    # 效果
    effects: List[SkillEffect] = field(default_factory=list)
    
    # 升级系统
    max_level: int = 10
    current_level: int = 1
    level_up_cost: int = 100  # 灵石
    level_up_cultivation: int = 100  # 修为
    
    # 特殊属性
    element: Optional[str] = None  # 五行属性
    is_secret: bool = False  # 是否为秘传功法
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "skill_type": self.skill_type.value,
            "quality": self.quality.value,
            "description": self.description,
            "sect": self.sect,
            "realm_required": self.realm_required,
            "prerequisites": self.prerequisites,
            "effects": [e.to_dict() for e in self.effects],
            "max_level": self.max_level,
            "current_level": self.current_level,
            "level_up_cost": self.level_up_cost,
            "level_up_cultivation": self.level_up_cultivation,
            "element": self.element,
            "is_secret": self.is_secret
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Skill":
        """从字典创建"""
        skill_type = SkillType(data["skill_type"])
        quality = SkillQuality(data["quality"])
        
        effects = [SkillEffect.from_dict(e) for e in data.get("effects", [])]
        
        return cls(
            id=data["id"],
            name=data["name"],
            skill_type=skill_type,
            quality=quality,
            description=data["description"],
            sect=data.get("sect"),
            realm_required=data.get("realm_required", "练气期"),
            prerequisites=data.get("prerequisites", []),
            effects=effects,
            max_level=data.get("max_level", 10),
            current_level=data.get("current_level", 1),
            level_up_cost=data.get("level_up_cost", 100),
            level_up_cultivation=data.get("level_up_cultivation", 100),
            element=data.get("element"),
            is_secret=data.get("is_secret", False)
        )
    
    def get_cultivation_bonus(self) -> float:
        """获取修炼加成（主修功法）"""
        bonus = 1.0
        for effect in self.effects:
            if effect.effect_type == "passive" and "修炼" in effect.name:
                # 等级加成：每级增加 10% 效果
                bonus += effect.value * (1 + (self.current_level - 1) * 0.1)
        return bonus
    
    def get_passive_bonuses(self) -> Dict[str, float]:
        """获取所有被动加成"""
        bonuses = {}
        for effect in self.effects:
            if effect.effect_type == "passive":
                # 等级加成
                value = effect.value * (1 + (self.current_level - 1) * 0.1)
                bonuses[effect.name] = value
        return bonuses
    
    def get_active_skills(self) -> List[SkillEffect]:
        """获取主动技能列表"""
        return [e for e in self.effects if e.effect_type == "active"]
    
    def get_special_skills(self) -> List[SkillEffect]:
        """获取特殊技能列表"""
        return [e for e in self.effects if e.effect_type == "special"]
    
    def can_level_up(self, spirit_stones: int, cultivation: int) -> bool:
        """检查是否可以升级"""
        if self.current_level >= self.max_level:
            return False
        
        cost = int(self.level_up_cost * (1 + (self.current_level - 1) * 0.5))
        cult = int(self.level_up_cultivation * (1 + (self.current_level - 1) * 0.5))
        
        return spirit_stones >= cost and cultivation >= cult
    
    def get_level_up_cost(self) -> dict:
        """获取升级所需资源"""
        return {
            "spirit_stones": int(self.level_up_cost * (1 + (self.current_level - 1) * 0.5)),
            "cultivation": int(self.level_up_cultivation * (1 + (self.current_level - 1) * 0.5))
        }
    
    def level_up(self):
        """升级功法"""
        if self.current_level < self.max_level:
            self.current_level += 1
            return True
        return False
    
    def __str__(self) -> str:
        """功法信息字符串"""
        quality_colors = {
            "凡": "⚪",
            "灵": "🔵",
            "仙": "🟣",
            "神": "🟡",
            "圣": "🔴"
        }
        
        emoji = quality_colors.get(self.quality.value, "⚪")
        type_str = f"[{self.skill_type.value}]"
        level_str = f"Lv.{self.current_level}/{self.max_level}"
        
        info = f"{emoji} {self.name} {type_str} {level_str}\n"
        info += f"   品质：{self.quality.value}品\n"
        info += f"   描述：{self.description}\n"
        
        if self.sect:
            info += f"   门派：{self.sect}\n"
        
        if self.effects:
            info += "   效果：\n"
            for effect in self.effects:
                effect_str = f"     • {effect.name}: {effect.description}"
                if effect.value > 0:
                    effect_str += f" (+{effect.value * (1 + (self.current_level - 1) * 0.1):.0%})"
                info += effect_str + "\n"
        
        return info.strip()


class SkillManager:
    """功法管理器"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.skills: Dict[str, Skill] = {}
        self.load_skills()
    
    def load_skills(self):
        """加载功法数据"""
        skill_file = self.data_dir / "skills.json"
        
        if not skill_file.exists():
            # 创建默认功法数据
            self._create_default_skills()
            return
        
        with open(skill_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for skill_data in data.get("skills", []):
            skill = Skill.from_dict(skill_data)
            self.skills[skill.id] = skill
    
    def _create_default_skills(self):
        """创建默认功法数据"""
        # 这里只创建基础功法，详细功法在 skills.json 中定义
        default_skills = {
            "skills": [
                {
                    "id": "basic_qigong",
                    "name": "基础吐纳法",
                    "skill_type": "主修",
                    "quality": "凡",
                    "description": "修真入门功法，吐纳天地灵气",
                    "effects": [
                        {
                            "name": "修炼加成",
                            "description": "提升修炼速度",
                            "effect_type": "passive",
                            "value": 0.1
                        }
                    ]
                }
            ]
        }
        
        self.data_dir.mkdir(exist_ok=True)
        skill_file = self.data_dir / "skills.json"
        with open(skill_file, "w", encoding="utf-8") as f:
            json.dump(default_skills, f, ensure_ascii=False, indent=2)
        
        # 重新加载
        self.load_skills()
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """获取功法"""
        return self.skills.get(skill_id)
    
    def get_skill_by_name(self, name: str) -> Optional[Skill]:
        """通过名称获取功法"""
        for skill in self.skills.values():
            if skill.name == name:
                return skill
        return None
    
    def get_skills_by_sect(self, sect: str) -> List[Skill]:
        """获取门派功法"""
        return [s for s in self.skills.values() if s.sect == sect]
    
    def get_skills_by_type(self, skill_type: SkillType) -> List[Skill]:
        """获取指定类型的功法"""
        return [s for s in self.skills.values() if s.skill_type == skill_type]
    
    def get_skills_by_quality(self, quality: SkillQuality) -> List[Skill]:
        """获取指定品质的功法"""
        return [s for s in self.skills.values() if s.quality == quality]
    
    def get_available_skills(self, 
                            realm: str, 
                            learned_skills: List[str],
                            sect: Optional[str] = None) -> List[Skill]:
        """
        获取可学习的功法
        
        Args:
            realm: 当前境界
            learned_skills: 已学功法ID列表
            sect: 所属门派
        
        Returns:
            可学习的功法列表
        """
        from config import REALMS
        
        current_level = REALMS.get(realm, {}).get("level", 1)
        available = []
        
        for skill in self.skills.values():
            # 已学过
            if skill.id in learned_skills:
                continue
            
            # 境界要求
            required_level = REALMS.get(skill.realm_required, {}).get("level", 1)
            if current_level < required_level:
                continue
            
            # 前置功法
            if skill.prerequisites:
                if not all(p in learned_skills for p in skill.prerequisites):
                    continue
            
            # 门派秘传
            if skill.is_secret and skill.sect != sect:
                continue
            
            available.append(skill)
        
        return available
    
    def search_skills(self, keyword: str) -> List[Skill]:
        """搜索功法"""
        keyword = keyword.lower()
        results = []
        
        for skill in self.skills.values():
            if (keyword in skill.name.lower() or 
                keyword in skill.description.lower() or
                (skill.sect and keyword in skill.sect.lower())):
                results.append(skill)
        
        return results
    
    def get_all_skills(self) -> List[Skill]:
        """获取所有功法"""
        return list(self.skills.values())
    
    def __len__(self) -> int:
        """功法总数"""
        return len(self.skills)
    
    def __contains__(self, skill_id: str) -> bool:
        """检查功法是否存在"""
        return skill_id in self.skills
