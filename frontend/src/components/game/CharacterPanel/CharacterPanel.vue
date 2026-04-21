<template>
  <SsCard class="character-panel" :hoverable="false">
    <div class="character-panel__header">
      <div class="character-avatar">
        <el-icon><UserFilled /></el-icon>
      </div>
      <div class="character-info">
        <h3 class="character-name">{{ player?.name || '未登录' }}</h3>
        <span v-if="player" class="character-realm" :style="realmStyle">{{ player.realm }}</span>
        <span v-if="player?.sect" class="character-sect">{{ player.sect }}</span>
      </div>
    </div>

    <div v-if="player" class="character-panel__stats">
      <div class="stat-row">
        <span class="stat-label">生命</span>
        <div class="stat-bar">
          <div class="stat-bar__track">
            <div class="stat-bar__fill stat-bar__fill--hp" :style="{ width: hpPercent + '%' }" />
          </div>
          <span class="stat-value">{{ player.currentHp }}/{{ player.maxHp }}</span>
        </div>
      </div>
      <div class="stat-row">
        <span class="stat-label">真元</span>
        <div class="stat-bar">
          <div class="stat-bar__track">
            <div class="stat-bar__fill stat-bar__fill--mp" :style="{ width: mpPercent + '%' }" />
          </div>
          <span class="stat-value">{{ player.currentMp }}/{{ player.maxMp }}</span>
        </div>
      </div>
      <div class="stat-row">
        <span class="stat-label">修为</span>
        <div class="stat-bar">
          <div class="stat-bar__track">
            <div class="stat-bar__fill stat-bar__fill--exp" :style="{ width: expPercent + '%' }" />
          </div>
          <span class="stat-value">{{ player.cultivation.toLocaleString() }}</span>
        </div>
      </div>
    </div>

    <div v-if="player" class="character-panel__attributes">
      <div class="attr-grid">
        <div class="attr-item">
          <span class="attr-label">攻击</span>
          <span class="attr-value">{{ player.stats.attack }}</span>
        </div>
        <div class="attr-item">
          <span class="attr-label">防御</span>
          <span class="attr-value">{{ player.stats.defense }}</span>
        </div>
        <div class="attr-item">
          <span class="attr-label">速度</span>
          <span class="attr-value">{{ player.stats.speed }}</span>
        </div>
        <div class="attr-item">
          <span class="attr-label">悟性</span>
          <span class="attr-value">{{ player.stats.wisdom }}</span>
        </div>
        <div class="attr-item">
          <span class="attr-label">气运</span>
          <span class="attr-value">{{ player.stats.luck }}</span>
        </div>
        <div class="attr-item">
          <span class="attr-label">功德</span>
          <span class="attr-value">{{ player.karma }}</span>
        </div>
      </div>
    </div>

    <div v-if="player" class="character-panel__equipment">
      <div v-if="player.equippedArtifact" class="equipment-item">
        <el-icon><KnifeFork /></el-icon>
        <span>{{ player.equippedArtifact.name }}</span>
        <span class="equipment-level">+{{ player.equippedArtifact.level }}</span>
      </div>
      <div v-else class="equipment-item empty">
        <el-icon><KnifeFork /></el-icon>
        <span>未装备法宝</span>
      </div>
      <div v-if="player.mainSkillId" class="equipment-item">
        <el-icon><Reading /></el-icon>
        <span>{{ mainSkillName }}</span>
      </div>
      <div v-else class="equipment-item empty">
        <el-icon><Reading /></el-icon>
        <span>未修炼功法</span>
      </div>
    </div>

    <div v-if="player" class="character-panel__quick-actions">
      <SsButton type="primary" size="small" block @click="$router.push('/cultivate')">
        修炼
      </SsButton>
      <SsButton type="gold" size="small" block :disabled="!canAdvance" @click="handleAdvance">
        突破
      </SsButton>
    </div>
  </SsCard>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElIcon } from 'element-plus'
import { UserFilled, KnifeFork, Reading } from '@element-plus/icons-vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { usePlayerStore } from '@/stores/player'
import type { Player } from '@/types'

const router = useRouter()
const playerStore = usePlayerStore()

const props = defineProps<{
  player?: Player | null
}>()

const hpPercent = computed(() => {
  if (!props.player) return 0
  return (props.player.currentHp / props.player.maxHp) * 100
})

const mpPercent = computed(() => {
  if (!props.player) return 0
  return (props.player.currentMp / props.player.maxMp) * 100
})

const expPercent = computed(() => {
  if (!props.player) return 0
  return Math.min((props.player.cultivation / 10000) * 100, 100)
})

const canAdvance = computed(() => playerStore.canAdvance)

const mainSkillName = computed(() => {
  if (!props.player?.mainSkillId) return ''
  const skill = props.player.skills.find(s => s.id === props.player?.mainSkillId)
  return skill?.name || '未知功法'
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
  color: realmColors[props.player?.realm || '练气期'],
}))

async function handleAdvance() {
  const result = await playerStore.advanceRealm()
  if (result.success) {
    alert(result.message)
  }
}
</script>

<style scoped lang="scss">
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
  margin-right: var(--space-2);
}

.character-sect {
  font-size: var(--text-xs);
  color: var(--text-muted);
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
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
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--space-2);
}

.attr-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-2);
  background: var(--bg-card);
  border-radius: var(--radius-md);
}

.attr-label {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}

.attr-value {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
}

.equipment-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--text-primary);
  padding: var(--space-1) 0;

  &.empty {
    color: var(--text-muted);
  }
}

.equipment-level {
  color: var(--text-gold);
  font-weight: 600;
  margin-left: auto;
}
</style>
