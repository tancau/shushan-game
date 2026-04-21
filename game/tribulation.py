#!/usr/bin/env python3
"""
蜀山剑侠传 - 天劫系统
修仙者渡劫飞升的核心玩法
"""

import random
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field


# ==================== 枚举类型 ====================

class TribulationType(Enum):
    """天劫类型"""
    THUNDER = "雷劫"          # 天雷劫 - 最常见的天劫
    HEART_DEMON = "心魔劫"    # 心魔入侵 - 考验道心
    FIVE_DECAYS = "天人五衰"   # 生老病死苦 - 最危险的天劫


class TribulationTier(Enum):
    """天劫等级"""
    MINOR = "小天劫"          # 初级天劫
    MAJOR = "大天劫"          # 中级天劫
    EXTINCTION = "灭世天劫"   # 最高级天劫


class TribulationStage(Enum):
    """天劫境界阶段"""
    FOUNDATION = "筑基劫"      # 筑基期渡劫
    GOLDEN_CORE = "金丹劫"     # 金丹期渡劫
    NASCENT_SOUL = "元婴劫"    # 元婴期渡劫
    SPIRIT_SEVERING = "化神劫" # 化神期渡劫
    TRIBULATION = "渡劫期天劫" # 渡劫期飞升


class TribulationStatus(Enum):
    """天劫状态"""
    PENDING = "未开始"
    IN_PROGRESS = "渡劫中"
    SUCCESS = "渡劫成功"
    FAILED = "渡劫失败"


class PreparationType(Enum):
    """渡劫准备类型"""
    ARTIFACT = "法宝"
    PILL = "丹药"
    FORMATION = "阵法"


# ==================== 数据类 ====================

@dataclass
class TribulationWave:
    """天劫波次"""
    wave_number: int
    wave_type: TribulationType
    damage: int                    # 基础伤害
    rounds: int = 1                # 持续回合
    special_effect: Optional[str] = None  # 特殊效果
    description: str = ""


@dataclass
class TribulationConfig:
    """天劫配置"""
    tribulation_id: str
    name: str
    stage: TribulationStage
    tier: TribulationTier
    tribulation_type: TribulationType
    
    # 基础属性
    description: str
    waves: List[TribulationWave]
    
    # 难度参数
    base_difficulty: int = 50      # 基础难度 (0-100)
    success_rate_base: float = 0.5  # 基础成功率
    
    # 奖励
    cultivation_reward: int = 0     # 修为奖励
    spirit_stone_reward: int = 0    # 灵石奖励
    special_rewards: List[str] = field(default_factory=list)
    
    # 失败惩罚
    cultivation_loss_rate: float = 0.1  # 修为损失比例
    realm_demotion: bool = False         # 是否降级
    karma_penalty: int = 0                # 业力增加
    
    # 前置条件
    cultivation_required: int = 0
    karma_required: int = -100            # 需要的最小功德(-100表示需要功德>业力)


@dataclass
class PreparationItem:
    """渡劫准备物品"""
    item_id: str
    name: str
    preparation_type: PreparationType
    effect_type: str              # 伤害减免、成功率提升、道心保护等
    effect_value: float           # 效果数值
    description: str
    duration: int = 1             # 持续回合
    consumable: bool = True       # 是否消耗品


@dataclass
class TribulationResult:
    """渡劫结果"""
    success: bool
    status: TribulationStatus
    waves_survived: int
    total_damage_taken: int
    rewards: Dict[str, int]
    penalties: Dict[str, int]
    message: str
    special_event: Optional[str] = None


@dataclass
class AscensionReward:
    """飞升奖励"""
    realm: str
    cultivation_bonus: int
    stat_multipliers: Dict[str, float]
    skill_unlocks: List[str]
    special_abilities: List[str]
    title: str


# ==================== 天劫管理器 ====================

