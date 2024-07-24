"""
该脚本使用Selenium自动化进行网页操作，具体流程如下：
1. 使用cookie打开指定网址；
2. 根据页面元素是否显示，来判断是否为星期天。
3. 如果是，则采集页面元素A，并根据信息进行判断，是否买入
4. 如果不是，则采集页面元素B，并根据信息进行判断，是否卖出
5. 在买入或卖出后，会刷新页面。再次采集页面元素，用以判断其它数据，例如这次买了多少，卖了多少，该次操作盈利多少，
6. 将数据写入MySQL数据库。
7. 完成后关闭浏览器。

"""
import logging.config
import re
import datetime
# 导入Selenium相关模块，用于自动化浏览器操作
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from mysql import connector
# 导入配置文件常量
from config_ptvicomo_02 import CHROME_DRIVER_PATH, DB_CONFIG, WEB_COOKIE, WEBSITE_URL, WAIT_TIMEOUT, TABLE_NAME, \
    CURRENT_ACTION

# 导入日志配置文件
logging.config.fileConfig('logging_ptvicomo.conf', encoding='utf-8')
logger = logging.getLogger('ptvicomo_log')

# 定义Chrome驱动程序路径，使用环境变量或默认路径
chrome_driver_path = CHROME_DRIVER_PATH
# 初始化Chrome浏览器驱动服务
service = Service(chrome_driver_path)
# 创建Chrome浏览器实例
driver = webdriver.Chrome(service=service)

# 卖出数量
SALE_NUMBER = 1
BUY_NUMBER = 1


def initialize_browser():
    """
    初始化浏览器，打开目标网址并最大化窗口
    """
    global driver
    driver.get(WEBSITE_URL)
    WebDriverWait(driver, WAIT_TIMEOUT).until(ec.presence_of_element_located((By.XPATH, '//body')))
    driver.maximize_window()


def get_cookies():
    """
    打印当前浏览器会话的所有Cookies
    """
    try:
        logger.info(driver.get_cookies())
    except NoSuchElementException:
        logger.error("NoSuchElementException")


def set_cookies(cookies):
    """
    设置Cookies到浏览器会话
    :param cookies: 需要设置的Cookies列表
    """
    global driver
    for cookie in cookies:
        driver.add_cookie(cookie)
    # 再次访问网页，这时应该已经应用了Cookies
    driver.get(WEBSITE_URL)


def sale_action(number, sale_price, sale_cost):
    try:
        driver.find_element(By.XPATH, '//input[@name="saleTurnipNum"]').send_keys(number)
        driver.find_element(By.XPATH, '//input[@value="出售"]').click()
        logger.info(f"点击出售按钮成功,出售数量为{number}")

        # 计算单笔盈利
        sale_profit = (sale_price - sale_cost) * number
        logger.info(f'计算【单笔盈利】成功：{sale_profit}')
        return sale_profit
    except Exception as e:
        logger.error(f"点击出售按钮失败: {e}")


def buy_action(number, buy_price):
    try:
        driver.find_element(By.XPATH, '//input[@name="buyTurnipNum"]').send_keys(number)
        driver.find_element(By.XPATH, '//input[@value="进货"]').click()
        buy_total_money = -buy_price * number
        logger.info(f"点击购买按钮成功,购买数量为{number},购买单价{buy_price},购买总金额为{buy_total_money}")
        return buy_total_money
    except Exception as e:
        logger.error(f"点击购买按钮失败: {e}")


