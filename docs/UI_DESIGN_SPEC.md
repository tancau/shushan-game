# 蜀山剑侠传 - UI设计方案

> 版本：v1.0.0 | 日期：2026-04-22 | 状态：设计稿阶段

---

## 一、项目分析总结

### 1.1 项目定位

《蜀山剑侠传》是一款基于还珠楼主同名小说改编的**文字修仙养成游戏**。玩家扮演修真弟子，通过修炼、探索、战斗逐步成长为一代仙侠。

### 1.2 技术架构

| 层级 | 技术栈 | 状态 |
|------|--------|------|
| 后端 | Python 3.10 + Flask | 已完成 (33个API) |
| 数据存储 | JSON文件 | 已完成 |
| 前端框架 | Vue 3 (计划中) | 待开发 |
| UI组件库 | Element Plus (计划中) | 待开发 |
| 部署 | Vercel | 已完成 |

### 1.3 核心系统模块 (19个)

```
核心养成：修炼、法宝、功法、炼丹炼器
探索冒险：地图探索、副本、奇遇、天劫
社交竞技：好友、排行榜、门派战
辅助系统：任务、成就、道心、灵兽、阵法、NPC、商店、活动
```

### 1.4 目标用户画像

| 维度 | 特征 |
|------|------|
| 年龄层 | 18-35岁 |
| 性别倾向 | 男性为主 (70%)，女性用户增长中 |
| 兴趣标签 | 仙侠文化、国风美学、放置养成、策略战斗 |
| 游戏习惯 | 碎片化时间、轻度操作、重视成长反馈 |
| 审美偏好 | 水墨国风、古典雅致、仙气飘渺 |
| 设备分布 | 移动端60% / PC端40% |

---

## 二、整体视觉风格定义

### 2.1 设计主题

**「水墨仙侠 · 意境修真」**

以中国传统水墨画为视觉基调，融合仙侠世界的飘渺意境，营造沉浸式修真体验。界面设计追求"虚实相生、留白意境"的东方美学。

### 2.2 色彩系统

#### 主色调

```css
/* 品牌主色 - 青冥之色 */
--color-primary: #2D5A7B;        /* 青冥蓝 - 主品牌色 */
--color-primary-light: #4A8BB5;   /* 浅青冥 - 悬停/高亮 */
--color-primary-dark: #1A3A52;    /* 深青冥 - 按压/阴影 */

/* 辅助色 */
--color-secondary: #8B6914;       /* 古铜金 - 强调/奖励 */
--color-secondary-light: #C4A35A; /* 浅金色 - 悬停 */
--color-accent: #C0392B;          /* 朱砂红 - 警告/战斗 */
--color-success: #27AE60;         /* 翡翠绿 - 成功/生命 */
--color-info: #5DADE2;            /* 天青蓝 - 信息提示 */
```

#### 五行色彩体系

```css
/* 五行对应色 - 贯穿游戏核心机制 */
--element-metal: #B8B8B8;         /* 金 - 银白 */
--element-wood: #27AE60;          /* 木 - 翠绿 */
--element-water: #2E86AB;         /* 水 - 湛蓝 */
--element-fire: #E74C3C;          /* 火 - 赤红 */
--element-earth: #8B4513;         /* 土 - 赭石 */
```

#### 境界色彩阶梯

```css
/* 境界对应色 - 视觉成长反馈 */
--realm-1: #95A5A6;               /* 练气期 - 灰白 */
--realm-2: #27AE60;               /* 筑基期 - 翠绿 */
--realm-3: #F39C12;               /* 金丹期 - 金黄 */
--realm-4: #E74C3C;               /* 元婴期 - 赤红 */
--realm-5: #9B59B6;               /* 化神期 - 紫霞 */
--realm-6: #3498DB;               /* 合体期 - 天蓝 */
--realm-7: #FFD700;               /* 渡劫期 - 金芒 */
```

#### 中性色阶

