<template>
  <div class="achievement-view">
    <div class="achievement-header">
      <h1 class="page-title">成就</h1>
      <p class="page-subtitle">记录您的修仙历程</p>
    </div>

    <div class="achievement-stats">
      <div class="stat-card">
        <span class="stat-value">{{ completedCount }}/{{ achievements.length }}</span>
        <span class="stat-label">已完成</span>
      </div>
      <div class="stat-card">
        <span class="stat-value">{{ completionPercent }}%</span>
        <span class="stat-label">完成度</span>
      </div>
    </div>

    <div class="achievement-content">
      <SsCard title="成就列表" class="achievement-list-card">
        <div class="achievement-grid">
          <div
            v-for="achievement in achievements"
            :key="achievement.id"
            :class="['achievement-item', { 'is-completed': achievement.completed }]"
          >
            <div class="achievement-icon">{{ achievement.icon }}</div>
            <div class="achievement-info">
              <h4 class="achievement-name">{{ achievement.name }}</h4>
              <p class="achievement-desc">{{ achievement.description }}</p>
              <div class="achievement-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: (achievement.progress / achievement.target * 100) + '%' }" />
                </div>
                <span class="progress-text">{{ achievement.progress }}/{{ achievement.target }}</span>
              </div>
            </div>
            <div v-if="achievement.completed" class="completed-mark">✓</div>
          </div>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'

interface Achievement {
  id: string
  name: string
  icon: string
  description: string
  progress: number
  target: number
  completed: boolean
}

const achievements: Achievement[] = [
  {
    id: 'first-cultivate',
    name: '初入道途',
    icon: '🧘',
    description: '完成第一次修炼',
    progress: 1,
    target: 1,
    completed: true,
  },
  {
    id: 'cultivate-100',
    name: '百日筑基',
    icon: '📿',
    description: '累计修炼100次',
    progress: 65,
    target: 100,
    completed: false,
  },
  {
    id: 'first-battle',
    name: '初试锋芒',
    icon: '⚔️',
    description: '完成第一次战斗',
    progress: 1,
    target: 1,
    completed: true,
  },
  {
    id: 'win-10',
    name: '常胜将军',
    icon: '🏆',
    description: '累计获得10场战斗胜利',
    progress: 7,
    target: 10,
    completed: false,
  },
  {
    id: 'first-artifact',
    name: '得宝',
    icon: '🔮',
    description: '获得第一件法宝',
    progress: 1,
    target: 1,
    completed: true,
  },
  {
    id: 'explore-50',
    name: '探险家',
    icon: '🗺️',
    description: '累计探索50次',
    progress: 23,
    target: 50,
    completed: false,
  },
  {
    id: 'advance-realm',
    name: '突破自我',
    icon: '✨',
    description: '成功突破一个境界',
    progress: 1,
    target: 1,
    completed: true,
  },
  {
    id: 'rich',
    name: '富甲一方',
    icon: '💰',
    description: '累计拥有10000灵石',
    progress: 8500,
    target: 10000,
    completed: false,
  },
]

const completedCount = computed(() => achievements.filter(a => a.completed).length)
const completionPercent = computed(() => Math.round((completedCount.value / achievements.length) * 100))
</script>

<style scoped lang="scss">
.achievement-view {
  max-width: 800px;
  margin: 0 auto;
}

.achievement-header {
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

.achievement-stats {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.stat-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-4);
  background: linear-gradient(135deg, var(--bg-card), var(--bg-secondary));
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
}

.stat-value {
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--text-gold);
  margin-bottom: var(--space-1);
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.achievement-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}

.achievement-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  transition: all 0.2s;
  position: relative;

  &:hover {
    border-color: var(--border-active);
  }

  &.is-completed {
    border-color: rgba(212, 175, 55, 0.3);
    background: rgba(212, 175, 55, 0.05);
  }
}

.achievement-icon {
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

.achievement-info {
  flex: 1;
  min-width: 0;
}

.achievement-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.achievement-desc {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  margin: 0 0 var(--space-2);
}

.achievement-progress {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.progress-bar {
  flex: 1;
  height: 6px;
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
  flex-shrink: 0;
}

.completed-mark {
  position: absolute;
  top: var(--space-2);
  right: var(--space-2);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(39, 174, 96, 0.2);
  color: #27AE60;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
}

@media (max-width: 640px) {
  .achievement-grid {
    grid-template-columns: 1fr;
  }
}
</style>
