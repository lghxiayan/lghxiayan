from id_validator import validator
from concurrent.futures import ThreadPoolExecutor, as_completed
from mysql.connector.pooling import MySQLConnectionPool
from mysql import connector
from faker import Faker
from tqdm import tqdm
import random
import os
import logging

my_string = ['芦柴湖办事处', '沙湖办事处', '洋湖办事处', '严家闸办事处', '春港办事处', '塞湖办事处', '青泥湖办事处']
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.112.13'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),  # 注意这里信息是在1panel中，点击【数据库】->【连接信息】里的信息，别搞错了。
    'password': os.getenv('DB_PASSWORD', 'Lghgs2019'),
    'database': os.getenv('DB_NAME', 'fake_data'),
    'charset': 'utf8mb3'
}
FORMAT = '%(asctime)s, %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)  # We'll talk about this sonn!

fake = Faker('zh_CN')

# 连接到MySQL
cnx = connector.connect(**DB_CONFIG)

# 动态设置max_allowed_packet
cnx.cmd_query("SET GLOBAL max_allowed_packet = 128*1024*1024;")


def get_sex(sex_code):
    return '男' if sex_code == 1 else '女'


def generate_data(_):
    name = fake.name()
    id_card_number = validator.fake_id()
    sex = get_sex(validator.get_info(id_card_number)['sex'])
    birthday = validator.get_info(id_card_number)['birthday_code']
    street_address = fake.street_address()
    address = validator.get_info(id_card_number)['address'] + street_address
    age = validator.get_info(id_card_number)['age']
    phone_number = fake.phone_number()
    area = random.choice(my_string)
    return name, id_card_number, sex, birthday, address, age, phone_number, area


def generate_data_parallel(n_records):
    # 创建数据库连接池
    pool = MySQLConnectionPool(pool_name="mypool", pool_size=8, **DB_CONFIG)
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(generate_data, _) for _ in range(n_records)]
        data = []
        for future in tqdm(as_completed(futures), total=n_records, desc="Generating data"):
            data.append(future.result())
    return data, pool


def insert_data_into_db(data, pool):
    conn = pool.get_connection()
    cursor = conn.cursor()
    try:
        if conn.is_connected():
            query = (
                "INSERT INTO validator_test (name, id_card_number, sex, birthday, address, age, phone_number, area) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
            # 批量插入数据
            cursor.executemany(query, data)
            conn.commit()
        else:
            raise Exception("Failed to connect to MariaDB")
    finally:
        cursor.close()
        pool.get_connection().close()


if __name__ == '__main__':
    n_records = 99900
    data, pool = generate_data_parallel(n_records)
    insert_data_into_db(data, pool)
