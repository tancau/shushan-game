/**
 * 战斗场景
 * 回合制战斗系统 - 使用动画角色
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS } from '../config/gameConfig'

interface BattleCharacter {
  sprite: Phaser.GameObjects.Sprite
  name: string
  hp: number
  maxHp: number
  attack: number
  x: number
  y: number
  healthBar?: Phaser.GameObjects.Rectangle
}

export class BattleScene extends BaseScene {
  private player!: BattleCharacter
  private enemy!: BattleCharacter
  private turnNumber = 1
  private isPlayerTurn = true
  private logText!: Phaser.GameObjects.Text

  constructor() {
    super(SCENE_KEYS.BATTLE)
  }

  protected onCreate(): void {
    this.createBattleField()
    this.createCharacters()
    this.createBattleUI()
    this.createActionButtons()
    this.startBattle()
  }

  private createBattleField(): void {
    // 使用生成的地图背景
    if (this.textures.exists('bg-map')) {
      const bg = this.add.image(this.centerX, this.centerY, 'bg-map')
      bg.setScale(0.8)
    } else {
      const graphics = this.add.graphics()
      graphics.fillGradientStyle(0x1a1a2e, 0x1a1a2e, 0x16213e, 0x16213e, 1)
      graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)
    }
    
    // 战斗地面
    const ground = this.add.rectangle(this.centerX, 500, this.cameras.main.width, 100, 0x16213E, 0.6)
    ground.setStrokeStyle(2, COLORS.PRIMARY_GOLD)
  }

  private createCharacters(): void {
    // 玩家
    const playerX = 200
    const playerY = 400
    
    const playerSprite = this.add.sprite(playerX, playerY, 'player-idle-0')
    playerSprite.setScale(0.8)
    
    // 播放待机动画
    if (this.anims.exists('player-idle')) {
      playerSprite.play('player-idle')
    }

    this.player = { 
      sprite: playerSprite, 
      name: '主角', 
      hp: 100, 
      maxHp: 100, 
      attack: 50, 
      x: playerX, 
      y: playerY 
    }

    // 敌人
    const enemyX = 1080
    const enemyY = 400
    
    const enemySprite = this.add.sprite(enemyX, enemyY, 'wolf-idle-0')
    enemySprite.setScale(0.8)
    
    // 播放待机动画
    if (this.anims.exists('wolf-idle')) {
      enemySprite.play('wolf-idle')
    }

    this.enemy = { 
      sprite: enemySprite, 
      name: '妖狼', 
      hp: 500, 
      maxHp: 500, 
      attack: 30, 
      x: enemyX, 
      y: enemyY 
    }

    this.createHealthBar(this.player)
    this.createHealthBar(this.enemy)
  }

  private createHealthBar(character: BattleCharacter): void {
    const barWidth = 100
    const barY = character.y - 70

    const bg = this.add.rectangle(character.x, barY, barWidth, 10, 0x333333)
    bg.setStrokeStyle(1, 0xFFFFFF)

    const bar = this.add.rectangle(character.x - barWidth / 2 + 1, barY, barWidth - 2, 8, COLORS.DANGER)
    bar.setOrigin(0, 0.5)

    const nameText = this.createText(character.x, barY - 20, character.name, { fontSize: '14px' })
    nameText.setOrigin(0.5)

    character.healthBar = bar
  }

  private createBattleUI(): void {
    const turnText = this.createText(this.centerX, 30, `战斗 - 第 ${this.turnNumber} 回合`, { 
      fontSize: '24px', 
      color: '#FFD700' 
    })
    turnText.setOrigin(0.5)

    const logBg = this.add.rectangle(this.centerX, 550, 600, 80, 0x16213E, 0.9)
    logBg.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    this.logText = this.createText(this.centerX, 560, '战斗开始！', { fontSize: '14px' })
    this.logText.setOrigin(0.5)
  }

  private createActionButtons(): void {
    const buttonY = 650
    const spacing = 150
    const startX = this.centerX - spacing * 1.5

    const buttons = [
      { key: 'button-attack', action: () => this.performAttack() },
      { key: 'button-skill', action: () => this.showSkills() },
      { key: 'button-item', action: () => this.showItems() },
      { key: 'button-defend', action: () => this.defend() }
    ]

    buttons.forEach((btn, i) => {
      if (this.textures.exists(btn.key)) {
        const button = this.add.image(startX + spacing * i, buttonY, btn.key)
        button.setInteractive({ useHandCursor: true })
        button.on('pointerdown', btn.action)
        button.on('pointerover', () => button.setScale(1.1))
        button.on('pointerout', () => button.setScale(1))
      } else {
        this.createButton(startX + spacing * i, buttonY, '按钮', btn.action)
      }
    })
  }

  private startBattle(): void {
    this.addLog('战斗开始！')
  }

  private async performAttack(): Promise<void> {
    if (!this.isPlayerTurn) return
    this.isPlayerTurn = false

    // 播放攻击动画
    if (this.anims.exists('player-attack')) {
      this.player.sprite.play('player-attack')
      this.time.delayedCall(400, () => {
        if (this.anims.exists('player-idle')) {
          this.player.sprite.play('player-idle')
        }
      })
    }

    const damage = Math.floor(this.player.attack * (0.8 + Math.random() * 0.4))
    
    await this.delay(300)
    
    // 敌人受击
    if (this.anims.exists('wolf-hurt')) {
      this.enemy.sprite.play('wolf-hurt')
      this.time.delayedCall(250, () => {
        if (this.anims.exists('wolf-idle')) {
          this.enemy.sprite.play('wolf-idle')
        }
      })
    }
    
    this.showDamageNumber(this.enemy.x, this.enemy.y - 50, damage, false)
    await this.takeDamage(this.enemy, damage)
    
    this.addLog(`攻击造成 ${damage} 伤害`)

    if (this.enemy.hp <= 0) {
      await this.onBattleWon()
      return
    }

    await this.delay(1000)
    await this.enemyTurn()
  }

  private async enemyTurn(): Promise<void> {
    const damage = Math.floor(this.enemy.attack * (0.8 + Math.random() * 0.4))
    
    // 敌人攻击动画
    if (this.anims.exists('wolf-attack')) {
      this.enemy.sprite.play('wolf-attack')
      this.time.delayedCall(400, () => {
        if (this.anims.exists('wolf-idle')) {
          this.enemy.sprite.play('wolf-idle')
        }
      })
    }
    
    await this.delay(300)
    
    // 玩家受击
    if (this.anims.exists('player-hurt')) {
      this.player.sprite.play('player-hurt')
      this.time.delayedCall(250, () => {
        if (this.anims.exists('player-idle')) {
          this.player.sprite.play('player-idle')
        }
      })
    }
    
    this.cameras.main.shake(200, 0.02)
    this.showDamageNumber(this.player.x, this.player.y - 50, damage, true)
    await this.takeDamage(this.player, damage)
    
    this.addLog(`敌人攻击造成 ${damage} 伤害`)

    if (this.player.hp <= 0) {
      await this.onBattleLost()
      return
    }

    this.turnNumber++
    this.isPlayerTurn = true
  }

  private showDamageNumber(x: number, y: number, damage: number, isPlayer: boolean): void {
    const color = isPlayer ? '#F45C43' : '#38EF7D'
    const text = this.createText(x, y, `${damage}`, { 
      fontSize: '32px', 
      color: color 
    })
    text.setOrigin(0.5)

    this.tweens.add({
      targets: text,
      y: y - 50,
      alpha: 0,
      duration: 1000,
      onComplete: () => text.destroy()
    })
  }

  private async takeDamage(character: BattleCharacter, damage: number): Promise<void> {
    character.hp = Math.max(0, character.hp - damage)
    
    if (character.healthBar) {
      const progress = character.hp / character.maxHp
      this.tweens.add({ 
        targets: character.healthBar, 
        width: 98 * progress, 
        duration: 300 
      })
    }
  }

  private async onBattleWon(): Promise<void> {
    this.addLog('战斗胜利！')
    await this.delay(2000)
    this.transitionTo({ targetScene: SCENE_KEYS.WORLD_MAP })
  }

  private async onBattleLost(): Promise<void> {
    this.addLog('战斗失败...')
    await this.delay(2000)
    this.transitionTo({ targetScene: SCENE_KEYS.MAIN_MENU })
  }

  private showSkills(): void {
    this.addLog('技能功能开发中...')
    this.isPlayerTurn = false
    this.time.delayedCall(1000, () => {
      this.isPlayerTurn = true
    })
  }

  private showItems(): void {
    this.addLog('物品功能开发中...')
    this.isPlayerTurn = false
    this.time.delayedCall(1000, () => {
      this.isPlayerTurn = true
    })
  }

  private defend(): void {
    if (!this.isPlayerTurn) return
    this.addLog('防御姿态')
    this.isPlayerTurn = false
    this.time.delayedCall(500, () => this.enemyTurn())
  }

  private addLog(message: string): void {
    this.logText.setText(message)
  }
}