```css
--bg-primary: #0F1419;            /* 主背景 - 墨夜 */
--bg-secondary: #1A1F2E;          /* 次级背景 - 深靛 */
--bg-card: #242B3D;               /* 卡片背景 - 暗蓝灰 */
--bg-hover: #2E364A;              /* 悬停背景 */
--bg-overlay: rgba(0,0,0,0.7);    /* 遮罩层 */

--text-primary: #E8E4DC;          /* 主文字 - 米白 */
--text-secondary: #9CA3AF;        /* 次级文字 - 银灰 */
--text-muted: #6B7280;            /* 弱化文字 - 灰蓝 */
--text-gold: #D4AF37;             /* 金色文字 - 奖励/品质 */

--border-default: rgba(255,255,255,0.1);
--border-gold: rgba(212,175,55,0.3);
--border-active: rgba(74,139,181,0.5);
```

### 2.3 字体规范

#### 中文字体栈

```css
/* 标题字体 - 书法风格 */
--font-title: "Noto Serif SC", "Source Han Serif SC", "SimSun", serif;

/* 正文字体 - 清晰易读 */
--font-body: "Noto Sans SC", "Source Han Sans SC", "Microsoft YaHei", sans-serif;

/* 数字/数据字体 - 等宽 */
--font-mono: "JetBrains Mono", "Fira Code", "Consolas", monospace;

/* 装饰字体 - 古风 */
--font-decorative: "ZCOOL XiaoWei", "Ma Shan Zheng", cursive;
```

#### 字号规范

| 层级 | 字号 | 字重 | 用途 |
|------|------|------|------|
| H1 | 32px / 2rem | 700 | 页面主标题、境界名称 |
| H2 | 24px / 1.5rem | 600 | 区块标题、系统名称 |
| H3 | 18px / 1.125rem | 600 | 卡片标题、功能名称 |
| H4 | 16px / 1rem | 500 | 小标题、标签 |
| Body | 14px / 0.875rem | 400 | 正文内容、描述 |
| Small | 12px / 0.75rem | 400 | 辅助信息、时间戳 |
| Caption | 11px / 0.6875rem | 400 | 标签、徽章文字 |

#### 行高规范

```css
--line-height-tight: 1.25;    /* 标题 */
--line-height-normal: 1.5;    /* 正文 */
--line-height-relaxed: 1.75;  /* 描述文本 */
```

### 2.4 图标体系

#### 图标风格

- **风格**：线性图标 + 国风装饰元素
- **描边**：1.5px - 2px
- **端点**：圆角端点
- **尺寸**：16px(小) / 20px(中) / 24px(大) / 32px(超大)

#### 核心图标映射

| 系统 | 图标语义 | 视觉元素 |
|------|----------|----------|
| 修炼 | 打坐/莲花 | 莲花座、灵气波纹 |
| 法宝 | 剑/器 | 飞剑、鼎炉 |
| 功法 | 卷轴/书 | 竹简、古籍 |
| 战斗 | 剑交叉 | 双剑、战意 |
| 地图 | 山水/罗盘 | 山峰、指南针 |
| 任务 | 卷轴/旗 | 令旗、卷轴 |
| 灵兽 | 神兽轮廓 | 龙、凤、麒麟 |
| 道心 | 太极/心 | 太极图、心形 |
| 好友 | 双人 | 并立人形 |
| 商店 | 铜钱/袋 | 古钱币、钱袋 |
| 成就 | 勋章/星 | 五角星、奖牌 |
| 排行榜 | 榜单/ crown | 榜单、crown |

---

## 三、页面布局结构

### 3.1 整体布局框架

```
┌─────────────────────────────────────────────────────────┐
│  [顶部导航栏]  角色信息 | 资源栏 | 系统通知 | 设置       │  56px
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [左侧边栏]          [主内容区域]          [右侧边栏]   │
│  168px               flex-1                  280px      │
│  ┌─────────┐        ┌─────────────────┐    ┌────────┐ │
│  │ 主菜单   │        │                 │    │ 角色   │ │
│  │ 修炼     │        │   页面核心内容   │    │ 状态   │ │
│  │ 法宝     │        │                 │    │ 面板   │ │
│  │ 功法     │        │                 │    │        │ │
│  │ 探索     │        │                 │    │ 快捷   │ │
│  │ 战斗     │        │                 │    │ 操作   │ │
│  │ ...      │        │                 │    │        │ │
│  └─────────┘        └─────────────────┘    └────────┘ │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  [底部信息栏]  当前位置 | 在线状态 | 版本信息            │  40px
└─────────────────────────────────────────────────────────┘
```

