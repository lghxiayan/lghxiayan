import unittest
import datetime
from unittest.mock import patch, MagicMock
from selenium_ptvicomo_cookie_04 import BrowserManager, DataExtractor, DatabaseManager, Application
# 导入配置文件常量
from config_ptvicomo_04 import CHROME_DRIVER_PATH, DB_CONFIG, WEB_COOKIE, WEBSITE_URL, WAIT_TIMEOUT, TABLE_NAME, \
    CURRENT_ACTION, SALE_NUMBER, BUY_NUMBER, PROFIT_MARGIN, SAVE_PAGE, HEAD_LESS


class TestBrowserManager(unittest.TestCase):
    @patch('selenium_ptvicomo_cookie_04.webdriver.Chrome')
    def test_initialize_driver_headless(self, mock_chrome):
        browser_manager = BrowserManager(head_less=True)
        mock_chrome.assert_called_once_with(service=browser_manager.service, options=unittest.mock.ANY)

    @patch('selenium_ptvicomo_cookie_04.webdriver.Chrome')
    def test_initialize_driver_normal(self, mock_chrome):
        browser_manager = BrowserManager(head_less=False)
        mock_chrome.assert_called_once_with(service=browser_manager.service)

    @patch('selenium_ptvicomo_cookie_04.webdriver.Chrome')
    def test_initialize_browser(self, mock_chrome):
        browser_manager = BrowserManager(head_less=False)
        browser_manager.initialize_browser()
        browser_manager.driver.get.assert_called_once_with(WEBSITE_URL)
        browser_manager.driver.maximize_window.assert_called_once()

    @patch('selenium_ptvicomo_cookie_04.webdriver.Chrome')
    def test_set_cookies(self, mock_chrome):
        browser_manager = BrowserManager(head_less=False)
        cookies = [{'name': 'test_cookie', 'value': 'test_value'}]
        browser_manager.set_cookies(cookies)
        browser_manager.driver.add_cookie.assert_called_once_with(cookies[0])
        browser_manager.driver.get.assert_called_once_with(WEBSITE_URL)