class TribulationManager:
    """天劫管理器"""
    
    def __init__(self, data_path: str = "data/tribulations.json"):
        self.data_path = Path(data_path)
        self.tribulations: Dict[str, TribulationConfig] = {}
        self.preparations: Dict[str, PreparationItem] = {}
        self._load_data()
    
    def _load_data(self):
        """加载天劫数据"""
        if not self.data_path.exists():
            self._create_default_data()
            return
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 加载天劫配置
        for t_id, t_data in data.get("tribulations", {}).items():
            waves = []
            for wave_data in t_data.get("waves", []):
                waves.append(TribulationWave(
                    wave_number=wave_data["wave_number"],
                    wave_type=TribulationType(wave_data["wave_type"]),
                    damage=wave_data["damage"],
                    rounds=wave_data.get("rounds", 1),
                    special_effect=wave_data.get("special_effect"),
                    description=wave_data.get("description", "")
                ))
            
            self.tribulations[t_id] = TribulationConfig(
                tribulation_id=t_id,
                name=t_data["name"],
                stage=TribulationStage(t_data["stage"]),
                tier=TribulationTier(t_data["tier"]),
                tribulation_type=TribulationType(t_data["tribulation_type"]),
                description=t_data["description"],
                waves=waves,
                base_difficulty=t_data.get("base_difficulty", 50),
                success_rate_base=t_data.get("success_rate_base", 0.5),
                cultivation_reward=t_data.get("cultivation_reward", 0),
                spirit_stone_reward=t_data.get("spirit_stone_reward", 0),
                special_rewards=t_data.get("special_rewards", []),
                cultivation_loss_rate=t_data.get("cultivation_loss_rate", 0.1),
                realm_demotion=t_data.get("realm_demotion", False),
                karma_penalty=t_data.get("karma_penalty", 0),
                cultivation_required=t_data.get("cultivation_required", 0),
                karma_required=t_data.get("karma_required", -100)
            )
        
        # 加载渡劫准备物品
        for p_id, p_data in data.get("preparations", {}).items():
            self.preparations[p_id] = PreparationItem(
                item_id=p_id,
                name=p_data["name"],
                preparation_type=PreparationType(p_data["preparation_type"]),
                effect_type=p_data["effect_type"],
                effect_value=p_data["effect_value"],
                description=p_data["description"],
                duration=p_data.get("duration", 1),
                consumable=p_data.get("consumable", True)
            )
    
    def _create_default_data(self):
        """创建默认数据"""
        default_data = {
            "tribulations": {},
            "preparations": {}
        }
        
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    def get_tribulation(self, tribulation_id: str) -> Optional[TribulationConfig]:
        """获取天劫配置"""
        return self.tribulations.get(tribulation_id)
    
    def get_tribulations_by_stage(self, stage: TribulationStage) -> List[TribulationConfig]:
        """获取指定境界的天劫"""
        return [t for t in self.tribulations.values() if t.stage == stage]
    
    def get_tribulations_by_type(self, trib_type: TribulationType) -> List[TribulationConfig]:
        """获取指定类型的天劫"""
        return [t for t in self.tribulations.values() if t.tribulation_type == trib_type]
    
    def get_available_preparations(self) -> List[PreparationItem]:
        """获取可用的渡劫准备物品"""
        return list(self.preparations.values())
    
    def get_preparation(self, item_id: str) -> Optional[PreparationItem]:
        """获取渡劫准备物品"""
        return self.preparations.get(item_id)


# ==================== 渡劫系统 ====================

