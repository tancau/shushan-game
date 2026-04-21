<template>
  <div class="skill-view">
    <div class="skill-header">
      <h1 class="page-title">功法</h1>
      <p class="page-subtitle">学习和升级功法，提升战斗能力</p>
    </div>

    <div class="skill-content">
      <SsCard title="已学功法" class="learned-skills-card">
        <div class="skills-list">
          <div
            v-for="skill in learnedSkills"
            :key="skill.id"
            :class="['skill-item', { 'is-main': skill.id === playerStore.player?.mainSkillId }]"
            @click="selectSkill(skill)"
          >
            <div class="skill-icon">📜</div>
            <div class="skill-info">
              <h4 class="skill-name">{{ skill.name }}</h4>
              <div class="skill-level">
                <div class="level-bar">
                  <div class="level-fill" :style="{ width: (skill.level / skill.maxLevel * 100) + '%' }" />
                </div>
                <span class="level-text">Lv.{{ skill.level }}/{{ skill.maxLevel }}</span>
              </div>
            </div>
            <div v-if="skill.id === playerStore.player?.mainSkillId" class="main-mark">主修</div>
          </div>
          <div v-if="learnedSkills.length === 0" class="empty-state">
            尚未学习任何功法
          </div>
        </div>
      </SsCard>

      <SsCard v-if="selectedSkill" title="功法详情" class="skill-detail-card">
        <div class="detail-header">
          <div class="detail-icon">📜</div>
          <div class="detail-info">
            <h3 class="detail-name">{{ selectedSkill.name }}</h3>
            <span class="detail-level">等级 {{ selectedSkill.level }}/{{ selectedSkill.maxLevel }}</span>
          </div>
        </div>

        <div class="detail-description">
          <p>{{ selectedSkill.description }}</p>
        </div>

        <div class="detail-effect">
          <h4>效果</h4>
          <p>{{ selectedSkill.effect }}</p>
        </div>

        <div class="detail-actions">
          <SsButton
            v-if="selectedSkill.id !== playerStore.player?.mainSkillId"
            type="primary"
            block
            @click="setMainSkill(selectedSkill.id)"
          >
            设为主修
          </SsButton>
          <SsButton
            type="gold"
            block
            :disabled="selectedSkill.level >= selectedSkill.maxLevel"
            @click="upgradeSkill(selectedSkill.id)"
          >
            升级功法
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
import type { LearnedSkill } from '@/types'

const playerStore = usePlayerStore()

const selectedSkill = ref<LearnedSkill | null>(null)

const learnedSkills = computed(() => playerStore.player?.skills || [])

function selectSkill(skill: LearnedSkill) {
  selectedSkill.value = skill
}

function setMainSkill(id: string) {
  console.log('设为主修功法', id)
}

function upgradeSkill(id: string) {
  console.log('升级功法', id)
}
</script>

<style scoped lang="scss">
.skill-view {
  max-width: 900px;
  margin: 0 auto;
}

.skill-header {
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

.skill-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.skills-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.skill-item {
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

  &.is-main {
    border-color: var(--color-primary-light);
    background: rgba(45, 90, 123, 0.1);
  }
}

.skill-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.skill-info {
  flex: 1;
}

.skill-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.skill-level {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.level-bar {
  flex: 1;
  height: 6px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.level-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
  border-radius: var(--radius-full);
  transition: width 0.3s;
}

.level-text {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  width: 60px;
  text-align: right;
}

.main-mark {
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

.detail-icon {
  font-size: 36px;
  width: 56px;
  height: 56px;
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

.detail-level {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.detail-description {
  margin-bottom: var(--space-4);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);

  p {
    font-size: var(--text-sm);
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
  }
}

.detail-effect {
  margin-bottom: var(--space-4);

  h4 {
    font-size: var(--text-sm);
    color: var(--text-secondary);
    margin: 0 0 var(--space-2);
  }

  p {
    font-size: var(--text-base);
    color: var(--text-primary);
    margin: 0;
    padding: var(--space-3);
    background: var(--bg-card);
    border-radius: var(--radius-md);
    border-left: 3px solid var(--color-primary);
  }
}

.detail-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

@media (max-width: 768px) {
  .skill-content {
    grid-template-columns: 1fr;
  }
}
</style>
