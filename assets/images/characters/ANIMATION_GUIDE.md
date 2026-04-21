# 《蜀山剑侠传》角色动画素材清单

> **创建日期：** 2026-04-22  
> **版本：** v1.0  
> **目标：** 生成高质量角色动画素材

---

## 📋 目录结构

```
assets/images/characters/
├── player/              # 玩家角色动画
│   ├── idle/           # 待机动画
│   ├── attack/         # 攻击动画
│   ├── meditate/       # 打坐动画
│   └── breakthrough/   # 突破动画
├── enemies/            # 敌人动画
│   ├── lianqi/        # 练气期
│   ├── zhuji/         # 筑基期
│   ├── jindan/        # 金丹期
│   └── yuanying/      # 元婴期
└── ANIMATION_GUIDE.md  # 本文档
```

---

## 🎮 动画规格

### 通用规格
| 参数 | 值 |
|------|-----|
| **尺寸** | 64x64 像素 |
| **帧率** | 12 FPS |
| **格式** | PNG（透明背景） |
| **方向** | 右侧面（side view） |
| **调色板** | 仙侠风格，以青、白、金为主 |

### 命名规范
```
[角色]_[动画类型]_[帧序号].png
示例：player_idle_01.png, wolf_attack_05.png
```

---

## 👤 玩家角色动画

### 1. 待机动画 (Idle) - 8帧

**动作描述：** 角色站立呼吸，身体微微起伏，衣袍随风轻摆

| 帧 | 动作说明 |
|----|----------|
| 01 | 站立初始姿态，双手自然下垂 |
| 02 | 轻微吸气，上身微微上抬 |
| 03 | 呼吸中段，衣袍开始飘动 |
| 04 | 呼气开始，上身略微下沉 |
| 05 | 呼气结束，自然放松状态 |
| 06 | 微微转头，眼神扫视 |
| 07 | 转回正前方，衣袍继续飘动 |
| 08 | 回到初始姿态（与帧01相同，循环） |

**AI 提示词：**
```
Chinese male cultivator, white robes with blue embroidery, 
standing idle breathing animation, 
side view facing right, 
character sprite sheet, 
8 frames, 64x64, transparent background, 
idle pose, gentle breathing, flowing robes, 
game asset, pixel art style
```

---

### 2. 攻击动画 (Attack) - 12帧

**动作描述：** 拔剑挥砍，剑气纵横，仙家剑法

| 帧 | 动作说明 |
|----|----------|
| 01 | 准备姿态，右手按剑柄 |
| 02 | 拔剑出鞘，剑光闪现 |
| 03 | 剑出鞘，准备挥砍 |
| 04 | 开始挥剑，身体旋转蓄力 |
| 05 | 挥剑过半，剑气成形 |
| 06 | 剑斩到最高点，剑光最亮 |
| 07 | 剑势下行，剑气斩出 |
| 08 | 收剑回撤，身体前倾 |
| 09 | 剑收至身侧 |
| 10 | 准备归鞘姿态 |
| 11 | 剑归鞘动作 |
| 12 | 回到待机姿态 |

**AI 提示词：**
```
Chinese male cultivator, white robes, 
sword attack animation, drawing sword and slash, 
side view facing right, 
character sprite sheet, 
12 frames, 64x64, transparent background, 
martial arts sword strike, sword glow effect, 
game asset, pixel art style
```

---

### 3. 打坐动画 (Meditate) - 8帧

**动作描述：** 盘膝而坐，修炼吐纳，灵气环绕

| 帧 | 动作说明 |
|----|----------|
| 01 | 站立准备打坐 |
| 02 | 开始下蹲 |
| 03 | 盘膝坐下的过程 |
| 04 | 完全盘膝坐定，双手放膝 |
| 05 | 双手结印，灵气开始聚集 |
| 06 | 周身灵气环绕，闭眼冥想 |
| 07 | 灵气流转，额头有微光 |
| 08 | 深度冥想状态（循环回帧05或06） |

**AI 提示词：**
```
Chinese male cultivator, white robes, 
meditation animation, sitting cross-legged, 
side view facing right, 
character sprite sheet, 
8 frames, 64x64, transparent background, 
cultivation practice, spiritual energy aura, 
closed eyes, hand mudra, 
game asset, pixel art style
```

---

### 4. 突破动画 (Breakthrough) - 16帧

**动作描述：** 修炼突破，灵气爆发，光芒万丈

