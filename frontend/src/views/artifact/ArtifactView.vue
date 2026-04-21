<template>
  <div class="artifact-view">
    <div class="artifact-header">
      <h1 class="page-title">法宝</h1>
      <p class="page-subtitle">管理和强化您的法宝</p>
    </div>

    <div class="artifact-content">
      <SsCard title="法宝列表" class="artifact-list-card">
        <div class="artifact-grid">
          <div
            v-for="artifact in artifacts"
            :key="artifact.id"
            :class="['artifact-item', { 'is-equipped': artifact.equipped }]"
            @click="selectArtifact(artifact)"
          >
            <div class="artifact-icon" :style="{ background: getElementColor(artifact.element) }">
              {{ artifact.name[0] }}
            </div>
            <div class="artifact-info">
              <h4 class="artifact-name">{{ artifact.name }}</h4>
              <div class="artifact-meta">
                <span class="quality-badge" :class="`quality--${artifact.quality}`">{{ qualityLabels[artifact.quality] }}</span>
                <span class="element-tag">{{ artifact.element }}</span>
              </div>
              <div class="artifact-stats">
                <span>威力 {{ artifact.power }}</span>
                <span>速度 {{ artifact.speed }}</span>
              </div>
            </div>
            <div v-if="artifact.equipped" class="equipped-mark">装备中</div>
          </div>
        </div>
      </SsCard>

      <SsCard v-if="selectedArtifact" title="法宝详情" class="artifact-detail-card">
        <div class="detail-header">
          <div class="detail-icon" :style="{ background: getElementColor(selectedArtifact.element) }">
            {{ selectedArtifact.name[0] }}
          </div>
          <div class="detail-info">
            <h3 class="detail-name">{{ selectedArtifact.name }}</h3>
            <div class="detail-meta">
              <span class="quality-badge" :class="`quality--${selectedArtifact.quality}`">{{ qualityLabels[selectedArtifact.quality] }}</span>
              <span class="element-tag">{{ selectedArtifact.element }}</span>
              <span class="type-tag">{{ selectedArtifact.artifactType }}</span>
            </div>
          </div>
        </div>

        <div class="detail-stats">
          <div class="stat-item">
            <span class="stat-label">威力</span>
            <span class="stat-value">{{ selectedArtifact.power }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">速度</span>
            <span class="stat-value">{{ selectedArtifact.speed }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">等级</span>
            <span class="stat-value">{{ selectedArtifact.level }}/{{ selectedArtifact.maxLevel }}</span>
          </div>
        </div>

        <p class="detail-description">{{ selectedArtifact.description }}</p>

        <div class="detail-actions">
          <SsButton
            v-if="!selectedArtifact.equipped"
            type="primary"
            block
            @click="equipArtifact(selectedArtifact.id)"
          >
            装备
          </SsButton>
          <SsButton
            v-else
            type="ghost"
            block
            @click="unequipArtifact(selectedArtifact.id)"
          >
            卸下
          </SsButton>
          <SsButton
            type="gold"
            block
            :disabled="selectedArtifact.level >= selectedArtifact.maxLevel"
            @click="upgradeArtifact(selectedArtifact.id)"
          >
            强化
          </SsButton>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { usePlayerStore } from '@/stores/player'
import type { Artifact, Element, Quality } from '@/types'

const playerStore = usePlayerStore()

const selectedArtifact = ref<Artifact | null>(null)

const artifacts = computed(() => playerStore.player?.artifacts || [])

const qualityLabels: Record<Quality, string> = {
  common: '普通',
  uncommon: '优秀',
  rare: '稀有',
  epic: '史诗',
  legendary: '传说',
  mythic: '神话',
  divine: '神器',
}

const elementColors: Record<Element, string> = {
  '金': 'rgba(184, 184, 184, 0.3)',
  '木': 'rgba(39, 174, 96, 0.3)',
  '水': 'rgba(46, 134, 171, 0.3)',
  '火': 'rgba(231, 76, 60, 0.3)',
  '土': 'rgba(139, 69, 19, 0.3)',
}

function getElementColor(element: Element) {
  return elementColors[element] || 'rgba(255, 255, 255, 0.1)'
}

function selectArtifact(artifact: Artifact) {
  selectedArtifact.value = artifact
}

function equipArtifact(id: string) {
  console.log('装备法宝', id)
}

function unequipArtifact(id: string) {
  console.log('卸下法宝', id)
}

function upgradeArtifact(id: string) {
  console.log('强化法宝', id)
}
</script>

<style scoped lang="scss">
.artifact-view {
  max-width: 900px;
  margin: 0 auto;
}

.artifact-header {
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

.artifact-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.artifact-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.artifact-item {
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

  &.is-equipped {
    border-color: var(--color-primary-light);
    background: rgba(45, 90, 123, 0.1);
  }
}

.artifact-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  flex-shrink: 0;
}

.artifact-info {
  flex: 1;
}

.artifact-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.artifact-meta {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-1);
}

.artifact-stats {
  display: flex;
  gap: var(--space-3);
  font-size: var(--text-xs);
  color: var(--text-secondary);
}

.equipped-mark {
  position: absolute;
  top: var(--space-1);
  right: var(--space-2);
  font-size: var(--text-xs);
  color: var(--color-primary-light);
  font-weight: 500;
}

.quality-badge {
  font-size: var(--text-xs);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  font-weight: 500;

  &.quality--common {
    color: #95A5A6;
    border: 1px solid rgba(149, 165, 166, 0.3);
  }

  &.quality--uncommon {
    color: #27AE60;
    border: 1px solid rgba(39, 174, 96, 0.3);
  }

  &.quality--rare {
    color: #3498DB;
    border: 1px solid rgba(52, 152, 219, 0.3);
  }

  &.quality--epic {
    color: #9B59B6;
    border: 1px solid rgba(155, 89, 182, 0.3);
  }

  &.quality--legendary {
    color: #F39C12;
    border: 1px solid rgba(243, 156, 18, 0.3);
  }

  &.quality--mythic {
    color: #E74C3C;
    border: 1px solid rgba(231, 76, 60, 0.3);
  }

  &.quality--divine {
    color: #FFD700;
    border: 1px solid rgba(255, 215, 0, 0.3);
  }
}

.element-tag {
  font-size: var(--text-xs);
  padding: 1px 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}

.detail-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-default);
}

.detail-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 600;
  color: var(--text-primary);
  flex-shrink: 0;
}

.detail-info {
  flex: 1;
}

.detail-name {
  font-family: var(--font-title);
  font-size: var(--text-xl);
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.detail-meta {
  display: flex;
  gap: var(--space-2);
}

.type-tag {
  font-size: var(--text-xs);
  padding: 1px 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}

.detail-stats {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-3);
  background: var(--bg-card);
  border-radius: var(--radius-md);
}

.stat-label {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}

.stat-value {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.detail-description {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: var(--space-4);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.detail-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

@media (max-width: 768px) {
  .artifact-content {
    grid-template-columns: 1fr;
  }
}
</style>
