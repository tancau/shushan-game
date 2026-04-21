export interface Skill {
  id: string
  name: string
  type: string
  level: number
  maxLevel: number
  description: string
  effect: string
  cultivationRequired: number
}

export interface SkillLearnResult {
  success: boolean
  message: string
  skill?: Skill
}
