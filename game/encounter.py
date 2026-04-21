#!/usr/bin/env python3
"""
蜀山剑侠传 - 奇遇系统
"""

import json
import random
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime


class EncounterType(Enum):
    """奇遇类型"""
    INHERITANCE = "传承"      # 前辈传承、洞府遗宝
    TREASURE = "宝物"         # 天地灵物、法宝丹药
    OPPORTUNITY = "机缘"      # 灵兽认主、功法领悟
    DANGER = "危险"           # 妖兽袭击、阵法陷阱
    STRANGER = "奇人"         # 隐世高人、散修前辈


class TriggerConditionType(Enum):
    """触发条件类型"""
    LOCATION = "地点"         # 特定地点
    REALM = "境界"            # 修为境界
    TIME = "时间"             # 游戏时间
    RANDOM = "概率"           # 随机概率
    KARMA = "功德"            # 功德/业力
    SECT = "门派"             # 门派要求
    SKILL = "功法"            # 已学功法
    ARTIFACT = "法宝"         # 拥有法宝
    FLAG = "标记"             # 游戏标记


class RewardType(Enum):
    """奖励类型"""
    CULTIVATION = "修为"
    SPIRIT_STONES = "灵石"
    KARMA = "功德"
    SKILL = "功法"
    ARTIFACT = "法宝"
    ITEM = "物品"
    MATERIAL = "材料"
    EXPERIENCE = "经验"


class ChoiceEffectType(Enum):
    """选择效果类型"""
    GAIN = "获得"
    LOSE = "失去"
    SET_FLAG = "设置标记"
    UNLOCK = "解锁"
    TRIGGER = "触发"
    DAMAGE = "伤害"
    HEAL = "治疗"


@dataclass
class TriggerCondition:
    """触发条件"""
    condition_type: TriggerConditionType
    value: Any
    description: str = ""
    
    def check(self, player_data: dict, skip_random: bool = False) -> bool:
        """检查条件是否满足
        
        Args:
            player_data: 玩家数据
            skip_random: 是否跳过概率检查（用于获取可用奇遇列表）
        """
        if self.condition_type == TriggerConditionType.LOCATION:
            if isinstance(self.value, list):
                return player_data.get("location") in self.value
            return player_data.get("location") == self.value
        
        elif self.condition_type == TriggerConditionType.REALM:
            player_realm = player_data.get("realm_level", 1)
            if isinstance(self.value, dict):
                min_level = self.value.get("min", 1)
                max_level = self.value.get("max", 99)
                return min_level <= player_realm <= max_level
            return player_realm >= self.value
        
        elif self.condition_type == TriggerConditionType.TIME:
            # 游戏时间检查（可扩展）
            return True
        
        elif self.condition_type == TriggerConditionType.RANDOM:
            if skip_random:
                return True  # 跳过概率检查
            return random.random() < self.value
        
        elif self.condition_type == TriggerConditionType.KARMA:
            player_karma = player_data.get("karma", 0)
            if isinstance(self.value, dict):
                min_karma = self.value.get("min", -9999)
                max_karma = self.value.get("max", 9999)
                return min_karma <= player_karma <= max_karma
            return player_karma >= self.value
        
        elif self.condition_type == TriggerConditionType.SECT:
            return player_data.get("sect") == self.value
        
        elif self.condition_type == TriggerConditionType.SKILL:
            learned_skills = player_data.get("learned_skills", {})
            if isinstance(self.value, list):
                return any(skill in learned_skills for skill in self.value)
            return self.value in learned_skills
        
        elif self.condition_type == TriggerConditionType.ARTIFACT:
            artifacts = player_data.get("artifacts", [])
            artifact_names = [a.get("name") for a in artifacts]
            if isinstance(self.value, list):
                return any(a in artifact_names for a in self.value)
            return self.value in artifact_names
        
        elif self.condition_type == TriggerConditionType.FLAG:
            flags = player_data.get("flags", {})
            return flags.get(self.value, False)
        
        return False


