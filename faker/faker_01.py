from faker import Faker
import random

my_string = ['芦柴湖办事处', '沙湖办事处', '洋湖办事处', '严家闸办事处', '春港办事处', '塞湖办事处', '青泥湖办事处']


def custom_random_string(s):
    return random.choice(s)


# 创建一个Faker实例，指定locale为'zh_CN'，用于生成中国相关的数据
fake = Faker('zh_CN')

# 生成中国人名字
chinese_name = fake.name()

# 生成身份证号码
id_card_number = fake.ssn()
# 653000196807299156
"""
    归属地：新疆维吾尔自治区克孜勒苏柯尔克孜自治州
    省份：新疆维吾尔自治区
    城市：克孜勒苏柯尔克孜自治州
    区域：
    出生日：1968-07-29
    性别：男
    合法：是
"""

address = fake.address()
# 云南省颖县涪城韦街t座 723666

# 生成地址信息
# for _ in range(5):
#     address = fake.address()
#     value1 = fake.texts(nb_texts=1)
#     print(address, value1)

print(f"中国人名字: {chinese_name}")
print(f"身份证号码: {id_card_number}")
print(f"地址信息: {address}")
print(f"随机字符串: {custom_random_string(my_string)}")
