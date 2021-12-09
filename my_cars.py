#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/12/09 16:42
# @Author : xiayan
# @Email : lghxiayan@163.com

from car import Car, ElectricCar
import car

my_beetle = car.Car('volkswagen', 'beetle', 2019)
my_beetle.get_describe()

my_tesla = car.ElectricCar('tesla', 'model s', 2018)
my_tesla.get_describe()
