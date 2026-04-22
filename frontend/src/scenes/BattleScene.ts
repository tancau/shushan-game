import Phaser from 'phaser'

export class BattleScene extends Phaser.Scene {
  private player!: Phaser.GameObjects.Sprite
  private enemy!: Phaser.GameObjects.Sprite
  private playerHP!: Phaser.GameObjects.Text
  private enemyHP!: Phaser.GameObjects.Text
  private combatLog!: Phaser.GameObjects.Text
  private attackButton!: Phaser.GameObjects.Text
  private skillButton!: Phaser.GameObjects.Text
  private fleeButton!: Phaser.GameObjects.Text

  constructor() {
    super('BattleScene')
  }

  preload() {
    // 预加载资源
    this.load.image('battle_background', 'assets/images/battle_background.jpg')
    this.load.image('player', 'assets/images/player.png')
    this.load.image('enemy', 'assets/images/enemy.png')
  }

  create() {
    // 创建战斗背景
    this.add.image(400, 300, 'battle_background').setScale(0.5)

    // 创建玩家和敌人
    this.player = this.add.sprite(200, 300, 'player').setScale(0.5)
    this.enemy = this.add.sprite(600, 300, 'enemy').setScale(0.5)

    // 创建HP显示
    this.playerHP = this.add.text(100, 100, '玩家 HP: 100', {
      fontSize: '24px',
      fill: '#ffffff'
    })

    this.enemyHP = this.add.text(500, 100, '敌人 HP: 50', {
      fontSize: '24px',
      fill: '#ffffff'
    })

    // 创建战斗日志
    this.combatLog = this.add.text(100, 400, '战斗开始！', {
      fontSize: '18px',
      fill: '#ffffff',
      wordWrap: { width: 600 }
    })

    // 创建战斗按钮
    this.attackButton = this.add.text(100, 500, '攻击', {
      fontSize: '24px',
      fill: '#ffffff',
      backgroundColor: '#333333',
      padding: { x: 20, y: 10 }
    })

    this.skillButton = this.add.text(300, 500, '技能', {
      fontSize: '24px',
      fill: '#ffffff',
      backgroundColor: '#333333',
      padding: { x: 20, y: 10 }
    })

    this.fleeButton = this.add.text(500, 500, '逃跑', {
      fontSize: '24px',
      fill: '#ffffff',
      backgroundColor: '#333333',
      padding: { x: 20, y: 10 }
    })

    // 设置按钮交互
    this.attackButton.setInteractive()
    this.attackButton.on('pointerdown', () => {
      this.attack()
    })

    this.skillButton.setInteractive()
    this.skillButton.on('pointerdown', () => {
      this.useSkill()
    })

    this.fleeButton.setInteractive()
    this.fleeButton.on('pointerdown', () => {
      this.flee()
    })
  }

  attack() {
    // 模拟攻击
    const damage = Phaser.Math.Between(10, 20)
    this.enemyHP.setText(`敌人 HP: ${Math.max(0, 50 - damage)}`)
    this.combatLog.setText(`你使用了普通攻击，造成${damage}点伤害！`)

    // 敌人反击
    setTimeout(() => {
      const enemyDamage = Phaser.Math.Between(5, 15)
      this.playerHP.setText(`玩家 HP: ${Math.max(0, 100 - enemyDamage)}`)
      this.combatLog.setText(`敌人反击，造成${enemyDamage}点伤害！`)
    }, 1000)
  }

  useSkill() {
    // 模拟技能
    const damage = Phaser.Math.Between(20, 30)
    this.enemyHP.setText(`敌人 HP: ${Math.max(0, 50 - damage)}`)
    this.combatLog.setText(`你使用了火球术，造成${damage}点伤害！`)

    // 敌人反击
    setTimeout(() => {
      const enemyDamage = Phaser.Math.Between(5, 15)
      this.playerHP.setText(`玩家 HP: ${Math.max(0, 100 - enemyDamage)}`)
      this.combatLog.setText(`敌人反击，造成${enemyDamage}点伤害！`)
    }, 1000)
  }

  flee() {
    // 逃跑
    this.combatLog.setText('你成功逃跑了！')
    setTimeout(() => {
      this.scene.start('MapScene')
    }, 1000)
  }
}
