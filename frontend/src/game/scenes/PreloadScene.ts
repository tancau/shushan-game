/**
 * 预加载场景
 * 显示加载进度条，加载所有游戏资源
 */

import { BaseScene } from './BaseScene'
import { SCENE_KEYS } from '../Game'
import { COLORS, DURATION, SCENE_ASSETS } from '../config/gameConfig'

export class PreloadScene extends BaseScene {
  private progressBar!: Phaser.GameObjects.Rectangle
  private progressBox!: Phaser.GameObjects.Rectangle
  private loadingText!: Phaser.GameObjects.Text
  private percentText!: Phaser.GameObjects.Text

  constructor() {
    super(SCENE_KEYS.PRELOAD)
  }

  protected onCreate(): void {
    // 创建加载界面
    this.createLoadingUI()

    // 设置加载事件
    this.setupLoadEvents()

    // 加载所有资源
    this.loadAllAssets()
  }

  /**
   * 创建加载界面 UI
   */
  private createLoadingUI(): void {
    const width = this.cameras.main.width
    const height = this.cameras.main.height

    // 进度条背景框
    this.progressBox = this.add.rectangle(
      this.centerX,
      this.centerY,
      320,
      50,
      COLORS.BG_MEDIUM
    )
    this.progressBox.setStrokeStyle(2, COLORS.PRIMARY_GOLD)

    // 进度条
    this.progressBar = this.add.rectangle(
      this.centerX - 150,
      this.centerY,
      0,
      30,
      COLORS.PRIMARY_GOLD
    )
    this.progressBar.setOrigin(0, 0.5)

    // 加载文字
    this.loadingText = this.createText(
      this.centerX,
      this.centerY - 50,
      '加载中...',
      { fontSize: '24px', color: '#FFD700' }
    )
    this.loadingText.setOrigin(0.5)

    // 百分比文字
    this.percentText = this.createText(
      this.centerX,
      this.centerY,
      '0%',
      { fontSize: '20px', color: '#FFFFFF' }
    )
    this.percentText.setOrigin(0.5)

    // 标题
    const titleText = this.createText(
      this.centerX,
      this.centerY - 120,
      '蜀山剑侠传',
      { fontSize: '48px', color: '#FFD700', strokeThickness: 6 }
    )
    titleText.setOrigin(0.5)

    // 标题光效
    this.tweens.add({
      targets: titleText,
      alpha: 0.7,
      duration: 1000,
      yoyo: true,
      repeat: -1
    })
  }

  /**
   * 设置加载事件监听
   */
  private setupLoadEvents(): void {
    // 加载进度事件
    this.load.on('progress', (value: number) => {
      // 更新进度条
      this.progressBar.width = 300 * value

      // 更新百分比文字
      this.percentText.setText(`${Math.floor(value * 100)}%`)
    })

    // 加载文件事件
    this.load.on('fileprogress', (file: Phaser.Loader.File) => {
      // 可以在这里显示当前加载的文件
      // console.log(`加载: ${file.key}`)
    })

    // 加载完成事件
    this.load.once('complete', () => {
      this.loadingText.setText('加载完成!')

      // 延迟后切换到主菜单
      this.time.delayedCall(500, () => {
        this.transitionTo({ targetScene: SCENE_KEYS.MAIN_MENU })
      })
    })
  }

  /**
   * 加载所有游戏资源
   */
  private loadAllAssets(): void {
    // 加载图片资源
    this.loadImages()

    // 加载音频资源
    this.loadAudio()

    // 加载精灵表
    this.loadSpritesheets()

    // 开始加载
    this.load.start()
  }

  /**
   * 加载图片资源
   */
  private loadImages(): void {
    // 主菜单
    this.load.image('bg-main', '/assets/images/ui/bg-main.png')
    this.load.image('logo', '/assets/images/ui/logo.png')

    // 角色
    this.load.image('bg-character', '/assets/images/ui/bg-character.png')
    this.load.image('player-sprite', '/assets/images/characters/player.png')

    // 修炼
    this.load.image('bg-cultivate', '/assets/images/ui/bg-cultivate.png')
    this.load.image('meditation-effect', '/assets/images/effects/meditation.png')

    // 战斗
    this.load.image('bg-battle', '/assets/images/ui/bg-battle.png')
    this.load.image('battle-ground', '/assets/images/ui/battle-ground.png')
    this.load.image('effect-sword-slash', '/assets/images/effects/sword-slash.png')

    // 世界地图
    this.load.image('bg-worldmap', '/assets/images/ui/bg-worldmap.png')
    this.load.image('map-marker', '/assets/images/ui/map-marker.png')

    // 副本
    this.load.image('bg-dungeon', '/assets/images/ui/bg-dungeon.png')

    // 天劫
    this.load.image('bg-tribulation', '/assets/images/ui/bg-tribulation.png')
  }

  /**
   * 加载音频资源
   */
  private loadAudio(): void {
    // 背景音乐
    this.load.audio('bgm-main', '/assets/audio/bgm/bgm_main.mp3')
    this.load.audio('bgm-character', '/assets/audio/bgm/bgm_character.mp3')
    this.load.audio('bgm-cultivate', '/assets/audio/bgm/bgm_cultivate.mp3')
    this.load.audio('bgm-battle', '/assets/audio/bgm/bgm_battle.mp3')
    this.load.audio('bgm-explore', '/assets/audio/bgm/bgm_explore.mp3')
    this.load.audio('bgm-dungeon', '/assets/audio/bgm/bgm_dungeon.mp3')
    this.load.audio('bgm-tribulation', '/assets/audio/bgm/bgm_tribulation.mp3')

    // UI 音效
    this.load.audio('sfx-click', '/assets/audio/sfx/sfx_click.wav')
    this.load.audio('sfx-confirm', '/assets/audio/sfx/sfx_confirm.wav')
    this.load.audio('sfx-cancel', '/assets/audio/sfx/sfx_cancel.wav')
    this.load.audio('sfx-item', '/assets/audio/sfx/sfx_item.wav')

    // 战斗音效
    this.load.audio('sfx-sword', '/assets/audio/sfx/sfx_sword.wav')
    this.load.audio('sfx-hit', '/assets/audio/sfx/sfx_hit.wav')
    this.load.audio('sfx-critical', '/assets/audio/sfx/sfx_critical.wav')
    this.load.audio('sfx-victory', '/assets/audio/sfx/sfx_victory.wav')
    this.load.audio('sfx-defeat', '/assets/audio/sfx/sfx_defeat.wav')

    // 修炼音效
    this.load.audio('sfx-meditate', '/assets/audio/sfx/sfx_meditate.wav')
    this.load.audio('sfx-cultivate', '/assets/audio/sfx/sfx_cultivate.wav')
    this.load.audio('sfx-breakthrough', '/assets/audio/sfx/sfx_breakthrough.wav')
    this.load.audio('sfx-fail', '/assets/audio/sfx/sfx_fail.wav')
  }

  /**
   * 加载精灵表
   */
  private loadSpritesheets(): void {
    // 角色精灵表（如果存在）
    // this.load.atlas('characters', '/assets/sprites/characters.png', '/assets/sprites/characters.json')

    // 特效精灵表（如果存在）
    // this.load.atlas('effects', '/assets/sprites/effects.png', '/assets/sprites/effects.json')
  }
}
