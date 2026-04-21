<template>
  <div class="leaderboard-view">
    <div class="leaderboard-header">
      <h1 class="page-title">排行榜</h1>
      <p class="page-subtitle">全服修仙者排名</p>
    </div>

    <div class="leaderboard-content">
      <SsCard class="leaderboard-card">
        <div class="leaderboard-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            :class="['tab-btn', { 'is-active': activeTab === tab.key }]"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="leaderboard-list">
          <div class="list-header">
            <span class="col-rank">排名</span>
            <span class="col-name">道号</span>
            <span class="col-realm">境界</span>
            <span class="col-value">{{ activeTabLabel }}</span>
          </div>

          <div
            v-for="(item, index) in leaderboardData"
            :key="item.id"
            :class="['list-item', { 'is-top3': index < 3 }]"
          >
            <span class="col-rank">
              <span v-if="index < 3" class="rank-medal">{{ ['🥇', '🥈', '🥉'][index] }}</span>
              <span v-else class="rank-number">{{ index + 1 }}</span>
            </span>
            <span class="col-name">{{ item.name }}</span>
            <span class="col-realm" :style="{ color: getRealmColor(item.realm) }">{{ item.realm }}</span>
            <span class="col-value">{{ item.value.toLocaleString() }}</span>
          </div>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'

interface LeaderboardItem {
  id: string
  name: string
  realm: string
  value: number
}

const tabs = [
  { key: 'cultivation', label: '修为榜' },
  { key: 'combat', label: '战力榜' },
  { key: 'wealth', label: '财富榜' },
]

const activeTab = ref('cultivation')

const activeTabLabel = computed(() => {
  const labels: Record<string, string> = {
    cultivation: '修为',
    combat: '战力',
    wealth: '灵石',
  }
  return labels[activeTab.value] || '数值'
})

const leaderboardData = computed<LeaderboardItem[]>(() => {
  const data: Record<string, LeaderboardItem[]> = {
    cultivation: [
      { id: '1', name: '太虚真人', realm: '渡劫期', value: 850000 },
      { id: '2', name: '紫霞仙子', realm: '合体期', value: 620000 },
      { id: '3', name: '剑无尘', realm: '化神期', value: 480000 },
      { id: '4', name: '玉清子', realm: '化神期', value: 420000 },
      { id: '5', name: '血河老祖', realm: '元婴期', value: 350000 },
      { id: '6', name: '青云道长', realm: '元婴期', value: 280000 },
      { id: '7', name: '冰心', realm: '金丹期', value: 150000 },
      { id: '8', name: '烈焰', realm: '金丹期', value: 120000 },
      { id: '9', name: '风行', realm: '筑基期', value: 80000 },
      { id: '10', name: '剑心', realm: '筑基期', value: 65000 },
    ],
    combat: [
      { id: '1', name: '太虚真人', realm: '渡劫期', value: 9999 },
      { id: '2', name: '血河老祖', realm: '元婴期', value: 8500 },
      { id: '3', name: '剑无尘', realm: '化神期', value: 7200 },
      { id: '4', name: '紫霞仙子', realm: '合体期', value: 6800 },
      { id: '5', name: '玉清子', realm: '化神期', value: 5500 },
    ],
    wealth: [
      { id: '1', name: '太虚真人', realm: '渡劫期', value: 999999 },
      { id: '2', name: '玉清子', realm: '化神期', value: 850000 },
      { id: '3', name: '紫霞仙子', realm: '合体期', value: 720000 },
    ],
  }
  return data[activeTab.value] || []
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

function getRealmColor(realm: string) {
  return realmColors[realm] || '#95A5A6'
}
</script>

<style scoped lang="scss">
.leaderboard-view {
  max-width: 700px;
  margin: 0 auto;
}

.leaderboard-header {
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

.leaderboard-tabs {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-default);
}

.tab-btn {
  padding: var(--space-2) var(--space-4);
  background: transparent;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--border-active);
    color: var(--text-primary);
  }

  &.is-active {
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
    border-color: var(--color-primary-light);
    color: var(--text-primary);
  }
}

.leaderboard-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.list-header {
  display: grid;
  grid-template-columns: 80px 1fr 100px 100px;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-xs);
  color: var(--text-muted);
  font-weight: 500;
}

.list-item {
  display: grid;
  grid-template-columns: 80px 1fr 100px 100px;
  gap: var(--space-2);
  align-items: center;
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  transition: all 0.2s;

  &:hover {
    background: var(--bg-hover);
  }

  &.is-top3 {
    background: rgba(212, 175, 55, 0.05);
    border: 1px solid rgba(212, 175, 55, 0.1);
  }
}

.col-rank {
  text-align: center;
}

.rank-medal {
  font-size: 20px;
}

.rank-number {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.col-name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.col-realm {
  font-size: var(--text-xs);
  font-weight: 500;
}

.col-value {
  font-size: var(--text-sm);
  color: var(--text-gold);
  font-weight: 600;
  text-align: right;
}

@media (max-width: 640px) {
  .list-header,
  .list-item {
    grid-template-columns: 60px 1fr 80px 80px;
  }
}
</style>
