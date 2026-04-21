<template>
  <div class="auth-layout">
    <div class="auth-layout__background"></div>
    <div class="auth-layout__content">
      <router-view />
    </div>
  </div>
</template>

<style scoped lang="scss">
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;

  &__background {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 50%, #0f1419 100%);

    &::before {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at 30% 20%, rgba(45, 90, 123, 0.15) 0%, transparent 50%),
                  radial-gradient(ellipse at 70% 80%, rgba(139, 105, 20, 0.1) 0%, transparent 50%);
    }
  }

  &__content {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 420px;
    padding: var(--space-6);
  }
}
</style>