def get_current_time():
    """
    获取当前时间，格式为：年-月-日 时:分:秒
    :return: 当前时间字符串
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def get_current_week():
    # 获取当前日期
    today = datetime.date.today()

    # 计算年份
    year = today.year

    # 计算周数，从周日开始计算
    # weekday() 方法返回的是星期几，星期一是0，星期日是6
    # 因此，如果今天是周日，则周数加1
    # 如果今天是一年的第一天且是周日，则已经是第一周了
    if today.weekday() == 6:
        week_number = (today - datetime.date(year, 1, 1)).days // 7 + 1
    else:
        # 如果今天不是周日，找到最近的周日
        last_sunday = today - datetime.timedelta(days=today.weekday() + 1)
        # 计算周数
        week_number = (last_sunday - datetime.date(year, 1, 1)).days // 7 + 1

    return week_number


def get_data():
    """
    从网页获取指定数据，并返回
    :return: 返回数据的元组，包括名称、价格和累计盈利
    """
    # 获取当前时间
    current_time = get_current_time()
    logger.info(f'获取【当前时间】成功:{current_time}')
    # 获取当前周数
    week_number = get_current_week()
    logger.info(f'获取【当前周数】成功:{week_number}')
    try:
        # 获取星期天详细数据
        buy_text = driver.find_element(By.XPATH, '//*[@id="buyTurnipSunday"]').text
        logger.info(buy_text)
        # 尝试获取星期天才会出现的元素，如果存在，则说明是星期天，返回True
        # 如果为开售中，取第6栏数据；否则取第7栏数据
        if buy_text:
            # 获取名称
            buy_name_pattern = '[\u4e00-\u9fff]+(?=的价格是)'
            buy_name = re.findall(buy_name_pattern, buy_text)[0]
            logger.info(f'获取【蔬菜名称】成功:{buy_name}')
            # 获取市场单价
            buy_price_pattern = r"(?<=价格是)\d+"
            buy_price = re.findall(buy_price_pattern, buy_text)[0]
            buy_price = int(buy_price)
            logger.info(f'获取【市场单价】成功:{buy_price}')
            # 获取剩余配货量
            buy_other_number_pattern = "(? <= 剩余配货量为)(. +?)(?=kg)"  # todo = 这句应该有问题。
            buy_other_number = re.findall(buy_other_number_pattern, buy_text)[0]
            buy_other_number = int(buy_other_number)
            logger.info(f'获取【剩余配货量】成功:{buy_other_number}')

            # 购买动作
            if buy_other_number > 0:
                # 计算总购买金额
                logger.info(f'当前购买数量{buy_other_number}')
                buy_total_money = buy_action(BUY_NUMBER, buy_price)
                logger.info(f'购买成功，购买总金额为{buy_total_money}')
                buy_action_name = CURRENT_ACTION['buy']
                logger.info(f'获取【当前操作】成功：{buy_action_name}')
                # 返回：名称, 市场单价, 累计盈利, 当前可卖数量, 成本,
                # 单笔盈利, 当前操作, 当前时间, 当前周数
                return (buy_name, buy_price, 0, 0, buy_price,
                        buy_total_money, buy_action_name, current_time, week_number)

    except NoSuchElementException:
        logger.warning("今天不是星期天.")

        try:
            # 获取非星期天详细数据
            sale_text = driver.find_element(By.XPATH, '//*[@id="saleTurnip"]').text
            # 如果找到，则说明不是星期天，返回True。会继续下面的代码
            if sale_text:
                """
                象岛新鲜蔬菜店 【鲜红象胡萝卜条 市场单价：536.0 库存：146 成本：523.0】
                价格每天0:00和12:00波动一次，保质期至周六晚24:00 鲜红象胡萝卜条~ 鲜红象胡萝卜条~ 能涨价就太好了~~
                开店累计盈利 67886.0 盈利目标 380000(净利润上限, 随用户等级增加)
                
                输入出售数量当前可卖数量为 146 点击出售 ! (超过盈利目标后盈利的库存会自动原价卖出)
                """
                # 获取名称
                sale_name_pattern = r"(?<=象岛新鲜蔬菜店 【)(.+)(?=\s市场单价)"
                sale_name = re.findall(sale_name_pattern, sale_text)[0]
                logger.info(f'获取【名称】成功:{sale_name}')
                # 获取市场单价
                sale_price_pattern = r"(?<=市场单价：)\d+"
                sale_price = re.findall(sale_price_pattern, sale_text)[0]
                sale_price = int(sale_price)
                logger.info(f'获取【市场单价】成功:{sale_price}')
                # 获取累计盈利
                sale_total_profit_pattern = r"(?<=累计盈利 )\d+"
                sale_total_profit = re.search(sale_total_profit_pattern, sale_text).group()
                sale_total_profit = int(sale_total_profit)
                logger.info(f'获取【累计盈利】成功：{sale_total_profit}')
                # 获取当前可卖数量，即库存
                sale_current_number_pattern = r"(?<=当前可卖数量为 )\d+"
                sale_current_number = re.search(sale_current_number_pattern, sale_text).group()
                sale_current_number = int(sale_current_number)
                logger.info(f'获取【当前可卖数量】成功：{sale_current_number}')
                # 获取成本
                sale_cost_pattern = r"(?<=成本：)\d+"
                sale_cost = re.search(sale_cost_pattern, sale_text).group()
                sale_cost = int(sale_cost)
                logger.info(f'获取【成本】成功：{sale_cost}')
                # 出售动作
                if sale_current_number > 0 and sale_current_number >= SALE_NUMBER > 0:
                    # 计算单笔盈利
                    logger.info(f'当前卖出数量{SALE_NUMBER}')
                    sale_profit = sale_action(SALE_NUMBER, sale_price, sale_cost)
                    logger.info(f'计算【单笔盈利】成功：{sale_profit}')
                    sale_action_name = CURRENT_ACTION['sale']
                    logger.info(f'获取【当前操作】成功：{sale_action_name}')
                    # 返回：名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数
                    return (sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                            sale_profit, sale_action_name, current_time, week_number)
                else:
                    sale_profit = 0
                    # logger.info(f'计算【单笔盈利】成功：{sale_profit}')
                    sale_action_name = CURRENT_ACTION['get_data']
                    logger.info(f'获取【当前操作】成功：{sale_action_name}')
                    return (sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                            sale_profit, sale_action_name, current_time, week_number)
        except Exception as e:
            logger.error(f'获取数据失败:{e}')


def connect_to_mysql():
    """
    连接到MYSQL数据库
    :return: 返回数据库连接对象
    """
    try:
        conn = connector.connect(**DB_CONFIG)
        logger.info("连接到 MYSQL 成功!")
        return conn
    except connector.Error as error:
        logger.info(f"连接到 MYSQL 失败: {error}")
        return None


def query_from_mysql(conn):
    """
    从数据库中查询数据
    :param conn: 数据库连接对象
    """
    cursor = conn.cursor()
    cursor.execute(f'select * from {TABLE_NAME}')
    db_result = cursor.fetchall()
    for row in db_result:
        data = list(row)
        名称 = data[0]
        成本 = data[1]
        累计盈利 = data[2]
        当前可卖数量 = data[3]
        市场单价 = data[4]
        当前时间 = data[5]
        剩余配货量 = data[6]
        当前周数 = data[7]
        当前操作 = data[8]
        本周盈利 = data[9]
        logger.info(f'{名称},{成本},{累计盈利},{当前可卖数量},{市场单价},{当前时间},'
                    f'{剩余配货量},{当前周数},{当前操作},{本周盈利}')


def insert_data_to_mysql(conn, sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                         sale_profit, sale_action_name, current_time, week_number):
    """
    向数据库中插入数据
    """

    cursor = conn.cursor()
    insert_data_query = (
        f"INSERT INTO {TABLE_NAME} (名称,市场单价,累计盈利,当前可卖数量,成本,本周盈利,当前操作,当前时间,当前周数) "
        f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    user_data = (sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                 sale_profit, sale_action_name, current_time, week_number)
    cursor.execute(insert_data_query, user_data)
    conn.commit()
    logger.info("数据插入成功！")
    logger.info('-' * 30)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    initialize_browser()
    set_cookies(WEB_COOKIE)
    my_conn = connect_to_mysql()
    if my_conn:
        # query_from_mysql(my_conn)
        (sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
         sale_profit, sale_action_name, current_time, week_number) = get_data()
        if sale_name is not None:
            insert_data_to_mysql(my_conn, sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                                 sale_profit, sale_action_name, current_time, week_number)
        else:
            logger.error("无法获取名称，数据未插入")

    driver.close()
    driver.quit()
