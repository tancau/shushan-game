# 蜀山剑侠传 - API 文档

## 基础信息

**Base URL:** https://shushan-game.vercel.app

**玩家ID:** 默认使用 'tancau'

---

## 通用响应格式

```json
{
  "success": true/false,
  "message": "提示信息",
  "data": { ... }
}
```

---

## 核心 API

### 1. 玩家状态

**GET** `/api/status`

获取玩家当前状态

**响应：**
```json
{
  "success": true,
  "name": "tancau",
  "realm": "练气期",
  "cultivation": "1,000",
  "hp": "100/100",
  "mp": "95/100",
  "spirit_stones": "100",
  "sect": "峨眉派",
  "location": "峨眉山脚",
  "equipped_artifact": "青竹剑"
}
```

---

### 2. 修炼

**GET** `/api/cultivate`

进行修炼

**响应：**
```json
{
  "success": true,
  "message": "吐纳天地灵气，获得修为 +22"
}
```

---

### 3. 突破境界

**GET** `/api/advance`

尝试突破境界

**响应：**
```json
{
  "success": true,
  "message": "🎉 恭喜突破至筑基期！"
}
```

---

### 4. 战斗

**GET** `/api/battle`

与随机敌人战斗

**响应：**
```json
{
  "success": true,
  "message": "战斗胜利！修为 +500，灵石 +100"
}
```

---

### 5. 探索

**GET** `/api/explore`

探索当前位置

**响应：**
```json
{
  "success": true,
  "message": "探索事件: 宝物 - 发现了珍贵的灵草"
}
```

---

### 6. 法宝列表

**GET** `/api/artifacts`

获取玩家法宝列表

**响应：**
```json
{
  "success": true,
  "artifacts": [
    {
      "name": "青竹剑",
      "power": 100,
      "element": "木",
      "description": "入门级飞剑"
    }
  ]
}
```

---

### 7. 功法列表

**GET** `/api/skills`

获取已学功法

**响应：**
```json
{
  "success": true,
  "skills": [
    {
      "name": "峨眉剑法",
      "type": "辅修",
      "quality": "灵"
    }
  ]
}
```

---

### 8. 任务列表

**GET** `/api/quests`

获取任务列表

**响应：**
```json
{
  "success": true,
  "quests": [
    {
      "id": "quest_001",
      "name": "初入蜀山",
      "type": "主线",
      "status": "进行中"
    }
  ]
}
```

---

### 9. 地图

**GET** `/api/map`

获取可访问的地图地点

**响应：**
```json
{
  "success": true,
  "locations": [
    {
      "name": "峨眉山",
      "region": "中原",
      "danger": 1
    }
  ]
}
```

---

### 10. 移动

**POST** `/api/travel`

移动到指定地点

**请求：**
```json
{
  "location": "成都府"
}
```

**响应：**
```json
{
  "success": true,
  "message": "已到达成都府"
}
```

---

### 11. 成就列表

**GET** `/api/achievements`

获取成就列表

**响应：**
```json
{
  "success": true,
  "achievements": [
    {
      "id": "ach_001",
      "name": "初入仙门",
      "description": "开始修真之路",
      "completed": true
    }
  ]
}
```

---

## 高级 API（需实现）

### 灵兽系统
- `GET /api/spirit-beasts` - 获取灵兽列表
- `POST /api/spirit-beast/capture` - 捕捉灵兽
- `POST /api/spirit-beast/feed` - 喂养灵兽

### 天劫系统
- `GET /api/tribulation/status` - 天劫状态
- `POST /api/tribulation/start` - 开始渡劫

### 道心系统
- `GET /api/dao-heart` - 获取道心信息
- `GET /api/merit-shop` - 功德商店

### 排行榜
- `GET /api/leaderboard/<type>` - 获取排行榜

### 副本
- `GET /api/dungeons` - 副本列表
- `POST /api/dungeon/enter` - 进入副本

### 活动
- `GET /api/events` - 活动列表
- `POST /api/sign-in` - 每日签到

### 好友
- `GET /api/friends` - 好友列表
- `POST /api/friend/add` - 添加好友
- `POST /api/friend/gift` - 赠送礼物

---

## 错误处理

所有 API 在失败时返回：

```json
{
  "success": false,
  "error": "错误信息"
}
```

---

## 开发建议

1. **缓存策略** - 玩家状态可缓存 1-5 秒
2. **错误重试** - 网络错误自动重试 3 次
3. **加载状态** - 所有 API 调用显示加载动画
4. **离线支持** - 关键数据可本地存储

---

*更新时间: 2026-04-22*
