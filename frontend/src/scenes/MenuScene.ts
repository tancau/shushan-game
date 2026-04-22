import Phaser from 'phaser'

export class MenuScene extends Phaser.Scene {
  constructor() {
    super('MenuScene')
  }

  preload() {
    // 预加载资源
    this.load.image('background', 'assets/images/background.jpg')
  }

  create() {
    // 创建背景
    this.add.image(400, 300, 'background').setScale(0.5)

    // 创建标题
    this.add.text(400, 150, '蜀山剑侠传', {
      fontSize: '48px',
      fill: '#ffffff'
    }).setOrigin(0.5)

    // 创建开始游戏按钮
    const startButton = this.add.text(400, 300, '开始游戏', {
      fontSize: '32px',
      fill: '#ffffff',
      backgroundColor: '#333333',
      padding: { x: 20, y: 10 }
    }).setOrigin(0.5)

    startButton.setInteractive()
    startButton.on('pointerdown', () => {
      this.scene.start('MapScene')
    })

    // 创建退出按钮
    const exitButton = this.add.text(400, 400, '退出游戏', {
      fontSize: '32px',
      fill: '#ffffff',
      backgroundColor: '#333333',
      padding: { x: 20, y: 10 }
    }).setOrigin(0.5)

    exitButton.setInteractive()
    exitButton.on('pointerdown', () => {
      window.close()
    })
  }
}
