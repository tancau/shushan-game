import Phaser from 'phaser'

export class MapScene extends Phaser.Scene {
  private player!: Phaser.GameObjects.Sprite
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys

  constructor() {
    super('MapScene')
  }

  preload() {
    // 预加载资源
    this.load.image('map', 'assets/images/map.jpg')
    this.load.image('player', 'assets/images/player.png')
  }

  create() {
    // 创建地图
    this.add.image(400, 300, 'map').setScale(0.5)

    // 创建玩家
    this.player = this.add.sprite(400, 300, 'player').setScale(0.5)

    // 启用物理引擎
    this.physics.add.existing(this.player)

    // 配置键盘输入
    this.cursors = this.input.keyboard.createCursorKeys()

    // 创建返回按钮
    const backButton = this.add.text(100, 50, '返回菜单', {
      fontSize: '24px',
      fill: '#ffffff',
      backgroundColor: '#333333',
      padding: { x: 10, y: 5 }
    })

    backButton.setInteractive()
    backButton.on('pointerdown', () => {
      this.scene.start('MenuScene')
    })

    // 模拟随机遇敌
    this.time.addEvent({
      delay: 5000,
      callback: () => {
        this.scene.start('BattleScene')
      },
      loop: false
    })
  }

  update() {
    // 处理玩家移动
    const speed = 100

    if (this.cursors.left.isDown) {
      this.player.x -= speed * this.game.loop.delta / 1000
    } else if (this.cursors.right.isDown) {
      this.player.x += speed * this.game.loop.delta / 1000
    }

    if (this.cursors.up.isDown) {
      this.player.y -= speed * this.game.loop.delta / 1000
    } else if (this.cursors.down.isDown) {
      this.player.y += speed * this.game.loop.delta / 1000
    }
  }
}
