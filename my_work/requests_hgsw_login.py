import requests
import json
import logging.config
# from config_hgsw import DB_CONFIG, WEB_HEADERS, WEB_URL_LIST, SWJG_DM_LIST, SQL_INSERT_DATA, LOGIN_DATA
from mysql.connector import connect, Error
from urllib.parse import parse_qs, urlparse

logging.config.fileConfig('logging_hgsw.conf', encoding='utf-8', disable_existing_loggers=False)
logger = logging.getLogger('hgsw_log')
logger.setLevel(logging.DEBUG)

WEB_URL_LIST = ['http://84.52.16.1/s-admin/login.html?v=20191023',
                'http://84.52.16.1/admin_user_gettable.action?swjg_dm=14211280000',
                'http://84.52.16.1/admin_user_gettable.action?swjg_dm=14211288500',
                'http://84.52.16.1/admin_user_gettable.action?swjg_dm=14211288100',
                'http://84.52.16.1/admin_user_gettable.action?swjg_dm=24211290300']

# WEB_HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
#     "Accept": "application/json, text/javascript, */*; q=0.01",
#     "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
#     "Accept-Encoding": "gzip, deflate",
#     "X-Requested-With": "XMLHttpRequest",
#     "Origin": "http://84.52.16.1",
#     "DNT": "1",
#     "Connection": "keep-alive",
#     "Referer": "http://84.52.16.1/s-admin/index.html?v=20200116",
#     "Cookie": "JSESSIONID=14hTmZ5PXCc20J7pqJj3ntpLzCBr7rLqM5x1LJRqT8wDrZ78tJd4!-2102725246"  # 替换为实际的会话ID
# }

WEB_HEADERS = {
    'Host': '84.52.16.1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'http://84.52.16.1/s-admin/index.html?v=20200116',
    'Cookie': 'JSESSIONID=6G91mhmVLfJ4TV2V11htnypD3LX83n0QncLgwnf9hQLHTsZyBKK4!-2102725246'}

LOGIN_DATA = {
    'dldm': 'j289103',
    'dlmm': 'xia11111111',
}

COOKIE_NAME = WEB_HEADERS['Cookie']


def update_web_headers_with_cookie(new_cookie_value):
    global WEB_HEADERS
    WEB_HEADERS['Cookie'] = f"JSESSIONID={new_cookie_value}"
    print(f"更新后的Cookie: {WEB_HEADERS['Cookie']}")


# 会话有效性检查
def is_cookie_valid(session):
    if COOKIE_NAME in session and check_session_validity(session[COOKIE_NAME]):
        return True
    return False


# 示例会话有效性检查函数
def check_session_validity(session_id):
    # 这里应该实现与后端服务的交互验证会话ID
    return True


# 登录函数
def login_to_web(data=None):
    try:
        if "Cookie" in WEB_HEADERS:
            headers = WEB_HEADERS.copy()
            response = requests.post(WEB_URL_LIST[0], headers=headers)
            response.raise_for_status()
            # logger.debug(f"登录响应内容: {response.text}")
        else:
            response = requests.post(WEB_URL_LIST[0], headers=WEB_HEADERS, data=data)
            response.raise_for_status()
            logger.debug(f"登录响应内容: {response.text}")
            logger.info("登录成功")
            logger.info(f"登录响应状态码: {response.status_code}")

        cookies = response.cookies
        jsessionid = cookies.get('JSESSIONID')

        if jsessionid:
            print(f"登录成功，JSESSIONID: {jsessionid}")
            update_web_headers_with_cookie(jsessionid)
        else:
            print("登录失败未找到JSESSIONID")
    except requests.RequestException as e:
        logger.error(f"网络请求错误: {e}")
    except Exception as e:
        logger.error(f"其他错误: {e}")


# 主程序
print(is_cookie_valid(WEB_HEADERS))
if not is_cookie_valid(WEB_HEADERS):
    login_to_web(LOGIN_DATA)
