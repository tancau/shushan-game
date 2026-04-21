<template>
  <div class="quest-view">
    <div class="quest-header">
      <h1 class="page-title">任务</h1>
      <p class="page-subtitle">完成任务获取奖励</p>
    </div>

    <div class="quest-content">
      <SsCard title="进行中的任务" class="active-quests">
        <div class="quest-list">
          <div
            v-for="quest in activeQuests"
            :key="quest.id"
            :class="['quest-item', { 'is-completable': quest.progress >= quest.target }]"
          >
            <div class="quest-icon">{{ quest.icon }}</div>
            <div class="quest-info">
              <h4 class="quest-name">{{ quest.name }}</h4>
              <p class="quest-desc">{{ quest.description }}</p>
              <div class="quest-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: (quest.progress / quest.target * 100) + '%' }" />
                </div>
                <span class="progress-text">{{ quest.progress }}/{{ quest.target }}</span>
              </div>
            </div>
            <SsButton
              v-if="quest.progress >= quest.target"
              type="gold"
              size="small"
              @click="completeQuest(quest.id)"
            >
              完成
            </SsButton>
          </div>
          <div v-if="activeQuests.length === 0" class="empty-state">
            暂无进行中的任务
          </div>
        </div>
      </SsCard>

      <SsCard title="可接取的任务" class="available-quests">
        <div class="quest-list">
          <div
            v-for="quest in availableQuests"
            :key="quest.id"
            class="quest-item"
          >
            <div class="quest-icon">{{ quest.icon }}</div>
            <div class="quest-info">
              <h4 class="quest-name">{{ quest.name }}</h4>
              <p class="quest-desc">{{ quest.description }}</p>
              <div class="quest-rewards">
                <span v-for="reward in quest.rewards" :key="reward" class="reward-tag">{{ reward }}</span>
              </div>
            </div>
            <SsButton
              type="primary"
              size="small"
              @click="acceptQuest(quest.id)"
            >
              接受
            </SsButton>
          </div>
          <div v-if="availableQuests.length === 0" class="empty-state">
            暂无可接取的任务
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

interface Quest {
  id: string
  name: string
  icon: string
  description: string
  progress: number
  target: number
  rewards: string[]
}

const activeQuests = ref<Quest[]>([
  {
    id: 'cultivate-1',
    name: '初入道途',
    icon: '🧘',
    description: '通过修炼累计获得100修为',
    progress: 65,
    target: 100,
    rewards: ['修为+50', '灵石+10'],
  },
  {
    id: 'explore-1',
    name: '探索未知',
    icon: '🗺️',
    description: '成功探索5次',
    progress: 3,
    target: 5,
    rewards: ['灵石+20'],
  },
])

const availableQuests = ref<Quest[]>([
  {
    id: 'combat-1',
    name: '初试锋芒',
    icon: '⚔️',
    description: '完成3次战斗',
    progress: 0,
    target: 3,
    rewards: ['修为+80', '灵石+15'],
  },
  {
    id: 'artifact-1',
    name: '寻宝之旅',
    icon: '🔮',
    description: '获得1件法宝',
    progress: 0,
    target: 1,
    rewards: ['灵石+30'],
  },
])

function completeQuest(id: string) {
  console.log('完成任务', id)
  const index = activeQuests.value.findIndex(q => q.id === id)
  if (index > -1) {
    activeQuests.value.splice(index, 1)
  }
}

function acceptQuest(id: string) {
  console.log('接受任务', id)
  const quest = availableQuests.value.find(q => q.id === id)
  if (quest) {
    availableQuests.value = availableQuests.value.filter(q => q.id !== id)
    activeQuests.value.push({ ...quest })
  }
}
</script>

<style scoped lang="scss">
.quest-view {
  max-width: 800px;
  margin: 0 auto;
}

.quest-header {
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

.quest-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.quest-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.quest-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  transition: all 0.2s;

  &:hover {
    border-color: var(--border-active);
  }

  &.is-completable {
    border-color: var(--color-secondary-light);
    background: rgba(139, 105, 20, 0.1);
  }
}

.quest-icon {
  font-size: 28px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.quest-info {
  flex: 1;
}

.quest-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.quest-desc {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin: 0 0 var(--space-2);
}

.quest-progress {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
  border-radius: var(--radius-full);
  transition: width 0.3s;
}

.progress-text {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  width: 50px;
  text-align: right;
}

.quest-rewards {
  display: flex;
  gap: var(--space-1);
  flex-wrap: wrap;
}

.reward-tag {
  font-size: var(--text-xs);
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  color: var(--text-gold);
}

.empty-state {
  text-align: center;
  padding: var(--space-6);
  color: var(--text-muted);
}
</style>
