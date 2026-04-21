#!/usr/bin/env python3
"""
蜀山剑侠传 - 炼丹炼器系统

包含材料管理、炼丹、炼器、法宝强化等功能
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"


@dataclass
class Material:
    """材料类"""
    name: str
    material_type: str  # 矿石、药材、妖丹、灵材
    quality: str  # 凡、灵、仙、神
    element: str
    description: str
    base_value: int
    rarity: int
    source: List[str]
    stack_max: int
    count: int = 1
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "material_type": self.material_type,
            "quality": self.quality,
            "element": self.element,
            "description": self.description,
            "base_value": self.base_value,
            "rarity": self.rarity,
            "source": self.source,
            "stack_max": self.stack_max,
            "count": self.count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Material":
        return cls(
            name=data["name"],
            material_type=data["type"],
            quality=data["quality"],
            element=data["element"],
            description=data["description"],
            base_value=data["base_value"],
            rarity=data["rarity"],
            source=data["source"],
            stack_max=data["stack_max"],
            count=data.get("count", 1)
        )


@dataclass
class Pill:
    """丹药类"""
    name: str
    tier: int
    description: str
    effect: Dict
    value: int
    count: int = 1
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "tier": self.tier,
            "description": self.description,
            "effect": self.effect,
            "value": self.value,
            "count": self.count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Pill":
        return cls(
            name=data["name"],
            tier=data["tier"],
            description=data["description"],
            effect=data["effect"],
            value=data["value"],
            count=data.get("count", 1)
        )


class CraftingManager:
    """炼丹炼器管理器"""
    
    # 材料数据库
    MATERIALS_DB: Dict = {}
    # 配方数据库
    RECIPES_DB: Dict = {}
    # 是否已加载
    _loaded = False
    
    @classmethod
    def load_data(cls):
        """加载数据库"""
        if cls._loaded:
            return
        
        # 加载材料
        materials_file = DATA_DIR / "materials.json"
        if materials_file.exists():
            with open(materials_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                cls.MATERIALS_DB = data.get("materials", {})
        
        # 加载配方
        recipes_file = DATA_DIR / "recipes.json"
        if recipes_file.exists():
            with open(recipes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                cls.RECIPES_DB = data.get("recipes", {})
        
        cls._loaded = True
    
    @classmethod
    def get_material(cls, name: str) -> Optional[Material]:
        """获取材料信息"""
        cls.load_data()
        if name in cls.MATERIALS_DB:
            return Material.from_dict(cls.MATERIALS_DB[name])
        return None
    
    @classmethod
    def get_recipe(cls, name: str) -> Optional[dict]:
        """获取配方信息"""
        cls.load_data()
        # 支持带或不带"_配方"后缀
        recipe_name = name if name in cls.RECIPES_DB else f"{name}_配方"
        return cls.RECIPES_DB.get(recipe_name)
    
    @classmethod
    def get_recipes_by_type(cls, recipe_type: str) -> List[str]:
        """获取指定类型的所有配方名称"""
        cls.load_data()
        return [
            name for name, data in cls.RECIPES_DB.items()
            if data.get("type") == recipe_type
        ]
    
    @classmethod
    def get_recipes_by_tier(cls, tier: int) -> List[str]:
        """获取指定品阶的所有配方名称"""
        cls.load_data()
        return [
            name for name, data in cls.RECIPES_DB.items()
            if data.get("tier") == tier
        ]


class AlchemySystem:
    """炼丹系统"""
    
    def __init__(self):
        CraftingManager.load_data()
    
    def can_craft(self, recipe_name: str, inventory: Dict, realm: str, cultivation: int) -> Tuple[bool, str]:
        """
        检查是否可以炼丹
        
        Args:
            recipe_name: 配方名称
            inventory: 背包材料
            realm: 当前境界
            cultivation: 当前修为
        
        Returns:
            (是否可以炼制, 原因说明)
        """
        recipe = CraftingManager.get_recipe(recipe_name)
        if not recipe:
            return False, f"未找到配方：{recipe_name}"
        
        if recipe.get("type") != "丹药":
            return False, "这不是丹药配方"
        
        # 检查境界
        from config import REALMS
        required_realm = recipe.get("realm_required", "练气期")
        current_level = REALMS.get(realm, {}).get("level", 1)
        required_level = REALMS.get(required_realm, {}).get("level", 1)
        
        if current_level < required_level:
            return False, f"境界不足，需要 {required_realm}"
        
        # 检查修为
        if cultivation < recipe.get("cultivation_required", 0):
            return False, f"修为不足，需要 {recipe.get('cultivation_required')} 修为"
        
        # 检查材料
        materials = recipe.get("materials", {})
        for mat_name, count in materials.items():
            if inventory.get(mat_name, 0) < count:
                return False, f"材料不足：{mat_name} 需要 {count}，现有 {inventory.get(mat_name, 0)}"
        
        return True, "可以炼制"
    
    def craft(self, recipe_name: str, inventory: Dict, realm: str, cultivation: int,
              skill_bonus: float = 0.0, luck: int = 50) -> dict:
        """
        炼丹
        
        Args:
            recipe_name: 配方名称
            inventory: 背包材料
            realm: 当前境界
            cultivation: 当前修为
            skill_bonus: 功法加成（0-1）
            luck: 幸运值
        
        Returns:
            炼丹结果
        """
        # 检查是否可以炼制
        can_craft, reason = self.can_craft(recipe_name, inventory, realm, cultivation)
        if not can_craft:
            return {"success": False, "message": reason}
        
        recipe = CraftingManager.get_recipe(recipe_name)
        
        # 消耗材料
        materials = recipe.get("materials", {})
        for mat_name, count in materials.items():
            inventory[mat_name] -= count
            if inventory[mat_name] <= 0:
                del inventory[mat_name]
        
        # 计算成功率
        base_rate = recipe.get("success_rate", 50) / 100
        # 幸运加成
        luck_bonus = (luck - 50) / 200  # -0.25 到 0.25
        # 功法加成
        final_rate = base_rate + luck_bonus + skill_bonus
        final_rate = max(0.1, min(0.95, final_rate))  # 限制在 10%-95%
        
        # 判定是否成功
        success = random.random() < final_rate
        
        if success:
            output_count = recipe.get("output_count", 1)
            pill = Pill(
                name=recipe.get("name"),
                tier=recipe.get("tier"),
                description=recipe.get("description"),
                effect=recipe.get("effect"),
                value=recipe.get("value"),
                count=output_count
            )
            return {
                "success": True,
                "message": f"🎉 炼制成功！获得 {recipe.get('name')} x{output_count}",
                "pill": pill,
                "consumed": materials
            }
        else:
            return {
                "success": False,
                "message": "炼制失败，材料已消耗",
                "consumed": materials
            }
    
    def use_pill(self, pill_name: str, player) -> dict:
        """
        使用丹药
        
        Args:
            pill_name: 丹药名称
            player: 玩家对象
        
        Returns:
            使用结果
        """
        # 从玩家丹药列表查找
        pill = None
        for p in player.pills:
            if p.name == pill_name:
                pill = p
                break
        
        if not pill:
            return {"success": False, "message": f"未找到丹药：{pill_name}"}
        
        # 应用效果
        effects = pill.effect
        messages = []
        
        if "生命" in effects:
            heal = min(effects["生命"], player.max_hp - player.current_hp)
            player.current_hp += heal
            messages.append(f"生命 +{heal}")
        
        if "真元" in effects:
            restore = min(effects["真元"], player.max_mp - player.current_mp)
            player.current_mp += restore
            messages.append(f"真元 +{restore}")
        
        if "修为" in effects:
            player.cultivation += effects["修为"]
            messages.append(f"修为 +{effects['修为']}")
        
        if "全属性" in effects:
            for stat in player.stats:
                player.stats[stat] += effects["全属性"]
            messages.append(f"全属性 +{effects['全属性']}")
        
        # 减少数量
        pill.count -= 1
        if pill.count <= 0:
            player.pills.remove(pill)
        
        return {
            "success": True,
            "message": f"使用 {pill_name}，" + "，".join(messages)
        }
    
    def list_pills(self) -> List[str]:
        """列出所有丹药配方"""
        return CraftingManager.get_recipes_by_type("丹药")


class ForgeSystem:
    """炼器系统"""
    
    def __init__(self):
        CraftingManager.load_data()
    
    def can_craft(self, recipe_name: str, inventory: Dict, realm: str, cultivation: int) -> Tuple[bool, str]:
        """检查是否可以炼器"""
        recipe = CraftingManager.get_recipe(recipe_name)
        if not recipe:
            return False, f"未找到配方：{recipe_name}"
        
        if recipe.get("type") != "法宝":
            return False, "这不是法宝配方"
        
        # 检查境界
        from config import REALMS
        required_realm = recipe.get("realm_required", "练气期")
        current_level = REALMS.get(realm, {}).get("level", 1)
        required_level = REALMS.get(required_realm, {}).get("level", 1)
        
        if current_level < required_level:
            return False, f"境界不足，需要 {required_realm}"
        
        # 检查修为
        if cultivation < recipe.get("cultivation_required", 0):
            return False, f"修为不足，需要 {recipe.get('cultivation_required')} 修为"
        
        # 检查材料
        materials = recipe.get("materials", {})
        for mat_name, count in materials.items():
            if inventory.get(mat_name, 0) < count:
                return False, f"材料不足：{mat_name} 需要 {count}，现有 {inventory.get(mat_name, 0)}"
        
        return True, "可以炼制"
    
    def craft(self, recipe_name: str, inventory: Dict, realm: str, cultivation: int,
              skill_bonus: float = 0.0, luck: int = 50) -> dict:
        """炼器"""
        can_craft, reason = self.can_craft(recipe_name, inventory, realm, cultivation)
        if not can_craft:
            return {"success": False, "message": reason}
        
        recipe = CraftingManager.get_recipe(recipe_name)
        
        # 消耗材料
        materials = recipe.get("materials", {})
        for mat_name, count in materials.items():
            inventory[mat_name] -= count
            if inventory[mat_name] <= 0:
                del inventory[mat_name]
        
        # 计算成功率
        base_rate = recipe.get("success_rate", 50) / 100
        luck_bonus = (luck - 50) / 200
        final_rate = base_rate + luck_bonus + skill_bonus
        final_rate = max(0.1, min(0.95, final_rate))
        
        success = random.random() < final_rate
        
        if success:
            output = recipe.get("output", {})
            artifact = {
                "name": output.get("name", recipe.get("name")),
                "artifact_type": output.get("artifact_type", "飞剑"),
                "element": output.get("element", "金"),
                "power": output.get("power", 50),
                "speed": output.get("speed", 50),
                "tier": recipe.get("tier", 1),
                "description": recipe.get("description", ""),
                "special_effect": output.get("special_effect"),
                "enhance_level": 0  # 强化等级
            }
            return {
                "success": True,
                "message": f"🎉 炼制成功！获得法宝【{artifact['name']}】",
                "artifact": artifact,
                "consumed": materials
            }
        else:
            return {
                "success": False,
                "message": "炼制失败，材料已消耗",
                "consumed": materials
            }
    
    def enhance_artifact(self, artifact: dict, inventory: Dict, realm: str,
                         luck: int = 50) -> dict:
        """
        强化法宝
        
        Args:
            artifact: 法宝数据
            inventory: 背包材料
            realm: 当前境界
            luck: 幸运值
        
        Returns:
            强化结果
        """
        current_level = artifact.get("enhance_level", 0)
        
        if current_level >= 10:
            return {"success": False, "message": "法宝已达最高强化等级"}
        
        # 确定需要的材料
        if current_level < 3:
            required = {"精金": 2, "妖兽内丹": 1}
        elif current_level < 6:
            required = {"星辰砂": 2, "妖王晶": 1}
        elif current_level < 9:
            required = {"天雷石": 2, "龙鳞": 1}
        else:
            required = {"太乙精金": 1, "龙珠": 1}
        
        # 检查材料
        for mat_name, count in required.items():
            if inventory.get(mat_name, 0) < count:
                return {"success": False, "message": f"材料不足：{mat_name} 需要 {count}"}
        
        # 消耗材料
        for mat_name, count in required.items():
            inventory[mat_name] -= count
            if inventory[mat_name] <= 0:
                del inventory[mat_name]
        
        # 计算成功率
        base_rate = 0.9 - current_level * 0.08  # 逐级递减
        luck_bonus = (luck - 50) / 200
        final_rate = base_rate + luck_bonus
        final_rate = max(0.1, min(0.9, final_rate))
        
        success = random.random() < final_rate
        
        if success:
            artifact["enhance_level"] = current_level + 1
            # 属性提升 10%
            artifact["power"] = int(artifact["power"] * 1.1)
            if artifact["speed"] > 0:
                artifact["speed"] = int(artifact["speed"] * 1.1)
            
            return {
                "success": True,
                "message": f"强化成功！法宝强化至 +{artifact['enhance_level']}",
                "artifact": artifact
            }
        else:
            return {
                "success": False,
                "message": "强化失败，材料已消耗",
                "consumed": required
            }
    
    def list_artifacts(self) -> List[str]:
        """列出所有法宝配方"""
        return CraftingManager.get_recipes_by_type("法宝")


class Inventory:
    """背包系统"""
    
    def __init__(self):
        self.materials: Dict[str, int] = {}  # 材料名称 -> 数量
        self.pills: List[Pill] = []  # 丹药列表
        self.capacity: int = 100  # 背包容量（不同物品数）
    
    def add_material(self, name: str, count: int = 1) -> bool:
        """添加材料"""
        material = CraftingManager.get_material(name)
        if not material:
            return False
        
        if name in self.materials:
            # 检查堆叠上限
            if self.materials[name] + count > material.stack_max:
                self.materials[name] = material.stack_max
                return False
            self.materials[name] += count
        else:
            # 检查容量
            if len(self.materials) >= self.capacity:
                return False
            self.materials[name] = min(count, material.stack_max)
        
        return True
    
    def remove_material(self, name: str, count: int = 1) -> bool:
        """移除材料"""
        if name not in self.materials:
            return False
        
        if self.materials[name] < count:
            return False
        
        self.materials[name] -= count
        if self.materials[name] <= 0:
            del self.materials[name]
        
        return True
    
    def get_material_count(self, name: str) -> int:
        """获取材料数量"""
        return self.materials.get(name, 0)
    
    def add_pill(self, pill: Pill) -> bool:
        """添加丹药"""
        # 检查是否已有同类型丹药
        for p in self.pills:
            if p.name == pill.name:
                p.count += pill.count
                return True
        
        # 检查容量
        if len(self.pills) >= self.capacity:
            return False
        
        self.pills.append(pill)
        return True
    
    def remove_pill(self, name: str, count: int = 1) -> bool:
        """移除丹药"""
        for pill in self.pills:
            if pill.name == name:
                if pill.count < count:
                    return False
                pill.count -= count
                if pill.count <= 0:
                    self.pills.remove(pill)
                return True
        return False
    
    def to_dict(self) -> dict:
        """序列化为字典"""
        return {
            "materials": self.materials.copy(),
            "pills": [p.to_dict() for p in self.pills],
            "capacity": self.capacity
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Inventory":
        """从字典创建"""
        inv = cls()
        inv.materials = data.get("materials", {})
        inv.pills = [Pill.from_dict(p) for p in data.get("pills", [])]
        inv.capacity = data.get("capacity", 100)
        return inv
    
    def list_materials(self) -> List[Tuple[str, int, str]]:
        """列出所有材料（名称、数量、品质）"""
        result = []
        for name, count in self.materials.items():
            material = CraftingManager.get_material(name)
            if material:
                result.append((name, count, material.quality))
        return result
    
    def __str__(self) -> str:
        """背包信息"""
        lines = ["【背包】"]
        lines.append(f"容量：{len(self.materials) + len(self.pills)}/{self.capacity}")
        lines.append("")
        
        if self.materials:
            lines.append("【材料】")
            for name, count in self.materials.items():
                material = CraftingManager.get_material(name)
                quality = material.quality if material else "?"
                lines.append(f"  {name} x{count} [{quality}]")
        
        if self.pills:
            lines.append("")
            lines.append("【丹药】")
            for pill in self.pills:
                lines.append(f"  {pill.name} x{pill.count} (品阶:{pill.tier})")
        
        return "\n".join(lines)


# 便捷函数
def get_crafting_info() -> str:
    """获取炼丹炼器系统信息"""
    CraftingManager.load_data()
    
    info = """
【炼丹炼器系统】

=== 材料类型 ===
- 矿石：炼器主材
- 药材：炼丹主材
- 妖丹：炼丹炼器辅材
- 灵材：炼丹炼器辅材

=== 品质等级 ===
- 凡（白色）：凡间常见
- 灵（绿色）：蕴含灵气
- 仙（蓝色）：仙家珍品
- 神（金色）：上古神物

=== 丹药配方 ===
{pills}

=== 法宝配方 ===
{artifacts}
""".format(
        pills="\n".join([f"  - {name}" for name in AlchemySystem().list_pills()]),
        artifacts="\n".join([f"  - {name}" for name in ForgeSystem().list_artifacts()])
    )
    
    return info
