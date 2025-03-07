config_file_path = 'config_ptvicomo_04.py'

new_config = {
    'SAVE_PAGE': True,
    'PRINT_PAGE': 10,
    'SAVE_PAGE_2': False,
    'WEBSITE_URL': 'https://ptvicomo.net/customgame.php',
    'LOGIN_USERNAME': 'ledor2024',
    'LOGIN_PASSWORD': "VvyNFQ*!Q]Bv5^'",
    'MY_LIST': [5, 6, 7, 8],
    'CURRENT_ACTION': {'buy': '买入', 'sale': '卖出', 'get_data': '提取数据'}
}

with open(config_file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# print(lines)

with open('new_config_ptvicomo_04.py', 'w', encoding='utf-8') as f:
    for line in lines:
        # print(line)
        for key, value in new_config.items():
            print(key, value)
            if f"{key} = " in line:
                print(f'{key}', type(key), type(value))
                if isinstance(value, str):
                    f.write(f'{key} = "{value}"\n')
                else:
                    f.write(f"{key} = {value}\n")
                break
        else:
            f.write(line)