class TribulationSystem:
    """渡劫系统"""
    
    def __init__(self, tribulation_manager: TribulationManager):
        self.manager = tribulation_manager
        self.current_tribulation: Optional[TribulationConfig] = None
        self.current_wave: int = 0
        self.current_round: int = 0  # 当前波次的回合数
        self.preparations_used: List[PreparationItem] = []
        self.status: TribulationStatus = TribulationStatus.PENDING
    
    def can_attempt_tribulation(self, player, tribulation_id: str) -> Tuple[bool, str]:
        """检查是否可以渡劫"""
        trib = self.manager.get_tribulation(tribulation_id)
        if not trib:
            return False, "未知的天劫"
        
        # 检查修为
        if player.cultivation < trib.cultivation_required:
            return False, f"修为不足，需要 {trib.cultivation_required:,} 修为"
        
        # 检查境界
        stage_realm_map = {
            TribulationStage.FOUNDATION: "筑基期",
            TribulationStage.GOLDEN_CORE: "金丹期",
            TribulationStage.NASCENT_SOUL: "元婴期",
            TribulationStage.SPIRIT_SEVERING: "化神期",
            TribulationStage.TRIBULATION: "渡劫期"
        }
        required_realm = stage_realm_map.get(trib.stage)
        if required_realm and player.realm != required_realm:
            return False, f"境界不符，需要达到 {required_realm}"
        
        # 检查功德/业力
        if player.dao_heart:
            karma_diff = player.dao_heart.merit - player.dao_heart.sin
            if karma_diff < trib.karma_required:
                return False, f"功德不足，道心不稳，渡劫必败"
        
        return True, "可以开始渡劫"
    
    def prepare_tribulation(self, preparations: List[PreparationItem]) -> Dict[str, float]:
        """准备渡劫"""
        self.preparations_used = preparations
        
        bonuses = {
            "damage_reduction": 0.0,      # 伤害减免
            "success_rate_bonus": 0.0,    # 成功率加成
            "heart_protection": 0.0,      # 道心保护
            "recovery_bonus": 0.0         # 恢复加成
        }
        
        for prep in preparations:
            if prep.effect_type == "damage_reduction":
                bonuses["damage_reduction"] += prep.effect_value
            elif prep.effect_type == "success_rate":
                bonuses["success_rate_bonus"] += prep.effect_value
            elif prep.effect_type == "heart_protection":
                bonuses["heart_protection"] += prep.effect_value
            elif prep.effect_type == "recovery":
                bonuses["recovery_bonus"] += prep.effect_value
        
        return bonuses
    
    def start_tribulation(self, tribulation_id: str, player) -> Dict:
        """开始渡劫"""
        trib = self.manager.get_tribulation(tribulation_id)
        if not trib:
            return {"success": False, "message": "未知的天劫"}
        
        can_attempt, msg = self.can_attempt_tribulation(player, tribulation_id)
        if not can_attempt:
            return {"success": False, "message": msg}
        
        self.current_tribulation = trib
        self.current_wave = 0
        self.current_round = 0  # 重置回合计数
        self.status = TribulationStatus.IN_PROGRESS
        
        # 初始化第一波的回合数
        if trib.waves:
            self.current_round = trib.waves[0].rounds
        
        return {
            "success": True,
            "message": f"开始渡【{trib.name}】",
            "tribulation": {
                "id": trib.tribulation_id,
                "name": trib.name,
                "type": trib.tribulation_type.value,
                "tier": trib.tier.value,
                "total_waves": len(trib.waves),
                "description": trib.description
            }
        }
    
    def process_wave(self, player, wave_action: str = "defend") -> Dict:
        """处理天劫波次"""
        if not self.current_tribulation or self.status != TribulationStatus.IN_PROGRESS:
            return {"success": False, "message": "当前没有进行中的天劫"}
        
        trib = self.current_tribulation
        wave = trib.waves[self.current_wave]
        
        result = {
            "wave_number": wave.wave_number,
            "wave_type": wave.wave_type.value,
            "action": wave_action,
            "damage": 0,
            "hp_remaining": player.current_hp,
            "special_effect": wave.special_effect,
            "description": wave.description
        }
        
        # 计算伤害
        base_damage = wave.damage
        
        # 根据动作调整伤害
        if wave_action == "defend":
            base_damage = int(base_damage * 0.7)  # 防御减伤30%
        elif wave_action == "dodge":
            # 闪避有概率成功
            dodge_chance = 0.3 + (player.stats.get("身法", 10) / 100)
            if random.random() < dodge_chance:
                base_damage = int(base_damage * 0.3)  # 闪避成功大幅减伤
                result["dodged"] = True
            else:
                result["dodged"] = False
        elif wave_action == "counter":
            # 反击：高风险高回报
            if random.random() < 0.4:
                base_damage = int(base_damage * 1.5)  # 反击失败伤害更高
                result["counter_success"] = False
            else:
                base_damage = int(base_damage * 0.5)  # 反击成功大幅减伤
                result["counter_success"] = True
        
        # 应用准备物品加成
        prep_bonuses = self.prepare_tribulation(self.preparations_used)
        base_damage = int(base_damage * (1 - prep_bonuses["damage_reduction"]))
        
        # 道心保护（心魔劫）
        if wave.wave_type == TribulationType.HEART_DEMON:
            heart_protection = prep_bonuses.get("heart_protection", 0)
            if player.dao_heart:
                dao_bonus = player.dao_heart.merit / 1000  # 功德加成
                heart_protection += dao_bonus
            base_damage = int(base_damage * (1 - min(heart_protection, 0.5)))
        
        # 应用伤害
        player.current_hp -= base_damage
        result["damage"] = base_damage
        result["hp_remaining"] = max(0, player.current_hp)
        
        # 检查是否死亡
        if player.current_hp <= 0:
            return self._fail_tribulation(player, wave.wave_number)
        
        # 处理多回合波次
        self.current_round -= 1
        if self.current_round > 0:
            result["rounds_remaining"] = self.current_round
            return result
        
        # 进入下一波
        self.current_wave += 1
        
        if self.current_wave >= len(trib.waves):
            return self._complete_tribulation(player)
        
        # 重置下一波的回合数
        self.current_round = trib.waves[self.current_wave].rounds
        result["next_wave"] = self.current_wave + 1
        return result
    
    def _complete_tribulation(self, player) -> Dict:
        """完成渡劫"""
        if not self.current_tribulation:
            return {"success": False, "message": "无进行中的天劫"}
        
        trib = self.current_tribulation
        self.status = TribulationStatus.SUCCESS
        
        # 计算奖励
        cultivation_gain = trib.cultivation_reward
        spirit_stone_gain = trib.spirit_stone_reward
        
        # 应用准备物品加成
        prep_bonuses = self.prepare_tribulation(self.preparations_used)
        
        # 道心加成
        if player.dao_heart:
            cultivation_gain = int(cultivation_gain * (1 + player.dao_heart.merit / 100))
        
        # 发放奖励
        player.cultivation += cultivation_gain
        player.spirit_stones += spirit_stone_gain
        
        # 增加功德
        if player.dao_heart:
            from game.dao_heart import ActionType
            player.dao_heart.add_karma(ActionType.TRIBULATION_SUCCESS, f"成功渡过{trib.name}")
        
        # 特殊奖励
        special_rewards = []
        for reward in trib.special_rewards:
            if reward.startswith("skill:"):
                skill_id = reward.split(":")[1]
                result = player.learn_skill(skill_id)
                if result.get("success"):
                    special_rewards.append(f"习得功法：{result['skill'].name}")
            elif reward.startswith("artifact:"):
                artifact_name = reward.split(":")[1]
                player.add_artifact({"name": artifact_name, "type": "法宝", "power": 100})
                special_rewards.append(f"获得法宝：{artifact_name}")
            else:
                special_rewards.append(reward)
        
        return {
            "success": True,
            "status": "success",
            "message": f"🎉 恭喜！成功渡过【{trib.name}】！",
            "rewards": {
                "cultivation": cultivation_gain,
                "spirit_stones": spirit_stone_gain,
                "special": special_rewards
            }
        }
    
    def _fail_tribulation(self, player, wave_number: int) -> Dict:
        """渡劫失败"""
        if not self.current_tribulation:
            return {"success": False, "message": "无进行中的天劫"}
        
        trib = self.current_tribulation
        self.status = TribulationStatus.FAILED
        
        # 计算惩罚
        cultivation_loss = int(player.cultivation * trib.cultivation_loss_rate)
        player.cultivation -= cultivation_loss
        
        # 增加业力
        if player.dao_heart and trib.karma_penalty > 0:
            from game.dao_heart import ActionType, KarmaType
            player.dao_heart.sin += trib.karma_penalty
            player.dao_heart._update_dao_heart_type()
        
        # 境界降级（最严重惩罚）
        realm_demoted = False
        if trib.realm_demotion:
            realm_order = ["练气期", "筑基期", "金丹期", "元婴期", "化神期", "渡劫期"]
            current_idx = realm_order.index(player.realm) if player.realm in realm_order else 0
            if current_idx > 0:
                player.realm = realm_order[current_idx - 1]
                realm_demoted = True
        
        # 恢复一定生命
        player.current_hp = int(player.max_hp * 0.3)
        
        return {
            "success": False,
            "status": "failed",
            "message": f"💀 渡劫失败，在{trib.name}第{wave_number}波陨落...",
            "wave_survived": wave_number,
            "penalties": {
                "cultivation_loss": cultivation_loss,
                "karma_penalty": trib.karma_penalty,
                "realm_demoted": realm_demoted
            }
        }
    
    def get_tribulation_status(self) -> Dict:
        """获取渡劫状态"""
        if not self.current_tribulation:
            return {"status": "no_tribulation"}
        
        trib = self.current_tribulation
        return {
            "status": self.status.value,
            "tribulation": {
                "id": trib.tribulation_id,
                "name": trib.name,
                "type": trib.tribulation_type.value,
                "tier": trib.tier.value
            },
            "current_wave": self.current_wave,
            "total_waves": len(trib.waves),
            "progress": f"{self.current_wave}/{len(trib.waves)}"
        }
    
    def abandon_tribulation(self, player) -> Dict:
        """放弃渡劫"""
        if self.status != TribulationStatus.IN_PROGRESS:
            return {"success": False, "message": "当前没有进行中的天劫"}
        
        trib = self.current_tribulation
        self.status = TribulationStatus.FAILED
        
        # 放弃惩罚较轻
        cultivation_loss = int(player.cultivation * 0.05)
        player.cultivation -= cultivation_loss
        
        self.current_tribulation = None
        self.current_wave = 0
        self.current_round = 0
        self.preparations_used = []
        
        return {
            "success": True,
            "message": f"放弃渡过【{trib.name}】，损失修为 {cultivation_loss}",
            "cultivation_loss": cultivation_loss
        }