class TestDataExtractor(unittest.TestCase):
    def setUp(self):
        self.driver = MagicMock()
        self.data_extractor = DataExtractor(self.driver)

    def test_get_day_of_week(self):
        self.assertEqual(self.data_extractor.get_day_of_week('number'), datetime.datetime.now().weekday())
        self.assertEqual(self.data_extractor.get_day_of_week('chinese'),
                         ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][
                             datetime.datetime.now().weekday()])

    def test_sale_action(self):
        self.driver.find_element.return_value.get_attribute.return_value = False
        self.driver.find_element.return_value.send_keys.return_value = None
        self.driver.find_element.return_value.click.return_value = None
        result = self.data_extractor.sale_action(10, 100, 50)
        self.assertEqual(result, 1000)

    def test_buy_action(self):
        self.driver.find_element.return_value.send_keys.return_value = None
        self.driver.find_element.return_value.click.return_value = None
        result = self.data_extractor.buy_action(10, 100)
        self.assertEqual(result, -1000)

    def test_get_current_time(self):
        current_time = self.data_extractor.get_current_time()
        self.assertEqual(current_time, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def test_get_hours_until_next_sunday(self):
        hours = self.data_extractor.get_hours_until_next_sunday()
        self.assertIsInstance(hours, int)

    def test_get_current_week(self):
        week_number = self.data_extractor.get_current_week()
        self.assertIsInstance(week_number, int)

    def test_extract_data_from_sunday_text(self):
        text = "胡萝卜的价格是100 剩余配货量为20"
        current_time = self.data_extractor.get_current_time()
        week_number = self.data_extractor.get_current_week()
        result = self.data_extractor.extract_data_from_sunday_text(text, current_time, week_number)
        self.assertEqual(result[0], "胡萝卜")
        self.assertEqual(result[1], 100)
        self.assertEqual(result[9], 20)

    def test_extract_data_from_weekday_text(self):
        text = "象岛新鲜蔬菜店 【胡萝卜】 市场单价：100 累计盈利 500 当前可卖数量为 20 成本：50"
        current_time = self.data_extractor.get_current_time()
        week_number = self.data_extractor.get_current_week()
        result = self.data_extractor.extract_data_from_weekday_text(text, current_time, week_number)
        self.assertEqual(result[0], "胡萝卜")
        self.assertEqual(result[1], 100)
        self.assertEqual(result[2], 500)
        self.assertEqual(result[3], 20)
        self.assertEqual(result[4], 50)

    def test_is_sale_condition_met(self):
        self.assertTrue(self.data_extractor.is_sale_condition_met(10, 15, 20))
        self.assertFalse(self.data_extractor.is_sale_condition_met(15, 5, 20))

    def test_build_return_value(self):
        result = self.data_extractor.build_return_value("胡萝卜", 100, 500, 20, 50, 1000, "sale", "2023-10-01 12:00:00",
                                                        40, 0, 20)
        self.assertEqual(result[0], "胡萝卜")
        self.assertEqual(result[1], 100)
        self.assertEqual(result[2], 500)
        self.assertEqual(result[3], 20)
        self.assertEqual(result[4], 50)
        self.assertEqual(result[5], 1000)
        self.assertEqual(result[6], "sale")
        self.assertEqual(result[7], "2023-10-01 12:00:00")
        self.assertEqual(result[8], 40)
        self.assertEqual(result[9], 0)
        self.assertEqual(result[10], 20)


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_config = {'host': 'localhost', 'user': 'user', 'password': 'password', 'database': 'test_db'}
        self.table_name = 'test_table'
        self.database_manager = DatabaseManager(self.db_config, self.table_name)

    @patch('mysql.connector.connect')
    def test_connect_to_mysql(self, mock_connect):
        mock_connect.return_value = MagicMock()
        conn = self.database_manager.connect_to_mysql()
        mock_connect.assert_called_once_with(host='localhost', user='user', password='password', database='test_db')
        self.assertIsNotNone(conn)

    @patch('mysql.connector.connect')
    def test_insert_data_to_mysql(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        data_tuple = ("胡萝卜", 100, 500, 20, 50, 1000, "sale", "2023-10-01 12:00:00", 40, 0, 20)
        self.database_manager.insert_data_to_mysql(mock_conn, data_tuple)
        mock_conn.cursor().execute.assert_called_once_with(
            "INSERT INTO test_table (名称,市场单价,累计盈利,当前可卖数量,成本,本周盈利,当前操作,当前时间,当前周数,剩余配货量,买卖数量) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s)",
            data_tuple
        )
        mock_conn.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_create_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        self.database_manager.create_table(mock_conn)
        mock_conn.cursor().execute.assert_called_once_with(
            "CREATE TABLE IF NOT EXISTS test_table (id INT auto_increment PRIMARY KEY, 名称 VARCHAR(255) NULL, 市场单价 INT NULL, 累计盈利 INT NULL, 当前可卖数量 INT NULL, 成本 INT NULL, 本周盈利 INT NULL, 当前操作 VARCHAR(255) NULL, 当前时间 VARCHAR(255) NULL, 当前周数 INT NULL, 剩余配货량 INT NULL, 买卖数量 INT NULL);"
        )
        mock_conn.commit.assert_called_once()


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.browser_manager = MagicMock()
        self.data_extractor = MagicMock()
        self.database_manager = MagicMock()
        self.application = Application()
        self.application.browser_manager = self.browser_manager
        self.application.data_extractor = self.data_extractor
        self.application.database_manager = self.database_manager

    @patch('selenium_ptvicomo_cookie_04.BrowserManager')
    @patch('selenium_ptvicomo_cookie_04.DataExtractor')
    @patch('selenium_ptvicomo_cookie_04.DatabaseManager')
    def test_main(self, mock_db_manager, mock_data_extractor, mock_browser_manager):
        self.application.main()
        self.browser_manager.initialize_browser.assert_called_once()
        self.browser_manager.set_cookies.assert_called_once_with(WEB_COOKIE)
        self.database_manager.connect_to_mysql.assert_called_once()
        self.database_manager.create_table.assert_called_once()
        self.data_extractor.get_data.assert_called_once()
        self.database_manager.insert_data_to_mysql.assert_called_once()


if __name__ == '__main__':
    unittest.main()
