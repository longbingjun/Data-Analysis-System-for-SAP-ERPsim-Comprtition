from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import MarketSalesData, GroupSalesData
from datetime import datetime, date, timedelta
from django.db.models import Sum, F, Max
from django.utils.html import format_html
import json
from collections import defaultdict

# 导入数据资源
class MarketData(resources.ModelResource):
    date = fields.Field(attribute='date', column_name='Date')
    material_description = fields.Field(attribute='material_description', column_name='Material Description')
    area = fields.Field(attribute='area', column_name='Area')
    qty = fields.Field(attribute='qty', column_name='Qty')
    value = fields.Field(attribute='value', column_name='Value')
    price = fields.Field(attribute='price', column_name='Price')

    def before_import_row(self, row, **kwargs):
        # 假设日期格式为 MM/DD
        if 'Date' in row and row['Date']:
            try:
                # 自动补全年份为今年
                row['Date'] = datetime.now().strftime('%Y') + '-' + row['Date'].replace('/', '-')
                # 如果你想强制2024年，可以写成：
                # row['Date'] = '2024-' + row['Date'].replace('/', '-')
            except Exception:
                pass

    class Meta:
        model = MarketSalesData
        import_id_fields = ('date', 'material_description', 'area')
        fields = ('date', 'material_description', 'area', 'qty', 'value', 'price')

