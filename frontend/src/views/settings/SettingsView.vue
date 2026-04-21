<template>
  <div class="settings-view">
    <div class="settings-header">
      <h1 class="page-title">设置</h1>
      <p class="page-subtitle">系统设置与个性化</p>
    </div>

    <div class="settings-content">
      <SsCard title="游戏设置" class="settings-card">
        <div class="setting-group">
          <h4 class="group-title">通知</h4>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-name">战斗通知</span>
              <span class="setting-desc">战斗结果自动弹出通知</span>
            </div>
            <div class="setting-control">
              <input type="checkbox" v-model="settings.battleNotification" class="toggle" />
            </div>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-name">修炼提醒</span>
              <span class="setting-desc">定时提醒修炼</span>
            </div>
            <div class="setting-control">
              <input type="checkbox" v-model="settings.cultivateReminder" class="toggle" />
            </div>
          </div>
        </div>

        <div class="setting-group">
          <h4 class="group-title">显示</h4>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-name">伤害数字</span>
              <span class="setting-desc">战斗中显示伤害数字</span>
            </div>
            <div class="setting-control">
              <input type="checkbox" v-model="settings.showDamage" class="toggle" />
            </div>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-name">动画效果</span>
              <span class="setting-desc">开启界面动画效果</span>
            </div>
            <div class="setting-control">
              <input type="checkbox" v-model="settings.animation" class="toggle" />
            </div>
          </div>
        </div>
      </SsCard>

      <SsCard title="账号" class="account-card">
        <div class="account-info">
          <div class="info-item">
            <span class="info-label">道号</span>
            <span class="info-value">{{ playerStore.player?.name || '未登录' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">门派</span>
            <span class="info-value">{{ playerStore.player?.sect || '无' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">游戏时长</span>
            <span class="info-value">{{ formatPlayTime }}</span>
          </div>
        </div>

        <div class="account-actions">
          <SsButton type="danger" block @click="logout">
            退出登录
          </SsButton>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { usePlayerStore } from '@/stores/player'

const router = useRouter()
const playerStore = usePlayerStore()

const settings = ref({
  battleNotification: true,
  cultivateReminder: false,
  showDamage: true,
  animation: true,
})

const formatPlayTime = computed(() => {
  const minutes = playerStore.player?.playTime || 0
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  if (hours > 0) {
    return `${hours}小时${mins}分钟`
  }
  return `${mins}分钟`
})

function logout() {
  playerStore.logout()
  router.push('/auth/login')
}
</script>

<style scoped lang="scss">
.settings-view {
  max-width: 600px;
  margin: 0 auto;
}

.settings-header {
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

.settings-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.setting-group {
  margin-bottom: var(--space-4);

  &:last-child {
    margin-bottom: 0;
  }
}

.group-title {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin: 0 0 var(--space-3);
  padding-bottom: var(--space-2);
  border-bottom: 1px solid var(--border-default);
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3) 0;
}

.setting-info {
  display: flex;
  flex-direction: column;
}

.setting-name {
  font-size: var(--text-base);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.setting-desc {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.toggle {
  appearance: none;
  width: 44px;
  height: 24px;
  background: var(--bg-hover);
  border-radius: var(--radius-full);
  position: relative;
  cursor: pointer;
  transition: all 0.2s;

  &::after {
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    width: 20px;
    height: 20px;
    background: var(--text-secondary);
    border-radius: 50%;
    transition: all 0.2s;
  }

  &:checked {
    background: var(--color-primary);

    &::after {
      left: 22px;
      background: var(--text-primary);
    }
  }
}

.account-info {
  margin-bottom: var(--space-4);
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--border-default);

  &:last-child {
    border-bottom: none;
  }
}

.info-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.info-value {
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-weight: 500;
}

.account-actions {
  padding-top: var(--space-4);
}
</style>
