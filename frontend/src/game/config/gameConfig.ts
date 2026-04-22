/**
 * 游戏配置文件
 * 基于 FRONTEND_DESIGN.md 设计方案
 */

import Phaser from 'phaser'

/**
 * 游戏尺寸配置
 */
export const GAME_SIZE = {
  WIDTH: 1280,
  HEIGHT: 720
} as const

/**
 * 颜色配置 - 视觉设计规范
 */
export const COLORS = {
  // 主题色
  PRIMARY_GOLD: 0xFFD700,
  PRIMARY_PURPLE: 0x9C27B0,
  PRIMARY_BLUE: 0x2196F3,

  // 背景色
  BG_DARK: 0x1A1A2E,
  BG_MEDIUM: 0x16213E,
  BG_LIGHT: 0x0F3460,

  // 功能色
  SUCCESS: 0x38EF7D,
  DANGER: 0xF45C43,
  WARNING: 0xFFA726,
  INFO: 0x4FC3F7,

  // 境界色系
  REALM: {
    MORTAL: 0x9E9E9E,      // 凡人 - 灰色
    QI: 0x4FC3F7,          // 练气期 - 浅蓝
    FOUNDATION: 0x7C4DFF,  // 筑基期 - 紫色
    GOLDEN: 0xFFD700,      // 金丹期 - 金色
    NASCENT: 0xE91E63,     // 元婴期 - 粉红
    IMMORTAL: 0x00BCD4,    // 化神期 - 青色
    UNITY: 0xFF9800,       // 合体期 - 橙色
    TRIBULATION: 0x9C27B0  // 渡劫期 - 深紫
  },

  // 五行色系
  ELEMENT: {
    METAL: 0xFFC107,       // 金 - 金色
    WOOD: 0x4CAF50,        // 木 - 绿色
    WATER: 0x2196F3,       // 水 - 蓝色
    FIRE: 0xF44336,        // 火 - 红色
    EARTH: 0x795548        // 土 - 棕色
  }
} as const

/**
 * 动画时长配置
 */
export const DURATION = {
  // UI 动画
  BUTTON_CLICK: 150,
  PAGE_TRANSITION: 300,
  MODAL_OPEN: 200,
  TOAST: 3000,

  // 战斗动画
  ATTACK: 500,
  SKILL: 1000,
  DAMAGE_NUMBER: 1200,
  DEATH: 1000,

  // 特效动画
  BREAKTHROUGH: 3000,
  LEVEL_UP: 2000,
  TRIBULATION: 5000
} as const

/**
 * 缓动函数配置
 */
export const EASING = {
  LINEAR: 'Linear',
  EASE_OUT: 'Cubic.easeOut',
  EASE_IN: 'Cubic.easeIn',
  EASE_IN_OUT: 'Cubic.easeInOut',
  BACK: 'Back.easeOut',
  ELASTIC: 'Elastic.easeOut',
  BOUNCE: 'Bounce.easeOut',
  SINE: 'Sine.easeInOut'
} as const

/**
 * 粒子效果配置
 */
export const PARTICLE_CONFIG = {
  // 灵气粒子
  SPIRIT: {
    speed: { min: 50, max: 100 },
    angle: { min: 250, max: 290 },
    scale: { start: 0.6, end: 0 },
    alpha: { start: 1, end: 0 },
    lifespan: 3000,
    blendMode: 'ADD' as const,
    tint: [0x4FC3F7, 0x7C4DFF, 0x00BCD4] as number[]
  },

  // 剑气粒子
  SWORD: {
    speed: { min: 200, max: 400 },
    scale: { start: 0.8, end: 0 },
    alpha: { start: 1, end: 0 },
    lifespan: 500,
    blendMode: 'ADD' as const,
    tint: 0xFFD700
  },

  // 火焰粒子
  FIRE: {
    speed: { min: 50, max: 150 },
    angle: { min: 260, max: 280 },
    scale: { start: 1, end: 0 },
    alpha: { start: 1, end: 0 },
    lifespan: 1500,
    blendMode: 'ADD' as const,
    tint: [0xFF5722, 0xFF9800, 0xFFC107] as number[]
  },

  // 飞剑粒子
  FLYING_SWORD: {
    lifespan: 4000,
    speedY: { min: -100, max: -50 },
    scale: { start: 0.5, end: 0 },
    alpha: { start: 1, end: 0 },
    frequency: 200
  }
} as const

/**
 * 场景资源配置
 */
export const SCENE_ASSETS = {
  boot: {
    images: ['loading-bg', 'loading-bar'],
    audio: []
  },
  menu: {
    images: ['bg-main', 'logo', 'button'],
    audio: ['bgm-main', 'sfx-click']
  },
  character: {
    images: ['bg-character', 'player-sprite'],
    audio: ['bgm-character']
  },
  cultivate: {
    images: ['bg-cultivate', 'meditation-effect'],
    audio: ['bgm-cultivate', 'sfx-meditate', 'sfx-breakthrough']
  },
  battle: {
    images: ['bg-battle', 'battle-ground', 'effect-sword-slash'],
    audio: ['bgm-battle', 'sfx-sword', 'sfx-hit', 'sfx-victory']
  },
  worldmap: {
    images: ['bg-worldmap', 'map-marker'],
    audio: ['bgm-explore']
  }
} as const

/**
 * 获取 Phaser 游戏配置
 */
export function getGameConfig(parent: string, scenes: Phaser.Scene[]): Phaser.Types.Core.GameConfig {
  return {
    type: Phaser.AUTO,
    width: GAME_SIZE.WIDTH,
    height: GAME_SIZE.HEIGHT,
    parent: parent,
    backgroundColor: '#1a1a2e',

    scene: scenes,

    physics: {
      default: 'arcade',
      arcade: {
        gravity: { x: 0, y: 0 },
        debug: false
      }
    },

    audio: {
      disableWebAudio: false
    },

    render: {
      pixelArt: true,
      antialias: false
    },

    scale: {
      mode: Phaser.Scale.FIT,
      autoCenter: Phaser.Scale.CENTER_BOTH
    }
  }
}
