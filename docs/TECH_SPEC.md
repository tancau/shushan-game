# 技术规范文档

> 蜀山剑侠传 - JRPG技术架构

---

## 一、技术选型

### 1.1 前端技术

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| **游戏引擎** | Phaser 3 | 3.70+ | 2D游戏引擎 |
| **UI框架** | Vue 3 | 3.4+ | 用户界面 |
| **状态管理** | Pinia | 2.1+ | 数据状态 |
| **构建工具** | Vite | 5.0+ | 前端构建 |
| **语言** | TypeScript | 5.0+ | 类型支持 |

### 1.2 后端技术

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| **框架** | Flask | 3.0+ | Python Web框架 |
| **API** | RESTful | - | 接口设计 |
| **数据存储** | JSON | - | 本地存储 |
| **语言** | Python | 3.10+ | 后端语言 |

---

## 二、项目结构

```
shushan-game/
├── docs/                    # 设计文档
│   ├── GAME_DESIGN.md
│   ├── MAP_SYSTEM.md
│   ├── BATTLE_SYSTEM.md
│   └── ...
├── game/                    # 后端游戏逻辑
│   ├── __init__.py
│   ├── player.py           # 玩家系统
│   ├── combat.py           # 战斗系统
│   ├── enemy.py            # 敌人系统
│   └── battle_manager.py   # 战斗管理
├── data/                    # 数据文件
│   ├── enemies.json        # 敌人数据
│   ├── skills.json         # 技能数据
│   ├── items.json          # 物品数据
│   └── maps.json           # 地图数据
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── scenes/         # Phaser场景
│   │   │   ├── MenuScene.ts
│   │   │   ├── MapScene.ts
│   │   │   └── BattleScene.ts
│   │   ├── components/     # Vue组件
│   │   ├── stores/         # 状态管理
│   │   └── api/            # API封装
│   └── public/             # 静态资源
├── assets/                  # 美术资源
│   ├── images/             # 图片
│   ├── audio/              # 音效
│   └── fonts/              # 字体
├── api.py                   # API入口
├── main.py                  # 游戏入口
└── README.md
```

---

## 三、API设计

### 3.1 API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/player` | GET/POST | 玩家数据 |
| `/api/battle/start` | POST | 开始战斗 |
| `/api/battle/action` | POST | 战斗行动 |
| `/api/map` | GET | 地图数据 |
| `/api/save` | POST | 保存进度 |
| `/api/load` | GET | 加载进度 |

### 3.2 数据格式

**战斗请求**：
```json
{
  "action": "attack",
  "target": "enemy_01",
  "skill": "sword_slash"
}
```

**战斗响应**：
```json
{
  "damage": 150,
  "critical": true,
  "enemy_hp": 350,
  "combo": 5,
  "log": "主角使用剑斩，造成150点暴击伤害！"
}
```

---

## 四、状态管理

### 4.1 游戏状态

```typescript
interface GameState {
  player: Player;
  currentMap: string;
  battleState: BattleState | null;
  inventory: Item[];
  quests: Quest[];
  settings: Settings;
}
```

### 4.2 玩家状态

```typescript
interface Player {
  name: string;
  level: number;
  realm: string;
  hp: number;
  mp: number;
  attack: number;
  defense: number;
  speed: number;
  skills: Skill[];
}
```

---

## 五、部署方案

### 5.1 开发环境

```bash
# 后端
pip install flask flask-cors
python api.py

# 前端
cd frontend
npm install
npm run dev
```

### 5.2 生产环境

| 平台 | 用途 |
|------|------|
| **Vercel** | 前端部署 |
| **Railway** | 后端部署 |
| **GitHub** | 代码托管 |

---

## 六、性能优化

### 6.1 资源优化

| 优化项 | 方法 |
|--------|------|
| **图片** | 压缩、懒加载 |
| **音频** | 按需加载 |
| **数据** | 分块加载 |

### 6.2 渲染优化

| 优化项 | 方法 |
|--------|------|
| **地图渲染** | 视口裁剪 |
| **动画** | 对象池 |
| **UI更新** | 虚拟列表 |

---

## 七、开发计划

### Phase 1: 核心系统 (Day 1-7)
- [ ] 项目结构搭建
- [ ] 地图系统
- [ ] 战斗系统

### Phase 2: 素材集成 (Day 8-11)
- [ ] 美术资源
- [ ] 音频资源

### Phase 3: UI系统 (Day 12-13)
- [ ] 主菜单
- [ ] 战斗UI

### Phase 4: 测试优化 (Day 14)
- [ ] 功能测试
- [ ] 性能优化

---

*文档版本：v2.0.0-alpha*
*最后更新：2026-04-22*
