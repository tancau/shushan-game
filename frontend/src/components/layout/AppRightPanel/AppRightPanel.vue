<template>
  <aside :class="panelClasses">
    <div v-if="playerStore.player" class="character-panel">
      <div class="character-panel__header">
        <div class="character-avatar">
          <el-icon><UserFilled /></el-icon>
        </div>
        <div class="character-info">
          <h3 class="character-name">{{ playerStore.player.name }}</h3>
          <span class="character-realm" :style="realmStyle">{{ playerStore.player.realm }}</span>
        </div>
      </div>

      <div class="character-panel__stats">
        <div class="stat-row">
          <span class="stat-label">生命</span>
          <div class="stat-bar">
            <div class="stat-bar__track">
              <div
                class="stat-bar__fill stat-bar__fill--hp"
                :style="{ width: hpPercent + '%' }"
              />
            </div>
            <span class="stat-value">{{ playerStore.player.currentHp }}/{{ playerStore.player.maxHp }}</span>
          </div>
        </div>
        <div class="stat-row">
          <span class="stat-label">真元</span>
          <div class="stat-bar">
            <div class="stat-bar__track">
              <div
                class="stat-bar__fill stat-bar__fill--mp"
                :style="{ width: mpPercent + '%' }"
              />
            </div>
            <span class="stat-value">{{ playerStore.player.currentMp }}/{{ playerStore.player.maxMp }}</span>
          </div>
        </div>
        <div class="stat-row">
          <span class="stat-label">修为</span>
          <div class="stat-bar">
            <div class="stat-bar__track">
              <div
                class="stat-bar__fill stat-bar__fill--exp"
                :style="{ width: expPercent + '%' }"
              />
            </div>
            <span class="stat-value">{{ playerStore.player.cultivation.toLocaleString() }}</span>
          </div>
        </div>
      </div>

      <div class="character-panel__attributes">
        <div class="attr-grid">
          <div class="attr-item">
            <span class="attr-label">攻击</span>
            <span class="attr-value">{{ playerStore.player.stats.attack }}</span>
          </div>
          <div class="attr-item">
            <span class="attr-label">防御</span>
            <span class="attr-value">{{ playerStore.player.stats.defense }}</span>
          </div>
          <div class="attr-item">
            <span class="attr-label">速度</span>
            <span class="attr-value">{{ playerStore.player.stats.speed }}</span>
          </div>
          <div class="attr-item">
            <span class="attr-label">悟性</span>
            <span class="attr-value">{{ playerStore.player.stats.wisdom }}</span>
          </div>
        </div>
      </div>

      <div class="character-panel__equipment">
        <div v-if="playerStore.player.equippedArtifact" class="equipment-item">
          <el-icon><KnifeFork /></el-icon>
          <span>{{ playerStore.player.equippedArtifact.name }}</span>
        </div>
        <div v-else class="equipment-item empty">
          <el-icon><KnifeFork /></el-icon>
          <span>未装备法宝</span>
        </div>
      </div>

      <div class="character-panel__quick-actions">
        <SsButton type="primary" size="small" block @click="$router.push('/cultivate')">
          修炼
        </SsButton>
        <SsButton type="gold" size="small" block @click="handleAdvance">
          突破
        </SsButton>
      </div>
    </div>
    <div v-else class="character-panel--empty">
      <p>未登录</p>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElIcon } from 'element-plus'
import { UserFilled, KnifeFork } from '@element-plus/icons-vue'
import { usePlayerStore } from '@/stores/player'
import { useUiStore } from '@/stores/ui'
import SsButton from '@/components/common/SsButton/SsButton.vue'

const router = useRouter()
const playerStore = usePlayerStore()
const uiStore = useUiStore()

const panelClasses = computed(() => ({
  'app-right-panel': true,
  'is-collapsed': uiStore.rightPanelCollapsed,
}))

const hpPercent = computed(() => {
  if (!playerStore.player) return 0
  return (playerStore.player.currentHp / playerStore.player.maxHp) * 100
})

const mpPercent = computed(() => {
  if (!playerStore.player) return 0
  return (playerStore.player.currentMp / playerStore.player.maxMp) * 100
})

const expPercent = computed(() => {
  if (!playerStore.player) return 0
  return Math.min((playerStore.player.cultivation / 10000) * 100, 100)
})

const realmColors: Record<string, string> = {
  '练气期': '#95A5A6',
  '筑基期': '#27AE60',
  '金丹期': '#F39C12',
  '元婴期': '#E74C3C',
  '化神期': '#9B59B6',
  '合体期': '#3498DB',
  '渡劫期': '#FFD700',
}

const realmStyle = computed(() => ({
  color: realmColors[playerStore.player?.realm || '练气期'],
}))

async function handleAdvance() {
  const result = await playerStore.advanceRealm()
  if (result.success) {
    alert(result.message)
  }
}
</script>

<style scoped lang="scss">
.app-right-panel {
  width: var(--layout-sidebar-right);
  height: calc(100vh - var(--layout-header-height));
  background: linear-gradient(180deg, var(--bg-secondary), var(--bg-primary));
  border-left: 1px solid var(--border-default);
  position: fixed;
  right: 0;
  top: var(--layout-header-height);
  z-index: 90;
  transition: transform 0.3s var(--ease-default);
  overflow-y: auto;
  padding: var(--space-4);

  &.is-collapsed {
    transform: translateX(100%);
  }
}

.character-panel {
  &__header {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    margin-bottom: var(--space-4);
    padding-bottom: var(--space-4);
    border-bottom: 1px solid var(--border-default);
  }

  &__stats {
    margin-bottom: var(--space-4);
  }

  &__attributes {
    margin-bottom: var(--space-4);
  }

  &__equipment {
    margin-bottom: var(--space-4);
    padding: var(--space-3);
    background: var(--bg-card);
    border-radius: var(--radius-md);
  }

  &__quick-actions {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
  }
}

.character-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: var(--text-primary);
}

.character-info {
  flex: 1;
}

.character-name {
  font-family: var(--font-title);
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.character-realm {
  font-size: var(--text-sm);
  font-weight: 500;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}

.stat-label {
  width: 36px;
  font-size: var(--text-sm);
  color: var(--text-secondary);
  flex-shrink: 0;
}

.stat-bar {
  flex: 1;
  display: flex;
  align-items: center;
  gap: var(--space-2);

  &__track {
    flex: 1;
    height: 8px;
    background: rgba(0, 0, 0, 0.4);
    border-radius: var(--radius-full);
    overflow: hidden;
  }

  &__fill {
    height: 100%;
    border-radius: var(--radius-full);
    transition: width 0.5s var(--ease-default);

    &--hp {
      background: linear-gradient(90deg, #27AE60, #2ECC71);
    }

    &--mp {
      background: linear-gradient(90deg, #2E86AB, #5DADE2);
    }

    &--exp {
      background: linear-gradient(90deg, #F39C12, #F1C40F);
    }
  }
}

.stat-value {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  width: 70px;
  text-align: right;
  flex-shrink: 0;
}

.attr-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2);
}

.attr-item {
  display: flex;
  justify-content: space-between;
  padding: var(--space-2) var(--space-3);
  background: var(--bg-card);
  border-radius: var(--radius-md);
}

.attr-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.attr-value {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.equipment-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--text-primary);

  &.empty {
    color: var(--text-muted);
  }
}

@media (max-width: 1024px) {
  .app-right-panel {
    transform: translateX(100%);

    &.is-collapsed {
      transform: translateX(0);
    }
  }
}
</style>
