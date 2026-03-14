---
name: meal-planner
description: 根据食材、人数、饮食偏好生成一周食谱计划，自动生成购物清单，支持中西餐，无需 API Key。
version: "1.0.0"
metadata: {"openclaw": {"os": ["darwin", "linux", "win32"], "emoji": "🍳", "user-invocable": true, "homepage": "https://github.com/Allen091080/meal-planner", "tags": ["life", "food", "health", "planning"]}}
---

# 一周食谱规划 + 购物清单

根据你的食材库存、人数、口味偏好，生成一周三餐计划，并自动汇总购物清单，避免重复购买和食材浪费。

## 适用场景

| 场景 | 用这个？ |
|------|---------|
| 规划一周三餐 | ✅ 是 |
| 根据现有食材推荐菜谱 | ✅ 是 |
| 生成购物清单（含用量） | ✅ 是 |
| 设置饮食偏好/禁忌 | ✅ 是 |
| 营养均衡分析 | ✅ 是 |
| 单道菜谱查询 | ✅ 是 |
| 外卖/餐厅推荐 | ❌ 否 |

## 配置文件

偏好配置存储在 `~/.meal-planner/preferences.json`：

```json
{
  "servings": 2,
  "diet": "normal",
  "avoid": ["香菜", "榴莲"],
  "cuisine": ["中餐", "日料"],
  "budget_per_day": 80,
  "skill_level": "intermediate"
}
```

### 饮食类型（diet）

- `normal`：无限制
- `vegetarian`：素食
- `vegan`：纯素
- `low-carb`：低碳水
- `high-protein`：高蛋白（健身）
- `light`：清淡（适合肠胃不好）

## 如何使用

### 1. 初始化偏好

```bash
python3 {baseDir}/scripts/planner.py init
```

### 2. 生成一周食谱

```bash
# 默认配置生成本周食谱
python3 {baseDir}/scripts/planner.py plan --week

# 指定人数和饮食偏好
python3 {baseDir}/scripts/planner.py plan --week --servings 4 --diet vegetarian

# 只规划工作日（周一到周五）
python3 {baseDir}/scripts/planner.py plan --weekdays --servings 2
```

### 3. 根据现有食材推荐

```bash
# 告诉系统冰箱里有什么
python3 {baseDir}/scripts/planner.py suggest --ingredients "鸡蛋,西红柿,土豆,猪肉,豆腐"

# 输出：推荐今天能做的菜，并说明需要补充的食材
```

### 4. 生成购物清单

```bash
# 基于本周食谱生成购物清单
python3 {baseDir}/scripts/planner.py shopping

# 导出为 Markdown 格式（可粘贴到备忘录）
python3 {baseDir}/scripts/planner.py shopping --format markdown

# 导出为 JSON（方便二次处理）
python3 {baseDir}/scripts/planner.py shopping --format json
```

### 5. 营养分析

```bash
# 分析今日三餐营养
python3 {baseDir}/scripts/planner.py nutrition --today

# 分析本周营养均衡情况
python3 {baseDir}/scripts/planner.py nutrition --week
```

## 与 AI Agent 对话示例

```
用户：帮我规划这周的饭，我一个人住，不吃香菜
Agent：好的，为你生成本周（3/14-3/20）单人食谱：

周一：早餐-燕麦粥+水煮蛋 | 午餐-番茄炒蛋盖饭 | 晚餐-清蒸鱼+青菜
周二：早餐-三明治 | 午餐-麻婆豆腐+米饭 | 晚餐-蒸蛋+紫菜汤
...
[附购物清单]

用户：冰箱里还有鸡蛋、豆腐、菠菜，能做什么？
Agent：[运行 suggest，推荐 3 道菜]

用户：帮我把购物清单发给我
Agent：[输出 Markdown 格式清单]
```

## 重要规则

1. **生成食谱时考虑季节性食材**，优先推荐当季蔬菜
2. **购物清单自动合并相同食材用量**，避免重复
3. **营养分析基于中国居民膳食指南标准**
4. **输出格式要清晰易读**，用表格或分组列表展示
5. **尊重饮食禁忌**，avoid 列表中的食材绝不出现在食谱里
