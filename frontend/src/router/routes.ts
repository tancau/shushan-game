import type { RouteRecordRaw } from 'vue-router'

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
    path: '/game',
    name: 'Game',
    component: () => import('@/views/game/GameView.vue'),
    meta: { title: '游戏', fullScreen: true, public: true },
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('../components/layout/AppLayout/AppLayout.vue'),
    redirect: '/home',
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/main/HomeView.vue'),
        meta: { title: '修炼', icon: 'Star' },
      },
      {
        path: 'cultivate',
        name: 'Cultivate',
        component: () => import('@/views/cultivate/CultivateView.vue'),
        meta: { title: '修炼', icon: 'MagicStick' },
      },
      {
        path: 'artifacts',
        name: 'Artifacts',
        component: () => import('@/views/artifact/ArtifactView.vue'),
        meta: { title: '法宝', icon: 'Sword' },
      },
      {
        path: 'skills',
        name: 'Skills',
        component: () => import('@/views/skill/SkillView.vue'),
        meta: { title: '功法', icon: 'Reading' },
      },
      {
        path: 'map',
        name: 'Map',
        component: () => import('@/views/world/MapView.vue'),
        meta: { title: '地图', icon: 'MapLocation' },
      },
      {
        path: 'explore',
        name: 'Explore',
        component: () => import('@/views/world/ExploreView.vue'),
        meta: { title: '探索', icon: 'Compass' },
      },
      {
        path: 'combat',
        name: 'Combat',
        component: () => import('@/views/combat/CombatView.vue'),
        meta: { title: '战斗', icon: 'Aim', fullScreen: true },
      },
      {
        path: 'dungeons',
        name: 'Dungeons',
        component: () => import('@/views/dungeon/DungeonView.vue'),
        meta: { title: '副本', icon: 'Place' },
      },
      {
        path: 'quests',
        name: 'Quests',
        component: () => import('@/views/quest/QuestView.vue'),
        meta: { title: '任务', icon: 'List' },
      },
      {
        path: 'spirit-beasts',
        name: 'SpiritBeasts',
        component: () => import('@/views/spirit-beast/SpiritBeastView.vue'),
        meta: { title: '灵兽', icon: 'Chicken' },
      },
      {
        path: 'dao-heart',
        name: 'DaoHeart',
        component: () => import('@/views/dao-heart/DaoHeartView.vue'),
        meta: { title: '道心', icon: 'Heart' },
      },
      {
        path: 'friends',
        name: 'Friends',
        component: () => import('@/views/friend/FriendView.vue'),
        meta: { title: '好友', icon: 'User' },
      },
      {
        path: 'leaderboard',
        name: 'Leaderboard',
        component: () => import('@/views/leaderboard/LeaderboardView.vue'),
        meta: { title: '排行榜', icon: 'Trophy' },
      },
      {
        path: 'achievements',
        name: 'Achievements',
        component: () => import('@/views/achievement/AchievementView.vue'),
        meta: { title: '成就', icon: 'Medal' },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/SettingsView.vue'),
        meta: { title: '设置', icon: 'Setting' },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/NotFoundView.vue'),
    meta: { title: '页面未找到', public: true },
  },
]
