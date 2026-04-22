/**
 * 天劫场景
 * 渡劫特效、飞升动画
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS, DURATION, EASING } from '../config/gameConfig'

export class TribulationScene extends BaseScene {
  private tribulationCount = 1
  private maxTribulation = 9
  private isUndergoing = false

  constructor() {
    super(SCENE_KEYS.TRIBULATION)
  }

  protected onCreate(): void {
    this.createBackgroundWithTexture()
    this.createBackButton()
    this.createTitle()
    this.createTribulationInfo()
    this.createLightningEffect()
    this.createActionButtons()
    this.playBackgroundMusic()
  }

  private setupBackground(): void {
    if (this.textures.exists('bg-tribulation')) {
      this.createBackgroundWithTexture('bg-tribulation')
    } else {
      const graphics = this.add.graphics()
      graphics.fillGradientStyle(0x0D1B2A, 0x0D1B2A, COLORS.BG_DARK, COLORS.BG_DARK, 1)
      graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)
      graphics.setDepth(-1)
    }

    // 添加乌云效果
    this.createClouds()
  }

  private createClouds(): void {
    for (let i = 0; i < 5; i++) {
      const cloud = this.add.rectangle(
        Math.random() * this.cameras.main.width,
        50 + Math.random() * 100,
        200 + Math.random() * 200,
        60,
        0x333333,
        0.6
      )
      
      this.tweens.add({
        targets: cloud,
        x: cloud.x + (Math.random() > 0.5 ? 100 : -100),
        duration: 5000 + Math.random() * 5000,
        yoyo: true,
        repeat: -1
      })
    }
  }

  private createBackButton(): void {
    const backButton = this.createButton(100, 40, '返回', () => {
      if (this.isUndergoing) {
        this.showMessage('渡劫中，无法离开！', 1500, { color: '#F45C43' })
        return
      }
      this.sound.play('sfx-click', { volume: 0.7 })
      this.transitionTo({ targetScene: SCENE_KEYS.CHARACTER })
    })
    backButton.setScale(0.8)
  }

  private createTitle(): void {
    const title = this.createText(this.centerX, 40, '天劫', { fontSize: '32px', color: '#F45C43', strokeThickness: 6 })
    title.setOrigin(0.5)
  }

  private createTribulationInfo(): void {
    const panelY = 200
    
    const panel = this.add.rectangle(this.centerX, panelY, 500, 200, COLORS.BG_MEDIUM, 0.8)
    panel.setStrokeStyle(2, COLORS.DANGER)

    const title = this.createText(this.centerX, panelY - 70, '【天劫信息】', { fontSize: '24px', color: '#F45C43' })
    title.setOrigin(0.5)

    const countText = this.createText(this.centerX, panelY - 20, `当前: 第 ${this.tribulationCount} 重天劫`, { fontSize: '20px' })
    countText.setOrigin(0.5)

    const maxText = this.createText(this.centerX, panelY + 20, `共需渡过: ${this.maxTribulation} 重`, { fontSize: '18px', color: '#4FC3F7' })
    maxText.setOrigin(0.5)

    const warningText = this.createText(this.centerX, panelY + 60, '渡劫失败将损失大量修为！', { fontSize: '16px', color: '#FFA726' })
    warningText.setOrigin(0.5)
  }

  private createLightningEffect(): void {
    // 闪电效果容器
    const lightningContainer = this.add.container(this.centerX, 350)
    
    // 定期闪电视觉效果
    this.time.addEvent({
      delay: 3000,
      callback: () => {
        if (!this.isUndergoing) return
        
        // 闪电
        const lightning = this.add.rectangle(
          this.centerX + (Math.random() - 0.5) * 200,
          350,
          10,
          400,
          0xFFFFFF,
          0.8
        )
        
        this.tweens.add({
          targets: lightning,
          alpha: 0,
          duration: 200,
          onComplete: () => lightning.destroy()
        })
        
        // 屏幕闪烁
        this.cameras.main.flash(100, 255, 255, 255)
      },
      loop: true
    })
  }

  private createActionButtons(): void {
    const buttonY = 500

    this.createButton(this.centerX - 150, buttonY, '开始渡劫', () => this.startTribulation())
    this.createButton(this.centerX + 150, buttonY, '查看准备', () => this.showPreparation())
  }

  private startTribulation(): void {
    if (this.isUndergoing) return
    
    this.sound.play('sfx-breakthrough', { volume: 0.7 })
    this.isUndergoing = true
    
    this.showMessage(`第 ${this.tribulationCount} 重天劫降临！`, 2000, { color: '#F45C43' })
    
    // 渡劫过程
    this.time.delayedCall(2000, () => {
      this.undergoTribulation()
    })
  }

  private undergoTribulation(): void {
    // 模拟渡劫过程
    const success = Math.random() > 0.3 // 70% 成功率
    
    // 多次闪电
    for (let i = 0; i < 5; i++) {
      this.time.delayedCall(i * 500, () => {
        this.shake(0.03, 300)
        this.cameras.main.flash(100, 255, 255, 255)
      })
    }

    this.time.delayedCall(3000, () => {
      if (success) {
        this.onTribulationSuccess()
      } else {
        this.onTribulationFailed()
      }
    })
  }

  private onTribulationSuccess(): void {
    this.isUndergoing = false
    this.tribulationCount++
    
    // 成功特效
    this.showSuccessEffect()
    this.sound.play('sfx-victory', { volume: 0.7 })
    
    if (this.tribulationCount > this.maxTribulation) {
      this.showMessage('恭喜飞升成功！', 3000, { color: '#FFD700' })
      this.time.delayedCall(3000, () => {
        this.transitionTo({ targetScene: SCENE_KEYS.MAIN_MENU })
      })
    } else {
      this.showMessage(`第 ${this.tribulationCount - 1} 重天劫渡过！`, 3000, { color: '#38EF7D' })
    }
  }

  private showSuccessEffect(): void {
    if (this.textures.exists('particle-light')) {
      this.add.particles(this.centerX, 350, 'particle-light', {
        speed: { min: 200, max: 400 },
        angle: { min: 0, max: 360 },
        scale: { start: 1, end: 0 },
        lifespan: 2000,
        quantity: 100,
        blendMode: 'ADD',
        tint: [0xFFD700, 0x4FC3F7, 0x38EF7D]
      }).explode()
    }
  }

  private onTribulationFailed(): void {
    this.isUndergoing = false
    this.sound.play('sfx-defeat', { volume: 0.7 })
    
    this.showMessage('渡劫失败！修为大损...', 3000, { color: '#F45C43' })
    
    this.time.delayedCall(3000, () => {
      this.transitionTo({ targetScene: SCENE_KEYS.CULTIVATE })
    })
  }

  private showPreparation(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    this.showMessage('建议: 准备好丹药、法宝后再渡劫', 2500)
  }

  private playBackgroundMusic(): void {
    if (this.sound.get('bgm-tribulation')) {
      this.sound.play('bgm-tribulation', { loop: true, volume: 0.5 })
    }
  }
}