### 3.2 布局参数

```css
/* 布局尺寸 */
--layout-header-height: 56px;
--layout-footer-height: 40px;
--layout-sidebar-left: 168px;
--layout-sidebar-right: 280px;
--layout-content-padding: 24px;
--layout-gap: 16px;

/* 响应式断点 */
--bp-mobile: 640px;      /* 手机端 */
--bp-tablet: 1024px;     /* 平板端 */
--bp-desktop: 1440px;    /* 桌面端 */
--bp-wide: 1920px;       /* 宽屏端 */
```

### 3.3 页面清单与结构

| 页面 | 路由 | 布局类型 | 核心内容 |
|------|------|----------|----------|
| 登录/注册 | /auth | 全屏居中 | 角色创建、门派选择 |
| 主界面 | / | 三栏布局 | 修炼主面板 |
| 角色状态 | /status | 三栏布局 | 属性详情、装备展示 |
| 修炼 | /cultivate | 三栏布局 | 修炼方式、突破界面 |
| 法宝 | /artifacts | 三栏布局 | 法宝列表、装备、强化 |
| 功法 | /skills | 三栏布局 | 功法树、学习、升级 |
| 世界地图 | /map | 全屏地图 | 区域地图、地点详情 |
| 探索 | /explore | 三栏布局 | 探索事件、资源采集 |
| 战斗 | /combat | 全屏沉浸 | 回合制战斗界面 |
| 副本 | /dungeons | 三栏布局 | 副本列表、挑战 |
| 任务 | /quests | 三栏布局 | 任务追踪、奖励 |
| 灵兽 | /spirit-beasts | 三栏布局 | 灵兽列表、培养 |
| 道心 | /dao-heart | 三栏布局 | 功德业力、商店 |
| 好友 | /friends | 三栏布局 | 好友列表、互动 |
| 排行榜 | /leaderboard | 三栏布局 | 榜单展示 |
| 成就 | /achievements | 三栏布局 | 成就墙、称号 |
| 商店 | /shop | 三栏布局 | 商品列表、交易 |
| 设置 | /settings | 居中弹窗 | 系统设置 |

---

## 四、交互设计模式

### 4.1 核心交互原则

1. **即时反馈**：所有操作在300ms内给出视觉反馈
2. **渐进披露**：复杂系统分层展示，避免信息过载
3. **手势友好**：移动端支持滑动、长按等手势
4. **一致性**：相同操作在不同页面保持统一反馈

### 4.2 交互状态定义

```css
/* 按钮状态 */
--btn-hover-translate: translateY(-1px);
--btn-active-scale: scale(0.98);
--btn-transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);

/* 卡片状态 */
--card-hover-shadow: 0 8px 24px rgba(0,0,0,0.3);
--card-hover-border: rgba(212,175,55,0.3);
--card-transition: all 0.3s ease;

/* 页面转场 */
--page-transition: opacity 0.3s ease, transform 0.3s ease;
--modal-transition: opacity 0.2s ease, backdrop-filter 0.2s ease;
```

### 4.3 关键交互模式

#### 修炼交互

```
1. 点击修炼按钮 → 按钮涟漪动画
2. 播放修炼动画（灵气汇聚特效）
3. 修为数值滚动增加
4. 若可突破 → 境界图标闪烁提示
5. 连续修炼支持长按/自动模式
```

#### 战斗交互

```
1. 进入战斗 → 全屏切换动画（剑光划过）
2. 回合制操作 → 技能选择面板滑入
3. 释放技能 → 对应五行特效动画
4. 伤害数字 → 浮动弹出 + 屏幕震动
5. 战斗结束 → 战利品展示动画
```

#### 地图探索交互

```
1. 点击地图节点 → 节点高亮 + 路径绘制
2. 确认移动 → 角色图标沿路径移动动画
3. 到达地点 → 地点信息卡片弹出
4. 探索操作 → 随机事件动画展示
```

### 4.4 动效规范

