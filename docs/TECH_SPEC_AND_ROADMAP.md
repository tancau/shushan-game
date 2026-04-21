# 蜀山剑侠传 - 技术规范与开发计划

> 版本：v1.0.0 | 日期：2026-04-22 | 对应UI设计：v1.0.0

---

## 一、技术架构总览

### 1.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户层                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  PC浏览器 │  │ 移动浏览器│  │ 微信内置│  │ 桌面应用 │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
└───────┼─────────────┼─────────────┼─────────────┼────────┘
        │             │             │             │
        └─────────────┴──────┬──────┴─────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      前端层 (Frontend)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Vue 3 + Vite + TypeScript                          │   │
│  │  ├─ Element Plus (基础组件)                         │   │
│  │  ├─ Pinia (状态管理)                                │   │
│  │  ├─ Vue Router 4 (路由)                             │   │
│  │  ├─ Axios (HTTP请求)                                │   │
│  │  ├─ GSAP (动画引擎)                                 │   │
│  │  └─ Phaser 3 (战斗/地图特效)                        │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS/JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      后端层 (Backend)                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Python Flask API                                   │   │
│  │  ├─ 33个RESTful API端点                             │   │
│  │  ├─ CORS跨域支持                                    │   │
│  │  └─ JSON数据存储                                    │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      数据层 (Data)                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ 游戏配置JSON│  │ 玩家存档JSON│  │ 静态资源   │            │
│  │ (data/)    │  │ (save/)    │  │ (assets/)  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术栈选型

| 层级 | 技术 | 版本 | 选型理由 |
|------|------|------|----------|
| 构建工具 | Vite | ^5.0 | 极速冷启动、原生ESM、优化打包 |
| 前端框架 | Vue 3 | ^3.4 | 组合式API、TypeScript友好、性能优秀 |
| 类型系统 | TypeScript | ^5.3 | 类型安全、IDE支持、可维护性 |
| UI组件库 | Element Plus | ^2.5 | 与Vue3深度集成、主题定制能力强 |
| 状态管理 | Pinia | ^2.1 | Vue官方推荐、TypeScript友好、简洁 |
| 路由 | Vue Router 4 | ^4.2 | 官方路由、导航守卫、懒加载 |
| HTTP客户端 | Axios | ^1.6 | 拦截器、请求取消、错误处理 |
| 动画引擎 | GSAP | ^3.12 | 高性能动画、时间轴控制、粒子特效 |
| 游戏渲染 | Phaser 3 | ^3.70 | 2D游戏引擎、Canvas/WebGL、适合战斗场景 |
| 图标 | @element-plus/icons-vue | ^2.3 | 与Element Plus配套 |
| CSS预处理器 | SCSS | ^1.70 | 变量、嵌套、混合，适合设计系统 |
| 代码规范 | ESLint + Prettier | ^8.0 | 统一代码风格、自动格式化 |

---

## 二、项目目录结构规范

### 2.1 前端项目结构

