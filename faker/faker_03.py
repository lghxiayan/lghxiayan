from faker import Faker
from faker.providers import BaseProvider
import address_data


# 自定义的Provider类
class MyAddressProvider(BaseProvider):
    def my_address(self, district_code):
        # 获取对应的区域名称
        district_name = address_data.address_mapping.get(district_code)
        if district_name is None:
            raise ValueError(f"Invalid district code: {district_code}")

        # 这里你可以添加更详细的地址生成逻辑，比如街道、门牌号等
        # 为了示例，我们只返回区域名称
        street = fake.street_address()
        return f"{district_name}{street}"


# 创建Faker实例
fake = Faker('ZH-CN')

# 将自定义的Provider添加到Faker实例
fake.add_provider(MyAddressProvider)

# 使用自定义的方法生成特定区域的地址
district_code_to_generate = '421127'  # 指定要生成的区域代码，例如朝阳区
print(fake.my_address(district_code_to_generate))
