<template>
  <div class="app-layout">
    <AppHeader />
    <AppSidebar />
    <main class="app-layout__main">
      <router-view />
    </main>
    <AppRightPanel class="hidden-mobile" />
    <AppMobileNav class="hidden-desktop" />
  </div>
</template>

<script setup lang="ts">
import AppHeader from '../AppHeader/AppHeader.vue'
import AppSidebar from '../AppSidebar/AppSidebar.vue'
import AppRightPanel from '../AppRightPanel/AppRightPanel.vue'
import AppMobileNav from '../AppMobileNav/AppMobileNav.vue'
</script>

<style scoped lang="scss">
.app-layout {
  min-height: 100vh;
  background: var(--bg-primary);

  &__main {
    margin-left: var(--layout-sidebar-left);
    margin-right: var(--layout-sidebar-right);
    margin-top: var(--layout-header-height);
    padding: var(--layout-content-padding);
    min-height: calc(100vh - var(--layout-header-height));
    transition: margin 0.3s var(--ease-default);
  }
}

@media (max-width: 1024px) {
  .app-layout__main {
    margin-right: 0;
  }
}

@media (max-width: 640px) {
  .app-layout__main {
    margin-left: 0;
    margin-right: 0;
    margin-bottom: 64px;
    padding: var(--space-3);
    min-height: calc(100vh - var(--layout-header-height) - 64px);
  }
}
</style>
