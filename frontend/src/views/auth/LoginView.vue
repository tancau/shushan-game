<template>
  <SsCard class="login-card" :hoverable="false">
    <template #header>
      <div class="login-header">
        <h1 class="login-title">⚔️ 蜀山剑侠传</h1>
        <p class="login-subtitle">踏入修仙之路</p>
      </div>
    </template>

    <form class="login-form" @submit.prevent="handleLogin">
      <div class="form-group">
        <label class="form-label">道号</label>
        <input
          v-model="form.name"
          type="text"
          class="form-input"
          placeholder="请输入您的道号"
          required
        />
      </div>

      <div class="form-group">
        <label class="form-label">选择门派</label>
        <div class="sect-grid">
          <div
            v-for="sect in sects"
            :key="sect.name"
            :class="['sect-item', { 'is-selected': form.sect === sect.name }]"
            @click="form.sect = sect.name"
          >
            <span class="sect-icon">{{ sect.icon }}</span>
            <span class="sect-name">{{ sect.name }}</span>
            <span class="sect-desc">{{ sect.description }}</span>
          </div>
        </div>
      </div>

      <SsButton type="gold" size="large" block :loading="isLoading" @click="handleLogin">
        踏入修仙路
      </SsButton>
    </form>

    <template #footer>
      <p class="login-quote">"蜀山万载，剑气纵横三万里"</p>
    </template>
  </SsCard>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { usePlayerStore } from '@/stores/player'

const router = useRouter()
const playerStore = usePlayerStore()

const isLoading = ref(false)

const form = reactive({
  name: '',
  sect: '峨眉派',
})

const sects = [
  { name: '峨眉派', icon: '🗡️', description: '剑法精妙，正气凛然' },
  { name: '青城派', icon: '🏔️', description: '道法自然，清静无为' },
  { name: '昆仑派', icon: '☁️', description: '仙风道骨，高深莫测' },
  { name: '血河教', icon: '🩸', description: '魔功霸道，实力强横' },
]

async function handleLogin() {
  if (!form.name || !form.sect) return

  isLoading.value = true
  try {
    localStorage.setItem('shushan_token', 'demo_token')
    await playerStore.fetchStatus()
    router.push('/home')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-card {
  background: rgba(36, 43, 61, 0.8) !important;
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-gold) !important;
}

.login-header {
  text-align: center;
  padding: var(--space-4) 0;
}

.login-title {
  font-family: var(--font-title);
  font-size: var(--text-2xl);
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.login-subtitle {
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  font-weight: 500;
}

.form-input {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  color: var(--text-primary);
  font-size: var(--text-base);
  transition: all 0.2s;

  &:focus {
    outline: none;
    border-color: var(--color-primary-light);
    box-shadow: 0 0 0 3px rgba(74, 139, 181, 0.1);
  }

  &::placeholder {
    color: var(--text-muted);
  }
}

.sect-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2);
}

.sect-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-3);
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--border-active);
  }

  &.is-selected {
    border-color: var(--color-primary-light);
    background: rgba(45, 90, 123, 0.2);
    box-shadow: var(--shadow-primary);
  }
}

.sect-icon {
  font-size: 24px;
}

.sect-name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.sect-desc {
  font-size: var(--text-xs);
  color: var(--text-muted);
  text-align: center;
}

.login-quote {
  text-align: center;
  font-family: var(--font-decorative);
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin: 0;
  font-style: italic;
}
</style>
