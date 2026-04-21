import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Notification } from '@/types'

export const useGameStore = defineStore('game', () => {
  const currentLocation = ref('峨眉山脚')
  const notifications = ref<Notification[]>([])
  const isInCombat = ref(false)
  const isAutoCultivating = ref(false)

  function addNotification(message: string, type: 'success' | 'error' | 'info' = 'info') {
    const id = Date.now()
    notifications.value.push({ id, message, type })
    setTimeout(() => {
      removeNotification(id)
    }, 3000)
  }

  function removeNotification(id: number) {
    const index = notifications.value.findIndex((n) => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  return {
    currentLocation,
    notifications,
    isInCombat,
    isAutoCultivating,
    addNotification,
    removeNotification,
  }
})
