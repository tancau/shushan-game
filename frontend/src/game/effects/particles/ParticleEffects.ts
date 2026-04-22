/**
 * 粒子特效系统
 * 提供各种游戏粒子效果
 */

import Phaser from 'phaser'
import { COLORS, PARTICLE_CONFIG } from '../../config/gameConfig'

/**
 * 粒子效果类型
 */
export type ParticleType = 'spirit' | 'sword' | 'fire' | 'light' | 'coin' | 'cloud'

/**
 * 粒子效果工厂类
 */
export class ParticleFactory {
  /**
   * 创建灵气粒子
   */
  static createSpiritParticle(
    scene: Phaser.Scene,
    x: number,
    y: number,
    config?: Partial<Phaser.Types.GameObjects.Particles.ParticleEmitterConfig>
  ): Phaser.GameObjects.Particles.ParticleEmitter | null {
    if (!scene.textures.exists('particle-spirit')) return null

    return scene.add.particles(x, y, 'particle-spirit', {
      speed: PARTICLE_CONFIG.SPIRIT.speed,
      angle: PARTICLE_CONFIG.SPIRIT.angle,
      scale: PARTICLE_CONFIG.SPIRIT.scale,
      alpha: PARTICLE_CONFIG.SPIRIT.alpha,
      lifespan: PARTICLE_CONFIG.SPIRIT.lifespan,
      blendMode: PARTICLE_CONFIG.SPIRIT.blendMode,
      tint: PARTICLE_CONFIG.SPIRIT.tint,
      ...config
    })
  }

  /**
   * 创建剑气粒子
   */
  static createSwordParticle(
    scene: Phaser.Scene,
    x: number,
    y: number,
    config?: Partial<Phaser.Types.GameObjects.Particles.ParticleEmitterConfig>
  ): Phaser.GameObjects.Particles.ParticleEmitter | null {
    if (!scene.textures.exists('particle-sword')) return null

    return scene.add.particles(x, y, 'particle-sword', {
      speed: PARTICLE_CONFIG.SWORD.speed,
      scale: PARTICLE_CONFIG.SWORD.scale,
      alpha: PARTICLE_CONFIG.SWORD.alpha,
      lifespan: PARTICLE_CONFIG.SWORD.lifespan,
      blendMode: PARTICLE_CONFIG.SWORD.blendMode,
      tint: PARTICLE_CONFIG.SWORD.tint,
      ...config
    })
  }

  /**
   * 创建火焰粒子
   */
  static createFireParticle(
    scene: Phaser.Scene,
    x: number,
    y: number,
    config?: Partial<Phaser.Types.GameObjects.Particles.ParticleEmitterConfig>
  ): Phaser.GameObjects.Particles.ParticleEmitter | null {
    if (!scene.textures.exists('particle-fire')) return null

    return scene.add.particles(x, y, 'particle-fire', {
      speed: PARTICLE_CONFIG.FIRE.speed,
      angle: PARTICLE_CONFIG.FIRE.angle,
      scale: PARTICLE_CONFIG.FIRE.scale,
      alpha: PARTICLE_CONFIG.FIRE.alpha,
      lifespan: PARTICLE_CONFIG.FIRE.lifespan,
      blendMode: PARTICLE_CONFIG.FIRE.blendMode,
      tint: PARTICLE_CONFIG.FIRE.tint,
      ...config
    })
  }

  /**
   * 创建光芒粒子
   */
  static createLightParticle(
    scene: Phaser.Scene,
    x: number,
    y: number,
    config?: Partial<Phaser.Types.GameObjects.Particles.ParticleEmitterConfig>
  ): Phaser.GameObjects.Particles.ParticleEmitter | null {
    if (!scene.textures.exists('particle-light')) return null

    return scene.add.particles(x, y, 'particle-light', {
      speed: { min: 100, max: 200 },
      scale: { start: 0.8, end: 0 },
      alpha: { start: 1, end: 0 },
      lifespan: 1000,
      blendMode: 'ADD',
      ...config
    })
  }