```css
/* 缓动函数 */
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-decelerate: cubic-bezier(0, 0, 0.2, 1);
--ease-accelerate: cubic-bezier(0.4, 0, 1, 1);
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

/* 持续时间 */
--duration-instant: 100ms;
--duration-fast: 200ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
--duration-dramatic: 800ms;

/* 特殊动效 */
--float-animation: float 3s ease-in-out infinite;
--glow-animation: glow 2s ease-in-out infinite alternate;
--pulse-animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
```

---

## 五、响应式适配策略

### 5.1 断点策略

```css
/* 移动端优先设计 */

/* 手机端 (<=640px) */
@media (max-width: 640px) {
  --layout-sidebar-left: 0;      /* 左侧栏隐藏为抽屉 */
  --layout-sidebar-right: 0;     /* 右侧栏隐藏为标签页 */
  --layout-content-padding: 12px;
  --card-columns: 1;             /* 单列卡片 */
}

/* 平板端 (641px-1024px) */
@media (min-width: 641px) and (max-width: 1024px) {
  --layout-sidebar-left: 64px;   /* 图标模式侧边栏 */
  --layout-sidebar-right: 240px;
  --layout-content-padding: 16px;
  --card-columns: 2;
}

/* 桌面端 (1025px-1440px) */
@media (min-width: 1025px) and (max-width: 1440px) {
  --layout-sidebar-left: 168px;
  --layout-sidebar-right: 260px;
  --layout-content-padding: 20px;
  --card-columns: 3;
}

/* 宽屏端 (>1440px) */
@media (min-width: 1441px) {
  --layout-sidebar-left: 200px;
  --layout-sidebar-right: 320px;
  --layout-content-padding: 24px;
  --card-columns: 4;
  --layout-max-width: 1600px;
}
```

### 5.2 移动端适配要点

| 元素 | 桌面端 | 移动端 |
|------|--------|--------|
| 导航 | 左侧固定侧边栏 | 底部Tab栏 + 抽屉菜单 |
| 角色面板 | 右侧固定 | 顶部折叠面板 |
| 卡片网格 | 3-4列 | 1-2列 |
| 战斗界面 | 左右分栏 | 上下分栏 |
| 地图 | 全屏可缩放 | 全屏手势操作 |
| 操作按钮 | 悬停提示 | 长按菜单 |

### 5.3 触摸交互优化

```css
/* 触摸目标最小尺寸 */
--touch-target-min: 44px;

/* 手势支持 */
--swipe-threshold: 50px;       /* 滑动阈值 */
--long-press-duration: 500ms;  /* 长按时间 */
--double-tap-interval: 300ms;  /* 双击间隔 */
```

---

## 六、组件库设计规范

### 6.1 基础组件

#### 按钮 (Button)

```css
/* 主按钮 */
.btn-primary {
  background: linear-gradient(135deg, #2D5A7B, #4A8BB5);
  color: #E8E4DC;
  border: 1px solid rgba(74,139,181,0.5);
  border-radius: 8px;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(45,90,123,0.4);
}

/* 金色强调按钮 */
.btn-gold {
  background: linear-gradient(135deg, #8B6914, #C4A35A);
  border: 1px solid rgba(212,175,55,0.5);
}

/* 危险按钮 */
.btn-danger {
  background: linear-gradient(135deg, #922B21, #C0392B);
}

/* 幽灵按钮 */
.btn-ghost {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.2);
}
```

#### 卡片 (Card)

```css
.card {
  background: linear-gradient(180deg, #242B3D, #1A1F2E);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 16px;
  transition: all 0.3s ease;
}
.card:hover {
  border-color: rgba(212,175,55,0.2);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.card--highlight {
  border-color: rgba(212,175,55,0.3);
  background: linear-gradient(180deg, #2E364A, #242B3D);
}
```

#### 输入框 (Input)

```css
.input {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 10px 14px;
  color: #E8E4DC;
  font-size: 14px;
  transition: all 0.2s ease;
}
.input:focus {
  border-color: rgba(74,139,181,0.5);
  box-shadow: 0 0 0 3px rgba(74,139,181,0.1);
  outline: none;
}
```

### 6.2 游戏专用组件