```
frontend/                          # 前端项目根目录
├── public/                        # 静态资源（不经过构建）
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── main.ts                    # 应用入口
│   ├── App.vue                    # 根组件
│   ├── env.d.ts                   # 环境类型声明
│   │
│   ├── api/                       # API接口层
│   │   ├── index.ts               # axios实例配置
│   │   ├── types.ts               # API通用类型
│   │   ├── player.ts              # 玩家相关API
│   │   ├── cultivate.ts           # 修炼相关API
│   │   ├── combat.ts              # 战斗相关API
│   │   ├── artifact.ts            # 法宝相关API
│   │   ├── skill.ts               # 功法相关API
│   │   ├── world.ts               # 地图/探索相关API
│   │   ├── quest.ts               # 任务相关API
│   │   ├── dungeon.ts             # 副本相关API
│   │   ├── spiritBeast.ts         # 灵兽相关API
│   │   ├── tribulation.ts         # 天劫相关API
│   │   ├── daoHeart.ts            # 道心相关API
│   │   ├── leaderboard.ts         # 排行榜相关API
│   │   ├── friend.ts              # 好友相关API
│   │   ├── achievement.ts         # 成就相关API
│   │   └── event.ts               # 活动相关API
│   │
│   ├── assets/                    # 构建资源
│   │   ├── icons/                 # SVG图标
│   │   ├── images/                # 图片资源
│   │   │   ├── bg/                # 背景图
│   │   │   ├── artifacts/         # 法宝图
│   │   │   └── beasts/            # 灵兽图
│   │   ├── fonts/                 # 字体文件
│   │   └── styles/                # 全局样式
│   │       ├── variables.scss     # SCSS变量（Design Tokens）
│   │       ├── mixins.scss        # SCSS混合
│   │       ├── global.scss        # 全局样式
│   │       └── animations.scss    # 全局动画
│   │
│   ├── components/                # 公共组件
│   │   ├── common/                # 通用基础组件
│   │   │   ├── SsButton/          # 游戏按钮
│   │   │   ├── SsCard/            # 游戏卡片
│   │   │   ├── SsModal/           # 游戏弹窗
│   │   │   ├── SsStatBar/         # 属性条
│   │   │   ├── SsQualityBadge/    # 品质标签
│   │   │   ├── SsElementIcon/     # 五行图标
│   │   │   ├── SsRealmBadge/      # 境界徽章
│   │   │   ├── SsLoading/         # 加载动画
│   │   │   └── SsEmpty/           # 空状态
│   │   ├── layout/                # 布局组件
│   │   │   ├── AppHeader/         # 顶部导航
│   │   │   ├── AppSidebar/        # 左侧菜单
│   │   │   ├── AppRightPanel/     # 右侧面板
│   │   │   ├── AppFooter/         # 底部信息
│   │   │   └── AppLayout/         # 整体布局
│   │   ├── game/                  # 游戏专用组件
│   │   │   ├── CharacterPanel/    # 角色面板
│   │   │   ├── CombatPanel/       # 战斗面板
│   │   │   ├── CultivatePanel/    # 修炼面板
│   │   │   ├── MapViewer/         # 地图查看器
│   │   │   ├── ArtifactCard/      # 法宝卡片
│   │   │   ├── SkillTree/         # 功法树
│   │   │   ├── QuestTracker/      # 任务追踪
│   │   │   └── LeaderboardTable/  # 排行榜表格
│   │   └── effects/               # 特效组件
│   │       ├── SpiritParticles/   # 灵气粒子
│   │       ├── SwordSlash/        # 剑光特效
│   │       └── ElementBurst/      # 五行爆发
│   │
│   ├── composables/               # 组合式函数
│   │   ├── usePlayer.ts           # 玩家数据
│   │   ├── useCultivate.ts        # 修炼逻辑
│   │   ├── useCombat.ts           # 战斗逻辑
│   │   ├── useWorld.ts            # 地图逻辑
│   │   ├── useLoading.ts          # 加载状态
│   │   ├── useNotification.ts     # 通知提示
│   │   └── useResponsive.ts       # 响应式
│   │
│   ├── stores/                    # Pinia状态管理
│   │   ├── index.ts               # store入口
│   │   ├── player.ts              # 玩家状态
│   │   ├── game.ts                # 游戏全局状态
│   │   ├── ui.ts                  # UI状态（主题、侧边栏等）
│   │   └── settings.ts            # 用户设置
│   │
│   ├── router/                    # 路由配置
│   │   ├── index.ts               # 路由入口
│   │   ├── routes.ts              # 路由定义
│   │   └── guards.ts              # 导航守卫
│   │
│   ├── views/                     # 页面视图
│   │   ├── auth/                  # 认证相关
│   │   │   ├── LoginView.vue
│   │   │   └── RegisterView.vue
│   │   ├── main/                  # 主界面
│   │   │   └── HomeView.vue
│   │   ├── cultivate/             # 修炼
│   │   │   └── CultivateView.vue
│   │   ├── artifact/              # 法宝
│   │   │   └── ArtifactView.vue
│   │   ├── skill/                 # 功法
│   │   │   └── SkillView.vue
│   │   ├── world/                 # 世界地图
│   │   │   ├── MapView.vue
│   │   │   └── ExploreView.vue
│   │   ├── combat/                # 战斗
│   │   │   └── CombatView.vue
│   │   ├── dungeon/               # 副本
│   │   │   └── DungeonView.vue
│   │   ├── quest/                 # 任务
│   │   │   └── QuestView.vue
│   │   ├── spirit-beast/          # 灵兽
│   │   │   └── SpiritBeastView.vue
│   │   ├── dao-heart/             # 道心
│   │   │   └── DaoHeartView.vue
│   │   ├── friend/                # 好友
│   │   │   └── FriendView.vue
│   │   ├── leaderboard/           # 排行榜
│   │   │   └── LeaderboardView.vue
│   │   ├── achievement/           # 成就
│   │   │   └── AchievementView.vue
│   │   └── settings/              # 设置
│   │       └── SettingsView.vue
│   │
│   ├── types/                     # TypeScript类型定义
│   │   ├── index.ts               # 类型入口
│   │   ├── player.ts              # 玩家类型
│   │   ├── game.ts                # 游戏类型
│   │   ├── combat.ts              # 战斗类型
│   │   ├── world.ts               # 地图类型
│   │   ├── artifact.ts            # 法宝类型
│   │   ├── skill.ts               # 功法类型
│   │   └── common.ts              # 通用类型
│   │
│   ├── utils/                     # 工具函数
│   │   ├── index.ts               # 工具入口
│   │   ├── format.ts              # 格式化
│   │   ├── validate.ts            # 验证
│   │   ├── storage.ts             # 本地存储
│   │   └── constants.ts           # 常量定义
│   │
│   └── plugins/                   # 插件
│       ├── element-plus.ts        # Element Plus配置
│       └── gsap.ts                # GSAP配置
│
├── index.html                     # HTML模板
├── vite.config.ts                 # Vite配置
├── tsconfig.json                  # TypeScript配置
├── tsconfig.app.json              # 应用TS配置
├── tsconfig.node.json             # NodeTS配置
├── package.json                   # 依赖管理
├── eslint.config.js               # ESLint配置
├── prettier.config.js             # Prettier配置
└── README.md                      # 项目说明
```

### 2.2 命名规范

#### 文件命名

| 类型 | 命名方式 | 示例 |
|------|----------|------|
| 组件 | PascalCase | `SsButton.vue`, `CharacterPanel.vue` |
| 组合式函数 | camelCase with use prefix | `usePlayer.ts`, `useCombat.ts` |
| Store | camelCase | `player.ts`, `game.ts` |
| 类型定义 | PascalCase | `Player.ts`, `CombatResult.ts` |
| 工具函数 | camelCase | `formatNumber.ts`, `storage.ts` |
| 样式文件 | kebab-case | `variables.scss`, `global.scss` |
| 视图页面 | PascalCase + View suffix | `HomeView.vue`, `CombatView.vue` |

#### 组件命名规范

```
# 公共组件前缀：Ss (Shushan)
SsButton, SsCard, SsModal, SsStatBar

# 布局组件前缀：App
AppHeader, AppSidebar, AppLayout

# 游戏组件：直接功能命名
CharacterPanel, CombatPanel, MapViewer

# 组件文件内：PascalCase
<script setup lang="ts">
# 组件使用：kebab-case
<character-panel />
```

---

## 三、TypeScript类型规范

### 3.1 核心类型定义

