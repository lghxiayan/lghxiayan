"""
从黄冈税务云平台网站取操作人员信息
会跟本地数据库进行比对,如果一致就不更新.
如果出现这样的提示：2024-07-19 21:49:52 | hgsw_log     | INFO     | requests_hgsw.py:33 | 响应内容: {'success': False}
是因为SESSION过期，需要重新登录。将新登录的JSESSIONID值更新到WEB_HEADERS中。
但现在我没办法使用requests获取该值，只能使用COOKIE中获取.在获取的过程中,必须关闭chrome.
[这条路走不通,requests登录后生成的JSESSIONID和从chrome cookie中取得的JSESSIONID是不同的...]
如果要获取得数据,必须要从chrome浏览器登录,从而使JSESSIONID生效.只取得该JSESSIONID值,是没有用的.
必须手动登录,获取JSESSIONID,然后更新到WEB_HEADERS中.
这样做至少比手工更新WEB_HEADERS中获取的JSESSIONID值,要好一点点.
还是要想办法获取requests登录成功后生成的JSESSIONID值.  TODO
"""
import requests
import json
import logging.config
from config_hgsw import DB_CONFIG, WEB_HEADERS, WEB_URL_LIST, SWJG_DM_LIST, SQL_INSERT_DATA, LOGIN_DATA, LOGIN_URL
from mysql.connector import connect, Error
from urllib.parse import parse_qs, urlparse
from browser_cookie3 import chrome

logging.config.fileConfig('logging_hgsw.conf', encoding='utf-8', disable_existing_loggers=False)
logger = logging.getLogger('hgsw_log')
logger.setLevel(logging.INFO)


def get_cookies():
    try:
        chrome_cookie = chrome(domain_name='84.52.16.1')
        logger.info(f"Cookie: {chrome_cookie}")
        return chrome_cookie
    except PermissionError:
        logger.error(f"无法读取 Cookie. 必须关闭chrome浏览器才能取得Cookie!")


def get_jsessionid(cookie):
    # 查找特定的cookie
    jsessionid_cookie = next((c for c in cookie if c.name == 'JSESSIONID'), None)
    if jsessionid_cookie:
        logger.info(f"JSESSIONID: {jsessionid_cookie.value}")
        return jsessionid_cookie.value
    else:
        logger.error("JSESSIONID not found")


def build_headers_with_jsessionid(jsessionid):
    new_headers = WEB_HEADERS.copy()
    new_headers['Cookie'] = f"JSESSIONID={jsessionid}"
    logger.info(f"新的请求头: {new_headers}")
    return new_headers


def get_data(conn, new_headers):
    if not WEB_URL_LIST:
        logger.info("URL列表为空，无数据可抓取")
        return

    session = requests.Session()
    login_response = session.post(LOGIN_URL, data=LOGIN_DATA, headers=new_headers)
    login_response.encoding = 'utf-8'
    # print(login_response.text)
    for url in WEB_URL_LIST:
        try:
            # logger.info(f"请求URL: {url}")
            # logger.info(f"请求头: {new_headers}")
            response = session.get(url, headers=new_headers)
            # logger.info(f"响应状态码: {response.status_code}")
            # response.encoding = "utf-8"
            # logger.info(f"响应内容: {response.text}")
            query = urlparse(response.url).query
            query_dict = parse_qs(query)
            swjg_dm = query_dict['swjg_dm'][0]
            swjg_mc = SWJG_DM_LIST.get(swjg_dm, '未知机构代码')

            data = response.json()
            # logger.info(f"响应内容: {data}")
            for row in data.get('rows', []):
                # logger.info(
                #     f"代码: {row['czry_dm']}, 名称: {row['czry_mc']}, 登录代码: {row['dldm']}, 有效标志: {row['xybz']}")
                if row['xybz'] == 'Y':
                    # logger.info(f"有效用户: {row['czry_mc']}")
                    check_and_insert_or_update_data(conn, row['czry_dm'], row['czry_mc'], row['dldm'], row['xybz'],
                                                    swjg_dm, swjg_mc)
        except json.JSONDecodeError:
            logger.error("响应内容不是有效的 JSON 格式")
        except requests.RequestException as e:
            logger.error(f"请求错误: {e}")
        except KeyError as e:
            logger.error(f"解析数据时遇到KeyError: {e}")
        except Exception as e:
            logger.error(f"其他错误: {e}")


def connect_to_mysql():
    """
    连接到MYSQL数据库
    :return: 返回数据库连接对象
    """
    try:
        conn = connect(**DB_CONFIG)
        logger.info("连接MYSQL数据库成功!")
        return conn
    except Error as error:
        logger.error(f"连接MYSQL数据库失败: {error}")
        return None


def check_and_insert_or_update_data(conn, czry_dm, czry_mc, dldm, xybz, swjg_dm, swjg_mc):
    """
    检查数据是否变动并执行插入或更新操作
    """
    select_sql = "SELECT * FROM hgsw_czry WHERE czry_dm = %s"
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(select_sql, (czry_dm,))
            existing_record = cursor.fetchone()
            # logger.info(f"查询结果: {existing_record}")
            if existing_record:
                update_needed = any(existing_record[field] != value for field, value in
                                    [('czry_mc', czry_mc), ('dldm', dldm), ('xybz', xybz), ('swjg_dm', swjg_dm),
                                     ('swjg_mc', swjg_mc)])
                if update_needed:
                    logger.info(f"数据已存在，更新数据: {existing_record}")
                    update_sql = ("UPDATE hgsw_czry SET czry_mc = %s, dldm = %s, xybz = %s, swjg_dm = %s, swjg_mc = %s "
                                  "WHERE czry_dm = %s")
                    update_values = (czry_mc, dldm, xybz, swjg_dm, swjg_mc, czry_dm)
                    cursor.execute(update_sql, update_values)
                    conn.commit()
                    logger.warning(f"数据已更新！czry_dm: {czry_dm} czry_mc: {czry_mc}")
                else:
                    logger.info(f"数据未变动，无需更新！czry_dm: {czry_dm} czry_mc: {czry_mc}")
            else:
                cursor.execute(SQL_INSERT_DATA, (czry_dm, czry_mc, dldm, xybz, swjg_dm, swjg_mc))
                conn.commit()
                logger.warning("数据插入成功！")
    except Error as error:
        logger.error(f"数据插入失败: {error}")
        conn.rollback()


if __name__ == '__main__':
    cookies = get_cookies()
    new_jsessionid = get_jsessionid(cookies)
    headers = build_headers_with_jsessionid(new_jsessionid)
    with connect_to_mysql() as my_conn:
        if my_conn is not None:
            get_data(my_conn, headers)
            my_conn.close()
        else:
            logger.error("无法连接到MYSQL数据库")
