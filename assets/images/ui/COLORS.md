# 配色方案

> 《蜀山剑侠传》UI 配色规范

---

## 🎨 主色调

### 玄金色 (Mystic Gold)
```css
/* 主要边框、强调元素 */
--gold-primary: #D4AF37;
--gold-light: #F1C40F;
--gold-dark: #B8860B;
```
- HEX: `#D4AF37`
- RGB: `rgb(212, 175, 55)`
- 用途：主要边框、按钮、强调文字、稀有物品

### 仙韵青 (Immortal Cyan)
```css
/* 次要元素、链接、特殊效果 */
--cyan-primary: #4ECDC4;
--cyan-light: #76D7C4;
--cyan-dark: #1ABC9C;
```
- HEX: `#4ECDC4`
- RGB: `rgb(78, 205, 196)`
- 用途：次要元素、链接、特效、冰属性

### 剑魄紫 (Sword Soul Purple)
```css
/* 特殊/稀有元素 */
--purple-primary: #9B59B6;
--purple-light: #BB8FCE;
--purple-dark: #7D3C98;
```
- HEX: `#9B59B6`
- RGB: `rgb(155, 89, 182)`
- 用途：特殊物品、稀有装备、雷属性

### 修真绿 (Cultivation Green)
```css
/* 生命、成功状态 */
--green-primary: #27AE60;
--green-light: #2ECC71;
--green-dark: #1E8449;
```
- HEX: `#27AE60`
- RGB: `rgb(39, 174, 96)`
- 用途：生命条、成功提示、木属性

### 真元蓝 (True Essence Blue)
```css
/* 真元、魔法值 */
--blue-primary: #3498DB;
--blue-light: #5DADE2;
--blue-dark: #2E86C1;
```
- HEX: `#3498DB`
- RGB: `rgb(52, 152, 219)`
- 用途：真元条、魔法值、水属性

### 灵石橙 (Spirit Stone Orange)
```css
/* 灵石、货币 */
--orange-primary: #E67E22;
--orange-light: #F39C12;
--orange-dark: #D35400;
```
- HEX: `#E67E22`
- RGB: `rgb(230, 126, 34)`
- 用途：灵石、货币、土属性、经验条

---

## 🌑 背景色

### 云雾灰 (Cloud Mist Gray)
```css
/* 主背景 */
--bg-primary: #2C3E50;
--bg-secondary: #34495E;
--bg-tertiary: #5D6D7E;
```
- HEX: `#2C3E50`
- RGB: `rgb(44, 62, 80)`
- 用途：主背景、面板背景

### 幽暗黑 (Dark Void)
```css
/* 深色背景、对话框 */
--black-primary: #1A1A2E;
--black-secondary: #16213E;
--black-tertiary: #0F0F1A;
```
- HEX: `#1A1A2E`
- RGB: `rgb(26, 26, 46)`
- 用途：深色背景、夜间模式、对话框

### 古卷褐 (Ancient Scroll Brown)
```css
/* 古风面板、书卷 */
--brown-primary: #3D2914;
--brown-light: #5D4037;
--brown-dark: #2C1810;
```
- HEX: `#3D2914`
- RGB: `rgb(61, 41, 20)`
- 用途：古风面板、书卷、木质元素

### 剑鞘深蓝 (Sheath Blue)
```css
/* 技能面板、深邃元素 */
--deepblue-primary: #16213E;
--deepblue-light: #1A237E;
--deepblue-dark: #0D1B3D;
```
- HEX: `#16213E`
- RGB: `rgb(22, 33, 62)`
- 用途：技能面板、深邃元素、神秘感

---

## ⚡ 状态色

### 正常状态 (Normal)
```css
--status-normal: #27AE60;
--status-normal-light: #2ECC71;
```
- HEX: `#27AE60`
- 用途：生命充足、正常状态、成功提示

### 警告状态 (Warning)
```css
--status-warning: #F39C12;
--status-warning-light: #F4D03F;
```
- HEX: `#F39C12`
- 用途：生命中等、警告提示、注意力

### 危险状态 (Danger)
```css
--status-danger: #E74C3C;
--status-danger-light: #EC7063;
```
- HEX: `#E74C3C`
- 用途：生命低、错误提示、火属性

### 冷却状态 (Cooldown)
```css
--status-cooldown: #95A5A6;
--status-cooldown-light: #BDC3C7;
```
- HEX: `#95A5A6`
- RGB: `rgb(149, 165, 166)`
- 用途：技能冷却、禁用状态、不可用

---

## 🔥 五行配色

### 金 (Metal)
```css
--metal-primary: #BDC3C7;
--metal-accent: #ECF0F1;
--metal-glow: rgba(255, 255, 255, 0.5);
```
- 主色: `#BDC3C7`
- 光效: 白色光晕