```typescript
// types/player.ts
export interface Player {
  name: string;
  realm: Realm;
  cultivation: number;
  spiritStones: number;
  stats: PlayerStats;
  currentHp: number;
  maxHp: number;
  currentMp: number;
  maxMp: number;
  sect: Sect | null;
  location: string;
  artifacts: Artifact[];
  equippedArtifact: Artifact | null;
  skills: LearnedSkill[];
  mainSkillId: string | null;
  activeQuests: string[];
  completedQuests: string[];
  karma: number;
  playTime: number;
}

export interface PlayerStats {
  hp: number;
  mp: number;
  attack: number;
  defense: number;
  speed: number;
  wisdom: number;
  luck: number;
}

export type Realm = 
  | '练气期' | '筑基期' | '金丹期' | '元婴期' 
  | '化神期' | '合体期' | '渡劫期';

export type Sect = '峨眉派' | '青城派' | '昆仑派' | '血河教';

export type Element = '金' | '木' | '水' | '火' | '土';

// types/artifact.ts
export interface Artifact {
  id: string;
  name: string;
  artifactType: ArtifactType;
  element: Element;
  power: number;
  speed: number;
  level: number;
  maxLevel: number;
  description: string;
  quality: Quality;
}

export type ArtifactType = '飞剑' | '防御' | '攻击' | '辅助' | '特殊';

export type Quality = 
  | 'common' | 'uncommon' | 'rare' | 'epic' 
  | 'legendary' | 'mythic' | 'divine';

// types/combat.ts
export interface CombatResult {
  success: boolean;
  message: string;
  turn: number;
  playerDamage?: number;
  enemyDamage?: number;
  winner?: 'player' | 'enemy' | null;
  rewards?: CombatRewards;
}

export interface CombatRewards {
  cultivation: number;
  spiritStones: number;
  artifact?: Artifact;
}

// types/api.ts
export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  message?: string;
  code?: number;
}

export interface ApiError {
  success: false;
  message: string;
  code: number;
}
```

### 3.2 类型导出规范

```typescript
// types/index.ts
export * from './player';
export * from './game';
export * from './combat';
export * from './world';
export * from './artifact';
export * from './skill';
export * from './common';
```

---

## 四、API接口规范

### 4.1 Axios实例配置

```typescript
// api/index.ts
import axios, { AxiosInstance, AxiosError, AxiosResponse } from 'axios';
import type { ApiResponse, ApiError } from '@/types';
import { usePlayerStore } from '@/stores/player';

const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    const playerStore = usePlayerStore();
    if (playerStore.token) {
      config.headers.Authorization = `Bearer ${playerStore.token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    if (!response.data.success) {
      return Promise.reject(response.data);
    }
    return response.data;
  },
  (error: AxiosError<ApiError>) => {
    const message = error.response?.data?.message || '网络请求失败';
    // 统一错误处理
    return Promise.reject({ success: false, message, code: error.response?.status || 0 });
  }
);

export default apiClient;
```

### 4.2 API模块示例

```typescript
// api/player.ts
import apiClient from './index';
import type { ApiResponse, Player } from '@/types';

export const playerApi = {
  // 获取玩家状态
  getStatus(): Promise<ApiResponse<Player>> {
    return apiClient.get('/api/status');
  },

  // 修炼
  cultivate(method: string): Promise<ApiResponse<{ cultivation: number; message: string }>> {
    return apiClient.get('/api/cultivate', { params: { method } });
  },

  // 突破境界
  advance(): Promise<ApiResponse<{ message: string }>> {
    return apiClient.get('/api/advance');
  },

  // 获取法宝列表
  getArtifacts(): Promise<ApiResponse<{ artifacts: Artifact[] }>> {
    return apiClient.get('/api/artifacts');
  },

  // 获取功法列表
  getSkills(): Promise<ApiResponse<{ skills: Skill[] }>> {
    return apiClient.get('/api/skills');
  },

  // 移动位置
  travel(location: string): Promise<ApiResponse<{ message: string }>> {
    return apiClient.post('/api/travel', { location });
  },
};

// api/combat.ts
export const combatApi = {
  // 开始战斗
  startBattle(): Promise<ApiResponse<{ message: string }>> {
    return apiClient.get('/api/battle');
  },

  // 执行攻击
  attack(): Promise<ApiResponse<CombatResult>> {
    return apiClient.get('/api/battle/attack');
  },

  // 执行防御
  defend(): Promise<ApiResponse<CombatResult>> {
    return apiClient.get('/api/battle/defend');
  },
};
```

### 4.3 API端点映射表

| 功能模块 | API端点 | 方法 | 前端API模块 |
|----------|---------|------|-------------|
| 玩家状态 | /api/status | GET | playerApi.getStatus |
| 修炼 | /api/cultivate | GET | playerApi.cultivate |
| 突破 | /api/advance | GET | playerApi.advance |
| 战斗 | /api/battle | GET | combatApi.startBattle |
| 探索 | /api/explore | GET | worldApi.explore |
| 法宝列表 | /api/artifacts | GET | playerApi.getArtifacts |
| 功法列表 | /api/skills | GET | playerApi.getSkills |
| 任务列表 | /api/quests | GET | questApi.getQuests |
| 地图 | /api/map | GET | worldApi.getMap |
| 移动 | /api/travel | POST | playerApi.travel |
| 灵兽列表 | /api/spirit-beasts | GET | spiritBeastApi.getList |
| 捕捉灵兽 | /api/spirit-beast/capture | POST | spiritBeastApi.capture |
| 天劫状态 | /api/tribulation/status | GET | tribulationApi.getStatus |
| 开始渡劫 | /api/tribulation/start | POST | tribulationApi.start |
| 道心信息 | /api/dao-heart | GET | daoHeartApi.getInfo |
| 功德商店 | /api/merit-shop | GET | daoHeartApi.getShop |
| 排行榜 | /api/leaderboard/:type | GET | leaderboardApi.getList |
| 副本列表 | /api/dungeons | GET | dungeonApi.getList |
| 进入副本 | /api/dungeon/:id/enter | POST | dungeonApi.enter |
| 活动列表 | /api/events | GET | eventApi.getList |
| 每日签到 | /api/sign-in | POST | eventApi.signIn |
| 好友列表 | /api/friends | GET | friendApi.getList |
| 添加好友 | /api/friend/add | POST | friendApi.add |
| 成就列表 | /api/achievements | GET | achievementApi.getList |

---

## 五、状态管理规范

### 5.1 Store架构设计

```typescript
// stores/player.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Player, Realm } from '@/types';
import { playerApi } from '@/api/player';