# ==================== 飞升系统 ====================

class AscensionSystem:
    """飞升系统"""
    
    # 飞升条件
    ASCENSION_REQUIREMENTS = {
        "cultivation": 10000000,      # 一千万修为
        "realm": "渡劫期",
        "merit": 1000,                # 千功德
        "tribulation_success": True,  # 需渡劫成功
        "title_required": "渡劫仙尊"  # 需要称号
    }
    
    # 飞升奖励
    ASCENSION_REWARDS = {
        "realm": "真仙",
        "cultivation_bonus": 5000000,
        "stat_multipliers": {
            "生命": 2.0,
            "真元": 2.0,
            "攻击": 1.5,
            "防御": 1.5,
            "身法": 1.3
        },
        "skill_unlocks": [
            "immortal_qi",
            "domain_mastery",
            "soul_refinement"
        ],
        "special_abilities": [
            "瞬移",
            "分身术",
            "法相天地"
        ],
        "title": "真仙"
    }
    
    def __init__(self, tribulation_manager: TribulationManager):
        self.manager = tribulation_manager
    
    def check_ascension_requirements(self, player) -> Tuple[bool, List[str]]:
        """检查飞升条件"""
        requirements_met = []
        requirements_failed = []
        
        # 检查修为
        if player.cultivation >= self.ASCENSION_REQUIREMENTS["cultivation"]:
            requirements_met.append(f"✓ 修为达标：{player.cultivation:,}/{self.ASCENSION_REQUIREMENTS['cultivation']:,}")
        else:
            requirements_failed.append(f"✗ 修为不足：{player.cultivation:,}/{self.ASCENSION_REQUIREMENTS['cultivation']:,}")
        
        # 检查境界
        if player.realm == self.ASCENSION_REQUIREMENTS["realm"]:
            requirements_met.append(f"✓ 境界达标：{player.realm}")
        else:
            requirements_failed.append(f"✗ 境界不符：{player.realm}（需要 {self.ASCENSION_REQUIREMENTS['realm']}）")
        
        # 检查功德
        if player.dao_heart:
            if player.dao_heart.merit >= self.ASCENSION_REQUIREMENTS["merit"]:
                requirements_met.append(f"✓ 功德深厚：{player.dao_heart.merit}")
            else:
                requirements_failed.append(f"✗ 功德不足：{player.dao_heart.merit}/{self.ASCENSION_REQUIREMENTS['merit']}")
        
        # 检查渡劫成功（需要渡劫期天劫成功记录）
        trib_id = "tribulation_period_thunder"
        # 这里可以检查玩家是否有渡劫成功的记录
        
        return len(requirements_failed) == 0, requirements_met + requirements_failed
    
    def perform_ascension(self, player) -> Dict:
        """执行飞升仪式"""
        can_ascend, messages = self.check_ascension_requirements(player)
        
        if not can_ascend:
            return {
                "success": False,
                "message": "飞升条件不足",
                "requirements": messages
            }
        
        # 飞升仪式
        rewards = self.ASCENSION_REWARDS
        
        # 更新境界
        old_realm = player.realm
        player.realm = rewards["realm"]
        
        # 发放修为奖励
        player.cultivation += rewards["cultivation_bonus"]
        
        # 提升属性
        for stat, multiplier in rewards["stat_multipliers"].items():
            if stat in player.stats:
                player.stats[stat] = int(player.stats[stat] * multiplier)
        
        # 更新最大生命/真元
        player.max_hp = player.stats["生命"]
        player.max_mp = player.stats["真元"]
        player.current_hp = player.max_hp
        player.current_mp = player.max_mp
        
        # 解锁功法
        unlocked_skills = []
        for skill_id in rewards["skill_unlocks"]:
            result = player.learn_skill(skill_id)
            if result.get("success"):
                unlocked_skills.append(result["skill"].name)
        
        # 检查功德
        merit_before = player.dao_heart.merit if player.dao_heart else 0
        
        return {
            "success": True,
            "message": "🌟 飞升成功！恭喜成为真仙！🌟",
            "ascension_result": {
                "old_realm": old_realm,
                "new_realm": rewards["realm"],
                "cultivation_bonus": rewards["cultivation_bonus"],
                "unlocked_skills": unlocked_skills,
                "special_abilities": rewards["special_abilities"],
                "title": rewards["title"]
            },
            "merit_before": merit_before,
            "merit_after": player.dao_heart.merit if player.dao_heart else 0
        }
    
    def get_ascension_preview(self, player) -> Dict:
        """获取飞升预览"""
        can_ascend, messages = self.check_ascension_requirements(player)
        
        return {
            "can_ascend": can_ascend,
            "requirements": messages,
            "rewards_preview": {
                "new_realm": self.ASCENSION_REWARDS["realm"],
                "cultivation_bonus": self.ASCENSION_REWARDS["cultivation_bonus"],
                "special_abilities": self.ASCENSION_REWARDS["special_abilities"]
            }
        }


