# ⚔️ 蜀山剑侠传

> 横板动作游戏 - 基于《蜀山剑侠传》世界观的仙侠Metroidvania

[![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue.svg)](https://github.com/tancau/shushan-game)
[![Engine](https://img.shields.io/badge/engine-Godot_4.x-478cbf.svg)](https://godotengine.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 🎮 游戏简介

《蜀山剑侠传》是一款基于还珠楼主同名小说改编的横板动作游戏（Side-scrolling Metroidvania）。玩家扮演初入修真界的弟子，在广袤的蜀山世界中探索、战斗、修炼，从练气期菜鸟成长为渡劫飞升的剑仙。

### 核心玩法

- **流畅战斗** - 轻攻击连击/重攻击破甲/法宝技能/功法特技，连击越高伤害越猛
- **深度探索** - 连通式世界地图，境界解锁新能力通往新区域
- **境界成长** - 每次境界突破解锁新操控能力（二段跳/御剑/飞行/瞬移）
- **五行博弈** - 金木水火土实时克制，灵活切换法宝应对不同敌人
- **剑仙之路** - 练气→筑基→金丹→元婴→化神→合体→渡劫→飞升

### 参考作品

《空洞骑士》·《死亡细胞》·《奥日》·《盐与避难所》

---

## ✨ 核心系统

### 战斗系统

| 系统 | 说明 |
|------|------|
| 轻攻击连击 | 四段连击，第4段释放剑气波 |
| 重攻击 | 快速重击(破防)/蓄力重击(破甲+眩晕)/跳跃重击(AOE)/冲刺重击(穿透) |
| 连击加成 | 5/10/20/50/100连击阶梯增伤，最高+75% |
| 法宝技能 | 3个法宝槽位(U/I/O键)，剑/印/镜/特殊类 |
| 功法特技 | 大招级技能(L键)，消耗大量真元 |
| 五行克制 | 金克木/木克土/土克水/水克火/火克金，克制+50%伤害 |
| 异常状态 | 灼烧/冰冻/麻痹/中毒/定身/流血/眩晕/减速 |

### 修炼与境界

| 境界 | 解锁能力 | 属性倍率 |
|------|---------|---------|
| 练气期 | 基础动作 | 1.0x |
| 筑基期 | 二段跳 + 墙壁滑行 | 1.3x |
| 金丹期 | 御剑冲刺 + 空中冲刺跳 | 1.7x |
| 元婴期 | 元神出窍(2s无敌+穿墙) | 2.2x |
| 化神期 | 飞行(5s限时) | 2.8x |
| 合体期 | 瞬移闪避 | 3.5x |
| 渡劫期 | 天劫模式(全属性x3) | 5.0x |

### 技能树（三大流派）

| 流派 | 风格 | 代表功法 |
|------|------|---------|
| 剑修 | 近战连击+高机动 | 峨眉剑法/昆仑剑经 |
| 法修 | 远程法术+AOE | 太清一气诀/五行遁术 |
| 体修 | 防御反击+重击 | 金刚不坏体 |

### 世界地图

13个连通区域，从峨眉山出发探索蜀山世界：

峨眉山 → 青城山 → 华山 → 成都府(中枢) → 苗疆 → 昆仑山 → 东海渡口 → 龙宫遗迹 → 西域荒漠 → 血河教 → 昆仑秘境 → 幽冥鬼域 → 天外天

---

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 游戏引擎 | Godot 4.x |
| 编程语言 | GDScript + C#(性能热点) |
| 美术风格 | 水墨仙侠(Shader特效) |
| 目标平台 | PC(Steam) / Web / 移动端 |

---

## 📁 项目结构

```
shushan-game/
+-- project.godot           # Godot项目配置
+-- scenes/                 # 游戏场景
|   +-- player/             # 玩家场景+状态机
|   +-- enemies/            # 敌人+Boss场景
|   +-- levels/             # 各区域关卡
|   +-- ui/                 # HUD/菜单/技能树
|   +-- systems/            # 战斗/修炼/装备/存档
+-- assets/                 # 美术/音效/Shader
+-- data/                   # 游戏数据JSON
+-- docs/                   # 设计文档
```

---

## 📖 设计文档

| 文档 | 内容 |
|------|------|
| [GAME_DESIGN.md](docs/GAME_DESIGN.md) | 总体设计 - 游戏概述/角色控制 |
| [COMBAT_SYSTEM.md](docs/COMBAT_SYSTEM.md) | 战斗系统 - 攻击/连击/伤害/五行/异常 |
| [LEVEL_DESIGN.md](docs/LEVEL_DESIGN.md) | 关卡设计 - 世界地图/区域/机关/Boss战 |
| [PROGRESSION_SYSTEM.md](docs/PROGRESSION_SYSTEM.md) | 成长系统 - 修炼/境界/技能树/法宝/丹药 |
| [ENEMY_DESIGN.md](docs/ENEMY_DESIGN.md) | 敌人系统 - 小怪/精英/Boss设计 |
| [UI_DESIGN.md](docs/UI_DESIGN.md) | 界面设计 - HUD/菜单/视觉风格 |
| [TECH_SPEC.md](docs/TECH_SPEC.md) | 技术规范 - 架构/引擎/开发路线 |

---

## 📝 开发计划

### Phase 1 - 核心原型（4周）

- [ ] 角色控制系统（移动/跳跃/闪避/攻击状态机）
- [ ] 战斗系统（轻连击/重攻击/连击计数/伤害计算）
- [ ] 第一个关卡（峨眉山入口5房间）
- [ ] 第一个Boss（妖狼王3阶段）

### Phase 2 - 系统完善（6周）

- [ ] 7大境界 + 突破Boss
- [ ] 法宝/功法/丹药系统
- [ ] 三大流派技能树

### Phase 3 - 内容扩展（8周）

- [ ] 13个区域关卡设计
- [ ] 20+种敌人 + 15+Boss

### Phase 4 - 打磨上线（4周）

- [ ] 完整UI + 仙侠BGM
- [ ] 测试/优化/发布

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- **还珠楼主** - 《蜀山剑侠传》原作者
- **Team Cherry** - 《空洞骑士》设计灵感
- **Motion Twin** - 《死亡细胞》战斗系统参考
- **开源社区** - Godot引擎及各种开源工具

---

<div align="center">

**⚔️ 剑气纵横三万里，一剑光寒十九洲 ⚔️**

Made with ❤️ by tancau

</div>
