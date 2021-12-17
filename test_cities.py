import unittest

import city_function


class TestCities(unittest.TestCase):
    """定义测试类"""

    def test_city_country(self):
        city_name = city_function.city_country('beijin', 'china')
        self.assertEqual(city_name, 'Beijin, China')

    def test_city_country_population(self):
        city_name = city_function.city_country('beijin', 'china', 'population 5000000')
        self.assertEqual(city_name, 'Beijin, China - Population 5000000')


if __name__ == '__main__':
    unittest.main()
