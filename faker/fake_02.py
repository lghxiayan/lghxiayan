def check_id_card(id_number):
    if len(id_number) != 18:
        return False

    coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    # 计算校验码
    sum = 0
    for i in range(17):
        sum += int(id_number[i]) * coefficients[i]
    mod = sum % 11

    # 检查校验位
    return check_codes[mod] == id_number[-1]


# 测试
id_number = "123456789012345678"  # 替换为需要检验的身份证号码
print(check_id_card(id_number))
