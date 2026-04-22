#!/usr/bin/env python3
"""
蜀山剑侠传 UI元素生成器
生成SVG格式的按钮和图标素材
"""

import os
from pathlib import Path

# 配色方案
COLORS = {
    '玄金色': '#D4AF37',
    '仙韵青': '#4ECDC4',
    '剑魄紫': '#9B59B6',
    '修真绿': '#27AE60',
    '真元蓝': '#3498DB',
    '灵石橙': '#E67E22',
    '云雾灰': '#2C3E50',
    '幽暗黑': '#1A1A2E',
    '古卷褐': '#3D2914',
    '剑鞘深蓝': '#16213E',
    # 状态色
    '正常绿': '#27AE60',
    '警告橙': '#F39C12',
    '危险红': '#E74C3C',
    '冷却灰': '#95A5A6',
}

# 输出目录
BASE_DIR = Path.home() / '.openclaw' / 'workspace' / 'shushan-game' / 'frontend' / 'public' / 'assets' / 'images' / 'ui'
BUTTONS_DIR = BASE_DIR / 'buttons'
ICONS_DIR = BASE_DIR / 'icons'

def create_dir(path: Path):
    """创建目录"""
    path.mkdir(parents=True, exist_ok=True)

def generate_button(name: str, width: int, height: int, color: str, text: str, icon_svg: str = "") -> str:
    """生成按钮SVG"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#3D2914;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1A1A2E;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="50%" style="stop-color:#FFD700;stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color};stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- 背景 -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="8" ry="8" fill="url(#bg)" stroke="url(#border)" stroke-width="2"/>
  
  <!-- 内部装饰边框 -->
  <rect x="6" y="6" width="{width-12}" height="{height-12}" rx="6" ry="6" fill="none" stroke="{color}" stroke-width="1" opacity="0.5"/>
  
  <!-- 图标 -->
  <g transform="translate({width//2 - 12 if not text else 12}, {height//2 - 12})">
    {icon_svg}
  </g>
  
  <!-- 文字 -->
  {f'<text x="{width//2 + 12 if icon_svg else width//2}" y="{height//2 + 5}" text-anchor="middle" fill="{color}" font-family="Noto Serif SC, serif" font-size="14" font-weight="bold" filter="url(#glow)">{text}</text>' if text else ''}
</svg>'''

def generate_icon(name: str, size: int, color: str, icon_svg: str) -> str:
    """生成图标SVG"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <defs>
    <linearGradient id="iconGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FFD700;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- 背景 -->
  <circle cx="{size//2}" cy="{size//2}" r="{size//2 - 2}" fill="#1A1A2E" stroke="url(#iconGrad)" stroke-width="2"/>
  
  <!-- 图标内容 -->
  <g transform="translate({size//4}, {size//4}) scale(0.5)">
    {icon_svg}
  </g>
</svg>'''

def generate_status_icon(name: str, size: int, color: str, icon_svg: str) -> str:
    """生成状态图标SVG（更简洁的设计）"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- 图标内容 -->
  <g filter="url(#glow)">
    {icon_svg}
  </g>
</svg>'''

# ==================== 按钮图标定义 ====================

