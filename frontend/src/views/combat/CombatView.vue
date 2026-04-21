<template>
  <div class="combat-view">
    <div class="combat-header">
      <h1 class="combat-title">战斗</h1>
      <div class="combat-turn">
        <span class="turn-label">回合</span>
        <span class="turn-value">{{ combatState.turn }}</span>
      </div>
    </div>

    <div class="combat-arena">
      <!-- 敌方区域 -->
      <div class="enemy-section">
        <div class="combatant enemy">
          <div class="combatant-avatar">
            <span class="avatar-icon">🐺</span>
          </div>
          <div class="combatant-info">
            <h3 class="combatant-name">{{ enemy.name }}</h3>
            <span class="combatant-type">{{ enemy.type }}</span>
          </div>
          <div class="combatant-stats">
            <div class="hp-bar">
              <div class="hp-label">
                <span>生命</span>
                <span>{{ enemy.currentHp }}/{{ enemy.maxHp }}</span>
              </div>
              <div class="hp-track">
                <div class="hp-fill enemy-hp" :style="{ width: enemyHpPercent + '%' }" />
              </div>
            </div>
          </div>
          <div v-if="enemy.status.length > 0" class="status-effects">
            <span v-for="status in enemy.status" :key="status" class="status-tag">{{ status }}</span>
          </div>
        </div>
      </div>

      <!-- VS 标识 -->
      <div class="vs-divider">
        <span class="vs-text">VS</span>
      </div>

      <!-- 我方区域 -->
      <div class="player-section">
        <div class="combatant player">
          <div class="combatant-avatar">
            <span class="avatar-icon">🗡️</span>
          </div>
          <div class="combatant-info">
            <h3 class="combatant-name">{{ playerStore.player?.name || '玩家' }}</h3>
            <span class="combatant-realm">{{ playerStore.currentRealm }}</span>
          </div>
          <div class="combatant-stats">
            <div class="hp-bar">
              <div class="hp-label">
                <span>生命</span>
                <span>{{ playerHp }}/{{ playerMaxHp }}</span>
              </div>
              <div class="hp-track">
                <div class="hp-fill player-hp" :style="{ width: playerHpPercent + '%' }" />
              </div>
            </div>
            <div class="mp-bar">
              <div class="mp-label">
                <span>真元</span>
                <span>{{ playerMp }}/{{ playerMaxMp }}</span>
              </div>
              <div class="mp-track">
                <div class="mp-fill" :style="{ width: playerMpPercent + '%' }" />
              </div>
            </div>
          </div>
          <div v-if="playerStatus.length > 0" class="status-effects">
            <span v-for="status in playerStatus" :key="status" class="status-tag">{{ status }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 战斗日志 -->
    <div class="combat-log">
      <SsCard title="战斗日志" :hoverable="false">
        <div class="log-list">
          <div
            v-for="(log, index) in combatLogs"
            :key="index"
            :class="['log-item', log.type]"
          >
            <span class="log-turn">回合{{ log.turn }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
          <div v-if="combatLogs.length === 0" class="log-empty">
            战斗即将开始...
          </div>
        </div>
      </SsCard>
    </div>

    <!-- 战斗操作 -->
    <div class="combat-actions">
      <SsCard :hoverable="false">
        <div class="action-grid">
          <SsButton
            type="primary"
            size="large"
            :disabled="!isPlayerTurn || combatState.isOver"
            @click="handleAttack"
          >
            <template #icon>
              <el-icon><Aim /></el-icon>
            </template>
            普通攻击
          </SsButton>
          <SsButton
            type="gold"
            size="large"
            :disabled="!isPlayerTurn || combatState.isOver"
            @click="handleSkill"
          >
            <template #icon>
              <el-icon><MagicStick /></el-icon>
            </template>
            释放技能
          </SsButton>
          <SsButton
            type="default"
            size="large"
            :disabled="!isPlayerTurn || combatState.isOver"
            @click="handleDefend"
          >
            <template #icon>
              <el-icon><Lock /></el-icon>
            </template>
            防御
          </SsButton>
          <SsButton
            type="ghost"
            size="large"
            :disabled="combatState.isOver"
            @click="handleFlee"
          >
            <template #icon>
              <el-icon><Right /></el-icon>
            </template>
            逃跑
          </SsButton>
        </div>
      </SsCard>
    </div>

    <!-- 战斗结果 -->
    <div v-if="combatState.isOver" class="combat-result-overlay">
      <div class="result-modal">
        <h2 class="result-title" :class="combatState.result">{{ resultTitle }}</h2>
        <div v-if="combatState.rewards" class="result-rewards">
          <div class="reward-item">
            <span class="reward-label">修为</span>
            <span class="reward-value">+{{ combatState.rewards.cultivation }}</span>
          </div>
          <div class="reward-item">
            <span class="reward-label">灵石</span>
            <span class="reward-value">+{{ combatState.rewards.spiritStones }}</span>
          </div>
        </div>
        <SsButton type="primary" size="large" @click="resetCombat">
          继续冒险
        </SsButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { ElIcon } from 'element-plus'
import { Aim, MagicStick, Lock, Right } from '@element-plus/icons-vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { usePlayerStore } from '@/stores/player'
import { useGameStore } from '@/stores/game'

const playerStore = usePlayerStore()
const gameStore = useGameStore()

interface CombatLog {
  turn: number
  message: string
  type: 'player' | 'enemy' | 'system'
}

interface CombatState {
  turn: number
  isPlayerTurn: boolean
  isOver: boolean
  result: 'win' | 'lose' | 'flee' | ''
  rewards?: {
    cultivation: number
    spiritStones: number
  }
}

const enemy = reactive({
  name: '山中妖兽',
  type: '妖兽',
  maxHp: 200,
  currentHp: 200,
  attack: 30,
  status: [] as string[],
})

const playerHp = ref(1000)
const playerMaxHp = ref(1000)
const playerMp = ref(500)
const playerMaxMp = ref(500)
const playerStatus = ref<string[]>([])

const combatState = reactive<CombatState>({
  turn: 1,
  isPlayerTurn: true,
  isOver: false,
  result: '',
})

const combatLogs = ref<CombatLog[]>([])

const enemyHpPercent = computed(() => (enemy.currentHp / enemy.maxHp) * 100)
const playerHpPercent = computed(() => (playerHp.value / playerMaxHp.value) * 100)
const playerMpPercent = computed(() => (playerMp.value / playerMaxMp.value) * 100)
const isPlayerTurn = computed(() => combatState.isPlayerTurn && !combatState.isOver)

const resultTitle = computed(() => {
  switch (combatState.result) {
    case 'win': return '战斗胜利！'
    case 'lose': return '战斗失败...'
    case 'flee': return '成功逃脱'
    default: return ''
  }
})

function addLog(message: string, type: CombatLog['type'] = 'system') {
  combatLogs.value.unshift({
    turn: combatState.turn,
    message,
    type,
  })
  if (combatLogs.value.length > 20) {
    combatLogs.value.pop()
  }
}

function handleAttack() {
  if (!combatState.isPlayerTurn || combatState.isOver) return

  const damage = Math.floor(Math.random() * 20) + 30
  enemy.currentHp = Math.max(0, enemy.currentHp - damage)
  addLog(`你对${enemy.name}造成了 ${damage} 点伤害！`, 'player')

  if (enemy.currentHp <= 0) {
    endCombat('win')
    return
  }

  combatState.isPlayerTurn = false
  setTimeout(enemyTurn, 1000)
}

function handleSkill() {
  if (!combatState.isPlayerTurn || combatState.isOver) return

  const damage = Math.floor(Math.random() * 30) + 50
  enemy.currentHp = Math.max(0, enemy.currentHp - damage)
  playerMp.value = Math.max(0, playerMp.value - 20)
  addLog(`你释放技能，对${enemy.name}造成了 ${damage} 点伤害！`, 'player')

  if (enemy.currentHp <= 0) {
    endCombat('win')
    return
  }

  combatState.isPlayerTurn = false
  setTimeout(enemyTurn, 1000)
}

function handleDefend() {
  if (!combatState.isPlayerTurn || combatState.isOver) return

  addLog('你摆出防御姿态，受到的伤害减少50%', 'player')
  combatState.isPlayerTurn = false
  setTimeout(() => enemyTurn(true), 1000)
}

function handleFlee() {
  if (combatState.isOver) {
    resetCombat()
    return
  }

  const fleeChance = Math.random()
  if (fleeChance > 0.5) {
    endCombat('flee')
  } else {
    addLog('逃跑失败！', 'system')
    combatState.isPlayerTurn = false
    setTimeout(enemyTurn, 1000)
  }
}

function enemyTurn(isDefending = false) {
  if (combatState.isOver) return

  const baseDamage = Math.floor(Math.random() * 15) + enemy.attack
  const damage = isDefending ? Math.floor(baseDamage * 0.5) : baseDamage
  playerHp.value = Math.max(0, playerHp.value - damage)
  addLog(`${enemy.name}对你造成了 ${damage} 点伤害！`, 'enemy')

  if (playerHp.value <= 0) {
    endCombat('lose')
    return
  }

  combatState.turn++
  combatState.isPlayerTurn = true
}

function endCombat(result: 'win' | 'lose' | 'flee') {
  combatState.isOver = true
  combatState.result = result

  if (result === 'win') {
    combatState.rewards = {
      cultivation: 100,
      spiritStones: 20,
    }
    addLog('战斗胜利！获得奖励', 'system')
  } else if (result === 'lose') {
    addLog('战斗失败...', 'system')
  } else {
    addLog('成功逃脱', 'system')
  }
}

function resetCombat() {
  enemy.currentHp = enemy.maxHp
  playerHp.value = playerMaxHp.value
  playerMp.value = playerMaxMp.value
  combatState.turn = 1
  combatState.isPlayerTurn = true
  combatState.isOver = false
  combatState.result = ''
  combatState.rewards = undefined
  combatLogs.value = []
}
</script>

<style scoped lang="scss">
.combat-view {
  max-width: 800px;
  margin: 0 auto;
}

.combat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.combat-title {
  font-family: var(--font-title);
  font-size: var(--text-2xl);
  color: var(--text-primary);
  margin: 0;
}

.combat-turn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--bg-card);
  border-radius: var(--radius-md);
}