#### 属性条 (StatBar)

```css
.stat-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}
.stat-bar__track {
  flex: 1;
  height: 8px;
  background: rgba(0,0,0,0.4);
  border-radius: 4px;
  overflow: hidden;
}
.stat-bar__fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}
.stat-bar__fill--hp { background: linear-gradient(90deg, #27AE60, #2ECC71); }
.stat-bar__fill--mp { background: linear-gradient(90deg, #2E86AB, #5DADE2); }
.stat-bar__fill--exp { background: linear-gradient(90deg, #F39C12, #F1C40F); }
```

#### 品质标签 (QualityBadge)

```css
.quality-badge {
  display: inline-flex;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}
.quality--common    { color: #95A5A6; border: 1px solid rgba(149,165,166,0.3); }
.quality--uncommon  { color: #27AE60; border: 1px solid rgba(39,174,96,0.3); }
.quality--rare      { color: #3498DB; border: 1px solid rgba(52,152,219,0.3); }
.quality--epic      { color: #9B59B6; border: 1px solid rgba(155,89,182,0.3); }
.quality--legendary { color: #F39C12; border: 1px solid rgba(243,156,18,0.3); }
.quality--mythic    { color: #E74C3C; border: 1px solid rgba(231,76,60,0.3); }
.quality--divine    { color: #FFD700; border: 1px solid rgba(255,215,0,0.3); }
```

#### 五行标识 (ElementIcon)

```css
.element-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}
.element--metal { background: rgba(184,184,184,0.2); color: #B8B8B8; }
.element--wood  { background: rgba(39,174,96,0.2); color: #27AE60; }
.element--water { background: rgba(46,134,171,0.2); color: #2E86AB; }
.element--fire  { background: rgba(231,76,60,0.2); color: #E74C3C; }
.element--earth { background: rgba(139,69,19,0.2); color: #8B4513; }
```

#### 境界徽章 (RealmBadge)

```css
.realm-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  background: rgba(0,0,0,0.4);
  border: 1px solid currentColor;
}
/* 境界颜色继承自 --realm-* 变量 */
```

### 6.3 复合组件

#### 角色状态面板 (CharacterPanel)

```
┌─────────────────────────────┐
│  [头像]  玩家名称            │
│          境界徽章            │
│          门派标识            │
├─────────────────────────────┤
│  生命: [████████░░] 800/1000 │
│  真元: [██████░░░░] 600/1000 │
│  修为: [██████████] 可突破!  │
├─────────────────────────────┤
│  攻击: 150  防御: 80         │
│  速度: 120  悟性: 85         │
├─────────────────────────────┤
│  [装备法宝] 青竹剑 (+5)      │
│  [主修功法] 基础吐纳法 Lv.3  │
├─────────────────────────────┤
│  [快速操作]                  │
│  [修炼] [突破] [恢复] [背包] │
└─────────────────────────────┘
```

#### 战斗面板 (CombatPanel)

```
┌─────────────────────────────────────────┐
│  【战斗】第 3 回合                       │
├─────────────────────────────────────────┤
│                                         │
│      [敌方] 山中妖兽(木)                 │
│      HP: [██████░░░░] 120/200           │
│      [冰冻] 状态                         │
│                                         │
│      ─────────VS─────────               │
│                                         │
│      [我方] 玩家名称                     │
│      HP: [████████░░] 800/1000          │
│      MP: [██████░░░░] 600/1000          │
│      法宝: 青竹剑                        │
│      [金光阵] 激活中                     │
│                                         │
├─────────────────────────────────────────┤
│  [普通攻击] [释放技能] [布阵] [使用道具] │
│  [防御] [逃跑]                          │
└─────────────────────────────────────────┘
```

---

## 七、关键页面高保真设计

### 7.1 登录/角色创建页

**布局**：全屏背景图 + 居中卡片