@dataclass
class Reward:
    """奖励"""
    reward_type: RewardType
    value: Any
    quality: str = "普通"  # 普通、精良、稀有、传说
    description: str = ""
    
    def apply(self, player_data: dict) -> dict:
        """应用奖励"""
        result = {
            "type": self.reward_type.value,
            "value": self.value,
            "quality": self.quality,
            "description": self.description
        }
        
        if self.reward_type == RewardType.CULTIVATION:
            player_data["cultivation"] = player_data.get("cultivation", 0) + self.value
            result["message"] = f"修为 +{self.value}"
        
        elif self.reward_type == RewardType.SPIRIT_STONES:
            player_data["spirit_stones"] = player_data.get("spirit_stones", 0) + self.value
            result["message"] = f"灵石 +{self.value}"
        
        elif self.reward_type == RewardType.KARMA:
            player_data["karma"] = player_data.get("karma", 0) + self.value
            result["message"] = f"功德 +{self.value}" if self.value > 0 else f"业力 {self.value}"
        
        elif self.reward_type == RewardType.SKILL:
            learned_skills = player_data.get("learned_skills", {})
            skill_id = self.value.get("id", self.value) if isinstance(self.value, dict) else self.value
            if skill_id not in learned_skills:
                learned_skills[skill_id] = 1
                player_data["learned_skills"] = learned_skills
            result["message"] = f"习得功法【{self.value.get('name', skill_id)}】"
        
        elif self.reward_type == RewardType.ARTIFACT:
            artifacts = player_data.get("artifacts", [])
            artifacts.append(self.value)
            player_data["artifacts"] = artifacts
            result["message"] = f"获得法宝【{self.value.get('name', '未知法宝')}】"
        
        elif self.reward_type == RewardType.ITEM:
            items = player_data.get("items", {})
            item_name = self.value.get("name", "未知物品")
            items[item_name] = items.get(item_name, 0) + self.value.get("amount", 1)
            player_data["items"] = items
            result["message"] = f"获得 {item_name} x{self.value.get('amount', 1)}"
        
        elif self.reward_type == RewardType.MATERIAL:
            materials = player_data.get("materials", {})
            mat_name = self.value.get("name", "未知材料")
            materials[mat_name] = materials.get(mat_name, 0) + self.value.get("amount", 1)
            player_data["materials"] = materials
            result["message"] = f"获得 {mat_name} x{self.value.get('amount', 1)}"
        
        elif self.reward_type == RewardType.EXPERIENCE:
            # 经验值可以用于其他用途
            result["message"] = f"获得经验 +{self.value}"
        
        return result


