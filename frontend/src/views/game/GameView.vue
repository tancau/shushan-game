<template>
  <div class="game-page">
    <GameCanvas
      ref="gameCanvas"
      :initial-scene="initialScene"
      :show-controls="true"
      @game-ready="onGameReady"
      @scene-change="onSceneChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GameCanvas from '@/components/game/GameCanvas.vue'
import { ShushanGame, SCENE_KEYS } from '@/game/Game'

const route = useRoute()
const router = useRouter()

// 从路由参数获取初始场景
const initialScene = ref<string>(
  (route.query.scene as string) || SCENE_KEYS.BOOT
)

const gameCanvas = ref<InstanceType<typeof GameCanvas> | null>(null)

// 游戏就绪回调
const onGameReady = (game: ShushanGame) => {
  console.log('游戏已就绪', game)
}

// 场景变化回调
const onSceneChange = (scene: string) => {
  console.log('场景切换:', scene)
  
  // 更新 URL 参数
  router.replace({
    query: { scene }
  })
}

// 暴露方法给父组件
defineExpose({
  switchScene: (scene: string, data?: object) => {
    gameCanvas.value?.switchScene(scene, data)
  },
  pause: () => gameCanvas.value?.pause(),
  resume: () => gameCanvas.value?.resume()
})
</script>

<style scoped>
.game-page {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #1a1a2e;
}
</style>
