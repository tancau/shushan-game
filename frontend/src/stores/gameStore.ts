import { defineStore } from 'pinia'

export const useGameStore = defineStore('game', {
  state: () => ({
    player: {
      name: '主角',
      level: 1,
      realm: '练气期',
      hp: 100,
      max_hp: 100,
      mp: 50,
      max_mp: 50,
      attack: 20,
      defense: 10,
      speed: 15,
      skills: ['剑斩', '火球术'],
      inventory: []
    },
    currentMap: 'map_01',
    battleState: null as any,
    inventory: [],
    quests: [],
    settings: {
      sound: true,
      music: true,
      difficulty: 'normal'
    }
  }),

  actions: {
    updatePlayer(data: any) {
      this.player = { ...this.player, ...data }
    },

    setCurrentMap(mapId: string) {
      this.currentMap = mapId
    },

    setBattleState(state: any) {
      this.battleState = state
    },

    addItem(item: any) {
      this.inventory.push(item)
    },

    removeItem(itemId: string) {
      this.inventory = this.inventory.filter(item => item.id !== itemId)
    },

    updateSettings(settings: any) {
      this.settings = { ...this.settings, ...settings }
    }
  }
})
