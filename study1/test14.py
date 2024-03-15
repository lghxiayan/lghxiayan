class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_describe(self):
        print(f"{self.make} {self.model} {self.year}")

    def read_odometer(self):
        print(f'里程表计数为: {self.odometer_reading}')

    def update_odometer(self, num):
        if num > self.odometer_reading:
            self.odometer_reading = num
        else:
            print('里程表计数不能往回调')

    def increment_odometer(self, num):
        self.odometer_reading += num

    def fill_gas_tank(self):
        print('给车加油')


class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        # self.battery_size = 75
        self.battery = Battery()

    def fill_gas_tank(self):
        print('电动汽车不需要加油!')


class Battery:
    def __init__(self, battery_size=75):
        self.battery_size = battery_size

    def describe_battery(self):
        print(f"电池容量为 {self.battery_size}-kWh.")

    def get_range(self):
        if self.battery_size == 75:
            print('里程数为260')
        elif self.battery_size == 100:
            print('里程数为315')

    def update_battery(self):
        if self.battery_size != 100:
            self.battery_size = 100
        print('电池已升级')


my_tesla = ElectricCar('tesla', 'model s', 2019)
# my_tesla.describe_battery()
my_tesla.fill_gas_tank()
my_tesla.battery.describe_battery()
my_tesla.battery.get_range()
my_tesla.battery.update_battery()
my_tesla.battery.get_range()
