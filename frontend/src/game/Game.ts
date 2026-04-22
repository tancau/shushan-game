/**
 * 蜀山剑侠传 - 游戏主类
 * 基于 Phaser 3 游戏引擎
 */

import Phaser from 'phaser'
import { getGameConfig, GAME_SIZE } from './config/gameConfig'

// 导入所有场景
import { BootScene } from './scenes/BootScene'
import { PreloadScene } from './scenes/PreloadScene'
import { MainMenuScene } from './scenes/MainMenuScene'
import { CharacterScene } from './scenes/CharacterScene'
import { CultivateScene } from './scenes/CultivateScene'
import { BattleScene } from './scenes/BattleScene'
import { WorldMapScene } from './scenes/WorldMapScene'
import { DungeonScene } from './scenes/DungeonScene'
import { TribulationScene } from './scenes/TribulationScene'

/**
 * 场景键名常量
 */
export const SCENE_KEYS = {
  BOOT: 'BootScene',
  PRELOAD: 'PreloadScene',
  MAIN_MENU: 'MainMenuScene',
  CHARACTER: 'CharacterScene',
  CULTIVATE: 'CultivateScene',
  BATTLE: 'BattleScene',
  WORLD_MAP: 'WorldMapScene',
  DUNGEON: 'DungeonScene',
  TRIBULATION: 'TribulationScene'
} as const

/**
 * 蜀山剑侠传游戏类
 */
export class ShushanGame extends Phaser.Game {
  private static instance: ShushanGame | null = null

  /**
   * 私有构造函数，实现单例模式
   */
  private constructor(parent: string) {
    const config = {
      type: Phaser.AUTO,
      width: GAME_SIZE.WIDTH,
      height: GAME_SIZE.HEIGHT,
      parent: parent,
      backgroundColor: '#1a1a2e',
      scene: [
        BootScene,
        PreloadScene,
        MainMenuScene,
        CharacterScene,
        CultivateScene,
        BattleScene,
        WorldMapScene,
        DungeonScene,
        TribulationScene
      ],
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

    super(config)
  }

  /**
   * 获取游戏实例（单例）
   */
  public static getInstance(parent: string = 'game-container'): ShushanGame {
    if (!ShushanGame.instance) {
      ShushanGame.instance = new ShushanGame(parent)
    }
    return ShushanGame.instance
  }

  /**
   * 销毁游戏实例
   */
  public static destroyInstance(): void {
    if (ShushanGame.instance) {
      ShushanGame.instance.destroy(true)
      ShushanGame.instance = null
    }
  }

  /**
   * 切换到指定场景
   */
  public switchScene(sceneKey: string, data?: object): void {
    this.scene.start(sceneKey, data)
  }

  /**
   * 获取当前活动场景
   */
  public getActiveScene(): Phaser.Scene | null {
    // 遍历所有场景找到活动的
    const keys = Object.keys(this.scene.keys)
    for (const key of keys) {
      const scene = this.scene.getScene(key)
      if (scene && scene.scene.isActive()) {
        return scene
      }
    }
    return null
  }

  /**
   * 暂停游戏
   */
  public pauseGame(): void {
    const activeScene = this.getActiveScene()
    if (activeScene) {
      activeScene.scene.pause()
    }
  }

  /**
   * 恢复游戏
   */
  public resumeGame(): void {
    const activeScene = this.getActiveScene()
    if (activeScene) {
      activeScene.scene.resume()
    }
  }
}

/**
 * 创建游戏实例的便捷函数
 */
export function createGame(parent: string = 'game-container'): ShushanGame {
  return ShushanGame.getInstance(parent)
}

/**
 * 销毁游戏实例的便捷函数
 */
export function destroyGame(): void {
  ShushanGame.destroyInstance()
}

// 导出游戏尺寸
export { GAME_SIZE }
