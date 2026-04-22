# 蜀山剑侠传 JRPG - 详细开发计划

> 从Demo到完整游戏的开发路线图

---

## 📊 当前进度

### 已完成 ✅

| 模块 | 状态 | 说明 |
|------|------|------|
| 设计文档 | ✅ | 13个文档，JRPG设计完整 |
| 数据文件 | ✅ | 6个JSON文件 |
| 美术资源 | ✅ | 角色动画、地图、UI |
| 字体文件 | ✅ | 思源宋体 |
| 音频清单 | ✅ | 下载清单已准备 |

### 待完成 ⏳

| 模块 | 状态 | 说明 |
|------|------|------|
| 音频资源 | ⏳ | 待下载 |
| 前端代码 | ❌ | Phaser + Vue |
| 后端API | ❌ | Flask接口 |
| 测试 | ❌ | 功能测试 |

---

## 📅 开发时间线

### 阶段划分

```
Demo (已完成)
    ↓
Phase 1: 核心系统 (2周)
    ↓
Phase 2: 养成系统 (2周)
    ↓
Phase 3: 炼妖系统 (2周)
    ↓
Phase 4: 剧情系统 (2周)
    ↓
Phase 5: 完善优化 (1周)
    ↓
v1.0 发布
```

---

## Phase 1: 核心系统 (Week 1-2)

### 1.1 项目框架 (Day 1-2)

**前端结构**：
```
frontend/
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── scenes/
│   │   ├── BootScene.ts      # 加载资源
│   │   ├── MenuScene.ts      # 主菜单
│   │   ├── MapScene.ts       # 地图探索
│   │   └── BattleScene.ts    # 战斗场景
│   ├── systems/
│   │   ├── AnimationSystem.ts
│   │   ├── AudioSystem.ts
│   │   └── SaveSystem.ts
│   ├── stores/
│   │   ├── playerStore.ts
│   │   └── gameStore.ts
│   └── api/
│       └── index.ts
└── public/
    └── assets/
```

**后端结构**：
```
game/
├── __init__.py
├── player.py
├── combat.py
├── enemy.py
├── map_manager.py
└── battle_manager.py
```

**工时**: 8小时

---

### 1.2 地图系统 (Day 3-5)

**功能清单**：
- [ ] 加载地图数据
- [ ] 渲染地图背景
- [ ] 角色移动（WASD/方向键）
- [ ] 移动动画（使用生成的动画帧）
- [ ] 碰撞检测
- [ ] 遇敌触发（踩地雷）
- [ ] NPC交互
- [ ] 宝箱开启

**技术要点**：
```typescript
// MapScene.ts
class MapScene extends Phaser.Scene {
  preload() {
    // 加载地图背景
    this.load.image('map', 'assets/images/maps/shushan_foot.png');
    
    // 加载角色动画
    this.load.spritesheet('player_idle', 'assets/images/characters/player/idle.png', {
      frameWidth: 128,
      frameHeight: 192
    });
  }
  
  create() {
    // 创建地图
    this.add.image(800, 240, 'map');
    
    // 创建玩家
    this.player = this.physics.add.sprite(100, 400, 'player_idle');
    
    // 创建动画
    this.anims.create({
      key: 'idle',
      frames: this.anims.generateFrameNumbers('player_idle'),
      frameRate: 4,
      repeat: -1
    });
  }
}
```

**工时**: 16小时

---

### 1.3 战斗系统 (Day 6-10)

**功能清单**：
- [ ] 进入战斗场景
- [ ] 显示玩家/敌人
- [ ] 行动菜单（攻击/技能/物品/防御）
- [ ] 技能选择界面
- [ ] 伤害计算（五行克制）
- [ ] 回合制逻辑
- [ ] 战斗动画
- [ ] 伤害数字显示
- [ ] 战斗日志
- [ ] 胜利/失败判定
- [ ] 战利品掉落

**技术要点**：
```typescript
// BattleScene.ts
class BattleScene extends Phaser.Scene {
  async executePlayerTurn(action: string) {
    // 1. 播放攻击动画
    this.player.anims.play('attack');
    
    // 2. 调用后端API计算伤害
    const result = await fetch('/api/battle/action', {
      method: 'POST',
      body: JSON.stringify({ action })
    }).then(r => r.json());
    
    // 3. 显示伤害数字
    this.showDamageNumber(result.damage);
    
    // 4. 更新HP条
    this.updateHPBars(result);
    
    // 5. 敌人回合
    if (!result.battle_end) {
      await this.executeEnemyTurn();
    }
  }
}
```

**后端API**：
```python
# api.py
@app.route('/api/battle/start', methods=['POST'])
def start_battle():
    enemy_id = request.json.get('enemy_id')
    enemy = load_enemy(enemy_id)
    return jsonify({
        'player': player.to_dict(),
        'enemy': enemy.to_dict()
    })

@app.route('/api/battle/action', methods=['POST'])
def battle_action():
    action = request.json.get('action')
    result = battle_manager.execute(action)
    return jsonify(result)
```

**工时**: 24小时

---

### 1.4 UI系统 (Day 11-14)