| 帧 | 动作说明 |
|----|----------|
| 01 | 打坐初始状态 |
| 02-03 | 开始聚集灵气，身体微微发光 |
| 04-05 | 灵气聚集加速，光环出现 |
| 06-07 | 能量积蓄，身体颤抖 |
| 08-09 | 突破瞬间，光芒爆发 |
| 10-11 | 光芒扩散，气场扩大 |
| 12-13 | 境界提升，能量漩涡 |
| 14-15 | 光芒逐渐收敛 |
| 16 | 新境界稳定，回到打坐状态 |

**AI 提示词：**
```
Chinese male cultivator, white robes, 
cultivation breakthrough animation, 
spiritual energy explosion, 
side view facing right, 
character sprite sheet, 
16 frames, 64x64, transparent background, 
transcendence moment, golden light aura, 
energy vortex, divine glow, 
game asset, pixel art style
```

---

## 👹 敌人角色动画

### 练气期敌人

#### 1. 妖狼 (Spirit Wolf)
**动画：** 待机 + 攻击 + 移动

**AI 提示词：**
```
Spirit wolf demon, dark grey fur with glowing red eyes, 
idle animation, side view facing right, 
character sprite sheet, 
8 frames, 64x64, transparent background, 
feral wolf pose, mystical energy aura, 
game asset, pixel art style
```

#### 2. 妖蛇 (Demon Snake)
**动画：** 待机 + 攻击 + 移动

**AI 提示词：**
```
Demon snake, emerald green scales with golden patterns, 
idle animation coiled, side view facing right, 
character sprite sheet, 
8 frames, 64x64, transparent background, 
serpentine movement, poison aura, 
game asset, pixel art style
```

#### 3. 妖虎 (Demonic Tiger)
**动画：** 待机 + 攻击 + 移动

**AI 提示词：**
```
Demonic tiger, black fur with orange stripes, 
roaring attack animation, side view facing right, 
character sprite sheet, 
12 frames, 64x64, transparent background, 
fierce tiger pounce, dark energy claws, 
game asset, pixel art style
```

---

### 筑基期敌人

#### 1. 妖将 (Demon General)
**动画：** 待机 + 攻击 + 移动 + 特殊技能

**AI 提示词：**
```
Demon general, dark armor with bone decorations, 
commanding stance, side view facing right, 
character sprite sheet, 
12 frames, 64x64, transparent background, 
intimidating posture, demonic weapon, 
aura of authority, 
game asset, pixel art style
```

#### 2. 魔修 (Evil Cultivator)
**动画：** 待机 + 攻击 + 施法

**AI 提示词：**
```
Evil cultivator, black robes with blood red trim, 
dark magic casting animation, side view facing right, 
character sprite sheet, 
12 frames, 64x64, transparent background, 
forbidden technique, dark qi manipulation, 
malevolent aura, 
game asset, pixel art style
```

---

### 金丹期敌人

#### 1. 妖王 (Demon King)
**动画：** 待机 + 攻击 + 技能 + 召唤

**AI 提示词：**
```
Demon king, towering figure with obsidian skin, 
throne room pose, side view facing right, 
character sprite sheet, 
16 frames, 64x64, transparent background, 
majestic and terrifying, demonic crown, 
dark flames aura, 
game asset, pixel art style
```

#### 2. 魔尊 (Demon Lord)
**动画：** 待机 + 攻击 + 技能 + 禁术

**AI 提示词：**
```
Demon lord, twisted humanoid with multiple arms, 
ancient forbidden power, side view facing right, 
character sprite sheet, 
16 frames, 64x64, transparent background, 
eldritch energy, void magic, 
reality distortion, 
game asset, pixel art style
```

---

### 元婴期敌人

#### 远古凶兽 (Ancient Beast)
**动画：** 待机 + 攻击 + 技能 + 愤怒模式

**AI 提示词：**
```
Ancient primordial beast, massive creature, 
elemental fury, side view facing right, 
character sprite sheet, 
16 frames, 64x64, transparent background, 
primordial power, elemental aura, 
apocalyptic presence, 
game asset, pixel art style
```

---

## 🛠️ AI 动画生成工具推荐

### 一、专业级工具

#### 1. **Pika Labs** ⭐⭐⭐⭐⭐
- **网址：** https://pika.art/
- **特点：** 
  - 优秀的动作连贯性
  - 支持文字转视频
  - 风格一致性好
- **适用：** 玩家角色动画
- **费用：** 免费试用 + 付费订阅

#### 2. **RunwayML Gen-3** ⭐⭐⭐⭐⭐
- **网址：** https://runwayml.com/
- **特点：**
  - 专业级质量
  - 精准控制动画
  - 帧级别编辑
- **适用：** 复杂动画（突破、技能）
- **费用：** 付费订阅

