class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def describe_car(self):
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()

    def read_odometer(self):
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage: int):
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't")

    def increment_odometer(self, miles):
        self.odometer_reading += miles


def main():
    my_car = Car("audi", "A4", "2016")
    print(my_car.describe_car())
    my_car.update_odometer(23000000)
    my_car.increment_odometer(1_120_500)
    my_car.read_odometer()


if __name__ == '__main__':
    main()