@dataclass
class ChoiceEffect:
    """选择效果"""
    effect_type: ChoiceEffectType
    target: str
    value: Any
    probability: float = 1.0  # 触发概率
    
    def apply(self, player_data: dict) -> dict:
        """应用效果"""
        if random.random() > self.probability:
            return {"success": False, "message": "效果未触发"}
        
        result = {"success": True, "type": self.effect_type.value}
        
        if self.effect_type == ChoiceEffectType.GAIN:
            # 获得物品/属性
            if self.target == "修为":
                player_data["cultivation"] = player_data.get("cultivation", 0) + self.value
                result["message"] = f"修为 +{self.value}"
            elif self.target == "灵石":
                player_data["spirit_stones"] = player_data.get("spirit_stones", 0) + self.value
                result["message"] = f"灵石 +{self.value}"
            elif self.target == "功德":
                player_data["karma"] = player_data.get("karma", 0) + self.value
                result["message"] = f"功德 +{self.value}" if self.value > 0 else f"业力 {self.value}"
        
        elif self.effect_type == ChoiceEffectType.LOSE:
            # 失去物品/属性
            if self.target == "修为":
                lost = min(self.value, player_data.get("cultivation", 0))
                player_data["cultivation"] = player_data.get("cultivation", 0) - lost
                result["message"] = f"修为 -{lost}"
            elif self.target == "灵石":
                lost = min(self.value, player_data.get("spirit_stones", 0))
                player_data["spirit_stones"] = player_data.get("spirit_stones", 0) - lost
                result["message"] = f"灵石 -{lost}"
            elif self.target == "生命":
                lost = min(self.value, player_data.get("current_hp", 100))
                player_data["current_hp"] = player_data.get("current_hp", 100) - lost
                result["message"] = f"生命 -{lost}"
        
        elif self.effect_type == ChoiceEffectType.SET_FLAG:
            flags = player_data.get("flags", {})
            flags[self.target] = self.value
            player_data["flags"] = flags
            result["message"] = f"标记【{self.target}】已设置"
        
        elif self.effect_type == ChoiceEffectType.UNLOCK:
            unlocks = player_data.get("unlocks", [])
            if self.target not in unlocks:
                unlocks.append(self.target)
                player_data["unlocks"] = unlocks
            result["message"] = f"解锁【{self.target}】"
        
        elif self.effect_type == ChoiceEffectType.TRIGGER:
            # 触发另一个奇遇或事件
            result["trigger"] = self.value
            result["message"] = f"触发事件【{self.value}】"
        
        elif self.effect_type == ChoiceEffectType.DAMAGE:
            damage = self.value
            current_hp = player_data.get("current_hp", 100)
            player_data["current_hp"] = max(1, current_hp - damage)
            result["message"] = f"受到 {damage} 点伤害"
        
        elif self.effect_type == ChoiceEffectType.HEAL:
            heal = self.value
            current_hp = player_data.get("current_hp", 100)
            max_hp = player_data.get("max_hp", 100)
            player_data["current_hp"] = min(max_hp, current_hp + heal)
            result["message"] = f"恢复 {heal} 点生命"
        
        return result


@dataclass
class Choice:
    """选择项"""
    text: str
    description: str = ""
    requirements: List[TriggerCondition] = field(default_factory=list)
    effects: List[ChoiceEffect] = field(default_factory=list)
    rewards: List[Reward] = field(default_factory=list)
    next_encounter_id: Optional[str] = None  # 连锁奇遇
    karma_change: int = 0
    
    def can_choose(self, player_data: dict) -> bool:
        """检查是否可以选择"""
        for req in self.requirements:
            if not req.check(player_data):
                return False
        return True
    
    def execute(self, player_data: dict) -> dict:
        """执行选择"""
        result = {
            "text": self.text,
            "effects": [],
            "rewards": [],
            "karma_change": self.karma_change,
            "next_encounter": self.next_encounter_id
        }
        
        # 应用效果
        for effect in self.effects:
            effect_result = effect.apply(player_data)
            result["effects"].append(effect_result)
        
        # 应用奖励
        for reward in self.rewards:
            reward_result = reward.apply(player_data)
            result["rewards"].append(reward_result)
        
        # 修改功德
        if self.karma_change != 0:
            player_data["karma"] = player_data.get("karma", 0) + self.karma_change
        
        return result


