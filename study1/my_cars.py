#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/12/09 16:42
# @Author : xiayan
# @Email : lghxiayan@163.com

from car import Car
from electric_car import ElectricCar

my_beetle = Car('volkswagen', 'beetle', 2019)
print(my_beetle.descriptive_name())

my_tesla = ElectricCar('tesla', 'model s', 2018)
print(my_tesla.descriptive_name())
