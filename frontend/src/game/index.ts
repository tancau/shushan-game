/**
 * 游戏模块入口
 * 导出所有游戏相关功能
 */

// 游戏主类
export { ShushanGame, createGame, destroyGame, SCENE_KEYS, GAME_SIZE } from './Game'

// 场景
export { BaseScene } from './scenes/BaseScene'
export { BootScene } from './scenes/BootScene'
export { PreloadScene } from './scenes/PreloadScene'
export { MainMenuScene } from './scenes/MainMenuScene'
export { CharacterScene } from './scenes/CharacterScene'
export { CultivateScene } from './scenes/CultivateScene'
export { BattleScene } from './scenes/BattleScene'
export { WorldMapScene } from './scenes/WorldMapScene'
export { DungeonScene } from './scenes/DungeonScene'
export { TribulationScene } from './scenes/TribulationScene'

// 配置
export {
  COLORS,
  DURATION,
  EASING,
  PARTICLE_CONFIG,
  SCENE_ASSETS,
  getGameConfig
} from './config/gameConfig'

// 音效
export {
  AudioManager,
  audioManager,
  playBGM,
  stopBGM,
  playSFX
} from './audio/AudioManager'

// 粒子特效
export {
  ParticleFactory,
  EffectPlayer,
  type ParticleType
} from './effects/particles/ParticleEffects'