@dataclass
class Encounter:
    """奇遇类"""
    encounter_id: str
    name: str
    encounter_type: EncounterType
    description: str
    story: str  # 奇遇故事描述
    trigger_conditions: List[TriggerCondition] = field(default_factory=list)
    choices: List[Choice] = field(default_factory=list)
    rewards: List[Reward] = field(default_factory=list)
    risk_level: int = 1  # 风险等级 1-5
    rarity: str = "普通"  # 普通、稀有、传说
    chain_next: Optional[str] = None  # 连锁奇遇ID
    location_specific: List[str] = field(default_factory=list)  # 特定地点
    one_time: bool = True  # 是否一次性奇遇
    discovered: bool = False
    
    def can_trigger(self, player_data: dict, skip_random: bool = False) -> tuple:
        """
        检查是否可以触发
        
        Args:
            player_data: 玩家数据
            skip_random: 是否跳过概率检查（用于获取可用奇遇列表）
        
        Returns:
            (can_trigger, reason)
        """
        # 检查一次性奇遇
        if self.one_time and self.discovered:
            return False, "此奇遇已经触发过"
        
        # 检查地点限制
        if self.location_specific:
            player_loc = player_data.get("location", "")
            if player_loc not in self.location_specific:
                return False, f"需要地点：{', '.join(self.location_specific)}"
        
        # 检查触发条件
        for condition in self.trigger_conditions:
            if not condition.check(player_data, skip_random):
                return False, condition.description or f"条件不满足：{condition.condition_type.value}"
        
        return True, "可以触发"
    
    def trigger(self, player_data: dict, skip_random: bool = False) -> dict:
        """触发奇遇
        
        Args:
            player_data: 玩家数据
            skip_random: 是否跳过概率检查
        """
        can_trigger, reason = self.can_trigger(player_data, skip_random)
        
        if not can_trigger:
            return {
                "success": False,
                "message": reason,
                "encounter_id": self.encounter_id
            }
        
        # 标记为已发现
        self.discovered = True
        
        result = {
            "success": True,
            "encounter_id": self.encounter_id,
            "name": self.name,
            "type": self.encounter_type.value,
            "description": self.description,
            "story": self.story,
            "risk_level": self.risk_level,
            "rarity": self.rarity,
            "choices": [],
            "available_choices": [],
            "rewards": [],
            "chain_next": self.chain_next,
            "timestamp": datetime.now().isoformat()
        }
        
        # 准备选择项
        for i, choice in enumerate(self.choices):
            choice_info = {
                "index": i,
                "text": choice.text,
                "description": choice.description,
                "available": choice.can_choose(player_data)
            }
            result["choices"].append(choice_info)
            
            if choice_info["available"]:
                result["available_choices"].append(i)
        
        # 如果没有选择，直接发放奖励
        if not self.choices:
            for reward in self.rewards:
                reward_result = reward.apply(player_data)
                result["rewards"].append(reward_result)
        
        return result
    
    def make_choice(self, choice_index: int, player_data: dict) -> dict:
        """做出选择"""
        if choice_index < 0 or choice_index >= len(self.choices):
            return {
                "success": False,
                "message": "无效的选择"
            }
        
        choice = self.choices[choice_index]
        
        if not choice.can_choose(player_data):
            return {
                "success": False,
                "message": "无法选择此选项"
            }
        
        result = choice.execute(player_data)
        result["success"] = True
        result["encounter_id"] = self.encounter_id
        result["encounter_name"] = self.name
        
        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> "Encounter":
        """从字典创建奇遇"""
        # 解析奇遇类型
        encounter_type = EncounterType(data.get("type", "机缘"))
        
        # 解析触发条件
        trigger_conditions = []
        for cond_data in data.get("trigger_conditions", []):
            cond_type = TriggerConditionType(cond_data.get("type", "概率"))
            trigger_conditions.append(TriggerCondition(
                condition_type=cond_type,
                value=cond_data.get("value"),
                description=cond_data.get("description", "")
            ))
        
        # 解析选择项
        choices = []
        for choice_data in data.get("choices", []):
            # 解析选择的要求
            requirements = []
            for req_data in choice_data.get("requirements", []):
                req_type = TriggerConditionType(req_data.get("type", "概率"))
                requirements.append(TriggerCondition(
                    condition_type=req_type,
                    value=req_data.get("value"),
                    description=req_data.get("description", "")
                ))
            
            # 解析选择的效果
            effects = []
            for eff_data in choice_data.get("effects", []):
                eff_type = ChoiceEffectType(eff_data.get("type", "获得"))
                effects.append(ChoiceEffect(
                    effect_type=eff_type,
                    target=eff_data.get("target", ""),
                    value=eff_data.get("value"),
                    probability=eff_data.get("probability", 1.0)
                ))
            
            # 解析选择的奖励
            rewards = []
            for reward_data in choice_data.get("rewards", []):
                reward_type = RewardType(reward_data.get("type", "修为"))
                rewards.append(Reward(
                    reward_type=reward_type,
                    value=reward_data.get("value"),
                    quality=reward_data.get("quality", "普通"),
                    description=reward_data.get("description", "")
                ))
            
            choices.append(Choice(
                text=choice_data.get("text", ""),
                description=choice_data.get("description", ""),
                requirements=requirements,
                effects=effects,
                rewards=rewards,
                next_encounter_id=choice_data.get("next_encounter"),
                karma_change=choice_data.get("karma_change", 0)
            ))
        
        # 解析奖励
        rewards = []
        for reward_data in data.get("rewards", []):
            reward_type = RewardType(reward_data.get("type", "修为"))
            rewards.append(Reward(
                reward_type=reward_type,
                value=reward_data.get("value"),
                quality=reward_data.get("quality", "普通"),
                description=reward_data.get("description", "")
            ))
        
        return cls(
            encounter_id=data.get("id", ""),
            name=data.get("name", "未知奇遇"),
            encounter_type=encounter_type,
            description=data.get("description", ""),
            story=data.get("story", ""),
            trigger_conditions=trigger_conditions,
            choices=choices,
            rewards=rewards,
            risk_level=data.get("risk_level", 1),
            rarity=data.get("rarity", "普通"),
            chain_next=data.get("chain_next"),
            location_specific=data.get("location_specific", []),
            one_time=data.get("one_time", True)
        )


