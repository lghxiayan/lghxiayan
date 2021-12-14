import unittest

from name_function import get_formatted_name


class NameTest(unittest.TestCase):
    """测试name_function.py"""

    def test_name_function(self):
        formatted_name = get_formatted_name('xia', 'yan', 'xiao')
        self.assertEqual(formatted_name, 'Xia Xiao Yan')


if __name__ == '__main__':
    unittest.main()
