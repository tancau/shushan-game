<template>
  <aside :class="sidebarClasses">
    <nav class="app-sidebar__nav">
      <router-link
        v-for="route in menuRoutes"
        :key="route.path"
        :to="route.path"
        :class="['app-sidebar__item', { 'is-active': isActive(route.path) }]"
        @click="handleNavClick"
      >
        <el-icon class="app-sidebar__icon">
          <component :is="route.icon" />
        </el-icon>
        <span class="app-sidebar__text">{{ route.title }}</span>
      </router-link>
    </nav>
  </aside>
  <div
    v-if="isMobileOverlayVisible"
    class="app-sidebar__overlay hidden-desktop"
    @click="uiStore.toggleSidebar"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElIcon } from 'element-plus'
import {
  Star, MagicStick, KnifeFork, Reading,
  MapLocation, Compass, Aim, Place,
  List, Chicken, MostlyCloudy, User,
  Trophy, Medal, Setting
} from '@element-plus/icons-vue'
import { useUiStore } from '@/stores/ui'

const route = useRoute()
const uiStore = useUiStore()

const sidebarClasses = computed(() => ({
  'app-sidebar': true,
  'is-collapsed': uiStore.sidebarCollapsed,
  'is-mobile-open': uiStore.sidebarCollapsed,
}))

const isMobileOverlayVisible = computed(() => {
  return uiStore.sidebarCollapsed && window.innerWidth <= 640
})

const menuRoutes = [
  { path: '/home', title: '修炼', icon: Star },
  { path: '/artifacts', title: '法宝', icon: KnifeFork },
  { path: '/skills', title: '功法', icon: Reading },
  { path: '/map', title: '地图', icon: MapLocation },
  { path: '/explore', title: '探索', icon: Compass },
  { path: '/combat', title: '战斗', icon: Aim },
  { path: '/dungeons', title: '副本', icon: Place },
  { path: '/quests', title: '任务', icon: List },
  { path: '/spirit-beasts', title: '灵兽', icon: Chicken },
  { path: '/dao-heart', title: '道心', icon: MostlyCloudy },
  { path: '/friends', title: '好友', icon: User },
  { path: '/leaderboard', title: '排行', icon: Trophy },
  { path: '/achievements', title: '成就', icon: Medal },
  { path: '/settings', title: '设置', icon: Setting },
]

function isActive(path: string) {
  return route.path === path || route.path.startsWith(path + '/')
}

function handleNavClick() {
  if (window.innerWidth <= 640) {
    uiStore.sidebarCollapsed = false
  }
}
</script>

<style scoped lang="scss">
.app-sidebar {
  width: var(--layout-sidebar-left);
  height: calc(100vh - var(--layout-header-height));
  background: linear-gradient(180deg, var(--bg-secondary), var(--bg-primary));
  border-right: 1px solid var(--border-default);
  position: fixed;
  left: 0;
  top: var(--layout-header-height);
  z-index: 90;
  transition: width 0.3s var(--ease-default), transform 0.3s var(--ease-default);
  overflow-y: auto;

  &.is-collapsed {
    width: 64px;

    .app-sidebar__text {
      display: none;
    }

    .app-sidebar__item {
      justify-content: center;
      padding: var(--space-3);
    }
  }

  &__nav {
    padding: var(--space-2);
  }

  &__item {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    color: var(--text-secondary);
    text-decoration: none;
    transition: all 0.2s var(--ease-default);
    margin-bottom: var(--space-1);

    &:hover {
      background: var(--bg-hover);
      color: var(--text-primary);
    }

    &.is-active {
      background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
      color: var(--text-primary);
      box-shadow: var(--shadow-primary);
    }
  }

  &__icon {
    font-size: 20px;
    flex-shrink: 0;
  }

  &__text {
    font-size: var(--text-base);
    white-space: nowrap;
  }

  &__overlay {
    position: fixed;
    inset: 0;
    background: var(--bg-overlay);
    z-index: 80;
  }
}

@media (max-width: 640px) {
  .app-sidebar {
    transform: translateX(-100%);
    z-index: 95;

    &.is-mobile-open {
      transform: translateX(0);
      width: var(--layout-sidebar-left);

      .app-sidebar__text {
        display: inline;
      }

      .app-sidebar__item {
        justify-content: flex-start;
        padding: var(--space-3) var(--space-4);
      }
    }
  }
}
</style>
