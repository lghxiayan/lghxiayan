class Restaurant:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.number_served = 0

    def describe_restaurant(self):
        print(
            f"The restaurant name is {self.name}, the restaurant type is {self.type}, the restaurant number is {self.number_served}")

    def open_restaurant(self):
        print(f"The restaurant now is open! type is {self.type}")

    def set_number_served(self, number_served):
        self.number_served = number_served
        print(f"The restaurant has {self.number_served} served.")

    def increment_number_served(self, number_served):
        self.number_served += number_served


def main():
    restaurant = Restaurant("lgh", "open")
    restaurant.describe_restaurant()
    restaurant.open_restaurant()
    restaurant.set_number_served(100)
    restaurant.describe_restaurant()
    restaurant.increment_number_served(20)
    restaurant.describe_restaurant()

    restaurant_2 = Restaurant("222", "close")
    restaurant_2.describe_restaurant()

    restaurant_3 = Restaurant("333", "None")
    restaurant_3.describe_restaurant()


if __name__ == '__main__':
    main()
