import apiClient from './index'
import type { ApiResponse, MapLocation, ExploreResult } from '@/types'

export const worldApi = {
  getMap(): Promise<ApiResponse<{ locations: MapLocation[]; currentLocation: string }>> {
    return apiClient.get('/api/map')
  },

  explore(): Promise<ApiResponse<ExploreResult>> {
    return apiClient.get('/api/explore')
  },

  travel(location: string): Promise<ApiResponse<{ message: string }>> {
    return apiClient.post('/api/travel', { location })
  },
}
