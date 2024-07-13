from id_validator import validator
from concurrent.futures import ThreadPoolExecutor
from mysql import connector
from faker import Faker
from tqdm import tqdm
import random
import os
import logging

my_string = ['芦柴湖办事处', '沙湖办事处', '洋湖办事处', '严家闸办事处', '春港办事处', '塞湖办事处', '青泥湖办事处']
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.112.12'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Lghgs2023#'),
    'database': os.getenv('DB_NAME', 'fake_data'),
    'charset': 'utf8mb4'
}
FORMAT = '%(asctime)s, %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)  # We'll talk about this sonn!

fake = Faker('zh_CN')


def generate_data(_):
    chinese_name = fake.name()
    id_card_number = validator.fake_id()
    # address = fake.address()
    area = random.choice(my_string)
    # return chinese_name, id_card_number, address, area
    return id_card_number, area


def generate_data_parallel(n_records):
    with ThreadPoolExecutor(max_workers=8) as executor:
        # 使用 tqdm 包裹 range 对象，创建一个带进度条的迭代器
        results = list(tqdm(executor.map(generate_data, [None] * n_records), total=n_records))
    return results


def insert_data_into_db(data, conn):
    cursor = conn.cursor()
    # query = "INSERT INTO people (chinese_name, id_card_number, address, area) VALUES (%s, %s, %s, %s)"
    query = "INSERT INTO validator (id_card_number,area) VALUES (%s,%s)"
    # 使用 tqdm 包裹数据列表，创建一个带进度条的迭代器
    for record in tqdm(data, desc="Inserting records"):
        cursor.execute(query, record)
    conn.commit()


def connect_to_mariadb():
    try:
        conn = connector.connect(**DB_CONFIG)
        logging.info("Connected to MariaDB successfully!")
        return conn
    except connector.Error as error:
        logging.info(f"Failed to connect to MariaDB: {error}")
        return None


if __name__ == '__main__':
    my_conn = connect_to_mariadb()
    if my_conn:
        n_records = 10000
        data = generate_data_parallel(n_records)
        insert_data_into_db(data, my_conn)
        my_conn.close()
