export class Api {
  static async getPlayer() {
    const response = await fetch('/api/player')
    return response.json()
  }

  static async updatePlayer(data: any) {
    const response = await fetch('/api/player', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    return response.json()
  }

  static async startBattle(enemies: any[]) {
    const response = await fetch('/api/battle/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ enemies })
    })
    return response.json()
  }

  static async battleAction(action: string, target: string, skill?: string) {
    const response = await fetch('/api/battle/action', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ action, target, skill })
    })
    return response.json()
  }

  static async getMap(mapId: string) {
    const response = await fetch(`/api/map?id=${mapId}`)
    return response.json()
  }

  static async saveGame(data: any) {
    const response = await fetch('/api/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    return response.json()
  }

  static async loadGame() {
    const response = await fetch('/api/load')
    return response.json()
  }
}
