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
from mysql.connector import connect, Error
# 导入配置文件常量
from config_ptvicomo_02 import CHROME_DRIVER_PATH, DB_CONFIG, WEB_COOKIE, WEBSITE_URL, WAIT_TIMEOUT, TABLE_NAME, \
    CURRENT_ACTION, SALE_NUMBER, BUY_NUMBER

# 导入日志配置文件
logging.config.fileConfig('logging_ptvicomo.conf', encoding='utf-8')
logger = logging.getLogger('ptvicomo_log')

# 定义Chrome驱动程序路径，使用环境变量或默认路径
chrome_driver_path = CHROME_DRIVER_PATH
# 初始化Chrome浏览器驱动服务
service = Service(chrome_driver_path)
# 创建Chrome浏览器实例
driver = webdriver.Chrome(service=service)

# 预编译正则表达式，用于匹配购买和销售的相关信息
buy_name_pattern = re.compile('[\u4e00-\u9fff]+(?=的价格是)')
buy_price_pattern = re.compile(r"(?<=价格是)\d+")
buy_other_number_pattern = re.compile(r"(?<= 剩余配货量为)\d+")

sale_name_pattern = re.compile(r"(?<=象岛新鲜蔬菜店 【)(.+)(?=\s市场单价)")
sale_price_pattern = re.compile(r"(?<=市场单价：)\d+")
sale_total_profit_pattern = re.compile(r"(?<=累计盈利 )\d+")
sale_current_number_pattern = re.compile(r"(?<=当前可卖数量为 )\d+")
sale_cost_pattern = re.compile(r"(?<=成本：)\d+")


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


def get_day_of_week(date_format='number'):
    """
    获取当前日期是星期几
    :param date_format: 返回星期几的格式，可以是数字（0-6）或中文
    :return: 当前日期是星期几
    """
    today = datetime.datetime.now()
    day_of_week = today.weekday()

    if date_format == 'number':
        return day_of_week
    elif date_format == 'chinese':
        days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        return days[day_of_week]
    else:
        raise ValueError("Invalid format. Use 'number' or 'chinese'.")


def sale_action(number, sale_price, sale_cost):
    """
    执行卖出操作
    :param number: 卖出的数量
    :param sale_price: 单价
    :param sale_cost: 成本
    :return: 单笔盈利
    """
    try:
        logger.info(f'当前卖出数量{number}')
        driver.find_element(By.XPATH, '//input[@name="saleTurnipNum"]').send_keys(number)
        driver.find_element(By.XPATH, '//input[@value="出售"]').click()
        logger.info(f"点击出售按钮成功,出售数量为{number}")
        # 计算单笔盈利
        sale_profit = (sale_price - sale_cost) * number
        logger.info(f'计算【单笔盈利】成功：{sale_profit}')
        sale_action_name = CURRENT_ACTION['sale']
        logger.info(f'获取【当前操作】成功：{sale_action_name}')
        return sale_profit
    except Exception as e:
        logger.error(f"点击出售按钮失败: {e}")


def buy_action(number, buy_price):
    """
    执行买入操作
    :param number: 买入的数量
    :param buy_price: 单价
    :return: 总购买金额（负数表示购买花费）
    """
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


def hours_until_next_sunday():
    """
    计算距离下周星期天的剩余小时数
    :return: 距离下周星期天剩余的小时数
    """
    now = datetime.datetime.now()
    next_sunday = now + datetime.timedelta(days=(6 - now.weekday()) % 7)
    next_sunday = next_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
    remaining = (next_sunday - now).total_seconds() / 3600
    return remaining


def get_current_week():
    """
    获取当前是今年的第几周
    :return: 当前周数
    """
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


def extract_data_from_sunday_text(text, current_time, week_number):
    """
    从星期天的页面文本中提取购买相关信息
    :param text: 星期天页面的文本内容
    :param current_time: 当前时间
    :param week_number: 当前周数
    :return: 蔬菜名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数, 剩余配货量
    """
    # 获取名称
    buy_name = buy_name_pattern.findall(text)[0]
    logger.info(f'获取【蔬菜名称】成功:{buy_name}')
    # 获取市场单价
    buy_price = buy_price_pattern.findall(text)[0]
    buy_price = int(buy_price)
    logger.info(f'获取【市场单价】成功:{buy_price}')
    # 获取剩余配货量
    buy_other_number = buy_other_number_pattern.findall(text)[0]
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
                buy_total_money, buy_action_name, current_time, week_number, buy_other_number)


