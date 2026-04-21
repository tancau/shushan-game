#!/usr/bin/env python3
"""
蜀山剑侠传 - 世界地图与探索系统
"""

import json
import random
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class Location:
    """地点类"""
    
    def __init__(self, data: dict):
        self.id = data.get("id", "")
        self.name = data.get("name", "未知地点")
        self.type = data.get("type", "野外")
        self.region = data.get("region", "中原")
        self.description = data.get("description", "")
        self.danger_level = data.get("danger_level", 1)
        self.sect = data.get("sect", None)
        self.functions = data.get("functions", [])
        self.connected_to = data.get("connected_to", [])
        self.resources = data.get("resources", [])
        self.npcs = data.get("npcs", [])
        self.random_encounters = data.get("random_encounters", [])
        self.events = data.get("events", [])
        self.boss = data.get("boss", None)
        self.drops = data.get("drops", [])
        self.shops = data.get("shops", {})
        self.inns = data.get("inns", {})
        self.special = data.get("special", [])
        self.cultivation_bonus = data.get("cultivation_bonus", 1.0)
        self.level_required = data.get("level_required", 1)
    
    def can_enter(self, player_level: int) -> bool:
        """检查是否可以进入"""
        return player_level >= self.level_required
    
    def get_encounter_chance(self) -> float:
        """获取遭遇概率"""
        base = 0.3
        return base + (self.danger_level * 0.05)
    
    def get_resource_chance(self) -> float:
        """获取资源发现概率"""
        return 0.4 - (self.danger_level * 0.02)
    
    def __str__(self) -> str:
        danger_stars = "★" * self.danger_level if self.danger_level > 0 else "安全"
        return f"【{self.name}】({self.type}) 危险:{danger_stars}\n{self.description}"


