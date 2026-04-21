<template>
  <nav class="app-mobile-nav">
    <router-link
      v-for="item in navItems"
      :key="item.path"
      :to="item.path"
      :class="['app-mobile-nav__item', { 'is-active': isActive(item.path) }]"
    >
      <el-icon class="app-mobile-nav__icon">
        <component :is="item.icon" />
      </el-icon>
      <span class="app-mobile-nav__text">{{ item.title }}</span>
    </router-link>
  </nav>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ElIcon } from 'element-plus'
import {
  Star, KnifeFork, Reading, MapLocation,
  Compass, Aim, Place, List, Setting
} from '@element-plus/icons-vue'

const route = useRoute()

const navItems = [
  { path: '/home', title: '修炼', icon: Star },
  { path: '/artifacts', title: '法宝', icon: KnifeFork },
  { path: '/map', title: '地图', icon: MapLocation },
  { path: '/combat', title: '战斗', icon: Aim },
  { path: '/settings', title: '设置', icon: Setting },
]

function isActive(path: string) {
  return route.path === path || route.path.startsWith(path + '/')
}
</script>

<style scoped lang="scss">
.app-mobile-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: linear-gradient(0deg, var(--bg-secondary), var(--bg-primary));
  border-top: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: space-around;
  z-index: 100;
  padding-bottom: env(safe-area-inset-bottom);

  &__item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    color: var(--text-secondary);
    text-decoration: none;
    flex: 1;
    height: 100%;
    transition: all 0.2s var(--ease-default);

    &:active {
      transform: scale(0.95);
    }

    &.is-active {
      color: var(--color-primary-light);
    }
  }

  &__icon {
    font-size: 22px;
  }

  &__text {
    font-size: 10px;
  }
}
</style>