BUTTON_ICONS = {
    # 主按钮
    'start': '''<polygon points="24,8 24,40 52,24" fill="{color}"/>''',
    'confirm': '''<path d="M8,24 L20,36 L40,12" stroke="{color}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>''',
    'cancel': '''<path d="M12,12 L36,36 M36,12 L12,36" stroke="{color}" stroke-width="4" fill="none" stroke-linecap="round"/>''',
    'save': '''<rect x="8" y="8" width="32" height="36" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M14,8 L14,18 L34,18 L34,8" fill="none" stroke="{color}" stroke-width="2"/><line x1="14" y1="32" x2="34" y2="32" stroke="{color}" stroke-width="2"/>''',
    'back': '''<path d="M32,8 L16,24 L32,40" stroke="{color}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>''',
    'continue': '''<polygon points="8,8 8,40 32,24" fill="{color}"/><polygon points="28,8 28,40 52,24" fill="{color}"/>''',
    
    # 功能按钮
    'cultivate': '''<circle cx="24" cy="24" r="16" fill="none" stroke="{color}" stroke-width="2"/><circle cx="24" cy="24" r="8" fill="none" stroke="{color}" stroke-width="2"/><circle cx="24" cy="24" r="3" fill="{color}"/>''',
    'battle': '''<path d="M8,32 L24,16 L28,20 L12,36 Z" fill="{color}"/><path d="M40,32 L24,16 L20,20 L36,36 Z" fill="{color}"/>''',
    'explore': '''<circle cx="24" cy="24" r="16" fill="none" stroke="{color}" stroke-width="2"/><path d="M24,8 L24,12 M24,36 L24,40 M8,24 L12,24 M36,24 L40,24" stroke="{color}" stroke-width="2"/><polygon points="24,16 28,28 20,28" fill="{color}"/>''',
    'inventory': '''<rect x="8" y="12" width="32" height="28" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M16,12 L16,8 C16,4 32,4 32,8 L32,12" fill="none" stroke="{color}" stroke-width="2"/>''',
    'skills': '''<rect x="8" y="8" width="32" height="32" rx="2" fill="none" stroke="{color}" stroke-width="2"/><line x1="8" y1="18" x2="40" y2="18" stroke="{color}" stroke-width="1"/><line x1="8" y1="28" x2="40" y2="28" stroke="{color}" stroke-width="1"/>''',
    'quest': '''<rect x="12" y="8" width="24" height="32" rx="2" fill="none" stroke="{color}" stroke-width="2"/><circle cx="32" cy="12" r="4" fill="{color}"/>''',
    'shop': '''<circle cx="24" cy="20" r="12" fill="none" stroke="{color}" stroke-width="2"/><circle cx="18" cy="20" r="2" fill="{color}"/><circle cx="30" cy="20" r="2" fill="{color}"/><path d="M16,32 C16,28 32,28 32,32" stroke="{color}" stroke-width="2" fill="none"/>''',
    'craft': '''<ellipse cx="24" cy="24" rx="14" ry="10" fill="none" stroke="{color}" stroke-width="2"/><ellipse cx="24" cy="20" rx="10" ry="6" fill="none" stroke="{color}" stroke-width="1"/><path d="M24,30 L24,38" stroke="{color}" stroke-width="2"/>''',
    
    # 状态按钮
    'settings': '''<circle cx="24" cy="24" r="8" fill="none" stroke="{color}" stroke-width="2"/><path d="M24,4 L24,12 M24,36 L24,44 M4,24 L12,24 M36,24 L44,24 M10,10 L16,16 M32,32 L38,38 M10,38 L16,32 M32,16 L38,10" stroke="{color}" stroke-width="2"/>''',
    'sound_on': '''<path d="M8,18 L8,30 L16,30 L28,40 L28,8 L16,18 Z" fill="{color}"/><path d="M32,16 C36,20 36,28 32,32" stroke="{color}" stroke-width="2" fill="none"/>''',
    'sound_off': '''<path d="M8,18 L8,30 L16,30 L28,40 L28,8 L16,18 Z" fill="{color}"/><path d="M32,16 L40,32 M40,16 L32,32" stroke="{color}" stroke-width="2"/>''',
    'music_on': '''<path d="M8,18 L8,30 L16,30 L28,40 L28,8 L16,18 Z" fill="{color}"/><path d="M32,12 C40,16 40,32 32,36" stroke="{color}" stroke-width="2" fill="none"/><path d="M36,16 C42,20 42,28 36,32" stroke="{color}" stroke-width="2" fill="none"/>''',
    'fullscreen': '''<path d="M8,12 L8,8 L16,8 M32,8 L40,8 L40,16 M40,32 L40,40 L32,40 M16,40 L8,40 L8,32" stroke="{color}" stroke-width="3" fill="none"/>''',
    'help': '''<circle cx="24" cy="24" r="18" fill="none" stroke="{color}" stroke-width="2"/><path d="M16,18 C16,12 32,12 32,18 C32,24 24,24 24,30" stroke="{color}" stroke-width="2" fill="none"/><circle cx="24" cy="36" r="2" fill="{color}"/>''',
    'leaderboard': '''<rect x="8" y="24" width="12" height="16" fill="{color}" opacity="0.6"/><rect x="20" y="12" width="12" height="28" fill="{color}" opacity="0.8"/><rect x="32" y="18" width="12" height="22" fill="{color}"/>''',
}

