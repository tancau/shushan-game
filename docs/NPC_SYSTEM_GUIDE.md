# NPC 和商店系统使用指南

## 概述

蜀山剑侠传的 NPC 系统包含以下功能：

- **25 个 NPC**：涵盖商人、师傅、任务发布者、特殊 NPC 等类型
- **9 个商店**：提供丹药、法宝、材料、杂货等商品
- **完整的交互系统**：对话、交易、学习功法、门派兑换

## 快速开始

### 1. 初始化 NPC 管理器

```python
from game.npc import NPCManager

# 使用默认数据路径
manager = NPCManager('data/npcs.json', 'data/shops.json')
```

### 2. 与 NPC 对话

```python
player_data = {
    'level': 25,
    'spirit_stones': 5000,
    'sect': '峨眉派',
    'sect_contribution': 300,
    'completed_quests': [],
    'active_quests': [],
    'learned_skills': {}
}

# 与 NPC 对话
result = manager.talk_to_npc('miaoyi_zhenren', player_data)

if result['success']:
    print(f"NPC: {result['npc_name']}")
    print(f"对话: {result['dialogue']}")
    
    # 如果是商人
    if result.get('has_shop'):
        print(f"商店: {result['shop_name']}")
    
    # 如果有任务
    if result.get('has_quests'):
        print(f"可接任务: {result['quest_ids']}")
```

### 3. 打开商店

```python
# 打开灵药铺
shop_result = manager.open_shop('medicine_merchant', player_data)

if shop_result['success']:
    print(f"商店: {shop_result['shop_name']}")
    print(f"商品数量: {len(shop_result['items'])}")
    
    for item in shop_result['items']:
        print(f"  - {item['name']}: {item['price']} 灵石")
```

### 4. 购买商品

```python
# 购买回春丹 x5
buy_result = manager.buy_item('medicine_merchant', 'hunchun_pill', 5, player_data)

if buy_result['success']:
    print(f"购买成功！花费 {buy_result['cost']} 灵石")
    # 从玩家数据中扣除灵石
    player_data['spirit_stones'] -= buy_result['cost']
else:
    print(f"购买失败: {buy_result['message']}")
```

### 5. 学习功法

```python
# 向师傅学习功法
learn_result = manager.learn_skill('miaoyi_zhenren', 'emei_sword_art', player_data)

if learn_result['success']:
    print(f"可以向 {learn_result['npc_name']} 学习此功法")
    # 执行学习逻辑（需要在游戏主系统中实现）
```

### 6. 门派贡献兑换

```python
# 使用门派贡献兑换物品
exchange_result = manager.exchange_contribution('emei_steward', 'emei_pill', player_data)

if exchange_result['success']:
    print(f"兑换成功！花费 {exchange_result['contribution_cost']} 点贡献")
    # 从玩家数据中扣除贡献
    player_data['sect_contribution'] -= exchange_result['contribution_cost']
```

## NPC 类型说明

### 1. 商人 (MERCHANT)

贩卖各种物品的 NPC。

**示例：**
- 灵药商人（成都府）：贩卖丹药
- 法宝商人（成都府）：贩卖法宝装备
- 材料商人（成都府）：贩卖炼丹炼器材料

**功能：**
- 对话
- 打开商店
- 购买商品

### 2. 师傅 (MASTER)

门派师傅，可以传授功法。

**示例：**
- 妙一真人（峨眉派掌门）
- 钟离权（昆仑派祖师）
- 极乐真人（青城派掌门）

**功能：**
- 对话
- 学习功法
- 门派贡献兑换

### 3. 任务发布者 (QUEST_GIVER)

发布任务的 NPC。

**示例：**
- 村长（峨眉山脚）
- 猎人张三（峨眉山脚）
- 云游修士（成都府）

**功能：**
- 对话
- 接取任务

### 4. 特殊 NPC (SPECIAL)

隐藏或特殊的 NPC，通常有独特功能。

**示例：**
- 隐世高人（桃花源）：需要等级 50 才能遇到
- 神秘老者（华山）：需要等级 30 才能遇到
- 剑冢守护者（蜀山剑冢）：高级剑道试炼

**功能：**
- 特殊对话
- 隐藏任务
- 稀有功法

### 5. 黑市商人 (BLACK_MARKET)

贩卖稀有和禁忌物品的商人。

**示例：**
- 神秘商人（成都府黑市）

**特点：**
- 需要一定等级才能出现
- 贩卖稀有物品
- 血河教弟子享受折扣

