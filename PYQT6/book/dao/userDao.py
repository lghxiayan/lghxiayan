"""
用户模块-数据访问对象
"""

import os
import sys

from PyQt6.lupdate import user

# 这里需要先将util子目录添加进搜索目录,因为dbUtil.py文件中调用了loggin_book.conf文件,而.conf文件是不在python的默认搜索目录中的,需要手工添加
# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前文件所在的目录的父目录
parent_dir = os.path.dirname(os.path.dirname(current_file_path))
# 构建父目录下的 util 子目录路径
util_dir = os.path.join(parent_dir, 'util')
# 将该目录添加进系统搜索目录
sys.path.append(util_dir)

from entity.UserModel import User
from util import dbUtil


def login(user: User):
    """
    用户登录判断
    :param user:用户实体
    :return:登录成功返回用户信息实体,失败则返回None
    """
    con = None
    try:
        con = dbUtil.connect_to_mysql()
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM t_user WHERE userName = '{user.userName} and password = '{user.password}")
        result = cursor.fetchone()
        print(result)
        return result
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    login('xiayan', 1234)
