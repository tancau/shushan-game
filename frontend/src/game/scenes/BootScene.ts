/**
 * 启动场景
 * 负责游戏初始化和基础资源加载
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'

export class BootScene extends BaseScene {
  constructor() {
    super(SCENE_KEYS.BOOT)
  }

  protected onCreate(): void {
    this.setupLoadEvents()
    this.loadBaseAssets()
  }

  private setupLoadEvents(): void {
    this.load.once('complete', () => {
      this.transitionTo({ targetScene: SCENE_KEYS.PRELOAD })
    })

    this.load.on('loaderror', (file: Phaser.Loader.File) => {
      console.error(`加载资源失败: ${file.key}`, file)
    })
  }

  private loadBaseAssets(): void {
    // 粒子效果
    this.load.image('particle-light', '/assets/images/effects/particle-light.png')
    this.load.image('particle-spirit', '/assets/images/effects/particle-spirit.png')
    
    // 开始加载
    this.load.start()
  }
}
