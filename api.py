#!/usr/bin/env python3
"""
蜀山剑侠传 - Web API (完整版)
用于 Vercel 部署
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import sys
import os
import json
from pathlib import Path

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.player import Player
from game.artifact import ArtifactManager
from game.skills import SkillManager
from game.world import WorldMap, ExplorationSystem
from game.quest import QuestManager
from game.crafting import CraftingManager, Inventory
from game.formation import FormationManager
from game.encounter import EncounterManager

app = Flask(__name__)
CORS(app)

# 全局游戏实例
games = {}

def get_game(player_id):
    """获取或创建游戏实例"""
    if player_id not in games:
        games[player_id] = Player.load() or Player(player_id)
    return games[player_id]

# HTML 模板 - 完整界面
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>蜀山剑侠传</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
        }
        .header {
            background: rgba(0,0,0,0.3);
            padding: 15px;
            text-align: center;
            border-bottom: 2px solid #ffd700;
        }
        h1 { 
            color: #ffd700;
            font-size: 2em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .tabs {
            display: flex;
            background: rgba(0,0,0,0.2);
            overflow-x: auto;
            border-bottom: 1px solid #4a4a6a;
        }
        .tab {
            padding: 12px 20px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            white-space: nowrap;
            transition: all 0.3s;
        }
        .tab:hover { background: rgba(255,255,255,0.1); }
        .tab.active { 
            border-bottom-color: #ffd700;
            color: #ffd700;
        }
        .content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .panel { display: none; }
        .panel.active { display: block; }
        
        /* 状态卡片 */
        .status-card {
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
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
        }
        .status-item {
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 5px;
        }
        .status-label { color: #888; font-size: 0.85em; }
        .status-value { font-size: 1.1em; color: #4fc3f7; margin-top: 3px; }
        
        /* 按钮 */
        .btn-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        button {
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 0.95em;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-success {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }
        .btn-danger {
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            color: white;
        }
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: #e0e0e0;
            border: 1px solid #4a4a6a;
        }
        button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        /* 日志 */
        .log-box {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            max-height: 300px;
            overflow-y: auto;
        }
        .log-title { color: #ffd700; margin-bottom: 10px; font-weight: bold; }
        .log-item { 
            padding: 8px;
            margin: 5px 0;
            background: rgba(255,255,255,0.05);
            border-radius: 5px;
            border-left: 3px solid #4fc3f7;
        }
        .log-item.success { border-left-color: #38ef7d; }
        .log-item.error { border-left-color: #f45c43; }
        .log-item.warning { border-left-color: #ffd700; }
        
        /* 列表 */
        .list-item {
            background: rgba(255,255,255,0.05);
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border: 1px solid #4a4a6a;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .list-item:hover {
            background: rgba(255,255,255,0.1);
        }
        .item-name { font-weight: bold; color: #ffd700; }
        .item-desc { font-size: 0.85em; color: #888; margin-top: 3px; }
        .item-stats { font-size: 0.9em; color: #4fc3f7; }
        
        /* 进度条 */
        .progress-bar {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin: 5px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s;
        }
        
        /* 地图 */
        .map-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        .location-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid #4a4a6a;
            border-radius: 8px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .location-card:hover {
            background: rgba(255,255,255,0.1);
            transform: translateY(-2px);
        }
        .location-card.current {
            border-color: #ffd700;
            background: rgba(255,215,0,0.1);
        }
        .location-name { font-weight: bold; color: #ffd700; }
        .location-region { font-size: 0.85em; color: #888; margin-top: 3px; }
        .location-danger { font-size: 0.85em; color: #f45c43; margin-top: 3px; }
        
        @media (max-width: 768px) {
            .status-grid { grid-template-columns: repeat(2, 1fr); }
            .btn-grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚔️ 蜀山剑侠传</h1>
    </div>
    
    <div class="tabs">
        <div class="tab active" onclick="showPanel('status')">角色</div>
        <div class="tab" onclick="showPanel('cultivate')">修炼</div>
        <div class="tab" onclick="showPanel('explore')">探索</div>
        <div class="tab" onclick="showPanel('battle')">战斗</div>
        <div class="tab" onclick="showPanel('quest')">任务</div>
        <div class="tab" onclick="showPanel('inventory')">背包</div>
        <div class="tab" onclick="showPanel('skills')">功法</div>
        <div class="tab" onclick="showPanel('formation')">阵法</div>
    </div>
    
    <div class="content">
        <!-- 角色面板 -->
        <div id="status" class="panel active">
            <div class="status-card">
                <div class="status-title">
                    <span id="player-name">加载中...</span>
                    <span id="player-sect" style="font-size:0.8em;color:#888;"></span>
                </div>
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
                    <div class="status-item">
                        <div class="status-label">灵石</div>
                        <div class="status-value" id="spirit-stones">-</div>
                    </div>
                    <div class="status-item">
                        <div class="status-label">位置</div>
                        <div class="status-value" id="location">-</div>
                    </div>
                </div>
            </div>
            
            <div class="status-card">
                <div class="status-title">装备法宝</div>
                <div id="equipped-artifact">无</div>
            </div>
            
            <div class="log-box">
                <div class="log-title">消息日志</div>
                <div id="log"></div>
            </div>
        </div>
        
        <!-- 修炼面板 -->
        <div id="cultivate" class="panel">
            <div class="status-card">
                <div class="status-title">修炼</div>
                <div class="btn-grid">
                    <button class="btn-primary" onclick="doAction('cultivate')">打坐修炼</button>
                    <button class="btn-success" onclick="doAction('advance')">突破境界</button>
                </div>
            </div>
            
            <div class="status-card">
                <div class="status-title">炼丹</div>
                <div id="pills-list">加载中...</div>
            </div>
            
            <div class="status-card">
                <div class="status-title">炼器</div>
                <div id="forge-list">加载中...</div>
            </div>
        </div>
        
        <!-- 探索面板 -->
        <div id="explore" class="panel">
            <div class="status-card">
                <div class="status-title">当前位置: <span id="current-location">-</span></div>
                <div class="btn-grid">
                    <button class="btn-primary" onclick="doAction('explore')">探索</button>
                    <button class="btn-secondary" onclick="loadMap()">查看地图</button>
                </div>
            </div>
            
            <div id="map-container"></div>
        </div>
        
        <!-- 战斗面板 -->
        <div id="battle" class="panel">
            <div class="status-card">
                <div class="status-title">战斗</div>
                <div class="btn-grid">
                    <button class="btn-danger" onclick="doAction('battle')">寻找敌人</button>
                </div>
            </div>
            
            <div class="status-card">
                <div class="status-title">阵法</div>
                <div id="formations-list">加载中...</div>
            </div>
        </div>
        
        <!-- 任务面板 -->
        <div id="quest" class="panel">
            <div class="status-card">
                <div class="status-title">进行中的任务</div>
                <div id="active-quests">加载中...</div>
            </div>
        </div>
        
        <!-- 背包面板 -->
        <div id="inventory" class="panel">
            <div class="status-card">
                <div class="status-title">法宝 (<span id="artifact-count">0</span>)</div>
                <div id="artifacts-list">加载中...</div>
            </div>
            
            <div class="status-card">
                <div class="status-title">材料</div>
                <div id="materials-list">加载中...</div>
            </div>
        </div>
        
        <!-- 功法面板 -->
        <div id="skills" class="panel">
            <div class="status-card">
                <div class="status-title">已学功法</div>
                <div id="skills-list">加载中...</div>
            </div>
        </div>
        
        <!-- 阵法面板 -->
        <div id="formation" class="panel">
            <div class="status-card">
                <div class="status-title">已学阵法</div>
                <div id="player-formations">加载中...</div>
            </div>
        </div>
    </div>
    
    <script>
        const PLAYER_ID = 'tancau';
        
        function showPanel(panelId) {
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById(panelId).classList.add('active');
            event.target.classList.add('active');
            
            // 加载面板数据
            if (panelId === 'inventory') loadInventory();
            if (panelId === 'skills') loadSkills();
            if (panelId === 'quest') loadQuests();
            if (panelId === 'formation') loadFormations();
        }
        
        async function fetchAPI(action) {
            try {
                const response = await fetch('/api/' + action);
                return await response.json();
            } catch (e) {
                return { error: e.message };
            }
        }
        
        async function postAPI(action, data) {
            try {
                const response = await fetch('/api/' + action, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                return await response.json();
            } catch (e) {
                return { error: e.message };
            }
        }
        
        async function updateStatus() {
            const data = await fetchAPI('status');
            if (data.success) {
                document.getElementById('player-name').textContent = data.name;
                document.getElementById('player-sect').textContent = data.sect;
                document.getElementById('realm').textContent = data.realm;
                document.getElementById('cultivation').textContent = data.cultivation;
                document.getElementById('hp').textContent = data.hp;
                document.getElementById('mp').textContent = data.mp;
                document.getElementById('spirit-stones').textContent = data.spirit_stones;
                document.getElementById('location').textContent = data.location;
                document.getElementById('current-location').textContent = data.location;
                document.getElementById('equipped-artifact').textContent = data.equipped_artifact || '无';
            }
        }
        
        function addLog(message, type = '') {
            const log = document.getElementById('log');
            const item = document.createElement('div');
            item.className = 'log-item ' + type;
            item.textContent = message;
            log.insertBefore(item, log.firstChild);
            if (log.children.length > 20) log.removeChild(log.lastChild);
        }
        
        async function doAction(action) {
            const data = await fetchAPI(action);
            if (data.message) {
                addLog(data.message, data.success ? 'success' : 'error');
            }
            if (data.success !== false) {
                await updateStatus();
            }
        }
        
        async function loadInventory() {
            const data = await fetchAPI('artifacts');
            const list = document.getElementById('artifacts-list');
            document.getElementById('artifact-count').textContent = data.artifacts?.length || 0;
            
            if (data.artifacts && data.artifacts.length > 0) {
                list.innerHTML = data.artifacts.map(a => `
                    <div class="list-item">
                        <div>
                            <div class="item-name">${a.name}</div>
                            <div class="item-desc">${a.description || ''}</div>
                        </div>
                        <div class="item-stats">威力: ${a.power}</div>
                    </div>
                `).join('');
            } else {
                list.innerHTML = '<div style="color:#888;padding:10px;">暂无法宝</div>';
            }
        }
        
        async function loadSkills() {
            const data = await fetchAPI('skills');
            const list = document.getElementById('skills-list');
            
            if (data.skills && data.skills.length > 0) {
                list.innerHTML = data.skills.map(s => `
                    <div class="list-item">
                        <div>
                            <div class="item-name">${s.name || s}</div>
                            <div class="item-desc">${s.type || ''} - ${s.quality || ''}</div>
                        </div>
                    </div>
                `).join('');
            } else {
                list.innerHTML = '<div style="color:#888;padding:10px;">尚未学习功法</div>';
            }
        }
        
        async function loadQuests() {
            const data = await fetchAPI('quests');
            const list = document.getElementById('active-quests');
            
            if (data.quests && data.quests.length > 0) {
                list.innerHTML = data.quests.map(q => `
                    <div class="list-item">
                        <div>
                            <div class="item-name">${q.name}</div>
                            <div class="item-desc">${q.description || ''}</div>
                        </div>
                        <div class="item-stats">${q.type || ''}</div>
                    </div>
                `).join('');
            } else {
                list.innerHTML = '<div style="color:#888;padding:10px;">暂无进行中的任务</div>';
            }
        }
        
        async function loadFormations() {
            const list = document.getElementById('player-formations');
            list.innerHTML = '<div style="color:#888;padding:10px;">前往战斗面板查看和使用阵法</div>';
        }
        
        async function loadMap() {
            const data = await fetchAPI('map');
            const container = document.getElementById('map-container');
            
            if (data.locations) {
                container.innerHTML = '<div class="map-grid">' + 
                    data.locations.slice(0, 12).map(loc => `
                        <div class="location-card ${loc.current ? 'current' : ''}" 
                             onclick="travel('${loc.name}')">
                            <div class="location-name">${loc.name}</div>
                            <div class="location-region">${loc.region || ''}</div>
                            ${loc.danger ? `<div class="location-danger">危险: ${loc.danger}</div>` : ''}
                        </div>
                    `).join('') + 
                '</div>';
            }
        }
        
        async function travel(location) {
            const data = await postAPI('travel', { location: location });
            if (data.message) {
                addLog(data.message, data.success ? 'success' : 'error');
            }
            await updateStatus();
            await loadMap();
        }
        
        // 初始化
        updateStatus();
        addLog('欢迎来到蜀山世界...', 'warning');
    </script>
</body>
</html>
"""

