"""
该脚本使用Selenium自动化进行网页操作，具体流程如下：
1. 使用cookie打开指定网址；
2. 根据页面元素是否显示，来判断是否为星期天。
3. 如果是，则采集页面元素A，并根据信息进行判断，是否买入
4. 如果不是，则采集页面元素B，并根据信息进行判断，是否卖出
5. 在买入或卖出后，会刷新页面。再次采集页面元素，用以判断其它数据，例如这次买了多少，卖了多少，该次操作盈利多少，
6. 将数据写入MySQL数据库。
7. 完成后关闭浏览器。


改进：
还是要做web界面。里面一定在有这两个按钮：立即卖出，立即买入。或者一个按钮【立即执行】
碰到过好几次cookie失效，只要重新运行本程序（需要关闭无头模式才行）进行登录，会自动更新cookie。登录完成后就可以继续启用无头模式了。

这里可以改进为：
一种是：直接使用用户名密码登录，但要进行验证码认证，这个涉及到图形识别模块。（这种方式更好）。AI回答说频繁登录并不是一个好主意。每天登录只登录一次？
另一种是：先用cookie登录，如果提示“无法取得数据”，则提示【手工登录】。

还有一个就是：检测数据库记录，每1个小时检测一次，是否有本周期的数据。没有的话，则采集数据。


现在象岛首页增加了蔬菜的走势图，应该可以通过selenium来抓取。
"""

import json
import logging.config
import re
import datetime
import platform
import time

# 导入Selenium相关模块，用于自动化浏览器操作
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from mysql.connector import connect, Error

# 导入配置文件常量
from config_ptvicomo_04 import CHROME_DRIVER_PATH, DB_CONFIG, WEB_COOKIE, WEBSITE_URL, WAIT_TIMEOUT, TABLE_NAME, \
    CURRENT_ACTION, SALE_NUMBER, BUY_NUMBER, PROFIT_MARGIN, SAVE_PAGE, HEAD_LESS

# 导入日志配置文件
logging.config.fileConfig('logging_ptvicomo.conf', encoding='utf-8')
logger = logging.getLogger('ptvicomo_log')
logger.setLevel(logging.INFO)
# logger = logging.getLogger('app_log')

# 定义Chrome驱动程序路径，使用环境变量或默认路径
chrome_driver_path = CHROME_DRIVER_PATH
# 初始化Chrome浏览器驱动服务
service = Service(chrome_driver_path)

# 是否启用无头模式
if HEAD_LESS:
    # 创建无头模式参数.
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless=new')  # 启用无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if platform.system() == 'Linux':
        chrome_options.binary_location = "/opt/chrome-linux64/chrome"
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)  # 禁止加载图片
    # 创建无头模式Chrome浏览器实例
    driver = webdriver.Chrome(service=service, options=chrome_options)
else:
    # 创建正常模式Chrome浏览器实例
    driver = webdriver.Chrome(service=service)

# 预编译正则表达式，用于匹配购买和销售的相关信息
buy_name_pattern = re.compile('[\u4e00-\u9fff]+(?=的价格是)')
buy_price_pattern = re.compile(r"(?<=价格是)\d+")
buy_other_number_pattern = re.compile(r"(?<=剩余配货量为)\d+")

sale_name_pattern = re.compile(r"(?<=象岛新鲜蔬菜店 【)(.+)(?=\s市场单价)")
sale_price_pattern = re.compile(r"(?<=市场单价：)\d+")
sale_total_profit_pattern = re.compile(r"(?<=累计盈利 )\d+")
sale_current_number_pattern = re.compile(r"(?<=当前可卖数量为 )\d+")
sale_cost_pattern = re.compile(r"(?<=成本：)\d+")


def initialize_browser():
    """
    初始化浏览器，打开目标网址并最大化窗口
    """
    try:
        global driver
        driver.get(WEBSITE_URL)
        WebDriverWait(driver, WAIT_TIMEOUT).until(ec.presence_of_element_located((By.XPATH, '//body')))
        driver.maximize_window()
        if not HEAD_LESS:
            logger.warning("非无头模式，如果没有登录，将有30秒时间进行登录！")
            time.sleep(30)
        else:
            logger.warning(
                "无头模式，如果无法采集数据，请关闭无头模式使用正常模式登录一次！\n"
                "这将重写cookie内容，以便能正常登录。修改config.py文件中的HEAD_LESS参数即可。")

    except Exception as e:
        logger.error(f"Error occurred while opening the website: {e}")


