/**
 * 角色场景
 * 显示角色信息、属性、装备等
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS, DURATION, EASING } from '../config/gameConfig'

interface PlayerData {
  name: string
  realm: string
  sect: string
  location: string
  cultivation: number
  maxCultivation: number
  hp: number
  maxHp: number
  mp: number
  maxMp: number
  spiritStones: number
}

export class CharacterScene extends BaseScene {
  private playerSprite!: Phaser.GameObjects.Sprite
  private realmAura!: Phaser.GameObjects.Arc
  private statsTexts: Map<string, Phaser.GameObjects.Text> = new Map()

  // 模拟玩家数据
  private playerData: PlayerData = {
    name: 'tancau',
    realm: '筑基期',
    sect: '峨眉派',
    location: '峨眉山脚',
    cultivation: 1000,
    maxCultivation: 10000,
    hp: 150,
    maxHp: 150,
    mp: 120,
    maxMp: 150,
    spiritStones: 1000
  }

  constructor() {
    super(SCENE_KEYS.CHARACTER)
  }

  protected onCreate(): void {
    // 创建背景
    this.setupBackground()

    // 创建返回按钮
    this.createBackButton()

    // 创建标题
    this.createTitle()

    // 创建角色精灵
    this.createPlayerSprite()

    // 创建信息面板
    this.createInfoPanel()

    // 创建属性面板
    this.createStatsPanel()

    // 创建装备面板
    this.createEquipmentPanel()

    // 创建底部标签
    this.createTabButtons()

    // 播放背景音乐
    this.playBackgroundMusic()
  }

  /**
   * 创建背景
   */
  private setupBackground(): void {
    if (this.textures.exists('bg-character')) {
      this.createBackgroundWithTexture('bg-character')
    } else {
      this.createGradientBackground()
    }
  }

  /**
   * 创建返回按钮
   */
  private createBackButton(): void {
    const backButton = this.createButton(100, 40, '返回', () => {
      this.sound.play('sfx-click', { volume: 0.7 })
      this.transitionTo({ targetScene: SCENE_KEYS.MAIN_MENU })
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
      '角色',
      { fontSize: '32px', color: '#FFD700', strokeThickness: 6 }
    )
    title.setOrigin(0.5)
  }

  /**
   * 创建角色精灵
   */
  private createPlayerSprite(): void {
    // 角色位置
    const spriteX = 200
    const spriteY = 280

    // 创建角色精灵
    if (this.textures.exists('player-sprite')) {
      this.playerSprite = this.add.sprite(spriteX, spriteY, 'player-sprite')
    } else {
      // 使用占位图形
      const graphics = this.add.graphics()
      graphics.fillStyle(COLORS.PRIMARY_GOLD, 0.8)
      graphics.fillCircle(spriteX, spriteY, 60)
      graphics.setDepth(1)

      // 创建一个假的 sprite 用于动画
      this.playerSprite = this.add.sprite(spriteX, spriteY, '__DEFAULT')
    }

    // 角色呼吸动画
    this.tweens.add({
      targets: this.playerSprite,
      y: spriteY - 5,
      duration: 2000,
      yoyo: true,
      repeat: -1,
      ease: EASING.SINE
    })

    // 创建境界光环
    this.createRealmAura(spriteX, spriteY)
  }

  /**
   * 创建境界光环
   */
  private createRealmAura(x: number, y: number): void {
    // 根据境界获取颜色
    const realmColors: Record<string, number> = {
      '凡人': COLORS.REALM.MORTAL,
      '练气期': COLORS.REALM.QI,
      '筑基期': COLORS.REALM.FOUNDATION,
      '金丹期': COLORS.REALM.GOLDEN,
      '元婴期': COLORS.REALM.NASCENT,
      '化神期': COLORS.REALM.IMMORTAL,
      '合体期': COLORS.REALM.UNITY,
      '渡劫期': COLORS.REALM.TRIBULATION
    }

    const color = realmColors[this.playerData.realm] || COLORS.REALM.QI

    // 创建光环
    this.realmAura = this.add.circle(x, y, 80, color, 0.3)
    this.realmAura.setStrokeStyle(2, color)

    // 光环脉冲动画
    this.tweens.add({
      targets: this.realmAura,
      scale: 1.2,
      alpha: 0.5,
      duration: 1500,
      yoyo: true,
      repeat: -1
    })
  }

  /**
   * 创建信息面板
   */
  private createInfoPanel(): void {
    const panelX = 450
    const panelY = 150

    // 面板背景
    const panel = this.add.rectangle(panelX, panelY, 350, 180, COLORS.BG_MEDIUM, 0.8)
    panel.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 标题
    const title = this.createText(panelX, panelY - 70, '【基本信息】', {
      fontSize: '20px',
      color: '#FFD700'
    })
    title.setOrigin(0.5)

    // 信息内容
    const infoLines = [
      `名称: ${this.playerData.name}`,
      `境界: ${this.playerData.realm}`,
      `门派: ${this.playerData.sect}`,
      `位置: ${this.playerData.location}`
    ]

    infoLines.forEach((line, index) => {
      const text = this.createText(panelX - 150, panelY - 40 + index * 30, line, {
        fontSize: '18px'
      })
      this.statsTexts.set(`info-${index}`, text)
    })
  }

  /**
   * 创建属性面板
   */
  private createStatsPanel(): void {
    const panelX = this.centerX
    const panelY = 380

    // 面板背景
    const panel = this.add.rectangle(panelX, panelY, 600, 150, COLORS.BG_MEDIUM, 0.8)
    panel.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 标题
    const title = this.createText(panelX, panelY - 60, '【属性】', {
      fontSize: '20px',
      color: '#FFD700'
    })
    title.setOrigin(0.5)

    // 修为进度条
    this.createStatBar(
      panelX - 250,
      panelY - 20,
      '修为',
      this.playerData.cultivation,
      this.playerData.maxCultivation,
      COLORS.INFO
    )

    // 生命进度条
    this.createStatBar(
      panelX - 250,
      panelY + 10,
      '生命',
      this.playerData.hp,
      this.playerData.maxHp,
      COLORS.DANGER
    )

    // 真元进度条
    this.createStatBar(
      panelX - 250,
      panelY + 40,
      '真元',
      this.playerData.mp,
      this.playerData.maxMp,
      COLORS.PRIMARY_BLUE
    )

    // 灵石
    const spiritText = this.createText(
      panelX - 250,
      panelY + 70,
      `灵石: ${this.playerData.spiritStones.toLocaleString()}`,
      { fontSize: '18px', color: '#FFD700' }
    )
    this.statsTexts.set('spiritStones', spiritText)
  }

  /**
   * 创建属性进度条
   */
  private createStatBar(
    x: number,
    y: number,
    label: string,
    current: number,
    max: number,
    color: number
  ): void {
    // 标签
    const labelText = this.createText(x, y, `${label}:`, { fontSize: '16px' })

    // 进度条背景
    const barBg = this.add.rectangle(x + 200, y, 300, 20, 0x333333)
    barBg.setOrigin(0.5, 0.5)

    // 进度条
    const progress = current / max
    const bar = this.add.rectangle(x + 50, y, 300 * progress, 16, color)
    bar.setOrigin(0, 0.5)

    // 数值文字
    const valueText = this.createText(
      x + 360,
      y,
      `${current.toLocaleString()}/${max.toLocaleString()}`,
      { fontSize: '14px' }
    )
    valueText.setOrigin(0, 0.5)
  }

  /**
   * 创建装备面板
   */
  private createEquipmentPanel(): void {
    const panelX = this.centerX
    const panelY = 520

    // 面板背景
    const panel = this.add.rectangle(panelX, panelY, 600, 100, COLORS.BG_MEDIUM, 0.8)
    panel.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 标题
    const title = this.createText(panelX, panelY - 35, '【装备法宝】', {
      fontSize: '20px',
      color: '#FFD700'
    })
    title.setOrigin(0.5)

    // 装备列表
    const equipment = [
      { name: '紫郢剑', stat: '威力: 250' },
      { name: '灵石护符', stat: '防御: +50' }
    ]

    equipment.forEach((item, index) => {
      const itemText = this.createText(
        panelX - 250 + index * 300,
        panelY + 10,
        `${item.name} (${item.stat})`,
        { fontSize: '16px', color: '#4FC3F7' }
      )
    })
  }

  /**
   * 创建底部标签按钮
   */
  private createTabButtons(): void {
    const buttonY = 620
    const spacing = 150
    const startX = this.centerX - spacing * 1.5

    const tabs = [
      { text: '功法', callback: () => this.showMessage('功法功能开发中...') },
      { text: '法宝', callback: () => this.showMessage('法宝功能开发中...') },
      { text: '灵兽', callback: () => this.showMessage('灵兽功能开发中...') },
      { text: '成就', callback: () => this.showMessage('成就功能开发中...') }
    ]

    tabs.forEach((tab, index) => {
      const button = this.createButton(
        startX + index * spacing,
        buttonY,
        tab.text,
        () => {
          this.sound.play('sfx-click', { volume: 0.7 })
          tab.callback()
        }
      )
      button.setScale(0.7)
    })
  }

  /**
   * 播放背景音乐
   */
  private playBackgroundMusic(): void {
    if (this.sound.get('bgm-character')) {
      this.sound.play('bgm-character', { loop: true, volume: 0.5 })
    }
  }

  /**
   * 更新玩家数据
   */
  public updatePlayerData(data: Partial<PlayerData>): void {
    this.playerData = { ...this.playerData, ...data }

    // 更新显示
    // 这里可以添加动画效果
  }
}
