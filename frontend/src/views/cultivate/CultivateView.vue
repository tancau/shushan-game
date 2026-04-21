<template>
  <div class="cultivate-view">
    <div class="cultivate-header">
      <h1 class="page-title">修炼道场</h1>
      <p class="page-subtitle">选择修炼方式，提升修为境界</p>
    </div>

    <div class="cultivate-content">
      <SsCard title="修炼方式" class="methods-card">
        <div class="methods-list">
          <div
            v-for="method in cultivateMethods"
            :key="method.key"
            :class="['method-card', { 'is-selected': selectedMethod === method.key }]"
            @click="selectedMethod = method.key"
          >
            <div class="method-icon">{{ method.icon }}</div>
            <div class="method-info">
              <h4 class="method-name">{{ method.name }}</h4>
              <p class="method-desc">{{ method.description }}</p>
              <div class="method-tags">
                <span class="tag tag--gain">+{{ method.gain }}修为</span>
                <span v-if="method.mpCost > 0" class="tag tag--cost">-{{ method.mpCost }}真元</span>
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

        <div v-if="lastResult" class="cultivate-result animate-fade-in">
          <el-icon class="result-icon" :size="24"><CircleCheck /></el-icon>
          <p class="result-message">{{ lastResult.message }}</p>
          <p class="result-gain">修为 +{{ lastResult.gain }}</p>
        </div>
      </SsCard>

      <SsCard title="突破境界" class="advance-card">
        <div class="advance-info">
          <div class="current-realm">
            <span class="realm-label">当前境界</span>
            <span class="realm-value" :style="realmStyle">{{ playerStore.currentRealm }}</span>
          </div>
          <div class="cultivation-progress">
            <div class="progress-label">
              <span>修为进度</span>
              <span>{{ playerStore.player?.cultivation || 0 }} / {{ nextRealmRequirement }}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progressPercent + '%' }" />
            </div>
          </div>
        </div>

        <SsButton
          type="gold"
          size="large"
          block
          :disabled="!canAdvance"
          :loading="isAdvancing"
          @click="handleAdvance"
        >
          {{ canAdvance ? '突破境界' : '修为不足' }}
        </SsButton>

        <p v-if="advanceResult" class="advance-result" :class="advanceResult.type">
          {{ advanceResult.message }}
        </p>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElIcon } from 'element-plus'
import { CircleCheck } from '@element-plus/icons-vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { usePlayerStore } from '@/stores/player'

const playerStore = usePlayerStore()

const isCultivating = ref(false)
const isAdvancing = ref(false)
const selectedMethod = ref('吐纳')
const lastResult = ref<{ message: string; gain: number } | null>(null)
const advanceResult = ref<{ message: string; type: 'success' | 'error' } | null>(null)

const cultivateMethods = [
  { key: '打坐', name: '打坐', icon: '🧘', description: '静心打坐，稳固根基，消耗少收益稳', gain: 10, mpCost: 0 },
  { key: '吐纳', name: '吐纳', icon: '🌬️', description: '吐纳天地灵气，平衡消耗与收益', gain: 20, mpCost: 5 },
  { key: '悟道', name: '悟道', icon: '💭', description: '参悟天地大道，高收益高消耗', gain: 50, mpCost: 20 },
]

const realmRequirements: Record<string, number> = {
  '练气期': 1000,
  '筑基期': 5000,
  '金丹期': 15000,
  '元婴期': 40000,
  '化神期': 100000,
  '合体期': 250000,
  '渡劫期': 600000,
}

const nextRealmRequirement = computed(() => {
  return realmRequirements[playerStore.currentRealm] || 999999
})

const progressPercent = computed(() => {
  if (!playerStore.player) return 0
  return Math.min((playerStore.player.cultivation / nextRealmRequirement.value) * 100, 100)
})

const canAdvance = computed(() => {
  if (!playerStore.player) return false
  return playerStore.player.cultivation >= nextRealmRequirement.value
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

const realmStyle = computed(() => ({
  color: realmColors[playerStore.currentRealm] || '#95A5A6',
}))

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
      setTimeout(() => {
        lastResult.value = null
      }, 3000)
    }
  } finally {
    isCultivating.value = false
  }
}

async function handleAdvance() {
  if (!canAdvance.value || isAdvancing.value) return

  isAdvancing.value = true
  try {
    const result = await playerStore.advanceRealm()
    if (result.success) {
      advanceResult.value = { message: result.message || '突破成功！', type: 'success' }
    } else {
      advanceResult.value = { message: result.message || '突破失败', type: 'error' }
    }
    setTimeout(() => {
      advanceResult.value = null
    }, 5000)
  } finally {
    isAdvancing.value = false
  }
}
</script>

<style scoped lang="scss">
.cultivate-view {
  max-width: 600px;
  margin: 0 auto;
}

.cultivate-header {
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

.cultivate-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.methods-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.method-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
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
    background: rgba(45, 90, 123, 0.15);
    box-shadow: var(--shadow-primary);
  }
}

.method-icon {
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

.method-tags {
  display: flex;
  gap: var(--space-2);
}

.tag {
  font-size: var(--text-xs);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-weight: 500;

  &--gain {
    background: rgba(39, 174, 96, 0.2);
    color: #27AE60;
  }

  &--cost {
    background: rgba(46, 134, 171, 0.2);
    color: #2E86AB;
  }
}

.cultivate-action {
  margin-bottom: var(--space-4);
}

.cultivate-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4);
  background: rgba(39, 174, 96, 0.1);
  border: 1px solid rgba(39, 174, 96, 0.3);
  border-radius: var(--radius-md);
  text-align: center;
}

.result-icon {
  color: #27AE60;
}

.result-message {
  font-size: var(--text-base);
  color: var(--text-primary);
  margin: 0;
}

.result-gain {
  font-size: var(--text-lg);
  font-weight: 600;
  color: #27AE60;
  margin: 0;
}

.advance-info {
  margin-bottom: var(--space-4);
}

.current-realm {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}

.realm-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.realm-value {
  font-size: var(--text-lg);
  font-weight: 600;
}

.cultivation-progress {
  margin-bottom: var(--space-4);
}

.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-2);
}

.progress-bar {
  height: 12px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
  border-radius: var(--radius-full);
  transition: width 0.5s var(--ease-default);
}

.advance-result {
  text-align: center;
  margin-top: var(--space-3);
  padding: var(--space-2);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);

  &.success {
    background: rgba(39, 174, 96, 0.1);
    color: #27AE60;
  }

  &.error {
    background: rgba(231, 76, 60, 0.1);
    color: #E74C3C;
  }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
