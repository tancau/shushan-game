/**
 * 世界地图场景
 * 地点探索、移动、事件触发 - 使用生成的美术资源
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS } from '../config/gameConfig'

interface Location {
  name: string
  x: number
  y: number
  danger: number
  unlocked: boolean
}

export class WorldMapScene extends BaseScene {
  private locations: Location[] = []
  private currentLocation: string = '蜀山脚下'
  private playerMarker!: Phaser.GameObjects.Container
  private bg!: Phaser.GameObjects.Image

  constructor() {
    super(SCENE_KEYS.WORLD_MAP)
  }

  protected onCreate(): void {
    this.createBackground()
    this.createBackButton()
    this.createTitle()
    this.createLocations()
    this.createPlayerMarker()
    this.createLocationInfo()
    this.playBackgroundMusic()
  }

  private createBackground(): void {
    // 使用生成的地图背景
    if (this.textures.exists('bg-map')) {
      this.bg = this.add.image(this.centerX, this.centerY, 'bg-map')
      this.bg.setScale(0.8) // 适配屏幕
    } else {
      // 备用渐变背景
      const graphics = this.add.graphics()
      graphics.fillGradientStyle(0x1a1a2e, 0x1a1a2e, 0x16213e, 0x16213e, 1)
      graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)
    }
  }

  private createBackButton(): void {
    this.createButton(100, 40, '返回', () => {
      if (this.sound.get('sfx-click')) {
        this.sound.play('sfx-click', { volume: 0.7 })
      }
      this.transitionTo({ targetScene: SCENE_KEYS.MAIN_MENU })
    })
  }

  private createTitle(): void {
    const title = this.createText(this.centerX, 40, '世界地图', { 
      fontSize: '32px', 
      color: '#FFD700', 
      strokeThickness: 6 
    })
    title.setOrigin(0.5)
  }

  private createLocations(): void {
    this.locations = [
      { name: '蜀山脚下', x: 300, y: 250, danger: 1, unlocked: true },
      { name: '妖狼洞穴', x: 600, y: 200, danger: 4, unlocked: true },
      { name: '剑灵峰', x: 900, y: 150, danger: 3, unlocked: true },
      { name: '蜀山镇', x: 350, y: 400, danger: 0, unlocked: true },
      { name: '灵兽谷', x: 700, y: 380, danger: 2, unlocked: true },
      { name: '天劫之地', x: 500, y: 300, danger: 5, unlocked: false }
    ]

    this.locations.forEach(loc => {
      this.createLocationMarker(loc)
    })
  }

  private createLocationMarker(loc: Location): void {
    const container = this.add.container(loc.x, loc.y)

    // 地点圆圈
    const bg = this.add.circle(0, 0, 40, loc.unlocked ? 0x16213E : 0x333333, 0.8)
    bg.setStrokeStyle(2, loc.unlocked ? COLORS.PRIMARY_GOLD : 0x666666)

    // 地点名称
    const nameText = this.createText(0, -60, loc.name, { 
      fontSize: '16px', 
      color: loc.unlocked ? '#FFFFFF' : '#666666' 
    })
    nameText.setOrigin(0.5)

    // 危险等级星号
    const dangerStars = '★'.repeat(loc.danger) + '☆'.repeat(5 - loc.danger)
    const dangerText = this.createText(0, 60, `[${dangerStars}]`, { 
      fontSize: '12px', 
      color: '#FFA726' 
    })
    dangerText.setOrigin(0.5)

    container.add([bg, nameText, dangerText])

    if (loc.unlocked) {
      container.setSize(80, 120)
      container.setInteractive({ useHandCursor: true })

      container.on('pointerover', () => {
        this.tweens.add({ targets: container, scale: 1.1, duration: 200 })
      })

      container.on('pointerout', () => {
        this.tweens.add({ targets: container, scale: 1, duration: 200 })
      })

      container.on('pointerdown', () => this.moveToLocation(loc))
    }
  }

  private createPlayerMarker(): void {
    const currentLoc = this.locations.find(l => l.name === this.currentLocation) || this.locations[0]
    
    this.playerMarker = this.add.container(currentLoc.x, currentLoc.y - 30)
    
    // 标记图标
    const marker = this.add.text(0, 0, '📍', { fontSize: '32px' })
    marker.setOrigin(0.5)
    
    // "你在这里"文字
    const label = this.createText(0, -30, '你在这里', { 
      fontSize: '12px', 
      color: '#4FC3F7' 
    })
    label.setOrigin(0.5)
    
    this.playerMarker.add([marker, label])
    
    // 呼吸动画
    this.tweens.add({
      targets: this.playerMarker,
      y: this.playerMarker.y - 5,
      duration: 1000,
      yoyo: true,
      repeat: -1
    })
  }

  private createLocationInfo(): void {
    const panelY = 580
    
    const panel = this.add.rectangle(this.centerX, panelY, 600, 80, 0x16213E, 0.9)
    panel.setStrokeStyle(2, COLORS.PRIMARY_GOLD)
    
    const infoText = this.createText(this.centerX, panelY - 20, `当前位置: ${this.currentLocation}`, { 
      fontSize: '18px', 
      color: '#FFD700' 
    })
    infoText.setOrigin(0.5)
    
    const hint = this.createText(this.centerX, panelY + 15, '点击地点可移动', { 
      fontSize: '14px', 
      color: '#4FC3F7' 
    })
    hint.setOrigin(0.5)
  }

  private moveToLocation(loc: Location): void {
    if (loc.name === this.currentLocation) {
      this.showMessage('你已在此地', 1500)
      return
    }

    if (this.sound.get('sfx-click')) {
      this.sound.play('sfx-click', { volume: 0.7 })
    }
    
    // 移动动画
    this.tweens.add({
      targets: this.playerMarker,
      x: loc.x,
      y: loc.y - 30,
      duration: 1000,
      onComplete: () => {
        this.currentLocation = loc.name
        this.showMessage(`到达 ${loc.name}`, 1500)
        
        // 随机触发事件
        if (Math.random() > 0.5) {
          this.time.delayedCall(1500, () => this.triggerExploreEvent(loc))
        }
      }
    })
  }

  private triggerExploreEvent(loc: Location): void {
    if (loc.danger === 0) return
    
    // 随机决定事件类型
    if (Math.random() > 0.5) {
      this.showMessage('遭遇敌人！', 1500)
      this.time.delayedCall(1500, () => {
        this.transitionTo({ targetScene: SCENE_KEYS.BATTLE })
      })
    } else {
      const rewards = ['灵石+50', '发现丹药', '获得材料']
      const reward = rewards[Math.floor(Math.random() * rewards.length)]
      this.showMessage(`探索发现: ${reward}`, 2000, { color: '#38EF7D' })
    }
  }

  private playBackgroundMusic(): void {
    if (this.sound.get('bgm-explore')) {
      this.sound.play('bgm-explore', { loop: true, volume: 0.5 })
    }
  }
}