**功能清单**：
- [ ] 主菜单界面
- [ ] 游戏HUD（HP/MP/等级）
- [ ] 战斗UI
- [ ] 菜单界面（角色/物品/技能）
- [ ] 对话框系统
- [ ] 提示信息

**工时**: 16小时

---

## Phase 2: 养成系统 (Week 3-4)

### 2.1 境界系统 (Day 15-17)

**功能清单**：
- [ ] 修为获取（战斗/任务）
- [ ] 境界升级
- [ ] 境界突破（Boss战）
- [ ] 境界加成计算

**数据结构**：
```typescript
interface Realm {
  name: string;        // 练气期
  expRequired: number; // 修为需求
  bonus: number;       // 属性加成
  skills: string[];    // 解锁技能
}
```

**工时**: 12小时

---

### 2.2 法宝系统 (Day 18-20)

**功能清单**：
- [ ] 法宝装备
- [ ] 法宝强化
- [ ] 法宝技能

**工时**: 12小时

---

### 2.3 功法系统 (Day 21-22)

**功能清单**：
- [ ] 功法学习
- [ ] 功法升级
- [ ] 技能栏管理

**工时**: 8小时

---

### 2.4 灵兽系统基础 (Day 23-28)

**功能清单**：
- [ ] 灵兽捕捉
- [ ] 灵兽装备
- [ ] 灵兽战斗召唤
- [ ] 灵兽培养

**工时**: 16小时

---

## Phase 3: 炼妖系统 (Week 5-6)

### 3.1 炼化系统 (Day 29-32)

**功能清单**：
- [ ] 炼化界面
- [ ] 配方匹配
- [ ] 炼化成功率
- [ ] 产出物品

**工时**: 12小时

---

### 3.2 灵兽进化 (Day 33-35)

**功能清单**：
- [ ] 进化材料
- [ ] 进化动画
- [ ] 属性提升

**工时**: 8小时

---

## Phase 4: 剧情系统 (Week 7-8)

### 4.1 主线剧情 (Day 36-40)

**功能清单**：
- [ ] 序章（新手教学）
- [ ] 第一章（门派选择）
- [ ] 第二章（修炼成长）
- [ ] 第三章（门派冲突）

**工时**: 20小时

---

### 4.2 支线任务 (Day 41-43)

**功能清单**：
- [ ] 任务接取
- [ ] 任务追踪
- [ ] 任务奖励

**工时**: 12小时

---

### 4.3 多结局系统 (Day 44-45)

**功能清单**：
- [ ] 结局判定
- [ ] 结局动画
- [ ] 结局奖励

**工时**: 8小时

---

## Phase 5: 完善优化 (Week 9)

### 5.1 音效集成 (Day 46-47)

**功能清单**：
- [ ] BGM播放
- [ ] 音效触发
- [ ] 音量控制

**工时**: 8小时

---

### 5.2 存档系统 (Day 48-49)

**功能清单**：
- [ ] 本地存档
- [ ] 云端存档（可选）
- [ ] 多存档槽

**工时**: 8小时

---

### 5.3 性能优化 (Day 50-52)

**优化项**：
- [ ] 资源预加载
- [ ] 对象池
- [ ] 内存管理
- [ ] 帧率优化

**工时**: 12小时

---

### 5.4 Bug修复 (Day 53-56)

**测试项**：
- [ ] 功能测试
- [ ] 兼容性测试
- [ ] 性能测试

**工时**: 16小时

---

## 📊 总工时估算

| Phase | 工时 | 天数 |
|-------|------|------|
| Phase 1: 核心系统 | 64小时 | 14天 |
| Phase 2: 养成系统 | 48小时 | 14天 |
| Phase 3: 炼妖系统 | 20小时 | 7天 |
| Phase 4: 剧情系统 | 40小时 | 10天 |
| Phase 5: 完善优化 | 44小时 | 11天 |
| **总计** | **216小时** | **56天** |

**每日投入4小时，预计约2个月完成**

---

## 🎯 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|------|--------|
| **M1: Demo完成** | 现在 | 可运行Demo |
| **M2: 核心完成** | 2周后 | 地图+战斗完整 |
| **M3: 养成完成** | 4周后 | 境界/法宝/灵兽 |
| **M4: 炼妖完成** | 6周后 | 炼化系统 |
| **M5: 剧情完成** | 8周后 | 多线剧情 |
| **M6: 1.0发布** | 9周后 | 完整游戏 |

---

## 🔧 技术栈

| 层级 | 技术 |
|------|------|
| **前端引擎** | Phaser 3.70+ |
| **UI框架** | Vue 3.4+ |
| **状态管理** | Pinia |
| **后端** | Flask 3.0+ |
| **数据** | JSON |

---

## 📝 开发规范

### Git分支

```
main        # 主分支
develop     # 开发分支
feature/*   # 功能分支
bugfix/*    # 修复分支
release/*   # 发布分支
```

### 提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

---

## 🚀 下一步行动

1. **下载音频资源**（BGM + 音效）
2. **实现BootScene**（加载资源）
3. **实现MenuScene**（主菜单）
4. **实现MapScene**（地图探索）

---

*文档版本：v1.0*
*创建日期：2026-04-22*
