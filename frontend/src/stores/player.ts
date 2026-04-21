import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Player } from '@/types'
import { playerApi } from '@/api/player'

export const usePlayerStore = defineStore('player', () => {
  const player = ref<Player | null>(null)
  const isLoading = ref(false)
  const token = ref(localStorage.getItem('shushan_token') || '')

  const isLoggedIn = computed(() => !!player.value)
  const currentRealm = computed(() => player.value?.realm || '练气期')
  const canAdvance = computed(() => {
    if (!player.value) return false
    return false
  })

  async function fetchStatus() {
    isLoading.value = true
    try {
      const res = await playerApi.getStatus()
      if (res.success && res.data) {
        player.value = res.data as Player
      }
    } finally {
      isLoading.value = false
    }
  }

  async function cultivate(method: string = '吐纳') {
    try {
      const res = await playerApi.cultivate(method)
      if (res.success) {
        await fetchStatus()
      }
      return res
    } catch (error) {
      return { success: false, message: '修炼失败' }
    }
  }

  async function advanceRealm() {
    try {
      const res = await playerApi.advance()
      if (res.success) {
        await fetchStatus()
      }
      return res
    } catch (error) {
      return { success: false, message: '突破失败' }
    }
  }

  function logout() {
    player.value = null
    token.value = ''
    localStorage.removeItem('shushan_token')
  }

  return {
    player,
    isLoading,
    token,
    isLoggedIn,
    currentRealm,
    canAdvance,
    fetchStatus,
    cultivate,
    advanceRealm,
    logout,
  }
})
