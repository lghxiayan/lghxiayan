class User:
    """用户类"""

    def __init__(self, first_name, last_name):
        """初始化"""
        self.first_name = first_name
        self.last_name = last_name
        self.login_attempts = 0

    def describe_user(self):
        """描述用户信息"""
        long_name = (self.first_name + " " + self.last_name).title()
        print(long_name)

    def greet_user(self):
        """个性化打招呼"""
        print(f"Hello {self.first_name.title()} {self.last_name.title()} ")

    def increment_login_attempts(self):
        """递增登录次数"""
        self.login_attempts += 1

    def reset_login_attempts(self):
        """重置登录次数"""
        self.login_attempts = 0


class Admin(User):
    """创建Admin类,继承User类"""

    def __init__(self, first, last):
        """初始化"""
        super().__init__(first, last)
        self.privileges = Privileges()


class Privileges:
    """权限类"""

    def __init__(self, privileges=['can add post', 'can delete post', 'can ban user']):
        self.privileges = privileges

    def show_privileges(self):
        """显示权限"""
        for privilege in self.privileges:
            print(f"- {privilege}")


user2 = Admin('xia', 'yan')
user2.greet_user()
user2.privileges.show_privileges()
