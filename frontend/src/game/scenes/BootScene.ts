/**
 * 启动场景
 * 负责游戏初始化和基础资源加载
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS } from '../config/gameConfig'

export class BootScene extends BaseScene {
  constructor() {
    super(SCENE_KEYS.BOOT)
  }

  protected onCreate(): void {
    // 设置加载事件
    this.setupLoadEvents()

    // 加载基础资源
    this.loadBaseAssets()
  }

  /**
   * 设置加载事件监听
   */
  private setupLoadEvents(): void {
    // 加载完成事件
    this.load.once('complete', () => {
      this.transitionTo({ targetScene: SCENE_KEYS.PRELOAD })
    })

    // 加载错误事件
    this.load.on('loaderror', (file: Phaser.Loader.File) => {
      console.error(`加载资源失败: ${file.key}`, file)
    })
  }

  /**
   * 加载基础资源
   */
  private loadBaseAssets(): void {
    // 加载进度条背景
    this.load.image('loading-bg', '/assets/images/ui/loading-bg.png')
    this.load.image('loading-bar', '/assets/images/ui/loading-bar.png')

    // 加载基础粒子
    this.load.image('particle-spirit', '/assets/images/effects/particle-spirit.png')
    this.load.image('particle-sword', '/assets/images/effects/particle-sword.png')
    this.load.image('particle-fire', '/assets/images/effects/particle-fire.png')
    this.load.image('particle-light', '/assets/images/effects/particle-light.png')

    // 开始加载
    this.load.start()
  }

  /**
   * 创建简单的加载提示（在资源加载前显示）
   */
  private createLoadingHint(): void {
    const text = this.createText(
      this.centerX,
      this.centerY,
      '正在初始化游戏...',
      { fontSize: '28px', color: '#FFD700' }
    )
    text.setOrigin(0.5)

    // 简单的闪烁动画
    this.tweens.add({
      targets: text,
      alpha: 0.5,
      duration: 500,
      yoyo: true,
      repeat: -1
    })
  }
}
