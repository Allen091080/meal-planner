#!/usr/bin/env python3
"""
meal-planner — 一周食谱规划 + 购物清单脚本
用法: python3 planner.py plan --week
"""

import argparse
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

PREFS_FILE = Path.home() / ".meal-planner" / "preferences.json"
DEFAULT_PREFS = {
    "servings": 2,
    "diet": "normal",
    "avoid": [],
    "cuisine": ["中餐"],
    "budget_per_day": 100,
    "skill_level": "intermediate",
}

# 内置菜谱库（精简版，实际可扩展）
RECIPE_DB = {
    "中餐": {
        "breakfast": [
            {"name": "白米粥+咸蛋", "ingredients": {"大米": "100g", "咸蛋": "1个"}, "time": 20, "kcal": 280},
            {"name": "豆浆油条", "ingredients": {"豆浆": "400ml", "油条": "2根"}, "time": 10, "kcal": 450},
            {"name": "燕麦粥+水煮蛋", "ingredients": {"燕麦": "80g", "鸡蛋": "1个"}, "time": 15, "kcal": 320},
            {"name": "番茄鸡蛋面", "ingredients": {"面条": "150g", "番茄": "1个", "鸡蛋": "2个"}, "time": 20, "kcal": 420},
            {"name": "包子+豆浆", "ingredients": {"包子": "3个", "豆浆": "300ml"}, "time": 5, "kcal": 380},
        ],
        "lunch": [
            {"name": "番茄炒蛋盖饭", "ingredients": {"大米": "150g", "番茄": "2个", "鸡蛋": "3个"}, "time": 25, "kcal": 520},
            {"name": "麻婆豆腐+米饭", "ingredients": {"豆腐": "300g", "猪肉末": "50g", "大米": "150g"}, "time": 30, "kcal": 580},
            {"name": "红烧肉+白菜+米饭", "ingredients": {"猪五花": "300g", "白菜": "200g", "大米": "150g"}, "time": 60, "kcal": 750},
            {"name": "清蒸鱼+青菜+米饭", "ingredients": {"鱼": "400g", "青菜": "150g", "大米": "150g"}, "time": 35, "kcal": 520},
            {"name": "蒜蓉西兰花+鸡胸肉+米饭", "ingredients": {"西兰花": "200g", "鸡胸肉": "200g", "大米": "150g"}, "time": 30, "kcal": 480},
            {"name": "扬州炒饭", "ingredients": {"大米": "200g", "鸡蛋": "2个", "火腿": "50g", "胡萝卜": "50g"}, "time": 20, "kcal": 560},
        ],
        "dinner": [
            {"name": "蒸蛋+紫菜汤+米饭", "ingredients": {"鸡蛋": "2个", "紫菜": "10g", "大米": "150g"}, "time": 25, "kcal": 420},
            {"name": "宫保鸡丁+米饭", "ingredients": {"鸡胸肉": "250g", "花生": "50g", "大米": "150g"}, "time": 30, "kcal": 610},
            {"name": "水煮牛肉+米饭", "ingredients": {"牛肉": "300g", "青菜": "100g", "大米": "150g"}, "time": 40, "kcal": 680},
            {"name": "豆腐汤+炒青菜+米饭", "ingredients": {"豆腐": "200g", "青菜": "200g", "大米": "150g"}, "time": 25, "kcal": 450},
            {"name": "皮蛋瘦肉粥", "ingredients": {"大米": "150g", "猪肉": "100g", "皮蛋": "1个"}, "time": 45, "kcal": 480},
        ],
    },
    "日料": {
        "breakfast": [{"name": "日式味噌汤+米饭", "ingredients": {"味噌": "30g", "豆腐": "100g", "大米": "150g"}, "time": 15, "kcal": 380}],
        "lunch": [{"name": "日式炸猪排饭", "ingredients": {"猪里脊": "200g", "大米": "150g", "鸡蛋": "1个"}, "time": 35, "kcal": 680}],
        "dinner": [{"name": "日式照烧鸡腿+米饭", "ingredients": {"鸡腿": "2个", "大米": "150g"}, "time": 30, "kcal": 600}],
    },
}


