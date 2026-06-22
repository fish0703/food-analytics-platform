"""
prepare_data.py
将 for_visualization/ 中的新 CSV 数据转换为 visualization_web/data/ 中
现有 API 所需的精确格式。

来源：大众点评/美团 10,000 条爬取数据
用法：python prepare_data.py
"""
import pandas as pd
import json
import os
import io
import sys
from collections import Counter

# Windows GBK 终端中文兼容
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 路径常量
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEW_DIR = os.path.join(BASE_DIR, 'for_visualization')
OUT_DIR = os.path.join(BASE_DIR, 'visualization_web', 'data')

# 读取主数据（BOM 头 → utf-8-sig）
print("[1/11] 读取 shop_data_raw.csv (10,000 条)...")
raw = pd.read_csv(
    os.path.join(NEW_DIR, 'shop_data_raw.csv'),
    encoding='utf-8-sig',
    dtype={'点评数量': int, '人均消费(元)': float}
)

# 读取辅助预聚合文件
score_summary = pd.read_csv(os.path.join(NEW_DIR, 'score_summary.csv'), encoding='utf-8-sig')
city_food_cross = pd.read_csv(os.path.join(NEW_DIR, 'city_food_cross.csv'), encoding='utf-8-sig')
food_type_dist = pd.read_csv(os.path.join(NEW_DIR, 'food_type_distribution.csv'), encoding='utf-8-sig')
price_level = pd.read_csv(os.path.join(NEW_DIR, 'price_level.csv'), encoding='utf-8-sig')
rating_level = pd.read_csv(os.path.join(NEW_DIR, 'rating_level.csv'), encoding='utf-8-sig')

# ============================================================
#  1. overview.json  →  /api/overview
# ============================================================
print("[2/11] 生成 overview.json...")
high_value_pct = round((raw['是否高性价比'] == True).sum() / len(raw) * 100, 1)
overview = {
    "total_cities": int(raw['城市'].nunique()),
    "total_merchants": len(raw),
    "total_reviews": int(raw['点评数量'].sum()),
    "avg_cost": round(raw['人均消费(元)'].mean()),
    "total_food_types": int(raw['美食类型'].nunique()),
    "high_value_pct": high_value_pct,
    # 附加 score_summary 的统计值
    "avg_taste": round(score_summary['avg_taste'].values[0], 2),
    "avg_env": round(score_summary['avg_env'].values[0], 2),
    "avg_service": round(score_summary['avg_service'].values[0], 2),
    "avg_overall": round(score_summary['avg_overall'].values[0], 2),
    "corr_taste_overall": float(score_summary['corr_taste_overall'].values[0]),
    "corr_env_overall": float(score_summary['corr_env_overall'].values[0]),
}
with open(os.path.join(OUT_DIR, 'overview.json'), 'w', encoding='utf-8') as f:
    json.dump(overview, f, ensure_ascii=False, indent=2)
print(f"    → {overview['total_merchants']} 商家, {overview['total_reviews']} 条点评, "
      f"¥{overview['avg_cost']} 人均, {overview['high_value_pct']}% 高性价比")

# ============================================================
#  2. city_stats.csv  →  /api/city_stats
# ============================================================
print("[3/11] 生成 city_stats.csv...")
grouped = raw.groupby('城市')
city_stats_list = []
for city, grp in grouped:
    total = len(grp)
    city_stats_list.append({
        'name': city,
        'merchants': total,
        'reviews': int(grp['点评数量'].sum()),
        'avg_cost': round(grp['人均消费(元)'].mean()),
        'avg_popularity': round(grp['热门度'].mean(), 1),
        'high_value_ratio': round((grp['是否高性价比'] == True).sum() / total * 100, 1),
    })
city_stats_df = pd.DataFrame(city_stats_list)
city_stats_df.to_csv(os.path.join(OUT_DIR, 'city_stats.csv'), index=False)
for _, r in city_stats_df.iterrows():
    print(f"    {r['name']}: 商家{r['merchants']}, 点评{r['reviews']}, "
          f"人均¥{r['avg_cost']}, 高性价比{r['high_value_ratio']}%")

