class Car:
    """模拟汽车类"""

    def __init__(self, make, model, year):
        """初始化"""
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        """返回整洁的描述性信息"""
        long_name = f"{self.year} {self.make} {self.model} "
        return long_name

    def read_odometer(self):
        """打印一条汽车里程的消息"""
        print(f"This car has {self.odometer_reading} miles on it.")


my_car = Car('audi', 'A6', '2019')
print(my_car.get_descriptive_name(), my_car.odometer_reading)
my_car.read_odometer()
