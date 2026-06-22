"""一次性生成所有需要的CSV数据文件 — 适配 cleaned_restaurants.csv (19列)"""
import pandas as pd
import json
from collections import Counter
import re

df = pd.read_csv('../cleaned_restaurants.csv')

# ============ 0. 数据校验 ============
print(f'[INFO] 总记录: {len(df)}, 列数: {len(df.columns)}')
print(f'[INFO] 城市数: {df["城市"].nunique()}, 美食类型数: {df["美食类型"].nunique()}')

# ============ 1. 城市统计 (增加热门度均值) ============
city_group = df.groupby('城市')
city_stats = []
for city, grp in city_group:
    city_stats.append({
        'name': city,
        'merchants': int(len(grp)),
        'reviews': int(grp['点评数量'].sum()),
        'avg_cost': round(grp['人均消费(元)'].mean()),
        'avg_popularity': round(grp['热门度'].mean(), 1),
        'high_value_ratio': round(grp['是否高性价比'].sum() / len(grp) * 100, 1),
    })
pd.DataFrame(city_stats).to_csv('data/city_stats.csv', index=False, encoding='utf-8-sig')
print(f'[OK] city_stats.csv: {len(city_stats)} cities (+热门度/高性价比比)')

# ============ 2. 美食偏好 ============
food_pref = {}
for city, grp in city_group:
    total = len(grp)
    type_counts = grp['美食类型'].value_counts()
    top10 = [{'type': t, 'ratio': round(int(c)/total*100, 1)}
             for t, c in type_counts.head(10).items()]
    food_pref[city] = top10
with open('data/food_preference.json', 'w', encoding='utf-8') as f:
    json.dump(food_pref, f, ensure_ascii=False)
print(f'[OK] food_preference.json: {len(food_pref)} cities')

# ============ 3. 热力图数据 ============
food_types_list = df['美食类型'].value_counts().head(12).index.tolist()
heatmap_data = []
for c in df['城市'].unique():
    for ft in food_types_list:
        subset = df[(df['城市'] == c) & (df['美食类型'] == ft)]
        if len(subset) > 0:
            avg_cost = round(subset['人均消费(元)'].mean())
            heatmap_data.append([c, ft, avg_cost])
pd.DataFrame(heatmap_data, columns=['city', 'food_type', 'avg_cost']).to_csv(
    'data/food_cost_heatmap.csv', index=False, encoding='utf-8-sig')
print(f'[OK] food_cost_heatmap.csv: {len(heatmap_data)} rows')

# ============ 4. 散点图数据 (增加服务评分/热门度/口碑均衡度) ============
sample = df.sample(n=min(2000, len(df)), random_state=42)
scatter_data = []
for _, row in sample.iterrows():
    scatter_data.append([
        int(row['人均消费(元)']),
        float(row['口味评分']),
        float(row['口味评分']),
        float(row['环境评分']),
        float(row['服务评分']),
        float(row['综合评分']),
        int(row['点评数量']),
        float(row['热门度']),
        float(row['口碑均衡度']),
        row['美食类型'],
        row['城市']
    ])
with open('data/score_matrix.json', 'w', encoding='utf-8') as f:
    json.dump(scatter_data, f, ensure_ascii=False)
print(f'[OK] score_matrix.json: {len(scatter_data)} points (含服务/热门度/口碑均衡度)')

# ============ 5. 趋势页: 烧烤vs面馆 ============
total_by_city = df.groupby('城市').size()
bbq_by_city = df[df['美食类型'] == '烧烤'].groupby('城市').size()
noodle_by_city = df[df['美食类型'] == '面馆'].groupby('城市').size()

trend_data = {'cities': [], 'bbq_ratio': [], 'noodle_ratio': []}
for c in df['城市'].unique():
    total = int(total_by_city[c])
    bbq = int(bbq_by_city.get(c, 0))
    noodle = int(noodle_by_city.get(c, 0))
    trend_data['cities'].append(c)
    trend_data['bbq_ratio'].append(round(bbq/total*100, 1))
    trend_data['noodle_ratio'].append(round(noodle/total*100, 1))
