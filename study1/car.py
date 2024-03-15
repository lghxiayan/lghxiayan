#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/12/08 15:12
# @Author : xiayan
# @Email : lghxiayan@163.com

class Car:
    """汽车类"""

    def __init__(self, make, model, year):
        """初始化属性"""
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def descriptive_name(self):
        """描述名称"""
        long_name = f"{self.make} {self.model} {self.year}"
        return long_name.title()

    def read_odometer(self):
        """读取里程数"""
        print(f"里程数为:{self.odometer_reading}")

    def update_odometer(self, mileage):
        """更新里程数"""
        if mileage > self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("里程数不能往回调！")

    def increment_odometer(self, mileage):
        """递增的里程数"""
        self.odometer_reading += mileage

    def fill_gas_tank(self):
        """加油"""
        print("给汽车加油！")
