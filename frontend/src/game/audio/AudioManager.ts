/**
 * 音效管理器
 * 基于 Howler.js 的音频管理系统
 */

import { Howl, Howler } from 'howler'

type SoundType = 'bgm' | 'sfx'

interface SoundConfig {
  src: string
  loop?: boolean
  volume?: number
  preload?: boolean
}

/**
 * 音效管理器类
 */
export class AudioManager {
  private static instance: AudioManager | null = null
  
  private bgmPlayer: Howl | null = null
  private sfxPlayers: Map<string, Howl> = new Map()
  private bgmVolume = 0.5
  private sfxVolume = 0.7
  private currentBgm: string = ''
  private isMuted = false

  private constructor() {
    // 预加载常用音效
    this.preloadCommonSFX()
  }

  /**
   * 获取单例实例
   */
  public static getInstance(): AudioManager {
    if (!AudioManager.instance) {
      AudioManager.instance = new AudioManager()
    }
    return AudioManager.instance
  }

  /**
   * 预加载常用音效
   */
  private preloadCommonSFX(): void {
    const commonSfx = [
      'sfx_click',
      'sfx_confirm',
      'sfx_cancel',
      'sfx_sword',
      'sfx_hit',
      'sfx_victory',
      'sfx_defeat',
      'sfx_meditate',
      'sfx_cultivate',
      'sfx_breakthrough'
    ]

    commonSfx.forEach(name => {
      this.loadSFX(name)
    })
  }

  /**
   * 加载音效
   */
  private loadSFX(name: string): Howl {
    if (this.sfxPlayers.has(name)) {
      return this.sfxPlayers.get(name)!
    }

    const sfx = new Howl({
      src: [`/assets/audio/sfx/${name}.wav`],
      volume: this.sfxVolume,
      preload: true
    })

    this.sfxPlayers.set(name, sfx)
    return sfx
  }

  /**
   * 播放背景音乐
   */
  public playBGM(name: string, fadeIn = true): void {
    if (this.isMuted) return
    if (this.currentBgm === name && this.bgmPlayer?.playing()) return

    // 停止当前背景音乐
    if (this.bgmPlayer) {
      if (fadeIn) {
        this.bgmPlayer.fade(this.bgmVolume, 0, 1000)
        setTimeout(() => this.bgmPlayer?.stop(), 1000)
      } else {
        this.bgmPlayer.stop()
      }
    }

    // 创建新的背景音乐播放器
    this.bgmPlayer = new Howl({
      src: [`/assets/audio/bgm/${name}.mp3`],
      loop: true,
      volume: fadeIn ? 0 : this.bgmVolume,
      onloaderror: () => {
        console.warn(`背景音乐加载失败: ${name}`)
      }
    })

    this.currentBgm = name
    this.bgmPlayer.play()

    // 淡入效果
    if (fadeIn) {
      this.bgmPlayer.fade(0, this.bgmVolume, 1000)
    }
  }

  /**
   * 停止背景音乐
   */
  public stopBGM(fadeOut = true): void {
    if (!this.bgmPlayer) return

    if (fadeOut) {
      this.bgmPlayer.fade(this.bgmVolume, 0, 1000)
      setTimeout(() => {
        this.bgmPlayer?.stop()
        this.bgmPlayer = null
        this.currentBgm = ''
      }, 1000)
    } else {
      this.bgmPlayer.stop()
      this.bgmPlayer = null
      this.currentBgm = ''
    }
  }

  /**
   * 暂停背景音乐
   */
  public pauseBGM(): void {
    this.bgmPlayer?.pause()
  }

  /**
   * 恢复背景音乐
   */
  public resumeBGM(): void {
    if (this.isMuted) return
    this.bgmPlayer?.play()
  }

  /**
   * 播放音效
   */
  public playSFX(name: string): void {
    if (this.isMuted) return

    let sfx = this.sfxPlayers.get(name)
    
    if (!sfx) {
      sfx = this.loadSFX(name)
    }

    // 如果正在播放，创建新的实例
    if (sfx.playing()) {
      sfx = new Howl({
        src: [`/assets/audio/sfx/${name}.wav`],
        volume: this.sfxVolume
      })
    }

    sfx.play()
  }

  /**
   * 设置音量
   */
  public setVolume(type: SoundType, volume: number): void {
    const clampedVolume = Math.max(0, Math.min(1, volume))

    if (type === 'bgm') {
      this.bgmVolume = clampedVolume
      if (this.bgmPlayer) {
        this.bgmPlayer.volume(clampedVolume)
      }
    } else {
      this.sfxVolume = clampedVolume
      // 更新所有已加载音效的音量
      this.sfxPlayers.forEach(sfx => {
        sfx.volume(clampedVolume)
      })
    }
  }

  /**
   * 获取音量
   */
  public getVolume(type: SoundType): number {
    return type === 'bgm' ? this.bgmVolume : this.sfxVolume
  }

  /**
   * 静音
   */
  public mute(): void {
    this.isMuted = true
    Howler.mute(true)
  }

  /**
   * 取消静音
   */
  public unmute(): void {
    this.isMuted = false
    Howler.mute(false)
  }

  /**
   * 切换静音状态
   */
  public toggleMute(): boolean {
    if (this.isMuted) {
      this.unmute()
    } else {
      this.mute()
    }
    return this.isMuted
  }

  /**
   * 获取静音状态
   */
  public getMuted(): boolean {
    return this.isMuted
  }

  /**
   * 销毁管理器
   */
  public destroy(): void {
    this.stopBGM(false)
    this.sfxPlayers.forEach(sfx => sfx.unload())
    this.sfxPlayers.clear()
    AudioManager.instance = null
  }
}

// 导出便捷函数
export const audioManager = AudioManager.getInstance()
export const playBGM = (name: string, fadeIn?: boolean) => audioManager.playBGM(name, fadeIn)
export const stopBGM = (fadeOut?: boolean) => audioManager.stopBGM(fadeOut)
export const playSFX = (name: string) => audioManager.playSFX(name)
