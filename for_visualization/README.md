# 大众点评/美团餐饮数据分析 — 可视化数据包

## 数据来源
- MongoDB `food_project.shop_data` 集合，10,000 条爬取数据
- Hive 分析查询结果
- 10个城市：北京、上海、广州、深圳、杭州、成都、武汉、南京、苏州、重庆

## 文件说明

| 文件 | 说明 | 建议图表 | 行数 |
|------|------|----------|------|
| city_shop_count.csv | 各城市餐厅数量分布 | 柱状图 / 中国地图热力图 | 10 |
| city_top5_food.csv | 每个城市最受欢迎的5种美食类型 | 分组柱状图 / 堆叠图 | 50 |
| food_type_distribution.csv | 全部美食类型分布 | 饼图 / 柱状图 | 19 |
| city_food_cross.csv | 城市和美食类型交叉统计（店数、均价、评分） | 热力图 / 气泡图 | 189 |
| price_level.csv | 价格等级分布 | 饼图 | 5 |
| rating_level.csv | 评分等级分布 | 饼图 / 柱状图 | 5 |
| city_avg_consumption.csv | 各城市人均消费（含标准差、最值） | 柱状图（带误差线） | 10 |
| price_range_dist.csv | 人均消费区间分布 | 饼图 / 柱状图 | 5 |
| food_type_avg_price.csv | 各美食类型人均消费排名 | 横向柱状图 | 19 |
| city_good_value.csv | 各城市高性价比餐厅比例 | 柱状图 | 10 |
| top20_popularity.csv | 热门度最高的20家餐厅 | 横向柱状图 / 表格 | 20 |
| top30_dishes.csv | 最常见的30个推荐菜 | 词云 / 柱状图 | 30 |
| price_vs_score.csv | 不同价格区间的各项评分变化 | 折线图（多线） | 23 |
| taste_vs_env.csv | 口味评分与环境评分的关系 | 散点图 / 折线图 | 28 |
| score_summary.csv | 评分汇总统计及相关系数 | 数值展示卡 / 雷达图 | 1 |
| reputation_balance.csv | 口碑均衡度（口味/环境/服务一致性） | 饼图 | 4 |
| food_type_score_rank.csv | 各美食类型综合评分排名 | 横向柱状图 / 气泡图 | 19 |
| review_vs_score.csv | 不同评论数区间的评分和均价 | 折线图 | 6 |
| top20_reviewed.csv | 评论数最多的20家餐厅 | 横向柱状图 | 20 |
| city_review_activity.csv | 各城市点评活跃度 | 分组柱状图 | 10 |
| correlation_coeff.csv | 评论数与评分/口味/价格的相关系数 | 数值展示卡 | 1 |
| shop_data_raw.csv | 原始10,000条餐厅数据（全部字段） | 任意图表 | 10000 |

## 建议可视化方案（课程要求覆盖）

| 分析维度 | 数据文件 | 推荐图表 |
|----------|----------|----------|
| 1. 城市分布 | city_shop_count.csv, city_food_cross.csv | 中国地图 + 柱状图 |
| 2. 美食类型 | food_type_distribution.csv, food_type_score_rank.csv | 饼图 + 横向柱状图 |
| 3. 人均消费 | city_avg_consumption.csv, price_range_dist.csv | 柱状图(误差线) + 饼图 |
| 4. 口味vs环境 | taste_vs_env.csv, score_summary.csv | 散点图 + 数值卡 |
| 5. 评分分析 | price_vs_score.csv, food_type_score_rank.csv | 多线折线图 + 柱状图 |
| 6. 评论分析 | review_vs_score.csv, city_review_activity.csv | 折线图 + 分组柱状图 |
| 7. 价格vs评分 | price_vs_score.csv, correlation_coeff.csv | 折线图 + 热力图 |
| 8. 热门推荐 | top20_popularity.csv, top30_dishes.csv | 横向柱状图 + 词云 |

## 工具推荐
- **Python**: matplotlib + seaborn + pyecharts
- **Web**: ECharts（推荐，交互效果好）
- **BI工具**: Tableau / FineBI
- **Excel**: 也能做基础图表

## 核心结论（可直接标在图上）
- 火锅占比12.5%，远超第二名日料(8.3%)
- 上海人均消费最高(¥110.9)，武汉最低(¥73)
- 口味与环境相关系数0.901（强正相关）
- 消费越高评分越高
- 评论数与评分弱相关(0.062)
- 海鲜人均最贵(¥188)，小吃最便宜(¥23)