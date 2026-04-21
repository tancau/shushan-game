#!/usr/bin/env python3
"""
蜀山剑侠传 - 好友系统
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, field


class FriendshipLevel(Enum):
    """好感度等级"""
    STRANGER = "陌生人"
    ACQUAINTANCE = "点头之交"
    FRIEND = "好友"
    CLOSE_FRIEND = "挚友"
    CONFIDANT = "知己"
    SWORN_SIBLING = "结拜兄弟"


class GiftType(Enum):
    """礼物类型"""
    SPIRIT_STONES = "灵石"
    MATERIAL = "材料"
    ARTIFACT = "法宝"
    PILL = "丹药"
    SKILL_BOOK = "功法秘籍"


class MessageType(Enum):
    """消息类型"""
    TEXT = "文字"
    SYSTEM = "系统通知"
    GIFT = "礼物"
    CHALLENGE = "切磋邀请"
    FRIEND_REQUEST = "好友申请"


@dataclass
class Interaction:
    """互动记录"""
    interaction_type: str
    timestamp: str
    description: str
    favor_change: int = 0


@dataclass
class Friend:
    """好友数据结构"""
    friend_id: str
    name: str
    realm: str = "练气期"
    sect: Optional[str] = None
    favorability: int = 0  # 好感度 0-1000
    interactions: List[Interaction] = field(default_factory=list)
    gifts_sent: int = 0
    gifts_received: int = 0
    battles_won: int = 0
    battles_lost: int = 0
    last_interaction: Optional[str] = None
    added_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def get_friendship_level(self) -> FriendshipLevel:
        """获取好感度等级"""
        if self.favorability < 100:
            return FriendshipLevel.STRANGER
        elif self.favorability < 300:
            return FriendshipLevel.ACQUAINTANCE
        elif self.favorability < 500:
            return FriendshipLevel.FRIEND
        elif self.favorability < 700:
            return FriendshipLevel.CLOSE_FRIEND
        elif self.favorability < 900:
            return FriendshipLevel.CONFIDANT
        else:
            return FriendshipLevel.SWORN_SIBLING
    
    def get_level_bonus(self) -> Dict[str, float]:
        """获取好感度加成"""
        level = self.get_friendship_level()
        bonuses = {
            FriendshipLevel.STRANGER: {"gift_bonus": 0, "battle_bonus": 0},
            FriendshipLevel.ACQUAINTANCE: {"gift_bonus": 0.05, "battle_bonus": 0},
            FriendshipLevel.FRIEND: {"gift_bonus": 0.1, "battle_bonus": 0.05},
            FriendshipLevel.CLOSE_FRIEND: {"gift_bonus": 0.15, "battle_bonus": 0.1},
            FriendshipLevel.CONFIDANT: {"gift_bonus": 0.2, "battle_bonus": 0.15},
            FriendshipLevel.SWORN_SIBLING: {"gift_bonus": 0.3, "battle_bonus": 0.25},
        }
        return bonuses.get(level, {"gift_bonus": 0, "battle_bonus": 0})
    
    def add_interaction(self, interaction_type: str, description: str, favor_change: int = 0):
        """添加互动记录"""
        interaction = Interaction(
            interaction_type=interaction_type,
            timestamp=datetime.now().isoformat(),
            description=description,
            favor_change=favor_change
        )
        self.interactions.append(interaction)
        self.favorability = max(0, min(1000, self.favorability + favor_change))
        self.last_interaction = interaction.timestamp
    
    def get_recent_interactions(self, limit: int = 10) -> List[Dict]:
        """获取最近互动记录"""
        recent = self.interactions[-limit:] if self.interactions else []
        return [
            {
                "type": i.interaction_type,
                "time": i.timestamp,
                "desc": i.description,
                "favor": i.favor_change
            }
            for i in recent
        ]
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "friend_id": self.friend_id,
            "name": self.name,
            "realm": self.realm,
            "sect": self.sect,
            "favorability": self.favorability,
            "interactions": [
                {
                    "type": i.interaction_type,
                    "timestamp": i.timestamp,
                    "description": i.description,
                    "favor_change": i.favor_change
                }
                for i in self.interactions
            ],
            "gifts_sent": self.gifts_sent,
            "gifts_received": self.gifts_received,
            "battles_won": self.battles_won,
            "battles_lost": self.battles_lost,
            "last_interaction": self.last_interaction,
            "added_at": self.added_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Friend":
        """从字典创建"""
        friend = cls(
            friend_id=data["friend_id"],
            name=data["name"],
            realm=data.get("realm", "练气期"),
            sect=data.get("sect"),
            favorability=data.get("favorability", 0),
            gifts_sent=data.get("gifts_sent", 0),
            gifts_received=data.get("gifts_received", 0),
            battles_won=data.get("battles_won", 0),
            battles_lost=data.get("battles_lost", 0),
            last_interaction=data.get("last_interaction"),
            added_at=data.get("added_at", datetime.now().isoformat())
        )
        
        # 恢复互动记录
        for i in data.get("interactions", []):
            interaction = Interaction(
                interaction_type=i["type"],
                timestamp=i["timestamp"],
                description=i["description"],
                favor_change=i.get("favor_change", 0)
            )
            friend.interactions.append(interaction)
        
        return friend


@dataclass
class FriendRequest:
    """好友申请"""
    request_id: str
    sender_id: str
    sender_name: str
    sender_realm: str
    sender_sect: Optional[str]
    message: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "sender_realm": self.sender_realm,
            "sender_sect": self.sender_sect,
            "message": self.message,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FriendRequest":
        return cls(
            request_id=data["request_id"],
            sender_id=data["sender_id"],
            sender_name=data["sender_name"],
            sender_realm=data.get("sender_realm", "练气期"),
            sender_sect=data.get("sender_sect"),
            message=data.get("message", ""),
            created_at=data.get("created_at", datetime.now().isoformat())
        )


@dataclass
class ChatMessage:
    """聊天消息"""
    message_id: str
    sender_id: str
    sender_name: str
    content: str
    message_type: MessageType = MessageType.TEXT
    is_read: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "content": self.content,
            "message_type": self.message_type.value,
            "is_read": self.is_read,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        return cls(
            message_id=data["message_id"],
            sender_id=data["sender_id"],
            sender_name=data["sender_name"],
            content=data["content"],
            message_type=MessageType(data.get("message_type", "文字")),
            is_read=data.get("is_read", False),
            created_at=data.get("created_at", datetime.now().isoformat())
        )


@dataclass
class Gift:
    """礼物"""
    gift_id: str
    gift_type: GiftType
    name: str
    value: int  # 价值（灵石）
    quantity: int = 1
    favor_bonus: int = 0  # 赠送获得的好感度
    description: str = ""
    
    def to_dict(self) -> dict:
        return {
            "gift_id": self.gift_id,
            "gift_type": self.gift_type.value,
            "name": self.name,
            "value": self.value,
            "quantity": self.quantity,
            "favor_bonus": self.favor_bonus,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Gift":
        return cls(
            gift_id=data["gift_id"],
            gift_type=GiftType(data.get("gift_type", "灵石")),
            name=data["name"],
            value=data["value"],
            quantity=data.get("quantity", 1),
            favor_bonus=data.get("favor_bonus", 0),
            description=data.get("description", "")
        )


# 预定义礼物列表
DEFAULT_GIFTS = [
    {"gift_id": "spirit_stone_small", "gift_type": GiftType.SPIRIT_STONES, "name": "灵石(小)", "value": 100, "favor_bonus": 5},
    {"gift_id": "spirit_stone_medium", "gift_type": GiftType.SPIRIT_STONES, "name": "灵石(中)", "value": 500, "favor_bonus": 20},
    {"gift_id": "spirit_stone_large", "gift_type": GiftType.SPIRIT_STONES, "name": "灵石(大)", "value": 1000, "favor_bonus": 40},
    {"gift_id": "spirit_herb", "gift_type": GiftType.MATERIAL, "name": "灵草", "value": 200, "favor_bonus": 10},
    {"gift_id": "spirit_ore", "gift_type": GiftType.MATERIAL, "name": "灵矿", "value": 300, "favor_bonus": 15},
    {"gift_id": "heaven_material", "gift_type": GiftType.MATERIAL, "name": "天材地宝", "value": 800, "favor_bonus": 35},
    {"gift_id": "qi_pill", "gift_type": GiftType.PILL, "name": "聚气丹", "value": 400, "favor_bonus": 18},
    {"gift_id": "spirit_pill", "gift_type": GiftType.PILL, "name": "灵韵丹", "value": 600, "favor_bonus": 25},
    {"gift_id": "immortal_pill", "gift_type": GiftType.PILL, "name": "仙灵丹", "value": 1500, "favor_bonus": 60},
    {"gift_id": "basic_skill_book", "gift_type": GiftType.SKILL_BOOK, "name": "基础功法", "value": 500, "favor_bonus": 22},
    {"gift_id": "advanced_skill_book", "gift_type": GiftType.SKILL_BOOK, "name": "进阶功法", "value": 2000, "favor_bonus": 80},
]


class FriendManager:
    """好友管理器"""
    
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.friends: Dict[str, Friend] = {}  # friend_id -> Friend
        self.friend_requests: List[FriendRequest] = []  # 待处理的好友申请
        self.messages: Dict[str, List[ChatMessage]] = {}  # friend_id -> messages
        self.max_friends = 50
        self.max_requests = 20
    
    # ==================== 好友管理 ====================
    
    def add_friend(self, friend_id: str, name: str, realm: str = "练气期", 
                   sect: Optional[str] = None) -> dict:
        """添加好友"""
        if len(self.friends) >= self.max_friends:
            return {"success": False, "message": f"好友数量已达上限({self.max_friends})"}
        
        if friend_id in self.friends:
            return {"success": False, "message": "该玩家已在好友列表中"}
        
        friend = Friend(
            friend_id=friend_id,
            name=name,
            realm=realm,
            sect=sect,
            favorability=10  # 初始好感度
        )
        friend.add_interaction("add_friend", f"与{name}结为好友", 10)
        
        self.friends[friend_id] = friend
        self.messages[friend_id] = []
        
        return {
            "success": True,
            "message": f"成功添加好友【{name}】",
            "friend": friend
        }
    
    def remove_friend(self, friend_id: str) -> dict:
        """删除好友"""
        if friend_id not in self.friends:
            return {"success": False, "message": "该玩家不在好友列表中"}
        
        friend = self.friends[friend_id]
        del self.friends[friend_id]
        
        if friend_id in self.messages:
            del self.messages[friend_id]
        
        return {
            "success": True,
            "message": f"已将【{friend.name}】从好友列表移除"
        }
    
    def get_friend(self, friend_id: str) -> Optional[Friend]:
        """获取好友信息"""
        return self.friends.get(friend_id)
    
    def get_all_friends(self) -> List[Friend]:
        """获取所有好友"""
        return list(self.friends.values())
    
    def get_friends_by_level(self, level: FriendshipLevel) -> List[Friend]:
        """按好感度等级筛选好友"""
        return [f for f in self.friends.values() if f.get_friendship_level() == level]
    
    def get_friend_summary(self) -> str:
        """获取好友概要"""
        if not self.friends:
            return "暂无好友"
        
        summary = f"【好友列表】({len(self.friends)}/{self.max_friends})\n"
        summary += "─" * 30 + "\n"
        
        # 按好感度排序
        sorted_friends = sorted(self.friends.values(), key=lambda f: f.favorability, reverse=True)
        
        for friend in sorted_friends[:10]:  # 显示前10个
            level = friend.get_friendship_level()
            summary += f"• {friend.name} [{friend.realm}] {level.value}\n"
            summary += f"  好感度: {friend.favorability}/1000\n"
        
        if len(self.friends) > 10:
            summary += f"\n... 还有 {len(self.friends) - 10} 位好友\n"
        
        # 统计好感度等级分布
        level_counts = {}
        for friend in self.friends.values():
            level = friend.get_friendship_level()
            level_counts[level.value] = level_counts.get(level.value, 0) + 1
        
        summary += "\n【好感度分布】\n"
        for level_name, count in level_counts.items():
            summary += f"  {level_name}: {count}人\n"
        
        return summary
    
    # ==================== 好友申请 ====================
    
    def send_friend_request(self, sender_id: str, sender_name: str, 
                            sender_realm: str = "练气期",
                            sender_sect: Optional[str] = None,
                            message: str = "") -> dict:
        """发送好友申请（模拟其他玩家向自己申请）"""
        if len(self.friend_requests) >= self.max_requests:
            return {"success": False, "message": "好友申请列表已满"}
        
        if sender_id in self.friends:
            return {"success": False, "message": "已是好友"}
        
        # 检查是否已有待处理的申请
        for req in self.friend_requests:
            if req.sender_id == sender_id:
                return {"success": False, "message": "已有待处理的好友申请"}
        
        request = FriendRequest(
            request_id=f"req_{sender_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            sender_id=sender_id,
            sender_name=sender_name,
            sender_realm=sender_realm,
            sender_sect=sender_sect,
            message=message
        )
        
        self.friend_requests.append(request)
        
        # 添加系统消息
        self.add_system_message(f"【{sender_name}】向你发送了好友申请")
        
        return {
            "success": True,
            "message": f"已收到【{sender_name}】的好友申请",
            "request": request
        }
    
    def accept_friend_request(self, request_id: str) -> dict:
        """接受好友申请"""
        request = None
        for i, req in enumerate(self.friend_requests):
            if req.request_id == request_id:
                request = self.friend_requests.pop(i)
                break
        
        if not request:
            return {"success": False, "message": "好友申请不存在或已处理"}
        
        result = self.add_friend(
            friend_id=request.sender_id,
            name=request.sender_name,
            realm=request.sender_realm,
            sect=request.sender_sect
        )
        
        if result["success"]:
            self.add_system_message(f"你与【{request.sender_name}】成为好友")
        
        return result
    
    def reject_friend_request(self, request_id: str) -> dict:
        """拒绝好友申请"""
        for i, req in enumerate(self.friend_requests):
            if req.request_id == request_id:
                rejected = self.friend_requests.pop(i)
                return {
                    "success": True,
                    "message": f"已拒绝【{rejected.sender_name}】的好友申请"
                }
        
        return {"success": False, "message": "好友申请不存在或已处理"}
    
    def get_pending_requests(self) -> List[FriendRequest]:
        """获取待处理的好友申请"""
        return self.friend_requests.copy()
    
    # ==================== 赠送系统 ====================
    
    def get_available_gifts(self) -> List[Gift]:
        """获取可赠送的礼物列表"""
        return [Gift.from_dict(g) for g in DEFAULT_GIFTS]
    
    def send_gift(self, friend_id: str, gift: Gift, player_spirit_stones: int) -> dict:
        """赠送礼物"""
        if friend_id not in self.friends:
            return {"success": False, "message": "该玩家不在好友列表中"}
        
        friend = self.friends[friend_id]
        
        # 计算花费
        total_cost = gift.value * gift.quantity
        
        if player_spirit_stones < total_cost:
            return {"success": False, "message": f"灵石不足，需要 {total_cost} 灵石"}
        
        # 计算好感度加成
        level_bonus = friend.get_level_bonus()
        actual_favor = int(gift.favor_bonus * gift.quantity * (1 + level_bonus["gift_bonus"]))
        
        # 更新好友信息
        friend.gifts_sent += 1
        friend.add_interaction("send_gift", f"赠送了{gift.name}x{gift.quantity}", actual_favor)
        
        # 添加聊天消息
        self.send_message(
            friend_id,
            f"我送了你一份礼物：{gift.name}x{gift.quantity}",
            MessageType.GIFT
        )
        
        return {
            "success": True,
            "message": f"成功向【{friend.name}】赠送{gift.name}x{gift.quantity}",
            "cost": total_cost,
            "favor_gained": actual_favor,
            "new_favorability": friend.favorability
        }
    
    def receive_gift(self, friend_id: str, gift: Gift) -> dict:
        """收到礼物（模拟好友赠送）"""
        if friend_id not in self.friends:
            return {"success": False, "message": "该玩家不在好友列表中"}
        
        friend = self.friends[friend_id]
        friend.gifts_received += 1
        
        # 添加聊天消息
        self.messages[friend_id].append(ChatMessage(
            message_id=f"msg_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            sender_id=friend_id,
            sender_name=friend.name,
            content=f"送了你一份礼物：{gift.name}x{gift.quantity}",
            message_type=MessageType.GIFT
        ))
        
        return {
            "success": True,
            "message": f"收到【{friend.name}】赠送的{gift.name}x{gift.quantity}",
            "gift": gift
        }
    
    # ==================== 切磋系统 ====================
    
    def challenge_friend(self, friend_id: str, player_power: int) -> dict:
        """与好友切磋"""
        if friend_id not in self.friends:
            return {"success": False, "message": "该玩家不在好友列表中"}
        
        friend = self.friends[friend_id]
        
        # 模拟好友战力（基于境界）
        realm_powers = {
            "练气期": 100,
            "筑基期": 300,
            "金丹期": 800,
            "元婴期": 2000,
            "化神期": 5000,
            "合体期": 12000,
            "大乘期": 30000,
            "渡劫期": 80000,
            "真仙": 200000,
        }
        friend_power = realm_powers.get(friend.realm, 100) * (1 + friend.favorability / 1000)
        
        # 添加随机因素
        import random
        player_roll = player_power * random.uniform(0.8, 1.2)
        friend_roll = friend_power * random.uniform(0.8, 1.2)
        
        won = player_roll > friend_roll
        
        # 更新切磋记录
        if won:
            friend.battles_won += 1
            favor_change = 5
            result_msg = f"切磋胜利！你击败了【{friend.name}】"
        else:
            friend.battles_lost += 1
            favor_change = 2  # 输了也增加好感（互相学习）
            result_msg = f"切磋失败，【{friend.name}】技高一筹"
        
        friend.add_interaction("challenge", result_msg, favor_change)
        
        # 添加聊天消息
        self.send_message(
            friend_id,
            f"切磋结果：{'你赢了！' if won else '你输了！'}",
            MessageType.CHALLENGE
        )
        
        return {
            "success": True,
            "won": won,
            "message": result_msg,
            "player_power": int(player_roll),
            "friend_power": int(friend_roll),
            "favor_gained": favor_change,
            "battle_record": {
                "wins": friend.battles_won,
                "losses": friend.battles_lost
            }
        }
    
    # ==================== 聊天系统 ====================
    
    def send_message(self, friend_id: str, content: str, 
                     message_type: MessageType = MessageType.TEXT) -> dict:
        """发送消息"""
        if friend_id not in self.friends:
            return {"success": False, "message": "该玩家不在好友列表中"}
        
        friend = self.friends[friend_id]
        
        message = ChatMessage(
            message_id=f"msg_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            sender_id=self.player_id,
            sender_name="我",
            content=content,
            message_type=message_type
        )
        
        if friend_id not in self.messages:
            self.messages[friend_id] = []
        
        self.messages[friend_id].append(message)
        
        return {
            "success": True,
            "message": "消息已发送",
            "sent_message": message.to_dict()
        }
    
    def receive_message(self, friend_id: str, content: str, 
                        message_type: MessageType = MessageType.TEXT) -> dict:
        """接收消息（模拟好友发送）"""
        if friend_id not in self.friends:
            return {"success": False, "message": "该玩家不在好友列表中"}
        
        friend = self.friends[friend_id]
        
        message = ChatMessage(
            message_id=f"msg_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            sender_id=friend_id,
            sender_name=friend.name,
            content=content,
            message_type=message_type
        )
        
        if friend_id not in self.messages:
            self.messages[friend_id] = []
        
        self.messages[friend_id].append(message)
        
        return {
            "success": True,
            "message": f"收到【{friend.name}】的消息",
            "received_message": message.to_dict()
        }
    
    def get_chat_history(self, friend_id: str, limit: int = 50) -> List[ChatMessage]:
        """获取聊天记录"""
        if friend_id not in self.messages:
            return []
        
        messages = self.messages[friend_id][-limit:]
        
        # 标记为已读
        for msg in messages:
            msg.is_read = True
        
        return messages
    
    def get_unread_count(self, friend_id: Optional[str] = None) -> int:
        """获取未读消息数量"""
        if friend_id:
            if friend_id not in self.messages:
                return 0
            return sum(1 for m in self.messages[friend_id] if not m.is_read and m.sender_id != self.player_id)
        
        # 所有好友的未读总数
        total = 0
        for fid, msgs in self.messages.items():
            total += sum(1 for m in msgs if not m.is_read and m.sender_id != self.player_id)
        return total
    
    def add_system_message(self, content: str):
        """添加系统通知"""
        system_id = "system"
        if system_id not in self.messages:
            self.messages[system_id] = []
        
        message = ChatMessage(
            message_id=f"sys_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            sender_id="system",
            sender_name="系统",
            content=content,
            message_type=MessageType.SYSTEM
        )
        
        self.messages[system_id].append(message)
    
    def get_system_messages(self, limit: int = 20) -> List[ChatMessage]:
        """获取系统消息"""
        system_id = "system"
        if system_id not in self.messages:
            return []
        return self.messages[system_id][-limit:]
    
    # ==================== 排行榜互动 ====================
    
    def get_friend_rankings(self, ranking_type: str = "cultivation") -> List[dict]:
        """获取好友排行榜
        
        ranking_type: cultivation(修为), favorability(好感), battles(切磋胜率)
        """
        if not self.friends:
            return []
        
        rankings = []
        
        for friend in self.friends.values():
            entry = {
                "friend_id": friend.friend_id,
                "name": friend.name,
                "realm": friend.realm,
                "sect": friend.sect or "散修",
                "favorability": friend.favorability,
                "friendship_level": friend.get_friendship_level().value
            }
            
            if ranking_type == "cultivation":
                # 模拟修为
                realm_cultivation = {
                    "练气期": 1000,
                    "筑基期": 5000,
                    "金丹期": 20000,
                    "元婴期": 100000,
                    "化神期": 500000,
                    "合体期": 2000000,
                    "大乘期": 10000000,
                    "渡劫期": 50000000,
                    "真仙": 200000000,
                }
                entry["value"] = realm_cultivation.get(friend.realm, 1000)
                entry["value_name"] = "修为"
            elif ranking_type == "favorability":
                entry["value"] = friend.favorability
                entry["value_name"] = "好感度"
            elif ranking_type == "battles":
                total = friend.battles_won + friend.battles_lost
                if total > 0:
                    entry["value"] = friend.battles_won / total * 100
                else:
                    entry["value"] = 0
                entry["value_name"] = "胜率%"
            
            rankings.append(entry)
        
        # 排序
        rankings.sort(key=lambda x: x["value"], reverse=True)
        
        # 添加排名
        for i, entry in enumerate(rankings):
            entry["rank"] = i + 1
        
        return rankings
    
    def challenge_ranking_record(self, friend_id: str, record_type: str, player_value: int) -> dict:
        """挑战好友记录"""
        if friend_id not in self.friends:
            return {"success": False, "message": "该玩家不在好友列表中"}
        
        friend = self.friends[friend_id]
        
        # 获取好友记录值
        rankings = self.get_friend_rankings(record_type)
        friend_rank = None
        for r in rankings:
            if r["friend_id"] == friend_id:
                friend_rank = r
                break
        
        if not friend_rank:
            return {"success": False, "message": "无法获取好友记录"}
        
        friend_value = friend_rank["value"]
        
        if player_value > friend_value:
            # 破纪录
            favor_change = 10
            friend.add_interaction("break_record", f"你在{record_type}榜超越了{friend.name}", favor_change)
            
            return {
                "success": True,
                "broken": True,
                "message": f"恭喜！你在{friend_rank['value_name']}榜超越了【{friend.name}】！",
                "player_value": player_value,
                "friend_value": friend_value,
                "favor_gained": favor_change
            }
        else:
            return {
                "success": True,
                "broken": False,
                "message": f"未能超越【{friend.name}】的记录",
                "player_value": player_value,
                "friend_value": friend_value,
                "favor_gained": 0
            }
    
    # ==================== 好感度奖励 ====================
    
    def get_favorability_rewards(self, friend_id: str) -> dict:
        """获取好感度奖励"""
        if friend_id not in self.friends:
            return {"available": False, "message": "该玩家不在好友列表中"}
        
        friend = self.friends[friend_id]
        level = friend.get_friendship_level()
        
        rewards = {
            FriendshipLevel.STRANGER: {
                "name": "陌生人",
                "rewards": [],
                "unlocked": []
            },
            FriendshipLevel.ACQUAINTANCE: {
                "name": "点头之交",
                "rewards": [
                    {"type": "gift_discount", "value": 0.05, "desc": "赠送礼物消耗-5%"}
                ],
                "unlocked": ["basic_gift"]
            },
            FriendshipLevel.FRIEND: {
                "name": "好友",
                "rewards": [
                    {"type": "gift_discount", "value": 0.1, "desc": "赠送礼物消耗-10%"},
                    {"type": "battle_bonus", "value": 0.05, "desc": "切磋好感+5%"}
                ],
                "unlocked": ["basic_gift", "special_gift", "chat_history"]
            },
            FriendshipLevel.CLOSE_FRIEND: {
                "name": "挚友",
                "rewards": [
                    {"type": "gift_discount", "value": 0.15, "desc": "赠送礼物消耗-15%"},
                    {"type": "battle_bonus", "value": 0.1, "desc": "切磋好感+10%"},
                    {"type": "daily_bonus", "value": 10, "desc": "每日互动奖励+10灵石"}
                ],
                "unlocked": ["basic_gift", "special_gift", "chat_history", "shared_quests"]
            },
            FriendshipLevel.CONFIDANT: {
                "name": "知己",
                "rewards": [
                    {"type": "gift_discount", "value": 0.2, "desc": "赠送礼物消耗-20%"},
                    {"type": "battle_bonus", "value": 0.15, "desc": "切磋好感+15%"},
                    {"type": "daily_bonus", "value": 20, "desc": "每日互动奖励+20灵石"},
                    {"type": "shared_exp", "value": 0.1, "desc": "共享10%修炼经验"}
                ],
                "unlocked": ["basic_gift", "special_gift", "chat_history", "shared_quests", "team_formation"]
            },
            FriendshipLevel.SWORN_SIBLING: {
                "name": "结拜兄弟",
                "rewards": [
                    {"type": "gift_discount", "value": 0.3, "desc": "赠送礼物消耗-30%"},
                    {"type": "battle_bonus", "value": 0.25, "desc": "切磋好感+25%"},
                    {"type": "daily_bonus", "value": 50, "desc": "每日互动奖励+50灵石"},
                    {"type": "shared_exp", "value": 0.2, "desc": "共享20%修炼经验"},
                    {"type": "special_skill", "value": "joint_attack", "desc": "解锁合击技能"}
                ],
                "unlocked": ["all_features"]
            }
        }
        
        return {
            "available": True,
            "current_level": level.value,
            "favorability": friend.favorability,
            "rewards_info": rewards.get(level, rewards[FriendshipLevel.STRANGER])
        }
    
    # ==================== 每日互动 ====================
    
    def daily_interaction(self, friend_id: str) -> dict:
        """每日互动奖励"""
        if friend_id not in self.friends:
            return {"success": False, "message": "该玩家不在好友列表中"}
        
        friend = self.friends[friend_id]
        level = friend.get_friendship_level()
        
        # 基础奖励
        base_spirit_stones = 5
        base_favor = 2
        
        # 根据好感度等级加成
        level_rewards = {
            FriendshipLevel.STRANGER: {"stones": 0, "favor": 1},
            FriendshipLevel.ACQUAINTANCE: {"stones": 5, "favor": 2},
            FriendshipLevel.FRIEND: {"stones": 10, "favor": 3},
            FriendshipLevel.CLOSE_FRIEND: {"stones": 20, "favor": 5},
            FriendshipLevel.CONFIDANT: {"stones": 30, "favor": 7},
            FriendshipLevel.SWORN_SIBLING: {"stones": 50, "favor": 10},
        }
        
        rewards = level_rewards.get(level, level_rewards[FriendshipLevel.STRANGER])
        
        friend.add_interaction("daily", f"每日互动", rewards["favor"])
        
        return {
            "success": True,
            "message": f"与【{friend.name}】进行每日互动",
            "spirit_stones": rewards["stones"],
            "favor_gained": rewards["favor"],
            "new_favorability": friend.favorability
        }
    
    # ==================== 存档 ====================
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "player_id": self.player_id,
            "friends": {fid: f.to_dict() for fid, f in self.friends.items()},
            "friend_requests": [r.to_dict() for r in self.friend_requests],
            "messages": {
                fid: [m.to_dict() for m in msgs]
                for fid, msgs in self.messages.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FriendManager":
        """从字典创建"""
        manager = cls(data["player_id"])
        
        # 恢复好友列表
        for fid, fdata in data.get("friends", {}).items():
            manager.friends[fid] = Friend.from_dict(fdata)
        
        # 恢复好友申请
        for rdata in data.get("friend_requests", []):
            manager.friend_requests.append(FriendRequest.from_dict(rdata))
        
        # 恢复消息
        for fid, msgs in data.get("messages", {}).items():
            manager.messages[fid] = [ChatMessage.from_dict(m) for m in msgs]
        
        return manager


# ==================== 模拟好友数据 ====================

def generate_mock_friends() -> List[dict]:
    """生成模拟好友数据（用于测试）"""
    mock_data = [
        {"id": "npc_001", "name": "李逍遥", "realm": "金丹期", "sect": "峨眉派"},
        {"id": "npc_002", "name": "赵灵儿", "realm": "元婴期", "sect": "昆仑派"},
        {"id": "npc_003", "name": "林月如", "realm": "筑基期", "sect": "青城派"},
        {"id": "npc_004", "name": "酒剑仙", "realm": "化神期", "sect": None},
        {"id": "npc_005", "name": "阿奴", "realm": "金丹期", "sect": "血河教"},
    ]
    return mock_data
