# meal-planner 🍳

> 一周食谱规划 + 购物清单生成技能 — 根据人数、食材、饮食偏好自动规划三餐，零浪费购物。

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Allen091080/meal-planner/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)](.)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://skills.sh)

---

## ✨ 功能特性

- 📅 **一周食谱规划** — 自动生成 5-7 天三餐计划
- 🧅 **食材推荐** — 根据冰箱现有食材推荐今天能做的菜
- 🛒 **购物清单** — 自动汇总所需食材，合并用量
- 🥦 **饮食偏好** — 支持素食、低碳水、高蛋白等模式
- 🚫 **忌口设置** — 设置不吃的食材，永远不会出现在食谱里
- 🔢 **热量统计** — 显示每餐和每日总热量

## 📋 需求

| 依赖 | 版本 |
|------|------|
| Python | 3.10+ |

内置菜谱库，无需联网，无需 API Key。

## 🚀 安装

```bash
npx skills add https://github.com/Allen091080/meal-planner -g -y
```

## 📖 使用示例

### 初始化偏好配置

```bash
python3 scripts/planner.py init
# 配置文件：~/.meal-planner/preferences.json
```

编辑 `~/.meal-planner/preferences.json` 设置你的偏好：

```json
{
  "servings": 2,
  "diet": "normal",
  "avoid": ["香菜", "榴莲"],
  "cuisine": ["中餐", "日料"],
  "budget_per_day": 80
}
```

### 生成一周食谱

```bash
python3 scripts/planner.py plan --week
```

输出示例：

```
🍽️  2026年03月14日 起 7 天食谱计划
   人数：2 人 | 饮食：normal | 忌口：香菜、榴莲
────────────────────────────────────────────────────────────

  周六 (03/14)
  早餐：燕麦粥+水煮蛋            ⏱ 15min  🔥320kcal
  午餐：番茄炒蛋盖饭              ⏱ 25min  🔥520kcal
  晚餐：清蒸鱼+青菜+米饭          ⏱ 35min  🔥520kcal
  ──────────────────────────────────────────────────
  今日总热量：约 1360 kcal

  周日 (03/15)
  早餐：豆浆油条                  ⏱ 10min  🔥450kcal
  ...
```

### 根据现有食材推荐

```bash
python3 scripts/planner.py suggest --ingredients "鸡蛋,西红柿,土豆,豆腐,猪肉"
```

```
🍳 根据你的食材推荐菜谱：鸡蛋、西红柿、土豆、豆腐、猪肉

  1. 番茄炒蛋盖饭
     ⏱ 25分钟  🔥520kcal
     ✅ 食材充足，可以直接做！

  2. 麻婆豆腐+米饭
     ⏱ 30分钟  🔥580kcal
     还需购买：大米

  3. 蒸蛋+紫菜汤+米饭
     ⏱ 25分钟  🔥420kcal
     还需购买：紫菜、大米
```

### 生成购物清单

```bash
# 文本格式
python3 scripts/planner.py shopping

# Markdown 格式（分类整理，可粘贴到备忘录）
python3 scripts/planner.py shopping --format markdown
```

Markdown 格式输出：

```markdown
# 购物清单 — 2026年03月14日

> 人数：2 人 | 涵盖 7 天

## 🥩 肉蛋类
- [ ] 猪五花（约 300g）
- [ ] 鸡胸肉（约 200g + 250g）
- [ ] 鸡蛋（约 2个 + 3个 + 1个）

## 🥦 蔬菜类
- [ ] 番茄（约 2个 + 1个）
- [ ] 青菜（约 150g + 200g）
- [ ] 西兰花（约 200g）

## 🌾 主食类
- [ ] 大米（约 150g × 7）
```

## 💬 与 AI Agent 对话

```
帮我规划这周的饭，我一个人住，不吃香菜
→ 生成单人7天食谱（自动过滤含香菜菜品）

冰箱里还有鸡蛋、豆腐、菠菜，今天能做什么？
→ 推荐3道菜，标注哪些还需要购买

给我一份购物清单，用 Markdown 格式
→ 输出分类整理的清单，可直接复制到备忘录
```

## 📁 项目结构

```
meal-planner/
├── SKILL.md              # Agent 技能定义
├── scripts/
│   └── planner.py        # 核心脚本（菜谱/购物清单/推荐）
├── README.md
├── LICENSE               # MIT
└── .github/
    └── workflows/
        └── test.yml
```

## 📄 License

MIT © 2026 [Allen091080](https://github.com/Allen091080)
