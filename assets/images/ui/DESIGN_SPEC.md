# 设计规范

> 《蜀山剑侠传》UI 设计规范文档

---

## 📐 尺寸规范

### 按钮尺寸
| 类型 | 尺寸 | 用途 |
|------|------|------|
| 大型按钮 | 240×80 px | 开始游戏、主要操作 |
| 中型按钮 | 160×50 px | 确认、取消、通用操作 |
| 小型按钮 | 120×40 px | 返回、次要操作 |
| 功能按钮 | 100×100 px | 修炼、战斗、探索等 |
| 圆形按钮 | 60×60 px | 设置、音效、音乐等 |

### 图标尺寸
| 类型 | 尺寸 | 用途 |
|------|------|------|
| 标准图标 | 48×48 px | 状态图标、功能图标、五行图标 |
| 境界图标 | 64×64 px | 境界显示、特殊标识 |
| 操作图标 | 32×32 px | 关闭、最小化、编辑等 |

### 面板尺寸
| 类型 | 尺寸 | 用途 |
|------|------|------|
| 大型面板 | 500×600 px | 角色面板 |
| 中型面板 | 450×500 px | 技能面板、任务面板 |
| 小型面板 | 300×200 px | 提示框、对话框 |

---

## 🔤 字体规范

### 字体家族
```css
/* 标题字体 */
font-family: 'Noto Serif SC', 'Source Han Serif CN', serif;

/* 正文字体 */
font-family: 'Noto Sans SC', 'Source Han Sans CN', sans-serif;

/* 数字字体 */
font-family: 'Roboto Mono', 'Courier New', monospace;
```

### 字号规范
| 类型 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| 大标题 | 32px | 40px | 700 | 面板标题 |
| 中标题 | 24px | 32px | 600 | 项目标题 |
| 小标题 | 18px | 24px | 600 | 子项目标题 |
| 正文 | 14px | 20px | 400 | 标准正文 |
| 小字 | 12px | 16px | 400 | 辅助文字、提示 |

### 字重规范
```css
--font-weight-light: 300;     /* 轻字重 */
--font-weight-regular: 400;   /* 常规字重 */
--font-weight-medium: 500;    /* 中等字重 */
--font-weight-semibold: 600;  /* 半粗字重 */
--font-weight-bold: 700;      /* 粗字重 */
```

---

## 🎨 圆角规范

### 标准圆角
| 元素类型 | 圆角 | CSS |
|---------|------|-----|
| 按钮 | 8px | `border-radius: 8px;` |
| 面板 | 12px | `border-radius: 12px;` |
| 图标 | 4px | `border-radius: 4px;` |
| 圆形按钮 | 50% | `border-radius: 50%;` |
| 输入框 | 6px | `border-radius: 6px;` |

---

## 📏 间距规范

### 内边距 (Padding)
| 元素类型 | 内边距 | CSS |
|---------|--------|-----|
| 大型面板 | 24px | `padding: 24px;` |
| 中型面板 | 16px | `padding: 16px;` |
| 小型面板 | 12px | `padding: 12px;` |
| 按钮 | 12px 24px | `padding: 12px 24px;` |
| 输入框 | 8px 12px | `padding: 8px 12px;` |

### 外边距 (Margin)
| 元素类型 | 外边距 | CSS |
|---------|--------|-----|
| 面板间距 | 16px | `margin-bottom: 16px;` |
| 元素间距 | 8px | `margin: 8px;` |
| 紧凑间距 | 4px | `margin: 4px;` |

---

## 🖼️ 边框规范

### 标准边框
```css
/* 玄金边框 */
border: 2px solid #D4AF37;
border-radius: 8px;

/* 发光边框 */
border: 2px solid #D4AF37;
box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);

/* 内发光边框 */
border: 2px solid #D4AF37;
box-shadow: inset 0 0 10px rgba(212, 175, 55, 0.3);
```

### 边框样式
| 类型 | 宽度 | 颜色 | 用途 |
|------|------|------|------|
| 主要边框 | 2-3px | #D4AF37 | 主要元素 |
| 次要边框 | 1-2px | #BDC3C7 | 次要元素 |
| 分割线 | 1px | rgba(255, 255, 255, 0.1) | 内容分割 |

---

## 🌟 阴影规范

### 标准阴影
```css
/* 柔和阴影 */
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);

/* 强调阴影 */
box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);

/* 发光阴影 */
box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);

/* 内阴影 */
box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
```

### 阴影层级
| 层级 | 参数 | 用途 |
|------|------|------|
| Level 1 | `0 2px 4px rgba(0,0,0,0.2)` | 轻微浮起 |
| Level 2 | `0 4px 8px rgba(0,0,0,0.3)` | 标准浮起 |
| Level 3 | `0 6px 12px rgba(0,0,0,0.4)` | 明显浮起 |
| Level 4 | `0 8px 16px rgba(0,0,0,0.5)` | 高层浮起 |

---

## ✨ 动画规范

### 过渡动画
```css
/* 标准过渡 */
transition: all 0.3s ease;

/* 快速过渡 */
transition: all 0.15s ease;

/* 慢速过渡 */
transition: all 0.5s ease;
```

### 动画效果
| 状态 | 效果 | CSS |
|------|------|-----|
| 悬停 | 放大 1.05 | `transform: scale(1.05);` |
| 点击 | 缩小 0.95 | `transform: scale(0.95);` |
| 发光 | 边框发光 | `box-shadow: 0 0 20px rgba(212, 175, 55, 0.8);` |
| 渐隐 | 透明度变化 | `opacity: 0.7;` |

### 关键帧动画
```css
/* 呼吸动画 */
@keyframes breathe {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* 脉冲动画 */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* 发光动画 */
@keyframes glow {
  0%, 100% { box-shadow: 0 0 10px rgba(212, 175, 55, 0.5); }
  50% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.8); }
}
```

---

## 📱 响应式规范

### 断点
| 设备 | 宽度范围 | 用途 |
|------|---------|------|
| 移动端 | < 768px | 手机 |
| 平板 | 768px - 1024px | 平板电脑 |
| 桌面端 | > 1024px | 电脑显示器 |

### 缩放比例
```css
/* 移动端缩放 */
@media (max-width: 768px) {
  .button { transform: scale(0.9); }
  .panel { width: 95%; }
}

/* 平板缩放 */
@media (min-width: 768px) and (max-width: 1024px) {
  .button { transform: scale(0.95); }
  .panel { width: 80%; }
}
```

---

## 🎯 设计原则

### 1. 一致性
- 相同功能使用相同的视觉元素
- 保持颜色、字体、间距的一致
- 动画效果统一

### 2. 层次感
- 重要元素使用金色强调
- 次要元素使用灰色或青色
- 背景使用深色营造氛围

### 3. 文化契合
- 使用中国传统元素（云纹、莲花、龙凤）
- 颜色符合仙侠主题
- 字体选择古风风格

### 4. 易用性
- 按钮尺寸足够大，易于点击
- 文字清晰可读
- 交互反馈明显

---

## 📝 CSS 变量汇总

```css
:root {
  /* 字体 */
  --font-title: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
  --font-mono: 'Roboto Mono', monospace;

  /* 字号 */
  --font-size-lg: 32px;
  --font-size-md: 24px;
  --font-size-sm: 18px;
  --font-size-base: 14px;
  --font-size-xs: 12px;

  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 50%;

  /* 过渡 */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}
```

---

*设计规范版本：1.0*
