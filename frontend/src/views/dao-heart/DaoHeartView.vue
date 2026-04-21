<template>
  <div class="dao-heart-view">
    <div class="dao-heart-header">
      <h1 class="page-title">道心</h1>
      <p class="page-subtitle">修炼道心，积累功德</p>
    </div>

    <div class="dao-heart-content">
      <SsCard title="道心状态" class="dao-status-card">
        <div class="karma-display">
          <div class="karma-value">
            <span class="karma-number">{{ playerStore.player?.karma || 0 }}</span>
            <span class="karma-label">功德值</span>
          </div>
          <div class="karma-bar">
            <div class="karma-fill" :style="{ width: karmaPercent + '%' }" />
          </div>
        </div>

        <div class="dao-level">
          <span class="level-label">道心境界</span>
          <span class="level-value">{{ daoLevel }}</span>
        </div>
      </SsCard>

      <SsCard title="功德商店" class="merit-shop-card">
        <div class="shop-items">
          <div
            v-for="item in shopItems"
            :key="item.id"
            class="shop-item"
          >
            <div class="item-icon">{{ item.icon }}</div>
            <div class="item-info">
              <h4 class="item-name">{{ item.name }}</h4>
              <p class="item-desc">{{ item.description }}</p>
            </div>
            <div class="item-price">
              <span class="price-value">{{ item.price }}</span>
              <span class="price-label">功德</span>
            </div>
            <SsButton
              type="gold"
              size="small"
              :disabled="(playerStore.player?.karma || 0) < item.price"
              @click="buyItem(item.id)"
            >
              兑换
            </SsButton>
          </div>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { usePlayerStore } from '@/stores/player'

const playerStore = usePlayerStore()

const karmaPercent = computed(() => {
  const karma = playerStore.player?.karma || 0
  return Math.min((karma / 1000) * 100, 100)
})

const daoLevel = computed(() => {
  const karma = playerStore.player?.karma || 0
  if (karma >= 1000) return '功德圆满'
  if (karma >= 500) return '道心坚定'
  if (karma >= 200) return '初悟大道'
  return '道心初立'
})

interface ShopItem {
  id: string
  name: string
  icon: string
  description: string
  price: number
}

const shopItems: ShopItem[] = [
  { id: 'pill-1', name: '洗髓丹', icon: '💊', description: '洗髓伐骨，提升修炼速度', price: 100 },
  { id: 'stone-1', name: '灵石袋', icon: '💰', description: '内含100灵石', price: 50 },
  { id: 'book-1', name: '功法残卷', icon: '📜', description: '可用于学习新功法', price: 200 },
  { id: 'artifact-1', name: '护身符', icon: '🧿', description: '战斗中自动防御一次', price: 150 },
]

function buyItem(id: string) {
  console.log('购买物品', id)
}
</script>

<style scoped lang="scss">
.dao-heart-view {
  max-width: 800px;
  margin: 0 auto;
}

.dao-heart-header {
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

.dao-heart-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.karma-display {
  text-align: center;
  padding: var(--space-4);
}

.karma-value {
  margin-bottom: var(--space-3);
}

.karma-number {
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--text-gold);
  display: block;
}

.karma-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.karma-bar {
  height: 12px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.karma-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-secondary), var(--color-secondary-light));
  border-radius: var(--radius-full);
  transition: width 0.5s;
}

.dao-level {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.level-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.level-value {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-gold);
}

.shop-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.shop-item {
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
}

.item-icon {
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

.item-info {
  flex: 1;
}

.item-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.item-desc {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  margin: 0;
}

.item-price {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 var(--space-3);
}

.price-value {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-gold);
}

.price-label {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}
</style>
