import unittest

from name_function import get_formatted_name


class TestName(unittest.TestCase):
    """定义测试类"""

    def test_name(self):
        formatted_name = get_formatted_name('xia', 'yan')
        self.assertEqual(formatted_name, 'Xia Yan')


if __name__ == '__main__':
    unittest.main()