# API 路由
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
        'spirit_stones': f"{player.spirit_stones:,}",
        'sect': player.sect or '散修',
        'location': player.location,
        'equipped_artifact': player.equipped_artifact['name'] if player.equipped_artifact else None
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
    
    messages = []
    turn = 0
    while turn < 10:
        turn += 1
        attack = combat.player_attack()
        messages.append(f"[回合{turn}] {attack['message']}")
        
        winner = combat.check_victory()
        if winner == 'player':
            rewards = combat.get_rewards()
            player.cultivation += rewards['cultivation']
            player.spirit_stones += rewards['spirit_stones']
            if rewards['artifact']:
                player.add_artifact(rewards['artifact'].to_dict())
            player.current_hp = player.max_hp
            player.save()
            return jsonify({
                'success': True,
                'message': f"战斗胜利！修为 +{rewards['cultivation']}，灵石 +{rewards['spirit_stones']}"
            })
        
        enemy_atk = combat.enemy_attack()
        messages.append(f"敌方反击：{enemy_atk['damage']} 伤害")
        
        if player.current_hp <= 0:
            player.current_hp = 1
            player.save()
            return jsonify({
                'success': False,
                'message': '战斗失败，勉强逃脱！'
            })
    
    return jsonify({'success': True, 'message': '战斗超时，平局收场'})

