# config_ptvicomo.py
import os

CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', 'D:\\google_chrome\\chromedriver-win64\\chromedriver.exe')
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.112.12'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Lghgs2023#'),
    'database': os.getenv('DB_NAME', 'pt'),
    'charset': 'utf8mb4'
}
WEB_COOKIE = [
    {'domain': 'ptvicomo.net', 'expiry': 1724921413, 'httpOnly': True, 'name': 'c_secure_login', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'bm9wZQ%3D%3D'},
    {'domain': 'ptvicomo.net', 'expiry': 1724921413, 'httpOnly': True, 'name': 'c_secure_tracker_ssl',
     'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'eWVhaA%3D%3D'},
    {'domain': 'ptvicomo.net', 'expiry': 1724921413, 'httpOnly': True, 'name': 'c_secure_ssl', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'eWVhaA%3D%3D'},
    {'domain': 'ptvicomo.net', 'expiry': 1724921413, 'httpOnly': True, 'name': 'c_secure_pass', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': '14c96bacdf049a639abbe1b38199655d'},
    {'domain': 'ptvicomo.net', 'expiry': 1724921413, 'httpOnly': True, 'name': 'c_secure_uid', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'MjI1MzM%3D'}]

WEBSITE_URL = 'https://ptvicomo.net/customgame.php'
WAIT_TIMEOUT = 5
