import datetime

from django.contrib import admin
from django.db import models


class Customer(models.Model):  # 创建一个名叫Customer的表
    name = models.CharField(max_length=200)  # 客户名称字段，CharField对应数据库中的vchar类型
    phone_number = models.CharField(max_length=200)  # 手机号字段
    address = models.CharField(max_length=200)  # 地址字段
    qq = models.CharField(max_length=30, null=True, blank=True)  # qq字段，可以为空，也可以为空值。


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    sn = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)


class Order(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    create_date = models.DateField(default=datetime.datetime.now)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


admin.site.register(Customer)
admin.site.register(Medicine)
admin.site.register(Order)
