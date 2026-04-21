import type { Element, Quality, ArtifactType } from './player'

export interface ArtifactDetail {
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
  equipped: boolean
}

export interface ArtifactUpgradeResult {
  success: boolean
  message: string
  newLevel?: number
  newPower?: number
}
