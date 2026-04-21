import apiClient from './index'
import type { ApiResponse, Player } from '@/types'

export const playerApi = {
  getStatus(): Promise<ApiResponse<Player>> {
    return apiClient.get('/api/status')
  },

  cultivate(method: string): Promise<ApiResponse<{ cultivation: number; message: string }>> {
    return apiClient.get('/api/cultivate', { params: { method } })
  },

  advance(): Promise<ApiResponse<{ message: string }>> {
    return apiClient.get('/api/advance')
  },

  getArtifacts(): Promise<ApiResponse<{ artifacts: import('@/types').Artifact[] }>> {
    return apiClient.get('/api/artifacts')
  },

  getSkills(): Promise<ApiResponse<{ skills: import('@/types').Skill[] }>> {
    return apiClient.get('/api/skills')
  },

  travel(location: string): Promise<ApiResponse<{ message: string }>> {
    return apiClient.post('/api/travel', { location })
  },
}
