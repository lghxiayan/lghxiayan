class User:
    """用户类"""

    def __init__(self, first, last):
        """初始化first_name和last_name等两个属性"""
        self.first_name = first
        self.last_name = last
        self.login_attempts = 0

    def describe_user(self):
        """打印用户信息摘要"""
        print(f"This man first name is {self.first_name}")
        print(f"and last name is {self.last_name}")

    def greet_user(self):
        """个性的问候"""
        print(f"Hello {self.last_name} {self.first_name}")

    def increment_login_attempts(self):
        self.login_attempts += 1
        print(f"尝试登录了 {self.login_attempts} 次")

    def reset_login_attempts(self):
        self.login_attempts = 0
        print(f"已对登录次数进行了重置。")


tom = User('tom', 'jack')
print(tom.first_name, tom.last_name)
tom.describe_user()
tom.greet_user()
for i in range(3):
    tom.increment_login_attempts()
    print(tom.login_attempts)
tom.reset_login_attempts()