### 6. 路人 (VILLAGER)

普通 NPC，提供信息和背景故事。

**示例：**
- 客栈掌柜（成都府）
- 茶馆老板（成都府）
- 算命先生（长安城）

**功能：**
- 对话
- 打听消息
- 背景故事

## 商店系统

### 商店类型

1. **丹药店 (PILL)**：贩卖各种丹药
2. **法宝店 (ARTIFACT)**：贩卖法宝装备
3. **材料店 (MATERIAL)**：贩卖炼丹炼器材料
4. **功法店 (SKILL)**：贩卖功法秘籍
5. **杂货店 (MISC)**：贩卖各种杂货
6. **黑市 (BLACK_MARKET)**：贩卖稀有禁忌物品

### 商品属性

```python
{
    "item_id": "zhujidan",          # 物品 ID
    "name": "筑基丹",                # 显示名称
    "category": "丹药",              # 分类
    "price": 1000,                  # 价格（灵石）
    "stock": 5,                     # 库存（-1 表示无限）
    "level_required": 10,           # 需要等级
    "realm_required": "练气期",      # 需要境界
    "is_rare": true,                # 是否稀有
    "discount": 1.0,                # 折扣
    "description": "筑基期突破必备"  # 描述
}
```

### 门派折扣

门派弟子在本门派商店可享受折扣：

```json
{
  "discount_for_sect": {
    "峨眉派": 0.7,  // 7折
    "昆仑派": 0.7,  // 7折
    "血河教": 0.6   // 6折（黑市）
  }
}
```

## 数据结构

### NPC 数据 (data/npcs.json)

```json
{
  "npc_id": "miaoyi_zhenren",
  "name": "妙一真人",
  "npc_type": "师傅",
  "location": "峨眉山",
  "description": "峨眉派掌门...",
  "dialogues": [...],
  "shop_id": null,
  "quest_ids": ["emei_trial"],
  "skill_ids": ["emei_sword_art"],
  "sect": "峨眉派",
  "can_exchange": true,
  "exchange_items": [...]
}
```

### 商店数据 (data/shops.json)

```json
{
  "shop_id": "chengdu_pill_shop",
  "name": "灵药铺",
  "shop_type": "丹药",
  "owner_npc": "medicine_merchant",
  "items": [...],
  "discount_for_sect": {}
}
```

## API 参考

### NPCManager 类

#### 主要方法

- `get_npc(npc_id)` - 获取指定 NPC
- `get_npcs_at_location(location)` - 获取某位置的所有 NPC
- `get_shop(shop_id)` - 获取指定商店
- `get_merchants()` - 获取所有商人
- `get_masters()` - 获取所有师傅
- `talk_to_npc(npc_id, player_data)` - 与 NPC 对话
- `open_shop(npc_id, player_data)` - 打开商店
- `buy_item(npc_id, item_id, quantity, player_data)` - 购买商品
- `learn_skill(npc_id, skill_id, player_data)` - 学习功法
- `exchange_contribution(npc_id, exchange_id, player_data)` - 门派兑换

## 扩展开发

### 添加新 NPC

在 `data/npcs.json` 中添加新条目：

```json
{
  "npc_id": "new_npc",
  "name": "新角色",
  "npc_type": "路人",
  "location": "成都府",
  "description": "一个新角色",
  "default_greeting": "你好！",
  "dialogues": [
    {
      "text": "欢迎来到蜀山世界！",
      "options": [
        {"text": "告辞", "action": "leave"}
      ]
    }
  ]
}
```

### 添加新商店

在 `data/shops.json` 中添加新条目：

```json
{
  "shop_id": "new_shop",
  "name": "新商店",
  "shop_type": "杂货",
  "owner_npc": "new_npc",
  "items": [
    {
      "item_id": "new_item",
      "name": "新商品",
      "category": "杂货",
      "price": 100,
      "description": "这是一个新商品"
    }
  ]
}
```

## 测试

运行测试文件：

```bash
python3 test_npc.py
```

## 注意事项

1. **门派限制**：某些 NPC 只与特定门派弟子交互
2. **等级限制**：某些 NPC 和商品有等级要求
3. **隐藏 NPC**：某些 NPC 需要满足特定条件才会出现
4. **稀有商品**：稀有商品有概率出现在商店中
5. **库存管理**：注意商品的库存限制

---

**版本：** 1.0.0  
**作者：** 蜀山剑侠传开发团队  
**更新日期：** 2026-04-22