@admin.register(MarketSalesData)
class MarketSalesDataAdmin(ImportExportModelAdmin):
    resource_class = MarketData
    list_display = ['date', 'material_description', 'area', 'qty', 'value', 'price']
    actions = ['delete_all_records']
    change_list_template = "admin/market_change_list.html"  # 使用独立模板，避免覆盖默认模板

    @admin.action(description='一键删除所有市场销售数据')
    def delete_all_records(self, request, queryset):
        self.model.objects.all().delete()
        self.message_user(request, "所有市场销售数据已被删除！", level='WARNING')

    def changelist_view(self, request, extra_context=None):
        # 轮次与时间区间定义
        round_ranges = [
            (1, '01-05', '01-20'),
            (2, '02-05', '02-20'),
            (3, '03-05', '03-20'),
            (4, '04-05', '04-20'),
        ]
        round_data = {}
        for round_num, start_day, end_day in round_ranges:
            # 构造日期范围
            year = datetime.now().year
            start_date = f"{year}-{start_day}"
            end_date = f"{year}-{end_day}"
            # 查询该轮数据
            qs = MarketSalesData.objects.filter(date__gte=start_date, date__lte=end_date)
            agg = (
                qs.values('material_description')
                .annotate(qty_sum=Sum('qty'))
                .order_by('-qty_sum')
            )
            chart_data = [
                {'name': d['material_description'], 'qty': d['qty_sum']}
                for d in agg
            ]
            round_data[str(round_num)] = chart_data

        # ========== 利润排行逻辑 ===========
        # 获取所有产品
        all_products = MarketSalesData.objects.values('material_description').distinct()
        # 获取页面传入的成本价
        cost_dict = {}
        if request.method == 'POST' and 'cost_update' in request.POST:
            for p in all_products:
                mat = p['material_description']
                cost_val = request.POST.get(f'cost_{mat}', '')
                try:
                    cost_dict[mat] = float(cost_val)
                except:
                    cost_dict[mat] = 0.0
            request.session['market_cost_dict'] = cost_dict
        else:
            cost_dict = request.session.get('market_cost_dict', {})
        # 统计qty之和
        qty_agg = MarketSalesData.objects.values('material_description').annotate(qty_sum=Sum('qty'))
        qty_map = {d['material_description']: d['qty_sum'] for d in qty_agg}
        # 统计每个产品最新一天的最高市场价
        price_map = {}
        for p in all_products:
            mat = p['material_description']
            # 找到该产品的最新一天
            last = MarketSalesData.objects.filter(material_description=mat).order_by('-date').first()
            if last:
                # 取最新一天所有该产品的最高价
                max_price = MarketSalesData.objects.filter(material_description=mat, date=last.date).aggregate(maxp=Max('price'))['maxp']
                price_map[mat] = max_price
            else:
                price_map[mat] = 0.0
        # 计算单个利润
        profit_list = []
        for mat in qty_map:
            qty = qty_map[mat]
            price = price_map.get(mat, 0.0)
            cost = cost_dict.get(mat, 0.0)
            profit = price - cost
            profit_list.append({'material_description': mat, 'qty': qty, 'profit': profit, 'cost': cost, 'price': price})
        # 按qty排序（用于配色）
        qty_sorted = sorted(profit_list, key=lambda x: x['qty'], reverse=True)
        qty_rank_map = {x['material_description']: i+1 for i, x in enumerate(qty_sorted)}
        # 按单个利润排序
        profit_sorted = sorted(profit_list, key=lambda x: x['profit'], reverse=True)
        for i, item in enumerate(profit_sorted):
            item['rank'] = i+1
            item['qty_rank'] = qty_rank_map[item['material_description']]

        # ========== 分地区偏好排行逻辑 ===========
        # 统计每个产品各地区qty总和
        region_agg = MarketSalesData.objects.values('material_description', 'area').annotate(qty_sum=Sum('qty'))
        # 构建产品-地区-qty字典
        region_map = {}
        for row in region_agg:
            mat = row['material_description']
            area = row['area'].strip().lower()
            qty = row['qty_sum']
            if mat not in region_map:
                region_map[mat] = {'north': 0, 'south': 0, 'west': 0}
            if area == 'north':
                region_map[mat]['north'] += qty
            elif area == 'south':
                region_map[mat]['south'] += qty
            elif area == 'west':
                region_map[mat]['west'] += qty
        # 总体偏好排序（按qty总和降序）
        total_qty_map = {mat: sum(vals.values()) for mat, vals in region_map.items()}
        sorted_mats = sorted(total_qty_map.items(), key=lambda x: x[1], reverse=True)
        region_list = []
        for idx, (mat, total_qty) in enumerate(sorted_mats):
            north = region_map[mat]['north']
            south = region_map[mat]['south']
            west = region_map[mat]['west']
            # 计算比例
            total = north + south + west
            if total > 0:
                n_ratio = north / total
                s_ratio = south / total
                w_ratio = west / total
                # 比例化为1.x格式
                n_show = round(n_ratio * 4, 1)
                s_show = round(s_ratio * 4, 1)
                w_show = round(w_ratio * 4, 1)
                ratio_str = f"{n_show} : {s_show} : {w_show}"
            else:
                n_ratio = s_ratio = w_ratio = 1/3
                ratio_str = "0 : 0 : 0"
            # 应分配库存逻辑
            if idx < 4:
                max_stock = 12000
            elif idx < 7:
                max_stock = 10000
            elif idx < 10:
                max_stock = 8000
            else:
                max_stock = 0
            # 找到最大值归属地区
            ratios = [n_ratio, s_ratio, w_ratio]
            max_idx = ratios.index(max(ratios))
            stock = [0, 0, 0]
            if max_stock > 0:
                stock[max_idx] = max_stock
                # 其余两个地区按比例分配
                other_idxs = [i for i in range(3) if i != max_idx]
                # 计算剩余比例
                remain = 1 - ratios[max_idx]
                if remain > 0:
                    stock[other_idxs[0]] = int(round(max_stock * ratios[other_idxs[0]] / ratios[max_idx]))
                    stock[other_idxs[1]] = int(round(max_stock * ratios[other_idxs[1]] / ratios[max_idx]))
                else:
                    stock[other_idxs[0]] = 0
                    stock[other_idxs[1]] = 0
            stock_str = f"{stock[0]} : {stock[1]} : {stock[2]}"
            region_list.append({
                'rank': idx+1,
                'material_description': mat,
                'north': north,
                'south': south,
                'west': west,
                'ratio': ratio_str,
                'stock': stock_str
            })

        extra_context = extra_context or {}
        extra_context['round_chart_data'] = json.dumps(round_data, ensure_ascii=False)
        extra_context['profit_sorted'] = profit_sorted
        all_prod_list = [p['material_description'] for p in all_products]
        extra_context['all_products'] = all_prod_list
        # 拆分为1kg与500g两组，便于模板渲染两列
        extra_context['all_products_1kg'] = [m for m in all_prod_list if '1kg' in str(m).lower()]
        extra_context['all_products_500g'] = [m for m in all_prod_list if '500g' in str(m).lower()]
        extra_context['cost_dict'] = cost_dict
        extra_context['region_list'] = region_list
        return super().changelist_view(request, extra_context=extra_context)

