"""
餐饮大数据分析 — 可视化网站
Flask 主程序
启动方式: python app.py
访问地址: http://localhost:5000
"""
from flask import Flask, render_template, jsonify
import pandas as pd
import json
import os
import sys
import io

# 解决 Windows GBK 终端 emoji 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def read_json(filename):
    """读取 data/ 下的 JSON 文件"""
    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)


def read_csv(filename):
    """读取 data/ 下的 CSV 文件"""
    return pd.read_csv(os.path.join(DATA_DIR, filename))


# ── 页面路由 ──────────────────────────────────────

@app.route('/')
def index():
    """首页仪表盘"""
    return render_template('index.html')

@app.route('/city-map')
def city_map():
    """城市分布地图"""
    return render_template('city_map.html')

@app.route('/food-preference')
def food_preference():
    """美食偏好分析"""
    return render_template('food_preference.html')

@app.route('/review-analysis')
def review_analysis():
    """评价分析"""
    return render_template('review_analysis.html')

@app.route('/taste-trend')
def taste_trend():
    """口味趋势"""
    return render_template('taste_trend.html')


# ── 数据 API 接口 ─────────────────────────────────

@app.route('/api/overview')
def api_overview():
    """首页概览数据 — 读取 data/overview.json"""
    return jsonify(read_json('overview.json'))


@app.route('/api/city_stats')
def api_city_stats():
    """城市统计数据 — 读取 data/city_stats.csv"""
    df = read_csv('city_stats.csv')
    return jsonify(df.to_dict(orient='records'))


@app.route('/api/city_food_preference')
def api_city_food_preference():
    """各城市美食类型Top10 — 读取 data/food_preference.json"""
    return jsonify(read_json('food_preference.json'))


@app.route('/api/score_matrix')
def api_score_matrix():
    """
    评价分析散点图数据
    每个点: [人均消费, 评价指数(=口味评分), 口味指数, 环境指数, 综合指数, 点评数量, 美食类型, 城市]
    读取 data/score_matrix.json
    """
    return jsonify(read_json('score_matrix.json'))


@app.route('/api/food_trend')
def api_food_trend():
    """
    口味趋势数据 — 烧烤 vs 面馆 各城市占比对比
    读取 data/food_trend.json
    结构: {cities: [...], bbq_ratio: [...], noodle_ratio: [...]}
    """
    return jsonify(read_json('food_trend.json'))


@app.route('/api/food_cost_heatmap')
def api_food_cost_heatmap():
    """城市 x 美食类型 人均消费热力图 — 读取 data/food_cost_heatmap.csv"""
    df = read_csv('food_cost_heatmap.csv')
    # 返回 [[city, food_type, avg_cost], ...]
    return jsonify(df.values.tolist())


@app.route('/api/pie_data')
def api_pie_data():
    """美食类型占比饼图 — 读取 data/pie_data.json"""
    return jsonify(read_json('pie_data.json'))


@app.route('/api/wordcloud_data')
def api_wordcloud_data():
    """推荐菜词云 — 读取 data/wordcloud.json (来源: 推荐菜_清洗)"""
    return jsonify(read_json('wordcloud.json'))


@app.route('/api/price_tier')
def api_price_tier():
    """价格等级分布 — 读取 data/price_tier.json"""
    return jsonify(read_json('price_tier.json'))


@app.route('/api/rating_tier')
def api_rating_tier():
    """评分等级分布 — 读取 data/rating_tier.json"""
    return jsonify(read_json('rating_tier.json'))


@app.route('/api/value_for_money')
def api_value_for_money():
    """各城市高性价比占比排名 — 读取 data/value_for_money.json"""
    return jsonify(read_json('value_for_money.json'))


if __name__ == '__main__':
    print("[OK] 餐饮大数据分析可视化平台启动中...")
    print("      访问地址: http://localhost:5000")
    app.run(debug=True, port=5000)
