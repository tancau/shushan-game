/**
 * 预加载场景
 * 加载所有游戏资源
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS } from '../config/gameConfig'

export class PreloadScene extends BaseScene {
  private progressBar!: Phaser.GameObjects.Rectangle
  private loadingText!: Phaser.GameObjects.Text

  constructor() {
    super(SCENE_KEYS.PRELOAD)
  }

  protected onCreate(): void {
    this.createLoadingUI()
    this.setupLoadEvents()
    this.loadAllAssets()
  }

  private createLoadingUI(): void {
    // 背景
    const graphics = this.add.graphics()
    graphics.fillGradientStyle(0x1a1a2e, 0x1a1a2e, 0x16213e, 0x16213e, 1)
    graphics.fillRect(0, 0, this.cameras.main.width, this.cameras.main.height)

    // 标题
    const titleText = this.createText(this.centerX, this.centerY - 120, '蜀山剑侠传', {
      fontSize: '48px',
      color: '#FFD700',
      strokeThickness: 6
    })
    titleText.setOrigin(0.5)

    // 进度条背景
    const progressBox = this.add.rectangle(this.centerX, this.centerY, 320, 50, 0x16213E)
    progressBox.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 进度条
    this.progressBar = this.add.rectangle(this.centerX - 150, this.centerY, 0, 30, COLORS.PRIMARY_GOLD)
    this.progressBar.setOrigin(0, 0.5)

    // 加载文字
    this.loadingText = this.createText(this.centerX, this.centerY - 50, '加载中...', {
      fontSize: '24px',
      color: '#FFD700'
    })
    this.loadingText.setOrigin(0.5)
  }

  private setupLoadEvents(): void {
    this.load.on('progress', (value: number) => {
      this.progressBar.width = 300 * value
    })

    this.load.once('complete', () => {
      this.loadingText.setText('加载完成!')
      this.time.delayedCall(500, () => {
        this.transitionTo({ targetScene: SCENE_KEYS.MAIN_MENU })
      })
    })
  }

  private loadAllAssets(): void {
    this.loadImages()
    this.loadAudio()
    this.load.start()
  }

  private loadImages(): void {
    // 地图背景
    this.load.image('bg-map', '/assets/images/maps/shushan_foot.png')
    
    // UI按钮
    this.load.image('button-attack', '/assets/images/ui/button_attack.png')
    this.load.image('button-skill', '/assets/images/ui/button_skill.png')
    this.load.image('button-item', '/assets/images/ui/button_item.png')
    this.load.image('button-defend', '/assets/images/ui/button_defend.png')
    this.load.image('hp-bar', '/assets/images/ui/hp_bar.png')
    this.load.image('mp-bar', '/assets/images/ui/mp_bar.png')
    this.load.image('menu-bg', '/assets/images/ui/menu_bg.png')

    // 角色动画帧
    this.load.image('player-idle', '/assets/images/characters/player/idle_00.png')
    this.load.image('wolf-idle', '/assets/images/characters/wolf/idle_00.png')
  }

  private loadAudio(): void {
    // 背景音乐
    this.load.audio('bgm-battle', '/assets/audio/bgm/bgm_battle.mp3')
    this.load.audio('bgm-explore', '/assets/audio/bgm/bgm_explore.mp3')
    
    // 音效
    this.load.audio('sfx-sword', '/assets/audio/sfx/sfx_sword.wav')
    this.load.audio('sfx-hit', '/assets/audio/sfx/sfx_hit.wav')
    this.load.audio('sfx-victory', '/assets/audio/sfx/victory.ogg')
    this.load.audio('sfx-click', '/assets/audio/sfx/ui_click.ogg')
  }
}