export const usePlayerStore = defineStore('player', () => {
  // State
  const player = ref<Player | null>(null);
  const isLoading = ref(false);
  const token = ref(localStorage.getItem('shushan_token') || '');

  // Getters
  const isLoggedIn = computed(() => !!player.value);
  const currentRealm = computed(() => player.value?.realm || '练气期');
  const canAdvance = computed(() => {
    if (!player.value) return false;
    // 根据境界配置判断
    return false; // 具体逻辑根据后端返回
  });

  // Actions
  async function fetchStatus() {
    isLoading.value = true;
    try {
      const res = await playerApi.getStatus();
      if (res.success && res.data) {
        player.value = res.data;
      }
    } finally {
      isLoading.value = false;
    }
  }

  async function cultivate(method: string = '吐纳') {
    try {
      const res = await playerApi.cultivate(method);
      if (res.success) {
        await fetchStatus(); // 刷新状态
      }
      return res;
    } catch (error) {
      return { success: false, message: '修炼失败' };
    }
  }

  async function advanceRealm() {
    try {
      const res = await playerApi.advance();
      if (res.success) {
        await fetchStatus();
      }
      return res;
    } catch (error) {
      return { success: false, message: '突破失败' };
    }
  }

  function logout() {
    player.value = null;
    token.value = '';
    localStorage.removeItem('shushan_token');
  }

  return {
    player,
    isLoading,
    token,
    isLoggedIn,
    currentRealm,
    canAdvance,
    fetchStatus,
    cultivate,
    advanceRealm,
    logout,
  };
});
```

```typescript
// stores/game.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useGameStore = defineStore('game', () => {
  // 游戏全局状态
  const currentLocation = ref('峨眉山脚');
  const notifications = ref<Notification[]>([]);
  const isInCombat = ref(false);
  const isAutoCultivating = ref(false);

  function addNotification(message: string, type: 'success' | 'error' | 'info' = 'info') {
    const id = Date.now();
    notifications.value.push({ id, message, type });
    setTimeout(() => {
      removeNotification(id);
    }, 3000);
  }

  function removeNotification(id: number) {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index > -1) {
      notifications.value.splice(index, 1);
    }
  }

  return {
    currentLocation,
    notifications,
    isInCombat,
    isAutoCultivating,
    addNotification,
    removeNotification,
  };
});
```

```typescript
// stores/ui.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUiStore = defineStore('ui', () => {
  const sidebarCollapsed = ref(false);
  const rightPanelCollapsed = ref(false);
  const currentTheme = ref<'dark' | 'light'>('dark');
  const isMobile = ref(false);

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value;
  }

  function toggleRightPanel() {
    rightPanelCollapsed.value = !rightPanelCollapsed.value;
  }

  function setMobile(value: boolean) {
    isMobile.value = value;
    if (value) {
      sidebarCollapsed.value = true;
      rightPanelCollapsed.value = true;
    }
  }

  return {
    sidebarCollapsed,
    rightPanelCollapsed,
    currentTheme,
    isMobile,
    toggleSidebar,
    toggleRightPanel,
    setMobile,
  };
});
```

### 5.2 Store使用规范

```vue
<!-- 在组件中使用 -->
<script setup lang="ts">
import { usePlayerStore, useGameStore, useUiStore } from '@/stores';
import { storeToRefs } from 'pinia';

const playerStore = usePlayerStore();
const gameStore = useGameStore();
const uiStore = useUiStore();

// 使用 storeToRefs 解构响应式状态
const { player, currentRealm, isLoading } = storeToRefs(playerStore);
const { isMobile } = storeToRefs(uiStore);

// 直接调用 actions
async function handleCultivate() {
  const result = await playerStore.cultivate('吐纳');
  if (result.success) {
    gameStore.addNotification(result.message, 'success');
  }
}
</script>
```

---

## 六、路由规范

### 6.1 路由配置

```typescript
// router/routes.ts
import type { RouteRecordRaw } from 'vue-router';

export const routes: RouteRecordRaw[] = [
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('@/views/auth/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/views/auth/LoginView.vue'),
        meta: { title: '登录', public: true },
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('@/views/auth/RegisterView.vue'),
        meta: { title: '注册', public: true },
      },
    ],
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/components/layout/AppLayout.vue'),
    redirect: '/home',
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/main/HomeView.vue'),
        meta: { title: '修炼', icon: ' meditation' },
      },
      {
        path: 'cultivate',
        name: 'Cultivate',
        component: () => import('@/views/cultivate/CultivateView.vue'),
        meta: { title: '修炼', icon: 'star' },
      },
      {
        path: 'artifacts',
        name: 'Artifacts',
        component: () => import('@/views/artifact/ArtifactView.vue'),
        meta: { title: '法宝', icon: 'sword' },
      },
      {
        path: 'skills',
        name: 'Skills',
        component: () => import('@/views/skill/SkillView.vue'),
        meta: { title: '功法', icon: 'book' },
      },
      {
        path: 'map',
        name: 'Map',
        component: () => import('@/views/world/MapView.vue'),
        meta: { title: '地图', icon: 'map-location' },
      },
      {
        path: 'explore',
        name: 'Explore',
        component: () => import('@/views/world/ExploreView.vue'),
        meta: { title: '探索', icon: 'compass' },
      },
      {
        path: 'combat',
        name: 'Combat',
        component: () => import('@/views/combat/CombatView.vue'),
        meta: { title: '战斗', icon: 'aim', fullScreen: true },
      },
      {
        path: 'dungeons',
        name: 'Dungeons',
        component: () => import('@/views/dungeon/DungeonView.vue'),
        meta: { title: '副本', icon: 'place' },
      },
      {
        path: 'quests',
        name: 'Quests',
        component: () => import('@/views/quest/QuestView.vue'),
        meta: { title: '任务', icon: 'list' },
      },
      {
        path: 'spirit-beasts',
        name: 'SpiritBeasts',
        component: () => import('@/views/spirit-beast/SpiritBeastView.vue'),
        meta: { title: '灵兽', icon: 'chicken' },
      },
      {
        path: 'dao-heart',
        name: 'DaoHeart',
        component: () => import('@/views/dao-heart/DaoHeartView.vue'),
        meta: { title: '道心', icon: 'heart' },
      },
      {
        path: 'friends',
        name: 'Friends',
        component: () => import('@/views/friend/FriendView.vue'),
        meta: { title: '好友', icon: 'user' },
      },
      {
        path: 'leaderboard',
        name: 'Leaderboard',
        component: () => import('@/views/leaderboard/LeaderboardView.vue'),
        meta: { title: '排行榜', icon: 'trophy' },
      },
      {
        path: 'achievements',
        name: 'Achievements',
        component: () => import('@/views/achievement/AchievementView.vue'),
        meta: { title: '成就', icon: 'medal' },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/SettingsView.vue'),
        meta: { title: '设置', icon: 'setting' },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/NotFoundView.vue'),
    meta: { title: '页面未找到', public: true },
  },
];
```

### 6.2 导航守卫

```typescript
// router/guards.ts
import type { Router, NavigationGuardNext, RouteLocationNormalized } from 'vue-router';
import { usePlayerStore } from '@/stores/player';

