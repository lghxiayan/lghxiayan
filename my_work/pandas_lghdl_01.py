"""
读取龙感湖电力EXCEL数据,指定行.
然后进行行列互换
最后写入MYSQL中
"""

import pandas as pd
import logging.config
from mysql.connector import connect, Error
import mysql.connector.errorcode as errorcode
from config_lghdl import DB_CONFIG, REORDER_COL_NAMES, REPLACE_COL_NAMES, COL_NAMES, TABLE_NAME, TRUNCATE_TABLE, \
    DTYPE_MAPPING

# 导入日志配置文件
logging.config.fileConfig('logging_lghdl.conf', encoding='utf-8')
logger = logging.getLogger('lghdl_log')


def open_csv(file_, col_names_):
    try:
        df_ = pd.read_excel(file_, usecols=col_names_)
        logger.info(f'数据读取成功！{file_}')
        return df_
    except Exception as e:
        logger.error(f'数据读取失败！{file_}')
        logger.error(e)


def row_to_col(df_):
    melted_df = df_.melt(id_vars=['户名', '2023年1-6月累计用电量'], var_name='月份', value_name='用电量')
    logger.info('行列互换成功！')
    return melted_df


def df_to_excel(df_, file_):
    df_.to_excel(file_, index=False)
    logger.info('数据导出成功！')
    return None


def df_rename(df_, col_names_):
    df_.rename(columns=col_names_, inplace=True)
    logger.info('列名替换成功！')
    return df_


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


def query_from_mysql(conn, df_):
    """
    从MySQL数据库中查询所有数据。

    参数:
    - conn: 数据库连接对象。
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'select * from {TABLE_NAME}')
            db_result = cursor.fetchall()
            for row in db_result:
                row_data = list(row)
                logger.info(f'{row_data}')
    except Error as e:
        if e.errno == errorcode.ER_NO_SUCH_TABLE:
            logger.info(f'表 {TABLE_NAME} 不存在，正在创建...')
            create_table(conn, df_)
            return
        logger.error(f'查询数据失败: {e}')


def clear_table(conn, action):
    try:
        with conn.cursor() as cursor:
            if action == 'truncate':
                sql_query = f"TRUNCATE TABLE {TABLE_NAME}"
            elif action == 'drop':
                sql_query = f"DROP TABLE IF EXISTS {TABLE_NAME}"
            else:
                logger.warning(f'无效的操作类型: 【{action}】,什么也不干！')
                return None
            cursor.execute(sql_query)
            conn.commit()
            logger.info(f"表 {TABLE_NAME} 【{action}】 操作成功！")
    except Error as e:
        logger.error(f"表 {TABLE_NAME} 【{action}】操作失败: {e}")


def insert_data_to_mysql(conn, df_):
    """
    向MySQL数据库插入数据。

    参数:
    - conn: 数据库连接对象。
    - df: 包含要插入的数据的DataFrame。
    """

    # logger.info(df_)
    columns = df_.columns.tolist()
    columns_str = ', '.join(["`" + col + "`" for col in columns])
    placeholders = ', '.join(['%s'] * len(columns))
    insert_data_query = (
        f"INSERT INTO {TABLE_NAME} ({columns_str}) VALUES ({placeholders})")
    data_tuples = [tuple(row) for row in df_.itertuples(index=False)]
    # logger.info(f'{data_tuples}')
    # logger.info(insert_data_query)
    try:
        with conn.cursor() as cursor:
            cursor.executemany(insert_data_query, data_tuples)
            conn.commit()
            logger.info(f"批量插入 {len(data_tuples)} 条数据成功！")
    except Error as e:
        logger.error(f"插入数据失败: {e}")


def create_table(conn, df_):
    """
    根据df的字段自动创建MySQL数据库表。
    """
    columns = []
    for col_name, dtype in df_.dtypes.items():
        mysql_type = DTYPE_MAPPING.get(str(dtype), 'VARCHAR(255)')
        columns.append(f"`{col_name}` {mysql_type} NULL")

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT auto_increment PRIMARY KEY,
        {' ,'.join(columns)}
    );
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
            conn.commit()
            logger.info(f"表创建成功！{TABLE_NAME}")
    except Error as e:
        logger.error(f"创建表失败: {e}")


if __name__ == '__main__':
    df = open_csv('dl_2024.xlsx', COL_NAMES)
    # logger.info(df.sample(3))

    df = df_rename(df, REPLACE_COL_NAMES)
    # print(df.sample(3))

    df = df.reindex(columns=REORDER_COL_NAMES)
    df = df.dropna()

    df = row_to_col(df)
    logger.info(df.sample(3))

    # df_to_excel(df, 'dl_2024_new.xlsx')
    my_conn = connect_to_mysql()
    if my_conn:
        clear_table(my_conn, 'drop')  # truncate or drop
        query_from_mysql(my_conn, df)
        insert_data_to_mysql(my_conn, df)
