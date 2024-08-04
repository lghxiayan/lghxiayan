"""
多线程生成假个人信息用于测试,并插入到MYSQL8中,带进度条,10万条数据耗时大约1分钟.
不使用多线程生成数据,速度非常慢.
我写了一个address_data.py文件，包含了中国行政区划信息，引用了进来，这个要注意。
"""
from concurrent.futures import ThreadPoolExecutor
from faker.providers import BaseProvider
from mysql import connector
from faker import Faker
from tqdm import tqdm
import random
import os
import logging
from datetime import datetime
import address_data

my_sex = ['男', '女']
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
logging.basicConfig(level=logging.INFO, format=FORMAT)  # We'll talk about this sonn!

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


def generate_data_parallel(n_records):
    with ThreadPoolExecutor(max_workers=8) as executor:
        # 使用 tqdm 包裹 range 对象，创建一个带进度条的迭代器
        results = list(tqdm(executor.map(generate_data, [None] * n_records), total=n_records))
    return results


def insert_data_into_db(data, conn):
    cursor = conn.cursor()
    query = (
        "INSERT INTO validator (name, id_card_number,  birthday,sex, age, phone_number,address,  area) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
    # 使用 tqdm 包裹数据列表，创建一个带进度条的迭代器
    for record in tqdm(data, desc="Inserting records"):
        cursor.execute(query, record)
    conn.commit()


def connect_to_MYSQL():
    try:
        conn = connector.connect(**DB_CONFIG)
        logging.info("Connected to MYSQL successfully!")
        return conn
    except connector.Error as error:
        logging.info(f"Failed to connect to MYSQL: {error}")
        return None


if __name__ == '__main__':
    my_conn = connect_to_MYSQL()
    if my_conn:
        n_records = 99000
        data = generate_data_parallel(n_records)
        insert_data_into_db(data, my_conn)
        my_conn.close()
