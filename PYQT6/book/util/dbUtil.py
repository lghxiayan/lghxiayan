"""
数据库连接工具包
"""

import os
from mysql.connector import connect, Error
import logging.config
from config_book_01 import DB_CONFIG, TABLE_NAME

# 导入日志配置文件
# 先获取绝对路径,再拼接在一起,这样就不会报错
# 使用 __file__ 来构建配置文件的路径
config_file_path = os.path.join(os.path.dirname(__file__), 'logging_book.conf')
logging.config.fileConfig(config_file_path, encoding='utf-8')
logger = logging.getLogger('book_log')
logger.setLevel(logging.INFO)


def connect_to_mysql():
    """
    获取数据库连接
    :return:
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
            logger.info(f'查询数据开始！表名：{TABLE_NAME}')
            cursor.execute(f'select * from {TABLE_NAME}')
            db_result = cursor.fetchall()
            for row in db_result:
                row_data = list(row)
                logger.info(f'{row_data}')
            logger.info(f'查询数据结束！')
    except Exception as e:
        logger.error(f'查询数据失败:{e}')


def main():
    try:
        with connect_to_mysql() as my_conn:
            if my_conn is None:
                logger.error("无法连接到数据库!")
                return

            try:
                query_from_mysql(my_conn)
                # insert_data_to_mysql(my_conn, data)
            except Error as e:
                logger.error(f'插入数据失败: {e}')

    except Exception as e:
        logger.error(f'程序运行失败:{e}')


if __name__ == '__main__':
    main()
