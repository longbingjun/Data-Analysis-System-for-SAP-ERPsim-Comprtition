from django.db import models

class MarketSalesData(models.Model):
    date = models.DateField(verbose_name="日期")
    material_description = models.CharField(max_length=255, verbose_name="物料描述")
    area = models.CharField(max_length=100, verbose_name="区域")
    qty = models.FloatField(verbose_name="数量")
    value = models.FloatField(verbose_name="金额")
    price = models.FloatField(verbose_name="单价")

    class Meta:
        verbose_name = "市场销售数据"
        verbose_name_plural = "市场销售数据"

    def __str__(self):
        return f"{self.date} - {self.material_description} - {self.area}"

class GroupSalesData(models.Model):
    round = models.IntegerField(verbose_name="轮次")
    day = models.IntegerField(verbose_name="天数")
    area = models.CharField(max_length=20, verbose_name="区域")
    sloc = models.CharField(max_length=20, verbose_name="库存地点")
    distribution_channel = models.CharField(max_length=20, verbose_name="分销渠道")
    material = models.CharField(max_length=100, verbose_name="物料编码")
    material_description = models.CharField(max_length=255, verbose_name="物料描述")
    price = models.FloatField(verbose_name="单价")
    qty = models.FloatField(verbose_name="数量")
    value = models.FloatField(verbose_name="金额")
    cost = models.FloatField(verbose_name="成本")

    class Meta:
        verbose_name = "本小组销售数据"
        verbose_name_plural = "本小组销售数据"

    def __str__(self):
        return f"第{self.round}轮-第{self.day}天-{self.material_description}"