"""
龙感湖电力分析配置文件
"""
import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.112.13'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'lghdl'),
    'password': os.getenv('DB_PASSWORD', 'yZJsKpATCNFi4xiX'),
    'database': os.getenv('DB_NAME', 'lghdl'),
    'charset': 'utf8mb4'
}
COL_NAMES = ['户名', '1月份合计用电量（万kWh）', '2月份合计用电量（万kWh）', '3月份合计用电量（万kWh）',
             '4月份合计用电量（万kWh）', '5月份合计用电量（万kWh）', '6月份合计用电量（万kWh）', '2023年1-6月累计用电量']

REORDER_COL_NAMES = ['户名', '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2023年1-6月累计用电量']

REPLACE_COL_NAMES = {'1月份合计用电量（万kWh）': '2024-01', '2月份合计用电量（万kWh）': '2024-02',
                     '3月份合计用电量（万kWh）': '2024-03', '4月份合计用电量（万kWh）': '2024-04',
                     '5月份合计用电量（万kWh）': '2024-05', '6月份合计用电量（万kWh）': '2024-06',
                     '2023年1-6月累计用电量': '2023年1-6月累计用电量'}

TABLE_NAME = 'lghdl_2024'
# 是否清空表
TRUNCATE_TABLE = True

DTYPE_MAPPING = {
    'int64': 'INT',
    'float64': 'FLOAT',
    'object': 'VARCHAR(255)',  # 对于字符串类型，你可以根据实际需求调整长度
    'datetime64[ns]': 'DATETIME',
    # 添加更多数据类型映射，如果需要的话
}

# 定义的SQL插入语句
SQL_INSERT_DATA = "INSERT INTO hgsw_czry (czry_dm, czry_mc, dldm, xybz,swjg_dm,swjg_mc) VALUES (%s, %s, %s, %s,%s,%s)"
