# ERP比赛数据分析系统

## 项目简介

这是一个基于Django开发的ERP比赛数据分析系统，专为ERPsim比赛设计。该系统通过上传比赛数据，自动分析市场销售情况、畅销产品排名、产品利润分析和推荐下单产品列表，为比赛团队提供数据支持和决策参考。

## 项目背景

本系统是在参加**ERPsim INTERNATIONAL Competition 2025**比赛期间开发的，作为团队中的数据分析工具，为团队决策提供了重要支持，最终帮助团队获得了**国际赛季军**的优异成绩。

## 项目功能

- 📊 **数据导入导出**：支持Excel数据批量导入和导出
- 📈 **市场销售分析**：分析不同轮次、不同地区的销售趋势
- 💰 **产品利润分析**：计算各产品的利润空间，辅助定价决策
- 📍 **地区偏好分析**：分析不同地区对产品的偏好程度
- 📋 **智能库存分配**：根据销售数据自动推荐库存分配方案
- 📉 **价格对比分析**：对比本团队与市场价格走势
- 🎨 **数据可视化**：通过图表直观展示分析结果

## 技术栈

- **后端框架**：Django 5.1.6
- **数据库**：MySQL
- **前端美化**：SimpleUI
- **数据处理**：pandas
- **数据导入导出**：django-import-export
- **数据可视化**：JavaScript (前端图表)

## 项目结构

```
ERP/
├── ERP/                # 项目配置目录
│   ├── __init__.py
│   ├── settings.py     # 项目配置文件
│   ├── urls.py         # URL路由配置
│   └── wsgi.py
├── ErpSim/             # 主要应用
│   ├── __init__.py
│   ├── admin.py        # 后台管理配置
│   ├── apps.py
│   ├── models.py       # 数据模型
│   ├── views.py        # 视图函数
│   ├── migrations/     # 数据库迁移文件
│   └── templatetags/   # 模板标签
├── datasets/           # 数据集目录
│   └── *.xlsx          # 比赛数据文件
├── templates/          # 模板目录
│   └── admin/          # 自定义后台模板
├── manage.py           # 项目管理脚本
└── README.md           # 项目说明文档
```

## 核心功能模块

### 1. 数据导入导出模块

通过`django-import-export`实现Excel数据的批量导入和导出，支持市场销售数据和小组销售数据的快速录入。

### 2. 市场销售分析模块

- 按轮次分析市场销售趋势
- 统计各产品的销售数量和金额
- 分析不同地区的销售偏好

### 3. 小组销售分析模块

- 分析本团队各轮次、各天的销售情况
- 对比本团队与市场价格走势
- 评估定价策略的有效性

### 4. 智能库存分配模块

根据销售数据和地区偏好，自动计算并推荐最优库存分配方案，提高库存周转率和销售效率。

### 5. 产品利润分析模块

通过输入成本数据，计算各产品的利润空间，辅助团队制定合理的定价策略。

### 6. 数据可视化模块

通过自定义后台模板，使用JavaScript图表库展示分析结果，包括：
- 各轮次销售趋势图
- 产品价格对比图
- 地区偏好分析图

## 数据模型

### 市场销售数据 (MarketSalesData)

- `date`：日期
- `material_description`：物料描述
- `area`：区域
- `qty`：数量
- `value`：金额
- `price`：单价

### 小组销售数据 (GroupSalesData)

- `round`：轮次
- `day`：天数
- `area`：区域
- `sloc`：库存地点
- `distribution_channel`：分销渠道
- `material`：物料编码
- `material_description`：物料描述
- `price`：单价
- `qty`：数量
- `value`：金额
- `cost`：成本

## 安装指南

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+
- Django 5.1.6+

### 2. 安装步骤

1. 克隆项目
   ```bash
   git clone <repository-url>
   cd ERP
   ```

2. 创建虚拟环境
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # 或
   source venv/bin/activate  # Linux/Mac
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 配置数据库
   - 在MySQL中创建数据库：`erp_analysis`
   - 修改`ERP/settings.py`中的数据库配置

5. 数据库迁移
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. 创建超级用户
   ```bash
   python manage.py createsuperuser
   ```

7. 启动服务器
   ```bash
   python manage.py runserver
   ```

8. 访问后台
   - 地址：`http://127.0.0.1:8000/admin/`
   - 使用创建的超级用户登录

## 使用指南

### 1. 数据导入

1. 登录后台管理系统
2. 进入「市场销售数据」或「本小组销售数据」页面
3. 点击「导入」按钮，上传Excel数据文件
4. 系统会自动解析并导入数据

### 2. 数据分析

1. 市场销售数据分析：
   - 查看各轮次销售趋势图表
   - 分析产品利润排名
   - 查看地区偏好分析和库存分配建议

2. 小组销售数据分析：
   - 查看本团队销售价格与市场价格对比
   - 分析定价策略效果

### 3. 数据导出

- 在数据列表页面，点击「导出」按钮
- 选择导出格式（Excel、CSV等）
- 系统会生成并下载数据文件

## 项目亮点

1. **比赛成绩验证**：帮助团队获得ERPsim国际赛季军
2. **智能分析**：自动分析销售数据，提供决策支持
3. **可视化展示**：通过图表直观展示分析结果
4. **灵活配置**：支持自定义成本数据，适应不同场景
5. **批量处理**：支持Excel数据批量导入导出
6. **用户友好**：基于Django Admin的简洁界面

## 贡献指南

欢迎对本项目提出建议和改进：

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目作者：Bingjun Long
- 邮箱：bingjunlong@link.cuhk.edu.cn
- 比赛成绩：ERPsim INTERNATIONAL Competition 2025 - 3rd place in the international season

---

**感谢使用ERP比赛数据分析系统！** 希望本系统能为您的ERP比赛之旅提供有力支持。