class EncounterManager:
    """奇遇管理器"""
    
    def __init__(self, data_path: str = "data/encounters.json"):
        self.encounters: Dict[str, Encounter] = {}
        self.encounter_history: List[dict] = []
        self.discovered_encounters: set = set()
        self.load_encounters(data_path)
    
    def load_encounters(self, data_path: str):
        """加载奇遇数据"""
        path = Path(data_path)
        if not path.exists():
            print(f"警告：奇遇数据文件不存在: {data_path}")
            return
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for encounter_data in data.get("encounters", []):
            encounter = Encounter.from_dict(encounter_data)
            self.encounters[encounter.encounter_id] = encounter
        
        print(f"加载了 {len(self.encounters)} 个奇遇")
    
    def get_encounter(self, encounter_id: str) -> Optional[Encounter]:
        """获取奇遇"""
        return self.encounters.get(encounter_id)
    
    def get_available_encounters(self, player_data: dict, location: str = None) -> List[Encounter]:
        """获取可触发的奇遇列表（跳过概率检查）"""
        available = []
        
        for encounter in self.encounters.values():
            # 跳过概率检查，只检查硬性条件
            can_trigger, _ = encounter.can_trigger(player_data, skip_random=True)
            
            if can_trigger:
                # 地点过滤
                if location and encounter.location_specific:
                    if location not in encounter.location_specific:
                        continue
                
                available.append(encounter)
        
        return available
    
    def trigger_random_encounter(self, player_data: dict, location: str = None) -> Optional[dict]:
        """
        随机触发一个奇遇
        
        Args:
            player_data: 玩家数据
            location: 当前地点
        
        Returns:
            触发结果
        """
        available = self.get_available_encounters(player_data, location)
        
        if not available:
            return None
        
        # 尝试触发多个奇遇，直到成功或全部失败
        random.shuffle(available)  # 随机打乱顺序
        
        for encounter in available:
            # 检查概率条件
            can_trigger, _ = encounter.can_trigger(player_data, skip_random=False)
            
            if can_trigger:
                # 成功触发，跳过概率检查直接触发
                result = encounter.trigger(player_data, skip_random=True)
                
                # 记录历史
                if result.get("success"):
                    self.encounter_history.append({
                        "encounter_id": encounter.encounter_id,
                        "name": encounter.name,
                        "type": encounter.encounter_type.value,
                        "location": location,
                        "timestamp": datetime.now().isoformat()
                    })
                    self.discovered_encounters.add(encounter.encounter_id)
                
                return result
        
        # 所有奇遇的概率条件都不满足
        return None
    
    def trigger_specific_encounter(self, encounter_id: str, player_data: dict, check_probability: bool = True) -> Optional[dict]:
        """触发指定奇遇
        
        Args:
            encounter_id: 奇遇ID
            player_data: 玩家数据
            check_probability: 是否检查概率条件
        """
        encounter = self.get_encounter(encounter_id)
        
        if not encounter:
            return {
                "success": False,
                "message": f"未知奇遇：{encounter_id}"
            }
        
        result = encounter.trigger(player_data, skip_random=not check_probability)
        
        if result.get("success"):
            self.encounter_history.append({
                "encounter_id": encounter_id,
                "name": encounter.name,
                "type": encounter.encounter_type.value,
                "timestamp": datetime.now().isoformat()
            })
            self.discovered_encounters.add(encounter_id)
        
        return result
    
    def make_choice(self, encounter_id: str, choice_index: int, player_data: dict) -> dict:
        """做出选择"""
        encounter = self.get_encounter(encounter_id)
        
        if not encounter:
            return {
                "success": False,
                "message": f"未知奇遇：{encounter_id}"
            }
        
        result = encounter.make_choice(choice_index, player_data)
        
        # 如果有连锁奇遇，自动触发
        if result.get("success") and result.get("next_encounter"):
            next_id = result["next_encounter"]
            next_encounter = self.get_encounter(next_id)
            if next_encounter:
                chain_result = next_encounter.trigger(player_data)
                result["chain_result"] = chain_result
        
        return result
    
    def get_encounter_info(self, encounter_id: str) -> Optional[dict]:
        """获取奇遇详情"""
        encounter = self.get_encounter(encounter_id)
        
        if not encounter:
            return None
        
        return {
            "id": encounter.encounter_id,
            "name": encounter.name,
            "type": encounter.encounter_type.value,
            "description": encounter.description,
            "story": encounter.story,
            "risk_level": encounter.risk_level,
            "rarity": encounter.rarity,
            "locations": encounter.location_specific,
            "one_time": encounter.one_time,
            "discovered": encounter.discovered
        }
    
    def get_encounter_history(self, limit: int = 10) -> List[dict]:
        """获取奇遇历史"""
        return self.encounter_history[-limit:]
    
    def get_discovered_count(self) -> int:
        """获取已发现的奇遇数量"""
        return len(self.discovered_encounters)
    
    def get_total_count(self) -> int:
        """获取总奇遇数量"""
        return len(self.encounters)
    
    def get_encounters_by_type(self, encounter_type: EncounterType) -> List[Encounter]:
        """按类型获取奇遇"""
        return [e for e in self.encounters.values() if e.encounter_type == encounter_type]
    
    def get_encounters_by_location(self, location: str) -> List[Encounter]:
        """按地点获取奇遇"""
        return [e for e in self.encounters.values() 
                if not e.location_specific or location in e.location_specific]
    
    def reset_discovered(self):
        """重置已发现状态（用于新游戏）"""
        self.discovered_encounters.clear()
        self.encounter_history.clear()
        for encounter in self.encounters.values():
            encounter.discovered = False


