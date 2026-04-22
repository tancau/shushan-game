/**
 * 主菜单场景
 * 游戏主界面，包含开始游戏、排行榜、设置等入口
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS, DURATION, EASING, PARTICLE_CONFIG } from '../config/gameConfig'

export class MainMenuScene extends BaseScene {
  private logo!: Phaser.GameObjects.Image
  private particles!: Phaser.GameObjects.Particles.ParticleEmitter

  constructor() {
    super(SCENE_KEYS.MAIN_MENU)
  }

  protected onCreate(): void {
    // 创建背景
    this.createBackgroundWithTexture()

    // 创建 Logo
    this.createLogo()

    // 创建粒子效果
    this.createParticles()

    // 创建菜单按钮
    this.createMenuButtons()

    // 播放背景音乐
    this.playBackgroundMusic()
  }

  /**
   * 创建背景
   */
  private setupBackground(): void {
    // 尝试加载背景图片，如果不存在则使用纯色背景
    if (this.textures.exists('bg-main')) {
      const bg = this.add.tileSprite(
        this.centerX,
        this.centerY,
        this.cameras.main.width,
        this.cameras.main.height,
        'bg-main'
      )
      bg.setDepth(-1)

      // 云雾飘动效果
      this.tweens.add({
        targets: bg,
        tilePositionX: bg.tilePositionX + 100,
        duration: 20000,
        repeat: -1
      })
    } else {
      // 使用渐变背景
      const graphics = this.add.graphics()
      graphics.fillGradientStyle(
        COLORS.BG_DARK,
        COLORS.BG_DARK,
        COLORS.BG_MEDIUM,
        COLORS.BG_MEDIUM,
        1
      )
      graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)
      graphics.setDepth(-1)
    }
  }

  /**
   * 创建 Logo
   */
  private createLogo(): void {
    if (this.textures.exists('logo')) {
      this.logo = this.add.image(this.centerX, 150, 'logo')
    } else {
      // 使用文字作为 Logo
      this.logo = this.add.image(this.centerX, 150, '__DEFAULT')

      const logoText = this.createText(
        this.centerX,
        150,
        '蜀山剑侠传',
        { fontSize: '64px', color: '#FFD700', strokeThickness: 8 }
      )
      logoText.setOrigin(0.5)

      // Logo 光效
      this.tweens.add({
        targets: logoText,
        alpha: 0.7,
        duration: 2000,
        yoyo: true,
        repeat: -1
      })
    }

    // Logo 缩放动画
    this.tweens.add({
      targets: this.logo,
      scale: 1.05,
      duration: 1500,
      yoyo: true,
      repeat: -1,
      ease: EASING.SINE
    })
  }

  /**
   * 创建粒子效果
   */
  private createParticles(): void {
    // 飞剑粒子（从下往上飘动）
    if (this.textures.exists('particle-sword')) {
      this.add.particles(0, 0, 'particle-sword', {
        x: { min: 0, max: this.cameras.main.width },
        y: this.cameras.main.height,
        lifespan: PARTICLE_CONFIG.FLYING_SWORD.lifespan,
        speedY: PARTICLE_CONFIG.FLYING_SWORD.speedY,
        scale: PARTICLE_CONFIG.FLYING_SWORD.scale,
        alpha: PARTICLE_CONFIG.FLYING_SWORD.alpha,
        frequency: PARTICLE_CONFIG.FLYING_SWORD.frequency,
        blendMode: 'ADD'
      })
    }

    // 灵气粒子（环形扩散）
    if (this.textures.exists('particle-spirit')) {
      this.add.particles(this.centerX, this.centerY, 'particle-spirit', {
        speed: { min: 20, max: 50 },
        angle: { min: 0, max: 360 },
        scale: { start: 0.4, end: 0 },
        alpha: { start: 0.6, end: 0 },
        lifespan: 4000,
        frequency: 300,
        blendMode: 'ADD',
        tint: PARTICLE_CONFIG.SPIRIT.tint
      })
    }
  }

  /**
   * 创建菜单按钮
   */
  private createMenuButtons(): void {
    const buttonY = 350
    const spacing = 70

    // 开始游戏按钮
    const startButton = this.createButton(
      this.centerX,
      buttonY,
      '开始游戏',
      () => this.startGame()
    )

    // 排行榜按钮
    const leaderboardButton = this.createButton(
      this.centerX,
      buttonY + spacing,
      '排行榜',
      () => this.showLeaderboard()
    )

    // 设置按钮
    const settingsButton = this.createButton(
      this.centerX,
      buttonY + spacing * 2,
      '设置',
      () => this.showSettings()
    )

    // 按钮入场动画
    const buttons = [startButton, leaderboardButton, settingsButton]
    buttons.forEach((btn, index) => {
      btn.setAlpha(0)
      btn.setY(btn.y + 50)

      this.tweens.add({
        targets: btn,
        alpha: 1,
        y: btn.y - 50,
        duration: 500,
        delay: index * 150,
        ease: EASING.BACK
      })
    })
  }

  /**
   * 播放背景音乐
   */
  private playBackgroundMusic(): void {
    if (this.sound.get('bgm-main')) {
      this.sound.play('bgm-main', { loop: true, volume: 0.5 })
    }
  }

  /**
   * 开始游戏
   */
  private startGame(): void {
    // 播放点击音效
    this.sound.play('sfx-click', { volume: 0.7 })

    // 切换到角色场景
    this.transitionTo({ targetScene: SCENE_KEYS.CHARACTER })
  }

  /**
   * 显示排行榜
   */
  private showLeaderboard(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    this.showMessage('排行榜功能开发中...', 2000)
  }

  /**
   * 显示设置
   */
  private showSettings(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    this.showMessage('设置功能开发中...', 2000)
  }
}
