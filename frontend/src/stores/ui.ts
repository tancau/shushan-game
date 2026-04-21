import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const sidebarCollapsed = ref(false)
  const rightPanelCollapsed = ref(false)
  const currentTheme = ref<'dark' | 'light'>('dark')
  const isMobile = ref(false)

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function toggleRightPanel() {
    rightPanelCollapsed.value = !rightPanelCollapsed.value
  }

  function setMobile(value: boolean) {
    isMobile.value = value
    if (value) {
      sidebarCollapsed.value = true
      rightPanelCollapsed.value = true
    }
  }

  return {
    sidebarCollapsed,
    rightPanelCollapsed,
    currentTheme,
    isMobile,
    toggleSidebar,
    toggleRightPanel,
    setMobile,
  }
})
