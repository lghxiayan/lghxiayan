"""
龙感湖人员信息表单录入
"""
import os
import random

from pywebio.input import input_group, input, TEXT, radio
from pywebio.output import put_text, put_markdown, put_html
import logging.config
from datetime import datetime
import address_data
from faker import Faker
from mysql.connector import connect, Error

TABLE_NAME = 'validator_test'

my_string = ['芦柴湖办事处', '沙湖办事处', '洋湖办事处', '严家闸办事处', '春港办事处', '塞湖办事处', '青泥湖办事处']
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.112.13'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Lghgs2019'),
    'database': os.getenv('DB_NAME', 'fake_data'),
    'charset': 'utf8mb4'
}

FORMAT = '%(asctime)s, %(message)s'
# 导入日志配置文件
logging.config.fileConfig('logging_lgh_info.conf', encoding='utf-8')
logger = logging.getLogger('lgh_info_log')

fake = Faker('zh_CN')


def calculate_age(birth_year, birth_month, birth_day):
    today = datetime.today()
    age = today.year - birth_year
    if (today.month, today.day) < (birth_month, birth_day):
        age -= 1
    return age


def get_address_from_id_card(id_card_number):
    logging.debug(id_card_number)
    address_code = id_card_number[:6]
    address_sheng = address_data.address_mapping.get(address_code[:2] + '0000', '未知地址')
    address_shi = address_data.address_mapping.get(address_code[:4] + '00', '未知地址')
    if address_code[2:4] == '00':
        address_shi = ''
    address_xiang = address_data.address_mapping.get(address_code, '未知地址')
    if address_code[4:6] == '00':
        address_shi = ''
    address_street = fake.street_address()
    address = address_sheng + address_shi + address_xiang + address_street
    logging.debug(address)
    return address


def generate_data(_):
    name = fake.name()
    id_card_number = fake.ssn()
    phone_number = fake.phone_number()
    # 获取生日
    birth_year = int(id_card_number[6:10])
    birth_month = int(id_card_number[10:12])
    birth_day = int(id_card_number[12:14])
    birthday = f'{birth_year}-{birth_month}-{birth_day}'
    # 获取性别
    gender_sex = int(id_card_number[16])
    sex = '男' if gender_sex % 2 == 0 else '女'
    # 获取年龄
    age = calculate_age(birth_year, birth_month, birth_day)
    # address = fake.address()
    address = get_address_from_id_card(id_card_number)
    area = random.choice(my_string)
    return name, id_card_number, birthday, sex, age, phone_number, address, area


def read_info_from_mysql():
    # 直接从配置文件中读取参数

    pass


def read_info_from_web():
    # todo 这里涉及到实时通信功能,但pywebio 不支持,所以还是得搞flask或django等.先放放吧.
    # info_dict = read_info_from_mysql()
    put_html("""
        <script>
        document.getElementByName('id_card_number').addEventListener('input', function() {
            var idCard = this.value;
            fetch('/check_id_card', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ idCard: idCard })
            }).then(response => response.json())
               .then(data => {
                   // 根据data的值更新界面，例如显示提示信息
                   document.getElementById('idCardCheckResult').innerText = data.message;
               });
        });
        </script>
        <div>
            <input type="text" name="id_card_number">
            <div id="idCardCheckResult"></div>
        </div>
        """)

    # 使用配置文件中的值作为表单的默认值
    inputs = input_group("龙感湖人员信息录入", [
        input(label='姓名', name='name', type=TEXT, value='刘冬梅', placeholder='请输入姓名', validate=None),
        input(label='身份证号码', name='id_card_number', type=TEXT, value='370200196505289543',
              placeholder='请输入身份证号码', validate=None),
        input(label='出生日期', name='birthday', type=TEXT, value=None, placeholder='获取出生日期', readonly=True),
        input(label='性别', name='sex', type=TEXT, value=None, placeholder='获取性别', readonly=True),
        input(label='年龄', name='age', type=TEXT, value=None, placeholder='获取年龄', readonly=True),
        input(label='手机号码', name='phone_number', type=TEXT, value=None, placeholder='请输入手机号码',
              validate=None),
        input(label='住址', name='address', type=TEXT, value=None, placeholder='请输入住址'),
        # input(label='办事处', name='area', type=TEXT, value=None, placeholder='请输入所属办事处'),
        radio(label='选择办事处', name='radio_area',
              options=['芦柴湖办事处', '沙湖办事处', '洋湖办事处', '严家闸办事处', '春港办事处', '塞湖办事处',
                       '青泥湖办事处'], value='严家闸办事处'),
        # textarea(label='备注', name='remark', placeholder='请输入备注', value='测试测试'),
        # file_upload(label='上传身份证照片', name='id_card_photo', accept='image/*', multiple=False,
        #             placeholder='请上传身份证照片')
    ])

    # 输出确认信息
    put_text("配置已收集，以下是您输入的参数：")
    put_markdown(f"""
    - 姓名: {inputs['name']}
    - 身份证号码: {inputs['id_card_number']}
    - 出生日期: {inputs['birthday']}
    - 性别: {inputs['sex']}
    - 年龄: {inputs['age']}
    - 手机号码: {inputs['phone_number']}
    - 住址: {inputs['address']}
    - 办事处: {inputs['radio_area']}
    """)
    logger.info(f'输入信息:{inputs}')
    return inputs


def query_from_mysql(conn, id_card_number):
    """
    从MySQL数据库中查询所有数据。

    参数:
    - conn: 数据库连接对象。
    """
    try:
        with conn.cursor() as cursor:
            logger.info(f'查询数据开始')
            cursor.execute(f'select * from {TABLE_NAME} where id_card_number = "{id_card_number}"')
            db_result = cursor.fetchall()
            for row in db_result:
                row_data = list(row)
                logger.info(f'{row_data}')
                return row_data
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
            cursor.execute(insert_data_query, data_tuple)
            conn.commit()
            logger.info("数据插入成功！")
            logger.info('-' * 30)
    except Error as e:
        logger.error(f"数据插入失败: {e}")


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


def main():
    inputs = read_info_from_web()
    id_card_number = inputs['id_card_number']

    try:
        with connect_to_mysql() as my_conn:
            if my_conn is None:
                logger.error("无法连接到数据库!")
                return

                # 查询当前录入的身份证号码信息是否存在
                # if 身份证号码存在:
                # 则读取信息到表单
                # else:
                # 保存表单信息
                # 调用数据库插入

            data = query_from_mysql(my_conn, id_card_number)
            logger.info(f'查询结果:{data}')
            if data is None:
                logger.error("无法获取数据!")
                return

            # try:
            #     insert_data_to_mysql(my_conn, data)
            # except Error as e:
            #     logger.error(f'插入数据失败: {e}')

    except Exception as e:
        logger.error(f'程序运行失败:{e}')


if __name__ == '__main__':
    main()