# ==================== 图标定义 ====================

STATUS_ICONS = {
    # 状态图标
    'health': ('''<path d="M24,8 C16,8 8,16 8,24 C8,36 24,44 24,44 C24,44 40,36 40,24 C40,16 32,8 24,8 Z" fill="{color}"/>''', COLORS['正常绿']),
    'mana': ('''<polygon points="24,4 28,16 40,16 32,24 36,40 24,32 12,40 16,24 8,16 20,16" fill="{color}"/>''', COLORS['真元蓝']),
    'cultivation_points': ('''<circle cx="24" cy="24" r="16" fill="none" stroke="{color}" stroke-width="2"/><path d="M24,12 L26,20 L24,28 L22,20 Z" fill="{color}"/><circle cx="24" cy="24" r="4" fill="{color}"/>''', COLORS['玄金色']),
    'spirit_stones': ('''<polygon points="24,4 40,16 40,32 24,44 8,32 8,16" fill="{color}"/>''', COLORS['灵石橙']),
    'experience': ('''<rect x="8" y="12" width="32" height="24" rx="2" fill="none" stroke="{color}" stroke-width="2"/><line x1="12" y1="20" x2="36" y2="20" stroke="{color}" stroke-width="1"/><line x1="12" y1="28" x2="28" y2="28" stroke="{color}" stroke-width="1"/>''', COLORS['玄金色']),
    'attack': ('''<path d="M8,36 L24,12 L28,16 L12,40 Z" fill="{color}"/><path d="M40,36 L24,12 L20,16 L36,40 Z" fill="{color}" opacity="0.7"/>''', COLORS['危险红']),
    'defense': ('''<path d="M24,4 L40,12 L40,28 C40,36 24,44 24,44 C24,44 8,36 8,28 L8,12 Z" fill="none" stroke="{color}" stroke-width="3"/>''', COLORS['仙韵青']),
    'speed': ('''<path d="M8,24 C8,16 16,12 24,12 L40,12" stroke="{color}" stroke-width="3" fill="none"/><path d="M32,4 L40,12 L32,20" stroke="{color}" stroke-width="3" fill="none"/>''', COLORS['仙韵青']),
    'critical': ('''<polygon points="24,4 28,18 40,18 30,28 34,42 24,32 14,42 18,28 8,18 20,18" fill="{color}"/>''', COLORS['警告橙']),
    'dodge': ('''<circle cx="24" cy="24" r="12" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="4,2"/><path d="M12,24 Q24,16 36,24" stroke="{color}" stroke-width="2" fill="none"/>''', COLORS['剑魄紫']),
}