# ==================== 辅助函数 ====================

def calculate_success_rate(player, tribulation: TribulationConfig, preparations: List[PreparationItem]) -> float:
    """计算渡劫成功率"""
    base_rate = tribulation.success_rate_base
    
    # 修为加成
    cultivation_ratio = player.cultivation / tribulation.cultivation_required if tribulation.cultivation_required > 0 else 1
    cultivation_bonus = min(0.2, (cultivation_ratio - 1) * 0.1)
    
    # 功德加成
    merit_bonus = 0
    if player.dao_heart:
        karma_diff = player.dao_heart.merit - player.dao_heart.sin
        merit_bonus = min(0.15, karma_diff / 10000)
    
    # 准备物品加成
    prep_bonus = sum(p.effect_value for p in preparations if p.effect_type == "success_rate")
    
    # 法宝加成
    artifact_bonus = 0
    if player.equipped_artifact:
        artifact_bonus = min(0.1, player.equipped_artifact.get("power", 0) / 1000)
    
    # 道心加成
    dao_heart_bonus = 0
    if player.dao_heart and hasattr(player.dao_heart, 'get_tribulation_modifier'):
        mod = player.dao_heart.get_tribulation_modifier()
        dao_heart_bonus = mod.get("success_rate", 0) / 100
    
    total_rate = base_rate + cultivation_bonus + merit_bonus + prep_bonus + artifact_bonus + dao_heart_bonus
    
    return min(0.95, max(0.05, total_rate))


def get_tribulation_description(tribulation: TribulationConfig) -> str:
    """获取天劫描述"""
    desc = f"""
【{tribulation.name}】
类型：{tribulation.tribulation_type.value}
等级：{tribulation.tier.value}
阶段：{tribulation.stage.value}

{tribulation.description}

难度：{'★' * (tribulation.base_difficulty // 20)}
波次：{len(tribulation.waves)} 波
基础成功率：{tribulation.success_rate_base:.0%}

前置条件：
- 修为：{tribulation.cultivation_required:,}
- 功德：{tribulation.karma_required}

奖励：
- 修为：{tribulation.cultivation_reward:,}
- 灵石：{tribulation.spirit_stone_reward:,}

失败惩罚：
- 修为损失：{tribulation.cultivation_loss_rate:.0%}
- 境界降级：{'是' if tribulation.realm_demotion else '否'}
- 业力增加：{tribulation.karma_penalty}
    """.strip()
    
    return desc
