import datetime

# 获取当前日期
today = datetime.date.today()

# 计算年份
year = today.year

# 计算周数，从周日开始计算
# weekday() 方法返回的是星期几，星期一是0，星期日是6
# 因此，如果今天是周日，则周数加1
# 如果今天是一年的第一天且是周日，则已经是第一周了
if today.weekday() == 6:
    week_number = (today - datetime.date(year, 1, 1)).days // 7 + 1
else:
    # 如果今天不是周日，找到最近的周日
    last_sunday = today - datetime.timedelta(days=today.weekday() + 1)
    # 计算周数
    week_number = (last_sunday - datetime.date(year, 1, 1)).days // 7 + 1

print(f"{week_number}")
