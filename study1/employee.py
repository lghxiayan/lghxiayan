class Employee:
    """定义类"""

    def __init__(self, first, last, salary):
        """初始化"""
        self.first_name = first
        self.last_name = last
        self.salary = salary

    def give_raise(self, add_raise=5000):
        """增加年薪"""
        self.salary += add_raise
        print(f"年薪增加了： {add_raise}")