```
┌─────────────────────────────────────────┐
│                                         │
│    [水墨山水背景动画]                    │
│                                         │
│         ┌───────────────────┐           │
│         │   ⚔️ 蜀山剑侠传    │           │
│         │                   │           │
│         │  请输入道号:      │           │
│         │  [____________]   │           │
│         │                   │           │
│         │  选择门派:        │           │
│         │  [峨眉][青城]    │           │
│         │  [昆仑][血河]    │           │
│         │                   │           │
│         │  [ 踏入修仙路 ]   │           │
│         │                   │           │
│         │  "蜀山万载，      │           │
│         │   剑气纵横三万里" │           │
│         └───────────────────┘           │
│                                         │
└─────────────────────────────────────────┘
```

**设计要点**：
- 背景：动态水墨山水，云雾飘动
- 卡片：毛玻璃效果 + 金色边框
- 门派选择：图标 + 描述 + 特性标签
- 进入动画：剑光划过转场

### 7.2 主界面/修炼页

**布局**：三栏布局，中间修炼为核心

```
┌─────────────────────────────────────────────────────────┐
│ [头像] 剑心 | 灵石: 1,250 | 消息[3] | 设置              │
├──────────┬──────────────────────────┬───────────────────┤
│ [主菜单] │                          │ [角色面板]        │
│  修炼 ◄── │    【修炼道场】           │ 剑心              │
│  法宝    │                          │ 筑基期 ●───────   │
│  功法    │    [打坐] [吐纳] [悟道]   │ 修为: 8,520/10K   │
│  地图    │                          │                   │
│  战斗    │    当前: 吐纳修炼中...    │ 生命: 800/1000    │
│  副本    │                          │ 真元: 600/1000    │
│  任务    │    [修炼动画区域]         │                   │
│  灵兽    │    (灵气汇聚粒子特效)      │ 攻击: 150         │
│  道心    │                          │ 防御: 80          │
│  好友    │    本次获得: +20 修为     │ 速度: 120         │
│  排行    │    总计: 8,520 修为       │                   │
│  成就    │                          │ [青竹剑] 装备中   │
│  商店    │    [开始修炼] [自动修炼]  │ [基础吐纳法] 主修 │
│          │                          │                   │
│          │    【修炼记录】           │ [快速操作]        │
│          │    刚刚 - 吐纳 +20        │ [突破] [背包]     │
│          │    2分钟前 - 打坐 +10     │ [地图] [任务]     │
│          │                          │                   │
├──────────┴──────────────────────────┴───────────────────┤
│  📍 当前位置: 峨眉山脚 | 🟢 在线 | v0.5.0              │
└─────────────────────────────────────────────────────────┘
```

### 7.3 战斗界面

**布局**：全屏沉浸 + 上下分栏

```
┌─────────────────────────────────────────┐
│  【战斗】第 3/10 回合                    │
├─────────────────────────────────────────┤
│                                         │
│           [敌方区域]                     │
│                                         │
│         ┌─────────────┐                 │
│         │  山中妖兽   │                 │
│         │    (木)     │                 │
│         │             │                 │
│         │ HP: ▓▓▓░░░  │                 │
│         │ [冰冻]      │                 │
│         └─────────────┘                 │
│                                         │
│         ─────── VS ───────              │
│                                         │
│         ┌─────────────┐                 │
│         │   剑心      │                 │
│         │  筑基期     │                 │
│         │             │                 │
│         │ HP: ▓▓▓▓▓░░░│                 │
│         │ MP: ▓▓▓▓░░░░ │                 │
│         │ 青竹剑(+5)  │                 │
│         │ [金光阵]    │                 │
│         └─────────────┘                 │
│                                         │
│      [战斗日志]                         │
│      回合2: 青竹剑造成 85 伤害!         │
│      回合2: 敌方被冰冻，无法行动        │
│                                         │
├─────────────────────────────────────────┤
│  [普通攻击] [技能 ▼] [阵法] [道具]     │
│  [防御] [逃跑]                          │
└─────────────────────────────────────────┘
```

### 7.4 世界地图页

**布局**：全屏地图 + 浮动信息面板

