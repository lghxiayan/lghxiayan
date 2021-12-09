class Restaurant:
    """餐厅类"""

    def __init__(self, restaurant_name, cuisine_type):
        """初始化属性"""
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.number_served = 0
        self.ice_cream_stand = IceCreamStand()

    def describe_restaurant(self):
        """描述餐厅"""
        long_name = f'{self.restaurant_name} 是一家 {self.cuisine_type}'
        print(long_name)

    def open_restaurant(self):
        """让餐厅开始营业"""
        print(f'{self.restaurant_name} 开始营业')

    def get_number_served(self):
        """打印服务过多少人"""
        print(f"{self.restaurant_name} 一共服务过 {self.number_served} 人")

    def set_number_served(self, num):
        """设置服务过的人数"""
        self.number_served = num

    def increment_number_served(self, num):
        """递增餐厅服务过的人数"""
        self.number_served += num


class IceCreamStand:
    """冰激凌类"""

    def __init__(self, *flavors):
        """初始化"""
        self.flavors = flavors

    def disp_flavors(self):
        """显示冰激凌的口味"""
        print(f"冰激凌的口味有：")
        for i in list(self.flavors):
            for j in i:
                print(f"- {j}")
        # print(list(self.flavors), type(self.flavors))


ct1 = Restaurant('北京莫斯科餐厅', '西餐厅')
ct1.describe_restaurant()
ct1.open_restaurant()
ct1.get_number_served()
ct1.set_number_served(35)
ct1.get_number_served()
ct1.increment_number_served(100)
ct1.get_number_served()
# ct1.ice_cream_stand.disp_flavors()
ice1 = IceCreamStand(['口味4', '口味5', '口味6'])
ice1.disp_flavors()
