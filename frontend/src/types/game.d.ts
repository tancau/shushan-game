/**
 * 游戏相关类型定义
 */

import Phaser from 'phaser'

/**
 * 场景键名类型
 */
export type SceneKey =
  | 'BootScene'
  | 'PreloadScene'
  | 'MainMenuScene'
  | 'CharacterScene'
  | 'CultivateScene'
  | 'BattleScene'
  | 'WorldMapScene'
  | 'DungeonScene'
  | 'TribulationScene'

/**
 * 玩家数据类型
 */
export interface PlayerData {
  id: string
  name: string
  realm: RealmType
  sect: string
  location: string
  cultivation: number
  maxCultivation: number
  hp: number
  maxHp: number
  mp: number
  maxMp: number
  spiritStones: number
  attack: number
  defense: number
  speed: number
}

/**
 * 境界类型
 */
export type RealmType =
  | '凡人'
  | '练气期'
  | '筑基期'
  | '金丹期'
  | '元婴期'
  | '化神期'
  | '合体期'
  | '渡劫期'
  | '飞升'

/**
 * 战斗角色类型
 */
export interface BattleCharacter {
  id: string
  name: string
  sprite: Phaser.GameObjects.Sprite
  hp: number
  maxHp: number
  attack: number
  defense: number
  speed: number
  x: number
  y: number
}

/**
 * 战斗结果类型
 */
export interface BattleResult {
  victory: boolean
  exp: number
  spiritStones: number
  items: ItemDrop[]
}

/**
 * 物品掉落类型
 */
export interface ItemDrop {
  id: string
  name: string
  type: 'artifact' | 'pill' | 'material'
  quantity: number
}

/**
 * 地点类型
 */
export interface Location {
  id: string
  name: string
  x: number
  y: number
  danger: number
  description: string
  unlocked: boolean
  requiredRealm?: RealmType
}

/**
 * 技能类型
 */
export interface Skill {
  id: string
  name: string
  type: 'attack' | 'defense' | 'support'
  element: ElementType
  damage: number
  mpCost: number
  cooldown: number
  description: string
}

/**
 * 五行元素类型
 */
export type ElementType = 'metal' | 'wood' | 'water' | 'fire' | 'earth'

/**
 * 法宝类型
 */
export interface Artifact {
  id: string
  name: string
  type: 'weapon' | 'armor' | 'accessory'
  element: ElementType
  attack: number
  defense: number
  special: string
  level: number
  equipped: boolean
}

/**
 * 丹药类型
 */
export interface Pill {
  id: string
  name: string
  type: 'healing' | 'cultivation' | 'breakthrough'
  effect: number
  quantity: number
}

/**
 * 任务类型
 */
export interface Quest {
  id: string
  name: string
  description: string
  type: 'main' | 'side' | 'daily'
  status: 'pending' | 'in_progress' | 'completed'
  rewards: QuestReward[]
}

/**
 * 任务奖励类型
 */
export interface QuestReward {
  type: 'exp' | 'spiritStones' | 'item'
  amount: number
  itemId?: string
}

/**
 * 成就类型
 */
export interface Achievement {
  id: string
  name: string
  description: string
  type: 'cultivation' | 'combat' | 'exploration' | 'collection'
  unlocked: boolean
  progress: number
  target: number
}

/**
 * 游戏配置类型
 */
export interface GameConfig {
  bgmVolume: number
  sfxVolume: number
  autoSave: boolean
  language: 'zh-CN' | 'en-US'
}

/**
 * 存档类型
 */
export interface SaveData {
  id: string
  name: string
  timestamp: number
  player: PlayerData
  config: GameConfig
}
