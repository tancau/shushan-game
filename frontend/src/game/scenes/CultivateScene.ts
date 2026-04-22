/**
 * 修炼场景
 * 打坐、突破、炼丹、炼器
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS, DURATION, EASING, PARTICLE_CONFIG } from '../config/gameConfig'

export class CultivateScene extends BaseScene {
  private spiritParticles!: Phaser.GameObjects.Particles.ParticleEmitter
  private playerSprite!: Phaser.GameObjects.Sprite
  private isMeditating = false
  private cultivationBar!: Phaser.GameObjects.Rectangle
  private cultivationText!: Phaser.GameObjects.Text

  // 模拟修炼数据
  private cultivation = 1000
  private maxCultivation = 10000

  constructor() {
    super(SCENE_KEYS.CULTIVATE)
  }

  protected onCreate(): void {
    // 创建背景
    this.createBackgroundWithTexture()

    // 创建返回按钮
    this.createBackButton()

    // 创建标题
    this.createTitle()

    // 创建打坐区域
    this.createMeditationArea()

    // 创建进度条
    this.createProgressBar()

    // 创建操作按钮
    this.createActionButtons()

    // 创建炼丹炼器面板
    this.createCraftingPanel()

    // 播放背景音乐
    this.playBackgroundMusic()
  }

  /**
   * 创建背景
   */
  private setupBackground(): void {
    if (this.textures.exists('bg-cultivate')) {
      this.createBackgroundWithTexture('bg-cultivate')
    } else {
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
   * 创建返回按钮
   */
  private createBackButton(): void {
    const backButton = this.createButton(100, 40, '返回', () => {
      this.stopMeditation()
      this.sound.play('sfx-click', { volume: 0.7 })
      this.transitionTo({ targetScene: SCENE_KEYS.CHARACTER })
    })
    backButton.setScale(0.8)
  }

  /**
   * 创建标题
   */
  private createTitle(): void {
    const title = this.createText(
      this.centerX,
      40,
      '修炼',
      { fontSize: '32px', color: '#FFD700', strokeThickness: 6 }
    )
    title.setOrigin(0.5)
  }

  /**
   * 创建打坐区域
   */
  private createMeditationArea(): void {
    const centerX = this.centerX
    const centerY = 250

    // 打坐区域背景
    const area = this.add.circle(centerX, centerY, 120, COLORS.BG_MEDIUM, 0.5)
    area.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 创建角色精灵
    if (this.textures.exists('player-sprite')) {
      this.playerSprite = this.add.sprite(centerX, centerY, 'player-sprite')
      this.playerSprite.setScale(1.5)
    } else {
      // 使用占位图形
      const graphics = this.add.graphics()
      graphics.fillStyle(COLORS.PRIMARY_GOLD, 0.8)
      graphics.fillCircle(centerX, centerY, 50)
      graphics.setDepth(1)

      this.playerSprite = this.add.sprite(centerX, centerY, '__DEFAULT')
    }

    // 创建灵气粒子系统
    if (this.textures.exists('particle-spirit')) {
      this.spiritParticles = this.add.particles(
        centerX,
        centerY + 50,
        'particle-spirit',
        {
          speed: PARTICLE_CONFIG.SPIRIT.speed,
          angle: PARTICLE_CONFIG.SPIRIT.angle,
          scale: PARTICLE_CONFIG.SPIRIT.scale,
          alpha: PARTICLE_CONFIG.SPIRIT.alpha,
          lifespan: PARTICLE_CONFIG.SPIRIT.lifespan,
          frequency: -1, // 暂停
          blendMode: PARTICLE_CONFIG.SPIRIT.blendMode,
          tint: PARTICLE_CONFIG.SPIRIT.tint
        }
      )
    }
  }

  /**
   * 创建进度条
   */
  private createProgressBar(): void {
    const barX = this.centerX
    const barY = 400
    const barWidth = 500

    // 背景
    const bg = this.add.rectangle(barX, barY, barWidth, 30, 0x333333)
    bg.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 进度条
    const progress = this.cultivation / this.maxCultivation
    this.cultivationBar = this.add.rectangle(
      barX - barWidth / 2 + 2,
      barY,
      (barWidth - 4) * progress,
      24,
      COLORS.INFO
    )
    this.cultivationBar.setOrigin(0, 0.5)

    // 文字
    this.cultivationText = this.createText(
      barX,
      barY,
      `${this.cultivation.toLocaleString()} / ${this.maxCultivation.toLocaleString()}`,
      { fontSize: '16px', color: '#FFFFFF' }
    )
    this.cultivationText.setOrigin(0.5)

    // 标签
    const label = this.createText(barX, barY - 30, '修为进度', {
      fontSize: '18px',
      color: '#FFD700'
    })
    label.setOrigin(0.5)
  }

  /**
   * 创建操作按钮
   */
  private createActionButtons(): void {
    const buttonY = 480
    const spacing = 180
    const startX = this.centerX - spacing

    // 打坐按钮
    const meditateButton = this.createButton(
      startX,
      buttonY,
      '打坐',
      () => this.toggleMeditation()
    )

    // 吐纳按钮
    const breatheButton = this.createButton(
      startX + spacing,
      buttonY,
      '吐纳',
      () => this.doBreathe()
    )

    // 突破按钮
    const breakthroughButton = this.createButton(
      startX + spacing * 2,
      buttonY,
      '突破',
      () => this.attemptBreakthrough()
    )

    // 修炼速度提示
    const speedText = this.createText(
      this.centerX,
      buttonY + 50,
      '修炼速度: +41% (功法加成)',
      { fontSize: '16px', color: '#4FC3F7' }
    )
    speedText.setOrigin(0.5)
  }

  /**
   * 创建炼丹炼器面板
   */
  private createCraftingPanel(): void {
    const panelX = this.centerX
    const panelY = 580

    // 面板背景
    const panel = this.add.rectangle(panelX, panelY, 500, 100, COLORS.BG_MEDIUM, 0.8)
    panel.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 标题
    const title = this.createText(panelX, panelY - 35, '【炼丹炼器】', {
      fontSize: '20px',
      color: '#FFD700'
    })
    title.setOrigin(0.5)

    // 按钮
    const buttonY = panelY + 10
    const spacing = 150

    const alchemyButton = this.createButton(
      panelX - spacing,
      buttonY,
      '炼丹',
      () => this.showAlchemy()
    )
    alchemyButton.setScale(0.7)

    const forgeButton = this.createButton(
      panelX,
      buttonY,
      '炼器',
      () => this.showForge()
    )
    forgeButton.setScale(0.7)

    const recipeButton = this.createButton(
      panelX + spacing,
      buttonY,
      '配方',
      () => this.showRecipe()
    )
    recipeButton.setScale(0.7)
  }

  /**
   * 切换打坐状态
   */
  private toggleMeditation(): void {
    if (this.isMeditating) {
      this.stopMeditation()
    } else {
      this.startMeditation()
    }
  }

  /**
   * 开始打坐
   */
  private startMeditation(): void {
    if (this.isMeditating) return

    this.isMeditating = true
    this.sound.play('sfx-meditate', { volume: 0.7 })

    // 启动粒子效果
    if (this.spiritParticles) {
      this.spiritParticles.start()
    }

    // 角色呼吸动画增强
    this.tweens.add({
      targets: this.playerSprite,
      scale: 1.6,
      alpha: 0.8,
      duration: 1000,
      yoyo: true,
      repeat: -1,
      ease: EASING.SINE
    })

    // 模拟修炼增加
    this.time.addEvent({
      delay: 1000,
      callback: () => {
        if (this.isMeditating) {
          this.addCultivation(20)
        }
      },
      loop: true
    })

    this.showMessage('开始打坐修炼...', 1500)
  }

  /**
   * 停止打坐
   */
  private stopMeditation(): void {
    if (!this.isMeditating) return

    this.isMeditating = false

    // 停止粒子效果
    if (this.spiritParticles) {
      this.spiritParticles.stop()
    }

    // 停止动画
    this.tweens.killTweensOf(this.playerSprite)
    this.playerSprite.setScale(1.5)
    this.playerSprite.setAlpha(1)
  }

  /**
   * 吐纳
   */
  private doBreathe(): void {
    this.sound.play('sfx-cultivate', { volume: 0.7 })

    // 显示吐纳效果
    const text = this.createText(
      this.centerX,
      250,
      '吐纳天地灵气...',
      { fontSize: '24px', color: '#4FC3F7' }
    )
    text.setOrigin(0.5)

    this.tweens.add({
      targets: text,
      alpha: 0,
      y: text.y - 50,
      duration: 1500,
      onComplete: () => {
        text.destroy()
        this.addCultivation(50)
        this.showMessage('吐纳完成，修为+50', 1500)
      }
    })
  }

  /**
   * 尝试突破
   */
  private attemptBreakthrough(): void {
    this.stopMeditation()
    this.sound.play('sfx-breakthrough', { volume: 0.7 })

    // 模拟突破
    const success = Math.random() > 0.5

    if (success) {
      this.showBreakthroughEffect()
    } else {
      this.sound.play('sfx-fail', { volume: 0.7 })
      this.showMessage('突破失败，继续修炼吧...', 2000)
    }
  }

  /**
   * 显示突破成功特效
   */
  private showBreakthroughEffect(): void {
    // 光柱效果
    const beam = this.add.rectangle(
      this.centerX,
      this.centerY,
      200,
      this.cameras.main.height,
      COLORS.PRIMARY_GOLD,
      0
    )

    this.tweens.add({
      targets: beam,
      alpha: 0.8,
      duration: 500,
      yoyo: true,
      hold: 2000,
      onComplete: () => beam.destroy()
    })

    // 粒子爆炸
    if (this.textures.exists('particle-light')) {
      this.add.particles(this.centerX, 250, 'particle-light', {
        speed: { min: 200, max: 400 },
        scale: { start: 1, end: 0 },
        lifespan: 2000,
        quantity: 50,
        blendMode: 'ADD'
      }).explode()
    }

    // 屏幕震动
    this.shake(0.02, 500)

    // 显示成功消息
    this.time.delayedCall(1000, () => {
      this.showMessage('突破成功！境界提升！', 3000, { color: '#FFD700' })
    })
  }

  /**
   * 增加修为
   */
  private addCultivation(amount: number): void {
    this.cultivation = Math.min(this.cultivation + amount, this.maxCultivation)

    // 更新进度条
    const barWidth = 500 - 4
    const progress = this.cultivation / this.maxCultivation

    this.tweens.add({
      targets: this.cultivationBar,
      width: barWidth * progress,
      duration: 300
    })

    // 更新文字
    this.cultivationText.setText(
      `${this.cultivation.toLocaleString()} / ${this.maxCultivation.toLocaleString()}`
    )

    // 显示修为增加
    const text = this.createText(
      this.centerX,
      280,
      `+${amount}`,
      { fontSize: '36px', color: '#4FC3F7', strokeThickness: 4 }
    )
    text.setOrigin(0.5)

    this.tweens.add({
      targets: text,
      y: text.y - 80,
      alpha: 0,
      duration: 1500,
      ease: EASING.EASE_OUT,
      onComplete: () => text.destroy()
    })
  }

  /**
   * 显示炼丹界面
   */
  private showAlchemy(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    this.showMessage('炼丹功能开发中...', 2000)
  }

  /**
   * 显示炼器界面
   */
  private showForge(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    this.showMessage('炼器功能开发中...', 2000)
  }

  /**
   * 显示配方界面
   */
  private showRecipe(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    this.showMessage('配方功能开发中...', 2000)
  }

  /**
   * 播放背景音乐
   */
  private playBackgroundMusic(): void {
    if (this.sound.get('bgm-cultivate')) {
      this.sound.play('bgm-cultivate', { loop: true, volume: 0.5 })
    }
  }
}
