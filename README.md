# 🍜 餐饮大数据分析平台

基于 **Flask + ECharts 5.5.0** 的餐饮大数据可视化分析平台，覆盖 **10 个城市、19 种美食类型、10,000 家餐厅** 的多维度数据。

## ✨ 功能页面

| 页面 | 内容 |
|:---|:---|
| 🏠 **首页概览** | 核心指标卡片、城市商户分布、美食类型排名、评分/价格散点矩阵 |
| 🗺️ **城市分布** | 中国地图（商户/点评/人均消费热力）、城市对比柱状图、数据明细表 |
| 🍽️ **美食偏好** | 各城市 Top10 美食类型、城市×美食人均消费热力图 |
| 📊 **评价分析** | 多维评分雷达图、评分相关性分析、评论活跃度、口碑均衡度 |
| 📈 **口味趋势** | 烧烤vs面馆占比对比、美食市场份额饼图、推荐菜词云、价格/评分等级分布、高性价比排名 |

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/fish0703/food-analytics-platform.git
cd food-analytics-platform
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
cd visualization_web
python app.py
```

### 4. 打开浏览器

访问 **http://localhost:5000**

## 📁 项目结构

```
food-analytics-platform/
├── visualization_web/
│   ├── app.py              # Flask 主程序
│   ├── data/               # 预处理后的数据文件（11个）
│   ├── templates/          # Jinja2 HTML 模板（5个页面）
│   └── gen_data.py         # 旧版数据生成脚本
├── for_visualization/      # 原始分析数据（22个CSV）
├── prepare_data.py         # 数据转换脚本（原始→可视化）
├── requirements.txt        # Python 依赖
└── README.md
```

## 🛠 技术栈

- **后端**: Python Flask
- **前端**: ECharts 5.5.0 + Jinja2 模板
- **数据处理**: Pandas
- **地图**: DataV GeoJSON 中国地图
- **字体**: Google Fonts Noto Serif SC（思源宋体）
- **设计**: 暖陶色系简约主题，CSS 变量系统

## 📊 数据说明

原始数据来自大众点评/美团爬取，包含 10,000 条餐厅记录，覆盖：

- **城市**: 北京、上海、广州、深圳、杭州、南京、苏州、成都、武汉、重庆
- **美食类型**: 火锅、川菜、本帮菜、粤菜、日料、面馆、烧烤等 19 种
- **字段**: 综合评分、口味、环境、服务、人均消费、点评数、推荐菜等

## 🎨 预览

![首页概览](screenshots/index.png)

> 暖陶色系（#c97d60）简约温馨主题，思源宋体标题排版
