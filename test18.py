class User:
    """用户类"""

    def __init__(self, first, last):
        """初始化first_name和last_name等两个属性"""
        self.first_name = first
        self.last_name = last

    def describe_user(self):
        """打印用户信息摘要"""
        print(f"This man first name is {self.first_name}")
        print(f"and last name is {self.last_name}")

    def greet_user(self):
        """个性的问候"""
        print(f"Hello {self.last_name} {self.first_name}")


tom = User('tom', 'jack')
print(tom.first_name, tom.last_name)
tom.describe_user()
tom.greet_user()
