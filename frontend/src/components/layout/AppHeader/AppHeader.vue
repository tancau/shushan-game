<template>
  <header class="app-header">
    <div class="app-header__left">
      <button class="app-header__menu-btn hidden-desktop" @click="uiStore.toggleSidebar">
        <el-icon><Menu /></el-icon>
      </button>
      <div class="app-header__brand">
        <span class="app-header__logo">⚔️</span>
        <span class="app-header__title">蜀山剑侠传</span>
      </div>
    </div>
    <div class="app-header__center hidden-mobile">
      <div v-if="playerStore.player" class="app-header__resources">
        <span class="resource-item">
          <el-icon><Coin /></el-icon>
          {{ playerStore.player.spiritStones.toLocaleString() }}
        </span>
      </div>
    </div>
    <div class="app-header__right">
      <el-badge :value="3" class="notification-badge hidden-mobile">
        <el-icon class="header-icon"><Bell /></el-icon>
      </el-badge>
      <router-link to="/settings">
        <el-icon class="header-icon"><Setting /></el-icon>
      </router-link>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ElIcon, ElBadge } from 'element-plus'
import { Menu, Coin, Bell, Setting } from '@element-plus/icons-vue'
import { usePlayerStore } from '@/stores/player'
import { useUiStore } from '@/stores/ui'

const playerStore = usePlayerStore()
const uiStore = useUiStore()
</script>

<style scoped lang="scss">
.app-header {
  height: var(--layout-header-height);
  background: linear-gradient(180deg, var(--bg-secondary), var(--bg-primary));
  border-bottom: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-4);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;

  &__left {
    display: flex;
    align-items: center;
    gap: var(--space-4);
  }

  &__menu-btn {
    background: none;
    border: none;
    color: var(--text-primary);
    font-size: 20px;
    cursor: pointer;
    padding: var(--space-2);
    border-radius: var(--radius-md);
    transition: all 0.2s;
    touch-action: manipulation;

    &:hover {
      background: var(--bg-hover);
    }
  }

  &__brand {
    display: flex;
    align-items: center;
    gap: var(--space-2);
  }

  &__logo {
    font-size: 24px;
  }

  &__title {
    font-family: var(--font-title);
    font-size: var(--text-lg);
    font-weight: 600;
    color: var(--text-primary);
  }

  &__center {
    display: flex;
    align-items: center;
  }

  &__resources {
    display: flex;
    align-items: center;
    gap: var(--space-4);
  }

  &__right {
    display: flex;
    align-items: center;
    gap: var(--space-4);
  }
}

.resource-item {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  color: var(--text-gold);
  font-weight: 500;
}

.header-icon {
  font-size: 20px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 0.2s;

  &:hover {
    color: var(--text-primary);
  }
}

.notification-badge {
  :deep(.el-badge__content) {
    background-color: var(--color-danger);
    border: none;
  }
}

@media (max-width: 640px) {
  .app-header {
    padding: 0 var(--space-3);

    &__title {
      font-size: var(--text-base);
    }
  }
}
</style>
