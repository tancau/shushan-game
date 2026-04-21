<template>
  <div class="spirit-beast-view">
    <div class="spirit-beast-header">
      <h1 class="page-title">灵兽</h1>
      <p class="page-subtitle">捕捉和培养灵兽，助您修仙之路</p>
    </div>

    <div class="spirit-beast-content">
      <SsCard title="我的灵兽" class="my-beasts-card">
        <div class="beasts-list">
          <div
            v-for="beast in myBeasts"
            :key="beast.id"
            :class="['beast-item', { 'is-active': beast.isActive }]"
            @click="selectBeast(beast)"
          >
            <div class="beast-avatar">{{ beast.icon }}</div>
            <div class="beast-info">
              <h4 class="beast-name">{{ beast.name }}</h4>
              <div class="beast-meta">
                <span class="beast-type">{{ beast.type }}</span>
                <span class="beast-level">Lv.{{ beast.level }}</span>
              </div>
              <div class="beast-loyalty">
                <span class="loyalty-label">忠诚度</span>
                <div class="loyalty-bar">
                  <div class="loyalty-fill" :style="{ width: beast.loyalty + '%' }" />
                </div>
                <span class="loyalty-value">{{ beast.loyalty }}%</span>
              </div>
            </div>
            <div v-if="beast.isActive" class="active-mark">出战</div>
          </div>
          <div v-if="myBeasts.length === 0" class="empty-state">
            尚未拥有灵兽
          </div>
        </div>
      </SsCard>

      <SsCard v-if="selectedBeast" title="灵兽详情" class="beast-detail-card">
        <div class="detail-header">
          <div class="detail-avatar">{{ selectedBeast.icon }}</div>
          <div class="detail-info">
            <h3 class="detail-name">{{ selectedBeast.name }}</h3>
            <span class="detail-type">{{ selectedBeast.type }}</span>
          </div>
        </div>

        <div class="detail-stats">
          <div class="stat-item">
            <span class="stat-label">等级</span>
            <span class="stat-value">{{ selectedBeast.level }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">攻击</span>
            <span class="stat-value">{{ selectedBeast.attack }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">防御</span>
            <span class="stat-value">{{ selectedBeast.defense }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">速度</span>
            <span class="stat-value">{{ selectedBeast.speed }}</span>
          </div>
        </div>

        <div class="detail-actions">
          <SsButton
            v-if="!selectedBeast.isActive"
            type="primary"
            block
            @click="setActiveBeast(selectedBeast.id)"
          >
            设为出战
          </SsButton>
          <SsButton
            type="gold"
            block
            @click="feedBeast(selectedBeast.id)"
          >
            喂养
          </SsButton>
          <SsButton
            type="ghost"
            block
            @click="releaseBeast(selectedBeast.id)"
          >
            放生
          </SsButton>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'

interface SpiritBeast {
  id: string
  name: string
  icon: string
  type: string
  level: number
  loyalty: number
  attack: number
  defense: number
  speed: number
  isActive: boolean
}

const myBeasts = ref<SpiritBeast[]>([
  {
    id: 'beast-1',
    name: '火灵狐',
    icon: '🦊',
    type: '火系',
    level: 5,
    loyalty: 80,
    attack: 45,
    defense: 30,
    speed: 60,
    isActive: true,
  },
  {
    id: 'beast-2',
    name: '青木狼',
    icon: '🐺',
    type: '木系',
    level: 3,
    loyalty: 65,
    attack: 35,
    defense: 40,
    speed: 45,
    isActive: false,
  },
])

const selectedBeast = ref<SpiritBeast | null>(null)

function selectBeast(beast: SpiritBeast) {
  selectedBeast.value = beast
}

function setActiveBeast(id: string) {
  console.log('设为出战', id)
  myBeasts.value.forEach(beast => {
    beast.isActive = beast.id === id
  })
}

function feedBeast(id: string) {
  console.log('喂养灵兽', id)
  const beast = myBeasts.value.find(b => b.id === id)
  if (beast) {
    beast.loyalty = Math.min(100, beast.loyalty + 5)
    beast.level += 1
  }
}

function releaseBeast(id: string) {
  console.log('放生灵兽', id)
  myBeasts.value = myBeasts.value.filter(b => b.id !== id)
  if (selectedBeast.value?.id === id) {
    selectedBeast.value = null
  }
}
</script>

<style scoped lang="scss">
.spirit-beast-view {
  max-width: 900px;
  margin: 0 auto;
}

.spirit-beast-header {
  text-align: center;
  margin-bottom: var(--space-6);
}

.page-title {
  font-family: var(--font-title);
  font-size: var(--text-2xl);
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.page-subtitle {
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin: 0;
}

.spirit-beast-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.beasts-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.beast-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
  position: relative;

  &:hover {
    border-color: var(--border-active);
  }

  &.is-active {
    border-color: var(--color-primary-light);
    background: rgba(45, 90, 123, 0.1);
  }
}

.beast-avatar {
  font-size: 32px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.beast-info {
  flex: 1;
}

.beast-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.beast-meta {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}

.beast-type {
  font-size: var(--text-xs);
  padding: 2px 8px;
  background: rgba(231, 76, 60, 0.2);
  color: #E74C3C;
  border-radius: var(--radius-sm);
}

.beast-level {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}

.beast-loyalty {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.loyalty-label {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  width: 40px;
}

.loyalty-bar {
  flex: 1;
  height: 6px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.loyalty-fill {
  height: 100%;
  background: linear-gradient(90deg, #E74C3C, #F39C12, #27AE60);
  border-radius: var(--radius-full);
  transition: width 0.3s;
}

.loyalty-value {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  width: 35px;
  text-align: right;
}

.active-mark {
  position: absolute;
  top: var(--space-1);
  right: var(--space-2);
  font-size: var(--text-xs);
  color: var(--color-primary-light);
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: var(--space-6);
  color: var(--text-muted);
}

.detail-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-default);
}

.detail-avatar {
  font-size: 48px;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.detail-info {
  flex: 1;
}

.detail-name {
  font-family: var(--font-title);
  font-size: var(--text-xl);
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.detail-type {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.detail-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: var(--space-2) var(--space-3);
  background: var(--bg-card);
  border-radius: var(--radius-md);
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.stat-value {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
}

.detail-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

@media (max-width: 768px) {
  .spirit-beast-content {
    grid-template-columns: 1fr;
  }
}
</style>