  /**
   * 创建金币粒子
   */
  static createCoinParticle(
    scene: Phaser.Scene,
    x: number,
    y: number,
    config?: Partial<Phaser.Types.GameObjects.Particles.ParticleEmitterConfig>
  ): Phaser.GameObjects.Particles.ParticleEmitter | null {
    if (!scene.textures.exists('particle-light')) return null

    return scene.add.particles(x, y, 'particle-light', {
      speed: { min: 100, max: 200 },
      angle: { min: 0, max: 360 },
      scale: { start: 0.8, end: 0 },
      alpha: { start: 1, end: 0 },
      lifespan: 2000,
      blendMode: 'ADD',
      tint: 0xFFD700,
      ...config
    })
  }

  /**
   * 根据类型创建粒子
   */
  static create(
    scene: Phaser.Scene,
    type: ParticleType,
    x: number,
    y: number,
    config?: Partial<Phaser.Types.GameObjects.Particles.ParticleEmitterConfig>
  ): Phaser.GameObjects.Particles.ParticleEmitter | null {
    switch (type) {
      case 'spirit':
        return this.createSpiritParticle(scene, x, y, config)
      case 'sword':
        return this.createSwordParticle(scene, x, y, config)
      case 'fire':
        return this.createFireParticle(scene, x, y, config)
      case 'light':
        return this.createLightParticle(scene, x, y, config)
      case 'coin':
        return this.createCoinParticle(scene, x, y, config)
      default:
        return null
    }
  }
}

/**
 * 特效播放器
 * 提供便捷的特效播放方法
 */
export class EffectPlayer {
  /**
   * 播放突破特效
   */
  static playBreakthroughEffect(scene: Phaser.Scene, x: number, y: number): void {
    // 光柱
    const beam = scene.add.rectangle(x, y, 200, 720, COLORS.PRIMARY_GOLD, 0)
    
    scene.tweens.add({
      targets: beam,
      alpha: 0.8,
      duration: 500,
      yoyo: true,
      hold: 2000,
      onComplete: () => beam.destroy()
    })

    // 粒子爆炸
    const emitter = ParticleFactory.createLightParticle(scene, x, y, {
      speed: { min: 200, max: 400 },
      scale: { start: 1, end: 0 },
      lifespan: 2000,
      quantity: 50
    })
    
    if (emitter) {
      emitter.explode()
    }

    // 屏幕震动
    scene.cameras.main.shake(500, 0.01)
  }

  /**
   * 播放胜利特效
   */
  static playVictoryEffect(scene: Phaser.Scene, x: number, y: number): void {
    const emitter = ParticleFactory.createCoinParticle(scene, x, y, {
      speed: { min: 100, max: 200 },
      angle: { min: 0, max: 360 },
      scale: { start: 0.8, end: 0 },
      lifespan: 2000,
      quantity: 30
    })
    
    if (emitter) {
      emitter.explode()
    }
  }

  /**
   * 播放命中特效
   */
  static playHitEffect(scene: Phaser.Scene, x: number, y: number): void {
    const emitter = ParticleFactory.createLightParticle(scene, x, y, {
      speed: { min: 100, max: 200 },
      scale: { start: 0.5, end: 0 },
      lifespan: 500,
      quantity: 10
    })
    
    if (emitter) {
      emitter.explode()
    }
  }

  /**
   * 播放攻击轨迹
   */
  static playAttackTrail(
    scene: Phaser.Scene,
    fromX: number,
    fromY: number,
    toX: number,
    toY: number,
    color: number = COLORS.PRIMARY_GOLD
  ): void {
    const graphics = scene.add.graphics()
    graphics.lineStyle(4, color, 1)
    graphics.beginPath()
    graphics.moveTo(fromX, fromY)
    graphics.lineTo(toX, toY)
    graphics.strokePath()

    scene.tweens.add({
      targets: graphics,
      alpha: 0,
      duration: 300,
      onComplete: () => graphics.destroy()
    })
  }
}
