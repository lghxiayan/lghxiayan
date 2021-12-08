class Car:
    """模拟汽车类"""

    def __init__(self, make, model, year):
        """初始化"""
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 64  # 给属性指定默认值

    def get_descriptive_name(self):
        """返回整洁的描述性信息"""
        long_name = f"{self.year} {self.make} {self.model} "
        return long_name

    def read_odometer(self):
        """打印一条汽车里程的消息"""
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage):
        """
        更新里程数
        禁止把里程表计数往回调
        """
        if mileage > self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print('不能把里程表计数往回调')

    def increment_odometer(self, miles):
        """将里程表计数增加指定的量"""
        self.odometer_reading += miles


my_car = Car('audi', 'A6', '2019')
print(my_car.get_descriptive_name())
my_car.read_odometer()
my_car.update_odometer(100)
my_car.read_odometer()
my_car.increment_odometer(23_500)
my_car.read_odometer()
