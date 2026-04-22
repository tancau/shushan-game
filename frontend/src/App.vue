<template>
  <div id="app">
    <h1>蜀山剑侠传</h1>
    <div id="game-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { MenuScene } from './scenes/MenuScene'
import { MapScene } from './scenes/MapScene'
import { BattleScene } from './scenes/BattleScene'
import Phaser from 'phaser'

onMounted(() => {
  const config: Phaser.Types.Core.GameConfig = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: 'game-container',
    scene: [MenuScene, MapScene, BattleScene],
    physics: {
      default: 'arcade',
      arcade: {
        gravity: { y: 0 },
        debug: false
      }
    }
  }

  new Phaser.Game(config)
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

#game-container {
  margin: 0 auto;
}
</style>
