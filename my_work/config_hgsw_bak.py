"""
黄冈税务网站采集配置文件
"""
import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.112.13'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Lghgs2019'),
    'database': os.getenv('DB_NAME', 'easyspide'),
    'charset': 'utf8mb4'
}

WEB_URL_LIST = ['http://84.52.16.1/admin_user_gettable.action?swjg_dm=14211280000',
                'http://84.52.16.1/admin_user_gettable.action?swjg_dm=14211288500',
                'http://84.52.16.1/admin_user_gettable.action?swjg_dm=14211288100',
                'http://84.52.16.1/admin_user_gettable.action?swjg_dm=24211290300']

SWJG_DM_LIST = {'14211280000': '国家税务总局黄冈市税务局龙感湖管理区税务分局',
                '14211288500': '龙感湖税务分局税源管理股',
                '14211288100': '龙感湖税务分局办公室', '24211290300': '龙感湖税务分局综合业务股'}

WEB_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "http://84.52.16.1",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "http://84.52.16.1/s-admin/org-user.html?v=20191202",
    "Cookie": "JSESSIONID=0fF4mfsTQJMjtYHlGxR22pvk9ph2yMLFDkmzphLF4GGLXg5TQ0VS!-2102725246"  # 替换为实际的会话ID

}

LOGIN_DATA = {
    'dldm': 'j289103',
    'dlmm': 'xia11111111',
}

# 定义的SQL插入语句
SQL_INSERT_DATA = "INSERT INTO hgsw_czry (czry_dm, czry_mc, dldm, xybz,swjg_dm,swjg_mc) VALUES (%s, %s, %s, %s,%s,%s)"
