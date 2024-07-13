"""
该脚本使用Selenium自动化进行网页操作，具体流程如下：
1. 打开指定网址并登陆；
2. 点击进入子系统，选择特定的页面；
3. 在页面上填写信息、选择接收对象，并发送信息；
4. 完成后关闭浏览器。

注意：该脚本依赖于具体的网页结构和元素ID、CSS选择器等，若网页结构发生变化，脚本可能无法正常工作。
"""
import logging.config
import re
import time

# 导入Selenium相关模块，用于自动化浏览器操作
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# 导入MySQL连接模块，用于数据库操作
from mysql import connector

from config_ptvicomo import CHROME_DRIVER_PATH, DB_CONFIG, WEB_COOKIE, WEBSITE_URL, WAIT_TIMEOUT

# 定义Chrome驱动程序路径，使用环境变量或默认路径
chrome_driver_path = CHROME_DRIVER_PATH

# 定义数据库配置信息，使用环境变量或默认值
db_config = DB_CONFIG
my_cookies = WEB_COOKIE
logging.config.fileConfig('logging_ptvicomo.conf', encoding='utf-8')
logger = logging.getLogger('ptvicomo_log')

# 初始化Chrome浏览器驱动服务
service = Service(chrome_driver_path)
# 创建Chrome浏览器实例
driver = webdriver.Chrome(service=service)
# 定义目标网址
my_url = WEBSITE_URL


def initialize_browser():
    """
    初始化浏览器，打开目标网址并最大化窗口
    """
    global driver
    driver.get(my_url)
    WebDriverWait(driver, WAIT_TIMEOUT).until(ec.presence_of_element_located((By.XPATH, '//body')))
    driver.maximize_window()


def my_get_cookies():
    """
    打印当前浏览器会话的所有Cookies
    """
    try:
        logger.info(driver.get_cookies())
    except NoSuchElementException:
        logger.error("NoSuchElementException")


def my_set_cookies(cookies):
    """
    设置Cookies到浏览器会话
    :param cookies: 需要设置的Cookies列表
    """
    global driver
    for cookie in cookies:
        driver.add_cookie(cookie)
    # 再次访问网页，这时应该已经应用了Cookies
    driver.get(my_url)


def my_get_data():
    """
    从网页获取指定数据，并返回
    :return: 返回数据的元组，包括名称、价格和累计盈利
    """
    # 取第6栏数据，累计盈利
    try:
        sale_turnip_element = WebDriverWait(driver, WAIT_TIMEOUT).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="saleTurnip"]')))
        sale_turnip_text = sale_turnip_element.text
        sale_turnip_text = re.findall(r"(?<=累计盈利 )(.+?)(?=盈利目标)", sale_turnip_text)[
            0]  # findall函数输出的是List,我加了下标，就是string
        pattern = re.compile(r'[\u4e00-\u9fff\s]+', re.UNICODE)
        cleaned_string = pattern.sub('', sale_turnip_text)
        total = int(float(cleaned_string))
    except Exception as e:
        logger.error('无法获取累计盈利数据!')
        logger.exception(e)
        return None, None, 0

    try:
        # 取第5栏数据，如果为开售中，取第5栏数据，名称和价格；否则取第6栏数据，名称和价格
        sunday_text = driver.find_element(By.XPATH, '//*[@id="buyTurnipSunday"]').text
        if sunday_text:
            logger.info(sunday_text)
            # pattern = re.search(r'休息日', sunday_text)
            # sunday_text = sunday_text.replace('休息日】 ', '')
            name = re.findall(r'[\u4e00-\u9fff]+(?=的价格是)', sunday_text)[0]
            price = int(float(re.findall(r'\d+\.\d+', sunday_text)[0]))
            logger.info(name, price, total)
            return name, price, total

    except NoSuchElementException:
        try:
            turnip_text = driver.find_element(By.XPATH, '//*[@id="saleTurnip"]/h1').text
            name = re.findall(r"(?<=象岛新鲜蔬菜店 【)(.+?)(?= 市场单价)", turnip_text)[0]
            price = re.findall(r"(?<=市场单价：)(.+?)(?=库存)", turnip_text)[0]
            price = int(float(price))
            if name:
                return name, price, total
            else:
                logger.error("No matches found.")
                return None, None, total
        except NoSuchElementException:
            logger.info("No matches found.")


def connect_to_mariadb():
    """
    连接到MariaDB数据库
    :return: 返回数据库连接对象
    """
    try:
        conn = connector.connect(**db_config)
        logger.info("Connected to MariaDB successfully!")
        return conn
    except connector.Error as error:
        logger.info(f"Failed to connect to MariaDB: {error}")
        return None


def query_from_mariadb(conn):
    """
    从数据库中查询数据
    :param conn: 数据库连接对象
    """
    cursor = conn.cursor()
    cursor.execute('select * from ptvicomo')
    db_result = cursor.fetchall()
    for row in db_result:
        my_id, name, datetime, price, total = row
        formatted_datetime = datetime.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{my_id}, {name}, {formatted_datetime}, {price}, {total}")


def insert_data_to_mariadb(conn, sale_name, sale_price, sale_total):
    """
    向数据库中插入数据
    :param conn: 数据库连接对象
    :param sale_name: 销售名称
    :param sale_price: 销售价格
    :param sale_total: 销售累计盈利
    """
    my_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    cursor = conn.cursor()
    insert_data_query = "INSERT INTO ptvicomo (name,datetime, price,total) VALUES (%s, %s, %s, %s)"
    user_data = (sale_name, my_date, sale_price, sale_total)
    cursor.execute(insert_data_query, user_data)
    conn.commit()
    logger.info("数据插入成功！")
    logger.info('-' * 30)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    initialize_browser()
    my_set_cookies(my_cookies)
    my_conn = connect_to_mariadb()
    if my_conn:
        # query_from_mariadb(my_conn)
        my_name, my_price, my_total = my_get_data()
        if my_price is not None:
            insert_data_to_mariadb(my_conn, my_name, my_price, my_total)
        else:
            logger.error("无法获取销售价格，数据未插入")

    # time.sleep(5)
    # 关闭浏览器
    driver.close()
    driver.quit()
