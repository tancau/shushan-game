import apiClient from './index'
import type { ApiResponse, CombatResult } from '@/types'

export const combatApi = {
  startBattle(): Promise<ApiResponse<{ message: string }>> {
    return apiClient.get('/api/battle')
  },

  attack(): Promise<ApiResponse<CombatResult>> {
    return apiClient.get('/api/battle/attack')
  },

  defend(): Promise<ApiResponse<CombatResult>> {
    return apiClient.get('/api/battle/defend')
  },

  flee(): Promise<ApiResponse<CombatResult>> {
    return apiClient.get('/api/battle/flee')
  },

  useSkill(skillId: string): Promise<ApiResponse<CombatResult>> {
    return apiClient.get('/api/battle/skill', { params: { skill_id: skillId } })
  },
}
