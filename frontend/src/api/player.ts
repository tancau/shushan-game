import apiClient from './index'
import type { PlayerStatusApiResponse, CultivateApiResponse, AdvanceApiResponse } from '@/types'
import type { ApiResponse, Player, Artifact, Skill } from '@/types'

export const playerApi = {
  getStatus(): Promise<PlayerStatusApiResponse> {
    return apiClient.get('/api/status')
  },

  cultivate(method: string): Promise<CultivateApiResponse> {
    return apiClient.get('/api/cultivate', { params: { method } })
  },

  advance(): Promise<AdvanceApiResponse> {
    return apiClient.get('/api/advance')
  },

  getArtifacts(): Promise<ApiResponse<{ artifacts: Artifact[] }>> {
    return apiClient.get('/api/artifacts')
  },

  getSkills(): Promise<ApiResponse<{ skills: Skill[] }>> {
    return apiClient.get('/api/skills')
  },

  travel(location: string): Promise<ApiResponse<{ message: string }>> {
    return apiClient.post('/api/travel', { location })
  },
}
