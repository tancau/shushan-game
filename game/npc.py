#!/usr/bin/env python3
"""
蜀山剑侠传 - NPC 系统
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field
import random


class NPCType(Enum):
    """NPC 类型"""
    MERCHANT = "商人"          # 商人：买卖物品
    QUEST_GIVER = "任务发布者"  # 任务发布者
    MASTER = "师傅"            # 门派师傅：传授功法
    VILLAGER = "路人"          # 普通NPC
    SPECIAL = "特殊NPC"        # 特殊NPC：隐藏任务、奇遇
    BLACK_MARKET = "黑市商人"  # 黑市商人：稀有物品


class ShopType(Enum):
    """商店类型"""
    PILL = "丹药"              # 丹药店
    ARTIFACT = "法宝"          # 法宝店
    MATERIAL = "材料"          # 材料店
    SKILL = "功法"             # 功法传授
    MISC = "杂货"              # 杂货店
    BLACK_MARKET = "黑市"      # 黑市


@dataclass
class ShopItem:
    """商店商品"""
    item_id: str               # 物品ID
    name: str                  # 显示名称
    category: str              # 分类
    price: int                 # 价格（灵石）
    stock: int = -1            # 库存，-1 表示无限
    level_required: int = 1    # 需要等级
    realm_required: str = ""   # 需要境界
    is_rare: bool = False      # 是否稀有商品
    discount: float = 1.0      # 折扣
    description: str = ""      # 描述
    
    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "level_required": self.level_required,
            "realm_required": self.realm_required,
            "is_rare": self.is_rare,
            "discount": self.discount,
            "description": self.description
        }


@dataclass
class Shop:
    """商店"""
    shop_id: str
    name: str
    shop_type: ShopType
    owner_npc: str             # 所属 NPC ID
    items: List[ShopItem] = field(default_factory=list)
    refresh_time: int = 24     # 刷新时间（小时）
    last_refresh: str = ""     # 上次刷新时间
    reputation_required: int = 0  # 需要声望
    discount_for_sect: Dict[str, float] = field(default_factory=dict)  # 门派折扣
    
    def get_item(self, item_id: str) -> Optional[ShopItem]:
        """获取商品"""
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None
    
    def to_dict(self) -> dict:
        return {
            "shop_id": self.shop_id,
            "name": self.name,
            "shop_type": self.shop_type.value,
            "owner_npc": self.owner_npc,
            "items": [item.to_dict() for item in self.items],
            "refresh_time": self.refresh_time,
            "last_refresh": self.last_refresh,
            "reputation_required": self.reputation_required,
            "discount_for_sect": self.discount_for_sect
        }


@dataclass
class Dialogue:
    """对话"""
    text: str                          # 对话内容
    options: List[Dict[str, Any]] = field(default_factory=list)  # 选项
    condition: Optional[str] = None    # 触发条件
    quest_trigger: Optional[str] = None  # 触发任务
    
    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "options": self.options,
            "condition": self.condition,
            "quest_trigger": self.quest_trigger
        }


@dataclass
class NPC:
    """NPC 类"""
    npc_id: str
    name: str
    npc_type: NPCType
    location: str                     # 所在位置
    description: str = ""
    
    # 对话系统
    dialogues: List[Dialogue] = field(default_factory=list)
    default_greeting: str = "你好，道友。"
    
    # 商店
    shop_id: Optional[str] = None
    
    # 任务
    quest_ids: List[str] = field(default_factory=list)
    
    # 功法传授（师傅特有）
    skill_ids: List[str] = field(default_factory=list)
    sect: Optional[str] = None        # 所属门派
    
    # 特殊功能
    can_exchange: bool = False        # 是否可兑换门派贡献
    exchange_items: List[Dict] = field(default_factory=list)
    
    # 条件
    level_required: int = 1
    quest_required: Optional[str] = None
    sect_required: Optional[str] = None
    
    # 黑市特有
    hidden: bool = False              # 是否隐藏
    appear_condition: Optional[str] = None  # 出现条件
    disappear_after: int = 0          # 消失时间
    
    def get_dialogue(self, player_data: dict) -> Dialogue:
        """获取对话（根据玩家状态）"""
        # 检查条件对话
        for dialogue in self.dialogues:
            if self._check_condition(dialogue.condition, player_data):
                return dialogue
        
        # 返回默认问候
        return Dialogue(text=self.default_greeting)
    
    def _check_condition(self, condition: Optional[str], player_data: dict) -> bool:
        """检查对话条件"""
        if not condition:
            return False
        
        # 简单条件检查
        # 格式: "quest_completed:quest_id" 或 "level>=10" 等
        try:
            if condition.startswith("quest_completed:"):
                quest_id = condition.split(":")[1]
                return quest_id in player_data.get("completed_quests", [])
            elif condition.startswith("level>="):
                level = int(condition.split(">=")[1])
                return player_data.get("level", 1) >= level
            elif condition.startswith("sect:"):
                sect = condition.split(":")[1]
                return player_data.get("sect") == sect
        except:
            pass
        
        return False
    
    def can_interact(self, player_data: dict) -> tuple:
        """检查是否可以交互"""
        # 检查等级
        if player_data.get("level", 1) < self.level_required:
            return False, f"需要达到 Lv.{self.level_required} 才能与此人交谈"
        
        # 检查门派
        if self.sect_required and player_data.get("sect") != self.sect_required:
            return False, f"此人是 {self.sect_required} 的，不与外人交谈"
        
        # 检查前置任务
        if self.quest_required:
            if self.quest_required not in player_data.get("completed_quests", []):
                return False, "此人似乎有话要说，但你现在还不够资格"
        
        # 黑市检查
        if self.hidden:
            # 随机出现或满足特定条件
            if self.appear_condition:
                if not self._check_condition(self.appear_condition, player_data):
                    return False, "这里似乎没有人..."
        
        return True, ""
    
    def to_dict(self) -> dict:
        return {
            "npc_id": self.npc_id,
            "name": self.name,
            "npc_type": self.npc_type.value,
            "location": self.location,
            "description": self.description,
            "dialogues": [d.to_dict() for d in self.dialogues],
            "default_greeting": self.default_greeting,
            "shop_id": self.shop_id,
            "quest_ids": self.quest_ids,
            "skill_ids": self.skill_ids,
            "sect": self.sect,
            "can_exchange": self.can_exchange,
            "exchange_items": self.exchange_items,
            "level_required": self.level_required,
            "quest_required": self.quest_required,
            "sect_required": self.sect_required,
            "hidden": self.hidden,
            "appear_condition": self.appear_condition,
            "disappear_after": self.disappear_after
        }


class NPCManager:
    """NPC 管理器"""
    
    def __init__(self, npc_path: str = "data/npcs.json", shop_path: str = "data/shops.json"):
        self.npc_path = Path(npc_path)
        self.shop_path = Path(shop_path)
        
        self.npcs: Dict[str, NPC] = {}
        self.shops: Dict[str, Shop] = {}
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        # 加载 NPC
        if self.npc_path.exists():
            with open(self.npc_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for npc_data in data.get("npcs", []):
                npc = self._parse_npc(npc_data)
                self.npcs[npc.npc_id] = npc
        
        # 加载商店
        if self.shop_path.exists():
            with open(self.shop_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for shop_data in data.get("shops", []):
                shop = self._parse_shop(shop_data)
                self.shops[shop.shop_id] = shop
    
    def _parse_npc(self, data: dict) -> NPC:
        """解析 NPC 数据"""
        dialogues = []
        for d in data.get("dialogues", []):
            dialogues.append(Dialogue(
                text=d.get("text", ""),
                options=d.get("options", []),
                condition=d.get("condition"),
                quest_trigger=d.get("quest_trigger")
            ))
        
        return NPC(
            npc_id=data["npc_id"],
            name=data["name"],
            npc_type=NPCType(data["npc_type"]),
            location=data.get("location", ""),
            description=data.get("description", ""),
            dialogues=dialogues,
            default_greeting=data.get("default_greeting", "你好，道友。"),
            shop_id=data.get("shop_id"),
            quest_ids=data.get("quest_ids", []),
            skill_ids=data.get("skill_ids", []),
            sect=data.get("sect"),
            can_exchange=data.get("can_exchange", False),
            exchange_items=data.get("exchange_items", []),
            level_required=data.get("level_required", 1),
            quest_required=data.get("quest_required"),
            sect_required=data.get("sect_required"),
            hidden=data.get("hidden", False),
            appear_condition=data.get("appear_condition"),
            disappear_after=data.get("disappear_after", 0)
        )
    
    def _parse_shop(self, data: dict) -> Shop:
        """解析商店数据"""
        items = []
        for item_data in data.get("items", []):
            items.append(ShopItem(
                item_id=item_data["item_id"],
                name=item_data["name"],
                category=item_data["category"],
                price=item_data["price"],
                stock=item_data.get("stock", -1),
                level_required=item_data.get("level_required", 1),
                realm_required=item_data.get("realm_required", ""),
                is_rare=item_data.get("is_rare", False),
                discount=item_data.get("discount", 1.0),
                description=item_data.get("description", "")
            ))
        
        return Shop(
            shop_id=data["shop_id"],
            name=data["name"],
            shop_type=ShopType(data["shop_type"]),
            owner_npc=data.get("owner_npc", ""),
            items=items,
            refresh_time=data.get("refresh_time", 24),
            last_refresh=data.get("last_refresh", ""),
            reputation_required=data.get("reputation_required", 0),
            discount_for_sect=data.get("discount_for_sect", {})
        )
    
    def get_npc(self, npc_id: str) -> Optional[NPC]:
        """获取 NPC"""
        return self.npcs.get(npc_id)
    
    def get_npc_by_name(self, name: str) -> Optional[NPC]:
        """通过名称获取 NPC"""
        for npc in self.npcs.values():
            if npc.name == name:
                return npc
        return None
    
    def get_npcs_at_location(self, location: str) -> List[NPC]:
        """获取某位置的所有 NPC"""
        return [npc for npc in self.npcs.values() if npc.location == location]
    
    def get_shop(self, shop_id: str) -> Optional[Shop]:
        """获取商店"""
        return self.shops.get(shop_id)
    
    def get_npc_shop(self, npc_id: str) -> Optional[Shop]:
        """获取 NPC 的商店"""
        npc = self.get_npc(npc_id)
        if npc and npc.shop_id:
            return self.shops.get(npc.shop_id)
        return None
    
    def get_merchants(self) -> List[NPC]:
        """获取所有商人"""
        return [npc for npc in self.npcs.values() 
                if npc.npc_type in [NPCType.MERCHANT, NPCType.BLACK_MARKET]]
    
    def get_quest_givers(self) -> List[NPC]:
        """获取所有任务发布者"""
        return [npc for npc in self.npcs.values() 
                if npc.npc_type == NPCType.QUEST_GIVER or npc.quest_ids]
    
    def get_masters(self) -> List[NPC]:
        """获取所有师傅"""
        return [npc for npc in self.npcs.values() 
                if npc.npc_type == NPCType.MASTER]
    
    def get_masters_by_sect(self, sect: str) -> List[NPC]:
        """获取某门派的师傅"""
        return [npc for npc in self.npcs.values() 
                if npc.npc_type == NPCType.MASTER and npc.sect == sect]
    
    # ==================== 交互方法 ====================
    
    def talk_to_npc(self, npc_id: str, player_data: dict) -> dict:
        """与 NPC 对话"""
        npc = self.get_npc(npc_id)
        if not npc:
            return {"success": False, "message": "此人不在"}
        
        # 检查是否可以交互
        can_interact, msg = npc.can_interact(player_data)
        if not can_interact:
            return {"success": False, "message": msg}
        
        # 获取对话
        dialogue = npc.get_dialogue(player_data)
        
        result = {
            "success": True,
            "npc_name": npc.name,
            "npc_type": npc.npc_type.value,
            "dialogue": dialogue.text,
            "options": dialogue.options,
            "description": npc.description
        }
        
        # 商人：显示商店选项
        if npc.shop_id:
            shop = self.get_shop(npc.shop_id)
            if shop:
                result["has_shop"] = True
                result["shop_name"] = shop.name
        
        # 任务发布者：显示可用任务
        if npc.quest_ids:
            result["has_quests"] = True
            result["quest_ids"] = npc.quest_ids
        
        # 师傅：显示可学功法
        if npc.skill_ids:
            result["has_skills"] = True
            result["skill_ids"] = npc.skill_ids
        
        # 门派兑换
        if npc.can_exchange:
            result["can_exchange"] = True
            result["exchange_items"] = npc.exchange_items
        
        # 触发任务
        if dialogue.quest_trigger:
            result["quest_trigger"] = dialogue.quest_trigger
        
        return result
    
    def open_shop(self, npc_id: str, player_data: dict) -> dict:
        """打开商店"""
        npc = self.get_npc(npc_id)
        if not npc:
            return {"success": False, "message": "此人不在"}
        
        if not npc.shop_id:
            return {"success": False, "message": "此人不做买卖"}
        
        shop = self.get_shop(npc.shop_id)
        if not shop:
            return {"success": False, "message": "商店不存在"}
        
        # 检查声望
        if player_data.get("reputation", 0) < shop.reputation_required:
            return {
                "success": False, 
                "message": f"需要声望达到 {shop.reputation_required} 才能在此购买"
            }
        
        # 获取门派折扣
        discount = 1.0
        player_sect = player_data.get("sect")
        if player_sect and player_sect in shop.discount_for_sect:
            discount = shop.discount_for_sect[player_sect]
        
        # 过滤商品（根据等级和境界）
        available_items = []
        for item in shop.items:
            # 检查库存
            if item.stock == 0:
                continue
            
            # 检查等级
            if player_data.get("level", 1) < item.level_required:
                continue
            
            # 稀有商品概率显示
            if item.is_rare:
                # 黑市有更高概率显示稀有商品
                if shop.shop_type == ShopType.BLACK_MARKET:
                    if random.random() > 0.3:  # 30% 概率显示
                        continue
                else:
                    if random.random() > 0.1:  # 10% 概率显示
                        continue
            
            # 计算折扣后价格
            final_price = int(item.price * discount * item.discount)
            
            available_items.append({
                "item_id": item.item_id,
                "name": item.name,
                "category": item.category,
                "price": final_price,
                "original_price": item.price,
                "stock": item.stock,
                "is_rare": item.is_rare,
                "description": item.description
            })
        
        return {
            "success": True,
            "shop_name": shop.name,
            "shop_type": shop.shop_type.value,
            "npc_name": npc.name,
            "discount": discount,
            "items": available_items,
            "player_spirit_stones": player_data.get("spirit_stones", 0)
        }
    
    def buy_item(self, npc_id: str, item_id: str, quantity: int, player_data: dict) -> dict:
        """购买商品"""
        npc = self.get_npc(npc_id)
        if not npc or not npc.shop_id:
            return {"success": False, "message": "无法购买"}
        
        shop = self.get_shop(npc.shop_id)
        if not shop:
            return {"success": False, "message": "商店不存在"}
        
        item = shop.get_item(item_id)
        if not item:
            return {"success": False, "message": "商品不存在"}
        
        # 检查库存
        if item.stock > 0 and item.stock < quantity:
            return {"success": False, "message": f"库存不足，仅剩 {item.stock} 个"}
        
        # 计算价格
        discount = 1.0
        player_sect = player_data.get("sect")
        if player_sect and player_sect in shop.discount_for_sect:
            discount = shop.discount_for_sect[player_sect]
        
        total_price = int(item.price * discount * item.discount * quantity)
        
        # 检查灵石
        if player_data.get("spirit_stones", 0) < total_price:
            return {"success": False, "message": f"灵石不足，需要 {total_price} 灵石"}
        
        # 扣除库存
        if item.stock > 0:
            item.stock -= quantity
        
        return {
            "success": True,
            "message": f"购买成功：{item.name} x{quantity}",
            "item_id": item.item_id,
            "item_name": item.name,
            "quantity": quantity,
            "cost": total_price
        }
    
    def learn_skill(self, npc_id: str, skill_id: str, player_data: dict) -> dict:
        """学习功法（门派师傅）"""
        npc = self.get_npc(npc_id)
        if not npc:
            return {"success": False, "message": "此人不在"}
        
        if npc.npc_type != NPCType.MASTER:
            return {"success": False, "message": "此人不会传授功法"}
        
        if skill_id not in npc.skill_ids:
            return {"success": False, "message": "此功法不在传授范围内"}
        
        # 检查门派
        if npc.sect and player_data.get("sect") != npc.sect:
            return {"success": False, "message": f"此功法只传 {npc.sect} 弟子"}
        
        # 检查是否已学
        if skill_id in player_data.get("learned_skills", {}):
            return {"success": False, "message": "已经学过此功法了"}
        
        return {
            "success": True,
            "message": f"可以向 {npc.name} 学习此功法",
            "skill_id": skill_id,
            "npc_name": npc.name,
            "sect": npc.sect
        }
    
    def exchange_contribution(self, npc_id: str, exchange_id: str, player_data: dict) -> dict:
        """兑换门派贡献物品"""
        npc = self.get_npc(npc_id)
        if not npc or not npc.can_exchange:
            return {"success": False, "message": "此人无法兑换"}
        
        # 查找兑换项
        exchange_item = None
        for item in npc.exchange_items:
            if item.get("exchange_id") == exchange_id:
                exchange_item = item
                break
        
        if not exchange_item:
            return {"success": False, "message": "兑换项不存在"}
        
        # 检查门派贡献
        contribution_required = exchange_item.get("contribution", 0)
        if player_data.get("sect_contribution", 0) < contribution_required:
            return {
                "success": False, 
                "message": f"门派贡献不足，需要 {contribution_required} 点"
            }
        
        return {
            "success": True,
            "message": f"兑换成功：{exchange_item.get('name')}",
            "item_id": exchange_item.get("item_id"),
            "item_name": exchange_item.get("name"),
            "contribution_cost": contribution_required
        }
    
    def get_available_quests_from_npc(self, npc_id: str, player_data: dict) -> List[str]:
        """获取 NPC 可接取的任务"""
        npc = self.get_npc(npc_id)
        if not npc or not npc.quest_ids:
            return []
        
        available = []
        completed = player_data.get("completed_quests", [])
        active = player_data.get("active_quests", [])
        
        for quest_id in npc.quest_ids:
            if quest_id not in completed and quest_id not in active:
                available.append(quest_id)
        
        return available
    
    def refresh_shop(self, shop_id: str):
        """刷新商店（稀有商品）"""
        shop = self.get_shop(shop_id)
        if not shop:
            return
        
        # 重置库存
        for item in shop.items:
            if item.is_rare:
                # 随机库存
                item.stock = random.randint(1, 5)
    
    def to_dict(self) -> dict:
        """导出数据"""
        return {
            "npcs": [npc.to_dict() for npc in self.npcs.values()],
            "shops": [shop.to_dict() for shop in self.shops.values()]
        }


# ==================== 便捷函数 ====================

def create_default_npcs() -> List[NPC]:
    """创建默认 NPC 列表"""
    return [
        # 峨眉派 NPC
        NPC(
            npc_id="miaoyi_zhenren",
            name="妙一真人",
            npc_type=NPCType.MASTER,
            location="峨眉山",
            description="峨眉派掌门，正道领袖，飞剑之术登峰造极",
            default_greeting="峨眉弟子，可有什么不解之处？",
            sect="峨眉派",
            skill_ids=["emei_sword_art", "purple_cloud_sutra"],
            can_exchange=True,
            exchange_items=[
                {"exchange_id": "emei_sword", "name": "峨眉飞剑", "item_id": "emei_flying_sword", "contribution": 500},
                {"exchange_id": "emei_armor", "name": "峨眉道袍", "item_id": "emei_robe", "contribution": 300}
            ]
        ),
        NPC(
            npc_id="qi_shushi",
            name="齐漱石",
            npc_type=NPCType.MASTER,
            location="峨眉山",
            description="峨眉派长老，精通阵法与炼器",
            default_greeting="需要炼制法宝吗？峨眉炼器术天下闻名。",
            sect="峨眉派",
            skill_ids=["emei_formation", "artifact_refining"],
            shop_id="emei_artifact_shop"
        ),
        NPC(
            npc_id="li_yingqiong",
            name="李英琼",
            npc_type=NPCType.QUEST_GIVER,
            location="峨眉山",
            description="峨眉派天才弟子，剑术超群",
            default_greeting="师弟/师妹，正想去山中历练，可愿同行？",
            sect="峨眉派",
            quest_ids=["emei_trial", "sword_seeking"],
            dialogues=[
                Dialogue(
                    text="我刚从后山回来，那里似乎有妖兽出没...",
                    condition="level>=10",
                    quest_trigger="investigate_back_mountain"
                )
            ]
        ),
        
        # 成都府商人
        NPC(
            npc_id="medicine_merchant",
            name="灵药商人·孙思邈",
            npc_type=NPCType.MERCHANT,
            location="成都府",
            description="行走江湖的灵药商人，据说与药王孙思邈有渊源",
            default_greeting="道友需要什么灵药？小店应有尽有。",
            shop_id="chengdu_pill_shop",
            quest_ids=["herb_collection"]
        ),
        NPC(
            npc_id="artifact_merchant",
            name="法宝商人·欧冶子后人",
            npc_type=NPCType.MERCHANT,
            location="成都府",
            description="传说中的铸剑师欧冶子后人，贩卖各式法宝",
            default_greeting="看看有没有合手的法宝？",
            shop_id="chengdu_artifact_shop"
        ),
        NPC(
            npc_id="material_merchant",
            name="材料商人",
            npc_type=NPCType.MERCHANT,
            location="成都府",
            description="贩卖各种炼丹炼器材料",
            default_greeting="上好的材料，炼丹炼器必备！",
            shop_id="chengdu_material_shop"
        ),
        NPC(
            npc_id="black_market_merchant",
            name="神秘商人",
            npc_type=NPCType.BLACK_MARKET,
            location="成都府",
            description="隐藏在暗处的黑市商人，贩卖稀有物品",
            default_greeting="嘘...这里的东西，不要外传。",
            shop_id="black_market_shop",
            hidden=True,
            appear_condition="level>=20"
        ),
        
        # 青城派 NPC
        NPC(
            npc_id="jile_zhenren",
            name="极乐真人",
            npc_type=NPCType.MASTER,
            location="青城山",
            description="青城派掌门，剑术防御见长",
            default_greeting="青城弟子，来修炼剑术吗？",
            sect="青城派",
            skill_ids=["qingcheng_sword", "defense_art"],
            can_exchange=True
        ),
        
        # 昆仑派 NPC
        NPC(
            npc_id="zhongli_quan",
            name="钟离权",
            npc_type=NPCType.MASTER,
            location="昆仑山",
            description="昆仑派祖师，八仙之一，炼器大成",
            default_greeting="昆仑炼器术，天下无双。",
            sect="昆仑派",
            skill_ids=["kunlun_refining", "artifact_mastery"],
            shop_id="kunlun_artifact_shop"
        ),
        NPC(
            npc_id="lv_dongbin",
            name="吕洞宾",
            npc_type=NPCType.MASTER,
            location="昆仑山",
            description="昆仑派祖师，八仙之一，剑术通神",
            default_greeting="剑道万千，各有千秋。",
            sect="昆仑派",
            skill_ids=["immortal_sword_art", "pure_yang_art"]
        ),
        
        # 任务发布者
        NPC(
            npc_id="village_elder",
            name="村长",
            npc_type=NPCType.QUEST_GIVER,
            location="峨眉山脚",
            description="峨眉山脚小村的村长",
            default_greeting="年轻人，能否帮我一个忙？",
            quest_ids=["village_wolf", "village_herbs"]
        ),
        NPC(
            npc_id="hunter_zhang",
            name="猎人张三",
            npc_type=NPCType.QUEST_GIVER,
            location="峨眉山脚",
            description="山脚下的猎人，熟悉山中地形",
            default_greeting="山中的妖兽最近不太安分啊...",
            quest_ids=["hunt_beast", "explore_cave"]
        ),
        NPC(
            npc_id="wandering_cultivator",
            name="云游修士",
            npc_type=NPCType.QUEST_GIVER,
            location="成都府",
            description="四处云游的修士，见多识广",
            default_greeting="我曾游历四方，有什么想问的吗？",
            quest_ids=["secret_map", "lost_artifact"]
        ),
        
        # 特殊 NPC
        NPC(
            npc_id="hidden_master",
            name="隐世高人",
            npc_type=NPCType.SPECIAL,
            location="桃花源",
            description="隐居桃源的高人，据说已臻化境",
            default_greeting="能来到此地，说明你有缘。",
            hidden=True,
            appear_condition="level>=50",
            quest_ids=["hidden_legacy"],
            skill_ids=["supreme_sword_art"],
            dialogues=[
                Dialogue(
                    text="我在此等候有缘人已千年...你可愿继承我的传承？",
                    condition="level>=50",
                    quest_trigger="hidden_master_trial"
                )
            ]
        ),
        NPC(
            npc_id="mysterious_old_man",
            name="神秘老者",
            npc_type=NPCType.SPECIAL,
            location="华山",
            description="华山上出现的神秘老者，身份成谜",
            default_greeting="年轻人，悟性不错。",
            hidden=True,
            appear_condition="level>=30",
            quest_ids=["sword_enlightenment"],
            dialogues=[
                Dialogue(
                    text="华山的剑意，你可有所感悟？",
                    options=[
                        {"text": "请前辈指点", "action": "learn_sword"},
                        {"text": "告辞", "action": "leave"}
                    ]
                )
            ]
        ),
        
        # 路人 NPC
        NPC(
            npc_id="inn_keeper",
            name="客栈掌柜",
            npc_type=NPCType.VILLAGER,
            location="成都府",
            description="云来客栈的掌柜",
            default_greeting="客官要住店吗？一晚十块灵石，可恢复精力。"
        ),
        NPC(
            npc_id="teahouse_owner",
            name="茶馆老板",
            npc_type=NPCType.VILLAGER,
            location="成都府",
            description="茶馆老板，消息灵通",
            default_greeting="来喝杯茶？最近江湖上发生了不少事...",
            dialogues=[
                Dialogue(
                    text="听说血河教最近又蠢蠢欲动了...",
                    condition="level>=20"
                ),
                Dialogue(
                    text="东海龙宫似乎有异动，不少修士都去探查了。",
                    condition="level>=40"
                )
            ]
        ),
        NPC(
            npc_id="fortune_teller",
            name="算命先生",
            npc_type=NPCType.VILLAGER,
            location="长安城",
            description="长安城的算命先生，据说颇为灵验",
            default_greeting="客官，算一卦？",
            dialogues=[
                Dialogue(
                    text="你的命格奇特...将来必有大机缘！",
                    options=[
                        {"text": "请问大机缘是什么？", "response": "天机不可泄露..."},
                        {"text": "告辞", "action": "leave"}
                    ]
                )
            ]
        ),
        
        # 血河教 NPC
        NPC(
            npc_id="blood_river_ancestor",
            name="血河老祖",
            npc_type=NPCType.MASTER,
            location="血河教总坛",
            description="血河教教主，邪道巨擘",
            default_greeting="入我血河，可得永生！",
            sect="血河教",
            skill_ids=["blood_river_art", "blood_sacrifice"],
            sect_required="血河教"
        ),
        
        # 门派贡献兑换官
        NPC(
            npc_id="emei_steward",
            name="峨眉执事",
            npc_type=NPCType.MASTER,
            location="峨眉山",
            description="峨眉派执事，负责门派贡献兑换",
            default_greeting="弟子可用门派贡献兑换物品。",
            sect="峨眉派",
            can_exchange=True,
            exchange_items=[
                {"exchange_id": "emei_pill", "name": "峨眉筑基丹", "item_id": "emei_foundation_pill", "contribution": 200},
                {"exchange_id": "emei_token", "name": "峨眉令牌", "item_id": "emei_token", "contribution": 100}
            ]
        )
    ]


def create_default_shops() -> List[Shop]:
    """创建默认商店列表"""
    return [
        # 成都府灵药店
        Shop(
            shop_id="chengdu_pill_shop",
            name="灵药铺",
            shop_type=ShopType.PILL,
            owner_npc="medicine_merchant",
            items=[
                ShopItem(item_id="hunchun_pill", name="回春丹", category="丹药", price=50, description="恢复生命值"),
                ShopItem(item_id="buqi_pill", name="补气丹", category="丹药", price=50, description="恢复真元"),
                ShopItem(item_id="lingqi_pill", name="灵气丹", category="丹药", price=200, description="增加修为"),
                ShopItem(item_id="zhujidan", name="筑基丹", category="丹药", price=1000, is_rare=True, description="筑基必备"),
                ShopItem(item_id="jindan", name="金丹", category="丹药", price=5000, is_rare=True, description="金丹期突破")
            ]
        ),
        
        # 成都府法宝店
        Shop(
            shop_id="chengdu_artifact_shop",
            name="法宝阁",
            shop_type=ShopType.ARTIFACT,
            owner_npc="artifact_merchant",
            items=[
                ShopItem(item_id="iron_sword", name="铁剑", category="法宝", price=100, description="普通铁剑"),
                ShopItem(item_id="spirit_sword", name="灵剑", category="法宝", price=500, level_required=10),
                ShopItem(item_id="flying_sword", name="飞剑", category="法宝", price=2000, level_required=20, is_rare=True),
                ShopItem(item_id="protective_charm", name="护身符", category="法宝", price=100),
                ShopItem(item_id="spirit_armor", name="灵甲", category="法宝", price=800, level_required=15)
            ]
        ),
        
        # 成都府材料店
        Shop(
            shop_id="chengdu_material_shop",
            name="材料铺",
            shop_type=ShopType.MATERIAL,
            owner_npc="material_merchant",
            items=[
                ShopItem(item_id="xuantie", name="玄铁", category="材料", price=10, description="炼器基础材料"),
                ShopItem(item_id="jingjin", name="精金", category="材料", price=50),
                ShopItem(item_id="lingshen", name="灵参", category="材料", price=100),
                ShopItem(item_id="zhuguo", name="朱果", category="材料", price=150),
                ShopItem(item_id="monster_core", name="妖兽内丹", category="材料", price=500, is_rare=True)
            ]
        ),
        
        # 黑市
        Shop(
            shop_id="black_market_shop",
            name="黑市",
            shop_type=ShopType.BLACK_MARKET,
            owner_npc="black_market_merchant",
            items=[
                ShopItem(item_id="blood_pill", name="血丹", category="丹药", price=500, is_rare=True, description="血河教秘制丹药"),
                ShopItem(item_id="demon_core", name="魔晶", category="材料", price=1000, is_rare=True),
                ShopItem(item_id="cursed_sword", name="诅咒之剑", category="法宝", price=3000, is_rare=True),
                ShopItem(item_id="forbidden_scroll", name="禁术卷轴", category="功法", price=5000, is_rare=True, stock=1)
            ],
            discount_for_sect={"血河教": 0.8}
        ),
        
        # 峨眉法宝店
        Shop(
            shop_id="emei_artifact_shop",
            name="峨眉法宝殿",
            shop_type=ShopType.ARTIFACT,
            owner_npc="qi_shushi",
            items=[
                ShopItem(item_id="emei_sword", name="峨眉飞剑", category="法宝", price=3000, level_required=25, is_rare=True),
                ShopItem(item_id="emei_robe", name="峨眉道袍", category="法宝", price=1500, level_required=15)
            ],
            discount_for_sect={"峨眉派": 0.7}
        ),
        
        # 昆仑法宝店
        Shop(
            shop_id="kunlun_artifact_shop",
            name="昆仑炼器阁",
            shop_type=ShopType.ARTIFACT,
            owner_npc="zhongli_quan",
            items=[
                ShopItem(item_id="kunlun_mirror", name="昆仑镜", category="法宝", price=10000, level_required=40, is_rare=True),
                ShopItem(item_id="star_sword", name="星辰剑", category="法宝", price=5000, level_required=30, is_rare=True)
            ],
            discount_for_sect={"昆仑派": 0.7}
        )
    ]


if __name__ == "__main__":
    # 测试
    manager = NPCManager()
    print(f"加载了 {len(manager.npcs)} 个 NPC")
    print(f"加载了 {len(manager.shops)} 个商店")
    
    # 测试对话
    player_data = {"level": 25, "spirit_stones": 1000, "sect": "峨眉派"}
    result = manager.talk_to_npc("miaoyi_zhenren", player_data)
    print(f"\n与妙一真人对话：{result}")