n_cities = len(trend_data['cities'])
with open('data/food_trend.json', 'w', encoding='utf-8') as f:
    json.dump(trend_data, f, ensure_ascii=False)
print(f'[OK] food_trend.json: {n_cities} cities')

# ============ 6. 饼图数据 ============
food_counts = df['美食类型'].value_counts().to_dict()
total_all = int(len(df))
pie_data = [{'name': k, 'value': int(v), 'ratio': round(v/total_all*100, 1)}
            for k, v in food_counts.items()]
with open('data/pie_data.json', 'w', encoding='utf-8') as f:
    json.dump(pie_data, f, ensure_ascii=False)
print(f'[OK] pie_data.json: {len(pie_data)} types')

# ============ 7. 词云数据 (使用推荐菜_清洗) ============
dish_words = []
for dishes in df['推荐菜_清洗'].dropna():
    items = re.split(r'[//、,，\s]+', str(dishes))
    for item in items:
        item = item.strip().strip('"').strip()
        if 2 <= len(item) <= 6 and not item.isdigit():
            dish_words.append(item)
counter = Counter(dish_words)
top60 = counter.most_common(60)
max_count = top60[0][1]
wordcloud_data = [{'name': w, 'value': int(c), 'scaled': int(c/max_count*100)}
                  for w, c in top60]
with open('data/wordcloud.json', 'w', encoding='utf-8') as f:
    json.dump(wordcloud_data, f, ensure_ascii=False)
print(f'[OK] wordcloud.json: {len(wordcloud_data)} words (来源: 推荐菜_清洗)')

# ============ 8. 价格等级分布 (新增) ============
# 按人均消费区间自然排序
price_tier_counts = df['价格等级'].value_counts()
price_sort = {'低消费': 0, '中低': 1, '中等': 2, '中高': 3, '高消费': 4, '高': 5}
price_data = sorted(
    [{'name': k, 'value': int(v)} for k, v in price_tier_counts.items()],
    key=lambda x: next((price_sort[sk] for sk in price_sort if sk in x['name']), 99)
)
with open('data/price_tier.json', 'w', encoding='utf-8') as f:
    json.dump(price_data, f, ensure_ascii=False)
print(f'[OK] price_tier.json: {len(price_data)} tiers')

# ============ 9. 评分等级分布 (新增) ============
rating_tier_counts = df['评分等级'].value_counts()
rating_sort = {'较差': 0, '一般': 1, '良好': 2, '优秀': 3, '卓越': 4}
rating_data = sorted(
    [{'name': k, 'value': int(v)} for k, v in rating_tier_counts.items()],
    key=lambda x: next((rating_sort[sk] for sk in rating_sort if sk in x['name']), 99)
)
with open('data/rating_tier.json', 'w', encoding='utf-8') as f:
    json.dump(rating_data, f, ensure_ascii=False)
print(f'[OK] rating_tier.json: {len(rating_data)} tiers')

# ============ 10. 各城市性价比排名 (新增) ============
value_data = []
for city, grp in city_group:
    high_value = int(grp['是否高性价比'].sum())
    total = len(grp)
    value_data.append({
        'city': city,
        'high_value_count': high_value,
        'total': total,
        'ratio': round(high_value/total*100, 1)
    })
value_data.sort(key=lambda x: x['ratio'], reverse=True)
with open('data/value_for_money.json', 'w', encoding='utf-8') as f:
    json.dump(value_data, f, ensure_ascii=False)
print(f'[OK] value_for_money.json: {len(value_data)} cities')

# ============ 11. 概览数据 ============
overview = {
    'total_cities': df['城市'].nunique(),
    'total_merchants': int(len(df)),
    'total_reviews': int(df['点评数量'].sum()),
    'avg_cost': round(df['人均消费(元)'].mean()),
    'total_food_types': df['美食类型'].nunique(),
    'high_value_pct': round(df['是否高性价比'].sum() / len(df) * 100, 1),
}
with open('data/overview.json', 'w', encoding='utf-8') as f:
    json.dump(overview, f, ensure_ascii=False)
print(f'[OK] overview.json (含美食类型数/高性价比占比)')

print('\n=== DONE === All data files generated in data/')
