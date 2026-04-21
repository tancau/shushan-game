# 蜀山剑侠传 - 完整 API 文档

## 📊 API 概览

**Base URL:** https://shushan-game.vercel.app

**总路由数:** 33 个

**支持系统:** 19 个游戏模块全覆盖

---

## 🔗 API 列表

### 1. 核心系统（11个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/status` | 获取玩家状态 |
| GET | `/api/cultivate` | 修炼 |
| GET | `/api/advance` | 突破境界 |
| GET | `/api/battle` | 战斗 |
| GET | `/api/explore` | 探索 |
| GET | `/api/artifacts` | 法宝列表 |
| GET | `/api/skills` | 功法列表 |
| GET | `/api/quests` | 任务列表 |
| GET | `/api/map` | 地图 |
| POST | `/api/travel` | 移动 |

### 2. 灵兽系统（3个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/spirit-beasts` | 获取灵兽列表 |
| POST | `/api/spirit-beast/capture` | 捕捉灵兽 |
| POST | `/api/spirit-beast/<id>/feed` | 喂养灵兽 |

### 3. 天劫系统（2个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/tribulation/status` | 天劫状态 |
| POST | `/api/tribulation/start` | 开始渡劫 |

### 4. 道心系统（2个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/dao-heart` | 道心信息 |
| GET | `/api/merit-shop` | 功德商店 |

### 5. 排行榜（1个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/leaderboard/<type>` | 排行榜（power/cultivation/realm/wealth/achievement） |

### 6. 副本系统（2个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/dungeons` | 副本列表 |
| POST | `/api/dungeon/<id>/enter` | 进入副本 |

### 7. 活动系统（2个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/events` | 活动列表 |
| POST | `/api/sign-in` | 每日签到 |

### 8. 好友系统（3个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/friends` | 好友列表 |
| POST | `/api/friend/add` | 添加好友 |
| POST | `/api/friend/gift` | 赠送礼物 |

### 9. 成就系统（4个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/achievements` | 成就列表 |
| GET | `/api/achievements/check` | 检查成就 |
| GET | `/api/achievements/summary` | 成就概要 |
| POST | `/api/achievements/<id>/claim` | 领取奖励 |

### 10. 称号系统（3个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/titles` | 称号列表 |
| POST | `/api/titles/<id>/equip` | 装备称号 |
| POST | `/api/titles/remove` | 移除称号 |

---

## 📝 详细说明

### 玩家状态

**GET** `/api/status`

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
  "location": "峨眉山脚"
}
```

### 灵兽捕捉

**POST** `/api/spirit-beast/capture`

```json
{
  "success": true,
  "message": "成功捕捉 青龙！",
  "beast": {
    "name": "青龙",
    "type": "神兽",
    "level": 1,
    "affection": 0
  }
}
```

### 天劫状态

**GET** `/api/tribulation/status`

```json
{
  "success": true,
  "realm": "练气期",
  "can_attempt": true,
  "next_tribulation": "练气期天劫"
}
```

### 排行榜

**GET** `/api/leaderboard/power`

```json
{
  "success": true,
  "type": "power",
  "leaderboard": [
    {"rank": 1, "name": "剑圣", "value": 99999},
    {"rank": 2, "name": "tancau", "value": 1000}
  ]
}
```

---

## 🎯 使用示例

### JavaScript (Axios)

```javascript
import axios from 'axios'

const API_BASE = 'https://shushan-game.vercel.app/api'

// 获取状态
const status = await axios.get(`${API_BASE}/status`)

// 修炼
const result = await axios.get(`${API_BASE}/cultivate`)

// 捕捉灵兽
const beast = await axios.post(`${API_BASE}/spirit-beast/capture`)

// 移动
await axios.post(`${API_BASE}/travel`, { location: '成都府' })
```

### Python (requests)

```python
import requests

API_BASE = 'https://shushan-game.vercel.app/api'

# 获取状态
status = requests.get(f'{API_BASE}/status').json()

# 修炼
result = requests.get(f'{API_BASE}/cultivate').json()

# 捕捉灵兽
beast = requests.post(f'{API_BASE}/spirit-beast/capture').json()
```

---

## ⚠️ 注意事项

1. **玩家ID** - 当前固定为 'tancau'
2. **数据保存** - 所有修改自动保存
3. **跨域** - 已配置 CORS
4. **缓存** - 建议状态数据缓存 1-5 秒

---

*更新时间: 2026-04-22*
*版本: v0.5.0 完整版*