# 便捷函数
def create_encounter_manager(data_path: str = "data/encounters.json") -> EncounterManager:
    """创建奇遇管理器"""
    return EncounterManager(data_path)


# 测试代码
if __name__ == "__main__":
    # 测试奇遇管理器
    manager = create_encounter_manager()
    
    print(f"\n总奇遇数: {manager.get_total_count()}")
    print(f"已发现: {manager.get_discovered_count()}")
    
    # 按类型统计
    print("\n按类型统计:")
    for et in EncounterType:
        count = len(manager.get_encounters_by_type(et))
        print(f"  {et.value}: {count}")
    
    # 测试触发
    print("\n测试触发奇遇:")
    player = {
        "name": "测试玩家",
        "realm_level": 2,
        "cultivation": 1500,
        "spirit_stones": 500,
        "karma": 10,
        "location": "峨眉山",
        "stats": {"幸运": 60},
        "learned_skills": {},
        "artifacts": [],
        "flags": {}
    }
    
    result = manager.trigger_random_encounter(player)
    if result:
        print(f"\n触发奇遇: {result['name']}")
        print(f"类型: {result['type']}")
        print(f"故事: {result['story']}")
        print(f"可选操作: {len(result['available_choices'])} 个")
    else:
        print("没有可触发的奇遇")
