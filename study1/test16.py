class Restaurant:
    """模拟餐厅"""

    def __init__(self, restaurant_name, cuisine_type):
        """初始化"""
        self.name = restaurant_name
        self.type = cuisine_type
        self.number_served = 0

    def describe_restaurant(self):
        """描述餐厅"""
        print(f"{self.name} 是一家 {self.type}")

    def open_restaurant(self):
        """餐厅正在营业"""
        print(f"{self.name} 正在营业")

    def print_number_served(self):
        """打印服务过的人数"""
        print(f"{self.name} 一共服务过 {self.number_served} 人")

    def update_number_served(self, number):
        """更新服务过的人数"""
        self.number_served = number

    def today_number_served(self, today_num):
        """今天共服务过的人数"""
        print(f"今天服务过 {today_num} 人")
        self.number_served += today_num

    def set_number_served(self, number):
        """设置最多就餐人数"""
        print(f"{self.name} 最多可以就餐 {number} 人")


ct1 = Restaurant('斯斯科餐厅', '西餐厅')
ct1.describe_restaurant()
ct1.open_restaurant()
# ct1.number_served = 33
ct1.update_number_served(22)
ct1.today_number_served(20)
ct1.print_number_served()
ct1.set_number_served(11)