def load_prefs() -> dict:
    if PREFS_FILE.exists():
        with open(PREFS_FILE) as f:
            return {**DEFAULT_PREFS, **json.load(f)}
    return DEFAULT_PREFS.copy()


def save_prefs(prefs: dict):
    PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PREFS_FILE, "w") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)


def filter_recipes(recipes: list, avoid: list) -> list:
    if not avoid:
        return recipes
    return [r for r in recipes if not any(a in r["name"] or a in str(r["ingredients"]) for a in avoid)]


def pick_meal(meal_type: str, cuisine_list: list, avoid: list) -> dict:
    candidates = []
    for cuisine in cuisine_list:
        if cuisine in RECIPE_DB:
            candidates.extend(RECIPE_DB[cuisine].get(meal_type, []))
    candidates = filter_recipes(candidates, avoid)
    if not candidates:
        return {"name": "（自由选择）", "ingredients": {}, "time": 0, "kcal": 0}
    return random.choice(candidates)


def cmd_init(args):
    prefs = load_prefs()
    save_prefs(prefs)
    print(f"✅ 配置文件已初始化：{PREFS_FILE}")
    print(f"\n当前配置：")
    for k, v in prefs.items():
        print(f"  {k}: {v}")
    print(f"\n修改配置请直接编辑：{PREFS_FILE}")


def cmd_plan(args):
    prefs = load_prefs()
    avoid = prefs["avoid"]
    cuisine = prefs.get("cuisine", ["中餐"])
    if args.diet:
        prefs["diet"] = args.diet
    if args.servings:
        prefs["servings"] = int(args.servings)

    today = date.today()
    days = 7 if args.week else 5

    print(f"\n🍽️  {today.strftime('%Y年%m月%d日')} 起 {days} 天食谱计划")
    print(f"   人数：{prefs['servings']} 人 | 饮食：{prefs['diet']} | 忌口：{'、'.join(avoid) if avoid else '无'}")
    print(f"{'─'*60}")

    plan = []
    for i in range(days):
        d = today + timedelta(days=i)
        weekday = ["周一","周二","周三","周四","周五","周六","周日"][d.weekday()]
        breakfast = pick_meal("breakfast", cuisine, avoid)
        lunch = pick_meal("lunch", cuisine, avoid)
        dinner = pick_meal("dinner", cuisine, avoid)
        day_plan = {"date": d.isoformat(), "weekday": weekday, "breakfast": breakfast, "lunch": lunch, "dinner": dinner}
        plan.append(day_plan)

        total_kcal = breakfast["kcal"] + lunch["kcal"] + dinner["kcal"]
        print(f"\n  {weekday} ({d.strftime('%m/%d')})")
        print(f"  早餐：{breakfast['name']:<20} ⏱ {breakfast['time']}min  🔥{breakfast['kcal']}kcal")
        print(f"  午餐：{lunch['name']:<20} ⏱ {lunch['time']}min  🔥{lunch['kcal']}kcal")
        print(f"  晚餐：{dinner['name']:<20} ⏱ {dinner['time']}min  🔥{dinner['kcal']}kcal")
        print(f"  {'─'*50}")
        print(f"  今日总热量：约 {total_kcal} kcal")

    # 保存计划
    plan_file = Path.home() / ".meal-planner" / "current_plan.json"
    plan_file.parent.mkdir(parents=True, exist_ok=True)
    with open(plan_file, "w") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 计划已保存，运行 'shopping' 命令生成购物清单")