```
┌─────────────────────────────────────────┐
│  【世界地图】        [中原 ▼] [筛选]    │
├─────────────────────────────────────────┤
│                                         │
│         [地图可视化区域]                 │
│                                         │
│      北                                 │
│       ↑                                 │
│    冰宫 ●────● 屠龙岛                   │
│     │                                   │
│    北海之滨                              │
│     │                                   │
│    黄河渡口──● 长安城──● 华山           │
│     │              │                    │
│    成都府──● 峨眉山──● 青城山           │
│     │         │      │                  │
│    苗疆入口  金顶   青城后山             │
│     │                                   │
│    苗疆腹地──● 虫谷                     │
│                                         │
│  ┌─────────────┐                        │
│  │ 峨眉山脚     │  ← 浮动地点信息        │
│  │ 类型: 野外   │                        │
│  │ 危险: ★☆☆☆☆ │                        │
│  │ [前往] [探索]│                        │
│  └─────────────┘                        │
│                                         │
└─────────────────────────────────────────┘
```

### 7.5 法宝系统页

**布局**：三栏布局，中间法宝列表 + 右侧详情

```
┌─────────────────────────────────────────────────────────┐
│ [法宝系统] | 拥有: 12/50 | 灵石: 1,250                   │
├──────────┬──────────────────────────┬───────────────────┤
│ [主菜单] │  [筛选: 全部 ▼] [排序 ▼]  │ [法宝详情]        │
│          │                          │                   │
│          │  ┌────┐ ┌────┐ ┌────┐   │  [青竹剑]         │
│          │  │🗡️  │ │🛡️  │ │📿  │   │  品质: 灵器       │
│          │  │青竹│ │玄铁│ │佛珠│   │  五行: 木         │
│          │  │剑  │ │盾  │ │    │   │  类型: 飞剑       │
│          │  │+5  │ │+2  │ │+0  │   │  威力: 85         │
│          │  └────┘ └────┘ └────┘   │  速度: 120        │
│          │                          │                   │
│          │  ┌────┐ ┌────┐ ┌────┐   │  [装备中]         │
│          │  │⚔️  │ │🔮  │ │💍  │   │                   │
│          │  │紫郢│ │八卦│ │储物│   │  描述:            │
│          │  │剑  │ │镜  │ │戒指│   │  峨眉派入门法宝   │
│          │  │+0  │ │+1  │ │+0  │   │  以千年青竹炼制   │
│          │  └────┘ └────┘ └────┘   │                   │
│          │                          │  [强化] [卸下]    │
│          │                          │  [查看五行克制]   │
│          │                          │                   │
├──────────┴──────────────────────────┴───────────────────┤
│  📍 当前位置: 峨眉山脚 | 🟢 在线 | v0.5.0              │
└─────────────────────────────────────────────────────────┘
```

---

## 八、设计决策依据

### 8.1 色彩选择依据

| 决策 | 依据 |
|------|------|
| 深色背景为主 | 1. 修仙题材适合暗色调营造神秘感<br>2. 减少长时间游戏的视觉疲劳<br>3. 亮色内容在暗底上更突出 |
| 青冥蓝为主色 | 1. 对应"青天"意象，符合仙侠氛围<br>2. 蓝色在深色背景上可读性佳<br>3. 区别于市面上大量红金配色的仙侠游戏 |
| 金色为强调色 | 1. 中国传统文化中金色代表尊贵<br>2. 用于奖励、品质等正向反馈<br>3. 与深色背景形成高对比 |
| 五行独立色彩 | 1. 游戏核心机制需要快速识别<br>2. 传统五行已有固定色彩认知<br>3. 增强战斗和法宝系统的策略感 |

### 8.2 布局选择依据

| 决策 | 依据 |
|------|------|
| 三栏布局 | 1. 信息密度高，需要同时展示菜单、内容、状态<br>2. PC端主流游戏界面模式<br>3. 左右面板可折叠适配移动端 |
| 左侧功能菜单 | 1. 符合用户从左到右的阅读习惯<br>2. 与主流游戏界面一致降低学习成本<br>3. 图标+文字双模式适配不同屏幕 |
| 右侧角色面板 | 1. 角色状态需要随时可见<br>2. 右侧是视觉终点，适合放置重要信息<br>3. 可快速执行常用操作 |

### 8.3 交互设计依据

