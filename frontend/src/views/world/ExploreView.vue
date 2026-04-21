<template>
  <div class="explore-view">
    <div class="explore-header">
      <h1 class="page-title">探索</h1>
      <p class="page-subtitle">当前位置：{{ gameStore.currentLocation }}</p>
    </div>

    <div class="explore-content">
      <SsCard title="探索区域" class="explore-card">
        <div class="explore-scene">
          <div class="scene-icon">🏔️</div>
          <h3 class="scene-name">{{ gameStore.currentLocation || '未知区域' }}</h3>
          <p class="scene-desc">在这片区域中探索，可能会发现资源、遭遇敌人或触发奇遇</p>
        </div>

        <div class="explore-action">
          <SsButton
            type="primary"
            size="large"
            block
            :loading="isExploring"
            @click="handleExplore"
          >
            {{ isExploring ? '探索中...' : '开始探索' }}
          </SsButton>
        </div>
      </SsCard>

      <SsCard v-if="exploreResult" title="探索结果" class="result-card" highlight>
        <div class="result-content">
          <div class="result-icon">{{ getEventIcon(exploreResult.eventType) }}</div>
          <h4 class="result-title">{{ getEventTitle(exploreResult.eventType) }}</h4>
          <p class="result-message">{{ exploreResult.message }}</p>

          <div v-if="exploreResult.rewards" class="result-rewards">
            <div v-if="exploreResult.rewards.cultivation" class="reward-item">
              <span class="reward-label">修为</span>
              <span class="reward-value">+{{ exploreResult.rewards.cultivation }}</span>
            </div>
            <div v-if="exploreResult.rewards.spiritStones" class="reward-item">
              <span class="reward-label">灵石</span>
              <span class="reward-value">+{{ exploreResult.rewards.spiritStones }}</span>
            </div>
            <div v-if="exploreResult.rewards.items?.length" class="reward-items">
              <span class="reward-label">物品</span>
              <div class="item-tags">
                <span v-for="item in exploreResult.rewards.items" :key="item" class="item-tag">{{ item }}</span>
              </div>
            </div>
          </div>
        </div>
      </SsCard>

      <SsCard title="探索记录" class="history-card">
        <div class="history-list">
          <div v-for="(record, index) in exploreHistory" :key="index" class="history-item">
            <span class="history-time">{{ record.time }}</span>
            <span class="history-event">{{ record.event }}</span>
            <span class="history-result" :class="record.type">{{ record.result }}</span>
          </div>
          <div v-if="exploreHistory.length === 0" class="history-empty">
            暂无探索记录
          </div>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { useGameStore } from '@/stores/game'
import { usePlayerStore } from '@/stores/player'

const gameStore = useGameStore()
const playerStore = usePlayerStore()

const isExploring = ref(false)
const exploreResult = ref<ExploreResult | null>(null)
const exploreHistory = ref<Array<{ time: string; event: string; result: string; type: string }>>([])

interface ExploreResult {
  success: boolean
  message: string
  eventType: 'resource' | 'encounter' | 'treasure' | 'nothing'
  rewards?: {
    cultivation?: number
    spiritStones?: number
    items?: string[]
  }
}

const eventIcons: Record<string, string> = {
  resource: '🌿',
  encounter: '⚔️',
  treasure: '💎',
  nothing: '🍃',
}

const eventTitles: Record<string, string> = {
  resource: '发现资源',
  encounter: '遭遇敌人',
  treasure: '发现宝藏',
  nothing: '一无所获',
}

function getEventIcon(type: string) {
  return eventIcons[type] || '❓'
}

function getEventTitle(type: string) {
  return eventTitles[type] || '未知事件'
}

async function handleExplore() {
  if (isExploring.value) return

  isExploring.value = true
  exploreResult.value = null

  setTimeout(() => {
    const events: ExploreResult['eventType'][] = ['resource', 'encounter', 'treasure', 'nothing']
    const eventType = events[Math.floor(Math.random() * events.length)]!

    const results: Record<string, ExploreResult> = {
      resource: {
        success: true,
        message: '你发现了一处灵草生长地，采集了一些珍贵药材',
        eventType: 'resource',
        rewards: { cultivation: 15, items: ['灵草', '矿石'] },
      },
      encounter: {
        success: true,
        message: '你遭遇了一只山中妖兽，经过一番激战将其击退',
        eventType: 'encounter',
        rewards: { cultivation: 30, spiritStones: 10 },
      },
      treasure: {
        success: true,
        message: '你发现了一个古老的洞府，里面藏有前人留下的宝物',
        eventType: 'treasure',
        rewards: { cultivation: 50, spiritStones: 25, items: ['古卷', '灵石'] },
      },
      nothing: {
        success: true,
        message: '你在这片区域搜索了一番，但没有发现什么特别的东西',
        eventType: 'nothing',
      },
    }

    exploreResult.value = results[eventType]!

    exploreHistory.value.unshift({
      time: new Date().toLocaleTimeString(),
      event: eventTitles[eventType]!,
      result: exploreResult.value!.rewards ? '有收获' : '无收获',
      type: exploreResult.value!.rewards ? 'success' : 'normal',
    })

    if (exploreHistory.value.length > 10) {
      exploreHistory.value.pop()
    }

    isExploring.value = false
  }, 1500)
}
</script>

<style scoped lang="scss">
.explore-view {
  max-width: 600px;
  margin: 0 auto;
}

.explore-header {
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

.explore-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.explore-scene {
  text-align: center;
  padding: var(--space-6);
}

.scene-icon {
  font-size: 64px;
  margin-bottom: var(--space-3);
}

.scene-name {
  font-family: var(--font-title);
  font-size: var(--text-xl);
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.scene-desc {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin: 0;
}

.explore-action {
  margin-top: var(--space-4);
}

.result-content {
  text-align: center;
  padding: var(--space-4);
}

.result-icon {
  font-size: 48px;
  margin-bottom: var(--space-3);
}

.result-title {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.result-message {
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin: 0 0 var(--space-4);
}

.result-rewards {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-3);
  background: rgba(39, 174, 96, 0.1);
  border: 1px solid rgba(39, 174, 96, 0.3);
  border-radius: var(--radius-md);
}

.reward-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reward-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.reward-value {
  font-size: var(--text-base);
  font-weight: 600;
  color: #27AE60;
}

.reward-items {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.item-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  justify-content: flex-end;
}

.item-tag {
  font-size: var(--text-xs);
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.history-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
}

.history-time {
  color: var(--text-muted);
  width: 80px;
  flex-shrink: 0;
}

.history-event {
  flex: 1;
  color: var(--text-secondary);
}

.history-result {
  font-weight: 500;

  &.success {
    color: #27AE60;
  }

  &.normal {
    color: var(--text-muted);
  }
}

.history-empty {
  text-align: center;
  color: var(--text-muted);
  padding: var(--space-4);
}
</style>
