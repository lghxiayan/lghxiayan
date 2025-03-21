# -*- coding: utf-8 -*-

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


现在象岛首页增加了蔬菜的走势图，应该可以通过selenium来抓取。首页地址为：https://ptvicomo.net/index.php，通过它可以获取历史数据。
定义了一个get_history_data函数，先从首页提取数据。如果达到了条件，就转到买卖页面进行操作。
"""

import logging.config
import re
import datetime
import platform
import time
import os

# 导入Selenium相关模块，用于自动化浏览器操作
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
# 导入sqlalchemy 2.x 模块,用于数据库处理.跟1.x版本有很多不同.
from sqlalchemy import create_engine, Column, Integer, String, Sequence, inspect, and_, DDL
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.mysql import VARCHAR
# 导入配置文件常量
from config_ptvicomo_04 import CHROME_DRIVER_PATH, DB_CONFIG, WEB_COOKIE, WEBSITE_URL, WEBSITE_MAIN_URL, WAIT_TIMEOUT, \
    TABLE_NAME, DB_TYPE, \
    CURRENT_ACTION, SALE_NUMBER, BUY_NUMBER, PROFIT_MARGIN, SAVE_PAGE, HEAD_LESS

Base = declarative_base()
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 导入日志配置文件
logging.config.fileConfig('logging_ptvicomo.conf', encoding='utf-8')
logger = logging.getLogger('ptvicomo_log')
logger.setLevel(logging.INFO)


class BrowserManager:
    def __init__(self, head_less=HEAD_LESS):
        # 定义Chrome驱动程序路径，使用环境变量或默认路径
        self.chrome_driver_path = CHROME_DRIVER_PATH
        # 初始化Chrome浏览器驱动服务
        self.service = Service(self.chrome_driver_path)

        self.head_less = head_less
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        # 是否启用无头模式
        if self.head_less:
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
            return webdriver.Chrome(service=self.service, options=chrome_options)
        else:
            # 创建正常模式Chrome浏览器实例
            return webdriver.Chrome(service=self.service)

    def initialize_browser(self, web_url):
        """
        初始化浏览器，打开目标网址并最大化窗口
        """
        try:
            self.driver.get(web_url)
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(ec.presence_of_element_located((By.XPATH, '//body')))
            self.driver.maximize_window()
            if not self.head_less:
                logger.warning("非无头模式，如果没有登录，将有30秒时间进行登录！")
                time.sleep(30)
            else:
                logger.warning(
                    "无头模式，如果无法采集数据，请关闭无头模式使用正常模式登录一次！\n"
                    "这将重写cookie内容，以便能正常登录。修改config.py文件中的HEAD_LESS参数即可。")
        except Exception as e:
            logger.error(f"Error occurred while opening the website: {e}")

    def get_cookies_save_to_file(self):
        """
        打印当前浏览器会话的所有Cookies
        """
        try:
            cookies = self.driver.get_cookies()
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

    def set_cookies(self, cookies, url):
        """
        设置Cookies到浏览器会话
        :param url:
        :param cookies: 需要设置的Cookies列表
        """
        # global driver
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        # 再次访问网页，这时应该已经应用了Cookies
        self.driver.get(url)

    def save_page(self, day_of_week):
        """
        保存网页源码到文件
        """
        try:
            page_source = self.driver.page_source
            # logger.info(page_source)
            with open('象岛_' + day_of_week + '.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
                logger.info("网页源码已保存到【象岛_" + day_of_week + ".html】文件")
        except Exception as e:
            logger.error(f"Error occurred while saving the page source: {e}")

    def close_browser(self):
        try:
            self.driver.close()
        except Exception as e:
            logger.error(f"关闭浏览器窗口失败:{e}")
        finally:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"退出浏览器驱动失败: {e}")


class DataExtractor:
    def __init__(self, driver):
        self.driver = driver
        # 预编译正则表达式，用于主页面，匹配购买和销售的相关信息
        self.vegetable_name_pattern = re.compile(r"^(.+?)价格走势")
        self.vegetable_history_date_pattern = re.compile(r"labels:\s*\[(.*?)]")
        self.vegetable_history_price_pattern = re.compile(r"data:\s*\[(.*?)]")

        # 预编译正则表达式，用于交易页面，匹配购买和销售的相关信息
        self.buy_name_pattern = re.compile('[\u4e00-\u9fff]+(?=的价格是)')
        self.buy_price_pattern = re.compile(r"(?<=价格是)\d+")
        self.buy_other_number_pattern = re.compile(r"(?<=剩余配货量为)\d+")

        self.sale_name_pattern = re.compile(r"(?<=象岛新鲜蔬菜店 【)(.+)(?=\s市场单价)")
        self.sale_price_pattern = re.compile(r"(?<=市场单价：)\d+")
        self.sale_total_profit_pattern = re.compile(r"(?<=累计盈利 )\d+")
        self.sale_current_number_pattern = re.compile(r"(?<=当前可卖数量为 )\d+")
        self.sale_cost_pattern = re.compile(r"(?<=成本：)\d+")

    def extract_homepage_data(self):
        """
        提取主页面的数据
        :return:
        """
        try:
            logger.info("开始提取主页面数据...")
            homepage_data_title = self.driver.find_element(By.XPATH, "//h2[contains(text(), '价格走势')]").text
            vegetable_name = self.vegetable_name_pattern.findall(homepage_data_title)[0]
            logger.info(f'获取主页面蔬菜名称:{vegetable_name}')

            # 取蔬菜历史价格
            homepage_data_trend_script = self.driver.find_element(By.XPATH,
                                                                  "//div[@class='menuLeft']/script[1]").get_attribute(
                'innerHTML')

            vegetable_history_date = self.vegetable_history_date_pattern.findall(homepage_data_trend_script)[0]
            logger.info(f'{vegetable_history_date}')

            vegetable_history_price = self.vegetable_history_price_pattern.findall(homepage_data_trend_script)[0]
            logger.info(f'{vegetable_history_price}')

            current_week = self.get_current_week()
            converted_history_dates = self.convert_time_strings(vegetable_name, vegetable_history_date,
                                                                vegetable_history_price, current_week)
            return converted_history_dates
        except Exception as e:
            logger.error(f"提取主页面数据失败: {e}")
            return None

    @staticmethod
    def convert_time_strings(name_str: str, date_strs: str, price_strs: str, current_week: int) -> list:
        """
        将日期时间字符串转换为具体的日期时间格式。将'上午'替换为'11:11:11'，将'下午'替换为'22:22:22'
        :param name_str: 名称字符串
        :param date_strs: 日期字符串
        :param price_strs: 单价字符串
        :param current_week: 当前周数
        :return: 转换后的可运行SQL插入参数列表
        """
        # 对日期字符串进行分割，并替换里面的单引号
        date_list = [date.replace("'", "") for date in date_strs.split(', ')]
        # 对单价字符串进行分割，并转换成数字类型
        price_list = [int(price) for price in price_strs.split(', ')]
        history_data_list = []
        for date_str, price in zip(date_list, price_list):
            # 根据字符串中包含的时段信息替换时间部分
            if '上午' in date_str:
                date_str = date_str.replace('上午', '11:11:11')
                date_str = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            elif '下午' in date_str:
                date_str = date_str.replace('下午', '22:22:22')
                date_str = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            # 构造历史数据元组
            values = name_str, price, 0, 0, price, 0, '提取数据', date_str, current_week, 0, 0
            history_data_list.append(values)
        return history_data_list

    @staticmethod
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

    def sale_action(self, number, sale_price, sale_cost):
        """
        执行卖出操作
        :param number: 卖出的数量
        :param sale_price: 单价
        :param sale_cost: 成本
        :return: 单笔盈利
        """
        try:
            logger.info(f'sale_action函数,当前卖出数量{number}')
            sell_input_num = self.driver.find_element(By.XPATH, '//input[@name="saleTurnipNum"]')
            if not sell_input_num.get_attribute('disabled'):
                sell_input_num.send_keys(number)
                logger.info(f"输入卖出数量成功,卖出数量为{number}")
            else:
                logger.error("卖出数量输入框处于禁用状态")

            sell_bottom = self.driver.find_element(By.XPATH, '//input[@value="出售"]')
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
            #     # logger.error("卖出数量输入框或出售按钮处于禁用状态,无法卖出！测试数据")  # 测试数据,完成后return 0
            #     # # 计算单笔盈利
            #     # sale_profit = (sale_price - sale_cost) * number
            #     return 0

        except Exception as e:
            logger.error(f"卖出失败: {e}")

    def buy_action(self, number, buy_price):
        """
        执行买入操作
        :param number: 买入的数量
        :param buy_price: 单价
        :return: 总购买金额（负数表示购买花费）
        """
        try:
            self.driver.find_element(By.XPATH, '//input[@name="buyTurnipNum"]').send_keys(number)
            self.driver.find_element(By.XPATH, '//input[@value="进货"]').click()
            buy_total_money = -buy_price * number
            logger.info(f"点击购买按钮成功,购买数量为{number},购买单价{buy_price},购买总金额为{buy_total_money}")
            return buy_total_money
        except Exception as e:
            logger.error(f"点击购买按钮失败: {e}")

    @staticmethod
    def get_current_time() -> datetime:
        """
        获取当前日期和时间，格式为：年-月-日 时:分:秒,不要毫秒.
        :return: 当前日期和时间,不包括毫秒
        """
        current_time = datetime.datetime.now().replace(microsecond=0)
        return current_time

    @staticmethod
    def get_hours_until_next_sunday() -> int:
        """
        计算距离下周星期天的剩余小时数
        :return: 距离下周星期天剩余的小时数
        """
        now = datetime.datetime.now()
        next_sunday = now + datetime.timedelta(days=(6 - now.weekday()) % 7)
        next_sunday = next_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
        remaining = int((next_sunday - now).total_seconds() / 3600)
        return remaining

    @staticmethod
    def get_current_week():
        """
        获取当前是今年的第几周。
        计算周数，从周日开始计算。weekday() 方法返回的是星期几，星期一是0，星期日是6
        因此，如果今天是周日，则周数加1。如果今天是一年的第一天且是周日，则已经是第一周了
        :return: 当前周数
        """
        # 获取当前日期
        today = datetime.date.today()
        # 计算年份
        year = today.year

        if today.weekday() == 6:
            week_number = (today - datetime.date(year, 1, 1)).days // 7 + 1
        else:
            # 如果今天不是周日，找到最近的周日
            last_sunday = today - datetime.timedelta(days=today.weekday() + 1)
            # 计算周数
            week_number = (last_sunday - datetime.date(year, 1, 1)).days // 7 + 1
        return week_number

    def extract_data_from_sunday_text(self, text, current_time, week_number):
        """
        从星期天的页面文本中提取购买相关信息
        :param text: 星期天页面的文本内容
        :param current_time: 当前时间
        :param week_number: 当前周数
        :return: 蔬菜名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数, 剩余配货量, 买卖数量
        """
        try:
            # 获取名称
            buy_name = self.buy_name_pattern.findall(text)[0]
            logger.info(f'获取【蔬菜名称】成功:{buy_name}')
            # 获取市场单价
            buy_price = self.buy_price_pattern.findall(text)[0]
            buy_price = int(buy_price)
            logger.info(f'获取【市场单价】成功:{buy_price}')
            # 获取剩余配货量
            buy_other_number = self.buy_other_number_pattern.findall(text)[0]
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
                    buy_total_money = self.buy_action(BUY_NUMBER, buy_price)
                    logger.info(f'购买成功，购买总金额为{buy_total_money}')
                    buy_action_name = CURRENT_ACTION['buy']
                else:
                    logger.info(f'当前购买数量{buy_other_number}')
                    buy_total_money = self.buy_action(buy_other_number, buy_price)
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

    def extract_data_from_weekday_text(self, text, current_time, week_number):
        """
        从非星期天的页面文本中提取销售相关信息
        :param text: 非星期天页面的文本内容
        :param current_time: 当前时间
        :param week_number: 当前周数
        :return: 蔬菜名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数, 剩余配货量
        """
        try:
            # 获取名称
            sale_name = self.sale_name_pattern.findall(text)[0]
            logger.info(f'获取【名称】成功:{sale_name}')
            # 获取市场单价
            sale_price = self.sale_price_pattern.findall(text)[0]
            sale_price = int(sale_price)
            logger.info(f'获取【市场单价】成功:{sale_price}')
            # 获取累计盈利
            sale_total_profit = self.sale_total_profit_pattern.search(text).group()
            sale_total_profit = int(sale_total_profit)
            logger.info(f'获取【累计盈利】成功：{sale_total_profit}')
            # 获取当前可卖数量，即库存
            sale_current_number = self.sale_current_number_pattern.search(text).group()
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
            sale_cost = self.sale_cost_pattern.search(text).group()
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
            hours_until_next_sunday = self.get_hours_until_next_sunday()
            logger.info(f'获取【距离下个星期日还有多少小时】成功:{hours_until_next_sunday}')

            # 设置买卖数量
            num_sale_and_buy = 0

            if sale_current_number > 0:
                # 如果距离星期天还不到12个小时,或者,当前利润超过10%,清仓
                if self.is_sale_condition_met(hours_until_next_sunday, profit_margin, sale_current_number):
                    sale_profit = self.sale_action(sale_current_number, sale_price, sale_cost)
                    sale_action_name = CURRENT_ACTION['sale']
                    num_sale_and_buy = sale_current_number
                    logger.info(f'获取【买卖数量】成功：{sale_current_number}')
                elif sale_current_number >= SALE_NUMBER > 0:
                    sale_profit = self.sale_action(SALE_NUMBER, sale_price, sale_cost)
                    sale_action_name = CURRENT_ACTION['sale']
                    num_sale_and_buy = SALE_NUMBER
                    logger.info(f'获取【买卖数量】成功：{SALE_NUMBER}')

            logger.info(f'获取【当前操作】成功：{sale_action_name}')
            if sale_action_name != '提取数据':
                logger.info(f'计算【单笔盈利】成功：{sale_profit}')
            # :return: 蔬菜名称, 市场单价, 累计盈利, 当前可卖数量, 成本, 单笔盈利, 当前操作, 当前时间, 当前周数, 剩余配货量, 买卖数量
            return self.build_return_value(sale_name, sale_price, sale_total_profit, sale_current_number, sale_cost,
                                           sale_profit, sale_action_name, current_time, week_number, remaining_stock,
                                           num_sale_and_buy)
        except Exception as e:
            logger.error(f'函数执行过程中发生异常,获取数据失败:{e}')
            return None

    @staticmethod
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

    @staticmethod
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

    def get_trade_page_data(self):
        """
        从交易网页获取数据。
        返回:
        - 如果找到数据，则返回一个包含名称、价格和盈利的元组。
        - 如果找不到数据或出现异常，则返回None。
        """
        # 获取当天是星期几
        day_of_week = self.get_day_of_week('chinese')
        logger.info(f'获取【星期几】成功:{day_of_week}')
        # 获取当前时间
        current_time = self.get_current_time()
        logger.info(f'获取【当前时间】成功:{current_time}')
        # 获取当前周数
        week_number = self.get_current_week()
        logger.info(f'获取【当前周数】成功:{week_number}')
        try:
            # 尝试查找星期天的数据元素
            # 获取星期天详细数据
            sunday_element = self.driver.find_elements(By.XPATH, '//*[@id="buyTurnipSunday"]')
            # 如果找到，则处理并返回星期天的数据
            if sunday_element:
                sunday_text = sunday_element[0].text
                # logger.info(sunday_text)
                return self.extract_data_from_sunday_text(sunday_text, current_time, week_number)
            # 如果没找到星期天的数据，尝试查找工作日的数据元素
            else:
                weekday_element = self.driver.find_elements(By.XPATH, '//*[@id="saleTurnip"]')
                # 如果找到，则处理并返回工作日的数据
                if not weekday_element:
                    logger.warning("今天不是星期天,也找不到非星期天的相关数据")
                    return None
                weekday_text = weekday_element[0].text
                return self.extract_data_from_weekday_text(weekday_text, current_time, week_number)
        except NoSuchElementException:
            logger.error('找不到必要的元素')
        except Exception as e:
            logger.error(f'获取数据失败:{e}')
        return None


class DataRecord(Base):
    __tablename__ = TABLE_NAME

    id = Column(Integer, Sequence('data_record_seq'), primary_key=True, autoincrement=True)
    名称 = Column(String(255), nullable=True)  # 商品名称
    市场单价 = Column(Integer, nullable=True)  # 市场单价
    累计盈利 = Column(Integer, nullable=True)  # 累计盈利
    当前可卖数量 = Column(Integer, nullable=True)  # 当前可卖数量
    成本 = Column(Integer, nullable=True)  # 成本
    本周盈利 = Column(Integer, nullable=True)  # 本周盈利
    当前操作 = Column(String(255), nullable=True)  # 当前操作
    当前时间 = Column(String(255), nullable=True)  # 当前时间
    当前周数 = Column(Integer, nullable=True)  # 当前周数
    剩余配货量 = Column(Integer, nullable=True)  # 剩余配货量
    买卖数量 = Column(Integer, nullable=True)  # 买卖数量


class DatabaseManager:
    def __init__(self, db_type, db_config):
        self.db_type = db_type
        self.db_config = db_config
        self.engine = self._create_engine()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_engine(self):  # 新增公共方法，提供对外访问 engine 的接口
        return self.engine

    def _create_engine(self):
        if self.db_type == 'sqlite':
            sqlalchemy_database_url = f'sqlite:///{self.db_config["sqlite"]["database"]}'
            return create_engine(sqlalchemy_database_url, future=True)
        elif self.db_type == 'mysql':
            sqlalchemy_database_url = (
                f'mysql+pymysql://{self.db_config["mysql"]["user"]}:{self.db_config["mysql"]["password"]}'
                f'@{self.db_config["mysql"]["host"]}/{self.db_config["mysql"]["database"]}')
            return create_engine(sqlalchemy_database_url, future=True)
        else:
            logger.error("未知的数据库类型！")
            return None

    def create_db_table(self):
        try:
            inspector = inspect(self.engine)
            table_exists = inspector.has_table(TABLE_NAME)
            if not table_exists:
                Base.metadata.create_all(self.engine)
                logger.info(f"创建表 {TABLE_NAME} 成功！")
        except SQLAlchemyError as e:
            logger.error(f"创建表失败: {e}")

    def insert_data_to_db(self, data):
        """
        向数据库插入数据。
        参数:
        - conn: 数据库连接对象。
        - data: 要插入的数据。先要判断传入的是列表还是元组，如果是列表，就循环。元组则不处理。
        """
        # 校验输入数据类型
        if not isinstance(data, (list, tuple)):
            logger.error('数据类型不正确，需要列表或元组')
            return

        # 校验数据内容
        if isinstance(data, list):
            if not all(isinstance(item, tuple) and len(item) == 11 for item in data):
                logger.error("列表中的元素必须是长度为11的元组")
                return

        # 插入数据
        try:
            records_to_insert = []
            if isinstance(data, tuple):
                # 如果是元组，则直接插入
                record_time = data[7]
                if not self.check_record_exists_for_period(record_time):
                    records_to_insert.append(DataRecord(
                        名称=data[0],
                        市场单价=data[1],
                        累计盈利=data[2],
                        当前可卖数量=data[3],
                        成本=data[4],
                        本周盈利=data[5],
                        当前操作=data[6],
                        当前时间=data[7],
                        当前周数=data[8],
                        剩余配货量=data[9],
                        买卖数量=data[10]
                    ))
            elif isinstance(data, list):
                # 如果是列表，则逐条检查并插入
                for item in data:
                    record_time = item[7]
                    if not self.check_record_exists_for_period(record_time):
                        records_to_insert.append(DataRecord(
                            名称=item[0],
                            市场单价=item[1],
                            累计盈利=item[2],
                            当前可卖数量=item[3],
                            成本=item[4],
                            本周盈利=item[5],
                            当前操作=item[6],
                            当前时间=item[7],
                            当前周数=item[8],
                            剩余配货量=item[9],
                            买卖数量=item[10]
                        ))
            else:
                logger.error("数据类型不正确，需要元组或列表")
                return

            if records_to_insert:
                self.session.bulk_save_objects(records_to_insert)
                self.session.commit()
                logger.info(f"{len(records_to_insert)} 条数据插入成功！")
            else:
                logger.info(f"所有数据均已存在于数据库中，未插入新记录。")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"数据插入失败: {e},数据: {data}")

    def check_record_exists_for_period(self, record_time: datetime) -> bool:
        """
        检查特定时间点的数据是否已经存在于数据库中。
        :param record_time: 要检查的时间字符串，格式为 "YYYY-MM-DD HH:MM:SS"
        :return: 如果存在返回 True，否则返回 False
        """
        current_date = datetime.datetime.date(record_time)
        current_hour = record_time.hour

        period_start = datetime.datetime.strptime(f"{current_date} 00:00:00", "%Y-%m-%d %H:%M:%S")
        period_end = datetime.datetime.strptime(f"{current_date} 23:59:59", "%Y-%m-%d %H:%M:%S")
        if current_hour < 12:
            period_end = datetime.datetime.strptime(f"{current_date} 11:59:59", "%Y-%m-%d %H:%M:%S")
        else:
            period_start = datetime.datetime.strptime(f"{current_date} 12:00:00", "%Y-%m-%d %H:%M:%S")

        try:
            # query = self.session.query(DataRecord).filter(DataRecord.当前时间.between(period_start, period_end))
            query = self.session.query(DataRecord).filter(
                and_(DataRecord.当前时间 >= period_start, DataRecord.当前时间 <= period_end))
            return query.count() > 0
        except SQLAlchemyError as e:
            logger.error(f"检查记录时发生错误：{e}")
            return False

    def close_session(self):
        self.session.close()

    def alter_table_to_datetime(self, table_name):
        """
        将表结构中的字符串类型时间字段转换为DATETIME类型
        完整执行步骤：
        1. 检查原字段是否存在
        2. 重命名字段为临时字段
        3. 添加新DATETIME字段
        4. 转换旧数据到新字段
        5. 删除旧字段
        6. 重命名新字段
        :param table_name:
        :return:
        """

        inspector = inspect(self.engine)
        with self.engine.connect() as connection:
            with connection.begin():
                # 获取列详细信息（包含数据类型）
                columns = inspector.get_columns(table_name)
                time_column = next((col for col in columns if col['name'].lower() == '当前时间'), None)
                # 验证原始列是否存在
                if not time_column:
                    raise ValueError(f"列 '当前时间' 不存在于表 {table_name}['name']")
                # 获取数据库方言特定类型名称
                col_type = time_column['type']
                if not isinstance(col_type, (String, VARCHAR)):  # 兼容不同数据库类型
                    # logger.info(f"当前时间字段类型已经是 {type(col_type).__name__}，无需转换")
                    return
                # 使用方言特定的标识符转义
                quoted_table = connection.dialect.identifier_preparer.quote(table_name)
                # 修改 DDL 步骤定义
                steps = [
                    DDL(f'ALTER TABLE {quoted_table} RENAME COLUMN "当前时间" TO "当前时间_old"'),
                    DDL(f'ALTER TABLE {quoted_table} ADD COLUMN 当前时间_new DATETIME'),  # 直接写 SQL
                    DDL(f'UPDATE {quoted_table} SET "当前时间_new" = "当前时间_old"'),
                    DDL(f'ALTER TABLE {quoted_table} DROP COLUMN "当前时间_old"'),
                    DDL(f'ALTER TABLE {quoted_table} RENAME COLUMN "当前时间_new" TO "当前时间33"')
                ]
                try:
                    for step in steps:
                        connection.execute(step)
                    logger.info(f"表 {table_name} 的【当前时间】字段已修改为 datetime 类型")
                except Exception as e:
                    logger.error(f"数据库操作失败: {str(e)}")
                    raise RuntimeError(f"数据库操作失败:{str(e)}") from e


class Application:
    def __init__(self, url):
        self.url = url
        # 创建BrowserManager实例
        self.browser_manager = BrowserManager()
        self.data_extractor = DataExtractor(self.browser_manager.driver)
        self.database_manager = DatabaseManager(DB_TYPE, DB_CONFIG)

    def main(self):
        # 浏览器部分
        try:
            day_of_week = self.data_extractor.get_day_of_week('chinese')
            # 初始化页面
            self.browser_manager.initialize_browser(self.url)
            if not HEAD_LESS:
                self.browser_manager.get_cookies_save_to_file()
            self.browser_manager.set_cookies(WEB_COOKIE, self.url)
            if SAVE_PAGE:
                self.browser_manager.save_page(day_of_week)
        except Exception as e:
            logger.error(f"初始化浏览器或设置Cookie失败: {e}")
            return

        # 修改表结构
        try:
            self.database_manager.alter_table_to_datetime(TABLE_NAME)
        except SQLAlchemyError as e:
            logger.error(f"数据库操作失败: {e}")

        # 数据库写入操作
        try:
            data = None
            self.database_manager.create_db_table()
            # 这里要做个判断，因为各个页面的元素是不一样的
            if self.url == WEBSITE_URL:
                # 在提取交易页面的数据的时候,就进行了买卖的操作.
                data = self.data_extractor.get_trade_page_data()
            elif self.url == WEBSITE_MAIN_URL:
                data = self.data_extractor.extract_homepage_data()
            if data is None:
                logger.error("无法获取数据!")
                return

            self.database_manager.insert_data_to_db(data)

        except Exception as e:
            logger.error(f'程序运行失败:{e}')
        finally:
            self.browser_manager.close_browser()
            self.database_manager.close_session()


if __name__ == '__main__':
    # for i in tqdm.tqdm(range(1, 100), desc='进度'):
    import sys
    import os

    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")

    # 获取主页面历史数据
    app1 = Application(WEBSITE_MAIN_URL)
    app1.main()

    print('-' * 150)

    # 获取交易页面数据，并执行买卖操作
    app2 = Application(WEBSITE_URL)
    app2.main()