# 组数据资源
class GroupSalesDataResource(resources.ModelResource):
    round = fields.Field(attribute='round', column_name='Round')
    day = fields.Field(attribute='day', column_name='Day')
    area = fields.Field(attribute='area', column_name='Area')
    sloc = fields.Field(attribute='sloc', column_name='SLoc.')
    distribution_channel = fields.Field(attribute='distribution_channel', column_name='Distribution Channel')
    material = fields.Field(attribute='material', column_name='Material')
    material_description = fields.Field(attribute='material_description', column_name='Material Description')
    price = fields.Field(attribute='price', column_name='Price')
    qty = fields.Field(attribute='qty', column_name='Qty')
    value = fields.Field(attribute='value', column_name='Value')
    cost = fields.Field(attribute='cost', column_name='Cost')

    class Meta:
        model = GroupSalesData
        import_id_fields = (
            'round', 'day', 'area', 'sloc', 'distribution_channel',
            'material', 'material_description', 'price', 'qty', 'value', 'cost'
        )
        fields = (
            'round', 'day', 'area', 'sloc', 'distribution_channel',
            'material', 'material_description', 'price', 'qty', 'value', 'cost'
        )

@admin.register(GroupSalesData)
class GroupSalesDataAdmin(ImportExportModelAdmin):
    resource_class = GroupSalesDataResource
    list_display = [
        'round', 'day', 'area', 'sloc', 'distribution_channel',
        'material', 'material_description', 'price', 'qty', 'value', 'cost'
    ]
    actions = ['delete_all_records']
    change_list_template = "admin/group_change_list.html"  # 指定自定义模板

    @admin.action(description='一键删除所有小组销售数据')
    def delete_all_records(self, request, queryset):
        self.model.objects.all().delete()
        self.message_user(request, "所有小组销售数据已被删除！", level='WARNING')

    def changelist_view(self, request, extra_context=None):
        # 1. 定义轮次和日期区间
        round_ranges = {
            1: ('01-05', '01-20'),
            2: ('02-05', '02-20'),
            3: ('03-05', '03-20'),
            4: ('04-05', '04-20'),
        }
        # 轮次->所有天
        round_days = {}
        for r, (start, end) in round_ranges.items():
            start_date = date(2025, int(start.split('-')[0]), int(start.split('-')[1]))
            end_date = date(2025, int(end.split('-')[0]), int(end.split('-')[1]))
            days = []
            d = start_date
            while d <= end_date:
                days.append(d)
                d += timedelta(days=1)
            round_days[r] = days

        # 2. 获取所有material description（大包装/小包装）
        all_market = MarketSalesData.objects.all().values('material_description')
        all_group = GroupSalesData.objects.all().values('material_description')
        all_mats = set([x['material_description'] for x in all_market] + [x['material_description'] for x in all_group])
        mats_1kg = [m for m in all_mats if '1kg' in m]
        mats_500g = [m for m in all_mats if '500g' in m]

        # 3. 市场数据补全区间
        market_data = MarketSalesData.objects.all().values('material_description', 'date', 'price')
        market_dict = defaultdict(lambda: defaultdict(list))  # mat -> date -> [price]
        for row in market_data:
            market_dict[row['material_description']][str(row['date'])].append(row['price'])

        print('market_dict', dict(market_dict))

        # 4. 小组数据
        group_data = GroupSalesData.objects.all().values('material_description', 'round', 'day', 'price')
        group_dict = defaultdict(lambda: defaultdict(dict))  # mat -> round -> day -> price
        for row in group_data:
            mat = row['material_description']
            r = int(row['round'])
            d = int(row['day'])
            group_dict[mat][r][d] = row['price']

        # 5. 构造前端需要的数据结构
        def build_chart_data(mats, round_days, market_data_list):
            # 自动获取实际年份
            all_years = set()
            for row in market_data_list:
                y = str(row['date'])[:4]
                all_years.add(y)
            if all_years:
                use_year = sorted(all_years)[-1]  # 取最大年份
            else:
                use_year = str(datetime.now().year)

            # 定义每轮的区间分组（严格按你的要求）
            group_ranges = [
                (1, [(1,5,5),(6,10,10),(11,15,15),(16,20,20)]),
                (2, [(5,10,10),(11,15,15),(16,20,20)]),
                (3, [(5,10,10),(11,15,15),(16,20,20)]),
                (4, [(5,10,10),(11,15,15),(16,20,20)])
            ]
            round_group = {r:grps for r,grps in group_ranges}

            result = {}
            for r, days in round_days.items():
                result[r] = {}
                for mat in mats:
                    mat_market = market_dict[mat]
                    # 构造区间映射
                    day_to_market = {}
                    grps = round_group[r]
                    for start, end, ref_day in grps:
                        # 取区间指定ref_day的市场价
                        ref_date = date(2025, r, ref_day)
                        ref_date_str = f"{use_year}-{r:02d}-{ref_day:02d}"
                        prices = mat_market.get(ref_date_str, [])
                        if prices:
                            max_price = max(prices)
                            min_price = min(prices)
                        else:
                            max_price = None
                            min_price = None
                        for d in days:
                            if start <= d.day <= end:
                                day_to_market[d] = {'max': max_price, 'min': min_price}
                    # 小组价格
                    group_prices = group_dict[mat][r] if mat in group_dict and r in group_dict[mat] else {}
                    # 组装x轴和y轴
                    x_list = []
                    market_max = []
                    market_min = []
                    group_price = []
                    for d in days:
                        x = f"{r}-{d.day:02d}"
                        x_list.append(x)
                        market_price_data = day_to_market.get(d, {'max': None, 'min': None})
                        max_val = market_price_data['max'] if market_price_data['max'] is not None else None
                        min_val = market_price_data['min'] if market_price_data['min'] is not None else None
                        group_val = group_prices.get(d.day, None) if group_prices.get(d.day, None) is not None else None
                        market_max.append(max_val)
                        market_min.append(min_val)
                        group_price.append(group_val)
                    result[r][mat] = {
                        'x': x_list,
                        'market_max': market_max,
                        'market_min': market_min,
                        'group_price': group_price,
                    }
            return result

        chart_1kg = build_chart_data(mats_1kg, round_days, market_data)
        chart_500g = build_chart_data(mats_500g, round_days, market_data)

        extra_context = extra_context or {}
        extra_context['chart_1kg'] = json.dumps(chart_1kg or {}, ensure_ascii=False)
        extra_context['chart_500g'] = json.dumps(chart_500g or {}, ensure_ascii=False)
        extra_context['mats_1kg'] = json.dumps(mats_1kg or [], ensure_ascii=False)
        extra_context['mats_500g'] = json.dumps(mats_500g or [], ensure_ascii=False)
        return super().changelist_view(request, extra_context=extra_context)