def extract_data_from_weekday_text(text, current_time, week_number):
    """
    从非星期天的页面文本中提取销售相关信息
    :param text: 非星期天页面的文本内容
    :param current_time: 当前时间
    :param week_number: 当前周数
    :return: 蔬菜名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数, 剩余配货量
    """
    try:
        # 获取名称
        # sale_name_pattern = r"(?<=象岛新鲜蔬菜店 【)(.+)(?=\s市场单价)"
        sale_name = sale_name_pattern.findall(text)[0]
        logger.info(f'获取【名称】成功:{sale_name}')
        # 获取市场单价
        sale_price = sale_price_pattern.findall(text)[0]
        sale_price = int(sale_price)
        logger.info(f'获取【市场单价】成功:{sale_price}')
        # 获取累计盈利
        sale_total_profit = sale_total_profit_pattern.search(text).group()
        sale_total_profit = int(sale_total_profit)
        logger.info(f'获取【累计盈利】成功：{sale_total_profit}')
        # 获取当前可卖数量，即库存
        sale_current_number = sale_current_number_pattern.search(text).group()
        sale_current_number = int(sale_current_number)
        logger.info(f'获取【当前可卖数量】成功：{sale_current_number}')
        # 获取成本
        sale_cost = sale_cost_pattern.search(text).group()
        sale_cost = int(sale_cost)
        logger.info(f'获取【成本】成功：{sale_cost}')
        # 出售动作
        # 如果距离星期天还不到12个小时,或者,当前利润超过10%,清仓
        if hours_until_next_sunday() < 12 or sale_price / sale_cost > 1.1:
            sale_profit = sale_action(sale_current_number, sale_price, sale_cost)
            return (sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                    sale_profit, '卖出', current_time, week_number, 0)
        elif sale_current_number > 0 and sale_current_number >= SALE_NUMBER > 0:
            sale_profit = sale_action(SALE_NUMBER, sale_price, sale_cost)
            # 返回：名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数, 剩余配货量
            return (sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                    sale_profit, '卖出', current_time, week_number, 0)
        else:
            sale_profit = 0
            # logger.info(f'计算【单笔盈利】成功：{sale_profit}')
            sale_action_name = CURRENT_ACTION['get_data']
            logger.info(f'获取【当前操作】成功：{sale_action_name}')
            return (sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                    sale_profit, sale_action_name, current_time, week_number, 0)
    except Exception as e:
        logger.error(f'获取数据失败:{e}')


def get_data():
    """
    从网页获取交易数据。

    返回:
    - 如果找到数据，则返回一个包含名称、价格和盈利的元组。
    - 如果找不到数据或出现异常，则返回None。
    """
    """
    从网页获取指定数据，并返回
    :return: 返回数据的元组，包括名称、价格和累计盈利
    """
    # 获取当前是星期几
    # 获取当天是星期几
    day_of_week = get_day_of_week('chinese')
    logger.info(f'获取【星期几】成功:{day_of_week}')
    # 获取当前时间
    # 获取当前时间
    current_time = get_current_time()
    logger.info(f'获取【当前时间】成功:{current_time}')
    # 获取当前周数
    # 获取当前周数
    week_number = get_current_week()
    logger.info(f'获取【当前周数】成功:{week_number}')
    try:
        # 尝试查找星期天的数据元素
        # 获取星期天详细数据
        sunday_element = driver.find_elements(By.XPATH, '//*[@id="buyTurnipSunday"]')
        # 如果找到，则处理并返回星期天的数据
        if sunday_element:
            sunday_text = sunday_element[0].text
            logger.info(sunday_text)
            return extract_data_from_sunday_text(sunday_text, current_time, week_number)
        # 如果没找到星期天的数据，尝试查找工作日的数据元素
        else:
            weekday_element = driver.find_elements(By.XPATH, '//*[@id="saleTurnip"]')
            # 如果找到，则处理并返回工作日的数据
            if not weekday_element:
                logger.warning("今天不是星期天,也找不到非星期天的相关数据")
                return None
            weekday_text = weekday_element[0].text
            return extract_data_from_weekday_text(weekday_text, current_time, week_number)
    except NoSuchElementException:
        logger.error('找不到必要的元素')
    except Exception as e:
        logger.error(f'获取数据失败:{e}')
    return None


def connect_to_mysql():
    """
    连接到MySQL数据库。

    返回:
    - 如果连接成功，则返回数据库连接对象。
    - 如果连接失败，则返回None。
    """
    """
    连接到MYSQL数据库
    :return: 返回数据库连接对象
    """
    try:
        conn = connect(**DB_CONFIG)
        logger.info("连接到 MYSQL 成功!")
        return conn
    except Error as error:
        logger.info(f"连接到 MYSQL 失败: {error}")
        return None


def query_from_mysql(conn):
    """
    从MySQL数据库中查询所有数据。

    参数:
    - conn: 数据库连接对象。
    """
    """
    从数据库中查询数据
    :param conn: 数据库连接对象
    """
    cursor = conn.cursor()
    cursor.execute(f'select * from {TABLE_NAME}')
    db_result = cursor.fetchall()
    for row in db_result:
        row_data = list(row)
        logger.info(f'{row_data}')


def insert_data_to_mysql(conn, data_tuple):
    """
    向MySQL数据库插入数据。

    参数:
    - conn: 数据库连接对象。
    - data_tuple: 包含要插入的数据的元组。
    """
    """
    向数据库中插入数据
    """
    insert_data_query = (
        f"INSERT INTO {TABLE_NAME} (名称,市场单价,累计盈利,当前可卖数量,成本,本周盈利,当前操作,当前时间,当前周数,剩余配货量) "
        f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)")
    with conn.cursor() as cursor:
        cursor.execute(insert_data_query, data_tuple)
        conn.commit()
        logger.info("数据插入成功！")
        logger.info('-' * 30)


if __name__ == '__main__':
    initialize_browser()
    set_cookies(WEB_COOKIE)
    my_conn = connect_to_mysql()
    if my_conn is not None:
        # query_from_mysql(my_conn)
        data = get_data()
        if data is not None:
            insert_data_to_mysql(my_conn, data)
        else:
            logger.error("无法获取数据，数据未插入")
    else:
        logger.error("无法连接到数据库,未进行数据插入")

    driver.close()
    driver.quit()
