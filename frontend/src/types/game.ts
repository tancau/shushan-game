export interface Notification {
  id: number
  message: string
  type: 'success' | 'error' | 'info'
}

export interface GameState {
  currentLocation: string
  notifications: Notification[]
  isInCombat: boolean
  isAutoCultivating: boolean
}
