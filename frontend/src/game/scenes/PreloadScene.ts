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
  private bg!: Phaser.GameObjects.Image

  constructor() {
    super(SCENE_KEYS.PRELOAD)
  }

  protected onCreate(): void {
    this.createLoadingUI()
    this.setupLoadEvents()
    this.loadAllAssets()
  }

  private createLoadingUI(): void {
    // 使用地图背景作为加载页背景
    this.bg = this.add.image(this.centerX, this.centerY, 'bg-map')
    this.bg.setScale(0.8)
    
    // 半透明遮罩
    const overlay = this.add.rectangle(this.centerX, this.centerY, 1280, 720, 0x000000, 0.5)

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
      this.createAnimations()
      this.time.delayedCall(500, () => {
        this.transitionTo({ targetScene: SCENE_KEYS.MAIN_MENU })
      })
    })
  }

  private loadAllAssets(): void {
    this.loadImages()
    this.loadCharacterFrames()
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
  }

  private loadCharacterFrames(): void {
    // 主角动画帧
    for (let i = 0; i < 4; i++) {
      this.load.image(`player-idle-${i}`, `/assets/images/characters/player/idle_0${i}.png`)
      this.load.image(`player-attack-${i}`, `/assets/images/characters/player/attack_0${i}.png`)
      this.load.image(`player-hurt-${i}`, `/assets/images/characters/player/hurt_0${i}.png`)
      this.load.image(`player-walk-${i}`, `/assets/images/characters/player/walk_0${i}.png`)
    }
    
    // 妖狼动画帧
    for (let i = 0; i < 4; i++) {
      this.load.image(`wolf-idle-${i}`, `/assets/images/characters/wolf/idle_0${i}.png`)
      this.load.image(`wolf-attack-${i}`, `/assets/images/characters/wolf/attack_0${i}.png`)
      this.load.image(`wolf-hurt-${i}`, `/assets/images/characters/wolf/hurt_0${i}.png`)
    }
  }

  private createAnimations(): void {
    // 创建主角动画
    this.anims.create({
      key: 'player-idle',
      frames: [
        { key: 'player-idle-0' },
        { key: 'player-idle-1' },
        { key: 'player-idle-2' },
        { key: 'player-idle-3' }
      ],
      frameRate: 6,
      repeat: -1
    })

    this.anims.create({
      key: 'player-attack',
      frames: [
        { key: 'player-attack-0' },
        { key: 'player-attack-1' },
        { key: 'player-attack-2' },
        { key: 'player-attack-3' }
      ],
      frameRate: 10,
      repeat: 0
    })

    this.anims.create({
      key: 'player-hurt',
      frames: [
        { key: 'player-hurt-0' },
        { key: 'player-hurt-1' },
        { key: 'player-hurt-2' },
        { key: 'player-hurt-3' }
      ],
      frameRate: 8,
      repeat: 0
    })

    this.anims.create({
      key: 'player-walk',
      frames: [
        { key: 'player-walk-0' },
        { key: 'player-walk-1' },
        { key: 'player-walk-2' },
        { key: 'player-walk-3' }
      ],
      frameRate: 8,
      repeat: -1
    })

    // 创建妖狼动画
    this.anims.create({
      key: 'wolf-idle',
      frames: [
        { key: 'wolf-idle-0' },
        { key: 'wolf-idle-1' },
        { key: 'wolf-idle-2' },
        { key: 'wolf-idle-3' }
      ],
      frameRate: 6,
      repeat: -1
    })

    this.anims.create({
      key: 'wolf-attack',
      frames: [
        { key: 'wolf-attack-0' },
        { key: 'wolf-attack-1' },
        { key: 'wolf-attack-2' },
        { key: 'wolf-attack-3' }
      ],
      frameRate: 10,
      repeat: 0
    })

    this.anims.create({
      key: 'wolf-hurt',
      frames: [
        { key: 'wolf-hurt-0' },
        { key: 'wolf-hurt-1' },
        { key: 'wolf-hurt-2' },
        { key: 'wolf-hurt-3' }
      ],
      frameRate: 8,
      repeat: 0
    })
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