class WorldMap:
    """世界地图类"""
    
    def __init__(self, data_path: str = "data/maps.json"):
        self.locations: Dict[str, Location] = {}
        self.regions: Dict[str, dict] = {}
        self.travel_times: Dict[str, int] = {}
        self.load_map(data_path)
    
    def load_map(self, data_path: str):
        """加载地图数据"""
        path = Path(data_path)
        if not path.exists():
            raise FileNotFoundError(f"地图数据文件不存在: {data_path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 加载地点
        for loc_id, loc_data in data.get("locations", {}).items():
            self.locations[loc_data["name"]] = Location(loc_data)
        
        # 加载区域
        self.regions = data.get("regions", {})
        
        # 加载旅行时间
        self.travel_times = data.get("travel_times", {
            "同城": 1, "邻城": 2, "跨区域": 5, "远距离": 10
        })
    
    def get_location(self, name: str) -> Optional[Location]:
        """获取地点"""
        return self.locations.get(name)
    
    def get_connected_locations(self, location_name: str) -> List[str]:
        """获取相连地点列表"""
        loc = self.get_location(location_name)
        if not loc:
            return []
        
        connected = []
        for name in loc.connected_to:
            if name in self.locations:
                connected.append(name)
        
        return connected
    
    def calculate_travel_time(self, from_loc: str, to_loc: str) -> int:
        """计算旅行时间"""
        if from_loc == to_loc:
            return 0
        
        from_location = self.get_location(from_loc)
        to_location = self.get_location(to_loc)
        
        if not from_location or not to_location:
            return -1
        
        # 检查是否直接相连
        if to_loc in from_location.connected_to:
            return self.travel_times.get("邻城", 2)
        
        # 同区域
        if from_location.region == to_location.region:
            return self.travel_times.get("同城", 1)
        
        # 跨区域
        return self.travel_times.get("跨区域", 5)
    
    def can_travel_to(self, from_loc: str, to_loc: str) -> bool:
        """检查是否可以到达目标地点"""
        from_location = self.get_location(from_loc)
        
        if not from_location:
            return False
        
        # 检查是否直接相连
        return to_loc in from_location.connected_to
    
    def get_locations_by_type(self, loc_type: str) -> List[Location]:
        """按类型获取地点"""
        return [loc for loc in self.locations.values() if loc.type == loc_type]
    
    def get_locations_by_region(self, region: str) -> List[Location]:
        """按区域获取地点"""
        return [loc for loc in self.locations.values() if loc.region == region]
    
    def get_locations_by_danger(self, max_danger: int) -> List[Location]:
        """按危险等级获取地点"""
        return [loc for loc in self.locations.values() if loc.danger_level <= max_danger]
    
    def get_starting_locations(self) -> List[Location]:
        """获取新手起始地点"""
        return [loc for loc in self.locations.values() if loc.level_required == 1]
    
    def find_path(self, from_loc: str, to_loc: str) -> List[str]:
        """寻找路径 (BFS)"""
        if from_loc == to_loc:
            return [from_loc]
        
        visited = set()
        queue = [[from_loc]]
        
        while queue:
            path = queue.pop(0)
            current = path[-1]
            
            if current in visited:
                continue
            
            visited.add(current)
            
            current_loc = self.get_location(current)
            if not current_loc:
                continue
            
            for neighbor in current_loc.connected_to:
                if neighbor == to_loc:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    queue.append(path + [neighbor])
        
        return []  # 无路径


class ExplorationEvent:
    """探索事件类"""
    
    EVENT_TYPES = {
        "战斗": {"weight": 30, "description": "遭遇敌人"},
        "宝物": {"weight": 15, "description": "发现宝物"},
        "资源": {"weight": 25, "description": "采集资源"},
        "NPC": {"weight": 15, "description": "遇到路人"},
        "奇遇": {"weight": 5, "description": "触发奇遇"},
        "无事": {"weight": 10, "description": "平安无事"}
    }
    
    @classmethod
    def generate_event(cls, location: Location, player_luck: int = 50) -> dict:
        """生成探索事件"""
        events = []
        
        # 根据地点类型调整事件权重
        weights = {k: v["weight"] for k, v in cls.EVENT_TYPES.items()}
        
        # 危险等级影响战斗概率
        weights["战斗"] += location.danger_level * 5
        weights["奇遇"] += player_luck // 20
        
        # 门派和城市更安全
        if location.type in ["门派", "城市"]:
            weights["战斗"] = 0
            weights["宝物"] = 5
            weights["NPC"] = 30
        
        # 秘境更容易出宝物
        if location.type == "秘境":
            weights["宝物"] += 20
            weights["战斗"] += 10
        
        # 随机选择事件
        total = sum(weights.values())
        rand = random.randint(1, total)
        cumulative = 0
        selected = "无事"
        
        for event_type, weight in weights.items():
            cumulative += weight
            if rand <= cumulative:
                selected = event_type
                break
        
        return cls.create_event_detail(selected, location, player_luck)
    
    @classmethod
    def create_event_detail(cls, event_type: str, location: Location, player_luck: int) -> dict:
        """创建事件详情"""
        event = {
            "type": event_type,
            "location": location.name,
            "timestamp": datetime.now().isoformat()
        }
        
        if event_type == "战斗":
            # 从地点的随机遭遇中选择敌人
            enemies = location.random_encounters if location.random_encounters else ["妖兽", "山贼", "魔修"]
            enemy = random.choice(enemies)
            
            # 敌人等级基于危险等级
            enemy_level = max(1, location.danger_level * 5 + random.randint(-3, 3))
            
            event["enemy"] = {
                "name": enemy,
                "level": enemy_level,
                "danger": location.danger_level
            }
            event["description"] = f"遭遇 {enemy} (等级 {enemy_level})"
            event["rewards"] = cls.calculate_combat_rewards(location, enemy_level)
        
        elif event_type == "宝物":
            treasures = location.drops if location.drops else ["灵石袋", "丹药", "法宝碎片"]
            treasure = random.choice(treasures)
            
            # 宝物品质
            quality_roll = random.randint(1, 100)
            quality = "普通"
            if quality_roll > 90:
                quality = "稀有"
            elif quality_roll > 70:
                quality = "精良"
            
            event["treasure"] = {
                "name": treasure,
                "quality": quality
            }
            event["description"] = f"发现 {quality} [{treasure}]"
        
        elif event_type == "资源":
            resources = location.resources if location.resources else ["灵草", "矿石", "药材"]
            
            # 采集数量
            amount = random.randint(1, 3 + player_luck // 20)
            resource = random.choice(resources)
            
            event["resource"] = {
                "name": resource,
                "amount": amount
            }
            event["description"] = f"采集到 {resource} x{amount}"
        
        elif event_type == "NPC":
            npcs = location.npcs if location.npcs else ["游方道士", "商人", "受伤修士", "乞丐"]
            npc = random.choice(npcs)
            
            event["npc"] = {
                "name": npc,
                "dialog": cls.generate_npc_dialog(npc, location)
            }
            event["description"] = f"遇到 {npc}"
        
        elif event_type == "奇遇":
            adventures = [
                "发现隐秘洞府",
                "拾得残破古籍",
                "感应到法宝气息",
                "遇到高人指点",
                "触发上古阵法"
            ]
            
            adventure = random.choice(adventures)
            event["adventure"] = adventure
            event["description"] = f"奇遇：{adventure}"
            event["luck_bonus"] = player_luck // 10
        
        else:  # 无事
            event["description"] = "此地风平浪静，并无异常"
            event["cultivation_bonus"] = 5  # 安静修炼加成
        
        return event
    
    @classmethod
    def calculate_combat_rewards(cls, location: Location, enemy_level: int) -> dict:
        """计算战斗奖励"""
        base_exp = enemy_level * 10
        base_spirit_stones = enemy_level * random.randint(1, 5)
        
        # 危险等级加成
        bonus = 1 + (location.danger_level * 0.2)
        
        return {
            "experience": int(base_exp * bonus),
            "spirit_stones": int(base_spirit_stones * bonus),
            "drop_chance": 0.3 + (location.danger_level * 0.05)
        }
    
    @classmethod
    def generate_npc_dialog(cls, npc_name: str, location: Location) -> str:
        """生成NPC对话"""
        dialogs = {
            "游方道士": [
                "道友，此地灵气充沛，适合修炼。",
                "在下刚从昆仑而来，那边似乎有异动。",
                "若要寻宝，不妨去秘境一试。"
            ],
            "商人": [
                "这位道友，要不要看看我的货物？",
                "最近灵石不太稳定，买卖要谨慎。",
                "听说东海蓬莱岛上有仙丹现世。"
            ],
            "受伤修士": [
                "前方危险，道友小心...",
                "那妖兽实力强悍，我差点丧命。",
                "若能帮我疗伤，必有重谢。"
            ],
            "乞丐": [
                "呵呵，莫看老叫花子这般模样...",
                "小子，我看你骨骼惊奇，送你个消息。",
                "这世道，低调做人才能活得长久。"
            ]
        }
        
        # 默认对话
        default = [
            "道友有礼了。",
            "此地风景不错。",
            "我还有事，先行一步。"
        ]
        
        npc_dialogs = dialogs.get(npc_name, default)
        return random.choice(npc_dialogs)


class ExplorationSystem:
    """探索系统类"""
    
    def __init__(self, world_map: WorldMap):
        self.world_map = world_map
        self.exploration_history: List[dict] = []
    
    def explore(self, location_name: str, player_data: dict) -> dict:
        """
        探索地点
        
        Args:
            location_name: 地点名称
            player_data: 玩家数据 (包含等级、幸运等)
        
        Returns:
            探索结果
        """
        location = self.world_map.get_location(location_name)
        
        if not location:
            return {
                "success": False,
                "message": f"未知地点：{location_name}"
            }
        
        player_level = player_data.get("realm_level", 1)
        player_luck = player_data.get("stats", {}).get("幸运", 50)
        
        # 检查等级要求
        if not location.can_enter(player_level):
            return {
                "success": False,
                "message": f"需要等级 {location.level_required} 才能进入 {location.name}"
            }
        
        # 检查是否有遭遇
        if random.random() < location.get_encounter_chance():
            event = ExplorationEvent.generate_event(location, player_luck)
        else:
            event = {
                "type": "无事",
                "description": f"在{location.name}探索一番，并无异常发现。",
                "cultivation_bonus": location.cultivation_bonus * 5
            }
        
        # 记录探索历史
        self.exploration_history.append({
            "location": location_name,
            "event": event,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "location": location.name,
            "event": event,
            "location_info": {
                "type": location.type,
                "danger_level": location.danger_level,
                "resources": location.resources,
                "connected_to": location.connected_to
            }
        }
    
    def gather_resource(self, location_name: str, resource_type: str = None) -> dict:
        """
        采集资源
        
        Args:
            location_name: 地点名称
            resource_type: 资源类型 (可选)
        
        Returns:
            采集结果
        """
        location = self.world_map.get_location(location_name)
        
        if not location:
            return {"success": False, "message": "未知地点"}
        
        if not location.resources:
            return {"success": False, "message": f"{location.name}没有可采集的资源"}
        
        # 选择资源
        if resource_type and resource_type in location.resources:
            resource = resource_type
        else:
            resource = random.choice(location.resources)
        
        # 采集成功率
        success_rate = location.get_resource_chance()
        
        if random.random() < success_rate:
            amount = random.randint(1, 3)
            return {
                "success": True,
                "resource": resource,
                "amount": amount,
                "message": f"成功采集到 {resource} x{amount}"
            }
        else:
            return {
                "success": False,
                "message": f"未能找到{resource}，或许换个时间试试？"
            }
    
    def search_treasure(self, location_name: str, player_luck: int = 50) -> dict:
        """
        搜刮寻宝
        
        Args:
            location_name: 地点名称
            player_luck: 玩家幸运值
        
        Returns:
            寻宝结果
        """
        location = self.world_map.get_location(location_name)
        
        if not location:
            return {"success": False, "message": "未知地点"}
        
        # 秘境更容易找到宝物
        treasure_chance = 0.2 + (player_luck / 200)
        if location.type == "秘境":
            treasure_chance += 0.2
        if location.type == "野外":
            treasure_chance += 0.1
        
        if random.random() < treasure_chance:
            # 随机宝物
            treasures = location.drops if location.drops else [
                "灵石袋", "丹药", "残破法宝", "古籍残卷"
            ]
            treasure = random.choice(treasures)
            
            # 品质判定
            quality_roll = random.randint(1, 100) + player_luck // 5
            quality = "普通"
            if quality_roll > 95:
                quality = "传说"
            elif quality_roll > 85:
                quality = "稀有"
            elif quality_roll > 70:
                quality = "精良"
            
            return {
                "success": True,
                "treasure": treasure,
                "quality": quality,
                "message": f"发现 {quality} [{treasure}]！"
            }
        else:
            return {
                "success": False,
                "message": "仔细搜寻一番，并无发现..."
            }
    
    def get_available_actions(self, location_name: str) -> List[str]:
        """获取当前可用的行动"""
        location = self.world_map.get_location(location_name)
        
        if not location:
            return []
        
        actions = []
        
        # 基础行动
        if location.resources:
            actions.append("采集资源")
        
        # 地点功能
        for func in location.functions:
            if func not in actions:
                actions.append(func)
        
        # 通用行动
        actions.extend(["探索", "休息", "查看地图"])
        
        return actions


class TravelSystem:
    """旅行系统类"""
    
    def __init__(self, world_map: WorldMap):
        self.world_map = world_map
    
    def travel(self, from_location: str, to_location: str, player_data: dict) -> dict:
        """
        移动到新地点
        
        Args:
            from_location: 当前地点
            to_location: 目标地点
            player_data: 玩家数据
        
        Returns:
            旅行结果
        """
        # 验证地点
        from_loc = self.world_map.get_location(from_location)
        to_loc = self.world_map.get_location(to_location)
        
        if not from_loc:
            return {"success": False, "message": f"未知起点：{from_location}"}
        
        if not to_loc:
            return {"success": False, "message": f"未知目的地：{to_location}"}
        
        # 检查等级要求
        player_level = player_data.get("realm_level", 1)
        if not to_loc.can_enter(player_level):
            return {
                "success": False,
                "message": f"需要等级 {to_loc.level_required} 才能进入 {to_loc.name}"
            }
        
        # 检查路径
        if not self.world_map.can_travel_to(from_location, to_location):
            # 尝试寻找路径
            path = self.world_map.find_path(from_location, to_location)
            if path:
                return {
                    "success": False,
                    "message": f"无法直接到达，需要经过：{' → '.join(path)}",
                    "path": path
                }
            else:
                return {
                    "success": False,
                    "message": f"无法从 {from_location} 到达 {to_location}"
                }
        
        # 计算旅行时间
        travel_time = self.world_map.calculate_travel_time(from_location, to_location)
        
        # 途中可能遭遇
        encounter = None
        if to_loc.danger_level > 0 and random.random() < 0.3:
            encounter = ExplorationEvent.generate_event(
                to_loc, 
                player_data.get("stats", {}).get("幸运", 50)
            )
        
        return {
            "success": True,
            "from": from_location,
            "to": to_location,
            "travel_time": travel_time,
            "location_info": {
                "name": to_loc.name,
                "type": to_loc.type,
                "region": to_loc.region,
                "description": to_loc.description,
                "danger_level": to_loc.danger_level,
                "functions": to_loc.functions,
                "connected_to": self.world_map.get_connected_locations(to_location)
            },
            "encounter": encounter,
            "message": f"成功抵达 {to_loc.name}"
        }
    
    def get_nearby_locations(self, current_location: str) -> List[dict]:
        """获取附近可到达的地点"""
        connected = self.world_map.get_connected_locations(current_location)
        result = []
        
        for loc_name in connected:
            loc = self.world_map.get_location(loc_name)
            if loc:
                result.append({
                    "name": loc.name,
                    "type": loc.type,
                    "danger_level": loc.danger_level,
                    "travel_time": self.world_map.calculate_travel_time(current_location, loc_name)
                })
        
        return result


# 便捷函数
def create_world(data_path: str = "data/maps.json") -> WorldMap:
    """创建世界地图实例"""
    return WorldMap(data_path)


def create_exploration_system(world_map: WorldMap = None) -> ExplorationSystem:
    """创建探索系统实例"""
    if world_map is None:
        world_map = create_world()
    return ExplorationSystem(world_map)


def create_travel_system(world_map: WorldMap = None) -> TravelSystem:
    """创建旅行系统实例"""
    if world_map is None:
        world_map = create_world()
    return TravelSystem(world_map)


# 测试代码
if __name__ == "__main__":
    # 测试地图加载
    world = create_world()
    print(f"加载了 {len(world.locations)} 个地点")
    print(f"区域: {list(world.regions.keys())}")
    
    # 测试地点
    emei = world.get_location("峨眉山")
    print(f"\n{emei}")
    print(f"相连地点: {world.get_connected_locations('峨眉山')}")
    
    # 测试探索
    exploration = create_exploration_system(world)
    player = {"realm_level": 1, "stats": {"幸运": 60}}
    result = exploration.explore("峨眉山脚", player)
    print(f"\n探索结果: {result}")
    
    # 测试旅行
    travel = create_travel_system(world)
    travel_result = travel.travel("峨眉山脚", "成都府", player)
    print(f"\n旅行结果: {travel_result}")
