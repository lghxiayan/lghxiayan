"""
象岛_数据采集配置文件
"""
import os
import platform


def get_chrome_driver_path():
    system = platform.system()
    if system == 'Windows':
        return os.getenv(
            'CHROME_DRIVER_PATH', 'D:\\google_chrome\\chromedriver-win64\\chromedriver.exe')
    elif system == 'Linux':
        return os.getenv(
            'CHROME_DRIVER_PATH', '/opt/chromedriver-linux64/chromedriver')
    else:
        raise EnvironmentError(f'不支持的操作系统：{system}')


CHROME_DRIVER_PATH = get_chrome_driver_path()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.112.13'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Lghgs2019'),
    'database': os.getenv('DB_NAME', 'easyspide'),
    'charset': 'utf8mb4'
}

TABLE_NAME = 'pt_vicomo_01'
WEB_COOKIE = [{'domain': 'ptvicomo.net', 'expiry': 1749262235, 'httpOnly': True, 'name': 'c_secure_login', 'path': '/',
               'sameSite': 'Lax', 'secure': False, 'value': 'bm9wZQ%3D%3D'},
              {'domain': 'ptvicomo.net', 'expiry': 1749262235, 'httpOnly': True, 'name': 'c_secure_tracker_ssl',
               'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'eWVhaA%3D%3D'},
              {'domain': 'ptvicomo.net', 'expiry': 1749262235, 'httpOnly': True, 'name': 'c_secure_ssl', 'path': '/',
               'sameSite': 'Lax', 'secure': False, 'value': 'eWVhaA%3D%3D'},
              {'domain': 'ptvicomo.net', 'expiry': 1749262235, 'httpOnly': True, 'name': 'c_secure_pass', 'path': '/',
               'sameSite': 'Lax', 'secure': False, 'value': '14c96bacdf049a639abbe1b38199655d'},
              {'domain': 'ptvicomo.net', 'expiry': 1749262235, 'httpOnly': True, 'name': 'c_secure_uid', 'path': '/',
               'sameSite': 'Lax', 'secure': False, 'value': 'MjI1MzM%3D'}]
# WEB_COOKIE = "c_secure_uid=MjI1MzM%3D; c_secure_pass=14c96bacdf049a639abbe1b38199655d; c_secure_ssl=eWVhaA%3D%3D; c_secure_tracker_ssl=eWVhaA%3D%3D; c_secure_login=bm9wZQ%3D%3D"

WEBSITE_URL = 'https://ptvicomo.net/customgame.php'
LOGIN_USERNAME = 'ledor2024'
LOGIN_PASSWORD = "VvyNFQ*!Q]Bv5^'"

WAIT_TIMEOUT = 5
# 卖出动作
CURRENT_ACTION = {'buy': '买入', 'sale': '卖出', 'get_data': '提取数据'}
# 买卖数量
SALE_NUMBER = 0
BUY_NUMBER = 450
# 卖出利润率
PROFIT_MARGIN = 30
# 保存页面
SAVE_PAGE = False
# 无头模式
HEAD_LESS = True