# ============================================================
#  3. score_matrix.json  →  /api/score_matrix
# ============================================================
print("[4/11] 生成 score_matrix.json (10,000 行)...")
# 映射为 11 元素数组：与原格式完全一致
matrix = []
for _, row in raw.iterrows():
    matrix.append([
        float(row['人均消费(元)']),       # 0: 人均消费
        float(row['口味评分']),           # 1: 评价指数(=口味评分)
        float(row['口味评分']),           # 2: 口味评分
        float(row['环境评分']),           # 3: 环境评分
        float(row['服务评分']),           # 4: 服务评分
        float(row['综合评分']),           # 5: 综合评分
        int(row['点评数量']),              # 6: 点评数量
        float(row['热门度']),              # 7: 热门度
        float(row['口碑均衡度']),          # 8: 口碑均衡度
        str(row['美食类型']),              # 9: 美食类型
        str(row['城市']),                 # 10: 城市
    ])
with open(os.path.join(OUT_DIR, 'score_matrix.json'), 'w', encoding='utf-8') as f:
    json.dump(matrix, f, ensure_ascii=False)
print(f"    → {len(matrix)} 条数据点")

# ============================================================
#  4. food_preference.json  →  /api/city_food_preference
# ============================================================
print("[5/11] 生成 food_preference.json...")
food_pref = {}
for city, grp in grouped:
    type_counts = grp['美食类型'].value_counts()
    city_total = len(grp)
    top10 = []
    for food_type, count in type_counts.head(10).items():
        top10.append({
            'type': food_type,
            'ratio': round(count / city_total * 100, 1)
        })
    food_pref[city] = top10
    print(f"    {city}: top1={top10[0]['type']}({top10[0]['ratio']}%)")
with open(os.path.join(OUT_DIR, 'food_preference.json'), 'w', encoding='utf-8') as f:
    json.dump(food_pref, f, ensure_ascii=False, indent=2)

# ============================================================
#  5. food_cost_heatmap.csv  →  /api/food_cost_heatmap
# ============================================================
print("[6/11] 生成 food_cost_heatmap.csv...")
heatmap_df = city_food_cross[['city', 'food_type', 'avg_price']].copy()
heatmap_df.columns = ['city', 'food_type', 'avg_cost']
heatmap_df['avg_cost'] = heatmap_df['avg_cost'].round(0).astype(int)
heatmap_df.to_csv(os.path.join(OUT_DIR, 'food_cost_heatmap.csv'), index=False)
print(f"    → {len(heatmap_df)} 行 (城市×美食类型)")

# ============================================================
#  6. pie_data.json  →  /api/pie_data
# ============================================================
print("[7/11] 生成 pie_data.json...")
pie_data = []
for _, row in food_type_dist.iterrows():
    pie_data.append({
        'name': row['food_type'],
        'value': int(row['count']),
        'ratio': round(float(row['pct']), 1)
    })
with open(os.path.join(OUT_DIR, 'pie_data.json'), 'w', encoding='utf-8') as f:
    json.dump(pie_data, f, ensure_ascii=False, indent=2)
print(f"    → {len(pie_data)} 种美食类型, top1={pie_data[0]['name']}({pie_data[0]['ratio']}%)")

# ============================================================
#  7. wordcloud.json  →  /api/wordcloud_data
# ============================================================
print("[8/11] 生成 wordcloud.json...")
dish_counter = Counter()
for dishes in raw['推荐菜_清洗'].dropna():
    for dish in str(dishes).split('、'):
        dish = dish.strip()
        if dish and len(dish) >= 1:
            dish_counter[dish] += 1

top60 = dish_counter.most_common(60)
max_count = top60[0][1]
wordcloud_data = []
for name, value in top60:
    wordcloud_data.append({
        'name': name,
        'value': value,
        'scaled': round(value / max_count * 100)
    })
