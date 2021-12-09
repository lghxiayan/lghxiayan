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

    def fill_gas_tank(self):
        """加油"""
        print('给车加油！')


my_car = Car('audi', 'A6', '2019')
print(my_car.get_descriptive_name())
my_car.read_odometer()
my_car.update_odometer(100)
my_car.read_odometer()
my_car.increment_odometer(23_500)
my_car.read_odometer()
my_car.fill_gas_tank()


class ElectricCar(Car):
    """电动车类"""

    def __init__(self, make, model, year):
        """
        初始化父类的属性
        再初始化电动车特有的属性
        """
        super().__init__(make, model, year)
        self.battery_size = 75

    def describe_battery(self):
        """描述电池信息"""
        print(f"This car has a {self.battery_size}-kWh battery.")

    def fill_gas_tank(self):
        """继承自父类的方法，子类进行重写"""
        print("电动汽车没有油箱！")


my_tesla = ElectricCar('tesla', 'model s', 2019)
print(my_tesla.get_descriptive_name())
my_tesla.describe_battery()
my_tesla.fill_gas_tank()
