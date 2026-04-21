<template>
  <div class="home-view">
    <div class="home-header">
      <h1 class="home-title">修炼道场</h1>
      <p class="home-subtitle">当前位置：{{ gameStore.currentLocation }}</p>
    </div>

    <div class="cultivate-section">
      <SsCard title="修炼方式" class="cultivate-card">
        <div class="cultivate-methods">
          <div
            v-for="method in cultivateMethods"
            :key="method.key"
            :class="['method-item', { 'is-selected': selectedMethod === method.key }]"
            @click="selectedMethod = method.key"
          >
            <div class="method-icon">{{ method.icon }}</div>
            <div class="method-info">
              <h4 class="method-name">{{ method.name }}</h4>
              <p class="method-desc">{{ method.description }}</p>
              <div class="method-stats">
                <span class="stat-tag">+{{ method.gain }}修为</span>
                <span v-if="method.mpCost > 0" class="stat-tag mp-cost">-{{ method.mpCost }}真元</span>
              </div>
            </div>
          </div>
        </div>

        <div class="cultivate-action">
          <SsButton
            type="primary"
            size="large"
            block
            :loading="isCultivating"
            @click="handleCultivate"
          >
            {{ isCultivating ? '修炼中...' : '开始修炼' }}
          </SsButton>
        </div>

        <div v-if="lastResult" class="cultivate-result">
          <p class="result-message">{{ lastResult.message }}</p>
          <p class="result-gain">获得修为 +{{ lastResult.gain }}</p>
        </div>
      </SsCard>

      <SsCard title="修炼记录" class="history-card">
        <div class="history-list">
          <div v-for="(record, index) in cultivateHistory" :key="index" class="history-item">
            <span class="history-time">{{ record.time }}</span>
            <span class="history-action">{{ record.method }}</span>
            <span class="history-gain">+{{ record.gain }}</span>
          </div>
          <div v-if="cultivateHistory.length === 0" class="history-empty">
            暂无修炼记录
          </div>
        </div>
      </SsCard>
    </div>

    <div class="quick-actions">
      <SsCard title="快捷操作">
        <div class="action-grid">
          <SsButton type="ghost" @click="$router.push('/map')">
            <template #icon><el-icon><MapLocation /></el-icon></template>
            地图
          </SsButton>
          <SsButton type="ghost" @click="$router.push('/combat')">
            <template #icon><el-icon><Aim /></el-icon></template>
            战斗
          </SsButton>
          <SsButton type="ghost" @click="$router.push('/quests')">
            <template #icon><el-icon><List /></el-icon></template>
            任务
          </SsButton>
          <SsButton type="ghost" @click="$router.push('/artifacts')">
            <template #icon><el-icon><KnifeFork /></el-icon></template>
            法宝
          </SsButton>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElIcon } from 'element-plus'
import { MapLocation, Aim, List, KnifeFork } from '@element-plus/icons-vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { usePlayerStore } from '@/stores/player'
import { useGameStore } from '@/stores/game'

const playerStore = usePlayerStore()
const gameStore = useGameStore()

const isCultivating = ref(false)
const selectedMethod = ref('吐纳')
const lastResult = ref<{ message: string; gain: number } | null>(null)
const cultivateHistory = ref<Array<{ time: string; method: string; gain: number }>>([])

const cultivateMethods = [
  { key: '打坐', name: '打坐', icon: '🧘', description: '静心打坐，稳固根基', gain: 10, mpCost: 0 },
  { key: '吐纳', name: '吐纳', icon: '🌬️', description: '吐纳天地灵气', gain: 20, mpCost: 5 },
  { key: '悟道', name: '悟道', icon: '💭', description: '参悟天地大道', gain: 50, mpCost: 20 },
]

async function handleCultivate() {
  if (isCultivating.value) return

  isCultivating.value = true
  try {
    const result = await playerStore.cultivate(selectedMethod.value)
    if (result.success) {
      const method = cultivateMethods.find(m => m.key === selectedMethod.value)
      lastResult.value = {
        message: result.message || '修炼成功',
        gain: method?.gain || 0,
      }
      cultivateHistory.value.unshift({
        time: new Date().toLocaleTimeString(),
        method: selectedMethod.value,
        gain: method?.gain || 0,
      })
      if (cultivateHistory.value.length > 10) {
        cultivateHistory.value.pop()
      }
    }
  } finally {
    isCultivating.value = false
  }
}
</script>

<style scoped lang="scss">
.home-view {
  max-width: 800px;
  margin: 0 auto;
}

.home-header {
  text-align: center;
  margin-bottom: var(--space-6);
}

.home-title {
  font-family: var(--font-title);
  font-size: var(--text-2xl);
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.home-subtitle {
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin: 0;
}

.cultivate-section {
  display: grid;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.cultivate-methods {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.method-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--border-active);
  }

  &.is-selected {
    border-color: var(--color-primary-light);
    background: rgba(45, 90, 123, 0.1);
  }
}

.method-icon {
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

.method-info {
  flex: 1;
}

.method-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.method-desc {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin: 0 0 var(--space-2);
}

.method-stats {
  display: flex;
  gap: var(--space-2);
}

.stat-tag {
  font-size: var(--text-xs);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  background: rgba(39, 174, 96, 0.2);
  color: #27AE60;

  &.mp-cost {
    background: rgba(46, 134, 171, 0.2);
    color: #2E86AB;
  }
}

.cultivate-action {
  margin-bottom: var(--space-4);
}

.cultivate-result {
  text-align: center;
  padding: var(--space-3);
  background: rgba(39, 174, 96, 0.1);
  border-radius: var(--radius-md);
  border: 1px solid rgba(39, 174, 96, 0.3);
}

.result-message {
  font-size: var(--text-base);
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.result-gain {
  font-size: var(--text-lg);
  font-weight: 600;
  color: #27AE60;
  margin: 0;
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

.history-action {
  flex: 1;
  color: var(--text-secondary);
}

.history-gain {
  color: #27AE60;
  font-weight: 500;
}

.history-empty {
  text-align: center;
  color: var(--text-muted);
  padding: var(--space-4);
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}
</style>
