export interface CombatResult {
  success: boolean
  message: string
  turn: number
  playerDamage?: number
  enemyDamage?: number
  winner?: 'player' | 'enemy' | null
  rewards?: CombatRewards
}

export interface CombatRewards {
  cultivation: number
  spiritStones: number
  artifact?: import('./player').Artifact
}
