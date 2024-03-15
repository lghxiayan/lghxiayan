#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/12/09 16:29
# @Author : xiayan
# @Email : lghxiayan@163.com

from electric_car import ElectricCar

my_tesla = ElectricCar('tesla', 'model s', 2019)
print(my_tesla.descriptive_name())
my_tesla.battery.describe_battery()
my_tesla.battery.get_range()
