#!/usr/bin/env python3
"""
蜀山剑侠传 - 任务系统
包含任务类、目标追踪、奖励发放、剧情对话
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
import json
from pathlib import Path


class QuestType(Enum):
    """任务类型"""
    MAIN = "主线"        # 主线任务
    SIDE = "支线"        # 支线任务
    DAILY = "日常"       # 日常任务
    ENCOUNTER = "奇遇"   # 奇遇任务


class QuestStatus(Enum):
    """任务状态"""
    LOCKED = "未解锁"      # 未解锁（前置任务未完成）
    AVAILABLE = "可接取"   # 可接取
    IN_PROGRESS = "进行中" # 进行中
    COMPLETED = "已完成"   # 已完成
    FAILED = "失败"        # 失败


class ObjectiveType(Enum):
    """目标类型"""
    KILL = "击杀"         # 击杀怪物
    COLLECT = "收集"       # 收集物品
    EXPLORE = "探索"       # 探索地点
    TALK = "对话"         # 对话NPC
    CULTIVATE = "修炼"     # 修炼次数
    BREAKTHROUGH = "突破"  # 突破境界
    OBTAIN_ITEM = "获取"   # 获取物品/法宝
    DEFEAT_BOSS = "挑战"   # 击败BOSS


@dataclass
class QuestObjective:
    """任务目标"""
    objective_type: ObjectiveType
    target: str           # 目标名称（怪物名、物品名、地点名、NPC名等）
    required: int = 1     # 需求数量
    current: int = 0      # 当前进度
    description: str = "" # 目标描述
    
    def is_complete(self) -> bool:
        return self.current >= self.required
    
    def progress_text(self) -> str:
        return f"{self.current}/{self.required}"
    
    def to_dict(self) -> dict:
        return {
            "objective_type": self.objective_type.value,
            "target": self.target,
            "required": self.required,
            "current": self.current,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "QuestObjective":
        return cls(
            objective_type=ObjectiveType(data["objective_type"]),
            target=data["target"],
            required=data.get("required", 1),
            current=data.get("current", 0),
            description=data.get("description", "")
        )


@dataclass
class QuestReward:
    """任务奖励"""
    cultivation: int = 0      # 修为
    spirit_stones: int = 0    # 灵石
    karma: int = 0            # 功德/业力
    artifacts: List[str] = field(default_factory=list)  # 法宝奖励
    skills: List[str] = field(default_factory=list)     # 功法奖励
    items: Dict[str, int] = field(default_factory=dict) # 其他物品
    
    def to_dict(self) -> dict:
        return {
            "cultivation": self.cultivation,
            "spirit_stones": self.spirit_stones,
            "karma": self.karma,
            "artifacts": self.artifacts,
            "skills": self.skills,
            "items": self.items
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "QuestReward":
        return cls(
            cultivation=data.get("cultivation", 0),
            spirit_stones=data.get("spirit_stones", 0),
            karma=data.get("karma", 0),
            artifacts=data.get("artifacts", []),
            skills=data.get("skills", []),
            items=data.get("items", {})
        )


@dataclass
class DialogueChoice:
    """对话选项"""
    text: str                    # 选项文本
    next_dialogue_id: Optional[str] = None  # 下一段对话ID
    effects: Dict[str, Any] = field(default_factory=dict)  # 选择效果
    karma_change: int = 0        # 功德变化
    required_karma: int = 0      # 需要的功德值（正=正道，负=魔道）
    
    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "next_dialogue_id": self.next_dialogue_id,
            "effects": self.effects,
            "karma_change": self.karma_change,
            "required_karma": self.required_karma
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DialogueChoice":
        return cls(
            text=data["text"],
            next_dialogue_id=data.get("next_dialogue_id"),
            effects=data.get("effects", {}),
            karma_change=data.get("karma_change", 0),
            required_karma=data.get("required_karma", 0)
        )


@dataclass
class Dialogue:
    """对话"""
    dialogue_id: str
    speaker: str              # 说话者
    text: str                 # 对话内容
    choices: List[DialogueChoice] = field(default_factory=list)  # 选项
    next_dialogue_id: Optional[str] = None  # 无选项时的下一段对话
    
    def to_dict(self) -> dict:
        return {
            "dialogue_id": self.dialogue_id,
            "speaker": self.speaker,
            "text": self.text,
            "choices": [c.to_dict() for c in self.choices],
            "next_dialogue_id": self.next_dialogue_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Dialogue":
        return cls(
            dialogue_id=data["dialogue_id"],
            speaker=data["speaker"],
            text=data["text"],
            choices=[DialogueChoice.from_dict(c) for c in data.get("choices", [])],
            next_dialogue_id=data.get("next_dialogue_id")
        )


@dataclass
class Quest:
    """任务"""
    quest_id: str
    name: str
    description: str
    quest_type: QuestType
    objectives: List[QuestObjective]
    rewards: QuestReward
    prerequisites: List[str] = field(default_factory=list)  # 前置任务ID
    status: QuestStatus = QuestStatus.LOCKED
    giver_npc: str = ""       # 任务发布者
    completer_npc: str = ""   # 任务完成者（提交NPC）
    dialogues: List[Dialogue] = field(default_factory=list)  # 任务对话
    current_dialogue_id: Optional[str] = None  # 当前对话ID
    story_chapter: int = 0    # 剧情章节
    time_limit: int = 0       # 时间限制（分钟），0表示无限制
    
    def is_available(self, completed_quests: List[str]) -> bool:
        """检查任务是否可接取"""
        return all(pre in completed_quests for pre in self.prerequisites)
    
    def is_complete(self) -> bool:
        """检查任务是否完成"""
        return all(obj.is_complete() for obj in self.objectives)
    
    def update_objective(self, objective_type: ObjectiveType, target: str, amount: int = 1) -> bool:
        """更新任务目标进度"""
        updated = False
        for obj in self.objectives:
            if obj.objective_type == objective_type and obj.target == target:
                obj.current = min(obj.current + amount, obj.required)
                updated = True
        return updated
    
    def get_progress(self) -> str:
        """获取任务进度描述"""
        lines = []
        for obj in self.objectives:
            status = "✓" if obj.is_complete() else "○"
            desc = obj.description or f"{obj.objective_type.value}{obj.target}"
            lines.append(f"  {status} {desc}: {obj.progress_text()}")
        return "\n".join(lines)
    
    def get_start_dialogue(self) -> Optional[Dialogue]:
        """获取任务开始对话"""
        if self.dialogues:
            return self.dialogues[0]
        return None
    
    def get_dialogue(self, dialogue_id: str) -> Optional[Dialogue]:
        """获取指定对话"""
        for d in self.dialogues:
            if d.dialogue_id == dialogue_id:
                return d
        return None
    
    def to_dict(self) -> dict:
        return {
            "quest_id": self.quest_id,
            "name": self.name,
            "description": self.description,
            "quest_type": self.quest_type.value,
            "objectives": [obj.to_dict() for obj in self.objectives],
            "rewards": self.rewards.to_dict(),
            "prerequisites": self.prerequisites,
            "status": self.status.value,
            "giver_npc": self.giver_npc,
            "completer_npc": self.completer_npc,
            "dialogues": [d.to_dict() for d in self.dialogues],
            "current_dialogue_id": self.current_dialogue_id,
            "story_chapter": self.story_chapter,
            "time_limit": self.time_limit
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Quest":
        return cls(
            quest_id=data["quest_id"],
            name=data["name"],
            description=data["description"],
            quest_type=QuestType(data["quest_type"]),
            objectives=[QuestObjective.from_dict(obj) for obj in data["objectives"]],
            rewards=QuestReward.from_dict(data["rewards"]),
            prerequisites=data.get("prerequisites", []),
            status=QuestStatus(data.get("status", "未解锁")),
            giver_npc=data.get("giver_npc", ""),
            completer_npc=data.get("completer_npc", ""),
            dialogues=[Dialogue.from_dict(d) for d in data.get("dialogues", [])],
            current_dialogue_id=data.get("current_dialogue_id"),
            story_chapter=data.get("story_chapter", 0),
            time_limit=data.get("time_limit", 0)
        )


class QuestManager:
    """任务管理器"""
    
    def __init__(self, data_path: str = None):
        self.quests: Dict[str, Quest] = {}
        self.active_quests: Dict[str, Quest] = {}
        self.completed_quests: List[str] = []
        self.data_path = data_path or "data/quests.json"
        
        # 任务完成回调
        self.on_quest_complete: Optional[Callable] = None
        
        # 加载任务数据
        self.load_quests()
    
    def load_quests(self):
        """从JSON加载任务数据"""
        quest_file = Path(self.data_path)
        if not quest_file.exists():
            return
        
        with open(quest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for quest_data in data.get("quests", []):
            quest = Quest.from_dict(quest_data)
            self.quests[quest.quest_id] = quest
    
    def save_quests(self):
        """保存任务数据（用于存档）"""
        data = {
            "quests": [q.to_dict() for q in self.quests.values()],
            "active_quests": list(self.active_quests.keys()),
            "completed_quests": self.completed_quests
        }
        return data
    
    def load_state(self, data: dict):
        """加载任务状态（用于读档）"""
        self.completed_quests = data.get("completed_quests", [])
        self.active_quests = {}
        
        for quest_id in data.get("active_quests", []):
            if quest_id in self.quests:
                self.active_quests[quest_id] = self.quests[quest_id]
    
    def get_available_quests(self) -> List[Quest]:
        """获取可接取的任务"""
        available = []
        for quest in self.quests.values():
            if quest.quest_id not in self.completed_quests:
                if quest.quest_id not in self.active_quests:
                    if quest.is_available(self.completed_quests):
                        quest.status = QuestStatus.AVAILABLE
                        available.append(quest)
        return available
    
    def get_active_quests(self) -> List[Quest]:
        """获取进行中的任务"""
        return list(self.active_quests.values())
    
    def get_quest_by_npc(self, npc_name: str) -> List[Quest]:
        """获取NPC可发布的任务"""
        return [
            q for q in self.get_available_quests()
            if q.giver_npc == npc_name
        ]
    
    def accept_quest(self, quest_id: str) -> dict:
        """接取任务"""
        if quest_id not in self.quests:
            return {"success": False, "message": "任务不存在"}
        
        if quest_id in self.active_quests:
            return {"success": False, "message": "任务已接取"}
        
        if quest_id in self.completed_quests:
            return {"success": False, "message": "任务已完成"}
        
        quest = self.quests[quest_id]
        
        if not quest.is_available(self.completed_quests):
            return {"success": False, "message": "前置任务未完成"}
        
        quest.status = QuestStatus.IN_PROGRESS
        self.active_quests[quest_id] = quest
        
        # 获取开始对话
        start_dialogue = quest.get_start_dialogue()
        
        return {
            "success": True,
            "message": f"接取任务：{quest.name}",
            "quest": quest,
            "dialogue": start_dialogue
        }
    
    def update_objective(self, objective_type: ObjectiveType, target: str, amount: int = 1) -> List[dict]:
        """更新所有进行中任务的目标进度"""
        updates = []
        for quest in self.active_quests.values():
            if quest.update_objective(objective_type, target, amount):
                updates.append({
                    "quest_id": quest.quest_id,
                    "quest_name": quest.name,
                    "progress": quest.get_progress()
                })
                
                # 检查任务是否完成
                if quest.is_complete():
                    updates.append({
                        "quest_id": quest.quest_id,
                        "quest_name": quest.name,
                        "complete": True,
                        "message": f"任务「{quest.name}」目标已达成，可去提交！"
                    })
        
        return updates
    
    def complete_quest(self, quest_id: str, player) -> dict:
        """完成任务并发放奖励"""
        if quest_id not in self.active_quests:
            return {"success": False, "message": "任务未接取"}
        
        quest = self.active_quests[quest_id]
        
        if not quest.is_complete():
            return {"success": False, "message": "任务目标未完成"}
        
        # 发放奖励
        rewards = quest.rewards
        reward_text = []
        
        if rewards.cultivation > 0:
            player.cultivation += rewards.cultivation
            reward_text.append(f"修为 +{rewards.cultivation}")
        
        if rewards.spirit_stones > 0:
            player.spirit_stones += rewards.spirit_stones
            reward_text.append(f"灵石 +{rewards.spirit_stones}")
        
        if rewards.karma != 0:
            player.karma += rewards.karma
            karma_desc = "功德" if rewards.karma > 0 else "业力"
            reward_text.append(f"{karma_desc} +{abs(rewards.karma)}")
        
        for artifact_name in rewards.artifacts:
            player.artifacts.append({"name": artifact_name, "level": 1, "type": "法宝"})
            reward_text.append(f"获得法宝「{artifact_name}」")
        
        for skill_name in rewards.skills:
            if skill_name not in player.skills:
                player.skills.append(skill_name)
                reward_text.append(f"学会功法「{skill_name}」")
        
        # 更新状态
        quest.status = QuestStatus.COMPLETED
        self.completed_quests.append(quest_id)
        del self.active_quests[quest_id]
        
        # 解锁后续任务
        unlocked = self._unlock_following_quests(quest_id)
        
        result = {
            "success": True,
            "message": f"完成任务「{quest.name}」！",
            "rewards": reward_text,
            "unlocked_quests": unlocked
        }
        
        # 回调
        if self.on_quest_complete:
            self.on_quest_complete(quest, player)
        
        return result
    
    def _unlock_following_quests(self, completed_quest_id: str) -> List[str]:
        """解锁后续任务"""
        unlocked = []
        for quest in self.quests.values():
            if completed_quest_id in quest.prerequisites:
                if quest.quest_id not in self.completed_quests:
                    if quest.quest_id not in self.active_quests:
                        if quest.is_available(self.completed_quests):
                            quest.status = QuestStatus.AVAILABLE
                            unlocked.append(quest.name)
        return unlocked
    
    def abandon_quest(self, quest_id: str) -> dict:
        """放弃任务"""
        if quest_id not in self.active_quests:
            return {"success": False, "message": "任务未接取"}
        
        quest = self.active_quests[quest_id]
        
        # 重置任务进度
        for obj in quest.objectives:
            obj.current = 0
        
        quest.status = QuestStatus.AVAILABLE
        del self.active_quests[quest_id]
        
        return {"success": True, "message": f"已放弃任务「{quest.name}」"}
    
    def get_quest_info(self, quest_id: str) -> Optional[Quest]:
        """获取任务详情"""
        return self.quests.get(quest_id)
    
    def get_daily_quests(self) -> List[Quest]:
        """获取日常任务列表"""
        return [
            q for q in self.quests.values()
            if q.quest_type == QuestType.DAILY
            and q.quest_id not in self.completed_quests
        ]
    
    def reset_daily_quests(self):
        """重置日常任务（每日刷新）"""
        for quest in self.quests.values():
            if quest.quest_type == QuestType.DAILY:
                if quest.quest_id in self.completed_quests:
                    self.completed_quests.remove(quest.quest_id)
                quest.status = QuestStatus.AVAILABLE
                for obj in quest.objectives:
                    obj.current = 0
    
    def get_story_progress(self) -> dict:
        """获取剧情进度"""
        main_quests = [
            q for q in self.quests.values()
            if q.quest_type == QuestType.MAIN
        ]
        
        completed_main = [
            q for q in main_quests
            if q.quest_id in self.completed_quests
        ]
        
        return {
            "total_main_quests": len(main_quests),
            "completed_main_quests": len(completed_main),
            "current_chapter": max((q.story_chapter for q in completed_main), default=0),
            "total_quests": len(self.quests),
            "completed_quests": len(self.completed_quests)
        }


class DialogueManager:
    """对话管理器"""
    
    def __init__(self):
        self.current_dialogue: Optional[Dialogue] = None
        self.dialogue_history: List[str] = []
        self.choices_made: List[Dict] = []
    
    def start_dialogue(self, dialogue: Dialogue) -> dict:
        """开始对话"""
        self.current_dialogue = dialogue
        self.dialogue_history.append(dialogue.dialogue_id)
        
        return {
            "speaker": dialogue.speaker,
            "text": dialogue.text,
            "choices": [
                {
                    "index": i,
                    "text": choice.text,
                    "available": True  # 可以添加条件检查
                }
                for i, choice in enumerate(dialogue.choices)
            ] if dialogue.choices else None
        }
    
    def make_choice(self, choice_index: int, player_karma: int = 0) -> dict:
        """做出对话选择"""
        if not self.current_dialogue or not self.current_dialogue.choices:
            return {"success": False, "message": "无可选选项"}
        
        if choice_index >= len(self.current_dialogue.choices):
            return {"success": False, "message": "无效选项"}
        
        choice = self.current_dialogue.choices[choice_index]
        
        # 检查功德要求
        if choice.required_karma > 0 and player_karma < choice.required_karma:
            return {"success": False, "message": "功德不足，无法选择此选项"}
        if choice.required_karma < 0 and player_karma > choice.required_karma:
            return {"success": False, "message": "业力不足，无法选择此选项"}
        
        # 记录选择
        self.choices_made.append({
            "dialogue_id": self.current_dialogue.dialogue_id,
            "choice_index": choice_index,
            "choice_text": choice.text,
            "karma_change": choice.karma_change
        })
        
        # 处理效果
        effects = choice.effects
        
        # 移动到下一段对话
        if choice.next_dialogue_id:
            return {
                "success": True,
                "effects": effects,
                "karma_change": choice.karma_change,
                "next_dialogue_id": choice.next_dialogue_id
            }
        elif self.current_dialogue.next_dialogue_id:
            return {
                "success": True,
                "effects": effects,
                "karma_change": choice.karma_change,
                "next_dialogue_id": self.current_dialogue.next_dialogue_id
            }
        else:
            # 对话结束
            return {
                "success": True,
                "effects": effects,
                "karma_change": choice.karma_change,
                "dialogue_end": True
            }
    
    def continue_dialogue(self, next_id: str = None) -> dict:
        """继续对话"""
        if next_id:
            # 需要从任务或全局对话中获取
            return {"next_dialogue_id": next_id}
        elif self.current_dialogue and self.current_dialogue.next_dialogue_id:
            return {"next_dialogue_id": self.current_dialogue.next_dialogue_id}
        else:
            return {"dialogue_end": True}
    
    def end_dialogue(self):
        """结束对话"""
        self.current_dialogue = None
    
    def get_karma_changes(self) -> int:
        """获取本次对话的总功德变化"""
        return sum(c["karma_change"] for c in self.choices_made)
    
    def to_dict(self) -> dict:
        """保存状态"""
        return {
            "dialogue_history": self.dialogue_history,
            "choices_made": self.choices_made
        }
    
    def from_dict(self, data: dict):
        """加载状态"""
        self.dialogue_history = data.get("dialogue_history", [])
        self.choices_made = data.get("choices_made", [])


class StoryEngine:
    """剧情引擎"""
    
    def __init__(self, quest_manager: QuestManager):
        self.quest_manager = quest_manager
        self.dialogue_manager = DialogueManager()
        self.story_flags: Dict[str, Any] = {}  # 剧情标记
        self.player_choices: Dict[str, int] = {}  # 玩家关键选择
    
    def set_flag(self, flag_name: str, value: Any):
        """设置剧情标记"""
        self.story_flags[flag_name] = value
    
    def get_flag(self, flag_name: str, default: Any = None) -> Any:
        """获取剧情标记"""
        return self.story_flags.get(flag_name, default)
    
    def record_choice(self, choice_id: str, choice_value: int):
        """记录关键选择（影响结局）"""
        self.player_choices[choice_id] = choice_value
    
    def get_ending(self) -> str:
        """根据选择计算结局"""
        karma = sum(self.player_choices.values())
        
        if karma >= 100:
            return "正道飞升"
        elif karma <= -100:
            return "魔道称霸"
        elif karma >= 50:
            return "剑仙证道"
        elif karma <= -50:
            return "血魔降世"
        else:
            return "逍遥散仙"
    
    def process_dialogue_choice(self, quest: Quest, choice_index: int, player) -> dict:
        """处理任务对话选择"""
        if not self.dialogue_manager.current_dialogue:
            return {"success": False, "message": "无进行中的对话"}
        
        result = self.dialogue_manager.make_choice(choice_index, player.karma)
        
        if result.get("success"):
            # 应用功德变化
            if result.get("karma_change"):
                player.karma += result["karma_change"]
            
            # 应用效果
            effects = result.get("effects", {})
            for key, value in effects.items():
                if key == "set_flag":
                    for flag_name, flag_value in value.items():
                        self.set_flag(flag_name, flag_value)
                elif key == "give_item":
                    # 给予物品
                    pass
            
            # 记录关键选择
            if "choice_id" in effects:
                self.record_choice(effects["choice_id"], result.get("karma_change", 0))
        
        return result
    
    def to_dict(self) -> dict:
        """保存状态"""
        return {
            "story_flags": self.story_flags,
            "player_choices": self.player_choices,
            "dialogue_state": self.dialogue_manager.to_dict()
        }
    
    def from_dict(self, data: dict):
        """加载状态"""
        self.story_flags = data.get("story_flags", {})
        self.player_choices = data.get("player_choices", {})
        self.dialogue_manager.from_dict(data.get("dialogue_state", {}))
