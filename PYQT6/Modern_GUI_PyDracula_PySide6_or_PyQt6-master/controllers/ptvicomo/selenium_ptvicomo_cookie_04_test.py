import datetime


def convert_time_strings(date_strs, price_list):
    """
    将日期时间字符串转换为具体的日期时间格式
    :param date_strs: 日期字符串列表
    :param price_list: 单价列表
    :return: 转换后的日期时间列表
    """
    datetime_list = []
    for date_str, price in zip(date_strs, price_list):
        if '上午' in date_str:
            date_str = date_str.replace('上午', '11:11:11')
            print(date_str, price)
        elif '下午' in date_str:
            date_str = date_str.replace('下午', '22:22:22')
            print(date_str, price)
        # datetime_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        datetime_list.append(date_str)
    return datetime_list


date_strs = "'2025-03-16 上午', '2025-03-16 下午', '2025-03-17 上午', '2025-03-17 下午'"
print(type(date_strs), date_strs)
price_strs = "2214, 2214, 2291, 2557"
print(type(price_strs), price_strs)

print('-' * 100)
date_list = [date.replace("'", "") for date in date_strs.split(', ')]
print(type(date_list), date_list)

price_list = [int(price) for price in price_strs.split(', ')]
print(type(price_list), price_list)

converted_dates = convert_time_strings(date_list, price_list)
print(converted_dates)