def get_cookies_save_to_file():
    """
    打印当前浏览器会话的所有Cookies
    """
    try:
        cookies = driver.get_cookies()
        logger.info(cookies)

        with open('config_ptvicomo_04.py', 'r', encoding='utf-8') as file:
            content = file.read()

        cookie_var_name = 'WEB_COOKIE'
        pattern = re.compile(fr"(?<={cookie_var_name} = )([^]]+)(?=])")
        math = re.findall(pattern, content)
        old_cookies = f"{cookie_var_name} = {math[0]}]"
        # print(f"正则匹配的结果是：{old_cookies}")

        new_cookies = f"{cookie_var_name} = {cookies}"
        if cookie_var_name in content:
            logger.info(f"{cookie_var_name}变量已存在，进行替换操作")
            content = content.replace(old_cookies, new_cookies)
        else:
            logger.info(f"{cookie_var_name}变量不存在，进行添加操作")
            content += f"\n{cookie_var_name} = {cookies}"

        with open('config_ptvicomo_04.py', 'w', encoding='utf-8') as file:
            file.write(content)
            logger.info("config_ptvicomo_04.py文件已更新")

    except NoSuchElementException as e:
        logger.error(f"NoSuchElementException: {e}")


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


def save_page(day_of_week):
    """
    保存网页源码到文件
    """
    try:
        page_source = driver.page_source
        # logger.info(page_source)
        with open('象岛_' + day_of_week + '.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
            logger.info("网页源码已保存到【象岛_" + day_of_week + ".html】文件")
    except Exception as e:
        logger.error(f"Error occurred while saving the page source: {e}")


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
        logger.info(f'sale_action函数,当前卖出数量{number}')
        sell_input_num = driver.find_element(By.XPATH, '//input[@name="saleTurnipNum"]')
        if not sell_input_num.get_attribute('disabled'):
            sell_input_num.send_keys(number)
            logger.info(f"输入卖出数量成功,卖出数量为{number}")
        else:
            logger.error("卖出数量输入框处于禁用状态")

        sell_bottom = driver.find_element(By.XPATH, '//input[@value="出售"]')
        if not sell_bottom.get_attribute('disabled'):
            sell_bottom.click()
            logger.info(f"点击出售按钮成功,出售数量为{number}")
            sale_profit = sale_price * number
            return sale_profit
        else:
            logger.error("出售按钮处于禁用状态")

        # # 下面这段代码其实没有运行，因为一点击上面的出售按钮，就相当于卖出了所有的库存，就会让下面的2个元素被禁用。
        # if not sell_input_num.get_attribute('disabled') and not sell_bottom.get_attribute('disabled'):
        #     # 计算单笔盈利
        #     sale_profit = (sale_price - sale_cost) * number
        #     logger.info(f'sale_action函数,计算【单笔盈利】成功：{sale_profit}')
        #     sale_action_name = CURRENT_ACTION['sale']
        #     logger.info(f'sale_action函数,获取【当前操作】成功：{sale_action_name}')
        #     return sale_profit
        # else:
        #     # logger.error("卖出数量输入框或出售按钮处于禁用状态,无法卖出！测试数据")  # todo 测试数据,完成后return 0
        #     # # 计算单笔盈利
        #     # sale_profit = (sale_price - sale_cost) * number
        #     return 0

    except Exception as e:
        logger.error(f"卖出失败: {e}")


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


def get_hours_until_next_sunday():
    """
    计算距离下周星期天的剩余小时数
    :return: 距离下周星期天剩余的小时数
    """
    now = datetime.datetime.now()
    next_sunday = now + datetime.timedelta(days=(6 - now.weekday()) % 7)
    next_sunday = next_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
    remaining = int((next_sunday - now).total_seconds() / 3600)
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
    :return: 蔬菜名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数, 剩余配货量, 买卖数量
    """
    try:
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

        # 获取累计盈利,在这里无法获取。因为传过来的text只包括星期天的购买这一栏（第6栏）的数据，并不包括（第7栏）的数据
        # logger.info(text)
        # sale_total_profit = sale_total_profit_pattern.search(text).group()
        # sale_total_profit = int(sale_total_profit)
        # logger.info(f'获取【累计盈利】成功：{sale_total_profit}')

        # 购买动作
        buy_total_money = 0
        buy_action_name = CURRENT_ACTION['get_data']
        if buy_other_number > 0:
            if buy_other_number > BUY_NUMBER:
                # 计算总购买金额
                logger.info(f'当前购买数量{BUY_NUMBER}')
                buy_total_money = buy_action(BUY_NUMBER, buy_price)
                logger.info(f'购买成功，购买总金额为{buy_total_money}')
                buy_action_name = CURRENT_ACTION['buy']
            else:
                logger.info(f'当前购买数量{buy_other_number}')
                buy_total_money = buy_action(buy_other_number, buy_price)
                logger.info(f'购买成功，购买总金额为{buy_total_money}')
                buy_action_name = CURRENT_ACTION['buy']
        else:
            # 获取买卖数量
            logger.warning(
                f'因为【剩余配货量】为:{buy_other_number},无法进行买入操作!即使当前【买入数量】指令为:{BUY_NUMBER}')
            # 返回：名称, 市场单价, 累计盈利, 当前可卖数量, 成本,
            # 单笔盈利, 当前操作, 当前时间, 当前周数, 买卖数量

        logger.info(f'获取【当前操作】成功：{buy_action_name}')
        return (buy_name, buy_price, 0, 0, buy_price,
                buy_total_money, buy_action_name, current_time, week_number, buy_other_number, BUY_NUMBER)
    except Exception as e:
        logger.error(f"获取数据失败: {e}")


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

        # 重置常量, 测试用
        # sale_current_number = 150
        # logger.warning(f'重置【当前可卖数量】成功：{sale_current_number}')
        # sale_price = 3000
        # logger.warning(f'重置【市场单价】成功：{sale_price}')
        # hours_until_next_sunday = 10
        # logger.info(f'重置【距离下个星期日还有多少小时】成功：{hours_until_next_sunday}')

        # 获取成本
        sale_cost = sale_cost_pattern.search(text).group()
        sale_cost = int(sale_cost)
        logger.info(f'获取【成本】成功：{sale_cost}')

        # 计算当前利润率
        # 这里要考虑如果周未没有购买蔬菜的情况
        if sale_cost == 0:
            profit_margin = 0
            logger.info(f'本周没有购买蔬菜，【利润率】为【0】')
        else:
            profit_margin = round((sale_price / sale_cost - 1) * 100, 2)
            logger.info(f'获取【利润率】成功：{profit_margin}%')

        # 出售动作
        sale_profit = 0
        sale_action_name = CURRENT_ACTION['get_data']
        remaining_stock = 0

        # 获取当前离周日0点还有多少小时
        hours_until_next_sunday = get_hours_until_next_sunday()
        logger.info(f'获取【距离下个星期日还有多少小时】成功:{hours_until_next_sunday}')

        # 设置买卖数量
        num_sale_and_buy = 0

        if sale_current_number > 0:
            # 如果距离星期天还不到12个小时,或者,当前利润超过10%,清仓
            if is_sale_condition_met(hours_until_next_sunday, profit_margin, sale_current_number):
                sale_profit = sale_action(sale_current_number, sale_price, sale_cost)
                sale_action_name = CURRENT_ACTION['sale']
                num_sale_and_buy = sale_current_number
                logger.info(f'获取【买卖数量】成功：{sale_current_number}')
            elif sale_current_number >= SALE_NUMBER > 0:
                sale_profit = sale_action(SALE_NUMBER, sale_price, sale_cost)
                sale_action_name = CURRENT_ACTION['sale']
                num_sale_and_buy = SALE_NUMBER
                logger.info(f'获取【买卖数量】成功：{SALE_NUMBER}')

        logger.info(f'获取【当前操作】成功：{sale_action_name}')
        if sale_action_name != '提取数据':
            logger.info(f'计算【单笔盈利】成功：{sale_profit}')
        # :return: 蔬菜名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数, 剩余配货量, 买卖数量
        return build_return_value(sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                                  sale_profit, sale_action_name, current_time, week_number, remaining_stock,
                                  num_sale_and_buy)
    except Exception as e:
        logger.error(f'函数执行过程中发生异常,获取数据失败:{e}')
        return None


def is_sale_condition_met(hours_until_next_sunday, profit_margin, sale_current_number):
    """
    判断是否满足销售条件。
    :return: True/False
    """
    try:
        # 检查是否离下个周日不足12小时或利润空间超过指定值
        if hours_until_next_sunday < 12 or profit_margin > PROFIT_MARGIN:
            logger.info(
                f'距离下个星期日还有{hours_until_next_sunday}小时,或者 利润空间超过{profit_margin}%,满足销售条件,清仓!')
            return True
        if sale_current_number < SALE_NUMBER > 0:
            logger.warning(f'当前可卖数量小于指定卖出数量:{SALE_NUMBER},将全部卖出')
            return True

    except Exception as e:
        logger.error(f"判断销售条件时发生异常：{e}")
    return False


def build_return_value(sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                       sale_profit, sale_action_name, current_time, week_number, remaining_stock,
                       num_sale_and_buy):
    """
    构建返回值。
    :param sale_name:名称
    :param sale_price:市场单价
    :param sale_total_profit:累计盈利
    :param sale_current_number:当前可卖数量
    :param sale_cost:成本
    :param sale_profit:单笔盈利
    :param sale_action_name:当前操作
    :param current_time:当前时间
    :param week_number:当前周数
    :param remaining_stock:剩余配货量
    :param num_sale_and_buy:买卖数量
    :return:名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数, 剩余配货量, 买卖数量
    """
    return (sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
            sale_profit, sale_action_name, current_time, week_number, remaining_stock,
            num_sale_and_buy)


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
    # 获取当天是星期几
    day_of_week = get_day_of_week('chinese')
    logger.info(f'获取【星期几】成功:{day_of_week}')
    # 获取当前时间
    current_time = get_current_time()
    logger.info(f'获取【当前时间】成功:{current_time}')
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
            # logger.info(sunday_text)
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
    try:
        with conn.cursor() as cursor:
            logger.info(f'查询数据开始')
            cursor.execute(f'select * from {TABLE_NAME}')
            db_result = cursor.fetchall()
            for row in db_result:
                row_data = list(row)
                logger.info(f'{row_data}')
    except Exception as e:
        logger.error(f'查询数据失败:{e}')


def insert_data_to_mysql(conn, data_tuple):
    """
    向MySQL数据库插入数据。

    参数:
    - conn: 数据库连接对象。
    - data_tuple: 包含要插入的数据的元组。
    """
    try:
        insert_data_query = (
            f"INSERT INTO {TABLE_NAME} (名称,市场单价,累计盈利,当前可卖数量,成本,本周盈利,当前操作,当前时间,当前周数,剩余配货量,买卖数量) "
            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s)")
        with conn.cursor() as cursor:
            logger.info(data_tuple)
            cursor.execute(insert_data_query, data_tuple)
            conn.commit()
            logger.info("数据插入成功！")
            logger.info('-' * 30)
    except Error as e:
        logger.error(f"数据插入失败: {e}")


def create_table(conn, table_name):
    """
    根据df的字段自动创建MySQL数据库表。
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT auto_increment PRIMARY KEY,
        名称 VARCHAR(255) NULL,
        市场单价 INT NULL,
        累计盈利 INT NULL,
        当前可卖数量 INT NULL,
        成本 INT NULL,
        本周盈利 INT NULL,
        当前操作 VARCHAR(255) NULL,
        当前时间 VARCHAR(255) NULL,
        当前周数 INT NULL,
        剩余配货量 INT NULL,
        买卖数量 INT NULL
    );
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
            conn.commit()
    except Error as e:
        logger.error(f"创建表失败: {e}")


def main():
    try:
        day_of_week = get_day_of_week('chinese')
        initialize_browser()
        if not HEAD_LESS:
            get_cookies_save_to_file()
        set_cookies(WEB_COOKIE)
        if SAVE_PAGE:
            save_page(day_of_week)

    except Exception as e:
        logger.error(f"初始化浏览器或设置Cookie失败: {e}")
        return

    # 这里应该有个判断cookie是否过期?如果过期,则使用帐号登录,重新获取cookie.
    # time.sleep(10)
    # get_cookies_save_to_file()

    try:
        with connect_to_mysql() as my_conn:
            if my_conn is None:
                logger.error("无法连接到数据库!")
                return

            create_table(my_conn, TABLE_NAME)

            data = get_data()
            if data is None:
                logger.error("无法获取数据!")
                return

            try:
                # query_from_mysql(my_conn)
                insert_data_to_mysql(my_conn, data)
            except Error as e:
                logger.error(f'插入数据失败: {e}')

    except Exception as e:
        logger.error(f'程序运行失败:{e}')
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    # for i in tqdm.tqdm(range(1, 100), desc='进度'):
    main()