export function setupRouterGuards(router: Router) {
  // 前置守卫
  router.beforeEach(
    async (
      to: RouteLocationNormalized,
      from: RouteLocationNormalized,
      next: NavigationGuardNext
    ) => {
      const playerStore = usePlayerStore();

      // 设置页面标题
      document.title = to.meta.title ? `${to.meta.title} - 蜀山剑侠传` : '蜀山剑侠传';

      // 公开页面直接放行
      if (to.meta.public) {
        next();
        return;
      }

      // 检查登录状态
      if (!playerStore.isLoggedIn) {
        await playerStore.fetchStatus();
      }

      if (!playerStore.isLoggedIn) {
        next('/auth/login');
        return;
      }

      next();
    }
  );

  // 后置钩子
  router.afterEach((to) => {
    // 页面统计、滚动恢复等
    window.scrollTo(0, 0);
  });
}
```

---

## 七、组件开发规范

### 7.1 组件模板规范

```vue
<!-- components/common/SsButton/SsButton.vue -->
<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <ss-loading v-if="loading" size="small" />
    <span v-else class="ss-button__content">
      <el-icon v-if="icon" class="ss-button__icon">
        <component :is="icon" />
      </el-icon>
      <slot />
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Component } from 'vue';

interface Props {
  type?: 'primary' | 'gold' | 'danger' | 'ghost' | 'default';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  icon?: Component;
  block?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'default',
  size: 'medium',
  disabled: false,
  loading: false,
  block: false,
});

const emit = defineEmits<{
  click: [event: MouseEvent];
}>();

const buttonClasses = computed(() => ({
  'ss-button': true,
  [`ss-button--${props.type}`]: true,
  [`ss-button--${props.size}`]: true,
  'ss-button--block': props.block,
  'ss-button--loading': props.loading,
}));

function handleClick(event: MouseEvent) {
  if (!props.disabled && !props.loading) {
    emit('click', event);
  }
}
</script>

<style scoped lang="scss">
.ss-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s var(--ease-default);
  position: relative;
  overflow: hidden;

  &--medium {
    padding: 10px 24px;
    font-size: 14px;
    height: 40px;
  }

  &--small {
    padding: 6px 16px;
    font-size: 12px;
    height: 32px;
  }

  &--large {
    padding: 14px 32px;
    font-size: 16px;
    height: 48px;
  }

  &--primary {
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
    color: var(--text-primary);
    border: 1px solid rgba(74, 139, 181, 0.5);

    &:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(45, 90, 123, 0.4);
    }
  }

  &--gold {
    background: linear-gradient(135deg, var(--color-secondary), var(--color-secondary-light));
    color: var(--text-primary);
    border: 1px solid rgba(212, 175, 55, 0.5);

    &:hover:not(:disabled) {
      box-shadow: var(--shadow-gold);
    }
  }

  &--block {
    width: 100%;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &--loading {
    cursor: wait;
  }
}
</style>
```

### 7.2 组合式函数规范

```typescript
// composables/useCultivate.ts
import { ref, computed } from 'vue';
import { usePlayerStore } from '@/stores/player';
import { useGameStore } from '@/stores/game';
import { playerApi } from '@/api/player';

export interface CultivateMethod {
  name: string;
  key: string;
  cultivationGain: number;
  mpCost: number;
  description: string;
}

const CULTIVATE_METHODS: CultivateMethod[] = [
  { name: '打坐', key: '打坐', cultivationGain: 10, mpCost: 0, description: '静心打坐，稳固根基' },
  { name: '吐纳', key: '吐纳', cultivationGain: 20, mpCost: 5, description: '吐纳天地灵气' },
  { name: '悟道', key: '悟道', cultivationGain: 50, mpCost: 20, description: '参悟天地大道' },
];

