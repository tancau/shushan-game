/**
 * 场景基类
 * 提供通用的场景功能
 */

import Phaser from 'phaser'
import { COLORS, DURATION, EASING } from '../config/gameConfig'

/**
 * 场景过渡配置
 */
interface TransitionConfig {
  duration?: number
  targetScene: string
  data?: object
}

/**
 * 基础场景类
 */
export abstract class BaseScene extends Phaser.Scene {
  // 场景是否已初始化
  protected isInitialized = false

  // UI 容器
  protected uiContainer!: Phaser.GameObjects.Container

  // 场景中心点
  protected centerX!: number
  protected centerY!: number

  constructor(sceneKey: string) {
    super({ key: sceneKey })
  }

  /**
   * 场景初始化
   */
  init(data?: object): void {
    this.centerX = this.cameras.main.width / 2
    this.centerY = this.cameras.main.height / 2
    this.isInitialized = true
  }

  /**
   * 场景创建
   */
  create(data?: object): void {
    // 创建 UI 容器
    this.uiContainer = this.add.container(0, 0)
    this.uiContainer.setDepth(100)

    // 子类实现
    this.onCreate(data)
  }

  /**
   * 子类实现的创建方法
   */
  protected abstract onCreate(data?: object): void

  /**
   * 创建背景
   */
  protected createBackgroundWithTexture(textureKey: string): Phaser.GameObjects.TileSprite {
    const bg = this.add.tileSprite(
      this.centerX,
      this.centerY,
      this.cameras.main.width,
      this.cameras.main.height,
      textureKey
    )
    bg.setDepth(-1)
    return bg
  }

  /**
   * 创建渐变背景
   */
  protected createGradientBackground(color1: number = COLORS.BG_DARK, color2: number = COLORS.BG_MEDIUM): Phaser.GameObjects.Graphics {
    const graphics = this.add.graphics()
    graphics.fillGradientStyle(color1, color1, color2, color2, 1)
    graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)
    graphics.setDepth(-1)
    return graphics
  }

  /**
   * 创建按钮
   */
  protected createButton(
    x: number,
    y: number,
    text: string,
    callback: () => void,
    style: Phaser.Types.GameObjects.Text.TextStyle = {}
  ): Phaser.GameObjects.Container {
    const container = this.add.container(x, y)

    // 默认按钮样式
    const defaultStyle: Phaser.Types.GameObjects.Text.TextStyle = {
      fontSize: '24px',
      color: '#FFD700',
      stroke: '#000000',
      strokeThickness: 4,
      ...style
    }

    // 创建按钮背景
    const bg = this.add.rectangle(0, 0, 200, 50, COLORS.BG_MEDIUM, 0.8)
    bg.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 创建按钮文字
    const buttonText = this.add.text(0, 0, text, defaultStyle)
    buttonText.setOrigin(0.5)

    container.add([bg, buttonText])
    container.setSize(200, 50)
    container.setInteractive({ useHandCursor: true })

    // 悬停效果
    container.on('pointerover', () => {
      this.tweens.add({
        targets: container,
        scale: 1.1,
        duration: DURATION.BUTTON_CLICK,
        ease: EASING.EASE_OUT
      })
      bg.setFillStyle(COLORS.BG_LIGHT, 0.9)
    })

    container.on('pointerout', () => {
      this.tweens.add({
        targets: container,
        scale: 1,
        duration: DURATION.BUTTON_CLICK,
        ease: EASING.EASE_OUT
      })
      bg.setFillStyle(COLORS.BG_MEDIUM, 0.8)
    })

    // 点击效果
    container.on('pointerdown', () => {
      this.tweens.add({
        targets: container,
        scale: 0.95,
        duration: 50,
        yoyo: true,
        onComplete: callback
      })
    })

    return container
  }

  /**
   * 创建文本
   */
  protected createText(
    x: number,
    y: number,
    text: string,
    style: Phaser.Types.GameObjects.Text.TextStyle = {}
  ): Phaser.GameObjects.Text {
    const defaultStyle: Phaser.Types.GameObjects.Text.TextStyle = {
      fontSize: '20px',
      color: '#FFFFFF',
      stroke: '#000000',
      strokeThickness: 2,
      ...style
    }

    return this.add.text(x, y, text, defaultStyle)
  }

  /**
   * 创建进度条
   */
  protected createProgressBar(
    x: number,
    y: number,
    width: number,
    height: number = 20
  ): { bg: Phaser.GameObjects.Rectangle; bar: Phaser.GameObjects.Rectangle } {
    // 背景
    const bg = this.add.rectangle(x, y, width, height, 0x333333)
    bg.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 进度条
    const bar = this.add.rectangle(x - width / 2 + 2, y, 0, height - 4, COLORS.PRIMARY_GOLD)
    bar.setOrigin(0, 0.5)

    return { bg, bar }
  }

  /**
   * 更新进度条
   */
  protected updateProgressBar(
    bar: Phaser.GameObjects.Rectangle,
    progress: number,
    maxWidth: number
  ): void {
    const width = Math.max(0, Math.min(maxWidth, maxWidth * progress))
    this.tweens.add({
      targets: bar,
      width: width,
      duration: 200,
      ease: EASING.EASE_OUT
    })
  }

  /**
   * 显示消息
   */
  protected showMessage(
    message: string,
    duration: number = DURATION.TOAST,
    style: Phaser.Types.GameObjects.Text.TextStyle = {}
  ): Phaser.GameObjects.Text {
    const defaultStyle: Phaser.Types.GameObjects.Text.TextStyle = {
      fontSize: '24px',
      color: '#FFFFFF',
      stroke: '#000000',
      strokeThickness: 4,
      ...style
    }

    const text = this.createText(this.centerX, this.centerY, message, defaultStyle)
    text.setOrigin(0.5)
    text.setDepth(1000)

    // 淡入淡出动画
    text.setAlpha(0)
    this.tweens.add({
      targets: text,
      alpha: 1,
      duration: 200,
      yoyo: true,
      hold: duration - 400,
      onComplete: () => text.destroy()
    })

    return text
  }

  /**
   * 显示伤害数字
   */
  protected showDamageNumber(
    x: number,
    y: number,
    damage: number,
    isPlayer: boolean = false
  ): void {
    const color = isPlayer ? '#ff4444' : '#4FC3F7'
    const text = this.add.text(x, y, `-${damage}`, {
      fontSize: '40px',
      color: color,
      stroke: '#000000',
      strokeThickness: 6
    }).setOrigin(0.5)

    // 放大+上升动画
    this.tweens.add({
      targets: text,
      y: y - 100,
      scale: 1.5,
      alpha: 0,
      duration: DURATION.DAMAGE_NUMBER,
      ease: EASING.EASE_OUT,
      onComplete: () => text.destroy()
    })
  }

  /**
   * 场景过渡
   */
  protected transitionTo(config: TransitionConfig): void {
    const duration = config.duration || DURATION.PAGE_TRANSITION

    // 淡出当前场景
    this.cameras.main.fadeOut(duration, 0, 0, 0)

    this.time.delayedCall(duration, () => {
      this.scene.start(config.targetScene, config.data)
    })
  }

  /**
   * 屏幕震动
   */
  protected shake(intensity: number = 0.01, duration: number = 200): void {
    this.cameras.main.shake(duration, intensity)
  }

  /**
   * 延迟执行
   */
  protected delay(ms: number): Promise<void> {
    return new Promise(resolve => {
      this.time.delayedCall(ms, resolve)
    })
  }
}