def cmd_shopping(args):
    plan_file = Path.home() / ".meal-planner" / "current_plan.json"
    if not plan_file.exists():
        print("❌ 请先运行 plan 命令生成本周食谱", file=sys.stderr)
        sys.exit(1)

    with open(plan_file) as f:
        plan = json.load(f)

    prefs = load_prefs()
    servings = prefs["servings"]

    # 汇总食材
    shopping = {}
    for day in plan:
        for meal_key in ["breakfast", "lunch", "dinner"]:
            meal = day[meal_key]
            for item, qty in meal.get("ingredients", {}).items():
                if item in shopping:
                    shopping[item].append(qty)
                else:
                    shopping[item] = [qty]

    if args.format == "markdown":
        print(f"# 购物清单 — {date.today().strftime('%Y年%m月%d日')}\n")
        print(f"> 人数：{servings} 人 | 涵盖 {len(plan)} 天\n")
        categories = {
            "🥩 肉蛋类": ["猪", "牛", "鸡", "鸭", "鱼", "虾", "鸡蛋", "咸蛋", "皮蛋"],
            "🥦 蔬菜类": ["菜", "番茄", "白菜", "西兰花", "胡萝卜", "土豆", "洋葱", "蒜"],
            "🌾 主食类": ["大米", "面条", "面粉", "燕麦", "包子", "油条"],
            "🥛 豆制品": ["豆腐", "豆浆", "豆皮"],
            "🧂 调味料": ["味噌", "花生", "紫菜", "火腿"],
        }
        categorized = set()
        for cat, keywords in categories.items():
            items_in_cat = [(k, v) for k, v in shopping.items() if any(kw in k for kw in keywords)]
            if items_in_cat:
                print(f"## {cat}\n")
                for item, qtys in items_in_cat:
                    print(f"- [ ] {item}（约 {', '.join(qtys)}）")
                    categorized.add(item)
                print()
        # 其他
        others = [(k, v) for k, v in shopping.items() if k not in categorized]
        if others:
            print("## 🛒 其他\n")
            for item, qtys in others:
                print(f"- [ ] {item}（约 {', '.join(qtys)}）")
    else:
        print(f"\n🛒 购物清单（{len(plan)} 天，{servings} 人份）")
        print(f"{'─'*40}")
        for item, qtys in sorted(shopping.items()):
            print(f"  □ {item:<12} {' + '.join(qtys)}")
        print(f"{'─'*40}")
        print(f"  共 {len(shopping)} 种食材")


def cmd_suggest(args):
    ingredients = [i.strip() for i in args.ingredients.split(",")]
    print(f"\n🍳 根据你的食材推荐菜谱：{', '.join(ingredients)}\n")

    suggestions = []
    for cuisine, meal_types in RECIPE_DB.items():
        for meal_type, recipes in meal_types.items():
            for recipe in recipes:
                match_count = sum(1 for ing in recipe["ingredients"] if any(i in ing or ing in i for i in ingredients))
                if match_count > 0:
                    suggestions.append({**recipe, "match": match_count, "meal_type": meal_type})

    suggestions.sort(key=lambda x: -x["match"])
    for i, s in enumerate(suggestions[:5], 1):
        missing = [ing for ing in s["ingredients"] if not any(av in ing or ing in av for av in ingredients)]
        print(f"  {i}. {s['name']}")
        print(f"     ⏱ {s['time']}分钟  🔥{s['kcal']}kcal")
        if missing:
            print(f"     还需购买：{', '.join(missing)}")
        else:
            print(f"     ✅ 食材充足，可以直接做！")
        print()


def main():
    parser = argparse.ArgumentParser(description="一周食谱规划工具")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init", help="初始化偏好配置")

    p_plan = sub.add_parser("plan", help="生成食谱计划")
    p_plan.add_argument("--week", action="store_true", help="规划整周（7天）")
    p_plan.add_argument("--weekdays", action="store_true", help="只规划工作日（5天）")
    p_plan.add_argument("--servings", type=int, help="人数")
    p_plan.add_argument("--diet", choices=["normal","vegetarian","vegan","low-carb","high-protein","light"])

    p_shop = sub.add_parser("shopping", help="生成购物清单")
    p_shop.add_argument("--format", choices=["text","markdown","json"], default="text")

    p_sug = sub.add_parser("suggest", help="根据食材推荐菜谱")
    p_sug.add_argument("--ingredients", required=True, help="现有食材，逗号分隔")

    args = parser.parse_args()
    dispatch = {"init": cmd_init, "plan": cmd_plan, "shopping": cmd_shopping, "suggest": cmd_suggest}
    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
