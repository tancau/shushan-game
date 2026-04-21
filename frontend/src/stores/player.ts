import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Player, PlayerStatusApiResponse } from '@/types'
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
      const res: PlayerStatusApiResponse = await playerApi.getStatus()
      if (res.success) {
        // 解析 API 返回的数据（snake_case -> camelCase）
        const hpParts = (res.hp || '100/100').split('/')
        const mpParts = (res.mp || '100/100').split('/')
        
        player.value = {
          name: res.name || '未知',
          realm: res.realm as any || '练气期',
          cultivation: parseInt(String(res.cultivation || '0').replace(/,/g, '')),
          spiritStones: parseInt(String(res.spirit_stones || '0').replace(/,/g, '')),
          stats: {
            hp: parseInt(hpParts[1] || '100') || 100,
            mp: parseInt(mpParts[1] || '100') || 100,
            attack: 10,
            defense: 5,
            speed: 10,
            wisdom: 10,
            luck: 5,
          },
          currentHp: parseInt(hpParts[0] || '100') || 100,
          maxHp: parseInt(hpParts[1] || '100') || 100,
          currentMp: parseInt(mpParts[0] || '100') || 100,
          maxMp: parseInt(mpParts[1] || '100') || 100,
          sect: (res.sect || null) as any,
          location: res.location || '峨眉山脚',
          artifacts: [],
          equippedArtifact: res.equipped_artifact ? { id: '1', name: res.equipped_artifact } as any : null,
          skills: [],
          mainSkillId: null,
          activeQuests: [],
          completedQuests: [],
          karma: 0,
          playTime: 0,
        }
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