#### 3. **Midjourney + AnimateDiff** ⭐⭐⭐⭐
- **网址：** https://midjourney.com/
- **特点：**
  - 顶级画质
  - 艺术风格多样
  - 需配合动画工具
- **适用：** 关键帧生成
- **费用：** 付费订阅

---

### 二、免费/开源工具

#### 4. **Stable Diffusion + AnimateDiff** ⭐⭐⭐⭐
- **网址：** https://github.com/guoyww/AnimateDiff
- **特点：**
  - 完全免费
  - 本地运行
  - 高度自定义
- **适用：** 所有动画类型
- **费用：** 免费（需GPU）

#### 5. **Leonardo.AI** ⭐⭐⭐⭐
- **网址：** https://leonardo.ai/
- **特点：**
  - 免费额度充足
  - 游戏资产生成
  - 支持动画
- **适用：** 敌人角色
- **费用：** 免费套餐 + 付费

#### 6. **Krea AI** ⭐⭐⭐
- **网址：** https://www.krea.ai/
- **特点：**
  - 实时生成
  - 快速迭代
- **适用：** 快速原型
- **费用：** 免费试用

---

### 三、像素艺术专用

#### 7. **Aseprite** ⭐⭐⭐⭐⭐
- **网址：** https://www.aseprite.org/
- **特点：**
  - 专业像素编辑
  - 动画时间轴
  - 导出精灵表
- **适用：** 手动调整/优化
- **费用：** $20（一次性购买）

#### 8. **Pixelorama** ⭐⭐⭐⭐
- **网址：** https://orama-interactive.itch.io/pixelorama
- **特点：**
  - 免费开源
  - 功能完整
  - 支持精灵表
- **适用：** 手动调整
- **费用：** 免费

---

## 📝 推荐工作流

### 最佳实践流程

```
1. 概念设计
   ↓ 使用 Midjourney 生成关键帧概念图
   
2. AI 动画生成
   ↓ 使用 Pika Labs 或 RunwayML 生成动画帧
   
3. 帧提取
   ↓ 导出为单帧图片
   
4. 优化调整
   ↓ 使用 Aseprite 调整尺寸、透明背景
   
5. 格式转换
   ↓ 导出 64x64 PNG 序列
   
6. 测试集成
   ↓ 在游戏中测试动画效果
```

---

## 🎯 提示词优化技巧

### 提高一致性
```
✅ 好的提示词：
"Chinese male cultivator, white robes, 
sword attack, 12 frames animation, 
side view, character sprite sheet, 
64x64, transparent background, 
consistent character design, game asset"

❌ 避免：
"man with sword fighting" （太模糊）
```

### 常用修饰词
- **风格：** pixel art, game asset, sprite sheet
- **背景：** transparent background, no background
- **视角：** side view, right-facing, profile
- **动作：** smooth animation, fluid motion
- **质量：** high quality, detailed, consistent

### 负面提示词
```
blurry, low quality, inconsistent, 
background elements, watermark, 
text, signature, 3D render, realistic photo
```

---

## 📊 生成清单统计

### 玩家角色
| 动画类型 | 帧数 | 提示词状态 |
|---------|------|-----------|
| 待机 | 8 | ✅ 已完成 |
| 攻击 | 12 | ✅ 已完成 |
| 打坐 | 8 | ✅ 已完成 |
| 突破 | 16 | ✅ 已完成 |
| **小计** | **44** | - |

### 敌人角色
| 境界 | 敌人类型 | 每类帧数 | 提示词状态 |
|------|---------|---------|-----------|
| 练气期 | 3 种 | 28 | ✅ 已完成 |
| 筑基期 | 2 种 | 36 | ✅ 已完成 |
| 金丹期 | 2 种 | 48 | ✅ 已完成 |
| 元婴期 | 1 种 | 16 | ✅ 已完成 |
| **小计** | **8 种** | **128** | - |

### 总计
- **动画类型：** 12 种
- **总帧数：** 172 帧
- **预计工时：** 
  - AI 生成：2-3 小时
  - 手动优化：4-6 小时
  - 测试调整：1-2 小时

---

## 🔄 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-04-22 | v1.0 | 初始版本，完成所有提示词和清单 |

---

## 📌 下一步行动

1. **使用 Midjourney 生成关键帧概念图**
2. **使用 Pika Labs 生成玩家角色动画**
3. **使用 Leonardo.AI 生成敌人动画**
4. **使用 Aseprite 优化所有帧**
5. **集成到游戏引擎测试**

---

*文档维护者：初初 💎*  
*最后更新：2026-04-22*