with open(os.path.join(OUT_DIR, 'wordcloud.json'), 'w', encoding='utf-8') as f:
    json.dump(wordcloud_data, f, ensure_ascii=False, indent=2)
print(f"    → 唯一菜品 {len(dish_counter)} 个, top1='{top60[0][0]}'({top60[0][1]}次)")

# ============================================================
#  8. price_tier.json  →  /api/price_tier
# ============================================================
print("[9/11] 生成 price_tier.json...")
PRICE_ORDER = ['低消费(≤30)', '中低(31-60)', '中等(61-100)', '中高(101-200)', '高端(>200)']
price_tier = []
for _, row in price_level.iterrows():
    price_tier.append({
        'name': row['price_level'],
        'value': int(row['count'])
    })
# 按固定顺序排序
price_order_map = {v: i for i, v in enumerate(PRICE_ORDER)}
price_tier.sort(key=lambda x: price_order_map.get(x['name'], 99))
with open(os.path.join(OUT_DIR, 'price_tier.json'), 'w', encoding='utf-8') as f:
    json.dump(price_tier, f, ensure_ascii=False, indent=2)
print(f"    → {len(price_tier)} 个价格等级")

# ============================================================
#  9. rating_tier.json  →  /api/rating_tier
# ============================================================
print("[10/11] 生成 rating_tier.json...")
RATING_ORDER = ['较差(<3)', '一般(3-3.5)', '良好(3.5-4)', '优秀(4-4.5)', '卓越(≥4.5)']
rating_tier = []
for _, row in rating_level.iterrows():
    rating_tier.append({
        'name': row['rating_level'],
        'value': int(row['count'])
    })
rating_order_map = {v: i for i, v in enumerate(RATING_ORDER)}
rating_tier.sort(key=lambda x: rating_order_map.get(x['name'], 99))
with open(os.path.join(OUT_DIR, 'rating_tier.json'), 'w', encoding='utf-8') as f:
    json.dump(rating_tier, f, ensure_ascii=False, indent=2)
print(f"    → {len(rating_tier)} 个评分等级")

# ============================================================
#  10. value_for_money.json  →  /api/value_for_money
# ============================================================
print("[11/11] 生成 value_for_money.json...")
value_list = []
for city, grp in grouped:
    total = len(grp)
    hvc = int((grp['是否高性价比'] == True).sum())
    value_list.append({
        'city': city,
        'high_value_count': hvc,
        'total': total,
        'ratio': round(hvc / total * 100, 1)
    })
value_list.sort(key=lambda x: x['ratio'], reverse=True)
with open(os.path.join(OUT_DIR, 'value_for_money.json'), 'w', encoding='utf-8') as f:
    json.dump(value_list, f, ensure_ascii=False, indent=2)
for v in value_list:
    print(f"    {v['city']}: {v['high_value_count']}/{v['total']} = {v['ratio']}%")

# ============================================================
#  11. food_trend.json  →  /api/food_trend
# ============================================================
print("[11/11] 生成 food_trend.json...")
cities_order = []
bbq_ratios = []
noodle_ratios = []
for city, grp in grouped:
    total = len(grp)
    cities_order.append(city)
    bbq_ratios.append(round((grp['美食类型'] == '烧烤').sum() / total * 100, 1))
    noodle_ratios.append(round((grp['美食类型'] == '面馆').sum() / total * 100, 1))

food_trend = {
    'cities': cities_order,
    'bbq_ratio': bbq_ratios,
    'noodle_ratio': noodle_ratios
}
with open(os.path.join(OUT_DIR, 'food_trend.json'), 'w', encoding='utf-8') as f:
    json.dump(food_trend, f, ensure_ascii=False, indent=2)
for i, c in enumerate(cities_order):
    print(f"    {c}: 烧烤{bbq_ratios[i]}% 面馆{noodle_ratios[i]}%")

print("\n✓ 全部 11 个数据文件生成完成！")
print(f"  输出目录: {OUT_DIR}")
