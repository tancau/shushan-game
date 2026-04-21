"""
蜀山剑侠传 - 游戏模块
"""

from .player import Player
from .artifact import Artifact, ArtifactManager
from .combat import CombatSystem, Enemy
from .quest import (
    Quest, QuestManager, QuestObjective, QuestReward, QuestStatus, QuestType,
    ObjectiveType, Dialogue, DialogueChoice, DialogueManager, StoryEngine
)
from .dao_heart import (
    DaoHeart, DaoHeartType, ActionType, KarmaType, KarmaRecord,
    MeritReward, SinPenalty, MeritShop, SinPenaltySystem
)
from .tribulation import (
    TribulationType, TribulationTier, TribulationStage, TribulationStatus,
    PreparationType, TribulationWave, TribulationConfig, PreparationItem,
    TribulationResult, AscensionReward, TribulationManager, TribulationSystem,
    AscensionSystem, calculate_success_rate, get_tribulation_description
)
from .spirit_beast import (
    SpiritBeast, SpiritBeastType, SpiritBeastElement, SpiritBeastSkill,
    SpiritBeastManager, CaptureSystem, TrainingSystem, SpiritBeastCombatSystem
)
from .event import (
    EventType, EventStatus, EventTaskType,
    EventReward, EventTask, RankReward, PointExchange, Event,
    SignInReward, SignInSystem, EventManager
)

__all__ = [
    'Player', 'Artifact', 'ArtifactManager', 'CombatSystem', 'Enemy',
    'Quest', 'QuestManager', 'QuestObjective', 'QuestReward', 'QuestStatus', 'QuestType',
    'ObjectiveType', 'Dialogue', 'DialogueChoice', 'DialogueManager', 'StoryEngine',
    'DaoHeart', 'DaoHeartType', 'ActionType', 'KarmaType', 'KarmaRecord',
    'MeritReward', 'SinPenalty', 'MeritShop', 'SinPenaltySystem',
    # 天劫系统
    'TribulationType', 'TribulationTier', 'TribulationStage', 'TribulationStatus',
    'PreparationType', 'TribulationWave', 'TribulationConfig', 'PreparationItem',
    'TribulationResult', 'AscensionReward', 'TribulationManager', 'TribulationSystem',
    'AscensionSystem', 'calculate_success_rate', 'get_tribulation_description',
    # 灵兽系统
    'SpiritBeast', 'SpiritBeastType', 'SpiritBeastElement', 'SpiritBeastSkill',
    'SpiritBeastManager', 'CaptureSystem', 'TrainingSystem', 'SpiritBeastCombatSystem',
    # 排行榜系统
    'LeaderboardType', 'RewardType', 'LeaderboardReward', 'LeaderboardEntry',
    'RankingTitle', 'Leaderboard', 'LeaderboardManager',
    # 活动系统
    'EventType', 'EventStatus', 'EventTaskType',
    'EventReward', 'EventTask', 'RankReward', 'PointExchange', 'Event',
    'SignInReward', 'SignInSystem', 'EventManager'
]