FUNCTIONAL_ICONS = {
    # 功能图标
    'map': ('''<rect x="8" y="12" width="32" height="24" rx="2" fill="none" stroke="{color}" stroke-width="2"/><circle cx="24" cy="24" r="4" fill="{color}"/><path d="M20,16 L28,16 M16,20 L32,20" stroke="{color}" stroke-width="1"/>''', COLORS['仙韵青']),
    'quest': ('''<rect x="10" y="6" width="28" height="36" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M16,18 L32,18 M16,26 L28,26 M16,34 L24,34" stroke="{color}" stroke-width="2"/><circle cx="34" cy="10" r="4" fill="{color}"/>''', COLORS['玄金色']),
    'achievement': ('''<circle cx="24" cy="20" r="12" fill="none" stroke="{color}" stroke-width="2"/><path d="M24,10 L26,16 L32,16 L28,20 L30,26 L24,22 L18,26 L20,20 L16,16 L22,16 Z" fill="{color}"/>''', COLORS['玄金色']),
    'friends': ('''<circle cx="16" cy="20" r="6" fill="none" stroke="{color}" stroke-width="2"/><circle cx="32" cy="20" r="6" fill="none" stroke="{color}" stroke-width="2"/><path d="M6,36 C6,28 16,28 16,36 M32,36 C32,28 42,28 42,36" stroke="{color}" stroke-width="2" fill="none"/>''', COLORS['仙韵青']),
    'mail': ('''<rect x="8" y="12" width="32" height="24" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M8,14 L24,26 L40,14" stroke="{color}" stroke-width="2" fill="none"/>''', COLORS['真元蓝']),
    'announcement': ('''<path d="M12,16 L12,32 C12,36 16,36 16,32 L16,16 Z" fill="{color}"/><path d="M16,16 L40,8 L40,40 L16,32" fill="none" stroke="{color}" stroke-width="2"/>''', COLORS['玄金色']),
    'calendar': ('''<rect x="8" y="12" width="32" height="28" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M8,20 L40,20" stroke="{color}" stroke-width="2"/><path d="M14,8 L14,14 M26,8 L26,14 M34,8 L34,14" stroke="{color}" stroke-width="2"/>''', COLORS['仙韵青']),
    'checkin': ('''<circle cx="24" cy="24" r="16" fill="none" stroke="{color}" stroke-width="2"/><path d="M14,24 L22,32 L36,16" stroke="{color}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>''', COLORS['修真绿']),
    'recharge': ('''<circle cx="24" cy="24" r="16" fill="none" stroke="{color}" stroke-width="2"/><text x="24" y="30" text-anchor="middle" fill="{color}" font-size="16" font-weight="bold">$</text>''', COLORS['灵石橙']),
    'support': ('''<circle cx="24" cy="24" r="16" fill="none" stroke="{color}" stroke-width="2"/><path d="M16,26 C16,20 20,18 24,18 C28,18 32,20 32,26" stroke="{color}" stroke-width="2" fill="none"/><circle cx="24" cy="14" r="4" fill="{color}"/>''', COLORS['仙韵青']),
    'feedback': ('''<rect x="8" y="10" width="32" height="24" rx="4" fill="none" stroke="{color}" stroke-width="2"/><path d="M16,38 L24,34 L32,38 L32,34 L16,34 Z" fill="{color}"/>''', COLORS['真元蓝']),
    'share': ('''<circle cx="16" cy="12" r="6" fill="none" stroke="{color}" stroke-width="2"/><circle cx="32" cy="12" r="6" fill="none" stroke="{color}" stroke-width="2"/><circle cx="24" cy="32" r="6" fill="none" stroke="{color}" stroke-width="2"/><line x1="20" y1="14" x2="22" y2="28" stroke="{color}" stroke-width="2"/><line x1="28" y1="14" x2="26" y2="28" stroke="{color}" stroke-width="2"/>''', COLORS['仙韵青']),
}

ELEMENT_ICONS = {
    # 五行图标
    'metal': ('''<polygon points="24,8 40,20 36,40 12,40 8,20" fill="none" stroke="{color}" stroke-width="2"/><path d="M24,16 L24,36 M16,24 L32,24" stroke="{color}" stroke-width="2"/>''', '#FFFFFF'),
    'wood': ('''<path d="M24,8 L24,40" stroke="{color}" stroke-width="3"/><path d="M16,16 L24,24 L32,16" stroke="{color}" stroke-width="2" fill="none"/><path d="M12,26 L24,32 L36,26" stroke="{color}" stroke-width="2" fill="none"/><circle cx="24" cy="12" r="4" fill="{color}"/>''', COLORS['修真绿']),
    'water': ('''<path d="M8,20 Q24,8 40,20 Q24,32 40,44 Q24,32 8,44 Q24,32 8,20" stroke="{color}" stroke-width="2" fill="none"/>''', COLORS['真元蓝']),
    'fire': ('''<path d="M24,40 C12,32 8,20 16,12 C16,20 24,20 24,12 C24,20 32,20 32,12 C40,20 36,32 24,40 Z" fill="{color}"/>''', COLORS['危险红']),
    'earth': ('''<polygon points="24,8 40,20 40,36 24,44 8,36 8,20" fill="none" stroke="{color}" stroke-width="2"/><line x1="24" y1="8" x2="24" y2="44" stroke="{color}" stroke-width="1"/><line x1="8" y1="20" x2="40" y2="20" stroke="{color}" stroke-width="1"/>''', '#F4D03F'),
}