export function useCultivate() {
  const playerStore = usePlayerStore();
  const gameStore = useGameStore();

  const isCultivating = ref(false);
  const selectedMethod = ref<CultivateMethod>(CULTIVATE_METHODS[1]);
  const lastResult = ref<{ gain: number; message: string } | null>(null);

  const canCultivate = computed(() => {
    if (!playerStore.player) return false;
    return playerStore.player.currentMp >= selectedMethod.value.mpCost;
  });

  const canAdvance = computed(() => playerStore.canAdvance);

  async function cultivate() {
    if (isCultivating.value || !canCultivate.value) return;

    isCultivating.value = true;
    try {
      const result = await playerStore.cultivate(selectedMethod.value.key);
      if (result.success) {
        lastResult.value = {
          gain: selectedMethod.value.cultivationGain,
          message: result.message,
        };
        gameStore.addNotification(result.message, 'success');
      }
    } finally {
      isCultivating.value = false;
    }
  }

  async function advance() {
    if (!canAdvance.value) return;

    const result = await playerStore.advanceRealm();
    if (result.success) {
      gameStore.addNotification(result.message, 'success');
    }
  }

  return {
    methods: CULTIVATE_METHODS,
    selectedMethod,
    isCultivating,
    canCultivate,
    canAdvance,
    lastResult,
    cultivate,
    advance,
  };
}
```

---

## 八、样式系统规范

### 8.1 SCSS变量文件

```scss
// assets/styles/variables.scss
:root {
  // 品牌色
  --color-primary: #2D5A7B;
  --color-primary-light: #4A8BB5;
  --color-primary-dark: #1A3A52;
  --color-primary-rgb: 45, 90, 123;

  --color-secondary: #8B6914;
  --color-secondary-light: #C4A35A;
  --color-secondary-dark: #5C4510;

  --color-accent: #C0392B;
  --color-success: #27AE60;
  --color-warning: #F39C12;
  --color-info: #5DADE2;
  --color-danger: #E74C3C;

  // 五行色
  --element-metal: #B8B8B8;
  --element-wood: #27AE60;
  --element-water: #2E86AB;
  --element-fire: #E74C3C;
  --element-earth: #8B4513;

  // 境界色
  --realm-1: #95A5A6;
  --realm-2: #27AE60;
  --realm-3: #F39C12;
  --realm-4: #E74C3C;
  --realm-5: #9B59B6;
  --realm-6: #3498DB;
  --realm-7: #FFD700;

  // 背景色
  --bg-primary: #0F1419;
  --bg-secondary: #1A1F2E;
  --bg-card: #242B3D;
  --bg-hover: #2E364A;
  --bg-active: #3A4460;
  --bg-overlay: rgba(0, 0, 0, 0.7);

  // 文字色
  --text-primary: #E8E4DC;
  --text-secondary: #9CA3AF;
  --text-muted: #6B7280;
  --text-gold: #D4AF37;
  --text-inverse: #0F1419;

  // 边框
  --border-default: rgba(255, 255, 255, 0.1);
  --border-gold: rgba(212, 175, 55, 0.3);
  --border-active: rgba(74, 139, 181, 0.5);

  // 间距
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;

  // 圆角
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  // 阴影
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.4);
  --shadow-gold: 0 0 20px rgba(212, 175, 55, 0.2);
  --shadow-primary: 0 0 20px rgba(45, 90, 123, 0.3);

  // 字体
  --font-title: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', serif;
  --font-body: 'Noto Sans SC', 'Source Han Sans SC', 'Microsoft YaHei', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  --font-decorative: 'ZCOOL XiaoWei', 'Ma Shan Zheng', cursive;

  // 字号
  --text-xs: 11px;
  --text-sm: 12px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 18px;
  --text-2xl: 24px;
  --text-3xl: 32px;

  // 布局
  --layout-header-height: 56px;
  --layout-footer-height: 40px;
  --layout-sidebar-left: 168px;
  --layout-sidebar-right: 280px;
  --layout-content-padding: 24px;

  // 动画
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-decelerate: cubic-bezier(0, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 350ms;
}

// Element Plus 主题覆盖
@forward 'element-plus/theme-chalk/src/common/var.scss' with (
  $colors: (
    'primary': (
      'base': #2D5A7B,
    ),
    'success': (
      'base': #27AE60,
    ),
    'warning': (
      'base': #F39C12,
    ),
    'danger': (
      'base': #E74C3C,
    ),
    'info': (
      'base': #5DADE2,
    ),
  ),
  $bg-color: (
    'page': #0F1419,
    '': #242B3D,
    'overlay': rgba(0, 0, 0, 0.7),
  ),
  $text-color: (
    'primary': #E8E4DC,
    'regular': #9CA3AF,
    'secondary': #6B7280,
    'placeholder': #4B5563,
  ),
  $border-color: (
    '': rgba(255, 255, 255, 0.1),
    'light': rgba(255, 255, 255, 0.05),
  ),
);
```

### 8.2 全局样式

```scss
// assets/styles/global.scss
@import './variables.scss';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--text-primary);
  background-color: var(--bg-primary);
  line-height: 1.5;
  overflow-x: hidden;
}

// 滚动条样式
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-full);
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.25);
}

// 选中文字样式
::selection {
  background: rgba(45, 90, 123, 0.4);
  color: var(--text-primary);
}

// 游戏专用工具类
.glow-gold {
  box-shadow: var(--shadow-gold);
}

.glow-primary {
  box-shadow: var(--shadow-primary);
}

