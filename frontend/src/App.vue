<template>
  <div id="app">
    <div id="game-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { ShushanGame } from './game/Game'

onMounted(() => {
  // 使用完整的游戏系统
  new ShushanGame('game-container')
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#app {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #0F1419;
}

#game-container {
  width: 100%;
  height: 100%;
}

#game-container canvas {
  display: block;
  margin: 0 auto;
}
</style>
