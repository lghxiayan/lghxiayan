import os
import sqlite3

os.environ['PYTHONIOENCODING'] = 'utf-8'

conn = sqlite3.connect('example.db')

# 创建一个 Cursor 游标对象
cursor = conn.cursor()
# 使用游标对象执行 SQL 语句
# 创建一个表
cursor.execute('''
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY,
    name text NOT NULL,
    age integer NOT NULL,
    address char(50),
    salary real
)
''')

# 提交事务
conn.commit()

# 关闭游标
cursor.close()
