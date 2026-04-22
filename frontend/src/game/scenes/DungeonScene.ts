/**
 * 副本场景
 * 多层副本挑战、Boss战
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS, DURATION, EASING } from '../config/gameConfig'

export class DungeonScene extends BaseScene {
  private currentFloor = 1
  private maxFloor = 10

  constructor() {
    super(SCENE_KEYS.DUNGEON)
  }

  protected onCreate(): void {
    this.createBackgroundWithTexture()
    this.createBackButton()
    this.createTitle()
    this.createFloorInfo()
    this.createDungeonMap()
    this.createActionButtons()
    this.playBackgroundMusic()
  }

  private setupBackground(): void {
    if (this.textures.exists('bg-dungeon')) {
      this.createBackgroundWithTexture('bg-dungeon')
    } else {
      const graphics = this.add.graphics()
      graphics.fillGradientStyle(COLORS.BG_DARK, COLORS.BG_DARK, 0x0D1B2A, 0x0D1B2A, 1)
      graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)
      graphics.setDepth(-1)
    }
  }

  private createBackButton(): void {
    const backButton = this.createButton(100, 40, '返回', () => {
      this.sound.play('sfx-click', { volume: 0.7 })
      this.transitionTo({ targetScene: SCENE_KEYS.WORLD_MAP })
    })
    backButton.setScale(0.8)
  }

  private createTitle(): void {
    const title = this.createText(this.centerX, 40, '秘境副本', { fontSize: '32px', color: '#FFD700', strokeThickness: 6 })
    title.setOrigin(0.5)
  }

  private createFloorInfo(): void {
    const infoBg = this.add.rectangle(this.centerX, 100, 400, 60, COLORS.BG_MEDIUM, 0.8)
    infoBg.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    const floorText = this.createText(this.centerX, 100, `第 ${this.currentFloor} 层 / 共 ${this.maxFloor} 层`, { fontSize: '24px', color: '#FFD700' })
    floorText.setOrigin(0.5)
  }

  private createDungeonMap(): void {
    const startY = 200
    const floorHeight = 45

    for (let i = 1; i <= this.maxFloor; i++) {
      const y = startY + (i - 1) * floorHeight
      const isCurrent = i === this.currentFloor
      const isCleared = i < this.currentFloor

      const floorBg = this.add.rectangle(this.centerX, y, 500, 35, 
        isCurrent ? COLORS.PRIMARY_GOLD : (isCleared ? COLORS.SUCCESS : COLORS.BG_MEDIUM),
        isCurrent ? 0.3 : 0.8
      )
      floorBg.setStrokeStyle(2, isCurrent ? COLORS.PRIMARY_GOLD : 0x666666)

      const floorLabel = this.createText(this.centerX - 200, y, `第 ${i} 层`, { 
        fontSize: '16px',
        color: isCurrent ? '#FFD700' : (isCleared ? '#38EF7D' : '#FFFFFF')
      })
      floorLabel.setOrigin(0, 0.5)

      // Boss 标记
      if (i % 3 === 0) {
        const bossText = this.createText(this.centerX + 150, y, '【BOSS】', { 
          fontSize: '14px',
          color: isCleared ? '#666666' : '#F45C43'
        })
        bossText.setOrigin(0.5)
      }

      // 状态标记
      if (isCleared) {
        const clearText = this.createText(this.centerX + 180, y, '✓', { fontSize: '20px', color: '#38EF7D' })
        clearText.setOrigin(0.5)
      }
    }
  }

  private createActionButtons(): void {
    const buttonY = 660

    this.createButton(this.centerX - 150, buttonY, '挑战本层', () => this.challengeFloor())
    this.createButton(this.centerX + 150, buttonY, '查看奖励', () => this.showRewards())
  }

  private challengeFloor(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    
    if (this.currentFloor > this.maxFloor) {
      this.showMessage('已通关所有层！', 2000, { color: '#FFD700' })
      return
    }

    this.showMessage(`开始挑战第 ${this.currentFloor} 层...`, 1500)
    
    this.time.delayedCall(1500, () => {
      this.transitionTo({ targetScene: SCENE_KEYS.BATTLE, data: { floor: this.currentFloor } })
    })
  }

  private showRewards(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    this.showMessage('奖励: 灵石、材料、法宝碎片', 2000)
  }

  private playBackgroundMusic(): void {
    if (this.sound.get('bgm-dungeon')) {
      this.sound.play('bgm-dungeon', { loop: true, volume: 0.5 })
    }
  }
}
