import os
# from datetime import datetime
import datetime

os.environ['PYTHONIOENCODING'] = 'utf-8'
#
# 给定的日期字符串
give_str = '2025-03-23 上午'

# 取给定字符串的日期，并转为datetime格式
give_str_date = datetime.datetime.strptime(give_str.split()[0], '%Y-%m-%d').date()
print("给定日期:", give_str_date)

# 取给定字符串后面的文字
give_str_time = give_str.split()[1]
print("给定时间标识:", give_str_time)

# 取当前日期
current_date = datetime.datetime.now().date()
print("当前日期:", current_date)
# 取当前时间
current_hour_minute_second = datetime.datetime.now().time()
print("当前时间:", type(current_hour_minute_second), current_hour_minute_second)

current_hour_minute_second_str = str(datetime.datetime.now().time())
print("当前时间:", type(current_hour_minute_second_str), current_hour_minute_second_str)

forenoon_start_time = datetime.time(0, 0, 0)
forenoon_end_time = datetime.time(11, 59, 59)
afternoon_start_time = datetime.time(12, 0, 0)
afternoon_end_time = datetime.time(23, 59, 59)

# 初始化结果变量
date_str = None

if '上午' in give_str:
    if give_str_date == current_date and (forenoon_start_time <= current_hour_minute_second <= forenoon_end_time):
        date_str = give_str.replace('上午', current_hour_minute_second_str)
    else:
        date_str = give_str.replace('上午', '11:11:11.000000')

elif '下午' in give_str:
    if give_str_date == current_date and (afternoon_start_time <= current_hour_minute_second <= afternoon_end_time):
        date_str = give_str.replace('下午', current_hour_minute_second_str)
    else:
        date_str = give_str.replace('下午', '22:22:22.000000')

print(date_str)
date_str = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

print("最终生成的时间:", date_str)