.turn-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.turn-value {
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--color-primary-light);
}

.combat-arena {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.combatant {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: linear-gradient(135deg, var(--bg-card), var(--bg-secondary));
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);

  &.enemy {
    border-color: rgba(231, 76, 60, 0.3);
  }

  &.player {
    border-color: rgba(39, 174, 96, 0.3);
  }
}

.combatant-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  background: var(--bg-secondary);
  flex-shrink: 0;
}

.combatant-info {
  flex: 1;
}

.combatant-name {
  font-family: var(--font-title);
  font-size: var(--text-lg);
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.combatant-type,
.combatant-realm {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.combatant-stats {
  width: 200px;
}

.hp-bar,
.mp-bar {
  margin-bottom: var(--space-2);
}

.hp-label,
.mp-label {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-xs);
  color: var(--text-secondary);
  margin-bottom: var(--space-1);
}

.hp-track,
.mp-track {
  height: 10px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.hp-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.5s var(--ease-default);

  &.enemy-hp {
    background: linear-gradient(90deg, #E74C3C, #C0392B);
  }

  &.player-hp {
    background: linear-gradient(90deg, #27AE60, #2ECC71);
  }
}

.mp-fill {
  height: 100%;
  background: linear-gradient(90deg, #2E86AB, #5DADE2);
  border-radius: var(--radius-full);
  transition: width 0.5s var(--ease-default);
}

.status-effects {
  display: flex;
  gap: var(--space-1);
  flex-wrap: wrap;
}

.status-tag {
  font-size: var(--text-xs);
  padding: 2px 8px;
  background: rgba(155, 89, 182, 0.2);
  color: #9B59B6;
  border-radius: var(--radius-sm);
}

.vs-divider {
  text-align: center;
  padding: var(--space-2);
}

.vs-text {
  font-family: var(--font-title);
  font-size: var(--text-2xl);
  color: var(--text-gold);
  font-weight: 700;
}

.combat-log {
  margin-bottom: var(--space-4);
}

.log-list {
  max-height: 200px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.log-item {
  display: flex;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);

  &.player {
    border-left: 3px solid #27AE60;
  }

  &.enemy {
    border-left: 3px solid #E74C3C;
  }

  &.system {
    border-left: 3px solid var(--color-primary-light);
  }
}

.log-turn {
  color: var(--text-muted);
  width: 60px;
  flex-shrink: 0;
}

.log-message {
  color: var(--text-primary);
}

.log-empty {
  text-align: center;
  color: var(--text-muted);
  padding: var(--space-4);
}

.combat-actions {
  margin-bottom: var(--space-4);
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}

.combat-result-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.result-modal {
  background: linear-gradient(180deg, var(--bg-card), var(--bg-secondary));
  border: 1px solid var(--border-gold);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  text-align: center;
  min-width: 300px;
}

.result-title {
  font-family: var(--font-title);
  font-size: var(--text-3xl);
  margin: 0 0 var(--space-4);

  &.win {
    color: #27AE60;
  }

  &.lose {
    color: #E74C3C;
  }

  &.flee {
    color: var(--color-primary-light);
  }
}

.result-rewards {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
  padding: var(--space-4);
  background: rgba(39, 174, 96, 0.1);
  border-radius: var(--radius-md);
}

.reward-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reward-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.reward-value {
  font-size: var(--text-lg);
  font-weight: 600;
  color: #27AE60;
}

@media (max-width: 640px) {
  .combatant {
    flex-direction: column;
    text-align: center;
  }

  .combatant-stats {
    width: 100%;
  }

  .action-grid {
    grid-template-columns: 1fr;
  }
}
</style>