### 木 (Wood)
```css
--wood-primary: #27AE60;
--wood-accent: #2ECC71;
--wood-glow: rgba(39, 174, 96, 0.5);
```
- 主色: `#27AE60`
- 光效: 绿色光晕

### 水 (Water)
```css
--water-primary: #3498DB;
--water-accent: #5DADE2;
--water-glow: rgba(52, 152, 219, 0.5);
```
- 主色: `#3498DB`
- 光效: 蓝色光晕

### 火 (Fire)
```css
--fire-primary: #E74C3C;
--fire-accent: #EC7063;
--fire-glow: rgba(231, 76, 60, 0.5);
```
- 主色: `#E74C3C`
- 光效: 红色光晕

### 土 (Earth)
```css
--earth-primary: #E67E22;
--earth-accent: #F39C12;
--earth-glow: rgba(230, 126, 34, 0.5);
```
- 主色: `#E67E22`
- 光效: 橙色光晕

---

## 🌟 境界配色

| 境界 | 主色 | HEX | 描述 |
|------|------|-----|------|
| 炼气期 | 青白 | #BDC3C7 | 基础、纯净 |
| 筑基期 | 翠绿 | #27AE60 | 生机、成长 |
| 金丹期 | 金黄 | #D4AF37 | 金光、圆润 |
| 元婴期 | 紫色 | #9B59B6 | 神秘、灵动 |
| 化神期 | 深蓝 | #3498DB | 深邃、强大 |
| 合体期 | 七彩 | 渐变 | 多元、融合 |
| 大乘期 | 金白 | #F1C40F + #FFFFFF | 至高、超凡 |

---

## 🎨 渐变配色

### 生命条渐变
```css
background: linear-gradient(90deg, #27AE60 0%, #2ECC71 100%);
```

### 真元条渐变
```css
background: linear-gradient(90deg, #3498DB 0%, #5DADE2 100%);
```

### 经验条渐变
```css
background: linear-gradient(90deg, #F39C12 0%, #F1C40F 100%);
```

### 金色边框渐变
```css
border: 2px solid;
border-image: linear-gradient(135deg, #D4AF37 0%, #F1C40F 50%, #D4AF37 100%) 1;
```

### 神秘紫渐变
```css
background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%);
```

---

## 📐 透明度规范

```css
/* 常用透明度 */
--opacity-full: 1;
--opacity-high: 0.9;
--opacity-medium: 0.7;
--opacity-low: 0.5;
--opacity-minimal: 0.3;

/* 背景透明 */
--bg-transparent: rgba(44, 62, 80, 0.9);
--panel-transparent: rgba(26, 26, 46, 0.85);
--modal-transparent: rgba(0, 0, 0, 0.7);
```

---

## 🔤 文字配色

### 标题文字
```css
--text-title-primary: #D4AF37; /* 金色标题 */
--text-title-secondary: #F1C40F; /* 浅金标题 */
--text-title-dark: #B8860B; /* 深金标题 */
```

### 正文文字
```css
--text-body-primary: #FFFFFF; /* 白色正文 */
--text-body-secondary: #BDC3C7; /* 灰色正文 */
--text-body-muted: #95A5A6; /* 淡灰正文 */
```

### 特殊文字
```css
--text-link: #4ECDC4; /* 链接文字 */
--text-highlight: #F39C12; /* 高亮文字 */
--text-warning: #E74C3C; /* 警告文字 */
```

---

## 🎨 CSS 变量完整清单

```css
:root {
  /* 主色调 */
  --color-gold: #D4AF37;
  --color-cyan: #4ECDC4;
  --color-purple: #9B59B6;
  --color-green: #27AE60;
  --color-blue: #3498DB;
  --color-orange: #E67E22;

  /* 背景色 */
  --bg-primary: #2C3E50;
  --bg-dark: #1A1A2E;
  --bg-brown: #3D2914;
  --bg-deepblue: #16213E;

  /* 状态色 */
  --status-normal: #27AE60;
  --status-warning: #F39C12;
  --status-danger: #E74C3C;
  --status-cooldown: #95A5A6;

  /* 文字色 */
  --text-title: #D4AF37;
  --text-body: #FFFFFF;
  --text-secondary: #BDC3C7;
  --text-link: #4ECDC4;
}
```

---

## 📝 使用建议

1. **主次分明**：金色为主强调，青色为次强调
2. **对比度**：确保文字与背景对比度 ≥ 4.5:1
3. **一致性**：相同功能使用相同颜色
4. **文化契合**：颜色符合中国古风仙侠主题

---

*配色版本：1.0*