@app.route('/api/explore')
def api_explore():
    """探索"""
    player = get_game('tancau')
    
    try:
        from game.world import ExplorationSystem
        exploration = ExplorationSystem(player)
        event = exploration.explore()
        
        message = f"探索事件: {event.get('type', '未知')}"
        if event.get('description'):
            message += f" - {event['description']}"
        
        player.save()
        return jsonify({
            'success': True,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': True,
            'message': f"在{player.location}探索了一番，没有发现特别的东西"
        })

@app.route('/api/artifacts')
def api_artifacts():
    """法宝列表"""
    player = get_game('tancau')
    return jsonify({
        'success': True,
        'artifacts': player.artifacts or []
    })

@app.route('/api/skills')
def api_skills():
    """功法列表"""
    player = get_game('tancau')
    return jsonify({
        'success': True,
        'skills': player.skills if hasattr(player, 'skills') else []
    })

@app.route('/api/quests')
def api_quests():
    """任务列表"""
    player = get_game('tancau')
    
    # 简化返回
    return jsonify({
        'success': True,
        'quests': []
    })

@app.route('/api/map')
def api_map():
    """地图"""
    try:
        from game.world import WorldMap
        world = WorldMap()
        
        locations = []
        for region in ['中原', '南疆', '北海', '西域', '东海']:
            locs = world.get_locations_by_region(region)
            for loc in locs[:5]:
                locations.append({
                    'name': loc.name,
                    'region': region,
                    'danger': getattr(loc, 'danger_level', 0)
                })
        
        return jsonify({
            'success': True,
            'locations': locations
        })
    except Exception as e:
        return jsonify({
            'success': True,
            'locations': [
                {'name': '峨眉山', 'region': '中原'},
                {'name': '青城山', 'region': '中原'},
                {'name': '昆仑山', 'region': '中原'},
                {'name': '成都府', 'region': '中原'},
                {'name': '苗疆', 'region': '南疆'},
            ]
        })

@app.route('/api/travel', methods=['POST'])
def api_travel():
    """移动"""
    player = get_game('tancau')
    data = request.get_json()
    location = data.get('location')
    
    if location:
        player.location = location
        player.save()
        return jsonify({
            'success': True,
            'message': f'已到达 {location}'
        })
    
    return jsonify({
        'success': False,
        'message': '无效的位置'
    })

if __name__ == '__main__':
    app.run(debug=True)