.text-gradient-gold {
  background: linear-gradient(135deg, var(--color-secondary-light), #FFD700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

// 响应式隐藏
@media (max-width: 640px) {
  .hidden-mobile {
    display: none !important;
  }
}

@media (min-width: 641px) {
  .hidden-desktop {
    display: none !important;
  }
}
```

---

## 九、动画与特效规范

### 9.1 GSAP动画配置

```typescript
// plugins/gsap.ts
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// 注册插件
gsap.registerPlugin(ScrollTrigger);

// 全局默认配置
gsap.defaults({
  duration: 0.3,
  ease: 'power2.out',
});

export default gsap;

// composables/useAnimation.ts
import gsap from '@/plugins/gsap';

export function useAnimation() {
  // 数字滚动动画
  function animateNumber(
    element: HTMLElement,
    from: number,
    to: number,
    duration: number = 1
  ) {
    const obj = { value: from };
    gsap.to(obj, {
      value: to,
      duration,
      ease: 'power2.out',
      onUpdate: () => {
        element.textContent = Math.floor(obj.value).toLocaleString();
      },
    });
  }

  // 卡片进入动画
  function cardEnter(element: HTMLElement, delay: number = 0) {
    gsap.from(element, {
      opacity: 0,
      y: 20,
      duration: 0.4,
      delay,
      ease: 'power2.out',
    });
  }

  // 按钮点击涟漪
  function buttonRipple(event: MouseEvent, element: HTMLElement) {
    const rect = element.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const ripple = document.createElement('span');
    ripple.style.cssText = `
      position: absolute;
      border-radius: 50%;
      background: rgba(255,255,255,0.3);
      transform: scale(0);
      pointer-events: none;
      width: 100px;
      height: 100px;
      left: ${x - 50}px;
      top: ${y - 50}px;
    `;
    element.appendChild(ripple);

    gsap.to(ripple, {
      scale: 3,
      opacity: 0,
      duration: 0.6,
      ease: 'power2.out',
      onComplete: () => ripple.remove(),
    });
  }

  return {
    animateNumber,
    cardEnter,
    buttonRipple,
  };
}
```

### 9.2 CSS动画关键帧

```scss
// assets/styles/animations.scss
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes glow {
  from {
    box-shadow: 0 0 5px rgba(212, 175, 55, 0.2);
  }
  to {
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

// 动画工具类
.animate-float {
  animation: float 3s ease-in-out infinite;
}

.animate-glow {
  animation: glow 2s ease-in-out infinite alternate;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-slide-in-up {
  animation: slideInUp 0.4s ease-out;
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

.animate-shake {
  animation: shake 0.3s ease-in-out;
}

.animate-spin {
  animation: spin 1s linear infinite;
}
```

---

## 十、构建与部署规范

### 10.1 Vite配置

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
      imports: ['vue', 'vue-router', 'pinia'],
      dts: true,
    }),
    Components({
      resolvers: [ElementPlusResolver()],
      dts: true,
    }),
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/assets/styles/variables.scss" as *;`,
      },
    },
  },
  build: {
    target: 'esnext',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          'element-plus': ['element-plus'],
          'gsap': ['gsap'],
          'phaser': ['phaser'],
          'vendor': ['vue', 'vue-router', 'pinia', 'axios'],
        },
      },
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

### 10.2 package.json

```json
{
  "name": "shushan-game-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc --noEmit && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .vue,.ts,.tsx --fix",
    "format": "prettier --write \"src/**/*.{vue,ts,tsx,scss,css}\"",
    "typecheck": "vue-tsc --noEmit"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "element-plus": "^2.5.0",
    "gsap": "^3.12.0",
    "phaser": "^3.70.0",
    "pinia": "^2.1.0",
    "vue": "^3.4.0",
    "vue-router": "^4.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@vitejs/plugin-vue": "^5.0.0",
    "@vue/tsconfig": "^0.5.0",
    "eslint": "^8.56.0",
    "eslint-plugin-vue": "^9.19.0",
    "prettier": "^3.1.0",
    "sass": "^1.69.0",
    "typescript": "^5.3.0",
    "unplugin-auto-import": "^0.17.0",
    "unplugin-vue-components": "^0.26.0",
    "vite": "^5.0.0",
    "vue-tsc": "^1.8.0"
  }
}
```

### 10.3 部署配置

```json
// vercel.json（前端部署）
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://shushan-game.vercel.app/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

---

## 十一、开发计划与里程碑

### 11.1 项目阶段划分

```
Phase 1: 基础架构搭建 (Week 1-2)
├── 项目初始化与工程配置
├── 设计系统搭建（变量、组件、样式）
├── 路由与布局框架
├── API层与状态管理
└── 登录/注册页面

Phase 2: 核心系统开发 (Week 3-5)
├── 主界面/修炼系统
├── 角色状态面板
├── 法宝系统
├── 功法系统
└── 世界地图与探索

Phase 3: 战斗与冒险 (Week 6-7)
├── 战斗界面
├── 副本系统
├── 任务系统
└── 灵兽系统

Phase 4: 社交与进阶 (Week 8-9)
├── 好友系统
├── 排行榜
├── 成就系统
├── 道心系统
└── 活动/签到

Phase 5: 优化与上线 (Week 10)
├── 性能优化
├── 响应式适配完善
├── 动画特效优化
├── 测试与Bug修复
└── 部署上线
```

### 11.2 详细任务分解

#### Phase 1: 基础架构搭建（第1-2周）

| 任务 | 优先级 | 预估工时 | 负责人 |
|------|--------|----------|--------|
| 初始化Vue 3 + Vite项目 | P0 | 2h | - |
| 配置TypeScript + ESLint + Prettier | P0 | 2h | - |
| 配置Element Plus + 主题覆盖 | P0 | 4h | - |
| 搭建SCSS变量系统（Design Tokens） | P0 | 4h | - |
| 配置Pinia状态管理 | P0 | 2h | - |
| 配置Vue Router + 导航守卫 | P0 | 3h | - |
| 搭建Axios实例 + 拦截器 | P0 | 3h | - |
| 开发基础组件（SsButton, SsCard, SsModal） | P0 | 8h | - |
| 开发布局组件（AppHeader, AppSidebar, AppLayout） | P0 | 8h | - |
| 开发登录/注册页面 | P0 | 8h | - |
| 开发角色创建流程 | P0 | 6h | - |
| **Phase 1 合计** | | **50h** | |

#### Phase 2: 核心系统开发（第3-5周）

| 任务 | 优先级 | 预估工时 | 负责人 |
|------|--------|----------|--------|
| 开发角色状态面板组件 | P0 | 6h | - |
| 开发修炼主界面 | P0 | 10h | - |
| 开发修炼动画特效 | P0 | 6h | - |
| 开发突破境界界面 | P0 | 4h | - |
| 开发法宝列表页面 | P0 | 8h | - |
| 开发法宝详情/装备界面 | P0 | 6h | - |
| 开发功法树页面 | P0 | 8h | - |
| 开发功法学习/升级界面 | P0 | 6h | - |
| 开发世界地图页面 | P0 | 12h | - |
| 开发探索界面 | P0 | 8h | - |
| 开发探索事件展示 | P0 | 6h | - |
| **Phase 2 合计** | | **90h** | |

#### Phase 3: 战斗与冒险（第6-7周）

| 任务 | 优先级 | 预估工时 | 负责人 |
|------|--------|----------|--------|
| 开发战斗界面布局 | P0 | 8h | - |
| 开发回合制战斗逻辑 | P0 | 10h | - |
| 开发战斗动画特效（Phaser） | P0 | 12h | - |
| 开发伤害数字浮动效果 | P1 | 4h | - |
| 开发副本列表页面 | P0 | 6h | - |
| 开发副本挑战流程 | P0 | 8h | - |
| 开发任务追踪面板 | P0 | 6h | - |
| 开发任务列表页面 | P0 | 6h | - |
| 开发灵兽列表页面 | P1 | 6h | - |
| 开发灵兽培养界面 | P1 | 6h | - |
| **Phase 3 合计** | | **82h** | |

#### Phase 4: 社交与进阶（第8-9周）

| 任务 | 优先级 | 预估工时 | 负责人 |
|------|--------|----------|--------|
| 开发好友列表页面 | P1 | 6h | - |
| 开发好友互动功能 | P1 | 6h | - |
| 开发排行榜页面 | P1 | 6h | - |
| 开发成就墙页面 | P1 | 8h | - |
| 开发称号系统界面 | P1 | 4h | - |
| 开发道心/功德界面 | P1 | 6h | - |
| 开发功德商店 | P1 | 4h | - |
| 开发活动列表页面 | P1 | 4h | - |
| 开发签到功能 | P1 | 4h | - |
| 开发设置页面 | P1 | 4h | - |
| **Phase 4 合计** | | **52h** | |

#### Phase 5: 优化与上线（第10周）

| 任务 | 优先级 | 预估工时 | 负责人 |
|------|--------|----------|--------|
| 性能优化（懒加载、代码分割） | P0 | 6h | - |
| 移动端响应式适配 | P0 | 8h | - |
| 动画性能优化 | P1 | 4h | - |
| 功能测试与Bug修复 | P0 | 12h | - |
| 构建配置优化 | P0 | 2h | - |
| Vercel部署配置 | P0 | 2h | - |
| 上线前检查清单 | P0 | 2h | - |
| **Phase 5 合计** | | **36h** | |

### 11.3 里程碑时间表

| 里程碑 | 日期 | 交付物 | 验收标准 |
|--------|------|--------|----------|
| M1: 架构完成 | Week 2结束 | 可运行的基础框架 | 登录/注册可用，路由正常，API可调用 |
| M2: 核心系统 | Week 5结束 | 修炼/法宝/功法/地图 | 可完整体验养成循环 |
| M3: 战斗系统 | Week 7结束 | 战斗/副本/任务 | 可完成一次完整战斗流程 |
| M4: 功能完整 | Week 9结束 | 所有19个系统 | 所有页面可访问，功能可用 |
| M5: 正式上线 | Week 10结束 | 生产环境部署 | 通过测试，性能达标 |

### 11.4 风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| Phaser 3学习曲线 | 战斗特效延期 | 先用CSS动画实现MVP，后续迭代 |
| 移动端适配复杂 | 开发时间增加 | 使用响应式优先设计，逐步增强 |
| API性能瓶颈 | 用户体验差 | 增加前端缓存，实现请求合并 |
| 资源加载慢 | 首屏时间长 | 图片懒加载、骨架屏、CDN加速 |

---

## 十二、代码规范与最佳实践

### 12.1 Vue组件规范

```typescript
// 组合式API使用顺序
<script setup lang="ts">
// 1. 导入
import { ref, computed, watch, onMounted } from 'vue';
import type { PropType } from 'vue';

// 2. 类型导入
import type { Player } from '@/types';

// 3. 组件导入
import SsButton from '@/components/common/SsButton/SsButton.vue';

// 4. Store/Composable导入
import { usePlayerStore } from '@/stores/player';
import { useAnimation } from '@/composables/useAnimation';

// 5. Props定义
interface Props {
  player: Player;
  showDetail?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showDetail: false,
});

// 6. Emits定义
const emit = defineEmits<{
  update: [player: Player];
  delete: [id: string];
}>();

// 7. 注入
const playerStore = usePlayerStore();

// 8. 响应式数据
const isExpanded = ref(false);
const localPlayer = ref<Player>({ ...props.player });

// 9. 计算属性
const playerLevel = computed(() => playerStore.currentRealm);

// 10. 监听
watch(() => props.player, (newVal) => {
  localPlayer.value = { ...newVal };
});

// 11. 方法
function handleUpdate() {
  emit('update', localPlayer.value);
}

// 12. 生命周期
onMounted(() => {
  // 初始化逻辑
});
</script>
```

### 12.2 Git提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

| Type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug修复 |
| docs | 文档更新 |
| style | 代码格式（不影响功能） |
| refactor | 重构 |
| perf | 性能优化 |
| test | 测试相关 |
| chore | 构建/工具相关 |

示例：
```
feat(combat): 实现回合制战斗界面

- 添加战斗面板组件
- 实现攻击/防御/逃跑操作
- 集成战斗API

Closes #123
```

### 12.3 文件头注释规范

```typescript
/**
 * @file 战斗面板组件
 * @description 实现回合制战斗的UI交互
 * @author 开发者名称
 * @since 2026-04-22
 */
```

---

> **文档结束**
>
> 本技术规范基于UI设计方案制定，涵盖前端架构、组件开发、状态管理、API对接、构建部署等全流程。开发团队应严格遵循本规范，确保代码质量和项目可维护性。