| 决策 | 依据 |
|------|------|
| 即时动画反馈 | 1. 放置类游戏依赖反馈获得成就感<br>2. 修仙题材适合灵气、光芒等特效<br>3. 减少等待感的枯燥 |
| 渐进式功能解锁 | 1. 19个系统一次性展示会信息过载<br>2. 随境界提升解锁符合游戏设定<br>3. 保持玩家持续探索的动力 |
| 一键快捷操作 | 1. 移动端屏幕空间有限<br>2. 高频操作需要最短路径<br>3. 右侧面板常驻快捷按钮 |

### 8.4 技术可行性评估

| 设计要素 | 技术实现 | 复杂度 |
|----------|----------|--------|
| 深色主题 + 渐变 | CSS变量 + linear-gradient | 低 |
| 卡片式布局 | Flex/Grid + 圆角边框 | 低 |
| 响应式三栏 | CSS Media Query + 条件渲染 | 中 |
| 粒子特效(修炼) | Canvas/CSS Animation | 中 |
| 战斗动画 | CSS Animation + 关键帧 | 中 |
| 地图可视化 | SVG/Canvas + 交互 | 高 |
| 毛玻璃效果 | backdrop-filter | 低(注意性能) |
| 水墨背景 | 静态图/视频/Canvas生成 | 中 |

---

## 九、设计资源清单

### 9.1 需要制作的视觉资源

| 资源类型 | 数量 | 规格 | 优先级 |
|----------|------|------|--------|
| 门派Logo | 4个 | 64x64 SVG | 高 |
| 五行图标 | 5个 | 24x24 SVG | 高 |
| 境界图标 | 7个 | 32x32 SVG | 高 |
| 功能图标 | 20个 | 24x24 SVG | 高 |
| 法宝图标 | 15个 | 64x64 PNG | 中 |
| 灵兽图标 | 25个 | 64x64 PNG | 中 |
| 背景图 | 5张 | 1920x1080 | 中 |
| 特效素材 | 10套 | 序列帧/粒子 | 低 |

### 9.2 推荐字体资源

| 字体 | 用途 | 获取方式 |
|------|------|----------|
| Noto Serif SC | 标题 | Google Fonts |
| Noto Sans SC | 正文 | Google Fonts |
| ZCOOL XiaoWei | 装饰文字 | 站酷免费字体 |

---

## 十、附录

### 10.1 设计令牌 (Design Tokens)

```css
/* 完整CSS变量定义 */
:root {
  /* Colors */
  --color-primary: #2D5A7B;
  --color-primary-light: #4A8BB5;
  --color-primary-dark: #1A3A52;
  --color-secondary: #8B6914;
  --color-secondary-light: #C4A35A;
  --color-accent: #C0392B;
  --color-success: #27AE60;
  --color-warning: #F39C12;
  --color-info: #5DADE2;

  /* Backgrounds */
  --bg-primary: #0F1419;
  --bg-secondary: #1A1F2E;
  --bg-card: #242B3D;
  --bg-hover: #2E364A;
  --bg-active: #3A4460;

  /* Text */
  --text-primary: #E8E4DC;
  --text-secondary: #9CA3AF;
  --text-muted: #6B7280;
  --text-gold: #D4AF37;

  /* Border */
  --border-default: rgba(255,255,255,0.1);
  --border-gold: rgba(212,175,55,0.3);
  --border-active: rgba(74,139,181,0.5);

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* Shadow */
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.2);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.3);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.4);
  --shadow-gold: 0 0 20px rgba(212,175,55,0.2);

  /* Transition */
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
  --transition-slow: 350ms ease;
}
```

### 10.2 文件命名规范

```
assets/
├── icons/                    # 图标资源
│   ├── icon-{name}.svg
│   └── element-{type}.svg
├── images/                   # 图片资源
│   ├── bg-{scene}.jpg
│   ├── artifact-{name}.png
│   └── beast-{name}.png
├── fonts/                    # 字体文件
│   └── font-{name}.{woff2|ttf}
└── effects/                  # 特效资源
    └── effect-{name}.json
```

---

> **文档结束**
>
> 本方案基于项目现有技术架构（Vue 3 + Element Plus + Flask API）设计，所有视觉和交互规范均可直接用于前端开发实现。建议在开发过程中优先实现核心页面（登录、主界面、战斗），再逐步扩展其他系统页面。
