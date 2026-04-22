/**
 * 战斗场景
 * 回合制战斗系统 - 使用生成的美术资源
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
  private turnText!: Phaser.GameObjects.Text

  constructor() {
    super(SCENE_KEYS.BATTLE)
  }

  protected onCreate(): void {
    this.createBattleField()
    this.createCharacters()
    this.createBattleUI()
    this.createActionButtons()
    this.playBackgroundMusic()
    this.startBattle()
  }

  private createBattleField(): void {
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
    
    // 战斗地面
    const ground = this.add.rectangle(this.centerX, 500, this.cameras.main.width, 100, 0x16213E, 0.6)
    ground.setStrokeStyle(2, COLORS.PRIMARY_GOLD)
  }

  private createCharacters(): void {
    // 玩家 - 使用生成的动画帧
    const playerX = 200
    const playerY = 400
    
    let playerSprite: Phaser.GameObjects.Sprite
    
    if (this.textures.exists('player-idle')) {
      playerSprite = this.add.sprite(playerX, playerY, 'player-idle')
      playerSprite.setScale(0.8)
    } else {
      // 备用占位符
      const graphics = this.add.graphics()
      graphics.fillStyle(COLORS.PRIMARY_GOLD, 0.8)
      graphics.fillCircle(playerX, playerY, 50)
      playerSprite = this.add.sprite(playerX, playerY, '__DEFAULT')
    }

    this.player = { 
      sprite: playerSprite, 
      name: 'tancau', 
      hp: 100, 
      maxHp: 100, 
      attack: 50, 
      x: playerX, 
      y: playerY 
    }

    // 敌人 - 使用生成的妖狼动画帧
    const enemyX = 1080
    const enemyY = 400
    
    let enemySprite: Phaser.GameObjects.Sprite
    
    if (this.textures.exists('wolf-idle')) {
      enemySprite = this.add.sprite(enemyX, enemyY, 'wolf-idle')
      enemySprite.setScale(0.8)
    } else {
      // 备用占位符
      const graphics = this.add.graphics()
      graphics.fillStyle(COLORS.DANGER, 0.8)
      graphics.fillCircle(enemyX, enemyY, 50)
      enemySprite = this.add.sprite(enemyX, enemyY, '__DEFAULT')
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

    // 背景
    const bg = this.add.rectangle(character.x, barY, barWidth, 10, 0x333333)
    bg.setStrokeStyle(1, 0xFFFFFF)

    // 填充（绿色HP条）
    const bar = this.add.rectangle(character.x - barWidth / 2 + 1, barY, barWidth - 2, 8, COLORS.DANGER)
    bar.setOrigin(0, 0.5)

    // 名字
    const nameText = this.createText(character.x, barY - 20, character.name, { fontSize: '14px' })
    nameText.setOrigin(0.5)

    character.healthBar = bar
  }

  private createBattleUI(): void {
    this.turnText = this.createText(this.centerX, 30, `战斗 - 第 ${this.turnNumber} 回合`, { 
      fontSize: '24px', 
      color: '#FFD700' 
    })
    this.turnText.setOrigin(0.5)

    // 战斗日志背景
    const logBg = this.add.rectangle(this.centerX, 550, 600, 80, 0x16213E, 0.9)
    logBg.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    const logTitle = this.createText(this.centerX, 520, '【战斗日志】', { 
      fontSize: '16px', 
      color: '#FFD700' 
    })
    logTitle.setOrigin(0.5)

    this.logText = this.createText(this.centerX, 560, '', { fontSize: '14px' })
    this.logText.setOrigin(0.5)
  }

  private createActionButtons(): void {
    const buttonY = 650
    const spacing = 150
    const startX = this.centerX - spacing * 1.5

    // 使用生成的按钮图片
    const buttons = [
      { key: 'button-attack', label: '攻击', action: () => this.performAttack() },
      { key: 'button-skill', label: '技能', action: () => this.showSkills() },
      { key: 'button-item', label: '物品', action: () => this.showItems() },
      { key: 'button-defend', label: '防御', action: () => this.defend() }
    ]

    buttons.forEach((btn, i) => {
      if (this.textures.exists(btn.key)) {
        const button = this.add.image(startX + spacing * i, buttonY, btn.key)
        button.setInteractive({ useHandCursor: true })
        button.on('pointerdown', btn.action)
        button.on('pointerover', () => button.setScale(1.1))
        button.on('pointerout', () => button.setScale(1))
      } else {
        // 备用文字按钮
        this.createButton(startX + spacing * i, buttonY, btn.label, btn.action)
      }
    })
  }

  private startBattle(): void {
    this.addLog('战斗开始！')
    this.showMessage('战斗开始！', 1500)
  }

  private async performAttack(): Promise<void> {
    if (!this.isPlayerTurn) return
    this.isPlayerTurn = false
    
    // 播放音效
    if (this.sound.get('sfx-sword')) {
      this.sound.play('sfx-sword', { volume: 0.7 })
    }

    const damage = Math.floor(this.player.attack * (0.8 + Math.random() * 0.4))
    
    // 攻击动画
    await this.playAttackAnimation(this.player, this.enemy)
    
    // 显示伤害
    this.showDamageNumber(this.enemy.x, this.enemy.y - 50, damage, false)
    
    // 造成伤害
    await this.takeDamage(this.enemy, damage)
    
    this.addLog(`攻击造成 ${damage} 伤害`)

    if (this.enemy.hp <= 0) {
      await this.onBattleWon()
      return
    }

    await this.delay(1000)
    await this.enemyTurn()
  }

  private async playAttackAnimation(attacker: BattleCharacter, target: BattleCharacter): Promise<void> {
    return new Promise(resolve => {
      this.tweens.add({
        targets: attacker.sprite,
        x: attacker.x + (target.x > attacker.x ? 100 : -100),
        duration: 200,
        yoyo: true,
        hold: 100,
        onComplete: () => resolve()
      })
    })
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
    
    const healthBar = character.healthBar
    if (healthBar) {
      const progress = character.hp / character.maxHp
      this.tweens.add({ 
        targets: healthBar, 
        width: 98 * progress, 
        duration: 300 
      })
    }
    
    // 受击动画
    this.tweens.add({ 
      targets: character.sprite, 
      alpha: 0.5, 
      duration: 100, 
      yoyo: true 
    })
  }

  private async enemyTurn(): Promise<void> {
    const damage = Math.floor(this.enemy.attack * (0.8 + Math.random() * 0.4))
    
    await this.playAttackAnimation(this.enemy, this.player)
    
    // 播放受击音效
    if (this.sound.get('sfx-hit')) {
      this.sound.play('sfx-hit', { volume: 0.7 })
    }
    
    // 屏幕震动
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
    this.turnText.setText(`战斗 - 第 ${this.turnNumber} 回合`)
  }

  private async onBattleWon(): Promise<void> {
    // 播放胜利音效
    if (this.sound.get('sfx-victory')) {
      this.sound.play('sfx-victory', { volume: 0.7 })
    }
    
    this.showMessage('战斗胜利！获得 100 经验，50 灵石', 3000, { color: '#FFD700' })
    
    await this.delay(3000)
    this.transitionTo({ targetScene: SCENE_KEYS.WORLD_MAP })
  }

  private async onBattleLost(): Promise<void> {
    this.showMessage('战斗失败...', 3000, { color: '#F45C43' })
    await this.delay(3000)
    this.transitionTo({ targetScene: SCENE_KEYS.MAIN_MENU })
  }

  private showSkills(): void {
    this.addLog('技能功能开发中...')
    this.showMessage('技能功能开发中...', 2000)
  }

  private showItems(): void {
    this.addLog('物品功能开发中...')
    this.showMessage('物品功能开发中...', 2000)
  }

  private defend(): void {
    if (!this.isPlayerTurn) return
    this.addLog('进入防御姿态，减少50%伤害')
    this.isPlayerTurn = false
    this.time.delayedCall(500, () => this.enemyTurn())
  }

  private addLog(message: string): void {
    this.logText.setText(message)
  }

  private playBackgroundMusic(): void {
    if (this.sound.get('bgm-battle')) {
      this.sound.play('bgm-battle', { loop: true, volume: 0.5 })
    }
  }
}
