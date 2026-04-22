/**
 * 战斗场景
 * 回合制战斗系统
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS, DURATION, EASING } from '../config/gameConfig'

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
    if (this.textures.exists('bg-battle')) {
      this.add.image(this.centerX, this.centerY, 'bg-battle')
    } else {
      const graphics = this.add.graphics()
      graphics.fillGradientStyle(COLORS.BG_DARK, COLORS.BG_DARK, COLORS.BG_MEDIUM, COLORS.BG_MEDIUM, 1)
      graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)
    }

    if (this.textures.exists('battle-ground')) {
      this.add.image(this.centerX, 500, 'battle-ground')
    } else {
      const ground = this.add.rectangle(this.centerX, 500, this.cameras.main.width, 100, COLORS.BG_LIGHT, 0.5)
      ground.setStrokeStyle(2, COLORS.PRIMARY_GOLD)
    }
  }

  private createCharacters(): void {
    // 玩家
    const playerX = 200
    const playerY = 400
    let playerSprite: Phaser.GameObjects.Sprite
    
    if (this.textures.exists('player-sprite')) {
      playerSprite = this.add.sprite(playerX, playerY, 'player-sprite')
    } else {
      const graphics = this.add.graphics()
      graphics.fillStyle(COLORS.PRIMARY_GOLD, 0.8)
      graphics.fillCircle(playerX, playerY, 50)
      playerSprite = this.add.sprite(playerX, playerY, '__DEFAULT')
    }

    this.player = { sprite: playerSprite, name: 'tancau', hp: 100, maxHp: 100, attack: 50, x: playerX, y: playerY }

    // 敌人
    const enemyX = 1080
    const enemyY = 400
    let enemySprite: Phaser.GameObjects.Sprite
    
    if (this.textures.exists('enemy-sprite')) {
      enemySprite = this.add.sprite(enemyX, enemyY, 'enemy-sprite')
    } else {
      const graphics = this.add.graphics()
      graphics.fillStyle(COLORS.DANGER, 0.8)
      graphics.fillCircle(enemyX, enemyY, 50)
      enemySprite = this.add.sprite(enemyX, enemyY, '__DEFAULT')
    }

    this.enemy = { sprite: enemySprite, name: '妖兽', hp: 500, maxHp: 500, attack: 30, x: enemyX, y: enemyY }

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
    this.turnText = this.createText(this.centerX, 30, `战斗 - 第 ${this.turnNumber} 回合`, { fontSize: '24px', color: '#FFD700' })
    this.turnText.setOrigin(0.5)

    const logBg = this.add.rectangle(this.centerX, 550, 600, 80, COLORS.BG_MEDIUM, 0.8)
    logBg.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    const logTitle = this.createText(this.centerX, 520, '【战斗日志】', { fontSize: '16px', color: '#FFD700' })
    logTitle.setOrigin(0.5)

    this.logText = this.createText(this.centerX, 560, '', { fontSize: '14px' })
    this.logText.setOrigin(0.5)

    const fleeButton = this.createButton(this.cameras.main.width - 100, 40, '逃跑', () => this.flee())
    fleeButton.setScale(0.7)
  }

  private createActionButtons(): void {
    const buttonY = 650
    const spacing = 150
    const startX = this.centerX - spacing

    this.createButton(startX, buttonY, '攻击', () => this.performAttack())
    this.createButton(startX + spacing, buttonY, '技能', () => this.showSkills())
    this.createButton(startX + spacing * 2, buttonY, '法宝', () => this.showArtifacts())
  }

  private startBattle(): void {
    this.addLog('战斗开始！')
    this.showMessage('战斗开始！', 1500)
  }

  private async performAttack(): Promise<void> {
    if (!this.isPlayerTurn) return
    this.isPlayerTurn = false
    this.sound.play('sfx-sword', { volume: 0.7 })

    const damage = Math.floor(this.player.attack * (0.8 + Math.random() * 0.4))
    await this.playAttackAnimation(this.player, this.enemy)
    this.createSwordSlash(this.player.x, this.player.y, this.enemy.x, this.enemy.y)
    this.showDamageNumber(this.enemy.x, this.enemy.y - 50, damage, false)
    await this.takeDamage(this.enemy, damage)
    this.addLog(`[回合${this.turnNumber}] 攻击造成 ${damage} 伤害`)

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

  private createSwordSlash(fromX: number, fromY: number, toX: number, toY: number): void {
    const graphics = this.add.graphics()
    graphics.lineStyle(4, COLORS.PRIMARY_GOLD, 1)
    graphics.beginPath()
    graphics.moveTo(fromX, fromY)
    graphics.lineTo(toX, toY)
    graphics.strokePath()

    this.tweens.add({
      targets: graphics,
      alpha: 0,
      duration: 300,
      onComplete: () => {
        graphics.destroy()
        this.createHitEffect(toX, toY)
      }
    })
  }

  private createHitEffect(x: number, y: number): void {
    if (this.textures.exists('particle-light')) {
      this.add.particles(x, y, 'particle-light', {
        speed: { min: 100, max: 200 },
        scale: { start: 0.5, end: 0 },
        lifespan: 500,
        quantity: 10,
        blendMode: 'ADD'
      }).explode()
    }
  }

  private async takeDamage(character: BattleCharacter, damage: number): Promise<void> {
    character.hp = Math.max(0, character.hp - damage)
    const healthBar = character.healthBar
    if (healthBar) {
      const progress = character.hp / character.maxHp
      this.tweens.add({ targets: healthBar, width: 98 * progress, duration: 300 })
    }
    this.tweens.add({ targets: character.sprite, alpha: 0.5, duration: 100, yoyo: true })
  }

  private async enemyTurn(): Promise<void> {
    const damage = Math.floor(this.enemy.attack * (0.8 + Math.random() * 0.4))
    await this.playAttackAnimation(this.enemy, this.player)
    this.shake(0.02, 200)
    this.showDamageNumber(this.player.x, this.player.y - 50, damage, true)
    this.sound.play('sfx-hit', { volume: 0.7 })
    await this.takeDamage(this.player, damage)
    this.addLog(`[回合${this.turnNumber}] 敌人攻击造成 ${damage} 伤害`)

    if (this.player.hp <= 0) {
      await this.onBattleLost()
      return
    }

    this.turnNumber++
    this.isPlayerTurn = true
    this.turnText.setText(`战斗 - 第 ${this.turnNumber} 回合`)
  }

  private async onBattleWon(): Promise<void> {
    this.showVictoryEffect()
    this.sound.play('sfx-victory', { volume: 0.7 })
    this.showMessage('战斗胜利！获得 100 经验，50 灵石', 3000, { color: '#FFD700' })
    await this.delay(3000)
    this.transitionTo({ targetScene: SCENE_KEYS.WORLD_MAP })
  }

  private showVictoryEffect(): void {
    if (this.textures.exists('particle-light')) {
      this.add.particles(this.centerX, this.centerY, 'particle-light', {
        speed: { min: 100, max: 200 },
        angle: { min: 0, max: 360 },
        scale: { start: 0.8, end: 0 },
        lifespan: 2000,
        quantity: 30,
        blendMode: 'ADD'
      }).explode()
    }
  }

  private async onBattleLost(): Promise<void> {
    this.sound.play('sfx-defeat', { volume: 0.7 })
    this.showMessage('战斗失败...', 3000, { color: '#F45C43' })
    await this.delay(3000)
    this.transitionTo({ targetScene: SCENE_KEYS.CHARACTER })
  }

  private flee(): void {
    this.sound.play('sfx-cancel', { volume: 0.7 })
    this.showMessage('逃跑成功！', 1500)
    this.time.delayedCall(1500, () => this.transitionTo({ targetScene: SCENE_KEYS.WORLD_MAP }))
  }

  private showSkills(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    this.showMessage('技能功能开发中...', 2000)
  }

  private showArtifacts(): void {
    this.sound.play('sfx-click', { volume: 0.7 })
    this.showMessage('法宝功能开发中...', 2000)
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
