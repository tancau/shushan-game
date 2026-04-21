export interface MapLocation {
  id: string
  name: string
  region: string
  type: 'city' | 'wilderness' | 'dungeon' | 'sect' | 'special'
  dangerLevel: number
  resources: string[]
  connections: string[]
  description: string
}

export interface ExploreResult {
  success: boolean
  message: string
  eventType: 'resource' | 'encounter' | 'treasure' | 'nothing'
  rewards?: {
    cultivation?: number
    spiritStones?: number
    items?: string[]
  }
}
