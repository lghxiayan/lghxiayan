from faker import Faker
from faker.providers import BaseProvider
import address_data


# 自定义的Provider类
class MyAddressProvider(BaseProvider):
    def my_address(self, district_code):
        """
        根据行政区域代码生成地址
        :param district_code: 行政区域代码，也就是身份证号码前6位
        :return:
        """
        # 输入验证
        if not isinstance(district_code, str) or len(district_code) != 6 or not district_code.isdigit():
            raise ValueError(f"无效的区域代码: {district_code}")
        # 获取对应的区域名称
        try:
            district_name = address_data.address_mapping.get(district_code)
            if district_name is None:
                raise ValueError(f"无效的区域代码: {district_code}")
            address_sheng = address_data.address_mapping.get(district_code[:2] + '0000', '未知地址')
            address_shi = address_data.address_mapping.get(district_code[:4] + '00', '未知地址')
            if district_code[2:4] == '00':
                address_shi = ''
            address_xiang = address_data.address_mapping.get(district_code, '未知地址')
            if district_code[4:6] == '00':
                address_shi = ''
            street = fake.street_address()
            return f"{address_sheng}{address_shi}{address_xiang}{street}"
        except KeyError:
            raise ValueError(f"无效的区域代码: {district_code}")


# 创建Faker实例
fake = Faker('ZH-CN')

# 将自定义的Provider添加到Faker实例
fake.add_provider(MyAddressProvider)

# 使用自定义的方法生成特定区域的地址
district_code_to_generate = '42117'  # 指定要生成的区域代码，例如朝阳区
print(fake.my_address(district_code_to_generate))