REALM_ICONS = {
    # 境界图标
    'qi_refining': ('''<circle cx="24" cy="24" r="16" fill="none" stroke="{color}" stroke-width="2"/><path d="M24,12 L24,36" stroke="{color}" stroke-width="1"/><path d="M16,24 Q24,16 32,24" stroke="{color}" stroke-width="1" fill="none"/>''', '#FFFFFF'),
    'foundation': ('''<rect x="12" y="16" width="24" height="24" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M16,16 L24,8 L32,16" stroke="{color}" stroke-width="2" fill="none"/>''', '#A9CCE3'),
    'golden_core': ('''<circle cx="24" cy="24" r="12" fill="none" stroke="{color}" stroke-width="3"/><circle cx="24" cy="24" r="6" fill="{color}"/>''', COLORS['玄金色']),
    'nascent_soul': ('''<ellipse cx="24" cy="28" rx="12" ry="8" fill="none" stroke="{color}" stroke-width="2"/><circle cx="24" cy="20" r="8" fill="none" stroke="{color}" stroke-width="2"/><circle cx="22" cy="18" r="2" fill="{color}"/><circle cx="26" cy="18" r="2" fill="{color}"/>''', '#D7BDE2'),
    'soul_formation': ('''<path d="M24,8 L28,20 L40,20 L32,28 L36,40 L24,32 L12,40 L16,28 L8,20 L20,20 Z" fill="none" stroke="{color}" stroke-width="2"/>''', COLORS['剑魄紫']),
    'body_integration': ('''<circle cx="24" cy="24" r="16" fill="none" stroke="{color}" stroke-width="2"/><path d="M24,8 A16,16 0 0,1 24,40 A16,16 0 0,1 24,8" fill="{color}" opacity="0.3"/>''', '#85C1E9'),
    'mahayana': ('''<circle cx="24" cy="24" r="18" fill="none" stroke="{color}" stroke-width="2"/><polygon points="24,6 26,12 24,10 22,12" fill="{color}"/><polygon points="42,24 36,26 38,24 36,22" fill="{color}"/><polygon points="24,42 22,36 24,38 26,36" fill="{color}"/><polygon points="6,24 12,22 10,24 12,26" fill="{color}"/>''', COLORS['玄金色']),
}

