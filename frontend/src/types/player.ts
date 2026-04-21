export interface Player {
  name: string
  realm: Realm
  cultivation: number
  spiritStones: number
  stats: PlayerStats
  currentHp: number
  maxHp: number
  currentMp: number
  maxMp: number
  sect: Sect | null
  location: string
  artifacts: Artifact[]
  equippedArtifact: Artifact | null
  skills: LearnedSkill[]
  mainSkillId: string | null
  activeQuests: string[]
  completedQuests: string[]
  karma: number
  playTime: number
}

export interface PlayerStats {
  hp: number
  mp: number
  attack: number
  defense: number
  speed: number
  wisdom: number
  luck: number
}

export type Realm =
  | '练气期'
  | '筑基期'
  | '金丹期'
  | '元婴期'
  | '化神期'
  | '合体期'
  | '渡劫期'

export type Sect = '峨眉派' | '青城派' | '昆仑派' | '血河教'

export type Element = '金' | '木' | '水' | '火' | '土'

export interface Artifact {
  id: string
  name: string
  artifactType: ArtifactType
  element: Element
  power: number
  speed: number
  level: number
  maxLevel: number
  description: string
  quality: Quality
}

export type ArtifactType = '飞剑' | '防御' | '攻击' | '辅助' | '特殊'

export type Quality =
  | 'common'
  | 'uncommon'
  | 'rare'
  | 'epic'
  | 'legendary'
  | 'mythic'
  | 'divine'

export interface LearnedSkill {
  id: string
  name: string
  level: number
  maxLevel: number
  description: string
}
