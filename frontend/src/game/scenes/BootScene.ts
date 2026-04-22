/**
 * 启动场景
 * 预加载地图背景，立即显示
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'

export class BootScene extends BaseScene {
  constructor() {
    super(SCENE_KEYS.BOOT)
  }

  protected onCreate(): void {
    this.createInitialBackground()
    this.setupLoadEvents()
    this.loadBaseAssets()
  }

  private createInitialBackground(): void {
    // 先显示纯色背景
    const graphics = this.add.graphics()
    graphics.fillGradientStyle(0x1a1a2e, 0x1a1a2e, 0x16213e, 0x16213e, 1)
    graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)
    
    // 显示加载提示
    const text = this.createText(this.centerX, this.centerY, '正在初始化...', {
      fontSize: '28px',
      color: '#FFD700'
    })
    text.setOrigin(0.5)
    
    // 闪烁动画
    this.tweens.add({
      targets: text,
      alpha: 0.5,
      duration: 500,
      yoyo: true,
      repeat: -1
    })
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
    // 预加载地图背景（PreloadScene会用到）
    this.load.image('bg-map', '/assets/images/maps/shushan_foot.png')
    
    // 粒子效果
    this.load.image('particle-light', '/assets/images/effects/particle-light.png')
    
    this.load.start()
  }
}