OPERATION_ICONS = {
    # 操作图标
    'close': ('''<path d="M8,8 L40,40 M40,8 L8,40" stroke="{color}" stroke-width="4" stroke-linecap="round"/>''', COLORS['危险红']),
    'minimize': ('''<line x1="8" y1="24" x2="40" y2="24" stroke="{color}" stroke-width="4" stroke-linecap="round"/>''', COLORS['仙韵青']),
    'maximize': ('''<rect x="8" y="8" width="32" height="32" rx="2" fill="none" stroke="{color}" stroke-width="3"/>''', COLORS['仙韵青']),
    'refresh': ('''<path d="M36,24 A12,12 0 1,1 24,12" stroke="{color}" stroke-width="3" fill="none"/><polygon points="24,4 28,12 24,10 20,12" fill="{color}"/>''', COLORS['仙韵青']),
    'search': ('''<circle cx="20" cy="20" r="12" fill="none" stroke="{color}" stroke-width="3"/><line x1="30" y1="30" x2="40" y2="40" stroke="{color}" stroke-width="3" stroke-linecap="round"/>''', COLORS['仙韵青']),
    'filter': ('''<path d="M8,8 L40,8 L28,24 L28,40 L20,40 L20,24 Z" fill="none" stroke="{color}" stroke-width="2"/>''', COLORS['仙韵青']),
    'sort': ('''<path d="M12,12 L24,4 L36,12" stroke="{color}" stroke-width="2" fill="none"/><path d="M12,36 L24,44 L36,36" stroke="{color}" stroke-width="2" fill="none"/><line x1="24" y1="4" x2="24" y2="44" stroke="{color}" stroke-width="2"/>''', COLORS['仙韵青']),
    'lock': ('''<rect x="10" y="20" width="28" height="20" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M16,20 L16,14 C16,8 32,8 32,14 L32,20" stroke="{color}" stroke-width="2" fill="none"/>''', COLORS['玄金色']),
    'unlock': ('''<rect x="10" y="20" width="28" height="20" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M16,20 L16,14 C16,8 32,8 32,14" stroke="{color}" stroke-width="2" fill="none"/>''', COLORS['仙韵青']),
    'edit': ('''<path d="M8,40 L12,28 L36,4 L44,12 L20,36 Z" fill="none" stroke="{color}" stroke-width="2"/><line x1="32" y1="8" x2="40" y2="16" stroke="{color}" stroke-width="2"/>''', COLORS['仙韵青']),
    'delete': ('''<path d="M12,12 L12,44 L36,44 L36,12" fill="none" stroke="{color}" stroke-width="2"/><path d="M8,12 L40,12" stroke="{color}" stroke-width="2"/><path d="M20,8 L20,4 L28,4 L28,8" stroke="{color}" stroke-width="2" fill="none"/><line x1="20" y1="20" x2="20" y2="36" stroke="{color}" stroke-width="1"/><line x1="28" y1="20" x2="28" y2="36" stroke="{color}" stroke-width="1"/>''', COLORS['危险红']),
    'copy': ('''<rect x="12" y="12" width="24" height="32" rx="2" fill="none" stroke="{color}" stroke-width="2"/><rect x="8" y="8" width="24" height="32" rx="2" fill="none" stroke="{color}" stroke-width="2" opacity="0.5"/>''', COLORS['仙韵青']),
    'paste': ('''<rect x="10" y="12" width="28" height="32" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M18,8 L26,8 L28,12 L16,12 Z" fill="{color}"/>''', COLORS['仙韵青']),
    'undo': ('''<path d="M16,24 L8,16 L16,8" stroke="{color}" stroke-width="3" fill="none"/><path d="M8,16 C8,16 16,16 24,24 C32,32 40,32 40,32" stroke="{color}" stroke-width="2" fill="none"/>''', COLORS['仙韵青']),
    'redo': ('''<path d="M32,24 L40,16 L32,8" stroke="{color}" stroke-width="3" fill="none"/><path d="M40,16 C40,16 32,16 24,24 C16,32 8,32 8,32" stroke="{color}" stroke-width="2" fill="none"/>''', COLORS['仙韵青']),
    'save': ('''<rect x="8" y="8" width="32" height="32" rx="2" fill="none" stroke="{color}" stroke-width="2"/><path d="M14,8 L14,18 L34,18 L34,8" fill="none" stroke="{color}" stroke-width="2"/><line x1="14" y1="28" x2="34" y2="28" stroke="{color}" stroke-width="2"/>''', COLORS['仙韵青']),
}

