<template>
  <div class="game-container">
    <div id="game-canvas" ref="gameContainer"></div>
    
    <!-- 游戏加载遮罩 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p>正在加载游戏...</p>
      </div>
    </div>
    
    <!-- 游戏控制栏 -->
    <div v-if="showControls" class="game-controls">
      <button @click="toggleFullscreen" class="control-btn" title="全屏">
        <span v-if="!isFullscreen">⛶</span>
        <span v-else>⛶</span>
      </button>
      <button @click="toggleSound" class="control-btn" title="音效">
        <span v-if="!isMuted">🔊</span>
        <span v-else>🔇</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { createGame, destroyGame, ShushanGame, SCENE_KEYS } from '@/game/Game'
import { audioManager } from '@/game/audio/AudioManager'

// Props
interface Props {
  initialScene?: string
  showControls?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  initialScene: SCENE_KEYS.BOOT,
  showControls: true
})

// Emits
const emit = defineEmits<{
  gameReady: [game: ShushanGame]
  sceneChange: [scene: string]
}>()

// Refs
const gameContainer = ref<HTMLDivElement | null>(null)
const isLoading = ref(true)
const isFullscreen = ref(false)
const isMuted = ref(false)

// Game instance
let game: ShushanGame | null = null

// 初始化游戏
onMounted(() => {
  if (gameContainer.value) {
    // 确保容器有 ID
    gameContainer.value.id = 'game-canvas'
    
    // 创建游戏实例
    game = createGame('game-canvas')
    
    // 监听游戏就绪
    game.events.once('ready', () => {
      isLoading.value = false
      emit('gameReady', game!)
      
      // 如果指定了初始场景，切换到该场景
      if (props.initialScene !== SCENE_KEYS.BOOT) {
        game?.switchScene(props.initialScene)
      }
    })
    
    // 监听场景变化
    game.events.on('scenechange', (scene: string) => {
      emit('sceneChange', scene)
    })
  }
})

// 清理游戏
onUnmounted(() => {
  destroyGame()
  audioManager.destroy()
})

// 切换全屏
const toggleFullscreen = async () => {
  if (!document.fullscreenElement) {
    await document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    await document.exitFullscreen()
    isFullscreen.value = false
  }
}

// 切换音效
const toggleSound = () => {
  isMuted.value = audioManager.toggleMute()
}

// 暴露方法
defineExpose({
  getGame: () => game,
  switchScene: (scene: string, data?: object) => game?.switchScene(scene, data),
  pause: () => game?.pauseGame(),
  resume: () => game?.resumeGame()
})
</script>

<style scoped>
.game-container {
  position: relative;
  width: 100%;
  height: 100%;
  background: #1a1a2e;
  overflow: hidden;
}

#game-canvas {
  width: 100%;
  height: 100%;
}

#game-canvas canvas {
  display: block;
  margin: 0 auto;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(26, 26, 46, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.loading-content {
  text-align: center;
  color: #FFD700;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid #333;
  border-top: 3px solid #FFD700;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-content p {
  font-size: 18px;
  margin: 0;
}

.game-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 10px;
  z-index: 50;
}

.control-btn {
  width: 40px;
  height: 40px;
  border: 2px solid #FFD700;
  background: rgba(26, 26, 46, 0.8);
  color: #FFD700;
  font-size: 20px;
  cursor: pointer;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.control-btn:hover {
  background: rgba(255, 215, 0, 0.2);
  transform: scale(1.1);
}
</style>
