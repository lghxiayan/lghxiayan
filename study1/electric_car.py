#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/12/08 15:12
# @Author : xiayan
# @Email : lghxiayan@163.com
from car import Car


class Battery():
    """定义电池类"""

    def __init__(self, battery_size=75):
        """电池类初始化"""
        self.battery_size = battery_size

    def describe_battery(self):
        """描述电池的属性"""
        print(f"这辆车有个 {self.battery_size}-kWh 电池！")

    def get_range(self):
        """指出电瓶的续航里程"""
        if self.battery_size == 75:
            range_length = 260
        else:
            range_length = 315
        print(f'续航里程是 {range_length}')

    def update_battery(self):
        if self.battery_size != 100:
            self.battery_size = 100
        print('电池已升级')


class ElectricCar(Car):
    """电动汽车类"""

    def __init__(self, make, model, year):
        """初始化父类的属性"""
        super().__init__(make, model, year)
        self.battery = Battery()

    def fill_gas_tank(self):
        """对父类的该方法进行重写"""
        print("电动汽车没有油箱！")
