#!/usr/bin/env python3
"""
蜀山剑侠传 - Web API
用于 Vercel 部署
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.player import Player
from game.artifact import ArtifactManager
from game.skills import SkillManager
from game.world import WorldMap
from game.quest import QuestManager

app = Flask(__name__)
CORS(app)

# 全局游戏实例
games = {}

def get_game(player_id):
    """获取或创建游戏实例"""
    if player_id not in games:
        games[player_id] = Player.load() or Player(player_id)
    return games[player_id]

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>蜀山剑侠传</title>
    <style>
        * { margin: 0; padding:0; box-sizing:border-box; }
        body { 
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { 
            text-align: center;
            color: #ffd700;
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .status-box {
            background: rgba(255,255,255,0.1);
            border: 2px solid #4a4a6a;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .status-title {
            font-size: 1.5em;
            color: #ffd700;
            margin-bottom: 15px;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .status-item {
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 5px;
        }
        .status-label { color: #888; font-size: 0.9em; }
        .status-value { font-size: 1.2em; color: #4fc3f7; margin-top: 5px; }
        
        .actions {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }
        button {
            padding: 15px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: #e0e0e0;
            border: 1px solid #4a4a6a;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        
        .log-box {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            max-height: 300px;
            overflow-y: auto;
        }
        .log-title { color: #ffd700; margin-bottom: 10px; }
        .log-item { padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚔️ 蜀山剑侠传</h1>
        
        <div class="status-box">
            <div class="status-title" id="player-name">加载中...</div>
            <div class="status-grid">
                <div class="status-item">
                    <div class="status-label">境界</div>
                    <div class="status-value" id="realm">-</div>
                </div>
                <div class="status-item">
                    <div class="status-label">修为</div>
                    <div class="status-value" id="cultivation">-</div>
                </div>
                <div class="status-item">
                    <div class="status-label">生命</div>
                    <div class="status-value" id="hp">-</div>
                </div>
                <div class="status-item">
                    <div class="status-label">真元</div>
                    <div class="status-value" id="mp">-</div>
                </div>
            </div>
        </div>
        
        <div class="actions">
            <button class="btn-primary" onclick="doAction('cultivate')">修炼</button>
            <button class="btn-primary" onclick="doAction('advance')">突破</button>
            <button class="btn-secondary" onclick="doAction('battle')">战斗</button>
            <button class="btn-secondary" onclick="doAction('status')">状态</button>
            <button class="btn-secondary" onclick="doAction('artifacts')">法宝</button>
            <button class="btn-secondary" onclick="doAction('skills')">功法</button>
        </div>
        
        <div class="log-box">
            <div class="log-title">消息</div>
            <div id="log">欢迎来到蜀山世界...</div>
        </div>
    </div>
    
    <script>
        const PLAYER_ID = 'tancau';
        
        async function fetchAPI(action) {
            try {
                const response = await fetch('/api/' + action);
                const data = await response.json();
                return data;
            } catch (e) {
                return { error: e.message };
            }
        }
        
        async function updateStatus() {
            const data = await fetchAPI('status');
            if (data.success) {
                document.getElementById('player-name').textContent = data.name;
                document.getElementById('realm').textContent = data.realm;
                document.getElementById('cultivation').textContent = data.cultivation;
                document.getElementById('hp').textContent = data.hp;
                document.getElementById('mp').textContent = data.mp;
            }
        }
        
        async function doAction(action) {
            const data = await fetchAPI(action);
            if (data.message) {
                const log = document.getElementById('log');
                log.innerHTML = '<div class="log-item">' + data.message + '</div>' + log.innerHTML;
            }
            if (data.success !== false) {
                await updateStatus();
            }
        }
        
        // 初始化
        updateStatus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def api_status():
    """获取状态"""
    player = get_game('tancau')
    return jsonify({
        'success': True,
        'name': player.name,
        'realm': player.realm,
        'cultivation': f"{player.cultivation:,}",
        'hp': f"{player.current_hp}/{player.max_hp}",
        'mp': f"{player.current_mp}/{player.max_mp}",
        'spirit_stones': player.spirit_stones,
        'sect': player.sect or '散修'
    })

@app.route('/api/cultivate')
def api_cultivate():
    """修炼"""
    player = get_game('tancau')
    result = player.cultivate('吐纳')
    player.save()
    return jsonify({
        'success': True,
        'message': result['message']
    })

@app.route('/api/advance')
def api_advance():
    """突破"""
    player = get_game('tancau')
    if player.can_advance_realm():
        result = player.advance_realm()
        player.save()
        return jsonify({'success': True, 'message': result})
    else:
        return jsonify({
            'success': False,
            'message': '修为不足，无法突破！'
        })

@app.route('/api/battle')
def api_battle():
    """战斗"""
    player = get_game('tancau')
    from game.combat import CombatSystem
    
    enemy = CombatSystem.create_random_enemy(player.get_realm_level())
    combat = CombatSystem(player, enemy)
    
    # 简化战斗
    attack = combat.player_attack()
    winner = combat.check_victory()
    
    if winner == 'player':
        rewards = combat.get_rewards()
        player.cultivation += rewards['cultivation']
        player.spirit_stones += rewards['spirit_stones']
        if rewards['artifact']:
            player.add_artifact(rewards['artifact'].to_dict())
        player.save()
        return jsonify({
            'success': True,
            'message': f"战斗胜利！修为 +{rewards['cultivation']}，灵石 +{rewards['spirit_stones']}"
        })
    else:
        enemy_atk = combat.enemy_attack()
        player.save()
        return jsonify({
            'success': True,
            'message': f"战斗失败！损失 {enemy_atk['damage']} 生命"
        })

@app.route('/api/artifacts')
def api_artifacts():
    """法宝列表"""
    player = get_game('tancau')
    return jsonify({
        'success': True,
        'message': f"拥有 {len(player.artifacts)} 件法宝",
        'artifacts': player.artifacts
    })

@app.route('/api/skills')
def api_skills():
    """功法列表"""
    player = get_game('tancau')
    return jsonify({
        'success': True,
        'message': f"已学 {len(player.skills)} 种功法",
        'skills': player.skills
    })

if __name__ == '__main__':
    app.run(debug=True)
