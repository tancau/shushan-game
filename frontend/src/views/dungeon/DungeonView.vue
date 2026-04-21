<template>
  <div class="dungeon-view">
    <div class="dungeon-header">
      <h1 class="page-title">副本挑战</h1>
      <p class="page-subtitle">挑战秘境，获取珍稀奖励</p>
    </div>

    <div class="dungeon-list">
      <SsCard
        v-for="dungeon in dungeons"
        :key="dungeon.id"
        :title="dungeon.name"
        :class="['dungeon-card', { 'is-locked': dungeon.locked }]"
      >
        <div class="dungeon-info">
          <div class="dungeon-icon">{{ dungeon.icon }}</div>
          <div class="dungeon-meta">
            <div class="meta-row">
              <span class="difficulty-label">难度</span>
              <span class="difficulty-stars">{{ '★'.repeat(dungeon.difficulty) }}</span>
            </div>
            <div class="meta-row">
              <span class="reward-label">奖励</span>
              <span class="reward-text">{{ dungeon.rewards }}</span>
            </div>
            <div class="meta-row">
              <span class="level-label">推荐境界</span>
              <span class="level-text">{{ dungeon.recommendedRealm }}</span>
            </div>
          </div>
        </div>

        <p class="dungeon-description">{{ dungeon.description }}</p>

        <template #footer>
          <SsButton
            :type="dungeon.locked ? 'default' : 'primary'"
            block
            :disabled="dungeon.locked"
            @click="enterDungeon(dungeon.id)"
          >
            {{ dungeon.locked ? '未解锁' : '进入副本' }}
          </SsButton>
        </template>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'

interface Dungeon {
  id: string
  name: string
  icon: string
  difficulty: number
  rewards: string
  recommendedRealm: string
  description: string
  locked: boolean
}

const dungeons: Dungeon[] = [
  {
    id: 'beginner',
    name: '新手试炼',
    icon: '🏔️',
    difficulty: 1,
    rewards: '修为+100，灵石+20',
    recommendedRealm: '练气期',
    description: '适合初入修仙之路的道友，难度较低，可获得基础修炼资源',
    locked: false,
  },
  {
    id: 'spirit-mine',
    name: '灵矿秘境',
    icon: '⛏️',
    difficulty: 2,
    rewards: '灵石+100，矿石',
    recommendedRealm: '筑基期',
    description: '蕴藏着丰富灵矿的秘境，可采集大量灵石和珍稀矿石',
    locked: false,
  },
  {
    id: 'beast-valley',
    name: '万兽谷',
    icon: '🐉',
    difficulty: 3,
    rewards: '灵兽蛋，修为+300',
    recommendedRealm: '金丹期',
    description: '各类妖兽聚集之地，击败它们可获得灵兽蛋和大量修为',
    locked: true,
  },
  {
    id: 'ancient-tomb',
    name: '古修洞府',
    icon: '🏛️',
    difficulty: 4,
    rewards: '功法秘籍，法宝',
    recommendedRealm: '元婴期',
    description: '上古修士遗留的洞府，藏有珍贵的功法秘籍和法宝',
    locked: true,
  },
  {
    id: 'thunder-peak',
    name: '雷劫峰',
    icon: '⚡',
    difficulty: 5,
    rewards: '渡劫材料，神器',
    recommendedRealm: '化神期',
    description: '天雷汇聚之地，只有实力强大的修士才能在此生存',
    locked: true,
  },
]

function enterDungeon(id: string) {
  console.log('进入副本', id)
}
</script>

<style scoped lang="scss">
.dungeon-view {
  max-width: 900px;
  margin: 0 auto;
}

.dungeon-header {
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

.dungeon-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

.dungeon-card {
  &.is-locked {
    opacity: 0.6;
  }
}

.dungeon-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}

.dungeon-icon {
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

.dungeon-meta {
  flex: 1;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-1);
}

.difficulty-label,
.reward-label,
.level-label {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}

.difficulty-stars {
  font-size: var(--text-sm);
  color: #F39C12;
}

.reward-text,
.level-text {
  font-size: var(--text-xs);
  color: var(--text-primary);
}

.dungeon-description {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}
</style>
