from flask import Flask, request, jsonify
from flask_cors import CORS
from game.player import Player
from game.battle_manager import BattleManager
import json
import os

app = Flask(__name__)
CORS(app)

# 初始化游戏数据
player = Player()
battle_manager = BattleManager()

# 加载数据文件
def load_data(filename):
    with open(os.path.join('data', filename), 'r', encoding='utf-8') as f:
        return json.load(f)

enemies_data = load_data('enemies.json')
skills_data = load_data('skills.json')
items_data = load_data('items.json')
maps_data = load_data('maps.json')

@app.route('/api/player', methods=['GET', 'POST'])
def player_api():
    if request.method == 'GET':
        return jsonify(player.to_dict())
    elif request.method == 'POST':
        data = request.json
        player.from_dict(data)
        return jsonify(player.to_dict())

@app.route('/api/battle/start', methods=['POST'])
def start_battle():
    data = request.json
    enemy_configs = data.get('enemies', [])
    result = battle_manager.start_battle(player, enemy_configs)
    return jsonify(result)

@app.route('/api/battle/action', methods=['POST'])
def battle_action():
    data = request.json
    action = data.get('action')
    target = data.get('target')
    skill = data.get('skill')
    
    # 解析target格式，如enemy_01 -> 0
    target_index = int(target.split('_')[1]) - 1
    
    result = battle_manager.process_action(action, target_index, skill)
    return jsonify(result)

@app.route('/api/map', methods=['GET'])
def get_map():
    map_id = request.args.get('id', 'map_01')
    for map_data in maps_data['maps']:
        if map_data['id'] == map_id:
            return jsonify(map_data)
    return jsonify({"error": "Map not found"})

@app.route('/api/save', methods=['POST'])
def save_game():
    data = request.json
    with open('save.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({"message": "Game saved"})

@app.route('/api/load', methods=['GET'])
def load_game():
    if os.path.exists('save.json'):
        with open('save.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"error": "Save file not found"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
