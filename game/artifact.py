#!/usr/bin/env python3
"""
蜀山剑侠传 - 法宝系统
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Artifact:
    """法宝类"""
    name: str
    artifact_type: str  # 飞剑、防御、攻击、辅助、特殊
    element: str  # 金木水火土
    power: int  # 威力
    speed: int  # 速度
    tier: int  # 品阶 1-5
    description: str
    special_effect: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "artifact_type": self.artifact_type,
            "element": self.element,
            "power": self.power,
            "speed": self.speed,
            "tier": self.tier,
            "description": self.description,
            "special_effect": self.special_effect
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Artifact":
        return cls(
            name=data["name"],
            artifact_type=data["artifact_type"],
            element=data["element"],
            power=data["power"],
            speed=data["speed"],
            tier=data["tier"],
            description=data["description"],
            special_effect=data.get("special_effect")
        )


class ArtifactManager:
    """法宝管理器"""
    
    # 法宝数据库
    ARTIFACTS_DB = {
        # 一级法宝（练气期可用）
        "青竹剑": {
            "artifact_type": "飞剑",
            "element": "木",
            "power": 50,
            "speed": 60,
            "tier": 1,
            "description": "青竹炼制的基础飞剑",
            "special_effect": None
        },
        "铁精剑": {
            "artifact_type": "飞剑",
            "element": "金",
            "power": 60,
            "speed": 50,
            "tier": 1,
            "description": "精铁打造的入门飞剑",
            "special_effect": None
        },
        "护身玉佩": {
            "artifact_type": "防御",
            "element": "土",
            "power": 30,
            "speed": 0,
            "tier": 1,
            "description": "简单的护身法宝",
            "special_effect": "自动护主，抵挡一次致命攻击"
        },
        
        # 二级法宝（筑基期可用）
        "青索剑": {
            "artifact_type": "飞剑",
            "element": "木",
            "power": 200,
            "speed": 150,
            "tier": 2,
            "description": "峨眉镇山之宝之一，剑光如青索",
            "special_effect": "剑光坚韧，可缠绕敌人"
        },
        "紫郢剑": {
            "artifact_type": "飞剑",
            "element": "金",
            "power": 250,
            "speed": 180,
            "tier": 2,
            "description": "峨眉镇山至宝，剑光紫若云霞",
            "special_effect": "无视部分防御"
        },
        "五云锁仙屏": {
            "artifact_type": "防御",
            "element": "土",
            "power": 150,
            "speed": 0,
            "tier": 2,
            "description": "五色云光组成的护身屏风",
            "special_effect": "可抵挡多次攻击"
        },
        
        # 三级法宝（金丹期可用）
        "七修剑": {
            "artifact_type": "飞剑",
            "element": "金",
            "power": 500,
            "speed": 300,
            "tier": 3,
            "description": "七口飞剑合一，威力无穷",
            "special_effect": "可分化七道剑光"
        },
        "白眉针": {
            "artifact_type": "攻击",
            "element": "金",
            "power": 400,
            "speed": 500,
            "tier": 3,
            "description": "细如牛毛，专破护身法宝",
            "special_effect": "高穿透，难以防御"
        },
        "天蝉灵叶": {
            "artifact_type": "辅助",
            "element": "木",
            "power": 0,
            "speed": 0,
            "tier": 3,
            "description": "身化蝉蜕，可避致命一击",
            "special_effect": "濒死时自动使用，保留1点生命"
        },
        
        # 四级法宝（元婴期可用）
        "天魔诛仙剑": {
            "artifact_type": "飞剑",
            "element": "火",
            "power": 800,
            "speed": 400,
            "tier": 4,
            "description": "魔教至宝，剑光黑红交织",
            "special_effect": "附带灼烧效果"
        },
        "九天元阳尺": {
            "artifact_type": "防御",
            "element": "火",
            "power": 600,
            "speed": 0,
            "tier": 4,
            "description": "尺身阳火旺盛，可炼化邪魔",
            "special_effect": "对邪道敌人伤害加成"
        },
        
        # 五级法宝（化神期可用）
        "轩辕剑": {
            "artifact_type": "飞剑",
            "element": "金",
            "power": 2000,
            "speed": 1000,
            "tier": 5,
            "description": "上古神器，剑气纵横三万里",
            "special_effect": "每回合自动发动一次剑气攻击"
        },
        "昊天镜": {
            "artifact_type": "特殊",
            "element": "金",
            "power": 1500,
            "speed": 0,
            "tier": 5,
            "description": "照妖镜，可破一切幻术",
            "special_effect": "识破敌人所有幻术和隐身"
        }
    }
    
    @classmethod
    def get_artifact(cls, name: str) -> Optional[Artifact]:
        """获取法宝"""
        if name in cls.ARTIFACTS_DB:
            data = cls.ARTIFACTS_DB[name]
            data["name"] = name
            return Artifact.from_dict(data)
        return None
    
    @classmethod
    def get_artifacts_by_tier(cls, tier: int) -> List[str]:
        """获取指定品阶的所有法宝名称"""
        return [
            name for name, data in cls.ARTIFACTS_DB.items()
            if data["tier"] == tier
        ]
    
    @classmethod
    def get_artifacts_by_type(cls, artifact_type: str) -> List[str]:
        """获取指定类型的所有法宝名称"""
        return [
            name for name, data in cls.ARTIFACTS_DB.items()
            if data["artifact_type"] == artifact_type
        ]
    
    @classmethod
    def calculate_damage(cls, attacker_artifact: Artifact, 
                        defender_element: str = None,
                        attacker_realm_level: int = 1) -> int:
        """
        计算伤害
        
        Args:
            attacker_artifact: 攻击方法宝
            defender_element: 防御方五行
            attacker_realm_level: 攻击方境界等级
        
        Returns:
            伤害值
        """
        base_damage = attacker_artifact.power
        
        # 境界加成
        realm_bonus = 1.0 + (attacker_realm_level - 1) * 0.2
        base_damage = int(base_damage * realm_bonus)
        
        # 五行克制
        if defender_element:
            elements = {
                "金": {"克制": "木", "被克": "火"},
                "木": {"克制": "土", "被克": "金"},
                "水": {"克制": "火", "被克": "土"},
                "火": {"克制": "金", "被克": "水"},
                "土": {"克制": "水", "被克": "木"}
            }
            
            if attacker_artifact.element in elements:
                if elements[attacker_artifact.element]["克制"] == defender_element:
                    base_damage = int(base_damage * 1.5)  # 克制加成
                elif elements[attacker_artifact.element]["被克"] == defender_element:
                    base_damage = int(base_damage * 0.7)  # 被克减成
        
        return base_damage
    
    @classmethod
    def create_random_artifact(cls, tier: int = 1) -> Optional[Artifact]:
        """随机创建一个法宝（用于掉落）"""
        import random
        
        artifacts = cls.get_artifacts_by_tier(tier)
        if not artifacts:
            return None
        
        name = random.choice(artifacts)
        return cls.get_artifact(name)
    
    @classmethod
    def list_all(cls) -> Dict[str, dict]:
        """列出所有法宝"""
        return cls.ARTIFACTS_DB.copy()
