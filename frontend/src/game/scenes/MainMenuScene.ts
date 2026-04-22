/**
 * 主菜单场景
 * 游戏主界面 - 使用生成的美术资源
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS } from '../config/gameConfig'

export class MainMenuScene extends BaseScene {
  constructor() {
    super(SCENE_KEYS.MAIN_MENU)
  }

  protected onCreate(): void {
    this.createBackground()
    this.createLogo()
    this.createParticles()
    this.createMenuButtons()
    this.playBackgroundMusic()
  }

  private createBackground(): void {
    // 使用生成的地图背景
    if (this.textures.exists('bg-map')) {
      const bg = this.add.image(this.centerX, this.centerY, 'bg-map')
      bg.setScale(0.8) // 适配屏幕
    } else {
      // 备用渐变背景
      const graphics = this.add.graphics()
      graphics.fillGradientStyle(0x1a1a2e, 0x1a1a2e, 0x16213e, 0x16213e, 1)
      graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)
    }
  }

  private createLogo(): void {
    // 游戏标题
    const titleText = this.createText(this.centerX, 150, '蜀山剑侠传', {
      fontSize: '64px',
      color: '#FFD700',
      strokeThickness: 8
    })
    titleText.setOrigin(0.5)

    // 光效动画
    this.tweens.add({
      targets: titleText,
      alpha: 0.7,
      duration: 2000,
      yoyo: true,
      repeat: -1
    })

    // 副标题
    const subtitle = this.createText(this.centerX, 220, 'JRPG Demo', {
      fontSize: '24px',
      color: '#4FC3F7'
    })
    subtitle.setOrigin(0.5)
  }

  private createParticles(): void {
    // 灵气粒子效果
    if (this.textures.exists('particle-light')) {
      this.add.particles(this.centerX, this.centerY, 'particle-light', {
        speed: { min: 20, max: 50 },
        angle: { min: 0, max: 360 },
        scale: { start: 0.4, end: 0 },
        alpha: { start: 0.6, end: 0 },
        lifespan: 4000,
        frequency: 300,
        blendMode: 'ADD'
      })
    }
  }

  private createMenuButtons(): void {
    const buttonY = 350
    const spacing = 70

    // 开始游戏
    this.createButton(this.centerX, buttonY, '开始游戏', () => this.startGame())

    // 排行榜
    this.createButton(this.centerX, buttonY + spacing, '排行榜', () => {
      this.showMessage('排行榜功能开发中...', 2000)
    })

    // 设置
    this.createButton(this.centerX, buttonY + spacing * 2, '设置', () => {
      this.showMessage('设置功能开发中...', 2000)
    })
  }

  private playBackgroundMusic(): void {
    if (this.sound.get('bgm-battle')) {
      this.sound.play('bgm-battle', { loop: true, volume: 0.5 })
    }
  }

  private startGame(): void {
    if (this.sound.get('sfx-click')) {
      this.sound.play('sfx-click', { volume: 0.7 })
    }
    this.transitionTo({ targetScene: SCENE_KEYS.WORLD_MAP })
  }
}