def generate_all_buttons():
    """生成所有按钮"""
    buttons = [
        # 主按钮 (name, width, height, text, icon_key)
        ('start', 240, 80, '开始游戏', 'start'),
        ('confirm', 160, 50, '确认', 'confirm'),
        ('cancel', 160, 50, '取消', 'cancel'),
        ('save', 160, 50, '保存', 'save'),
        ('back', 120, 40, '返回', 'back'),
        ('continue', 160, 50, '继续', 'continue'),
        
        # 功能按钮
        ('cultivate', 100, 100, '修炼', 'cultivate'),
        ('battle', 100, 100, '战斗', 'battle'),
        ('explore', 100, 100, '探索', 'explore'),
        ('inventory', 100, 100, '背包', 'inventory'),
        ('skills', 100, 100, '功法', 'skills'),
        ('artifact', 100, 100, '法宝', 'craft'),
        ('spirit_beast', 100, 100, '灵兽', 'quest'),
        ('settings', 100, 100, '设置', 'settings'),
        
        # 状态按钮
        ('sound_on', 60, 60, '', 'sound_on'),
        ('sound_off', 60, 60, '', 'sound_off'),
        ('music_on', 60, 60, '', 'music_on'),
        ('music_off', 60, 60, '', 'sound_off'),
        ('vibration_on', 60, 60, '', 'settings'),
        ('vibration_off', 60, 60, '', 'settings'),
        ('notification_on', 60, 60, '', 'quest'),
        ('notification_off', 60, 60, '', 'quest'),
        ('pause', 60, 60, '', 'settings'),
        ('help', 60, 60, '', 'help'),
    ]
    
    create_dir(BUTTONS_DIR)
    
    for name, width, height, text, icon_key in buttons:
        color = COLORS['玄金色']
        icon_svg = BUTTON_ICONS.get(icon_key, '').format(color=color)
        svg_content = generate_button(name, width, height, color, text, icon_svg)
        
        filepath = BUTTONS_DIR / f'{name}.svg'
        filepath.write_text(svg_content, encoding='utf-8')
        print(f'✓ 生成按钮: {name}')

def generate_all_icons():
    """生成所有图标"""
    create_dir(ICONS_DIR)
    
    # 状态图标
    for name, (icon_svg, color) in STATUS_ICONS.items():
        svg_content = generate_status_icon(name, 48, color, icon_svg.format(color=color))
        filepath = ICONS_DIR / f'{name}.svg'
        filepath.write_text(svg_content, encoding='utf-8')
        print(f'✓ 生成状态图标: {name}')
    
    # 功能图标
    for name, (icon_svg, color) in FUNCTIONAL_ICONS.items():
        svg_content = generate_status_icon(name, 48, color, icon_svg.format(color=color))
        filepath = ICONS_DIR / f'{name}.svg'
        filepath.write_text(svg_content, encoding='utf-8')
        print(f'✓ 生成功能图标: {name}')
    
    # 五行图标
    for name, (icon_svg, color) in ELEMENT_ICONS.items():
        svg_content = generate_status_icon(name, 48, color, icon_svg.format(color=color))
        filepath = ICONS_DIR / f'element_{name}.svg'
        filepath.write_text(svg_content, encoding='utf-8')
        print(f'✓ 生成五行图标: {name}')
    
    # 境界图标
    for name, (icon_svg, color) in REALM_ICONS.items():
        svg_content = generate_status_icon(name, 64, color, icon_svg.format(color=color))
        filepath = ICONS_DIR / f'realm_{name}.svg'
        filepath.write_text(svg_content, encoding='utf-8')
        print(f'✓ 生成境界图标: {name}')
    
    # 操作图标
    for name, (icon_svg, color) in OPERATION_ICONS.items():
        svg_content = generate_status_icon(name, 32, color, icon_svg.format(color=color))
        filepath = ICONS_DIR / f'op_{name}.svg'
        filepath.write_text(svg_content, encoding='utf-8')
        print(f'✓ 生成操作图标: {name}')

def main():
    """主函数"""
    print('='*50)
    print('蜀山剑侠传 UI元素生成器')
    print('='*50)
    
    print('\n生成按钮素材...')
    generate_all_buttons()
    
    print('\n生成图标素材...')
    generate_all_icons()
    
    print('\n' + '='*50)
    print('生成完成!')
    print(f'按钮目录: {BUTTONS_DIR}')
    print(f'图标目录: {ICONS_DIR}')
    print('='*50)

if __name__ == '__main__':
    main()