# 设置后台标题
admin.site.site_header = "ERP比赛数据分析"
admin.site.index_title = "ERP比赛数据分析"
admin.site.site_title = "ERP比赛数据分析"

def get_market_price_dict():
    # 获取所有市场价格，按material_description和date分组
    market_data = MarketSalesData.objects.filter(material_description__contains='1kg').values('material_description', 'date', 'price')
    price_dict = defaultdict(dict)
    for row in market_data:
        price_dict[row['material_description']][str(row['date'])] = row['price']
    return price_dict

def get_group_price_points():
    # 获取所有小组销售数据（1kg产品）
    group_data = GroupSalesData.objects.filter(material_description__contains='1kg').values('material_description', 'round', 'day', 'price')
    points = defaultdict(list)
    for row in group_data:
        # 构造x轴：2025-<round>-<day>
        x = f"2025-{int(row['round']):02d}-{int(row['day']):02d}"
        points[row['material_description']].append({'x': x, 'price': row['price']})
    return points

def get_market_price_for_group_dates(price_dict, group_points):
    # 按你的规则补全市场价格
    # 1月1-5日用1月5日，1月6-10日用1月10日，依此类推
    # 先生成所有需要的日期
    date_ranges = [
        ('01-01', '01-05'),
        ('01-06', '01-10'),
        ('01-11', '01-15'),
        ('01-16', '01-20'),
        ('02-05', '02-20'),
        ('03-05', '03-20'),
        ('04-05', '04-20'),
    ]
    year = 2025
    date_map = {}
    for start, end in date_ranges:
        start_date = date.fromisoformat(f"{year}-{start}")
        end_date = date.fromisoformat(f"{year}-{end}")
        # 用end_date的市场价补全区间
        for i in range((end_date - start_date).days + 1):
            d = start_date + timedelta(days=i)
            date_map[str(d)] = str(end_date)
    # 返回：{material_description: {group_x: market_price}}
    market_for_group = defaultdict(dict)
    for mat, points in group_points.items():
        for p in points:
            # p['x']格式为2025-01-03
            market_date = date_map.get(p['x'])
            if market_date:
                market_for_group[mat][p['x']] = price_dict.get(mat, {}).get(market_date)
            else:
                market_for_group[mat][p['x']] = None
    return market_for_group

print(MarketSalesData.objects.filter(material_description='1kg Blueberry Muesli').values('date', 'price'))