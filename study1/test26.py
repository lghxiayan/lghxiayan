import unittest

from employee import Employee


class TestEmployee(unittest.TestCase):
    """定义测试类"""

    def setUp(self):
        """定义共用实例"""
        self.my_employee = Employee('xia', 'yan', 100)

    def test_give_default_raise(self):
        """测试默认增加值"""
        self.my_employee.give_raise()
        self.assertEqual(5100, self.my_employee.salary)

    def test_give_custom_raise(self):
        """测试自定义增加值"""
        self.my_employee.give_raise(3000)
        self.assertEqual(3100, self.my_employee.salary)


if __name__ == '__main__':
    unittest.main()
