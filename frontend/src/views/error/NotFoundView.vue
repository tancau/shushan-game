<template>
  <div class="not-found">
    <h1 class="not-found__title">404</h1>
    <p class="not-found__subtitle">此路不通，道友请回</p>
    <SsButton type="primary" @click="$router.push('/home')">
      返回修炼道场
    </SsButton>
  </div>
</template>

<script setup lang="ts">
import SsButton from '@/components/common/SsButton/SsButton.vue'
</script>

<style scoped lang="scss">
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;

  &__title {
    font-family: var(--font-title);
    font-size: 96px;
    color: var(--color-primary);
    margin: 0;
    opacity: 0.5;
  }

  &__subtitle {
    font-size: var(--text-xl);
    color: var(--text-secondary);
    margin: var(--space-4) 0 var(--space-6);
  }
}
</style>
