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


class ElectricCar(Car):
    """电动汽车类"""

    def __init__(self, make, model, year):
        """初始化父类的属性"""
        super().__init__(make, model, year)
        self.battery = Battery()

    def fill_gas_tank(self):
        """对父类的该方法进行重写"""
        print("电动汽车没有油箱！")


my_tesla = ElectricCar('tesla', 'model s', 2019)
print(my_tesla.descriptive_name())
my_tesla.read_odometer()
my_tesla.update_odometer(100)
my_tesla.read_odometer()
my_tesla.increment_odometer(1000)
my_tesla.read_odometer()
my_tesla.battery.describe_battery()
my_tesla.fill_gas_tank()
my_tesla.battery.get_range()
